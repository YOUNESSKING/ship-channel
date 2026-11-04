"""Map agent hook (Grant #16, prefix gh_): trace the Tennessee, Cumberland, Ohio and Mississippi centrelines on a basemap's HD elevation
(D8 flow with pysheds, downstream from a start point snapped to the strongest flow nearby) -> assets/media/gh_<map>_rivers.json
{name: [[x, y], ...]} in MAP px (2880 x 1620). usage (from grant/): python3 tools/gh_rivers.py tennessee"""
import json, math, sys
import numpy as np
if not hasattr(np, "in1d"): np.in1d = np.isin
from affine import Affine
from pysheds.grid import Grid
from pysheds.sview import Raster, ViewFinder
from scipy import ndimage
m = sys.argv[1]
J = json.load(open(f"assets/{m}_hd_lift.json")); Z = J["zoom"]; OX, OY = J["origin_world_px"]
def P(lat, lon):
    n = 256 * 2 ** Z; r = math.radians(lat)
    return ((lon + 180) / 360 * n - OX, (1 - math.asinh(math.tan(r)) / math.pi) / 2 * n - OY)
e = np.load(f"assets/src/{m}_hd_elev.npy").astype(np.float64)
e = e.reshape(e.shape[0] // 2, 2, e.shape[1] // 2, 2).mean(axis=(1, 3))          # map px
e = np.clip(e, -50, None); e = ndimage.median_filter(e, 3)
vf = ViewFinder(affine=Affine(1, 0, 0, 0, 1, 0), shape=e.shape, nodata=-9999.0)
g = Grid(viewfinder=vf); dem = Raster(e, viewfinder=vf)
d = g.resolve_flats(g.fill_depressions(g.fill_pits(dem)))
fdir = np.asarray(g.flowdir(d)); acc = np.asarray(g.accumulation(g.flowdir(d)))
DIRS = {64: (-1, 0), 128: (-1, 1), 1: (0, 1), 2: (1, 1), 4: (1, 0), 8: (1, -1), 16: (0, -1), 32: (-1, -1)}
H, W = e.shape
def trace(lat, lon, r=10, stop=None, maxn=6000):
    x, y = P(lat, lon); x, y = int(round(x)), int(round(y))
    y0, y1, x0, x1 = max(0, y - r), min(H, y + r + 1), max(0, x - r), min(W, x + r + 1)
    win = acc[y0:y1, x0:x1]; iy, ix = np.unravel_index(np.argmax(win), win.shape); y, x = y0 + iy, x0 + ix
    pts = [(x, y)]
    for _ in range(maxn):
        dd = DIRS.get(int(fdir[y, x]))
        if not dd: break
        y, x = y + dd[0], x + dd[1]
        if not (0 <= y < H and 0 <= x < W): break
        pts.append((x, y))
    a = np.array(pts, float)
    if stop: a = a[:int(np.argmin(np.hypot(a[:, 0] - stop[0], a[:, 1] - stop[1]))) + 1]   # cut at the confluence
    if len(a) > 9: a = np.stack([ndimage.uniform_filter1d(a[:, 0], 9, mode="nearest"), ndimage.uniform_filter1d(a[:, 1], 9, mode="nearest")], 1)
    return [[round(float(px), 1), round(float(py), 1)] for px, py in a[::4]] + [[round(float(a[-1, 0]), 1), round(float(a[-1, 1]), 1)]]
START = {"tennessee": {"cumberland": (36.17, -86.78, (37.14, -88.41)), "tennessee": (35.10, -88.20, (37.07, -88.59)),
                       "ohio": (37.07, -88.62, (37.00, -89.17)), "ohio_up": (37.78, -87.60, (37.00, -89.17))}}
out = {}
for nm, (la, lo, st) in START.get(m, {}).items():
    out[nm] = trace(la, lo, stop=P(*st) if st else None); print(nm, len(out[nm]), out[nm][0], out[nm][-1])
json.dump(out, open(f"assets/media/gh_{m}_rivers.json", "w"))
