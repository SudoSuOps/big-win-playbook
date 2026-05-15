# Big Win Playbook

> **The doctrine, templates, and case studies for actually beating base models.**
>
> Built by the Swarm & Bee firm in the dmack.ai v1 cook (2026-05-14). Owned by Donovan Mackey. Licensed to operate within the firm. We win, validates the pattern. We lose, this is the receipt of why.

---

## The thesis

Most fine-tuned LLMs lose to base. The data is brutal:
- Atlas-Qwen-27B v1 cooked 244,000 pairs with the Gold Standard recipe and full discipline → **net regression on 6 of 10 institutional CRE prompts vs base**
- Curator-Mistral-3B v2 cooked 501 surgical pairs → **beat its predecessor but never beat base outright on a locked institutional eval**
- Industry-wide: most published fine-tunes are evaluated against weaker baselines; the few that face base + a real eval mostly lose

That's the receipt. **Fine-tuning to beat base is hard, and the firm-OS discipline that produces a winning cook is most of the work.**

This playbook is that discipline, codified.

---

## The five-layer pattern

Every cook in this playbook follows the same shape:

```
1 · DOCTRINE     ← the rules of the game (this repo's /doctrine)
2 · BRIEFS       ← specialist hack contracts (per-cook · in /workstreams)
3 · EXECUTION    ← code + corpus + recipe (per-cook · in /case_studies)
4 · GATE         ← dual-judge eval + human blind read (binding)
5 · RECEIPT      ← Hedera-anchored Defendable verdict OR PROPOLIS evidence
```

Each layer owns its accountability. SRs sign off on briefs. MDs sign off on architecture. Founder owns outcomes when MDs are fired.

## The accountability rule

> **Every cook has a named owner with skin in the game.**
> If the cook fails to beat base big, the owner is fired and ownership escalates one rung up the food chain.

Locked in `doctrine/outcome_ownership.md`. Demonstrated live in `case_studies/dmack_ai_v1/`.

## Repo map

| Path | What lives here |
|---|---|
| `doctrine/` | The rules — what discipline applies to every cook |
| `templates/` | Reusable patterns — cook recipe, SR signoff, eval set, runner scripts |
| `scripts/` | Reference implementations — pre-flight, spot-audit, blind-read, base-verify |
| `workstreams/` | Hack brief templates — when you build a firm OS for a project |
| `case_studies/` | Real cooks under this playbook — what worked, what didn't |
| `case_studies/dmack_ai_v1/` | The first cook to use this playbook end-to-end (in flight 2026-05-14) |
| `case_studies/dss_firm_os/` | The firm-OS proof on the commerce side (DSS · 2026-05-14) |

## Status

| Cook | Doctrine applied | Verdict |
|---|---|---|
| dmack.ai v1 | Full pattern · 3 SR seats fired pre-cook · MD signed off | **In flight 2026-05-14** |
| DSS firm OS | 8-hack workstream pattern · 4 parallel agents · 1 session ship | **Validated 2026-05-14** ✅ |
| Atlas-Qwen-27B v1 | Pre-playbook · single SR review · no MD layer | **PROPOLIS** (net regression vs base) — the failure receipt this playbook is built to prevent |

## Read order for a new operator

1. `README.md` (this file)
2. `doctrine/firm_os_pattern.md` — the architectural thesis
3. `doctrine/outcome_ownership.md` — the accountability rule
4. `doctrine/canary_then_cook.md` — the 5-stage discipline
5. `doctrine/bakers_before_baker.md` — the "must beat base" gate
6. `case_studies/dmack_ai_v1/sr_md_signoff.md` — what a binding cook sign-off looks like
7. `templates/cook_recipe_template.md` — what a cook plan looks like
8. `case_studies/dmack_ai_v1/lessons_learned.md` — post-cook (filled in after verdict)

## Owned by

Donovan Mackey · Swarm & Bee LLC · Florida · D-U-N-S 138652395

Reach: hello at swarmandbee dot ai
