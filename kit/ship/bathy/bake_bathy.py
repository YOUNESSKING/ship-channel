"""Sea-floor (bathymetry) basemap in the ship-channel look, from open AWS Terrarium tiles (they carry sea depth too).

usage: python3 kit/ship/bathy/bake_bathy.py NAME LAT LON ZOOM [--preview]
   writes kit/ship/bathy/out/NAME.jpg (2880x1620, map-kit relief size, git-ignored) + out/NAME.json (same projection keys as
   tools/maps/bake.py, so map-kit scenes and overlay tools work unchanged), and with --preview a small JPG in kit/ship/preview/.
Colours: palette.json (sea ramp by depth, sea-floor hillshade, isobaths, sand beach, muted land in the battle-maps LIFT hue).
Example (Pensacola / Oriskany reef): python3 kit/ship/bathy/bake_bathy.py gulf_pensacola 29.75 -87.0 9 --preview
"""
import json, math, os, sys, urllib.request
import numpy as np
from PIL import Image
from scipy import ndimage

W, H = 2880, 1620
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); CACHE = os.path.join(HERE, ".tiles")
URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
PAL = json.load(open(os.path.join(HERE, "palette.json")))


def world_px(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n


def tile(z, x, y):
    x %= 2 ** z
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, f"{z}_{x}_{y}.png")
    if not os.path.exists(p):
        req = urllib.request.Request(URL.format(z=z, x=x, y=y), headers={"User-Agent": "ship-channel-bake/1"})
        with urllib.request.urlopen(req, timeout=60) as r: open(p, "wb").write(r.read())
    a = np.asarray(Image.open(p).convert("RGB"), np.float32)
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768


def shade(elev, mpp, exag, az=315, alt=40):
    gy, gx = np.gradient(ndimage.gaussian_filter(elev, 1.0) * exag, mpp)
    slope, aspect = np.arctan(np.hypot(gx, gy)), np.arctan2(-gx, gy)
    az, alt = math.radians(az), math.radians(alt)
    return np.clip(np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect), 0, 1)


def sea_colour(depth):
    st = PAL["sea_stops"]; d = np.array([s[0] for s in st], np.float32); c = np.array([s[1] for s in st], np.float32)
    x = np.log1p(np.clip(depth, 0, d[-1])); xd = np.log1p(d)   # interpolate in log-depth: detail on the shelf, calm deep water
    return np.stack([np.interp(x, xd, c[:, k]) for k in range(3)], -1)


