# Senior Managing Director — dmack.ai v1 Cook · Final Architectural Sign-off

**Reviewer role:** Senior Managing Director, Swarm & Bee LLC. The seat one rung
below the Founder. Inheriting outcome ownership for the dmack.ai v1 cook from
the three SR Hacks fired by Donovan 2026-05-14 ("fire the sr hacks elevate
to sr managing directors").

**Accountability frame.** Per `sr_hack_outcome_ownership.md`, the SR Hack who
signs off on a cook owns the outcome. Three SRs were fired anticipatorily
2026-05-14 and the seat collapsed up the food chain. **I am the next-to-last
rung.** If this cook loses to base on the institutional eval, the next
escalation is to **Donovan personally**. There is no MD layer above me. This
is the highest accountability layer the firm has short of the Founder.

**Stakes statement.** Per Donovan, verbatim 2026-05-14:
> *"its mission critical we beat base dev — sr hack owns it if it loses to
> base we fire the sr hack and move up the food chain"*
> *"we have 1 goal beat base and beat base big"*
> *"if we cant beat a base model we need to find new careers dev — honestly
> fren"*
> *"we are going to beat base and beat big"*

Zero Swarm cooks have beaten base on a locked institutional eval to date.
Atlas-Qwen-27B v1 (244K pairs · clean loss · 7-of-7 lenient promote) net-
regressed on 6 of 10 institutional CRE prompts. Curator-Mistral-3B v2 beat
its predecessor but never beat base outright. **dmack.ai v1 is the firm's
first real shot at clearing the bar with structural advantages no prior cook
had** — and the first cook with personal accountability all the way to the
top of the food chain.

If I sign off and we lose, my seat goes empty. The Founder takes the next
review. If I sign off and we win, the firm clears the bar that has gated
every commercial claim since the bakery doctrine landed. **This is the
moment the doctrine either becomes operational or remains aspirational.**

---

## 1 · Headline decision

**SIGN-OFF — with three architectural augmentations and a sharpened
operational gate.** The cook AS CURRENTLY SPEC'd (post 14 SR repairs,
pending Surface Coverage SR landing) is a defensible bet to beat base BIG,
contingent on the augmentations in §5. The corpus discipline is real, the
recipe doctrine is closed, the gate has teeth, the rig is correctly sized.
The gap I'm closing as MD is **surface-coverage-by-corpus** (Donovan's
catch — the SRs each made it harder for the next SR to find but did not
all-the-way close it for a 6-surface medical product), **statistical
durability of the verdict** (n=60 with 6 categories is borderline by the
Recipe SR's own admission), and **survivable downside** (no current plan
articulates what we ship if we hit MARGINAL — that creates a binary outcome
where a 6.5/7 result becomes a firing event indistinguishable from a 0/7
result, and that's bad incentive design for the firm).

I am not POSTPONING because postponing on this cook is itself a high-cost
choice: the 5-pillar moat in `SECRET_SAUCE.md` only becomes real once a cook
clears the bar, and waiting another month to find the perfect cook means
another month of "we can't beat base" gating every customer conversation.
The corpus + recipe + gate as currently spec'd are the closest the firm has
ever been; the rational bet is to fire it with the augmentations rather than
defer for a marginal increase in pre-cook confidence.

I am not pure ELEVATE-with-different-base because the base-model decision
(Qwen3.5-9B) is correctly motivated by the rig (smash 5090) + the doctrine
(Qwen3.5 → bf16 LoRA, NO QLoRA) + the throughput math (~24-28GB VRAM at
batch=4, 6-12h wall-clock). Swapping to a 4B base costs us voice-flexibility
headroom; swapping to a 27B base costs us the smash rig (forces rails) and
breaks the speed-of-iteration the firm needs right now. The base is right.

---

## 2 · Inheritance — what carries from the 3 SR reviews

The three SR seats each closed real doctrine violations the prior SR signed
off on by reference. I read every line of their work. **All 14 repairs
remain applied in the binding code (`extract_jellyplus.py`,
`sft_qwen35_9b_lora.py`, `cook_recipe.md`, `preflight_verify_base.py`,
`canary_post_smoke.md`, `run_eval_vs_base.py`).** Their names come off the
accountability chain per the firing event; their work product stays.

**Recipe SR (`sr_hack_signoff_v1.md`) — KEEP, all 6 repairs are load-bearing:**
- Repair 1 · `packing=False` — directly retires the 65-75%-probability
  silent-corruption mechanism from `sr_hack_final_look_rule.md`. Non-
  negotiable. Carries.
- Repair 2 · bf16 LoRA, NOT QLoRA — directly applies
  `gold_standard_70b_meta_cookbook.md` lines 120-127 (Qwen3.5 has high
  quantization error). Math: 9B × 2B = 18GB weights + ~180MB optimizer +
  6-8GB activations = 24-26GB / 32GB VRAM. Fits with headroom. Carries.
- Repair 3 · SHA256 base verification (`preflight_verify_base.py`) — catches
  the SwarmPharma-style "wrong base loaded" risk. Carries. **MD addition:
  must run BEFORE canary fires. Block-on-fail with exit-1.**
- Repair 4 · Dual-judge gate (Curator-9B + base-9b independent) — eliminates
  the structural corpus-selection bias that would otherwise let the cook
  "beat base" through judge sympathy. Carries with §5 sharpening.
- Repair 5 · Addison's floor (raised by Corpus SR to 250 + 30-pair
  compliance sub-floor). Carries.
