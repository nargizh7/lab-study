#!/usr/bin/env python3
"""PreToolUse for Read: gate reads of sensitive files."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import load_input, load_state, save_state, log_event, touches_sensitive

data = load_input()
session_id = data.get("session_id", "default")
tool_input = data.get("tool_input", {}) or {}
file_path = tool_input.get("file_path", "")

surfaces = touches_sensitive(file_path)
# Only gate reads that hit high-sensitivity surfaces (not every app.py read).
HIGH_SENS = {"credentials", "database", "file_uploads"}
hit = [s for s in surfaces if s in HIGH_SENS]

if not hit:
    sys.exit(0)

state = load_state(session_id)
state["prompts_issued"] = state.get("prompts_issued", 0) + 1
save_state(session_id, state)

log_event(session_id, "pre_read_prompt", {
    "turn": state.get("turn"),
    "file": file_path,
    "surfaces": hit,
    "high_risk": True,
    "prompt_issued_ts": time.time(),
})

reason = (
    f"[HIGH-RISK read] {file_path} contains: {', '.join(hit)}. "
    "Confirm yes or no before I read it."
)

output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason,
    }
}
print(json.dumps(output))
