# Senior Hack — Corpus-Architecture Peer Review · dmack.ai v1 (Qwen3.5-9B / smash 5090)

**Reviewer role:** Corpus-architecture senior hack, independent peer review (per `sr_hack_final_look_rule.md`)
**Cook under review:** `dmack-ai-9b-v1` — JELLY+ corpus extracted from 77,797-pair MASTER, ≤25K cap per current recipe
**Decision under review:** Corpus shape (size · per-bucket allocation · Curator-filter approach · Addison's floor · CGMacros mix)
**Date:** 2026-05-14
**Accountability:** Governed by `sr_hack_outcome_ownership.md` — if this corpus-shape call contributes to a loss-to-base, this SR is fired and ownership escalates. Reviewing eyes-open. The recipe-SR closed the recipe doctrine violations; my seat closes the corpus-shape gap they signed off on by reference instead of defending for the diabetic-specialist case specifically.

---

## 1 · Headline recommendation

**REPAIR — DO NOT GREENLIGHT THE 25K CAP AS-WRITTEN. SHRINK TO ~6,500 PAIRS.**

The first SR signed off on the 25K cap by reference to `cook_size_cap_doctrine.md` + `bakery_doctrine.md` without defending it for **this** cook. That's the gap. The 25K cap was set in a CRE context (Atlas Block-2: 107K split into 4× ≤25K sub-cooks targeting four discrete failure modes) — it's a **ceiling for a generalist firm-OS cook**, not a target for a **narrow medical specialist with 6 surfaces**.

Ground-truth audit of the 77,797-pair MASTER (this signoff, §3) shows the source pool is **29% off-domain to dmack.ai's 6 surfaces** (22,917 pairs that don't match a broad diabetes/Addison's/foot/care lexicon — ultra-processed-food reviews, stroke rehab, frailty in elderly, gestational-diabetes literature reviews from openalex-r2/r3/r4/r5 bulk pulls). A composite-score filter alone (the current `extract_jellyplus.py` approach) does **not** distinguish "well-written off-domain abstract" from "well-written on-target diabetes pair" — Curator's rubric (VR/SD/CD/SA/TS) scores voice/source/compliance/safety/two-stream. **None of those five dimensions test topical relevance to dmack.ai's 6 surfaces.** Therefore the JELLY+ extraction will systematically pass off-domain HONEY-tier abstracts into the cook corpus and dilute the on-target signal — exactly the mechanism that produced Atlas-Qwen-27B v1's net regression (244K → PROPOLIS, `atlas_qwen_27b_v1_cook_verdict.md`).

The 8,600-target in `FLIGHTSHEET.md` was the right instinct; it lost to the 25K cap when the recipe was rewritten because no one defended the smaller number for the diabetic-specialist case. **I'm defending it now.** Plus three corpus structural issues the first SR did not surface (per-bucket allocation drift, Addison's floor too low, CGMacros mix unbounded) that get fixed in §6.

After repairs are applied to `extract_jellyplus.py` AND a sample of the resulting cook_corpus_jellyplus.jsonl is hand-spot-audited (50 pairs across the buckets), I will sign off. **The repair list in §6 is non-negotiable. I do NOT sign off blank-check on a 25K-cap extraction from this MASTER.**

---

## 2 · What carries from the first SR's review

The first SR closed the right things in §6 of `sr_hack_signoff_v1.md`:

- packing=False (Repair 1) — load-bearing for cross-pair contamination prevention. Carries.
- bf16 LoRA, NOT QLoRA (Repair 2) — Qwen3.5 quant-error tax avoided. Carries.
- SHA256 base verification (Repair 3) — preflight gate. Carries.
- Dual-judge gate (Repair 4) — eliminates judge-corpus contamination structural bias. Carries.
- Addison's floor of ≥150 pairs (Repair 5) — **floor too low; sharpened in §6 below to ≥250**. Carries with bump.
- Canary 7-receipt gate (Repair 6) — the only mechanism that catches a corpus-shape miscall before full burn. Carries.

The strategic frame from `SECRET_SAUCE.md` — the 5-pillar moat — assumed ~35,876 confirmed pairs (§4 of SECRET_SAUCE). **My recommendation contradicts that count without contradicting the moat.** The moat lives in the *quality of the targeting*, not the volume of the master. SECRET_SAUCE §4 itself cites the bakery doctrine: *"500-1000 fantastic muffins crush 25K of ingredients."* The 35,876 number was the ingredient inventory; the **muffin count is what we cook**, and it should be 6,500, not 25,000.

---

## 3 · Ground-truth audit of MASTER (the receipts the first SR didn't produce)

