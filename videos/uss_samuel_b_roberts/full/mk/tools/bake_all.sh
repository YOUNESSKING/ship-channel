#!/usr/bin/env bash
# Bake every sea-floor basemap the USS Samuel B. Roberts map scenes use (bake_sea.py; DEEP=1 = deep-ocean ramp + 2-8 km contours).
# Tiles are cached in tools/.tiles (git-ignored); existing jpgs are skipped (delete one to re-bake).
set -e; cd "$(dirname "$0")"
b() { [ -f ../assets/$1.jpg ] && { echo "skip $1"; return; }; python3 bake_sea.py "$@"; }
DEEP=1 b wpac      12    132   4    # Western Pacific: Philippines, Philippine Sea, Marianas, Japan's approaches
DEEP=1 b leyte     11.5  126   7    # Leyte Gulf, Samar, San Bernardino Strait, Surigao Strait, Philippine Trench
DEEP=1 b samar     11.6  126.3 8    # off Samar: the battle area and the wreck site above the trench
DEEP=1 b trench    11.6  126.6 9    # close: the trench slope at the wreck site
b gulf_houston     29.4  -94.8 8    # Houston / Galveston (built at Brown Shipbuilding, Houston)
b solomons         -9.3  159.9 8    # Guadalcanal (namesake Samuel B. Roberts, Sept 1942)
