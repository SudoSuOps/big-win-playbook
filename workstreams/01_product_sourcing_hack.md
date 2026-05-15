# Hack 01 — Product Sourcing

## Mission
Find high-quality products in the five DSS categories — Foot Care, Wound Care, Diabetic Essentials, Wellness Support, Books & Education — that earn a slot in a daily prevention-first routine.

## Scope
- Real products you can verify (manufacturer URL, retailer presence, recent reviews).
- US-available with reasonable shipping economics.
- Pricing tier appropriate for everyday diabetic supplies (not $5 commodity, not luxury).
- No medical-device-class products that require licensing to resell (insulin, prescription wound care, etc.).
- Five-category coverage with priority weight:
  1. Foot Care (primary — Donovan's lived authority)
  2. Wound Care preparedness (NOT serious wound treatment)
  3. Diabetic Essentials (daily)
  4. Books & Education
  5. Wellness Support (carefully — no disease claims)

## Research targets per product
- Manufacturer + brand
- Retail price band (low / mid / premium)
- Why it earns its slot (single sentence — must align with prevention-first mission)
- Lived-experience relevance (does it solve a problem Donovan has lived? if yes, note it)
- Compliance risk band (low / medium / high) — flag Hack 03 review needed
- Supplier candidates known (feeds Hack 02)
- Substitutes (so we have fallbacks if one supplier fails)

## Output files
- `/data/research/product_research_matrix.csv` — full scoring matrix (see fields below)
- `/data/products/product_candidates.json` — structured candidates ready for catalog ingestion
- `/reports/product_sourcing_report.md` — narrative with top picks, category coverage analysis, gaps, risks

### CSV fields
`product_name, category, subcategory, supplier_candidate, estimated_cost, estimated_retail_price, estimated_margin_percent, mission_fit_score, customer_need_score, quality_confidence_score, supplier_reliability_score, shipping_simplicity_score, compliance_risk_score, bundle_potential_score, notes, recommendation`

All scores 1–5. Recommendation: `MVP`, `Phase 2`, `Skip`, `Pending Compliance`.

## Quality bar
- **No fabrication.** Every supplier candidate gets a URL. Every "estimated" price is sourced or marked `estimated — verify with sample order`.
- **Compliance-first**: any product whose category copy could imply disease treatment goes to Hack 03 with `compliance_risk_score >= 4` for review.
- **Margin reality check**: if estimated margin < 35%, justify why it stays (loss leader, halo product, mission-critical).
- **Mission alignment**: every product earns a one-sentence "why this is on Diabetic Supply Shop" — if you can't write it, the product doesn't belong.

## Things to avoid
- Miracle-cure supplements (gymnema "cures diabetes" stuff)
- Generic dropshipped Amazon junk with no brand authority
- Anything requiring medical device licensing without verifying we can resell
- Diabetic socks at $2 wholesale that compete on price-floor only — we sell on prevention, not on lowest-cost commodity
- Counterfeit-prone categories (CGM accessories, lancets from no-name suppliers)

## Final deliverables
1. Product research matrix CSV with 100–250 candidates
2. Candidate JSON with the top ~50 (MVP-recommended)
3. Sourcing report calling out: top 25 MVP picks, 10 must-stock bundle anchors, gaps, compliance flags
4. Handoff note for Hack 02 listing suppliers worth approaching first
