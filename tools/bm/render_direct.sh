#!/usr/bin/env bash
# Render the already-built scenes one at a time (the agents' custom inline builders must NOT be re-run by render_all.sh).
# usage: bash tools/render_direct.sh SCENE [SCENE ...]   progress: logs/render_direct.log ; marker logs/render_direct.done
cd "$(dirname "$0")/.."
if [ -z "${RD_DETACHED:-}" ]; then rm -f logs/render_direct.done; RD_DETACHED=1 setsid nohup bash "$0" "$@" > logs/render_direct.log 2>&1 < /dev/null & echo started $!; exit 0; fi
F=0
for n in "$@"; do
  mkdir -p scenes/$n/renders
  if [ -s scenes/$n/renders/$n.mp4 ] && grep -q "Render complete" scenes/$n/render.log 2>/dev/null; then echo "skip $n"; continue; fi
  echo "=== $(date -u +%T) render $n"
  (cd scenes/$n && nice -n 5 hyperframes render . -o renders/$n.mp4 > render.log 2>&1)
  if grep -q "Render complete" scenes/$n/render.log; then echo "=== $(date -u +%T) OK $n"; else echo "=== $(date -u +%T) FAILED $n"; F=1; fi
done
echo "=== $(date -u +%T) finished failed=$F"; echo "failed=$F" > logs/render_direct.done
