# opencode.py — read one line of dumpboth's OpenCode export: {info: {role}, parts: [...]}.
# Why: one OpenCode message holds text and tool parts together (call + result in same part),
#      so this adapter returns a list of turns in order.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
from text_of import text_of


def opencode(record):
    info, parts = record.get("info"), record.get("parts")
    if not isinstance(info, dict) or not isinstance(parts, list) or info.get("role") not in ("user", "assistant"):
        return None                                                # session header line has no role/parts
    turns = []
    for part in parts:
        if part.get("type") == "text" and not part.get("synthetic"):   # synthetic = OpenCode-injected text
            turns.append((info["role"], part.get("text", "").strip()))
        elif part.get("type") == "tool":                           # reasoning/step/patch/file parts dropped
            state = part.get("state", {})
            turns.append(("assistant", f"<tool_use name={part.get('tool', 'tool')}>\n{text_of(state.get('input', {}))}\n</tool_use>"))
            turns.append(("user", f"<tool_result>\n{text_of(state.get('output') or state.get('error') or '')}\n</tool_result>"))
    return turns
