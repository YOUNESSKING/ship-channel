"""Oriskany thumbnails v3: final Test & Compare set, after the 20-channel study (research/thumbnails/THUMBNAIL_STUDY.md)
and its two critics (CRITIQUE_1_method_ctr.md, CRITIQUE_2_truth_rights_design.md).

Real US Navy / NARA images only, no repaint. Sea-only steel-blue grade (hue ~205-215, not cyan, not violet).
White text + one red word, 5 px dark stroke (Anton). Bottom-right timestamp and top-right hover icons kept clear.

F1  "37 MINUTES"           NARA 6698612  bow high, island going under (reads as "carrier sinking" at 168x94)
F2  "1969 / 2006" stack    NARA 87411 (1969 colour aerial, film) over NARA 6698621 (17 May 2006), same starboard view
F3  "WHAT'S LEFT INSIDE?"  NARA 6698620  whole carrier awash, island visible
Truth: 37 min = FACT G5 (HIGH); 1969 = NARA 87411 catalog date 1969-09-10; 2006 = 17 May 2006;
"what's left inside" = FACT E7 (~700 lb PCBs aboard), paid off in the hook (~0:20).
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PH = os.path.join(ROOT, "videos", "oriskany", "footage", "src", "photos")
REEL = os.path.join(ROOT, "videos", "oriskany", "footage", "src", "film", "nara_87411.mp4")
FONT = os.path.join(ROOT, "tools", "fonts", "Anton-Regular.ttf")
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE
W, H = 1280, 720
WHITE, RED, INK = (255, 255, 255), (224, 53, 43), (10, 14, 22)


def sea_grade(img, horizon, amount=0.55):
    """Steel-blue push on the sea only: below the horizon, mid-grey, low-saturation pixels.
    Dark hull, rust deck and white foam are excluded by luminance/saturation, so the ship is untouched."""
    a = np.asarray(img).astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    sat = (mx - mn) / (mx + 1e-6)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    m = ((lum > 0.16) & (lum < 0.72) & (sat < 0.30) & (r <= g + 0.04)).astype(np.float32)
    yy = np.arange(a.shape[0])[:, None]
    m *= np.clip((yy - horizon) / 25.0, 0, 1)
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
    tint = np.array([0.80, 0.97, 1.16])  # less red than v2 -> no violet
    out = a * (1 - amount * m[..., None]) + np.clip(a * tint + 0.02, 0, 1) * (amount * m[..., None])
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))


def finish(img, grain=0.012):
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=2))
    a = np.asarray(img).astype(np.float32)
    a += np.random.default_rng(3).normal(0, 255 * grain, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def words(img, parts, xy, size, anchor="ls"):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, size)
    x, y = xy
    if anchor == "rs":  # right-aligned: lay out from the right edge
        total = sum(d.textlength(t, font=f) for t, _ in parts) + d.textlength(" ", font=f) * (len(parts) - 1)
        x -= total
    # soft shadow, once
    sh = Image.new("L", img.size, 0)
    sd = ImageDraw.Draw(sh)
    xx = x
    for t, _ in parts:
        sd.text((xx + 5, y + 7), t, font=f, fill=200, anchor="ls")
        xx += d.textlength(t + " ", font=f)
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    img = Image.composite(Image.new("RGB", img.size, (0, 0, 0)), img, sh)
    d = ImageDraw.Draw(img)
    for t, c in parts:
        d.text((x, y), t, font=f, fill=c, stroke_width=5, stroke_fill=INK, anchor="ls")
        x += d.textlength(t + " ", font=f)
    return img


def save(img, name):
    img.save(f"{OUT}/{name}.jpg", quality=95, subsampling=0)
    img.resize((168, 94), Image.LANCZOS).save(f"{OUT}/{name}_sidebar.png")


# F1: "37 MINUTES" on 6698612 (critic 1 crop): text bottom-left over dark sea, baseline lifted off the progress bar.
f1 = Image.open(f"{PH}/nara_6698612.jpg").convert("RGB").crop((500, 60, 2633, 1260)).resize((W, H), Image.LANCZOS)
f1 = finish(sea_grade(f1, horizon=455))
f1 = words(f1, [("37", RED), ("MINUTES", WHITE)], (40, 655), 175)
save(f1, "v3_F1_37_minutes")

# F2: stacked 1969 / 2006 (critic 2 spec). Top strip from the 720x480 reel at ~62 s, SAR 10:11 corrected.
tmp = os.path.join(OUT, "_reel62.png")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "62", "-i", REEL, "-frames:v", "1", tmp], check=True)
top = Image.open(tmp).convert("RGB").resize((655, 480), Image.LANCZOS).crop((109, 222, 591, 358))
top = top.resize((W, 356), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 50, 2))
os.remove(tmp)
bot = Image.open(f"{PH}/nara_6698621.jpg").convert("RGB").crop((0, 740, 3000, 1584)).resize((W, 356), Image.LANCZOS)
bot = sea_grade(bot, horizon=0, amount=0.5)
f2 = Image.new("RGB", (W, H), (255, 255, 255))
f2.paste(top, (0, 0))
f2.paste(bot, (0, 364))
f2 = finish(f2, grain=0.014)
f2 = words(f2, [("1969", WHITE)], (30, 300), 135)
f2 = words(f2, [("2006", RED)], (30, 665), 135)
save(f2, "v3_F2_1969_2006")

# F3: "WHAT'S LEFT INSIDE?" on 6698620, words across the top over the sky/horizon band.
im = Image.open(f"{PH}/nara_6698620.jpg").convert("RGB")
iw, ih = im.size
cw = int(iw * 0.92)
ch = int(cw * 9 / 16)
cx, cy = int(iw * 0.50), int(ih * 0.50)
f3 = im.crop((cx - cw // 2, cy - ch // 2, cx + cw // 2, cy + ch // 2)).resize((W, H), Image.LANCZOS)
f3 = finish(sea_grade(f3, horizon=230))
f3 = words(f3, [("WHAT'S", WHITE), ("LEFT", RED), ("INSIDE?", WHITE)], (40, 150), 140)
save(f3, "v3_F3_whats_left_inside")

strip = Image.new("RGB", (3 * 346 + 10, 300), (15, 15, 15))
for i, n in enumerate(["v3_F1_37_minutes", "v3_F2_1969_2006", "v3_F3_whats_left_inside"]):
    t = Image.open(f"{OUT}/{n}.jpg")
    strip.paste(t.resize((336, 189), Image.LANCZOS), (10 + i * 346, 10))
    strip.paste(t.resize((168, 94), Image.LANCZOS), (10 + i * 346, 200))
strip.save(f"{OUT}/v3_feed_strip.png")
