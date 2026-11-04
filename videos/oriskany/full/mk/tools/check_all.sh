#!/usr/bin/env bash
# run templates/check_safe_text.js on every built map scene; the only accepted failure is the small basemap credit line
# (same as the approved test v4 maps). Output: logs/check_safe.log
cd "$(dirname "$0")/.."; REPO=$(cd ../../../.. && pwd)
: > logs/check_safe.log
for d in scenes/*/; do n=$(basename $d)
  r=$(cd "$REPO" && NODE_PATH=$(npm root -g) timeout 300 node templates/check_safe_text.js "videos/oriskany/full/mk/$d/index.html" 0.5 2>&1 | grep -v "Terrain & bathymetry")
  if echo "$r" | grep -q "^  "; then echo "FAIL $n"; echo "$r" | grep "^  "; else echo "PASS $n (credit line excepted)"; fi
done >> logs/check_safe.log
