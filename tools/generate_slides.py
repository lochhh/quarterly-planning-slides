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


MAX_VISUAL_LINES = 6


def _visual_weight(line: str) -> int:
    """Estimate display lines: blank=0, long line=2, else 1."""
    stripped = line.strip()
    if not stripped:
        return 0
    return 2 if len(stripped) > 80 else 1


def _find_header_end(lines: list[str]) -> int:
    """Index of first top-level bullet line (start of content)."""
    for i, line in enumerate(lines):
        if line.startswith("- "):
            return i
    return len(lines)


def split_subslide(text: str, max_lines: int = MAX_VISUAL_LINES) -> list[str]:
    """Split a subslide's content if it exceeds max_lines, no repeated headers."""
    lines = text.split("\n")
    header_end = _find_header_end(lines)
    header = lines[:header_end]
    content = lines[header_end:]

    if sum(_visual_weight(l) for l in content) <= max_lines:
        return [text]

    chunks: list[list[str]] = []
    current: list[str] = []
    visual = 0

    for line in content:
        w = _visual_weight(line)
        if visual + w > max_lines and current:
            # Don't break mid-group: if next line is indented, back up to last top-level bullet
            if line.startswith("  -"):
                # find last top-level bullet in current and split there
                split_at = next(
                    (j for j in range(len(current) - 1, -1, -1) if current[j].startswith("- ")),
                    None,
                )
                if split_at is not None:
                    chunks.append(current[:split_at])
                    current = current[split_at:]
                    visual = sum(_visual_weight(l) for l in current)
                else:
                    chunks.append(current)
                    current = []
                    visual = 0
            else:
                # 6th line is a top-level bullet — move to next slide
                chunks.append(current)
                current = []
                visual = 0
        current.append(line)
        visual += w

    if current:
        chunks.append(current)

    result = []
    for i, chunk in enumerate(chunks):
        slide_lines = (header + chunk) if i == 0 else chunk
        result.append("\n".join(slide_lines))
    return result


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


def build_project_slides(project: str, quarterly: dict, github: dict, qa: dict) -> list[str]:
    """Return a list of subslide strings for a project (joined with ---- by caller)."""
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

    subslides = []

    if ch_deliverables:
        lines = [f"## Last Quarter — {project}\n", "**Planned**\n"]
        in_group = False
        for d in ch_deliverables:
            text = d["text"]
            is_group_header = text.strip().startswith("`") or strip_md(text).startswith("ARC-DJ")
            plain = strip_md(text).lower()
            matched_status = ""
            for key, val in status_map.items():
                key_plain = strip_md(key).lower()
                if key_plain[:40] in plain or plain[:40] in key_plain:
                    matched_status = val
                    break
            emoji = STATUS_EMOJI.get(matched_status, "")
            prefix = f"{emoji} " if emoji else ""
            display = strip_md(text) if not is_group_header else text
            if is_group_header:
                lines.append(f"- {display}")
                in_group = True
            else:
                indent = "  " if in_group else ""
                lines.append(f"{indent}- {prefix}{display}")
        subslides.extend(split_subslide("\n".join(lines)))

    if unplanned:
        lines = ["**Unplanned**\n"]
        current_group = None
        for item in unplanned:
            if ": " in item:
                group, _, detail = item.partition(": ")
                if group != current_group:
                    label = f"`{group}`" if ("_" in group or "/" in group) else group
                    lines.append(f"- {label}")
                    current_group = group
                lines.append(f"  - {detail}")
            else:
                current_group = None
                lines.append(f"- {item}")
        subslides.extend(split_subslide("\n".join(lines)))

    if carry_overs:
        lines = ["**Carry-overs / in progress**\n"]
        for item in carry_overs:
            lines.append(f"- 🔄 {item}")
        subslides.extend(split_subslide("\n".join(lines)))

    return subslides



def build_next_quarter_slide(project: str, qa: dict) -> str | None:
    proj_qa = qa["projects"].get(project, {})
    priorities = proj_qa.get("priorities", [])
    if not priorities:
        return None
    lines = [f"## Next Quarter — {project}\n"]
    for p in priorities:
        lines.append(f"- {p}")
    extra = proj_qa.get("extra_notes", "").strip()
    if extra:
        lines.append(f"\n_{extra}_")
    return "\n".join(lines)


def render(github: dict, quarterly: dict, qa: dict, meeting_date: str | None = None) -> str:
    end_date = github["period"]["end"]
    title_date = meeting_date or end_date
    sections = []

    sections.append(build_title_slide(title_date))

    for project in PROJECTS:
        subslides = build_project_slides(project, quarterly, github, qa)
        next_q = build_next_quarter_slide(project, qa)
        if next_q:
            subslides.append(next_q)
        if subslides:
            sections.append("\n\n----\n\n".join(subslides))

    body = "\n\n---\n\n".join(sections)
    return f"{FRONTMATTER}\n\n{body}\n"


def main():
    parser = argparse.ArgumentParser(description="Generate HackMD reveal.js slide deck")
    parser.add_argument("--github-data", default=".claude/handoff/github_activity.json")
    parser.add_argument("--quarterly-data", default=".claude/handoff/quarterly_notes.json")
    parser.add_argument("--qa-data", default=".claude/handoff/qa_answers.json")
    parser.add_argument("--output", default=None, help="Output path (derived from end date if omitted)")
    parser.add_argument("--meeting-date", default=None, help="Date shown on title slide YYYY-MM-DD (defaults to end date)")
    args = parser.parse_args()

    github = json.loads(Path(args.github_data).read_text(encoding="utf-8"))
    quarterly = json.loads(Path(args.quarterly_data).read_text(encoding="utf-8"))
    qa = json.loads(Path(args.qa_data).read_text(encoding="utf-8"))

    end_date = github["period"]["end"]
    file_date = args.meeting_date or end_date
    output_path = Path(args.output) if args.output else Path(f"deliverables/slides-{file_date}.md")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render(github, quarterly, qa, args.meeting_date), encoding="utf-8")
    print(f"Slides written to {output_path}")


if __name__ == "__main__":
    main()
