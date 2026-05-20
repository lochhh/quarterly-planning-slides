#!/usr/bin/env python3
"""Extract GitHub activity for a given author and date range via gh CLI.

Usage:
    python extract_github.py --start YYYY-MM-DD --end YYYY-MM-DD [--author lochhh]

Output:
    .claude/handoff/github_activity.json
"""

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

EXCLUDED_REPOS = {"e-babylab", "claude-code-slides", "quarterly-planning-slides"}
OUTPUT_PATH = Path(".claude/handoff/github_activity.json")


def run_gh(args: list[str]) -> list[dict]:
    cmd = ["gh"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout) if result.stdout.strip() else []
    except FileNotFoundError:
        print("Error: gh CLI not found. Install from https://cli.github.com", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running gh: {e.stderr}", file=sys.stderr)
        sys.exit(2)


def is_excluded(repo_name: str) -> bool:
    name_lower = repo_name.lower()
    return any(excl in name_lower for excl in EXCLUDED_REPOS)


def extract_prs(author: str, start: str, search_end: str) -> list[dict]:
    raw = run_gh([
        "search", "prs",
        "--author", author,
        "--created", f"{start}..{search_end}",
        "--json", "title,repository,url,state,closedAt,body",
        "--limit", "200",
    ])
    return [
        {
            "title": item["title"],
            "repo": item["repository"]["nameWithOwner"],
            "url": item["url"],
            "state": item["state"],
            "merged_at": item.get("closedAt"),
            "body": (item.get("body") or "")[:500],
        }
        for item in raw
        if not is_excluded(item["repository"]["nameWithOwner"])
    ]


def extract_issues(author: str, start: str, search_end: str) -> list[dict]:
    raw = run_gh([
        "search", "issues",
        "--author", author,
        "--created", f"{start}..{search_end}",
        "--json", "title,repository,url,state,closedAt",
        "--limit", "200",
    ])
    return [
        {
            "title": item["title"],
            "repo": item["repository"]["nameWithOwner"],
            "url": item["url"],
            "state": item["state"],
            "closed_at": item.get("closedAt"),
        }
        for item in raw
        if not is_excluded(item["repository"]["nameWithOwner"])
    ]


def extract_commits(author: str, start: str, search_end: str) -> list[dict]:
    """Fetch commits authored by the user in the date range via GraphQL."""
    query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      commitContributionsByRepository(maxRepositories: 100) {
        repository {
          nameWithOwner
        }
        contributions(first: 100) {
          nodes {
            commitCount
            occurredAt
          }
        }
      }
    }
  }
}
"""
    variables = {
        "login": author,
        "from": f"{start}T00:00:00Z",
        "to": f"{search_end}T23:59:59Z",
    }
    payload = json.dumps({"query": query, "variables": variables})
    cmd = ["gh", "api", "graphql", "--input", "-"]
    try:
        result = subprocess.run(
            cmd, input=payload, capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)
    except FileNotFoundError:
        print("Error: gh CLI not found.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running gh graphql: {e.stderr}", file=sys.stderr)
        sys.exit(2)

    commits = []
    repos = (
        data.get("data", {})
        .get("user", {})
        .get("contributionsCollection", {})
        .get("commitContributionsByRepository", [])
    )
    for repo_entry in repos:
        repo_name = repo_entry["repository"]["nameWithOwner"]
        if is_excluded(repo_name):
            continue
        for node in repo_entry["contributions"]["nodes"]:
            commits.append({
                "repo": repo_name,
                "commit_count": node["commitCount"],
                "date": node["occurredAt"],
            })
    return commits


def main():
    parser = argparse.ArgumentParser(description="Extract GitHub activity via gh CLI")
    parser.add_argument("--author", default="lochhh")
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date YYYY-MM-DD (quarterly planning date)")
    args = parser.parse_args()

    end_date = datetime.strptime(args.end, "%Y-%m-%d").date()
    search_end = min(end_date, date.today()).strftime("%Y-%m-%d")

    print(f"Extracting GitHub activity for {args.author}: {args.start} -> {args.end} (search up to {search_end})")

    prs = extract_prs(args.author, args.start, search_end)
    issues = extract_issues(args.author, args.start, search_end)
    commits = extract_commits(args.author, args.start, search_end)

    output = {
        "period": {
            "start": args.start,
            "end": args.end,
            "search_end": search_end,
        },
        "pull_requests": prs,
        "issues": issues,
        "commits": commits,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(f"Found: {len(prs)} PRs, {len(issues)} issues, {len(commits)} commit entries")
    print(f"Written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
