# BMAD Prompts for BIO CMC Target Agent

Use these exact prompts in Copilot Chat with the BMAD agents. Start with the PM agent, then the architect agent, then the builder agent. For nontechnical explanation, use the analyst or tech writer agent.

## 1. BMAD PM prompt

```
I am building the app described in PROJECT_BRIEF.md in this repo. I am a non-developer using GitHub Copilot.

Create a PRD for the MVP scope only (section 4 of PROJECT_BRIEF.md).

Requirements:
- Respect the hard constraints in section 7.
- Use the domain model in section 6 and the scoring schema in 01_schema/scoring_schema.md.
- Recommend the Streamlit + Claude API + SQLite stack unless there is a strong reason not to.
- Keep stories small enough that one passes per short session.
- Do not add features beyond the MVP scope.

Output:
- A clear PRD in `prd.md`.
- Epics and stories for E1 through E6.
- A short day-by-day plan for 2 to 3 days.
```

## 2. BMAD Architect prompt

```
I have a PRD for the BIO CMC Target Agent MVP in this repo. The project should be a simple local app built with Streamlit, SQLite, and optional Claude API integration.

Create an `architecture.md` that includes:
- a minimal folder and file structure,
- the core modules and responsibilities,
- the persistence design for SQLite,
- the model integration design,
- the UI pages/components needed,
- how the translation helper works.

The architecture should be enough for a developer to start building the MVP immediately.
```

## 3. BMAD Builder prompt

```
I have `PROJECT_BRIEF.md`, `prd.md`, and `architecture.md` in this repo. Build the MVP story by story.

Start with the first story from the PRD: ingest and save a draft target record locally. Then scaffold the next story: apply the scoring schema and show the records in a dashboard.

Create or update actual files in the repo. Keep the scope small and functional. Use Streamlit + SQLite for the MVP.
```

## 4. BMAD Analyst / Tech Writer prompt

```
I am a nontechnical user. Explain the current technical design and next steps in plain English.

Translate any code terms into simple language. Give me a short action list of what I should do next in this repo.
```

## 5. BMAD Workflow order

1. Run `bmad-agent-pm` with the PM prompt.
2. Run `bmad-agent-architect` with the architect prompt.
3. Run `bmad-agent-builder` with the builder prompt.
4. Use `bmad-agent-analyst` or `bmad-agent-tech-writer` to translate the plan into simple steps.

## 6. Notes

- If the builder agent needs to decide between a web app and local tool, choose local Streamlit for the MVP.
- Keep the app single-user and local.
- Keep LinkedIn scraping and live crawling out of scope.
