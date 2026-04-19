#!/usr/bin/env python3
"""PostToolUse: log successful completions for latency / approval-rate analysis."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import load_input, load_state, save_state, log_event

data = load_input()
session_id = data.get("session_id", "default")
tool = data.get("tool_name", "")
tool_input = data.get("tool_input", {}) or {}

if tool not in ("Edit", "Write", "MultiEdit", "NotebookEdit", "Bash", "Read"):
    sys.exit(0)

state = load_state(session_id)
if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
    state["edits_approved"] = state.get("edits_approved", 0) + 1
save_state(session_id, state)

log_event(session_id, "tool_completed", {
    "turn": state.get("turn"),
    "tool": tool,
    "file_path": tool_input.get("file_path"),
    "command_preview": (tool_input.get("command") or "")[:200],
    "completed_ts": time.time(),
})
