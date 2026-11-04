#!/usr/bin/env python3
"""mkjson.py NAME LAT LON ZOOM [SEA_LEVEL]  (NEW) writes assets/NAME.json exactly like bake.py does, without baking the (unused) parchment jpg.
Use before bake_hd.py:  SEA_LEVEL=-120 python3 tools/bake_hd.py NAME  (bake_hd reads this json)."""
import sys, json, math, os
n, lat, lon, z = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]); S = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
W, H = 2880, 1620; N = 256*2**z
cx = (lon+180)/360*N; cy = (1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*N
x0, y0 = int(cx-W/2), int(cy-H/2)
os.makedirs("assets", exist_ok=True)
json.dump({"name": n, "center": [lat, lon], "zoom": z, "origin_world_px": [x0, y0], "size": [W, H], "meters_per_px": round(156543.03392*math.cos(math.radians(lat))/2**z, 2),
           "sea_below": 0.5, "sea_level": S, "credit": "Terrain: Mapzen / AWS Terrain Tiles (open data)"}, open(f"assets/{n}.json", "w"), indent=1)
