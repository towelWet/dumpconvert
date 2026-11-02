# dumpconvert

Claude Code skill: `/dumpconvert` turns saved AI coding chats into training dataset (Unsloth, Soup, etc).

![/dumpconvert typed in live Claude Code chat, writing training dataset](docs/images/dumpconvert.png)

## Install

```sh
cp -R skills/* ~/.claude/skills/
```

Needs Python 3. No packages to install.

## Use

In Claude Code:

```text
/dumpconvert all
/dumpconvert mylabel
```

Reads exports from Claude Code, Codex, Cursor, Devin, Gemini CLI and OpenCode.
Writes one `{"messages": [...]}` conversation per line to `~/Old Chats/datasets/`.

Full instructions: [skills/dumpconvert/SKILL.md](skills/dumpconvert/SKILL.md).

## See also

[dumpboth](https://github.com/towelWet/dumpboth): save your AI coding chat as `.md` + `.jsonl`.

[dbv](https://github.com/towelWet/dbv): read saved chats on Mac.