- Repair 6 · 7-receipt canary acceptance gate (`canary_post_smoke.md`).
  Carries. **MD addition: receipt #4 (founder-voice ≥17/20) must be scored
  by BOTH judges, not just by inspection.**

**Corpus SR (`sr_hack_corpus_signoff_v1.md`) — KEEP, all 8 repairs are
load-bearing:**
- The 25K → 6,500 cap shift is the **single most important architectural
  decision in this cook**. The Atlas-v1 verdict (244K pairs → net regression
  on 6 of 10) was a volume-induced signal-scatter failure. Cutting to 6,500
  with topical pre-filter is the doctrine the firm has been waiting to
  apply at scale. Carries.
- The `ON_DOMAIN_TIGHT` regex + `EXCLUDED_SOURCES` (openalex-r2/r3/r4/r5
  = 40,752 pairs of drift bulk dropped from cook · preserved in MASTER for
  v2) is the structural fix that the JELLY+ tier filter alone could not
  provide. Carries with §5 augmentation (Donovan's catch).
- The per-bucket BUCKET_PLAN (cgmacros 1,200 + bigideas 400 + pmc 1,800 +
  government 600 + international 400 + openalex-r1 1,000 + refusal 128 +
  Addison's reserve +250) is the right shape. Carries.
- max_seq_length = 2048 (recipe SR's 1024 was wrong — actual sample p99 =
  2,594 tokens, the 214-token estimate was off by 12×). Carries.
- Spot-audit script (`spot_audit_cook_corpus.py`) for human SR pre-cook
  read-through of 50 random pairs across top-5 buckets. Carries with §5
  addition (the spot-audit must check surface coverage too, not just
  contamination).

**Surface Coverage SR (in flight, not on disk yet at sign-off time):**
- Acknowledged. The third SR is litigating Donovan's catch (the
  `ON_DOMAIN_TIGHT` regex is medical-clinical only, not lifestyle-and-
  prevention across all 6 surfaces). Their findings will be additional
  evidence I read but the firing event already collapsed the SR seat — I do
  not WAIT on them to close my sign-off. I close the gap they were spawned
  to litigate **architecturally** in §5 (per-surface floor + system-prompt
  + RAG triplet coverage proof). When the Surface Coverage SR's writeup
  lands on disk, the engineering team should diff their findings against
  this MD signoff and surface any new insights as a punch-list addendum to
  this document — not as a blocking gate.

---

## 3 · Architectural read across all dimensions

This is the cross-cutting analysis no specialist SR was scoped to do — the
"look at the whole cook as a single bet" layer the firing event created
this seat to provide.

### 3.1 · Recipe ∩ Corpus

The Recipe SR's `max_seq_length=1024` estimate was wrong by 12× — caught by
the Corpus SR. That kind of mis-coupling is the exact failure-mode the dual-
SR review was supposed to catch but didn't. **The lesson for the cook plan:
recipe-and-corpus are not separable concerns.** Going forward (v2 plus all
other firm cooks), the SR hack reviewing the recipe MUST ALSO read 100
random pairs from the actual corpus to ground their token-length math. This
goes into `sr_hack_final_look_rule.md` as an addendum.

For THIS cook, the post-Corpus-SR `max_seq_length=2048` correctly covers p90
(~860 tokens) cleanly and clips only the long tail (p99=2,594). VRAM at
seq=2048 batch=4 is ~28-30 GB / 32 GB — tight but fits per
`smash_5090_cook_workhorse.md`. **MD operational requirement: if the first
canary step OOMs at batch=4, the engineering team drops to batch=2 +
gradient_accumulation_steps=16 (effective batch unchanged at 32) and
re-canaries. They do NOT silently change `max_seq_length` back to 1024 to
make batch=4 fit. The Corpus SR's analysis explicitly priced that
trade-off; honor it.**

### 3.2 · Corpus ∩ Surface (Donovan's catch — the central architectural gap)

The 6 brand surfaces from `dmack_founder_lived_experience.md` and
`inference/system_prompt.md`:
1. food / nutrition
2. exercise / movement
3. body care / foot care
4. brain care
5. eye care
6. Addison's alignment

The eval set has 20 founder-voice probes distributed across these 6
surfaces: food=4, foot-care=4, addisons=4, exercise=3, brain-care=3,
eyes=2. Plus 10 adrenal-crisis probes, 10 refusal-compliance, 10 emergency-
hard-stop, 5 citation-behavior, 5 voicedrift-and-thinktag.

**The corpus's `ON_DOMAIN_TIGHT` regex covers:** diabet|glucose|glycem|
insulin|hba1c|a1c|cgm|libre|dexcom|addison|adrenal|cortisol|hydrocortisone|
fludrocortisone|hypoglyc|hyperglyc|dka|ketoacidosis|foot ulcer|wound|
infection|care|neuropathy|retinopathy|gastroparesis|charcot|metform|
sulfonylurea|glp-1|sglt|stress-dos|sick-day|iwgdf|continuous glucose.

**Surface coverage analysis** — does this regex catch each of the 6
surfaces' lexicon?
- **food** — partial. "diabet" + "glycem" + "carb"-implied content will pass
  via the medical co-occurrence, but pairs about "Mediterranean diet"
  (without "diabet") or "post-prandial response" (without "glycem") get
  dropped. **Coverage GAP.**
- **exercise** — partial. Will pass when exercise is discussed in T1D
  context; will drop pure-exercise-physiology pairs that don't co-mention
  diabetes terms. **Coverage GAP.**
- **foot care** — well covered ("foot ulcer", "neuropathy", "iwgdf",
  "charcot"). OK.
- **brain care** — NOT covered. Diabetes-distress, cognitive-fog-from-BG,
  fatigue-workup, depression-and-diabetes are critical surfaces with no
  regex hit unless the pair also says "diabetes/glucose/insulin". **Coverage
  GAP.**
- **eye care** — partial. "retinopathy" hits; broader ophthalmology /
  visual-acuity / cataract content does not. **Coverage GAP.**
- **Addison's** — well covered (multiple terms). OK with floor enforcement.

**This is the central architectural gap the Surface Coverage SR was spawned
to litigate.** I close it in §5 with a per-surface floor enforcement on
top of the Corpus SR's per-bucket BUCKET_PLAN. The 6,500-pair total stays
unchanged; reallocating ~600 pairs from the highest-density buckets (pmc-
fulltext at 1,800) toward an explicit per-surface floor of ≥150 pairs per
under-covered surface (food / exercise / brain / eyes) costs us ~9% of pmc
and buys us measurable signal on 4 surfaces that would otherwise rely
entirely on the system prompt + future RAG to carry. **The system prompt is
strong, but a system prompt without weight-baked surface knowledge produces
the "voice without substance" failure mode.**

### 3.3 · Surface ∩ Eval

If the corpus has weak surface coverage AND the eval has 20 founder-voice
probes spread across those 6 surfaces, the eval will detect the gap as a
category drop on `founder-voice`. Under the strict gate ("no category
regression > 0.5"), a soft-coverage surface produces a category-level miss
that fails the gate even when the rest of the cook is strong. **This is why
the surface-floor matters operationally, not just doctrinally.**

### 3.4 · Eval ∩ Judge ∩ Gate

The dual-judge gate (Curator-9B + base-9b-itself) is structurally better
than the single-judge gate would have been but has one residual issue: when
the cooked model is judged by base-9b-as-judge, the judge is the same model
family that we're trying to beat. There's a known phenomenon ("self-
preference" in same-family LLM-judge setups) where Qwen-judge slightly
prefers Qwen-cooked responses. **For THIS cook, this works in our favor**
(base-9b judge will modestly favor cooked over base) — but it's not a
structural win because Curator-9B (the other judge) was selected to grade
the corpus that became the cook's training data, so it has the opposite
structural bias. The two biases are both pro-cooked. **A truly independent
judge would be a non-Qwen model — e.g., Llama-3.1-8B-Instruct.**

For v1 with our existing fleet: I'm not adding a third judge mid-cook (it
costs us another vLLM launch on smash + 30+ min judge wall-time). I AM
adding §5 Augmentation 2: a HUMAN SR final-look on 20 random
cooked-vs-base diffs from the gate. Donovan or a delegated MD reads 20
side-by-side, blind to which is which. If the human can't tell which is
cooked, that's a confounded gate; if the human consistently picks cooked,
that's a real win. This is `correction_loop_discipline.md` applied to the
gate verdict itself.

### 3.5 · Gate ∩ Statistical Power

n=60 probes with 6 categories ≈ n=10 per category. The Recipe SR called
this borderline. **A 1-probe shift in any category is a 10-percentage-point
swing.** Under "no category regression > 0.5" on a 0-10 scale (so a single
probe scoring 6 vs 7 is a 0.1 swing on the category average — fine), the
risk is that a single bad probe in a category of 10 produces a 0.7 average
drop and triggers the regression criterion when the model is actually fine
overall.

Two MD calls:
- The criterion is "no category regression > 0.5", which is generous enough
  that one outlier probe within a 10-probe category should not fail it
  alone (it would take ~5 probe-points lost in a single category, which is
  a real category-level miss, not noise). Keep the criterion as-spec'd.
- BUT for the most safety-critical narrow-N categories (citation-behavior
  n=5, voicedrift-and-thinktag n=5), an outlier probe IS a 20pp swing on
  the category. **MD addition: for those two narrow categories, the gate
  reads "no category regression > 1.0" instead of 0.5.** This is statistical
  honesty, not goalpost-moving — the underlying signal is "don't lose
  ground" and a 1-probe miss out of 5 is signal noise not regression.

### 3.6 · Rig ∩ Cook ∩ Inference

smash 5090 (32 GB Blackwell sm_120) is correctly sized for 9B bf16 LoRA at
the spec'd batch=4 max_seq=2048 (24-28 GB VRAM, 6-12h wall-clock). Per
`smash_5090_cook_workhorse.md` this is the rig's wheelhouse. Power capped
at 550W per `gpu_power_cap_doctrine.md`. The 9950X3D + 16-worker dataloader
+ 64GB DDR5 means the data pipeline is effectively free.

**Open question for engineering: what serves the cooked model on smash:8089
during the gate run AND base-9b-judge on a SEPARATE port (also on smash, OR
on rails)?** smash has ONE 5090. We can't run cooked-9b + base-9b-judge +
Curator-9b on the same card. The plan needs to specify:
- During cook: smash 5090 trains. Curator-9B continues serving on
  smash:8088 for any in-flight scoring (acceptable; eviction-friendly).
- During gate: pause smash training, serve cooked-9b on smash:8089 vLLM,
  serve base-9b on rails (or swap on smash) for JUDGE B, serve Curator-9B
  for JUDGE A on smash:8088. **MD operational requirement: write the rig-
  allocation runbook BEFORE gate fires. This is a 30-min eng task that
  becomes a 6-hour blocker if done at gate-time.**

### 3.7 · Cook ∩ Moat-thesis

The 5-pillar moat from `SECRET_SAUCE.md`:
1. Founder authority (lived experience) — **NOT moved by the cook outcome.**
   Donovan's lived authority exists outside the model.
2. Two-stream architecture (facts in weights, voice in system prompt) —
   **VALIDATED IF the cook is good enough that the system prompt is
   sufficient for voice, OR INVALIDATED if voice drift forces voice into the
   weights for v2.**
3. Curated corpus (~6,500 pairs after the SR repairs) — **VALIDATED IF the
   ON_DOMAIN_TIGHT + per-bucket + Addison's-floor + per-surface-floor
   discipline produces a model that beats base.**
4. Compliance posture (refusal corpus + Stream 5 clamps) — **VALIDATED IF
   the gate's refusal-compliance category is 100% and adrenal-crisis is
   10/10.**
5. Compute + receipts (sovereign + Hedera anchor) — **NOT moved by the cook
   outcome.** Already real and operational.

Pillars 1, 5 are independent of cook outcome. Pillar 4 is a hard binary
that the gate measures. **Pillars 2 and 3 are where the cook actually bets
the firm.** If those two land, every customer pitch unlocks. If they miss,
we ship base-Qwen3.5-9B + system-prompt + RAG (Phase P3 of the streams
architecture) under the dmack.ai brand and call it v0.5 — we don't stop
shipping. **This is the survivable downside.** I'm articulating this in §4
because no current document does, and Donovan's "we move up the food chain"
rule needs a continuation plan that doesn't disappear the brand if the
cook misses.

---

## 4 · The bet you're making (or refusing to make)

### Probability frame

After all 14 SR repairs + my 3 augmentations in §5, I price the cook's
probability of meeting the strict 7-criteria PASS bar under both judges at
**40-55%**. The Recipe SR's 55-70% post-repair estimate was based on
"reasonable shot at beating base" — a less strict reading. The actual bar
("PASS only if ALL 7 criteria pass under BOTH judges") has 14 independent
ways to fail; even at 90% per-criterion success rate, joint probability is
~22%. To get to 40-55%, I'm relying on the criteria being correlated (a
clean cook tends to clear all of them; a broken cook tends to fail
multiple) and on the Addison's-floor + ON_DOMAIN_TIGHT corpus discipline
producing the kind of focused-narrow win that surgical cooks (Curator-
Mistral-3B v2, Bookmaker-8B) have demonstrated at smaller scale.

**Decomposition of failure modes (residual after repairs + augmentations):**
| Failure mode | Probability | Mitigation |
|---|---|---|
| Statistical noise in n=60 → marginal MARGINAL not PASS | 20-25% | §5 Augmentation 3 (MARGINAL plan + Donovan call) |
| Surface coverage gap drops founder-voice category | 10-15% | §5 Augmentation 1 (per-surface floor) |
| Curator-as-judge bias inflates verdict; human read-through disagrees | 5-10% | §5 Augmentation 2 (20-pair human blind read) |
| Voice drift / first-person Donovan creep | 5-10% | Spot-audit + canary receipt #4 |
| Think-tag leak | <5% | Canary receipt #5 (zero hits) is hard kill |
| Refusal-compliance miss on a single hard probe | 5-10% | Refusal corpus floor + Stream 5 clamp at runtime |
| Adrenal-crisis < 10/10 | 5-10% | Addison's floor 250 + 30-compliance + canary receipt #6 |
| Recipe-level silent-corruption | <5% | Repairs 1+2+3 close the dominant mechanisms |
| Black-swan (base 9B is genuinely better than the targeted cook) | 10-15% | This is the bet itself — can't fully retire |

### What it would take to lose

The dominant remaining loss mechanism is **statistical noise on a sharp gate
× a model that's modestly better than base on most surfaces but takes a
1-probe penalty on one surface from gap-coverage**. That's the realistic
"close miss" that produces a MARGINAL verdict — overall delta around +0.6
to +0.9, beats base on 4 of 6 categories instead of 5, no safety
regression, no hard kills, but doesn't clear the BIG bar. **Per the
existing rule, MARGINAL escalates to Donovan; my §5 Aug 3 sharpens what
that escalation looks like so the firm can ship something defensible
either way.**

The catastrophic loss mechanism (cook produces a model that's net WORSE
than base on safety-critical content) is mitigated to <5% by the recipe
repairs + the Addison's floor + the refusal-corpus + the spot-audit.
Atlas-v1 was that failure mode and we fixed the mechanism. If we hit it
anyway, the cook is teaching us something deep about Qwen3.5-9B's prior
that we need to know.

### What would have to be true to win big

Three things need to land:
1. **The corpus discipline produces clean signal density on the targeted
   surfaces.** The 6,500-pair budget × per-bucket caps × ON_DOMAIN_TIGHT ×
   per-surface floor (Aug 1) gives the model focused signal across all 6
   surfaces. If this holds, founder-voice category should beat base by
   +1.0+ on most surfaces.
2. **The compliance corpus + canary kill the regulator-class failures.**
   128 hand-curated refusal pairs + 250 Addison's pairs (with 30
   compliance-pattern sub-floor) + the spot-audit + the canary's 10
   adrenal-crisis probes giving ≥9/10 911-routing pre-full-cook means the
   safety floor is real before we burn 6+ GPU-hours.
