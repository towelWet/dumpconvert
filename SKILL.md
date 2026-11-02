---
name: dumpconvert
description: Convert dumpboth/dumpjsonl .jsonl exports (Claude Code, Codex, Cursor, Devin, Gemini CLI, OpenCode) into one {"messages": [...]} training dataset for Unsloth Studio, Soup, etc. Use on /dumpconvert, "convert my dumps to a dataset", "make training data from old chats".
---

# /dumpconvert

<!-- NEVER DELETE COMMENTS — explain every non-obvious line. -->
<!-- Update comments with the code; do not strip them. -->

Turns raw dumpboth `.jsonl` exports into one dataset file.
One conversation per line, `{"messages": [{"role", "content"}]}`.
Soup calls this `chatml`; Unsloth Studio reads it as chat dataset.

## Run

```bash
python3 "$HOME/.claude/skills/dumpconvert/dumpconvert.py" \
  <exports.jsonl ...> -o "$HOME/Old Chats/datasets/train-$(date +%Y-%m-%d).jsonl"
```

Args (pick exports, then pass them to script):
`all` → every `~/Old Chats/oldchat*.jsonl` (explicit opt-in to whole archive).
word(s), e.g. `parser-tests` → `~/Old Chats/oldchat*<word>*.jsonl` per word.
file paths / globs → used as given.
No args → ask which chats; never silently default to whole archive.
Zero files matched → say so; do not run script.
Create `~/Old Chats/datasets/` first (`mkdir -p`).
Report stderr verbatim: `wrote N conversation(s)` plus any `skipped:` lines.
Exit 1 = empty dataset; say so, never claim success.

## What it keeps

User + assistant turns. Tool calls/results as tagged text. Thinking dropped.
Same-speaker runs joined so turns alternate; rows start with user turn.

## Then train

Unsloth Studio: Train → pick model → upload dataset → Ready → Start Training.
Soup: in YAML config, `data:` → `train: <dataset>.jsonl` and `format: chatml`. See `/unsloth`, `/soup`.

## Source

Code: this folder
(tests: `python3 tests/run_tests.py`).
Sister tools: `/dumpboth` (export), `/dbv` (viewer).

Publishing: before upload, this skill must have no leaks (private paths, personal names, emails, drive paths, private chat notes, blocked-folder paths, machine-only rules). Remove only the leaks, then upload this real skill folder as it is. dumpboth, dbv, and dumpconvert stay three repos and three skills; dumpchat and dumpjsonl stay nested inside dumpboth. No rewritten copy, no invented skills/ parent, no extra release or staging folders.
