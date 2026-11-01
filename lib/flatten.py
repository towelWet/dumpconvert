# flatten.py — turn one message's content (string or block list) into plain text.
# Why: Claude and Cursor store content as typed blocks; trainers want one string.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
import json


def flatten(content):
    if isinstance(content, str):                                   # Devin + simple turns: already text
        return content.strip()
    if not isinstance(content, list):                              # null / unexpected shape → no text
        return ""
    parts = []
    for block in content:
        if not isinstance(block, dict):                            # skip stray scalars inside block list
            continue
        kind = block.get("type")
        if kind == "text":
            parts.append(block.get("text", ""))                   # visible prose
        elif kind == "tool_use":                                   # keep tool calls so model learns agent steps
            args = json.dumps(block.get("input", {}), ensure_ascii=False)
            parts.append(f"<tool_use name={block.get('name', 'tool')}>\n{args}\n</tool_use>")
        elif kind == "tool_result":                                # tool output; may itself be a block list
            parts.append(f"<tool_result>\n{flatten(block.get('content', ''))}\n</tool_result>")
        # thinking blocks intentionally dropped: private reasoning, not training target
    return "\n".join(p for p in parts if p).strip()
