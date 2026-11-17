"""USS Nevada thumbnails v1 (video 3), built to research/thumbnails/THUMBNAIL_STUDY.md s10 and the Mallows Bay critiques
(make_thumbs_v2.py helpers: sea-only grade, word_shade, stroke 9 + shadow, white word on a red box, sharpen <= 1.1,
words top/left, bottom-right 300x160 clear). Real archive frames only, no repaint, no AI.
V1 "SURVIVED / 2 A-BOMBS"  Navy film MN 6517 (Operation Crossroads: Able and Baker Day Tests), window w01g 0.5 s: Nevada at anchor, wide.
V2 "BULL'S-EYE"            split: NARA 80-G-396226 (Able, 1 July 1946, B&W still) | w01g 32 s (Nevada's tripod mast and 14-in turrets).
V3 "THEY MISSED"           w01g 32 s full frame (the same colour shot as V2 left, wider).
Colour is the film's own (faded, then graded in the video's grade pass); no claim about the colour is written on the image."""
import os, subprocess, colorsys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
SRC = os.path.join(ROOT, "videos/uss_nevada/footage/src"); FONT = os.path.join(ROOT, "tools/fonts/Anton-Regular.ttf")
W, H = 1280, 720; WHITE, RED, INK = (255, 255, 255), (224, 53, 43), (8, 10, 14)

def frame(clip, t, crop=(1450, 1076, 235, 2)):   # active picture of the 4:3 film inside the 1920x1080 file (pillarbox removed)
    out = "/dev/shm/_thumb_frame.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", os.path.join(SRC, "film", clip),
                    "-vf", "crop=%d:%d:%d:%d" % crop, "-frames:v", "1", out], check=True)
    return Image.open(out).convert("RGB")

def cover(im, w=W, h=H, cx=0.5, cy=0.5, zoom=1.0):
    r = max(w / im.width, h / im.height) * zoom
    im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    x = int((im.width - w) * cx); y = int((im.height - h) * cy); return im.crop((x, y, x + w, y + h))

def sea_grade(im, sat=1.4, toward=195 / 360, amt=0.4, lift=0.3):
    """Study s10: mask the water (hue 160-270, lum < 85 %, not rust), +40 % saturation, hue 40 % toward 195 deg,
    then lift midtones ~0.3 EV over the whole frame. Wreck, rust, trees untouched by the hue move."""
    a = np.asarray(im).astype(np.float32) / 255
    mx, mn = a.max(-1), a.min(-1); d = mx - mn + 1e-6; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6
    s = np.where(mx > 0, d / (mx + 1e-6), 0); v = mx; lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    mask = (hue > 160 / 360) & (hue < 270 / 360) & (lum < 0.85) & ~((hue > 10 / 360) & (hue < 50 / 360) & (s > 0.25))
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

V1_BOX = None
def crop169(im, y_from_bottom=0, x=0):
    h = int(im.width * 9 / 16); y = im.height - h - y_from_bottom; return im.crop((0, y, im.width, y + h))

def grade_film(im, sea=True):
    im = sea_grade(im, sat=1.25, amt=0.45, lift=0.35) if sea else im
    return ImageEnhance.Color(im).enhance(1.08)

# V1 SURVIVED / 2 A-BOMBS
f = frame("crossroads_mn6517_w01g.mp4", 0.5)
v1 = cover(crop169(f, 0), W, H)
v1 = sharp(grade_film(v1)); v1 = ImageEnhance.Contrast(v1).enhance(1.08)
v1 = word_shade(v1, (0, 0, 760, 200), 0.5); v1 = word_shade(v1, (0, 440, 820, 720), 0.55)
words(v1, [("SURVIVED", WHITE)], 44, 18, 165)
boxword(v1, "2 A-BOMBS", 60, 495, 150)
save(v1, "V1_survived_2_a_bombs")

# V2 split: Able burst | Nevada
nev = frame("crossroads_mn6517_w01g.mp4", 32)
left = nev.crop((int(nev.width * 0.12), 0, int(nev.width * 0.12) + 960, nev.height))
left = sharp(grade_film(cover(left, 640, 720, cx=0.5, cy=0.5)))
able = Image.open(os.path.join(SRC, "photos/cx_able_80g_396226.jpg")).convert("RGB")   # NARA 80-G-396226, Able, 1 July 1946 (B&W)
ax = int(able.width * 0.665) - 693
able = able.crop((ax, 0, ax + 1386, able.height))
right = ImageEnhance.Contrast(sharp(cover(able, 640, 720, cx=0.5, cy=0.5))).enhance(1.12)
v2 = Image.new("RGB", (W, H)); v2.paste(right, (0, 0)); v2.paste(left, (640, 0))
v2 = word_shade(v2, (0, 0, 1280, 230), 0.5)
ImageDraw.Draw(v2).rectangle((636, 0, 643, H), fill=WHITE)
boxword(v2, "BULL'S-EYE", 46, 24, 150)
save(v2, "V2_bulls_eye")

# V3 THEY MISSED
v3 = cover(crop169(nev, 1076 - 815), W, H)
v3 = sharp(grade_film(v3)); v3 = ImageEnhance.Contrast(v3).enhance(1.08)
v3 = word_shade(v3, (0, 0, 520, 420), 0.5)
words(v3, [("THEY", WHITE)], 46, 16, 160); boxword(v3, "MISSED", 60, 208, 160)
save(v3, "V3_they_missed")

NAMES = ["V1_survived_2_a_bombs", "V2_bulls_eye", "V3_they_missed"]
strip = Image.new("RGB", (168 * 3 + 40, 114 * 2 - 10), (15, 15, 15))
for i, n in enumerate(NAMES):
    t = Image.open(os.path.join(HERE, n + "_sidebar.png")); strip.paste(t, (10 + i * 178, 10)); strip.paste(t.convert("L").convert("RGB"), (10 + i * 178, 114))
strip.save(os.path.join(HERE, "sidebar_strip.png")); print("ok")
