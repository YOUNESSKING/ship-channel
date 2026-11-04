#!/bin/bash
# cut_clips.sh - regenerate patton/assets/film/clips/*.mp4 from public-domain archive.org sources (US Army Signal Corps film in NARA).
# Usage: cd patton/assets/film && bash cut_clips.sh   (downloads ~700 MB into src/ if missing; src/ is not kept)
# Clips: 1920x1080 (4:3 sources cropped to fill 16:9, no black bars), 30 fps, libx264 crf20, no audio. See MANIFEST.md.
set -e
cd "$(dirname "$0")"; mkdir -p src clips
UA="battle-maps-research/1.0 (contact: younessfakiri123@gmail.com)"
dl() { id="$1"; [ -s "src/$id.mp4" ] && return
  for i in 1 2 3; do curl -sS -L -A "$UA" -o "src/$id.mp4" "https://archive.org/download/$id/$id.mp4" && [ -s "src/$id.mp4" ] && break; sleep 5; done; }
for id in ADC-1672b 111-adc-2041 111-adc-3114 ARC-39153 111-adc-9718; do dl $id; done
VF="scale='iw*sar':'ih',setsar=1,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30"
cut() { ffmpeg -y -loglevel error -ss "$2" -i "src/$1.mp4" -t "$3" -vf "$VF" -an -c:v libx264 -crf 20 -pix_fmt yuv420p "clips/$4"; }
# Move 1 end: Avranches / Normandy breakout, Third Army columns, July-Aug 1944

cut 111-adc-2041 380 6 m1_avranches_pows.mp4
cut 111-adc-2041 332 6 m1_columns_pow.mp4
cut 111-adc-2041 750 6 m1_armored_cars.mp4
cut ADC-1672b   124 7 m1_coutances_halftracks.mp4
# Move 2 end: Bastogne, winter 1944-45
cut ARC-39153   348 6 m2_aircraft_snow.mp4
cut ARC-39153   372 6 m2_bundles_tank.mp4
cut ARC-39153   462 7 m2_bastogne_sign.mp4
cut 111-adc-3114  12 6 m2_halftracks_snow.mp4
cut 111-adc-3114 190 7 m2_column_snow.mp4
# Move 3 end: Rhine crossing, 27 Mar 1945
cut 111-adc-9718  70 7 m3_pontoon_ferry.mp4
cut 111-adc-9718 192 7 m3_columns_pontoon.mp4
cut 111-adc-9718 396 7 m3_dukw_gun.mp4
cut 111-adc-9718 430 7 m3_dukw_river.mp4
