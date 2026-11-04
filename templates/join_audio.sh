#!/usr/bin/env bash
# Per-chapter audio for the final join: mux.sh loudness chain, but no edge fades, no silence pad (audio is resampled by a hair to the exact picture length) so the music bed runs across chapter joins. usage: join_audio.sh WORK_DIR FADEIN_MS FADEOUT_MS OUT.wav VIDEO_DUR
set -euo pipefail
A="$1/audio"; FI="$2"; FO="$3"; OUT="$4"; VD="$5"
M=$(ffmpeg -hide_banner -nostats -i "$A/mix_raw.wav" -af loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$M" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
T=$(mktemp -d)
ffmpeg -y -loglevel error -i "$A/mix_raw.wav" -af "loudnorm=I=-14:TP=-1.5:LRA=9:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" $T/f.wav
I=$(ffmpeg -hide_banner -nostats -i $T/f.wav -af ebur128 -f null - 2>&1 | grep -A1 "Integrated loudness" | grep "I:" | tail -1 | awk '{print $2}')
GAIN=$(python3 -c "print(round(-14-($I),2))")
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $T/f.wav)
EDGE=$(python3 -c "
d=float('$VD');p=[]
if $FI>0: p.append('afade=t=in:d=%g'%($FI/1000))
if $FO>0: p.append('afade=t=out:st=%g:d=%g'%(d-$FO/1000,$FO/1000))
print(','.join(p) or 'anull')")
TEMPO=$(python3 -c "print($DUR/$VD)")
ffmpeg -y -loglevel error -i $T/f.wav -af "apad=pad_dur=0.1,volume=${GAIN}dB,alimiter=limit=0.84:level=false,atrim=start=0.005,asetpts=PTS-STARTPTS" $T/g.wav
ffmpeg -y -loglevel error -i $T/g.wav -af "aformat=sample_rates=48000:channel_layouts=stereo,asetrate=$(python3 -c "print(round(48000*$TEMPO))"),aresample=48000,apad,atrim=end=$VD,$EDGE" -c:a pcm_s16le "$OUT"
rm -rf $T
