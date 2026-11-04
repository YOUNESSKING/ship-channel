"""quick review grid: python3 tools/m1_quick.py SCENE OUT.jpg [cols]"""
import glob, sys
from PIL import Image, ImageDraw
fs = sorted(glob.glob(f"scenes/{sys.argv[1]}/snapshots/frame-*-at-*s.png"), key=lambda p: float(p.rsplit("-at-", 1)[1][:-5]))
C = int(sys.argv[3]) if len(sys.argv) > 3 else 3; W, H = 800, 450; R = (len(fs) + C - 1) // C
sh = Image.new("RGB", (C * W, R * H), (0, 0, 0)); d = ImageDraw.Draw(sh)
for i, f in enumerate(fs):
    x, y = (i % C) * W, (i // C) * H; sh.paste(Image.open(f).convert("RGB").resize((W, H)), (x, y))
    d.rectangle([x, y, x + 70, y + 22], fill=(200, 0, 0)); d.text((x + 4, y + 4), f.rsplit("-at-", 1)[1][:-4], fill="white")
sh.save(sys.argv[2], quality=80)
