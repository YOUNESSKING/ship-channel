"""Move-3 agent helper: lat/lon -> basemap px for the m3a-m3d + ending maps; marks places on a preview.
usage: python3 tools/m3_proj.py MAP [out.jpg]   (MAP = richmond / jamesriver / petersburg / mississippi / tennessee or a preview bake m3x_*, ghx_jam)"""
import json, math, os, sys
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
PL = {"RICHMOND": (37.5407, -77.4360), "COLD HARBOR": (37.591, -77.271), "PETERSBURG": (37.2279, -77.4019), "CITY POINT": (37.313, -77.276),
      "BERMUDA HUNDRED": (37.341, -77.273), "DREWRYS BLUFF": (37.424, -77.425), "WILCOX LDG": (37.318, -77.103), "WEYANOKE": (37.2915, -77.0655),
      "FT POWHATAN": (37.271, -77.080), "CHARLES CITY CH": (37.343, -77.073), "TREVILIAN": (38.047, -78.077), "LONG BRIDGE": (37.452, -77.170),
      "RIDDELLS SHOP": (37.422, -77.250), "WHITE HOUSE": (37.571, -77.000), "JONES BRIDGE": (37.393, -77.030), "CHAFFINS BLUFF": (37.400, -77.360),
      "MALVERN HILL": (37.409, -77.249), "PRINCE GEORGE CH": (37.221, -77.288), "WASHINGTON": (38.907, -77.037), "APPOMATTOX": (37.377, -78.796),
      "FREDERICKSBURG": (38.303, -77.461), "VICKSBURG": (32.3526, -90.8779), "MEMPHIS": (35.1495, -90.0490), "NEW ORLEANS": (29.951, -90.071),
      "PORT HUDSON": (30.69, -91.27), "BATON ROUGE": (30.4515, -91.1871), "JACKSON": (32.2988, -90.1848), "GRAND GULF": (32.03, -91.05),
      "BRUINSBURG": (31.958, -91.155), "FORT DONELSON": (36.4935, -87.8570), "FORT HENRY": (36.5150, -88.0300), "NASHVILLE": (36.1627, -86.7816),
      "CAIRO": (37.0053, -89.1765), "BATT 5": (37.2425, -77.3570), "BATT 3": (37.2500, -77.3590), "BATT 11": (37.2230, -77.3530),
      "BATT 9": (37.2310, -77.3555), "BATT 7": (37.2370, -77.3560), "BATT 15": (37.2100, -77.3600), "BAYLORS FARM": (37.272, -77.330)}
if __name__ == "__main__":
    m = sys.argv[1]; P = proj(m)
    f = f"{ROOT}/assets/{m}_hd_lift.jpg"
    if not os.path.exists(f): f = f"{ROOT}/assets/{m}.jpg"
    im = Image.open(f).convert("RGB").resize((2880, 1620)); d = ImageDraw.Draw(im)
    for k, (la, lo) in PL.items():
        x, y = P(la, lo)
        if -50 < x < 2930 and -50 < y < 1670:
            print(f"{k:20s} {x:7.0f} {y:7.0f}"); d.ellipse([x - 6, y - 6, x + 6, y + 6], outline=(255, 0, 0), width=3); d.text((x + 8, y - 8), k, fill=(255, 0, 0))
    for gx in range(0, 2880, 100): d.line([gx, 0, gx, 1620], fill=(0, 0, 255) if gx % 500 == 0 else (120, 120, 255), width=1); d.text((gx + 2, 2), str(gx), fill=(0, 0, 255))
    for gy in range(0, 1620, 100): d.line([0, gy, 2880, gy], fill=(0, 0, 255) if gy % 500 == 0 else (120, 120, 255), width=1); d.text((2, gy + 2), str(gy), fill=(0, 0, 255))
    out = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/m3_{m}.jpg"
    if len(sys.argv) > 3:   # crop x0,y0,x1,y1
        im = im.crop(tuple(int(v) for v in sys.argv[3].split(",")))
    im.save(out, quality=85)
