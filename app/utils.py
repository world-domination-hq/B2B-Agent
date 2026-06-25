import csv
import io
import json


def parse_upload(file_bytes, filename):
    text = file_bytes.decode("utf-8", errors="ignore")
    if filename.lower().endswith(".csv"):
        return _parse_csv_text(text)
    return text


def _parse_csv_text(text):
    reader = csv.DictReader(io.StringIO(text))
    return [row for row in reader]


def safe_json_load(text):
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def safe_json_dump(data):
    if data is None:
        return None
    return json.dumps(data, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Scoring engine — source of truth: 01_Schema/scoring_schema.md
# ---------------------------------------------------------------------------

def compute_fit_score(F1: int, F2: int, F3: int, F4: int) -> float:
    """
    fit_score = (F1*15) + (F2*15) + (F3*12.5) + (F4*7.5)
    Each rating is 0, 1, or 2. Max = 100.
    """
    return (F1 * 15) + (F2 * 15) + (F3 * 12.5) + (F4 * 7.5)


def compute_fit_band(fit_score: float) -> str:
    if fit_score >= 80:
        return "hot"
    if fit_score >= 50:
        return "warm"
    return "park"


def compute_arm_status(signals_hit: list[str]) -> str:
    count = len([s for s in signals_hit if s.strip()])
    if count >= 4:
        return "active"
    if count >= 2:
        return "forming"
    return "dormant"


def score_record(record: dict) -> dict:
    """
    Given a record dict with F1–F4 ratings and signals_hit, return a copy
    with fit_score, fit_band, and arm_status filled in.
    """
    record = record.copy()

    # signals → arm_status
    raw_signals = record.get("signals_hit") or ""
    if isinstance(raw_signals, str):
        signals = [s.strip() for s in raw_signals.split(",") if s.strip()]
    else:
        signals = list(raw_signals)
    record["arm_status"] = compute_arm_status(signals)

    # F1–F4 → fit_score + fit_band (only for forming/active)
    if record["arm_status"] in ("forming", "active"):
        try:
            F1 = int(record.get("F1") or 0)
            F2 = int(record.get("F2") or 0)
            F3 = int(record.get("F3") or 0)
            F4 = int(record.get("F4") or 0)
        except (ValueError, TypeError):
            F1 = F2 = F3 = F4 = 0
        record["fit_score"] = compute_fit_score(F1, F2, F3, F4)
        record["fit_band"] = compute_fit_band(record["fit_score"])
    else:
        record["fit_score"] = 0.0
        record["fit_band"] = "park"

    return record
