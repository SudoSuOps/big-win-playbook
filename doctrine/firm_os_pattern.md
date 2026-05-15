# Firm OS Pattern

> The architectural thesis: build the firm, then build the product. The firm's discipline is what produces a winning cook.

## The org chart

```
                       ┌─────────────────────────┐
                       │  Founder · Operator     │   ← outcome of last resort
                       └────────────┬────────────┘
                                    │
                       ┌────────────▼────────────┐
                       │ Senior Managing Director │   ← architectural cross-cut
                       │   (MD seat · per cook)  │     · owns the bet
                       └────────────┬────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
       ┌──────▼──────┐       ┌──────▼──────┐       ┌──────▼──────┐
       │ Senior Hack │       │ Senior Hack │       │ Senior Hack │
       │   (Recipe)  │       │  (Corpus)   │       │ (Surface...│
       │             │       │             │       │             │
       │ owns one    │       │ owns one    │       │ owns one    │
       │ slice       │       │ slice       │       │ slice       │
       └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
              │                     │                     │
              └─────────────────────┴─────────────────────┘
                                    │
   ┌──────────┬──────────┬──────────┼──────────┬──────────┬──────────┐
   │          │          │          │          │          │          │
┌──▼──┐   ┌──▼──┐    ┌──▼──┐    ┌──▼──┐    ┌──▼──┐    ┌──▼──┐    ┌──▼──┐
│Hack │   │Hack │    │Hack │    │Hack │    │Hack │    │Hack │    │Hack │
│  1  │   │  2  │    │  3  │    │  4  │    │  5  │    │  6  │    │  7  │
└─────┘   └─────┘    └─────┘    └─────┘    └─────┘    └─────┘    └─────┘
specialist work · narrow scope · feeds upward via deterministic outputs
```

## The doctrine

1. **Specialists at the bottom · generalists at the top.** Hacks own a single workstream and a single output contract. SRs review one slice at higher rigor. MD reads across all slices. Founder owns the firm.

2. **Outputs are contracted, not negotiated.** Every layer produces deterministic artifacts (CSV / JSON / MD / code) the next layer up consumes. No tribal knowledge. No "ask the senior person what they meant."

3. **Discipline is what scales.** The same firm OS works for a CRE brokerage (Atlas), a commerce build (DSS), an AI cook (dmack.ai). Different domain · same shape.

4. **Compliance is the floor, not the ceiling.** Every firm has a gating constraint (Compliance · Safety · Eval-set authorship · Tribunal). It runs in parallel with research-heavy hacks but downstream hacks (catalog · code · ship) wait for its sign-off.

5. **Parallel by default · gated by review.** Most hacks run in parallel. They sync at the gating constraint and at the synthesis hack at the end.

6. **Outcome accountability is real.** Per `outcome_ownership.md` — every layer's sign-off carries personal accountability. Fail → fire → escalate up.

## What this pattern produced (receipts)

### DSS Firm OS · validated 2026-05-14 (1 session)

8 specialist hack briefs written → 4 research hacks fired in parallel as background agents → all 4 returned within ~12 min · all 4 converged independently on the same MVP shape (Cardinal Health anchor · hybrid dropship+self-fulfilled · same compliance pattern) → 3 build hacks ran sequentially → final synthesis (launch checklist + readiness report) shipped.

**Result**: full firm OS scaffold for Diabetic Supply Shop. 8 hack briefs · 6 hack reports · 4 SOPs · 7 dmack.ai skill specs · launch checklist · 50-product merged catalog candidate · 65 vetted suppliers · `om.diabeticsupplyshop.com` review dashboard live with Cloudflare Access. **Donovan's verdict: "firmOS doctrine is cracked fren ill review"** — pattern validated.

### dmack.ai v1 cook · in flight 2026-05-14

Same firm OS pattern applied to AI training:
- 7 specialist hack briefs (sourcing → suppliers → compliance → distribution → catalog → AI skills → SEO)
- Recipe SR caught 6 doctrine violations the engineering team missed (packing+SDPA bug, QLoRA-on-Qwen, single-judge gate)
- Corpus SR caught 8 more the Recipe SR missed (25K cap too lenient, topic-blind Curator filter, openalex over-pull)
- Surface Coverage SR caught 1 more the Corpus SR over-corrected on (Donovan caught it first)
- All 3 SRs fired before cook fired (anticipatory · pattern-of-compounding-gaps signal)
- MD seat signed off with 3 architectural augmentations (per-surface floor · human blind-read · MARGINAL ship plan)
- Cook fires with 14 doctrine repairs applied + 17 operational receipts gating launch + dual-judge eval gate enforcing the verdict

**Outcome pending. The result either validates the pattern (first Swarm cook to beat base big) or refutes it.**

## When to use this pattern

- Multi-stream ambiguous build (commerce build · AI cook · ecosystem product)
- High-stakes outcome with measurable success criteria
- Specialist domains where one operator can't hold all the rigor
- Anywhere "ship blind and hope" has historically lost

## When NOT to use this pattern

- Simple one-shot builds (no need for hack fleet)
- Tight time pressure where overhead > value (the doctrine takes ~30 min to set up before any hack fires)
- Domains with no measurable success gate (the playbook depends on having a "did we beat base" verdict)

## Anti-patterns the pattern prevents

- **Volume-induced signal scatter** — Atlas v1's 244K-pair cook → net regression. Bakery doctrine + 25K cap + Curator-tier-filter prevents this.
- **Single-judge bias** — judge selected the corpus AND grades the eval. Dual-judge gate eliminates.
- **Doctrine drift** — engineer cooks with `packing=True` because TRL defaults · SR catches because doctrine says `packing=False` for SDPA on Blackwell · the discipline is in the review, not the engineer's memory.
- **No accountability** — Atlas v1 failed and nobody was named. Outcome ownership rule fixes this.
- **Binary outcome** — "cook ships OR firm has nothing." MARGINAL ship plan (P3.5 dual-routing) kills the binary trap.

## Related doctrine

- `outcome_ownership.md` — the accountability rule
- `canary_then_cook.md` — 5-stage discipline that gates Stage 3 (full cook)
- `bakers_before_baker.md` — the "beat base" gate
- `bakery_doctrine.md` — less is more · 500-1000 surgical pairs > 25K bulk
- `25k_cap.md` — the firm-wide ceiling
- `senior_hack_final_look.md` — the SR review process
- `correction_loop.md` — qualitative judgment beyond eval numbers
