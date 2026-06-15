# Step 4: Write the one-page brief

## Prompt to paste into Claude

```
Write a one-page target brief from the facts and scores I paste. Operator voice, tight, no em-dashes. Sections:

1. Snapshot: company, arm, modality, arm_status, fit_score + band.
2. Why now: the de-risking window or pressure in one or two sentences.
3. People: each contact as a row -> name | role | title | professional_signal | my_angle (one line linking their signal to a CMC-partner conversation).
4. The opener: 2 to 3 sentences I could actually say or send, leading with the education wedge, pointing toward a CMC-partner relationship (scale-up, auditing). Reference the paper_trail_hook.
5. Access note: warmth tag + the specific way in (e.g. Arcturus peer path).

Also output one CSV line for ClickUp with these fields in order:
Company,Parent,Modality,Arm status,Fit score,Fit band,Engagement,Access,At BIO,Hook,Contact,Role,Title,Signal,My angle,Status

FACTS AND SCORES:
[paste Step 1 + 2 + 3 output]
```

## What you get
A brief you save to `04_outputs/<company>.md`, plus a CSV line you paste into ClickUp.
