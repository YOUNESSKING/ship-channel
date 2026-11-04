#!/usr/bin/env bash
# Re-assemble the full video (1080p master + 720p preview) and bring both to ~-14 LUFS (Gavin lesson: the linear
# loudnorm stops at ~-15 with the peaky TTS voice). Detached; progress in logs/finalize.log, marker logs/finalize.done
set -u
cd "$(dirname "$0")/.."
if [ -z "${FIN_DETACHED:-}" ]; then
  mkdir -p logs; rm -f logs/finalize.done
  FIN_DETACHED=1 setsid nohup bash "$0" > logs/finalize.log 2>&1 < /dev/null &
  echo "finalize started (pid $!)"; exit 0
fi
ok=1
python3 tools/assemble_full.py || ok=0
python3 tools/assemble_full.py --preview || ok=0
if [ $ok = 1 ]; then
  ffmpeg -v error -y -i build/mix.wav -af "volume=11.8dB,alimiter=limit=0.8:attack=2:release=80:level=false,aresample=48000" -c:a pcm_s16le build/mix_final.wav || ok=0
  for H in 1080 720; do
    OUT=$([ $H = 1080 ] && echo build/arnold.mp4 || echo build/arnold-720p.mp4)
    D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 build/video_only_${H}p.mp4)
    ffmpeg -v error -y -i build/video_only_${H}p.mp4 -i build/mix_final.wav -map 0:v -map 1:a -t "$D" -c:v copy -c:a aac -b:a 192k -movflags +faststart build/tmp_$H.mp4 && mv build/tmp_$H.mp4 $OUT || ok=0
  done
fi
echo "ok=$ok" > logs/finalize.done
