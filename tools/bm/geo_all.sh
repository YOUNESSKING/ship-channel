#!/bin/bash
cd /home/user/battle-maps/grant
python3 tools/fetch_osm.py chatt "34.70,-85.50,35.20,-84.80"
python3 tools/fetch_osm.py tunnel "35.00,-85.35,35.12,-85.15"
python3 tools/fetch_osm.py ringgold "34.88,-85.17,34.98,-85.03"
python3 tools/fetch_osm.py pickett "33.94,-84.85,34.03,-84.72"
for n in chatt tunnel ringgold pickett; do python3 tools/make_geo_layer.py $n ref; done
touch logs/geo.done
