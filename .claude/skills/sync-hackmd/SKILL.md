---
description: Push a local file to a HackMD note
allowed-tools: Bash
---

# /sync-hackmd — Push a local file to HackMD

Propagate local content to a HackMD note.

## Usage

```
/sync-hackmd <local_file>
```

## Known notes

| Local file               | Note ID                 |
|--------------------------|-------------------------|
| deliverables/slides-2026-06-02.md | WTLXst8MSuavlX7zSxX8EQ |

## What to do

1. Look up `<local_file>` in the Known notes table above
2. If found, run:

```bash
python ".claude/skills/sync-hackmd/sync_hackmd.py" "<local_file>" "<note_id>"
```

3. If not found, ask the user if a note exists on HackMD for this content. If yes, ask for the Note ID. If no, create a new note on HackMD. In either case, once you have the Note ID:
   - Add the new row to the Known notes table in this file
   - Run the script with the provided ID

4. Confirm success (`OK (202)`) or report the error

## Rules

- Never modify the content — push verbatim
- Requires `HACKMD_API_TOKEN` env var
