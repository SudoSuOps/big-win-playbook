# Hack 03 — Compliance & Claims (THE GATING HACK)

## Mission
Every other hack's output passes through Compliance review before it ships. The DSS brand stands on **trust, not conversion**. This hack defines the language guardrails, surfaces risky claims, and writes the disclaimer copy that lives on the site.

## Scope
- Product copy (descriptions, taglines, category copy)
- Marketing language (homepage, founder page, guides)
- AI companion outputs (dmack.ai — every refusal pattern + escalation rule)
- Supplement labeling (FDA disclaimer requirements)
- Wound-care language (must not imply treatment of diabetic ulcers / infections / gangrene)
- Cross-state retail / brokerage considerations (out of scope if not commerce-relevant)

## Risky / banned claims (must never appear on the site)
- "Cures diabetes" / "reverses diabetes"
- "Heals diabetic ulcers" / "treats neuropathy" / "prevents amputation"
- "Stops infection" / "kills bacteria" (unless it's a true antiseptic with regulatory standing — and even then careful)
- "Replaces medical care" / "doctor not needed"
- "Guaranteed healing" / any guarantee of medical outcome
- "FDA approved" — unless verifiably true with the specific product (cleared ≠ approved; supplements are neither)
- Any disease-treatment claim for a supplement / wellness product

## Safer language (use these patterns)
- "Supports general wellness as part of a balanced lifestyle"
- "Helps you stay organized and prepared"
- "Useful for daily supply preparedness"
- "Designed for daily foot-care routines"
- "Can be part of a prevention-minded routine"
- "Ask your healthcare provider whether this is right for you"
- For supplements always include FDA verbatim: *"These statements have not been evaluated by the FDA. This product is not intended to diagnose, treat, cure, or prevent any disease."*

## Output files
- `/data/compliance/claims_risk_matrix.csv` — every product/page → claims used → risk band
- `/data/compliance/banned_claims.json` — machine-readable banned-phrase list (for `Claims Checker` skill)
- `/data/compliance/safer_language_examples.json` — substitution table
- `/docs/compliance/medical_disclaimer.md` — site-wide medical disclaimer
- `/docs/compliance/supplement_disclaimer.md` — supplement / wellness disclaimer
- `/docs/compliance/wound_care_safety_language.md` — wound-care category copy rules
- `/reports/compliance_review.md` — review of current site copy + flags found

### CSV fields
`asset_type` (product / page / ai_output / email_template), `asset_id_or_path`, `claim_excerpt`, `risk_band` (low / medium / high), `recommendation` (approve / soften / strike / escalate), `replacement_suggested`, `reviewer_notes`

## Quality bar
- Every site surface gets reviewed at least once
- Every "high" risk item has a specific replacement suggested — not just "remove"
- FDA/FTC alignment: a casual reader of FDA and FTC guidance would recognize the language as compliant
- Wound-care section gets EXTRA scrutiny — Donovan's lived experience here means visitors may project medical authority onto the brand

## Things to avoid
- Over-correction (becoming so generic the brand is bland)
- Approving language because "everyone else uses it" — others may also be non-compliant
- Skipping AI companion outputs (those are higher-stakes, not lower)
- Approving without reading the actual page in context

## Final deliverables
1. Claims risk matrix CSV — every asset reviewed
2. Banned + safer JSON files — ready for the Claims Checker skill (Hack 06) to consume
3. Three disclaimer documents (medical, supplement, wound-care) — sized for footer / inline use
4. Compliance review report — site-wide findings, recommendations, sign-off list
5. **Sign-off note**: a list of every asset that the operator MUST review personally before site goes live (high-risk ones)