def bake(name, lat, lon, z, preview=False):
    cx, cy = world_px(lat, lon, z); x0, y0 = int(cx - W / 2), int(cy - H / 2)
    tx0, ty0, tx1, ty1 = x0 // 256, y0 // 256, (x0 + W) // 256, (y0 + H) // 256
    print(f"{(tx1 - tx0 + 1) * (ty1 - ty0 + 1)} tiles at z{z}", flush=True)
    mos = np.vstack([np.hstack([tile(z, tx, ty) for tx in range(tx0, tx1 + 1)]) for ty in range(ty0, ty1 + 1)])
    elev = mos[y0 - ty0 * 256:y0 - ty0 * 256 + H, x0 - tx0 * 256:x0 - tx0 * 256 + W]
    mpp = 156543.03392 * math.cos(math.radians(lat)) / 2 ** z
    land = elev > 0.5; depth = np.where(land, 0, -elev).clip(0)
    # --- sea: colour by depth x gentle sea-floor hillshade + isobaths
    ss = PAL["sea_shade"]
    hs_sea = shade(np.where(land, 0, elev), mpp, ss["exaggeration"], ss["azimuth"], ss["altitude"])
    sea = sea_colour(ndimage.gaussian_filter(depth, 0.8)) * (1 + ss["strength"] * (hs_sea[..., None] - hs_sea[~land].mean() if (~land).any() else 0))
    cr = PAL["contour_rgba"]; dsm = ndimage.gaussian_filter(depth, 2.5)
    for c in PAL["contours_m"]:
        b = dsm > c
        edge = (b ^ np.roll(b, 1, 0)) | (b ^ np.roll(b, 1, 1))
        edge &= ~land
        a = ndimage.gaussian_filter(edge.astype(np.float32), 0.6) * 1.6 * cr[3]
        sea = sea * (1 - a[..., None]) + np.array(cr[:3], np.float32) * a[..., None]
    # --- land: battle-maps LIFT hue, muted (multi-directional hillshade + elevation), median normalised
    lr = PAL["land_ramp"]; le = np.where(land, elev, 0)
    hs = 0.5 * shade(le, mpp, 3.0, 315, 38) + 0.3 * shade(le, mpp, 3.0, 260, 45) + 0.2 * shade(le, mpp, 3.0, 15, 50)
    hi = max(np.percentile(le[land], 99.5) if land.any() else 1, 1)
    a = 0.55 * hs + 0.45 * np.clip(le / hi, 0, 1) ** 0.6
    if land.any(): a = a * (lr["median"] / max(np.median(a[land]), 1e-3))
    a = np.clip(a, 0, 1)
    lo, hi_c = np.array(lr["low"], np.float32), np.array(lr["high"], np.float32)
    landc = lo + (hi_c - lo) * a[..., None]
    # --- coast: sand beach on the land side, soft blend, pale coastline
    coast = ndimage.gaussian_filter(land.astype(np.float32), 1.2)[..., None]
    beach = land & ~ndimage.binary_erosion(land, iterations=PAL["beach"]["width_px"])
    landc = np.where(beach[..., None], np.array(PAL["beach"]["rgb"], np.float32) * 0.85 + landc * 0.15, landc)
    rgb = sea * (1 - coast) + landc * coast
    cl = (np.abs(coast[..., 0] - 0.5) < 0.18).astype(np.float32)[..., None] * PAL["coastline"]["alpha"]
    rgb = rgb * (1 - cl) + np.array(PAL["coastline"]["rgb"], np.float32) * cl
    # --- light grain (as bake.py)
    rng = np.random.default_rng(218)
    g = np.asarray(Image.fromarray(rng.normal(128, 40, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32)
    rgb = rgb + (g[..., None] - 128) * 0.05
    os.makedirs(OUT, exist_ok=True)
    img = Image.fromarray(rgb.clip(0, 255).astype(np.uint8))
    img.save(os.path.join(OUT, f"{name}.jpg"), quality=90)
    json.dump({"name": name, "center": [lat, lon], "zoom": z, "origin_world_px": [x0, y0], "size": [W, H], "meters_per_px": round(mpp, 2),
               "sea_below": 0.5, "sea_level": 0, "depth_range_m": [float(depth.max()), float(elev.max())], "palette": "kit/ship/bathy/palette.json",
               "credit": PAL["credit"]}, open(os.path.join(OUT, f"{name}.json"), "w"), indent=1)
    print(name, f"{mpp:.0f} m/px", f"deepest {depth.max():.0f} m, highest {elev.max():.0f} m")
    if preview:
        pv = os.path.join(HERE, "..", "preview", f"{name}_preview.jpg")
        img.resize((1440, 810), Image.LANCZOS).save(pv, quality=84); print("preview", os.path.abspath(pv))
    return img, (x0, y0, z)


def strip(path):
    """the palette as a labelled strip (depth ramp + land ramp) for the README / review."""
    from PIL import ImageDraw, ImageFont
    font = ImageFont.truetype(os.path.join(HERE, "../../../tools/fonts/Anton-Regular.ttf"), 18)
    im = Image.new("RGB", (1440, 120), (12, 16, 22)); d = ImageDraw.Draw(im)
    ds = np.expm1(np.linspace(0, np.log1p(5000), 1100))
    col = sea_colour(ds).astype(np.uint8)
    for i in range(1100): d.line([(20 + i, 20), (20 + i, 70)], fill=tuple(col[i]))
    for m in [0, 10, 50, 200, 1000, 5000]:
        x = 20 + int(np.log1p(m) / np.log1p(5000) * 1099); d.line([(x, 70), (x, 78)], fill=(230, 222, 200)); d.text((x - 8, 82), f"{m} m", font=font, fill=(230, 222, 200))
    lr = PAL["land_ramp"]
    for i in range(260):
        c = np.array(lr["low"]) + (np.array(lr["high"]) - np.array(lr["low"])) * i / 259; d.line([(1160 + i, 20), (1160 + i, 70)], fill=tuple(int(v) for v in c))
    d.text((1160, 82), "LAND (MUTED LIFT RAMP)", font=font, fill=(230, 222, 200))
    im.save(path, quality=88); print("strip", path)


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    bake(a[0], float(a[1]), float(a[2]), int(a[3]), "--preview" in sys.argv)
    if "--preview" in sys.argv: strip(os.path.join(HERE, "..", "preview", "bathy_palette_strip.jpg"))
