#!/usr/bin/env python3
"""Fetch and parse NIU quarterly planning notes from GitHub.

Finds the notes file closest to the given start date, extracts deliverables
for Aeon, Movement, and PoseInterface from both the "last quarter" and
"next quarter" sections, and tags each deliverable by assignee.

Assignment rules:
  - Aeon: all deliverables belong to CH (no other assignees in those sections)
  - Movement / PoseInterface: items under "CH:" subsection, "All:" subsection,
    or with inline "(CH)" marker belong to CH; others are "other"
  - Also parses "Personal time allocation" > "CH" table for commitment data

Usage:
    python parse_quarterly_notes.py --start YYYY-MM-DD

Output:
    .claude/handoff/quarterly_notes.json
"""

import argparse
import base64
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = "neuroinformatics-unit/documentation"
NOTES_PATH = "minutes/quarterly_planning"
PROJECTS = ["Aeon", "Movement", "PoseInterface"]

# For these projects every deliverable belongs to CH
CH_OWNED_PROJECTS = {"Aeon"}

# Inline CH marker: "(CH)" or leading "CH:" on the bullet text
CH_INLINE_RE = re.compile(r"\(CH\)|\bCH\s*:", re.IGNORECASE)

# Subsection header patterns (bare line, e.g. "CH:", "NS primary:", "All:")
PERSON_SUBSECTION_RE = re.compile(
    r"^([A-Z]{2,3})(\s+(primary|stretch|secondary|other))?\s*:?\s*$"
)
ALL_SUBSECTION_RE = re.compile(r"^all\s*:?\s*$", re.IGNORECASE)

OUTPUT_PATH = Path(".claude/handoff/quarterly_notes.json")


def run_gh_api(endpoint: str) -> dict | list:
    cmd = ["gh", "api", endpoint]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except FileNotFoundError:
        print("Error: gh CLI not found.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: gh api {endpoint}: {e.stderr}", file=sys.stderr)
        sys.exit(2)


def find_closest_file(start_date: datetime.date) -> tuple[str, datetime.date]:
    contents = run_gh_api(f"repos/{REPO}/contents/{NOTES_PATH}")
    candidates = []
    for item in contents:
        name = item["name"]
        if re.match(r"^\d{4}-\d{2}-\d{2}\.md$", name):
            try:
                file_date = datetime.strptime(name[:10], "%Y-%m-%d").date()
                candidates.append((file_date, name))
            except ValueError:
                continue

    if not candidates:
        print("Error: no dated quarterly notes files found.", file=sys.stderr)
        sys.exit(1)

    candidates.sort(key=lambda x: (abs((x[0] - start_date).days), x[0]))
    return candidates[0][1], candidates[0][0]


def fetch_file_content(filename: str) -> str:
    data = run_gh_api(f"repos/{REPO}/contents/{NOTES_PATH}/{filename}")
    return base64.b64decode(data["content"]).decode("utf-8")


def find_top_section_bounds(lines: list[str], keyword: str) -> tuple[int, int]:
    """Find bounds of a top-level (##) section containing keyword."""
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+", line) and keyword.lower() in line.lower():
            start = i
            break
    if start is None:
        return -1, -1
    for j in range(start + 1, len(lines)):
        if re.match(r"^##\s+", lines[j]):
            return start, j
    return start, len(lines)


def find_project_bounds_within(
    lines: list[str], project: str, section_start: int, section_end: int
) -> tuple[int, int]:
    """Find the subsection for a project within a given line range."""
    # Aliases: PoseInterface → also match "pose interface"
    aliases = [project.lower()]
    if project.lower() == "poseinterface":
        aliases.append("pose interface")

    heading_re = re.compile(r"^#{2,4}\s+")
    start = None
    for i in range(section_start, section_end):
        line_lower = lines[i].lower()
        if heading_re.match(lines[i]) and any(a in line_lower for a in aliases):
            start = i
            break
    if start is None:
        return -1, -1

    level = len(re.match(r"^(#+)", lines[start]).group(1))
    for j in range(start + 1, section_end):
        m = re.match(r"^(#+)\s+", lines[j])
        if m and len(m.group(1)) <= level:
            return start, j
    return start, section_end


