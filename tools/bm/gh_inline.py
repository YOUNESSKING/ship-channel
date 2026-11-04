"""Map agent hook (Grant #16, prefix gh_): kit + data + body -> scenes-src/<scene>.js, copies the extra map layers into assets/media,
then builds the scene with build_scene.py.  usage (from grant/): python3 tools/gh_inline.py SCENE BASEMAP FIRST_TAG LAST_TAG
  reads tools/gh_kit.js and tools/gh_body_<SCENE>.js; GD.riv = traced rivers (tools/gh_rivers.py) of the tennessee map (map px).
  Extra layers (copied when present): gh_ten_relief.jpg (tennessee), gh_hen_relief.jpg (henry), gh_vks_relief.jpg (vicksburg_siege),
  gh_jam_relief.jpg (jamesriver); a missing map falls back to its plain bake (assets/<map>.jpg) or a neutral placeholder."""
import json, os, shutil, subprocess, sys
from PIL import Image
scene, base, first, last = sys.argv[1:5]
LAY = {"gh_ten_relief.jpg": "tennessee", "gh_hen_relief.jpg": "henry", "gh_vks_relief.jpg": "vicksburg_siege", "gh_jam_relief.jpg": "jamesriver"}
QUICK = {"vicksburg_siege": "ghx_vks", "jamesriver": "ghx_jam"}   # quick plain bakes (tools/bake.py ghx_...) used until the v11 map exists
for out, m in LAY.items():
    dst = f"assets/media/{out}"
    for src in (f"assets/{m}_hd_lift.jpg", f"assets/{m}.jpg", f"assets/{QUICK.get(m, m)}.jpg"):
        if os.path.exists(src):
            if not os.path.exists(f"logs/{m}.done"): print("NOTE", m, "not finished baking (v11 look may be missing): rebuild later")
            if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                shutil.copy(src, dst); print("layer", out, "<-", src)
            break
    else:
        if not os.path.exists(dst): Image.new("RGB", (2880, 1620), (196, 184, 150)).save(dst, quality=80); print("layer", out, "PLACEHOLDER (map not baked yet)")
import math
def origin(m, lat, lon, z):
    if os.path.exists(f"assets/{m}_hd_lift.json"): J = json.load(open(f"assets/{m}_hd_lift.json")); return [J["zoom"], *J["origin_world_px"]]
    n = 256 * 2 ** z; cx, cy = (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return [z, int(cx - 1440), int(cy - 810)]
GD = {"riv": json.load(open("assets/media/gh_tennessee_rivers.json")),
      "maps": {"vicksburg_siege": origin("vicksburg_siege", 32.33, -90.87, 12), "jamesriver": origin("jamesriver", 37.3, -77.05, 12)}}
kit = open("tools/gh_kit.js").read()
body = open(f"tools/gh_body_{scene}.js").read()
out = body.replace("// @@KIT", "// @@KIT (tools/gh_kit.js)\n" + kit + "// @@END-KIT").replace("// @@DATA", "// @@DATA (tools/gh_inline.py)\nconst GD = " + json.dumps(GD, separators=(",", ":")) + ";\n// @@END-DATA")
open(f"scenes-src/{scene}.js", "w").write(out)
print(f"scenes-src/{scene}.js", len(out) // 1024, "KB")
r = subprocess.run(["python3", "tools/build_scene.py", scene, base, first, last], capture_output=True, text=True); print(r.stdout.strip(), r.stderr.strip()[-800:])
