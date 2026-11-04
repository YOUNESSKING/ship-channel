#!/bin/bash
# broll_sheet.sh SRC STEP [START] [END] -> footage/sheets/<stem>_<start>.jpg : one frame every STEP s, timestamp burned in, 6 per row
src="$1"; step="${2:-3}"; a="${3:-0}"; b="${4:-}"
stem=$(basename "$src" .mp4); out="$(dirname "$0")/sheets/${stem}_${a%.*}.jpg"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src"); b=${b:-$dur}
n=$(python3 -c "import math;print(max(1,math.ceil(($b-$a)/$step)))"); rows=$(( (n+5)/6 ))
ffmpeg -v error -y -ss "$a" -t "$(python3 -c "print($b-$a)")" -i "$src" -vf "fps=1/$step,scale=320:-2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:text='%{pts\:hms\:$a}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=6x$rows:padding=2" -frames:v 1 -q:v 4 "$out"
echo "$out"
