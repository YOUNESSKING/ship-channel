"""Period flags drawn by us (public-domain designs) for Sherman #13 (1864-65):
us35_flag.png = US flag with 35 stars (official 4 Jul 1863 - 3 Jul 1865; star layout was not fixed by law: 5 rows of 7, a common pattern)
csa3_flag.png = Confederate Third National (4 Mar 1865): the Second National with a red vertical bar at the fly (ratio 2:3).
run from sherman/: python3 tools/make_period_flags.py"""
import math
from PIL import Image, ImageDraw
M = "assets/media/"
RED, WHITE, BLUE = (191, 10, 48), (255, 255, 255), (0, 32, 91)  # same as us34_flag.png
def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.382
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)
# US 35 stars, 10:19 proportions like the meade us34 file (600 wide)
W, H = 1200, 632; im = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(im)
sh = H / 13
for i in range(13):
    if i % 2 == 0: d.rectangle((0, round(i * sh), W, round((i + 1) * sh)), fill=RED)
cw, ch = W * 0.4, sh * 7; d.rectangle((0, 0, cw, ch), fill=BLUE)
for r in range(5):
    for c in range(7):
        star(d, cw * (c + 0.5) / 7, ch * (r + 0.5) / 5, ch * 0.066, WHITE)
im.resize((600, 316), Image.LANCZOS).save(M + "us35_flag.png")
# Third National from the Second National file (canton kept as drawn there)
s2 = Image.open(M + "csa2_flag.png").convert("RGB")  # 2:1 stainless banner, 600x300
H3 = 400; W3 = 600; f = Image.new("RGB", (W3, H3), WHITE)
can = s2.crop((0, 0, s2.height * 2 // 3, s2.height * 2 // 3))  # 2nd National union = square, 2/3 of the hoist
# canton = top-left square-ish block of the 2nd National: height 2/3 of the flag
ch3 = int(H3 * 0.6); cw3 = int(ch3 * can.width / can.height); f.paste(can.resize((cw3, ch3), Image.LANCZOS), (0, 0))
d = ImageDraw.Draw(f); bar = int((W3 - cw3) / 2)  # Act of 4 Mar 1865: the outer half of the field beyond the union is a red bar
d.rectangle((W3 - bar, 0, W3, H3), fill=(190, 30, 45))
f.save(M + "csa3_flag.png")
print("ok", cw3, ch3, bar)
