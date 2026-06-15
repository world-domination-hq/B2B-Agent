# Step 3: Score fit and tag access

## Prompt to paste into Claude

```
Score this target using my schema. Use only the facts I paste.

Rate four inputs 0, 1, or 2:
- F1 arm stage: 0 commercial, 1 clinical, 2 pre-GMP/IND-enabling
- F2 internal CMC maturity gap: 0 deep team, 1 partial, 2 thin/none
- F3 modality match to my depth (saRNA, LNP, mRNA drug substance/product, plasmid): 0 outside, 1 adjacent, 2 direct
- F4 leverage of my edge (ex-Arcturus saRNA/LNP knowledge maps to their modality): 0 none, 1 some, 2 strong

Compute: fit_score = (F1*15) + (F2*15) + (F3*12.5) + (F4*7.5)
Band it: 80-100 hot, 50-79 warm, below 50 park.

Then tag (do not add to score):
- engagement_type: consulting / relationship / channel / partner
- access_warmth: cold / warm_arcturus / warm_network
- bio_partnering_attending: yes / no / unknown

Output: the four ratings, the math, fit_score, band, and the three tags. One line each.

FACTS:
[paste Step 1 + Step 2 output]
```

## What you get
A defensible number and the access read. This is what decides who you chase first.
