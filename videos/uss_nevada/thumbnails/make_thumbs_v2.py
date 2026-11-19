"""USS Nevada thumbnails v2 (video 3). Built to research/thumbnails/THUMBNAIL_STUDY.md (s7, s8, s10), STYLE_LOCK s6,
the Mallows critiques and CRITIQUE_1.md (v1). Real archive frames only (no repaint, no AI), sea/sky-only grade,
white Anton words + one red box, stroke 9 + shadow, sharpen <= 1.1 after resize, bottom-right 300x160 and the
top-right hover corner clear. Two real 1946 Crossroads images side by side are always separated by a white divider:
the ship is never pasted INTO an explosion.

Sources (all Navy film MN 6517 "Operation Crossroads: Able and Baker Day Tests", COMJTF-1 / NPC 1949, archive.org
OperationCrossroads; US Navy production = federal work):
  NEV_CLOSE  w01g 5.5 s   Nevada at anchor at Bikini, bow three-quarter, tower and 14-in turrets (colour)
  NEV_WIDE   w01g 3.4 s   Nevada at anchor at Bikini, the whole ship (colour)
  ABLE_RING  w03  54 s    Able, 1 July 1946, the mushroom with its red-rimmed condensation ring, from the air (colour)
  ABLE_LAG   w03  29.5 s  Able, the mushroom rising over the lagoon and reef, from the air (colour)
Each film still is a 7-9 frame median of the same shot, aligned by phase correlation (removes grain and dust,
adds nothing), then the vertical film scratches are filled from their neighbour columns.
Colour: w01g is the video's colour-corrected window (toward the documented international orange, BS-A1); nothing on
any image says "orange", "colour" or "restored".
Truth: SURVIVED / 2 A-BOMBS / SHE SURVIVED = FACTCHECK_B F1 (true; never "only"). THEY MISSED = Able only (C1, C8).
"""
import os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
SRC = os.path.join(ROOT, "videos/uss_nevada/footage/src"); FONT = os.path.join(ROOT, "tools/fonts/Anton-Regular.ttf")
CACHE = "/dev/shm/nevada_thumbs_v2"; os.makedirs(CACHE, exist_ok=True)
W, H = 1280, 720; WHITE, RED, INK = (255, 255, 255), (224, 53, 43), (8, 10, 14)
CROP43 = "1450:1076:235:2"          # active 4:3 picture inside the 1920x1080 file (pillarbox removed)

