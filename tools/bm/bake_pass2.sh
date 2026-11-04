#!/bin/bash
# pass 2 (after bake_all + DEM rivers): islands punched out, Canada water via WorldCover, modern reservoirs/canals erased
cd /home/user/battle-maps/arnold
two() { n=$1; shift; [ -f logs/${n}_p2.done ] && return; env NO_RESERVOIR=1 "$@" python3 tools/make_detail_layers.py $n && env NO_RESERVOIR=1 SIMPLE=1 "$@" python3 tools/make_detail_layers.py $n \
  && NO_TREES=1 FULL=1 python3 tools/ref_look_v11.py $n 2880 1620 assets/${n}_hd_lift.jpg && touch logs/${n}_p2.done; }
two quebec WIDE=1
two valcour X=1
two saratoga X=1
two maine "ERASE=45.25,-70.52,45.12,-70.17;45.23,-69.96,45.04,-69.84"
two champsouth X=1
two champlain X=1
two northeast "ERASE=45.25,-70.52,45.12,-70.17"
two hudson X=1
touch logs/pass2.done
