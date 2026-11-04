"""Date cards for the Grant archive blocks. Run from grant/: python3 tools/make_cards_grant.py"""
import sys
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, "tools")
from archive_shots import headline_layer
M = "assets/media/"; W, H = 1920, 1080
def cover(im, fy=0.4):
    k = max(W / im.width, H / im.height); im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    x0 = (im.width - W) // 2; y0 = int(min(max(im.height * fy - H / 2, 0), im.height - H)); return im.crop((x0, y0, x0 + W, y0 + H))
def datecard(src, year, text, out):
    im = Image.open(M + src).convert("RGB")
    a = np.asarray(cover(im), np.float32) * 0.5; b = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    Image.alpha_composite(b, headline_layer(year, text, W, H)).convert("RGB").save(M + out, quality=92)
def wide(src, out, fx=0.5):
    im = Image.open(M + src).convert("RGB")
    bg = cover(im).filter(ImageFilter.GaussianBlur(40)); bg = Image.fromarray((np.asarray(bg, np.float32) * 0.45).astype(np.uint8))
    w = int(im.width * H / im.height); fg = im.resize((w, H), Image.LANCZOS); bg.paste(fg, (int(W * fx - w / 2), 0)); bg.save(M + out, quality=93)
datecard("arch_fort_henry_litho.jpg", "JANUARY 1862", "CAIRO, ILLINOIS", "card_1862_cairo.jpg")
datecard("arch_massaponax.jpg", "MARCH 1864", "WASHINGTON", "card_1864_washington.jpg")
for n in ("grant_1862_harpers", "grant_ltgen_harpers", "lincoln_1863", "lincoln_1864"): wide(f"arch_{n}.jpg", f"archw_{n}.jpg")
print("ok")
