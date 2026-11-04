#!/usr/bin/env python3
"""bake_clean.py - CLEAN map videos for the template library (map_clip): terrain, moving coastline, ice growth, ocean darkening, camera move.
NO text, NO pin, NO gauge are drawn (the templates draw them). Same look as the approved North Atlantic map (bake_hd dark grade + make_ice_progress ice),
but numpy/OpenCV only (no browser), so it runs in parallel on a rented CPU pod.

  python3 tools/bake_clean.py plan                    # list shots + views
  python3 tools/bake_clean.py bake [ID ...] [-j N]    # bake shots (all if none); outputs OUT_DIR/<id>.mp4 + <id>.json
  env: MAP_CACHE (default /tmp/mapbake: tiles, elevation, level renders), OUT_DIR, MAP_NE (Natural Earth geojson folder)

Stages (each parallel over N processes): 1 elevation per view  2 sea-level renders (every 4 m) + ice frames per view  3 frames -> ffmpeg per shot.
Coastline animation = cross-fade of real renders at 4 m steps, so the shore really moves. Ice = per-pixel arrival-time field, limited to LAND
at the current sea level (grounded Antarctic ice excepted); the ocean darkens (never drawn as ice). Shot table: tools/v01_map_shots.py."""
import os, sys, json, math, time, subprocess, urllib.request, urllib.error
import numpy as np, cv2
from PIL import Image
from scipy import ndimage
from concurrent.futures import ThreadPoolExecutor
cv2.setNumThreads(1)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lgm_polys import POLYS

W, H, S = 2880, 1620, 2                      # canvas, and HD factor used for shading
OW, OH, FPS = 1920, 1080, 30
CACHE = os.environ.get("MAP_CACHE", "/tmp/mapbake")
NE = os.environ.get("MAP_NE", os.path.join(HERE, "..", "assets", "src", "ne"))
OUT_DIR = os.environ.get("OUT_DIR", os.path.join(CACHE, "out"))
URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
EARTH = 6371000.0
LSTEP = 4                                    # metres between pre-rendered sea levels
NICE = 12                                    # ice frames: p = k/NICE
def P(*a): os.makedirs(os.path.join(CACHE, *a[:-1]), exist_ok=True); return os.path.join(CACHE, *a)

# ------------------------------------------------------------------ projections (canvas px = 2880x1620)
class Merc:
    kind = "merc"
    def __init__(s, lat, lon, z):
        s.lat0, s.lon0, s.z = lat, lon, z; s.N = 256 * 2 ** z
        cx, cy = s._w(lat, lon); s.ox, s.oy = cx - W / 2, cy - H / 2
    def _w(s, lat, lon, N=None):
        N = N or s.N; lat = np.clip(lat, -85.0511, 85.0511)
        return (np.asarray(lon, np.float64) + 180) / 360 * N, (1 - np.arcsinh(np.tan(np.radians(lat))) / np.pi) / 2 * N
    def fwd(s, lat, lon, wrap=True):
        lon = np.asarray(lon, np.float64)
        if wrap: lon = s.lon0 + ((lon - s.lon0 + 180) % 360 - 180)
        x, y = s._w(lat, lon); return x - s.ox, y - s.oy
    def inv(s, x, y):
        wx, wy = np.asarray(x, np.float64) + s.ox, np.asarray(y, np.float64) + s.oy
        return np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * wy / s.N)))), wx / s.N * 360 - 180
    def mpp(s, lat): return 156543.03392 * np.cos(np.radians(lat)) / 2 ** s.z      # metres per canvas px
    def key(s): return f"m_{s.lat0}_{s.lon0}_{s.z}"
