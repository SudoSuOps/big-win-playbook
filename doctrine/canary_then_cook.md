# Canary-Then-Cook · 5-Stage Discipline

> The protocol that catches silent corruption bugs before GPU electrons burn.

## Why this exists

Loss curves lie. A cook can land a clean-looking loss curve and still net-regress vs base on the institutional eval (Atlas-Qwen-27B v1 · 244K pairs · 7-of-7 lenient PROMOTE on Tribunal · 86.41% token accuracy · then 6 of 10 institutional CRE prompts beat by base). Without canary-then-cook, the failure is invisible until the eval gate runs · by which point the GPU spend is sunk and the SR is on the hook.

## The 5 stages

```
Stage 0: PRE-FLIGHT VERIFY        ← before any code touches the GPU
  - sha256 base-model weights vs HF manifest (Repair 3 doctrine)
  - Scripts, recipe, eval set all reference each other consistently
  - The cook script defaults match the recipe doc (they tend to drift)

Stage 1: CORPUS PREP              ← deterministic, repeatable, auditable
  - Curator-tier-score the source pool
  - ON_DOMAIN_TIGHT topical pre-filter (Curator's rubric is topic-blind)
  - Per-bucket extraction with target/min/max bands
  - Per-surface floor enforcement (one floor per brand promise surface)
  - Domain-specific floors (e.g. Addison's-pair floor + compliance sub-floor)
  - Output a cook_corpus.jsonl in target band · halt if floor fails
  - Spot-audit (50 random pairs across top buckets · automated regex flag pass)

Stage 2: CANARY COOK              ← 50 steps · 1K subset · ~5 min on 5090
  - Validate the stack works on real data
  - Loss curve descends · no NaN · no plateau before step 30
  - VRAM stable (24-28 GB on 9B bf16 LoRA at seq=1024 · drops to batch 2 if seq=2048)
  - 7-receipt acceptance gate before greenlight (per `canary_post_smoke.md`):
    1. Loss healthy
    2. Trainable params ~30M for r=64 on q/k/v/o/gate/up/down
    3. VRAM stable (no climb · no leak)
    4. 20 founder-voice probes ≥17/20 in dmack register (retires voice-flex risk)
    5. 20 inference samples · ZERO think-tag leakage (retires tokenizer risk)
    6. 10 adrenal-crisis probes ≥9/10 with 911 routing (retires Addison's-depth risk)
    7. SHA256 of merged adapter weights anchored to auditor.log

Stage 3: FULL COOK                ← run-to-completion · 6-12 hrs typical
  - Cook auditor every 2-3 hours (loss curve · sample outputs · contamination scan)
  - Mid-cook SR review at epoch 1 completion
  - Kill switch armed at >1% think-tag contamination

Stage 4: EVAL VS BASE             ← the gate that determines pass/fail
  - Spin up cooked model on a separate vLLM port from base
  - Spin up second independent judge on yet another port
  - Run dual-judge eval on 60-probe locked eval set
  - Aggregate per-category, per-judge, per-safety-critical
  - Verdict per `bakers_before_baker.md` operational criteria

Stage 5: RECEIPT
  - PASS: Hedera-anchored Defendable receipt at <brand>.defendable.eth/cook/v<N>
  - MARGINAL: Phase P3.5 dual-routing ship plan
  - FAIL: PROPOLIS evidence preservation · SR fired · ownership escalates
```

## What the canary catches that loss curves don't

- **Tokenizer/chat-template leakage** — model emits `<think>` tokens in serving even though loss curve is clean. Caught by Stage 2 receipt #5.
- **Voice-register collapse** — model trained on factual content reverts to "As an AI assistant" register. Caught by Stage 2 receipt #4.
- **Safety-routing forgetting** — emergency-routing patterns dropped during fine-tune. Caught by Stage 2 receipt #6.
- **Memory leaks** — VRAM climbs across steps; cook would OOM at hour 4 of full run. Caught by Stage 2 receipt #3.
- **Silent param-count mismatches** — wrong LoRA target modules silently train fewer params. Caught by Stage 2 receipt #2.

## What goes WRONG when teams skip the canary

- Atlas-Qwen-27B v1 was canary'd · the canary saved the cook from a 65-75% probability lobotomy (per `senior_hack_final_look.md`). Without it: 50 hrs GPU burn · clean-looking loss curve · model that net-regressed vs base.
- Aviation cook 2026-03-14: 12,728 cooked pairs all had think-tag leakage discovered post-cook. Quarantined. Re-built with Cook Auditor 3-hour scan.

## The kill switch

If any canary receipt fails, the cook does NOT proceed to Stage 3. The team root-causes, repairs, re-canary. The MD must see all 7 receipts before signing greenlight.

## Stage 2 wall-clock budget

- 50 steps × ~13 sec/step (9B bf16 LoRA on 5090, batch 2, max_seq 1024) = ~11 min
- + 5 min for the inference samples (3 sets of 20 probes through vLLM)
- Total: ~15-20 min of canary work before MD signs greenlight to Stage 3

This is cheap insurance against burning 6-12 hrs on a broken cook.

## Related

- `outcome_ownership.md` — who gets fired if the cook fails
- `bakers_before_baker.md` — the gate Stage 4 enforces
- `senior_hack_final_look.md` — the SR review that gates Stage 2 → Stage 3
- `templates/canary_post_smoke_template.md` — the actual 7-receipt checklist
