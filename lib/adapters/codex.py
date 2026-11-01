# codex.py — read one Codex rollout record (~/.codex/sessions/**/rollout-*.jsonl).
# Why: Codex wraps everything in `response_item` → `payload`; chat text lives in
#      input_text/output_text blocks, tool calls are separate records.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
import json

INJECTED = ("<environment_context", "<instructions", "<system-reminder",
            "# AGENTS.md", "# Codex Global", "<external_codex_")   # same skips as dumpboth agents/codex/turn.py; last = app UI marker
CALLS = {"custom_tool_call": "input", "function_call": "arguments"}   # tool call kind → its argument field
OUTPUTS = ("custom_tool_call_output", "function_call_output")


def codex(record):
    payload = record.get("payload")
    if record.get("type") != "response_item" or not isinstance(payload, dict):
        return None                                               # event_msg, token counts, turn_context…
    kind = payload.get("type")
    if kind in CALLS:                                             # agent step → assistant turn, tagged like Claude
        args = payload.get(CALLS[kind], "")
        args = args if isinstance(args, str) else json.dumps(args, ensure_ascii=False)
        return "assistant", f"<tool_use name={payload.get('name', 'tool')}>\n{args}\n</tool_use>"
    if kind in OUTPUTS:                                           # tool output → user turn, like Claude tool_result
        out = payload.get("output", "")
        out = out if isinstance(out, str) else json.dumps(out, ensure_ascii=False)
        return "user", f"<tool_result>\n{out}\n</tool_result>"
    role = payload.get("role")
    if kind != "message" or role not in ("user", "assistant"):
        return None                                               # developer/system prompts, reasoning
    texts = [b.get("text", "") for b in payload.get("content") or []
             if isinstance(b, dict) and b.get("type") in ("input_text", "output_text")]
    texts = [t.strip() for t in texts if t.strip() and not t.strip().startswith(INJECTED)]
    return role, "\n".join(texts)                                 # empty → convert.py drops it
