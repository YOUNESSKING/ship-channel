"""Generic contact sheet: python3 tools/quick_sheet.py SCENE [STEP_S]  -> build/sheet-SCENE.jpg (a frame every STEP_S s, default 4)."""
import glob, json, os, shutil, subprocess, sys
from PIL import Image, ImageDraw
scene = sys.argv[1]; step = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
tj = open(f"scenes/{scene}/timing.js").read(); dur = json.loads(tj[tj.index("=") + 1:].strip().rstrip(";")).get("duration")
if not dur:
    T = json.load(open("audio/timing.json"))
    dur = 60
ts = [round(i * step, 1) for i in range(int(dur / step))] if dur else [0, 5, 10]
subprocess.run(["hyperframes", "snapshot", ".", "--at", ",".join(map(str, ts))], cwd=f"scenes/{scene}", capture_output=True, text=True)
d = max(glob.glob(f"scenes/{scene}/.hyperframes/artifacts/snapshots/*/"), key=os.path.getmtime)
fs = sorted(glob.glob(d + "frame-*.png")); W, H, C = 640, 360, 3
rows = (len(fs) + C - 1) // C; sheet = Image.new("RGB", (W * C, (H + 18) * rows), (20, 20, 20)); dr = ImageDraw.Draw(sheet)
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB").resize((W, H)); x, y = (i % C) * W, (i // C) * (H + 18)
    sheet.paste(im, (x, y + 18)); dr.text((x + 4, y + 3), f"{scene} {ts[i] if i < len(ts) else ''}s", fill=(255, 220, 120))
sheet.save(f"build/sheet-{scene}.jpg", quality=85); shutil.rmtree(f"scenes/{scene}/.hyperframes", ignore_errors=True); print(scene, len(fs))
