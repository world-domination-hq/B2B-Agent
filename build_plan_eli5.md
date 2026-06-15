# Build Plan (ELI5), 2 to 3 days

You have never built an agent. Good news: you are not building software. You are building a tidy set of folders and running prompts by hand. Think of it like a recipe binder. Each folder is a step. You do the steps in order.

## What "agent" means here
An agent is just: instructions + inputs + a place to put outputs. You are the runtime. The AI assistant does the thinking when you paste a prompt. Later you can automate it. Not now.

---

## Day 1: set up the binder and gather facts (about 3 to 4 hours)

1. **Make the repo.** On GitHub, create a new repository called `bio-cmc-agent`. Choose "private."
2. **Upload this folder.** Drag the whole `bio-cmc-agent` folder I gave you into the repo (GitHub lets you drag files into the web uploader). Now your folder structure exists online.
3. **Read two files:** `README.md` and `01_schema/scoring_schema.md`. That is the whole system.
4. **Pick your first 6 targets.** From `00_targets/target_list.md`, take the priority 1 and 2 rows: Replicate, Strand, AGC Biologics, ProBio, Arcturus, CSL/Seqirus.
5. **Gather raw facts** for each into a note (follow the "gather first" list in `02_prompts/step1_find_contacts.md`). For public ones, EDGAR officers section is the fastest real-name source. Save each note as `03_inputs/<company>.md`. Use the Replicate example as your shape.

Stop when you have 6 input notes. Do not score yet.

---

## Day 2: run the four prompts per target (about 4 to 5 hours)

For each of the 6 companies, in order, paste these into Claude and save the answers:
1. `step1_find_contacts.md` -> get arm_status + contact table.
2. `step2_enrich.md` -> get company read + per-person signal.
3. `step3_score.md` -> get fit_score + band + tags.
4. `step4_write_brief.md` -> get the one-page brief + the ClickUp CSV line.

Save each brief to `04_outputs/<company>.md`. Commit to GitHub as you go (the web editor has a "commit changes" button; just click it).

Tip: do Replicate first. It is your strongest target and gives you a clean template to copy.

---

## Day 3: rank, load ClickUp, prep openers (about 2 to 3 hours)

1. **Collect the CSV lines** from each brief into one file.
2. **Sort by fit_score.** Hot first.
3. **Load ClickUp.** Make the List "BIO CMC Targets" with the fields in the schema's Part 6, then paste or import your CSV lines.
4. **For every hot/warm target, confirm BIO attendance** in the BIO Partnering directory and set the "At BIO" field.
5. **Copy the openers** from each brief into your conference notes.

Done. You now have a ranked, sourced, opener-ready target sheet you ran yourself.

---

## What to skip if you run out of time
- Skip the franchise-arm group (Pfizer, J&J, etc.) for this BIO. Run arm detection on them later. They take longer to verify and pay off slower.
- Skip enrichment on any `dormant` arm. Move on.

## How to upgrade later (not now)
When you want it automated: replace your manual fact-gathering with a tool like Clay for contact enrichment, keep these exact prompts as the scoring brain, and have Claude write to ClickUp through your existing connector. The folders and schema stay the same. You just stop being the runtime.

## One reminder
No automated LinkedIn scraping. Use BIO Partnering for attendance and Sales Navigator by hand for titles. Professional signal only. This keeps you safe and keeps your openers credible.
