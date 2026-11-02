# gemini.py — read one Gemini CLI record (~/.gemini/tmp/<project>/chats/session-*.jsonl).
# Why: Gemini puts reply text, tool calls AND tool results in one `gemini` record, so this
#      adapter returns a list of turns: reply → tool_use (assistant) → tool_result (user).
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
from text_of import text_of


def gemini(record):
    kind = record.get("type")
    if kind == "user":                                             # content = [{"text": ...}, ...]
        parts = record.get("content") or []
        texts = [p.get("text", "") for p in parts if isinstance(p, dict)]
        return [("user", "\n".join(t.strip() for t in texts if t.strip()))]
    if kind != "gemini":
        return None                                                # info notices, $set updates, session header
    turns = [("assistant", text_of(record.get("content") or "").strip())]   # thoughts dropped, like Claude thinking
    for call in record.get("toolCalls") or []:
        turns.append(("assistant", f"<tool_use name={call.get('name', 'tool')}>\n{text_of(call.get('args', {}))}\n</tool_use>"))
        outs = [r.get("functionResponse", {}).get("response", {}).get("output", r)
                for r in call.get("result") or [] if isinstance(r, dict)]
        if outs:
            turns.append(("user", "<tool_result>\n" + "\n".join(text_of(o) for o in outs) + "\n</tool_result>"))
    return turns
