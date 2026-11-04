#!/bin/bash
# owner 2026-11-01: trees ONLY along the main river (MAIN_ONLY=1), not every pocket/bay/oxbow. One bake at a time (memory).
cd /home/user/battle-maps/grant
for spec in donelson:16 henry:16 tennessee:16 vicksburg:16 grandgulf:16 vicksburg_siege:16 mississippi:16 jamesriver:16 petersburg:10 richmond:12; do
  n=${spec%%:*}; o=${spec##*:}
  MAIN_ONLY=1 RIV_OPEN=$o FULL=1 python3 tools/ref_look_v11.py $n 2880 1620 assets/${n}_hd_lift.jpg && touch logs/trees_$n.done
done
touch logs/trees.done
