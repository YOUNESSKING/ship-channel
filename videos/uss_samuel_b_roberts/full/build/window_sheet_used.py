"""Frame-check sheet of every film window the shot lists actually use (start / middle / end of reel_in..reel_in+dur)."""
import json, os, subprocess, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); FT = os.path.join(HERE, "../../footage/src/film")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/dev/shm/window_sheet_used.jpg"
S = [s for s in json.load(open(os.path.join(HERE, "segments.json"))) if s["kind"] == "film"]
TW, TH = 240, 135; rows = []
for s in S:
    a, b = s["reel_in"], s["reel_in"] + s["dur"]; fr = []
    for t in (a + 0.05, (a + b) / 2, b - 0.1):
        p = f"/dev/shm/wsu_{s['file']}_{t:.2f}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", os.path.join(FT, s["reel"] + ".mp4"), "-frames:v", "1", "-vf", f"scale={TW}:{TH}", p])
        fr.append(Image.open(p) if os.path.exists(p) else Image.new("RGB", (TW, TH), (90, 0, 0)))
    rows.append((f"{s['chapter']} {s['shot']} {s['clip']} {a:.1f}-{b:.1f}", fr))
per = 2; W = per * (3 * TW + 10); H = ((len(rows) + per - 1) // per) * (TH + 16)
sh = Image.new("RGB", (W, H), (20, 20, 20)); d = ImageDraw.Draw(sh)
for i, (lab, fr) in enumerate(rows):
    x0 = (i % per) * (3 * TW + 10); y0 = (i // per) * (TH + 16)
    for j, im in enumerate(fr): sh.paste(im.convert("RGB"), (x0 + j * TW, y0 + 14))
    d.text((x0 + 2, y0), lab, fill=(255, 220, 80))
sh.save(OUT, quality=85); print(OUT, sh.size)
