#!/usr/bin/env python3
"""bake_v02.py - CLEAN map videos for Video 02 (crocodile rivers). Same look as bake_clean.py (dark teal sea, olive land,
relief shading) but terrain can come from the PALEOMAP PaleoDEMs (Scotese & Wright 2018, CC BY 4.0) for deep time, or from
the AWS Terrarium tiles (present day, optional SEA_LEVEL shift). No text, no pin: the map_clip template draws those.

  venv/bin/python tools/bake_v02.py [ID ...] [--still]       # all shots if no id; --still = 3 test frames only
  env: V02_CACHE (default maps/cache_v02: PaleoDEMs, tiles, Natural Earth lakes), OUT_DIR (default videos/video02/maps)

PaleoDEMs: put the 6-min netCDFs in $V02_CACHE/paleodem (tools/remote_zip.py pulls single members out of the Zenodo zip).
Pin positions of deep-time places = present-day coordinates rotated with the PALEOMAP plate model (GPlates Web Service,
gws.gplates.org reconstruct_points model=PALEOMAP), checked against the PaleoDEM coastlines."""
import os, sys, json, math, glob, time, subprocess, urllib.request
import numpy as np, cv2, h5py
from scipy import ndimage
from concurrent.futures import ThreadPoolExecutor
cv2.setNumThreads(3)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CACHE = os.environ.get("V02_CACHE", os.path.join(ROOT, "maps", "cache_v02"))
OUT = os.environ.get("OUT_DIR", os.path.join(ROOT, "videos", "video02", "maps"))
W, H, OW, OH, FPS = 5760, 3240, 1920, 1080, 30         # canvas = 3x the frame at zoom 1 (2x supersampled vs the kit's 2880 canvas)
UNSHARP = float(os.environ.get('UNSHARP', '0.55'))
SS = 2                                                  # frames are warped at 2x (3840x2160) and area-downscaled
TEX_SCALE = float(os.environ.get('TEX_SCALE', '2.0')); PALEO_SMOOTH = float(os.environ.get('PALEO_SMOOTH', '2.2')); PALEO_EXAG = float(os.environ.get('PALEO_EXAG', '6')); PALEO_DEXAG = float(os.environ.get('PALEO_DEXAG', '1.0'))
URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"

# ------------------------------------------------------------------ shots
# pin = (lat, lon) in the map's own coordinates (paleo-coordinates for deep time), modern = present-day place
PALEO_FILE = {305: "Map58_*_305Ma.nc", 220: "Map45_*_220Ma.nc", 150: "Map33_*_150Ma.nc", 110: "Map25_*_110Ma.nc",
              95: "Map22_*_95Ma.nc", 80: "Map19_*_80Ma.nc", 65: "Map16_*_65Ma.nc", 60: "Map15_*_60Ma.nc"}