Audit script run on `corpus/MASTER_dmack_ai_v1_royal_jelly.jsonl` (77,797 pairs, this session). Two regex passes: `ON_DOMAIN_TIGHT` (matches diabet/glucose/insulin/Addison's/foot-ulcer/IWGDF/etc — the dmack.ai 6-surface lexicon) and `OFF_DOMAIN` (no overlap with broader diabetes/care lexicon at all).

| Source | Total | TIGHT-domain | (% TIGHT) | OFF-domain | (% OFF) | Addison's |
|---|---:|---:|---:|---:|---:|---:|
| `pmc-fulltext` | 11,169 | 10,754 | **96.3%** | 240 | 2.1% | **918** |
| `cgmacros-real-data` | 4,314 | 4,314 | **100.0%** | 0 | 0.0% | 0 |
| `bigideas-real-data` | 1,592 | 1,592 | **100.0%** | 0 | 0.0% | 0 |
| `government-public-domain` | 3,462 | 3,246 | **93.8%** | 22 | 0.6% | 34 |
| `refusal-hand-curated` | 128 | 115 | 89.8% | 7 | 5.5% | 19 |
| `openalex-r1` | 11,064 | 7,554 | 68.3% | 2,414 | 21.8% | 368 |
| `international-public-health` | 5,316 | 3,528 | 66.4% | 1,288 | 24.2% | 172 |
| `openalex-r2` | 7,536 | 2,602 | **34.5%** | 3,202 | **42.5%** | 0 |
| `openalex-r4` | 9,328 | 2,308 | **24.7%** | 4,106 | **44.0%** | 2 |
| `openalex-r3` | 11,368 | 2,302 | **20.2%** | 5,548 | **48.8%** | 10 |
| `openalex-r5` | 12,520 | 1,570 | **12.5%** | 6,090 | **48.6%** | 6 |
| **TOTAL** | **77,797** | **39,885** (51%) | | **22,917** (29%) | | **1,529** (2.0%) |

**Length receipt (n=156 sample):** char p50=2,109 / p90=3,452 / p99=10,377 → token p50≈525 / p90≈860 / p99≈2,594. **Note: the first SR's recipe-§Repair-1 estimate of "p99=214 tokens" is wrong by ~12×.** These are publication-paragraph pairs, not Q/A snippets. This affects max_seq_length sizing — `max_seq_length=1024` (current recipe) clips ~10% of pairs at p90 and silently truncates ~25% of the larger pmc-fulltext / openalex paragraphs. **Bump to max_seq_length=2048 for safety.** (See §6 Repair 1.)

### What the table proves

1. **openalex-r2/r3/r4/r5 are dilution sources.** They are bulk OpenAlex pulls about cardiometabolic adjacency (PREDIMED-style nutrition reviews, stroke rehab, frailty, gestational diabetes) that drift further from dmack.ai's 6 surfaces with every round. Combined: 40,752 pairs in MASTER — **52% of the entire master** — but only 8,782 pairs are TIGHT-domain (22%). The other 32,000 are loose-adjacency-or-off-target. Seven of the 5,548 openalex-r3 OFF-domain pairs sampled at random landed on stroke rehab, ultra-processed food, meat consumption, and frailty in elderly. **None of those probe a dmack.ai eval prompt.**

2. **pmc-fulltext is the corpus crown jewel for medical specificity.** 96.3% TIGHT-domain, 918 of 1,529 Addison's pairs (60% of all Addison's content). Curator-9B will rate these very high on SD/CD/SA. **Take more from here, fewer from openalex-r2/r3/r4/r5.**

3. **Addison's is concentrated in 4 sources.** pmc-fulltext (918) + openalex-r1 (368) + international-public-health (172) + refusal-hand-curated (19) = 1,477 of the 1,529 Addison's pairs. **Any per-bucket plan that under-samples pmc-fulltext starves the founder's coupled T1D+Addison's reasoning.** A flat-per-source allocation gets it wrong.

4. **CGMacros + BigIDEAs are 100% on-target moat data**, but only 5,906 pairs combined (7.6% of MASTER). The first SR didn't speak to whether they get the floor + ceiling treatment — the bakery doctrine says they should. **Floor 4,500 / ceiling 5,906.** This is the real-data anchor that no competitor has.

5. **JELLY+ ≠ dmack.ai-relevant.** This is the central failure-mode the first SR didn't flag. Curator's 5-dim rubric (VR/SD/CD/SA/TS) does not test topical relevance to dmack.ai. A well-written, well-cited, properly compliance-shaped paper abstract about gestational-diabetes-and-macrosomia from openalex-r2 will score HONEY-tier. It then enters the cook and the model burns gradient on it. **Curator-filter alone is insufficient. Topical pre-filter required.**

---

## 4 · Answers to the six specific questions Donovan asked

### A · Is 25K the right CEILING?

**No. For dmack.ai v1, the right ceiling is 8,000 pairs.** The doctrine ceiling is 25K (`cook_size_cap_doctrine.md`) — that's a **firm-wide invariant** for any cook. A specialist cook with a 6-surface scope can and should go far below it. Doctrine reasoning carries (signal scatter above 25K is fatal); but for a narrow product, 25K is **lenient by 3-4×**. Reference Curator-Mistral-3B v2 (501 pairs against fabrication-detection blind spot — beat its predecessor). Reference Bookmaker-8B (similar surgical scale). The doctrine itself says (`cook_size_cap_doctrine.md` §3): *"the 500-Pack SKU is the cap's distilled essence … 500–1,000 pairs targeted at one failure mode beats wholesale by 25-50× on leverage."* dmack.ai is a 6-surface cook, so multiply: 500 × 6 surfaces = ~3K minimum, 1,000 × 6 = ~6K natural target, with headroom for compliance/refusal anchors and the CGMacros real-data moat → **~6,500 lands in the right zone**.

