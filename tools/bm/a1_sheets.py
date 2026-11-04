"""Arnold #17 map agent (a1_): snapshots + ONE contact sheet per scene -> build/sheet-<scene>.jpg, then deletes the snapshots.
usage (from arnold/): python3 tools/ar3_sheets.py SCENE [ROUND]   frames = (scene seconds, what, sound) from tools/a1_frames.json"""
import glob, json, os, shutil, subprocess, sys
scene = sys.argv[1]; rnd = sys.argv[2] if len(sys.argv) > 2 else "1"
F = json.load(open("tools/a1_frames.json"))[scene]
T = json.loads(open(f"scenes/{scene}/timing.js").read().split("=", 1)[1].rstrip().rstrip(";")); A0 = T["abs_start"]
ts = ",".join(str(t) for t, _, _ in F)
r = subprocess.run(["hyperframes", "snapshot", ".", "--at", ts], cwd=f"scenes/{scene}", capture_output=True, text=True, timeout=1500)
if r.returncode: print(r.stdout[-1500:], r.stderr[-1500:])
D = sorted(glob.glob(f"scenes/{scene}/.hyperframes/artifacts/snapshots/*/"), key=os.path.getmtime)[-1]
os.makedirs(f"scenes/{scene}/snapshots", exist_ok=True)
for p in glob.glob(f"scenes/{scene}/snapshots/frame-*.png"): os.remove(p)
for p in glob.glob(D + "frame-*.png"): shutil.copy(p, f"scenes/{scene}/snapshots/")
mm = lambda t: f"{int((A0 + t) // 60)}:{(A0 + t) % 60:04.1f}"
spec = {"title": f"Arnold #17 {scene.upper()} ({' - '.join(T['paras'])}) - map agent a1_, round {rnd}, {T['duration']} s",
        "note": "STYLE_LOCK 1a + 1c + 2b/2c: nothing before it is spoken, one big card at a time, option 2 on close-ups, visible fire only",
        "frames": [[scene, t, mm(t), w, s] for t, w, s in F]}
os.makedirs("build", exist_ok=True); json.dump(spec, open(f"build/a1_sheet_{scene}.json", "w"), indent=1)
print(subprocess.run(["python3", "tools/make_sheet.py", f"build/a1_sheet_{scene}.json", f"build/sheet-{scene}.jpg"], capture_output=True, text=True).stdout)
if os.environ.get("KEEP") != "1":
    shutil.rmtree(f"scenes/{scene}/.hyperframes/artifacts", ignore_errors=True)
