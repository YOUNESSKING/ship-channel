#!/usr/bin/env bash
# Sound for every rendered chapter, loudness + mux per chapter, then join into ../preview/v02_draft_720p.mp4. 3 CPU cores.
# Four layers (GOLD 99-100, fixpass/SOUND.md): environment beds (env:), things (el:, library ../sfx_el), mood (music bed + heart/hit/boom
# + stings), graphics (synth). Music never stops: hook score until the drop (0.6 s silence, rule 30), then ONE continuous lo-fi bed from
# the end of the drop through the end screen (sliced per chapter, so chapters join with no seam).
# Levels: voice ~12 LU over the sound design under speech, bed up ~5 LU in pauses; mux.sh sets -14 LUFS.
set -euo pipefail
cd "$(dirname "$0")"
KEYS="ch00 ch01 ch02 ch03 ch04 ch05 ch06 ch07 ch08 ch09 ch10 ch11 ch12 final"
WORK=${WORK:-work}; REND=${REND:-rendered}; OUTD=${OUTD:-final_mix}; OUT=${OUT:-../preview/v02_draft_720p.mp4}
VOICE=../voice/narration_full.mp3; BED=final_mix/lofi_bed.wav; mkdir -p final_mix $OUTD "$(dirname $OUT)"
MIX="taskset -c 0-2 python3 ../../../templates/mix_audio.py --amb-db -30 --amb-gap-db -23 --sfx-db 10 --things-db 6"   # owner 30 Oct: SFX must pop (+4 dB), environment beds out of the way (-8 dB)
MUS="--music-db -20 --music-gap-db -12"         # lo-fi bed: 20 dB under the voice while it speaks, 12 dB under in pauses (owner 30 Oct: music too loud, -6 dB)
# ch00 music = hook score, the silent drop, then the lo-fi bed (same rms as the score) from the end of the drop
DROP_END=$(python3 -c "import json;e=json.load(open('$WORK/ch00/sfx_events.json'));d=[x for x in e['inserts'] if x['id']=='drop'][0];print(round(d['at']+d['dur'],3))")
python3 - "$WORK/ch00/sfx_events.json" $DROP_END <<'EOF'
import sys, json, wave, numpy as np
d = json.load(open(sys.argv[1]))['duration']; t0 = float(sys.argv[2]); SR = 44100
def rd(p):
    with wave.open(p) as w: return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
h = rd('final_mix/hook_music.wav'); b = rd('final_mix/lofi_bed.wav')[:int((d - t0 + .5) * SR)].copy()
r = lambda x: np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2)); b *= r(h) / r(b); f = int(.7 * SR); b[:f] *= np.linspace(0, 1, f)
y = np.zeros(int((d + .5) * SR)); y[:len(h)] = h; i = int(t0 * SR); y[i:i + len(b)] += b[:len(y) - i]
with wave.open('final_mix/ch00_music.wav', 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
EOF
moff=$(python3 -c "import json;print(round(json.load(open('$WORK/ch00/sfx_events.json'))['duration']-$DROP_END,3))"); : > $OUTD/list.txt; ABS=$(cd $OUTD && pwd)
for k in $KEYS; do
  d=$(python3 -c "import json;print(json.load(open('$WORK/$k/sfx_events.json'))['duration'])")
  if [ "$k" = ch00 ]; then
    $MIX $WORK/$k --voice $VOICE --music final_mix/ch00_music.wav --music-db -21 --music-gap-db -13 > /dev/null   # hook score (make_hook_music.py), hard stop on the drop, then the bed
  else
    lift=""; [ "$k" = final ] && lift="--music-lift $(python3 -c "print(round($d-10,2))"),8"
    $MIX $WORK/$k --voice $VOICE --music $BED --music-offset $moff $MUS --music-fade-in 0 $lift > /dev/null
    moff=$(python3 -c "print($moff+$d)")
  fi
  taskset -c 0-2 ../../../templates/mux.sh $WORK/$k $REND/$k.mp4 $OUTD/$k.mp4 > /dev/null
  echo "file '$ABS/$k.mp4'" >> $OUTD/list.txt; echo "mixed $k ($d s)"
done
taskset -c 0-2 ffmpeg -y -loglevel error -f concat -safe 0 -i $OUTD/list.txt -c copy -movflags +faststart $OUT
ls -la $OUT
