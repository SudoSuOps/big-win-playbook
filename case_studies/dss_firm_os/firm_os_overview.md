# Diabetic Supply Shop — Firm OS

## What this is
DSS is structured as an **operating firm**, not just a website. Same shape as the Atlas Firm OS pattern — a small org chart with specialist hacks running their own workstreams. The repo is the command center.

## Org chart

```
                       ┌─────────────────────────┐
                       │   Founder · Operator    │
                       │     Donovan Mackey      │
                       └────────────┬────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
       ┌──────▼──────┐       ┌──────▼──────┐       ┌──────▼──────┐
       │  Senior Hack │       │  Compliance │       │  Engineering│
       │  (review +   │       │  Reviewer   │       │     Lead     │
       │   sign-off)  │       │  (Hack 03)  │       │   (this LLM) │
       └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
              │                     │                     │
              │                     │                     │
   ┌──────────┼──────────┬──────────┼──────────┬──────────┼──────────┐
   │          │          │          │          │          │          │
┌──▼──┐   ┌──▼──┐    ┌──▼──┐    ┌──▼──┐    ┌──▼──┐    ┌──▼──┐    ┌──▼──┐
│ H01 │   │ H02 │    │ H04 │    │ H05 │    │ H06 │    │ H07 │    │ H08 │
│Sour-│   │Sup- │    │Drop-│    │Cata-│    │Dmack│    │SEO +│    │Ops +│
│cing │   │plier│    │ship │    │log  │    │AI   │    │GEO  │    │Lnch │
└─────┘   └─────┘    └─────┘    └─────┘    └─────┘    └─────┘    └─────┘
```

## Doctrine

### 1. Trust > Conversion
DSS serves people whose disease never stops. Every brand decision answers "would Donovan tell this to his wife / kids?" before "does this convert?"

### 2. Compliance is the floor, not the ceiling
Hack 03 gates everything. No copy ships without compliance sign-off. No AI output ships without Claims Checker review. The disclaimer language is brand voice, not lawyer noise.

### 3. Prevention-first
Every product earns its slot against the prevention-first frame. If a product doesn't help someone stay ready for the work, it doesn't belong on this shop.

### 4. Lived authority, never medical authority
Donovan is the voice. Documented sources (ADA / IWGDF / Endocrine Society / NIDDK) are the facts. Same two-stream rule as the dmack.ai cook.

### 5. The repo is the operating system
Every workstream produces structured output (CSV, JSON, MD) that the next workstream consumes. No tribal knowledge. A new operator should be able to pick up any hack brief and execute.

### 6. Parallel by default, gated by compliance
Most hacks run in parallel. They sync at compliance review and at the launch readiness gate.

## Sister brand alignment

| | DiabeticSupplyShop.com | Dmack.ai |
|---|---|---|
| Surface | Commerce + education | AI companion |
| Asset | Curated supplies | Trained model + RAG |
| Voice | Founder-led prevention-first | Founder-voice with documented-source authority |
| Brand bridge | Founder story on both | Same Donovan-as-voice rule |
| Revenue | Product sales | Subscription / per-conversation (TBD) |
| Compliance | Same rules | Same rules |

## Pipeline overview

```
01 Sourcing ──→ 05 Catalog ──→ Site live
02 Suppliers ──→ 04 Distribution ──→ Operational
03 Compliance ──→ gates everything
06 Dmack AI Skills ──→ Companion live
07 SEO + GEO ──→ Discoverability
08 Operations + Launch ──→ Synthesis + go-live
```

## See also
- `/tasks/agent_workstreams/README.md` — workstream index + how to invoke a hack
- `/tasks/agent_workstreams/0[1-8]_*_hack.md` — the eight hack briefs
- Memory: `dmack_founder_lived_experience.md`, `dmack_ai_architecture.md`, `founder_family_office_posture.md`
