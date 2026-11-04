#!/usr/bin/env bash
# Loudness-normalise audio/mix_raw.wav (about -14 LUFS) and mux it with a silent chapter render. Same chain as v9.
#   ./mux.sh WORK_DIR SILENT_VIDEO.mp4 OUT.mp4
set -euo pipefail
W="$1"; VID="$2"; OUT="$3"; A="$W/audio"
if [ "${LOUDNORM:-0}" = 1 ]; then   # old chain: two-pass loudnorm (falls back to its dynamic mode when the peaks are high, which flattens SFX hits)
M=$(ffmpeg -hide_banner -nostats -i "$A/mix_raw.wav" -af loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$M" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -y -loglevel error -i "$A/mix_raw.wav" -af "loudnorm=I=-14:TP=-1.5:LRA=9:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" "$A/mix_final.wav"
else   # default (owner 30 Oct: SFX must pop): one static gain to -14 LUFS + a fast peak limiter, so only the tips of the hits are touched
ffmpeg -y -loglevel error -i "$A/mix_raw.wav" -af aresample=48000 "$A/mix_final.wav"
fi
I=$(ffmpeg -hide_banner -nostats -i "$A/mix_final.wav" -af ebur128 -f null - 2>&1 | grep -A1 "Integrated loudness" | grep "I:" | tail -1 | awk '{print $2}')
GAIN=$(python3 -c "print(round(-14-($I),2))")
# 10 ms fades at both ends: chapters join without clicks even when the music bed continues across the cut (FADE_MS=0 disables)
FMS=${FADE_MS:-10}; DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$A/mix_final.wav")
EDGE=$(python3 -c "d=$DUR;f=$FMS/1000;print(('afade=t=in:d=%g,afade=t=out:st=%g:d=%g' % (f,d-f,f)) if f>0 else 'anull')")
ffmpeg -y -loglevel error -i "$A/mix_final.wav" -af "volume=${GAIN}dB,alimiter=limit=0.84:attack=1:release=40:level=false,$EDGE" "$A/mix_final2.wav" && mv "$A/mix_final2.wav" "$A/mix_final.wav"
# audio is padded / cut to the exact picture length, so chapters concatenate with no gap and no drift
VD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VID")
ffmpeg -y -loglevel error -i "$VID" -i "$A/mix_final.wav" -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p -r 30 -af apad -c:a aac -b:a 192k -ac 2 -movflags +faststart -t "$VD" "$OUT"
echo "muxed $OUT"
