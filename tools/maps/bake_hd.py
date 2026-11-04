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
tx0, ty0, tx1, ty1 = x0 // 256, y0 // 256, (x0 + W) // 256, (y0 + H) // 256
print("tiles", (tx1 - tx0 + 1) * (ty1 - ty0 + 1), "at z", z, flush=True)
rows = []
for ty in range(ty0, ty1 + 1):
    rows.append(np.hstack([tile(z, tx, ty).astype(np.float32) for tx in range(tx0, tx1 + 1)]))
mosaic = np.vstack(rows); elev = mosaic[y0 - ty0 * 256:y0 - ty0 * 256 + H, x0 - tx0 * 256:x0 - tx0 * 256 + W]
# KIT CHANGE: repair rectangular no-data holes (exact 0 m blocks inside deep sea) that some Terrarium tiles contain
_z = elev == 0; _lab, _n = ndimage.label(_z)
for _i, _sl in enumerate(ndimage.find_objects(_lab), 1):
    _m = _lab[_sl] == _i; _a = _m.sum()
    if _a > 1500 and _a / _m.size > 0.9:
        _r = ndimage.binary_dilation(_lab == _i, iterations=6) & ~(_lab == _i)
        if np.median(elev[_r]) < -30:
            _idx = ndimage.distance_transform_edt(_lab == _i, return_distances=False, return_indices=True)
            elev[_lab == _i] = elev[tuple(_idx[:, _lab == _i])]; print("repaired no-data block", _a, "px", flush=True)
SEA_LEVEL = float(os.environ.get("SEA_LEVEL", J.get("sea_level", 0)))   # KIT CHANGE: see bake.py
elev_raw = elev.copy(); elev = elev - SEA_LEVEL
os.makedirs("assets/src", exist_ok=True)
np.save(f"assets/src/{base}_hd_elev.npy", elev.astype(np.float32))
lat = J["center"][0]; mpp = 156543.03392 * math.cos(math.radians(lat)) / 2 ** z
sea_below = J.get("sea_below", 0.5); land = elev > sea_below
le = np.where(land, elev, 0).astype(np.float32)
sm = ndimage.gaussian_filter(le, 1.0)
gy, gx = np.gradient(sm * exag, mpp)
slope, aspect = np.arctan(np.hypot(gx, gy)), np.arctan2(-gx, gy)
def shade(az, alt):
    az, alt = math.radians(az), math.radians(alt)
    return np.clip(np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect), 0, 1)
hs = 0.45 * shade(315, 38) + 0.25 * shade(260, 45) + 0.18 * shade(15, 50) + 0.12 * shade(135, 60)   # multi-directional
sl = np.clip(np.degrees(slope) / 25, 0, 1)                                                            # slope darkening
ao = np.clip((ndimage.gaussian_filter(le, 18) - le) / 40, -1, 1)                                      # >0 in valleys, <0 on ridges
fine = np.clip((le - ndimage.gaussian_filter(le, 2.5)) * exag / 6, -1, 1)                             # fine terrain texture
light = np.clip(0.42 + 0.72 * hs - 0.16 * sl - 0.18 * np.clip(ao, 0, 1) + 0.08 * np.clip(-ao, 0, 1) + 0.10 * fine, 0, 1.25)
hi = max(np.percentile(le[land], 99.5) if land.any() else 1, 1); t = np.clip(le / hi, 0, 1)[..., None]
coast = ndimage.gaussian_filter(land.astype(np.float32), 2.0)[..., None]
rng = np.random.default_rng(218)
def finish(rgb, out):
    g = np.asarray(Image.fromarray(rng.normal(128, 40, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32)
    rgb = rgb + (g[..., None] - 128) * 0.07
    Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).save(out, quality=90); print("wrote", out, flush=True)
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
# KIT CHANGE: sea coloured by depth below sea level (shelf lighter teal -> deep abyss) + exposed-shelf tint when SEA_LEVEL < 0
dd = np.clip(-elev / 3500, 0, 1)[..., None] ** 0.6
sea_c = np.array([30, 52, 62], np.float32) * (1 - dd) + np.array([9, 16, 24], np.float32) * dd
halo = ndimage.gaussian_filter(land.astype(np.float32), 8)[..., None] * (1 - coast)
sea_c = sea_c + halo * np.array([14, 26, 28], np.float32)
if SEA_LEVEL < -1:
    shelf = ndimage.gaussian_filter((land & (elev_raw <= 0)).astype(np.float32), 2.0)[..., None] * 0.55
    rgb = rgb * (1 - shelf) + (rgb * 0.55 + np.array([70, 62, 40], np.float32) * 0.6) * shelf
rgb = sea_c * (1 - coast) + rgb * coast
finish(rgb, f"assets/{base}_hd_ref.jpg")
for suf in ("_hd", "_hd_ref"):
    json.dump(dict(J, name=base + suf, hd_scale=S), open(f"assets/{base}{suf}.json", "w"), indent=1)
