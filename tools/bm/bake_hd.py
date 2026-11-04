"""HD relief for an existing basemap (map-detail test, owner 2026-10-06): same extent/projection as assets/<base>.json, but built
from elevation tiles one zoom deeper (2x resolution: 5760x3240, shown at 2880x1620 so it stays sharp when the camera zooms in) and
better shading: 4-direction hillshade + slope darkening + ambient occlusion (valleys darker, ridges lit) + fine terrain texture.
usage: python3 tools/bake_hd.py BASE [EXAG]   -> assets/BASE_hd.jpg (locked parchment palette) + assets/BASE_hd_ref.jpg (dark reference grade)
Elevation: Mapzen/AWS Terrain Tiles (open data)."""
import json, math, os, sys, urllib.request
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bake import tile, LOW, HIGH, PEAK, SEA, SEA_DEEP
base = sys.argv[1]; exag = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
J = json.load(open(f"assets/{base}.json")); z = J["zoom"] + 1; S = 2
W, H = J["size"][0] * S, J["size"][1] * S
x0, y0 = J["origin_world_px"][0] * S, J["origin_world_px"][1] * S
ZT = min(z, 15); F = 2 ** (z - ZT)  # terrain tiles stop at z15: above it, fetch z15 and upsample (meade getty15)
tx0, ty0, tx1, ty1 = x0 // F // 256, y0 // F // 256, (x0 + W) // F // 256, (y0 + H) // F // 256
print("tiles", (tx1 - tx0 + 1) * (ty1 - ty0 + 1), "at z", ZT, flush=True)
rows = []
for ty in range(ty0, ty1 + 1):
    rows.append(np.hstack([tile(ZT, tx, ty).astype(np.float32) for tx in range(tx0, tx1 + 1)]))
mosaic = np.vstack(rows)
if F > 1: mosaic = ndimage.zoom(mosaic, F, order=3)
elev = mosaic[y0 - ty0 * 256 * F:y0 - ty0 * 256 * F + H, x0 - tx0 * 256 * F:x0 - tx0 * 256 * F + W]
np.save(f"assets/src/{base}_hd_elev.npy", elev.astype(np.float32))
lat = J["center"][0]; mpp = 156543.03392 * math.cos(math.radians(lat)) / 2 ** z
sea_below = J.get("sea_below", 0.5); land = elev > sea_below
le = np.where(land, elev, 0).astype(np.float32)
LIFT = os.environ.get("LIFT") == "1"  # C1 'lifted Frontlines' TEST grade (research/MAP_COLOUR_REVIEW.md): writes only <map>_hd_lift
SOFT = LIFT and z >= 11                 # P6: calmer close-up texture (smoothing 1.6, fine 0.04)
sm = ndimage.gaussian_filter(le, 1.6 if SOFT else 1.0)
gy, gx = np.gradient(sm * exag, mpp)
slope, aspect = np.arctan(np.hypot(gx, gy)), np.arctan2(-gx, gy)
def shade(az, alt):
    az, alt = math.radians(az), math.radians(alt)
    return np.clip(np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect), 0, 1)
hs = 0.45 * shade(315, 38) + 0.25 * shade(260, 45) + 0.18 * shade(15, 50) + 0.12 * shade(135, 60)   # multi-directional
sl = np.clip(np.degrees(slope) / 25, 0, 1)                                                            # slope darkening
ao = np.clip((ndimage.gaussian_filter(le, 18) - le) / 40, -1, 1)                                      # >0 in valleys, <0 on ridges
fine = np.clip((le - ndimage.gaussian_filter(le, 2.5)) * exag / 6, -1, 1)                             # fine terrain texture
light = np.clip(0.42 + 0.72 * hs - 0.16 * sl - 0.18 * np.clip(ao, 0, 1) + 0.08 * np.clip(-ao, 0, 1) + (0.04 if SOFT else 0.10) * fine, 0, 1.25)
hi = max(np.percentile(le[land], 99.5) if land.any() else 1, 1); t = np.clip(le / hi, 0, 1)[..., None]
coast = ndimage.gaussian_filter(land.astype(np.float32), 2.0)[..., None]
rng = np.random.default_rng(218)
def finish(rgb, out):
    g = np.asarray(Image.fromarray(rng.normal(128, 40, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32)
    rgb = rgb + (g[..., None] - 128) * 0.07
    Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).save(out, quality=90); print("wrote", out, flush=True)
if LIFT:  # C1: same grey-green hue, exposure normalised per map (land median 0.70), sea (18,33,44)
    a = np.clip(light * 0.85 + t[..., 0] * 0.12, 0, 1) ** 1.15
    med = float(np.median(a[land])) if land.any() else 0.5; an = a ** (np.log(0.70) / np.log(max(min(med, 0.99), 0.01)))
    rgb = np.array([24, 31, 31.]) + (np.array([190, 202, 184.]) - np.array([24, 31, 31.])) * an[..., None]
    rgb = np.array([18, 33, 44.]) * (1 - coast) + rgb * coast
    finish(rgb, f"assets/{base}_hd_lift.jpg"); json.dump(dict(J, name=base + "_hd_lift", hd_scale=S), open(f"assets/{base}_hd_lift.json", "w"), indent=1)
    sys.exit(0)
# 1) locked parchment palette (bake.py colours), HD shading
basec = np.where(t < 0.7, LOW * (1 - t / 0.7) + HIGH * (t / 0.7), HIGH * (1 - (t - 0.7) / 0.3) + PEAK * ((t - 0.7) / 0.3))
rgb = basec * 0.3 + basec * (0.45 + 0.75 * light[..., None]) * 0.7
depth = np.clip(-elev / 2500, 0, 1)[..., None]; sea = SEA * (1 - depth) + SEA_DEEP * depth
rgb = sea * (1 - coast) + rgb * coast
edge = (np.abs(coast[..., 0] - 0.5) < 0.12)[..., None]; rgb = rgb * (1 - edge * 0.35) + np.array([90, 84, 66]) * edge * 0.35
grey = rgb.mean(axis=2, keepdims=True); rgb = grey * 0.2 + rgb * 0.8
finish(rgb, f"assets/{base}_hd.jpg")
# 2) dark reference grade (green-grey terrain, dark teal sea)
dark, lite = np.array([16, 22, 22], np.float32), np.array([138, 154, 140], np.float32)
a = np.clip(light * 0.85 + t[..., 0] * 0.12, 0, 1) ** 1.15
rgb = dark + (lite - dark) * a[..., None]
rgb = np.array([16, 27, 34], np.float32) * (1 - coast) + rgb * coast
finish(rgb, f"assets/{base}_hd_ref.jpg")
for suf in ("_hd", "_hd_ref"):
    json.dump(dict(J, name=base + suf, hd_scale=S), open(f"assets/{base}{suf}.json", "w"), indent=1)