class Polar:
    kind = "polar"
    def __init__(s, lat, lon, mpp, rot0=0.0):
        s.lat0, s.lon0, s.m, s.rot0 = lat, lon, mpp, rot0; s.cx, s.cy = s._p(lat, lon)
    def _p(s, lat, lon):
        r = 2 * EARTH * np.tan(np.radians(np.asarray(lat, np.float64) + 90) / 2); ph = np.radians(np.asarray(lon, np.float64) - s.rot0)
        return r * np.sin(ph) / s.m, -r * np.cos(ph) / s.m
    def fwd(s, lat, lon): x, y = s._p(lat, lon); return x - s.cx + W / 2, y - s.cy + H / 2
    def inv(s, x, y):
        px, py = np.asarray(x, np.float64) - W / 2 + s.cx, np.asarray(y, np.float64) - H / 2 + s.cy
        c = 2 * np.arctan(np.hypot(px, py) * s.m / (2 * EARTH)); return -90 + np.degrees(c), s.rot0 + np.degrees(np.arctan2(px, -py))
    def mpp(s, lat): return s.m * (1 + np.cos(np.radians(np.asarray(lat) + 90))) / 2
    def key(s): return f"p_{s.lat0}_{s.lon0}_{s.m}_{s.rot0}"
def make_proj(v):
    if v["proj"] == "polar": return Polar(v["lat"], v["lon"], v["mpp"], v.get("rot0", 0.0))
    return Merc(v["lat"], v["lon"], v["z"])

# ------------------------------------------------------------------ elevation (AWS Terrarium tiles)
def get_tile(z, x, y):
    x %= 2 ** z; path = P("tiles", f"{z}_{x}_{y}.png")
    if not os.path.exists(path):
        for k in range(6):
            try:
                with urllib.request.urlopen(URL.format(z=z, x=x, y=y), timeout=60) as r: data = r.read()
                open(path + ".tmp", "wb").write(data); os.replace(path + ".tmp", path); break
            except Exception as e:
                if k == 5: raise
                time.sleep(1 + k)
    a = np.asarray(Image.open(path).convert("RGB"), np.float32)
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768

def mosaic(Zt, tx0, tx1, ty0, ty1):
    ty0, ty1 = max(ty0, 0), min(ty1, 2 ** Zt - 1)
    jobs = [(tx, ty) for ty in range(ty0, ty1 + 1) for tx in range(tx0, tx1 + 1)]
    with ThreadPoolExecutor(16) as ex: tl = dict(zip(jobs, ex.map(lambda a: get_tile(Zt, *a), jobs)))
    return np.vstack([np.hstack([tl[(tx, ty)] for tx in range(tx0, tx1 + 1)]) for ty in range(ty0, ty1 + 1)]), ty0

def load_ne(name):
    return json.load(open(os.path.join(NE, name + ".geojson")))
def ne_fetch():
    os.makedirs(NE, exist_ok=True)
    for f in ("ne_10m_land", "ne_10m_antarctic_ice_shelves_polys", "ne_50m_admin_1_states_provinces", "ne_10m_lakes"):
        p = os.path.join(NE, f + ".geojson")
        if not os.path.exists(p):
            urllib.request.urlretrieve(f"https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/{f}.geojson", p)

