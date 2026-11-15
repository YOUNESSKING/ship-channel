#!/usr/bin/env bash
# Bake every sea-floor basemap the full Oriskany map scenes use (same look as test_v4/mk bake_sea.py).
# Tiles are cached in tools/.tiles; existing jpgs are skipped (delete one to re-bake). gulf_pan + pan_close come from test v4.
set -e; cd "$(dirname "$0")"
[ -f ../assets/grain.png ] || cp ../../../../../map-kit/assets/grain.png ../assets/grain.png   # same grain as the map-kit
[ -f ../assets/gulf_pan.jpg ] || cp ../../../test_v4/mk/assets/{gulf_pan,pan_close}.jpg ../assets/ 2>/dev/null || true
b() { [ -f ../assets/$1.jpg ] && { echo "skip $1"; return; }; python3 bake_sea.py "$@"; }
b pacific   30   -172   4     # North Pacific: Bremerton, SF, Tokyo Bay, Gulf of Tonkin
b americas  -8   -85    4     # 1999 tow: SF -> Cape Horn -> Beaumont
b westcoast 42.5 -124.5 6     # Bremerton -> San Francisco tow
b pnw       47.6 -122.9 8     # Puget Sound / Bremerton
b sfbay     38.0 -122.35 9    # San Francisco Bay / Mare Island
b nyc       40.68 -73.98 10   # New York harbour / Brooklyn Navy Yard
b korea     39.5 131    6     # Korea + Sea of Japan
b vietnam   19.5 106.8  7     # North Vietnam, Gulf of Tonkin, Yankee Station
b hanoi     21.03 105.84 10   # Hanoi close
b usse      33   -87    6     # US South-East + Gulf states, D.C., Atlanta
b gulf7     28.5 -91    7     # Gulf coast: Corpus Christi, Beaumont, Pensacola, hurricane tracks
