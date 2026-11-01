# merge.py — join back-to-back turns from same role into one turn.
# Why: agents split one reply across many records; chat templates expect user/assistant alternation.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.


def merge(turns):
    messages = []
    for role, text in turns:
        if messages and messages[-1]["role"] == role:
            messages[-1]["content"] += "\n\n" + text               # same speaker continues
        else:
            messages.append({"role": role, "content": text})
    while messages and messages[0]["role"] != "user":              # training rows must open with user turn
        messages.pop(0)
    return messages
