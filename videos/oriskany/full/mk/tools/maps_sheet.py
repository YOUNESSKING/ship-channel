"""Contact sheet of every rendered map scene: python3 tools/maps_sheet.py  ->  MAPS_SHEET.jpg
One frame per scene at 75 % of the shot (labels are in by then), in video order, with file name, start time and duration."""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_full as bf
ROOT = bf.ROOT
segs = bf.SEGS + [s for s in bf.plan_segs() if s["scene"] not in {q["scene"] for q in bf.SEGS}]
segs.sort(key=lambda s: s["t0_abs"])
F = os.path.join(ROOT, "tools", "oswald-latin-700-normal.ttf")
f1, f2, fT = ImageFont.truetype(F, 22), ImageFont.truetype(F, 17), ImageFont.truetype(F, 40)
C, W, H = 6, 480, 270
rows = (len(segs) + C - 1) // C
sheet = Image.new("RGB", (C * W + (C + 1) * 12, 90 + rows * (H + 66)), (18, 20, 24))
d = ImageDraw.Draw(sheet)
d.text((14, 18), f"ORISKANY FULL · MAP SCENES ({len(segs)})", font=fT, fill=(227, 194, 122))
tmp = tempfile.mkdtemp()
for i, s in enumerate(segs):
    x, y = 12 + (i % C) * (W + 12), 90 + (i // C) * (H + 66)
    mp4 = os.path.join(ROOT, "..", "segments", s["file"])
    used = "" if s in bf.SEGS else "  (dropped)"
    if os.path.exists(mp4):
        png = os.path.join(tmp, f"{i}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['dur'] * 0.75:.2f}", "-i", mp4, "-frames:v", "1", "-vf", f"scale={W}:{H}", png], check=True)
        sheet.paste(Image.open(png).convert("RGB"), (x, y))
    else:
        d.rectangle([x, y, x + W, y + H], outline=(160, 40, 40), width=3); d.text((x + 20, y + 120), "NOT RENDERED", font=f1, fill=(220, 80, 80))
    m, sec = divmod(s["t0_abs"], 60)
    d.text((x, y + H + 6), f"{s['file']}   {int(m)}:{sec:04.1f}  {s['dur']:.1f}s{used}", font=f1, fill=(240, 236, 226))
    d.text((x, y + H + 36), s["narration"][:62], font=f2, fill=(170, 180, 190))
out = os.path.join(ROOT, "MAPS_SHEET.jpg")
sheet.save(out, quality=84); print(out, sheet.size)
