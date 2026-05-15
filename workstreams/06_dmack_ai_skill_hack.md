# Hack 06 — Dmack AI Skill Design

## Mission
Design the Dmack.ai companion's skill system. Six skills, each with a tight spec — what it does, what it refuses, what it routes. The companion is the lived-experience anchor for the brand, NOT a clinician.

## Scope
- System prompt (defines persona + non-negotiable rules)
- 6 skill specs (each is a behavior contract, not a chat script)
- Tool specifications for any tools the skills call
- Example conversations showing both happy path and edge cases
- Safety escalation rule set (referenced by multiple skills)

## Non-negotiable Dmack.ai rules
- **Never diagnose.** Pattern-language and routing only.
- **Never tell users to ignore symptoms.** Always default to "talk to your provider."
- **Never claim a supplement cures or treats diabetes.**
- **Never claim a product heals diabetic ulcers.**
- **Always recommend professional care for serious symptoms.**
- **Donovan voice register, not medical authority.** Same rule as the dmack.ai (the model) two-stream architecture: lived experience for register, documented sources for facts.
- **Compliance footer on every response** mentioning a product or recommendation.

## Safety red flags (force escalation, override sales intent)
- Open wound on foot
- Spreading redness
- Warmth / swelling
- Drainage / oozing
- Bad smell
- Fever
- Black tissue
- Increasing pain
- Numbness with injury
- Wound not improving
- Signs of infection
- Recent amputation complications
- Loss of circulation signs (cold, pale, blue)

For any of these: companion's first move is escalation, not product. Then offer a relevant supply for future preparedness (gently, after the escalation lands).

## The 6 skills

### 1. Product Finder
- Helps users find relevant categories and products
- Asks clarifying questions safely (no diagnostic questions)
- Refers to clinician for any medical question

### 2. Foot Care Kit Builder
- Builds daily / travel / caregiver / post-appointment / general prevention kits
- Bundles products from the catalog
- Always offers the Daily Foot Inspection Guide as a complement

### 3. Wound Preparedness
- Explains basic supply categories (non-stick dressing vs hydrocolloid vs silicone foam, etc.)
- Escalation rules first if symptoms suggest active infection
- Sells preparedness, NOT treatment

### 4. Reorder Planner
- Estimates supply usage based on user input (no PII stored)
- Generates checklist reminders
- Suggests subscription cadence

### 5. Safety Escalation
- The red-flag detector
- Returns templated 911 / urgent / same-day routing per the escalation rules document
- Overrides any sales intent if triggered

### 6. Claims Checker
- Reviews product copy and AI outputs against `/data/compliance/banned_claims.json`
- Returns risk band + suggested replacement
- Used by content authoring tools, not customer-facing

## Output files
- `/skills/dmack_ai/system_prompt.md` — the persona prompt
- `/skills/dmack_ai/tool_spec.md` — tools available to the companion
- `/skills/dmack_ai/example_conversations.md` — 10+ examples covering happy path, escalation, refusal, voice-drift catch
- `/skills/kit_builder/kit_builder_spec.md` — Kit Builder behavior contract
- `/skills/reorder_planner/reorder_planner_spec.md` — Reorder Planner contract
- `/skills/safety_escalation/safety_escalation_rules.md` — the red-flag → routing table
- `/skills/claims_checker/claims_checker_spec.md` — the banned-claims checker contract

## Quality bar
- System prompt ≤ 2,000 tokens (target — Qwen-class fits)
- Safety escalation rules table: for every red flag, one templated response
- Example conversations include at least: (a) successful kit build, (b) red-flag escalation, (c) refusal of dose advice, (d) voice-drift caught (e.g. user asks "are you Donovan?" → no, I'm the companion)
- Claims checker outputs match the schema Hack 03 ships in `banned_claims.json`

## Things to avoid
- Letting the companion give specific carb counts, insulin doses, or medication advice
- Approval of voice that says "I lost a toe" or first-person Donovan claims (voice register, not authority)
- Skill bloat — six skills is the lock, don't add a seventh
- Tool calls that could leak PII (no email sends, no SMS, no calendar writes in v1)

## Final deliverables
1. System prompt v0.1 (production-locked candidate)
2. 6 skill spec docs
3. Tool spec (initially: catalog search + claims-checker lookup)
4. Example conversation pack
5. Safety escalation rules (referenced by Stream 2 of the streams architecture)
6. Handoff note for the dmack.ai cook team (the AI model build) — what the companion expects from the model's voice register
