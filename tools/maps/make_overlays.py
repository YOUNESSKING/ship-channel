#!/usr/bin/env python3
"""make_overlays.py ID [--tint R,G,B] [--lake LAT LON LEVEL_M] [--box S,W,N,E]   (NEW)
From assets/src/ID_now_hd_elev.npy (today's DEM) and ID_lgm_hd_elev.npy (shifted by the LGM sea level) writes, in assets/media/:
  ID_coast.png  thin ghost of TODAY's coastline      ID_shelf.png  newly exposed land (tinted, steppe texture, bright new-coast rim)
  ID_seadark.png  cold navy grade on the LGM sea (fade it in with the sea-level drop)
  ID_lake.png  (optional) fresh-water lake: sea/low pixels connected to the seed whose DEM is below LEVEL (default: the LGM sea itself)"""
import sys, os, json, math
import numpy as np
from PIL import Image
from scipy import ndimage
ID = sys.argv[1]; a = sys.argv[2:]
def opt(f, n=1):
    if f in a:
        i = a.index(f); v = a[i+1:i+1+n]; del a[i:i+1+n]; return v
tint = [float(v) for v in (opt("--tint") or ["214,164,92"])[0].split(",")]
lake = opt("--lake", 3); box = opt("--box"); ell = opt("--ell", 4)
J = json.load(open(f"assets/{ID}_lgm.json")); S = J["sea_level"]; Z = J["zoom"]; ox, oy = J["origin_world_px"]; N = 256*2**Z
ds = lambda e: e.reshape(1620, 2, 2880, 2).mean((1, 3)).astype(np.float32)
raw = ds(np.load(f"assets/src/{ID}_now_hd_elev.npy")); lg = ds(np.load(f"assets/src/{ID}_lgm_hd_elev.npy"))   # lg = raw - S
H, W = raw.shape
rows = oy + np.arange(H) + .5; lat = np.degrees(np.arctan(np.sinh(math.pi*(1-2*rows/N))))[:, None]*np.ones((1, W))
def noise(seed, scales):
    r = np.random.default_rng(seed); o = np.zeros((H, W), np.float32)
    for i, s in enumerate(scales):
        n = r.normal(0, 1, (H//s+3, W//s+3)).astype(np.float32); o += ndimage.zoom(n, s, order=3)[:H, :W]/(1.7**i)
    return o/o.std()
nz = noise(3, (160, 60, 24, 10))
land_now = raw > 0.5; land_lgm = lg > 0.5
out = "assets/media"; os.makedirs(out, exist_ok=True)
def save(rgb, al, n): Image.fromarray(np.dstack([np.broadcast_to(np.array(rgb, np.float32), (H, W, 3)) if np.ndim(rgb) == 1 else rgb, np.clip(al, 0, 1)*255]).clip(0, 255).astype(np.uint8), "RGBA").save(f"{out}/{ID}_{n}.png")
# today's coast ghost (thin line)
edge = land_now & ~ndimage.binary_erosion(land_now, iterations=2)
save([240, 232, 210], ndimage.gaussian_filter(edge.astype(np.float32), 0.9)*0.95, "coast")
# newly exposed land
ex = land_lgm & ~land_now
exs = ndimage.gaussian_filter(ex.astype(np.float32), 1.6)
rim = land_lgm & ~ndimage.binary_erosion(land_lgm, iterations=2) & ~land_now
rim = ndimage.gaussian_filter(rim.astype(np.float32), 1.0)
t = np.array(tint, np.float32); rgbs = t[None, None, :]*(0.9+0.12*np.tanh(nz))[..., None]
al = exs*(0.36+0.08*np.tanh(nz)); al = np.maximum(al, np.clip(rim*0.9, 0, 0.9))
rgbs = np.where(rim[..., None] > 0.3, np.array([252, 238, 205], np.float32), rgbs)
save(rgbs, al, "shelf")
# cold navy over the LGM sea
sea = 1 - ndimage.gaussian_filter(land_lgm.astype(np.float32), 1.0)
latb = np.clip((lat-25)/45, 0, 1)
save([4, 10, 24], np.clip(0.26*(0.85+0.45*latb), 0, 0.4)*sea, "seadark")
if lake:
    la, lo, lev = float(lake[0]), float(lake[1]), float(lake[2])
    px_ = ((lo+180)/360*N - ox); py_ = ((1-math.asinh(math.tan(math.radians(la)))/math.pi)/2*N - oy)
    cand = (raw < lev) if lev != 999 else (lg <= 0.5)
    if box:
        s, w, n, e = [float(v) for v in box[0].split(",")]
        lon = ((ox + np.arange(W) + .5)/N*360 - 180)[None, :]*np.ones((H, 1)); cand &= (lat > s) & (lat < n) & (lon > w) & (lon < e)
    if ell:
        cl, co, al_, ao = [float(v) for v in ell]
        lon_ = ((ox + np.arange(W) + .5)/N*360 - 180)[None, :]*np.ones((H, 1)); cand &= (((lat-cl)/al_)**2 + ((lon_-co)/ao)**2) < 1   # soft natural closure where the sill was
    lab, _ = ndimage.label(cand); k = lab[int(py_), int(px_)]; assert k > 0, "lake seed not inside a candidate pixel"
    m = ndimage.binary_closing(lab == k, iterations=2); ms = ndimage.gaussian_filter(m.astype(np.float32), 1.3)
    rimm = m & ~ndimage.binary_erosion(m, iterations=3); rimm = ndimage.gaussian_filter(rimm.astype(np.float32), 1.0)
    shade_ = 0.9 + 0.1*np.tanh(nz)
    rgbl = np.array([84, 128, 142], np.float32)[None, None, :]*shade_[..., None]
    rgbl = np.where(rimm[..., None] > 0.25, np.array([196, 232, 240], np.float32), rgbl)
    save(rgbl, np.maximum(ms*0.82, rimm*0.9)*ms.clip(0, 1) if False else np.maximum(ms*0.62, rimm*0.8), "lake")
print("overlays", ID)
