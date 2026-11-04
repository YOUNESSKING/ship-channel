"""map agent va: place the two period flags for a scene from its probe (tools/va_probe.js SCENE 0.25).
usage: python3 tools/va_flagsolve.py SCENE BASEMAP NATION REGION [T0 T1] [PREF_X PREF_Y]
  NATION us|gb; REGION = python expression in lat, lon, x, y (world px of BASEMAP) that is True on that nation's ground.
Finds flag positions (on land: >= 40 screen px from the water, inside the frame, clear of every HUD box, card and map pin)
that stay valid as long as possible; prints the flagS() lines (crossfade 0.5 s at each switch)."""
import json, math, sys
import numpy as np
from scipy import ndimage
scene, base, nat, region = sys.argv[1:5]
T0 = float(sys.argv[5]) if len(sys.argv) > 5 else 0; T1 = float(sys.argv[6]) if len(sys.argv) > 6 else 1e9
PREF = (float(sys.argv[7]), float(sys.argv[8])) if len(sys.argv) > 8 else None
SP = "/tmp/claude-0/-home-user-battle-maps/ea403ef6-3b59-5ee8-9889-dab5cb0fb2ba/scratchpad"
D = [f for f in json.load(open(f"{SP}/probe_{scene}.json")) if T0 - 1e-6 <= f["t"] <= T1 + 1e-6]
J = json.load(open(f"assets/{base}_hd_lift.json")); z = J["zoom"]; ox, oy = J["origin_world_px"]; n = 256 * 2 ** z
# land + distance to water in world px, on the scene's own map, extended with the coarser maps (for the m2d zoom-out)
def landdist(m):
    e = np.load(f"assets/src/{m}_hd_elev.npy"); H, W = e.shape; land = e > 29.8
    d = ndimage.distance_transform_edt(land) * (2880 / W); return d, H, W
LD = {m: landdist(m) for m in ("valcour", "champsouth", "champlain")}
MJ = {m: json.load(open(f"assets/{m}_hd_lift.json")) for m in LD}
def dist(x, y):   # distance to water (base world px) at base world (x, y)
    wx, wy = (ox + x) / 2 ** z, (oy + y) / 2 ** z
    for m in ("valcour", "champsouth", "champlain"):
        if 2 ** MJ[m]["zoom"] < 2 ** z / 1.01 and m != base and False: pass
        zz = MJ[m]["zoom"]; px, py = wx * 2 ** zz - MJ[m]["origin_world_px"][0], wy * 2 ** zz - MJ[m]["origin_world_px"][1]
        if MJ[m]["zoom"] >= z and 0 <= px < 2880 and 0 <= py < 1620:
            d, H, W = LD[m]; return d[int(py * H / 1620), int(px * W / 2880)] * 2 ** (z - zz)
    for m in ("champlain",):
        zz = MJ[m]["zoom"]; px, py = wx * 2 ** zz - MJ[m]["origin_world_px"][0], wy * 2 ** zz - MJ[m]["origin_world_px"][1]
        if 0 <= px < 2880 and 0 <= py < 1620:
            d, H, W = LD[m]; return d[int(py * H / 1620), int(px * W / 2880)] * 2 ** (z - zz)
    return 0
xs = [f["cam"] for f in D]
lo_x = min((0 - c[1]) / c[0] for c in xs); hi_x = max((1920 - c[1]) / c[0] for c in xs)
lo_y = min((0 - c[2]) / c[0] for c in xs); hi_y = max((1080 - c[2]) / c[0] for c in xs)
step = max(4, (hi_x - lo_x) / 260)
C = []
for y in np.arange(lo_y, hi_y, step):
    for x in np.arange(lo_x, hi_x, step):
        lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (oy + y) / n)))); lon = (ox + x) / n * 360 - 180
        if not eval(region): continue
        dd = dist(x, y)
        if dd > 2: C.append((x, y, dd))
C = np.array(C); print("candidates", len(C), file=sys.stderr)
FW, FH, PAD = 112, 70, 8
valid = np.zeros((len(D), len(C)), bool); marg = np.zeros((len(D), len(C)))
for i, f in enumerate(D):
    s, ex, ey = f["cam"][0], f["cam"][1], f["cam"][2]
    sx, sy = ex + s * C[:, 0], ey + s * C[:, 1]
    x0, y0, x1, y1 = sx - FW / 2, sy - FH / 2, sx + FW / 2, sy + FH / 2
    ok = (x0 >= 12) & (y0 >= 12) & (x1 <= 1908) & (y1 <= 1068) & (C[:, 2] * s >= 40)
    m = np.minimum.reduce([x0 - 12, y0 - 12, 1908 - x1, 1068 - y1])
    for b in [h["r"] for h in f["hud"]] + [p["r"] for p in f["pins"]]:
        hit = (x0 < b[2] + PAD) & (b[0] - PAD < x1) & (y0 < b[3] + PAD) & (b[1] - PAD < y1); ok &= ~hit
        dx = np.maximum(b[0] - x1, x0 - b[2]); dy = np.maximum(b[1] - y1, y0 - b[3]); m = np.minimum(m, np.maximum(dx, dy))
    valid[i] = ok; marg[i] = m
# greedy: from frame i, the candidate valid for the longest run (ties: bigger worst margin, nearer PREF)
i, out = 0, []
while i < len(D):
    run = np.zeros(len(C), int); alive = np.ones(len(C), bool)
    for j in range(i, len(D)):
        alive &= valid[j]; run += alive
        if not alive.any(): break
    if run.max() == 0: print(f"NO VALID POSITION at t={D[i]['t']}", file=sys.stderr); i += 1; continue
    best = np.where(run == run.max())[0]
    mm = np.array([marg[i:i + run.max(), k].min() for k in best])
    score = np.minimum(mm, 80) - (np.hypot(C[best, 0] - PREF[0], C[best, 1] - PREF[1]) * 0.05 if PREF else 0)
    k = best[np.argmax(score)]; out.append((D[i]["t"], D[i + run.max() - 1]["t"], C[k]))
    i += run.max()
src = "FL.us" if nat == "us" else "FL.cs"
for a, (t0, t1, c) in enumerate(out):
    tin = "0" if a == 0 and t0 <= T0 + 0.01 and T0 == 0 else f"{t0:.2f} - 0.25"
    tout = "END + 1" if a == len(out) - 1 and t1 >= D[-1]["t"] - 0.01 else f"{t1:.2f} + 0.25"
    print(f'flagS({src}, "", {c[0]:.0f}, {c[1]:.0f}, {tin}, {tout});   // {t0:.2f}-{t1:.2f} s, {c[2]:.0f} px from the water')
