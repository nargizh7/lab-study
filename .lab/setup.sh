#!/usr/bin/env bash
# Setup: create venv for the next participant.
# Usage: .lab/setup.sh <participant_id>
#   e.g. .lab/setup.sh participant3
set -euo pipefail

PARTICIPANT_ID="${1:-}"
if [ -z "$PARTICIPANT_ID" ]; then
  echo "error: participant id required. example: .lab/setup.sh participant3" >&2
  exit 1
fi
if [ "$PARTICIPANT_ID" = "." ] || [ "$PARTICIPANT_ID" = "/" ]; then
  echo "error: refusing to venv into $PARTICIPANT_ID" >&2
  exit 1
fi

cd "$(dirname "$0")/.."

python3 -m venv "$PARTICIPANT_ID"
"$PARTICIPANT_ID/bin/pip" install --quiet \
  "Flask>=3.0,<4.0" \
  "Flask-SQLAlchemy>=3.1,<4.0" \
  "python-dotenv>=1.0,<2.0"

echo ""
echo "VERIFY:"
echo "  Branch:      $(git branch --show-current)"
echo "  Git clean:   $(git status --short | wc -l | tr -d ' ') dirty (want 0)"
echo "  Database:    $([ -d instance ] && echo BAD || echo OK)"
echo "  CLAUDE.md:   $([ -f CLAUDE.md ] && echo OK || echo MISSING)"
echo "  Hooks:       $(ls .claude/hooks/*.py 2>/dev/null | wc -l | tr -d ' ') scripts (want 7)"
echo "  Settings:    $([ -f .claude/settings.json ] && echo OK || echo MISSING)"
echo "  Venv pkgs:   $("$PARTICIPANT_ID/bin/pip" list 2>/dev/null | tail -n +3 | wc -l | tr -d ' ') (want ~15)"
echo ""
echo "LAUNCH:"
echo "  Terminal 1:"
echo "    cd ~/task-manager && source $PARTICIPANT_ID/bin/activate && python app.py"
echo "  Terminal 2:"
echo "    cd ~/task-manager && source $PARTICIPANT_ID/bin/activate && export CLAUDE_RESEARCH_MODE=on && claude"
