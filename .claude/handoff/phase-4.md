# Phase 4 — Inquiry Phase Handoff

## User Answers

### Aeon

**Q1 — ARC-DJ / HPC**
- Private repo: https://github.com/UCL-ARC/SWC-aeon-datajoint/
- Replicated DataJoint setup on RHEL VM ✅
- Next step: ingest data (not yet done this quarter)

**Q2 — aeon_mecha releases**
- v0.3.0 = Pydantic migration (from DotMap) — planned deliverable
- v0.4.0 = DataJoint 2.x syntax migration — planned deliverable (pair with v0.3.0)
- v0.4.1, v0.4.2, v0.4.3 = bug fixes and refactors (unplanned patches)
- Issue #577 (spike sorting scripts): not mentioned as next quarter scope

**Q3 — aeon_api PR #82**
- Pending review
- Coverage: 78% → 99%
- Carries into next quarter (review + merge)

---

### Movement

**Q4 — COCO PR #818**
- Closed as out of scope: was for loading COCO *results* format, not annotations
- New direction: support loading COCO *annotations* + individual-wise confidence scores
- Issue #1000 ("Add support for COCO keypoint results format") = separate, open

**Q5 — Removing types from docstrings**
- Fully completed ✅

**Q6 — PR reduction**
- Quarter start: 80+ open PRs
- Quarter end: 60+ open PRs
- Reduced by ~20

---

### PoseInterface

**Q7 — Upload 2 SWC sessions (1 train / 1 test)**
- Not done ❌

**Q8 — Ethology scope clarification**
- Not done ❌

---

## Updated Deliverable Status (delta from Phase 3)

| Deliverable | Old | New | Notes |
|---|---|---|---|
| ARC-DJ (support) | ❓ | ⚠️ | RHEL VM set up; data ingestion pending |
| build infrastructure on SWC HPC | ❓ | ✅ | RHEL VM replicated (private repo) |
| ingest full social data | ❓ | 🔄 | Not yet ingested; infra ready |
| aeon_mecha v0.3.0 | ✅ | ✅ | Pydantic migration; v0.4.0 = DJ2.x migration (also planned) |
| Removing types from docstrings | ⚠️ | ✅ | Fully done |
| Help COCO PR #818 get merged | ❓ | ✅ | Closed (out of scope); pivoted to annotations |
| Ruthlessly cut open PRs | ⚠️ | ⚠️ | 80+ → 60+; partial progress |
| Upload 2 SWC sessions | ❓ | ❌ | Not done |
| Clarify ethology scope | ⚠️ | ❌ | Not done |

---

## Key Narrative Points for Slides

### Aeon
- v0.3.0 (Pydantic) + v0.4.0 (DJ2.x) delivered as a pair — major pipeline modernisation
- v0.4.1–v0.4.3 follow-up patches show active maintenance
- ARC-DJ: infrastructure landed on RHEL VM; data ingestion is the remaining step
- aeon_api near-complete: coverage 78% → 99%, pending review

### Movement
- Scope change: COCO results loading deprioritised; pivoted to annotations + confidence scores
- Docstring cleanup fully done
- ~20 PRs closed but still 60+ open — partial on "ruthless" goal
- Strong unplanned output: upstream fix (sphinx-autodoc-typehints), pre-commit hook, PEP 735, fork review

### PoseInterface
- Core data pipeline delivered by team (clips, cliplabels, video utilities)
- COCO/annotations work partially done (CH refactored annotations_to_coco)
- 2 deliverables not done: SWC session upload + ethology scope
- sleap-io upstream fix unblocked the pipeline

---

## Next Steps — Phase 5 (Synthesis)
- Combine Phase 3 status + Phase 4 answers
- Generate reveal.js slide deck: `deliverables/slides-2026-06-01.md`
- Structure: title → time allocation → per-project (planned ✅ / unplanned / carry-over) → cross-cutting themes
