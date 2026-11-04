#!/usr/bin/env bash
# build_v01.sh SCENE ID : builds scenes/SCENE for map ID (copies only ID_* media)
cd "$(dirname "$0")/.."; MEDIA_PREFIX=$2_ python3 tools/build_scene.py $1 ${3:-$2_lgm_hd_ref} v01-${4:-$2} v01-${4:-$2}
