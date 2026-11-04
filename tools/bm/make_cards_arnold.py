"""Date cards + wide (pillarbox-blur) versions for the Arnold archive blocks. Run from arnold/."""
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
datecard("arch_ticonderoga.jpg", "MAY 1775", "LAKE CHAMPLAIN", "card_1775_champlain.jpg")
datecard("arch_ticonderoga.jpg", "1777", "FORT TICONDEROGA", "card_1777_ticonderoga.jpg")
wide("arch_arnold_mezzotint.jpg", "archw_arnold.jpg")
wide("washington_src.jpg", "archw_washington.jpg")
wide("arch_philadelphia.jpg", "archw_philadelphia.jpg")
im = Image.open(M + "arch_kennebec_route.jpg").convert("RGB"); im.crop((0, 0, im.width, int(im.width * 0.75))).save(M + "arch_kennebec_top.jpg", quality=92)
print("ok")
