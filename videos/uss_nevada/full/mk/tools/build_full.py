"""Build one renderable HyperFrames map scene for the FULL Oriskany video.

usage: python3 tools/build_full.py SCENE [SCENE ...]     (SCENE = c02_bremerton etc., or 'all')
- The scene's time window comes from ../build/segments.json (kind 'map': t0_abs, dur); word timings from ../build/words.json.
- The basemap is named on the first line of scenes-src/SCENE.js:  // BASEMAP: gulf7
- Writes scenes/SCENE/ (index.html from tools/scene_template.html + lib/ship.js, assets, timing.js with SCENE_TIMING.words
  = [[word, t0, t1], ...] in scene seconds and SCENE_TIMING.map = the basemap projection json).
"""
import json, os, re, shutil, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FULL = os.path.join(ROOT, "..")
SEGS = [s for s in json.load(open(f"{FULL}/build/segments.json")) if s["kind"] == "map"]
WORDS = json.load(open(f"{FULL}/build/words.json"))
PAD = 0.1   # rendered a little longer than the shot (build_chapter trims / pads anyway)


def plan_segs():   # scenes RENDER_PLAN (step-1 commit) lists but the current shot lists dropped (c07_storm, c07_reefpin)
    import subprocess
    txt = subprocess.run(["git", "show", "15a5b66:videos/oriskany/full/build/segments.json"], cwd=FULL, capture_output=True, text=True).stdout
    return [s for s in json.loads(txt) if s["kind"] == "map"] if txt else []


def build(name):
    seg = next((s for s in SEGS if s["scene"] == name), None) or next(s for s in plan_segs() if s["scene"] == name)
    src = open(f"{ROOT}/scenes-src/{name}.js").read()
    basemap = re.match(r"//\s*BASEMAP:\s*(\w+)", src).group(1)
    t0, dur = seg["t0_abs"], round(seg["dur"] + PAD, 2)
    words = [[w["w"], round(w["start"] - t0, 3), round(w["end"] - t0, 3)] for w in WORDS if t0 - 1.0 <= w["start"] <= t0 + dur + 0.5]
    mp = json.load(open(f"{ROOT}/assets/{basemap}.json"))
    st = {"abs_start": t0, "duration": dur, "paras": {"s": [0, dur]}, "text": {"s": seg["narration"]}, "sents": {"s": []},
          "words": words, "map": mp, "file": seg["file"], "shows": seg["shows"]}
    out = f"{ROOT}/scenes/{name}"
    os.makedirs(f"{out}/assets/media", exist_ok=True)
    for d in ("lib", "vendor"):
        shutil.copytree(f"{ROOT}/{d}", f"{out}/{d}", dirs_exist_ok=True)
    shutil.copytree(f"{ROOT}/assets/fonts", f"{out}/assets/fonts", dirs_exist_ok=True)
    shutil.copy(f"{ROOT}/assets/grain.png", f"{out}/assets/grain.png")
    shutil.copy(f"{ROOT}/assets/{basemap}.jpg", f"{out}/assets/relief.jpg")
    for f in os.listdir(f"{ROOT}/assets/media"):
        shutil.copy(f"{ROOT}/assets/media/{f}", f"{out}/assets/media/{f}")
    geo = open(f"{ROOT}/assets/geo.json").read()
    open(f"{out}/timing.js", "w").write("window.SCENE_TIMING = " + json.dumps(st) + ";\nwindow.GEO = " + geo + ";\n")
    html = open(f"{ROOT}/tools/scene_template.html").read()
    html = html.replace("{{DURATION}}", str(dur)).replace("{{CREDIT}}", mp["credit"]).replace("{{SCENE_JS}}", src)
    open(f"{out}/index.html", "w").write(html)
    shutil.copy(f"{ROOT}/tools/hyperframes.json", f"{out}/hyperframes.json")
    json.dump({"id": name, "name": name, "createdAt": "2026-11-04T00:00:00.000Z"}, open(f"{out}/meta.json", "w"))
    print(f"{name}: {dur}s  basemap {basemap}  abs {t0:.2f}  -> {seg['file']}")


if __name__ == "__main__":
    names = sys.argv[1:]
    if names == ["all"]:
        names = [s["scene"] for s in SEGS] + [s["scene"] for s in plan_segs() if s["scene"] not in {q["scene"] for q in SEGS}]
    for n in names:
        build(n)
