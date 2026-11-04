"""Move-1 agent builder: scenes-src/<scene>.js = tools/m1_kit.js + tools/m1_body_<scene>.js, then tools/build_scene.py,
then checks every at(...) phrase against the paragraph text.  usage: python3 tools/m1_build.py SCENE BASEMAP FIRST LAST"""
import json, os, re, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
name, base, first, last = sys.argv[1:5]
kit = open(f"{ROOT}/tools/m1_kit.js").read(); body = open(f"{ROOT}/tools/m1_body_{name}.js").read()
hdr = body.split("\n// @@BODY", 1)[0] if "// @@BODY" in body else ""
src = hdr + "\n" + kit + body.split("// @@BODY", 1)[-1]
open(f"{ROOT}/scenes-src/{name}.js", "w").write(src)
subprocess.run([sys.executable, f"{ROOT}/tools/build_scene.py", name, base, first, last], check=True, cwd=ROOT)
t = json.loads(open(f"{ROOT}/scenes/{name}/timing.js").read().split("=", 1)[1].rstrip().rstrip(";"))
consts = dict(re.findall(r'\b(P\w*)\s*=\s*"([\w-]+)"', body))
bad = 0
for m in re.finditer(r'\bat\((\w+|"[\w-]+"),\s*"([^"]+)"', body):
    k = m.group(1).strip('"'); k = consts.get(k, k)
    if k not in t["text"] or m.group(2) not in t["text"][k]: print("MISSING PHRASE:", k, repr(m.group(2))); bad += 1
print("phrases OK" if not bad else f"{bad} missing phrases")
