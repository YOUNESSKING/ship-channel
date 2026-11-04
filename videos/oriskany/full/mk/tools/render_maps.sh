#!/usr/bin/env bash
# Render every full-video map scene to ../segments/m_<scene>.mp4, one at a time, detached and resumable.
# usage (from full/mk):  bash tools/render_maps.sh [SCENE ...]     (no args = all 48; RERENDER=1 forces)
# A scene is skipped when its segment exists and is newer than scenes-src/<scene>.js, lib/ship.js and its basemap.
# Progress: logs/render_maps.log; done marker: logs/render_maps.done; per scene: scenes/<scene>/render.log
set -u
cd "$(dirname "$0")/.."
mkdir -p logs ../segments
if [ -z "${RENDER_MAPS_DETACHED:-}" ]; then
  rm -f logs/render_maps.done
  RENDER_MAPS_DETACHED=1 setsid nohup bash "$0" "$@" >> logs/render_maps.log 2>&1 < /dev/null &
  echo "render_maps started (pid $!). Log: $(pwd)/logs/render_maps.log"; exit 0
fi
if [ $# -eq 0 ]; then set -- $(python3 -c "import sys;sys.path.insert(0,'tools');import build_full as b;print(' '.join([s['scene'] for s in b.SEGS]+[s['scene'] for s in b.plan_segs() if s['scene'] not in {q['scene'] for q in b.SEGS}]))"); fi
FAILED=0; T0=$(date +%s)
for name in "$@"; do
  out=../segments/m_$name.mp4
  base=$(head -1 scenes-src/$name.js | sed 's/.*BASEMAP: *//')
  if [ -z "${RERENDER:-}" ] && [ -f "$out" ] && [ "$out" -nt scenes-src/$name.js ] && [ "$out" -nt lib/ship.js ] && [ "$out" -nt assets/$base.jpg ]; then
    echo "=== skip $name (up to date)"; continue; fi
  echo "=== $(date -u +%T) build $name"
  python3 tools/build_full.py "$name" || { echo "BUILD FAILED $name"; FAILED=1; continue; }
  s=$(date +%s)
  (cd "scenes/$name" && rm -f "renders/$name.mp4" && nice -n 5 hyperframes render . -o "renders/$name.mp4" --workers 2 --quiet > render.log 2>&1) &
  wait $!
  if [ -s "scenes/$name/renders/$name.mp4" ] && ffprobe -v error "scenes/$name/renders/$name.mp4" 2>/dev/null; then
    cp "scenes/$name/renders/$name.mp4" "$out.tmp.mp4" && mv "$out.tmp.mp4" "$out"
    d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out")
    echo "=== $(date -u +%T) OK $name ${d}s in $(( $(date +%s) - s ))s"
  else
    echo "=== $(date -u +%T) RENDER FAILED $name (scenes/$name/render.log)"; FAILED=1
  fi
done
echo "=== $(date -u +%T) finished, failed=$FAILED, total $(( $(date +%s) - T0 ))s"
echo "failed=$FAILED" > logs/render_maps.done
