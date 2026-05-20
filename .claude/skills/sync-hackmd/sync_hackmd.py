#!/usr/bin/env python3
"""Push a local file to a HackMD note.

Usage: python sync_hackmd.py <local_file> <note_id>
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <local_file> <note_id>", file=sys.stderr)
        sys.exit(1)

    local_file, note_id = sys.argv[1], sys.argv[2]

    token = os.environ.get("HACKMD_API_TOKEN")
    if not token:
        print("Error: HACKMD_API_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    content = Path(local_file).read_text(encoding="utf-8")

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
            print(f"OK ({resp.status})")
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} — {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
