# Project Brief: BIO CMC Target Agent

Hand this file to Copilot. It is the input to BMAD's planning phase. Run the PM agent against it to generate `prd.md`, then the Architect agent for `architecture.md`, then build story by story.

## 1. What we are building, in one paragraph

A personal lead-research app for a CMC consultant. It ingests research two ways (the app fetches it, or I upload a hot tip), runs each company through a fixed qualification and scoring schema, shows me the results on a simple dashboard where I can edit and track status, and includes a translation helper that rewrites anything technical into plain English and flags fields it is unsure about for me to review. It is a single-user local app. I run it myself.

## 2. The user and the job

- User: me, one person. A CMC operator building a consulting and content business.
- Job: walk into a conference with a ranked, sourced, opener-ready list of the right companies and people, without doing all the research by hand or trusting a black box.

## 3. User journey (end to end, my point of view)

1. I open the app to a dashboard listing my target companies and their scores.
2. I add a target two ways: (a) type or paste a company name and ask the app to research it, or (b) upload a note or file when I already have a hot tip.
3. The app runs the company through the schema on the backend: detect the RNA/biologics arm, find contacts by role, score fit, tag access and engagement, check attendance.
4. The result appears on the dashboard as a card or row: fit score, band, arm status, contacts, the paper-trail hook.
5. I review it. The translation helper has added a plain-English summary and flagged any field it guessed or could not verify, so I know exactly what to check.
6. I edit anything wrong and confirm. I move the card through a status pipeline: to-research, enriched, contacted, meeting, dead.
7. I sort by fit score and export or copy the openers for the ones I will meet.

## 4. MVP scope (what to build in the next 2 to 3 days)

In scope:

- Ingest by manual upload (paste text or upload a .md/.txt/.csv).
- Ingest by app-run research (call an AI model to gather and structure facts).
- Scoring engine that applies the schema in `01_schema/scoring_schema.md`.
- Dashboard: table or card view of all targets with score, band, status.
- Edit a record and change its status.
- Translation helper: plain-English summary plus a list of low-confidence fields to review.
- Local persistence (a JSON file or SQLite). Survives restarts.

Out of scope for now (do later, do not let Copilot gold-plate):

- User accounts, auth, multi-user.
- Live LinkedIn integration of any kind (see constraints).
- Automated web crawling at scale.
- Fancy charts. A sortable table is enough.
- ClickUp sync. Export a CSV for now; wire ClickUp later.

## 5. Recommended architecture and stack

Pick the simplest thing that runs locally and that Copilot can scaffold fast.

**Recommended (fastest for a non-developer): Streamlit + Claude API + SQLite.**

- Streamlit gives you file upload, forms, tables, and edit widgets in one Python file. Least code to a working dashboard.
- The "backend" is Python functions that call the Claude API with the schema prompts in `02_prompts/`.
- SQLite (one file) or a JSON file stores records. No database server to run.

**Alternative (if you want a real web app): Next.js + SQLite via Prisma, deploy on Vercel.** More code, more concepts, slower for a first build. Only choose this if a hosted URL matters now.

Component shape either way:

- `ingest` module: takes pasted text, an uploaded file, or a company name. For a name, it calls the model to gather facts.
- `score` module: pure logic that turns facts into the schema fields and the fit score. Keep the math exactly as written in the schema so results are reproducible.
- `translate` module: one model call that returns a plain-English summary plus a list of fields tagged low-confidence.
- `store` module: read and write records.
- `ui`: the dashboard, the add-target form, the edit view, the status pipeline.

## 6. Domain model (source of truth)

Do not invent fields. The record shape and the scoring math live in `01_schema/scoring_schema.md`. A record is one company plus its contacts, with: arm_status, signals_hit, F1 to F4 ratings, fit_score, fit_band, engagement_type, access_warmth, bio_partnering_attending, paper_trail_hook, and per-contact rows. The starter target list is `00_targets/target_list.csv`. Example finished records are in `03_inputs/` and `04_outputs/`.

## 7. Hard constraints (tell Copilot these are non-negotiable)

- No automated LinkedIn scraping. It violates their terms and risks the account. Attendance comes from the BIO Partnering directory or manual entry. Role lookup is done by hand in Sales Navigator, not by the app.
- Store professional signal only (publications, talks, public roles, public posts). No private personal data. This keeps the build clear of privacy-law exposure.
- The scoring math is fixed by the schema. The model may gather facts and rate inputs, but the final number is computed by code, not guessed, so it is reproducible.

## 8. Epics and stories (BMAD will shard these)

- **E1 Ingest**

  S1.1 Paste or upload a note and save it as a draft record.

  S1.2 Enter a company name and have the app gather and structure facts.

- **E2 Scoring engine**

  S2.1 Run arm-detection signals and set arm_status.

  S2.2 Rate F1 to F4 and compute fit_score and band by the schema formula.

  S2.3 Set engagement_type and access_warmth tags.

- **E3 Dashboard**

  S3.1 List all records, sortable by fit_score.

  S3.2 Open one record and edit any field.

- **E4 Progress tracking**

  S4.1 Change a record's status through the pipeline and persist it.

- **E5 Translation and review**

  S5.1 Generate a plain-English summary per record.

  S5.2 List low-confidence fields for me to confirm.

- **E6 Export**

  S6.1 Export selected records as a CSV matching the ClickUp field map.

Build order: E1, then E2, then E3, then E4, then E5, then E6. Each is usable on its own, so if time runs out you still have something.

## 9. How to run this with BMAD and Copilot (the next 2 days)

1. In VS Code, open your repo. In a terminal: `npx bmad-method install`, and select GitHub Copilot as the IDE. This adds the BMAD agents and slash commands into `.github/` and a `_bmad-output/` folder.
2. Open Copilot Chat. Run the PM agent and point it at this brief to create the PRD: invoke the PM agent, then the create-prd workflow. Review the generated `prd.md`.
3. Run the Architect agent to produce `architecture.md`. Tell it the recommended stack in section 5.
4. Let the Scrum Master shard the PRD into story files.
5. Run the Dev agent one story at a time, starting at S1.1. Commit after each story passes.
6. Use the bmad-help skill whenever you are unsure what is next.

## 10. The 2 to 3 day plan, and the fallback

- Day 1: install BMAD, generate PRD and architecture, build E1 and E2 (ingest + scoring). At end of day you can score a company.
- Day 2: build E3 and E4 (dashboard + status). Now you can see and track everything.
- Day 3: build E5 and E6 (translation + export), load your six seeded targets, polish.
- Fallback: if the app is not done by conference time, the folder pipeline in this repo (the `02_prompts/` steps plus the `03_inputs/` notes I already filled) gives you the same result by hand. The app is the upgrade, not the only path.

## 11. Seed prompt to paste into the BMAD PM agent

```
I am building the app described in PROJECT_BRIEF.md in this repo. I am a non-developer using GitHub Copilot. Create a PRD for the MVP scope only (section 4). Respect the hard constraints in section 7 and the domain model in section 6, which lives in 01_schema/scoring_schema.md. Recommend the Streamlit + Claude API + SQLite stack unless you see a strong reason against it. Keep stories small enough that one passes per short session. Do not add features beyond the MVP scope.
```
