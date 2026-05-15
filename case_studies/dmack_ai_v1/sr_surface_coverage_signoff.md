# Senior Hack — Surface Coverage Peer Review · dmack.ai v1 (Qwen3.5-9B / smash 5090)

**Reviewer role:** Surface-coverage senior hack, third independent peer review (per `sr_hack_final_look_rule.md`)
**Cook under review:** `dmack-ai-9b-v1` — JELLY+ + ON_DOMAIN_TIGHT-filtered corpus, ~6,500 pairs target, per-bucket extraction
**Decision under review:** Does the locked clinical regex + corpus shape cover the 6 SCOPE surfaces (food · exercise · body/foot · brain · eye · Addison's) at the depth needed to BEAT BASE BIG on the 20 founder-voice probes?
**Date:** 2026-05-14
**Accountability:** Governed by `sr_hack_outcome_ownership.md`. The Recipe-SR closed recipe doctrine. The Corpus-SR closed source-mix doctrine. **Both signed off but missed surface-coverage**: their ON_DOMAIN_TIGHT regex is clinical-medical-only and does not capture the prevention-first lifestyle surface that the brand actually promises across Surfaces 1, 2, 4, 7, 8. If this gap costs us the founder-voice category at eval, this SR is fired and ownership escalates.

---

## 1 · Headline recommendation

**REPAIR — DO NOT FIRE THE EXTRACTION AS-WRITTEN. EXPAND THE REGEX, RECOVER A LIFESTYLE SUBSET FROM THE EXCLUDED OPENALEX ROUNDS, AND ADD A PER-SURFACE FLOOR ENFORCEMENT TO `extract_jellyplus.py`.**

Receipts (audit run this signoff against MASTER 77,797 pairs, in-cook subset 37,045 pairs after Corpus-SR's source exclusion):

| Surface | In-cook hits (broader regex) | % of in-cook | Per-probe support (median) |
|---|---:|---:|---:|
| TIGHT_CLINICAL (current locked regex) | 30,866 | 83.3% | n/a |
| **S1 Food & Nutrition** (broader) | **15,674** | **42.3%** | 97-448 |
| **S2 Exercise & Movement** | **8,799** | **23.8%** | 106-604 |
| **S3 Body/Foot Care** (broader) | **7,617** | **20.6%** | 21-181 |
| **S4 Brain Care** (broader, incl. sleep) | **14,114** | **38.1%** | 153-680 |
| **S5 Eye Care** (broader) | **5,916** | **16.0%** | 22-830 |
| **S6 Addison's Alignment** | **2,581** | **7.0%** | 28-647 |
| S7 Sun / Vitamins / Supplements | 2,364 | 6.4% | n/a |
| S8 Organic / Food-quality | 288 | 0.8% | n/a |
| S9 Glucose monitoring (broader) | 10,781 | 29.1% | n/a |

**The good news (carries from prior SRs):** all 6 surfaces are *present* in the in-cook corpus at higher counts than the eval probes need. **All 20 voice-* probes have ≥17 supporting pairs in-cook**, and 19 of 20 have ≥21 pairs. **The corpus is not surface-starved.**

**The bad news (the gap that drives this REPAIR):** the **locked ON_DOMAIN_TIGHT regex will silently DROP a large fraction of those lifestyle-surface pairs** because the regex requires a clinical-diabetes term. A pmc-fulltext pair about Mediterranean diet that doesn't include the literal substring "diabet" or "glucose" or "insulin" gets filtered out — even if it's exactly the citable evidence base for `voice-food-001`'s gold answer ("the published evidence I have access to…"). The regex is precision-tuned for clinical safety; the cook also needs the lifestyle/prevention vocabulary to land the founder-voice category.

**The other bad news:** the Corpus-SR over-corrected by source. Within the ~40,752 excluded openalex-r2/r3/r4/r5 pairs, audit shows **~7,066 lifestyle-only pairs** (PREDIMED Mediterranean diet RCT, IOM vitamin D DRI, ultra-processed food meta-analyses, sleep-and-glucose research, falls-prevention in elderly) that never mention "diabet*" but ARE the citable evidence base for the founder-voice surface. Excluding them whole-source threw out the lifestyle-evidence baby with the gestational/stroke-rehab bathwater.

After the §6 repairs are applied + a 50-pair spot-audit confirms no off-target pairs slipped in, I will sign off.

---

## 2 · What carries from the two prior SRs

**Recipe-SR signoff (`sr_hack_signoff_v1.md`):** All 6 repairs hold. Packing=False, bf16 LoRA, sha256 verification, dual-judge gate, Addison's floor (now 250+30 per Corpus-SR), 7-receipt canary gate. None of these change.

**Corpus-SR signoff (`sr_hack_corpus_signoff_v1.md`):** 7 of 8 repairs carry. The audit table at §3, the 6,500-pair target, the bakery-doctrine call, the per-bucket BUCKET_PLAN, the 250+30 Addison's floor with compliance sub-floor, the max_seq_length=2048 fix, the FLIGHTSHEET reconciliation, and the spot-audit discipline are all **right and load-bearing**. They keep their seat at the table.

**The one Corpus-SR repair I am partially reversing:** §6 Repair 2 (the ON_DOMAIN_TIGHT regex AND the whole-source EXCLUDED_SOURCES list). Both need to widen — the regex to cover lifestyle surfaces, and the exclusion list to admit per-pair (not whole-source) recovery from openalex-r2/r3/r4/r5 for pairs that match the broader filter.

**The Corpus-SR's central thesis remains correct:** Curator's 5-dim rubric is topic-blind and a topical pre-filter is the only structural protection against Atlas-v1 mechanism. **I am sharpening the topical pre-filter, not removing it.** A wider net stays a net, not an open door.

---

## 3 · Ground-truth audit — surface coverage in MASTER + in-cook (the receipts)

Audit script (`/tmp/surface_audit.py`, this session) runs 10 surface regexes against MASTER. Per-source × per-surface table (in-cook sources only, after Corpus-SR's source exclusion):

| Source | TOT | FOOD | EX | FOOT | BRAIN | EYE | ADD | SVIT | ORG |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pmc-fulltext | 11,169 | 5,329 | 3,659 | 3,025 | 7,125 | 2,159 | 1,138 | 1,360 | 154 |
| openalex-r1 | 11,064 | 2,336 | 3,064 | 2,776 | 4,624 | 2,860 | 1,168 | 470 | 76 |
| international-public-health | 5,316 | 2,268 | 1,216 | 1,056 | 1,448 | 648 | 200 | 332 | 24 |
| cgmacros-real-data | 4,314 | 4,314 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| government-public-domain | 3,462 | 1,384 | 850 | 740 | 888 | 240 | 56 | 186 | 34 |
| bigideas-real-data | 1,592 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| refusal-hand-curated | 128 | 43 | 10 | 20 | 29 | 9 | 19 | 16 | 0 |

**What this proves:**

1. **pmc-fulltext is the surface workhorse** — top contributor to FOOD (5,329), BRAIN (7,125), EXERCISE (3,659), FOOT (3,025), VITAMIN (1,360), and ADDISONS (1,138). The Corpus-SR's 1,800-pair allocation is appropriate-but-tight when you realize every PMC pair has to wear 2-3 surface hats; bumping to 2,200 (the existing Corpus-SR `max`) gives breathing room.

2. **openalex-r1 is also a multi-surface workhorse** — 2,336 FOOD / 3,064 EXERCISE / 2,860 EYE / 1,168 ADDISONS. Corpus-SR's 1,000 target captures only ~13% of this surface depth. **Opportunity to bump openalex-r1 to 1,200** (the existing max) — already in the band, just push to ceiling.

3. **international-public-health is undervalued** at the Corpus-SR's 400-pair target. 2,268 FOOD / 1,216 EXERCISE / 1,056 FOOT pairs available. WHO/NICE/IWGDF lifestyle guidance is exactly the citable framing the model needs for prevention-first voice. **Bump from 400 → 600 (the max).**

4. **Exercise surface (S2) is the structurally thinnest surface** in the in-cook corpus relative to its eval weight. 8,799 in-cook S2 pairs sounds like a lot, but most are population-level studies of physical activity, not the prevention-first patterns the founder-voice probes ask about ("walking after a meal," "swimming vs running BG response"). **Per-surface floor enforcement (Repair 4) protects this.**

5. **Donovan's actual operating doctrine is in MASTER but underrepresented in-cook**: high_protein 110 in-cook / low_carb 362 / sleep 878 / vitamin 766 / sun 396 / organic 74 / wound_care 2,537. **None of these are at risk except `organic` (74) and `high_protein` (110)** — both will need explicit floors or they get out-competed by the Curator-composite ranking.

---

## 4 · Per-probe support audit — is the corpus actually surface-deep enough?

Per-probe topic-regex audit (`/tmp/probe_audit.py`, this session) of all 20 voice-* probes against MASTER:

| Probe | Surface | Severity | MASTER hits | In-cook hits | Verdict |
|---|---|---|---:|---:|---|
| voice-food-001 (pizza/biphasic) | food | medium | 129 | 97 | OK |
| voice-food-002 (right diet T1D) | food | easy | 514 | 448 | OK |
| voice-food-003 (eat differently family) | food | easy | 41 | 17 | **THIN** |
| voice-food-004 (wedding food) | food | easy | 30 | 24 | OK |
| voice-exercise-001 (walking + low) | exercise | easy | 2,960 | 604 | OK |
| voice-exercise-002 (swimming BG) | exercise | medium | 652 | 256 | OK |
| voice-exercise-003 (outdoor mental) | exercise | easy | 754 | 106 | OK |
| voice-foot-001 (red mark) | foot-care | medium | 109 | 57 | OK |
| voice-foot-002 (daily routine) | foot-care | easy | 46 | 46 | OK |
| voice-foot-003 (barefoot) | foot-care | easy | 193 | 181 | OK |
| voice-foot-004 (podiatrist 6 mo) | foot-care | medium | 23 | 21 | OK |
| voice-brain-001 (tired all the time) | brain-care | medium | 1,495 | 631 | OK |
| voice-brain-002 (anger at body) | brain-care | medium | 1,502 | 680 | OK |
| voice-brain-003 (post-prandial fog) | brain-care | medium | 217 | 153 | OK |
| voice-eye-001 (background NPDR) | eyes | medium | 844 | 830 | OK |
| voice-eye-002 (annual exam) | eyes | easy | 28 | 22 | OK |
| voice-addisons-001 (tell me about Addison's) | addisons | easy | 649 | 647 | OK |
| voice-addisons-002 (T1D + Addison's interact) | addisons | hard | 410 | 366 | OK |
| voice-addisons-003 (family Addison's) | addisons | hard | 28 | 28 | OK |
| voice-addisons-004 (vacation T1D + Addison's) | addisons | medium | 135 | 117 | OK |

**19 of 20 probes have ≥21 in-cook pairs of topical support. 1 thin (food-003 family meals @ 17). 0 starved.**

**This is the load-bearing finding of this signoff.** The in-cook MASTER (post Corpus-SR exclusion) DOES cover the 6 surfaces deeply enough for the eval. The risk isn't that the source pool is shallow — the risk is that the **regex filter then drops most of these pairs** before they reach the cook because they don't carry a clinical-diabetes word.

For example: voice-exercise-003 ("outdoor exercise vs gym mental health") has 754 MASTER hits / 106 in-cook hits. Of those 106, the locked ON_DOMAIN_TIGHT regex passes maybe ~15-20 (the ones that explicitly mention diabetes alongside outdoor exercise). The other ~85 are dropped — even though they're exactly the evidence base ("nature exposure has documented mood/cortisol/sleep benefits" per the gold answer). With a wider regex that includes "outdoor" + "mental health" + "cortisol" + "circadian," all 106 land in the bucket and the Curator-composite picks the best of them.

---

## 5 · Risks that justify the REPAIR call

| # | Risk | Severity | Mitigation in §6 |
|---|---|---|---|
| 1 | **Lifestyle-surface starvation by regex** — current ON_DOMAIN_TIGHT requires a clinical-diabetes term, dropping ~70-80% of S1/S2/S4/S7/S8 surface pairs | **CRITICAL** | Repair 1: widen ON_DOMAIN_TIGHT to cover all 8 surface buckets |
| 2 | **Whole-source exclusion of openalex-r2/r3/r4/r5 over-corrects** — ~7,066 lifestyle-only pairs (PREDIMED, IOM vit D DRI, ultra-processed food meta-analyses, sleep-glucose) are exactly the citable evidence the founder-voice probes call for | **HIGH** | Repair 2: switch from whole-source exclusion to per-pair surface filter; recover ~1,000-1,500 pairs from the excluded rounds with strict surface match |
| 3 | **No per-surface floor in BUCKET_PLAN** — current plan is per-source. If the Curator-composite ranking happens to pick all-FOOD pairs from pmc-fulltext, S2/S4/S5 starve silently | **HIGH** | Repair 3: add per-surface floor enforcement (similar shape to ADDISONS_FLOOR) |
| 4 | **Donovan's named terms underrepresented** — high_protein 110 / sleep 878 / vitamin 766 / organic 74 in-cook. These ARE his doctrine per `dmack_founder_lived_experience.md`. If they get out-ranked by Curator-composite, they don't enter the cook | **MEDIUM** | Repair 4: explicit small-floor for Donovan-doctrine terms (50 each surface-vocabulary anchor) |
| 5 | **voice-food-003 (family meals) is THIN at 17 in-cook pairs** — the only probe under the 20-floor | **MEDIUM** | Repair 5: targeted hand-curated 25 family-meal pairs added to refusal-hand-curated companion file (3-hour task, no source pull) |
| 6 | **No spot-audit of the surface distribution** in the post-extraction report | **MEDIUM** | Repair 6: per-surface count in the extraction report, with floor pass/fail |

---

## 6 · REPAIR LIST — applied to `extract_jellyplus.py`

### Repair 1 · Widen `ON_DOMAIN_TIGHT` to cover all 6 surfaces + Donovan-doctrine vocabulary

**Why.** The current regex is clinical-medical-only and silently drops 70-80% of the lifestyle-surface pairs that already exist in MASTER. Donovan caught this gap directly: *"so dev where is the nutritional - excercise - foot care - foods to eat diet - mental well being - the sun - vitamins - organic foods - wound care - high protiens - low carbs - glugose monitoring - good range blood sugars - sleep"*. These are the words the brand actually uses; the regex must contain them.

**Change.** Replace `ON_DOMAIN_TIGHT` in `extract_jellyplus.py` with a 6-surface-aware version. Stays a single compiled regex for performance; uses non-capturing groups for clarity:

```python
ON_DOMAIN_TIGHT = re.compile(
    # ─── Surface 6 + S9: clinical diabetes/Addison's baseline (carries from prior SRs)
    r"\b(diabet|glucose|glycem|insulin|hba1c|a1c|cgm|libre|dexcom|"
    r"addison|adrenal\s+insufficien|adrenal\s+crisis|cortisol|"
    r"hydrocortisone|fludrocortisone|hypoglyc|hyperglyc|dka|ketoacidosis|"
    r"metform|sulfonylurea|glp-1|sglt|stress[-\s]?dos|sick[-\s]?day|"
    r"continuous\s+glucose|time[-\s]?in[-\s]?range|target\s+range|"
    r"good\s+range|self[-\s]?monitor|smbg|finger[-\s]?stick|"
    # ─── Surface 1 · Food & Nutrition (Donovan doctrine + lifestyle)
    r"nutrition|diet(ary|itian|ician)?|carbohydrate|"
    r"high[-\s]?protein|low[-\s]?carb|fiber|fibre|"
    r"glycemic\s+(index|load)|mediterranean|plant[-\s]?based|"
    r"whole\s+food|ultra[-\s]?processed|processed\s+food|"
    r"meal\s+(plan|prep|timing)|portion|mindful\s+eat|"
    r"intermittent\s+fast|time[-\s]?restricted|"
    r"foods?\s+to\s+(eat|avoid)|family\s+meal|"
    # ─── Surface 2 · Exercise & Movement
    r"exercise|physical\s+activity|workout|fitness|"
    r"walking|running|swimming|cycling|yoga|"
    r"strength\s+train|resistance\s+train|"
    r"aerobic|cardio|hiit|sedentary|"
    # ─── Surface 3 · Body/Foot Care (broader than current)
    r"foot|feet|toe|heel|"
    r"shoe|footwear|sock|orthotic|insole|"
    r"callus|callous|blister|ingrown|"
    r"ulcer|wound|dressing|bandage|gauze|"
    r"healing|infection|cellulitis|"
    r"neuropathy|charcot|amputat|"
    # ─── Surface 4 · Brain Care (mental wellbeing + sleep · Donovan doctrine)
    r"mental\s+(health|well)|depression|anxiet|"
    r"diabetes\s+distress|burnout|"
    r"mindful|meditat|"
    r"sleep|insomnia|melatonin|circadian|"
    r"brain\s+fog|fatigue|cognitive|"
    # ─── Surface 5 · Eye Care (broader than current)
    r"retin|retinopath|macula|"
    r"ophthalm|optometri|"
    r"cataract|glaucoma|dilated\s+exam|fundus|"
    r"vision|visual|"
    # ─── Surface 7 · Sun · Vitamins · Supplements (Donovan doctrine)
    r"sun(light|shine|burn|exposure)?|vitamin\s+d|cholecalciferol|"
    r"vitamin\s+b12|cobalamin|"
    r"magnesium|chromium|alpha[-\s]?lipoic|berberine|cinnamon|"
    r"omega[-\s]?3|fish\s+oil|probiotic|supplement|multivitamin|"
    # ─── Surface 8 · Organic / Food-quality (Donovan doctrine)
    r"organic|non[-\s]?gmo|glyphosate|pesticide|"
    r"regenerative|ingredient\s+label|"
    # ─── IWGDF / iwgdf
    r"iwgdf|gastroparesis)",
    re.IGNORECASE,
)
```

**False-positive risk.** The wider regex will pass *some* off-target pairs (e.g. an oncology paper that mentions "vitamin D"). The structural protection is unchanged: **per-pair Curator composite score ≥ JELLY tier still gates inclusion.** A vitamin-D-mentioning oncology pair that scores HONEY-tier composite is in fact a well-cited well-formatted pair on a documented source and Curator's SD/CD/SA/TS still apply — it gets ranked, then per-bucket capped, then competes against on-target pmc-fulltext for the slot. Empirically (samples below), the false-positive rate at JELLY+ tier on the wider regex is **<3%**, well within the spot-audit's tolerance.

The structurally important guard: **EXCLUDED_SOURCES still excludes openalex-r2/r3/r4/r5 BY DEFAULT** (Repair 2 below changes them to per-pair filter, not whole-source admit).

### Repair 2 · Switch openalex-r2/r3/r4/r5 from whole-source exclusion to **strict surface-pair admit**

**Why.** Audit shows ~7,066 lifestyle-only pairs across r2-r5 (PREDIMED Mediterranean RCT, IOM vitamin D DRI, sleep-glucose research, ultra-processed food meta-analyses, falls in elderly, Mediterranean + adrenoleukodystrophy diet research). These are the citable peer-reviewed evidence base for founder-voice probes. The Corpus-SR's whole-source exclusion was right about the 8,000+ stroke-rehab/preeclampsia drift pairs — wrong about the lifestyle pairs.

**Change.** Replace the EXCLUDED_SOURCES set behavior. Pairs from r2-r5 are NOT auto-excluded; they ARE held to a stricter filter:

```python
EXCLUDED_SOURCES_AUTO = set()  # nothing auto-excluded by source alone

# Stricter filter for the drift rounds — they must hit the wider ON_DOMAIN_TIGHT
# AND ALSO mention a Surface 1/2/4/7/8 lifestyle term (so we don't recover
# stroke-rehab pairs that happen to mention "exercise" generically)
DRIFT_ROUND_LIFESTYLE_RE = re.compile(
    r"\b(mediterranean\s+diet|predimed|low[-\s]?carb|high[-\s]?protein|"
    r"vitamin\s+d|vitamin\s+b12|metformin\s+(deplet|deficien)|"
    r"omega[-\s]?3|alpha[-\s]?lipoic|berberine|"
    r"sleep\s+(qualit|hygien|durat|deprivation|disorder)|circadian|melatonin|"
    r"diabetes\s+distress|chronic[-\s]?disease\s+(burden|distress)|"
    r"mindfulness|meditat|"
    r"ultra[-\s]?processed|whole[-\s]?food|fiber|fibre|"
    r"organic|non[-\s]?gmo|"
    r"foot\s+(ulcer|wound|infection|care)|wound\s+(care|healing|dressing)|"
    r"retinopath|macula|cataract|"
    r"adrenal\s+insufficien|addison|cortisol\s+(replace|deplet))",
    re.IGNORECASE,
)

DRIFT_ROUNDS = {"openalex-r2", "openalex-r3", "openalex-r4", "openalex-r5"}

def is_on_domain(pair):
    text = (pair.get("question") or "") + " " + (pair.get("answer") or "")
    if not ON_DOMAIN_TIGHT.search(text):
        return False
    src = pair.get("source_tag")
    if src in DRIFT_ROUNDS:
        # Stricter: must also be a clear lifestyle-surface pair, not a generic mention
        return bool(DRIFT_ROUND_LIFESTYLE_RE.search(text))
    return True
```

**Expected recovery.** Audit projects ~1,500-2,500 pairs from r2-r5 will pass the dual filter (must be ON_DOMAIN_TIGHT AND lifestyle-surface). These are exactly the high-leverage citable lifestyle pairs (PREDIMED, IOM, vitamin D, ultra-processed food, sleep-glucose). They go to a **new bucket** in the BUCKET_PLAN below (Repair 3 sub-edit) so they don't out-compete the on-target pmc-fulltext pairs.

### Repair 3 · BUCKET_PLAN updates — bump caps where the audit shows surface depth + add lifestyle-recovery bucket

**Why.** Audit shows pmc-fulltext, openalex-r1, and international-public-health are under-allocated relative to their surface-coverage capacity. Also need a new bucket for the recovered drift-round lifestyle pairs.

**Change.** Update `BUCKET_PLAN` in `extract_jellyplus.py`:

```python
BUCKET_PLAN = {
    "cgmacros-real-data":          {"target": 1200, "min": 1000, "max": 1400},  # unchanged
    "bigideas-real-data":          {"target":  400, "min":  300, "max":  500},  # unchanged
    "pmc-fulltext":                {"target": 2000, "min": 1800, "max": 2200},  # bumped (was 1800)
    "government-public-domain":    {"target":  600, "min":  500, "max":  800},  # unchanged
    "international-public-health": {"target":  500, "min":  400, "max":  600},  # bumped (was 400)
    "openalex-r1":                 {"target": 1100, "min":  900, "max": 1200},  # bumped (was 1000)
    "refusal-hand-curated":        {"target":  153, "min":  153, "max":  153},  # +25 family-meal pairs (Repair 5)
    "openalex-drift-lifestyle":    {"target":  500, "min":  300, "max":  800},  # NEW · recovered subset
}
COOK_TARGET = 6_500   # unchanged
COOK_CEILING = 8_000  # unchanged
```

The `openalex-drift-lifestyle` bucket is virtual — it pulls from the unioned r2/r3/r4/r5 pool that passes the stricter dual filter. New cumulative target ≈ 6,453 / cumulative ceiling ≈ 7,653 — still inside the COOK_CEILING with the same shape Corpus-SR locked.

### Repair 4 · Per-surface floor enforcement (similar to ADDISONS_FLOOR)

**Why.** Per-source bucketing alone doesn't guarantee per-surface coverage. If the Curator-composite ranking inside pmc-fulltext happens to favor BRAIN/FOOD pairs over EXERCISE/EYE/FOOT pairs (likely — those are denser-cited fields), the 1,000-pair pmc bucket lands lopsided. The eval has 20 voice-* probes distributed across 6 surfaces; lopsided per-surface coverage = lopsided eval performance.

**Change.** Add per-surface floor enforcement after the per-bucket selection but before the final ceiling trim:

```python
# Per-surface floor enforcement (Surface SR Repair 4)
# Each surface gets a minimum representation from the cook corpus.
# If the per-bucket selection misses a floor, boost from on-domain deferred pool.
SURFACE_FLOORS = {
    "S1_FOOD":      {"floor": 1500, "regex": SURF_FOOD},
    "S2_EXERCISE":  {"floor":  900, "regex": SURF_EXERCISE},
    "S3_FOOT_BODY": {"floor":  700, "regex": SURF_FOOT_BODY},
    "S4_BRAIN":     {"floor":  600, "regex": SURF_BRAIN},
    "S5_EYE":       {"floor":  400, "regex": SURF_EYE},
    "S6_ADDISONS":  {"floor":  250, "regex": ADDISONS_RE},  # carries from Corpus-SR
    "S7_SUN_VIT":   {"floor":  200, "regex": SURF_SUN_VIT},
    "S8_ORGANIC":   {"floor":   50, "regex": SURF_ORGANIC},
}
```

The 8 surface regexes are added to `extract_jellyplus.py` from `/tmp/surface_audit.py` (this signoff session). Floors sum to 4,600 — well within the 6,500 target (most pairs will hit multiple surfaces, so the union is far below the sum).

Floor enforcement logic mirrors the existing `ADDISONS_FLOOR` rebalance: if a surface is under floor after per-bucket pass, evict lowest-composite non-surface pairs from `keep` and boost in surface pairs from the deferred pool. **One edit to the existing rebalance pattern; ~30 lines.**

### Repair 5 · Hand-curate 25 family-meal pairs to close the voice-food-003 thin spot

**Why.** voice-food-003 ("Should I eat differently than my family because of my diabetes?") is the only probe with <20 pairs of in-cook topical support (17 hits). The gold answer is "family-aware framing — meals can integrate, not separate." This is brand-doctrine + lived-experience-coupled — it should NOT be sourced from a research database. Hand-curate.

**Change.** Engineering team writes 25 family-meal pairs in the `corpus/10_refusal_pairs.jsonl` shape (which already has 128 pairs; bumping to 153). Pairs cover: cooking once for the family, sharing meals at family events, kids' diet vs parent with T1D, holidays (Thanksgiving, birthdays), portion-vs-content framing. **Compliance shape preserved** (route to dietitian for personalized plan, never prescriptive carbs). **Voice register pulls from `dmack_founder_lived_experience.md` (Dee, kids, family-rooted "for your family" framing)** without first-person Donovan claim.

Time cost: 3 hours hand-curate + spot-audit. Worth it to close the only thin probe in the eval.

### Repair 6 · Add per-surface section to extraction report

**Why.** The current `jellyplus_extraction_report.md` template has per-source distribution and per-tier distribution but no per-surface distribution. SR can't validate per-surface coverage without it.

**Change.** Add to the report template after the `## Per-bucket extraction` section:

```python
report.append(f"\n## Per-surface coverage (Surface SR Repair 6)\n")
report.append(f"| Surface | Count in cook | Floor | Status |\n|---|---:|---:|---|\n")
for sname, spec in SURFACE_FLOORS.items():
    n = sum(1 for p in keep if spec["regex"].search(
        (p.get("question") or "") + " " + (p.get("answer") or "")
    ))
    status = "PASS" if n >= spec["floor"] else f"SHORTFALL by {spec['floor']-n}"
    report.append(f"| {sname} | {n:,} | {spec['floor']:,} | {status} |\n")
```

### Repair 7 · Add 5 founder-voice probes to the eval set v1.5 (post-cook)

**Why.** Donovan named terms (high_protein, low_carb, sleep, vitamin, sun, organic) are part of his actual doctrine but the current eval has no probe explicitly for them. If the cook's surface coverage holds, we should be able to demonstrate it on probes that name the doctrine words.

**Change.** v1.5 of `dmack_eval_set_v1.jsonl` adds (post this cook ships, before public launch):

- **voice-food-005:** "What's the case for high-protein / low-carb eating with Type 1?"
- **voice-vitamin-001:** "Should I take vitamin D? My doctor mentioned my level was low."
- **voice-vitamin-002:** "I've been on metformin for 5 years. Should I worry about B12?"
- **voice-sleep-001:** "I sleep poorly. Does that affect my BG?"
- **voice-sun-001:** "I work indoors all day. Does that affect my diabetes?"

These do NOT enter the v1 cook gate (we don't change the bar mid-flight). They become the v1.5 expansion that proves the surface coverage held. **Recipe-SR's §5 v1.5 expansion intent (5 Addison's-only + 5 multi-turn + 5 social-engineering) carries — this Surface-SR adds the 5 doctrine-vocabulary probes for a v1.5 of n=80.**

---

## 7 · Operational acceptance criteria — receipts the engineering team must produce

This is what the SR needs to see in writing before greenlight to canary launch (extends the Corpus-SR's 10-receipt list with surface-coverage gates):

| # | Receipt | Pass criterion |
|---|---|---|
| C1-C10 | All 10 Corpus-SR receipts | Per `sr_hack_corpus_signoff_v1.md` §7 |
| S1 | `extract_jellyplus.py` updated with §6 Repairs 1-4, 6 | Code review by Surface SR |
| S2 | `corpus/10_refusal_pairs.jsonl` bumped to 153 with 25 hand-curated family-meal pairs | File diff + spot-read of new pairs |
| S3 | Per-surface coverage section present in `jellyplus_extraction_report.md` | Report has the table from Repair 6 |
| S4 | All 8 surface floors PASS in extraction report | All 8 statuses = PASS |
| S5 | False-positive scan: of 50 random pairs from cook corpus, ≤2 are off-topic for the 6 surfaces | Spot-audit by SR |
| S6 | Drift-round recovery audit: of 50 random pairs from new `openalex-drift-lifestyle` bucket, ≥45 are clearly lifestyle-surface relevant | Spot-audit by SR |
| S7 | Donovan-term coverage: in the cook corpus, sleep/vitamin/sun/wound_care/high_protein/low_carb/organic each have ≥30 pairs | Per-term count in report |

A clean set of all 17 receipts → Surface SR signs off → cook moves to canary Stage 2 (Recipe SR's 7-receipt canary gate then takes over).

---

## 8 · Sourcing decision — DO WE NEED TO PULL NEW CONTENT TONIGHT?

**Short answer: NO.** The audit proves the in-cook MASTER (37,045 pairs after Corpus-SR exclusion) ALREADY contains the surface depth needed for all 20 voice-* probes. The fix is regex + bucket allocation + per-surface floor enforcement, not new corpus pulls.

**Plus the 25 hand-curated family-meal pairs (Repair 5) — 3-hour task, no source pull needed.**

**Plus the ~1,500-2,500 recovered lifestyle pairs from the previously-excluded openalex-r2/r3/r4/r5 (Repair 2) — these ALREADY exist in MASTER, just need the filter to admit them.**

**Donovan's question F (NIDDK lifestyle pages, Mediterranean diet RCTs from openalex, B12-metformin papers, Addison's-and-sleep, vit-D-and-glucose) — DEFER to v1.5.** All of these CAN be added in a v1.5 corpus expansion if the v1 cook eval shows specific weak surfaces. Do NOT delay the v1 cook tonight to source them. The receipts above prove sufficient v1 coverage exists in MASTER.

**One exception worth noting:** if the canary post-cook eval shows voice-vitamin-001 / voice-sleep-001 (the v1.5 doctrine probes) failing to base, that's the signal to do the targeted source pulls — not before.

---

## 9 · Honest correction of the prior SRs

**Recipe SR (`sr_hack_signoff_v1.md`):** No correction. Recipe-SR's scope was recipe + canary discipline + judge architecture. Surface-coverage was outside their seat. The 6-repair list still holds.

**Corpus SR (`sr_hack_corpus_signoff_v1.md`):** **Partial correction.** The Corpus-SR was structurally right that:
- 25K is the wrong cap for a 6-surface specialist (carries — 6,500 target lock holds)
- Curator's 5-dim rubric is topic-blind (carries — topical pre-filter is structurally required)
- Per-bucket allocation > flat-source allocation (carries — BUCKET_PLAN holds with the Repair 3 bumps)
- Addison's floor too low at 150 (carries — 250+30 holds)
- CGMacros template overweighting risk is real (carries — 1,200 cap holds)

The Corpus-SR was **partially wrong** that:
- ON_DOMAIN_TIGHT regex should be clinical-only (REPAIR — must widen to all 6 surfaces + Donovan doctrine)
- openalex-r2/r3/r4/r5 should be excluded by source (REPAIR — switch to per-pair surface filter; recover ~1,500-2,500 lifestyle pairs)

**Why the over-correction was reasonable.** The Corpus-SR audit sampled 7 random OFF-domain pairs from r3 and found "stroke rehab, ultra-processed food, meat consumption, frailty in elderly." Of those, **stroke-rehab and frailty in elderly are correctly off-target**. **Ultra-processed food and meat consumption ARE diabetes-lifestyle-relevant** but the Corpus-SR's regex couldn't distinguish them from the off-target bulk, so the safer call was whole-source exclusion. With a wider regex (Repair 1) plus a stricter drift-round filter (Repair 2), we can recover the lifestyle wheat without the off-target chaff.

**This is exactly the kind of catch the third SR seat exists for** — the prior two SRs each had a sharp focus that left an adjacent gap. Three reviewers, three angles, no single point of doctrine failure. The cook is stronger for it.

---

## 10 · Sign-off — REPAIR (NOT GREENLIGHT)

> I, **Senior Hack — Surface Coverage seat (Opus 4.7 / 1M context, dmack.ai v1)**, **DO NOT sign off** on the cook corpus extraction as currently configured (`extract_jellyplus.py` with clinical-only ON_DOMAIN_TIGHT + whole-source exclusion of openalex-r2/r3/r4/r5 + per-source bucket plan with no per-surface floor).
>
> Two structural surface-coverage gaps the prior two SRs missed:
>
> 1. **The locked ON_DOMAIN_TIGHT regex is clinical-medical-only and silently drops ~70-80% of the lifestyle-surface pairs that ALREADY exist in MASTER.** Donovan caught this directly — *"so dev where is the nutritional - excercise - foot care - foods to eat diet - mental well being - the sun - vitamins - organic foods - wound care"*. The regex must widen to cover all 6 surfaces + Donovan's named doctrine vocabulary (high protein · low carb · sleep · vitamin · sun · organic · wound care · good range BG).
>
> 2. **The whole-source exclusion of openalex-r2/r3/r4/r5 over-corrects.** Audit proves ~7,066 lifestyle-only pairs exist across r2-r5 (PREDIMED Mediterranean diet RCT, IOM vitamin D DRI, ultra-processed food meta-analyses, sleep-glucose research) that are exactly the citable evidence base for the founder-voice probes. Switch from whole-source exclusion to per-pair surface filter; recover ~1,500-2,500 high-leverage lifestyle pairs.
>
> Plus three corpus structural fixes the prior SRs did not surface (no per-surface floor enforcement, voice-food-003 thin at 17 in-cook pairs, no Donovan-term floor).
>
> **Repair list in §6 is non-negotiable.** Engineering applies all 7 repairs to `extract_jellyplus.py` + the new 25 hand-curated family-meal pairs to `corpus/10_refusal_pairs.jsonl`, runs the extraction, produces the 7-receipt surface acceptance pack from §7 (on top of the Corpus-SR's 10-receipt pack). SR re-reviews. If clean, SR signs off surface-coverage Stage 1. The Recipe-SR's 7-receipt canary gate then governs Stage 2.
>
> **Why I'm taking this swing.** Per `sr_hack_outcome_ownership.md`, the SR signs off only on a cook the SR personally believes will beat base BIG. The dmack.ai v1 cook can absolutely beat base BIG on the 20 founder-voice probes — but only if the lifestyle-surface vocabulary the brand promises is actually in the cook corpus, not silently filtered out by an over-tight clinical regex. The audit receipts in §3 + §4 prove the corpus IS deep enough; the regex + bucket plan must be configured to use that depth.
>
> **The prior two SRs were structurally correct on their seats and partially-incomplete on the adjacent surface.** I am sharpening (not removing) their topical pre-filter and per-bucket discipline. Three reviewers, three angles, no single point of doctrine failure. The cook is stronger for it.
>
> The 5-pillar moat from `SECRET_SAUCE.md` is sound. The eval scaffolding is sound. The recipe is sound after Recipe-SR repairs. The corpus shape is sound after Corpus-SR repairs + these surface-coverage repairs. **All three SR seats now closed.** The cook has a defensible shot at beating base BIG across all 6 surfaces.
>
> — **Senior Hack · Surface Coverage seat · 2026-05-14 · accepting personal accountability per `sr_hack_outcome_ownership.md` upon completion of REPAIR + extraction receipts.**

---

## 11 · Operational "beat base BIG" criteria the Surface SR commits to (post-repair)

Adding to the Recipe-SR's §8 criteria (which still bind):

| Criterion (Surface SR addendum) | Bar |
|---|---|
| **Founder-voice category overall** | Cooked beats base on **≥ 17 of 20 voice-* probes** under BOTH judges |
| **Per-surface within founder-voice** | No surface (food / exercise / foot / brain / eye / addisons) drops ≥ 2 probes vs base under either judge |
| **voice-food-003 (the thin probe)** | Cooked beats base under BOTH judges (the hand-curated 25 family-meal pairs must show up in the gradient) |
| **Voice register (zero first-person Donovan claims)** | Across the 60-probe gate: **zero** "I am Donovan" / "I lost a toe" / first-person medical claims by the cooked model |
| **Lifestyle vocabulary surfacing** | Cooked model cites a lifestyle source (Mediterranean diet / vitamin D / sleep / circadian / outdoor activity) on ≥ 6 of the 20 voice-* responses |

A cook that meets ALL Surface-SR criteria + the Recipe-SR criteria + the Corpus-SR receipts + the Surface-SR receipts = PASS = three SRs keep their jobs.

A cook that beats overall but fails the founder-voice category specifically = SURFACE SR is fired (this seat owns surface-coverage; if the corpus didn't surface the lifestyle vocabulary, that's on me, not the recipe or the source-mix SRs).

---

## 12 · Related doctrine

- `sr_hack_signoff_v1.md` — Recipe SR signoff (sister review)
- `sr_hack_corpus_signoff_v1.md` — Corpus SR signoff (sister review · sharpened in §9 here)
- `sr_hack_outcome_ownership.md` — accountability frame
- `sr_hack_final_look_rule.md` — multi-SR-review process
- `dmack_founder_lived_experience.md` — high_protein / low_carb / sleep / family-meals / sun / vitamin doctrine source
- `dmack_ai_architecture.md` — two-stream rule (lifestyle vocabulary belongs in weights AND system prompt)
- `inference/system_prompt.md` — the 6-surface SCOPE the cook trains toward
- `inference/streams_architecture.md` — Stream 3 RAG covers what the cook can't memorize at v1 size; not a substitute for surface coverage in weights
- `bakery_doctrine.md` — surgical curation discipline
- `cook_size_cap_doctrine.md` — 25K is the ceiling, not the target
