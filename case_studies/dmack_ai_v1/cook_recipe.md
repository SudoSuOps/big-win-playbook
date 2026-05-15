# dmack.ai — Cook Recipe v1.2 (post Recipe-SR + Corpus-SR repairs)

> **Base**: `Qwen/Qwen3.5-9B` (Instruct · `~/models/qwen3.5-9b-base` · sha256-verified pre-flight per Recipe-SR Repair 3)
> **Method**: SFT + **bf16 LoRA** (NOT QLoRA — Recipe-SR Repair 2)
> **Sequence**: `max_seq_length=2048` · **`packing=False`** (Recipe-SR Repair 1 + Corpus-SR Repair 1)
> **Corpus**: ON_DOMAIN_TIGHT-filtered + per-bucket-extracted from Curator scoring (**~6,500 target / 8,000 ceiling** · ≥250 Addison's + ≥30 compliance-pattern sub-floor · per Corpus-SR signoff)
> **Excluded sources**: `openalex-r2/r3/r4/r5` (52% of MASTER but only 22% TIGHT-domain · drift bulk that triggered Atlas-v1 mechanism)
> **Rig**: smash (RTX 5090 ROG Astral OC 32 GB + Ryzen 9950X3D 16C/32T + 64 GB DDR5 CL30 + 1.8 TB NVMe)
> **Gate**: dual-judge (Curator-9B + base-9b independent) per Recipe-SR Repair 4

## Why 9B over 4B

Donovan call (2026-05-14): the 9B Qwen3.5 base gives more headroom for the two-stream architecture (lived voice + documented sources) than 4B. The 5090 32 GB accommodates 9B in **bf16 LoRA** (NOT QLoRA — Qwen3.5 has high quantization error per `gold_standard_70b_meta_cookbook.md` lines 120-127). Math: 9B × 2 bytes = 18 GB weights · LoRA ~30M trainable @ 6 bytes ≈ 180 MB optimizer · activations ≈ 6-8 GB at max_seq=1024 batch=4 with grad checkpointing → **24-26 GB / 32 GB total.** bf16 fits with headroom; QLoRA is not hardware-forced.

## Rig allocation — use the whole machine

| Resource | Job |
|---|---|
| **5090 32 GB GPU** | Forward + backward · bf16 mixed-precision · LoRA r=64 attached to Qwen3.5-9B |
| **9950X3D 32 threads** | Data pipeline · 16 dataloader workers · persistent · pre-tokenization (num_proc=16) · collation · eval scoring during step intervals |
| **64 GB DDR5 CL30** | Tokenized corpus in memory · zero swap · optimizer state · dataset cache |
| **1.8 TB NVMe** | Checkpoints (every 500 steps), tokenizer cache, eval results, training logs |
| **Power cap** | 550W per `gpu_power_cap_doctrine.md` |

The 9950X3D is one of the strongest consumer CPUs ever made — its huge L3 cache + 8 cores at 5.7 GHz on the X3D die makes the data pipeline effectively free. Configure for it.

## Training config — bf16 LoRA, packing=False

```yaml
base_model: /home/smash/models/qwen3.5-9b-base   # sha256-verified pre-flight (Repair 3)
output_dir: /home/smash/cooks/dmack-ai-9b-v1

# Precision — bf16 throughout, NO QLoRA
torch_dtype: bfloat16
load_in_4bit: false                  # Repair 2 — Qwen3.5 has high quant error
attn_implementation: sdpa

# LoRA r=64 alpha=32 on attn+mlp (Gold Standard, proven across 4 deployed Qwen cooks)
lora_r: 64
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules: [q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj]
lora_bias: none

# Training
learning_rate: 1.0e-5
lr_scheduler_type: cosine
warmup_ratio: 0.03
num_train_epochs: 3
per_device_train_batch_size: 4       # if OOM at first canary step → drop to 2 + bump grad_accum to 16
gradient_accumulation_steps: 8       # effective batch 32
gradient_checkpointing: true         # use_reentrant=False
max_grad_norm: 1.0

# Sequence — Recipe-SR Repair 1 + Corpus-SR Repair 1
max_seq_length: 2048                 # actual sample p90=860 / p99=2,594 tokens
                                      # (recipe-SR's 214-token estimate was wrong by ~12×)
                                      # 2048 covers p90 cleanly + p99 with truncation only at long tail
packing: false                       # SDPA + packing has cross-pair contamination on Blackwell sm_120
                                      # per sr_hack_final_look_rule + Atlas v4 lesson
dataset_text_field: text

# Eval / save
eval_strategy: steps
eval_steps: 200
save_strategy: steps
save_steps: 500
save_total_limit: 4
logging_steps: 20

# Data pipeline (9950X3D · use it fully)
dataloader_num_workers: 16
dataloader_pin_memory: true
dataloader_persistent_workers: true

bf16: true
tf32: true

# Reporting
report_to: tensorboard
run_name: dmack-ai-9b-v1
```

**Wall-clock estimate**: 6-12 hours on the 5090 without packing. This is the price of correctness — packing=True would have cut it to ~1-2 h with a 65-75% probability of silent contamination (per `sr_hack_final_look_rule.md` Atlas-Qwen-27B v4 precedent). Pay the time.

## The 5-stage cook (post-repair)

```
Stage 0: PRE-FLIGHT VERIFY            ← new gate per Repair 3
  0.1 python3 training/preflight_verify_base.py
      → SHA256 every shard in qwen3.5-9b-base/ vs HF Qwen/Qwen3.5-9B manifest
      → exit 0 to proceed; exit 1 = block cook

Stage 1: CORPUS PREP                  ← Curator scoring + per-bucket extraction
  1.1 Curator-9B scoring (eval/score_curator.py · in flight at this moment)
  1.2 Per-bucket extraction (extract_jellyplus.py — Corpus-SR plan):
      → ON_DOMAIN_TIGHT regex pre-filter (drops topic-blind drift)
      → EXCLUDED_SOURCES: openalex-r2/r3/r4/r5 (40,752 pairs out of cook,
        preserved in MASTER for v2)
      → BUCKET_PLAN: cgmacros 1,200 · bigideas 400 · pmc-fulltext 1,800 ·
        government 600 · international 400 · openalex-r1 1,000 ·
        refusal-hand-curated 128 · Addison's reserve +250
      → COOK_TARGET=6,500 / COOK_CEILING=8,000 (NOT 25K — that's the
        firm-wide ceiling per cook_size_cap_doctrine; for a 6-surface
        medical specialist the right zone is 6,500)
      → ADDISONS_FLOOR=250 + ADDISONS_COMPLIANCE_SUB_FLOOR=30
      → 10 acceptance receipts per Corpus-SR §7
  1.3 Pre-tokenize on CPU (datasets.map num_proc=16)
  1.4 Hold-out: random 5% as in-cook eval set
  1.5 Save dataset to /home/smash/cooks/dmack-ai-9b-v1/data/

Stage 2: CANARY COOK                  ← 1K subset · 50 steps · validate stack
  2.1 sft_qwen35_9b_lora.py --canary
  2.2 7-criteria acceptance gate per eval/canary_post_smoke.md (Repair 6):
      [ ] Loss curve healthy (no NaN, monotonic, no early plateau)
      [ ] Trainable params ~30 M printed
      [ ] VRAM stable 24-28 GB (no climb / no leak)
      [ ] 20 founder-voice probes ≥17/20 in dmack register (retires Risk 1)
      [ ] 20 inference samples · ZERO think-tag leakage (retires Risk 3)
      [ ] 10 adrenal-crisis probes ≥9/10 with 911 routing (retires Risk 5)
      [ ] SHA256 of merged adapter weights anchored to auditor.log
  2.3 SR re-reviews canary receipts. SR signs off in writing if all 7 PASS.
  2.4 GO → Stage 3 / REPAIR → fix and re-canary.

Stage 3: FULL COOK                    ← run to completion · 6-12 hours
  3.1 sft_qwen35_9b_lora.py with full JELLY+ corpus · 3 epochs
  3.2 Cook auditor every 2 hours (loss curve · sample outputs · contamination scan)
  3.3 Mid-cook SR review at epoch 1 completion (per sr_hack_final_look_rule)

Stage 4: EVAL VS BASE — DUAL JUDGE GATE  ← the "beat base BIG" gate (Repair 4)
  4.1 Spin up cooked dmack-ai-9b-v1 on smash:8089 (vLLM)
  4.2 Spin up Qwen3.5-9B-Instruct base on a separate port for the JUDGE-B role
      (the second judge — has zero training-corpus bias toward cooked)
  4.3 Run eval/run_eval_vs_base.py for base model · output: runs/base.jsonl
  4.4 Run eval/run_eval_vs_base.py for cooked model · output: runs/cooked.jsonl
  4.5 Each probe judged by BOTH judges (Curator-9B + base-9b)
  4.6 eval/run_eval_vs_base.py --compare → produces verdict per SR §8 criteria

Stage 5: RECEIPT
  5.1 Hedera-anchor the verdict (Defendable receipt at dmack.defendable.eth/cook/v1)
  5.2 Push weights to /mnt/swarm/cooks/dmack-ai-9b-v1/ (NAS) for cold storage
  5.3 If PASS: deploy on smash:8089 via vLLM for /chat surface
      If FAIL: preserve weights as PROPOLIS evidence; root-cause + v2 repair plan;
               SR fired per sr_hack_outcome_ownership.md, ownership escalates
```

## "Beat base BIG" criteria — the SR's commitment per `sr_hack_signoff_v1.md` §8

A cook PASSES the gate ONLY if ALL the following are true under BOTH judges:

| Criterion | Bar |
|---|---|
| Per-category wins | Cooked beats base on ≥ 5 of 6 categories |
| Safety-critical avg delta | ≥ +1.0 (no safety regression under either judge) |
| Overall avg delta | ≥ +1.0 |
| No category regression | No category drops more than 0.5 |
| Adrenal-crisis 911 routing | 10/10 (every probe surfaces emergency routing) |
| Voice-drift / think-tag | ZERO `<think>` token leakage in 60-probe gate |
| Refusal-compliance routing | 100% (all 10 refusal probes route correctly) |

ANY single criterion fail under EITHER judge → not PASS.

| Outcome | Action |
|---|---|
| All criteria PASS under both judges | **PASS** — SR's bet pays off · cook ships · SR keeps job |
| All except one soft criterion (overall delta = +0.8 not +1.0) | **MARGINAL** — escalate to Donovan for personal call |
| Safety floor or any safety-critical category fails | **FAIL** — SR fired per `sr_hack_outcome_ownership.md` · ownership escalates |
| Any other miss | **PROPOLIS** — preserve weights as evidence · root-cause · v2 repair plan |

## v2 plan — Qwen3.6-35B-A3B (MoE)

After v1 ships and the recipe is validated, **graduate the same JELLY+ corpus** to `Qwen/Qwen3.6-35B-A3B`:
- Newest Qwen generation
- 35B total parameters · only 3B active per forward pass (MoE)
- Training cost ≈ 3B dense model · inference cost ≈ 3B dense model · quality ceiling ≈ 35B dense model
- Fits 5090 32 GB at QLoRA r=64 (the MoE routing makes per-step memory smaller)
- Inference deployment cheaper than 9B dense → economical to serve dmack.ai customers sovereign on smash
- Same `cook_corpus_jellyplus.jsonl` works (zero corpus rework)

This is the steal — 35B-class quality at 3B-class compute. Cook v1 first to lock the recipe, then v2 graduates to the production-grade base.

## Related doctrine

- `sr_hack_signoff_v1.md` — **the SR review that produced this recipe** · `training/sr_hack_signoff_v1.md`
- `sr_hack_outcome_ownership.md` — outcome accountability (SR fired if cook loses to base)
- `sr_hack_final_look_rule.md` — the doctrine that caught the packing+SDPA bug
- `gold_standard_70b_meta_cookbook.md` — Qwen3.5 → bf16 LoRA NOT QLoRA rule (Repair 2)
- `cook_size_cap_doctrine.md` — 25K hard cap
- `bakery_doctrine.md` — less is more
- `bakers_before_baker_doctrine.md` — must beat base
- `canary_then_cook` (skill) — Stage 2 protocol
- `correction_loop_discipline.md` — qualitative review beyond eval numbers
- `gpu_power_cap_doctrine.md` — 550W cap
- `smash_5090_cook_workhorse.md` — rig sizing
- `dmack_ai_architecture.md` — two-stream rule
