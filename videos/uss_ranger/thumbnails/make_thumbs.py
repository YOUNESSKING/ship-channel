"""USS Ranger (CV-61) thumbnails v1. Helpers copied from videos/uss_nevada/thumbnails/make_thumbs.py (sea-only grade,
stroke 9 + shadow, white word on red box, sharpen <= 1.1, bottom-right 300x160 clear). Real US Navy photos only, no repaint.
V1 "1¢"      split: NARA 6444104 (1988 aerial, jets on deck) | DVIDS 1799515 (ex-Ranger under tow, 2015)
V2 "FOR 1¢"  NARA 6486624 (F-14A launch from Ranger, 1993), full frame
V3 "ONE CENT" DVIDS 1799520 (ex-Ranger under tow, 2015), full frame
No imagery from the films Top Gun or Star Trek IV. No claim of a sale on the image (the Navy paid the breaker $0.01)."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
PH = os.path.join(ROOT, "videos/uss_ranger/footage/src/photos"); FONT = os.path.join(ROOT, "tools/fonts/Anton-Regular.ttf")
W, H = 1280, 720; WHITE, RED, INK = (255, 255, 255), (217, 87, 43), (8, 10, 14)
def P(n): return Image.open(os.path.join(PH, n + ".jpg")).convert("RGB")
def cover(im, w=W, h=H, cx=0.5, cy=0.5, zoom=1.0):
    r = max(w / im.width, h / im.height) * zoom
    im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    x = int((im.width - w) * cx); y = int((im.height - h) * cy); return im.crop((x, y, x + w, y + h))

def sea_grade(im, sat=1.4, toward=195 / 360, amt=0.4, lift=0.3, hz=0):
    """Study s10: mask the water (hue 160-270, lum < 85 %, not rust), +40 % saturation, hue 40 % toward 195 deg,
    then lift midtones ~0.3 EV over the whole frame. Wreck, rust, trees untouched by the hue move."""
    a = np.asarray(im).astype(np.float32) / 255
    mx, mn = a.max(-1), a.min(-1); d = mx - mn + 1e-6; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6
    s = np.where(mx > 0, d / (mx + 1e-6), 0); v = mx; lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    mask = (hue > 160 / 360) & (hue < 270 / 360) & (lum < 0.85) & ~((hue > 10 / 360) & (hue < 50 / 360) & (s > 0.25))
    mask = mask & (np.arange(a.shape[0])[:, None] > hz)
    m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)); m = np.asarray(m).astype(np.float32)[..., None] / 255
    h2 = hue + (toward - hue) * amt; s2 = np.clip(s * sat, 0, 1)
    i = np.floor(h2 * 6) % 6; f = h2 * 6 - np.floor(h2 * 6); p = v * (1 - s2); q = v * (1 - f * s2); t = v * (1 - (1 - f) * s2)
    rgb = np.stack([np.choose(i.astype(int), [v, q, p, p, t, v]), np.choose(i.astype(int), [t, v, v, q, p, p]),
                    np.choose(i.astype(int), [p, p, t, v, v, q])], -1)
    a = a * (1 - m) + rgb * m
    a = np.clip(a, 0, 1) ** (1 / (2 ** lift))      # midtone lift (~0.3 EV), highlights stay
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

def word_shade(im, box, strength=0.55):
    """Soft dark gradient only behind the words (box = x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box; m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle(box, 60, fill=int(255 * strength))
    m = m.filter(ImageFilter.GaussianBlur(70)); dark = Image.new("RGB", (W, H), (5, 8, 14)); return Image.composite(dark, im, m)

def shadow(im, draw_fn, off=(6, 8), alpha=170, blur=6):
    m = Image.new("L", im.size, 0); draw_fn(ImageDraw.Draw(m), 255)
    m = m.transform(m.size, Image.AFFINE, (1, 0, -off[0], 0, 1, -off[1])).filter(ImageFilter.GaussianBlur(blur))
    return Image.composite(Image.new("RGB", im.size, INK), im, m.point(lambda v: v * alpha // 255))

def words(im, parts, x, y, size):
    """White words, 9 px stroke + drop shadow (critique 2: the 4 px stroke vanished at 168x94)."""
    f = ImageFont.truetype(FONT, size); d0 = ImageDraw.Draw(im); xs = []
    for w, col in parts: xs.append(x); x += d0.textlength(w + " ", font=f)
    def draw(d, fill):
        for (w, _), xx in zip(parts, xs): d.text((xx, y), w, font=f, fill=fill, stroke_width=9, stroke_fill=fill)
    im2 = shadow(im, draw); d = ImageDraw.Draw(im2)
    for (w, col), xx in zip(parts, xs): d.text((xx, y), w, font=f, fill=col, stroke_width=9, stroke_fill=INK)
    im.paste(im2); return x

def boxword(im, w, x, y, size, pad=14):
    """The one red element: white word on a solid #E0352B box (critique 1: red text on the sea vanishes in greyscale)."""
    f = ImageFont.truetype(FONT, size); d = ImageDraw.Draw(im); l, t, r, b = d.textbbox((x, y), w, font=f)
    box = (l - pad, t - pad, r + pad, b + pad)
    im2 = shadow(im, lambda dd, fill: dd.rectangle(box, fill=fill)); d = ImageDraw.Draw(im2)
    d.rectangle(box, fill=RED); d.text((x, y), w, font=f, fill=WHITE, stroke_width=3, stroke_fill=INK)
    im.paste(im2); return r + pad + int(size * 0.18)

def save(im, name):
    im.save(os.path.join(HERE, name + ".jpg"), quality=93)
    im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, name + "_sidebar.png"))

def sharp(im, k=1.1): return ImageEnhance.Sharpness(im).enhance(k)   # <= 1.1, after the resize (critique 2: halos)


def grade(im, a=0.4, hz=0):
    return ImageEnhance.Color(sea_grade(im, sat=1.3, amt=a, lift=0.35, hz=hz)).enhance(1.08)

# V1 split
L = P("nara_6444104"); L = L.crop((380, 0, 380 + 1830, 2040))
L = ImageEnhance.Contrast(sharp(grade(cover(L, 640, 720, cx=.5, cy=.62), hz=110))).enhance(1.08)
R = P("dvids_ima_1799515"); R = R.crop((330, 0, 330 + 1260, 1333))
R = ImageEnhance.Contrast(sharp(grade(cover(R, 640, 720, cx=.5, cy=.5), 0.3, hz=450))).enhance(1.08)
v1 = Image.new("RGB", (W, H)); v1.paste(L, (0, 0)); v1.paste(R, (640, 0))
v1 = word_shade(v1, (200, 0, 1080, 330), 0.45)
ImageDraw.Draw(v1).rectangle((636, 0, 643, H), fill=WHITE)
boxword(v1, "1\u00a2", 490, 20, 300, pad=18)
save(v1, "V1_split_1c")

# V2 F-14 launch
a = P("nara_6486624"); a = a.crop((800, 330, 3000, 330 + 1237))
v2 = sharp(grade(cover(a, W, H), 0, hz=9999)); v2 = ImageEnhance.Contrast(v2).enhance(1.12)
v2 = ImageEnhance.Brightness(v2).enhance(0.92)
v2 = word_shade(v2, (0, 250, 800, 720), 0.55)
words(v2, [("FOR", WHITE)], 44, 250, 175); boxword(v2, "1\u00a2", 60, 425, 190)
save(v2, "V2_for_1c")

# V3 the tow
t = P("dvids_ima_1799520"); t = t.crop((0, 0, 2000, 1125))
v3 = sharp(grade(cover(t, W, H, cy=0.0), 0.3, hz=535)); v3 = ImageEnhance.Contrast(v3).enhance(1.1)
v3 = word_shade(v3, (0, 0, 760, 230), 0.4)
words(v3, [("ONE", WHITE)], 44, 14, 150); boxword(v3, "CENT", 330, 14, 150)
save(v3, "V3_one_cent")

NAMES = ["V1_split_1c", "V2_for_1c", "V3_one_cent"]
strip = Image.new("RGB", (168 * 3 + 40, 114 * 2 - 10), (15, 15, 15))
for i, n in enumerate(NAMES):
    t = Image.open(os.path.join(HERE, n + "_sidebar.png")); strip.paste(t, (10 + i * 178, 10)); strip.paste(t.convert("L").convert("RGB"), (10 + i * 178, 114))
strip.save(os.path.join(HERE, "sidebar_strip.png"))
strip2 = Image.new("RGB", (246 * 3 + 40, 138 * 2 + 30), (15, 15, 15))
for i, n in enumerate(NAMES):
    t = Image.open(os.path.join(HERE, n + ".jpg")).resize((246, 138), Image.LANCZOS); strip2.paste(t, (10 + i * 256, 10)); strip2.paste(t.convert("L").convert("RGB"), (10 + i * 256, 158))
strip2.save(os.path.join(HERE, "sidebar_strip_246.png")); print("ok")
