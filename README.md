# quarterly-planning-slides
Tool to generate team quarterly planning slides

## Initial Prompt

# Objective
Build a tool that, given a start date and end date (where the end date is the date of the next quarterly planning meeting), uses the GitHub CLI (gh) to extract all work I (CH / Chang Huan) completed in that period, combines this with quarterly planning notes, asks me structured questions for missing sections, generates a 5–10 minute HackMD reveal.js slide deck, and finally syncs the generated slides-<yyyy-mm-dd>.md to HackMD.io using my existing sync-hackmd skill.

The slide deck must include:
- A brief intro for each project
- Deliverables/outcomes (planned and unplanned, if any) from the last quarter
- Lessons learned (to be filled in via structured Q&A with me)
- Priorities for next quarter (also via structured Q&A)

## End-Date Semantics
The **end date** has 3 roles:
- naming the output file: the slide deck filename is slides-<yyyy-mm-dd>.md
- subtitle inside the slide deck (see #slide-deck-requirements)
- upper bound for GitHub activity extraction

## Data Sources
### Team quarterly notes
- stored at: https://github.com/neuroinformatics-unit/documentation/blob/main/minutes/quarterly_planning/<yyyy-mm-dd>.md
- Use the file with the closest date to the provided start date.
- The file contains the entire team's notes, including info irrelevant to me
- Relevant projects for me: Aeon, Movement, PoseInterface
- My mentions appear as "CH" or "Chang Huan"
- If nobody is specified/assigned to a project deliverable that's directly relevant for me, ask me to confirm   

### My GitHub activity
Use gh CLI to collect, within the specified start, end dates:
- All PRs, issues, commits, and discussions I contributed to in that period.
- Exclude these repositories: e-Babylab, claude-code-slides, quarterly-planning-slides
This must handle the case when end date is a future date (see #end-date-semantics)

## Tool Requirements
- Place Python scripts in `tools` 
- API calls, data transformations, file operations, database queries 
- Credentials and API keys are stored in `.env`

## Slide Deck Requirements
Generate a HackMD reveal.js slide deck (deliverables/slides-<yyyy-mm-dd>.md, where the date is the quarterly planning date) with the following front matter and title slide:

```yaml
---
slideOptions:
   transition: slide
   tags: NIU_team-meeting
---

# NIU Quarterly Planning

dd.mm.yyyy

Chang Huan Lo

---
````

### Structure
- Aim for a 5-10 minute presentation with 4 main slides (i.e. sections):
  - Brief intro on project(s)
  - Deliverables/outcomes from the last quarter
  - Lessons learned (ask me questions to fill these in)
  - Priorities for next quarter (ask me questions to fill these in)
- If the content of the main slide "overflows" or if there are multiple subsections within each section, split these into sub-slides using `----`.
- Avoid verbosity

### reveal.js Syntax Reference
| Element | Syntax |
|---------|--------|
| Slide separator (horizontal) | `---` on its own line |
| Slide separator (vertical/sub) | `----` on its own line |
| Speaker notes | `Note: <text>` after slide content |
| Slide title | `## Title` (h2 = slide heading) |
| Fragment (appear on click) | `<!-- .element: class="fragment" -->` |
| Background colour | `<!-- .slide: data-background="#hex" -->` |
| Code block | standard fenced ` ``` ` |

## Interaction Protocol
1. After extracting GitHub + quarterly notes data, produce a **per-project summary** of:
   - What you found
   - What's missing
   - What needs my input
2. Ask me **3-5 structured, actionable questions per-project** to fill in:
   - Lessons learnt
   - Priorities for next quarter
3. Generate the final `deliverables/slides-<yyyy-mm-dd>.md`. 
4. Sync the file to hackmd.io using the `sync-hackmd` skill