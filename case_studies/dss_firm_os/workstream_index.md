# DSS Hack Fleet — Workstream Index

Mirrors the Atlas Firm OS pattern (Senior MD + Underwriter + Book Maker + Closing + 10-Hack fleet) applied to commerce instead of brokerage. Each hack is a focused specialist with a tight Mission / Scope / Output contract.

## The hacks

| # | Hack | Type | Output owner | Gates |
|---|---|---|---|---|
| 01 | Product Sourcing | Research | `/data/research/` + `/data/products/` | Feeds Hack 5 catalog |
| 02 | Supplier Outreach | Research + outreach | `/data/suppliers/` + `/data/vendor_outreach/` | Feeds Hack 4 distribution |
| 03 | Compliance & Claims | Review | `/data/compliance/` + `/docs/compliance/` | **Gates Hacks 1, 5, 6, 7** |
| 04 | Dropship & Distribution | Research | `/data/dropship/` + `/data/distribution/` + `/reports/` | Feeds Hack 8 launch |
| 05 | Catalog Data | Build | `/data/products/seed_products.ts` etc. | Needs Hacks 1, 3 |
| 06 | Dmack AI Skills | Spec | `/skills/dmack_ai/` etc. | Needs Hack 3 |
| 07 | SEO + GEO Content | Build | `app/` (site code) + `/docs/strategy/` | Needs Hack 3 for copy review |
| 08 | Operations & Launch | Build SOPs | `/docs/operations/` + `/docs/launch/` | Synthesizes 1–7 |

## Run order

```
                ┌─── 01 (sourcing) ─────────┐
                ├─── 02 (suppliers) ────────┤
   03 (compliance)                          ├─── 05 (catalog) ─── 08 (launch)
        │       ├─── 04 (distribution) ────┘
        │       │
        └───────┼─── 06 (AI skills) ───────────┘
                │
                └─── 07 (SEO + GEO content) ───┘
```

**03 is the constraint** — every other hack's copy/claims/recommendations must pass Compliance review before shipping. Run 03 first (or in parallel with the research hacks, with a sync gate before publish).

## Parallelization advice

- **Run in parallel** (research-heavy, no shared code edits): 01, 02, 03, 04
- **Run after**: 05, 06, 07 (need outputs from above)
- **Run last**: 08 (synthesizes everything)
- **Coordinator**: the operator (or Senior Hack) reviews each Hack's final report before promoting outputs into the live site/catalog

## Quality bar (applies to every hack)

- Real research, sourced URLs — never fabricate suppliers, partnerships, or claims
- Mark unknowns explicitly: `needs verification`, `pricing unavailable — request wholesale sheet`, `dropship unclear — contact supplier`
- Output to the contracted file path, no surprise destinations
- Final markdown report at `/reports/<hack-name>_report.md` with a recommendations section the operator can act on
- Trust > conversion. No fear-based copy. No overpromises. No medical authority claims.

## How to invoke a hack

When delegating to an agent (Claude Code Agent tool or operator), pass the path to the brief:

```
Read /home/swarm/Desktop/diabetic-supply-shop/tasks/agent_workstreams/01_product_sourcing_hack.md and execute the workstream. Stay strictly within the documented scope and quality bar.
```
