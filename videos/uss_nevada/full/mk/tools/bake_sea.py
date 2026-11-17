"""Sea-first basemap for the ship channel: bathymetry is the subject (seafloor relief + depth ramp + contours),
land is a dark muted plate with a thin gold coastline. Same projection/json as bake.py so the map-kit engine works.
usage: python3 bake_sea.py NAME LAT LON ZOOM   (renders from ZOOM+1 tiles, downsampled 2x = sharp)"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bake import world_px, tile, blur, ASSETS
W, H = 2880, 1620
# depth ramp (m below sea level -> colour): shallow teal shelf -> navy -> abyss
RAMP = [(0, (58, 120, 128)), (15, (40, 98, 112)), (40, (28, 76, 98)), (80, (20, 58, 84)), (200, (14, 42, 66)),
        (1000, (9, 28, 48)), (3000, (5, 16, 30))]
LAND_LO, LAND_HI = np.array([46, 47, 42], float), np.array([78, 76, 64], float)
GOLD = np.array([201, 180, 138], float)

def ramp(d):
    ds = np.array([r[0] for r in RAMP], float); cs = np.array([r[1] for r in RAMP], float)
    return np.stack([np.interp(d, ds, cs[:, i]) for i in range(3)], -1)

OVERPASS = ["https://overpass.openstreetmap.fr/api/interpreter", "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter"]

def osm_coast(s, w, n, e):
    """OSM natural=coastline ways (lists of (lat, lon); land is on the LEFT of travel) for a bbox, cached in .tiles."""
    import hashlib, urllib.request, urllib.parse, time
    from bake import CACHE
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.md5(f"{s:.4f},{w:.4f},{n:.4f},{e:.4f}".encode()).hexdigest()[:12]
    path = os.path.join(CACHE, f"osmcoast_{key}.json")
    if not os.path.exists(path):
        q = f'[out:json][timeout:180];way["natural"="coastline"]({s},{w},{n},{e});out geom;'
        for k in range(6):
            url = OVERPASS[k % len(OVERPASS)]
            try:
                req = urllib.request.Request(url, urllib.parse.urlencode({"data": q}).encode(), {"User-Agent": "shipchannel-bake/1.0"})
                data = urllib.request.urlopen(req, timeout=200).read()
                json.loads(data); open(path + ".part", "wb").write(data); os.replace(path + ".part", path); break
            except Exception as ex:
                print("overpass retry", url, ex, flush=True); time.sleep(3 + 3 * k)
        else:
            raise SystemExit("WATERMASK=osm: no Overpass server answered")
    d = json.load(open(path))
    return [[(p["lat"], p["lon"]) for p in el["geometry"]] for el in d["elements"] if el.get("geometry")]

def osm_water_mask(lat, lon, zz, x0, y0, S):
    """bool (H, W) land mask on the output grid from OSM coastlines + (land-left rule) component voting; NaN-free:
    returns (land, known) where known=False for pixels in components no coastline could classify."""
    from PIL import ImageDraw
    from scipy import ndimage as ndi
    def px(la, lo):
        a, b = world_px(la, lo, zz); return ((a - x0) / S, (b - y0) / S)
    # bbox of the frame (+margin) from the corner pixels
    def ll(xp, yp):
        n_ = 256 * 2 ** zz; wx, wy = x0 + xp * S, y0 + yp * S
        return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * wy / n_)))), wx / n_ * 360 - 180
    n_, w_ = ll(-60, -60); s_, e_ = ll(W + 60, H + 60)
    ways = osm_coast(s_, w_, n_, e_)
    img = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(img); segs = []
    for wy_ in ways:
        pts = [px(*p) for p in wy_]
        dr.line(pts, fill=255, width=3)
        for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
            L = math.hypot(bx - ax, by - ay)
            if L < 1e-6: continue
            k = max(1, int(L // 40)) # a vote every ~40 px along long segments
            for t in (np.arange(k) + 0.5) / k:
                mx, my = ax + (bx - ax) * t, ay + (by - ay) * t
                lx, ly = (by - ay) / L, -(bx - ax) / L   # left of travel in y-down pixel coords
                segs.append((mx, my, lx, ly))
    line = np.asarray(img) > 0
    lab, nl = ndi.label(~line)
    land_v = np.zeros(nl + 1); sea_v = np.zeros(nl + 1)
    for mx, my, lx, ly in segs:
        for sgn, arr in ((1, land_v), (-1, sea_v)):
            xi, yi = int(round(mx + sgn * lx * 5)), int(round(my + sgn * ly * 5))
            if 0 <= xi < W and 0 <= yi < H and lab[yi, xi]: arr[lab[yi, xi]] += 1
    cls = np.where(land_v > sea_v, 1, np.where(sea_v > land_v, -1, 0))
    cls[0] = 0
    m = cls[lab]
    # coastline pixels take the class of the nearest classified pixel
    idx = ndi.distance_transform_edt(m == 0, return_distances=False, return_indices=True)
    m = m[idx[0], idx[1]]
    known = np.zeros((H, W), bool)
    known[:] = (cls[lab] != 0) | line
    print("osm coast:", len(ways), "ways,", nl, "regions,", int((cls[1:] != 0).sum()), "classified", flush=True)
    return m > 0, known

def main(name, lat, lon, z):
    S = int(os.environ.get('SS', 2)); zz = z + (1 if S == 2 else 0)
    cx, cy = world_px(lat, lon, zz); x0, y0 = int(cx - W * S / 2), int(cy - H * S / 2)
    tx0, ty0, tx1, ty1 = x0 // 256, y0 // 256, (x0 + W * S) // 256, (y0 + H * S) // 256
    mosaic = np.vstack([np.hstack([tile(zz, tx, ty) for tx in range(tx0, tx1 + 1)]) for ty in range(ty0, ty1 + 1)])
    e2 = mosaic[y0 - ty0 * 256:y0 - ty0 * 256 + H * S, x0 - tx0 * 256:x0 - tx0 * 256 + W * S]
    elev = e2.reshape(H, S, W, S).mean(axis=(1, 3)) if S > 1 else e2
    # fill data holes (flat 0 tiles at high zoom over open sea) from a lower zoom, bilinear
    zl = max(zz - 3, 1); f = 2 ** (zz - zl)
    gx0, gy0 = x0 / S, y0 / S  # in zz/S world px... recompute exactly per output pixel below
    YY, XX = np.mgrid[0:H, 0:W].astype(float)
    wx = (x0 + (XX + 0.5) * S) / f; wy = (y0 + (YY + 0.5) * S) / f
    lx0, ly0 = int(wx.min()) // 256, int(wy.min()) // 256; lx1, ly1 = int(wx.max()) // 256, int(wy.max()) // 256
    low = np.vstack([np.hstack([tile(zl, tx, ty) for tx in range(lx0, lx1 + 1)]) for ty in range(ly0, ly1 + 1)])
    from scipy.ndimage import map_coordinates
    lowv = map_coordinates(low, [wy - ly0 * 256, wx - lx0 * 256], order=1)
    hole = (np.abs(elev) < 0.6) & (lowv < -3)
    hole = blur(hole.astype(float), 1) > 0.05
    elev = np.where(hole, lowv, elev)
    # v3 seam fix: the sea floor always comes from the smooth lower-zoom data (one source = no seam where the
    # high-zoom tiles stop); land and the coastline keep the full-detail data.
    land_hi = elev > 0.5
    elev = np.where(land_hi, elev, np.minimum(lowv, -0.6))
    if os.environ.get('WATERMASK') == 'osm':   # OSM coastline overrides the DEM land/sea (Terrarium shows harbours as land)
        oland, known = osm_water_mask(lat, lon, zz, x0, y0, S)
        osea = ~oland & known
        oland &= known
        # harbour water: shallow teal (-12 m); next to open sea the depth blends smoothly into the real bathymetry
        from scipy import ndimage as ndi
        bad = osea & (elev > -4.0); good = osea & ~bad
        if bad.any() and good.any():
            d, (iy, ix) = ndi.distance_transform_edt(~good, return_indices=True)
            near = np.minimum(elev[iy, ix], -12.0)
            fill = -12.0 + (near + 12.0) * np.exp(-d / 80.0)
            elev = np.where(bad, blur(np.where(bad, fill, -12.0), 4), elev)
        elif bad.any():
            elev = np.where(bad, -12.0, elev)
        elev = np.where(oland & (elev < 0.5), 2.0, elev)
        print("watermask: sea forced", int((osea).sum()), "land forced", int(oland.sum()), flush=True)
    mpp = 156543.03392 * math.cos(math.radians(lat)) / 2 ** z
    land = elev > 0.5
    # seafloor hillshade (exaggerated: the Gulf shelf is very flat)
    sea_e = np.where(land, 0, elev); sm = blur(sea_e, 2)
    gy, gx = np.gradient(sm * 60, mpp); slope, aspect = np.arctan(np.hypot(gx, gy)), np.arctan2(-gx, gy)
    def shade(az, alt):
        az, alt = math.radians(az), math.radians(alt)
        return np.clip(np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect), 0, 1)
    hs = 0.65 * shade(315, 35) + 0.35 * shade(220, 55)
    depth = np.clip(-sm, 0, None)
    sea = ramp(depth) * (0.72 + 0.5 * hs[..., None])
    # depth contours (20, 50, 100, 200, 500, 1000, 2000 m): thin light lines
    cont = np.zeros((H, W))
    for lv in (20, 50, 100, 200, 500, 1000, 2000):
        b = (depth > lv).astype(float); edge = np.abs(blur(b, 1) - 0.5) < 0.18
        cont = np.maximum(cont, edge * (0.22 if lv < 200 else 0.14))
    sea = sea * (1 - cont[..., None]) + np.array([150, 200, 210]) * cont[..., None]
    # land: dark plate with soft relief
    le = np.where(land, elev, 0); ls = blur(le, 1)
    gy, gx = np.gradient(ls * 8, mpp); sl2, as2 = np.arctan(np.hypot(gx, gy)), np.arctan2(-gx, gy)
    hl = np.clip(np.sin(math.radians(40)) * np.cos(sl2) + np.cos(math.radians(40)) * np.sin(sl2) * np.cos(math.radians(315) - as2), 0, 1)
    t = np.clip(le / max(np.percentile(le[land], 99) if land.any() else 1, 1), 0, 1)[..., None]
    lnd = (LAND_LO * (1 - t) + LAND_HI * t) * (0.6 + 0.6 * hl[..., None])
    coast = blur(land.astype(float), 2)[..., None]
    rgb = sea * (1 - coast) + lnd * coast
    edge = (np.abs(coast[..., 0] - 0.5) < 0.16)[..., None]
    rgb = rgb * (1 - edge * 0.75) + GOLD * edge * 0.75
    rng = np.random.default_rng(34)
    grain = np.asarray(Image.fromarray(rng.normal(128, 40, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), float)
    rgb = rgb + (grain[..., None] - 128) * 0.05
    os.makedirs(ASSETS, exist_ok=True)
    Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).save(os.path.join(ASSETS, f"{name}.jpg"), quality=92)
    ox, oy = world_px(lat, lon, z); ox, oy = int(ox - W / 2), int(oy - H / 2)
    json.dump({"name": name, "center": [lat, lon], "zoom": z, "origin_world_px": [ox, oy], "size": [W, H], "meters_per_px": round(mpp, 2),
               "credit": "Terrain & bathymetry: Mapzen / AWS Terrain Tiles (open data)"}, open(os.path.join(ASSETS, f"{name}.json"), "w"), indent=1)
    print(name, f"{mpp:.1f} m/px", f"elev {elev.min():.0f}..{elev.max():.0f}", "origin", ox, oy)

if __name__ == "__main__":
    a = sys.argv[1:]; main(a[0], float(a[1]), float(a[2]), int(a[3]))
