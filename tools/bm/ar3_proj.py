"""Arnold #17 map agent (scenes m3a, m3b, hook-a, hook-b; prefix ar3_): lat/lon -> basemap px; marks the places on a preview.
usage: python3 tools/ar3_proj.py MAP OUT.jpg [x0,y0,x1,y1]"""
import json, math, os, sys
from PIL import Image, ImageDraw
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def meta(m):
    f = f"{ROOT}/assets/{m}_hd_lift.json"
    if not os.path.exists(f): f = f"{ROOT}/assets/{m}.json"
    return json.load(open(f))
def proj(m):
    J = meta(m); Z, (OX, OY) = J["zoom"], J["origin_world_px"]
    def P(lat, lon):
        n = 256 * 2 ** Z; r = math.radians(lat)
        return ((lon + 180) / 360 * n - OX, (1 - math.asinh(math.tan(r)) / math.pi) / 2 * n - OY)
    return P
PL0 = {"BEMIS": (42.985, -73.620), "FREEMAN": (43.003, -73.640), "WHEAT": (42.995, -73.645), "LIGHTINF": (43.005, -73.636),
      "BREYMANN": (43.0084, -73.6394), "SARATOGA": (43.10, -73.58), "ALBANY": (42.65, -73.75), "TICONDEROGA": (43.843, -73.387),
      "SKENESBOROUGH": (43.555, -73.404), "FT EDWARD": (43.267, -73.585), "QUEBEC": (46.81, -71.21), "MONTREAL": (45.50, -73.57),
      "ST JOHNS": (45.30, -73.26), "CROWN PT": (44.027, -73.424), "VALCOUR": (44.611, -73.430), "BOSTON": (42.36, -71.06), "NEW YORK": (40.71, -74.0),
      "WEST POINT": (41.39, -73.96), "PHILADELPHIA": (39.95, -75.16)}
PL = dict(PL0, **{"CAPE DIAMOND":(46.807,-71.205),"PRES DE VILLE":(46.803,-71.207),"SAULT":(46.8161,-71.2017),"PALACE":(46.817,-71.208),"LEVIS":(46.80,-71.18),"WOLFE":(46.79,-71.24),"PLAINS":(46.80,-71.22),"VALC CH":(44.611,-73.430),"VALC S":(44.597,-73.405),"SCHUYLER":(44.52,-73.40)})
if __name__ == "__main__":
    m = sys.argv[1]; P = proj(m)
    f = f"{ROOT}/assets/{m}_hd_lift.jpg"
    if not os.path.exists(f): f = f"{ROOT}/assets/{m}.jpg"
    im = Image.open(f).convert("RGB").resize((2880, 1620)); d = ImageDraw.Draw(im)
    for gx in range(0, 2880, 100): d.line([gx, 0, gx, 1620], fill=(0, 0, 255) if gx % 500 == 0 else (150, 150, 255), width=1); d.text((gx + 2, 2), str(gx), fill=(0, 0, 255))
    for gy in range(0, 1620, 100): d.line([0, gy, 2880, gy], fill=(0, 0, 255) if gy % 500 == 0 else (150, 150, 255), width=1); d.text((2, gy + 2), str(gy), fill=(0, 0, 255))
    for k, (la, lo) in PL.items():
        x, y = P(la, lo)
        if -50 < x < 2930 and -50 < y < 1670:
            print(f"{k:14s} {x:7.0f} {y:7.0f}"); d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=(255, 0, 0), width=3); d.text((x + 9, y - 9), k, fill=(200, 0, 0))
    if len(sys.argv) > 3: im = im.crop(tuple(int(v) for v in sys.argv[3].split(",")))
    im.save(sys.argv[2], quality=85)
