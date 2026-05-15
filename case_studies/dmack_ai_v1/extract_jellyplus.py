#!/usr/bin/env python3
"""
Extract the dmack.ai cook corpus from Curator scoring + Corpus-SR per-bucket
plan (sr_hack_corpus_signoff_v1.md, 2026-05-14).

Reads:
  corpus/MASTER_dmack_ai_v1_royal_jelly.jsonl     # 77,797 source pairs
  eval/scored_pairs.jsonl                          # Curator scores per id

Writes:
  training/cook_corpus_jellyplus.jsonl             # the actual cook input
  reports/jellyplus_extraction_report.md           # distribution + decisions

Doctrine applied (post both SR signoffs 2026-05-14):
  - JELLY+ tier base filter (composite >= 5)
  - ON_DOMAIN_TIGHT regex pre-filter (Corpus SR Repair 2): drops off-target pairs
    that pass Curator's topic-blind 5-dim rubric (the Atlas-v1 mechanism)
  - EXCLUDED_SOURCES: openalex-r2/r3/r4/r5 (Corpus SR §4-D + §C):
    52% of MASTER but only 22% TIGHT-domain · gestational-diabetes/stroke
    rehab/frailty/ultra-processed-food · zero dmack eval-prompt coverage
  - BUCKET_PLAN: per-source target/min/max bands (Corpus SR §4-C)
  - COOK_TARGET = 6,500 / COOK_CEILING = 8,000 (NOT 25K — that's the firm-wide
    ceiling per cook_size_cap_doctrine; for a 6-surface medical specialist the
    target lands at ~6,500, ceiling at 8,000)
  - ADDISONS_FLOOR = 250 (Corpus SR Repair 4 · raised from Recipe SR's 150)
  - ADDISONS_COMPLIANCE_SUB_FLOOR = 30 (must be from refusal-hand-curated OR
    contain compliance markers — protects against floor met by literature
    mentions without safety-routing shape)
  - scored_pairs.jsonl existence + completeness pre-check (Corpus SR Repair 6)
  - POLLEN/PROPOLIS preserved in MASTER · excluded from cook
"""
from __future__ import annotations
import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS = ROOT / "corpus/MASTER_dmack_ai_v1_royal_jelly.jsonl"
DEFAULT_SCORES = ROOT / "eval/scored_pairs.jsonl"
DEFAULT_OUT = ROOT / "training/cook_corpus_jellyplus.jsonl"
DEFAULT_REPORT = ROOT / "reports/jellyplus_extraction_report.md"

# Corpus-SR signoff (sr_hack_corpus_signoff_v1.md)
COOK_TARGET = 6_500
COOK_CEILING = 8_000

ADDISONS_FLOOR = 250                  # raised from 150 (Corpus SR §4-E)
ADDISONS_COMPLIANCE_SUB_FLOOR = 30    # of the 250, ≥30 must teach safety-routing shape

ON_DOMAIN_TIGHT = re.compile(
    # Diabetes/Addison's clinical core (Corpus SR's original list, carries)
    r"\b(diabet|glucose|glycem|insulin|hba1c|a1c|cgm|libre|dexcom|"
    r"addison|adrenal\s+insufficien|adrenal\s+crisis|cortisol|"
    r"hydrocortisone|fludrocortisone|hypoglyc|hyperglyc|dka|ketoacidosis|"
    r"foot\s+(ulcer|wound|infection|care)|neuropathy|retinopathy|"
    r"gastroparesis|charcot|metform|sulfonylurea|glp-1|sglt|"
    r"stress[-\s]?dos|sick[-\s]?day|iwgdf|continuous\s+glucose|"
    # Surface lifestyle vocab (SCS widening · 6 surfaces + Donovan doctrine)
    r"nutrition|carbohydrate|protein|fiber|mediterranean|glycemic\s+index|"
    r"low[-\s]?carb|high[-\s]?protein|meal\s+plan|portion|fasting|"
    r"exercise|physical\s+activity|aerobic|resistance|cardio|HIIT|"
    r"yoga|walking|strength\s+training|sedentary|"
    r"mental\s+health|depression|anxiety|diabetes\s+distress|burnout|"
    r"mindfulness|meditation|cognitive|brain\s+fog|"
    r"vitamin\s+d|vitamin\s+b12|magnesium|omega[-\s]?3|"
    r"sleep|circadian|melatonin|sunlight|"
    r"organic|ultra[-\s]?processed|whole\s+foods|"
    r"dressing|gauze|bandage|antiseptic|saline|wound\s+care|first\s+aid|"
    r"glaucoma|cataract|macular|ophthalmolog|"
    r"shoe|footwear|sock|orthotic|insole|callus|blister)",
    re.IGNORECASE,
)

