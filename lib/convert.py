# convert.py — one dumpboth .jsonl export → one {"messages": [...]} training row.
# Why: Unsloth Studio chat datasets read one conversation per line in messages format.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
import json
from merge import merge
from latest import latest


def convert(path, adapters):
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:                               # blank or partial line → skip
            continue
        if isinstance(record, dict):
            records.append(record)
    turns = []
    for record in latest(records):                                 # streamed rewrites collapse to final copy
        found = None                                               # reset so prior record's turn never leaks
        for adapter in adapters:
            found = adapter(record)                                # first adapter that recognizes shape wins
            if found:
                break
        found = [found] if isinstance(found, tuple) else found or []   # adapter may return one turn or a list
        turns += [turn for turn in found if turn[1]]               # drop turns with no usable text
    messages = merge(turns)
    return {"messages": messages} if len(messages) >= 2 else None  # need at least one exchange
