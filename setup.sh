#!/bin/bash
# Installs everything the video pipeline needs. Safe to run more than once.
# Runs automatically in the background when a Claude Code session starts (see .claude/settings.json).
# Progress: /tmp/battle-maps-setup.log   Done marker: /tmp/battle-maps-setup.done
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
log(){ echo "[setup $(date +%H:%M:%S)] $*"; }
command -v ffmpeg >/dev/null || { log "ffmpeg"; (apt-get update -qq && apt-get install -y -qq ffmpeg) >/dev/null 2>&1 || sudo apt-get install -y -qq ffmpeg >/dev/null 2>&1; }
command -v hyperframes >/dev/null || { log "hyperframes"; npm install -g hyperframes >/dev/null 2>&1; }
log "python packages"; pip install -q numpy pillow kokoro-onnx soundfile "rembg[cpu]" reportlab fonttools brotli pypdfium2 >/dev/null 2>&1
log "depth model + photo/whisper deps"; pip install -q onnxruntime opencv-python-headless faster-whisper av==15.1.0 pyloudnorm >/dev/null 2>&1
[ -f /opt/models/depth_anything_v2_small.onnx ] || { mkdir -p /opt/models; curl -sSL -o /opt/models/depth_anything_v2_small.onnx "https://huggingface.co/onnx-community/depth-anything-v2-small/resolve/main/onnx/model.onnx"; }   # Small = Apache 2.0 (never Base/Large: CC BY-NC)
log "chrome for rendering"; hyperframes browser ensure >/dev/null 2>&1
if [ ! -d "$HOME/.claude/skills/hyperframes" ]; then
  log "claude skills"; cd /tmp
  npx -y skills add heygen-com/hyperframes -g -a claude-code -s '*' -y --copy >/dev/null 2>&1
  npx -y skills add remotion-dev/skills -g -a claude-code -s '*' -y --copy >/dev/null 2>&1
fi
cd "$ROOT/tts"
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -f "$f" ] || { log "voice model $f"; curl -sSL -o "$f" "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"; }
done
for p in hannibal ridgway; do  # the pipeline reads voice.wav; the repo stores mp3
  [ -f "$ROOT/$p/audio/voice.wav" ] || ffmpeg -v error -y -i "$ROOT/$p/audio/voice.mp3" -ar 24000 "$ROOT/$p/audio/voice.wav"
done
[ -f "$ROOT/ridgway/assets/media/music.wav" ] || ffmpeg -v error -y -i "$ROOT/ridgway/assets/media/music.mp3" -ar 48000 "$ROOT/ridgway/assets/media/music.wav"
log "done"; touch /tmp/battle-maps-setup.done
