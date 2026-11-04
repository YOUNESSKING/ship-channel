#!/usr/bin/env bash
# build + snapshot scenes at 5 evenly spaced times; copies each contact sheet to logs/snap_SCENE.jpg
cd "$(dirname "$0")/.."
for s in "$@"; do
  python3 tools/build_full.py $s >/dev/null || { echo "BUILD FAIL $s"; continue; }
  d=$(python3 -c "import json;print(json.load(open('scenes/$s/meta.json')) and open('scenes/$s/index.html').read().split('data-duration=\"')[1].split('\"')[0])")
  at=$(python3 -c "d=$d;print(','.join(f'{x:.2f}' for x in [0.05,d*0.3,d*0.55,d*0.8,d-0.08]))")
  out=$(cd scenes/$s && hyperframes snapshot . --at $at 2>&1)
  sh=$(echo "$out" | grep -o '/[^ ]*contact-sheet.jpg' | tail -1)
  [ -n "$sh" ] && cp "$sh" logs/snap_$s.jpg && echo "ok $s $at" || { echo "SNAP FAIL $s"; echo "$out" | tail -5; }
done
