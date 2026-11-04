"""a1_: quick look (not the deliverable): snapshots at the given scene seconds -> one small sheet in the scratchpad.
usage (from arnold/): python3 tools/a1_quick.py SCENE OUT.jpg t1,t2,..."""
import glob, os, shutil, subprocess, sys
from PIL import Image, ImageDraw
sc, out, ts = sys.argv[1:4]
subprocess.run(["hyperframes", "snapshot", ".", "--at", ts], cwd=f"scenes/{sc}", capture_output=True, text=True, timeout=1500)
D = sorted(glob.glob(f"scenes/{sc}/.hyperframes/artifacts/snapshots/*/"), key=os.path.getmtime)[-1]
fs = sorted(glob.glob(D + "frame-*.png"), key=lambda p: float(p.rsplit("-at-", 1)[1][:-5]))
W, H = 960, 540; C = 2; rows = (len(fs) + 1) // 2
sh = Image.new("RGB", (C * W, rows * H)); d = ImageDraw.Draw(sh)
for i, p in enumerate(fs):
    sh.paste(Image.open(p).convert("RGB").resize((W, H)), ((i % C) * W, (i // C) * H)); d.text(((i % C) * W + 8, (i // C) * H + 8), p.rsplit("-at-", 1)[1][:-5], fill="red")
sh.save(out, quality=82); shutil.rmtree(f"scenes/{sc}/.hyperframes/artifacts", ignore_errors=True); print(out, len(fs))
