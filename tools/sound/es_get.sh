#!/usr/bin/env bash
# es_get.sh <file.wav> <signed url>: fetch an Epidemic WAV and convert it to 48 kHz / 24-bit into assets/sfx/epidemic/
set -e; D="$(cd "$(dirname "$0")/../.." && pwd)/assets/sfx/epidemic"; mkdir -p "$D"
T=$(mktemp /dev/shm/es_XXXX.wav); curl -sSL -o "$T" "$2"; ffmpeg -v error -y -i "$T" -ar 48000 -c:a pcm_s24le "$D/$1"; rm -f "$T"; echo "ok $1"