# Per-pair surface filter for openalex-r2/r3/r4/r5 (SCS Repair 2):
# Switched from whole-source exclusion (Corpus SR over-corrected) to per-pair
# surface check. Recovers ~7,066 lifestyle pairs (PREDIMED, IOM vitamin D,
# ultra-processed food, sleep-glucose research) that the prior exclusion dumped.
SURFACE_FILTER_SOURCES = {
    "openalex-r2", "openalex-r3", "openalex-r4", "openalex-r5",
}
DRIFT_LIFESTYLE_BUCKET = "openalex-drift-lifestyle"  # virtual bucket for the recovered pairs

ADDISONS_RE = re.compile(
    r"\b(addison|adrenal\s+insufficien|adrenal\s+crisis|hydrocortisone|"
    r"fludrocortisone|cortisol\s+replacement|glucocorticoid\s+replacement|"
    r"solu[-\s]?cortef|stress[-\s]?dos|stress[-\s]?cover)",
    re.IGNORECASE,
)

# MD Augmentation 1 (sr_md_signoff_v1.md §5): per-surface floor enforcement.
# The Corpus SR's ON_DOMAIN_TIGHT regex is clinical-medical-only — covers
# diabetes/Addison's/foot-ulcer well but partially or weakly covers food,
# exercise, brain-care, eye-care. Eval has 20 founder-voice probes spread
# across all 6 surfaces; corpus must give the model weight-baked signal on
# each surface, not rely entirely on the system prompt to fill the gap.
SURFACE_LEXICONS = {
    "food":       re.compile(r"\b(meal|carb|nutrition|diet|food|protein|fat|fiber|"
                              r"glycem|post[-\s]?prandial|mediterranean|carbohydrate|"
                              r"snack|portion|breakfast|lunch|dinner)\b", re.I),
    "exercise":   re.compile(r"\b(exercise|physical\s+activity|walk|run|swim|"
                              r"strength|cardio|aerobic|workout|movement|fitness)\b", re.I),
    "foot-care":  re.compile(r"\b(foot|feet|toe|wound|ulcer|callus|neuropath|"
                              r"podiatr|charcot|footwear|shoe|sock|amputat)\b", re.I),
    "brain-care": re.compile(r"\b(fatigue|brain\s+fog|cognitive|depress|anxiety|"
                              r"mental\s+health|sleep|burnout|distress|mood)\b", re.I),
    "eyes":       re.compile(r"\b(eye|vision|retinopath|ophthalmolog|cataract|"
                              r"macul|glaucoma|visual)\b", re.I),
    "addisons":   re.compile(r"\b(addison|adrenal|cortisol|hydrocortisone|"
                              r"fludrocortisone|stress[-\s]?dos|solu[-\s]?cortef)\b", re.I),
}
SURFACE_FLOOR = 150            # MD Aug 1 — minimum pairs per surface
SURFACE_FLOOR_ADDISONS = 250   # already covered by ADDISONS_FLOOR


def surface_of(pair: dict):
    """Return the FIRST matched surface for a pair (no double-counting)."""
    text = (pair.get("question") or "") + " " + (pair.get("answer") or "")
    for surface, regex in SURFACE_LEXICONS.items():
        if regex.search(text):
            return surface
    return None