def rings(gj, pred=None):
    for ft in gj["features"]:
        if pred and not pred(ft): continue
        g = ft["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys: yield poly

def raster_poly_px(V, poly, size, scale=1.0, minlat=None):
    """fill a lon/lat polygon (list of rings) into a uint8 mask of `size`=(h,w) at canvas*scale"""
    m = np.zeros(size, np.uint8)
    for k, ring in enumerate(poly):
        a = np.array(ring); x, y = V.fwd(a[:, 1], a[:, 0] if True else 0)
        pts = np.round(np.c_[x, y] * scale).astype(np.int32)
        cv2.fillPoly(m, [pts], 255 if k == 0 else 0)
    return m

def elevation(V, view):
    """raw HD elevation (m, 0 = today's sea level), shape (H*S, W*S)"""
    f = P("elev", V.key() + ".npy")
    if os.path.exists(f): return np.load(f)
    h, w = H * S, W * S
    if V.kind == "merc":
        Zt = int(math.ceil(V.z + 0.5)); k = 2 ** (Zt - V.z); Nt = 256 * 2 ** Zt
        x0, x1 = V.ox * k, (V.ox + W) * k; y0, y1 = V.oy * k, (V.oy + H) * k
        tx0, tx1, ty0, ty1 = int(x0 // 256), int((x1 - 1) // 256), int(y0 // 256), int((y1 - 1) // 256)
        mos, ty0c = mosaic(Zt, tx0, tx1, ty0, ty1)
        # world px -> mosaic px ; HD pixel (i,j) -> canvas (i+.5)/S
        sc = k / S
        M = np.array([[sc, 0, (V.ox * k - tx0 * 256) + 0.5 * sc - 0.5], [0, sc, (V.oy * k - ty0c * 256) + 0.5 * sc - 0.5]], np.float64)
        elev = cv2.warpAffine(mos, M, (w, h), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
    else:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        lat, lon = V.inv((xx + .5) / S, (yy + .5) / S); lat = lat.astype(np.float32); lon = lon.astype(np.float32)
        Zt = view.get("zt", 6); Nt = 256 * 2 ** Zt
        wy = ((1 - np.arcsinh(np.tan(np.radians(np.clip(lat, -85.05, 85.05)))) / np.pi) / 2 * Nt).astype(np.float32)
        lu = V.lon0 + ((lon - V.lon0 + 180) % 360 - 180); wx = ((lu + 180) / 360 * Nt).astype(np.float32)
        if wx.max() - wx.min() > Nt * 0.9: tx0, tx1 = 0, 2 ** Zt - 1; wx = ((lon % 360) / 360 * Nt).astype(np.float32)
        else: tx0, tx1 = int(wx.min() // 256), int(wx.max() // 256)
        ty0, ty1 = int(wy.min() // 256), int(wy.max() // 256)
        mos, ty0c = mosaic(Zt, tx0, tx1, ty0, ty1)
        elev = cv2.remap(mos, wx - tx0 * 256 - 0.5 + 0.5, np.clip(wy, 0, Nt - 1.01) - ty0c * 256, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        cap = np.clip((-lat - 80) / 4, 0, 1); elev = elev * (1 - cap) + 2400 * cap
        elev = antarctic_fix(V, elev, lat)
    elev = elev.astype(np.float32)
    _z = elev == 0; lab, n = ndimage.label(_z)                       # repair rectangular no-data holes in deep sea (as bake_hd)
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        m = lab[sl] == i; a = m.sum()
        if a > 1500 and a / m.size > 0.9:
            r = ndimage.binary_dilation(lab == i, iterations=6) & ~(lab == i)
            if np.median(elev[r]) < -30:
                idx = ndimage.distance_transform_edt(lab == i, return_distances=False, return_indices=True); elev[lab == i] = elev[tuple(idx[:, lab == i])]
    os.makedirs(os.path.dirname(f), exist_ok=True); np.save(f, elev); return elev

def antarctic_masks(V):
    """today's grounded continent + ice shelves (Natural Earth), HD mask; and the LGM grounded zone (out to the shelf edge) is made later"""
    ne_fetch(); h, w = H * S, W * S; m = np.zeros((h, w), np.uint8)
    for poly in rings(load_ne("ne_10m_land"), lambda ft: True):
        if min(p[1] for p in poly[0]) > -60: continue
        for k, ring in enumerate(poly):
            a = np.array(ring); a = a[a[:, 1] < -55] if False else a
            x, y = V.fwd(a[:, 1], a[:, 0]); cv2.fillPoly(m, [np.round(np.c_[x, y] * S).astype(np.int32)], 255 if k == 0 else 0)
    for poly in rings(load_ne("ne_10m_antarctic_ice_shelves_polys")):
        a = np.array(poly[0]); x, y = V.fwd(a[:, 1], a[:, 0]); cv2.fillPoly(m, [np.round(np.c_[x, y] * S).astype(np.int32)], 255)
    return ndimage.binary_closing(m > 127, iterations=3)
def antarctic_fix(V, elev, lat):
    cont = antarctic_masks(V); np.save(P("elev", V.key() + "_cont.npy"), cont)
    dist = ndimage.distance_transform_edt(cont); dome = np.clip(dist / (0.9 * max(dist.max(), 1)), 0, 1) ** 0.7 * 2900
    dome = ndimage.gaussian_filter(dome, 45)                                   # no medial-axis creases
    rough = noise(7, (500, 250), *elev.shape) * 45                         # the DEM under the ice is blocky: use smooth synthetic relief instead
    return np.where(cont, dome + rough + 30, np.where(elev > 0.5, elev, np.minimum(elev, -5)))

def hd_mpp(V):
    if V.kind == "merc":
        yy = (np.arange(H * S, dtype=np.float64) + .5) / S; lat, _ = V.inv(np.zeros_like(yy), yy)
        return (V.mpp(lat) / S).astype(np.float32)[:, None]
    yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32); lat, _ = V.inv((xx + .5) / S, (yy + .5) / S); return (V.mpp(lat) / S).astype(np.float32)
def canvas_latlon(V):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); lat, lon = V.inv(xx + .5, yy + .5); return lat.astype(np.float32), lon.astype(np.float32)

# ------------------------------------------------------------------ one sea-level render (the approved dark grade of bake_hd.py)
def blur_big(a, sigma, f=6):
    h, w = a.shape; s = a.reshape(h // f, f, w // f, f).mean((1, 3)); s = cv2.GaussianBlur(s, (0, 0), sigma / f)
    return cv2.resize(s, (w, h), interpolation=cv2.INTER_LINEAR)
class LevelCtx:
    def __init__(s, V, view, E):
        s.E = E
        lf = P("elev", V.key() + "_light.npy")
        if not os.path.exists(lf): np.save(lf, compute_light(V, view, E))
        s.light = np.load(lf)
        pos = E[E > 0.5]; s.hi = max(float(np.percentile(pos, 99.5)) if pos.size else 1.0, 1.0)
        s.lake = None; s.lake_level = None; s.force = None
        try:                                          # Terrarium has no bathymetry for the Caspian: keep it water at every sea level
            ne_fetch(); fm = np.zeros((H * S, W * S), np.uint8)
            for poly in rings(load_ne("ne_10m_land"), lambda ft: True):
                for hole in poly[1:]:                 # the Caspian Sea is a hole in the Eurasia land polygon
                    a = np.array(hole); cx_, cy_ = a[:, 0].mean(), a[:, 1].mean()
                    if not (46 < cx_ < 55 and 36 < cy_ < 48 and len(a) > 100): continue
                    x, y = V.fwd(a[:, 1], a[:, 0])
                    if x.max() < 0 or x.min() > W or y.max() < 0 or y.min() > H: continue
                    cv2.fillPoly(fm, [np.round(np.c_[x, y] * S).astype(np.int32)], 255)
            if fm.any(): s.force = fm > 0
        except Exception as e: print("caspian mask skipped", e)
        if view.get("lake"):
            lat, lon = view["lake"]["seed"]; level = view["lake"]["level"]; cand = E < level
            if view["lake"].get("box"):                       # keep the flood fill inside the basin (a lake whose sill is below the level would leak into the ocean)
                la0, la1, lo0, lo1 = view["lake"]["box"]; xa, ya = V.fwd(la1, lo0); xb, yb = V.fwd(la0, lo1); bm = np.zeros_like(cand); bm[int(ya * S):int(yb * S), int(xa * S):int(xb * S)] = True; cand &= bm
            lab, n = ndimage.label(cand)
            x, y = V.fwd(lat, lon); lid = lab[int(y * S), int(x * S)]
            if lid: s.lake = lab == lid; s.lake_level = level
def compute_light(V, view, E):
    """L-independent shading (4-direction hillshade + slope + ambient occlusion + fine texture) of the terrain above the lowest sea level (-120 m)"""
    exag = view.get("exag", 2.5); mpp = hd_mpp(V)
    le = np.maximum(E + 120.0, 0).astype(np.float32); sm = cv2.GaussianBlur(le, (0, 0), 1.0)
    gy, gx = np.gradient(sm * exag); gx = gx / mpp; gy = gy / mpp
    sa = np.arctan(np.hypot(gx, gy)); cs, ss = np.cos(sa), np.sin(sa); asp = np.arctan2(-gx, gy); ca, sn = np.cos(asp), np.sin(asp)
    def shade(az, alt):
        az, alt = math.radians(az), math.radians(alt); return np.clip(math.sin(alt) * cs + math.cos(alt) * ss * (math.cos(az) * ca + math.sin(az) * sn), 0, 1)
    hs = 0.45 * shade(315, 38) + 0.25 * shade(260, 45) + 0.18 * shade(15, 50) + 0.12 * shade(135, 60)
    sl = np.clip(np.degrees(sa) / 25, 0, 1)
    ao = np.clip((blur_big(le, 18) - le) / 40, -1, 1); fine = np.clip((le - cv2.GaussianBlur(le, (0, 0), 2.5)) * exag / 6, -1, 1)
    return np.clip(0.42 + 0.72 * hs - 0.16 * sl - 0.18 * np.clip(ao, 0, 1) + 0.08 * np.clip(-ao, 0, 1) + 0.10 * fine, 0, 1.25).astype(np.float16)
def render_level(c, L):
    E = c.E; elev = E - L; land = elev > 0.5
    if c.lake is not None and L < c.lake_level: land = land & ~c.lake
    if c.force is not None: land = land & ~c.force
    le = np.where(land, elev, 0).astype(np.float32); light = c.light.astype(np.float32)
    t = np.clip(le / c.hi, 0, 1)
    landf = land.astype(np.float32); coast = cv2.GaussianBlur(landf, (0, 0), 2.0)
    dark, lite = np.array([16, 22, 22], np.float32), np.array([138, 154, 140], np.float32)
    a = np.clip(light * 0.85 + t * 0.12, 0, 1) ** 1.15
    rgb = dark + (lite - dark) * a[..., None]
    dd = (np.clip(-elev / 3500, 0, 1) ** 0.6)[..., None]
    sea_c = np.array([30, 52, 62], np.float32) * (1 - dd) + np.array([9, 16, 24], np.float32) * dd
    halo = (blur_big(landf, 8, 4))[..., None] * (1 - coast[..., None])
    sea_c = sea_c + halo * np.array([14, 26, 28], np.float32)
    if L < -1:                                               # newly exposed shelf: warm olive tint
        shelf = cv2.GaussianBlur((land & (E <= 0)).astype(np.float32), (0, 0), 2.0)[..., None] * 0.55
        rgb = rgb * (1 - shelf) + (rgb * 0.55 + np.array([70, 62, 40], np.float32) * 0.6) * shelf
    rgb = sea_c * (1 - coast[..., None]) + rgb * coast[..., None]
    small = cv2.resize(rgb, (W, H), interpolation=cv2.INTER_AREA); cov = cv2.resize(coast, (W, H), interpolation=cv2.INTER_AREA)
    return np.dstack([np.clip(small, 0, 255), np.clip(cov, 0, 1) * 255]).astype(np.uint8)

def levels_file(vk, L): return P("levels", vk, f"L{int(L):+04d}.npy")

# ------------------------------------------------------------------ ice
def chaikin(pts, n):
    pts = list(pts); Ln = len(pts); out = []; M = 2 ** n
    for i in range(Ln):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % Ln], pts[(i + 2) % Ln]
        for j in range(M):
            t = j / M; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in range(2)))
    return out
def wobble(pts, amp, seed):
    rng = np.random.default_rng(seed); n = len(pts)
    off = ndimage.gaussian_filter(rng.normal(0, 1, n), 10, mode="wrap"); off = off / off.std() * amp; out = []
    for i, (x, y) in enumerate(pts):
        a, b = pts[i - 1], pts[(i + 1) % n]; tx, ty = b[0] - a[0], b[1] - a[1]; l = math.hypot(tx, ty) or 1
        out.append((x - ty / l * off[i], y + tx / l * off[i]))
    return out
def noise(seed, scales, h=H, w=W):
    r = np.random.default_rng(seed); o = np.zeros((h, w), np.float32)
    for i, s in enumerate(scales):
        n = r.normal(0, 1, (h // s + 3, w // s + 3)).astype(np.float32); o += ndimage.zoom(n, s, order=3)[:h, :w] / (1.7 ** i)
    return o / o.std()
SNOW_LAT = [0, 20, 30, 40, 50, 60, 70, 90]; SNOW_M = [4100, 3900, 3000, 2100, 1500, 1100, 900, 900]   # LGM snowline (m), rough

def poly_area_km2(pts):
    a = np.array(pts); la, lo = np.radians(a[:, 0]), np.radians(a[:, 1]); x = lo * np.cos(la.mean()); y = la
    return abs(0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)) * EARTH ** 2 / 1e6

def build_ice(V, view, E):
    """-> dict(frames=(NICE+1,H,W,4) uint8, dark_k (H,W) f16, free (H,W) uint8: grounded ice allowed over water)"""
    lat, lon = canvas_latlon(V); mpp = V.mpp(lat).astype(np.float32)
    elev = cv2.resize(E, (W, H), interpolation=cv2.INTER_AREA); lf = elev > -119.5          # land at the lowest level (-120 m)
    land = lf
    latb = np.clip((np.abs(lat) - 48) / 24, 0, 1)
    nA, nB, nE = noise(1, (400, 160, 70, 30)), noise(2, (60, 24, 10)), noise(3, (200, 90, 40, 18))
    lf_ = P("elev", V.key() + "_light.npy")
    light_c = cv2.resize(np.load(lf_).astype(np.float32), (W, H), interpolation=cv2.INTER_AREA)            # L-independent terrain shading (same as the base map)
    shade = np.clip((light_c - 0.40) * 1.8 + 0.5, 0.12, 1.0)
    rel = np.clip((light_c - cv2.GaussianBlur(light_c, (0, 0), 25)) * 3.2 + 0.5, 0.0, 1.0).astype(np.float32)   # local relief contrast: ridges lit, valleys dark
    T = np.full((H, W), 9.0, np.float32); Mk = np.zeros((H, W), np.float32); free = np.zeros((H, W), np.uint8)
    if V.kind == "polar":
        cont = np.load(P("elev", V.key() + "_cont.npy")); cont = cv2.resize(cont.astype(np.uint8), (W, H), interpolation=cv2.INTER_AREA) > 0
        bathy = np.where(cont, 0, elev); dkm = ndimage.distance_transform_edt(~cont) * mpp / 1000.0
        zone = (cont | ((bathy > view.get("shelf_edge", -550)) & (dkm < 900))) & (lat < -58)
        zone = ndimage.binary_closing(zone, iterations=4); zone = ndimage.binary_fill_holes(zone)
        zone = zone & ((dkm < 40) | (cv2.GaussianBlur(zone.astype(np.float32), (0, 0), 6) > 0.5))
        dmax = max(float(dkm[zone].max()), 1.0)
        Tz = np.where(cont, 0.05, 0.12 + 0.62 * np.clip(dkm / dmax, 0, 1) ** 0.9) + 0.06 * nA
        T = np.where(zone, Tz, 9.0).astype(np.float32); Mk = cv2.GaussianBlur(zone.astype(np.float32), (0, 0), 1.0); free = (zone * 255).astype(np.uint8)
        np.save(P("elev", V.key() + "_zone.npy"), zone)
    else:
        bx0, bx1 = 0, W
        for k, poly in POLYS.items():
            a = np.array(poly, float); lo = np.degrees(np.unwrap(np.radians(a[:, 1]))); lo = lo + 360 * np.round((V.lon0 - lo.mean()) / 360)     # keep the outline contiguous across the antimeridian
            fx, fy = V.fwd(a[:, 0], lo, wrap=False)
            if fx.max() < -300 or fx.min() > W + 300 or fy.max() < -300 or fy.min() > H + 300: continue
            if V.kind == "merc" and abs(V.lat0) > 80: continue
            pts = wobble(chaikin(list(zip(fx, fy)), 4), 6, 7)
            m = np.zeros((H * 2, W * 2), np.uint8); cv2.fillPoly(m, [np.round(np.array(pts) * 2).astype(np.int32)], 255)
            m = cv2.resize(m, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
            d = ndimage.distance_transform_edt(m > 0.5) * mpp / 1000.0
            rmax = math.sqrt(poly_area_km2(poly) / math.pi)
            dn = np.clip(d / (0.55 * rmax), 0, 1)
            if k == "iceland": dn = np.clip(d / (rmax), 0, 1)
            Ts = 0.74 - 0.6 * dn
            T = np.minimum(T, np.where(m > 0.5, Ts, 9.0)); Mk = np.maximum(Mk, m)
        dfield = ndimage.distance_transform_edt(Mk > 0.5) * 1.0
        inside = Mk > 0.5
        Mk = np.clip((dfield + nE * 14 - 3) / 22, 0, 1) * inside; Mk = Mk * Mk * (3 - 2 * Mk)
    hi = np.clip((elev - 250) / 1700, 0, 1); hi = hi * hi * (3 - 2 * hi)
    T = T - 0.42 * hi * land - 0.16 * latb + 0.12 * nA
    T = np.where(T > 8, 9.0, np.clip(T, 0.04, 0.80)).astype(np.float32)
    snowline = np.interp(np.abs(lat), SNOW_LAT, SNOW_M).astype(np.float32)
    alp = np.clip((elev - snowline) / 700, 0, 1) * land * (1 - Mk) * (np.abs(lat) < 75)
    Talp = 0.45 - 0.2 * np.clip((elev - snowline) / 1500, 0, 1) + 0.1 * nA
    dk = (0.30 * (0.8 + 0.55 * latb)).astype(np.float16)
    frames = np.zeros((NICE + 1, H, W, 4), np.uint8)
    for i in range(1, NICE + 1):
        p = i / NICE
        a = np.clip((p - T + 0.07 * nB) / 0.22, 0, 1); a = a * a * (3 - 2 * a) * Mk
        aa = np.clip((p - Talp + 0.06 * nB) / 0.2, 0, 1) ** 2 * alp
        land_a = np.clip(np.maximum(a, aa), 0, 1) * np.maximum(land, free > 0)
        lit = shade[..., None]
        rgb = np.array([105, 138, 182]) * (1 - lit) + np.array([244, 249, 255]) * lit
        rgb = rgb * (0.62 + 0.55 * rel[..., None]) * (1 + 0.03 * nB[..., None])
        rim = np.clip(land_a * (1 - land_a) * 4, 0, 1)[..., None]; rgb = rgb + rim * 30
        al = land_a * (0.66 + 0.16 * (shade - 0.5))
        frames[i] = np.dstack([np.clip(rgb, 0, 255), np.clip(al, 0, 0.95) * 255]).astype(np.uint8)
    return dict(frames=frames, dark_k=dk, free=free)

# ------------------------------------------------------------------ per-view preparation (stage 1/2 tasks)
def view_elev_task(vk, view):
    V = make_proj(view); t = time.time(); E = elevation(V, view); LevelCtx(V, view, E); return vk, round(time.time() - t, 1)
def level_task(vk, view, L):
    f = levels_file(vk, L)
    if os.path.exists(f): return vk, L, 0
    V = make_proj(view); E = elevation(V, view); t = time.time(); c = LevelCtx(V, view, E); r = render_level(c, L)
    os.makedirs(os.path.dirname(f), exist_ok=True); np.save(f + ".tmp.npy", r); os.replace(f + ".tmp.npy", f); return vk, L, round(time.time() - t, 1)
def ice_task(vk, view):
    f = P("ice", vk + "_frames.npy")
    if os.path.exists(f): return vk, 0
    V = make_proj(view); E = elevation(V, view); t = time.time(); r = build_ice(V, view, E)
    np.save(P("ice", vk + "_dark.npy"), r["dark_k"]); np.save(P("ice", vk + "_free.npy"), r["free"]); np.save(f + ".tmp.npy", r["frames"]); os.replace(f + ".tmp.npy", f)
    return vk, round(time.time() - t, 1)

if __name__ == "__main__":
    from bake_run import main
    main(sys.argv[1:])
