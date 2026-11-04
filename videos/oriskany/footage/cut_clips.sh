#!/bin/bash
# cut_clips.sh - regenerate videos/oriskany/footage/src/clips/*.mp4 from public-domain NARA film (US Navy RG 428, OWI RG 208).
# Usage: bash videos/oriskany/footage/cut_clips.sh            (MODE=pillar, default: 4:3 kept whole, black pillarbox)
#        MODE=fill bash videos/oriskany/footage/cut_clips.sh  (4:3 scaled + cropped to fill 16:9, Patton recipe)
# Downloads ~1.9 GB of NARA mp4 into src/film/ if missing (git-ignored). Clips: 1920x1080, 30 fps, crf 20, no audio, <= 6 s.
# In/out points were picked from 5-10 s contact sheets: re-check each clip by eye before it goes in a shot list.
# See FOOTAGE_LIST.md for what each clip shows and does NOT show.
set -e
cd "$(dirname "$0")"; mkdir -p src/film src/clips
UA="ship-channel-research/1.0 (contact: younessfakiri123@gmail.com)"
MODE=${MODE:-pillar}
dl() { id="$1"; url="$2"; [ -s "src/film/nara_$id.mp4" ] && return
  for i in 1 2 3; do curl -sS -L -C - -A "$UA" -o "src/film/nara_$id.mp4" "$url" && [ -s "src/film/nara_$id.mp4" ] && break; sleep 5; done; }
M=https://catalog.archives.gov/medialz/mopix/428/NPC
dl 39085 https://catalog.archives.gov/medialz/mopix/208/un/208-un-177_5Mbps.mp4
dl 78776 $M/428-npc-9584.mp4
dl 80446 $M/428-npc-16662.mp4
dl 85461 $M/428-npc-37479.mp4
dl 85446 $M/428-npc-37453.mp4
dl 85477 $M/428-npc-37521.mp4
dl 85479 $M/428-npc-37523.mp4
dl 85493 $M/428-npc-37596.mp4
dl 86313 $M/428-npc-39916.mp4
dl 86638 $M/428-npc-40802.mp4
dl 86031 $M/428-npc-39180.mp4
dl 87411 $M/428-npc-43159.mp4
dl 86032 $M/428-npc-39181.mp4
if [ "$MODE" = fill ]; then
  VF="scale='iw*sar':'ih',setsar=1,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30"
else
  VF="scale='iw*sar':'ih',setsar=1,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,fps=30"
fi
# 208-UN-177 is already pillarboxed inside a 1920x1080 frame: cut the 4:3 picture out first.
PRE_39085="crop=1440:1080:240:0,"
cut() { pre=""; [ "$1" = 39085 ] && pre="$PRE_39085"
  ffmpeg -y -loglevel error -ss "$2" -i "src/film/nara_$1.mp4" -t "$3" -vf "${pre}$VF" -an -c:v libx264 -crf 20 -pix_fmt yuv420p "src/clips/$4"; }

# Beat 1 - launch, 13 Oct 1945 (United News newsreel 208-UN-177)
cut 39085  42 6 b1_launch_crowd.mp4
cut 39085  53 6 b1_launch_bow.mp4
cut 39085  62 6 b1_launch_hull.mp4
# Beat 2 - early 1950s / Korea-era flight deck
cut 78776  11 6 b2_f9f_panther_deck.mp4
cut 78776  17 6 b2_f4u_corsair_landing.mp4
cut 78776  35 6 b2_bomb_rolls_explodes.mp4
cut 80446  80 6 b2_aj1_savage_taxi_1952.mp4
cut 80446 150 6 b2_aj1_savage_landing_1952.mp4
cut 80446 197 5 b2_oriskany_at_anchor_1952.mp4
# Beat 3 - Vietnam flight operations 1966-69 (colour)
cut 85461 118 6 b3_a4_catapult_1966.mp4
cut 85461 184 5 b3_f8_launch_1966.mp4
cut 85461 328 6 b3_f8_vf162_trap_1966.mp4
cut 85461 500 6 b3_unrep_oiler_1966.mp4
cut 85461 600 6 b3_bow_on_underway_1966.mp4
cut 85446 340 4 b3_island_34_1966.mp4
cut 85446 540 6 b3_carrier_aerial_1966.mp4
cut 86313  15 6 b3_island_a4e_parked_1968.mp4
cut 86313 212 6 b3_a4e_bombs_wing_1968.mp4
cut 86313 344 6 b3_deck_parked_1968.mp4
cut 86313 448 6 b3_a4e_launch_1968.mp4
cut 86638  10 6 b3_a4e_formation_1968.mp4
cut 86638 198 6 b3_strike_smoke_1968.mp4
cut 86638 470 6 b3_strike_fire_1968.mp4
cut 86031   8 6 b3_aerial_launching.mp4
cut 86031  40 6 b3_side_launch.mp4
cut 87411   8 6 b3_aerial_underway_1969.mp4
cut 87411  24 6 b3_helo_deck_1969.mp4
cut 87411  60 6 b3_aerial_underway2_1969.mp4
# Beat 4 - the fire, 26 Oct 1966, and the burial at sea, 6 Nov 1966
cut 85477 100 6 b4_fire_hose_lines.mp4
cut 85477 170 5 b4_fire_burned_a4.mp4
cut 85477 230 6 b4_fire_destroyer_alongside.mp4
cut 85477 250 6 b4_fire_island_smoke.mp4
cut 85477 280 6 b4_fire_deck_smoke.mp4
cut 85477 440 6 b4_fire_damaged_a4_316.mp4
cut 85479  40 6 b4_fire_hangar_sprinkler.mp4
cut 85479 140 6 b4_fire_hangar_hoses.mp4
cut 85479 240 6 b4_fire_sponson_hoses.mp4
cut 85479 440 6 b4_fire_oba_team.mp4
cut 85493 120 6 b4_burial_color_guard.mp4
cut 85493 200 6 b4_burial_formation.mp4
cut 85493 440 6 b4_burial_escorts.mp4
# Beat 10 - SS United States, US Navy film 1968 (428-NPC-39181)
cut 86032   9 6 b10_ssus_crane_river.mp4
cut 86032  19 6 b10_ssus_stacks.mp4
cut 86032  59 6 b10_ssus_bow_letters.mp4
cut 86032  65 6 b10_ssus_underway_side.mp4
cut 86032 110 6 b10_ssus_bow_wave.mp4
cut 86032 130 6 b10_ssus_passing_carrier.mp4
cut 86032 150 6 b10_ssus_profile.mp4
echo "clips done: $(ls src/clips | wc -l)"
