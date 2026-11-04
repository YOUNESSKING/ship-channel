#!/usr/bin/env bash
# Step 3: build + render every chapter of the full Oriskany video (test v4 chain: templates/build_chapter.py with GRADE=none,
# HyperFrames 0.8.188 at "standard" quality, 30 fps). Detached and resumable: run with
#   nohup bash build/render_all.sh > build/render_all.log 2>&1 &
# A chapter is skipped when chapter/render_cNN.mp4 exists and its stamp (shot list + every clip it uses) is unchanged.
# Renders go to a .part file first, so a reboot mid-render never leaves a half file that looks done. FORCE=1 re-renders.
set -uo pipefail
FULL="$(cd "$(dirname "$0")/.." && pwd)"; ROOT="$(cd "$FULL/../../.." && pwd)"
KEYS="${*:-c01 c02 c03 c04 c05 c06 c07}"
export NODE_PATH="$(npm root -g)"
for k in $KEYS; do
  J="$FULL/chapter/$k.json"; OUT="$FULL/chapter/render_$k.mp4"; W="$FULL/chapter/work/$k"
  STAMP=$(python3 - "$J" <<'EOF'
import json, os, sys, hashlib
j = sys.argv[1]; c = json.load(open(j)); d = os.path.join(os.path.dirname(j), c["clips_dir"])
h = hashlib.md5(open(j, "rb").read())
for s in c["shots"]:
    for key in ("clip", "bg_clip"):
        f = (s.get(key) or {}).get("file")
        if f:
            p = os.path.join(d, f); h.update((f + str(os.path.getsize(p)) + str(int(os.path.getmtime(p)))).encode())
print(h.hexdigest())
EOF
)
  if [ "${FORCE:-0}" != "1" ] && [ -f "$OUT" ] && [ "$(cat "$OUT.stamp" 2>/dev/null)" = "$STAMP" ]; then echo "$(date +%T) skip $k (done)"; continue; fi
  echo "$(date +%T) build $k"
  (cd "$ROOT/templates" && GRADE=none python3 build_chapter.py "$J" > "$FULL/chapter/build_$k.log" 2>&1) || { echo "BUILD FAILED $k"; exit 1; }
  echo "$(date +%T) safe-text $k"
  node "$ROOT/templates/check_safe_text.js" "$W/index.html" 0.5 > "$FULL/chapter/safe_$k.txt" 2>&1; echo "  safe-text exit $? ($(tail -1 "$FULL/chapter/safe_$k.txt"))"
  echo "$(date +%T) render $k"
  rm -f "$OUT.part.mp4"
  (cd "$W" && npx -y hyperframes@0.8.188 render --fps 30 --quality standard --output "$OUT.part.mp4" > "$FULL/chapter/render_$k.log" 2>&1) || { echo "RENDER FAILED $k (see chapter/render_$k.log)"; exit 1; }
  mv "$OUT.part.mp4" "$OUT" && echo "$STAMP" > "$OUT.stamp"
  echo "$(date +%T) done $k $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT") s"
done
echo "$(date +%T) ALL CHAPTERS DONE"
