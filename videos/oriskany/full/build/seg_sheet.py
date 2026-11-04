"""Contact sheets of built film segments: one row per segment (4 frames: 0.1 s, 1/3, 2/3, end-0.1 s), file name burned in.
  python3 build/seg_sheet.py OUT.jpg segments/f_c03_*.mp4"""
import subprocess, sys, os, tempfile
from PIL import Image, ImageDraw, ImageFont
out, files = sys.argv[1], sys.argv[2:]
TW, TH = 384, 216; F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)
sheet = Image.new("RGB", (TW * 4 + 260, TH * len(files)), (20, 20, 20)); d = ImageDraw.Draw(sheet)
for r, f in enumerate(files):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())
    for c, t in enumerate([0.1, dur / 3, 2 * dur / 3, max(0.1, dur - 0.12)]):
        tmp = tempfile.mktemp(suffix=".jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", f, "-frames:v", "1", "-vf", f"scale={TW}:{TH}", tmp], check=True)
        sheet.paste(Image.open(tmp), (260 + c * TW, r * TH)); os.remove(tmp)
    d.text((8, r * TH + 8), os.path.basename(f), font=F, fill=(255, 220, 80)); d.text((8, r * TH + 34), f"{dur:.2f}s", font=F, fill=(200, 200, 200))
sheet.save(out, quality=80); print(out)
