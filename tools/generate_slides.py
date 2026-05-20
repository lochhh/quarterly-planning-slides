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

PROJECTS = ["Aeon", "Movement", "PoseInterface"]

FRONTMATTER = """\
---
slideOptions:
  transition: slide
  tags: NIU_team-meeting
---\
"""


def fmt_date(iso: str) -> str:
    """Convert YYYY-MM-DD to dd.mm.yyyy."""
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%d.%m.%Y")


def build_title_slide(end_date: str) -> str:
    return f"# NIU Quarterly Planning\n\n{fmt_date(end_date)}\n\nChang Huan Lo"


def build_overview_slide(quarterly: dict, github: dict) -> str:
    lines = ["## Projects Overview\n"]
    for project in PROJECTS:
        proj_data = quarterly["projects"].get(project, {})
        deliverables = proj_data.get("deliverables", [])
        ch_deliverables = [d for d in deliverables if d["assigned"] == "ch"]

        prs = [pr for pr in github["pull_requests"] if project.lower() in pr["repo"].lower()]
        issues = [i for i in github["issues"] if project.lower() in i["repo"].lower()]

        desc_parts = []
        if ch_deliverables:
            desc_parts.append(f"{len(ch_deliverables)} planned deliverable(s)")
        if prs:
            desc_parts.append(f"{len(prs)} PR(s)")
        if issues:
            desc_parts.append(f"{len(issues)} issue(s)")

        summary = ", ".join(desc_parts) if desc_parts else "ongoing contributions"
        lines.append(f"**{project}** — {summary}")

    return "\n".join(lines)


def build_deliverables_slides(quarterly: dict, github: dict) -> list[str]:
    slides = []
    for project in PROJECTS:
        proj_data = quarterly["projects"].get(project, {})
        ch_deliverables = [d for d in proj_data.get("deliverables", []) if d["assigned"] == "ch"]
        prs = [pr for pr in github["pull_requests"] if project.lower() in pr["repo"].lower()]
        issues = [i for i in github["issues"] if project.lower() in i["repo"].lower()]

        if not ch_deliverables and not prs and not issues:
            continue

        lines = [f"## Last Quarter — {project}\n"]

        if ch_deliverables:
            lines.append("**Planned**\n")
            for d in ch_deliverables:
                lines.append(f"- {d['text']}")
            lines.append("")

        unplanned_prs = [
            pr for pr in prs
            if not any(d["text"].lower()[:30] in pr["title"].lower() for d in ch_deliverables)
        ]
        if unplanned_prs:
            lines.append("**Unplanned / additional**\n")
            for pr in unplanned_prs[:5]:
                state = "merged" if pr.get("merged_at") else pr["state"]
                lines.append(f"- [{pr['title']}]({pr['url']}) ({state})")

        slides.append("\n".join(lines))
    return slides


def build_lessons_slides(qa: dict) -> list[str]:
    slides = []
    for project in PROJECTS:
        proj_qa = qa["projects"].get(project, {})
        lessons = proj_qa.get("lessons_learned", [])
        if not lessons:
            continue
        lines = [f"## Lessons Learned — {project}\n"]
        for lesson in lessons:
            lines.append(f"- {lesson}")
        slides.append("\n".join(lines))
    return slides


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
            lines.append(f"\nNote: {extra}")
        slides.append("\n".join(lines))
    return slides


def render(github: dict, quarterly: dict, qa: dict) -> str:
    end_date = github["period"]["end"]
    sections = []

    sections.append(build_title_slide(end_date))

    overview = build_overview_slide(quarterly, github)
    sections.append(overview)

    deliverable_slides = build_deliverables_slides(quarterly, github)
    if deliverable_slides:
        sections.append("\n\n----\n\n".join(deliverable_slides))

    lesson_slides = build_lessons_slides(qa)
    if lesson_slides:
        sections.append("\n\n----\n\n".join(lesson_slides))

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
