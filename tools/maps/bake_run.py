"""Runner for bake_clean.py: shot setup, camera, compositing, extras (lines, glows, dots...), world inset, ffmpeg, json, parallel stages."""
import os, sys, json, math, time, subprocess, traceback
import numpy as np, cv2
from scipy import ndimage
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp
import bake_clean as BC
from bake_clean import W, H, OW, OH, FPS, NICE, LSTEP, P, make_proj, canvas_latlon
from v01_map_shots import VIEWS, SHOTS
PLAN = json.load(open(os.path.join(BC.HERE, "v01_map_plan.json")))
TAIL = 0.7                       # extra seconds baked after the planned shot length
NAVY = np.array([4, 10, 24], np.float32); AMBER = (214, 166, 84); GOLD = (201, 164, 92)
IW, IH, IX, IY = 360, 180, 50, 850     # world inset rectangle (1920x1080 px)

def ease2(u): u = min(max(u, 0.0), 1.0); return 2 * u * u if u < .5 else 1 - 2 * (1 - u) ** 2     # gsap power2.inOut (the template gauge)
def easeS(u): u = min(max(u, 0.0), 1.0); return 0.5 - 0.5 * math.cos(math.pi * u)
def lerp(a, b, f): return a + (b - a) * f
def snap(L): return int(round(L / LSTEP)) * LSTEP

class Shot:
    def __init__(s, sid):
        s.id = sid; s.spec = SHOTS[sid]; s.plan = PLAN[sid]; s.view = VIEWS[s.spec["view"]]
        s.V = make_proj(s.view); s.vk = s.V.key(); s.dur = round(s.plan["dur"] + TAIL, 3); s.n = int(round(s.dur * FPS))
        L0, L1 = s.spec["sl"]; g = s.plan.get("gauge")
        if "sl_t" in s.spec: s.sl_t = s.spec["sl_t"]
        elif g and L0 != L1: s.sl_t = (g["at_local"], g["dur"])
        else: s.sl_t = (0.0, 1.0)
        s.L0, s.L1 = L0, L1
        if L0 != L1 and s.sl_t[0] + s.sl_t[1] + 0.2 > s.dur:        # keep the coast in sync with the template gauge even when the gauge outlasts the shot
            s.dur = round(s.sl_t[0] + s.sl_t[1] + 0.2, 3); s.n = int(round(s.dur * FPS))
        s.p_t = s.spec.get("p_t", (0.0, s.dur))
    def L(s, t): return lerp(s.L0, s.L1, ease2((t - s.sl_t[0]) / s.sl_t[1])) if s.L0 != s.L1 else float(s.L0)
    def p(s, t):
        p0, p1 = s.spec["p"]; a, b = s.p_t; return lerp(p0, p1, easeS((t - a) / (b - a)))
    def levels(s):
        ls = {snap(s.L0), snap(s.L1)}
        if s.L0 != s.L1:
            lo, hi = sorted((snap(s.L0), snap(s.L1))); ls |= set(range(lo, hi + 1, LSTEP))
        for e in s.spec.get("extras", []):
            if e["k"] == "coast": ls.add(0)
            if e["k"] == "glow": ls |= {0, -120}
            if e["k"] == "lake": ls.add(snap(s.L0))
        return sorted(ls)
    def pin_planned(s):
        pp = s.plan.get("pin"); return (pp["x"], pp["y"]) if pp else None

# ------------------------------------------------------------------ geometry helpers
def catmull(pts, n=10):
    pts = [np.asarray(p, float) for p in pts]
    if len(pts) < 3: return np.array(pts)
    q = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for j in range(n):
            t = j / n; out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-1]); return np.array(out)
def trunc(path, u):
    """first fraction u of a polyline, + its head point and direction"""
    seg = np.hypot(*np.diff(path, axis=0).T); cum = np.r_[0, np.cumsum(seg)]; tot = cum[-1]; d = tot * min(max(u, 0), 1)
    k = int(np.searchsorted(cum, d, side="right")) - 1; k = min(max(k, 0), len(path) - 2)
    f = (d - cum[k]) / max(seg[k], 1e-6); head = path[k] + (path[k + 1] - path[k]) * f
    return np.vstack([path[:k + 1], head]), head, path[k + 1] - path[k], cum, d
def dashed_runs(path, dash, gap):
    seg = np.hypot(*np.diff(path, axis=0).T); cum = np.r_[0, np.cumsum(seg)]; tot = cum[-1]; runs = []; a = 0.0
    while a < tot:
        b = min(a + dash, tot); ia, ib = np.searchsorted(cum, [a, b]); xs = np.interp([a, b], cum, path[:, 0]); ys = np.interp([a, b], cum, path[:, 1])
        mid = path[ia:ib]; runs.append(np.vstack([[xs[0], ys[0]], mid, [xs[1], ys[1]]])); a += dash + gap
    return runs