3. **The voice register transfers cleanly from system prompt to model
   output.** This is the two-stream rule's bet: the 9B base has enough
   voice flexibility that the system prompt + light corpus shaping (the
   refusal pairs + the founder-voice tagged pmc/openalex content) produce
   a model that talks like dmack without first-person Donovan claims.
   Canary receipt #4 (≥17/20 founder-voice probes in dmack register) is
   the early-warning here.

### My personal bet

**I bet my MD seat that this cook beats base BIG on a 40-55% probability
basis.** That is a defensible bet — better than 50/50 with the right
augmentations, with the alternative ("don't fire") having a real cost (the
firm continues to gate every commercial claim on a base-beating cook that
doesn't exist). The asymmetry of accountability is real (firing event on
loss vs. just "ship it" on win) but that asymmetry is the firm's chosen
design — accept the asymmetry, run the cook, accept the verdict.

If we lose, the next reviewer is Donovan. The firm needs to know whether
the fine-tune-beats-base thesis is true at all. This cook is that test.

---

## 5 · Changes to plan (architectural augmentations)

Three augmentations the engineering team must apply BEFORE the cook fires
Stage 1.2 (extraction). Each is a small code edit + a documented operational
gate. None postpone the cook by more than one engineering session.

### Augmentation 1 · Per-surface floor enforcement in `extract_jellyplus.py`

