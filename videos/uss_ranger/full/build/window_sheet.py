"""Frame-check sheet (owner 2026-11-18): start, middle and end of every film window in beats.FILMS on one sheet."""
import os, subprocess, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from beats import FILMS
FT = os.path.join(HERE, "../../footage/src/film"); OUT = sys.argv[1] if len(sys.argv) > 1 else "/dev/shm/window_sheet.jpg"
TW, TH = 240, 135; rows = []
for k, v in FILMS.items():
    src = os.path.join(FT, v[0] + ".mp4")
    for a, b in v[1]:
        fr = []
        for t in (a + 0.15, (a + b) / 2, b - 0.3):
            p = f"/dev/shm/ws_{k}_{t:.2f}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", "-vf", f"scale={TW}:{TH}", p])
            fr.append(Image.open(p) if os.path.exists(p) else Image.new("RGB", (TW, TH), (90, 0, 0)))
        rows.append((f"{k} {a}-{b}", fr))
cols = 3; per = 2  # two windows per sheet row
W = per * (cols * TW + 10); H = ((len(rows) + per - 1) // per) * (TH + 16)
sh = Image.new("RGB", (W, H), (20, 20, 20)); d = ImageDraw.Draw(sh)
for i, (lab, fr) in enumerate(rows):
    x0 = (i % per) * (cols * TW + 10); y0 = (i // per) * (TH + 16)
    for j, im in enumerate(fr): sh.paste(im.convert("RGB"), (x0 + j * TW, y0 + 14))
    d.text((x0 + 2, y0), lab, fill=(255, 220, 80))
sh.save(OUT, quality=85); print(OUT, sh.size)
