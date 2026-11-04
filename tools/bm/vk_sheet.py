"""Map agent vk: snapshot a built scene at the given times and assemble ONE labelled contact sheet (tools/make_sheet.py).
usage (from grant/): python3 tools/vk_sheet.py SCENE SPEC.json   (SPEC = {"title","note","frames":[[t, "what", "sound"], ...]}) -> build/sheet-SCENE.jpg"""
import glob, json, os, shutil, subprocess, sys
scene, spec = sys.argv[1], json.load(open(sys.argv[2]))
T = json.load(open("audio/timing.json")); start = None
tjs = open(f"scenes/{scene}/timing.js").read(); st = json.loads(tjs[tjs.index("=") + 1:].strip().rstrip(";"))["abs_start"]
ts = [f[0] for f in spec["frames"]]
r = subprocess.run(["hyperframes", "snapshot", ".", "--at", ",".join(str(t) for t in ts)], cwd=f"scenes/{scene}", capture_output=True, text=True)
d = max(glob.glob(f"scenes/{scene}/.hyperframes/artifacts/snapshots/*/"), key=os.path.getmtime)
os.makedirs(f"scenes/{scene}/snapshots", exist_ok=True)
for f in glob.glob(f"scenes/{scene}/snapshots/frame-*.png"): os.remove(f)
for f in glob.glob(d + "frame-*.png"): shutil.copy(f, f"scenes/{scene}/snapshots/")
fr = []
for t, what, snd in spec["frames"]:
    a = st + t; fr.append([scene, t, f"{int(a // 60)}:{int(a % 60):02d}", what, snd])
json.dump({"title": spec["title"], "note": spec["note"], "frames": fr}, open(f"build/vk_spec_{scene}.json", "w"))
os.makedirs("build", exist_ok=True)
print(subprocess.run(["python3", "tools/make_sheet.py", f"build/vk_spec_{scene}.json", f"build/sheet-{scene}.jpg"], capture_output=True, text=True).stdout)
