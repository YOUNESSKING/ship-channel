"""Arnold #17 map agent (ar3_): who-controls-the-ground overlays (option 1, multiply; the scenes show them at HALF strength, 2c) for
the wide shots of hook-a (northeast, hudson) and m3a (hudson). Americans = BLUE, British = RED, two-colour rim where they touch.
Sides, autumn 1777 (FACT_NOTES; standard history): British = Canada (Quebec province north of 45 N and of the Maine highlands), Nova Scotia
side east of the St. Croix; Burgoyne's corridor from St. Johns down Lake Champlain (Crown Point, Ticonderoga, Skenesborough) and Fort
Edward to his camp above Bemis Heights (a ~12 km band; approximate); New York City + Long Island + Staten Island; Newport (Aquidneck).
Everything else on land = American. Sea = elevation <= 0 (the DEM), lakes = det_riv water: left clear.
-> assets/media/ar3_ctl_<map>_1777.png (2880 x 1620).   usage (from arnold/): python3 tools/ar3_make_control.py northeast hudson"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
W, H = 2880, 1620
CANADA = [(49, -82), (45.0, -82), (45.0, -71.5), (45.3, -70.8), (45.9, -70.25), (46.4, -70.05), (47.45, -69.2), (47.1, -67.8), (45.6, -67.8),
          (45.1, -67.1), (44.5, -66.9), (43.5, -66.0), (40.0, -63.0), (49, -60)]
CORR = [(45.45, -73.25), (45.30, -73.26), (45.0, -73.33), (44.611, -73.40), (44.25, -73.36), (44.027, -73.424), (43.843, -73.387), (43.555, -73.404),
        (43.40, -73.50), (43.267, -73.585), (43.10, -73.58), (43.02, -73.63)]
NYC = [(40.86, -74.06), (40.96, -73.80), (41.00, -72.00), (40.60, -71.80), (40.45, -74.30)]
NEWPORT = [(41.66, -71.25), (41.62, -71.20), (41.45, -71.29), (41.47, -71.35), (41.60, -71.30)]
def proj(m):
    J = json.load(open(f"assets/{m}_hd_lift.json" if os.path.exists(f"assets/{m}_hd_lift.json") else f"assets/{m}.json")); Z = J["zoom"]; OX, OY = J["origin_world_px"]
    def P(lat, lon):
        n = 256 * 2 ** Z; r = math.radians(lat)
        return ((lon + 180) / 360 * n - OX, (1 - math.asinh(math.tan(r)) / math.pi) / 2 * n - OY)
    return P, J
def build(m):
    P, J = proj(m)
    land = np.ones((H, W), bool)
    if os.path.exists(f"assets/src/{m}_hd_elev.npy"):
        e = np.load(f"assets/src/{m}_hd_elev.npy").astype(np.float32); e = e.reshape(H, e.shape[0] // H, W, e.shape[1] // W).mean(axis=(1, 3)); land &= e > 0.5
    if os.path.exists(f"assets/media/{m}_det_riv.png"):
        a = np.array(Image.open(f"assets/media/{m}_det_riv.png").convert("RGBA").resize((W, H), Image.BILINEAR))[:, :, 3]; land &= a <= 110
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im)
    for poly in (CANADA, NYC, NEWPORT): d.polygon([P(*q) for q in poly], fill=255)
    wkm = 12000 / J["meters_per_px"]; pts = [P(*q) for q in CORR]
    d.line(pts, fill=255, width=max(3, int(wkm)), joint="curve")
    for q in (pts[0], pts[-1]): d.ellipse([q[0] - wkm / 2, q[1] - wkm / 2, q[0] + wkm / 2, q[1] + wkm / 2], fill=255)
    gb = (np.array(im) > 0); gb = ndimage.gaussian_filter(gb.astype(np.float32), 2) > 0.5
    gb &= land; us = land & ~gb
    out = np.zeros((H, W, 4), np.float32)
    dU = ndimage.distance_transform_edt(~gb); dG = ndimage.distance_transform_edt(~us)
    out[us, :3] = (110, 160, 255); out[us, 3] = 0.565
    out[gb, :3] = (240, 105, 95); out[gb, 3] = (0.62 + 0.2 * np.exp(-dG / 40.0))[gb]
    rimU = us & (dU < 5); rimG = gb & (dG < 5)
    out[rimU, :3] = (70, 120, 235); out[rimU, 3] = 0.85; out[rimG, :3] = (215, 60, 55); out[rimG, 3] = 0.88
    a = ndimage.gaussian_filter(out[:, :, 3], 1.0); out[:, :, 3] = np.where(land, np.maximum(a, out[:, :, 3] * 0.9), a * 0.5)
    Image.fromarray(np.clip(out * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA").save(f"assets/media/ar3_ctl_{m}_1777.png", optimize=True)
    print("wrote", f"ar3_ctl_{m}_1777.png", int(us.sum()), int(gb.sum()))
for m in sys.argv[1:]: build(m)
