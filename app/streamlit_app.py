import json
import sys
import streamlit as st
from datetime import datetime
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
sys.path.append(str(APP_DIR))

from db import get_all_targets, get_target, save_target, update_target
from prompts import SCHEMA_PROMPT, TRANSLATE_PROMPT
from schema import init_db
from utils import parse_upload, safe_json_load
from model import call_claude

DATA_PATH = Path(__file__).resolve().parent


def init():
    init_db()
    st.set_page_config(page_title="BIO CMC Target Agent", layout="wide")
    st.title("BIO CMC Target Agent")
    st.markdown("A simple local app for target ingestion, scoring, translation, and tracking.")


def sidebar_add_target():
    st.sidebar.header("Add target")
    source = st.sidebar.radio("Ingest type", ["Manual note", "Upload file", "Company lookup"])

    if source == "Manual note":
        raw_note = st.sidebar.text_area("Paste research note", height=200)
        company = st.sidebar.text_input("Company name")
        if st.sidebar.button("Add draft record"):
            if not company:
                st.sidebar.error("Company name is required")
            else:
                save_target({
                    "company": company,
                    "raw_note": raw_note,
                    "status": "to-research",
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                })
                st.sidebar.success("Draft record added")

    elif source == "Upload file":
        upload = st.sidebar.file_uploader("Upload .md/.txt/.csv", type=["md", "txt", "csv"])
        if upload is not None:
            raw_note = parse_upload(upload.read(), upload.name)
            company = st.sidebar.text_input("Company name")
            if st.sidebar.button("Add uploaded target"):
                if not company:
                    st.sidebar.error("Company name is required")
                else:
                    save_target({
                        "company": company,
                        "raw_note": raw_note,
                        "status": "to-research",
                        "created_at": datetime.utcnow().isoformat(),
                        "updated_at": datetime.utcnow().isoformat(),
                    })
                    st.sidebar.success("Uploaded record added")

    else:
        company = st.sidebar.text_input("Company name")
        if st.sidebar.button("Research company"):
            if not company:
                st.sidebar.error("Company name is required")
            else:
                prompt = f"Research this company for BIO CMC target qualification: {company}. Use the schema in 01_schema/scoring_schema.md and return JSON."
                result = call_claude(prompt)
                try:
                    data = json.loads(result)
                except Exception:
                    st.sidebar.error("Model output could not be parsed as JSON")
                    return
                data["company"] = company
                data["status"] = "to-research"
                data["created_at"] = datetime.utcnow().isoformat()
                data["updated_at"] = datetime.utcnow().isoformat()
                save_target(data)
                st.sidebar.success("Company record added")


def render_dashboard():
    st.header("Dashboard")
    query = st.text_input("Search targets")
    targets = get_all_targets(search_text=query)
    if not targets:
        st.info("No targets found. Add one from the sidebar.")
        return

    for target in targets:
        with st.expander(f"{target['company']} — {target.get('fit_band', 'unknown')} ({target.get('status', 'unset')})"):
            st.markdown(f"**Score:** {target.get('fit_score', 'n/a')}  |  **Status:** {target.get('status', 'n/a')}")
            cols = st.columns([2, 1])
            with cols[0]:
                st.write(target.get('paper_trail_hook', ''))
                st.write(target.get('source_links', ''))
            with cols[1]:
                if st.button(f"Edit {target['id']}", key=f"edit-{target['id']}"):
                    st.session_state.selected_target = target['id']


def render_target_editor():
    target_id = st.session_state.get("selected_target")
    if not target_id:
        return

    target = get_target(target_id)
    if not target:
        st.error("Target not found")
        return

    st.header(f"Edit {target['company']}")
    company = st.text_input("Company", value=target['company'])
    arm_status = st.selectbox("Arm status", ["dormant", "forming", "active"], index=["dormant", "forming", "active"].index(target.get('arm_status', 'dormant')))
    fit_band = st.selectbox("Fit band", ["hot", "warm", "park"], index=["hot", "warm", "park"].index(target.get('fit_band', 'park')))
    status = st.selectbox("Track status", ["to-research", "enriched", "contacted", "meeting", "dead"], index=["to-research", "enriched", "contacted", "meeting", "dead"].index(target.get('status', 'to-research')))
    translation_summary = st.text_area("Translation summary", value=target.get('translation_summary', ''))
    low_confidence_fields = st.text_input("Low confidence fields", value=target.get('low_confidence_fields', ''))

    if st.button("Save changes"):
        update_target(target_id, {
            "company": company,
            "arm_status": arm_status,
            "fit_band": fit_band,
            "status": status,
            "translation_summary": translation_summary,
            "low_confidence_fields": low_confidence_fields,
            "updated_at": datetime.utcnow().isoformat(),
        })
        st.success("Target updated")
        del st.session_state["selected_target"]


def main():
    init()
    if "selected_target" not in st.session_state:
        st.session_state.selected_target = None

    sidebar_add_target()
    render_dashboard()
    render_target_editor()


if __name__ == "__main__":
    main()
