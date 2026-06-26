"""
Phase 2: One-time migration from SQLite + CSV + kol_tracker.md → Supabase.

Sources (in order):
  1. 00_Targets/target_list.csv  → companies table
  2. app/data.db (SQLite)        → companies table (fills in scored/enriched records)
  3. SQLite contacts_json blobs  → people table
  4. 00_Targets/kol_tracker.md   → people table (is_kol = true)

Safe to re-run: uses upsert on unique keys (company name, person name+org).

Usage:
    cd app

    # Dry run — prints what WOULD be upserted, touches nothing:
    python migrate_to_supabase.py --dry-run

    # Real run:
    python migrate_to_supabase.py
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

APP_DIR = Path(__file__).resolve().parent
REPO_DIR = APP_DIR.parent
sys.path.append(str(APP_DIR))

load_dotenv(REPO_DIR / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()

CSV_PATH   = REPO_DIR / "00_Targets" / "target_list.csv"
KOL_PATH   = REPO_DIR / "00_Targets" / "kol_tracker.md"
SQLITE_PATH = APP_DIR / "data.db"

# maps CSV group → Supabase category
GROUP_MAP = {
    "service_provider": "service_provider",
    "standalone_rna":   "standalone_rna",
    "franchise_arm":    "franchise_arm",
    "channel":          "channel",
}

# maps kol_tracker section headings → kol_track values
KOL_TRACK_MAP = {
    "CMC + Platform-Technology Regulation":          "cmc_reg",
    "Rare Disease / Patient-Centric Regulatory Pathways": "rare_disease",
    "Infectious Disease Preparedness + Biosecurity": "id_biosecurity",
    "China BD / Cross-Border Modality Landscape":    "china_bd",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _slug(name: str) -> str:
    """company name → markdown filename stem, e.g. 'Replicate Bioscience' → 'replicate-bioscience'"""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _notes_file(name: str, folder: str = "03_Inputs") -> str:
    return f"{folder}/{_slug(name)}.md"


def _existing_input(name: str) -> str | None:
    """Return relative path if a matching file already exists in 03_Inputs/."""
    slug = _slug(name)
    for p in (REPO_DIR / "03_Inputs").glob("*.md"):
        if slug in p.stem.lower() or p.stem.lower() in slug:
            return f"03_Inputs/{p.name}"
    return None


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_csv_companies() -> list[dict]:
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row.get("company", "").strip()
            if not name:
                continue
            existing = _existing_input(name)
            rows.append({
                "name":             name,
                "parent_franchise": row.get("parent_franchise", "").strip() or None,
                "modality":         row.get("modality", "").strip() or None,
                "category":         GROUP_MAP.get(row.get("group", "").strip(), "channel"),
                "engagement_type":  row.get("engagement", "").strip() or None,
                "evidence":         row.get("evidence", "").strip() or None,
                "priority":         int(row.get("priority", 3) or 3),
                "paper_trail_hook": row.get("catch_at", "").strip() or None,
                "status":           "to-research",
                "access_warmth":    "cold",
                "notes_file":       existing or _notes_file(name),
            })
    return rows


def load_sqlite_companies() -> list[dict]:
    """Pull enriched records from SQLite if data.db exists."""
    if not SQLITE_PATH.exists():
        print("  [skip] No app/data.db found — SQLite migration skipped.")
        return []

    import sqlite3
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM targets").fetchall()
    conn.close()

    out = []
    for r in rows:
        r = dict(r)
        name = r.get("company", "").strip()
        if not name:
            continue
        existing = _existing_input(name)
        out.append({
            "name":                  name,
            "parent_franchise":      r.get("parent_franchise"),
            "arm_name":              r.get("arm_name"),
            "modality":              r.get("modality"),
            "signals_hit":           r.get("signals_hit"),
            "arm_status":            r.get("arm_status"),
            "F1":                    r.get("F1"),
            "F2":                    r.get("F2"),
            "F3":                    r.get("F3"),
            "F4":                    r.get("F4"),
            "fit_score":             r.get("fit_score"),
            "fit_band":              r.get("fit_band"),
            "engagement_type":       r.get("engagement_type"),
            "access_warmth":         r.get("access_warmth"),
            "bio_partnering_attending": r.get("bio_partnering_attending"),
            "paper_trail_hook":      r.get("paper_trail_hook"),
            "source_links":          r.get("source_links"),
            "translation_summary":   r.get("translation_summary"),
            "low_confidence_fields": r.get("low_confidence_fields"),
            "raw_note":              r.get("raw_note"),
            "status":                r.get("status", "to-research"),
            "notes_file":            existing or _notes_file(name),
        })
    return out


def load_sqlite_contacts() -> list[dict]:
    """Extract contacts from the old contacts_json blobs."""
    if not SQLITE_PATH.exists():
        return []

    import sqlite3
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT company, contacts_json FROM targets WHERE contacts_json IS NOT NULL").fetchall()
    conn.close()

    people = []
    for row in rows:
        company = row["company"]
        try:
            contacts = json.loads(row["contacts_json"])
            if not isinstance(contacts, list):
                continue
        except (json.JSONDecodeError, TypeError):
            continue
        for c in contacts:
            name = c.get("contact_name", "").strip()
            if not name:
                continue
            people.append({
                "name":                name,
                "org_name":            company,
                "title":               c.get("title"),
                "role_bucket":         c.get("role_bucket"),
                "source":              c.get("source"),
                "professional_signal": c.get("professional_signal"),
                "my_angle":            c.get("my_angle"),
                "status":              c.get("status", "to-research"),
                "is_kol":              False,
                "notes_file":          _notes_file(name, "03_Inputs/contacts"),
            })
    return people


def load_kol_people() -> list[dict]:
    """Parse kol_tracker.md into people rows."""
    text = KOL_PATH.read_text(encoding="utf-8")
    people = []
    current_track = None

    for line in text.splitlines():
        # detect section headings
        for heading, track in KOL_TRACK_MAP.items():
            if heading in line:
                current_track = track
                break

        # parse table rows (skip header and separator rows)
        if line.startswith("|") and current_track:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 4:
                continue
            name = cells[0].strip()
            if not name or name.lower() in ("name", "---", ":---", ""):
                continue
            role  = cells[1].strip()
            org   = cells[2].strip()
            why   = cells[3].strip() if len(cells) > 3 else ""

            people.append({
                "name":       name,
                "org_name":   org,
                "title":      role,
                "is_kol":     True,
                "kol_track":  current_track,
                "why_track":  why,
                "status":     "to-research",
                "notes_file": _notes_file(name, "03_Inputs/kols"),
            })
    return people


# ---------------------------------------------------------------------------
# Merge logic: CSV is the base, SQLite enriches in place
# ---------------------------------------------------------------------------

def merge_companies(csv_rows: list[dict], sqlite_rows: list[dict]) -> list[dict]:
    by_name = {r["name"].lower(): r for r in csv_rows}
    for s in sqlite_rows:
        key = s["name"].lower()
        if key in by_name:
            # SQLite wins on scored/enriched fields; CSV wins on category/priority
            base = by_name[key]
            base.update({k: v for k, v in s.items() if v is not None and k not in ("notes_file",)})
            by_name[key] = base
        else:
            by_name[key] = s
    return list(by_name.values())


# ---------------------------------------------------------------------------
# Supabase upsert
# ---------------------------------------------------------------------------

def upsert_companies(sb, companies: list[dict], dry_run: bool):
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Upserting {len(companies)} companies...")
    for c in companies:
        if dry_run:
            print(f"  → {c['name']} | band={c.get('fit_band','?')} | status={c.get('status','?')}")
        else:
            sb.table("companies").upsert(c, on_conflict="name").execute()
    if not dry_run:
        print(f"  ✓ {len(companies)} companies upserted.")


def upsert_people(sb, people: list[dict], dry_run: bool):
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Upserting {len(people)} people...")

    # resolve org_id from Supabase if not dry run
    org_cache: dict[str, int] = {}

    def get_org_id(org_name: str) -> int | None:
        if not org_name or dry_run:
            return None
        if org_name not in org_cache:
            res = sb.table("companies").select("id").eq("name", org_name).execute()
            if res.data:
                org_cache[org_name] = res.data[0]["id"]
            else:
                org_cache[org_name] = None
        return org_cache.get(org_name)

    for p in people:
        if dry_run:
            kol_tag = " [KOL]" if p.get("is_kol") else ""
            print(f"  → {p['name']} @ {p.get('org_name','?')}{kol_tag} | track={p.get('kol_track') or p.get('track','?')}")
        else:
            row = {**p, "org_id": get_org_id(p.get("org_name"))}
            sb.table("people").upsert(row, on_conflict="name,org_name").execute()

    if not dry_run:
        print(f"  ✓ {len(people)} people upserted.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print what would be upserted without writing")
    args = parser.parse_args()

    if not args.dry_run:
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
            sys.exit(1)
        from supabase import create_client
        sb = create_client(SUPABASE_URL, SUPABASE_KEY)
    else:
        sb = None

    print("Loading data sources...")
    csv_companies   = load_csv_companies()
    sqlite_companies = load_sqlite_companies()
    contacts        = load_sqlite_contacts()
    kols            = load_kol_people()

    companies = merge_companies(csv_companies, sqlite_companies)
    people    = contacts + kols

    print(f"  CSV companies:    {len(csv_companies)}")
    print(f"  SQLite companies: {len(sqlite_companies)}")
    print(f"  Merged total:     {len(companies)}")
    print(f"  Contacts (SQLite): {len(contacts)}")
    print(f"  KOLs (markdown):   {len(kols)}")
    print(f"  People total:      {len(people)}")

    upsert_companies(sb, companies, dry_run=args.dry_run)
    upsert_people(sb, people, dry_run=args.dry_run)

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Done.")
    if args.dry_run:
        print("Re-run without --dry-run to write to Supabase.")


if __name__ == "__main__":
    main()
