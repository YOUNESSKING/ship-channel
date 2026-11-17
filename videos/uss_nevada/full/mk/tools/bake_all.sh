#!/usr/bin/env bash
# Bake every sea-floor basemap the USS Nevada map scenes use (bake_sea.py, the Oriskany/Mallows look).
# Tiles are cached in tools/.tiles (git-ignored); existing jpgs are skipped (delete one to re-bake).
set -e; cd "$(dirname "$0")"
b() { [ -f ../assets/$1.jpg ] && { echo "skip $1"; return; }; python3 bake_sea.py "$@"; }
b pearl     21.355 -157.955 13   # Pearl Harbor: Battleship Row, Ford Island, channel, Hospital Point
b oahu      21.15  -158.3   9    # Oahu + the 1948 sinking area ~65 nmi SW of Pearl Harbor
b hawaii    20.5   -157.5   7    # main Hawaiian islands
b pacific   22     170      4    # Pearl Harbor -> Bikini -> Kwajalein -> Iwo Jima / Okinawa
b bikini    11.6   165.45   11   # Bikini Atoll lagoon (target array)
b normandy  49.6   -1.0     9    # Utah Beach, Cotentin, Cherbourg
b channel   50.0   -2.0     7    # English Channel, Normandy and southern France context
b medit     43.0   6.5      8    # Operation Dragoon, Provence coast
