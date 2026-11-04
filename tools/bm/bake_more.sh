#!/bin/bash
# second batch of Patton maps (after bake_all.sh): close-ups and the Europe overview
cd /home/user/battle-maps/grant
bake() { n=$1; python3 tools/bake.py $n $2 $3 $4 $5 && LIFT=1 python3 tools/bake_hd.py $n; }
while [ ! -f logs/bake.done ]; do sleep 10; done
bake lemans 48.0 0.2 12 2.0
bake assenois 49.96 5.69 13 2.0
bake europe 49.8 3.0 7 2.0
python3 tools/make_land.py lemans assenois europe
for n in lemans assenois europe; do python3 tools/make_rivers_dem.py $n || true; done
touch logs/bake2.done
