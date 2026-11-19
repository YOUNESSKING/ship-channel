#!/bin/bash
# make_sheets.sh SRC [STEM] [STEP=2] : contact sheets sheets/<stem>_NN.jpg, one frame every STEP s, timestamp burned in, 6x6 = 36 frames per sheet.
src="$1"; stem="${2:-$(basename "${src%.*}")}"; step="${3:-2}"
cd "$(dirname "$0")/.."; mkdir -p sheets
ffmpeg -v error -y -i "$src" -vf "fps=1/$step,scale=320:240:force_original_aspect_ratio=decrease,pad=320:240:(ow-iw)/2:(oh-ih)/2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:text='%{pts\:hms}':x=6:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.55,tile=6x6" -q:v 4 "sheets/${stem}_%02d.jpg"