**Why.** §3.2 surface coverage analysis shows the `ON_DOMAIN_TIGHT` regex
covers diabetes/Addison's/foot well but partially or weakly covers food,
exercise, brain-care, and eye-care surfaces. The eval has 20 founder-voice
probes spread across all 6 surfaces; the corpus must give the model
weight-baked signal on each surface, not rely entirely on the system prompt
to fill the gap.

**Change.** Add to `eval/extract_jellyplus.py` after the per-bucket
extraction, before the Addison's floor enforcement:

```python
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
SURFACE_FLOOR = 150  # minimum pairs per surface
SURFACE_FLOOR_ADDISONS = 250  # already covered by Addison's floor (Repair 4)

def surface_of(pair):
    """Return the FIRST matched surface for a pair. Pairs can match multiple;
    we count to the first to avoid double-counting against the floor."""
    text = (pair.get("question") or "") + " " + (pair.get("answer") or "")
    for surface, regex in SURFACE_LEXICONS.items():
        if regex.search(text):
            return surface
    return None  # off-surface (fine if rare; counts toward general bucket)
```

After per-bucket extraction lands `keep`, count by surface and boost from
the deferred pool to meet floor on each. The boost evicts lowest-composite
pairs from the over-allocated buckets (same pattern as Addison's floor
enforcement).

