"""Map agent (Grant #16, m2a-m2d Vicksburg): kit + data + body -> scenes-src/<scene>.js, then build the scene.
usage (from grant/): python3 tools/vk_inline.py SCENE BASEMAP FIRST_TAG LAST_TAG
  reads tools/vk_kit.js and tools/vk_body_<SCENE>.js; GD.base = the scene map's json (zoom, origin, m/px);
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
kit = open("tools/vk_kit.js").read()
body = open(f"tools/vk_body_{scene}.js").read()
out = body.replace("// @@KIT", "// @@KIT (tools/vk_kit.js)\n" + kit + "// @@END-KIT").replace("// @@DATA", "// @@DATA (tools/vk_inline.py)\nconst GD = " + json.dumps(GD, separators=(",", ":")) + ";\n// @@END-DATA")
open(f"scenes-src/{scene}.js", "w").write(out)
print(f"scenes-src/{scene}.js", len(out) // 1024, "KB")
r = subprocess.run(["python3", "tools/build_scene.py", scene, base, first, last], capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip()[-800:])
