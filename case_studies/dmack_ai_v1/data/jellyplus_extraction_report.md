# JELLY+ Cook Corpus Extraction (Corpus-SR Plan v1)
Generated post Corpus-SR signoff (sr_hack_corpus_signoff_v1.md, 2026-05-14).

**Target:** 6,500 pairs  ·  **Ceiling:** 8,000 pairs

**Pre-filter:** ON_DOMAIN_TIGHT regex + EXCLUDED_SOURCES (openalex-r2/r3/r4/r5)

## Pipeline funnel
| Stage | Pair count |
|---|---:|
| Source corpus | 77,797 |
| Successfully scored | 77,796 |
| Merged corpus + scores | 77,796 |
| After ON_DOMAIN_TIGHT + EXCLUDED filter | 64,551 |
| JELLY+ tier (composite >= 5) | 63,707 |
| **Final cook corpus** | **6,418** |

## Per-bucket extraction (Corpus SR §4-C plan)
| Bucket | Pool (on-domain JELLY+) | Take | Target | Min-Max | Status |
|---|---:|---:|---:|---:|---|
| `cgmacros-real-data` | 4,314 | 1,200 | 1,200 | 1000-1400 | OK |
| `bigideas-real-data` | 1,592 | 400 | 400 | 300-500 | OK |
| `pmc-fulltext` | 10,370 | 2,000 | 2,000 | 1700-2300 | OK |
| `government-public-domain` | 3,410 | 600 | 600 | 500-800 | OK |
| `international-public-health` | 4,139 | 500 | 500 | 400-700 | OK |
| `openalex-r1` | 9,154 | 1,100 | 1,100 | 900-1300 | OK |
| `refusal-hand-curated` | 118 | 118 | 128 | 128-128 | SHORTFALL by 10 |
| `openalex-drift-lifestyle` | 30,610 | 500 | 500 | 300-700 | OK |

## Final cook composition
### By tier
| Tier | Count |
|---|---:|
| APEX | 6,361 |
| HONEY | 57 |
| JELLY | 0 |

### By source
| Source | Count |
|---|---:|
| `pmc-fulltext` | 2,000 |
| `cgmacros-real-data` | 1,200 |
| `openalex-r1` | 1,100 |
| `government-public-domain` | 600 |
| `international-public-health` | 500 |
| `openalex-r2` | 500 |
| `bigideas-real-data` | 400 |
| `refusal-hand-curated` | 118 |

## Per-surface coverage (MD Aug 1 · sr_md_signoff_v1.md §5)
| Surface | Pairs in cook | Floor | Pass |
|---|---:|---:|---|
| food | 2643 | ≥150 | OK |
| exercise | 227 | ≥150 | OK |
| foot-care | 356 | ≥150 | OK |
| brain-care | 231 | ≥150 | OK |
| eyes | 423 | ≥150 | OK |
| addisons | 365 | ≥250 | OK |

Surface-floor verdict: **PASS** (cook does NOT launch unless all 6 pass).

## Addison's floor check (Corpus SR §4-E)
- Total Addison's pairs: **414** (floor: 250)
- Compliance-pattern Addison's: **40** (sub-floor: 30)
- Floor pass: **PASS**

## Surface-filter sources (Corpus SR §4-D + SCS Repair 2)
Per SCS over-correction fix: openalex-r2/r3/r4/r5 are NOT whole-source-excluded. Their on-domain (lifestyle-relevant) subset is mapped to the new `openalex-drift-lifestyle` bucket (target 500). Off-topic pairs from those sources (gestational/stroke rehab/frailty/UPF) drop at the surface filter.

- `openalex-r2` → `openalex-drift-lifestyle` (per-pair surface filter)
- `openalex-r3` → `openalex-drift-lifestyle` (per-pair surface filter)
- `openalex-r4` → `openalex-drift-lifestyle` (per-pair surface filter)
- `openalex-r5` → `openalex-drift-lifestyle` (per-pair surface filter)
