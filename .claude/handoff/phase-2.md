# Phase 2 — Extraction Phase Handoff

## Period
2026-03-03 to 2026-06-01

## GitHub Activity Summary
- **59 PRs**, **25 issues**, **38 commit entries** extracted

### Aeon (SainsburyWellcomeCentre)
**aeon_docs** — 11 PRs (9 merged, 1 open, 1 closed-not-merged)
- SVG rendering improvements (dark/light mode)
- Strip inline HTML from prev/next nav titles
- Pixi + pyproject.toml migration (open)
- URL fixes (redirected/broken), Aeon email, sample datasets rename, globus.org ignore
- CI: concurrency settings, fetch tags fix, docfx v2.78.5 / dotnet v8

**aeon_mecha** — 12 PRs (9 merged, 2 closed, 1 open)
- Ephys pipeline (v0.2.0)
- Pydantic metadata migration (from DotMap)
- DataJoint 0.14.x → 2.x upgrade
- Reorganise tests and ephys test factories (merged 2026-05-21, NEW)
- CI: combine lint+test workflows, Dependabot, DJ test isolation fixes, DataJoint URL updates

**aeon_api** — 7 PRs (1 merged, 4 open, 2 closed/test)
- Unit tests for analysis modules
- Type hints + Google docstrings
- PEP 735 dependency groups (open)
- Codecov investigation (2 test PRs closed)
- Disable uv caching for publish job (merged)

**aeon_exp_foragingABC** — 1 PR (open)
- NumPy 2 / Python 3.13 support

### Movement (neuroinformatics-unit/movement)
**11 PRs** (6 merged, 4 closed-not-merged, 1 open)
- PEP 735 dependency groups migration
- PEP 695 TypeAliasType rendering fix (+ upstream sphinx-autodoc-typehints fix merged)
- Pin sphinx-autodoc-typehints>=3.10.4 — follow-up to upstream fix (open, NEW)
- Pre-commit hook: prevent hardcoded movement website references (merged 2026-05-28, NEW)
- User warnings refactor (warnings.warn)
- Contributor table: fixed → responsive grid
- Team meeting presentation added
- Docstring updates, pandas intersphinx URL fix
- Codecov testing (3 test PRs closed)
- Review suggestions on fork PR (ishan372or/movement, merged 2026-05-27)

### PoseInterface (neuroinformatics-unit/poseinterface)
**4 PRs by CH** (2 merged, 1 open, 1 closed-test)
- PEP 735 migration
- Makefile standardisation
- Pin sleap-io>=0.7.1 — upstream fix released (merged 2026-05-27, NEW)

**All-contributor commits to main** (13 total, 2026-03-03 → 2026-06-01):

| Author | Commits | Key work |
|---|---|---|
| Chang Huan Lo | 4 | sleap-io pin, annotations_to_coco refactor, PEP 735, Makefile |
| Niko Sirmpilatze | 7 | README, DLC benchmark example, homepage image, spec improvements, website structure/redirect, startlabels spec |
| sfmig | 2 | cliplabels.json from movement predictions, video formatting + clip extraction |

Commit log (newest first):
- `1e38d7f` 2026-05-27 **CH** — Pin sleap-io>=0.7.1 (#55)
- `24e4a37` 2026-05-26 Niko — Add installation instructions in README (#54)
- `f3a141c` 2026-05-26 Niko — Update example for converting DLC project to benchmark (v2) (#49)
- `2e72f28` 2026-05-14 sfmig — Convert predictions to cliplabels.json using movement (#45)
- `14b19b3` 2026-05-13 Niko — Add project overview image to homepage (#51)
- `42ac536` 2026-05-12 sfmig — Format videos to poseinterface spec. Extract clip function. (#39)
- `2881508` 2026-05-12 **CH** — Refactor annotations_to_coco (#26)
- `b158210` 2026-04-28 **CH** — Migrate dev+docs to PEP 735 dependency groups (#46)
- `abb95bf` 2026-03-31 Niko — Spec: clarify contributed vs published datasets (#42)
- `7349d05` 2026-03-26 Niko — Update website structure and project metadata (#37)
- `849f26a` 2026-03-25 Niko — Redirect base URL to poseinterface.neuroinformatics.dev (#36)
- `fa975c1` 2026-03-25 **CH** — Standardise make files (#35)
- `8f17ad7` 2026-03-25 Niko — Spec: support clip start labels (startlabels.json) (#34)

### Cross-project (neuroinformatics-unit/actions)
**3 PRs** (3 merged)
- 404.html fix for multiversion Sphinx docs
- PEP 735 docs group support + fallback

### External upstream (tox-dev/sphinx-autodoc-typehints, talmolab/sleap-io)
- sphinx-autodoc-typehints: PEP 695 TypeAliasType fix — **merged upstream**
- sleap-io: empty frame handling fix — **merged upstream** (NEW — was open in prior run)

---

## Quarterly Notes Summary (from 2026-03-03.md — "Deliverables for next quarter" only)

Assignment rules: Aeon=all CH; Movement/PoseInterface=subsection headers (`CH:`, `All:`) + inline `(CH)` markers.

| Project | Deliverables | CH-owned | Unassigned |
|---|---|---|---|
| Aeon | 11 | 11 | 0 |
| Movement | 16 | 3 | 5 |
| PoseInterface | 5 | 0 | 5 |

**5 unassigned** — all PoseInterface (no explicit markers; CH time allocation 1.5w confirms ownership, expect quick confirmations).

### CH Time Allocation (next quarter, from notes)
| Project | Commitment |
|---|---|
| Aeon | 3w |
| movement | 2w |
| poseinterface | 1.5w |
| ARC-DJ | 1w |
| Teaching | 0.5w |

9 working weeks total (3/3/2026–26/5/2026, 1w Easter + 2w annual leave)

---

## Notable Changes vs Prior Run (search end 2026-05-20 → 2026-06-01)
- **+5 PRs**: aeon_mecha test reorganisation; sleap-io pin; movement fork review; movement pre-commit hook; sphinx-autodoc-typehints pin
- **+4 issues**: 3 movement issues (confidence scores, COCO support, docs); 1 aeon_mecha issue (spike sorting scripts)
- **sleap-io PR merged upstream** (was open)
- **+6 commits**: movement (×2), poseinterface (×2), aeon_mecha (×1), aeon_docs (×1 via poseinterface)

---

## Files Produced
- `.claude/handoff/github_activity.json`
- `.claude/handoff/quarterly_notes.json`

## Next Steps — Phase 3 (Analysis)
- Map GitHub PRs to quarterly note deliverables per project; can have unplanned but delivered section for PRs that don't map to a note deliverable
- Flag completed, in-progress, and not-yet-started deliverables
- Prepare 3–5 targeted questions per project for Phase 4 
- PoseInterface deliverables: no need to confirm ownership, include all deliverables
