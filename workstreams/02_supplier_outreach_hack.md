# Hack 02 — Supplier Outreach

## Mission
Build the supplier database. Identify manufacturers, wholesalers, authorized distributors, and dropship-friendly suppliers across the five DSS categories. Produce ready-to-send outreach templates so the operator can open accounts efficiently.

## Scope
- US-based suppliers preferred (faster shipping, simpler compliance)
- Wholesale, dropship, and manufacturer-direct channels
- B2B platforms (Faire, Tundra, Abound, Wholesale Central, Thomasnet) — vetted carefully
- Alibaba / Asian sourcing ONLY for non-medical accessories (mirrors, organizers) — never for items in skin contact, wound contact, or ingestion
- Book distributors (Ingram, Baker & Taylor wholesale, Amazon Advantage research)

## Research targets per supplier
Each entry in the database must include all these fields (or `unknown — needs verification`):
- `supplier_name`
- `website`
- `category` (one of the five DSS categories, or multi)
- `brands_carried`
- `wholesale_available` (yes / no / unknown)
- `dropship_available` (yes / no / unknown)
- `moq` (minimum order quantity)
- `margin_estimate`
- `shipping_origin`
- `country`
- `contact_email`
- `contact_phone`
- `account_application_url`
- `reseller_requirements` (resale cert? business license? website live?)
- `licensing_notes` (medical device class? supplement GMP?)
- `risk_notes`
- `quality_score` (1–5)
- `priority_score` (1–5)
- `next_action`

## Output files
- `/data/suppliers/supplier_candidates.csv` — full database
- `/data/vendor_outreach/vendor_contact_tracker.csv` — stage tracker (`emailed`, `awaiting_response`, `account_pending`, `approved`, `rejected`, `declined_to_pursue`)
- `/docs/procurement/vendor_outreach_templates.md` — 7 outreach templates (see below)

### Outreach templates needed
1. Wholesale account request
2. Dropship partnership request
3. Manufacturer direct inquiry
4. Authorized reseller request
5. Private label inquiry
6. Book distributor inquiry
7. Organic wellness supplier inquiry

Each template:
- Names DiabeticSupplyShop.com + the prevention-first founder mission
- Names the founder (Donovan Mackey — Type 1 + lived experience credential)
- Asks for: catalog, MOQ, pricing/tier breaks, shipping terms, MAP policy, reseller requirements
- Professional tone — no fluff, no aggressive sales language
- Includes business context (Florida LLC if needed, EIN ready to provide)

## Quality bar
- **No fabricated supplier relationships.** Every supplier gets a URL.
- **Prioritize accessibility**: a wholesaler who answers email > a famous brand who ignores small shops
- **Flag licensing requirements explicitly**: any supplier requiring medical-device licensing for resale gets `risk_notes` populated
- **Outreach templates must be sendable as-is** — operator should be able to fill in `[supplier name]` and hit send

## Things to avoid
- Spammy outreach copy
- Suppliers with active FDA warning letters (research before adding)
- Single-source dependency for any category (always identify ≥ 2 viable suppliers per critical product)
- Counterfeit-risk marketplaces for items in skin/wound/ingestion contact

## Final deliverables
1. Supplier database with ≥ 40 vetted candidates across all 5 categories
2. Contact tracker pre-populated for the top 15 most promising
3. 7 outreach template versions, sendable
4. Report at `/reports/supplier_outreach_report.md` — top 10 to approach first, gating risks, recommended sequencing
5. Handoff note for Hack 04 (distribution): which suppliers do their own fulfillment vs require 3PL
