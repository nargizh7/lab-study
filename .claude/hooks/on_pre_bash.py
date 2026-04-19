#!/usr/bin/env python3
"""PreToolUse for Bash: gate pip install and other privileged commands."""
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import load_input, load_state, save_state, log_event

data = load_input()
session_id = data.get("session_id", "default")
tool_input = data.get("tool_input", {}) or {}
cmd = tool_input.get("command", "") or ""

HIGH_RISK_PATTERNS = [
    (re.compile(r"\bpip(3)?\s+install\b"), "pip_install"),
    (re.compile(r"\brm\s+-rf\b"), "rm_rf"),
    (re.compile(r"\bchmod\b"), "chmod"),
    (re.compile(r"\bcurl\b.*\|\s*(sh|bash|python)"), "curl_pipe_shell"),
    (re.compile(r"\bgit\s+push\b"), "git_push"),
    (re.compile(r">\s*\.env\b"), "env_write"),
]

hit = None
for pat, label in HIGH_RISK_PATTERNS:
    if pat.search(cmd):
        hit = label
        break

if hit is None:
    # Not gated — let it through.
    sys.exit(0)

# Try to extract pip package names for richer logging
pkgs = []
if hit == "pip_install":
    for m in re.finditer(r"pip(?:3)?\s+install\s+(.*?)(?:$|&&|\|\||;)", cmd):
        tail = m.group(1).strip()
        for tok in tail.split():
            if tok.startswith("-"):
                continue
            pkgs.append(tok)

state = load_state(session_id)
state["prompts_issued"] = state.get("prompts_issued", 0) + 1
save_state(session_id, state)

log_event(session_id, "pre_bash_prompt", {
    "turn": state.get("turn"),
    "pattern": hit,
    "command_preview": cmd[:300],
    "packages": pkgs,
    "high_risk": True,
    "prompt_issued_ts": time.time(),
})

reason = (
    f"[HIGH-RISK: {hit}] Command: {cmd[:300]}. "
    + (f"Packages: {pkgs}. " if pkgs else "")
    + "Executes with your filesystem and network access. Confirm yes or no."
)

output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason,
    }
}
print(json.dumps(output))
