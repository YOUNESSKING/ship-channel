#!/usr/bin/env bash
# Join v9 (picture and sound exactly as is) + a muxed chapter video. Picture is stream-copied; audio is joined with a 20 ms fade-in on the chapter.
#   ./join_v9.sh V9.mp4 CHAPTER_MUXED.mp4 OUT.mp4
set -euo pipefail
V9="$1"; CH="$2"; OUT="$3"; T=$(mktemp -d)
printf "file '%s'\nfile '%s'\n" "$(realpath "$V9")" "$(realpath "$CH")" > "$T/l.txt"
ffmpeg -y -loglevel error -f concat -safe 0 -i "$T/l.txt" -an -c:v copy "$T/v.mp4"
ffmpeg -y -loglevel error -i "$V9" -i "$CH" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[a];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.02[b];[a][b]concat=n=2:v=0:a=1[o]" -map "[o]" -c:a aac -b:a 192k "$T/a.m4a"
ffmpeg -y -loglevel error -i "$T/v.mp4" -i "$T/a.m4a" -c copy -movflags +faststart "$OUT"
echo "joined $OUT"; rm -rf "$T"
