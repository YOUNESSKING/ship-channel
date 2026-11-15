"""Mallows Bay thumbnails v2, built to research/thumbnails/THUMBNAIL_STUDY.md (sections 7, 8, 10):
blue sea dominant, colour (B&W only as the 'then' half of one split), bright overall, the wrecks as the subject,
a true number where one exists, one then/now split, 1-3 true words, Anton white + one red accent #E0352B, black stroke,
a soft dark gradient only behind the words, nothing in the bottom-right 300x160 (timestamp) or top-right (hover icons).
Real public-domain images only, no repaint, no AI. Sea-only grade per study section 10.

Revised after CRITIQUE_1_ctr.md and CRITIQUE_2_truth_rights_design.md: red element = white word on a red box, stroke 9 +
shadow, sharpen <= 1.1 after resize, crops that show a hull shape, frame dates instead of TODAY.
V3 "$3,200 A SHIP"   NOAA photo (Matt McIntosh): hull rows (+ kayaker). Main upload.
V2 "1936 | 2020"     NARA 18-AA-70-44 (Army Air Corps aerial of Mallows Bay, flown 6 Mar 1936) | NOAA ONMS staff drone video
                     (hq_noaa_wk309_birds, published Nov 2020, 1.2 s). Test & Compare.
V1 "TOO LATE"        the same NOAA drone frame, the burned hulk's bow + rows. Test & Compare, OWNER CHECK on the words.
The foreground hulk is a burned wooden hull of unknown name (NOT the Accomac).
Truth: GHOST FLEET = the common name (NOAA, MD DNR). $3,200 = $750,000 / 233 ships, 12 Sept 1922 auction (FACTCHECK_A,
narration "about three thousand two hundred dollars a ship"). 1936 = the aerial's own date; 1936 / 2020 = the frames' own dates. TOO LATE = FACT C19 /
narration (no wooden ship reached a port in Europe while the fighting lasted)."""
import os, subprocess, colorsys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
SRC = os.path.join(ROOT, "videos/mallows_bay/footage/src"); FONT = os.path.join(ROOT, "tools/fonts/Anton-Regular.ttf")
W, H = 1280, 720; WHITE, RED, INK = (255, 255, 255), (224, 53, 43), (8, 10, 14)

def frame(clip, t, crop):   # crop = (w, h, x, y) active picture (letterbox removed)
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
drone = frame("hq_noaa_wk309_birds.mp4", 1.2, (1280, 612, 0, 32))   # t 1.2: the hulk's bow shows (critique 1)

# V1 TOO LATE (owner check: FACT C19, none reached a European port while the fighting lasted; fallback BURNED)
v1 = sharp(sea_grade(cover(drone, cx=0.0, cy=0.75)))
v1 = ImageEnhance.Contrast(v1).enhance(1.06)
v1 = word_shade(v1, (10, 10, 820, 230))
x = words(v1, [("TOO", WHITE)], 50, 22, 165); boxword(v1, "LATE", x, 22, 165)
save(v1, "V1_too_late")

# V2 split 1936 | 2020: the frames' own dates (critique 2: the NOAA film is from Nov 2020, so not TODAY).
old = Image.open(os.path.join(SRC, "photos/aerial_1936_fleet.jpg")).convert("L")
old = Image.merge("RGB", [old] * 3).crop((980, 0, 1300, 360))         # fewer, larger hulls + the shore (critique 1)
a = np.asarray(cover(old, 640, 720)).astype(np.float32); a = 255 * (a / 255) ** 1.6
left = ImageEnhance.Contrast(Image.fromarray(np.clip(a * np.array([0.93, 0.98, 1.04]), 0, 255).astype(np.uint8))).enhance(1.15)
right = sharp(sea_grade(cover(drone, 640, 720, cx=0.0, cy=0.5)))
v2 = Image.new("RGB", (W, H)); v2.paste(left, (0, 0)); v2.paste(right, (640, 0))
v2 = word_shade(v2, (0, 0, 470, 200), 0.6); v2 = word_shade(v2, (640, 0, 1100, 200), 0.6)
ImageDraw.Draw(v2).rectangle((636, 0, 643, H), fill=WHITE)
words(v2, [("1936", WHITE)], 40, 28, 140); boxword(v2, "2020", 690, 28, 140)
save(v2, "V2_1936_2020")

# V3 $3,200 A SHIP (main upload): recrop so the hulls, not the kayak, carry the picture.
k = Image.open(os.path.join(SRC, "photos/noaa_kayaker_wrecks_mcintosh.jpg")).convert("RGB")
v3 = sharp(sea_grade(cover(k, cx=0.62, cy=0.80, zoom=1.15)))
v3 = ImageEnhance.Contrast(v3).enhance(1.06)
v3 = word_shade(v3, (10, 10, 1000, 240), 0.7)
x = boxword(v3, "$3,200", 50, 22, 165); words(v3, [("A SHIP", WHITE)], x, 22, 165)
save(v3, "V3_3200_a_ship")

NAMES = ["V3_3200_a_ship", "V2_1936_2020", "V1_too_late"]
strip = Image.new("RGB", (168 * 3 + 40, 114), (15, 15, 15))
for i, n in enumerate(NAMES):
    strip.paste(Image.open(os.path.join(HERE, n + "_sidebar.png")), (10 + i * 178, 10))
strip.save(os.path.join(HERE, "sidebar_strip_v2.png")); strip.convert("L").save(os.path.join(HERE, "sidebar_strip_v2_grey.png")); print("ok")
