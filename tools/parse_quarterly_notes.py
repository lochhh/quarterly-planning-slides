#!/usr/bin/env python3
"""Fetch and parse NIU quarterly planning notes from GitHub.

Finds the notes file closest to the given start date, extracts deliverables
for Aeon, Movement, and PoseInterface, and tags each by assignee.

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
CH_PATTERNS = re.compile(r"\bCH\b|Chang Huan", re.IGNORECASE)
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

    # Pick file with date closest to start_date; prefer earlier on tie
    candidates.sort(key=lambda x: (abs((x[0] - start_date).days), x[0]))
    return candidates[0][1], candidates[0][0]


def fetch_file_content(filename: str) -> str:
    data = run_gh_api(f"repos/{REPO}/contents/{NOTES_PATH}/{filename}")
    return base64.b64decode(data["content"]).decode("utf-8")


def find_section_bounds(lines: list[str], project: str) -> tuple[int, int]:
    """Return (start_idx, end_idx) of the section containing the project keyword."""
    heading_re = re.compile(r"^#{1,3}\s+", re.IGNORECASE)
    start = None
    for i, line in enumerate(lines):
        if project.lower() in line.lower() and heading_re.match(line):
            start = i
            break

    if start is None:
        return -1, -1

    # Section ends at next same-or-higher-level heading
    level = len(re.match(r"^(#+)", lines[start]).group(1))
    for j in range(start + 1, len(lines)):
        m = re.match(r"^(#+)\s+", lines[j])
        if m and len(m.group(1)) <= level:
            return start, j
    return start, len(lines)


def classify_assignee(text: str) -> str:
    if CH_PATTERNS.search(text):
        return "ch"
    # Heuristic: parenthetical or trailing initials suggest assigned-to-other
    if re.search(r"\b[A-Z]{2,3}\b", text):
        return "other"
    return "unassigned"


def extract_deliverables(lines: list[str]) -> list[dict]:
    deliverables = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("-", "*", "+")):
            text = stripped.lstrip("-*+ ").strip()
            if text:
                deliverables.append({
                    "text": text,
                    "assigned": classify_assignee(text),
                    "raw": stripped,
                })
    return deliverables


def parse_notes(content: str) -> dict:
    lines = content.splitlines()
    projects_data = {}
    unassigned = []

    for project in PROJECTS:
        start, end = find_section_bounds(lines, project)
        if start == -1:
            projects_data[project] = {"deliverables": [], "mentions": []}
            continue

        section_lines = lines[start:end]
        deliverables = extract_deliverables(section_lines)

        # Collect lines mentioning CH/Chang Huan anywhere in section
        mentions = [l.strip() for l in section_lines if CH_PATTERNS.search(l)]

        projects_data[project] = {"deliverables": deliverables, "mentions": mentions}

        for d in deliverables:
            if d["assigned"] == "unassigned":
                unassigned.append({"project": project, "text": d["text"]})

    return {"projects": projects_data, "unassigned_deliverables": unassigned}


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
        d = parsed["projects"][project]["deliverables"]
        ch_count = sum(1 for x in d if x["assigned"] == "ch")
        print(f"  {project}: {len(d)} deliverables ({ch_count} assigned to CH)")
    print(f"  Unassigned: {len(parsed['unassigned_deliverables'])} items flagged for confirmation")
    print(f"Written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
