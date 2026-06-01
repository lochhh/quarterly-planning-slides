#!/usr/bin/env python3
"""Extract GitHub activity for a given author and/or repo(s) and date range via gh CLI.

Usage:
    # Author-filtered activity (PRs, issues, commits):
    uv run python extract_github.py --start YYYY-MM-DD --end YYYY-MM-DD --author lochhh

    # All commits from a specific repo (any author):
    uv run python extract_github.py --start YYYY-MM-DD --end YYYY-MM-DD --repo neuroinformatics-unit/poseinterface

    # Both combined:
    uv run python extract_github.py --start YYYY-MM-DD --end YYYY-MM-DD --author lochhh --repo neuroinformatics-unit/poseinterface

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


def run_gh_paginate(args: list[str]) -> list[dict]:
    """Run gh with --paginate and collect all pages."""
    cmd = ["gh"] + args + ["--paginate"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if not result.stdout.strip():
            return []
        # gh --paginate concatenates JSON arrays; parse each line as array and flatten
        items = []
        for line in result.stdout.strip().splitlines():
            line = line.strip()
            if line:
                parsed = json.loads(line)
                if isinstance(parsed, list):
                    items.extend(parsed)
                else:
                    items.append(parsed)
        return items
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


def extract_author_commits(author: str, start: str, search_end: str) -> list[dict]:
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


def extract_repo_commits(repo: str, start: str, search_end: str, branch: str = "main") -> list[dict]:
    """Fetch all commits to a repo's branch in the date range, any author."""
    raw = run_gh_paginate([
        "api",
        f"repos/{repo}/commits",
        "--method", "GET",
        "-f", f"sha={branch}",
        "-f", f"since={start}T00:00:00Z",
        "-f", f"until={search_end}T23:59:59Z",
        "-F", "per_page=100",
    ])
    return [
        {
            "sha": item["sha"][:7],
            "date": item["commit"]["committer"]["date"],
            "author": item["commit"]["author"]["name"],
            "message": item["commit"]["message"].split("\n")[0],
        }
        for item in raw
    ]


def main():
    parser = argparse.ArgumentParser(description="Extract GitHub activity via gh CLI")
    parser.add_argument("--author", default=None, help="GitHub username for author-filtered extraction (PRs, issues, commits)")
    parser.add_argument("--repo", action="append", dest="repos", metavar="OWNER/REPO",
                        help="Repo to fetch all commits from (any author). Repeatable.")
    parser.add_argument("--branch", default="main", help="Branch for --repo commits (default: main)")
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date YYYY-MM-DD (quarterly planning date)")
    args = parser.parse_args()

    if not args.author and not args.repos:
        parser.error("Provide at least one of --author or --repo")

    end_date = datetime.strptime(args.end, "%Y-%m-%d").date()
    search_end = min(end_date, date.today()).strftime("%Y-%m-%d")

    output: dict = {
        "period": {
            "start": args.start,
            "end": args.end,
            "search_end": search_end,
        }
    }

    if args.author:
        print(f"Extracting activity for author={args.author}: {args.start} -> {search_end}")
        prs = extract_prs(args.author, args.start, search_end)
        issues = extract_issues(args.author, args.start, search_end)
        commits = extract_author_commits(args.author, args.start, search_end)
        output["pull_requests"] = prs
        output["issues"] = issues
        output["commits"] = commits
        print(f"  Found: {len(prs)} PRs, {len(issues)} issues, {len(commits)} commit entries")

    if args.repos:
        repo_commits: dict[str, list[dict]] = {}
        for repo in args.repos:
            print(f"Extracting all commits for {repo} ({args.branch}): {args.start} -> {search_end}")
            repo_commits[repo] = extract_repo_commits(repo, args.start, search_end, args.branch)
            print(f"  Found: {len(repo_commits[repo])} commits")
        output["repo_commits"] = repo_commits

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
