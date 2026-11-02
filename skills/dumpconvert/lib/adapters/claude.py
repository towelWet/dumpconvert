# claude.py — read one Claude Code session record.
# Why: Claude exports mark role in top-level `type`, content in `message.content`.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
from flatten import flatten


def claude(record):
    role = record.get("type")                                      # "user" / "assistant" / bookkeeping types
    message = record.get("message")
    if role not in ("user", "assistant") or not isinstance(message, dict):
        return None                                                # not Claude shape (or summary/meta line)
    return role, flatten(message.get("content"))                   # caller drops empty text
