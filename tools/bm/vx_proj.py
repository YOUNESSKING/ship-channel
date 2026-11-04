"""Map agent vx (m2e-m2g, Grant #16): lat/lon -> basemap px; marks the Vicksburg-campaign places on a gridded preview.
usage: python3 tools/vx_proj.py MAP OUT.jpg"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m1_proj import proj, ROOT
from PIL import Image, ImageDraw
PL = {"VICKSBURG": (32.352, -90.878), "GRAND GULF": (32.033, -91.053), "BRUINSBURG": (31.942, -91.157), "PORT GIBSON": (31.961, -90.984),
      "RAYMOND": (32.259, -90.422), "JACKSON": (32.299, -90.185), "CHAMPION HILL": (32.33, -90.53), "EDWARDS": (32.33, -90.605),
      "BIG BLACK BR": (32.347, -90.716), "HANKINSON": (32.19, -90.93), "ROCKY SPR": (32.087, -90.80), "UTICA": (32.108, -90.623),
      "CLINTON": (32.341, -90.322), "BOLTON": (32.35, -90.459), "WARRENTON": (32.20, -90.90), "HAINES BLUFF": (32.46, -90.80),
      "MILLIKENS": (32.48, -91.07), "HARD TIMES": (32.065, -91.095), "NATCHEZ": (31.56, -91.403), "PORT HUDSON": (30.678, -91.27),
      "MEMPHIS": (35.149, -90.049), "BATON ROUGE": (30.451, -91.187), "NEW ORLEANS": (29.951, -90.072), "HELENA": (34.527, -90.586),
      "CAIRO": (37.0, -89.18), "YAZOO CITY": (32.855, -90.405), "CANTON": (32.61, -90.04)}
if __name__ == "__main__":
    m = sys.argv[1]; P = proj(m)
    im = Image.open(f"{ROOT}/assets/{m}_hd_lift.jpg").convert("RGB").resize((2880, 1620)); d = ImageDraw.Draw(im)
    for k, (la, lo) in PL.items():
        x, y = P(la, lo)
        if -50 < x < 2930 and -50 < y < 1670:
            print(f"{k:16s} {x:7.0f} {y:7.0f}"); d.ellipse([x - 6, y - 6, x + 6, y + 6], outline=(255, 0, 0), width=3); d.text((x + 8, y - 8), k, fill=(255, 0, 0))
    for gx in range(0, 2880, 100): d.line([gx, 0, gx, 1620], fill=(0, 0, 255) if gx % 500 == 0 else (120, 120, 255), width=1); d.text((gx + 2, 2), str(gx), fill=(0, 0, 255))
    for gy in range(0, 1620, 100): d.line([0, gy, 2880, gy], fill=(0, 0, 255) if gy % 500 == 0 else (120, 120, 255), width=1); d.text((2, gy + 2), str(gy), fill=(0, 0, 255))
    im.save(sys.argv[2], quality=85)
