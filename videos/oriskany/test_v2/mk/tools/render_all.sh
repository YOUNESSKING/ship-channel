#!/usr/bin/env bash
# Render map scenes one at a time, then (optionally) assemble the full video. Safe to run in the background.
#
# usage (from the project folder, e.g. goosegreen/):
#   bash tools/render_all.sh [--assemble] "SCENE BASEMAP FIRST_TAG LAST_TAG" ["..." ...]
# example:
#   bash tools/render_all.sh --assemble "move3 darwin move3-1 move3-10" "ending isthmus end-1 end-2"
#
# Why this exists (lessons from the Goose Green session):
# - Renders started from a tool shell die with "render_cancelled_parent_exited" when that shell exits,
#   so this script re-launches itself detached (setsid + nohup) and returns at once.
# - Never wait with `pgrep -f "hyperframes render"`: it also matches other scripts' wait loops whose
#   command lines contain that text, so the wait never ends. We wait on the render's own PID instead.
# - Agents stopped by a usage limit can leave orphan wait/render loops behind; they are killed first.
# Progress: logs/render_all.log; per scene: scenes/NAME/render.log; finished marker: logs/render_all.done
set -u
cd "$(dirname "$0")/.."
PROJ=$(pwd)
mkdir -p logs

if [ -z "${RENDER_ALL_DETACHED:-}" ]; then
  rm -f logs/render_all.done
  RENDER_ALL_DETACHED=1 setsid nohup bash "$0" "$@" > logs/render_all.log 2>&1 < /dev/null &
  echo "render_all started in the background (pid $!). Log: $PROJ/logs/render_all.log; done marker: $PROJ/logs/render_all.done"
  exit 0
fi

ASSEMBLE=0
if [ "${1:-}" = "--assemble" ]; then ASSEMBLE=1; shift; fi

# Kill orphaned renders and wait loops from earlier (crashed or limit-stopped) sessions and agents.
for pid in $(pgrep -f "[h]yperframes render|[w]hile pgrep" || true); do
  [ "$pid" != "$$" ] && kill "$pid" 2>/dev/null && echo "killed stale process $pid"
done

FAILED=0
for spec in "$@"; do
  set -- $spec
  name=$1
  echo "=== $(date -u +%T) build $name"
  python3 tools/build_scene.py "$@" || { echo "BUILD FAILED $name"; FAILED=1; continue; }
  (cd "scenes/$name" && hyperframes lint . 2>&1 | tail -2)
  echo "=== $(date -u +%T) render $name"
  (cd "scenes/$name" && nice -n 5 hyperframes render . -o "renders/$name.mp4" > render.log 2>&1) &
  wait $!
  if grep -q "Render complete" "scenes/$name/render.log"; then
    echo "=== $(date -u +%T) OK $name"
  else
    echo "=== $(date -u +%T) RENDER FAILED $name (see scenes/$name/render.log)"; FAILED=1
  fi
done

if [ "$ASSEMBLE" = 1 ] && [ "$FAILED" = 0 ]; then
  echo "=== $(date -u +%T) assemble 1080p + 720p preview"
  python3 tools/assemble_full.py && python3 tools/assemble_full.py --preview || FAILED=1
fi
echo "=== $(date -u +%T) finished, failed=$FAILED"
echo "failed=$FAILED" > logs/render_all.done
