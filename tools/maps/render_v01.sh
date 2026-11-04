#!/usr/bin/env bash
cd "$(dirname "$0")/.."
for s in world southern beringia doggerland black_sea mediterranean red_sea carpentaria gulf_mexico sundaland; do
  [ -f out/v01_$s.mp4 ] && continue
  t0=$(date +%s)
  (cd scenes/v01_$s && npx -y hyperframes render . -o renders/v01_$s.mp4 > render.log 2>&1) && cp scenes/v01_$s/renders/v01_$s.mp4 out/v01_$s.mp4
  echo "$s $(( $(date +%s)-t0 ))s" >> logs/render_v01.log
done
echo ALLDONE >> logs/render_v01.log
