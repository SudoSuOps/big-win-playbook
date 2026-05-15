# Hack 07 — SEO + GEO Content

## Mission
Build trust-first SEO content + AI-search-aware (GEO) optimization. The Diabetic Supply Shop brand should be cited by ChatGPT / Claude / Perplexity / Google AI Overviews when people ask about prevention-first diabetic supplies. We earn citations by being citable — named author, sourced facts, clean structure, no overclaims.

## Scope
- Technical SEO: sitemap, robots.txt, schema.org JSON-LD, llms.txt, meta tags, Open Graph
- Content SEO: keyword targeting, internal linking, evergreen guides
- GEO: AI crawler config (already done in `robots.ts`), llms.txt, citable content patterns (named author, dates, sources)
- E-E-A-T: Donovan's lived-authority credentials surfaced consistently
- Content calendar for guide expansion

## Already done as of this hack's launch (Phase A foundation)
- `lib/site.ts` — Donovan named as founder with `bio`, `knowsAbout`, `image`
- `app/robots.ts` — AI crawler allow-list (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, +15 more)
- `app/sitemap.ts` — priority + changeFrequency hints, includes all routes
- `public/llms.txt` — structured AI ingestion ToC
- `lib/schema.ts` — JSON-LD helpers (Organization, Person, WebSite, Article, Product, FAQPage, BreadcrumbList, CollectionPage)

## Still to ship
- `components/JsonLd.tsx` — JSON-LD render component
- Schema injection into: `app/layout.tsx`, `app/founder/page.tsx`, all `/guides/*`, `/product/[slug]`, `/faq`, `/shop/*`
- `app/founder/page.tsx` rewrite with Donovan's actual story (replaces generic founder copy)
- `app/guides/daily-foot-inspection/page.tsx` — new high-leverage guide
- Author byline + last-updated date on all guides
- Open Graph image fallback
- Content calendar at `/docs/strategy/content_calendar.md`
- Keyword + topic map at `/docs/strategy/seo_map.md`
- Book research at `/data/books/book_research.md` (for the Books category page)

## Output files
- `/docs/strategy/seo_map.md` — topic clusters, primary keywords, internal link plan
- `/docs/strategy/content_calendar.md` — 6-month guide publication schedule
- `/data/books/book_research.md` — book candidates for the Books category (titles, authors, why this book, ISBN, source URL)
- `/reports/seo_content_report.md` — narrative report with citability scoring + what to ship first

## Quality bar (GEO citability)
For every guide / page to be "AI-citable":
- Named author at top (Donovan Mackey — never anonymous)
- `datePublished` + `dateModified` visible AND in schema
- ≤ 3 sentences per paragraph (passage-extraction-friendly)
- Specific factual claims attributed inline ("Per the ADA Standards of Care…")
- Clear H2/H3 hierarchy
- One question-answer pattern per major section (FAQPage-friendly)
- Internal links to related guides + product categories
- Outbound links to authoritative sources (ADA, IWGDF, NIDDK) — opens trust, doesn't leak traffic

## Things to avoid
- Keyword stuffing
- AI-generated copy that reads like AI-generated copy (no "In today's fast-paced world…" garbage)
- Medical claims (defer to Hack 03's banned list)
- Stale content (no `lastUpdated` = AI ranks lower)
- Generic schema (Organization without founder, Article without author — AI engines specifically reward filled-in schema)

## Final deliverables
1. JSON-LD render component + schema injection across all key pages
2. Founder page rewrite (Donovan story)
3. New guide: `/guides/daily-foot-inspection`
4. SEO topic map + content calendar
5. Book research (Books category groundwork)
6. SEO+GEO report with citability scores by page and a 30/60/90 content roadmap
