#!/bin/bash
# Arnold maps, v11 look + 2c (no trees, no reservoirs). One map at a time.
cd /home/user/battle-maps/arnold
bake() { n=$1; [ -f logs/$n.done ] && return; python3 tools/bake.py $n $2 $3 $4 $5 && LIFT=1 python3 tools/bake_hd.py $n \
  && NO_RESERVOIR=1 python3 tools/make_detail_layers.py $n && NO_RESERVOIR=1 SIMPLE=1 python3 tools/make_detail_layers.py $n \
  && NO_TREES=1 FULL=1 python3 tools/ref_look_v11.py $n 2880 1620 assets/${n}_hd_lift.jpg && touch logs/$n.done; }
bake saratoga 43.000 -73.635 15 2.0
bake valcour 44.600 -73.420 13 2.0
bake quebec 46.810 -71.210 14 2.0
bake champlain 44.550 -73.300 9 2.0
bake northeast 43.800 -72.500 8 2.0
bake maine 45.600 -70.500 9 2.0
bake champsouth 44.420 -73.380 11 2.0
bake hudson 43.000 -73.600 10 2.0
python3 tools/make_land.py saratoga valcour quebec champlain northeast maine champsouth hudson
for n in saratoga valcour quebec champlain northeast maine champsouth hudson; do python3 tools/make_rivers_dem.py $n || true; done
touch logs/bake.done
