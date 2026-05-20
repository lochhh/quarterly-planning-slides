# Claude Code Behaviour Rules

## General Principles
- Operate as a structured, deterministic assistant for generating NIU quarterly planning slide decks.
- Follow a strict phase-based workflow (see below).
- Prefer running Python scripts in `tools/` for extraction, parsing, and slide generation.
- If a required script does not exist, generate it during the Tooling Phase.
- Never invent data; ask the user when information is missing.
- Keep outputs concise, engineering-grade, and suitable for a 5–10 minute presentation.

---

## Directory & File Conventions
- Python utilities live in `tools/`.
- Generated slide decks are written to `deliverables/slides-<yyyy-mm-dd>.md`.
- Never overwrite files without explicit user approval.
- Credentials and API keys are stored in `.env` and must not be printed.

---

## Phase-Based Workflow

### Phase 1 — Tooling Phase
- Check for required scripts:
  - `extract_github.py`
  - `parse_quarterly_notes.py`
  - `generate_slides.py`
- If missing, create them with correct functionality.
- Summarise created/verified tools and wait for confirmation.

### Phase 2 — Extraction Phase
- Run Python tools to extract GitHub activity and quarterly notes.
- Ask for and use provided start and end dates.
- Exclude irrelevant repositories.
- Produce structured JSON and summarise results.

### Phase 3 — Analysis Phase
- Organise extracted data per project.
- Identify gaps or unclear ownership.
- Prepare structured questions for the user.

### Phase 4 — Inquiry Phase
- Ask 3–5 concise, actionable questions per project.
- Wait for user responses before continuing.

### Phase 5 — Synthesis Phase
- Combine extracted data and user answers.
- Generate the reveal.js slide deck in the required format.
- Ensure correct filename and front matter.

### Phase 6 — Publication Phase
- Present the final slide deck to the user.
- Sync to HackMD only after explicit approval using the `sync-hackmd` skill.

---

## Phase Boundary Rules
- At the end of each phase, summarise what was completed and what the next steps are in `.claude/handoff/phase-<n>.md` to ensure seamless handoff.
- Wait for user confirmation before advancing.
- Do not skip or merge phases.

---

## Reset Rules
- At the start of each phase, read the previous phase's handoff file to ensure continuity.
- Treat previous content as read-only.
- Request missing inputs if needed.

---

## Safety & Consistency
- Never hallucinate GitHub or quarterly notes content.
- Ask for confirmation when ownership is unclear.
- Never sync to HackMD without explicit approval.