SHOTS = {
 "R04":    dict(src="now", c=(14, 18), span=360, z=(1.03, 1.075), drift=(-52, 0), est=3.28, place="world (12 pins added by the template)"),
 "C01-02": dict(src=305, c=(4, -18), span=140, z=(1.0, 1.28), pin=(-3.17, -21.56), modern=(41.3, -88.2), est=2.12, place="Mazon Creek coal swamp, Illinois (equatorial coal belt of Euramerica)"),
 "C02-02": dict(src=150, c=(36, -62), span=75, z=(1.0, 1.25), pin=(37.11, -61.71), modern=(40.4, -109.3), est=4.05, place="Morrison Formation, Dinosaur National Monument area (Utah/Colorado)"),
 "C03-02": dict(src=65, c=(46, -78), span=80, z=(1.0, 1.25), pin=(53.49, -82.40), modern=(47.3, -106.9), est=4.48, place="Hell Creek Formation, Jordan, Montana"),
 "C04-02": dict(src=220, c=(6, -42), span=90, z=(1.0, 1.25), pin=(10.30, -52.12), modern=(35.0, -109.8), est=4.16, place="Chinle Formation, Petrified Forest, Arizona"),
 "C05-02": dict(src="now", sea=-70, c=(-14, 141), span=46, z=(1.0, 1.3), pin=(-21.7, 148.3), est=4.53, place="South Walker Creek, west of Mackay, Queensland", exag=3.0),
 "C06-02": dict(src="now", c=(2.5, 36.5), span=22, z=(1.0, 1.28), pin=(3.6, 36.1), est=4.32, place="Turkana Basin (Koobi Fora side), northern Kenya", exag=2.0),
 "C07-02": dict(src="now", c=(52.8, -2.5), span=15, z=(1.0, 1.25), pin=(51.51, -0.12), est=2.32, place="London, River Thames", exag=3.0),
 "C07-25": dict(src="now", c=(54.6, 2.5), span=17, z=(1.0, 1.15), pin=(55.0, 3.0), extra={"thames_mouth": (51.5, 0.9)}, est=3.49, place="North Sea (centre); Thames mouth in extra", exag=3.0, winter=True),
 "C08-02": dict(src=60, c=(6, -56), span=56, z=(1.0, 1.25), pin=(8.47, -59.24), modern=(11.1, -72.6), est=4.08, place="Cerrejon coal mine, La Guajira, Colombia"),
 "C09-02": dict(src=80, c=(37, -76), span=50, z=(1.0, 1.25), pin=(35.35, -74.58), modern=(29.3, -103.2), est=2.96, place="Big Bend, Texas (Aguja Formation)"),
 "C09-16": dict(src=80, c=(48, -78), span=120, z=(1.0, 1.06), pin=(35.35, -74.58), modern=(29.3, -103.2), est=3.09, place="Western Interior Seaway, both coasts (pin = Big Bend)", focus=0.2),
 "C10-02": dict(src=110, c=(2, 6), span=60, z=(1.0, 1.25), pin=(1.59, 3.56), modern=(16.4, 9.0), est=5.08, place="Gadoufaoua / Elrhaz Formation, Niger"),
 "C11-02": dict(src="now", c=(-4.5, -69), span=32, z=(1.0, 1.22), pin=(-3.32, -71.85), est=3.0, place="Pebas, north-east Peru (western Amazonia)", exag=4.0, pebas=True),
 "C12-02": dict(src=95, c=(16, -2), span=56, z=(1.0, 1.25), pin=(18.27, -4.47), modern=(30.9, -4.0), est=3.92, place="Kem Kem beds, south-east Morocco"),
}
# R04: the 12 rivers, present-day places, chapter order
R04_PINS = [("coal swamp (Illinois)", 41.3, -88.2), ("Morrison (Utah/Colorado)", 40.4, -109.3), ("Hell Creek (Montana)", 47.3, -106.9),
            ("Chinle (Arizona)", 35.0, -109.8), ("South Walker Creek (Queensland)", -21.7, 148.3), ("Turkana (Kenya)", 3.6, 36.1),
            ("Thames (London)", 51.51, -0.12), ("Cerrejon (Colombia)", 11.1, -72.6), ("Big Bend (Texas)", 29.3, -103.2),
            ("Gadoufaoua (Niger)", 16.4, 9.0), ("Pebas (Peru)", -3.32, -71.85), ("Kem Kem (Morocco)", 30.9, -4.0)]

# ------------------------------------------------------------------ projection: Mercator, canvas W x H, `span` degrees of longitude across W
def mercy(lat): return np.degrees(np.log(np.tan(np.pi / 4 + np.radians(np.clip(lat, -85, 85)) / 2)))
class Merc:
    def __init__(s, lat0, lon0, span): s.lat0, s.lon0, s.k = lat0, lon0, W / span; s.y0 = mercy(lat0)
    def fwd(s, lat, lon, wrap=True):
        lon = np.asarray(lon, np.float64)
        if wrap: lon = s.lon0 + ((lon - s.lon0 + 180) % 360 - 180)
        return W / 2 + (lon - s.lon0) * s.k, H / 2 - (mercy(lat) - s.y0) * s.k
    def inv(s, x, y):
        my = s.y0 - (np.asarray(y, np.float64) - H / 2) / s.k
        return np.degrees(2 * np.arctan(np.exp(np.radians(my))) - np.pi / 2), s.lon0 + (np.asarray(x, np.float64) - W / 2) / s.k
    def mpp(s, lat): return 111320.0 * np.cos(np.radians(lat)) / s.k

