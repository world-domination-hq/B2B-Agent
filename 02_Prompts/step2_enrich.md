# Step 2: Enrich the company and the people

## What you do first
Add to your note any extra public signal you found: talk titles at conferences, recent LinkedIn posts (read manually, do not scrape), prior employers, pipeline stage, facility news.

## Prompt to paste into Claude

```
Using only the facts I paste, enrich this target.

For the COMPANY, summarize in 3 bullets: (1) what the RNA/biologics arm is doing, (2) its likely CMC maturity (deep / partial / thin), (3) its top current interest or pressure (e.g. IND timing, scale-up, a specific modality problem).

For each CONTACT, add a one-line professional_signal: a real public fact (a paper, a talk, a prior role, a post). Professional only, no private personal data.

Output the company bullets, then the contact lines.

FACTS:
[paste Step 1 output + any extra signal]
```

## What you get
A company read plus a usable hook per person. Append to the same `03_inputs/<company>.md`.
