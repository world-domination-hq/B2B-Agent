import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    parent_franchise TEXT,
    arm_name TEXT,
    modality TEXT,
    arm_status TEXT,
    signals_hit TEXT,
    F1 INTEGER,
    F2 INTEGER,
    F3 INTEGER,
    F4 INTEGER,
    fit_score REAL,
    fit_band TEXT,
    engagement_type TEXT,
    access_warmth TEXT,
    bio_partnering_attending TEXT,
    paper_trail_hook TEXT,
    source_links TEXT,
    contacts_json TEXT,
    translation_summary TEXT,
    low_confidence_fields TEXT,
    status TEXT,
    raw_note TEXT,
    created_at TEXT,
    updated_at TEXT
);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
