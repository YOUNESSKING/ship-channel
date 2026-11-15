"""Mallows Bay thumbnails v2, built to research/thumbnails/THUMBNAIL_STUDY.md (sections 7, 8, 10):
blue sea dominant, colour (B&W only as the 'then' half of one split), bright overall, the wrecks as the subject,
a true number where one exists, one then/now split, 1-3 true words, Anton white + one red accent #E0352B, black stroke,
a soft dark gradient only behind the words, nothing in the bottom-right 300x160 (timestamp) or top-right (hover icons).
Real public-domain images only, no repaint, no AI. Sea-only grade per study section 10.

V1 "GHOST FLEET"     NOAA ONMS staff drone video (hq_noaa_wk309_birds, 1.6 s): hull rows in blue water, rusty wreck in front.
V2 "1936 | TODAY"    NARA 18-AA-70-44 (Army Air Corps aerial, Mallows Bay, 8 Apr 1936) | the same NOAA drone shot (2.2 s).
V3 "$3,200 A SHIP"   NOAA photo (Matt McIntosh): a kayaker among the hull rows.
Truth: GHOST FLEET = the common name (NOAA, MD DNR). $3,200 = $750,000 / 233 ships, 12 Sept 1922 auction (FACTCHECK_A,
narration "about three thousand two hundred dollars a ship"). 1936 = the aerial's own date; TODAY = 2010s NOAA footage."""
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

def words(im, parts, x, y, size):
    d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, size)
    for w, col in parts:
        d.text((x, y), w, font=f, fill=col, stroke_width=4, stroke_fill=INK); x += d.textlength(w + " ", font=f)
    return x

def save(im, name):
    im.save(os.path.join(HERE, name + ".jpg"), quality=93)
    im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, name + "_sidebar.png"))

drone = frame("hq_noaa_wk309_birds.mp4", 1.6, (1280, 612, 0, 32))
drone = ImageEnhance.Sharpness(drone).enhance(1.3)

# V1 GHOST FLEET: full drone frame, words top-left over the far water/treeline.
v1 = sea_grade(cover(drone, cx=0.25, cy=0.6))
v1 = ImageEnhance.Contrast(v1).enhance(1.08)
v1 = word_shade(v1, (10, 10, 900, 230))
words(v1, [("GHOST", WHITE), ("FLEET", RED)], 44, 18, 170)
save(v1, "V1_ghost_fleet")

# V2 split 1936 | TODAY: left = the 1936 rows, right = the drone rows today. White 8 px divider.
old = Image.open(os.path.join(SRC, "photos/aerial_1936_fleet.jpg")).convert("L")
old = Image.merge("RGB", [old] * 3)
old = old.crop((560, 230, 1180, 816))            # the hull rows, larger
left = cover(old, 640, 720, 0.5, 0.5); a = np.asarray(left).astype(np.float32)
a = 255 * (a / 255) ** 1.9                       # pull the washed-out water down to mid-grey so the hulls read
left = Image.fromarray(np.clip(a * np.array([0.93, 0.98, 1.04]), 0, 255).astype(np.uint8))
left = ImageEnhance.Contrast(left).enhance(1.25)   # cool, slightly down so it reads as 'then'
rows = ImageEnhance.Sharpness(frame("hq_noaa_wk309_birds.mp4", 2.2, (1280, 612, 0, 32))).enhance(1.3)
right = sea_grade(cover(rows, 640, 720, cx=0.35, cy=0.5))   # the hull rows today
v2 = Image.new("RGB", (W, H)); v2.paste(left, (0, 0)); v2.paste(right, (640, 0))
v2 = word_shade(v2, (0, 0, 500, 200), 0.6); v2 = word_shade(v2, (640, 0, 1120, 200), 0.6)
ImageDraw.Draw(v2).rectangle((636, 0, 643, H), fill=WHITE)
words(v2, [("1936", WHITE)], 36, 14, 150); words(v2, [("TODAY", RED)], 676, 14, 150)
save(v2, "V2_1936_today")

# V3 $3,200 A SHIP: the kayaker among the rows (blue, colour, wrecks).
k = Image.open(os.path.join(SRC, "photos/noaa_kayaker_wrecks_mcintosh.jpg")).convert("RGB")
v3 = sea_grade(cover(k, cx=0.5, cy=0.6, zoom=1.0))
v3 = ImageEnhance.Contrast(ImageEnhance.Sharpness(v3).enhance(1.4)).enhance(1.06)
v3 = word_shade(v3, (10, 10, 980, 230))
x = words(v3, [("$3,200", RED)], 44, 18, 170); words(v3, [("A SHIP", WHITE)], x - 10, 18, 170)
save(v3, "V3_3200_a_ship")

strip = Image.new("RGB", (168 * 3 + 40, 114), (15, 15, 15))
for i, n in enumerate(["V1_ghost_fleet", "V2_1936_today", "V3_3200_a_ship"]):
    strip.paste(Image.open(os.path.join(HERE, n + "_sidebar.png")), (10 + i * 178, 10))
strip.save(os.path.join(HERE, "sidebar_strip_v2.png")); print("ok")
