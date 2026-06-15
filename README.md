# BIO CMC Target Agent

A folder-driven research pipeline for finding and scoring RNA / biologics CMC opportunities. No coding. You run it by pasting prompts into an AI assistant (Claude) and saving the answers into folders.

## What this does, in one breath

For each target company, it finds the right people (BD, scientist, marketing, exec), pulls real background on them and the company, scores how well they fit a CMC-partner engagement, checks whether they are attending BIO, and writes you a one-page brief with an opener.

## The big idea: company vs arm

You are not targeting whole companies. You are targeting the small RNA or biologics **arm** inside a company that runs like a startup during its de-risking spend. A genetics or tools franchise standing up an mRNA platform on a lean team is your buyer even if the parent is huge. The agent's first job is to detect those arms. See `01_schema/scoring_schema.md`.

## How to run it (the loop)

1. Pick a company from `00_targets/target_list.md`.
2. Gather raw facts into `03_inputs/` (where to look is in each prompt).
3. Open `02_prompts/` and run the four prompts in order, pasting your raw facts each time.
4. Save the final brief into `04_outputs/`.
5. Move the best targets into ClickUp using the field map in the schema.

## Folder map

```
bio-cmc-agent/
  README.md                         <- you are here
  00_targets/
    target_list.md                  <- the full master list (Document A)
    target_list.csv                 <- same list as an editable table
  01_schema/
    scoring_schema.md               <- the agent's brain: fields, scoring, arm signals (Document B)
  02_prompts/
    step1_find_contacts.md          <- paste-in prompts, run in order
    step2_enrich.md
    step3_score.md
    step4_write_brief.md
  03_inputs/
    EXAMPLE_input_replicate.md      <- what raw facts look like before scoring
  04_outputs/
    EXAMPLE_brief_replicate.md      <- what a finished brief looks like
  05_build_plan/
    build_plan_eli5.md              <- day by day, 2 to 3 days
```

## Start here

Read `05_build_plan/build_plan_eli5.md` first. It tells you exactly what to do on Day 1.
