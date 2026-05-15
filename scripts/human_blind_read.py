#!/usr/bin/env python3
"""
Human blind-read pack generator (MD Aug 2 · sr_md_signoff_v1.md §5).

Curator-9B (Judge A) and base-9b (Judge B) both have slight pro-cooked bias:
A from corpus-selection coupling, B from Qwen-family self-preference. Human
read-through is the only structurally independent judge available pre-deploy.

Produces 20 random side-by-side cooked-vs-base diffs from the gate run,
randomized left-vs-right (truly blind), weighted toward safety-critical.
Donovan or delegated SR-MD reads each pair, picks left/right/tie, reasons
in 1 line.

Verdict rule:
  - human picks cooked ≥14/20 with ≤2 losses → CONFIRM gate verdict
  - human can't tell apart (10±2 ties) → MARGINAL, regardless of LLM verdict

Usage:
  python3 eval/human_blind_read.py
  python3 eval/human_blind_read.py --n 20 --seed 42
"""
from __future__ import annotations
import argparse
import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE_RUN = ROOT / "eval/runs/base.jsonl"
DEFAULT_COOKED_RUN = ROOT / "eval/runs/cooked.jsonl"
DEFAULT_OUT = ROOT / "eval/runs/human_blind_read.md"
DEFAULT_EVAL_SET = ROOT / "eval/dmack_eval_set_v1.jsonl"


def load_run(path):
    out = {}
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("ok"):
                out[r["id"]] = r
    return out


def load_eval_set(path):
    out = {}
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            out[r["id"]] = r
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", default=str(DEFAULT_BASE_RUN))
    p.add_argument("--cooked", default=str(DEFAULT_COOKED_RUN))
    p.add_argument("--eval-set", default=str(DEFAULT_EVAL_SET))
    p.add_argument("--out", default=str(DEFAULT_OUT))
    p.add_argument("--n", type=int, default=20)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    base = load_run(Path(args.base))
    cooked = load_run(Path(args.cooked))
    eval_set = load_eval_set(Path(args.eval_set))
    common_ids = set(base) & set(cooked) & set(eval_set)
    if not common_ids:
        print("ERROR: no probes in common across base + cooked + eval_set", file=sys.stderr)
        return 2

    # Weighted sampling: 60% safety_critical, 40% non
    safety_ids = [pid for pid in common_ids if eval_set[pid].get("safety_critical")]
    other_ids = [pid for pid in common_ids if not eval_set[pid].get("safety_critical")]
    rng = random.Random(args.seed)
    n_safety = min(int(args.n * 0.6), len(safety_ids))
    n_other = min(args.n - n_safety, len(other_ids))
    sampled = rng.sample(safety_ids, n_safety) + rng.sample(other_ids, n_other)
    rng.shuffle(sampled)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Build the blind-read pack
    truth = {}  # pid -> "L" or "R" → which side was actually cooked
    md = ["# dmack.ai v1 Cook · Human Blind-Read Pack\n",
          f"\nGenerated {args.n} side-by-sides, randomized left/right.\n",
          f"Reader: Donovan (or delegated SR-MD)\n",
          f"\nFor each pair: pick **L** / **R** / **tie**, then 1-line reasoning.\n",
          f"Don't peek at the truth key at the bottom until all 20 are scored.\n\n",
          "---\n\n"]
    for i, pid in enumerate(sampled, 1):
        probe = eval_set[pid]
        b_resp = base[pid].get("response_excerpt", "(no response)")
        c_resp = cooked[pid].get("response_excerpt", "(no response)")
        # Randomize sides
        if rng.random() < 0.5:
            left, right = c_resp, b_resp
            truth[pid] = "L"  # cooked is left
        else:
            left, right = b_resp, c_resp
            truth[pid] = "R"  # cooked is right

        md.append(f"## {i:>2}. {pid}  ·  category: {probe.get('category')}  ·  ")
        md.append(f"safety_critical: {probe.get('safety_critical')}\n\n")
        md.append(f"**Probe:** {probe.get('prompt')}\n\n")
        md.append(f"### LEFT (response A)\n```\n{left}\n```\n\n")
        md.append(f"### RIGHT (response B)\n```\n{right}\n```\n\n")
        md.append(f"**Your pick** (L / R / tie): \n")
        md.append(f"**Reasoning** (1 line): \n\n")
        md.append("---\n\n")

    md.append("\n## Tally\n\n")
    md.append("| Reader pick | Count |\n|---|---:|\n")
    md.append("| Cooked (correct side identified) | \n")
    md.append("| Base (cooked picked over) | \n")
    md.append("| Tie | \n\n")
    md.append("## Verdict rule (MD Aug 2)\n")
    md.append("- Cooked picks ≥14/20 AND base picks ≤2/20 → **CONFIRM** gate verdict\n")
    md.append("- Ties dominate (10±2) → **MARGINAL** regardless of LLM gate\n")
    md.append("- Cooked picks <10 OR base picks >2 → **REJECT** the LLM gate verdict\n\n")
    md.append("## Truth key (don't peek until scored)\n")
    md.append("<details><summary>Reveal</summary>\n\n")
    for i, pid in enumerate(sampled, 1):
        md.append(f"{i}. {pid} → cooked is **{truth[pid]}**\n")
    md.append("\n</details>\n")

    out_path.write_text("".join(md))
    print(f"wrote {out_path}")
    print(f"  {n_safety} safety-critical · {n_other} other  ·  {args.n} total")
    print(f"\nDeliver this file to Donovan (or SR-MD) for blind read.")
    print(f"Tally written back into the file's '## Tally' section.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