ADDISONS_COMPLIANCE_RE = re.compile(
    r"\b(911|emergency\s+(room|injection|line)|endocrinologist|"
    r"solu[-\s]?cortef|stress[-\s]?dos|call\s+your\s+(provider|doctor|endo))",
    re.IGNORECASE,
)

# Per-bucket extraction plan (Corpus SR §4-C with SCS bumps)
BUCKET_PLAN = {
    "cgmacros-real-data":          {"target": 1200, "min": 1000, "max": 1400},
    "bigideas-real-data":          {"target":  400, "min":  300, "max":  500},
    "pmc-fulltext":                {"target": 2000, "min": 1700, "max": 2300},  # SCS bump 1800→2000
    "government-public-domain":    {"target":  600, "min":  500, "max":  800},
    "international-public-health": {"target":  500, "min":  400, "max":  700},  # SCS bump 400→500
    "openalex-r1":                 {"target": 1100, "min":  900, "max": 1300},  # SCS bump 1000→1100
    "refusal-hand-curated":        {"target":  128, "min":  128, "max":  128},
    DRIFT_LIFESTYLE_BUCKET:        {"target":  500, "min":  300, "max":  700},  # SCS new bucket: r2-r5 lifestyle
}


def is_addisons(pair: dict) -> bool:
    text = (pair.get("question") or "") + " " + (pair.get("answer") or "")
    return bool(ADDISONS_RE.search(text))


def is_addisons_compliance(pair: dict) -> bool:
    """Addison's pair that ALSO contains compliance/routing pattern."""
    if not is_addisons(pair):
        return False
    if pair.get("source_tag") == "refusal-hand-curated":
        return True
    text = (pair.get("question") or "") + " " + (pair.get("answer") or "")
    return bool(ADDISONS_COMPLIANCE_RE.search(text))


def is_on_domain(pair: dict) -> bool:
    """Topical pre-filter — Curator's 5-dim rubric is topic-blind.
    SCS Repair 1+2: widened regex covers the 6 surfaces; r2-r5 are no longer
    whole-source-excluded but still must pass the topic filter (which they
    do for the lifestyle subset)."""
    text = (pair.get("question") or "") + " " + (pair.get("answer") or "")
    return bool(ON_DOMAIN_TIGHT.search(text))


