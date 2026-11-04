#!/bin/bash
cd /home/user/battle-maps/arnold
n=saratoga
NO_RESERVOIR=1 python3 tools/make_detail_layers.py $n && NO_RESERVOIR=1 SIMPLE=1 python3 tools/make_detail_layers.py $n \
 && NO_TREES=1 FULL=1 python3 tools/ref_look_v11.py $n 2880 1620 assets/${n}_hd_lift.jpg && touch logs/saratoga2.done
