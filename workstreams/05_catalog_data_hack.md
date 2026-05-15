# Hack 05 — Catalog Data

## Mission
Convert Hack 01's researched products into the actual ecommerce catalog. Owns the `lib/products.ts` and `lib/categories.ts` data, the seed kits, and the product schema documentation.

## Scope
- Read Hack 01 outputs (`/data/research/product_research_matrix.csv` + `/data/products/product_candidates.json`)
- Pass each through Hack 03 compliance review (only `approved` or `softened-approved` items get cataloged)
- Build the typed seed catalog matching the existing `lib/types.ts` `Product` shape
- Build the 5 starter kits as Kit records
- Write product schema documentation so future operators can add products without breaking the contract

## Output files
- `/data/products/seed_products.ts` — typed product array, drop-in for `lib/products.ts`
- `/data/products/products.json` — same data in JSON for non-TS consumers
- `/data/products/product_schema.md` — field-by-field documentation, examples, edge cases
- `/data/kits/starter_kits.json` — the 5 starter kits with component product IDs
- `/reports/catalog_readiness_report.md` — readiness summary, gaps, recommended next products

## Starter kits (build these as Kit records)
1. **Daily Foot Protection Kit** — diabetic socks + foot mirror + moisturizer + toe cushions + foot-care guide
2. **Wound Preparedness Kit** — non-stick dressings + gauze + medical tape + saline wash + safety guide
3. **Travel Diabetic Essentials Kit** — alcohol wipes + glucose tablets + sharps container + travel pouch + log card
4. **Caregiver Foot Check Kit** — foot mirror + checklist + socks + moisturizer + caregiver guide
5. **Prevention Starter Bundle** — foot-care kit + wound preparedness kit + log book + education guide

## Product schema (matches `lib/types.ts`)
Every product:
- `id`, `slug`, `name`, `category` (one of the 5 category slugs)
- `shortDescription` (≤ 160 chars — must be compliance-approved)
- `longDescription` (no medical claims — Hack 03 must approve)
- `price` (cents — integer, no floats)
- `compareAtPrice?` (cents)
- `image: { label, accent }`
- `tags: string[]`
- `featured?`, `inventoryStatus` (`in_stock | out_of_stock | preorder`)
- `medicalDisclaimer?`, `supplementDisclaimer?` (booleans → drive the per-product disclaimer block render)
- `safetyNotes?` (string — used by `SafetyNotice` component on product page)

## Quality bar
- Every product description compliance-reviewed (Hack 03 sign-off cited in `notes`)
- No price in floats — only integer cents
- Tags consistent across products (normalize: lowercase, hyphen-separated)
- Featured count between 8 and 12 (homepage budget)
- Kits use real product IDs (not placeholder strings)

## Things to avoid
- Lifting product copy directly from manufacturer marketing without compliance review
- Adding products without a corresponding supplier in `/data/suppliers/` (orphaned products)
- Hardcoding image URLs to external sources we don't control (use `PlaceholderImage` with `label` + `accent` until art is ready)
- Letting kit prices be cheaper than the sum of components without intentional bundle-discount note

## Final deliverables
1. Seed products TypeScript file ready to replace `lib/products.ts`
2. Same data as JSON for backups + Dmack.ai skill ingestion
3. Product schema docs (so operators can add products solo)
4. 5 starter kits as structured records
5. Readiness report: total products, per-category counts, MVP-ready vs Phase-2, compliance sign-off status
