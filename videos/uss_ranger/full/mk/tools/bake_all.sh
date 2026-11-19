#!/usr/bin/env bash
# Bake every sea-floor basemap the USS Ranger map scenes use (bake_sea.py, the Oriskany/Mallows/Nevada look).
# Tiles are cached in tools/.tiles (git-ignored); existing jpgs are skipped (delete one to re-bake).
set -e; cd "$(dirname "$0")"
b() { [ -f ../assets/$1.jpg ] && { echo "skip $1"; return; }; python3 bake_sea.py "$@"; }
b americas   2     -85    4    # the whole tow: Bremerton -> around South America -> Brownsville
WATERMASK=osm b puget 47.57 -122.55 10   # Puget Sound: Bremerton (Puget Sound Naval Shipyard), Seattle, Admiralty Inlet
b pnw        46.6  -123.2  8    # Pacific Northwest: Puget Sound + Columbia River + Portland (museum campaign)
WATERMASK=osm b brownsville 26.0 -97.3 10   # Brownsville Ship Channel, Port Isabel, Gulf entrance
b gulfmex    24.5  -90     6    # Gulf of Mexico approach
b magellan   -53.5 -71     7    # Strait of Magellan / Cape Horn
WATERMASK=osm b hampton 36.98 -76.35 10  # Newport News / Hampton Roads (built 1954-57)
b persian    27    51      6    # Persian Gulf (Desert Storm 1991)
b vietnam    17    110     5    # Gulf of Tonkin / Yankee Station
b somalia    3     47      5    # Somalia 1992-93
WATERMASK=osm b sandiego 32.7 -117.2 10   # San Diego / North Island (home port)