# ---------- source frames: aligned median of n frames, scratch fill ----------
def _grab(clip, t0, n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-i", os.path.join(SRC, "film", clip), "-vf",
                          "crop=" + CROP43, "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 1076, 1450, 3).astype(np.float32)

def _shift(ref, img):
    a = ref.mean(-1); b = img.mean(-1); A = np.fft.fft2(a - a.mean()); B = np.fft.fft2(b - b.mean())
    R = A * np.conj(B); R /= np.abs(R) + 1e-9; r = np.fft.ifft2(R).real; y, x = np.unravel_index(r.argmax(), r.shape)
    return (y - a.shape[0] if y > a.shape[0] // 2 else y), (x - a.shape[1] if x > a.shape[1] // 2 else x)

def _descratch(a, thr=3.0):
    """Vertical film scratches: columns whose median (whole height, or top half at 2x thr) differs from their +-4
    neighbours are grouped into bands and refilled by linear interpolation between the clean columns either side
    (restoration of a film defect; no picture content is added)."""
    g = a.mean(-1); nb = (np.roll(g, 4, 1) + np.roll(g, -4, 1)) / 2
    dev = np.median(g - nb, 0); dev2 = np.median((g - nb)[: g.shape[0] // 2], 0)
    bad = (np.abs(dev) > thr) | (np.abs(dev2) > 2 * thr); bad[:8] = bad[-8:] = False
    xs = np.where(bad)[0]; runs = []
    for x in xs:
        if runs and x <= runs[-1][1] + 3: runs[-1][1] = x
        else: runs.append([x, x])
    for s0, e0 in runs:
        l, r = max(s0 - 3, 0), min(e0 + 3, a.shape[1] - 1)
        for x in range(l + 1, r):
            t = (x - l) / (r - l); a[:, x] = a[:, l] * (1 - t) + a[:, r] * t
    return a

def still(clip, t0, n=7):
    p = os.path.join(CACHE, "%s_%s_%d.png" % (clip[:-4], t0, n))
    if not os.path.exists(p):
        fr = _grab(clip, t0, n); ref = fr[len(fr) // 2]
        al = [np.roll(f, _shift(ref, f), (0, 1)) for f in fr]
        m = _descratch(np.median(np.stack(al), 0))
        Image.fromarray(np.clip(m, 0, 255).astype(np.uint8)).save(p)
    return Image.open(p).convert("RGB")

# ---------- helpers (from v1 / Mallows make_thumbs_v2.py) ----------
def cover(im, w=W, h=H, cx=0.5, cy=0.5, zoom=1.0):
    r = max(w / im.width, h / im.height) * zoom
    im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    x = int((im.width - w) * cx); y = int((im.height - h) * cy); return im.crop((x, y, x + w, y + h))

def box_crop(im, cx, cy, w, h):
    """Crop a w x h window centred at (cx, cy) in source pixels, clamped to the frame."""
    x0 = int(min(max(cx - w / 2, 0), im.width - w)); y0 = int(min(max(cy - h / 2, 0), im.height - h))
    return im.crop((x0, y0, x0 + w, y0 + h))

def hsv_mask(im, h0, h1, lmax=0.85, smin=0.0):
    a = np.asarray(im).astype(np.float32) / 255
    mx, mn = a.max(-1), a.min(-1); d = mx - mn + 1e-6; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6
    s = np.where(mx > 0, d / (mx + 1e-6), 0); lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return a, hue, s, mx, (hue > h0 / 360) & (hue < h1 / 360) & (lum < lmax) & (s >= smin)

def sea_grade(im, sat=1.4, toward=200 / 360, amt=0.45, lift=0.3, h0=150, h1=270, lmax=0.9):
    """Study s10: water/sky mask (blue-cyan hues, not the salmon ship), +sat, hue toward steel-blue, midtone lift."""
    a, hue, s, v, mask = hsv_mask(im, h0, h1, lmax)
    m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    m = np.asarray(m).astype(np.float32)[..., None] / 255
    h2 = hue + (toward - hue) * amt; s2 = np.clip(s * sat, 0, 1)
    i = np.floor(h2 * 6) % 6; f = h2 * 6 - np.floor(h2 * 6); p = v * (1 - s2); q = v * (1 - f * s2); t = v * (1 - (1 - f) * s2)
    rgb = np.stack([np.choose(i.astype(int), [v, q, p, p, t, v]), np.choose(i.astype(int), [t, v, v, q, p, p]),
                    np.choose(i.astype(int), [p, p, t, v, v, q])], -1)
    a = a * (1 - m) + rgb * m
    a = np.clip(a, 0, 1) ** (1 / (2 ** lift))
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

def word_shade(im, box, strength=0.55, blur=70):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle(box, 60, fill=int(255 * strength))
    m = m.filter(ImageFilter.GaussianBlur(blur)); return Image.composite(Image.new("RGB", im.size, (5, 8, 14)), im, m)

def shadow(im, draw_fn, off=(6, 8), alpha=170, blur=6):
    m = Image.new("L", im.size, 0); draw_fn(ImageDraw.Draw(m), 255)
    m = m.transform(m.size, Image.AFFINE, (1, 0, -off[0], 0, 1, -off[1])).filter(ImageFilter.GaussianBlur(blur))
    return Image.composite(Image.new("RGB", im.size, INK), im, m.point(lambda v: v * alpha // 255))

def words(im, w, x, y, size, col=WHITE, stroke=9):
    f = ImageFont.truetype(FONT, size)
    def draw(d, fill): d.text((x, y), w, font=f, fill=fill, stroke_width=stroke, stroke_fill=fill)
    im2 = shadow(im, draw); ImageDraw.Draw(im2).text((x, y), w, font=f, fill=col, stroke_width=stroke, stroke_fill=INK)
    im.paste(im2); return ImageDraw.Draw(im).textbbox((x, y), w, font=f, stroke_width=stroke)

def boxword(im, w, x, y, size, pad=16):
    f = ImageFont.truetype(FONT, size); d = ImageDraw.Draw(im); l, t, r, b = d.textbbox((x, y), w, font=f)
    box = (l - pad, t - pad, r + pad, b + pad)
    im2 = shadow(im, lambda dd, fill: dd.rectangle(box, fill=fill)); d = ImageDraw.Draw(im2)
    d.rectangle(box, fill=RED); d.text((x, y), w, font=f, fill=WHITE, stroke_width=3, stroke_fill=INK)
    im.paste(im2); return box

def text_w(w, size): return ImageDraw.Draw(Image.new("L", (1, 1))).textlength(w, font=ImageFont.truetype(FONT, size))
def sharp(im, k=1.1): return ImageEnhance.Sharpness(im).enhance(k)
def divider(im, x, wd=10):
    ImageDraw.Draw(im).rectangle((x - wd // 2, 0, x + wd // 2 - 1, H), fill=WHITE)

def save(im, name):
    im.save(os.path.join(HERE, name + ".jpg"), quality=93)
    im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, name + "_sidebar.png"))

# ---------- graded source pieces ----------
def nevada_close(lift=0.25):
    im = still("crossroads_mn6517_w01g.mp4", 5.5, 7)
    im = sea_grade(im, sat=1.35, amt=0.5, lift=lift)
    return ImageEnhance.Contrast(im).enhance(1.08)   # tonal only: no colour push on the ship (critique 2)

def nevada_wide():
    im = still("crossroads_mn6517_w01g.mp4", 3.4, 7)
    im = sea_grade(im, sat=1.35, amt=0.5, lift=0.25)
    return ImageEnhance.Contrast(im).enhance(1.08)   # tonal only: no colour push on the ship (critique 2)

def able_ring():
    im = still("crossroads_mn6517_w03.mp4", 54, 9)
    im = sea_grade(im, sat=1.3, toward=195 / 360, amt=0.35, lift=0.2, h0=120, h1=260)
    return ImageEnhance.Contrast(im).enhance(1.12)

def able_lagoon():
    im = still("crossroads_mn6517_w03.mp4", 29.5, 7)
    im = sea_grade(im, sat=1.3, toward=195 / 360, amt=0.4, lift=0.3, h0=120, h1=260)
    return ImageEnhance.Contrast(im).enhance(1.08)

BUILDS = {}
def build(fn): BUILDS[fn.__name__] = fn; return fn

@build
def N1_split_2_a_bombs():
    """Split: whole Nevada at Bikini (left 760) | Able mushroom with its red-rimmed ring (right 520). SURVIVED / [2 A-BOMBS]."""
    L = sharp(cover(nevada_wide().crop((170, 0, 1306, 1076)), 760, H))
    R = sharp(cover(able_ring().crop((673, 0, 1450, 1076)), 520, H))
    im = Image.new("RGB", (W, H)); im.paste(L, (0, 0)); im.paste(R, (760, 0)); divider(im, 760)
    im = word_shade(im, (0, 0, 740, 200), 0.45)
    words(im, "SURVIVED", 40, 0, 170)
    im = word_shade(im, (0, 540, 700, 720), 0.4)
    boxword(im, "2 A-BOMBS", 56, 562, 118)
    return im

@build
def N2_she_survived():
    """Whole Nevada at Bikini, full frame, blue-graded sea and sky. SHE / [SURVIVED]."""
    im = sharp(cover(nevada_wide().crop((0, 160, 1450, 976)), W, H))
    im = word_shade(im, (0, 0, 900, 230), 0.45)
    x1 = words(im, "SHE", 40, 4, 170)[2]
    boxword(im, "SURVIVED", x1 + 40, 22, 150)
    return im

@build
def N3_big_2():
    """Close: Nevada's tower and 14-in turrets, full frame. Giant [2] red box + A-BOMBS."""
    im = sharp(cover(nevada_close().crop((0, 40, 1450, 856)), W, H))
    im = word_shade(im, (0, 0, 520, 470), 0.5)
    b = boxword(im, "2", 60, 24, 300, pad=22)
    words(im, "A-BOMBS", 40, b[3] + 8, 120)
    return im

@build
def N4_lagoon_she_survived():
    """Split: Able mushroom over the lagoon from the air (left 560) | Nevada close (right 720). SHE / [SURVIVED]."""
    L = sharp(cover(able_lagoon().crop((435, 60, 995, 780)), 560, H))
    R = sharp(cover(nevada_close().crop((300, 0, 1450, 1076)), 720, H, cx=0.5))
    im = Image.new("RGB", (W, H)); im.paste(L, (0, 0)); im.paste(R, (560, 0)); divider(im, 560)
    im = word_shade(im, (0, 430, 560, 720), 0.55)
    words(im, "SHE", 40, 440, 130)
    boxword(im, "SURVIVED", 52, 598, 100)
    return im

@build
def N5_half_split():
    """50/50 split: Nevada's tower and turrets (left) | Able mushroom with its red ring (right). SURVIVED / [2 A-BOMBS]."""
    L = sharp(cover(nevada_close().crop((150, 0, 1106, 1076)), 640, H))
    R = sharp(cover(able_ring().crop((494, 0, 1450, 1076)), 640, H))
    im = Image.new("RGB", (W, H)); im.paste(L, (0, 0)); im.paste(R, (640, 0)); divider(im, 640)
    im = word_shade(im, (660, 0, 1150, 190), 0.35)
    words(im, "SURVIVED", 668, 8, 128)   # ends x ~1120: clear of the top-right hover icons
    im = word_shade(im, (300, 560, 980, 720), 0.4)
    wd = text_w("2 A-BOMBS", 120); boxword(im, "2 A-BOMBS", int(640 - wd / 2), 572, 120)
    return im

@build
def N6_half_split_box_only():
    """As N5, one element only: [2 A-BOMBS] red box, bottom centre."""
    L = sharp(cover(nevada_close().crop((150, 0, 1106, 1076)), 640, H))
    R = sharp(cover(able_ring().crop((494, 0, 1450, 1076)), 640, H))
    im = Image.new("RGB", (W, H)); im.paste(L, (0, 0)); im.paste(R, (640, 0)); divider(im, 640)
    im = word_shade(im, (260, 540, 1020, 720), 0.4)
    wd = text_w("2 A-BOMBS", 136); boxword(im, "2 A-BOMBS", int(640 - wd / 2), 556, 136)
    return im

@build
def N8_wide_survived_2():
    """The whole ship, full frame (v1 V1 rebuilt from the denoised still): SURVIVED / [2 A-BOMBS] (box covers the barge)."""
    im = sharp(cover(nevada_wide().crop((0, 160, 1450, 976)), W, H))
    im = word_shade(im, (0, 0, 760, 220), 0.45)
    words(im, "SURVIVED", 40, 0, 175)
    im = word_shade(im, (330, 550, 960, 720), 0.4)
    boxword(im, "2 A-BOMBS", 410, 572, 122)
    return im

def _split(right):
    L = sharp(cover(nevada_close().crop((150, 0, 1106, 1076)), 640, H))
    im = Image.new("RGB", (W, H)); im.paste(L, (0, 0)); im.paste(right, (640, 0)); divider(im, 640); return im

@build
def N9_split_target():
    """50/50 split as N6; one word on the ship half: [TARGET]. She was the aiming point of Able and a target ship in Baker."""
    im = _split(sharp(cover(able_ring().crop((494, 0, 1450, 1076)), 640, H)))
    im = word_shade(im, (0, 540, 640, 720), 0.4)
    boxword(im, "TARGET", 70, 556, 136)
    return im

@build
def N10_split_lagoon_2():
    """50/50 split: Nevada (left) | Able over the lagoon and reef from the air (right, blue-green). [2 A-BOMBS] bottom centre."""
    im = _split(sharp(cover(able_lagoon().crop((380, 40, 1020, 760)), 640, H)))
    im = word_shade(im, (260, 540, 1020, 720), 0.4)
    wd = text_w("2 A-BOMBS", 136); boxword(im, "2 A-BOMBS", int(640 - wd / 2), 556, 136)
    return im

@build
def N11_split_lagoon_survived():
    """As N10 (Nevada | Able over the lagoon), one word: [SURVIVED]. Adds to titles that say 'target' or 'dropped'."""
    im = _split(sharp(cover(able_lagoon().crop((380, 40, 1020, 760)), 640, H)))
    im = word_shade(im, (260, 540, 1020, 720), 0.4)
    wd = text_w("SURVIVED", 136); boxword(im, "SURVIVED", int(640 - wd / 2), 556, 136)
    return im

BUILD_LIST = list(BUILDS)
RANKED = ["N10_split_lagoon_2", "N11_split_lagoon_survived", "N6_half_split_box_only", "N9_split_target", "N3_big_2", "N5_half_split"]

def strip(names, out):
    """168x94 sidebar tiles: colour row on top, greyscale row below (Mallows checklist item 5)."""
    st = Image.new("RGB", (178 * len(names) + 10, 114 * 2 - 10), (15, 15, 15))
    for i, n in enumerate(names):
        t = Image.open(os.path.join(HERE, n + "_sidebar.png")).convert("RGB")
        st.paste(t, (10 + i * 178, 10)); st.paste(t.convert("L").convert("RGB"), (10 + i * 178, 114))
    st.save(os.path.join(HERE, out + ".png"))
    st.convert("L").save(os.path.join(HERE, out + "_grey.png"))

if __name__ == "__main__":
    import sys
    names = sys.argv[1:] or BUILD_LIST
    for n in names: save(BUILDS[n](), n); print("built", n)
    if not sys.argv[1:]: strip(RANKED, "sidebar_strip_v2")
