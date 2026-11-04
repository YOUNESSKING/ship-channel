"""map agent va: check the probe of a scene (tools/va_probe.js) for flag problems.
usage: python3 tools/va_flagcheck.py SCENE BASEMAP   (BASEMAP = champlain|valcour|champsouth: the scene's world px system)
Reports per time span: a nation without a fully visible flag, a flag off its land (DEM <= 29.8 m = the lake), a flag under a HUD element, a flag on a boat/label."""
import json, math, sys
import numpy as np
scene, base = sys.argv[1:3]
SP = "/tmp/claude-0/-home-user-battle-maps/ea403ef6-3b59-5ee8-9889-dab5cb0fb2ba/scratchpad"
D = json.load(open(f"{SP}/probe_{scene}.json"))
maps = {}
for m in ("valcour", "champsouth", "champlain"):
    J = json.load(open(f"assets/{m}_hd_lift.json")); e = np.load(f"assets/src/{m}_hd_elev.npy"); maps[m] = (J["zoom"], J["origin_world_px"], e)
z0, o0, _ = maps[base]
def land(x, y):
    wx, wy = (o0[0] + x) / 2 ** z0, (o0[1] + y) / 2 ** z0          # world px at z0 -> z=0
    for m in ("valcour", "champsouth", "champlain"):
        z, o, e = maps[m]; px, py = wx * 2 ** z - o[0], wy * 2 ** z - o[1]
        if 0 <= px < 2880 and 0 <= py < 1620:
            H, W = e.shape; v = e[int(py * H / 1620), int(px * W / 2880)]
            return v > 29.8
    return None
def ov(a, b, pad=0): return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad
issues = []
for f in D:
    t = f["t"]
    for k in ("us", "gb"):
        ok = [g for g in f["flags"] if g["k"] == k and g["op"] > 0.6 and g["r"][0] >= 6 and g["r"][1] >= 6 and g["r"][2] <= 1914 and g["r"][3] <= 1074]
        if not ok: issues.append((t, f"NO FULL {k} FLAG " + ";".join(f"{g['r']} op{g['op']}" for g in f["flags"] if g["k"] == k)))
    for g in f["flags"]:
        if g["op"] < 0.3: continue
        if land(g["x"], g["y"]) is False: issues.append((t, f"{g['k']} flag on WATER at {g['x']},{g['y']}"))
        r = g["r"]
        if r[0] < 6 or r[1] < 6 or r[2] > 1914 or r[3] > 1074:
            if r[2] > 0 and r[0] < 1920 and r[3] > 0 and r[1] < 1080: issues.append((t, f"{g['k']} flag CUT by edge {r}"))
        for h in f["hud"]:
            if ov(r, h["r"], 6): issues.append((t, f"{g['k']} flag under HUD {h['n']!r} {h['r']}"))
        for p in f["pins"]:
            if ov(r, p["r"], 2): issues.append((t, f"{g['k']} flag on pin {p['n']!r}"))
# compress runs of the same message
last = {}
for t, m in issues:
    key = m.split(" at ")[0].split(" [")[0].split(" op")[0]
    if key in last and t - last[key][1] <= 0.6: last[key][1] = t
    else:
        if key in last: print(f"{last[key][0]:6.2f}-{last[key][1]:6.2f}  {last[key][2]}")
        last[key] = [t, t, m]
for a, b, m in last.values(): print(f"{a:6.2f}-{b:6.2f}  {m}")
print("frames", len(D), "issues", len(issues))
