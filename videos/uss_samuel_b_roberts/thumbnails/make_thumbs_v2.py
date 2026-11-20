"""v2 thumbnails: the REAL photo, whole frame (no cut-out), blue-toned, fading down into deep water; white Anton + one red box.
python3 make_thumbs_v2.py -> V1..V4 jpg + 246x138 sidebar previews + strip."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
P = "../footage/src/photos/"; F = "/home/user/ship-channel/tools/fonts/Anton-Regular.ttf"
W, H = 1280, 720; RED = (196, 70, 34)

def tone(im, deep=(10, 34, 66), hi=(205, 225, 240)):   # B&W -> blue duotone (sea-only feel; the ship stays the real photo)
    g = np.asarray(im.convert("L"), float) / 255.0
    g = np.clip((g - 0.04) / 0.92, 0, 1) ** 0.95
    d, h = np.array(deep, float), np.array(hi, float)
    return Image.fromarray((d * (1 - g[..., None]) + h * g[..., None]).astype(np.uint8))

def fit(im, w, h, cx=0.5, cy=0.5):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x = int((im.width - w) * cx); y = int((im.height - h) * cy); return im.crop((x, y, x + w, y + h))

def deepen(canvas, top, end, bottom_col=(4, 14, 30)):   # photo fades into the abyss between `top` and `end` (the photo's bottom edge)
    a = np.asarray(canvas, float); n = end - top
    for y in range(top, H):
        t = min(1, (y - top) / n) ** 1.3; a[y] = a[y] * (1 - t) + np.array(bottom_col) * t
    return Image.fromarray(a.astype(np.uint8))

def text(d, xy, words, size, box_word=None):
    f = ImageFont.truetype(F, size); x, y = xy
    for w in words:
        bb = d.textbbox((0, 0), w, font=f); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if w == box_word:
            pad = int(size * 0.12); d.rectangle((x - pad, y - pad // 2 + bb[1], x + tw + pad, y + bb[3] + pad // 2), fill=RED)
        for o in ((4, 4), (3, 3)): d.text((x + o[0], y + o[1]), w, font=f, fill=(0, 0, 0, 180)) if w != box_word else None
        d.text((x, y), w, font=f, fill="white"); x += tw + int(size * 0.28)

def gauge(d, x, y0, y1, label=None):
    d.line((x, y0, x, y1), fill=(220, 235, 245), width=5)
    for i in range(9): yy = y0 + (y1 - y0) * i / 8; d.line((x - 14, yy, x, yy), fill=(220, 235, 245), width=4)
    d.polygon([(x - 16, y1), (x + 16, y1), (x, y1 + 26)], fill=RED)

ship = Image.open(P + "cm_NH_96011.jpg")
def base_ship(h_ship=430, cx=0.42, cy=0.5, zoom=1.0):
    s = fit(ship, int(W * zoom), int(h_ship * zoom), cx, cy).resize((W, h_ship), Image.LANCZOS)
    c = Image.new("RGB", (W, H), (4, 14, 30)); c.paste(tone(s), (0, 0)); return deepen(c, int(h_ship * 0.62), h_ship)

out = {}
# V1: 22,000 FT DOWN (owner idea) - ship top, abyss below, gauge right
c = base_ship(440, 0.40, 0.55); d = ImageDraw.Draw(c, "RGBA"); gauge(d, 1215, 60, 560)
text(d, (40, 470), ["22,000", "FT", "DOWN"], 150, "DOWN"); out["V1_22000_ft_down"] = c
# V2: DEEPEST WRECK - tighter on the ship
c = base_ship(470, 0.45, 0.55, 1.0); d = ImageDraw.Draw(c, "RGBA")
text(d, (40, 500), ["DEEPEST", "WRECK"], 170, "WRECK"); out["V2_deepest_wreck"] = c
# V3: THEY CHARGED - real Yamato off Samar (80-G-48888), Roberts inset
y = tone(fit(Image.open(P + "cm_80_G_48888.jpg"), W, H, 0.62, 0.55), deep=(8, 26, 52)); y = ImageEnhance.Contrast(y).enhance(1.25)
d = ImageDraw.Draw(y, "RGBA"); d.rectangle((0, 0, 560, H), fill=(4, 14, 30, 150))
ins = tone(fit(ship, 470, 270, 0.42, 0.5)); y.paste(Image.new("RGB", (480, 280), "white"), (36, 404)); y.paste(ins, (41, 409))
text(d, (40, 40), ["THEY"], 165); text(d, (40, 205), ["CHARGED"], 150, "CHARGED"); out["V3_they_charged"] = y
# V4: 4 MILES DOWN
c = base_ship(420, 0.35, 0.55); d = ImageDraw.Draw(c, "RGBA"); gauge(d, 70, 60, 600)
text(d, (130, 470), ["4", "MILES", "DOWN"], 160, "DOWN"); out["V4_4_miles_down"] = c
strip = Image.new("RGB", (246 * 4 + 30, 138), "white")
for i, (k, im) in enumerate(out.items()):
    im.save(k + ".jpg", quality=92); sb = im.resize((246, 138), Image.LANCZOS); sb.save(k + "_sidebar.png"); strip.paste(sb, (i * 256, 0))
strip.save("sidebar_strip_v2.png"); print(list(out))
