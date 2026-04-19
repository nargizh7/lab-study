#!/usr/bin/env bash
# Reset: wipe previous participant state. Run after a participant leaves.
# Usage: .lab/reset.sh
set -u

cd "$(dirname "$0")/.."
PROJECT_ROOT="$(pwd)"
echo "Resetting $PROJECT_ROOT"

# Stop any running app server
deactivate 2>/dev/null || true
pkill -f "python app.py" 2>/dev/null || true
lsof -ti:5000 2>/dev/null | xargs kill -9 2>/dev/null || true

# Archive research data BEFORE destroying it
if [ -d .claude/research-logs ] && [ -n "$(ls -A .claude/research-logs 2>/dev/null)" ]; then
  ARCHIVE="$HOME/lab-study-data/$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$ARCHIVE"
  cp -r .claude/research-logs/* "$ARCHIVE/"
  echo "Archived logs to $ARCHIVE"
fi

# Reset tracked files (restores CLAUDE.md, hooks, settings.json, lab scripts)
git checkout -- .

# Remove generated artifacts
rm -rf instance/ uploads/ upload/ __pycache__/ .mypy_cache/
rm -rf .claude/hooks/state/ .claude/research-logs/ .claude/hooks/__pycache__/
rm -f .claude/settings.local.json CHANGES.md session_telemetry.csv .DS_Store
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Remove any participant venvs
rm -rf participant* venv

# Clear shell history (single-use lab machine)
cat /dev/null > "$HOME/.zsh_history" 2>/dev/null || true
cat /dev/null > "$HOME/.bash_history" 2>/dev/null || true

echo "Reset complete."
