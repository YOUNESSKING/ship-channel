"""Bake a parchment shaded-relief basemap (with sea) from open AWS Terrarium tiles.

usage: python3 bake.py NAME LAT LON ZOOM [EXAGGERATION]
writes assets/NAME.jpg (2880x1620) + assets/NAME.json (projection info for overlays)
Elevation: Mapzen/AWS Terrain Tiles (SRTM, GMTED, ETOPO1), open data.
"""
import json, math, os, sys, urllib.request
import numpy as np
from PIL import Image

W, H = 2880, 1620
LOW = np.array([226, 212, 176], float)    # lowland parchment
HIGH = np.array([146, 140, 100], float)   # mountain olive
PEAK = np.array([236, 232, 220], float)   # high peaks, snowy
SEA = np.array([168, 186, 184], float)    # muted sea
SEA_DEEP = np.array([132, 156, 160], float)
URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
CACHE = os.path.join(HERE, ".tiles")


def world_px(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n


def tile(z, x, y):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"{z}_{x}_{y}.png")
    if not os.path.exists(path):
        with urllib.request.urlopen(URL.format(z=z, x=x, y=y)) as r:
            open(path, "wb").write(r.read())
    a = np.asarray(Image.open(path).convert("RGB"), float)
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768


def blur(a, passes=1):
    k = np.array([1, 4, 6, 4, 1], float) / 16
    for _ in range(passes):
        a = np.pad(a, 2, mode="edge")
        a = np.apply_along_axis(lambda r: np.convolve(r, k, "valid"), 1, a)
        a = np.apply_along_axis(lambda c: np.convolve(c, k, "valid"), 0, a)
    return a


def main(name, lat, lon, z, exaggeration):
    cx, cy = world_px(lat, lon, z)
    x0, y0 = int(cx - W / 2), int(cy - H / 2)
    tx0, ty0, tx1, ty1 = x0 // 256, y0 // 256, (x0 + W) // 256, (y0 + H) // 256
    mosaic = np.vstack([np.hstack([tile(z, tx, ty) for tx in range(tx0, tx1 + 1)]) for ty in range(ty0, ty1 + 1)])
    elev = mosaic[y0 - ty0 * 256:y0 - ty0 * 256 + H, x0 - tx0 * 256:x0 - tx0 * 256 + W]

    mpp = 156543.03392 * math.cos(math.radians(lat)) / 2 ** z
    sea_below = float(os.environ.get("SEA_BELOW", 0.5))  # e.g. SEA_BELOW=-8 for the Dutch polders (land below sea level)
    land = elev > sea_below
    land_elev = np.where(land, elev, 0)
    smooth = blur(land_elev)
    gy, gx = np.gradient(smooth * exaggeration, mpp)
    slope, aspect = np.arctan(np.hypot(gx, gy)), np.arctan2(-gx, gy)

    def shade(az, alt):
        az, alt = math.radians(az), math.radians(alt)
        return np.clip(np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect), 0, 1)

    hs = (0.6 * shade(315, 40) + 0.25 * shade(270, 50) + 0.15 * shade(0, 60))[..., None]
    hi = max(np.percentile(land_elev[land], 99.5) if land.any() else 1, 1)
    t = np.clip(land_elev / hi, 0, 1)[..., None]
    base = np.where(t < 0.7, LOW * (1 - t / 0.7) + HIGH * (t / 0.7), HIGH * (1 - (t - 0.7) / 0.3) + PEAK * ((t - 0.7) / 0.3))
    rgb = base * (0.45 + 0.75 * hs)
    rgb = base * 0.3 + rgb * 0.7

    depth = np.clip(-elev / 2500, 0, 1)[..., None]
    sea = SEA * (1 - depth) + SEA_DEEP * depth
    coast = blur(land.astype(float), 2)[..., None]  # soft coastline blend
    rgb = sea * (1 - coast) + rgb * coast
    # thin coastline ink
    edge = np.clip(np.abs(coast[..., 0] - 0.5) < 0.12, 0, 1)[..., None] * (land.any())
    rgb = rgb * (1 - edge * 0.35) + np.array([90, 84, 66]) * edge * 0.35

    grey = rgb.mean(axis=2, keepdims=True)
    rgb = grey * 0.2 + rgb * 0.8
    rng = np.random.default_rng(218)
    grain = np.asarray(Image.fromarray(rng.normal(128, 40, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), float)
    rgb = rgb + (grain[..., None] - 128) * 0.09
    os.makedirs(ASSETS, exist_ok=True)
    Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).save(os.path.join(ASSETS, f"{name}.jpg"), quality=90)
    json.dump({"name": name, "center": [lat, lon], "zoom": z, "origin_world_px": [x0, y0], "size": [W, H],
               "meters_per_px": round(mpp, 2), "sea_below": sea_below, "credit": "Terrain: Mapzen / AWS Terrain Tiles (open data)"},
              open(os.path.join(ASSETS, f"{name}.json"), "w"), indent=1)
    print(name, f"{mpp:.1f} m/px", f"elev {elev.min():.0f}..{elev.max():.0f}")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], float(a[1]), float(a[2]), int(a[3]), float(a[4]) if len(a) > 4 else 2.0)
