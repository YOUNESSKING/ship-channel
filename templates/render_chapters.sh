#!/usr/bin/env bash
# Render chapter projects one by one (skips a chapter when its index.html and assets did not change), then join them.
#   ./render_chapters.sh WORK_ROOT KEY [KEY ...]
#   env: QUALITY=draft|standard|high (default draft)  WORKERS=n (Chrome workers, default auto)  FORCE=1 (render again)  OUT=joined.mp4 (default WORK_ROOT/../rendered/joined_silent.mp4)
# WORK_ROOT holds one folder per chapter (the output of build_chapter.py). Keys are the folder names, in video order.
set -euo pipefail
ROOT="$(cd "$1" && pwd)"; shift; Q="${QUALITY:-draft}"; R="$ROOT/../rendered"; mkdir -p "$R"
[ $# -gt 0 ] || { echo "give the chapter keys in order"; exit 1; }
: > "$R/list.txt"
for k in "$@"; do
  h=$( (cat "$ROOT/$k/index.html"; (cd "$ROOT/$k" && find assets -name '*.mp4' -o -name '*.jpg' -o -name '*.png' | sort | xargs stat -c '%n %s %Y' 2>/dev/null)) | md5sum | cut -d' ' -f1)
  if [ "${FORCE:-0}" != "1" ] && [ -f "$R/$k.hash" ] && [ "$(cat "$R/$k.hash")" = "$h" ] && [ -f "$R/$k.mp4" ]; then echo "skip $k (unchanged)"
  else echo "render $k"; (cd "$ROOT/$k" && npx -y hyperframes@0.8.188 render --fps 30 --quality "$Q" ${WORKERS:+--workers $WORKERS} --output "$R/$k.mp4" > "$R/$k.log" 2>&1) && echo "$h" > "$R/$k.hash"; fi
  echo "file '$R/$k.mp4'" >> "$R/list.txt"
done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$R/list.txt" -c copy "${OUT:-$R/joined_silent.mp4}"
echo "joined -> ${OUT:-$R/joined_silent.mp4}"
