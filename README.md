# dumpconvert

Turn your saved AI coding chats into a training dataset (Unsloth, Soup, etc).

dumpboth saves each chat's raw `.jsonl` in its agent's own format.
Trainers want one conversation per line as `{"messages": [...]}`.
Soup calls this `chatml`; Unsloth Studio reads it as a chat dataset. dumpconvert converts.

## Supported exports

| Agent       | Raw shape read                      |
|-------------|-------------------------------------|
| Claude Code | `type` + `message.content` blocks   |
| Codex       | `response_item` + `payload`         |
| Cursor      | `role` + `message.content` blocks   |
| Devin       | `role` + `content` string           |
| Gemini CLI  | `type` + `content` + `toolCalls`    |
| OpenCode    | `info.role` + `parts`               |

Only user and assistant turns are kept. Tool calls and results stay as tagged text; thinking is dropped.
Back-to-back turns from same speaker are joined, so turns alternate.

## Use

Needs Python 3. No packages to install.
As skill: put this folder in `~/.claude/skills/dumpconvert/`, then `/dumpconvert all`. As CLI:
```sh
python3 dumpconvert.py ~/"Old Chats"/oldchat*.jsonl -o train.jsonl
```

Skipped files are listed. Exit code is 1 when nothing was written.

## Train in Unsloth Studio

1. Open Unsloth Studio, go to Train, pick a model.
2. Under dataset, upload `train.jsonl`.
3. Wait for dataset preview to show Ready, click Start Training.

Only include chats you are fine training on: exports can hold code, paths, tool output.

## Add an agent

Drop one file in `lib/adapters/`, exporting one function named after file.
It takes one JSON record and returns `(role, text)`, a list of those, or `None`. No registry to edit.

## Test

```sh
python3 tests/run_tests.py
```