def blend(img, mask, color, alpha):
    if alpha <= 0: return
    a = (mask.astype(np.float32) * (alpha / 255.0))[..., None]; img *= 1 - a; img += a * np.array(color, np.float32)

class Renderer:
    def __init__(s, sh):
        s.sh = sh; s.V = sh.V; s.spec = sh.spec
        s.lv = {}; s.ice = np.load(P("ice", sh.vk + "_frames.npy"), mmap_mode="r")
        dk = np.load(P("ice", sh.vk + "_dark.npy")).astype(np.float32); fr = np.load(P("ice", sh.vk + "_free.npy"))
        s.aux = np.dstack([np.clip(dk / 0.5, 0, 1) * 255, fr]).astype(np.uint8)
        s.setup_camera(); s.setup_extras(); s.setup_inset(); s.setup_post()
    def level(s, L, vk=None, V=None):
        key = (vk or s.sh.vk, L)
        if key not in s.lv: s.lv[key] = np.load(BC.levels_file(*key), mmap_mode="r")
        return s.lv[key]
    # ---- camera
    def setup_camera(s):
        sp, V, sh = s.spec, s.V, s.sh; s.s0, s.s1 = sp["s"]
        s.pin = sp.get("pin"); pp = sh.pin_planned()
        s.anchor = None
        if sp.get("anchor_at"):
            (la, lo), (X, Y) = sp["anchor_at"]; x, y = V.fwd(la, lo); s.anchor = (float(x), float(y), X * 1.5, Y * 1.5)
        elif s.pin and not sp.get("free_pin"):
            ps = sp.get("pin_screen") or pp or (640, 360)
            x, y = V.fwd(*s.pin); s.anchor = (float(x), float(y), ps[0] * 1.5, ps[1] * 1.5)
        s.cpath = [tuple(map(float, V.fwd(*c))) for c in sp["center"]] if sp.get("center") else [(W / 2, H / 2)] * 2
        s.pan = None
        if sp.get("pan"):
            g, t0, t1 = sp["pan"]; s.pan = (tuple(map(float, V.fwd(*g))), t0, t1)
    def cam(s, t):
        sh = s.sh; u = easeS(t / sh.dur); sc = max(lerp(s.s0, s.s1, u), 0.667)
        if s.anchor: ax, ay, X, Y = s.anchor; cx, cy = ax - (X - OW / 2) / sc, ay - (Y - OH / 2) / sc
        else:
            f = easeS(t / sh.dur); cx, cy = lerp(s.cpath[0][0], s.cpath[1][0], f), lerp(s.cpath[0][1], s.cpath[1][1], f)
        if s.pan:
            (px, py), t0, t1 = s.pan; f = ease2((t - t0) / (t1 - t0)); cx, cy = lerp(px, cx, f), lerp(py, cy, f)
        cx = min(max(cx, OW / 2 / sc), W - OW / 2 / sc); cy = min(max(cy, OH / 2 / sc), H - OH / 2 / sc)
        return cx, cy, sc
    def M(s, cx, cy, sc): return np.array([[sc, 0, OW / 2 - cx * sc], [0, sc, OH / 2 - cy * sc]], np.float64)
    def to_screen(s, pts, M):          # canvas px -> screen px
        pts = np.asarray(pts, float); return np.c_[pts[:, 0] * M[0, 0] + M[0, 2], pts[:, 1] * M[1, 1] + M[1, 2]]
    def ll_screen(s, pts, M, V=None):
        a = np.asarray(pts, float); x, y = (V or s.V).fwd(a[:, 0], a[:, 1]); return s.to_screen(np.c_[x, y], M)
    # ---- extras (set up once per shot)
    def setup_extras(s):
        s.ex = []; sh = s.sh; V = s.V
        for e in s.spec.get("extras", []):
            e = dict(e); k = e["k"]
            if k == "coast":
                cov = (np.asarray(s.level(0)[..., 3]) > 127).astype(np.uint8)
                cs, _ = cv2.findContours(cov, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE); e["cnt"] = [c[:, 0, :].astype(float) for c in cs if len(c) > 60]
            elif k == "coastline":
                cov = (np.asarray(s.level(e["level"])[..., 3]) > 127).astype(np.uint8)
                cs, _ = cv2.findContours(cov, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE); la0, la1, lo0, lo1 = e["box"]; segs = []
                for c in cs:
                    c = c[:, 0, :].astype(float)
                    if len(c) < 200: continue
                    lat_, lon_ = V.inv(c[:, 0], c[:, 1]); lon_ = np.where(lon_ > 180, lon_ - 360, lon_); ok = (lat_ >= la0) & (lat_ <= la1) & (lon_ >= lo0) & (lon_ <= lo1)
                    idx = np.flatnonzero(ok)
                    if len(idx) < 50: continue
                    for run in np.split(idx, np.flatnonzero(np.diff(idx) > 3) + 1):
                        if len(run) > 80: segs.append(c[run[::2]])
                e["segs"] = segs
            elif k == "glow":
                lat, lon = canvas_latlon(V); box = np.zeros((H, W), bool)
                for la0, la1, lo0, lo1 in e["boxes"]:
                    lon_u = np.where(lon > 180, lon - 360, lon); box |= (lat >= la0) & (lat <= la1) & (lon_u >= lo0) & (lon_u <= lo1)
                c0 = np.asarray(s.level(0)[..., 3]) > 127; c1 = np.asarray(s.level(-120)[..., 3]) > 127
                m = (c1 if e.get("land") else (c1 & ~c0)).astype(np.float32) * cv2.GaussianBlur(box.astype(np.float32), (0, 0), 40)
                e["mask"] = (np.clip(cv2.GaussianBlur(m, (0, 0), 5) * 1.6, 0, 1) * 255).astype(np.uint8)
            elif k == "lake":
                cov = np.asarray(s.level(snap(sh.L0))[..., 3]) < 128; lab, n = ndimage.label(cov)
                seed = e.get("seed") or s.sh.view["lake"]["seed"]; x, y = V.fwd(*seed); lid = lab[int(y), int(x)]
                m = (lab == lid) if lid else np.zeros_like(cov); e["mask"] = (np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 2.5) * 1.3, 0, 1) * 255).astype(np.uint8)
            elif k == "zoneline":
                z = np.load(P("elev", V.key() + "_zone.npy")).astype(np.uint8)
                cs, _ = cv2.findContours(z, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); e["cnt"] = [c[:, 0, :].astype(float) for c in cs if len(c) > 400]
            elif k == "alaska":
                import bake_clean as B
                B.ne_fetch(); poly = max(((ft["geometry"]["coordinates"] if ft["geometry"]["type"] == "MultiPolygon" else [ft["geometry"]["coordinates"]]) for ft in B.load_ne("ne_50m_admin_1_states_provinces")["features"] if ft["properties"].get("name") == "Alaska"), key=len)
                parts = []
                lat0, lon0 = math.radians(64), math.radians(-152)
                for pl in poly:
                    a = np.array(pl[0]); la, lo = np.radians(a[:, 1]), np.radians(a[:, 0]); lo = np.where(lo > 0, lo - 2 * math.pi, lo)
                    kk = np.sqrt(2 / (1 + math.sin(lat0) * np.sin(la) + math.cos(lat0) * np.cos(la) * np.cos(lo - lon0)))
                    x = B.EARTH * kk * np.cos(la) * np.sin(lo - lon0); y = B.EARTH * kk * (math.cos(lat0) * np.sin(la) - math.sin(lat0) * np.cos(la) * np.cos(lo - lon0))
                    m = float(V.mpp(1.0)); parts.append(np.c_[x / m, -y / m])
                allp = np.vstack(parts); ctr = (allp.min(0) + allp.max(0)) / 2; e["parts"] = [p - ctr for p in parts if len(p) > 20]
                e["home"] = tuple(map(float, V.fwd(1.5, 108.0)))
            s.ex.append(e)
    def draw_extras(s, img, M, t, sc, cov):
        for e in s.ex:
            k = e["k"]
            if k in ("line", "arrow", "walk", "bar"):
                pts = e.get("pts") if k != "bar" else [e["a"], e["b"]]
                path = s.ll_screen(pts, M); path = catmull(path, 10) if k != "bar" else path
                u = ease2((t - e["t0"]) / max(e["t1"] - e["t0"], 1e-3))
                if u <= 0: continue
                tp, head, d, cum, dd = trunc(path, u); m = np.zeros((OH, OW), np.uint8); w = int(e.get("w", 4))
                if e.get("dash") and len(tp) > 1:
                    for r in dashed_runs(tp, *e["dash"]): cv2.polylines(m, [np.round(r * 16).astype(np.int32)], False, 255, w, cv2.LINE_AA, 4)
                elif k == "walk":
                    for r in dashed_runs(tp, 2, 15): cv2.polylines(m, [np.round(r * 16).astype(np.int32)], False, 255, 7, cv2.LINE_AA, 4)
                else: cv2.polylines(m, [np.round(tp * 16).astype(np.int32)], False, 255, w, cv2.LINE_AA, 4)
                col = e.get("color", (236, 224, 196)); fade = min(1.0, (t - e["t0"]) / 0.3 + 0.0)
                if k == "arrow" and u > 0.02:
                    dn = d / (np.hypot(*d) + 1e-6); nrm = np.array([-dn[1], dn[0]]); L = 3.2 * w
                    tri = np.array([head + dn * L * 0.6, head - dn * L + nrm * L * 0.8, head - dn * L - nrm * L * 0.8]); cv2.fillConvexPoly(m, np.round(tri * 16).astype(np.int32), 255, cv2.LINE_AA, 4)
                if k == "bar":
                    for q, f in ((path[0], 1), (head, 1)):
                        dn = (path[1] - path[0]) / np.hypot(*(path[1] - path[0])); nrm = np.array([-dn[1], dn[0]]) * 22
                        cv2.line(m, tuple(np.round((q - nrm) * 16).astype(int)), tuple(np.round((q + nrm) * 16).astype(int)), 255, w, cv2.LINE_AA, 4)
                if k == "walk": cv2.circle(m, tuple(np.round(head * 16).astype(int)), 11 * 16, 255, -1, cv2.LINE_AA, 4)
                if e.get("glow"): blend(img, cv2.GaussianBlur(m, (0, 0), 6), col, 0.5)
                blend(img, m, col, min(1.0, fade) * e.get("alpha", 0.92)); e["last"] = path
            elif k == "coast":
                m = np.zeros((OH, OW), np.uint8); u = 1.0
                if e.get("draw"): u = easeS((t - e["draw"][0]) / (e["draw"][1] - e["draw"][0]))
                for c in e["cnt"]:
                    q = s.to_screen(c, M); q = q[: max(2, int(len(q) * u))] if u < 1 else q
                    if u > 0: cv2.polylines(m, [np.round(q * 16).astype(np.int32)], u >= 1, 255, 2 if not e.get("color") else 3, cv2.LINE_AA, 4)
                blend(img, m, e.get("color", (236, 224, 196)), 0.85 * min(1, t / 0.5))
            elif k == "coastline":
                u = easeS((t - e["t0"]) / (e["t1"] - e["t0"])); m = np.zeros((OH, OW), np.uint8)
                for c in e["segs"]:
                    q = s.to_screen(c, M); q = q[: max(2, int(len(q) * u))]
                    if u > 0: cv2.polylines(m, [np.round(q * 16).astype(np.int32)], False, 255, e.get("w", 3), cv2.LINE_AA, 4)
                blend(img, m, e["color"], 0.95)
            elif k == "zoneline":
                m = np.zeros((OH, OW), np.uint8)
                for c in e["cnt"]:
                    for r in dashed_runs(s.to_screen(c[::3], M), 22, 16): cv2.polylines(m, [np.round(r * 16).astype(np.int32)], False, 255, 3, cv2.LINE_AA, 4)
                blend(img, m, (236, 224, 196), 0.9 * min(1, max(0, (t - e["t0"]) / 0.5)))
            elif k == "glow":
                u = (t - e["t0"]) / max(e["t1"] - e["t0"], 1e-3); a = easeS(u) * (0.88 + 0.12 * math.sin(t * 3.0)) * e.get("alpha", 0.35)
                if a > 0.003: blend(img, cv2.warpAffine(e["mask"], M, (OW, OH), flags=cv2.INTER_LINEAR), AMBER, a)
            elif k == "lake":
                a = easeS((t - e["t0"]) / max(e["t1"] - e["t0"], 1e-3)) * e.get("alpha", 0.5)
                if e.get("t_out"): a *= 1 - easeS((t - e["t_out"][0]) / (e["t_out"][1] - e["t_out"][0]))
                if a > 0.003: blend(img, cv2.warpAffine(e["mask"], M, (OW, OH), flags=cv2.INTER_LINEAR), e["color"], a)
            elif k == "dots":
                m = np.zeros((OH, OW), np.uint8); pts = s.ll_screen(e["pts"], M); a = easeS((t - e["t_in"]) / 0.4) * (1 - easeS((t - e["t_out"]) / 0.8)) if not e.get("sink") else easeS((t - e["t_in"]) / 0.4)
                for q in pts:
                    al = a
                    if e.get("sink"): xi, yi = int(min(max(q[0], 0), OW - 1)), int(min(max(q[1], 0), OH - 1)); al = a * float(cov[yi, xi]) ** 2
                    mm = np.zeros((OH, OW), np.uint8); cv2.circle(mm, tuple(np.round(q * 16).astype(int)), int(e["r"] * 16 * sc / 0.8), 255, -1, cv2.LINE_AA, 4); blend(img, mm, (232, 205, 140), al)
            elif k == "ring":
                q = s.ll_screen([e["pt"]], M)[0]; u = easeS((t - e["t0"]) / 0.7)
                if u > 0:
                    m = np.zeros((OH, OW), np.uint8); r = e["r"] * (1 + 0.06 * math.sin((t - e["t0"]) * 5)); cv2.ellipse(m, tuple(np.round(q * 16).astype(int)), (int(r * 16),) * 2, -90, 0, 360 * u, 255, 4, cv2.LINE_AA, 4)
                    blend(img, m, GOLD, 0.95)
            elif k == "icering":
                u = ease2((t - e["t0"]) / (e["t1"] - e["t0"])); V = s.V; th = np.linspace(0, 360, 361)
                rng = np.random.default_rng(3); co = rng.normal(0, 1, 8); wob = sum(co[2 * i] * np.cos(np.radians(th) * (i + 1)) + co[2 * i + 1] * np.sin(np.radians(th) * (i + 1)) for i in range(3)) / 2.5
                m = np.zeros((OH, OW), np.uint8)
                for lat_f, alpha_ in ((lambda: e["lat0"] + wob * 0.3, 0.7), (lambda: lerp(e["lat0"], e["lat1"], u) + wob * u * 1.2, 0.95)):
                    la = lat_f(); x, y = V.fwd(la, th + V.rot0); path = s.to_screen(np.c_[x, y], M); mm = np.zeros((OH, OW), np.uint8)
                    for r in dashed_runs(path, 24, 18): cv2.polylines(mm, [np.round(r * 16).astype(np.int32)], False, 255, 3, cv2.LINE_AA, 4)
                    blend(img, mm, (236, 224, 196) if alpha_ < 0.8 else GOLD, alpha_ * min(1, (t - 0.2) / 0.5))
            elif k == "alaska":
                u = ease2((t - e["t0"]) / (e["t1"] - e["t0"])); hx, hy = e["home"]; off = (1 - u) * 1100
                m = np.zeros((OH, OW), np.uint8); f = np.zeros((OH, OW), np.uint8)
                for p in e["parts"]:
                    q = s.to_screen(p + np.array([hx + off, hy]), M); cv2.fillPoly(f, [np.round(q * 16).astype(np.int32)], 255, cv2.LINE_AA, 4); cv2.polylines(m, [np.round(q * 16).astype(np.int32)], True, 255, 3, cv2.LINE_AA, 4)
                blend(img, f, AMBER, 0.28 * min(1, (t - e["t0"]) / 0.2)); blend(img, m, AMBER, 0.95 * min(1, (t - e["t0"]) / 0.2))
    # ---- world inset
    def setup_inset(s):
        s.inset = None
        if not s.spec.get("inset"): return
        wv = VIEWS["world"]; Vw = make_proj(wv); wk = Vw.key()
        xl = float(Vw.fwd(0, -169.9)[0]); xr = float(Vw.fwd(0, 189.9)[0]); yc = float(Vw.fwd(18, 0)[1]); h = (xr - xl) / 2
        x0, x1 = int(max(xl, 0)), int(min(xr, W)); y0 = int(min(max(yc - h / 2, 0), H - h)); y1 = int(y0 + (x1 - x0) / 2)
        wice = np.load(P("ice", wk + "_frames.npy"), mmap_mode="r"); wdk = np.load(P("ice", wk + "_dark.npy")).astype(np.float32); wfr = np.load(P("ice", wk + "_free.npy"))
        s.inset = dict(V=Vw, wk=wk, box=(x0, y0, x1, y1), ice=wice, dk=cv2.resize(wdk[y0:y1, x0:x1], (IW, IH), interpolation=cv2.INTER_AREA), fr=cv2.resize(wfr[y0:y1, x0:x1], (IW, IH), interpolation=cv2.INTER_AREA))
        s.inset["rect"] = None
    def draw_inset(s, img, t, L, p, M, cx, cy, sc):
        d = s.inset
        if d is None: return
        x0, y0, x1, y1 = d["box"]; k = -L / LSTEP; k0 = int(math.floor(k)); f = k - k0
        def part(arr): return cv2.resize(np.asarray(arr[y0:y1, x0:x1]), (IW, IH), interpolation=cv2.INTER_AREA).astype(np.float32)
        A = part(s.level(-LSTEP * k0, d["wk"]));
        if f > 1e-3 and os.path.exists(BC.levels_file(d["wk"], -LSTEP * (k0 + 1))): A = A * (1 - f) + part(s.level(-LSTEP * (k0 + 1), d["wk"])) * f
        base = A[..., :3].copy(); cov = A[..., 3:] / 255
        dark = np.clip(d["dk"] * max(p, 0) ** 0.9, 0, 0.42)[..., None] * (1 - cov); base = base * (1 - dark) + NAVY * dark
        i = min(int(p * NICE), NICE - 1); fi = p * NICE - i
        if p > 0:
            I0 = part(d["ice"][i]); I1 = part(d["ice"][min(i + 1, NICE)]); I = I0 * (1 - fi) + I1 * fi
            ia = I[..., 3:] / 255 * np.clip(np.maximum(cov, d["fr"][..., None] / 255.0), 0, 1); base = base * (1 - ia) + I[..., :3] * ia
        # viewport rectangle of the shot (screen corners -> canvas -> lat/lon -> world inset px)
        crn = np.array([[0, 0], [OW, 0], [OW, OH], [0, OH]], float); cv_ = np.c_[(crn[:, 0] - M[0, 2]) / M[0, 0], (crn[:, 1] - M[1, 2]) / M[1, 1]]
        la, lo = s.V.inv(cv_[:, 0], cv_[:, 1]); wx, wy = d["V"].fwd(la, lo); wx = (wx - x0) * IW / (x1 - x0); wy = (wy - y0) * IH / (y1 - y0)
        tile = np.clip(base, 0, 255).astype(np.uint8).copy()
        if s.V.kind == "merc":
            r = np.round([[min(wx), min(wy)], [max(wx), max(wy)]]).astype(int); r[1] = np.maximum(r[1], r[0] + 7); cv2.rectangle(tile, tuple(r[0]), tuple(r[1]), GOLD, 1, cv2.LINE_AA)
        cv2.rectangle(tile, (0, 0), (IW - 1, IH - 1), (236, 224, 196), 1)
        a = min(1.0, t / 0.5)
        img[IY:IY + IH, IX:IX + IW] = img[IY:IY + IH, IX:IX + IW] * (1 - a) + tile.astype(np.float32) * a
    # ---- vignette + grain
    def setup_post(s):
        yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32); y = yy / OH
        ab = 0.62 * np.clip(1 - y / 0.24, 0, 1) ** 1.0 * 0 + 0.62 * np.clip((y - 0.76) / 0.24, 0, 1); at = 0.35 * np.clip(1 - y / 0.14, 0, 1)
        r = np.hypot((xx / OW - .5) / .5, (y - .5) / .5) / 1.2; ar = 0.6 * np.clip((r - .52) / .48, 0, 1)
        a = 1 - (1 - ab) * (1 - at) * (1 - ar); s.vig = (a[..., None]).astype(np.float32); s.vigc = np.array([4, 7, 11], np.float32)
        rng = np.random.default_rng(1); s.grain = rng.normal(0, 1.6, (OH + 64, OW + 64)).astype(np.float32)
        s.rng = np.random.default_rng(2)
    # ---- one frame
    def frame(s, t):
        sh = s.sh; L = sh.L(t); p = sh.p(t); cx, cy, sc = s.cam(t); M = s.M(cx, cy, sc)
        def wp(a): return cv2.warpAffine(np.asarray(a), M, (OW, OH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        lo, hi = min(sh.levels()), max(sh.levels()); Lc = min(max(L, lo), hi); k = -Lc / LSTEP; k0 = int(math.floor(k)); f = k - k0
        A = wp(s.level(-LSTEP * k0)).astype(np.float32)
        if f > 1e-3 and (-LSTEP * (k0 + 1)) >= lo: A = A * (1 - f) + wp(s.level(-LSTEP * (k0 + 1))).astype(np.float32) * f
        img = A[..., :3].copy(); cov = A[..., 3] / 255.0
        aux = wp(s.aux).astype(np.float32); dk = aux[..., 0] / 255 * 0.5; fr = aux[..., 1] / 255
        dark = np.clip(dk * max(p, 0) ** 0.9, 0, 0.42) * (1 - cov); img = img * (1 - dark[..., None]) + NAVY * dark[..., None]
        if p > 0.004:
            i = min(int(p * NICE), NICE - 1); fi = p * NICE - i
            I = wp(s.ice[i]).astype(np.float32)
            if fi > 1e-3: I = I * (1 - fi) + wp(s.ice[i + 1]).astype(np.float32) * fi
            ia = (I[..., 3] / 255 * np.clip(np.maximum(cov, fr), 0, 1))[..., None]; img = img * (1 - ia) + I[..., :3] * ia
        s.draw_extras(img, M, t, sc, cov)
        img = img * (1 - s.vig) + s.vigc * s.vig
        s.draw_inset(img, t, L, p, M, cx, cy, sc)
        dy, dx = s.rng.integers(0, 64, 2); img += s.grain[dy:dy + OH, dx:dx + OW, None]
        return np.clip(img + 0.0, 0, 255).astype(np.uint8), (cx, cy, sc, M)

def render_shot(sid):
    t0 = time.time(); sh = Shot(sid); R = Renderer(sh); os.makedirs(BC.OUT_DIR, exist_ok=True)
    out = os.path.join(BC.OUT_DIR, sid + ".mp4")
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                           "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-threads", "2", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    track = []
    for i in range(sh.n):
        t = i / FPS; fr, (cx, cy, sc, M) = R.frame(t); ff.stdin.write(fr.tobytes())
        if R.pin and i % 6 == 0 or i == sh.n - 1:
            if R.pin: x, y = sh.V.fwd(*R.pin); track.append([round(t, 2), round(float(x * M[0, 0] + M[0, 2]) / 1.5, 1), round(float(y * M[1, 1] + M[1, 2]) / 1.5, 1)])
    mid = R.cam(sh.dur / 2); lat_c = float(sh.V.inv(mid[0], mid[1])[0]); mpp_c = float(sh.V.mpp(lat_c)) / mid[2]
    ff.stdin.close(); ff.wait(); os.replace(out + ".tmp.mp4", out)
    info = json.load(open(os.path.join(BC.HERE, "v01_map_plan.json")))[sid]
    j = dict(id=sid, file=sid + ".mp4", width=OW, height=OH, fps=FPS, frames=sh.n, duration=sh.dur, planned_duration=sh.plan["dur"], clean=True,
             note="Clean bake: terrain, coastline, ice, ocean darkening, camera only. No labels, pin or gauge are drawn; the template draws them. Pin/overlay coordinates are in the 1280x720 design space of map_clip.",
             sea_level=dict(**{"from": sh.L0, "to": sh.L1}, t0=round(sh.sl_t[0], 3), dur=sh.sl_t[1], ease="power2.inOut", animated=sh.L0 != sh.L1),
             ice=dict(p0=sh.spec["p"][0], p1=sh.spec["p"][1]), planned=dict(pin=info["pin"], name_at=info["name_at"], date_at=info["date_at"]))
    if sh.L0 != sh.L1 or info.get("gauge"):
        g = info.get("gauge") or {}
        j["gauge"] = {"from": sh.L0, "to": sh.L1, "at_local": round(sh.sl_t[0], 3), "dur": sh.sl_t[1]}
        j["template_gauge_params"] = {"from": sh.L0, "to": sh.L1, "dur": sh.sl_t[1]}
        if g and (abs((g.get("at_local") or 0) - sh.sl_t[0]) > 0.01): j["gauge_note"] = "bake moved the coast at a different time than the chapter-JSON gauge: set gauge.at to local time %.2f s" % sh.sl_t[0]
    j["scale"] = dict(note="at the middle of the clip, frame centre", centre_lat=round(lat_c, 2), km_per_px_1920=round(mpp_c / 1000, 3), km_per_px_1280=round(mpp_c * 1.5 / 1000, 3),
                      px_per_degree_lat_1280=round(111.195 / (mpp_c * 1.5 / 1000), 2), px_per_degree_lat_1920=round(111.195 / (mpp_c / 1000), 2), camera_scale=round(mid[2], 3))
    if sh.spec.get("anchor_at"):
        (la, lo), (X, Y) = sh.spec["anchor_at"]; x59 = sh.V.fwd(59, lo); x68 = sh.V.fwd(68, lo); end_cam = R.cam(sh.dur / 2); Mm = R.M(*end_cam)
        j["measure_frame"] = dict(note="static framing; lat 68N / 59N in 1280x720 px (the template bar is (640,260)-(640,460))", y_68N=round(float(x68[1] * Mm[1, 1] + Mm[1, 2]) / 1.5, 1), y_59N=round(float(x59[1] * Mm[1, 1] + Mm[1, 2]) / 1.5, 1), x=round(float(x68[0] * Mm[0, 0] + Mm[0, 2]) / 1.5, 1))
    if R.pin:
        end = track[-1]; j["pin"] = dict(lat=R.pin[0], lon=R.pin[1], x=end[1], y=end[2], x1920=round(end[1] * 1.5), y1920=round(end[2] * 1.5), static=R.anchor is not None and not R.pan,
                                       template_param={"x": round(end[1]), "y": round(end[2])}, track=track, planned=info["pin"])
        if R.pan: j["pin"]["note"] = "camera pans until %.2f s; the pin is at x,y only after that" % R.pan[2]
    for e in R.ex:
        if e["k"] == "bar" and e.get("last") is not None:
            j["measure_bar"] = dict(a_xy=[round(float(q), 1) for q in e["last"][0] / 1.5], b_xy=[round(float(q), 1) for q in e["last"][-1] / 1.5], t0=e["t0"], t1=e["t1"], km=1000)
    if sh.spec.get("inset"): j["inset"] = dict(x1920=IX, y1920=IY, w1920=IW, h1920=IH, x=IX / 1.5, y=IY / 1.5, w=IW / 1.5, h=IH / 1.5, note="world inset with the Ice Age sheets is baked in (rule 18); keep this corner free of overlays")
    json.dump(j, open(os.path.join(BC.OUT_DIR, sid + ".json"), "w"), indent=1)
    return sid, round(time.time() - t0, 1), sh.n

# ------------------------------------------------------------------ orchestration
def run_stage(name, fn, jobs, nproc):
    t = time.time(); res = []; fails = []
    print(f"[{time.strftime('%H:%M:%S')}] stage {name}: {len(jobs)} jobs on {nproc} procs", flush=True)
    if not jobs: return res, fails
    with ProcessPoolExecutor(max_workers=nproc, mp_context=mp.get_context("fork")) as ex:
        fut = {ex.submit(fn, *a): a for a in jobs}
        for i, f in enumerate(as_completed(fut), 1):
            try: res.append(f.result())
            except Exception as e: fails.append((fut[f][0], repr(e))); print("FAIL", fut[f][:1], repr(e), traceback.format_exc()[-600:], flush=True)
            if i % 20 == 0 or i == len(jobs): print(f"  {name} {i}/{len(jobs)}  {time.time()-t:.0f}s", flush=True)
    print(f"[{time.strftime('%H:%M:%S')}] stage {name} done in {time.time()-t:.0f}s, {len(fails)} failed", flush=True); return res, fails

def main(args):
    nproc = len(os.sched_getaffinity(0)); ids = []; cmd = args[0] if args else "plan"; i = 1
    while i < len(args):
        if args[i] == "-j": nproc = int(args[i + 1]); i += 2
        else: ids.append(args[i]); i += 1
    ids = ids or list(SHOTS)
    if cmd == "plan":
        for sid in ids: sh = Shot(sid); print(sid, sh.spec["view"], f"dur {sh.dur}", f"L {sh.L0}->{sh.L1} @{sh.sl_t}", "levels", len(sh.levels()), "p", sh.spec["p"])
        return
    t0 = time.time(); shots = [Shot(s) for s in ids]
    views = {}; need = {}; icev = {}
    def reg(vname, levels):
        V = make_proj(VIEWS[vname]); views[V.key()] = VIEWS[vname]; need.setdefault(V.key(), set()).update(levels); icev[V.key()] = VIEWS[vname]
    for sh in shots:
        reg(sh.spec["view"], sh.levels())
        if sh.spec.get("inset"): reg("world", range(-120, 1, LSTEP) if sh.L0 != sh.L1 else [snap(sh.L0)]) if False else reg("world", sh.levels() if sh.L0 != sh.L1 else [snap(sh.L0)])
    _, f1 = run_stage("elevation", BC.view_elev_task, [(k, v) for k, v in views.items()], min(nproc, 6))
    jobs = [(k, views[k], L) for k in views for L in sorted(need[k])]
    _, f2 = run_stage("levels", BC.level_task, jobs, min(nproc, int(os.environ.get("LEVEL_PROCS", 14))))
    _, f3 = run_stage("ice", BC.ice_task, [(k, views[k]) for k in views], max(2, nproc // 2))
    ok = [sh.id for sh in shots]
    res, f4 = run_stage("render", render_shot, [(s,) for s in ok], nproc)
    print("DONE", len(res), "shots in", round(time.time() - t0), "s; failures:", f1 + f2 + f3 + f4, flush=True)
    json.dump(dict(shots=[r for r in res], seconds=round(time.time() - t0), failures=[list(map(str, f)) for f in f1 + f2 + f3 + f4], procs=nproc), open(os.path.join(BC.OUT_DIR, "_bake_report.json"), "w"), indent=1)
