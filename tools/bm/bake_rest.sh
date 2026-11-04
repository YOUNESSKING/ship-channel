#!/bin/bash
cd /home/user/battle-maps/arnold
bake() { n=$1; shift; [ -f logs/$n.done ] && return; python3 tools/bake.py $n $1 $2 $3 $4 && LIFT=1 python3 tools/bake_hd.py $n && touch logs/${n}_raw.done; }
bake champsouth 44.420 -73.380 11 2.0
bake hudson 43.000 -73.600 10 2.0
python3 tools/make_land.py saratoga valcour quebec champlain northeast maine champsouth hudson
for n in saratoga valcour quebec champlain northeast maine champsouth hudson; do python3 tools/make_rivers_dem.py $n || true; done
touch logs/bake.done
two() { n=$1; shift; [ -f logs/${n}_p2.done ] && return; env NO_RESERVOIR=1 "$@" python3 tools/make_detail_layers.py $n && env NO_RESERVOIR=1 SIMPLE=1 "$@" python3 tools/make_detail_layers.py $n \
  && NO_TREES=1 FULL=1 python3 tools/ref_look_v11.py $n 2880 1620 assets/${n}_hd_lift.jpg && touch logs/${n}_p2.done; }
two quebec WIDE=1
two valcour WIDE=1
two saratoga X=1
two maine "ERASE=45.25,-70.52,45.12,-70.17;45.23,-69.96,45.04,-69.84"
two champsouth WIDE=1
two champlain X=1
two northeast "ERASE=45.25,-70.52,45.12,-70.17"
two hudson X=1
touch logs/pass2.done
