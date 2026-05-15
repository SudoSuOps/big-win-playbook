#!/usr/bin/env python3
"""
dmack.ai cook · pre-flight base-model verification.

Per SR Hack repair list (sr_hack_signoff_v1.md Repair 3):
  Compute SHA256 of every .safetensors shard in the local base directory
  and verify against the published HuggingFace manifest. Block the cook if
  any shard mismatches the published release.

This catches the SwarmPharma-style "wrong base loaded" risk that the prior
SR review (SENIOR_HACK_BASE_MODEL_REVIEW Risk 4) called out, carried
forward to the new Qwen3.5-9B-Instruct base.

Exits 0 on success (cook may proceed). Exits 1 on any mismatch (cook MUST NOT
proceed). Exits 2 on inability to verify (e.g. cannot reach HF API — manual
intervention required).

Usage:
  python3 training/preflight_verify_base.py
  python3 training/preflight_verify_base.py --base /home/smash/models/qwen3.5-9b-base
  python3 training/preflight_verify_base.py --hf-repo Qwen/Qwen3.5-9B
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

DEFAULT_BASE = "/home/smash/models/qwen3.5-9b-base"
DEFAULT_HF_REPO = "Qwen/Qwen3.5-9B"  # adjust to -Instruct if/when gated access available


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_hf_manifest(repo: str) -> dict[str, str]:
    """
    Fetch SHA256 manifest for safetensors shards from HF API.
    Returns {filename: sha256_hex}. Raises on inability to verify.
    """
    api_url = f"https://huggingface.co/api/models/{repo}/tree/main"
    req = urllib.request.Request(api_url, headers={"Accept": "application/json"})
    data = json.loads(urllib.request.urlopen(req, timeout=30).read())

    manifest: dict[str, str] = {}
    for entry in data:
        if entry.get("type") != "file":
            continue
        path = entry.get("path", "")
        if not path.endswith(".safetensors"):
            continue
        # HF API returns lfs.sha256 for tracked files
        lfs = entry.get("lfs", {})
        sha = lfs.get("sha256") or lfs.get("oid")
        if sha:
            manifest[path] = sha.lower()
    if not manifest:
        raise RuntimeError(f"no safetensors shards in HF manifest for {repo}")
    return manifest


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--base", default=DEFAULT_BASE,
                   help="Local base-model directory")
    p.add_argument("--hf-repo", default=DEFAULT_HF_REPO,
                   help="HuggingFace repo for the canonical manifest (default: Qwen/Qwen3.5-9B)")
    p.add_argument("--allow-unverified", action="store_true",
                   help="Skip HF check if API unreachable (still prints local hashes for manual audit)")
    args = p.parse_args()

    base = Path(args.base)
    if not base.exists():
        print(f"FAIL · base directory missing: {base}")
        return 1

    print(f"=== pre-flight base verify ===")
    print(f"  local base: {base}")
    print(f"  HF repo:    {args.hf_repo}")
    print()

    # Local
    shards = sorted(base.glob("*.safetensors"))
    if not shards:
        print(f"FAIL · no .safetensors shards in {base}")
        return 1
    print(f"=== local shards ({len(shards)}) ===")
    local: dict[str, str] = {}
    for s in shards:
        h = sha256_file(s)
        local[s.name] = h
        print(f"  {s.name}  {h[:16]}...  ({s.stat().st_size / 1e9:.2f} GB)")
    print()

    # Remote
    try:
        manifest = fetch_hf_manifest(args.hf_repo)
    except Exception as e:
        print(f"WARN · could not fetch HF manifest: {e}")
        if args.allow_unverified:
            print("  --allow-unverified set; printing hashes only for manual audit")
            return 2
        print("FAIL · without HF verification, the cook cannot proceed (per SR Repair 3)")
        return 2

    print(f"=== HF manifest ({len(manifest)} shards from {args.hf_repo}) ===")
    for name, sha in sorted(manifest.items()):
        print(f"  {name}  {sha[:16]}...")
    print()

    # Compare
    print("=== verification ===")
    mismatches: list[tuple[str, str, str]] = []
    missing_remote: list[str] = []
    for name, local_hash in local.items():
        remote_hash = manifest.get(name)
        if remote_hash is None:
            missing_remote.append(name)
            continue
        if local_hash != remote_hash:
            mismatches.append((name, local_hash, remote_hash))
            print(f"  MISMATCH · {name}")
            print(f"      local:  {local_hash}")
            print(f"      remote: {remote_hash}")
        else:
            print(f"  OK · {name}")

    print()
    if mismatches:
        print(f"FAIL · {len(mismatches)} shard(s) hash-mismatched against {args.hf_repo}")
        print("       Cook MUST NOT proceed. The local base is not the published release.")
        return 1
    if missing_remote:
        print(f"WARN · {len(missing_remote)} local shard(s) not in HF manifest:")
        for n in missing_remote:
            print(f"       {n}")
        print("       Manual review required.")
        return 2

    print(f"PASS · all {len(local)} shards match the published {args.hf_repo} manifest")
    print(f"       Cook is cleared to proceed (Repair 3 satisfied).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
