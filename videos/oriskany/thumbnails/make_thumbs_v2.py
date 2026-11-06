"""Oriskany thumbnails v2, after both critiques (CRITIQUE_1_ctr.md, CRITIQUE_2_truth_design.md) and COMPETITORS.md.

Real NARA 17 May 2006 photos (PH2 Kraus, US Navy, public domain). Crop + grade only; nothing added to the ship.
Changes from v1: brighter, bluer sea (competitors are bright); pure white text with ONE red accent word and a thin
dark outline; one clean shadow; text kept off the hull; three clearly different images and word sets; q95, 4:4:4.

Words (all true, fact sheet): NAVY DID THIS (G2: Navy demolition divers set the charges), 37 MINUTES (G5, HIGH),
WHAT'S LEFT INSIDE? (E7: ~700 lb PCBs left aboard, HIGH).
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "footage", "src", "photos")
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE
FONT = os.path.join(HERE, "..", "..", "..", "tools", "fonts", "Anton-Regular.ttf")
W, H = 1280, 720
WHITE = (255, 255, 255)
RED = (226, 38, 38)


def crop(img, cx, cy, frac_w):
    iw, ih = img.size
    cw = int(iw * frac_w)
    ch = int(cw * 9 / 16)
    if ch > ih:
        ch, cw = ih, int(ih * 16 / 9)
    x = min(max(int(iw * cx - cw / 2), 0), iw - cw)
    y = min(max(int(ih * cy - ch / 2), 0), ih - ch)
    return img.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS)


def grade(img, bright=1.12, blue=1.0):
    """Brighter, bluer sea; mild contrast; light sharpen. Rust stays rust (no orange push)."""
    img = ImageEnhance.Brightness(img).enhance(bright)
    img = ImageEnhance.Contrast(img).enhance(1.12)
    img = ImageEnhance.Color(img).enhance(1.12)
    a = np.asarray(img).astype(np.float32)
    # push blue/cyan only where the pixel is already bluish (the sea), not on the rust
    bluish = np.clip((a[..., 2] - a[..., 0]) / 40.0, 0, 1)[..., None]
    a = a + bluish * np.array([-6 * blue, 4 * blue, 18 * blue])
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return img.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))


def shade(img, box, strength=150):
    """Soft local darkening behind the text only (ellipse-ish, blurred), with light noise against banding."""
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle(box, radius=60, fill=strength)
    m = m.filter(ImageFilter.GaussianBlur(70))
    noise = (np.random.default_rng(7).normal(0, 3, (H, W))).astype(np.int16)
    m = Image.fromarray(np.clip(np.asarray(m).astype(np.int16) + noise, 0, 255).astype(np.uint8))
    return Image.composite(Image.new("RGB", (W, H), (4, 10, 20)), img, m)


def words(img, lines, x, y, size, anchor="la", gap=1.04):
    """lines = [[(text, colour), ...], ...]; one shadow pass, thin dark outline."""
    f = ImageFont.truetype(FONT, size)
    shadow = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(shadow)
    layout = []
    yy = y
    for line in lines:
        full = "".join(t for t, _ in line)
        bb = sd.textbbox((x, yy), full, font=f, anchor=anchor)
        cx = bb[0]
        for t, col in line:
            layout.append((cx, yy, t, col))
            cx += sd.textlength(t, font=f)
        sd.text((bb[0] + 5, yy + 7), full, font=f, fill=210, anchor="la" if anchor[0] == "l" else "la")
        yy += int(size * gap)
    shadow = shadow.filter(ImageFilter.GaussianBlur(9))
    img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, shadow)
    d = ImageDraw.Draw(img)
    for cx, yy, t, col in layout:
        d.text((cx, yy), t, font=f, fill=col, stroke_width=4, stroke_fill=(10, 14, 22))
    return img


def save(img, name):
    img.save(f"{OUT}/{name}.jpg", quality=95, subsampling=0)
    img.resize((168, 94), Image.LANCZOS).save(f"{OUT}/{name}_sidebar.png")


# T1 (launch thumbnail, pairs with "Nobody Wanted This Aircraft Carrier, So They Sank It"):
# the bow standing on end, recut lower so the foam ring and the support boat give scale; hull left, words right.
a = Image.open(f"{SRC}/nara_6698624.jpg").convert("RGB")
t1 = grade(crop(a, 0.62, 0.395, 1.0), bright=1.10)
t1 = shade(t1, (720, 70, 1290, 520), 150)
t1 = words(t1, [[("NAVY", RED)], [("DID THIS", WHITE)]], 1250, 85, 158, anchor="ra")
save(t1, "v2_T1_navy_did_this")

# T2: charges fired, smoke pouring off the deck, closer frame (NARA 6698619, ship ~2x v1 B); words in clear sea.
b = Image.open(f"{SRC}/nara_6698619.jpg").convert("RGB")
t2 = grade(crop(b, 0.50, 0.52, 0.92), bright=1.14)
t2 = shade(t2, (-40, 470, 640, 740), 140)
t2 = words(t2, [[("37 ", RED), ("MINUTES", WHITE)]], 50, 520, 150)
save(t2, "v2_T2_37_minutes")

# T3: bow slipping under, tighter crop (support ship out, hull bigger, foam less dominant).
c = Image.open(f"{SRC}/nara_6698625.jpg").convert("RGB")
t3 = grade(crop(c, 0.64, 0.45, 0.70), bright=1.10)
t3 = shade(t3, (-40, -40, 1320, 250), 150)
t3 = words(t3, [[("WHAT'S ", WHITE), ("LEFT", RED), (" INSIDE?", WHITE)]], 50, 25, 140)
save(t3, "v2_T3_whats_left_inside")

strip = Image.new("RGB", (3 * 336 + 40, 208), (15, 15, 15))
for i, n in enumerate(["v2_T1_navy_did_this", "v2_T2_37_minutes", "v2_T3_whats_left_inside"]):
    strip.paste(Image.open(f"{OUT}/{n}.jpg").resize((336, 188), Image.LANCZOS), (10 + i * 346, 10))
strip.save(f"{OUT}/v2_feed_strip.png")
