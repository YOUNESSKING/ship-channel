#!/usr/bin/env bash
cd "$(dirname "$0")/.."
for s in "$@"; do (cd scenes/v01_$s && npx -y hyperframes render . -o renders/v01_$s.mp4 > render.log 2>&1) && cp scenes/v01_$s/renders/v01_$s.mp4 out/v01_$s.mp4; echo "$s done" >> logs/render_some.log; done; echo ALLDONE >> logs/render_some.log
