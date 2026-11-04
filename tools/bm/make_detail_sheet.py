"""Detail test sheet: variants of the same battlefield crop. usage: python3 tools/make_detail_sheet.py OUT.jpg BASE:cx:cy ...
(cx, cy = centre of the 640x360-ish crop in 2x HD px; crop is 1400x788 HD px shown at 700x394)"""
import sys, json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
F = ImageFont.truetype("/home/user/battle-maps/arnold/tools/oswald-latin-700-normal.ttf", 20)
M = "assets/media/"
def ld(p): return Image.open(p).convert("RGBA")
def comp(base, layers):
    im = ld(f"assets/{base}_hd_lift.jpg").resize((5760, 3240))
    for l in layers: im = Image.alpha_composite(im, ld(M + f"{base}_det_{l}.png"))
    return im
VAR = [("A  NOW (no detail)", []), ("B  + rivers, creeks, lakes", ["riv"]), ("C  + trees + swamps", ["tree", "swamp", "riv"]), ("D  C + crown texture (bolder)", ["tree", "crown", "swamp", "riv"])]
CW, CH = 1400, 788
specs = sys.argv[2:]; tiles = []
for sp in specs:
    b, cx, cy = sp.split(":"); cx, cy = int(cx), int(cy)
    row = []
    for name, ls in VAR:
        im = comp(b, ls).convert("RGB").crop((cx - CW // 2, cy - CH // 2, cx + CW // 2, cy + CH // 2)).resize((700, 394), Image.LANCZOS)
        d = ImageDraw.Draw(im); d.rectangle((0, 0, 700, 28), fill=(0, 0, 0)); d.text((8, 3), f"{b.upper()}  {name}", font=F, fill=(240, 236, 226)); row.append(im)
    tiles.append(row)
sheet = Image.new("RGB", (700 * 4, 394 * len(tiles)), (20, 20, 20))
for r, row in enumerate(tiles):
    for c, im in enumerate(row): sheet.paste(im, (c * 700, r * 394))
sheet.save(sys.argv[1], quality=88); print(sys.argv[1], sheet.size)
