# Step 1: Find the arm and the contacts

## What you do first (gather raw facts)
For the company you picked, collect into a note:
- For public parents: open SEC EDGAR (sec.gov/edgar), find the latest 10-K or DEF 14A proxy, copy the officers / management section and any RNA / genetic-medicine / mRNA language.
- Open the company's careers page, copy any CMC, process, analytical, quality, or MSL job titles.
- Google "[company] mRNA" or "[company] RNA platform" news from the last 12 months, copy headlines + dates.
- Open the BIO Partnering directory, search the company, note who is listed.
- PubMed: search "[company] mRNA" or a known scientist's name, copy 1 to 2 recent paper titles.

Paste all of that under "RAW FACTS" below.

## Prompt to paste into Claude

```
You are helping me build a CMC business-development target record. Use ONLY the raw facts I paste. Do not invent names or titles. If something is unknown, write "unknown."

First, run arm detection using these signals (S1 build-verb hire, S2 CMC req cluster, S3 new RNA/biologics site, S4 first modality asset, S5 platform in-license, S6 new-segment 10-K language, S7 new BD/partnering). List which signals are hit and set arm_status: dormant (0-1), forming (2-3), active (4+).

Then list the contacts you can find in the raw facts, bucketed as BD, scientist, marketing, or exec. For each: name, title, source. Mark role_bucket. Do not guess emails.

Output as a short table plus a one-line arm summary.

RAW FACTS:
[paste here]
```

## What you get
An arm_status call and a clean contact table. Save it into `03_inputs/<company>.md`.
