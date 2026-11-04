"""Labelled snapshot sheet for the owner: python3 tools/make_sheet.py SPEC.json OUT.jpg
SPEC = {"title": "...", "note": "...", "frames": [["scene", seconds, "mm:ss in the video", "what happens", "sound"], ...]}
Uses scenes/<scene>/snapshots/frame-*-at-<seconds>s.png (made with hyperframes snapshot)."""
import glob, json, sys
from PIL import Image, ImageDraw, ImageFont
spec = json.load(open(sys.argv[1]))
F = "tools/oswald-latin-700-normal.ttf"
f1, f2, fT, fN = (ImageFont.truetype(F, n) for n in (26, 19, 40, 24))
W, H, C = 900, 506, 3
fr = spec["frames"]; rows = (len(fr) + C - 1) // C
sheet = Image.new("RGB", (C * W + (C + 1) * 20, 150 + rows * (H + 120)), (24, 22, 18))
d = ImageDraw.Draw(sheet)
d.text((20, 20), spec["title"], font=fT, fill=(247, 243, 234)); d.text((20, 82), spec.get("note", ""), font=fN, fill=(201, 180, 138))
for i, (scene, t, mm, what, snd) in enumerate(fr):
    m = [p for p in glob.glob(f"scenes/{scene}/snapshots/frame-*-at-*s.png") if abs(float(p.rsplit("-at-", 1)[1][:-5]) - t) < 0.05]
    x, y = 20 + (i % C) * (W + 20), 150 + (i // C) * (H + 120)
    if m: sheet.paste(Image.open(m[0]).convert("RGB").resize((W, H), Image.LANCZOS), (x, y))
    d.rectangle([x, y, x + 96, y + 40], fill=(196, 18, 31)); d.text((x + 10, y + 4), mm, font=f1, fill="white")
    d.text((x, y + H + 8), what, font=f2, fill=(247, 243, 234)); d.text((x, y + H + 40), snd, font=f2, fill=(201, 180, 138))
sheet.save(sys.argv[2], quality=86); print(sys.argv[2], sheet.size)
