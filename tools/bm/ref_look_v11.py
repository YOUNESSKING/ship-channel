"""TREE REDESIGN TEST v11 (owner 2026-10-31, research/TREE_REDESIGN_BRIEF.md; TEST ONLY, NOT applied to any video):
v10c (angle C: generated crown outlines filled with REAL forest canopy photos, public-domain USGS, sprites_C2.npz) plus the
fixes of build/judge-trees-v10.md + check-trees-v10.md. v9 ground, river and creeks unchanged.
Below: the v9 notes (tree paragraph superseded by the TREES v10 block).
usage (from cleburne/): python3 tools/ref_look_v11.py BASE CX CY OUT.jpg  (sprites: python3 tools/make_tree_sprites.py)
v9: the reference film's smooth,
painterly map (warm sand relief, soft shadow sides, natural pale river, hairline creeks, 3D tree canopies in ribbons along the water).
Copy of make_ref_look_test.py, rewritten. Not a recolour: every layer is rendered by a different method.
usage (from cleburne/): python3 tools/judge_ref2.py BASE CX CY OUT.jpg [VARIANT]   (CX,CY = crop centre in the 5760x3240 HD grid)
  VARIANT: A = riparian ribbons + sparse groves, B = denser groves, C = A without DEM gullies
  env OVERLAY=out.jpg : also write an overlay-compatibility test (territory multiply + 54 px counters + 15 px glowing front)
Method (per layer):
  terrain  : 3-scale smoothed DEM (sigma 2 / 5 / 14 px) -> illumination RELATIVE TO FLAT (flats = one calm sand tone), soft tanh
             compression, gradient-mapped (shadow brown -> sand -> sunlit orange -> pale highlight), slope-warmed base, ridge lift +
             valley ambient occlusion from a difference of Gaussians, 2-octave paper grain (+-3 %).
  water    : data mask (rivS + wide parts of det_riv) blurred and re-thresholded (smooth banks), colour by distance from the bank
             (darker grey-green edge -> pale grey-blue centre), soft pale sand bank strip, faint low-frequency water texture.
  creeks   : mapped creeks (det_riv minus wide water) as soft dark hairlines + DEM-flow gullies (D8 accumulation on the
             smoothed DEM, numba) traced as Chaikin-smoothed polylines, width ~ log(area), drawn 4x supersampled.
  trees    : crowns placed only where det_tree says forest: dense ribbons within ~34 px of the river, single/double rows on
             creeks, clustered groves elsewhere (smooth noise field, thinner where forest cover thins). Each crown = a bumpy
             dome (main hemisphere + 4-7 sub-lobes) stamped into a CANOPY HEIGHT FIELD at 2x; the field is hill-shaded (NW sun),
             height-darkened at crown gaps (AO), tinted per crown, cast-shadowed to the SE onto ground/water, area-downsampled.
  grade    : warm sand balance, gentle S-curve, soft vignette, fine grain."""
import sys, os, time, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
import numba

