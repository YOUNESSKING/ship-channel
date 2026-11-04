#!/bin/bash
# owner 2026-11-01: trees only along the MAIN river (MAIN_ONLY), no modern reservoirs (NO_RESERVOIR; NO_AREAS where the NHD river polygons ARE the reservoir: Cumberland/Tennessee).
cd /home/user/battle-maps/grant
one() { n=$1; open=$2; xenv=$3
  env NO_RESERVOIR=1 $xenv python3 tools/make_detail_layers.py $n && env NO_RESERVOIR=1 $xenv SIMPLE=1 python3 tools/make_detail_layers.py $n \
  && NO_TREES=1 MAIN_ONLY=1 RIV_OPEN=$open FULL=1 python3 tools/ref_look_v11.py $n 2880 1620 assets/${n}_hd_lift.jpg && touch logs/trees_$n.done; }
one donelson 12 NO_AREAS=1
one henry 12 NO_AREAS=1
one tennessee 12 NO_AREAS=1
one vicksburg 16 X=1
one grandgulf 16 X=1
one vicksburg_siege 16 X=1
one mississippi 16 X=1
one jamesriver 16 X=1
one petersburg 10 X=1
one richmond 12 X=1
touch logs/trees.done