def assign_deliverable(text: str, current_owner: str, project: str) -> str:
    """Return 'ch', 'other', or 'unassigned' for a deliverable line."""
    if project in CH_OWNED_PROJECTS:
        return "ch"
    if CH_INLINE_RE.search(text):
        return "ch"
    if current_owner == "ch":
        return "ch"
    if current_owner == "all":
        return "ch"
    if current_owner == "other":
        return "other"
    return "unassigned"


def extract_deliverables(
    lines: list[str], start: int, end: int, project: str
) -> list[dict]:
    """Extract deliverable bullets from lines[start:end], subsection-aware."""
    deliverables = []
    current_owner = "unassigned"

    for line in lines[start:end]:
        stripped = line.strip()

        # Detect person subsection header (e.g. "CH:", "NS primary:", "All:")
        if ALL_SUBSECTION_RE.match(stripped):
            current_owner = "all"
            continue
        m = PERSON_SUBSECTION_RE.match(stripped)
        if m:
            initials = m.group(1).upper()
            current_owner = "ch" if initials == "CH" else "other"
            continue

        if stripped.startswith(("-", "*", "+")):
            text = stripped.lstrip("-*+ ").strip()
            if text:
                assigned = assign_deliverable(text, current_owner, project)
                deliverables.append({
                    "text": text,
                    "assigned": assigned,
                    "raw": stripped,
                })

    return deliverables


def extract_ch_time_allocation(lines: list[str]) -> dict:
    """Parse the Personal time allocation > CH markdown table."""
    ch_start = None
    for i, line in enumerate(lines):
        if re.match(r"^###\s+CH\s*$", line.strip()):
            ch_start = i
            break
    if ch_start is None:
        return {}

    allocations = {}
    skip_header = True
    for line in lines[ch_start + 1:]:
        stripped = line.strip()
        # Stop at next section heading (### or higher level)
        if re.match(r"^#{2,3}\s+", stripped):
            break
        if not stripped.startswith("|"):
            continue
        cells = [c.strip().strip("*") for c in stripped.split("|")[1:-1]]
        if len(cells) < 4:
            continue
        project_name = cells[0]
        if not project_name or set(project_name) <= {"-", " "}:
            continue
        if project_name.lower() == "projects":
            skip_header = False
            continue
        if skip_header:
            skip_header = False
            continue
        commitment_next = cells[3] if len(cells) > 3 else ""
        notes = cells[4] if len(cells) > 4 else ""
        allocations[project_name] = {
            "commitment_next_quarter": commitment_next,
            "notes": notes,
        }

    return allocations


def parse_notes(content: str) -> dict:
    lines = content.splitlines()

    next_q_start, next_q_end = find_top_section_bounds(lines, "next quarter")

    projects_data = {}
    all_unassigned = []

    for project in PROJECTS:
        deliverables = []

        if next_q_start != -1:
            ps, pe = find_project_bounds_within(
                lines, project, next_q_start, next_q_end
            )
            if ps != -1:
                deliverables = extract_deliverables(lines, ps, pe, project)

        projects_data[project] = {"deliverables": deliverables}

        for d in deliverables:
            if d["assigned"] == "unassigned":
                all_unassigned.append({"project": project, "text": d["text"]})

    ch_allocation = extract_ch_time_allocation(lines)

    return {
        "projects": projects_data,
        "ch_time_allocation": ch_allocation,
        "unassigned_deliverables": all_unassigned,
    }


def main():
    parser = argparse.ArgumentParser(description="Parse NIU quarterly planning notes")
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    args = parser.parse_args()

    start_date = datetime.strptime(args.start, "%Y-%m-%d").date()

    print(f"Finding quarterly notes closest to {args.start}...")
    filename, notes_date = find_closest_file(start_date)
    print(f"Using: {filename}")

    content = fetch_file_content(filename)
    parsed = parse_notes(content)

    output = {
        "notes_date": notes_date.strftime("%Y-%m-%d"),
        "source_file": filename,
        **parsed,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")

    for project in PROJECTS:
        p = parsed["projects"][project]
        ch_count = sum(1 for x in p["deliverables"] if x["assigned"] == "ch")
        print(f"  {project}: {len(p['deliverables'])} deliverables ({ch_count} CH)")
    print(f"  Unassigned: {len(parsed['unassigned_deliverables'])} items flagged")
    if parsed["ch_time_allocation"]:
        print("  CH time allocation:")
        for proj, alloc in parsed["ch_time_allocation"].items():
            print(f"    {proj}: {alloc['commitment_next_quarter']}")
    print(f"Written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