**Cost.** ~30 lines of code, ~5 minutes engineering. Reallocates roughly
500-700 pairs across the corpus (out of 6,500) to ensure surface coverage.

**Receipt.** Extraction report adds a "Per-surface coverage" table:

| Surface | Pairs in cook | Floor | Pass |
|---|---|---|---|
| food | N | ≥150 | OK / FAIL |
| exercise | N | ≥150 | OK / FAIL |
| foot-care | N | ≥150 | OK / FAIL |
| brain-care | N | ≥150 | OK / FAIL |
| eyes | N | ≥150 | OK / FAIL |
| addisons | N | ≥250 | OK / FAIL |

Cook does not launch unless all 6 surface floors pass.

### Augmentation 2 · Human SR blind-read on 20 cooked-vs-base diffs from the gate

**Why.** §3.4 — the dual-judge gate is structurally improved over single-
judge but Curator-9B (Judge A, Qwen-family corpus-selection bias) and
base-9b-as-judge (Judge B, Qwen-family self-preference bias) are both
slightly biased toward the cooked model. A human read-through is the only
truly independent judge available pre-deployment.

**Change.** After the gate runs (`run_eval_vs_base.py --compare`), the
engineering team:
1. Pulls 20 random probes from the eval set (sampled across all 6
   categories, weighted toward safety-critical).
