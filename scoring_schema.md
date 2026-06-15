# Scoring Schema (Document B)

This is the agent's brain. It defines what to record per company and per person, how to detect a real RNA/biologics arm, and how to score fit for a CMC-partner relationship. Education is the wedge. The relationship you are scoring toward is **CMC partner doing scale-up and auditing**, not a one-off content sale.

---

## Part 1: arm-detection signals (run this first)

Before scoring fit or finding contacts, decide whether the company has a real RNA/biologics arm that is early enough to need outside CMC help. Check each signal. Each is a yes/no.

| # | Signal | What it looks like |
|---|---|---|
| S1 | Build-verb senior hire | A title like "Head of mRNA," "VP Genetic Medicine," or a bio saying "establishing / standing up" a platform |
| S2 | CMC req cluster | Several CMC, process development, analytical, or quality roles opening together, often in a new location |
| S3 | New site / facility | A facility or suite tagged to RNA, LNP, or biologics |
| S4 | First modality asset | A first preclinical or clinical asset in the new modality (trial, poster, pipeline page) |
| S5 | Platform in-license / acquisition | They bought or licensed an RNA, LNP, or delivery platform |
| S6 | New-segment language | A 10-K, annual report, or investor deck introduces the modality as a new segment |
| S7 | New BD / partnering | Partnering or conference activity in the modality (BIO Partnering profile, deal news) |

**arm_status** = count of signals:
- 0 to 1 = `dormant` (do not spend enrichment time)
- 2 to 3 = `forming` (worth a contact pass)
- 4 or more = `active` (priority: real spend, real gap)

The earlier and leaner the arm, the better for you, because that is the de-risking window when outside CMC partners are cheapest to bring in.

---

## Part 2: fit score (0 to 100)

Score only companies that are `forming` or `active`. Four inputs, weighted. Keep it simple: rate each input 0, 1, or 2, multiply by its weight, sum.

| Input | What scores high | Weight | 0 / 1 / 2 meaning |
|---|---|---|---|
| F1 Arm stage / spend window | Pre-GMP, IND-enabling, first-in-modality | 30 | 0 commercial, 1 clinical, 2 pre-GMP/IND-enabling |
| F2 Internal CMC maturity gap | Thin or no internal CMC/quality/MSAT for this modality | 30 | 0 deep team, 1 partial, 2 thin/none |
| F3 Modality match to your depth | saRNA, LNP, mRNA drug substance/product, plasmid | 25 | 0 outside, 1 adjacent, 2 direct |
| F4 Leverage of your edge | Your Arcturus saRNA/LNP knowledge maps to their modality | 15 | 0 none, 1 some, 2 strong |

**fit_score** = F1*15-equivalent... use this exact formula to avoid math drift:
`fit_score = (F1_rating * 15) + (F2_rating * 15) + (F3_rating * 12.5) + (F4_rating * 7.5)`
(each input maxes at its weight when rating = 2)

Bands:
- 80 to 100 = `hot` (lead with a CMC-partner conversation)
- 50 to 79 = `warm` (lead with the education wedge, build toward partner)
- below 50 = `park` (newsletter / nurture only)

---

## Part 3: separate tags (do not fold into the score)

These describe access and type, not fit. Keep them as their own fields so they do not distort the number.

- **engagement_type**: `consulting` | `relationship` | `channel` | `partner`
- **access_warmth**: `cold` | `warm_arcturus` (competitor/peer path) | `warm_network` (you know someone)
- **bio_partnering_attending**: `yes` | `no` | `unknown` (source: BIO Partnering directory first, LinkedIn #BIO2026 second)

The internal-relationships-first reflex is real, so `access_warmth` is what overcomes it. A `hot` fit with `cold` access still needs a way in; a `warm_arcturus` path is your unlock.

---

## Part 4: fields per company

- company
- parent_franchise (blank if standalone)
- arm_name
- modality
- arm_status (dormant / forming / active)
- signals_hit (list, e.g. S1,S2,S4)
- F1, F2, F3, F4 (ratings)
- fit_score
- fit_band (hot / warm / park)
- engagement_type
- access_warmth
- bio_partnering_attending
- paper_trail_hook (the one real fact your opener references)
- source_links

## Part 5: fields per contact (several per company)

- contact_name
- role_bucket: `BD` | `scientist` | `marketing` | `exec`
- title
- source: `EDGAR` | `press` | `PubMed` | `LinkedIn` | `BIO Partnering`
- professional_signal (a real, public, professional fact: a paper, a talk title, a recent post, a prior role). Keep it professional only. No private personal data.
- my_angle (one line that connects their signal to your CMC-partner value)
- status: `to-research` | `enriched` | `contacted` | `meeting` | `dead`

---

## Part 6: ClickUp field map

Make one ClickUp List called **BIO CMC Targets**. Use one task per contact, with company-level fields repeated on the task (simplest for a first build).

| ClickUp field | Type | Source field above |
|---|---|---|
| Company | text | company |
| Parent | text | parent_franchise |
| Modality | dropdown | modality |
| Arm status | dropdown | arm_status |
| Fit score | number | fit_score |
| Fit band | dropdown | fit_band |
| Engagement | dropdown | engagement_type |
| Access | dropdown | access_warmth |
| At BIO | dropdown | bio_partnering_attending |
| Hook | text | paper_trail_hook |
| Contact | text | contact_name |
| Role | dropdown | role_bucket |
| Title | text | title |
| Signal | text | professional_signal |
| My angle | text | my_angle |
| Status | dropdown (task status) | status |

You can paste the CSV-style output from Step 4 straight into ClickUp's table view, or import it.

---

## Compliance guardrails (read once)

- Use the BIO Partnering directory as the attendance source of truth. It is sanctioned and beats guessing from posts.
- Do not run automated scraping of LinkedIn. It violates their terms and risks your account. Use Sales Navigator manually for role lookup.
- Store professional signal only (pubs, talks, roles, public posts). Do not collect or store private personal data. That keeps you clear of CCPA / GDPR exposure and keeps your openers credible.
