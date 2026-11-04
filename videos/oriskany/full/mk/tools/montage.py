"""stack contact sheets vertically: python3 tools/montage.py OUT.jpg a.jpg b.jpg ..."""
import sys
from PIL import Image, ImageDraw
ims = [Image.open(p).convert("RGB") for p in sys.argv[2:]]
W = 1400; ims = [i.resize((W, int(i.height * W / i.width))) for i in ims]
out = Image.new("RGB", (W, sum(i.height + 30 for i in ims)), (0, 0, 0)); y = 0; d = ImageDraw.Draw(out)
for p, i in zip(sys.argv[2:], ims): d.text((10, y + 8), p.split("snap_")[-1], fill=(255, 220, 120)); out.paste(i, (0, y + 30)); y += i.height + 30
out.save(sys.argv[1], quality=85)
