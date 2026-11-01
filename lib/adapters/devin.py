# devin.py — read one Devin CLI message node.
# Why: Devin nodes are flat: top-level `role` plus `content` string; also system/tool roles.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
from flatten import flatten


def devin(record):
    role = record.get("role")
    content = record.get("content")
    if role not in ("user", "assistant") or not isinstance(content, str):
        return None                                                # system/tool nodes or other shapes
    return role, flatten(content)                                  # string path just trims whitespace
