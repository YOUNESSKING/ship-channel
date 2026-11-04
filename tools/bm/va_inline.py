"""Map agent va (Arnold #17, m2a-m2d Valcour): kit + data + body -> scenes-src/<scene>.js, then build the scene.
usage (from grant/): python3 tools/vk_inline.py SCENE BASEMAP FIRST_TAG LAST_TAG
  reads tools/va_kit.js and tools/va_body_<SCENE>.js; GD.base = the scene map's json (zoom, origin, m/px);
  GD.maps[<map>] = json of every other baked map (for the extra map layer of a continuous zoom, e.g. mississippi inside vicksburg)."""
import json, os, subprocess, sys, glob
scene, base, first, last = sys.argv[1:5]
m0 = base.replace("_hd_lift", "")
GD = {"base": m0, "maps": {}}
for f in glob.glob("assets/*_hd_lift.json"):
    J = json.load(open(f)); GD["maps"][J["name"].replace("_hd_lift", "")] = {k: J[k] for k in ("zoom", "origin_world_px", "meters_per_px")}
# maps not baked yet: the same origin bake.py will give (centre - half the 2880x1620 frame), from tools/bake_all.sh
import math, re
for m, la, lo, z in re.findall(r"^bake (\w+) ([-\d.]+) ([-\d.]+) (\d+)", open("tools/bake_all.sh").read(), re.M):
    if m in GD["maps"]: continue
    la, lo, z = float(la), float(lo), int(z); n = 256 * 2 ** z
    x = (lo + 180) / 360 * n; y = (1 - math.asinh(math.tan(math.radians(la))) / math.pi) / 2 * n
    GD["maps"][m] = {"zoom": z, "origin_world_px": [int(x - 1440), int(y - 810)], "meters_per_px": 156543.03 * math.cos(math.radians(la)) / 2 ** z, "est": True}
# m2d: the champlain map embedded in champsouth (refresh the downscaled copy whenever the champlain bake is newer)
if scene == "m2d":
    src, dst = "assets/champlain_hd_lift.jpg", "assets/media/va_champlain_relief.jpg"
    if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
        from PIL import Image; Image.open(src).resize((2880, 1620), Image.LANCZOS).save(dst, quality=88)
        subprocess.run(["python3", "tools/va_make_control.py", "champlain"])
kit = open("tools/va_kit.js").read()
body = open(f"tools/va_body_{scene}.js").read()
out = body.replace("// @@KIT", "// @@KIT (tools/va_kit.js)\n" + kit + "// @@END-KIT").replace("// @@DATA", "// @@DATA (tools/vk_inline.py)\nconst GD = " + json.dumps(GD, separators=(",", ":")) + ";\n// @@END-DATA")
open(f"scenes-src/{scene}.js", "w").write(out)
print(f"scenes-src/{scene}.js", len(out) // 1024, "KB")
r = subprocess.run(["python3", "tools/build_scene.py", scene, base, first, last], capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip()[-800:])
# phrase check: every at(P, "...") of the body must be in the paragraph text (case-sensitive)
import re
t = json.loads(open(f"scenes/{scene}/timing.js").read().split("=", 1)[1].rstrip().rstrip(";"))
consts = dict(re.findall(r'\b(P\w*)\s*=\s*"([\w-]+)"', body)); bad = 0
for m in re.finditer(r'\bat\((\w+|"[\w-]+"),\s*"([^"]+)"', body):
    k = m.group(1).strip('"'); k = consts.get(k, k)
    if k not in t["text"] or m.group(2) not in t["text"][k]: print("MISSING PHRASE:", k, repr(m.group(2))); bad += 1
print("phrases OK" if not bad else f"{bad} MISSING PHRASES")
if m0 in ("valcour", "champlain"): print(subprocess.run(["python3", "tools/va_tmp_islands.py", m0, scene], capture_output=True, text=True).stdout.strip())
