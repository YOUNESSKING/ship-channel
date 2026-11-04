"""Move-3 agent builder: scenes-src/<scene>.js = tools/m1_kit.js (35-star flag) + tools/m3_kitx.js + tools/m3_body_<scene>.js, then
tools/build_scene.py, extra basemaps for the scene (copied as assets/ext_<map>.jpg), then checks every at(...) phrase.
Uses <map>_hd_lift when its bake is done (logs/<map>.done), else the quick preview bake (m3x_ric / ghx_jam / m3x_pet / m3x_mis).
usage: python3 tools/m3_build.py SCENE MAP FIRST LAST [EXTRA_MAP ...]"""
import json, os, re, shutil, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PREV = {"richmond": "m3x_ric", "petersburg": "m3x_pet", "jamesriver": "ghx_jam", "mississippi": "m3x_mis"}
def base(m):
    # the v11 bake (logs/<m>.done) when finished; else the plain LIFT hd bake if present; else the quick preview (same projection)
    return f"{m}_hd_lift" if os.path.exists(f"{ROOT}/assets/{m}_hd_lift.jpg") and os.path.exists(f"{ROOT}/assets/{m}_hd_lift.json") else PREV[m]
name, mp, first, last = sys.argv[1:5]; extra = sys.argv[5:]
paras = [p["tag"].split("|")[0].replace("MAP:", "").strip() for p in json.load(open(f"{ROOT}/audio/timing.json"))["paragraphs"]]
if last not in paras: last = first      # e.g. "end-2" before the ending is re-voiced
kit = open(f"{ROOT}/tools/m1_kit.js").read().replace("us34_flag.png", "us35_flag.png").replace("US 34-star (Feb 1862)", "US 35-star (June 1864)")
kx = open(f"{ROOT}/tools/m3_kitx.js").read(); body = open(f"{ROOT}/tools/m3_body_{name}.js").read()
hdr = body.split("\n// @@BODY", 1)[0] if "// @@BODY" in body else ""
B = base(mp)
sys.path.insert(0, f"{ROOT}/tools"); import m3_geo
src = hdr + f"\nwindow.M3_BASE = {json.dumps(B)};\n" + m3_geo.js() + kit + kx + body.split("// @@BODY", 1)[-1]
open(f"{ROOT}/scenes-src/{name}.js", "w").write(src)
subprocess.run([sys.executable, f"{ROOT}/tools/build_scene.py", name, B, first, last], check=True, cwd=ROOT)
for m in extra:
    shutil.copy(f"{ROOT}/assets/{base(m)}.jpg", f"{ROOT}/scenes/{name}/assets/ext_{m}.jpg"); print("extra map", m, "<-", base(m))
t = json.loads(open(f"{ROOT}/scenes/{name}/timing.js").read().split("=", 1)[1].rstrip().rstrip(";"))
consts = dict(re.findall(r'\b(P\w*)\s*=\s*"([\w-]+)"', body))
bad = 0
for m in re.finditer(r'\bat\((\w+|"[\w-]+"),\s*"([^"]+)"', body):
    k = m.group(1).strip('"'); k = consts.get(k, k)
    if k not in t["text"] or m.group(2) not in t["text"][k]: print("MISSING PHRASE:", k, repr(m.group(2))); bad += 1
for m in re.finditer(r'\batAny\("([^"]+)"', body):
    if not any(m.group(1) in v for v in t["text"].values()): print("not (yet) spoken, skipped in the scene:", repr(m.group(1)))
print("basemap", B, "|", "phrases OK" if not bad else f"{bad} missing phrases")
