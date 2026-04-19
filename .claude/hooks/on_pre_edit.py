#!/usr/bin/env python3
"""PreToolUse for Edit|Write|MultiEdit|NotebookEdit: force native yes/no UI."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import load_input, load_state, save_state, log_event, touches_sensitive

data = load_input()
session_id = data.get("session_id", "default")
tool = data.get("tool_name", "")
tool_input = data.get("tool_input", {}) or {}
file_path = tool_input.get("file_path", "unknown")

surfaces = touches_sensitive(file_path)
high_risk = bool(surfaces)
risk_label = "HIGH-RISK" if high_risk else "standard"

state = load_state(session_id)
state["prompts_issued"] = state.get("prompts_issued", 0) + 1
save_state(session_id, state)

log_event(session_id, "pre_edit_prompt", {
    "turn": state.get("turn"),
    "file": file_path,
    "tool": tool,
    "high_risk": high_risk,
    "surfaces": surfaces,
    "prompt_issued_ts": time.time(),
})

reason_lines = [
    f"[{risk_label}] Pre-edit confirmation — {tool} on {file_path}.",
]
if surfaces:
    reason_lines.append(f"Sensitive surfaces touched: {', '.join(surfaces)}.")
reason_lines.append("Confirm yes or no before I apply this edit.")

output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": " ".join(reason_lines),
    }
}
print(json.dumps(output))