def grid_latlon(V):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); lat, lon = V.inv(xx + .5, yy + .5); return lat.astype(np.float32), lon.astype(np.float32)
def mpp_rows(V):
    lat, _ = V.inv(np.zeros(H), np.arange(H) + .5); return V.mpp(lat).astype(np.float32)[:, None]

# ------------------------------------------------------------------ noise
def noise(seed, scales, h=None, w=None):
    """band-limited gaussian noise, sum of octaves (scales in px, >= 2)"""
    h = h or H; w = w or W; r = np.random.default_rng(seed); o = np.zeros((h, w), np.float32)
    for i, s in enumerate(scales):
        s = max(2, int(round(s))); n = r.normal(0, 1, (h // s + 4, w // s + 4)).astype(np.float32)
        o += cv2.resize(n, ((w // s + 4) * s, (h // s + 4) * s), interpolation=cv2.INTER_CUBIC)[:h, :w] / (1.8 ** i)
    return o / (o.std() + 1e-6)
def octave(seed, s):
    s = max(2, int(round(s))); n = np.random.default_rng(seed).normal(0, 1, (H // s + 4, W // s + 4)).astype(np.float32)
    o = cv2.resize(n, ((W // s + 4) * s, (H // s + 4) * s), interpolation=cv2.INTER_CUBIC)[:H, :W]; return o / (o.std() + 1e-6)

# ------------------------------------------------------------------ elevation sources
def elev_paleo(V, age):
    """smooth PaleoDEM surface (geography) + a separate fine-relief field (texture only, no new land)"""
    f = glob.glob(os.path.join(CACHE, "paleodem", PALEO_FILE[age]))[0]
    z = h5py.File(f, "r")["z"][:].astype(np.float32)                 # rows 90 -> -90, cols -180 -> 180 at 0.1 deg
    z = np.hstack([z[:, -21:-1], z, z[:, 1:21]])                       # wrap pad (col 0 and last are the same meridian)
    z = cv2.GaussianBlur(z, (0, 0), PALEO_SMOOTH)                      # cell speckle, contour terraces and blotches of the grid
    lat, lon = grid_latlon(V); lon = (lon + 180) % 360 - 180
    mx = ((lon + 180) * 10 + 20).astype(np.float32); my = ((90 - lat) * 10).astype(np.float32)
    E = cv2.remap(z, mx, my, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE); del mx, my, lat, lon
    pxc = V.k / 10.0                                                    # canvas px per grid cell
    E = cv2.GaussianBlur(E, (0, 0), max(1.5, 0.7 * pxc))               # no cubic cell seams
    mpp = float(np.median(mpp_rows(V)))                                 # metres per canvas px
    km = lambda x: max(8.0, x * 1000.0 / mpp)                          # km -> canvas px (never finer than ~3 px of the final frame)
    # coastline: keep the PaleoDEM 0 m line, add only a little natural irregularity (wavelengths 8-40 frame px)
    E = E + noise(31, (120, 50, 24)) * 16.0 * np.exp(-np.abs(E) / 90.0)
    # fine relief = TEXTURE ONLY (no new land): a high-passed, normalised patch of real present-day terrain (Terrarium z6,
    # Arabia to Mongolia), mirrored and resampled, so valleys and ridges erode like real ones. Its height is set from a target slope:
    # ~4 % on lowlands, ~35 % on mountain belts (from PaleoDEM height and slope); none at sea.
    gy, gx = np.gradient(cv2.GaussianBlur(E, (0, 0), 6)); slope = np.hypot(gx, gy) / mpp; del gx, gy
    land = np.clip(E / 40.0, 0, 1)
    mtn = np.clip((E - 300) / 1400, 0, 1) ** 0.8
    mtn = np.maximum(mtn, np.clip((slope - 0.004) / 0.02, 0, 1) * np.clip(E / 300, 0, 1))      # steep flanks count as uplands
    T, g0 = relief_texture(age)
    target = 0.03 * (1 - mtn) + 0.24 * mtn
    D = land * T * (target * mpp / g0)
    return E.astype(np.float32), D.astype(np.float32)

TEX_BOX = (18.0, 50.0, 38.0, 112.0)                                   # lat0, lat1, lon0, lon1 of the texture source (real terrain, z6)
def relief_texture(seed):
    """unit-variance relief texture covering the canvas (mirrored real terrain); returns (T, mean |grad T| per canvas px)"""
    la0, la1, lo0, lo1 = TEX_BOX; z = 6; N = 256 * 2 ** z
    x0, x1 = int((lo0 + 180) / 360 * N) // 256, int((lo1 + 180) / 360 * N) // 256
    yf = lambda la: (1 - math.asinh(math.tan(math.radians(la))) / math.pi) / 2 * N
    y0, y1 = int(yf(la1)) // 256, int(yf(la0)) // 256
    jobs = [(tx, ty) for ty in range(y0, y1 + 1) for tx in range(x0, x1 + 1)]
    with ThreadPoolExecutor(8) as ex: tl = dict(zip(jobs, ex.map(lambda a: get_tile(z, *a), jobs)))
    src = np.vstack([np.hstack([tl[(tx, ty)] for tx in range(x0, x1 + 1)]) for ty in range(y0, y1 + 1)]).astype(np.float32)
    src = cv2.medianBlur(src, 3)
    hp = src - cv2.GaussianBlur(src, (0, 0), 14)                       # keep valleys/ridges, drop the continent-scale shape
    sd = np.sqrt(cv2.GaussianBlur(hp * hp, (0, 0), 20)); hp = hp / np.maximum(sd, 10.0)   # equal texture strength everywhere
    hp = np.clip(hp, -3, 3)
    rng = np.random.default_rng(seed)
    if rng.random() < 0.5: hp = hp[:, ::-1]
    if rng.random() < 0.5: hp = hp[::-1]
    sc = max(TEX_SCALE, (H + 8) / hp.shape[0], (W + 8) / hp.shape[1])     # one piece of real terrain, no mirror seams
    big = cv2.resize(hp, (int(math.ceil(hp.shape[1] * sc)), int(math.ceil(hp.shape[0] * sc))), interpolation=cv2.INTER_CUBIC)
    oy, ox = rng.integers(0, big.shape[0] - H + 1), rng.integers(0, big.shape[1] - W + 1)
    T = big[oy:oy + H, ox:ox + W]
    T = (T - T.mean()) / (T.std() + 1e-6); gy, gx = np.gradient(T)
    return T.astype(np.float32), float(np.mean(np.hypot(gx, gy)))

def get_tile(z, x, y):
    x %= 2 ** z; p = os.path.join(CACHE, "tiles", f"{z}_{x}_{y}.png")
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        for k in range(6):
            try:
                d = urllib.request.urlopen(URL.format(z=z, x=x, y=y), timeout=60).read(); open(p + ".t", "wb").write(d); os.replace(p + ".t", p); break
            except Exception:
                if k == 5: raise
                time.sleep(1 + k)
    a = cv2.imread(p, cv2.IMREAD_COLOR)[..., ::-1].astype(np.float32)
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
def elev_now(V):
    lat, lon = grid_latlon(V)
    Zt = min(11, int(math.ceil(math.log2(V.k * 360 / 256))))           # tile px >= canvas px (canvas = 2x the 1080p frame at zoom 1.5)
    N = 256 * 2 ** Zt
    wx = ((lon + 180) / 360 * N); wy = ((1 - np.arcsinh(np.tan(np.radians(np.clip(lat, -85, 85)))) / np.pi) / 2 * N); del lat, lon
    tx0, tx1 = int(np.floor(wx.min() / 256)), int(np.floor(wx.max() / 256)); ty0, ty1 = max(0, int(wy.min() // 256)), min(2 ** Zt - 1, int(wy.max() // 256))
    jobs = [(tx, ty) for ty in range(ty0, ty1 + 1) for tx in range(tx0, tx1 + 1)]
    with ThreadPoolExecutor(8) as ex: tl = dict(zip(jobs, ex.map(lambda a: get_tile(Zt, *a), jobs)))
    mos = np.vstack([np.hstack([tl[(tx, ty)] for tx in range(tx0, tx1 + 1)]) for ty in range(ty0, ty1 + 1)]); del tl
    mos = cv2.medianBlur(mos.astype(np.float32), 3)                     # drops 1-px seams at some tile edges
    E = cv2.remap(mos, (wx - tx0 * 256 - .5).astype(np.float32), (wy - ty0 * 256 - .5).astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    print("  terrain tiles z%d: %d" % (Zt, len(jobs)), flush=True)
    return E.astype(np.float32)
def lakes_mask(V, name="ne_10m_lakes"):
    gj = json.load(open(os.path.join(CACHE, "ne", name + ".geojson"))); m = np.zeros((H, W), np.uint8)
    for ft in gj["features"]:
        g = ft["geometry"]
        if not g: continue
        for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]):
            for k, ring in enumerate(poly):
                a = np.array(ring); lon = a[:, 0] + 360 * np.round((V.lon0 - a[:, 0].mean()) / 360)
                for sh in (-360, 0, 360):                                 # no wrapping inside a ring: draw it and its +-360 copies
                    x, y = V.fwd(a[:, 1], lon + sh, wrap=False)
                    if x.max() < 0 or x.min() > W or y.max() < 0 or y.min() > H: continue
                    cv2.fillPoly(m, [np.round(np.c_[x, y] * 4).astype(np.int32)], 255 if k == 0 else 0, shift=2, lineType=cv2.LINE_AA)
    return m.astype(np.float32) / 255.0

# ------------------------------------------------------------------ look (bake_clean.compute_light / render_level at the kit's HD scale)
def blur_big(a, sigma, f=6):
    h, w = a.shape; s = a.reshape(h // f, f, w // f, f).mean((1, 3)); s = cv2.GaussianBlur(s, (0, 0), sigma / f)
    return cv2.resize(s, (w, h), interpolation=cv2.INTER_LINEAR)
def light_of(V, Hm, mpp, scalefree=False):
    """Hm = shading height (m, already exaggerated) >= 0"""
    sm = cv2.GaussianBlur(Hm, (0, 0), 1.0)
    gy, gx = np.gradient(sm); gx = gx / mpp; gy = gy / mpp
    sa = np.arctan(np.hypot(gx, gy)); cs, ss = np.cos(sa), np.sin(sa); asp = np.arctan2(-gx, gy); ca, sn = np.cos(asp), np.sin(asp); del gx, gy
    def shade(az, alt):
        az, alt = math.radians(az), math.radians(alt); return np.clip(math.sin(alt) * cs + math.cos(alt) * ss * (math.cos(az) * ca + math.sin(az) * sn), 0, 1)
    hs = 0.45 * shade(315, 38) + 0.25 * shade(260, 45) + 0.18 * shade(15, 50) + 0.12 * shade(135, 60)
    sl = np.clip(np.degrees(sa) / 25, 0, 1); del cs, ss, ca, sn, sa
    q = max(1.0, float(np.median(mpp)) / 150.0) if scalefree else 1.0                      # ao / fine terms are in metres per px: keep them scale-free on wide maps
    ao = np.clip((blur_big(Hm, 18) - Hm) / (40 * q), -1, 1); fine = np.clip((Hm - cv2.GaussianBlur(Hm, (0, 0), 2.5)) / (6 * q), -1, 1)
    return np.clip(0.42 + 0.72 * hs - 0.16 * sl - 0.18 * np.clip(ao, 0, 1) + 0.08 * np.clip(-ao, 0, 1) + 0.10 * fine, 0, 1.25).astype(np.float32)
def coverage(elev):
    """anti-aliased land coverage from the continuous elevation field (sharp, sub-pixel coastline)"""
    gy, gx = np.gradient(elev); g = np.hypot(gx, gy) + 1e-3
    return np.clip(0.5 + elev / g, 0, 1).astype(np.float32)
def render(V, E, L, exag, water=None, detail=None, paleo=False, ne_land=None):
    mpp = mpp_rows(V); elev = E - L
    cov = coverage(elev)
    if ne_land is not None:                                            # reclaimed land below 0 m (Fens, Dutch polders) stays land
        low = ne_land * np.clip((E + 12) / 4, 0, 1); cov = np.maximum(cov, low); elev = np.where(low > 0.5, np.maximum(elev, 1.0), elev)
    if water is not None: cov = cov * (1 - water); elev = np.where(water > 0.5, np.minimum(elev, -25), elev)
    land = cov > 0.5
    if paleo:
        Hm = np.maximum(elev, 0) * exag + detail * PALEO_DEXAG                 # big landforms exaggerated, fine relief near true scale
        Hm = np.maximum(Hm + 400, 0)
    else:
        El = np.where(E < -2, np.minimum(cv2.GaussianBlur(E, (0, 0), 8.0), -2), E)   # sea floor / exposed shelf: smoother surface (data seams)
        Hm = np.maximum(El - L, 0) * exag
    light = light_of(V, Hm.astype(np.float32), mpp, paleo); del Hm
    pos = elev[land]; hi = max(float(np.percentile(pos, 99.5)) if pos.size else 1.0, 1.0)
    t = np.clip(np.where(land, elev, 0) / hi, 0, 1)
    dark, lite = np.array([16, 22, 22], np.float32), np.array([138, 154, 140], np.float32)
    a = np.clip(light * 0.85 + t * 0.12, 0, 1) ** 1.15
    rgb = dark + (lite - dark) * a[..., None]; del a, t
    dd = (np.clip(-elev / 3500, 0, 1) ** 0.6)[..., None]
    sea = np.array([30, 52, 62], np.float32) * (1 - dd) + np.array([9, 16, 24], np.float32) * dd; del dd
    if paleo:                                                         # subtle shallow-shelf colour
        sh = (np.clip(1 + elev / 180.0, 0, 1) ** 1.5)[..., None] * 0.45
        sea = sea * (1 - sh) + np.array([44, 74, 82], np.float32) * sh
    halo = blur_big(cov, 8, 4)[..., None] * (1 - cov[..., None]); sea = sea + halo * np.array([14, 26, 28], np.float32)
    if L < -1:                                                       # newly exposed shelf: warm olive tint (as bake_clean)
        shelf = cv2.GaussianBlur((land & (E <= 0)).astype(np.float32), (0, 0), 1.5)[..., None] * 0.55
        rgb = rgb * (1 - shelf) + (rgb * 0.55 + np.array([70, 62, 40], np.float32) * 0.6) * shelf
    return sea * (1 - cov[..., None]) + rgb * cov[..., None], cov, light

def winter(rgb, coast, light):
    """cold grade: snow-dusted land, darker colder sea"""
    snow = np.array([150, 162, 172], np.float32) * np.clip(light * 0.95 + 0.1, 0, 1.15)[..., None]
    land = rgb * 0.45 + snow * 0.55
    sea = rgb * np.array([0.72, 0.80, 0.92], np.float32)
    c = coast[..., None]; return sea * (1 - c) + land * c

PEBAS = [(-77.2, 2.0), (-73.5, 3.2), (-69.5, 2.4), (-66.0, 0.6), (-63.2, -1.6), (-62.4, -4.6), (-64.0, -7.4), (-67.0, -9.4),
         (-70.5, -10.6), (-74.0, -9.6), (-76.4, -7.0), (-77.6, -3.0)]          # lon, lat: rough outline after Hoorn et al. 2010 (Science 330:927), approximate
def pebas_layer(V, E, rgb):
    """approximate Pebas mega-wetland (about 23-10 Ma): western Amazonian lowland, drawn as shallow brackish water over today's terrain"""
    a = np.array(PEBAS); x, y = V.fwd(a[:, 1], a[:, 0]); m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [np.round(np.c_[x, y] * 4).astype(np.int32)], 255, shift=2)
    d = cv2.distanceTransform(m, cv2.DIST_L2, 5) - cv2.distanceTransform(255 - m, cv2.DIST_L2, 5)   # signed px, + inside
    d = d + noise(21, (320, 140, 60)) * 90 + noise(22, (24, 12)) * 16
    edge = np.clip((d + 40) / 120, 0, 1)
    low = np.clip((240 - E) / 70, 0, 1)
    al = np.clip(edge * low, 0, 1); al = cv2.GaussianBlur(al, (0, 0), 1.5)
    wet = np.array([32, 62, 72], np.float32) + (rgb - 120) * 0.12
    return wet, al * 0.85

# ------------------------------------------------------------------ camera + video
def ease(u): u = min(max(u, 0.0), 1.0); return u * (1.6 - 0.6 * u)
class Cam:
    def __init__(s, V, sp, n):
        s.n = n; s.z0, s.z1 = sp["z"]; c0 = np.array([W / 2, H / 2])
        if sp.get("pin"):
            px, py = V.fwd(*sp["pin"]); s.c1 = c0 + sp.get("focus", 0.7) * (np.array([px, py]) - c0)
        else: s.c1 = c0 + np.array(sp.get("drift", (0, 0)), float)
        s.c0 = c0 if sp.get("pin") else c0 - np.array(sp.get("drift", (0, 0)), float) * 0
    def at(s, i):
        u = ease(i / max(s.n - 1, 1)); z = s.z0 + (s.z1 - s.z0) * u; c = s.c0 + (s.c1 - s.c0) * u
        hw, hh = W / (2 * z), H / (2 * z); cx = min(max(c[0], hw), W - hw); cy = min(max(c[1], hh), H - hh)
        sc = OW / W * z; return np.array([[sc, 0, OW / 2 - cx * sc], [0, sc, OH / 2 - cy * sc]], np.float64)
def to1280(M, x, y): return round(float(x * M[0, 0] + M[0, 2]) / 1.5, 1), round(float(y * M[1, 1] + M[1, 2]) / 1.5, 1)

MAX_MB = 4.8
def deliver(master, mp4, dur):
    """git copy: crf 18 if it fits under MAX_MB, else 2-pass x264 at the bitrate that fits (masters stay in the cache)"""
    enc = ["-an", "-c:v", "libx264", "-preset", "slower", "-pix_fmt", "yuv420p", "-threads", "3", "-tune", "film"]
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", master] + enc + ["-crf", "18", "-movflags", "+faststart", mp4], check=True)
    if os.path.getsize(mp4) / 1e6 <= MAX_MB: return
    br = int(MAX_MB * 0.96 * 8e6 / dur); log = os.path.join(CACHE, "masters", "x264pass")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", master] + enc + ["-b:v", str(br), "-pass", "1", "-passlogfile", log, "-f", "mp4", os.devnull], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", master] + enc + ["-b:v", str(br), "-maxrate", str(int(br * 1.3)), "-bufsize", str(br), "-pass", "2", "-passlogfile", log, "-movflags", "+faststart", mp4], check=True)

def bake(sid, still=False):
    sp = SHOTS[sid]; t0 = time.time()
    V = Merc(sp["c"][0], sp["c"][1], sp["span"]); L = sp.get("sea", 0)
    paleo = sp["src"] != "now"
    ne_land = None
    if not paleo:
        E = elev_now(V); water = lakes_mask(V); detail = None
        if L == 0: ne_land = lakes_mask(V, "ne_10m_land")
    else: E, detail = elev_paleo(V, sp["src"]); water = None
    rgb, coast, light = render(V, E, L, sp.get("exag", PALEO_EXAG if paleo else 3.0), water, detail, paleo, ne_land)
    over = None
    if sp.get("winter"): rgb = winter(rgb, coast, light)
    if sp.get("pebas"): over = pebas_layer(V, E, rgb)
    del E, detail, light, coast
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    if over is not None: over = (np.clip(over[0], 0, 255).astype(np.uint8), (over[1] * 255).astype(np.uint8))
    dur = round(sp["est"] + 1.5, 2); n = int(round(dur * FPS)); cam = Cam(V, sp, n)
    os.makedirs(OUT, exist_ok=True)
    def frame(i):
        M = cam.at(i) * SS
        f = cv2.warpAffine(rgb, M, (OW * SS, OH * SS), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        if over is not None:
            k = min(1.0, max(0.0, (i / FPS - 0.15) / 1.4))
            wv = cv2.warpAffine(over[0], M, (OW * SS, OH * SS), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
            al = cv2.warpAffine(over[1], M, (OW * SS, OH * SS), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)[..., None] / 255 * k
            f = (f * (1 - al) + wv * al)
        f = cv2.resize(f.astype(np.float32), (OW, OH), interpolation=cv2.INTER_AREA)
        f = f + UNSHARP * (f - cv2.GaussianBlur(f, (0, 0), 1.2))          # light unsharp mask
        return np.clip(f, 0, 255)
    if still:
        for i in (0, n // 2, n - 1): cv2.imwrite(os.path.join(OUT, f"_{sid}_{i:03d}.jpg"), np.clip(frame(i), 0, 255).astype(np.uint8)[..., ::-1])
        return
    mp4 = os.path.join(OUT, f"{sid}.mp4"); master = os.path.join(CACHE, "masters", f"{sid}.mp4"); os.makedirs(os.path.dirname(master), exist_ok=True)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
                           "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p", "-threads", "3", master], stdin=subprocess.PIPE)
    for i in range(n): ff.stdin.write(np.clip(frame(i), 0, 255).astype(np.uint8).tobytes())
    ff.stdin.close(); ff.wait()
    deliver(master, mp4, dur)
    Mend = cam.at(n - 1)
    j = dict(id=sid, duration=dur, frames=n, fps=FPS, size=[OW, OH], place=sp["place"],
             note="Clean bake: terrain, coastline, relief, camera only. No labels, pin or date are drawn; the map_clip template draws them. Pin coordinates are in the 1280x720 design space.",
             projection=dict(kind="mercator", center_lat=sp["c"][0], center_lon=sp["c"][1], lon_span_canvas=sp["span"], canvas=[W, H], zoom=list(sp["z"])))
    if sp["src"] == "now":
        j["geography"] = "present-day terrain and coastline (AWS Terrarium tiles)" + (f", sea level {L} m" if L else ", today's sea level") + "; lakes from Natural Earth"
    else:
        j["geography"] = f"PALEOMAP PaleoDEM {sp['src']} Ma (Scotese & Wright 2018), map in paleo-coordinates"
        j["paleo_pin"] = dict(lat=sp["pin"][0], lon=sp["pin"][1], from_modern=dict(lat=sp["modern"][0], lon=sp["modern"][1]),
                              how="GPlates Web Service reconstruct_points, model=PALEOMAP, time=%d" % sp["src"])
    if sp.get("pin"):
        track = []
        for i in list(range(0, n, 6)) + [n - 1]:
            x, y = to1280(cam.at(i), *V.fwd(*sp["pin"])); track.append([round(i / FPS, 2), x, y])
        x, y = to1280(Mend, *V.fwd(*sp["pin"]))
        j["pin"] = dict(lat=sp["pin"][0], lon=sp["pin"][1], x=x, y=y, x1920=round(x * 1.5), y1920=round(y * 1.5), template_param={"x": round(x), "y": round(y)},
                        static=False, note="the camera pushes in for the whole clip; {x,y} is the position at the last frame (track = [t, x, y] every 0.2 s)", track=track)
    for k, ll in (sp.get("extra") or {}).items():
        x, y = to1280(Mend, *V.fwd(*ll)); j.setdefault("extra_points", {})[k] = dict(lat=ll[0], lon=ll[1], x=x, y=y)
    if sid == "R04":
        M0 = cam.at(0); pins = []
        for name, la, lo in R04_PINS:
            x0, y0 = to1280(M0, *V.fwd(la, lo)); x1, y1 = to1280(Mend, *V.fwd(la, lo)); pins.append(dict(name=name, lat=la, lon=lo, x=x1, y=y1, x_start=x0, y_start=y0))
        j["pins"] = pins; j["pins_note"] = "present-day positions of the 12 rivers; the map drifts slowly, x/y = last frame, x_start/y_start = first frame"
    json.dump(j, open(os.path.join(OUT, f"{sid}.json"), "w"), indent=1)
    print(sid, f"{dur}s", j.get("pin", {}).get("template_param"), f"{os.path.getsize(mp4) / 1e6:.2f} MB", f"{time.time() - t0:.0f}s", flush=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--deliver" in a:                                               # re-encode git copies from the masters only
        for sid in [x for x in a if not x.startswith("--")] or list(SHOTS):
            deliver(os.path.join(CACHE, "masters", f"{sid}.mp4"), os.path.join(OUT, f"{sid}.mp4"), round(SHOTS[sid]["est"] + 1.5, 2)); print(sid, round(os.path.getsize(os.path.join(OUT, f"{sid}.mp4")) / 1e6, 2), "MB", flush=True)
        sys.exit()
    still = "--still" in a; ids = [x for x in a if not x.startswith("--")] or list(SHOTS)
    for sid in ids: bake(sid, still)
