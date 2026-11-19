#!/bin/bash
# make_overview.sh SRC STEP : one-sheet overview (6x6, 1 frame per STEP s) in scratch/ov/<stem>_ov.jpg for fast review
src="$1"; step="${2:-10}"; stem="$(basename "${src%.*}")"
cd "$(dirname "$0")/.."; mkdir -p scratch/ov
ffmpeg -v error -y -i "$src" -vf "fps=1/$step,scale=320:240:force_original_aspect_ratio=decrease,pad=320:240:(ow-iw)/2:(oh-ih)/2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:text='%{pts\:hms}':x=6:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.55,tile=6x6" -frames:v 1 -q:v 4 "scratch/ov/${stem}_ov.jpg"
