# Hack 04 — Dropship & Distribution

## Mission
Decide HOW orders get fulfilled. Research the realistic options across pure-dropship, wholesale-held inventory, 3PL, hybrid, marketplace-assisted, and Shopify-ecosystem fulfillment. Recommend the MVP fulfillment shape and the v2 evolution.

## Scope
- Pure dropship (supplier ships direct to customer)
- Wholesale inventory at home / office / small warehouse
- 3PL fulfillment (ShipBob, ShipMonk, Easyship, Red Stag, etc.)
- Amazon MCF (Multi-Channel Fulfillment using FBA inventory)
- Shopify fulfillment network / Shopify Fulfillment Network alternatives
- Hybrid models (some held, some dropshipped)

## Research targets
For each option:
- Setup cost / time
- Per-order cost (pick + pack + ship for typical DSS order — ~3-5 items, ~2 lbs)
- Minimums (some 3PLs have monthly minimums)
- Onboarding complexity
- Integration with Next.js + Stripe + (eventually) Shopify
- Diabetic-supply specific concerns (lancets / sharps + IATA / DOT shipping?)
- Returns process (especially for unopened items)
- US-wide coverage / multi-warehouse for 2-day shipping economics
- Custom packaging support (matters for brand)

## Output files
- `/data/dropship/dropship_services.csv` — services scored
- `/data/distribution/fulfillment_options.csv` — full option matrix including 3PLs and Amazon MCF
- `/reports/distribution_strategy.md` — narrative recommendation with MVP shape + v2 evolution + cost projection

### CSV fields
`option_name`, `type` (dropship / 3pl / mcf / hybrid / in-house), `setup_cost`, `per_order_cost_estimate`, `monthly_minimum`, `onboarding_weeks`, `integration_method`, `usa_coverage`, `returns_handling`, `custom_packaging`, `diabetic_supply_notes`, `quality_score` (1–5), `priority_score` (1–5), `risk_notes`

## Recommended baseline (validate against research)
- **MVP**: Hybrid — start dropship + a small held inventory for high-trust kits (Daily Foot Protection Kit) and fast-moving foot-care items. Single-warehouse to start.
- **v2**: Add 3PL when order volume justifies (~50+ orders/day) and 2-day shipping economics start mattering.
- **AVOID v1**: Direct medical-device-class items requiring licensing, sharps that need IATA-trained shippers.

## Quality bar
- Real cost ranges sourced from vendor websites or industry data — no made-up numbers
- Diabetic-supply specifics addressed (lancets / sharps shipping is a real thing)
- "Vibes" recommendations are unhelpful — every recommendation must cite the trade-off
- Returns process explicit — unopened items return-eligible, opened wound-care / consumables don't

## Things to avoid
- Recommending a 3PL with $500+ monthly minimums for an unlaunched store
- Suggesting Amazon MCF for items that compete with Amazon's own listings (race-to-bottom risk)
- Ignoring the customs / international angle if any supplier ships from outside US
- Ignoring CO2 / waste — eco-conscious packaging is brand-aligned

## Final deliverables
1. Dropship services CSV (≥ 15 vetted)
2. Fulfillment options CSV (≥ 8 options across all types)
3. Distribution strategy report with MVP + v2 recommendation + cost projection at 10/50/200 orders/day
4. Sharps + lancets compliance note (separate one-pager)
5. Handoff for Hack 08 (launch): operational SOPs for the chosen fulfillment shape
