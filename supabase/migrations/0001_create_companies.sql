-- Migration 0001: companies table
-- Mirrors scoring_schema.md exactly. Do not add scoring fields not in the schema.

CREATE TABLE IF NOT EXISTS companies (
    id                      BIGSERIAL PRIMARY KEY,

    -- identity
    name                    TEXT NOT NULL,
    parent_franchise        TEXT,
    arm_name                TEXT,
    modality                TEXT,

    -- classification (from target_list.csv)
    category                TEXT,           -- service_provider | standalone_rna | franchise_arm | channel
    engagement_type         TEXT,           -- consulting | relationship | channel | partner
    evidence                TEXT,           -- confirmed | candidate-verify
    priority                INTEGER,        -- 1 (highest) to 4

    -- arm-detection signals (schema Part 1)
    -- stored as comma-separated signal codes, e.g. "S1,S2,S4"
    signals_hit             TEXT,
    arm_status              TEXT,           -- dormant | forming | active

    -- fit factors (schema Part 2) — ratings 0 | 1 | 2
    "F1"                    INTEGER CHECK ("F1" IN (0,1,2)),
    "F2"                    INTEGER CHECK ("F2" IN (0,1,2)),
    "F3"                    INTEGER CHECK ("F3" IN (0,1,2)),
    "F4"                    INTEGER CHECK ("F4" IN (0,1,2)),

    -- computed score (schema formula: F1*15 + F2*15 + F3*12.5 + F4*7.5)
    fit_score               NUMERIC(5,2),
    fit_band                TEXT,           -- hot | warm | park

    -- access tags (schema Part 3)
    access_warmth           TEXT,           -- cold | warm_arcturus | warm_network
    bio_partnering_attending TEXT,          -- yes | no | unknown

    -- research content
    paper_trail_hook        TEXT,
    source_links            TEXT,
    translation_summary     TEXT,
    low_confidence_fields   TEXT,
    raw_note                TEXT,

    -- CRM tracking
    status                  TEXT DEFAULT 'to-research',  -- to-research | enriched | contacted | meeting | dead
    touch_count             INTEGER DEFAULT 0,
    last_contact_date       DATE,
    last_contact_channel    TEXT,
    reply_due_date          DATE,

    -- link to markdown notes file in repo (e.g. "03_Inputs/replicate-bioscience.md")
    notes_file              TEXT,

    created_at              TIMESTAMPTZ DEFAULT NOW(),
    updated_at              TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT companies_name_unique UNIQUE (name)
);

-- auto-update updated_at on any row change
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER companies_updated_at
    BEFORE UPDATE ON companies
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
