# BIO CMC Target Agent

A work-in-progress single-user MVP for BIO CMC target research, scoring, and tracking. This repo now contains both the active implementation and the BMAD planning workflow.

## Current status

This project is under active build. The current repo includes:

- a Streamlit-based app scaffold in `app/`
- local persistence, scoring logic, and model integration support
- a public landing page in `index.html`, `assets/`, and `features/`
- the full BMAD planning toolchain for product, architecture, and implementation
- UX/design draft artifacts in `design-artifacts/`

## What this repo is for

Build and validate a local BIO CMC Target Agent that:

- ingests target research manually or with AI-assisted lookup
- applies a fixed CMC scoring schema
- displays ranked targets in a dashboard
- supports editable records and status tracking
- provides a plain-English summary and review flags
- exports results to CSV for ClickUp or manual workflow

## Important folders

- `app/` — current MVP implementation
- `00_Targets/` — seed target list and working target data
- `01_Schema/` — scoring schema and source-of-truth fields
- `02_Prompts/` — BMAD prompt workflow and agent templates
- `03_Inputs/` — raw example input notes
- `04_outputs/` — example completed briefs
- `05_Build Plan/` — build plan and planning notes
- `PROJECT_BRIEF.md` — BMAD planning input
- `prd.md` — generated product requirements
- `BMAD_PROMPTS.md` — exact BMAD prompts for the project
- `_bmad/`, `.agents/`, `.github/` — BMAD tooling and agent configuration
- `design-artifacts/` — UX/draft design reference material
- `index.html`, `assets/`, `features/` — public landing page

## Design artifacts

Keep `design-artifacts/` as active UX reference while design is still in draft. It is useful for later decisions and should remain alongside the implementation.

## How to run the app

1. Install Python dependencies:
   - `cd app && pip install -r requirements.txt`
2. Set Claude environment variables if using AI:
   - `CLAUDE_API_KEY`
   - `CLAUDE_API_URL`
3. Start the app:
   - `streamlit run app/streamlit_app.py`

## BMAD workflow

This repo preserves the full BMAD planning and validation workflow.

Use the following order:

1. `PROJECT_BRIEF.md` is the project planning input.
2. Run `bmad-agent-pm` with the brief to generate or refine `prd.md`.
3. Run `bmad-agent-architect` to generate `architecture.md`.
4. Use `bmad-agent-builder` or `bmad-agent-dev` to implement stories.

## Notes

- The implementation is intentionally single-user and local.
- The scoring schema in `01_Schema/scoring_schema.md` is the source of truth.
- This project is not building LinkedIn scraping or automated private-data collection.
- `design-artifacts/` is draft UX work and should be kept as a reference, not as the main app.

## Useful next steps

- Continue building the Streamlit MVP in `app/`.
- Use `PROJECT_BRIEF.md` and `prd.md` as the active planning docs.
- Keep `design-artifacts/` for UX reference while your design is not finalized.
- Keep the BMAD tooling intact for planning, validation, and shipping.
