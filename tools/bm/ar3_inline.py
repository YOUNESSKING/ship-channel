"""Arnold #17 map agent (prefix ar3_; scenes hook-a, hook-b, m3a, m3b): kit + data + body -> scenes-src/<scene>.js, then build_scene.py,
then the extra map layers (assets/ar3_<map>.jpg in the scene) + territory overlays, then checks every at(...) phrase against the narration.
usage (from arnold/): python3 tools/ar3_inline.py SCENE FIRST_TAG LAST_TAG
  kit = tools/gh_kit.js (Grant #16 hook kit, flags/legend/heads swapped for 1777) + tools/ar3_kit.js; body = tools/ar3_body_<SCENE>.js
  world = the saratoga map px (z15). Maps not baked yet (logs/<map>.done missing) fall back to the plain bake or a neutral placeholder."""
import json, math, os, re, shutil, subprocess, sys
from PIL import Image
scene, first, last = sys.argv[1:4]
MAPS = {"northeast": (43.8, -72.5, 8), "hudson": (43.0, -73.6, 10), "saratoga": (43.0, -73.635, 15), "quebec": (46.81, -71.21, 14), "valcour": (44.60, -73.42, 13)}
def origin(m):
    for f in (f"assets/{m}_hd_lift.json", f"assets/{m}.json"):
        if os.path.exists(f): J = json.load(open(f)); return [J["zoom"], *J["origin_world_px"]]
    lat, lon, z = MAPS[m]; n = 256 * 2 ** z; cx, cy = (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return [z, int(cx - 1440), int(cy - 810)]
GD = {"base": origin("saratoga"), "maps": {m: origin(m) for m in MAPS}}
kit = open("tools/gh_kit.js").read()
kit = kit.replace('const FL = { us: "assets/media/us34_flag.png", us35: "assets/media/us35_flag.png", csa: "assets/media/csa1_13_flag.png" };',
                  'const FL = { us: "assets/media/us_flag_13star.png", gb: "assets/media/gb_flag_1606.png" };')
kit = kit.replace("FL.csa", "FL.gb").replace('"UNION"], ["#be3a2a", "#bc2528", "CONFEDERACY"]', '"AMERICANS"], ["#be3a2a", "#bc2528", "BRITISH"]')
kit = kit.replace('headA: "UNION"', 'headA: "AMERICANS"').replace('headB: "CONFEDERATE"', 'headB: "BRITISH"')
kit = kit.replace("ring.style.overflow = \"visible\"; ring.appendChild(st);", "ring.style.overflow = \"visible\"; ring.appendChild(st); gsap.set(st, { autoAlpha: 0 });")
assert "gsap.set(st, { autoAlpha: 0 })" in kit
assert "FL.gb" in kit and "AMERICANS" in kit
body = open(f"tools/ar3_body_{scene}.js").read()
out = body.replace("// @@KIT", "// @@KIT (tools/gh_kit.js + tools/ar3_kit.js)\nconst GD = " + json.dumps(GD, separators=(",", ":")) + ";\n" + kit + open("tools/ar3_kit.js").read() + "// @@END-KIT")
open(f"scenes-src/{scene}.js", "w").write(out)
base = "saratoga_hd_lift" if os.path.exists("assets/saratoga_hd_lift.jpg") else "saratoga"
# build_scene.py, but without copying the (unused, ~250 MB) *_det_* tree/detail layers into the scene (disk space; trees are banned anyway)
SKIP_DET = "import shutil, sys; _c = shutil.copy; shutil.copy = lambda a, b, *k, **kw: None if '_det_' in str(a) else _c(a, b, *k, **kw); sys.argv = ['build_scene.py'] + sys.argv[1:]; exec(open('tools/build_scene.py').read(), {'__file__': 'tools/build_scene.py', '__name__': '__main__'})"
r = subprocess.run(["python3", "-c", SKIP_DET, scene, base, first, last] if True else ["python3", "tools/build_scene.py", scene, base, first, last], capture_output=True, text=True); print(r.stdout.strip(), r.stderr.strip()[-800:])
dst = f"scenes/{scene}/assets"
for m in MAPS:
    if f"ar3_{m}.jpg" not in body and f"mapGroup(\"{m}\"" not in body: continue
    for src in (f"assets/{m}_hd_lift.jpg", f"assets/{m}.jpg"):
        if os.path.exists(src):
            if not os.path.exists(f"logs/{m}.done"): print("NOTE", m, "not finished baking: rebuild later")
            shutil.copy(src, f"{dst}/ar3_{m}.jpg"); print("layer", m, "<-", src); break
    else:
        Image.new("RGB", (2880, 1620), (196, 184, 150)).save(f"{dst}/ar3_{m}.jpg", quality=80); print("layer", m, "PLACEHOLDER (not baked yet)")
for f in os.listdir("assets/media"):
    if f.startswith("ar3_ctl_") and f in body: shutil.copy(f"assets/media/{f}", f"{dst}/media/{f}")
t = json.loads(open(f"scenes/{scene}/timing.js").read().split("=", 1)[1].rstrip().rstrip(";"))
consts = dict(re.findall(r'\b(H\w*|P\w*)\s*=\s*"([\w-]+)"', body))
bad = 0
for mm in re.finditer(r'\bat\((\w+|"[\w-]+"),\s*"([^"]+)"', body):
    k = mm.group(1).strip('"'); k = consts.get(k, k)
    if k not in t["text"] or mm.group(2) not in t["text"][k]: print("MISSING PHRASE:", k, repr(mm.group(2))); bad += 1
print("phrases OK" if not bad else f"{bad} MISSING PHRASES")
