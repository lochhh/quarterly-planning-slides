#!/usr/bin/env python3
"""Generate a HackMD reveal.js slide deck from extracted GitHub + quarterly notes + Q&A data.

Usage:
    python generate_slides.py \\
        --github-data .claude/handoff/github_activity.json \\
        --quarterly-data .claude/handoff/quarterly_notes.json \\
        --qa-data .claude/handoff/qa_answers.json \\
        --output deliverables/slides-YYYY-MM-DD.md

The --output path is derived from the end date in github_activity.json if omitted.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

PROJECTS = ["Aeon", "PoseInterface"]

STATUS_EMOJI = {
    "done": "✅",
    "in_progress": "🔄",
    "partial": "⚠️",
    "not_done": "❌",
    "no_evidence": "❓",
}

FRONTMATTER = """\
---
slideOptions:
  transition: slide
  tags: NIU_team-meeting
---\
"""


import re


def fmt_date(iso: str) -> str:
    """Convert YYYY-MM-DD to dd.mm.yyyy."""
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%d.%m.%Y")


def strip_md(text: str) -> str:
    """Strip markdown links and bold/italic markers for plain comparison/display."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # [label](url) → label
    text = re.sub(r"\*+", "", text)                         # **bold** / *italic*
    return text.strip()


def build_title_slide(end_date: str) -> str:
    return f"# NIU Quarterly Planning\n\n{fmt_date(end_date)}\n\nChang Huan Lo"


def build_time_allocation_slide(quarterly: dict) -> str:
    alloc = quarterly.get("ch_time_allocation", {})
    lines = ["## Time Allocation\n"]
    for project, info in alloc.items():
        commitment = info.get("commitment_next_quarter", "-")
        if commitment and commitment != "-":
            lines.append(f"- **{project}**: {commitment}")
    return "\n".join(lines)


def build_project_slide(project: str, quarterly: dict, github: dict, qa: dict) -> str:
    proj_data = quarterly["projects"].get(project, {})
    all_deliverables = proj_data.get("deliverables", [])

    # Include CH-owned + unassigned (PoseInterface has no CH markers)
    ch_deliverables = [
        d for d in all_deliverables
        if d["assigned"] in ("ch", "unassigned")
    ]

    proj_qa = qa["projects"].get(project, {})
    status_map = proj_qa.get("deliverable_status", {})
    unplanned = proj_qa.get("unplanned", [])
    carry_overs = proj_qa.get("carry_overs", [])

    lines = [f"## Last Quarter — {project}\n"]

    if ch_deliverables:
        lines.append("**Planned**\n")
        for d in ch_deliverables:
            text = d["text"]
            plain = strip_md(text).lower()
            matched_status = ""
            for key, val in status_map.items():
                key_plain = strip_md(key).lower()
                if key_plain[:40] in plain or plain[:40] in key_plain:
                    matched_status = val
                    break
            emoji = STATUS_EMOJI.get(matched_status, "")
            prefix = f"{emoji} " if emoji else ""
            lines.append(f"- {prefix}{strip_md(text)}")
        lines.append("")

    if unplanned:
        lines.append("**Unplanned / additional**\n")
        for item in unplanned:
            lines.append(f"- {item}")
        lines.append("")

    if carry_overs:
        lines.append("**Carry-overs / in progress**\n")
        for item in carry_overs:
            lines.append(f"- 🔄 {item}")

    return "\n".join(lines)


def build_priorities_slides(qa: dict) -> list[str]:
    slides = []
    for project in PROJECTS:
        proj_qa = qa["projects"].get(project, {})
        priorities = proj_qa.get("priorities", [])
        if not priorities:
            continue
        lines = [f"## Next Quarter — {project}\n"]
        for p in priorities:
            lines.append(f"- {p}")
        extra = proj_qa.get("extra_notes", "").strip()
        if extra:
            lines.append(f"\n_{extra}_")
        slides.append("\n".join(lines))
    return slides


def render(github: dict, quarterly: dict, qa: dict) -> str:
    end_date = github["period"]["end"]
    sections = []

    sections.append(build_title_slide(end_date))
    sections.append(build_time_allocation_slide(quarterly))

    for project in PROJECTS:
        sections.append(build_project_slide(project, quarterly, github, qa))

    priority_slides = build_priorities_slides(qa)
    if priority_slides:
        sections.append("\n\n----\n\n".join(priority_slides))

    body = "\n\n---\n\n".join(sections)
    return f"{FRONTMATTER}\n\n{body}\n"


def main():
    parser = argparse.ArgumentParser(description="Generate HackMD reveal.js slide deck")
    parser.add_argument("--github-data", default=".claude/handoff/github_activity.json")
    parser.add_argument("--quarterly-data", default=".claude/handoff/quarterly_notes.json")
    parser.add_argument("--qa-data", default=".claude/handoff/qa_answers.json")
    parser.add_argument("--output", default=None, help="Output path (derived from end date if omitted)")
    args = parser.parse_args()

    github = json.loads(Path(args.github_data).read_text(encoding="utf-8"))
    quarterly = json.loads(Path(args.quarterly_data).read_text(encoding="utf-8"))
    qa = json.loads(Path(args.qa_data).read_text(encoding="utf-8"))

    end_date = github["period"]["end"]
    output_path = Path(args.output) if args.output else Path(f"deliverables/slides-{end_date}.md")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render(github, quarterly, qa), encoding="utf-8")
    print(f"Slides written to {output_path}")


if __name__ == "__main__":
    main()
