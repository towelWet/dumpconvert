# cursor.py — read one Cursor agent-transcript record.
# Why: Cursor puts role at top level and content blocks under `message.content`.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
from flatten import flatten


def cursor(record):
    role = record.get("role")
    message = record.get("message")
    if role not in ("user", "assistant") or not isinstance(message, dict):
        return None                                                # not Cursor shape
    return role, flatten(message.get("content"))                   # blocks → text, tool calls kept
