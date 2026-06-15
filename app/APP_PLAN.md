# App Plan: BIO CMC Target Agent

## Goal

Build a working Streamlit-based personal agent app for ingesting, scoring, translating, and tracking BIO CMC target research.

## MVP scope

- ingest by manual paste or file upload
- ingest by company name lookup using an AI model call
- scoring engine based on `01_schema/scoring_schema.md`
- dashboard of targets with score, band, and status
- editable record details and status pipeline
- translation helper that returns plain-English summaries and low-confidence fields
- local persistence in SQLite (`app/data.db`)
- CSV export for ClickUp import

## App structure

- `streamlit_app.py` - main UI and page flow
- `db.py` - SQLite persistence and record management
- `schema.py` - database schema and initialization
- `model.py` - Claude API integration / AI model helpers
- `prompts.py` - prompt templates and schema pointers
- `utils.py` - JSON, file parsing, and record helpers
- `requirements.txt` - Python dependencies

## Data model

One record contains company-level fields plus a JSON contact bundle:

- company
- parent_franchise
- arm_name
- modality
- arm_status
- signals_hit
- F1, F2, F3, F4
- fit_score
- fit_band
- engagement_type
- access_warmth
- bio_partnering_attending
- paper_trail_hook
- source_links
- contacts_json
- translation_summary
- low_confidence_fields
- status
- raw_note

The schema follows `01_schema/scoring_schema.md` as the source of truth.

## How to use it

1. install dependencies: `cd app && pip install -r requirements.txt`
2. set `CLAUDE_API_KEY` and `CLAUDE_API_URL` if you want model-powered research
3. run `streamlit run streamlit_app.py`
4. use the dashboard to add targets, upload notes, score records, and export CSV

## Notes

- The app is intentionally single-user and local.
- The model integration is optional; manual draft records are supported.
- `app/data.db` is the local store and survives restarts.
