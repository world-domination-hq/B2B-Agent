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
