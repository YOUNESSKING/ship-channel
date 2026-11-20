"""USS Samuel B. Roberts (DE-413) thumbnails. Real PD photos only (NHHC NH 96011 for the ship, NARA 80-G-48888 for Yamato).
Roberts cut out with a hand polygon + darkness key; composited on a deep-blue gradient. No wreck image, no AI image generation."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops, ImageOps
import numpy as np, os, random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
PH = os.path.join(ROOT, "videos/uss_samuel_b_roberts/footage/src/photos"); FONT = os.path.join(ROOT, "tools/fonts/Anton-Regular.ttf")
W, H = 1280, 720; WHITE, RED, INK = (255, 255, 255), (217, 87, 43), (4, 8, 14)
def P(n): return Image.open(os.path.join(PH, n + ".jpg")).convert("RGB")

# ---- Roberts cut-out (coordinates of a 900 px wide preview; scale to the 3840 px source)
def roberts():
    src = P("cm_NH_96011"); k = src.width / 900
    poly = [(0,380),(40,373),(70,365),(95,353),(130,346),(165,341),(185,331),(200,319),(214,312),(228,324),(250,328),(275,323),(300,319),
            (310,305),(318,285),(330,276),(345,270),(355,256),(385,251),(398,254),(420,266),(445,256),(468,262),(476,236),(488,236),
            (498,262),(520,275),(545,284),(600,282),(618,276),(640,272),(657,274),(690,290),(725,285),(745,298),(790,303),(815,292),
            (835,278),(852,275),(866,281),(869,302),(866,335),(863,382),(858,416),(800,413),(700,421),(600,425),(500,419),(430,414),
            (300,413),(200,411),(100,409),(0,405)]
    m = Image.new("L", src.size, 0); dr = ImageDraw.Draw(m)
    dr.polygon([(x * k, y * k) for x, y in poly], fill=255)
    sc = lambda pts: [(x * k, y * k) for x, y in pts]
    dr.line(sc([(347, 24), (374, 270)]), fill=255, width=int(5 * k))          # mast
    dr.line(sc([(342, 122), (398, 128)]), fill=255, width=int(3 * k))          # yardarm
    dr.polygon(sc([(310, 124), (342, 122), (343, 202), (312, 203)]), fill=255)  # flag hoist (left)
    dr.polygon(sc([(376, 134), (394, 132), (394, 152), (376, 154)]), fill=255)  # flags (right)
    dr.line(sc([(350, 40), (368, 40)]), fill=255, width=int(8 * k)); dr.polygon(sc([(352, 44), (372, 44), (372, 58), (352, 58)]), fill=255)  # crow's nest
    m = m.filter(ImageFilter.GaussianBlur(1.0 * k / 3))
    rgba = src.convert("RGBA"); rgba.putalpha(m)
    return rgba.crop((0, int(18 * k), int(880 * k), int(432 * k)))

def lin_grad(w, h, top, bot, gamma=1.0):
    t = (np.linspace(0, 1, h) ** gamma)[:, None, None]; a = np.array(top, np.float32) * (1 - t) + np.array(bot, np.float32) * t
    return Image.fromarray(np.repeat(a, w, 1).astype(np.uint8))

def abyss(surface_y=360, top=(52, 112, 168), mid=(8, 30, 58), bot=(1, 4, 9)):
    """light sea at the surface, falling to near black. Marine snow = tiny soft dots, no object."""
    a = np.zeros((H, W, 3), np.float32)
    for y in range(H):
        if y < surface_y: t = y / surface_y; c = np.array(top, np.float32) * (1 - 0.25 * (1 - t))
        else:
            t = min(1, (y - surface_y) / (H - surface_y)); t = t ** 0.55
            c = np.array(top, np.float32) * (1 - t) * 0.55 + np.array(mid, np.float32) * (1 - abs(2 * t - 1) * 0) * (t) ; c = c * (1 - t) + np.array(bot, np.float32) * t
        a[y] = c
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im, "RGBA"); rnd = random.Random(4)
    for _ in range(90):
        x = rnd.randint(0, W); y = rnd.randint(surface_y + 30, H); r = rnd.choice([1, 1, 2]); d.ellipse([x - r, y - r, x + r, y + r], fill=(180, 210, 235, rnd.randint(25, 70)))
    return im

POLY = [(0,380),(40,373),(70,365),(95,353),(130,346),(165,341),(185,331),(200,319),(214,312),(228,324),(250,328),(275,323),(300,319),
        (310,305),(318,285),(330,276),(345,270),(355,256),(385,251),(398,254),(420,266),(445,256),(468,262),(476,236),(488,236),
        (498,262),(520,275),(545,284),(600,282),(618,276),(640,272),(657,274),(690,290),(725,285),(745,298),(790,303),(815,292),
        (835,278),(852,275),(866,281),(869,302),(866,335),(863,382),(858,416),(800,413),(700,421),(600,425),(500,419),(430,414),
        (300,413),(200,411),(100,409),(0,405)]
def place_ship(im, width, x, y, tone=1.0):
    """Real photo, no cut-out: the print is multiplied into the canvas (its grey sky becomes the canvas colour, so there is no seam; the
    sea ripples go dark blue), and inside a loose hull outline the ship's own greys are kept light. Pixels are the original photograph."""
    src = P("cm_NH_96011"); k = src.width / 900
    c = ImageOps.autocontrast(src.crop((0, int(14 * k), int(900 * k), int(446 * k))).convert("L"), cutoff=(0.5, 0))
    r = width / c.width; c = c.resize((width, int(c.height * r)), Image.LANCZOS); w, h = c.size
    g = np.asarray(c).astype(np.float32); wp = np.percentile(g[: h // 5], 85)
    Ln = np.clip(g / wp, 0, 1) ** 1.25
    em = Image.new("L", (w, h), 0); f = 26; ImageDraw.Draw(em).rectangle([f, f, w - f, h - f], fill=255); em = np.asarray(em.filter(ImageFilter.GaussianBlur(f * .5))).astype(np.float32) / 255
    Ln = 1 - (1 - Ln) * em
    q = width / 900
    pm = Image.new("L", (w, h), 0); pd = ImageDraw.Draw(pm); pd.polygon([(px * q, (py - 14) * q) for px, py in POLY], fill=255)
    pass
    mm = Image.new("L", (w, h), 0); md = ImageDraw.Draw(mm)
    md.line([(349 * q, 30 * q), (374 * q, 256 * q)], fill=255, width=max(3, int(5 * q))); md.line([(338 * q, 108 * q), (400 * q, 114 * q)], fill=255, width=max(2, int(5 * q)))
    md.rectangle([308 * q, 108 * q, 345 * q, 188 * q], fill=255); md.rectangle([372 * q, 120 * q, 396 * q, 142 * q], fill=255)
    mm = np.asarray(mm.filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
    pm = np.asarray(pm.filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255
    km = Image.new("L", (w, h), 0); kd = ImageDraw.Draw(km); kd.polygon([(px * q, (py - 14) * q) for px, py in POLY], fill=255)
    kd.rectangle([300 * q, 14 * q, 410 * q, 280 * r], fill=255); km = np.asarray(km.filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255
    km = np.maximum(km, np.clip((np.arange(h)[:, None] - 0.86 * h) / (0.1 * h), 0, 1))      # keep the waves below the hull
    Ln = 1 - (1 - Ln) * (0.15 + 0.85 * km)                                                    # flatten the cloud mottling of the sky only
    wgt = np.maximum(pm * np.clip((0.80 - Ln) / 0.15, 0, 1), mm * np.clip((0.97 - Ln) / 0.08, 0, 1))
    cv = np.asarray(im.crop((x, y, x + w, y + h))).astype(np.float32)
    base = cv * Ln[..., None]
    ship = np.clip((Ln[..., None] ** 0.8) * np.array([225, 235, 246], np.float32) * tone, 0, 255)
    ship = np.where((mm > pm)[..., None], np.clip((Ln[..., None] ** 3.5) * np.array([225, 235, 246], np.float32) * tone, 0, 255), ship)
    out = base * (1 - wgt[..., None]) + ship * wgt[..., None]
    im.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), (x, y)); return (x, y, x + w, y + h)

def shadow(im, draw_fn, off=(6, 8), alpha=185, blur=6):
    m = Image.new("L", im.size, 0); draw_fn(ImageDraw.Draw(m), 255)
    m = m.transform(m.size, Image.AFFINE, (1, 0, -off[0], 0, 1, -off[1])).filter(ImageFilter.GaussianBlur(blur))
    return Image.composite(Image.new("RGB", im.size, INK), im, m.point(lambda v: v * alpha // 255))
def word(im, w, x, y, size, col=WHITE):
    """y = top of the capitals. Returns (right, bottom)."""
    f = ImageFont.truetype(FONT, size); bb = ImageDraw.Draw(im).textbbox((0, 0), w, font=f); yy = y - bb[1]
    im2 = shadow(im, lambda d, fill: d.text((x, yy), w, font=f, fill=fill, stroke_width=9, stroke_fill=fill))
    d = ImageDraw.Draw(im2); d.text((x, yy), w, font=f, fill=col, stroke_width=9, stroke_fill=INK); d.text((x, yy), w, font=f, fill=col); im.paste(im2)
    return x + bb[2], y + bb[3] - bb[1]
def boxword(im, w, x, y, size, pad=14):
    """The one red element. y = top of the capitals. Returns (right, bottom) of the box."""
    f = ImageFont.truetype(FONT, size); d = ImageDraw.Draw(im); bb = d.textbbox((0, 0), w, font=f); yy = y - bb[1]
    box = (x - pad, y - pad, x + bb[2] + pad, y + bb[3] - bb[1] + pad)
    im2 = shadow(im, lambda dd, fill: dd.rectangle(box, fill=fill)); d = ImageDraw.Draw(im2); d.rectangle(box, fill=RED)
    d.text((x, yy), w, font=f, fill=WHITE, stroke_width=3, stroke_fill=INK); im.paste(im2); return box[2], box[3]
def depthline(im, x, y0, y1, ticks=8, arrow=True):
    d = ImageDraw.Draw(im, "RGBA"); d.line([(x, y0), (x, y1)], fill=(255, 255, 255, 235), width=4)
    for i in range(ticks + 1):
        yy = y0 + (y1 - y0) * i / ticks; ln = 26 if i % 2 == 0 else 14; d.line([(x - ln, yy), (x, yy)], fill=(255, 255, 255, 220), width=3)
    if arrow: d.polygon([(x - 20, y1 - 6), (x + 20, y1 - 6), (x, y1 + 30)], fill=RED)
def vign(im, s=0.5):
    a = np.asarray(im).astype(np.float32); yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H * 0.4) / (H / 2)) ** 2)
    a *= (1 - s * np.clip(d - 0.5, 0, 1) ** 1.3)[..., None]; return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def save(im, name):
    im = im.convert("RGB"); im.save(os.path.join(HERE, name + ".jpg"), quality=92, optimize=True)
    im.resize((246, 138), Image.LANCZOS).save(os.path.join(HERE, name + "_sidebar.png"))

def build():
    out = []
    # T1: ship near the top, long dark water, depth line on the right, 22,000 FT / DOWN
    t = abyss(surface_y=408); place_ship(t, 920, 20, 0); depthline(t, 1150, 60, 515)
    r, bt = word(t, "22,000 FT", 45, 428, 160); boxword(t, "DOWN", r + 38, 428, 160, 13); save(vign(t, .3), "T1_22000_ft_down"); out.append("T1_22000_ft_down")
    # T2: big ship vs the abyss
    t = abyss(surface_y=548); place_ship(t, 1240, 20, 0)
    r, bt = word(t, "DEEPEST", 50, 572, 130); boxword(t, "WRECK", r + 30, 572, 130, 10); save(vign(t, .3), "T2_deepest_wreck"); out.append("T2_deepest_wreck")
    # T3: Yamato looming, the little Roberts as a white-bordered inset (a different photo: no claim they are in one frame)
    y = P("cm_80_G_48888").crop((690, 560, 690 + 960, 560 + 540)).resize((W, H), Image.LANCZOS)
    arr = np.asarray(ImageEnhance.Contrast(y).enhance(1.25)).astype(np.float32) * np.array([0.80, 0.96, 1.2], np.float32)
    t = vign(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), .4)
    ins = abyss(surface_y=300); ins = ins.crop((0, 0, 560, 270)); place_ship(ins, 600, -20, -6)
    fr = Image.new("RGB", (ins.width + 12, ins.height + 12), WHITE); fr.paste(ins, (6, 6)); t.paste(shadow_rect(fr), (30, 430)) if False else None
    t = shadow(t, lambda d, fill: d.rectangle([30, 430, 30 + fr.width, 430 + fr.height], fill=fill), off=(8, 10), alpha=200, blur=10); t.paste(fr, (30, 430))
    _, bt = word(t, "THEY", 40, 30, 190); boxword(t, "CHARGED", 40, bt + 36, 190, 14); save(t, "T3_they_charged"); out.append("T3_they_charged")
    # T4: 4 MILES DOWN, ship top-right, gauge on the left, stacked words
    t = abyss(surface_y=345); place_ship(t, 820, 460, 0); depthline(t, 70, 40, 640)
    _, bt = word(t, "4 MILES", 130, 375, 190); boxword(t, "DOWN", 140, bt + 34, 130, 12); save(vign(t, .3), "T4_4_miles_down"); out.append("T4_4_miles_down")
    return out
def strip(names, suffix, sz, out):
    w, h = sz; m = Image.new("RGB", (w * len(names) + 10 * (len(names) + 1), h * 2 + 30), (15, 15, 15))
    for i, n in enumerate(names):
        t = Image.open(os.path.join(HERE, n + ".jpg")).resize(sz, Image.LANCZOS); x = 10 + i * (w + 10)
        m.paste(t, (x, 10)); m.paste(t.convert("L").convert("RGB"), (x, 20 + h))
    m.save(os.path.join(HERE, out))
if __name__ == "__main__":
    n = build(); strip(n, "", (246, 138), "contact_strip_246.png"); strip(n, "", (320, 180), "contact_strip_320.png"); print(n)