t0 = time.time()
base, cx, cy, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
VAR = sys.argv[5] if len(sys.argv) > 5 else "A"
W, H, PAD = (5760, 3240, 0) if os.environ.get('FULL') == '1' else (1920, 1080, 48)   # FULL=1: whole basemap for a scene (no vignette)
x0, y0 = max(0, min(5760 - W, cx - W // 2)), max(0, min(3240 - H, cy - H // 2))
# padded window (filters need context; the full-map bake has no crop at all)
px0, py0 = max(0, x0 - PAD), max(0, y0 - PAD)
px1, py1 = min(5760, x0 + W + PAD), min(3240, y0 + H + PAD)
ox, oy = x0 - px0, y0 - py0
PW, PH = px1 - px0, py1 - py0
box = (px0, py0, px1, py1)
rng = np.random.default_rng(7)
G = ndimage.gaussian_filter
MPP = 7.82                                         # metres per HD px

def ss(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)

el = np.load(f"assets/src/{base}_hd_elev.npy")[py0:py1, px0:px1].astype(np.float32)
_rA = np.array(Image.open(f"assets/media/{base}_det_riv.png").convert("RGBA").crop(box))[..., 3] > 40
_rS = np.array(Image.open(f"assets/media/{base}_det_rivS.png").convert("RGBA").crop(box))[..., 3] > 40
_burn = ndimage.binary_dilation(_rA & ~ndimage.binary_dilation(_rS, iterations=4), iterations=5)
el = np.where(_burn, G(ndimage.grey_closing(el, size=11), 1.5), el)   # v7: no straight ghost trench under the creek hairline

# ---------------- TERRAIN ----------------
L_AZ, L_ALT = np.radians(315), np.radians(42)
Lv = np.array([np.cos(L_ALT) * np.sin(L_AZ), -np.cos(L_ALT) * np.cos(L_AZ), np.sin(L_ALT)])  # x right, y down, z up
def illum(e, zx):
    gy, gx = np.gradient(e * zx / MPP)
    n = 1 / np.sqrt(gx * gx + gy * gy + 1)
    return (-gx * Lv[0] - gy * Lv[1] + Lv[2]) * n - Lv[2]           # 0 on flat ground, + lit, - shadow
e_f, e_m, e_b = G(el, 2.0), G(el, 5.0), G(el, 14.0)
I = 0.50 * illum(e_m, 2.6) + 0.32 * illum(e_b, 3.4) + 0.18 * illum(e_f, 2.0)
I = np.tanh(I * 1.5) * 0.62                                               # soft compression: no plastic hot spots
I = G(I, 1.0)
gy, gx = np.gradient(e_m / MPP)
slope = ss(0.02, 0.35, np.hypot(gx, gy))
curv = G(el, 3) - G(el, 16)                                         # metres; + ridge, - valley
ridge = ss(0, 10, curv); valley = ss(0, 12, -curv)
SAND = np.array([190, 178, 134.]); EARTH = np.array([178, 156, 108.])
SHADOW = np.array([112, 96, 66.]); LIT = np.array([208, 188, 132.]); HI = np.array([226, 212, 166.])
basec = SAND * (1 - 0.7 * slope[..., None]) + EARTH * (0.7 * slope[..., None])
lit = np.clip(I, 0, 1)[..., None]; sh = np.clip(-I, 0, 1)[..., None]
col = basec + (LIT - basec) * np.clip(lit * 1.25, 0, 1) + (HI - LIT) * np.clip(lit * 1.25 - 1, 0, 1) * 0 \
      + (HI - basec) * ss(0.55, 1.0, lit) * 0.35
col = col * (1 - sh * 0.95) + SHADOW * (sh * 0.95)
col *= (1 + 0.07 * ridge - 0.16 * valley)[..., None]                # ridge emphasis + ambient occlusion
nz = rng.standard_normal((PH, PW)).astype(np.float32)
grain = 0.55 * G(nz, 1.0) / 0.28 + 0.45 * G(nz, 3.5) / 0.08
paper = G(nz, 0.6) / 0.35
col *= (1 + 0.016 * grain + 0.022 * paper)[..., None]

# swamps: damp olive ground
swa = np.array(Image.open(f"assets/media/{base}_det_swamp.png").convert("RGBA").crop(box))[..., 3].astype(np.float32) / 255
swa = G(swa, 2.5)
col = col * (1 - 0.45 * swa[..., None]) + np.array([118, 128, 88.]) * (0.45 * swa[..., None])

if os.environ.get("NEUTRAL") == "1":                                 # territory-friendly: pull the sand toward its luminance
    lum = col @ np.array([0.3, 0.59, 0.11]); col = col * 0.55 + lum[..., None] * 0.45 * np.array([1.02, 1.0, 0.94])
# ---------------- WATER ----------------
rivS = np.array(Image.open(f"assets/media/{base}_det_rivS.png").convert("RGBA").crop(box))[..., 3] > 40
rivA = np.array(Image.open(f"assets/media/{base}_det_riv.png").convert("RGBA").crop(box))[..., 3] > 40
wide = ndimage.binary_opening(rivA, iterations=3)
water0 = rivS | wide
water0 = water0 | (ndimage.binary_dilation(rivS, iterations=1) & (G(rivS.astype(np.float32), 3) < 0.35))
wsm = G(water0.astype(np.float32), 2.2)
wa = ss(0.38, 0.62, wsm)                                            # smooth antialiased banks
water = wa > 0.5
_lab, _n = ndimage.label(water); _sz = ndimage.sum(water, _lab, range(1, _n + 1))
water = np.isin(_lab, 1 + np.nonzero(_sz >= 400)[0]); wa = wa * G(water.astype(np.float32), 1.0) / np.maximum(G(water.astype(np.float32), 1.0), 1e-3) * water + wa * 0 * (~water)
din = ndimage.distance_transform_edt(water)
dout, (niy, nix) = ndimage.distance_transform_edt(~water, return_indices=True)
wmax = ndimage.maximum_filter(din, 81) + 1
rel = np.clip(din / np.maximum(wmax, 4), 0, 1)                       # 0 bank -> 1 centre
WEDGE, WMID, WCEN = np.array([118, 122, 114.]), np.array([142, 148, 144.]), np.array([160, 166, 162.])
wcol = WEDGE + (WMID - WEDGE) * ss(0, 0.35, rel)[..., None] + (WCEN - WMID) * ss(0.3, 1, rel)[..., None]
wtex = G(rng.standard_normal((PH, PW)).astype(np.float32), [2.0, 7.0]) / 0.1
spk = G(rng.standard_normal((PH, PW)).astype(np.float32), 0.6); spk /= spk.std()
wcol *= (1 + 0.012 * wtex + 0.055 * spk)[..., None]                 # stony speckle like the reference
bn = G(rng.standard_normal((PH, PW)).astype(np.float32), 6); bn /= bn.std()
_bigw = ndimage.binary_opening(water, iterations=3)
_dbig = ndimage.distance_transform_edt(~_bigw)
dirt = (1 - ss(2.0, np.maximum(5.5 + 1.5 * bn, 3.2), _dbig)) * (~water) * (_dbig < 9)
col = col * (1 - 0.75 * dirt[..., None]) + np.array([150, 132, 98.]) * (0.75 * dirt[..., None])
grass = ss(1.5, 4.0, _dbig) * (1 - ss(12 + 5 * bn, 20 + 5 * bn, _dbig)) * (~water) * (_dbig < 30)
col = col * (1 - 0.55 * grass[..., None]) + np.array([128, 138, 88.]) * (0.55 * grass[..., None])
rim = np.exp(-((din - 1.0) ** 2) / 1.5) * water

col = col * (1 - wa[..., None]) + wcol * wa[..., None]
col = col * (1 - 0.45 * rim[..., None]) + np.array([92, 86, 70.]) * (0.45 * rim[..., None])

# riparian meadow: a light green fringe on the floodplain next to the big water
mead = np.zeros((PH, PW), np.float32)
col = col * (1 - mead[..., None]) + np.array([150, 156, 100.]) * mead[..., None]

# ---------------- CREEKS (mapped + DEM flow) ----------------
SSx = 4
cre = rivA & ~ndimage.binary_dilation(water, iterations=2)
from skimage.morphology import skeletonize
_sk = skeletonize(cre).astype(np.float32)                           # thin hairline like the reference creeks
_wy = G(rng.standard_normal((PH, PW)).astype(np.float32), 3.0); _wx = G(rng.standard_normal((PH, PW)).astype(np.float32), 3.0)
_wy *= 2.2 / _wy.std(); _wx *= 2.2 / _wx.std()                       # wiggle: no ruler-straight creeks
_yy, _xx = np.mgrid[0:PH, 0:PW].astype(np.float32)
_sk = ndimage.map_coordinates(G(_sk, 0.6), [_yy + _wy, _xx + _wx], order=1)
cre_a = np.clip(_sk * 3.2, 0, 1) * 0.75

@numba.njit(cache=True)
def d8(e):
    h, w = e.shape; rec = -np.ones(h * w, np.int64)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            best = 0.0; bi = -1; z = e[y, x]
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0: continue
                    d = (z - e[y + dy, x + dx]) / (1.4142 if dx != 0 and dy != 0 else 1.0)
                    if d > best: best = d; bi = (y + dy) * w + x + dx
            rec[y * w + x] = bi
    order = np.argsort(-e.ravel())
    acc = np.ones(h * w)
    for i in order:
        r = rec[i]
        if r >= 0: acc[r] += acc[i]
    return rec, acc

paths = []
if VAR != "C":
    DS = 2
    ed = G(el, 3.0)[::DS, ::DS].astype(np.float64)
    rec, acc = d8(ed)
    hd, wd = ed.shape
    TH = 260                                                         # cells (~ 0.25 km^2 at 15.6 m) -> a gully
    ch = acc >= TH
    wdn = ndimage.binary_dilation(water, iterations=6)[::DS, ::DS].ravel()
    credn = ndimage.binary_dilation(cre, iterations=7)[::DS, ::DS].ravel()
    ch &= ~wdn & ~credn                                             # mapped creeks are drawn from data; DEM adds the gullies
    has_up = np.zeros(hd * wd, bool)
    idx = np.nonzero(ch)[0]
    r = rec[idx]; ok = r >= 0
    has_up[r[ok][ch[r[ok]]]] = True
    seen = np.zeros(hd * wd, bool)
    for h0 in idx[~has_up[idx]]:
        p = [h0]; c = h0
        while True:
            seen[c] = True; n = rec[c]
            if n < 0 or not ch[n]: break
            p.append(n)
            if seen[n]: break
            c = n
        if len(p) > 3: paths.append([(int(q % wd) * DS + DS / 2, int(q // wd) * DS + DS / 2, acc[q]) for q in p])

def chaikin(pts, it=3):
    for _ in range(it):
        if len(pts) < 3: return pts
        q = [pts[0]]
        for a, b in zip(pts[:-1], pts[1:]):
            q.append(tuple(0.75 * u + 0.25 * v for u, v in zip(a, b))); q.append(tuple(0.25 * u + 0.75 * v for u, v in zip(a, b)))
        q.append(pts[-1]); pts = q
    return pts

gl = Image.new("L", (PW * SSx, PH * SSx), 0); gd = ImageDraw.Draw(gl)
for p in paths:
    p = chaikin(p)
    for a, b in zip(p[:-1], p[1:]):
        wdt = 0.5 + 0.32 * np.log10(max(a[2], 1) / TH + 1) * 3        # 0.5 .. ~1.4 px
        gd.line([(a[0] * SSx, a[1] * SSx), (b[0] * SSx, b[1] * SSx)], fill=int(min(255, 140 + 60 * np.log10(a[2] / TH + 1))), width=max(1, int(wdt * SSx)))
gully = np.array(gl.resize((PW, PH), Image.BOX)).astype(np.float32) / 255
gully = G(gully, 0.5) * ss(0, 30, dout)
HAIR = np.array([78, 62, 42.])
col = col * (1 - 0.55 * gully[..., None]) + HAIR * (0.55 * gully[..., None])
col = col * (1 - 0.8 * cre_a[..., None]) + np.array([58, 52, 40.]) * (0.8 * cre_a[..., None])

# ---------------- TREES v11 (owner 2026-10-31 test; v10c + judge/checker fixes, build/judge-trees-v10.md) ----------------
# Angle C: every crown = one generated irregular outline filled with a window of a REAL forest canopy photo (3 public-
# domain USGS sources, assets/src/trees/SOURCES.md, tools/make_tree_sprites.py C2). v11: per-crown light ramp + small
# highlights (volume, not a textured ball), calmer texture, soft edges (no sticker ring), mid-green understory in the
# gaps (no black holes), shadows half as dark, trees exempt from the vignette, belts only along the RIVER, continuous.
K = 1 if os.environ.get('FULL') == '1' else 2              # FULL bake: no supersampling (memory)
TR = np.random.default_rng(23)
TBLUR = float(os.environ.get("TBLUR", "0.35"))
TMID = float(os.environ.get("TMID", "0.45"))
TCFG = dict(d=(24, 44), sp=21, tint=0.05, shade=0.12, tex=0.10, fine=float(os.environ.get("TFINE", "1.3")), low=0.25, lsig=float(os.environ.get("TLSIG", "8")), pit=0.8, rag=0.3)
# placement: belts on each bank of the RIVER only (thin creeks/ponds removed by an opening), few gaps
gap = G(rng.standard_normal((PH, PW)).astype(np.float32), 55); gap /= gap.std()
fld2 = G(rng.standard_normal((PH, PW)).astype(np.float32), 12); fld2 /= fld2.std()
RIV_OPEN = int(os.environ.get("RIV_OPEN", "9"))
river = ndimage.binary_opening(water, iterations=RIV_OPEN)               # only water wider than ~2*RIV_OPEN px
_rl, _rn = ndimage.label(river)
if _rn:
    _rs = ndimage.sum(river, _rl, range(1, _rn + 1)); river = np.isin(_rl, 1 + np.nonzero(_rs >= 6000)[0])
    if os.environ.get('MAIN_ONLY') == '1':                                   # owner 2026-11-01: trees ONLY along the main river, not every pocket/bay/oxbow
        river = (_rl == 1 + int(np.argmax(_rs)))
river = ndimage.binary_dilation(river, iterations=RIV_OPEN + 2) & water   # river banks back, creeks stay out
_drv = ndimage.distance_transform_edt(~river)
halfw = wmax[niy, nix] - 1
band = np.clip(46 + 1.2 * halfw, 52, 92) * (1 + 0.20 * fld2)
cand = []
for _ in range(int(PW * PH / 25)):
    x, y = rng.uniform(0, PW), rng.uniform(0, PH); iy, ix = int(y), int(x)
    d = _drv[iy, ix]
    if water[iy, ix] or d < 11 + 4 * fld2[iy, ix] or d > band[iy, ix]: continue
    if rng.random() > (0.45 + 0.55 * ss(-1.5, -0.9, gap[iy, ix])) * (1 - ss(0.7, 1.0, d / band[iy, ix]) * 0.8): continue
    cand.append((x, y))
if os.environ.get('NO_TREES') == '1': cand = []                     # owner 2026-11-01: no trees at all (distracting)
from scipy.spatial import cKDTree
pts = []
if cand:
    cand = np.array(cand); TR.shuffle(cand)
    occ = {}; CS = TCFG["sp"]
    for x, y in cand:
        gx_, gy_ = int(x // CS), int(y // CS); bad = False
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for (u, w) in occ.get((gx_ + dx, gy_ + dy), ()):
                    if (u - x) ** 2 + (w - y) ** 2 < CS * CS: bad = True
        if bad: continue
        occ.setdefault((gx_, gy_), []).append((x, y)); pts.append((x, y))
if pts:                                                              # no stray clumps: keep belts of >= 14 trees
    _a = np.array(pts); _pairs = cKDTree(_a).query_pairs(r=40, output_type="ndarray")
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    _g = coo_matrix((np.ones(len(_pairs)), (_pairs[:, 0], _pairs[:, 1])), shape=(len(_a), len(_a)))
    _nc, _lab = connected_components(_g, directed=False)
    _sz = np.bincount(_lab)
    pts = [p_ for p_, l_ in zip(pts, _lab) if _sz[l_] >= 14]
_lib = np.load("assets/src/trees/sprites_C2.npz")
LIB = [_lib[k] for k in sorted(_lib.files)]
def _bleed(s_):                                                      # transparent pixels take the nearest leaf colour
    s_ = s_.copy(); _, (iy_, ix_) = ndimage.distance_transform_edt(s_[..., 3] < 128, return_indices=True)
    s_[..., :3] = s_[iy_, ix_, :3]; return s_
LIB = [_bleed(s_) for s_ in LIB]
_px = np.concatenate([s_[..., :3][s_[..., 3] > 160] for s_ in LIB]).astype(np.float32)
_mu, _sd = _px.mean(0), _px.std(0)
T_MU = np.array([float(v) for v in os.environ.get("T_MU", "76,85,57").split(",")])
WL = np.array([0.33, 0.34, 0.33])
def regrade(rgb, a, dt):
    lum = (rgb - _mu) @ WL / _sd.mean()
    m = (a > 0.3).astype(np.float32)
    low = G(lum * m, dt / TCFG["lsig"]) / np.maximum(G(m, dt / TCFG["lsig"]), 1e-3)
    chrom = (rgb - _mu) - ((rgb - _mu) @ WL)[..., None]
    spk = G(lum, 1.1 * K)                                            # 3 bands: leaf speckle | camo-scale blotches | crown
    l2 = TCFG["fine"] * (lum - spk) + TMID * (spk - low) + TCFG["low"] * low
    l2 = np.where(l2 < 0, -TCFG["pit"] * np.tanh(-l2 / TCFG["pit"]), l2)
    return T_MU * (1 + 0.30 * l2)[..., None] + chrom * 0.35
YS, XS = PH * K, PW * K
big = np.repeat(np.repeat(col, K, 0), K, 1)
Hf = np.zeros((YS, XS), np.float32)
Grem = np.ones((YS, XS), np.float32)                                 # ground still visible through the trees
sun = Lv[:2] / np.linalg.norm(Lv[:2])                                # image-plane direction toward the sun (NW)
pts.sort(key=lambda p_: (p_[1] + TR.uniform(-12, 12)))
for x, y in pts:
    s_ = LIB[int(TR.integers(0, len(LIB)))]
    im = Image.fromarray(s_, "RGBA")
    if TR.random() < 0.5: im = im.transpose(Image.TRANSPOSE)
    im = im.rotate(TR.uniform(-40, 40), resample=Image.BICUBIC, expand=True)
    area = (np.asarray(im)[..., 3] > 128).sum()
    dt = TR.uniform(*TCFG["d"]) * K
    f = dt / max(2 * np.sqrt(area / np.pi), 4)
    im = im.resize((max(3, int(im.width * f)), max(3, int(im.height * f))), Image.LANCZOS)
    arr = np.asarray(im).astype(np.float32)
    a = np.clip(arr[..., 3] / 255, 0, 1)
    if a.max() < 0.5: continue
    rgb = G(arr[..., :3], (TBLUR * K, TBLUR * K, 0))                   # calmer texture (~0.4-0.7 px blur at 1x)
    rgb = regrade(rgb, a, dt)
    _d = rgb.mean(-1); _d = (_d - G(_d, 1.5 * K)) / 12
    _in = ndimage.distance_transform_edt(a > 0.5)
    a = np.clip(a + TCFG["rag"] * np.minimum(_d, 0.2) * (1 - ss(0, 3 * K, _in)) * (a > 0.05), 0, 1)
    a = np.clip(G(a, 0.6 * K) * 1.15 - 0.075, 0, 1)                     # 1-1.5 px soft edge, no stroke
    hh, ww = a.shape
    inside = ndimage.distance_transform_edt(a > 0.5)
    yy_, xx_ = np.mgrid[0:hh, 0:ww].astype(np.float32)
    r_ = dt / 2; px_, py_ = (xx_ - ww / 2) / r_, (yy_ - hh / 2) / r_
    v_ = np.clip(px_ * sun[0] + py_ * sun[1], -1, 1)                   # +1 top-left (sunward) .. -1 bottom-right
    hx, hy = 0.3 * sun[0], 0.3 * sun[1]
    dd = (px_ - hx) ** 2 + (py_ - hy) ** 2
    ramp = (1 + 0.20 * v_ - 0.02) * (1 - 0.05 * np.clip(dd, 0, 2))     # +18 % top-left .. -22 % bottom-right
    for _k in range(int(TR.integers(2, 5))):                           # 2-4 small sunlit sub-lobes
        ang = np.arctan2(sun[1], sun[0]) + TR.uniform(-1.3, 1.3); rad_ = TR.uniform(0.2, 0.6)
        cx_, cy_ = rad_ * np.cos(ang), rad_ * np.sin(ang); sg = TR.uniform(0.14, 0.22)
        ramp = ramp + TR.uniform(0.06, 0.11) * np.exp(-((px_ - cx_) ** 2 + (py_ - cy_) ** 2) / (2 * sg * sg))
    rgb = rgb * ramp[..., None]
    lum = rgb.mean(-1); lum = (lum - lum[a > 0.5].mean()) / (lum[a > 0.5].std() + 1e-3)
    ht = dt * TR.uniform(0.85, 1.15)
    dome = np.sqrt(np.clip(inside / (0.5 * dt / 2), 0, 1))
    h = ht * (0.62 + 0.38 * dome) + TCFG["tex"] * dt * 0.25 * lum * ss(0, 3 * K, inside)
    gy_, gx_ = np.gradient(G(ht * (0.62 + 0.38 * dome), 1.2 * K))
    nn = 1 / np.sqrt(gx_ ** 2 + gy_ ** 2 + 1)
    lam = (-gx_ * Lv[0] - gy_ * Lv[1] + Lv[2]) * nn / Lv[2]
    rgb = rgb * (1 + TCFG["shade"] * (np.clip(lam, 0, 1.6) - 1))[..., None]   # weak dome: no textured balls
    rgb = rgb * (1 + TCFG["tint"] * TR.normal() * np.array([1.0, 0.95, 0.7])) + np.array([3, 2, -1.]) * TR.normal()
    X, Y = int(x * K) - ww // 2, int(y * K) - hh // 2
    ya2, xa2 = max(Y, 0), max(X, 0); yb2, xb2 = min(Y + hh, YS), min(X + ww, XS)
    if yb2 <= ya2 or xb2 <= xa2: continue
    ky, kx = ya2 - Y, xa2 - X
    sl = (slice(ya2, yb2), slice(xa2, xb2)); ksl = (slice(ky, ky + yb2 - ya2), slice(kx, kx + xb2 - xa2))
    hk = h[ksl]; ak = a[ksl]
    w_ = ak * np.clip((hk - Hf[sl]) / (0.14 * dt) + 0.5, 0, 1)        # soft meeting line, no seam
    big[sl] = big[sl] * (1 - w_[..., None]) + rgb[ksl] * w_[..., None]
    Hf[sl] = np.maximum(Hf[sl], hk * (ak > 0.35))
    Grem[sl] *= (1 - w_)
# understory: the small gaps INSIDE a belt are mid-green leaf shade, not black ground shadow
onc = Hf > 0
belt = ndimage.binary_closing(onc, structure=ndimage.generate_binary_structure(2, 1), iterations=int(7 * K))
und = np.clip(Grem * 1.25, 0, 1) * G(belt.astype(np.float32), 1.0 * K)                 # every see-through seam/gap
UND = T_MU * 0.62
big = big * (1 - 0.85 * und[..., None]) + UND * (0.85 * und[..., None])
Acov = 1 - Grem * (1 - 0.85 * und)
# sun-ray cast shadows from the height field: soft, about half as dark as v10 (shadowed ground ~0.75 of open ground)
TAN = 1.9
occ = np.zeros_like(Hf)
for t in range(1, int(Hf.max() / TAN) + 2):
    sx, sy = int(round(-sun[0] * t)), int(round(-sun[1] * t))
    sh_ = np.roll(np.roll(Hf, sx, 1), sy, 0) - t * TAN
    np.maximum(occ, sh_, out=occ)
shd = np.clip((occ - Hf) / (3.0 * K), 0, 1)
shd_g = G(np.where(onc, 0.3, shd), 1.8 * K)
shd = np.where(onc, G(shd, 1.6 * K), shd_g)
cov = G(onc.astype(np.float32), 5 * K)
SH_G, SH_C = float(os.environ.get("SH_G", "0.22")), 0.22
big *= (1 - np.where(onc, SH_C, SH_G) * shd - np.where(onc, 0.0, 0.04) * cov)[..., None]
col = big.reshape(PH, K, PW, K, 3).mean((1, 3))
tal = Acov.reshape(PH, K, PW, K).mean((1, 3))
# ---------------- GRADE (trees exempt from most of the vignette: they keep the reference brightness) ----------------
col = col[oy:oy + H, ox:ox + W]; tal = tal[oy:oy + H, ox:ox + W, None]
c = np.clip(col / 255, 0, 1)
ct = c * np.array([1.02, 1.0, 0.97])
c = c + 0.06 * (c - c * c * (3 - 2 * c)) * -1                      # gentle S-curve
c = c * np.array([1.02, 1.0, 0.95])
yy, xx = np.mgrid[0:H, 0:W]
vig = (lambda v: np.ones_like(v) if os.environ.get('FULL') == '1' else v)(1 - 0.52 * ss(0.30, 1.25, np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)))
c = c * vig[..., None]
ct = ct * (1 - 0.30 * (1 - vig))[..., None]                         # a light vignette on the trees only
c = c * (1 - tal) + ct * tal + rng.normal(0, 0.004, (H, W))[..., None]
img = Image.fromarray(np.clip(c * 255, 0, 255).astype(np.uint8))
img.save(out, quality=93)
print(out, len(pts), "crowns", len(paths), "gullies", f"{time.time() - t0:.1f}s")

# ---------------- OVERLAY COMPATIBILITY TEST ----------------
ovp = os.environ.get("OVERLAY")
if ovp:
    ctl = Image.open(os.environ.get("CTL", f"assets/media/hka_{base}_ctl_nov25e_mx.png")).convert("RGBA")
    ctl = ctl.resize((5760, 3240), Image.BILINEAR).crop((x0, y0, x0 + W, y0 + H))
    o = np.array(ctl).astype(np.float32) / 255
    b = np.array(img).astype(np.float32) / 255
    b = b * (1 - o[..., 3:]) + b * o[..., :3] * o[..., 3:]                       # CSS mix-blend-mode: multiply
    im2 = Image.fromarray(np.clip(b * 255, 0, 255).astype(np.uint8)).convert("RGBA")
    # 15 px two-colour glowing front (blue #2c57b7 / red #bc2528, glow 0.47)
    fr = [(int(W * (0.30 + 0.12 * np.sin(f * 6.0))), int(H * f)) for f in np.linspace(0.10, 0.90, 40)]
    fr = [(x + int(W * 0.25), y) for x, y in fr]
    fx = [(x + 0.0, y) for x, y in fr]
    def off(pl, d):
        q = []
        for i, (x, y) in enumerate(pl):
            a, bb = pl[max(i - 1, 0)], pl[min(i + 1, len(pl) - 1)]
            dx, dy = bb[0] - a[0], bb[1] - a[1]; L = np.hypot(dx, dy) + 1e-6
            q.append((x - dy / L * d, y + dx / L * d))
        return q
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gdw = ImageDraw.Draw(glow)
    gdw.line(off(fx, -6), fill=(44, 87, 183, 255), width=18, joint="curve"); gdw.line(off(fx, 6), fill=(188, 37, 40, 255), width=18, joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(7)); ga = np.array(glow); ga[..., 3] = np.clip(ga[..., 3] * 0.47 * 1.6, 0, 255).astype(np.uint8)
    im2 = Image.alpha_composite(im2, Image.fromarray(ga))
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    bd.line(off(fx, -3.75), fill=(44, 87, 183, 255), width=8, joint="curve"); bd.line(off(fx, 3.75), fill=(188, 37, 40, 255), width=8, joint="curve")
    im2 = Image.alpha_composite(im2, band)
    d = ImageDraw.Draw(im2)
    def counter(x, y, colr):
        d.rectangle((x - 30, y - 22, x + 30, y + 22), fill=(0, 0, 0, 90))
        d.rectangle((x - 27, y - 20, x + 27, y + 20), fill=colr, outline=(20, 20, 20, 255), width=2)
        d.line((x - 18, y - 12, x + 18, y + 12), fill=(247, 243, 234, 255), width=3); d.line((x - 18, y + 12, x + 18, y - 12), fill=(247, 243, 234, 255), width=3)
    for f, s in [(0.35, -1), (0.45, -1), (0.55, -1), (0.40, 1), (0.52, 1), (0.64, 1)]:
        i = int((f - 0.28) / 0.44 * 39); x, y = fr[i]
        counter(int(x + s * 60), int(y), (31, 79, 196, 255) if s < 0 else (196, 18, 31, 255))
    im2.convert("RGB").save(ovp, quality=93)
    print(ovp)
