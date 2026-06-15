SCHEMA_PROMPT = """
You are building a BIO CMC target research record. Use the scoring schema in 01_schema/scoring_schema.md.

Return JSON with these fields:
- company
- parent_franchise
- arm_name
- modality
- signals_hit
- arm_status
- F1
- F2
- F3
- F4
- engagement_type
- access_warmth
- bio_partnering_attending
- paper_trail_hook
- source_links
- contacts_json (list of contact objects)
- raw_note
"""

TRANSLATE_PROMPT = """
Take the company research record and return:
- translation_summary: a plain-English summary the user can read quickly
- low_confidence_fields: a list of field names that are uncertain or need review
"""
