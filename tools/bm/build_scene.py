"""Assemble a renderable HyperFrames project for one map scene.

usage: python3 build_scene.py SCENE_NAME BASEMAP FIRST_TAG LAST_TAG
Takes the narration paragraphs FIRST_TAG..LAST_TAG from audio/timing.json, and writes
scenes/SCENE_NAME/ with index.html (from scenes-src/SCENE_NAME.js), the engine, assets and timing.js.
The scene runs from the start of FIRST_TAG to the start of the paragraph after LAST_TAG.
"""
import json, os, shutil, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
name, basemap, first, last = sys.argv[1:5]
timing = json.load(open(f"{ROOT}/audio/timing.json"))
paras = timing["paragraphs"]
key = lambda p: p["tag"].split("|")[0].replace("MAP:", "").strip()
i0 = next(i for i, p in enumerate(paras) if key(p) == first)
i1 = next(i for i, p in enumerate(paras) if key(p) == last)
t0 = paras[i0]["start"]
t_end = paras[i1 + 1]["start"] if i1 + 1 < len(paras) else timing["duration"]
dur = round(t_end - t0, 2)
scene_t = {"abs_start": t0, "duration": dur,
           "paras": {key(p): [round(p["start"] - t0, 2), round(p["end"] - t0, 2)] for p in paras[i0:i1 + 1]},
           "text": {key(p): p["text"] for p in paras[i0:i1 + 1]}}

out = f"{ROOT}/scenes/{name}"
os.makedirs(f"{out}/assets", exist_ok=True)
for d in ("lib", "vendor"):
    shutil.copytree(f"{ROOT}/{d}", f"{out}/{d}", dirs_exist_ok=True)
shutil.copytree(f"{ROOT}/assets/fonts", f"{out}/assets/fonts", dirs_exist_ok=True)
shutil.copy(f"{ROOT}/assets/grain.png", f"{out}/assets/grain.png")
shutil.copy(f"{ROOT}/assets/{basemap}.jpg", f"{out}/assets/relief.jpg")
# map overlays (assets/*.png) and photo media (assets/media/*.png|jpg|webp), referenced as assets/NAME and assets/media/NAME
for f in os.listdir(f"{ROOT}/assets"):
    if f.endswith(".png") and f != "grain.png":
        shutil.copy(f"{ROOT}/assets/{f}", f"{out}/assets/{f}")
if os.path.isdir(f"{ROOT}/assets/media"):
    os.makedirs(f"{out}/assets/media", exist_ok=True)
    for f in os.listdir(f"{ROOT}/assets/media"):
        if os.path.isfile(f"{ROOT}/assets/media/{f}") and f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            shutil.copy(f"{ROOT}/assets/media/{f}", f"{out}/assets/media/{f}")
open(f"{out}/timing.js", "w").write("window.SCENE_TIMING = " + json.dumps(scene_t) + ";\n")
credit = json.load(open(f"{ROOT}/assets/{basemap}.json"))["credit"]
html = open(f"{ROOT}/tools/scene_template.html").read()
html = html.replace("{{DURATION}}", str(dur)).replace("{{CREDIT}}", credit).replace("{{SCENE_JS}}", open(f"{ROOT}/scenes-src/{name}.js").read())
open(f"{out}/index.html", "w").write(html)
for f in ("hyperframes.json",):
    shutil.copy(f"/home/user/battle-maps/chipyongni/{f}", f"{out}/{f}")
json.dump({"id": name, "name": name, "createdAt": "2026-09-25T00:00:00.000Z"}, open(f"{out}/meta.json", "w"))
print(f"{name}: {dur}s  (abs {t0}-{t_end})  paras: {list(scene_t['paras'])}")
