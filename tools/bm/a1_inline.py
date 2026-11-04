"""Arnold #17 map agent a1_ (scenes m1a, m1b, ending): kit + data + body -> scenes-src/<scene>.js, build_scene.py, extra map layers
(assets/a1_<map>.jpg in the scene), then checks every at(...) phrase against the narration.
usage (from arnold/): python3 tools/a1_inline.py SCENE FIRST_TAG LAST_TAG BASEMAP
  kit = tools/gh_kit.js (flags/legend swapped) + tools/ar3_kit.js (multi-map camera, cards) + tools/a1_kit.js; body = tools/a1_body_<SCENE>.js
  world = the BASEMAP px. FL.us = Continental Colours (1775-76) except the ending (13-star flag, 1777)."""
import json, math, os, re, shutil, subprocess, sys
scene, first, last, basem = sys.argv[1:5]
MAPS = ["northeast", "maine", "quebec", "saratoga", "valcour", "champlain"]
def origin(m):
    J = json.load(open(f"assets/{m}_hd_lift.json")); return [J["zoom"], *J["origin_world_px"]]
GD = {"base": origin(basem), "maps": {m: origin(m) for m in MAPS if os.path.exists(f"assets/{m}_hd_lift.json")}}
us = "assets/media/us_flag_13star.png" if scene == "ending" else "assets/media/continental_colours.png"
kit = open("tools/gh_kit.js").read()
kit = kit.replace('const FL = { us: "assets/media/us34_flag.png", us35: "assets/media/us35_flag.png", csa: "assets/media/csa1_13_flag.png" };',
                  f'const FL = {{ us: "{us}", gb: "assets/media/gb_flag_1606.png" }};')
kit = kit.replace("FL.csa", "FL.gb").replace('"UNION"], ["#be3a2a", "#bc2528", "CONFEDERACY"]', '"AMERICANS"], ["#be3a2a", "#bc2528", "BRITISH"]')
kit = kit.replace('headA: "UNION"', 'headA: "AMERICANS"').replace('headB: "CONFEDERATE"', 'headB: "BRITISH"')
kit = kit.replace("ring.style.overflow = \"visible\"; ring.appendChild(st);", "ring.style.overflow = \"visible\"; ring.appendChild(st); gsap.set(st, { autoAlpha: 0 });")
assert "FL.gb" in kit and "AMERICANS" in kit and us in kit
k3 = open("tools/ar3_kit.js").read().replace("assets/ar3_${name}.jpg", "assets/a1_${name}.jpg")
body = open(f"tools/a1_body_{scene}.js").read()
out = body.replace("// @@KIT", "// @@KIT (tools/gh_kit.js + tools/ar3_kit.js + tools/a1_kit.js)\nconst GD = " + json.dumps(GD, separators=(",", ":")) + ";\n" + kit + k3 + open("tools/a1_kit.js").read() + "// @@END-KIT")
open(f"scenes-src/{scene}.js", "w").write(out)
# build_scene.py, but without copying the (unused, ~250 MB) *_det_* tree/detail layers into the scene (disk space; trees are banned anyway)
SKIP_DET = "import shutil, sys; _c = shutil.copy; shutil.copy = lambda a, b, *k, **kw: None if '_det_' in str(a) else _c(a, b, *k, **kw); sys.argv = ['build_scene.py'] + sys.argv[1:]; exec(open('tools/build_scene.py').read(), {'__file__': 'tools/build_scene.py', '__name__': '__main__'})"
r = subprocess.run(["python3", "-c", SKIP_DET, scene, f"{basem}_hd_lift", first, last] if scene == "ending" else ["python3", "tools/build_scene.py", scene, f"{basem}_hd_lift", first, last], capture_output=True, text=True); print(r.stdout.strip(), r.stderr.strip()[-800:])
dst = f"scenes/{scene}/assets"
for m in MAPS:
    if f'mapTop("{m}"' in body or f'mapGroup("{m}"' in body:
        shutil.copy(f"assets/{m}_hd_lift.jpg", f"{dst}/a1_{m}.jpg"); print("layer", m, "" if os.path.exists(f"logs/{m}_p2.done") else "(pass-2 bake not finished: rebuild later)")
if not os.path.exists(f"logs/{basem}_p2.done"): print("NOTE base", basem, "pass-2 bake not finished: rebuild later")
t = json.loads(open(f"scenes/{scene}/timing.js").read().split("=", 1)[1].rstrip().rstrip(";"))
consts = dict(re.findall(r'\b(P\w*)\s*=\s*"([\w-]+)"', body))
bad = 0
for mm in re.finditer(r'\bat\((\w+|"[\w-]+"),\s*"([^"]+)"', body):
    k = mm.group(1).strip('"'); k = consts.get(k, k)
    if k not in t["text"] or mm.group(2) not in t["text"][k]: print("MISSING PHRASE:", k, repr(mm.group(2))); bad += 1
print("phrases OK" if not bad else f"{bad} MISSING PHRASES")
