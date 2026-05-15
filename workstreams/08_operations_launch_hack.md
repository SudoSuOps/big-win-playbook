# Hack 08 — Operations & Launch

## Mission
Turn the firm into an operating business. Synthesize Hacks 1–7 outputs into SOPs and a launch checklist that an operator can execute solo. Owns the "go-live" gate.

## Scope
- Vendor onboarding SOP (how to evaluate + approve + integrate a new supplier)
- Product quality SOP (sample-order → inspect → approve / reject)
- Order fulfillment SOP (per chosen Hack 04 fulfillment shape)
- Customer feedback review process
- Product removal process (compliance flag, supplier failure, quality issue)
- Launch checklist (the actual day-of-launch runbook)
- Post-launch ongoing operations

## Output files
- `/docs/operations/vendor_onboarding_sop.md`
- `/docs/operations/product_quality_sop.md`
- `/docs/operations/order_fulfillment_sop.md`
- `/docs/launch/launch_checklist.md`
- `/reports/launch_readiness_report.md`

## Vendor onboarding SOP — required sections
1. Initial outreach + criteria for response evaluation
2. Sample order — what to test, what to measure
3. Account approval gates (resale cert, terms negotiated, MAP policy review)
4. Integration steps (catalog ingestion, image acquisition, compliance review of copy)
5. First order pilot (small inventory or first 10 dropship orders)
6. 30-day review checkpoint

## Product quality SOP — required sections
1. Sample testing protocol (per category — socks tested differently than dressings)
2. Inspection criteria (packaging integrity, expiration dates, labeling)
3. Pass / soft-pass / fail rubric
4. What triggers a recall / pull from catalog
5. Documentation requirements (photos, notes, supplier communication archive)

## Order fulfillment SOP — required sections
1. Per chosen fulfillment shape (likely hybrid per Hack 04 recommendation)
2. Daily order ingestion + processing flow
3. Inventory monitoring + reorder triggers
4. Shipping label + tracking + customer communication
5. Returns workflow (eligible vs ineligible, processing time, refund cadence)
6. Customer service escalation triggers

## Launch checklist — required sections
1. Pre-launch (T-30 days): finalize products, suppliers signed, compliance sign-off
2. Pre-launch (T-7 days): site QA, payment flow tested end-to-end, legal pages live, dmack.ai responses sanity-checked
3. Pre-launch (T-1 day): smoke test, founder review, monitoring set up
4. Launch day: open commerce, monitor for issues, soft-promote
5. Week 1: customer feedback, fulfillment SLA tracking, refund/return review

## Launch readiness report — required sections
- What's ready (per hack — done, in progress, blocked)
- Compliance sign-off status (Hack 03's high-risk list cleared?)
- Top 5 risks for launch with mitigations
- Recommended launch shape: soft launch (close friends), public soft launch (no marketing), full launch
- Day-1 metrics to track

## Quality bar
- Every SOP is **executable solo by a non-engineer operator** — instructions, not principles
- Every step has a clear "done" criterion
- Every checklist item has a single owner role (operator / engineer / compliance reviewer)
- The launch checklist fits on one screen at any given phase (no 200-item monsters)

## Things to avoid
- Theoretical SOPs that don't survive contact with reality (test against an actual practice order)
- Skipping the "what to do if X fails" branches
- Burying compliance gates (they should be the loudest items on the checklist)

## Final deliverables
1. 3 SOPs (vendor onboarding, product quality, order fulfillment) — executable solo
2. Launch checklist with phase gates
3. Launch readiness report with risk matrix
4. Sign-off list: every item the operator must personally green-light before launch (compliance review, payment flow, dmack.ai sanity check)
