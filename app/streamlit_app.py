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
from utils import parse_upload, safe_json_load, score_record
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
                with st.sidebar:
                    with st.spinner("Researching…"):
                        try:
                            prompt = f"{SCHEMA_PROMPT}\n\nCompany to research: {company}"
                            result = call_claude(prompt, max_tokens=2000)
                            data = safe_json_load(result)
                            if not data:
                                st.sidebar.error("Model returned unparseable JSON")
                                return
                            data = score_record(data)
                            data["company"] = company
                            data["status"] = "to-research"
                            save_target(data)
                            st.sidebar.success(f"Added {company} — {data.get('fit_band','?')} ({data.get('fit_score','?')})")
                        except Exception as e:
                            st.sidebar.error(f"Research failed: {e}")


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

    st.header(f"Edit — {target['company']}")

    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("Company", value=target.get("company", ""))
        modality = st.text_input("Modality", value=target.get("modality", "") or "")
        signals_hit = st.text_input("Signals hit (comma-separated, e.g. S1,S2,S4)", value=target.get("signals_hit", "") or "")
        engagement_type = st.selectbox(
            "Engagement type", ["consulting", "relationship", "channel", "partner"],
            index=["consulting", "relationship", "channel", "partner"].index(target.get("engagement_type") or "consulting"),
        )
        access_warmth = st.selectbox(
            "Access warmth", ["cold", "warm_arcturus", "warm_network"],
            index=["cold", "warm_arcturus", "warm_network"].index(target.get("access_warmth") or "cold"),
        )
        status = st.selectbox(
            "Track status", ["to-research", "enriched", "contacted", "meeting", "dead"],
            index=["to-research", "enriched", "contacted", "meeting", "dead"].index(target.get("status") or "to-research"),
        )

    with col2:
        st.markdown("**Fit factors** (0 = low, 2 = high)")
        F1 = st.slider("F1 — Arm stage / spend window", 0, 2, int(target.get("F1") or 0))
        F2 = st.slider("F2 — Internal CMC maturity gap", 0, 2, int(target.get("F2") or 0))
        F3 = st.slider("F3 — Modality match", 0, 2, int(target.get("F3") or 0))
        F4 = st.slider("F4 — Leverage of your edge", 0, 2, int(target.get("F4") or 0))

        scored = score_record({"signals_hit": signals_hit, "F1": F1, "F2": F2, "F3": F3, "F4": F4})
        st.metric("Fit score", scored["fit_score"])
        st.metric("Fit band", scored["fit_band"])
        st.metric("Arm status", scored["arm_status"])

    paper_trail_hook = st.text_area("Paper trail hook", value=target.get("paper_trail_hook", "") or "")
    source_links = st.text_input("Source links", value=target.get("source_links", "") or "")
    translation_summary = st.text_area("Translation summary", value=target.get("translation_summary", "") or "")
    low_confidence_fields = st.text_input("Low confidence fields", value=target.get("low_confidence_fields", "") or "")

    save_col, translate_col, close_col = st.columns([1, 1, 2])

    with save_col:
        if st.button("Save"):
            update_target(target_id, {
                "company": company,
                "modality": modality,
                "signals_hit": signals_hit,
                "F1": F1, "F2": F2, "F3": F3, "F4": F4,
                "fit_score": scored["fit_score"],
                "fit_band": scored["fit_band"],
                "arm_status": scored["arm_status"],
                "engagement_type": engagement_type,
                "access_warmth": access_warmth,
                "status": status,
                "paper_trail_hook": paper_trail_hook,
                "source_links": source_links,
                "translation_summary": translation_summary,
                "low_confidence_fields": low_confidence_fields,
            })
            st.success("Saved")
            del st.session_state["selected_target"]
            st.rerun()

    with translate_col:
        if st.button("Translate (AI)"):
            try:
                prompt = f"{TRANSLATE_PROMPT}\n\nRecord:\n{json.dumps(dict(target), indent=2)}"
                result = call_claude(prompt)
                parsed = safe_json_load(result)
                if parsed:
                    update_target(target_id, {
                        "translation_summary": parsed.get("translation_summary", ""),
                        "low_confidence_fields": parsed.get("low_confidence_fields", ""),
                    })
                    st.success("Translation saved — reload to see it.")
                else:
                    st.warning("Model returned unparseable output.")
            except Exception as e:
                st.error(f"Model call failed: {e}")

    with close_col:
        if st.button("Close editor"):
            del st.session_state["selected_target"]
            st.rerun()


def main():
    init()
    if "selected_target" not in st.session_state:
        st.session_state.selected_target = None

    sidebar_add_target()
    render_dashboard()
    render_target_editor()


if __name__ == "__main__":
    main()
