# latest.py — keep only newest copy of each record that carries a top-level `id`.
# Why: Gemini CLI rewrites a message as it streams (same id, later line adds toolCalls);
#      reading every copy would double the turn. Claude/Codex/Cursor/Devin records have
#      no top-level `id`, so they pass through untouched.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.


def latest(records):
    slot = {}                                                      # id → index of first appearance
    kept = []
    for record in records:
        key = record.get("id")
        if not isinstance(key, str):
            kept.append(record)                                    # no id → nothing to supersede
        elif key in slot:
            kept[slot[key]] = record                               # newer copy replaces older, keeps order
        else:
            slot[key] = len(kept)
            kept.append(record)
    return kept
