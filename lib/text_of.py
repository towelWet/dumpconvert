# text_of.py — any JSON value → string for a training turn.
# Why: tool args and outputs may be strings or nested objects; datasets need plain text.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
import json


def text_of(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)   # keep unicode readable
