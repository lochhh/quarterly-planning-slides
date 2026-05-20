# Phase 2 — Extraction Phase Handoff

## Period
2026-03-03 to 2026-06-02 (search up to 2026-05-20, today's date)

## GitHub Activity Summary
- **54 PRs**, **21 issues**, **32 commit entries** extracted

### Aeon (SainsburyWellcomeCentre)
**aeon_docs** — 10 PRs (8 merged, 1 open, 1 closed-not-merged)
- SVG rendering improvements (dark/light mode)
- Pixi + pyproject.toml migration (open)
- URL fixes (redirected/broken), Aeon email, sample datasets rename
- CI: concurrency settings, fetch tags fix, docfx v2.78.5 / dotnet v8

**aeon_mecha** — 8 PRs (6 merged, 1 closed, 1 open)
- Ephys pipeline (v0.2.0)
- Pydantic metadata migration (from DotMap)
- DataJoint 0.14.x → 2.x upgrade
- CI: combine lint+test workflows, Dependabot, DJ test isolation fixes

**aeon_api** — 5 PRs (1 merged, 4 open)
- Unit tests for analysis modules
- Type hints + Google docstrings
- PEP 735 dependency groups (open)
- Codecov investigation

**aeon_exp_foragingABC** — 1 PR (open)
- NumPy 2 / Python 3.13 support

### Movement (neuroinformatics-unit/movement)
**9 PRs** (6 merged, 3 closed-not-merged)
- PEP 735 dependency groups migration
- PEP 695 TypeAliasType rendering fix (+ upstream sphinx-autodoc-typehints fix merged)
- User warnings refactor (warnings.warn)
- Contributor table: fixed → responsive grid
- Team meeting presentation added
- Codecov testing (closed)

### PoseInterface (neuroinformatics-unit/poseinterface)
**3 PRs** (2 merged, 1 closed-not-merged)
- PEP 735 migration
- Makefile standardisation

### Cross-project (neuroinformatics-unit/actions)
**3 PRs** (3 merged)
- 404.html fix for multiversion Sphinx docs
- PEP 735 docs group support + fallback

### External upstream (tox-dev/sphinx-autodoc-typehints, talmolab/sleap-io)
- sphinx-autodoc-typehints: PEP 695 TypeAliasType fix — **merged upstream**
- sleap-io: empty frame handling fix — open PR

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

## Files Produced
- `.claude/handoff/github_activity.json`
- `.claude/handoff/quarterly_notes.json`

## Next Steps — Phase 3 (Analysis)
- Map GitHub PRs to quarterly note deliverables per project
- Flag completed, in-progress, and not-yet-started deliverables
- Prepare 3–5 targeted questions per project for Phase 4 (incl. 5 PoseInterface ownership confirmations)