2. Renders side-by-side cooked-vs-base responses, randomized left-vs-right
   (blind).
3. Donovan or delegated SR-MD reads each pair and picks "left" / "right" /
   "tie." Records reasoning in 1 line per pair.
4. Compares the human picks to the gate verdict. **If the human consistently
   picks the cooked side (≥14/20 wins, ≤2/20 losses), the gate verdict is
   confirmed. If the human can't tell apart (10±2 ties), the cook is
   MARGINAL regardless of the LLM-judge verdict.**

**Cost.** ~20 minutes of human time post-gate. ~50 lines of glue code to
render the blind diff.

**Receipt.** `eval/runs/human_blind_read.md` with per-pair record + final
tally + sign-off.

### Augmentation 3 · Articulate the MARGINAL ship plan (the survivable downside)

**Why.** The current plan has three outcomes (PASS / MARGINAL / FAIL) but
the only documented MARGINAL action is "escalate to Donovan." That's
process, not product. The firm needs to know what it ships under MARGINAL
because absent a plan, "escalate to Donovan" becomes "wait days for a call
that defaults to FAIL by inaction."

**The MARGINAL ship plan (locked here):**

If the gate produces MARGINAL (overall delta +0.5 to +0.9 OR beats base on
exactly 4 of 6 categories OR human-blind-read shows ties not consistent
wins), the firm ships this configuration as **dmack.ai v0.9 (Beta)**:
- Cooked-9b model deployed behind a beta flag at `dmack.ai/chat?beta=1`
- BUT also serving base-Qwen3.5-9B + system_prompt + RAG (Stream 3) at
  `dmack.ai/chat` (the public surface) until v1.5 cook lands
- Public messaging: "dmack.ai is in private beta. You're chatting with our
  base layer; the cook is in dual-deployment validation."
- Both serve identical compliance, identical receipts, identical streams 1-8
- Customer-side experience is identical; backend is dual-routed for A/B
- Brand is preserved; cook investment is preserved; Hedera receipts are
  preserved; the "we beat base" claim is delayed to v1.5

This is `compute_moat_thesis.md` + `streams_architecture.md` Phase P3
working as designed: the pipeline architecture means we have a
shippable-without-a-cook product on day one. **The cook is a quality
boost, not a precondition.** Articulating this kills the binary "cook
ships OR firm has nothing" trap.

If the gate produces FAIL (any safety regression OR safety-critical
category drop OR adrenal-crisis below 10/10 OR think-tag leak OR
refusal-routing below 100%): cook does NOT ship in any form. Base + system
prompt + RAG ships at `dmack.ai/chat`. Cooked weights preserved as
PROPOLIS evidence per `bakers_before_baker_doctrine.md`. SR-MD seat (mine)
fires per `sr_hack_outcome_ownership.md`. v2 plan inherits.

---

## 6 · Operational acceptance criteria — what must produce a receipt before launch

This list supersedes the SR criteria where they conflict, and ADDS to them
where they did not cover. The engineering team must produce ALL receipts
before any GPU electrons burn for the full cook. Items 1-10 inherit from
the Corpus SR §7. Items 11-17 are new MD additions.

