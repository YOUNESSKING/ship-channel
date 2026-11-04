#!/usr/bin/env python3
"""make_ice_progress.py BASE  -> assets/media/icep_01..10.png : glaciation progress p=0.1..1.0 as per-pixel overlays (p=0 = nothing).
Each pixel has an 'arrival time' T: early near the ice-sheet interiors (distance inside the LGM outline), at high elevation and high
latitude, plus fractal noise; ice_amount(p) = smoothstep((p - T)/width). Outlines from POLYS in make_ice.py (approximate).
Colour = cold white / ice-blue modulated by the relief hillshade (blue-grey in shadow), so the terrain stays visible through the ice.
Sea ice = soft noisy frost north of a rough winter edge. Needs assets/src/BASE_hd_elev.npy (written by bake_hd.py, sea-level shifted)."""
import sys, os, json, math
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt, gaussian_filter, zoom as ndzoom
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base = sys.argv[1]; PREFIX = sys.argv[2] if len(sys.argv) > 2 else None   # PREFIX: outputs PREFIX_icep_NN.png (per-map ice frames)
g = {"__file__": os.path.join(ROOT, "tools/make_ice.py")}; sys.argv = ["x", base]
exec(compile(open(os.path.join(ROOT, "tools/make_ice.py")).read().split("tex = fbm")[0], "make_ice", "exec"), g)
P, W, H, Z, ox, oy, N, px, POLYS, SEA_ICE, chaikin, wobble, fbm = (g[k] for k in "P W H Z ox oy N px POLYS SEA_ICE chaikin wobble fbm".split())
elev = np.load(os.path.join(ROOT, f"assets/src/{base.replace("_hd_ref","")}_hd_elev.npy"))
elev = elev.reshape(H, 2, W, 2).mean((1, 3)).astype(np.float32)        # 5760x3240 -> 2880x1620
land = elev > 0.5
rows = oy + np.arange(H) + 0.5
lat = np.degrees(np.arctan(np.sinh(math.pi*(1-2*rows/N))))[:, None] * np.ones((1, W))
lon = ((ox + np.arange(W) + 0.5)/N*360 - 180)[None, :] * np.ones((H, 1))
# hillshade for the ice colouring (sun NW), land only; sea/shelf-ice is flat
mpp = (156543.03*np.cos(np.radians(lat))/2**Z).astype(np.float32)
zs = gaussian_filter(np.where(land, elev, 0)*4.0, 1.5)
gy, gx = np.gradient(zs); gx /= mpp; gy /= mpp
nl = np.sqrt(gx**2+gy**2+1); az, alt = math.radians(315), math.radians(40)
shade = np.clip(((-gx)*math.sin(az)*math.cos(alt) + (gy)*math.cos(az)*math.cos(alt)*(-1) + math.sin(alt))/nl, 0, 1)
shade = np.clip((shade - 0.45)*1.9 + 0.55, 0.15, 1.0)
rng = np.random.default_rng(5)
rel = np.asarray(Image.open(os.path.join(ROOT, f"assets/{base}.jpg")).convert("L").resize((W, H), Image.LANCZOS), np.float32)/255
rel = np.clip((rel - gaussian_filter(rel, 25))*3.2 + 0.5, 0.0, 1.0)     # local relief contrast: ridges lit, valleys dark
def noise(seed, scales, h=H, w=W):
    r = np.random.default_rng(seed); o = np.zeros((h, w), np.float32)
    for i, s in enumerate(scales):
        n = r.normal(0, 1, (h//s+3, w//s+3)).astype(np.float32); o += ndzoom(n, s, order=3)[:h, :w]/(1.7**i)
    return o/o.std()
nA = noise(1, (400, 160, 70, 30)); nB = noise(2, (60, 24, 10)); nE = noise(3, (200, 90, 40, 18))
# ---- arrival time T over all sheets
T = np.full((H, W), 9.0, np.float32); M = np.zeros((H, W), np.float32)
for k, poly in POLYS.items():
    pts = wobble(chaikin([px(*p) for p in poly], 4), 6, 7)
    m = Image.new("L", (W*2, H*2), 0); ImageDraw.Draw(m).polygon([(x*2, y*2) for x, y in pts], fill=255)
    m = np.asarray(m.resize((W, H), Image.BILINEAR), np.float32)/255
    d = distance_transform_edt(m > 0.5)
    dn = np.clip(d/ (0.55*d.max() + 1e-6), 0, 1)                       # 0 at the margin, 1 deep inside
    if k == "iceland": dn = np.clip(d/(d.max()+1e-6), 0, 1)
    Ts = 0.74 - 0.6*dn                                                   # interiors freeze first
    T = np.minimum(T, np.where(m > 0.5, Ts, 9.0)); M = np.maximum(M, m)
dfield = distance_transform_edt(M > 0.5)
M = np.clip((dfield + nE*14 - 3)/22, 0, 1); M = M*M*(3-2*M)              # ragged fractal margin
hi = np.clip((elev-250)/1700, 0, 1); hi = hi*hi*(3-2*hi)
latb = np.clip((lat-48)/24, 0, 1)
T = T - 0.42*hi*land - 0.16*latb + 0.12*nA
T = np.clip(T, 0.04, 0.80)
# mountain snow outside the big sheets (Alps, Pyrenees, Scottish/Norwegian highlands...)
alp = np.clip((elev-900)/1500, 0, 1)*land*(1-M)*np.clip((lat-38)/10, 0, 1)
Talp = 0.45 - 0.2*np.clip((elev-900)/2000, 0, 1) + 0.1*nA
# ---------------- SEA ICE: crisp floes (Voronoi cells, shrunk by a lead width) -----------------
from scipy.spatial import cKDTree
sea = ~land
dland = distance_transform_edt(~land).astype(np.float32)
fl = np.array([q[1] for q in ([(52,-75),(49.5,-58),(47,-47)] + SEA_ICE)]); fa = np.array([q[0] for q in ([(52,-75),(49.5,-58),(47,-47)] + SEA_ICE)])
edge = np.interp(lon, fl, fa, left=53.0, right=72.0); dd = lat - edge
shelf_zone = (M > 0.35) & sea & (elev > -450)           # sea inside the LGM outlines (shelf ice / pack)
warp1 = noise(11, (40, 18)); warp2 = noise(12, (40, 18))
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def voronoi(spacing, seed, warp):
    r = np.random.default_rng(seed)
    gxs = np.arange(-2*spacing, W+2*spacing, spacing); gys = np.arange(-2*spacing, H+2*spacing, spacing)
    GX, GY = np.meshgrid(gxs, gys)
    pts = np.c_[(GX + r.uniform(-.48, .48, GX.shape)*spacing).ravel(), (GY + r.uniform(-.48, .48, GX.shape)*spacing).ravel()]
    tree = cKDTree(pts); hv = r.uniform(0, 1, len(pts)); hv2 = r.uniform(0, 1, len(pts))
    q = np.c_[(xx + warp*warp1).ravel(), (yy + warp*warp2).ravel()]
    d, i = tree.query(q, k=2, workers=-1)
    b = ((d[:, 1] - d[:, 0])/2).reshape(H, W).astype(np.float32); i0 = i[:, 0].reshape(H, W)
    sx = np.clip(pts[:, 0], 0, W-1).astype(int); sy = np.clip(pts[:, 1], 0, H-1).astype(int)
    return b, i0, hv, hv2, sx, sy
def build(spacing, seed, warp, shelf):
    b, i0, hv, hv2, sx, sy = voronoi(spacing, seed, warp)
    if shelf:   # arrival of the neighbouring land ice, slightly later
        Tf = T[sy, sx] + 0.04 + 0.18*hv
    else:       # coastal pack: early near land, earlier far north, never in the open south / central Atlantic
        dl = dland[sy, sx]; la = lat[sy, sx]; dg = dd[sy, sx]
        Tf = 0.10 + 0.9*np.clip(dl/185, 0, 1)**0.8 - 0.30*np.clip((la-58)/10, 0, 1) + 0.10*nA[sy, sx] + 0.28*hv \
             + 1.3*np.clip((3-dg)/4, 0, 1)
    return dict(b=b, Tf=Tf[i0], h2=hv2[i0], h=hv[i0])
# (sea-ice floes removed on request: the ocean darkens instead)
def floes(p):
    """RGBA (premultiplied-free) of sea ice at progress p"""
    out_rgb = np.zeros((H, W, 3), np.float32); out_a = np.zeros((H, W), np.float32)
    for S, shelf in ((ice_s, False), (ice_b, True)):
        zone = shelf_zone if shelf else (sea & ~shelf_zone)
        c = np.clip((p - S["Tf"])/0.4, 0, 1)
        gap = (1.0 + 5.5*(1-c)) if shelf else (1.4 + 7.0*(1-c))
        b = S["b"]; m = np.clip((b - gap)/1.1, 0, 1) * (p > S["Tf"]) * zone
        rimk = np.clip((gap + 3.2 - b)/3.2, 0, 1)                           # darker, bluer fracture rim
        base = np.array([241, 249, 255])*(0.86 + 0.14*S["h2"])[..., None]
        rgb = base*(1-0.2*rimk[..., None]) + np.array([150, 190, 222])*0.2*rimk[..., None]
        rgb = rgb*(1 + 0.035*nB[..., None])
        a = m*(0.93 if not shelf else 0.88)
        take = a > out_a
        out_rgb = np.where(take[..., None], rgb, out_rgb); out_a = np.where(take, a, out_a)
    return out_rgb, out_a
def frames(p):
    a = np.clip((p - T + 0.07*nB)/0.22, 0, 1); a = a*a*(3-2*a)
    a = a*M
    aa = np.clip((p - Talp + 0.06*nB)/0.2, 0, 1)**2*alp
    land_a = np.clip(np.maximum(a, aa), 0, 1)*land
    lit = shade[..., None]
    rgb_l = np.array([105, 138, 182])*(1-lit) + np.array([244, 249, 255])*lit
    rgb_l = rgb_l*(0.62 + 0.55*rel[..., None])*(1 + 0.03*nB[..., None])
    rim = np.clip(land_a*(1-land_a)*4, 0, 1)[..., None]
    rgb_l = rgb_l + rim*30
    al = land_a*(0.66 + 0.16*(shade-0.5))
    # no ice on water: the ocean slowly goes a colder, deeper navy as the Ice Age sets in (darkest in the north)
    seamask = 1 - gaussian_filter(land.astype(np.float32), 1.0)
    dark = 0.30*(p**0.9)*(0.8 + 0.55*latb)
    sa = np.clip(dark, 0, 0.42)*seamask
    sr = np.broadcast_to(np.array([4, 10, 24], np.float32), (H, W, 3))
    rgb = np.where(land[..., None], rgb_l, sr); al_tot = np.where(land, al, sa)
    out = np.dstack([np.clip(rgb, 0, 255), np.clip(al_tot, 0, 0.95)*255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")
os.makedirs(os.path.join(ROOT, "assets/media"), exist_ok=True)
for i in range(1, 11):
    frames(i/10).save(os.path.join(ROOT, f"assets/media/{PREFIX + '_' if PREFIX else ''}icep_{i:02d}.png"), optimize=False, compress_level=3); print(i, flush=True)
