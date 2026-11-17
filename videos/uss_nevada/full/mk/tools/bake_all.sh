#!/usr/bin/env bash
# Bake every sea-floor basemap the USS Nevada map scenes use (bake_sea.py, the Oriskany/Mallows look).
# Tiles are cached in tools/.tiles (git-ignored); existing jpgs are skipped (delete one to re-bake).
set -e; cd "$(dirname "$0")"
b() { [ -f ../assets/$1.jpg ] && { echo "skip $1"; return; }; python3 bake_sea.py "$@"; }
# WATERMASK=osm: OSM coastline (Overpass, cached in .tiles) overrides the DEM land/sea (Terrarium shows Pearl Harbor as land)
WATERMASK=osm b pearl     21.345 -157.965 14   # Pearl Harbor (~25.6 km wide): Ford Island, Battleship Row, channel, Hospital Point, Waipio
SS=1 WATERMASK=osm b pearl_row 21.362 -157.950 15   # closer: Battleship Row / Ford Island (~12.8 km wide; SS=1: Terrarium has no z16)
WATERMASK=osm b oahu      21.15  -158.3   9    # Oahu + the 1948 sinking area ~65 nmi SW of Pearl Harbor
b hawaii    20.5   -157.5   7    # main Hawaiian islands
b pacific   22     170      4    # Pearl Harbor -> Bikini -> Kwajalein -> Iwo Jima / Okinawa
b bikini    11.6   165.45   11   # Bikini Atoll lagoon (target array)
b normandy  49.6   -1.0     9    # Utah Beach, Cotentin, Cherbourg
b channel   50.0   -2.0     7    # English Channel, Normandy and southern France context
b medit     43.0   6.5      8    # Operation Dragoon, Provence coast
# --- added for the Nevada map scenes ---
b bikini_close 11.585 165.50 14   # Bikini lagoon close: Able miss (1/3 mile), Baker rings (240 / 380 / 1,060 yd)
b marshalls 10.2 166.6 8          # Bikini + Kwajalein
b northpac  50.5 -178 5           # Attu / Aleutians
b atlantic  42 -38 5              # US east coast -> Britain / Normandy
WATERMASK=osm b oahu_sw 21.1 -158.45 10   # Oahu + the 1948 sinking area (~65 nmi SW of Pearl Harbor), search box 10x10 nmi