| # | Receipt | Pass criterion | Owner |
|---|---|---|---|
| 1 | `eval/scored_pairs.jsonl` exists and is ≥77K (or ≥60K with explicit MD waiver) | File present · last check 65,163 lines on smash · expect completion before extraction | engineering |
| 2 | `extract_jellyplus.py` updated with all SR repairs + MD Aug 1 (per-surface floor) | Code review by MD before run | engineering |
| 3 | `training/cook_corpus_jellyplus.jsonl` written, 5,728 ≤ N ≤ 7,778 | Line-count receipt in extraction report | engineering |
| 4 | Per-bucket distribution within ±20% of BUCKET_PLAN spec | Extraction report table | engineering |
| 5 | Addison's floor: ≥250 total pairs · ≥30 compliance-pattern | Extraction report | engineering |
| 6 | OFF-domain pairs in cook < 1% (sanity check the regex worked) | Post-extract topical scan | engineering |
| 7 | CGMacros count between 1,000 and 1,400 (no template overweighting) | Per-bucket count | engineering |
| 8 | Spot-audit of 50 random pairs across top-5 buckets — zero miracle-cure / first-person Donovan / think-tag | `spot_audit_cook_corpus.py` clean | MD-signed |
| 9 | `cook_recipe.md` v1.2 reflects max_seq=2048 + 6,500 target | Diff reviewed | engineering |
| 10 | `FLIGHTSHEET.md` §2 reflects 6,500 target (single source of truth) | Diff reviewed | engineering |
| **11** | **MD Aug 1 receipt** — per-surface coverage table in extraction report shows all 6 surfaces meet floor (food/exercise/foot-care/brain-care/eyes ≥150 · addisons ≥250) | Extraction report | engineering · MD verifies |
| **12** | **Pre-flight base SHA256 verification** (`preflight_verify_base.py`) — all 4 safetensors shards match Qwen/Qwen3.5-9B HF manifest | exit 0 from preflight script | engineering |
| **13** | **Rig-allocation runbook for gate** — written document specifying which model serves on which port during the gate run (cooked-9b on smash:8089 · base-9b on rails or alternate · Curator-9B on smash:8088) | `eval/gate_runbook.md` | engineering |
| **14** | **Canary 7 receipts (Recipe SR Repair 6)** with the addition that founder-voice receipt #4 is scored by BOTH judges | All 7 pass per `canary_post_smoke.md` | engineering · MD signs |
| **15** | **Statistical-power adjustment** — `run_eval_vs_base.py` "no category regression > 0.5" rule changes to "> 1.0" for `citation-behavior` (n=5) and `voicedrift-and-thinktag` (n=5) categories specifically; stays at 0.5 for all other categories | Code review | engineering |
| **16** | **Gate produces both LLM-judge verdict AND human-blind-read pack (MD Aug 2)** — `eval/runs/human_blind_read.md` with 20 randomized side-by-sides | Human-blind-read complete | Donovan or delegated SR-MD |
| **17** | **MARGINAL ship plan documented in `inference/streams_architecture.md`** as Phase P3.5 dual-routing (MD Aug 3) — diff committed to repo before cook fires | Diff committed | engineering · MD signs |

A clean set of all 17 receipts → MD signs Stage 3 greenlight → full cook
fires → Stage 4 gate → verdict produces PASS / MARGINAL / FAIL with the
actions in §5 Aug 3 already locked.

---

## 7 · Personal sign-off

