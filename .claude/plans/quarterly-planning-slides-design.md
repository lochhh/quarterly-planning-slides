# Quarterly Planning Slides — Design Doc

## What this tool does

Automates NIU quarterly planning slide deck generation for Chang Huan (CH / lochhh).

Given a start date and end date (next quarterly planning meeting):
1. Extracts GitHub activity via `gh` CLI
2. Fetches + parses team quarterly planning notes from GitHub
3. Asks structured Q&A to fill lessons learned and next-quarter priorities
4. Generates a HackMD reveal.js slide deck
5. Publishes to HackMD as a new note

## End date semantics

The end date is always the quarterly planning meeting date (explicit arg, never derived):
- Names the output file: `deliverables/slides-<end_date>.md`
- Appears in the slide subtitle: `dd.mm.yyyy`
- Caps GitHub search: `min(end_date, today)` — handles future meeting dates

## Architecture

Claude orchestrates 6 phases. Python scripts in `tools/` are tools Claude calls.
Each phase produces a JSON handoff artifact in `.claude/handoff/`.

```
Phase 1: Tooling        → verify/create tools/
Phase 2: Extraction     → .claude/handoff/github_activity.json
                          .claude/handoff/quarterly_notes.json
Phase 3: Analysis       → Claude builds per-project summary (no artifact)
Phase 4: Inquiry        → Q&A → .claude/handoff/qa_answers.json
Phase 5: Synthesis      → deliverables/slides-<yyyy-mm-dd>.md
Phase 6: Publication    → sync-hackmd --create → new HackMD note URL
```

Claude waits for user confirmation at each phase boundary (CLAUDE.md rule).

## Scripts

### tools/extract_github.py

- Args: `--author lochhh`, `--start YYYY-MM-DD`, `--end YYYY-MM-DD`
- Fetches: PRs, issues, commits (via GraphQL contributionsCollection)
- Excludes repos: `e-babylab`, `claude-code-slides`, `quarterly-planning-slides`
- Output: `.claude/handoff/github_activity.json`

### tools/parse_quarterly_notes.py

- Args: `--start YYYY-MM-DD`
- Finds the notes file at `neuroinformatics-unit/documentation/minutes/quarterly_planning/`
  with date closest to `--start`
- Extracts deliverables from "Deliverables for next quarter" section for: Aeon, Movement, PoseInterface
- Assignment rules:
  - **Aeon**: all deliverables → `ch` (CH owns all Aeon work)
  - **Movement / PoseInterface**: gather all deliverables regardless of ownership; analysis is per-project, no need to confirm ownership
  - "PoseInterface" also matches "pose interface" (space variant in notes)
  - "Movement" also matches "movement" (lowercase variant in notes)
- Also parses "Personal time allocation > CH" markdown table for per-project
  commitment data (`commitment_next_quarter`, `notes`)
- Flags unassigned items → Claude asks user to confirm ownership in phase 4; except for movement/poseinterface deliverables which are all included regardless of ownership
- Output: `.claude/handoff/quarterly_notes.json`

Output JSON shape:
```json
{
  "notes_date": "YYYY-MM-DD",
  "source_file": "YYYY-MM-DD.md",
  "projects": {
    "Aeon": {
      "deliverables": [{"text": "...", "assigned": "ch", "raw": "..."}]
    }
  },
  "ch_time_allocation": {
    "Aeon": {"commitment_next_quarter": "3w", "notes": "..."},
    "movement": {"commitment_next_quarter": "2w", "notes": "..."}
  },
  "unassigned_deliverables": [{"project": "...", "text": "..."}]
}
```

### tools/generate_slides.py

- Args: `--github-data`, `--quarterly-data`, `--qa-data`, `--output` (optional)
- Renders HackMD reveal.js Markdown from all 3 JSONs
- Output: `deliverables/slides-<end_date>.md`

### .claude/skills/sync-hackmd/sync_hackmd.py (updated)

- `python sync_hackmd.py <file> <note_id>` — update existing note (PATCH)
- `python sync_hackmd.py <file> --create` — create new note (POST), prints URL + ID

## Q&A schema (.claude/handoff/qa_answers.json)

Claude writes this after Phase 4 Q&A:

```json
{
  "projects": {
    "Aeon": {
      "lessons_learned": ["..."],
      "priorities": ["..."],
      "extra_notes": ""
    },
    "Movement": { "lessons_learned": [], "priorities": [], "extra_notes": "" },
    "PoseInterface": { "lessons_learned": [], "priorities": [], "extra_notes": "" }
  }
}
```

## Slide structure

```
Title (NIU Quarterly Planning / dd.mm.yyyy / Chang Huan Lo)
---
Projects Overview (brief intro, 1-2 sentences per project)
----
[sub-slides if needed]
---
Last Quarter — [Project] (planned deliverables + unplanned PRs)
----
[one sub-slide per project]
---
Lessons Learned — [Project]
----
[one sub-slide per project if needed]
---
Next Quarter — [Project]
----
[one sub-slide per project if needed]
```

## Phase 3 analysis format (Claude output)

```
### [Project]
**Found in GitHub:** N PRs, N issues — bullet summaries
**Found in quarterly notes:** planned deliverables
**Missing / needs input:** gaps
```

## Phase 4 Q&A questions per project (3-5 each)

0. Which projects to include/exclude in the slides? 
1. What went well this quarter?
2. What was the biggest challenge or blocker?
3. Any unexpected outcomes (wins or slips)?
4. Top 2-3 priorities for next quarter?
5. Any cross-team dependencies to flag?

Unassigned deliverables: "Was [deliverable] something you worked on? (yes/no/partially)"
