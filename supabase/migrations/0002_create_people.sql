-- Migration 0002: people table
-- Covers both contacts (schema Part 5) and KOL tracker entries.
-- Replaces the contacts_json blob in the old SQLite targets table.

CREATE TABLE IF NOT EXISTS people (
    id                  BIGSERIAL PRIMARY KEY,

    -- identity
    name                TEXT NOT NULL,
    title               TEXT,
    org_id              BIGINT REFERENCES companies(id) ON DELETE SET NULL,
    org_name            TEXT,               -- denormalised fallback if no companies row yet

    -- schema Part 5 fields
    role_bucket         TEXT,               -- BD | scientist | marketing | exec
    source              TEXT,               -- EDGAR | press | PubMed | LinkedIn | BIO Partnering
    professional_signal TEXT,               -- one public professional fact
    my_angle            TEXT,               -- one-line connection to your CMC value

    -- KOL tracker fields
    is_kol              BOOLEAN DEFAULT FALSE,
    kol_track           TEXT,               -- cmc_reg | rare_disease | id_biosecurity | china_bd
    why_track           TEXT,               -- reason this person is worth following

    -- CRM
    track               TEXT,               -- cmc | reg | id | bd (for filtering)
    warm_intro_via      TEXT,
    status              TEXT DEFAULT 'to-research',  -- to-research | enriched | contacted | meeting | dead

    -- link to markdown notes file in repo
    notes_file          TEXT,

    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT people_name_org_unique UNIQUE (name, org_name)
);

CREATE TRIGGER people_updated_at
    BEFORE UPDATE ON people
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
