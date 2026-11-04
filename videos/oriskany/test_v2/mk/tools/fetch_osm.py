"""Fetch geography for a basemap from OpenStreetMap (Overpass; data (c) OpenStreetMap contributors, ODbL - credit on screen).
usage: python3 tools/fetch_osm.py BASE "S,W,N,E (focus box for villages/forests/streams)"  -> assets/src/BASE_osm.json"""
import json, math, sys, time, urllib.parse, urllib.request
base, focus = sys.argv[1], sys.argv[2]
J = json.load(open(f"assets/{base}.json")); z = J["zoom"]; ox, oy = J["origin_world_px"]; W, H = J["size"]
def ll(px, py):
    n = 256 * 2 ** z; lon = (px + ox) / n * 360 - 180; lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (py + oy) / n)))); return lat, lon
s, w = ll(0, H); n_, e = ll(W, 0); full = f"{s:.4f},{w:.4f},{n_:.4f},{e:.4f}"
URL = "https://overpass.private.coffee/api/interpreter"
def q(body):
    for k in range(4):
        try:
            data = urllib.parse.urlencode({"data": "[out:json][timeout:180];" + body}).encode()
            return json.load(urllib.request.urlopen(urllib.request.Request(URL, data=data), timeout=200))["elements"]
        except Exception as ex:
            print("retry", k, ex, flush=True); time.sleep(5 * (k + 1))
    raise SystemExit("overpass failed")
import os
path = f"assets/src/{base}_osm.json"
out = json.load(open(path)) if os.path.exists(path) else {}
out.update({"bbox": full, "focus": focus})
JOBS = {"places": f'(node["place"~"^(city|town)$"]({full});node["place"="village"]({focus}););out;',
        "rivers": f'way["waterway"~"^(river|canal)$"]({os.environ.get("RIVERBOX", full)});out geom;',
        "lakes": f'way["natural"="water"]({focus});out geom;',
        "streams": f'way["waterway"="stream"]({focus});out geom;',
        "forest": f'(way["landuse"="forest"]({focus});way["natural"="wood"]({focus}););out geom;'}
for k, body in JOBS.items():
    if k in out: continue
    t = time.time(); out[k] = q(body); json.dump(out, open(path, "w")); print(k, len(out[k]), f"{time.time() - t:.0f}s", flush=True)
print({k: len(v) for k, v in out.items() if isinstance(v, list)})