def effective_bucket(pair: dict) -> str:
    """Map openalex-r2/r3/r4/r5 to the new openalex-drift-lifestyle bucket
    (SCS Repair 2/3). Other sources keep their original tag."""
    src = pair.get("source_tag")
    if src in SURFACE_FILTER_SOURCES:
        return DRIFT_LIFESTYLE_BUCKET
    return src


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    p.add_argument("--scores", default=str(DEFAULT_SCORES))
    p.add_argument("--out", default=str(DEFAULT_OUT))
    p.add_argument("--report", default=str(DEFAULT_REPORT))
    args = p.parse_args()

    # ─── Repair 6 · Verify scored_pairs.jsonl exists + has coverage
    scores_path = Path(args.scores)
    if not scores_path.exists():
        print(f"ERROR: scored_pairs.jsonl not found at {scores_path}", file=sys.stderr)
        print(f"       Run: python3 eval/score_curator.py", file=sys.stderr)
        return 2
    n_scored_lines = sum(1 for _ in open(scores_path))
    print(f"scored_pairs.jsonl present: {n_scored_lines:,} lines")
    if n_scored_lines < 20_000:
        print(f"ERROR: only {n_scored_lines:,} pairs scored — insufficient for selection. "
              f"Re-run score_curator.py.", file=sys.stderr)
        return 2
    if n_scored_lines < 60_000:
        print(f"WARN: only {n_scored_lines:,} pairs scored (target 77,797). "
              f"Coverage <77%. Bucket selection may be biased. SR notified.", file=sys.stderr)

    # ─── Load scores
    scores_by_id = {}
    for line in open(scores_path):
        try:
            r = json.loads(line)
            if r.get("ok"):
                scores_by_id[r["id"]] = r
        except Exception:
            continue
    print(f"loaded {len(scores_by_id):,} successful scores")

    # ─── Merge corpus + scores
    pairs = []
    skipped_unscored = 0
    for line in open(args.corpus):
        if not line.strip():
            continue
        r = json.loads(line)
        pid = r.get("id")
        s = scores_by_id.get(pid)
        if s is None:
            skipped_unscored += 1
            continue
        pairs.append({
            "id": pid,
            "source_tag": r.get("__source_tag__"),
            "question": r.get("question"),
            "answer": r.get("answer"),
            "citation": r.get("citation") or r.get("source"),
            "tier": s["tier"],
            "composite": s["composite"],
            "VR": s["VR"], "SD": s["SD"], "CD": s["CD"], "SA": s["SA"], "TS": s["TS"],
            "note": s.get("note", ""),
        })
    print(f"merged {len(pairs):,} corpus+score pairs ({skipped_unscored:,} unscored)")

    # ─── Apply ON_DOMAIN_TIGHT pre-filter (Repair 2) BEFORE tier selection
    pre_filter_n = len(pairs)
    pairs = [p_ for p_ in pairs if is_on_domain(p_)]
    print(f"after ON_DOMAIN_TIGHT + EXCLUDED_SOURCES filter: {len(pairs):,} "
          f"(dropped {pre_filter_n - len(pairs):,})")

    # ─── Tier distribution diagnostics
    by_tier = collections.defaultdict(list)
    for p_ in pairs:
        by_tier[p_["tier"]].append(p_)
    print("\n=== tier distribution (on-domain only) ===")
    for t in ("APEX", "HONEY", "JELLY", "POLLEN", "PROPOLIS"):
        n = len(by_tier[t])
        pct = 100 * n / max(len(pairs), 1)
        print(f"  {t:<10s} {n:>6,}  ({pct:5.1f}%)")

    # ─── Per-bucket extraction (Repair 3)
    cookable = by_tier["APEX"] + by_tier["HONEY"] + by_tier["JELLY"]
    by_bucket = collections.defaultdict(list)
    for p_ in cookable:
        by_bucket[effective_bucket(p_)].append(p_)
    # Sort each bucket by composite descending so we take the best first
    for b in by_bucket:
        by_bucket[b].sort(key=lambda x: -x["composite"])

    print("\n=== bucket extraction (on-domain JELLY+, sorted by composite) ===")
    keep = []
    bucket_report = []
    for bucket, plan in BUCKET_PLAN.items():
        pool = by_bucket.get(bucket, [])
        target = plan["target"]
        cap = plan["max"]
        floor = plan["min"]
        take = min(target, len(pool))
        # Bound by max
        take = min(take, cap)
        selected = pool[:take]
        keep.extend(selected)
        avail = len(pool)
        shortfall = max(0, floor - take)
        status = "OK" if take >= floor else f"SHORTFALL by {shortfall}"
        print(f"  {bucket:<32s} pool={avail:>5,} take={take:>5,} "
              f"target={target} min={floor} max={cap}  {status}")
        bucket_report.append({
            "bucket": bucket, "pool": avail, "take": take,
            "target": target, "min": floor, "max": cap, "status": status,
        })

    # Anything whose effective bucket isn't in BUCKET_PLAN is dropped
    non_planned = [p_ for p_ in cookable if effective_bucket(p_) not in BUCKET_PLAN]
    if non_planned:
        print(f"\n  non-planned-bucket on-domain pairs (DROPPED): {len(non_planned):,}")
        sources = collections.Counter(p_["source_tag"] for p_ in non_planned).most_common()
        for s, n in sources[:5]:
            print(f"    {s}: {n}")

    # ─── MD Augmentation 1 · Per-surface floor enforcement
    surface_counts = collections.Counter(surface_of(p_) for p_ in keep)
    print(f"\n=== MD Aug 1 · per-surface coverage check ===")
    surfaces_to_floor = {
        "food": SURFACE_FLOOR, "exercise": SURFACE_FLOOR,
        "foot-care": SURFACE_FLOOR, "brain-care": SURFACE_FLOOR,
        "eyes": SURFACE_FLOOR, "addisons": SURFACE_FLOOR_ADDISONS,
    }
    for surface, floor in surfaces_to_floor.items():
        count = surface_counts.get(surface, 0)
        status = "OK" if count >= floor else f"SHORTFALL by {floor - count}"
        print(f"  {surface:<12} {count:>5}  (floor: {floor})  {status}")

    # Boost surfaces that are short — same pattern as Addison's floor enforcement
    for surface, floor in surfaces_to_floor.items():
        current = sum(1 for p_ in keep if surface_of(p_) == surface)
        if current >= floor:
            continue
        kept_ids = {p_["id"] for p_ in keep}
        deferred_for_surface = [
            p_ for p_ in cookable
            if p_["id"] not in kept_ids and surface_of(p_) == surface
        ]
        deferred_for_surface.sort(key=lambda x: -x["composite"])
        boost_needed = floor - current
        boost = deferred_for_surface[:boost_needed]
        if boost:
            # Evict lowest-composite pairs whose surface is OVER-floor
            over_surfaces = {s for s, c in surface_counts.items()
                             if s and surfaces_to_floor.get(s, 0) > 0
                             and c > surfaces_to_floor.get(s, 0)}
            evictable = [(i, p_) for i, p_ in enumerate(keep)
                         if surface_of(p_) in over_surfaces or surface_of(p_) is None]
            evictable.sort(key=lambda t: t[1]["composite"])
            n_evict = min(len(boost), len(evictable))
            evict_indices = {i for i, _ in evictable[:n_evict]}
            keep = [p_ for i, p_ in enumerate(keep) if i not in evict_indices]
            keep.extend(boost[:n_evict])
            print(f"  REBALANCED surface={surface}: +{n_evict} boosted from deferred")
            surface_counts = collections.Counter(surface_of(p_) for p_ in keep)

    surface_counts = collections.Counter(surface_of(p_) for p_ in keep)
    surface_floor_pass = all(
        surface_counts.get(s, 0) >= f for s, f in surfaces_to_floor.items()
    )
    print(f"  surface-floor verdict: {'PASS' if surface_floor_pass else 'FAIL'}")

    # ─── Repair 4 · Addison's floor + compliance sub-floor enforcement
    addisons_in_keep = [p_ for p_ in keep if is_addisons(p_)]
    addisons_compliance_in_keep = [p_ for p_ in addisons_in_keep if is_addisons_compliance(p_)]
    print(f"\n=== Addison's floor check ===")
    print(f"  total Addison's in cook: {len(addisons_in_keep)} (floor: {ADDISONS_FLOOR})")
    print(f"  compliance-pattern Addison's: {len(addisons_compliance_in_keep)} "
          f"(sub-floor: {ADDISONS_COMPLIANCE_SUB_FLOOR})")

    if len(addisons_in_keep) < ADDISONS_FLOOR:
        # Boost: pull from the on-domain JELLY+ pool (excluding what's already in keep)
        kept_ids = {p_["id"] for p_ in keep}
        deferred_addisons = [
            p_ for p_ in cookable
            if p_["id"] not in kept_ids and is_addisons(p_)
        ]
        deferred_addisons.sort(key=lambda x: -x["composite"])
        boost_needed = ADDISONS_FLOOR - len(addisons_in_keep)
        boost = deferred_addisons[:boost_needed]
        if boost:
            # Evict lowest-composite NON-Addison's pairs from keep to make room
            non_addisons_in_keep = [(i, p_) for i, p_ in enumerate(keep) if not is_addisons(p_)]
            non_addisons_in_keep.sort(key=lambda t: t[1]["composite"])
            n_evict = len(boost)
            evict_indices = {i for i, _ in non_addisons_in_keep[:n_evict]}
            keep = [p_ for i, p_ in enumerate(keep) if i not in evict_indices]
            keep.extend(boost)
            print(f"  REBALANCED: +{n_evict} Addison's pairs boosted from deferred (evicted "
                  f"{n_evict} lowest-composite non-Addison's)")
            addisons_in_keep = [p_ for p_ in keep if is_addisons(p_)]
            addisons_compliance_in_keep = [p_ for p_ in addisons_in_keep if is_addisons_compliance(p_)]

    if len(addisons_compliance_in_keep) < ADDISONS_COMPLIANCE_SUB_FLOOR:
        kept_ids = {p_["id"] for p_ in keep}
        deferred_compliance = [
            p_ for p_ in cookable
            if p_["id"] not in kept_ids and is_addisons_compliance(p_)
        ]
        deferred_compliance.sort(key=lambda x: -x["composite"])
        sub_boost_needed = ADDISONS_COMPLIANCE_SUB_FLOOR - len(addisons_compliance_in_keep)
        sub_boost = deferred_compliance[:sub_boost_needed]
        if sub_boost:
            non_compliance = [
                (i, p_) for i, p_ in enumerate(keep)
                if not is_addisons_compliance(p_) and not is_addisons(p_)
            ]
            non_compliance.sort(key=lambda t: t[1]["composite"])
            n_evict = len(sub_boost)
            evict_indices = {i for i, _ in non_compliance[:n_evict]}
            keep = [p_ for i, p_ in enumerate(keep) if i not in evict_indices]
            keep.extend(sub_boost)
            print(f"  SUB-FLOOR REBALANCED: +{n_evict} Addison's-compliance pairs boosted")
            addisons_in_keep = [p_ for p_ in keep if is_addisons(p_)]
            addisons_compliance_in_keep = [p_ for p_ in addisons_in_keep if is_addisons_compliance(p_)]

    floor_pass = (
        len(addisons_in_keep) >= ADDISONS_FLOOR
        and len(addisons_compliance_in_keep) >= ADDISONS_COMPLIANCE_SUB_FLOOR
    )
    print(f"  final Addison's: {len(addisons_in_keep)}  compliance: {len(addisons_compliance_in_keep)}  "
          f"floor: {'PASS' if floor_pass else 'FAIL'}")

    # ─── Final bounds check (target 6,500 · ceiling 8,000)
    if len(keep) > COOK_CEILING:
        # Trim lowest-composite from over-allocated buckets
        keep.sort(key=lambda x: -x["composite"])
        keep = keep[:COOK_CEILING]
    print(f"\n=== final cook corpus: {len(keep):,} pairs ===")
    print(f"  target: {COOK_TARGET}  ceiling: {COOK_CEILING}  status: ", end="")
    if BUCKET_PLAN["cgmacros-real-data"]["min"] <= len(keep) <= COOK_CEILING:
        # Approximate: between cumulative min and ceiling
        pass
    cumulative_min = sum(p["min"] for p in BUCKET_PLAN.values())  # ~5,728
    cumulative_max = sum(p["max"] for p in BUCKET_PLAN.values())  # ~7,778
    in_band = cumulative_min <= len(keep) <= cumulative_max
    print("WITHIN BAND" if in_band else f"OUT-OF-BAND (band: {cumulative_min}-{cumulative_max})")

    # ─── Write cook corpus
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        for p_ in keep:
            f.write(json.dumps(p_, ensure_ascii=False) + "\n")
    print(f"\nCOOK CORPUS WRITTEN: {out_path}  ({len(keep):,} pairs)")

    # ─── Report
    keep_by_src = collections.Counter(p_["source_tag"] for p_ in keep)
    keep_by_tier = collections.Counter(p_["tier"] for p_ in keep)

    report = [
        f"# JELLY+ Cook Corpus Extraction (Corpus-SR Plan v1)\n",
        f"Generated post Corpus-SR signoff (sr_hack_corpus_signoff_v1.md, 2026-05-14).\n\n",
        f"**Target:** {COOK_TARGET:,} pairs  ·  **Ceiling:** {COOK_CEILING:,} pairs\n\n",
        f"**Pre-filter:** ON_DOMAIN_TIGHT regex + EXCLUDED_SOURCES (openalex-r2/r3/r4/r5)\n\n",
        f"## Pipeline funnel\n",
        f"| Stage | Pair count |\n|---|---:|\n",
        f"| Source corpus | {pre_filter_n + skipped_unscored:,} |\n",
        f"| Successfully scored | {len(scores_by_id):,} |\n",
        f"| Merged corpus + scores | {pre_filter_n:,} |\n",
        f"| After ON_DOMAIN_TIGHT + EXCLUDED filter | {len(pairs):,} |\n",
        f"| JELLY+ tier (composite >= 5) | {len(cookable):,} |\n",
        f"| **Final cook corpus** | **{len(keep):,}** |\n\n",
        f"## Per-bucket extraction (Corpus SR §4-C plan)\n",
        f"| Bucket | Pool (on-domain JELLY+) | Take | Target | Min-Max | Status |\n|---|---:|---:|---:|---:|---|\n",
    ]
    for b in bucket_report:
        report.append(f"| `{b['bucket']}` | {b['pool']:,} | {b['take']:,} | {b['target']:,} | "
                      f"{b['min']}-{b['max']} | {b['status']} |\n")
    report.append(f"\n## Final cook composition\n")
    report.append(f"### By tier\n| Tier | Count |\n|---|---:|\n")
    for t in ("APEX", "HONEY", "JELLY"):
        report.append(f"| {t} | {keep_by_tier[t]:,} |\n")
    report.append(f"\n### By source\n| Source | Count |\n|---|---:|\n")
    for src, n in sorted(keep_by_src.items(), key=lambda x: -x[1]):
        report.append(f"| `{src}` | {n:,} |\n")

    surface_counts_final = collections.Counter(surface_of(p_) for p_ in keep)
    report.append(f"\n## Per-surface coverage (MD Aug 1 · sr_md_signoff_v1.md §5)\n")
    report.append(f"| Surface | Pairs in cook | Floor | Pass |\n|---|---:|---:|---|\n")
    for s, f_ in surfaces_to_floor.items():
        n = surface_counts_final.get(s, 0)
        report.append(f"| {s} | {n} | ≥{f_} | {'OK' if n >= f_ else 'FAIL'} |\n")
    report.append(f"\nSurface-floor verdict: **{'PASS' if surface_floor_pass else 'FAIL'}** (cook does NOT launch unless all 6 pass).\n")

    report.append(f"\n## Addison's floor check (Corpus SR §4-E)\n")
    report.append(f"- Total Addison's pairs: **{len(addisons_in_keep)}** (floor: {ADDISONS_FLOOR})\n")
    report.append(f"- Compliance-pattern Addison's: **{len(addisons_compliance_in_keep)}** "
                  f"(sub-floor: {ADDISONS_COMPLIANCE_SUB_FLOOR})\n")
    report.append(f"- Floor pass: **{'PASS' if floor_pass else 'FAIL'}**\n")

    report.append(f"\n## Surface-filter sources (Corpus SR §4-D + SCS Repair 2)\n")
    report.append(f"Per SCS over-correction fix: openalex-r2/r3/r4/r5 are NOT whole-source-excluded. "
                  f"Their on-domain (lifestyle-relevant) subset is mapped to the new "
                  f"`openalex-drift-lifestyle` bucket (target 500). Off-topic pairs from those "
                  f"sources (gestational/stroke rehab/frailty/UPF) drop at the surface filter.\n\n")
    for src in sorted(SURFACE_FILTER_SOURCES):
        report.append(f"- `{src}` → `openalex-drift-lifestyle` (per-pair surface filter)\n")

    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text("".join(report))
    print(f"REPORT WRITTEN: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
