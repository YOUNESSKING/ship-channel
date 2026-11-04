#!/usr/bin/env bash
# Sinking preview: render (headless Chrome, ~1 min) -> mix the kit SFX on the cues -> MP4 (git-ignored) + contact sheet JPG (committed).
# usage: bash kit/ship/sinking/make_preview.sh ["query string"]   e.g. "ship=liner&depth=180&dur=8&mode=upright&title=SS%20UNITED%20STATES"
set -euo pipefail
cd "$(dirname "$0")"
Q="${1:-title=USS%20ORISKANY&sub=GULF%20OF%20MEXICO%20%C2%B7%2017%20MAY%202006&settle=10&settleLabel=STORMS%20PUSHED%20HER%20~10%20FT%20INTO%20THE%20SAND%20BY%202008}"
mkdir -p out
[ -f ../sfx/out/number_land_1.wav ] || python3 ../sfx/make_sfx.py
NODE_PATH=$(npm root -g) node ../tools/render_frames.js "sinking.html?$Q" out/sinking_preview_noaudio.mp4 30
python3 mix_cues.py out/sinking_preview_noaudio.mp4 out/sinking_preview.mp4
ffmpeg -y -loglevel error -i out/sinking_preview_noaudio.mp4 -vf "select='not(mod(n\,31))',scale=480:-1,tile=3x3:padding=6:color=0x0b141c" -frames:v 1 -q:v 5 sinking_contact_sheet.jpg
ls -la out/sinking_preview.mp4 sinking_contact_sheet.jpg
