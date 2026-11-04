"""Designed newspaper / letter headline cards for the Arnold video (no real masthead). -> assets/media/headline_<id>.jpg"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage
SB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"; SR = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
CARDS = {
    "congress": ("CONTINENTAL CONGRESS  ·  FEBRUARY 1777", ["FIVE GENERALS", "PROMOTED"], "Congress promotes five generals who were junior to Benedict Arnold"),
    "ticonderoga": ("LAKE CHAMPLAIN  ·  MAY 1775", ["FORT TICONDEROGA", "CAPTURED"], "Benedict Arnold helps capture the fort weeks after the war began"),
    "mahan": ("ALFRED THAYER MAHAN  ·  NAVAL HISTORIAN", ["“THE INVALUABLE", "YEAR OF DELAY”"], "secured to them in 1776 by their little navy on Lake Champlain"),
    "gates": ("GEN. HORATIO GATES  ·  REPORT  ·  OCTOBER 1777", ["“THE GALLANT", "GENERAL ARNOLD”"], "whose Leg was fractured by a musket ball, as he forced the Enemy's Breast Work"),
}
PW, PH = 2400, 1350
for key, (top, lines, sub) in CARDS.items():
    rng = np.random.default_rng(len(key) * 7)
    pap = np.full((PH, PW, 3), (214, 203, 176), np.float32) + rng.normal(0, 7, (PH, PW, 1)) + ndimage.gaussian_filter(rng.normal(0, 25, (PH, PW)), 40)[..., None]
    yy, xx = np.mgrid[0:PH, 0:PW]; v = 1 - 0.35 * (((xx - PW / 2) / (PW / 2)) ** 2 + ((yy - PH / 2) / (PH / 2)) ** 2); pap *= v[..., None]
    im = Image.fromarray(pap.clip(0, 255).astype(np.uint8)); d = ImageDraw.Draw(im); ink = (28, 24, 20)
    d.line((260, 200, PW - 260, 200), fill=ink, width=6); d.line((260, 214, PW - 260, 214), fill=ink, width=2)
    d.text((PW / 2, 160), top, font=ImageFont.truetype(SR, 44), fill=ink, anchor="mm")
    fs = 165 if len(lines) == 2 else 130; step = fs * 1.12
    for i, line in enumerate(lines):
        f = ImageFont.truetype(SB, fs)
        while d.textlength(line, font=f) > PW - 480: f = ImageFont.truetype(SB, f.size - 6)
        d.text((PW / 2, 330 + i * step), line, font=f, fill=ink, anchor="mm")
    y = 330 + len(lines) * step + 10
    d.text((PW / 2, y), sub, font=ImageFont.truetype(SR, 50), fill=ink, anchor="mm")
    d.line((260, y + 70, PW - 260, y + 70), fill=ink, width=3)
    for col in range(4):
        x0 = 260 + col * (PW - 520) / 4 + 20
        for k in range(int((PH - y - 140) / 32)):
            w = (PW - 520) / 4 - 60 - (rng.random() * 120 if k % 5 == 4 else 0)
            d.rectangle((x0, y + 110 + k * 32, x0 + w, y + 110 + k * 32 + 12), fill=(70, 62, 52))
    im = im.filter(ImageFilter.GaussianBlur(1.2))
    a = np.asarray(im, np.float32) * np.array([0.86, 0.98, 1.02])
    Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(f"assets/media/headline_{key}.jpg", quality=92)
    print("ok", key)
