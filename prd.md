# Product Requirements Document (PRD)

## Product

A single-user local BIO CMC Target Agent app for a CMC consultant. The MVP ingests company research by manual upload or AI-assisted lookup, applies a fixed CMC scoring schema, shows ranked targets in a dashboard, supports edit and status tracking, and exports selected records for ClickUp.

## Objective

Deliver a lightweight, reproducible tool that helps a single user turn research into scored, reviewable BIO/CMC target records with a plain-English review layer and local persistence.

## Recommended stack

- Streamlit for the UI
- Claude API for research enrichment and translation helpers
- SQLite for local persistence

This is the recommended MVP stack because it minimizes infrastructure, keeps the app local, and matches the repo's existing `app/` architecture.

## MVP scope

Included:
- Manual ingestion by pasted text or uploaded `.md`, `.txt`, or `.csv` files
- AI-assisted ingest by company name lookup
- Scoring engine using `01_Schema/scoring_schema.md`
- Dashboard list of targets with fit score, fit band, and status
- Editable record details and status pipeline
- Translation helper with plain-English summary and low-confidence field flags
- Local persistence in SQLite, surviving restarts
- Export to CSV for ClickUp import

Excluded:
- User auth or multi-user support
- LinkedIn scraping or automated role discovery
- Live web crawling at scale
- Fancy analytics or charts
- ClickUp sync beyond CSV export

## Hard constraints

- Do not automate LinkedIn scraping or use any LinkedIn crawler.
- Store only public professional signals: publications, talks, public roles, public posts.
- Compute the final score in code using the fixed schema. Do not let the model guess the final `fit_score`, `fit_band`, or weight math.
- Use the BIO Partnering directory or manual input for attendance, not guessed social media activity.

## Domain model

Each target record includes company-level fields from the scoring schema:
- `company`
- `parent_franchise`
- `arm_name`
- `modality`
- `arm_status`
- `signals_hit`
- `F1`, `F2`, `F3`, `F4`
- `fit_score`
- `fit_band`
- `engagement_type`
- `access_warmth`
- `bio_partnering_attending`
- `paper_trail_hook`
- `source_links`

Each contact row includes:
- `contact_name`
- `role_bucket`
- `title`
- `source`
- `professional_signal`
- `my_angle`
- `status`

The scoring schema is the source of truth for arm detection, score math, bands, and tag definitions.

## Epics and stories

### E1: Ingest

S1.1 Paste or upload a note and save it as a draft record.
- Acceptance: user can paste raw notes or upload a `.md`, `.txt`, or `.csv` file and create a target draft.
- Data saved: raw source text, parsed company name, initial fields, status `to-research`.

S1.2 Enter a company name and have the app gather and structure facts.
- Acceptance: user submits a company name and the app calls Claude API to return structured company facts and candidate field values.
- Data saved: suggested company fields, signals, raw model output, and target draft.

### E2: Scoring engine

S2.1 Run arm-detection signals and set `arm_status`.
- Acceptance: the app evaluates the schema's S1–S7 signals and sets `arm_status` to `dormant`, `forming`, or `active`.
- `signals_hit` must list the positive signal codes.

S2.2 Rate `F1` to `F4` and compute `fit_score` and `fit_band` by the schema formula.
- Acceptance: the app computes ratings 0/1/2 for each F input, then calculates `fit_score` using:
  `fit_score = (F1*15) + (F2*15) + (F3*12.5) + (F4*7.5)`.
- `fit_band` must be `hot`, `warm`, or `park` based on the computed score.

S2.3 Set `engagement_type` and `access_warmth` tags.
- Acceptance: the app stores `engagement_type` as one of `consulting`, `relationship`, `channel`, `partner` and `access_warmth` as `cold`, `warm_arcturus`, or `warm_network`.

### E3: Dashboard

S3.1 List all records, sortable by `fit_score`.
- Acceptance: the dashboard displays saved targets in a table or cards and allows sorting by `fit_score`.
- It must show key company fields, score, band, and status.

S3.2 Open one record and edit any field.
- Acceptance: user can select a target and update company fields, contact rows, and review notes.
- Edited data must persist.

### E4: Progress tracking

S4.1 Change a record's status through the pipeline and persist it.
- Acceptance: user can move a record's status among `to-research`, `enriched`, `contacted`, `meeting`, and `dead`.
- Status changes are saved in the database.

### E5: Translation and review

S5.1 Generate a plain-English summary per record.
- Acceptance: the app calls Claude API to create a concise summary of the record's opportunity.
- The summary is visible on the record detail page.

S5.2 List low-confidence fields for me to confirm.
- Acceptance: the app lists fields the model flagged as uncertain or guessed.
- The user can review and correct those fields manually.

### E6: Export

S6.1 Export selected records as a CSV matching the ClickUp field map.
- Acceptance: user can export one or more records to CSV with company and contact fields mapped to the ClickUp task schema.
- Output must include the fields needed for ClickUp import.

## Day-by-day plan

### Day 1

- Install BMAD and confirm repository setup.
- Create `prd.md` and generate `architecture.md`.
- Build E1 ingest flows: manual paste/upload and company lookup.
- Build E2 scoring engine: arm detection, F1–F4 ratings, `fit_score`, `fit_band`, and tag fields.
- Validate local persistence in SQLite.

### Day 2

- Build E3 dashboard: target listing, sorting, and record editing.
- Build E4 progress tracking and status persistence.
- Add the translation helper UI placeholder and store summaries.

### Day 3

- Complete E5 translation and low-confidence review flow.
- Build E6 CSV export for ClickUp.
- Load seeded targets from `00_Targets/target_list.csv` and verify the MVP workflow.
- Polish UX, fix bugs, and ensure the app runs locally with Streamlit.

## Success criteria

- A user can ingest a target by paste/upload or by name lookup.
- The app computes scores using the fixed schema and shows a sortable target dashboard.
- The user can edit records, change status, and persist changes across restarts.
- The app provides a plain-English summary and highlights fields flagged for review.
- The user can export records to CSV for ClickUp import.

---

`prd.md` is scoped to the MVP only and follows the repo's existing recommended Streamlit + Claude API + SQLite architecture.
