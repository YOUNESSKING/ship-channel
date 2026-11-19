"""USS Ranger (CV-61) thumbnails v2. Helpers from make_thumbs.py (v1). Real US Navy photos (NARA / DVIDS, public domain), sea-only grade, no repaint,
no film or poster imagery, no claim of a sale (the Navy paid the breaker $0.01 to tow and scrap her)."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import os, numpy as np
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


def seabright(im, hz, gain=0.55, tone=0.55):
    """Sea-only lift: water below the horizon row hz (blue hues only) gets a gamma lift + blue push. Ship and sky untouched."""
    a = np.asarray(im).astype(np.float32) / 255
    mx, mn = a.max(-1), a.min(-1); d = mx - mn + 1e-6; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    mask = (hue > 150 / 360) & (hue < 280 / 360) & (lum < 0.6) & (np.arange(a.shape[0])[:, None] > hz)
    m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))).astype(np.float32)[..., None] / 255
    lift = np.clip(a, 0, 1) ** tone
    lift = lift * np.array([0.85, 1.02, 1.25], np.float32) * (1 + gain * 0.2)
    a = a * (1 - m) + np.clip(lift, 0, 1) * m
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

def finish(im, c=1.1):
    return ImageEnhance.Contrast(sharp(im)).enhance(c)

def draw_words(im, parts, x, y, size, pad=14):
    """parts: list of (text, kind) kind 'w' white-stroked or 'r' red box; laid out on one line."""
    f = ImageFont.truetype(FONT, size)
    for t, k in parts:
        if k == "w": x = words(im, [(t, WHITE)], x, y, size) 
        else: x = boxword(im, t, x, y, size, pad)
    return x

# T1: 1988 aerial, ship large, sea lifted
a = P("nara_6444104").crop((60, 600, 60 + 2080, 600 + 1170))
t1 = seabright(cover(a), hz=0, tone=0.62); t1 = finish(grade(t1, 0.35, hz=0), 1.08)
t1 = ImageEnhance.Brightness(t1).enhance(1.06)
t1 = word_shade(t1, (0, 0, 820, 330), 0.4)
x = words(t1, [("WORTH", WHITE)], 40, 14, 190); boxword(t1, "1¢?", 60, 220, 220, pad=16)
save(t1, "T1_worth_1c")

# T2: 1993 bow-on, crowded deck
a = P("nara_6655015").crop((0, 250, 3000, 250 + 1687))
t2 = seabright(cover(a), hz=330, tone=0.62, gain=0.2); t2 = finish(grade(t2, 0.3, hz=330), 1.05)
t2 = ImageEnhance.Brightness(t2).enhance(1.12)
t2 = word_shade(t2, (0, 330, 700, 720), 0.5)
words(t2, [("ONE", WHITE)], 40, 290, 185); boxword(t2, "CENT", 56, 470, 165, pad=12)
save(t2, "T2_one_cent_bow")

# T3: the tow, hull tight
a = P("dvids_ima_1799520").crop((0, 110, 1900, 110 + 1069))
t3 = seabright(cover(a), hz=590, tone=0.85, gain=0.1); t3 = finish(grade(t3, 0.2, hz=590), 1.1)
words(t3, [("FOR", WHITE)], 40, 14, 190); boxword(t3, "1¢", 330, 14, 190, pad=14)
save(t3, "T3_for_1c_tow")

# T4: split, bow-on glory | rust
L = P("nara_6655015").crop((300, 250, 300 + 2000, 250 + 2130 - 250)); 
L = seabright(cover(L, 760, 720, cx=.5, cy=.55), hz=170, tone=0.62, gain=0.2); L = finish(grade(L, 0.3, hz=170), 1.05); L = ImageEnhance.Brightness(L).enhance(1.12)
R = P("dvids_ima_1799520").crop((300, 0, 300 + 1100, 1060))
R = seabright(cover(R, 760, 720, cx=.5, cy=.45), hz=610, tone=0.85, gain=0.1); R = finish(grade(R, 0.2, hz=610), 1.1)
t4 = Image.new("RGB", (W, H)); t4.paste(L, (0, 0))
mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).polygon([(620, 0), (W, 0), (W, H), (520, H)], fill=255)
Rf = Image.new("RGB", (W, H)); Rf.paste(R, (520, 0)); t4 = Image.composite(Rf, t4, mask)
ImageDraw.Draw(t4).line([(620, 0), (520, H)], fill=WHITE, width=8)
boxword(t4, "1¢", 505, 20, 300, pad=18)
save(t4, "T4_split_1c")

NAMES = ["T1_worth_1c", "T2_one_cent_bow", "T3_for_1c_tow", "T4_split_1c"]
def montage(sz, out):
    w, h = sz; m = Image.new("RGB", (w * 4 + 50, h * 2 + 30), (15, 15, 15))
    for i, n in enumerate(NAMES):
        t = Image.open(os.path.join(HERE, n + ".jpg")).resize(sz, Image.LANCZOS)
        m.paste(t, (10 + i * (w + 10), 10)); m.paste(t.convert("L").convert("RGB"), (10 + i * (w + 10), 20 + h))
    m.save(os.path.join(HERE, out))
montage((168, 94), "sidebar_v2.png"); montage((246, 138), "sidebar_v2_246.png"); print("ok")
