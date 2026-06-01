# Phase 3 — Analysis Phase Handoff

## Deliverable Status by Project

Legend: ✅ Done · 🔄 In Progress · ❓ No GitHub Evidence · ⚠️ Partially Done

---

### Aeon (CH owns all)

| Deliverable | Status | Evidence |
|---|---|---|
| image improvements (dark mode, sizing) | ✅ | PR #246 merged 2026-05-19 |
| rename and redirect sample datasets page | ✅ | PR #235 merged 2026-03-19 |
| ephys pipeline | ✅ | PR #548 → v0.2.0 merged 2026-04-20 |
| use aeon_api pydantic models | ✅ | PR #551 merged 2026-04-21 |
| tests for analysis modules (aeon_api) | 🔄 | PR #82 open (also open: type hints PR #80, PEP 735 PR #84) |
| ARC-DJ (support) | ❓ | 1w allocated; no PRs/commits visible |
| build infrastructure on swc hpc | ❓ | No GitHub evidence (likely HPC ops work) |
| ingest full social data | ❓ | No GitHub evidence (likely operational) |
| aeon_mecha v0.3.0 | ✅ | Released 2026-04-21. Also: v0.4.0 (2026-04-28), v0.4.1 (2026-04-30), v0.4.2 (2026-05-11), v0.4.3 (2026-05-21) — 6 releases total this quarter. Issue #577 (spike sorting scripts) still open. |

**Unplanned but delivered:**
- aeon_docs: strip inline HTML from prev/next nav titles (PR #252)
- aeon_docs: fix broken/redirected URLs (PRs #247, #574)
- aeon_docs: ignore globus.org URLs (PR #238)
- aeon_docs: Aeon email update (PR #236)
- aeon_docs: CI — fetch tags on checkout, concurrency settings (PRs #240, #239)
- aeon_docs: dotnet v8 + docfx v2.78.5 (PR #234)
- aeon_docs: replace commutation translation system SVG (PR #242)
- aeon_docs: pixi+pyproject.toml migration (PR #253, open)
- aeon_mecha: DJ test isolation fixes (PRs #572, #573)
- aeon_mecha: Dependabot config (PR #556)
- aeon_mecha: combine lint+test workflows (PR #550)
- aeon_mecha: reorganise tests + ephys test factories (PR #576)
- aeon_exp_foragingABC: NumPy 2 / Python 3.13 support (PR #70, open)

---

### Movement (CH-owned items only)

| Deliverable | Status | Evidence |
|---|---|---|
| Removing types from docstrings | ⚠️ | PR #885 "Update and add missing docstrings" merged 2026-03-17; PR #976 "User warning" (warnings.warn) merged 2026-05-08. Unclear if the specific "removing types" deliverable is complete. |
| Help COCO keypoints loading PR (#818) get merged | ❓ | No direct PR activity on #818. Issue #1000 "Add support for COCO keypoint results format" is a new open issue. |
| Ruthlessly cut down open PRs | ⚠️ | 7 PRs closed (4 test PRs + 3 closed-not-merged). Scale unclear without PR count before/after. |

**Unplanned but delivered:**
- PEP 695 TypeAliasType workaround (PR #969) + upstream fix merged (tox-dev PR #691)
- sphinx-autodoc-typehints pin follow-up (PR #1016, open)
- PEP 735 dev+docs migration (PR #956)
- Pandas intersphinx URL fix (PR #895)
- Contributor table → responsive grid (PR #954)
- User warnings → `warnings.warn` refactor (PR #976)
- Pre-commit hook: prevent hardcoded website URLs in docs (PR #1010)
- Fork PR review suggestions (ishan372or PR #1, merged 2026-05-27)
- Team meeting presentation (neuroinformatics-unit/documentation PR #314)
- neuroinformatics-unit/actions: 404.html fix (#157), PEP 735 docs group support (#158, #159)
- sphinx-deployment-test: multi-version docs + 404 page setup (PRs #5–#9)
- External upstream: sleap-io empty frame fix merged (talmolab PR #418)

---

### PoseInterface (all team, CH 1.5w allocation)

| Deliverable | Status | Evidence |
|---|---|---|
| Extract clips and corresponding cliplabels.json | ✅ | sfmig commit #2e72f28 "Convert predictions to cliplabels.json using movement (#45)" |
| Utilities to extract clip(s) from video | ✅ | sfmig commit #42ac536 "Format videos + extract clip function (#39)" |
| Convert SLEAP/DLC predictions to COCO.json | ⚠️ | CH commit #2881508 "Refactor annotations_to_coco (#26)"; Niko DLC benchmark example (#49). Functional but unclear if fully complete. |
| Upload 2 sessions from SWC (1 train / 1 test) | ❓ | No GitHub evidence |
| Clarify relationship / scope with ethology | ⚠️ | ethology PEP 735 PR #156 open (movement→ethology migration); scope may be clearer now but not documented in visible PRs |

**Unplanned but delivered (CH):**
- Makefile standardisation (PR #35)
- PEP 735 migration (PR #46)
- sleap-io pin ≥0.7.1 (PR #55) — unblocked COCO pipeline after upstream fix merged

---

## Gaps / Unclear Ownership

| Gap | Project | Notes |
|---|---|---|
| ARC-DJ build infrastructure on SWC HPC | Aeon | No GitHub PRs; likely ops/HPC work. Confirm status. |
| Ingest full social data | Aeon | Same — may be tracked outside GitHub. |
| aeon_mecha v0.4.x | Aeon | v0.3.0–v0.4.3 all released this quarter (unplanned beyond v0.3.0). What drove v0.4.x? |
| COCO keypoints loading PR #818 | Movement | Was this actively helped/reviewed? |
| PR reduction | Movement | Total open PRs before vs. after unclear. |
| "Removing types from docstrings" | Movement | Does PR #885 complete this or is more remaining? |
| Upload SWC sessions | PoseInterface | Status unknown; may be data/storage work. |
| Ethology scope clarification | PoseInterface | Written down anywhere? Verbal agreement? |

---

## Questions for Phase 4

### Aeon
1. ARC-DJ / HPC: Any progress on build infrastructure + social data ingestion, or deferred?
2. aeon_mecha shipped v0.2.0–v0.4.3 (6 releases). What drove v0.4.x beyond the planned v0.3.0? Spike sorting scripts (#577) in scope for next quarter?
3. aeon_api tests (PR #82): Blocking anything, or carries into next quarter?

### Movement
4. COCO PR #818: Did you actively review/push it, or hand off? New issue #1000 — related or separate?
5. "Removing types from docstrings": Is PR #885 the completion of this, or is more work pending?
6. PR reduction: What was the open PR count at quarter start vs. now?

### PoseInterface
7. Upload 2 SWC sessions: Done, in progress, or blocked?
8. Ethology scope: Was relationship clarified (write-up, discussion, decision)? What was decided?

---

## Next Steps — Phase 4 (Inquiry)
- Present 3–5 questions per project (see above)
- Wait for user responses before proceeding to Phase 5