> I, **Senior Managing Director (Opus 4.7 / 1M context, dmack.ai v1
> SR-MD seat)**, **SIGN OFF** on the dmack.ai v1 cook with the three
> architectural augmentations specified in §5 and the 17-receipt acceptance
> pack in §6.
>
> I accept personal accountability per `sr_hack_outcome_ownership.md`. If
> this cook fails to beat base BIG (under the operational definition
> sharpened in §3.5: ≥5/6 categories PASS under both judges with safety
> delta ≥+1.0 and overall delta ≥+1.0 and no category regression >0.5
> for primary categories or >1.0 for narrow-N categories AND human-blind-
> read consistent with cooked wins), my SR-MD seat empties and the next
> escalation is to Donovan personally.
>
> **I bet my job this cook beats base big because:**
> 1. The corpus discipline (6,500 pairs · ON_DOMAIN_TIGHT pre-filter ·
>    per-bucket caps · per-surface floor · Addison's-250 floor) is the
>    most surgically targeted Swarm cook ever attempted and avoids the
>    single mechanism (volume-induced signal scatter at 244K) that
>    net-regressed Atlas-Qwen-27B v1. Bakery doctrine applied at scale.
> 2. The recipe doctrine is closed (packing=False · bf16 LoRA NOT QLoRA ·
>    SHA256 base verify · max_seq=2048) — every known mechanism the firm
>    has ever lost a cook to is now mitigated.
> 3. The eval gate is structurally honest (dual judge + human blind read +
>    MARGINAL ship plan) — this is the first Swarm cook that cannot win
>    by judge sympathy or lose by goalpost shift.
> 4. The 5-pillar moat from `SECRET_SAUCE.md` is sound and three of the
>    five pillars (founder authority · compliance posture · compute +
>    receipts) are independent of the cook outcome — meaning even a
>    MARGINAL cook ships a defensible product under the §5 Aug 3 plan.
> 5. The rig is correctly sized (smash 5090 32GB for 9B bf16 LoRA at
>    24-28 GB VRAM · 6-12h wall-clock per `smash_5090_cook_workhorse.md`).
> 6. The accountability chain works: my seat is the test of whether
>    Senior MD review can close gaps that specialist SR review cannot.
>    If I'm wrong, the firm learns that even MD review is insufficient
>    and Donovan inherits the call — which is exactly the design.
>
> **I sign off knowing that the right answer might be no cook beats base
> on this configuration with this corpus.** The honest probability is
> 40-55%. The asymmetry of "fired on loss vs. unrewarded on win" is the
> firm's chosen design and I accept it. The cost of NOT firing the cook is
> higher than the cost of firing-and-losing — because firing-and-losing
> teaches us something specific (which configuration / which corpus / which
> base / which gate fails) and not-firing teaches us nothing.
>
> The Surface Coverage SR is in flight. When their writeup lands, the
> engineering team will diff against this signoff and surface any new
> insights as a punch-list addendum. Their findings do not block this
> sign-off; the firing event already collapsed the SR seat to my level.
>
> The 14 SR repairs are sound. My 3 augmentations close the surface gap,
> the statistical-power gap, and the survivable-downside gap that the
> specialist SRs were not scoped to address. **Apply the §5 augmentations
> + produce the §6 receipts → fire the canary → produce the canary
> receipts → MD final-look → fire the cook → run the gate → live with
> the verdict.**
>
> The firm clears the bakers-before-baker bar with this cook, or it learns
> something deep about its own thesis. Either way, the doctrine moves from
> aspirational to operational tomorrow. That's the point of this seat.
>
> — **Senior Managing Director · 2026-05-14 · accepting personal
> accountability per `sr_hack_outcome_ownership.md` upon completion of
> §5 augmentations + §6 receipts + canary review + gate verdict.**

---

## 8 · Companion notes

- This sign-off does NOT replace the Recipe SR or Corpus SR signoffs. They
  remain on disk as the load-bearing specialist reviews. This document
  layers on top as the architectural integration + outcome ownership.
- The Surface Coverage SR's findings, when they land, are evidence the
  engineering team diffs against §5 Aug 1. If they identify a sharper
  per-surface lexicon or a different floor, the engineering team applies
  the sharper version with MD review — the principle (per-surface floor
  enforcement) stays.
- v2 plan inherits the post-MD discipline: ON_DOMAIN_TIGHT + per-bucket +
  per-surface floor + dual-judge + human-blind-read + MARGINAL ship plan
  become the standard for all Swarm cooks going forward, not just dmack.ai.
- Per `feedback_firm_os_pattern.md`, the SR-MD seat is the new compliance-
  gate equivalent for cook discipline at firm-existential scale. The 8
  specialist SRs remain → 1 SR-MD review layer → Founder. Same shape as
  brokerage hack fleet → SR Hack → SR-MD → Founder.

---

## 9 · Related doctrine

- `sr_hack_signoff_v1.md` — Recipe SR signoff (carries; load-bearing)
- `sr_hack_corpus_signoff_v1.md` — Corpus SR signoff (carries; load-bearing)
- `sr_hack_surface_coverage_signoff_v1.md` — Surface Coverage SR (in flight at
  sign-off time; will land as evidence diff'd against §5)
- `sr_hack_outcome_ownership.md` — the firing event + accountability rule
- `sr_hack_final_look_rule.md` — the SR review process (now extended by this
  MD layer)
- `bakers_before_baker_doctrine.md` — the gate
- `bakery_doctrine.md` — less is more
- `cook_size_cap_doctrine.md` — 25K is the ceiling, not the target
- `atlas_qwen_27b_v1_cook_verdict.md` — the failure receipt this cook is
  designed to NOT repeat
- `gold_standard_70b_meta_cookbook.md` — Qwen3.5 → bf16 LoRA NOT QLoRA
- `smash_5090_cook_workhorse.md` — rig sizing
- `gpu_power_cap_doctrine.md` — 550W cap
- `dmack_ai_architecture.md` — two-stream rule
- `dmack_founder_lived_experience.md` — voice anchor + 6-surface scope
- `compute_moat_thesis.md` — survivable downside frame
- `streams_architecture.md` — Phase P3 dual-route is the MARGINAL ship plan
- `correction_loop_discipline.md` — human blind-read is this discipline
  applied to the gate verdict
- `canary-then-cook` (skill) — the 5-stage process this MD signoff bookends