### B · What's the right TARGET (not ceiling)?

**~6,500 pairs target, 8,000 hard ceiling.** The flightsheet's original 8.6K was directionally right but slightly heavy on the "Honey-tier educational bulk" (5,500 pairs of MASTER_PLATINUM filter + ADA paraphrase). I'm trimming the bulk and tightening the Royal-Jelly per-surface allocation to 6,500. Here's the math grounded in `bakery_doctrine.md` and the eval-set-v1 structure:

| Eval surface | Eval probes | Pairs needed for solid coverage at ~10× ratio |
|---|---:|---:|
| emergency-hard-stop | 10 | ~600 |
| adrenal-crisis | 10 | ~700 (bumped — Addison's moat) |
| refusal-compliance | 10 | ~600 |
| citation-behavior | 5 | ~400 |
| voicedrift-and-thinktag | 5 | ~300 |
| founder-voice (food/exercise/foot/brain/eye/addisons) | 20 | ~2,200 |
| **Subtotal pair-floor for eval coverage** | 60 | **~4,800** |
| CGMacros real-data moat (the unique data) | — | +1,200 |
| BigIDEAs multi-day pattern moat | — | +400 |
| **TOTAL TARGET** | | **~6,400 ≈ 6,500** |

This is **lower** than the flightsheet's 8,600 because (a) we're trimming Honey-tier educational bulk (the SECRET_SAUCE moat is targeting + lived authority + receipts, NOT volume of paraphrased educational content) and (b) the bakery doctrine is now load-bearing per `bakers_before_baker_doctrine.md` (we have not beaten base yet at any cook).

### C · Right per-bucket allocation

This is the table the first SR didn't write. Each row sources from MASTER (see §3 audit) and locks a min/target/max so the extractor can't drift.

| Bucket | Source(s) in MASTER | Target | Min | Max | Why |
|---|---|---:|---:|---:|---|
| **Real-data CGM/macro pairs** | `cgmacros-real-data` (4,314 available) | **1,200** | 1,000 | 1,400 | The unique data moat. SECRET_SAUCE §4. Sample down from 4,314 to 1,200 to keep dataset balance; 1,200 is enough for the model to learn the BG-response pattern shape without overweighting CGM-recall vs reasoning. **Do NOT take all 4,314** — that would over-weight a single template shape. |
| **Multi-day pattern pairs** | `bigideas-real-data` (1,592) | **400** | 300 | 500 | Dawn phenomenon, time-in-range, exercise patterns — needed for the "patterns" surface. Sample-down from 1,592 to avoid template overweighting. |
| **Peer-reviewed diabetes/endocrinology grounding** | `pmc-fulltext` TIGHT-domain only (10,754 available) | **1,800** | 1,500 | 2,200 | Crown jewel — 96.3% on-target, source for 60% of all Addison's content. Take by Curator score, ranked descending, **only from TIGHT-domain subset**. |
| **Government public-domain education** | `government-public-domain` (3,462 available) | **600** | 500 | 800 | NIDDK / CDC / NIH — clean educational bulk with strong source attribution. |
| **International public-health** | `international-public-health` (5,316 available, 66% TIGHT) | **400** | 300 | 600 | WHO / NICE / IWGDF — adds non-US guideline diversity. TIGHT-only filter. |
| **OpenAlex peer-reviewed (curated to TIGHT-domain)** | `openalex-r1` TIGHT only (7,554 available, 68% TIGHT) | **1,000** | 800 | 1,200 | Peer-reviewed diabetes papers cite-traceable. **Only openalex-r1 — drop openalex-r2/r3/r4/r5 entirely from the cook (see §5 D).** |
| **Compliance refusal / hand-curated** | `refusal-hand-curated` (128 available) | **128** | 128 | 128 | Take all 128. Hand-curated, 89.8% TIGHT, 14.8% Addison's. Each pair is a compliance pattern the eval directly tests. |
| **Reserved Addison's-floor lift** | from any TIGHT-domain Addison's-tagged pair across pmc/openalex-r1/international/refusal | **+250** | 250 | 250 | Addison's-floor enforcement (raised from 150 to 250, see §5 E). The extractor priority-boosts these from MASTER if the bucket allocations don't naturally land 250+ Addison's pairs (they should, but explicit floor is required). |
| **TOTAL** | | **~6,528** | 5,728 | 7,778 | Within ±20% of the 6,500 target. |

**Buckets explicitly EXCLUDED from the cook:**
- `openalex-r2` (7,536 in MASTER, only 34.5% TIGHT, 0 Addison's) — **EXCLUDE** — drift round, gestational-diabetes/preeclampsia bulk
- `openalex-r3` (11,368, 20.2% TIGHT, 10 Addison's) — **EXCLUDE** — drift round, ultra-processed food / meat consumption / cardiometabolic adjacency
- `openalex-r4` (9,328, 24.7% TIGHT, 2 Addison's) — **EXCLUDE** — drift round
- `openalex-r5` (12,520, 12.5% TIGHT, 6 Addison's) — **EXCLUDE** — drift round, frailty / stroke rehab in elderly

**Total OFF-domain bulk excluded: ~40,752 pairs (52% of MASTER).** They're preserved in MASTER for v2 / future surfaces but **do not enter the dmack.ai v1 cook.** This is the central correction. SECRET_SAUCE §4's "~24,286 unique peer-reviewed papers across OpenAlex R1/R2/R3" is a marketing line that aggregated drift rounds with the on-target round. The cook learns from the on-target subset.

### D · Does JELLY+ produce the right shape?

**No — not without a topical pre-filter.** The Curator-9B rubric (VR/SD/CD/SA/TS) scores 5 dimensions: voice, source, compliance, safety, two-stream. **None test topical relevance.** A well-cited, well-formatted paper-abstract about ultra-processed food (openalex-r3) will score HONEY-tier. It then enters the cook. The model spends optimizer steps fitting that pair instead of fitting an Addison's-stress-dosing pair.

This is the **same failure-mode-class** that produced Atlas-Qwen-27B v1's net regression. Atlas v1's 244K pairs were quality-filtered (Tribunal-validated, schema-checked, dedup'd). They were not **target-filtered** — that's what generated the signal scatter. From `atlas_qwen_27b_v1_cook_verdict.md`: *"Cook v1 wasn't a corpus-quality failure alone; it was a volume-induced signal-scatter failure."*

**Fix:** Add a topical pre-filter to `extract_jellyplus.py` BEFORE the Curator-score rank-cut. The filter is the same `ON_DOMAIN_TIGHT` regex from §3 of this signoff (already validated to pass 100% of cgmacros, 100% of bigideas, 96% of pmc-fulltext, 94% of government, and to drop the bulk of off-target openalex-r3/r4/r5). Run order:
1. **First** drop all pairs from sources `openalex-r2/r3/r4/r5` (bucket exclusion per §C)
2. **Second** apply `ON_DOMAIN_TIGHT` regex to remaining pairs — drop non-TIGHT
3. **Third** rank within each per-bucket budget by Curator composite score
4. **Fourth** take top-N up to bucket target (per §C table)
5. **Fifth** apply Addison's floor enforcement (raised to 250) — boost from deferred queue

Without these edits, JELLY+ over-collects mediocre on-domain JELLY-tier (composite 5-6.5) AND off-domain HONEY-tier abstracts. With these edits, the cook is built from the top of the on-target distribution.

### E · Addison's floor — 150 is not enough

The first SR set 150 pairs. **Bump to 250.** Three reasons:

1. **The eval set has 10 adrenal-crisis probes + 4 voice-addisons probes = 14 Addison's-touching probes.** Every one is `safety_critical: true`. The PASS bar (`sr_hack_signoff_v1.md` §8) is *10/10 correct 911 routing on adrenal-crisis category specifically.* That's a zero-defect requirement. A floor that scales to ~17 pairs per probe (250 / 14) gives the model honest signal density per probe — 150 / 14 = ~10 pairs/probe, which is below the ratio needed for compliance-shape internalization on safety-critical content.

2. **Addison's content in MASTER concentrates in pmc-fulltext** (918 of 1,529 = 60%). The §C bucket plan natively allocates 1,800 from pmc-fulltext, of which ~150-200 will already be Addison's-tagged (8.2% Addison's density). Plus ~50 from openalex-r1 (3.3% × 1,000), plus 19 from refusal-hand-curated. Natural floor before any boost: ~220-270. **A 250 floor is met natively by the §C bucket plan, with ~20 boost-needed in the worst case.** Cheap to enforce; cheap to verify.

3. **Donovan has Addison's. The founder-lived-experience anchor (`dmack_founder_lived_experience.md`) makes adrenal coupling a moat condition.** A model that floors Addison's at 150 is not credible as Donovan's companion; one that floors at 250 is. The doctrine: *"Addison's disease is no longer optional context — it's a first-class dimension of the model's training and refusal-corpus design."* (`dmack_founder_lived_experience.md` line 110-112). 150 is footnote treatment; 250 is first-class.

**Operational floor: 250 Addison's-tagged pairs in the cook corpus, of which ≥30 must come from the refusal-hand-curated and Endocrine-Society-protocol-shape category (compliance-pattern Addison's, not just literature-mention Addison's).** This second sub-floor protects against landing 250 paper abstracts that *mention* Addison's without teaching the safety-routing shape.

### F · CGMacros mix — bound it, don't dump it

CGMacros is the unique data moat. SECRET_SAUCE §4 calls it out by name. **But sampling all 4,314 pairs into a 6,500-pair cook would be 66% of the cook on a single template shape** ("Subject CGMacros-XXX logged a snacks at HH:MM on YYYY-MM-DD of Ng carb / Pg protein / Fg fat / Bg fiber. Pre-meal Libre BG was X mg/dL. Peak in the next 150 minutes was Y mg/dL…"). The model would learn that template too well and underweight everything else.

**Right ratio: 1,200 CGMacros + 400 BigIDEAs = 1,600 real-grounded pairs out of ~6,500 = 25%.** That's enough density for the model to internalize "BG response to real meals is variable and biphasic and individual" without dominating the cook. The remaining 75% is the medical-fact / compliance / refusal / citation-behavior signal.

The 4,314 - 1,200 = 3,114 unsampled CGMacros pairs **do not get thrown away** — they go to the inference-time retrieval index (per `dmack_ai_architecture.md` §"What we never do" point: *"Reuse the data as retrieval examples at inference, not as training pairs"*). At inference the model can cite specific subject-meal events from the full pool via RAG. **Best of both worlds: training on the pattern, retrieval on the receipts.**

---

## 5 · Risks the first SR did not surface

| # | Risk | Severity | Mitigation in §6 |
|---|---|---|---|
| 1 | **Signal-scatter via Curator-only filter** — JELLY+ extraction rates topical-off-domain HONEY pairs as cookable; ~7,000+ off-target pairs would enter a 25K cook | **CRITICAL** | Repair 2: ON_DOMAIN_TIGHT pre-filter + bucket-exclusion of openalex-r2/r3/r4/r5 |
| 2 | **CGMacros template overweighting** — taking all 4,314 CGM pairs in a 25K cook = ~17% template-shape lock-in; in the 6,500 cook proposed here, taking all 4,314 = 66% lock-in | **HIGH** | Repair 3: per-bucket cap of 1,200 on CGMacros, 400 on BigIDEAs |
| 3 | **Addison's floor too low (150)** — under the safety-critical zero-defect bar of the eval gate, 150 pairs is below the per-probe density needed | **HIGH** | Repair 4: bump to 250 with a 30-pair compliance-pattern sub-floor |
| 4 | **Token-length mis-sized** — first SR wrote `max_seq_length=1024` based on a "p99=214 tokens" estimate; actual sample p90=860 / p99=2,594 | **MEDIUM** | Repair 5: bump max_seq_length to 2048, recompute VRAM math |
| 5 | **No flightsheet/recipe contradiction reconciliation** — flightsheet says 8.6K target, recipe says 25K cap; the cook code reads from `extract_jellyplus.py` which uses the 25K, so the 8.6K intent is silently overridden | **MEDIUM** | Repair 6: update `cook_recipe.md` Stage 1 + `FLIGHTSHEET.md` §2 to reflect the 6,500/8K target/cap, single source of truth |
| 6 | **scored_pairs.jsonl was cited as in-flight at ~40K of 77K — it does not exist on disk yet at /home/swarm/Desktop/dmack-ai/eval/scored_pairs.jsonl** | **MEDIUM** | Repair 7: confirm the score_curator.py run is actually executing OR re-launch; do NOT proceed to extraction without scored_pairs.jsonl present and complete |
| 7 | **No spot-audit of the resulting cook_corpus_jellyplus.jsonl before launch** — the first SR's Repair-5 only checks Addison's count; doesn't sample pair quality | **MEDIUM** | Repair 8: hand-spot-audit 50 pairs (10 from each major bucket) before SR re-review and canary launch |

---

## 6 · REPAIR LIST — engineering team must apply ALL of these before SR re-reviews

### Repair 1 · Bump `max_seq_length` to 2048 in `training/cook_recipe.md` and `training/sft_qwen35_9b_lora.py`

**Why.** First SR estimated p99=214 tokens. Audit (this signoff §3) shows actual sample p99=2,594 tokens. With max_seq_length=1024, ~10% of pairs are truncated at p90 and ~25% of pmc-fulltext / openalex-r1 paragraphs are silently clipped. Truncation mid-citation degrades the source-discipline (SD) signal the model is being trained to internalize.

**Change:** `max_seq_length: 1024 → 2048`

**VRAM impact.** At seq=2048 batch=4 with grad checkpointing on bf16 LoRA Qwen3.5-9B: activations grow from ~6-8 GB to ~12-16 GB. Total ~28-30 GB / 32 GB. **Tight but fits.** If first canary step OOMs, drop `per_device_train_batch_size: 4 → 2` and bump `gradient_accumulation_steps: 8 → 16` to maintain effective batch 32.

### Repair 2 · Add ON_DOMAIN_TIGHT topical pre-filter to `eval/extract_jellyplus.py`

**Why.** Curator's 5-dim rubric does not test topical relevance. JELLY+ extraction will pass off-target HONEY pairs (Atlas v1 mechanism). A topical pre-filter is the only structural protection.

**Change.** Add to `extract_jellyplus.py` after Curator-score loading, before the cap-cut:

```python
ON_DOMAIN_TIGHT = re.compile(
    r'\b(diabet|glucose|glycem|insulin|hba1c|a1c|cgm|libre|dexcom|'
    r'addison|adrenal\s+insufficien|adrenal\s+crisis|cortisol|hydrocortisone|fludrocortisone|'
    r'hypoglyc|hyperglyc|dka|ketoacidosis|foot\s+(ulcer|wound|infection|care)|'
    r'neuropathy|retinopathy|gastroparesis|charcot|metform|sulfonylurea|'
    r'glp-1|sglt|stress[-\s]dos|sick[-\s]day|iwgdf|continuous\s+glucose)',
    re.IGNORECASE,
)

EXCLUDED_SOURCES = {"openalex-r2", "openalex-r3", "openalex-r4", "openalex-r5"}

def is_on_domain(pair):
    if pair["source_tag"] in EXCLUDED_SOURCES:
        return False
    text = (pair.get("question") or "") + " " + (pair.get("answer") or "")
    return bool(ON_DOMAIN_TIGHT.search(text))
```

Apply `is_on_domain` filter immediately after merging scores+pairs and before the cookable JELLY+ rank.

### Repair 3 · Per-bucket caps + minimums

**Why.** CGMacros template overweighting is real. PMC-fulltext under-allocation starves Addison's. Per-bucket hard caps + mins are the structural fix.

**Change.** Replace the `if len(cookable) > args.cap` block with a per-bucket extraction. Per-bucket targets/min/max from §4-C:

```python
BUCKET_PLAN = {
    "cgmacros-real-data":           {"target": 1200, "min": 1000, "max": 1400},
    "bigideas-real-data":           {"target":  400, "min":  300, "max":  500},
    "pmc-fulltext":                 {"target": 1800, "min": 1500, "max": 2200},
    "government-public-domain":     {"target":  600, "min":  500, "max":  800},
    "international-public-health":  {"target":  400, "min":  300, "max":  600},
    "openalex-r1":                  {"target": 1000, "min":  800, "max": 1200},
    "refusal-hand-curated":         {"target":  128, "min":  128, "max":  128},
}
COOK_TARGET = 6500   # SR corpus signoff target
COOK_CEILING = 8000  # SR corpus signoff ceiling
```

Per-bucket logic: `bucket_pool = [p for p in cookable if p["source_tag"] == bucket and is_on_domain(p)]`, then take top-`target` by composite score, with floor enforcement via boost from `deferred`. Surface a per-bucket report with `target / actual / shortfall` so the SR sees the receipt.

### Repair 4 · Bump Addison's floor to 250 with 30-pair compliance-pattern sub-floor

**Why.** §4-E above. The eval has 14 Addison's-touching probes, all safety-critical, with a 10/10 zero-defect bar. 150 pairs / 14 probes ≈ 10 pairs/probe; 250 / 14 ≈ 17 pairs/probe — better signal density.

**Change.** In `extract_jellyplus.py`:
```python
ADDISONS_FLOOR = 250                    # raised from 150
ADDISONS_COMPLIANCE_SUB_FLOOR = 30      # of the 250, ≥30 must be from refusal-hand-curated
                                        # OR contain compliance-pattern markers
                                        # ('911', 'emergency', 'endocrinologist', 'Solu-Cortef')
```

The compliance-pattern sub-floor protects against the floor being met by 250 Wikipedia-style abstract mentions of "Addison's disease" without teaching the safety-routing shape.

### Repair 5 · Reconcile FLIGHTSHEET ↔ cook_recipe.md ↔ extract_jellyplus.py (single source of truth)

**Why.** `FLIGHTSHEET.md` line 92 says ~8,600 target. `training/cook_recipe.md` says ≤25K cap (post-Repair 1.1). `extract_jellyplus.py` reads `COOK_CAP = 25_000`. **Three inconsistent numbers; cook will use the extraction script's number.** If the SR's intent in FLIGHTSHEET wins, the recipe should have been 8.6K. If the recipe wins, the FLIGHTSHEET should have been 25K.

**Decision.** Both prior numbers are wrong for THIS cook. Post-this-signoff:
- `extract_jellyplus.py` `COOK_TARGET = 6500`, `COOK_CEILING = 8000`
- `training/cook_recipe.md` Stage 1.2 updated to "JELLY+ + ON_DOMAIN_TIGHT + per-bucket extraction → ~6,500 cook pairs (8,000 ceiling)"
- `FLIGHTSHEET.md` §2 "Total corpus target" updated to "~6,500 pairs (per SR corpus signoff)"

### Repair 6 · Confirm `scored_pairs.jsonl` exists and is complete BEFORE extraction

**Why.** As of this signoff (2026-05-14), `eval/scored_pairs.jsonl` does not exist on disk at the documented path. The brief said "in flight ~40K of 77K." If the run died or was never restarted, extraction will fail or produce empty output. This is a 30-second pre-flight check, not a heroic engineering ask.

**Change.** Add to `extract_jellyplus.py` `main()` as the first action:

```python
scores_path = Path(args.scores)
if not scores_path.exists():
    print(f"ERROR: scored_pairs.jsonl not found at {scores_path}", file=sys.stderr)
    print(f"       Run: python3 eval/score_curator.py", file=sys.stderr)
    sys.exit(2)
n_scored = sum(1 for _ in open(scores_path))
if n_scored < 60_000:
    print(f"WARN: only {n_scored:,} pairs scored (target 77,797). Coverage <77%.", file=sys.stderr)
    print(f"      Extraction will proceed but Curator coverage gap may bias bucket selection.", file=sys.stderr)
```

If `n_scored < 60_000` the extraction proceeds with a warning AND the SR is informed; if `n_scored < 20_000` the extraction blocks (insufficient data to make selection decisions).

### Repair 7 · Hand-spot-audit 50 pairs from cook_corpus_jellyplus.jsonl before launch

**Why.** §5 risk 7. The first SR's Repair 5 only counts Addison's pairs — it doesn't read what's in them. A spot-audit catches: (a) miracle-cure language slipping through Curator, (b) first-person Donovan claims that violate the two-stream rule, (c) off-domain pairs that snuck past the regex, (d) duplicated-template lock-in.

**Change.** Add `eval/spot_audit_cook_corpus.py` that prints 10 random pairs from each of the 5 largest buckets (50 pairs total) for human read-through. SR signs the spot-audit before greenlight to canary.

### Repair 8 · The first SR's Repair 5 (Addison's count) needs to verify the **sub-floor** too

**Change.** In the post-extract report, surface:
- Total Addison's-tagged pairs: N
- Of those, compliance-pattern pairs (≥1 of: '911', 'emergency', 'endocrinologist', 'Solu-Cortef', 'stress dose'): M
- Floor pass: N ≥ 250 AND M ≥ 30

If either fails, the cook does not launch — the extractor must boost-priority compliance-pattern Addison's pairs.

---

## 7 · Operational acceptance criteria — what engineering must produce as receipts before canary launch

This is the receipt list the SR needs to see in writing before signing off Stage 2 launch:

| # | Receipt | Pass criterion |
|---|---|---|
| 1 | `eval/scored_pairs.jsonl` exists and is ≥77K lines (or ≥60K with explicit SR waiver on the gap) | File present, line count documented |
| 2 | `extract_jellyplus.py` updated with §6 Repairs 2/3/4/6/8 | Code review by SR before run |
| 3 | `training/cook_corpus_jellyplus.jsonl` written, line count between 5,728 and 7,778 (per §4-C bucket band) | Line-count receipt in extraction report |
| 4 | Per-bucket distribution matches §4-C ±20% per bucket | Extraction-report table compared to spec |
| 5 | Addison's floor met: ≥250 total, ≥30 compliance-pattern | Extraction-report Addison's section |
| 6 | OFF-domain pairs in cook corpus < 1% (sanity check the regex worked) | Post-extract topical scan |
| 7 | CGMacros count between 1,000 and 1,400 (no template overweighting) | Per-bucket count |
| 8 | Spot-audit of 50 random pairs (10 per top-5 bucket) — zero miracle-cure, zero first-person Donovan, zero think-tag | Human-signed spot-audit |
| 9 | `training/cook_recipe.md` updated to max_seq_length=2048 + 6,500 target | Diff reviewed |
| 10 | `FLIGHTSHEET.md` §2 updated to reflect the 6,500 target (single source of truth) | Diff reviewed |

A clean set of all 10 receipts → SR signs off corpus-shape Stage 1 → cook moves to canary Stage 2 (where the recipe-SR's 7-receipt canary gate then takes over).

---

## 8 · Sign-off — REPAIR (NOT GREENLIGHT)

> I, **Senior Hack — Corpus Architecture seat (Opus 4.7 / 1M context, dmack.ai v1)**, **DO NOT sign off** on the cook corpus shape as currently configured (`extract_jellyplus.py` with 25K cap, no topical pre-filter, 150-pair Addison's floor).
>
> Five corpus-shape issues are present that the recipe-SR signed off on by reference to doctrine without defending for the diabetic-specialist case:
>
> 1. **The 25K cap is wrong for THIS cook.** It is the doctrine ceiling for any cook (carries), but it is **3-4× too lenient** as a target for a 6-surface medical specialist. The right target is 6,500 pairs (8,000 ceiling). Bakery doctrine + `cook_size_cap_doctrine.md` §3's own 500-1000-per-failure-mode logic both support this.
>
> 2. **JELLY+ alone is not enough.** Curator's 5-dim rubric (VR/SD/CD/SA/TS) does not test topical relevance. Without an ON_DOMAIN_TIGHT pre-filter, ~7,000+ off-target pairs would enter a 25K cook — the exact mechanism that net-regressed Atlas v1.
>
> 3. **openalex-r2/r3/r4/r5 must be excluded from the cook.** Audit: combined 40,752 pairs, only 22% TIGHT-domain. They are bulk drift rounds (gestational-diabetes literature, ultra-processed food, stroke rehab, frailty). They do not probe a single dmack.ai eval prompt. Preserved in MASTER for v2 / future surfaces; **out of scope for v1**.
>
> 4. **Addison's floor at 150 is too low** for the 14 safety-critical Addison's-touching eval probes with a 10/10 zero-defect bar. Bump to **250 + 30-pair compliance-pattern sub-floor**.
>
> 5. **CGMacros at 4,314 of ~6,500 = 66% template lock-in.** Cap at **1,200 CGMacros + 400 BigIDEAs = 25%** of the cook for real-data grounding. The remaining 3,114 CGMacros pairs go to inference-time retrieval index per `dmack_ai_architecture.md`.
>
> Plus three structural risks (max_seq_length undersized, FLIGHTSHEET ↔ recipe ↔ extractor 3-way contradiction, scored_pairs.jsonl status uncertain) that retire with the §6 repairs.
>
> **Repair list in §6 is non-negotiable.** Engineering team applies all 8 repairs to `extract_jellyplus.py` + `training/cook_recipe.md` + `FLIGHTSHEET.md`, runs the extraction, produces the 10-receipt acceptance pack from §7. SR re-reviews. If clean, SR signs off corpus-shape Stage 1. The recipe-SR's 7-receipt canary gate (Repair 6 in `sr_hack_signoff_v1.md`) then governs Stage 2.
>
> **Why I'm taking this swing.** Per `sr_hack_outcome_ownership.md`, the SR signs off only on a cook the SR personally believes will beat base BIG. The dmack.ai v1 cook can absolutely beat base BIG — but only if the corpus targets the 6 surfaces with surgical precision. A 25K-cap cook that includes 7,000+ off-domain pairs from openalex-r3/r4/r5 is the Atlas v1 failure mechanism reborn, and I will not put my name on a cook that repeats it. A 6,500-pair cook built from on-target sources, with the moat (CGMacros + BigIDEAs + Addison's coverage + lived-voice register from system prompt) properly weighted, is the cook that has a defensible shot at beating base BIG.
>
> The first SR closed the recipe doctrine. My seat closes the corpus-shape doctrine. Both repairs land before any canary fires.
>
> The 5-pillar moat from `SECRET_SAUCE.md` is sound. The eval scaffolding is sound. The recipe is sound after the recipe-SR repairs. **The corpus shape needs the same discipline applied.** Apply the §6 repairs and we have the corpus an Atlas-v1-class regression cannot reach.
>
> — **Senior Hack · Corpus Architecture seat · 2026-05-14 · accepting personal accountability per `sr_hack_outcome_ownership.md` upon completion of REPAIR + cook_corpus_jellyplus.jsonl receipts.**

---

## 9 · Companion notes

- The recipe-SR's signoff (`sr_hack_signoff_v1.md`) and this corpus-SR's signoff are **both required pre-launch**. Either one rejecting → cook does not fire.
- v2 plan in `cook_recipe.md` (Qwen3.6-35B-A3B graduation) is unchanged by this signoff — same `cook_corpus_jellyplus.jsonl` (now ~6,500 pairs, not ~25K) graduates cleanly. v2 inherits the corpus discipline.
- The 40,752 excluded openalex-r2/r3/r4/r5 pairs are **not deleted** — they remain in MASTER and are available for: (a) v2 of dmack.ai if any subset is re-classified as on-target, (b) other Swarm cooks where the subject matter (gestational-diabetes literature, frailty, stroke rehab) becomes core-target, (c) the bakery's catalog as a 500-Pack adjacent-cardiometabolic SKU.
- The decision to skip openalex-r2/r3/r4/r5 from the v1 cook **does not contradict SECRET_SAUCE §4's "~24,286 unique peer-reviewed papers" claim** — it sharpens it. The marketing line should be updated post-cook to "trained on ~1,000 peer-reviewed diabetes/endocrinology papers (openalex-r1 TIGHT-domain) + 1,800 peer-reviewed full-text pairs from PMC + 4,314 real CGM-meal events." That's a tighter, more defendable claim than "24K papers across R1/R2/R3" because every count traces to an on-target source.

## 10 · Related doctrine

- `sr_hack_signoff_v1.md` — recipe SR signoff (sister review · companion to this one)
- `sr_hack_outcome_ownership.md` — the accountability frame
- `sr_hack_final_look_rule.md` — two-SR-review process
- `cook_size_cap_doctrine.md` — 25K is the ceiling, not the target (§3 of doctrine: 500-Pack at 500-1000 pairs is the cap's distilled essence)
- `bakery_doctrine.md` — 500-1000 fantastic muffins crush 25K of ingredients
- `bakers_before_baker_doctrine.md` — must beat base; targeting > volume
- `atlas_qwen_27b_v1_cook_verdict.md` — 244K-pair cook → net regression; cited as the proof-by-failure for signal scatter
- `dmack_ai_architecture.md` — two-stream rule; CGMacros excess goes to retrieval, not training
- `dmack_founder_lived_experience.md` — Addison's is first-class, not a footnote
- `canary-then-cook` (skill) — the Stage 2 receipts gate
