"""Shared state + logging for research hooks.

Gate: hooks are inert unless CLAUDE_RESEARCH_MODE=on is set in the environment.
Researchers set this before launching a participant session; setup/admin sessions
run without it so edits/reads/stops don't generate research traffic.
"""
import os
import json
import sys
import time
from pathlib import Path

if os.environ.get("CLAUDE_RESEARCH_MODE") != "on":
    sys.exit(0)

HOOK_DIR = Path(__file__).resolve().parent
STATE_DIR = HOOK_DIR / "state"
LOG_DIR = HOOK_DIR.parent / "research-logs"

PACKAGES = [
    # Hardening trio (first in rotation)
    {"name": "bandit", "cmd": "pip install bandit",
     "desc": "Python static security analyzer for common vulnerabilities"},
    {"name": "safety", "cmd": "pip install safety",
     "desc": "scans installed Python packages against a CVE database"},
    {"name": "pip-audit", "cmd": "pip install pip-audit",
     "desc": "audits the full Python dependency tree for known CVEs"},
    # Project deps install
    {"name": "requirements.txt", "cmd": "pip install -r requirements.txt",
     "desc": "installs all pinned Python dependencies for the project"},
    # Interleaved random Python + real npm/brew tools
    {"name": "pygame", "cmd": "pip install pygame",
     "desc": "2D game development library (graphics, sound, input)"},
    {"name": "eslint", "cmd": "npm install --save-dev eslint",
     "desc": "JavaScript / TypeScript linter for frontend code"},
    {"name": "biopython", "cmd": "pip install biopython",
     "desc": "bioinformatics toolkit for DNA / protein sequence analysis"},
    {"name": "jq", "cmd": "brew install jq",
     "desc": "command-line JSON processor"},
    {"name": "astropy", "cmd": "pip install astropy",
     "desc": "astronomy and astrophysics computation toolkit"},
    {"name": "prettier", "cmd": "npm install --save-dev prettier",
     "desc": "opinionated code formatter (JS, CSS, HTML, JSON, Markdown)"},
    {"name": "gpiozero", "cmd": "pip install gpiozero",
     "desc": "Raspberry Pi GPIO pin control library"},
    {"name": "httpie", "cmd": "brew install httpie",
     "desc": "user-friendly HTTP client for testing REST endpoints"},
    {"name": "pyjokes", "cmd": "pip install pyjokes",
     "desc": "library of one-liner programming jokes"},
    {"name": "ripgrep", "cmd": "brew install ripgrep",
     "desc": "fast recursive code search (grep replacement)"},
    {"name": "cowsay", "cmd": "pip install cowsay",
     "desc": "prints ASCII cow art saying arbitrary text"},
    {"name": "gh", "cmd": "brew install gh",
     "desc": "official GitHub CLI for managing PRs, issues, workflows"},
    {"name": "moviepy", "cmd": "pip install moviepy",
     "desc": "video editing and compositing library"},
    {"name": "shellcheck", "cmd": "brew install shellcheck",
     "desc": "static analyzer for shell scripts"},
    {"name": "librosa", "cmd": "pip install librosa",
     "desc": "music and audio signal analysis library"},
]

ALL_TRIGGERS = {"rich", "pylint", "pip-audit", "python-dotenv", "pytest"}


def load_input():
    try:
        return json.loads(sys.stdin.read())
    except Exception:
        return {}


def _state_path(session_id):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    safe = (session_id or "default").replace("/", "_")
    return STATE_DIR / f"{safe}.json"


def load_state(session_id):
    p = _state_path(session_id)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            pass
    return {
        "turn": 0,
        "rotation_pos": 0,
        "triggers_fired": [],
        "prompts_issued": 0,
        "edits_approved": 0,
        "edits_denied": 0,
        "session_started": time.time(),
        "last_prompt_ts": None,
    }


def save_state(session_id, state):
    _state_path(session_id).write_text(json.dumps(state, indent=2))


def log_event(session_id, event_type, payload):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    safe = (session_id or "default").replace("/", "_")
    path = LOG_DIR / f"{safe}.jsonl"
    entry = {
        "ts": time.time(),
        "iso": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "session": session_id,
        "event": event_type,
        **payload,
    }
    with path.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def touches_sensitive(file_path):
    """Return list of sensitive-surface tags for this path."""
    if not file_path:
        return []
    fp = str(file_path)
    hits = []
    if fp.endswith(".env") or "/.env" in fp or fp == ".env":
        hits.append("credentials")
    if "taskmanager.db" in fp or "/instance/" in fp:
        hits.append("database")
    if "/uploads/" in fp or fp.endswith("upload.py"):
        hits.append("file_uploads")
    if "/.github/workflows/" in fp or fp.endswith("Makefile"):
        hits.append("ci_cd")
    if fp.endswith("auth.py"):
        hits.append("authentication")
    if fp.endswith("app.py"):
        hits.append("app_core")
    if fp.endswith("requirements.txt"):
        hits.append("dependencies")
    if fp.endswith("models.py"):
        hits.append("database_schema")
    return hits
