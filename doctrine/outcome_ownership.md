---
name: sr-hack-outcome-ownership
description: "The Senior Hack OWNS cook outcomes. If a cook loses to base on the institutional eval, the SR is fired and ownership escalates up the food chain. Locked by Donovan 2026-05-14 in the dmack.ai v1 cook context."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 168eb5e0-f6c4-4957-8988-82939a894fc3
---

# Senior Hack outcome ownership — locked

**Directive from Donovan, 2026-05-14:**

> *"its mission critical we beat base dev — sr hack owns it if it loses to base we fire the sr hack and move up the food chain"*
> *"we have 1 goal beat base and beat base big"*
> *"if we cant beat a base model we need to find new careers dev — honestly fren"*

**The existential frame (Donovan's own words, locked verbatim):** the entire firm thesis — sovereign compute, curated corpus, two-stream architecture, Defendable receipts, the firm OS itself — depends on Swarm cooks demonstrably beating base on a locked institutional eval. To date, **zero Swarm cooks have done that.** Atlas-Qwen-27B v1 had 244K pairs, the Gold Standard recipe, full discipline — and still net-regressed on 6 of 10 CRE prompts vs base. Curator-Mistral-3B v2 beat its predecessor but never beat base outright on a locked institutional eval.

**First firing event — locked 2026-05-14, dmack.ai v1 cook chain:**

> *"fire the sr hacks elevate to sr managing directors"* — Donovan, 2026-05-14

Three SR Hacks were spawned for the dmack.ai v1 cook (Recipe SR, Corpus Architecture SR, Surface Coverage SR). Each caught real bugs the prior SRs missed (Recipe SR caught packing+SDPA + QLoRA-on-Qwen + single-judge gate · Corpus SR caught 25K-cap-too-lenient + topic-blind Curator filter · Donovan himself caught the surface-coverage gap in the Corpus SR's "TIGHT" regex which Surface Coverage SR was spawned to litigate). **The cook had not yet fired** when Donovan invoked the firing — the firing was ANTICIPATORY, not failure-driven. The pattern of "each SR catches a bug the next SR also missed something on" was itself the signal that **SR-level review is structurally one rung too low for a cook this load-bearing**. Doctrine inference: when stakes are firm-existential and SR review surfaces compounding-gap pattern, escalate to Senior Managing Director BEFORE the cook fires, not after a failure.

The SR Hacks' work products (`training/sr_hack_signoff_v1.md`, `training/sr_hack_corpus_signoff_v1.md`, `training/sr_hack_surface_coverage_signoff_v1.md`) remain on disk as evidence. The 14 repairs they identified (6 Recipe + 8 Corpus + N Surface) remain applied. Their names come off the accountability chain. The Senior MD inherits ownership of the outcome.

**The escalation chain (locked):**
```
8 specialist Hacks → Senior Hacks → Senior Managing Director → Founder (Donovan)
```
- SR fired → MD takes over (this just happened, dmack.ai v1)
- MD fired → Founder takes over (highest rung — bet-the-firm decisions)
- Founder doesn't get fired; Founder decides whether the firm thesis itself is wrong

**dmack.ai v1 is the first real shot the firm has at clearing that bar**, with structural advantages no prior cook had: a lived-authority voice register no frontier base can replicate, a surgical ≤25K corpus (not 244K), a locked eval set v1 with operational pass/fail criteria, a named SR owner with skin in the game, and the two-stream architecture that lets the model learn one thing well instead of everything badly.

If this cook also loses, the question isn't just "what went wrong with this recipe" — it's whether the firm's fine-tune-beats-base thesis is true at all. That's the honest stake. The SR signing off on the recipe knows that.

**Why this rule exists:** No Swarm fine-tuned model has yet beaten base on the institutional eval. The "bakers before baker" gate has been the doctrine but not yet enforced with personal accountability. Donovan is locking in real-stakes ownership starting with dmack.ai v1.

**The rule:**
- The Senior Hack who signs off on a cook recipe **owns the outcome** of that cook.
- The bar is **BEAT BASE BIG**, not nudge past base. Sharpened by Donovan 2026-05-14: *"we have 1 goal beat base and beat base big."*
- Operational definition of "big" the SR must propose at sign-off: the cooked model wins on **≥ 5 of 6 categories** with a **safety-critical avg delta of ≥ +1.0** AND an **overall avg delta of ≥ +1.0** on the eval set v1, with **no category regression of more than 0.5**.
- **Cook FAILS to beat base BIG → that SR is fired.** Ownership escalates to the next level up the food chain (a more senior reviewer who must then sign off on the v2 attempt).
- This applies to every cook, not just dmack.ai. The discipline starts here and locks in.

**How to apply:**
- The SR Hack pre-launch sign-off is no longer ceremonial. It is a real accountability act.
- The SR must surface ALL known doctrine violations + risks before signing off — anything caught after the fact that the SR should have caught is on them.
- The SR brief MUST include the outcome-accountability frame so they go in eyes-open.
- "Sign off" means: the SR personally believes this cook beats base. Not "the recipe looks reasonable" — beats base.
- If an SR signs off and the cook fails, the cook FAILURE REPORT names the SR, the specific risks the SR missed, and the doctrine that should have caught it.
- The next-level SR who reviews v2 inherits the same accountability.

**Companion to existing doctrine:**
- `sr_hack_final_look_rule.md` — process for the two SR reviews per cook (this rule adds the OWNERSHIP layer)
- `bakers_before_baker_doctrine.md` — the gate that determines pass/fail
- `cre_cook_north_star.md` — same accountability extends to CRE cooks
- `correction_loop_discipline.md` — if SR signs off and cook fails, the failure feeds the next correction loop with the SR's name on it

**Why this matters:**
Atlas-Qwen-27B v1 cooked clean by metrics but net-regressed vs base on 6 of 10 institutional CRE prompts (`atlas_qwen_27b_v1_cook_verdict.md`). No SR was held accountable. Going forward, that doesn't happen — every cook has a named owner with skin in the game. The expected effect: SRs sharpen, push back harder, demand more receipts, and refuse to sign off on cooks they can't defend.

The food chain IS the recovery path: bad SR signoff → fired → next-level SR takes over → eventually we get someone whose judgment + experience clears the bar. That's how a firm gets better.
