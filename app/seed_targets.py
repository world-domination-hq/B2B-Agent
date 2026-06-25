"""
Run once to seed the SQLite database from 00_Targets/target_list.csv.
Safe to re-run: skips companies that already exist by name.

Usage:
    cd app && python seed_targets.py
"""
import csv
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
REPO_DIR = APP_DIR.parent
sys.path.append(str(APP_DIR))

from schema import init_db, get_connection

CSV_PATH = REPO_DIR / "00_Targets" / "target_list.csv"

GROUP_TO_ENGAGEMENT = {
    "service_provider": "partner",
    "standalone_rna": "consulting",
    "franchise_arm": "relationship",
    "channel": "channel",
}

PRIORITY_TO_ARM_STATUS = {
    "1": "active",
    "2": "forming",
    "3": "dormant",
    "4": "dormant",
}


def existing_companies(conn):
    rows = conn.execute("SELECT company FROM targets").fetchall()
    return {r["company"].lower() for r in rows}


def seed():
    init_db()
    with get_connection() as conn:
        existing = existing_companies(conn)
        added = 0
        skipped = 0

        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                company = row.get("company", "").strip()
                if not company or company.lower() in existing:
                    skipped += 1
                    continue

                group = row.get("group", "").strip()
                priority = row.get("priority", "3").strip()

                record = {
                    "company": company,
                    "parent_franchise": row.get("parent_franchise", "").strip() or None,
                    "modality": row.get("modality", "").strip() or None,
                    "arm_status": PRIORITY_TO_ARM_STATUS.get(priority, "dormant"),
                    "engagement_type": GROUP_TO_ENGAGEMENT.get(group, "partner"),
                    "access_warmth": "cold",
                    "paper_trail_hook": row.get("catch_at", "").strip() or None,
                    "status": "to-research",
                    "raw_note": f"Source: target_list.csv | group={group} | evidence={row.get('evidence','').strip()}",
                }

                cols = ", ".join(record.keys())
                placeholders = ", ".join(["?" for _ in record])
                conn.execute(
                    f"INSERT INTO targets ({cols}) VALUES ({placeholders})",
                    list(record.values()),
                )
                existing.add(company.lower())
                added += 1

        conn.commit()
        print(f"Seed complete: {added} added, {skipped} skipped (already existed or blank).")


if __name__ == "__main__":
    seed()
