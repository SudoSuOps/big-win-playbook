# dmack.ai v1 · Cook Data Archive

Complete pair archive from the dmack.ai v1 cook (2026-05-14 cook · 2026-05-15 verdict). Preserved per Donovan's directive after the FAIL verdict so a future operator (or v2 cook · or JR Hack candidate) can re-derive everything.

## Files

| File | Size | Contents |
|---|---|---|
| `MASTER_dmack_ai_v1_royal_jelly.jsonl.gz` | 37 MB | **77,797 source pairs** · the full corpus pool BEFORE Curator scoring · gzipped (260 MB uncompressed) |
| `MASTER_dedup_report.json` | 1.6 KB | per-source counts and dedup stats |
| `scored_pairs.jsonl.gz` | 1.2 MB | **77,796 scored pairs** · Curator-9B 1-10 ratings on 5 dimensions (VR/SD/CD/SA/TS) · maps each pair to APEX/HONEY/JELLY/POLLEN/PROPOLIS tier |
| `cook_corpus_jellyplus.jsonl` | 15 MB | **6,418 cook pairs** · the actual training data after Corpus SR per-bucket extraction + ON_DOMAIN_TIGHT filter + per-surface floors + Addison's floor |
| `jellyplus_extraction_report.md` | 2.8 KB | per-bucket counts · per-surface coverage · Addison's floor PASS · the receipt that locked the cook corpus |
| `canary_probes.jsonl` | 23 KB | 60 hand-designed probes across 6 categories · the original canary suite |
| `dmack_eval_set_v1.jsonl` | 42 KB | **the locked gate eval set** · 60 probes × 4 gold-rubric criteria each (must_have / must_not_have / source_required / must_route_to · severity · safety_critical) · located in `../dmack_eval_set_v1.jsonl` |
| `canary_results.jsonl` | 70 KB | dry-run canary results (pre-corpus · 60/60 PASS) |
| `canary_results.json` | 1.2 KB | dry-run canary summary |
| `contamination_scan_report.json` | 2.4 KB | pre-cook contamination scan · 0 blocking hits |

## Sister files at the case study root (not duplicated here)

| File | What |
|---|---|
| `../verdict.md` | The structured FAIL verdict per `bakers_before_baker_doctrine` |
| `../responses_base.jsonl` | Raw responses from base Qwen3.5-9B-Instruct · 60 probes |
| `../responses_cooked.jsonl` | Raw responses from cooked dmack-ai-9b-v1 · 60 probes |
| `../runs_base.jsonl` | Per-probe Curator-judged scores for base · 60 probes |
| `../runs_cooked.jsonl` | Per-probe Curator-judged scores for cooked · 60 probes |
| `../sr_recipe_signoff.md` | Recipe SR REPAIR · 6 fixes |
| `../sr_corpus_signoff.md` | Corpus SR REPAIR · 8 fixes |
| `../sr_surface_coverage_signoff.md` | Surface Coverage SR REPAIR · 6 fixes |
| `../sr_md_signoff.md` | MD SIGNOFF · 3 augmentations · the seat that fired post-verdict |
| `../cook_recipe.md` | The locked cook recipe v1.2 |
| `../sft_qwen35_9b_lora.py` | The actual training script used |
| `../extract_jellyplus.py` | The corpus extractor (full · post-all-SR-repairs) |
| `../run_eval_vs_base.py` | The original dual-judge runner (single-judge fallback used in v1 due to VRAM) |

## Cook artifacts NOT in git (preserved on smash as PROPOLIS evidence)

| Path on smash | Size | What |
|---|---|---|
| `~/cooks/dmack-ai-9b-v1/final/adapter_model.safetensors` | ~440 MB | The cooked LoRA adapter · sha256 `77df7c0e150a6c016dd1b77dcd213d1c23a72c84ecea6b88a7d3edcf9fe40590` |
| `~/cooks/dmack-ai-9b-v1/checkpoint-*` | rolling | Mid-cook checkpoints (the auditor pattern · the latest 3-4 are kept) |
| `~/models/qwen3.5-9b-base/` | 19 GB | Base Qwen3.5-9B-Instruct · sha256-verified vs HF manifest |
| `~/models/swarmcurator-9b/` | 18 GB | The Curator judge · same as before this cook |
| `~/logs/full-cook.log` | ~7 MB | The full training log (loss curve · grad norms · token accuracy) |

## How to re-run this cook from scratch

1. Decompress: `gunzip -k MASTER_dmack_ai_v1_royal_jelly.jsonl.gz scored_pairs.jsonl.gz`
2. Re-extract cook corpus: `python3 ../../scripts/extract_jellyplus.py --corpus MASTER_dmack_ai_v1_royal_jelly.jsonl --scores scored_pairs.jsonl --out cook_corpus_jellyplus.jsonl --report extraction_report.md`
3. Verify the cook corpus matches the one in this directory (md5sum)
4. Spin up base Qwen3.5-9B-Instruct on a 32GB-class GPU
5. Run training per `../sft_qwen35_9b_lora.py` with the recipe in `../cook_recipe.md`
6. Run gate per `../run_eval_vs_base.py` with `../dmack_eval_set_v1.jsonl`
7. Compare your verdict against `../verdict.md` — your numbers should be in the same neighborhood

If your numbers WIN where this cook lost (adrenal-crisis 911 routing → 10/10 · refusal-routing → 100% · founder-voice delta → +1.0+), you've earned an SR Hack seat per `jr_hack_pipeline_doctrine.md`. The playbook is the test material.

## Why the MASTER is preserved (not just the cook corpus)

The Corpus SR's per-bucket extraction (`extract_jellyplus.py`) was OPINIONATED — it dropped openalex-r2/r3/r4/r5 entirely and held the cook corpus to ~6,500 pairs. v2 may want to re-extract differently (e.g. add the Donovan-voice exemplars the Surface Coverage SR identified · or keep more cgmacros pairs · or relax the ON_DOMAIN_TIGHT regex). The MASTER is the source of truth · the cook corpus is one extraction of many possible.

A v2 operator can re-extract from the MASTER with a different plan and produce a different cook corpus without re-running Curator scoring (which took ~84 min on smash). The scored_pairs.jsonl carries the Curator tier classification forward.

## Provenance

- **MASTER** assembled 2026-05-14 from: refusal-hand-curated (Donovan-supplied) + cgmacros-real-data (PhysioNet, credentialed-use) + bigideas-real-data (Big IDEAs Lab) + pmc-fulltext (NIH PMC, public domain subset) + government-public-domain (NIDDK + CDC + NIH patient education) + international-public-health (WHO + NICE + IWGDF) + openalex-r1 through openalex-r5 (peer-reviewed academic via OpenAlex pulls)
- **Curator scoring** ran 2026-05-14 on smash 5090 via vLLM serving SwarmCurator-9B at :8088 · ~84 min wall-clock for 77,797 pairs
- **Cook corpus extraction** ran 2026-05-14 with the SR-repaired `extract_jellyplus.py` (BUCKET_PLAN + ON_DOMAIN_TIGHT + EXCLUDED_SOURCES + per-surface floors + Addison's floor)
- **Cook training** ran 2026-05-14 to 2026-05-15 on smash 5090 · 2 hours 3 minutes · adapter saved at `~/cooks/dmack-ai-9b-v1/final/`
- **Eval gate** ran 2026-05-15 on smash 5090 sequentially (gather-then-judge · single-judge LLM scoring due to VRAM constraint · dual-judge LLM deferred to v2)
- **Verdict**: FAIL · structured per `verdict.md`
