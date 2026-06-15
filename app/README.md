# BIO CMC Agent App

A simple local MVP built with Streamlit, Claude API calls, and SQLite.

## What it does

- ingest research by manual paste, file upload, or company lookup
- store target records locally in SQLite
- show a dashboard of targets and scores
- edit target fields and track status
- export records for ClickUp import

## Run it

1. Open a terminal in the `app/` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Claude API details if you want AI-powered company research:
   ```bash
   export CLAUDE_API_KEY="your-key"
   export CLAUDE_API_URL="https://api.anthropic.com/v1/complete"
   ```
4. Start the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Files

- `streamlit_app.py` — main UI and workflow
- `db.py` — SQLite persistence
- `schema.py` — database schema and initialization
- `model.py` — Claude API helper
- `prompts.py` — prompt templates for research and translation
- `utils.py` — file parsing and JSON helpers
- `requirements.txt` — Python dependencies
- `APP_PLAN.md` — app plan and architecture for this MVP

## Notes

- The app is single-user and local.
- You can use it without Claude if you paste notes manually.
- `app/data.db` is created automatically when the app runs.
