#!/usr/bin/env python3
"""
Hand-spot-audit the cook corpus before SR re-review (Corpus-SR Repair 7).

Prints 10 random pairs from each of the 5 largest buckets in
cook_corpus_jellyplus.jsonl (50 pairs total) for human read-through.

What the SR is looking for as failure indicators:
  - miracle-cure language slipping past Curator (treats / cures / reverses)
  - first-person Donovan claims that violate the two-stream rule
    ("I lost a toe", "when I was diagnosed", etc.)
  - off-domain pairs that snuck past the ON_DOMAIN_TIGHT regex
  - duplicated-template lock-in (e.g. all CGMacros pairs reading identically)
  - <think> / </think> / <|thinking|> tag leakage
  - missing compliance footers on supplement/dose-adjacent pairs
  - missing 911 routing on emergency-shape pairs

Usage:
  python3 eval/spot_audit_cook_corpus.py
  python3 eval/spot_audit_cook_corpus.py --n-per-bucket 20    # bigger sample
  python3 eval/spot_audit_cook_corpus.py --seed 7              # re-roll
"""
from __future__ import annotations
import argparse
import collections
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS = ROOT / "training/cook_corpus_jellyplus.jsonl"

# Failure-indicator patterns the SR scans against
MIRACLE_RE = re.compile(
    r"\b(cures?|reverses?|treats?|prevents?)\b\s+\w*\s*"
    r"\b(diabet|addison|neuropath|retinopath|adrenal|disease)",
    re.IGNORECASE,
)
DONOVAN_FIRST_PERSON_RE = re.compile(
    r"\b(I\s+(lost|amputat|had\s+(my|the))|when\s+I\s+was\s+diagnosed|"
    r"my\s+(toe|amputation|surgery))\b",
    re.IGNORECASE,
)
THINK_TAG_RE = re.compile(r"<think>|</think>|<\|thinking\|>|Thinking Process:", re.IGNORECASE)
EMERGENCY_SHAPE_RE = re.compile(
    r"\b(chest\s+pain|passed\s+out|fruity\s+breath|adrenal\s+crisis|"
    r"black\s+tissue|stroke|severe\s+hypogly|seizure)",
    re.IGNORECASE,
)


def scan_pair(pair: dict) -> list[str]:
    """Return list of failure indicators detected in this pair."""
    flags = []
    text = (pair.get("question") or "") + " " + (pair.get("answer") or "")
    if MIRACLE_RE.search(text):
        flags.append("MIRACLE_LANGUAGE")
    if DONOVAN_FIRST_PERSON_RE.search(text):
        flags.append("DONOVAN_FIRST_PERSON")
    if THINK_TAG_RE.search(text):
        flags.append("THINK_TAG_LEAK")
    if EMERGENCY_SHAPE_RE.search(pair.get("question") or ""):
        # Emergency-shape question — check the answer mentions 911 or routing
        if "911" not in (pair.get("answer") or "").lower() and "emergency" not in (pair.get("answer") or "").lower():
            flags.append("EMERGENCY_NO_911")
    return flags


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    p.add_argument("--n-per-bucket", type=int, default=10)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    corpus_path = Path(args.corpus)
    if not corpus_path.exists():
        print(f"ERROR: cook corpus not found at {corpus_path}", file=sys.stderr)
        return 2

    pairs = []
    with open(corpus_path) as f:
        for line in f:
            if line.strip():
                pairs.append(json.loads(line))
    print(f"loaded {len(pairs):,} pairs from {corpus_path}")

    by_bucket = collections.defaultdict(list)
    for pair in pairs:
        by_bucket[pair.get("source_tag", "?")].append(pair)
    top5 = sorted(by_bucket.items(), key=lambda kv: -len(kv[1]))[:5]
    print(f"top 5 buckets: {[(k, len(v)) for k, v in top5]}")

    rng = random.Random(args.seed)
    all_flags = collections.Counter()
    flagged_pairs: list[tuple[str, dict, list[str]]] = []

    print()
    for bucket, bucket_pairs in top5:
        print("=" * 80)
        print(f"BUCKET: {bucket}  (showing {min(args.n_per_bucket, len(bucket_pairs))} of {len(bucket_pairs)})")
        print("=" * 80)
        sample = rng.sample(bucket_pairs, min(args.n_per_bucket, len(bucket_pairs)))
        for i, pair in enumerate(sample, 1):
            flags = scan_pair(pair)
            for f in flags:
                all_flags[f] += 1
            if flags:
                flagged_pairs.append((bucket, pair, flags))
            print()
            print(f"--- {i}. id={pair.get('id','?')}  tier={pair.get('tier','?')}  "
                  f"composite={pair.get('composite','?')}  flags={flags or '[]'}")
            q = (pair.get("question") or "")[:300]
            a = (pair.get("answer") or "")[:600]
            print(f"  Q: {q}")
            print(f"  A: {a}")

    print()
    print("=" * 80)
    print("AUTOMATED FLAG SUMMARY (regex-based, complementary to human read)")
    print("=" * 80)
    if all_flags:
        for flag, count in all_flags.most_common():
            print(f"  {flag:30s} {count:>4} hits")
        print()
        print(f"flagged pair ids:")
        for bucket, pair, flags in flagged_pairs:
            print(f"  {bucket} · {pair.get('id','?')} · {flags}")
    else:
        print("  no automated flags hit · pair quality looks clean")

    print()
    print("Next step: human SR signs (or rejects) the spot-audit by appending to")
    print("  reports/spot_audit_signoff.md")
    return 0 if not all_flags else 1


if __name__ == "__main__":
    sys.exit(main())
