#!/usr/bin/env python3
"""Push a local file to a HackMD note.

Usage:
    python sync_hackmd.py <local_file> <note_id>          # update existing note
    python sync_hackmd.py <local_file> --create           # create new note, prints URL
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path


def _load_dotenv() -> None:
    """Load .env walking up from cwd, stopping at repo root (.git)."""
    for candidate in [Path.cwd(), *Path.cwd().parents]:
        if (candidate / ".env").exists():
            for line in (candidate / ".env").read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    os.environ.setdefault(key.strip(), val.strip())
            return
        if (candidate / ".git").exists():
            return  # reached repo root without finding .env


def main():
    _load_dotenv()
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <local_file> <note_id|--create>", file=sys.stderr)
        sys.exit(1)

    local_file, target = sys.argv[1], sys.argv[2]

    token = os.environ.get("HACKMD_API_TOKEN")
    if not token:
        print("Error: HACKMD_API_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    content = Path(local_file).read_text(encoding="utf-8")

    if target == "--create":
        _create_note(token, content, Path(local_file).stem)
    else:
        _update_note(token, content, target)


def _update_note(token: str, content: str, note_id: str) -> None:
    payload = json.dumps({"content": content}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.hackmd.io/v1/notes/{note_id}",
        data=payload,
        method="PATCH",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Updated note {note_id} (HTTP {resp.status})")
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} — {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def _create_note(token: str, content: str, title: str) -> None:
    payload = json.dumps({
        "content": content,
        "readPermission": "owner",
        "writePermission": "owner",
        "commentPermission": "disabled",
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.hackmd.io/v1/notes",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            note_id = data["id"]
            note_url = data.get("publishLink") or f"https://hackmd.io/{note_id}"
            print(f"Created note: {note_url}")
            print(f"Note ID: {note_id}")
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} — {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
