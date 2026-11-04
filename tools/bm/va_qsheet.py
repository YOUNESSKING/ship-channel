"""map agent va: low-disk contact sheet. python3 tools/va_qsheet.py SCENE STEP [EXTRA_T,...] -> build/sheet-SCENE.jpg
Snapshots in batches of 6 frames and deletes them right away (the disk is nearly full while other agents render)."""
import glob, json, os, shutil, subprocess, sys
from PIL import Image, ImageDraw
scene = sys.argv[1]; step = float(sys.argv[2])
tj = open(f"scenes/{scene}/timing.js").read(); dur = json.loads(tj[tj.index("=") + 1:].strip().rstrip(";"))["duration"]
ts = [round(i * step, 2) for i in range(int(dur / step) + 1) if i * step < dur - 0.05]
if len(sys.argv) > 3: ts = sorted(set(ts + [float(x) for x in sys.argv[3].split(",")]))
W, H, C = 640, 360, 3; thumbs = []
hf = f"scenes/{scene}/.hyperframes"
for k in range(0, len(ts), 6):
    b = ts[k:k + 6]
    env = dict(os.environ, HYPERFRAMES_HISTORY_ROOT="/dev/shm/va_hfhist", TMPDIR="/dev/shm")   # hyperframes history copies the project (~400 MB) per run
    subprocess.run(["hyperframes", "snapshot", ".", "--no-end", "--at", ",".join(map(str, b))], cwd=f"scenes/{scene}", capture_output=True, text=True, env=env)
    shutil.rmtree("/dev/shm/va_hfhist", ignore_errors=True)
    d = max(glob.glob(f"{hf}/artifacts/snapshots/*/"), key=os.path.getmtime)
    fs = sorted(f for f in glob.glob(d + "frame-*.png"))
    for f in fs[:len(b)]: thumbs.append(Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS))
    shutil.rmtree(hf, ignore_errors=True)
rows = (len(thumbs) + C - 1) // C; sheet = Image.new("RGB", (W * C, (H + 18) * rows), (20, 20, 20)); dr = ImageDraw.Draw(sheet)
for i, im in enumerate(thumbs):
    x, y = (i % C) * W, (i // C) * (H + 18); sheet.paste(im, (x, y + 18)); dr.text((x + 4, y + 3), f"{scene} {ts[i]}s", fill=(255, 220, 120))
sheet.save(f"build/sheet-{scene}.jpg", quality=82); print(scene, len(thumbs), "frames")
