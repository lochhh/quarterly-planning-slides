# Phase 5 — Synthesis Phase Handoff

## Output

`deliverables/slides-2026-06-01.md`

## Slide Structure

1. **Title** — NIU Quarterly Planning, 01.06.2026, Chang Huan Lo
2. **Time Allocation** — 3w Aeon, 2w Movement, 1.5w PoseInterface, 1w ARC-DJ, 0.5w Teaching, 1w admin
3. **Last Quarter — Aeon** — planned (with status) + unplanned + carry-overs
4. **Last Quarter — Movement** — planned (with status) + unplanned + carry-overs
5. **Last Quarter — PoseInterface** — planned (with status) + unplanned + carry-overs
6. **Next Quarter — Aeon / Movement / PoseInterface** (3 sub-slides, `----` separator)

## Status Summary in Slides

| Project | ✅ Done | ⚠️ Partial | 🔄 In Progress | ❌ Not Done |
|---|---|---|---|---|
| Aeon | 5 | 1 (ARC-DJ) | 2 (tests, ingest) | 0 |
| Movement | 2 | 1 (PRs) | 0 | 0 |
| PoseInterface | 2 | 1 (COCO) | 0 | 2 (upload, ethology) |

## Files Modified / Created

- `deliverables/slides-2026-06-01.md` — slide deck (new)
- `.claude/handoff/qa_answers.json` — Q&A + status + priorities (new)
- `tools/generate_slides.py` — enhanced: status markers, strip_md(), time allocation slide, unplanned/carry-over sections, PoseInterface unassigned deliverables included
- `tools/extract_github.py` — enhanced: releases + tags extraction

## Next Steps — Phase 6 (Publication)
- Review `deliverables/slides-2026-06-01.md`
- On explicit approval: sync to HackMD using `sync-hackmd` skill
