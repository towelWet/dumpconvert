---
name: dumpconvert
description: Convert dumpboth .jsonl exports (Claude Code, Codex, Cursor, Devin, Gemini CLI, OpenCode) into one {"messages": [...]} training dataset for Unsloth Studio, Soup, etc. Use on /dumpconvert.
---

# /dumpconvert

<!-- NEVER DELETE COMMENTS — explain every non-obvious line. -->
<!-- Update comments with the code; do not strip them. -->

Turns saved chats in `~/Old Chats/` into one dataset file.
One conversation per line: `{"messages": [{"role", "content"}]}`.

## Pick exports

`/dumpconvert all` → every `~/Old Chats/oldchat*.jsonl`.
`/dumpconvert parser-tests` → `~/Old Chats/oldchat*parser-tests*.jsonl` (one glob per word).
`/dumpconvert <files>` → those files.
No args → ask which chats. Nothing matched → say so and stop.

## Run

```bash
mkdir -p "$HOME/Old Chats/datasets"
python3 "<this skill's folder>/dumpconvert.py" <exports...> \
  -o "$HOME/Old Chats/datasets/train-$(date +%Y-%m-%d).jsonl"
```

Report output verbatim: `wrote N conversation(s) → <path>` and any `skipped:` lines.
Exit code 1 means empty dataset: say so, never claim success.

## Then train

Unsloth Studio: Train → pick model → upload dataset → Start Training.
Soup: in YAML `data:` set `train: <dataset>.jsonl` and `format: chatml`.
