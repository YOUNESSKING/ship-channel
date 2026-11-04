"""Move-1 agent helper: lat/lon -> basemap px (Web Mercator, from assets/<map>_hd_lift.json or <map>.json); marks places on a preview.
usage: python3 tools/m1_proj.py MAP [out.jpg]"""
import json, math, sys, os
from PIL import Image, ImageDraw
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def proj(base):
    f = f"{ROOT}/assets/{base}_hd_lift.json"
    if not os.path.exists(f): f = f"{ROOT}/assets/{base}.json"
    J = json.load(open(f)); Z, (OX, OY) = J["zoom"], J["origin_world_px"]
    def P(lat, lon):
        n = 256 * 2 ** Z; r = math.radians(lat)
        return ((lon + 180) / 360 * n - OX, (1 - math.asinh(math.tan(r)) / math.pi) / 2 * n - OY)
    return P
PL = {"FORT DONELSON": (36.4935, -87.8570), "WATER BATT": (36.4950, -87.8530), "DOVER": (36.4876, -87.8384),
      "FORT HENRY": (36.5150, -88.0300), "FORT HEIMAN": (36.5260, -88.0480), "HICKMAN CR": (36.508, -87.868), "LICK CR": (36.481, -87.828),
      "CRISP FARM": (36.478, -87.885), "CLARKSVILLE": (36.5298, -87.3595), "NASHVILLE": (36.1627, -86.7816), "PADUCAH": (37.0834, -88.6000),
      "CAIRO": (37.0053, -89.1765), "SMITHLAND": (37.1390, -88.4034), "COLUMBUS": (36.7598, -89.1034), "BOWLING GREEN": (36.9685, -86.4808),
      "FORT HENRY LANDING": (36.555, -88.012), "MEMPHIS": (35.1495, -90.0490), "CORINTH": (34.9343, -88.5223)}
if __name__ == "__main__":
    m = sys.argv[1]; P = proj(m)
    im = Image.open(f"{ROOT}/assets/{m}_hd_lift.jpg").convert("RGB").resize((2880, 1620)); d = ImageDraw.Draw(im)
    for k, (la, lo) in PL.items():
        x, y = P(la, lo)
        if -50 < x < 2930 and -50 < y < 1670:
            print(f"{k:20s} {x:7.0f} {y:7.0f}"); d.ellipse([x - 6, y - 6, x + 6, y + 6], outline=(255, 0, 0), width=3); d.text((x + 8, y - 8), k, fill=(255, 0, 0))
    for gx in range(0, 2880, 200): d.line([gx, 0, gx, 1620], fill=(0, 0, 255), width=1); d.text((gx + 2, 2), str(gx), fill=(0, 0, 255))
    for gy in range(0, 1620, 200): d.line([0, gy, 2880, gy], fill=(0, 0, 255), width=1); d.text((2, gy + 2), str(gy), fill=(0, 0, 255))
    im.save(sys.argv[2] if len(sys.argv) > 2 else f"/tmp/m1_{m}.jpg", quality=85)
