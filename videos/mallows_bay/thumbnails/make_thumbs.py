"""Mallows Bay thumbnails (Test & Compare set). Real archive / NOAA images only, no repaint, no AI.
White Anton text with one red word, dark stroke; bottom-right (timestamp) and top-right (hover icons) kept clear.
T1 "GHOST FLEET"  NARA 18-AA-70-44, Mallows Bay 8 Apr 1936 (Army Air Corps aerial): the fleet in rows.
T2 "GHOST FLEET"  NOAA (Matt McIntosh) drone photo: a kayaker among the hull outlines today.
T3 "SET ON FIRE"  NARA 111-SC-94285, the burn of 7 Nov 1925 (Signal Corps aerial).
Truth: GHOST FLEET = the common name of the Mallows Bay wrecks (NOAA, MD DNR); SET ON FIRE = FACTCHECK_B (31 ships, 7 Nov 1925)."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
PH = os.path.join(ROOT, "videos/mallows_bay/footage/src/photos"); FONT = os.path.join(ROOT, "tools/fonts/Anton-Regular.ttf")
W, H = 1280, 720; WHITE, RED = (255, 255, 255), (217, 64, 43)
def cover(im, cx=0.5, cy=0.5, zoom=1.0):
    im = im.convert("RGB"); r = max(W / im.width, H / im.height) * zoom; im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    x = int((im.width - W) * cx); y = int((im.height - H) * cy); return im.crop((x, y, x + W, y + H))
def vignette(im, k=0.55):
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    m = np.clip(1 - k * np.clip(d - 0.55, 0, 1), 0, 1)[..., None]; return Image.fromarray((np.asarray(im) * m).astype(np.uint8))
def text(im, lines, y0, size=150, x0=60):
    d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, size); y = y0
    for words in lines:
        x = x0
        for w, col in words:
            d.text((x, y), w, font=f, fill=col, stroke_width=7, stroke_fill=(8, 10, 14)); x += d.textlength(w + " ", font=f)
        y += int(size * 1.08)
    return im
def save(im, name):
    im.save(os.path.join(HERE, name + ".jpg"), quality=92)
    im.resize((168, 94), Image.LANCZOS).save(os.path.join(HERE, name + "_sidebar.png"))
# T1
a = Image.open(os.path.join(PH, "aerial_1936_fleet.jpg")); a = ImageEnhance.Contrast(a.convert("RGB")).enhance(1.35)
t1 = cover(a, 0.55, 0.45, 1.05)
arr = np.asarray(t1).astype(float); g = arr.mean(-1, keepdims=True); tint = np.concatenate([g * 0.86, g * 0.95, g * 1.05], -1)   # cold river tone
t1 = vignette(Image.fromarray(np.clip(tint * 0.72, 0, 255).astype(np.uint8)), 0.7)
save(text(t1, [[("GHOST", WHITE)], [("FLEET", RED)]], 180, 190), "T1_ghost_fleet_1936")
# T2
b = Image.open(os.path.join(PH, "noaa_aerial_kayak_wrecks_mcintosh.jpg"))
t2 = vignette(ImageEnhance.Contrast(cover(b, 0.5, 0.5, 1.0)).enhance(1.15), 0.6)
save(text(t2, [[("GHOST", WHITE), ("FLEET", RED)]], 40, 150), "T2_ghost_fleet_today")
# T3
c = Image.open(os.path.join(PH, "burn_quantico_1925_c_c.jpg")).convert("RGB")
t3 = cover(c, 0.5, 0.45, 1.1); arr = np.asarray(t3).astype(float); g = arr.mean(-1, keepdims=True)
t3 = Image.fromarray(np.clip(np.concatenate([g * 1.08, g * 0.98, g * 0.88], -1), 0, 255).astype(np.uint8))   # warm sepia, the burn
t3 = vignette(ImageEnhance.Contrast(t3).enhance(1.25), 0.7)
save(text(t3, [[("SET ON", WHITE)], [("FIRE", RED)]], 170, 190), "T3_set_on_fire")
strip = Image.new("RGB", (168 * 3 + 40, 114), (15, 15, 15))
for i, n in enumerate(["T1_ghost_fleet_1936", "T2_ghost_fleet_today", "T3_set_on_fire"]): strip.paste(Image.open(os.path.join(HERE, n + "_sidebar.png")), (10 + i * 178, 10))
strip.save(os.path.join(HERE, "sidebar_strip.png")); print("ok")
