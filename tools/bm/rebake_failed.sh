#!/bin/bash
cd /home/user/battle-maps/grant
while pgrep -f "tools/bake_all.sh" >/dev/null; do sleep 15; done
for n in grandgulf vicksburg_siege mississippi jamesriver petersburg richmond; do
  [ -f logs/$n.done ] || { FULL=1 python3 tools/ref_look_v11.py $n 2880 1620 assets/${n}_hd_lift.jpg && touch logs/$n.done; }
done
python3 tools/make_land.py grandgulf vicksburg_siege mississippi jamesriver petersburg richmond
for n in grandgulf vicksburg_siege mississippi jamesriver petersburg richmond; do python3 tools/make_rivers_dem.py $n || true; done
touch logs/rebake.done
