-- Migration 0003: touchpoints table
-- Every outreach attempt or response logged here, linked to a company and optionally a person.

CREATE TABLE IF NOT EXISTS touchpoints (
    id                  BIGSERIAL PRIMARY KEY,

    company_id          BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    person_id           BIGINT REFERENCES people(id) ON DELETE SET NULL,

    date                DATE NOT NULL DEFAULT CURRENT_DATE,
    channel             TEXT,               -- email | linkedin | event | call | other
    outcome             TEXT,               -- sent | opened | replied | meeting | no-response | bounced
    follow_up_date      DATE,
    leverage_notes      TEXT,               -- what you learned or can use next time

    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- index for fast lookup by company
CREATE INDEX touchpoints_company_idx ON touchpoints(company_id);
CREATE INDEX touchpoints_person_idx  ON touchpoints(person_id);
