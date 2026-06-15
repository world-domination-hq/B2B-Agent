from datetime import datetime
import json
from pathlib import Path
from schema import get_connection, init_db


def _normalize_json(value):
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _csv_join(values):
    if values is None:
        return None
    if isinstance(values, str):
        return values
    return ", ".join([str(v).strip() for v in values if v])


def get_all_targets(search_text=None):
    init_db()
    with get_connection() as conn:
        if search_text:
            query = "SELECT * FROM targets WHERE company LIKE ? OR paper_trail_hook LIKE ? ORDER BY fit_score DESC NULLS LAST"
            rows = conn.execute(query, (f"%{search_text}%", f"%{search_text}%")).fetchall()
        else:
            rows = conn.execute("SELECT * FROM targets ORDER BY fit_score DESC NULLS LAST").fetchall()
    return [dict(row) for row in rows]


def get_target(target_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM targets WHERE id = ?", (target_id,)).fetchone()
    return dict(row) if row else None


def save_target(record):
    init_db()
    now = datetime.utcnow().isoformat()
    record = record.copy()
    record["contacts_json"] = _normalize_json(record.get("contacts_json"))
    record["signals_hit"] = _csv_join(record.get("signals_hit"))
    record["source_links"] = _csv_join(record.get("source_links"))
    record["low_confidence_fields"] = _csv_join(record.get("low_confidence_fields"))
    record["created_at"] = now
    record["updated_at"] = now

    columns = ", ".join(record.keys())
    placeholders = ", ".join(["?" for _ in record])
    values = list(record.values())

    with get_connection() as conn:
        conn.execute(f"INSERT INTO targets ({columns}) VALUES ({placeholders})", values)
        conn.commit()


def update_target(target_id, updates):
    updates = updates.copy()
    if "contacts_json" in updates:
        updates["contacts_json"] = _normalize_json(updates.get("contacts_json"))
    if "signals_hit" in updates:
        updates["signals_hit"] = _csv_join(updates.get("signals_hit"))
    if "source_links" in updates:
        updates["source_links"] = _csv_join(updates.get("source_links"))
    if "low_confidence_fields" in updates:
        updates["low_confidence_fields"] = _csv_join(updates.get("low_confidence_fields"))

    updates["updated_at"] = datetime.utcnow().isoformat()
    assignments = ", ".join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values()) + [target_id]

    with get_connection() as conn:
        conn.execute(f"UPDATE targets SET {assignments} WHERE id = ?", values)
        conn.commit()


def delete_target(target_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM targets WHERE id = ?", (target_id,))
        conn.commit()
