"""1-minute Oriskany test: Python/PIL frames -> ffmpeg. Every visual is timed to a narration chunk in timing.json.
Run: python3 render.py   (writes ../renders/video_noaudio.mp4; mix.sh adds the sound)"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
SRC = os.path.join(HERE, "../src"); OUTD = os.path.join(HERE, "../renders"); os.makedirs(OUTD, exist_ok=True)
W, H, FPS = 1920, 1080, 30
TM = json.load(open(os.path.join(HERE, "timing.json")))
C = {c["id"]: c["start"] for c in TM["chunks"]}; END = TM["duration"] + 0.4
FONT_B = os.path.join(ROOT, "tools/fonts/Anton-Regular.ttf"); FONT_L = os.path.join(ROOT, "tools/maps/oswald-latin-700-normal.ttf")
_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]
AMBER, WHITE, RED, INK = (232, 176, 74), (240, 236, 226), (214, 60, 48), (10, 16, 26)

def ease(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
def prog(t, a, b): return ease((t - a) / max(b - a, 1e-6))

# ---------------- maps ----------------
MAPS = {}
for n in ("gulf_z6", "pan_z10"):
    MAPS[n] = (Image.open(os.path.join(HERE, "maps", n + ".png")).convert("RGB"), json.load(open(os.path.join(HERE, "maps", n + ".json"))))
def gpx(lon, lat, z):
    s = 256 * 2 ** z; x = (lon + 180) / 360 * s
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * s
    return x, y
class Cam:
    def __init__(s, lon, lat, z): s.lon, s.lat, s.z = lon, lat, z
    def to_screen(s, lon, lat):
        cx, cy = gpx(s.lon, s.lat, s.z); x, y = gpx(lon, lat, s.z); return W / 2 + x - cx, H / 2 + y - cy
def lerp_cam(a, b, p):
    return Cam(a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p, a[2] + (b[2] - a[2]) * p)
def draw_map(cam, name=None):
    if name is None: name = "pan_z10" if cam.z > 8.2 else "gulf_z6"
    img, m = MAPS[name]; zr = m["z"]; f = 2 ** (zr - cam.z)
    cx, cy = gpx(cam.lon, cam.lat, zr); cx -= m["px0"]; cy -= m["py0"]
    box = (cx - W / 2 * f, cy - H / 2 * f, cx + W / 2 * f, cy + H / 2 * f)
    out = img.transform((W, H), Image.EXTENT, box, Image.BILINEAR)
    return vignette(out)
_vig = None
def vignette(im):
    global _vig
    if _vig is None:
        y, x = np.mgrid[0:H, 0:W]; r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
        _vig = np.clip(1.08 - 0.42 * r ** 2, 0.45, 1.0)[..., None].astype(np.float32)
    return Image.fromarray((np.asarray(im).astype(np.float32) * _vig * 0.92).astype(np.uint8))

REEF = (-87.0068, 30.0426)          # FWC: 30 02.555 N, 87 00.406 W
PCOLA_PASS = (-87.31, 30.325); PCOLA = (-87.217, 30.421); DESTIN = (-86.496, 30.393)
SSUS_APPROX = (-86.80, 30.13)       # ~22 NM SW of Destin (AP, Oct 2026); approximate, labelled as such

def text(d, xy, s, f, fill=WHITE, anchor="la", shadow=True, stroke=0):
    if shadow: d.text((xy[0] + 3, xy[1] + 3), s, font=f, fill=(0, 0, 0), anchor=anchor, stroke_width=stroke)
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))
def marker(d, x, y, t, col=AMBER, r=10):
    pr = (t * 1.2) % 1.0
    d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    R = r + 34 * pr; a = int(255 * (1 - pr))
    d.ellipse((x - R, y - R, x + R, y + R), outline=col + (a,), width=3)
def label_box(d, x, y, s, f, col=AMBER):
    tw = d.textlength(s, font=f); pad = 14
    d.rectangle((x, y, x + tw + 2 * pad, y + f.size + 2 * pad), fill=(8, 12, 20, 210))
    d.rectangle((x, y, x + 6, y + f.size + 2 * pad), fill=col)
    d.text((x + pad + 4, y + pad - 2), s, font=f, fill=WHITE)
def card(d, s, t0, t, size=150, y=H / 2, col=WHITE, sub=None):
    """Big number/text card that 'slams' in on its spoken word."""
    p = prog(t, t0, t0 + 0.25); sc = 1.25 - 0.25 * p
    f = font(FONT_B, int(size * sc))
    text(d, (W / 2, y), s, f, fill=col, anchor="mm", stroke=2)
    if sub: text(d, (W / 2, y + size * 0.75), sub, font(FONT_L, 40), fill=AMBER, anchor="mm")
def credit(d, s):
    d.text((40, H - 46), s, font=font(FONT_L, 22), fill=(220, 214, 200))

# ---------------- film ----------------
FILM = {}
def load_film(key, src, ss, dur):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur + 0.3), "-i", os.path.join(SRC, src), "-vf",
           "yadif,fps=30,scale=1440:1080:flags=lanczos,setsar=1,eq=contrast=1.06:saturation=0.92", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    FILM[key] = np.frombuffer(raw, np.uint8).reshape(-1, 1080, 1440, 3)
def film_frame(key, t_in, zoom=(1.0, 1.06), dur=3.0):
    fr = FILM[key]; i = min(int(t_in * FPS), len(fr) - 1)
    im = Image.fromarray(fr[i]); z = zoom[0] + (zoom[1] - zoom[0]) * min(t_in / dur, 1)
    if z != 1.0:
        w2, h2 = 1440 / z, 1080 / z; im = im.crop(((1440 - w2) / 2, (1080 - h2) / 2, (1440 + w2) / 2, (1080 + h2) / 2)).resize((1440, 1080), Image.BILINEAR)
    bg = im.resize((96, 54)).filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR)
    bg = Image.fromarray((np.asarray(bg) * 0.45).astype(np.uint8)); bg.paste(im, (240, 0))
    return bg

# ---------------- ship cross-section (side view, to scale: 1 ft = 1.6 px) ----------------
FT = 1.9
def carrier_poly(x0, keel_y, tilt=0.0):
    """Essex-class-ish side profile, bow to the right. Lengths in ft: 900 long, keel->flight deck ~62 ft,
    island top ~70 ft above deck (sits at ~80 ft depth on the wreck, deck ~150 ft: AP/FWC)."""
    L = 900; pts_hull = [(0, 0), (40, 18), (60, 30), (60, 62), (L - 60, 62), (L - 10, 62), (L, 58), (L - 70, 18), (L - 120, 0)]
    pts_hull = [(0, 0), (0, 30), (30, 62), (L, 62), (L + 25, 66), (L - 40, 30), (L - 120, 0)]
    island = [(520, 62), (520, 100), (540, 100), (545, 125), (560, 125), (565, 100), (640, 100), (640, 62)]
    mast = [(552, 125), (552, 132), (548, 132), (548, 125)]
    def tf(pts):
        out = []
        for (x, y) in pts:
            xx, yy = x - 450, y
            rx = xx * math.cos(tilt) - yy * math.sin(tilt); ry = xx * math.sin(tilt) + yy * math.cos(tilt)
            out.append((x0 + rx * FT, keel_y - ry * FT))
        return out
    return tf(pts_hull), tf(island), tf(mast)
def section(t, depth_ft=212, ship_keel_ft=212, tilt=0.0, show_ship=True, xray=0.0, charges=0.0, shake=0.0, ruler=0.0, zoom=1.0):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im, "RGBA")
    top = 290  # sea surface y
    for y in range(H):  # water gradient
        k = min(max((y - top) / (depth_ft * FT + 10), 0), 1)
        col = (int(30 - 22 * k), int(70 - 50 * k), int(92 - 58 * k)) if y >= top else (18, 26, 38)
        d.line((0, y, W, y), fill=col)
    d.line((0, top, W, top), fill=(150, 190, 205), width=2)
    sea_floor = top + depth_ft * FT
    for y in range(int(sea_floor), H):
        k = (y - sea_floor) / max(H - sea_floor, 1); d.line((0, y, W, y), fill=(int(58 - 30 * k), int(52 - 28 * k), int(40 - 22 * k))); d.line((0, sea_floor, W, sea_floor), fill=(120, 108, 80), width=3)
    text(d, (W - 40, top - 40), "SURFACE", font(FONT_L, 26), fill=(170, 200, 210), anchor="ra")
    if show_ship:
        sx = W / 2 + (math.sin(t * 40) * 6 * shake); ky = top + ship_keel_ft * FT + (math.cos(t * 37) * 4 * shake)
        hull, isl, mast = carrier_poly(sx, ky, tilt)
        fill = (68, 74, 80) if xray < 0.5 else (40, 46, 54)
        for poly in (hull, isl, mast):
            d.polygon(poly, fill=fill, outline=(150, 156, 160))
        if xray > 0:  # hidden inside: glowing compartments with question marks
            a = int(200 * xray)
            for i in range(7):
                cx = sx + (-330 + i * 110) * FT * 0.5 * 2 / 2
                d.rectangle((cx - 40, ky - 46, cx + 40, ky - 14), fill=(232, 176, 74, int(a * 0.35)), outline=(232, 176, 74, a), width=2)
                text(d, (cx, ky - 30), "?", font(FONT_B, 30), fill=(232, 176, 74), anchor="mm", shadow=False)
        if charges > 0:
            for i in range(9):
                cx = sx + (-360 + i * 90) * FT; on = (math.sin(t * 22 + i) > 0) or charges > 1.5
                if on: d.ellipse((cx - 9, ky - 16, cx + 9, ky - 2), fill=(255, 70, 50, int(255 * min(charges, 1))))
    if ruler > 0:
        x0 = W / 2 - 450 * FT; x1 = x0 + 900 * FT * ruler; y = sea_floor + 40
        d.line((x0, y, x1, y), fill=AMBER, width=4); d.line((x0, y - 12, x0, y + 12), fill=AMBER, width=4)
        if ruler >= 1: d.line((x1, y - 12, x1, y + 12), fill=AMBER, width=4)
    return im

# ---------------- shot list (start chunk -> painter) ----------------
def S(cid, off=0.0): return C[cid] + off
SHOTS = []  # (t0, t1, fn)
def shot(t0, t1):
    def deco(fn): SHOTS.append((t0, t1, fn)); return fn
    return deco

GULF_WIDE = (-89.5, 25.4, 6.7); PAN = (-87.0, 30.25, 8.6); DIVE = (-87.0068, 30.10, 10.6)

@shot(0, S("c02"))
def s1(t, d=None):  # wide Gulf -> panhandle; "24 MILES"
    p = prog(t, 0.0, S("c02") + 0.2); cam = lerp_cam(GULF_WIDE, PAN, p); im = draw_map(cam); d = ImageDraw.Draw(im, "RGBA")
    if cam.z < 7.8: text(d, cam.to_screen(-90.5, 25.5), "GULF OF MEXICO", font(FONT_L, 44), fill=(170, 200, 215), anchor="mm")
    text(d, cam.to_screen(-84.0, 30.9 if cam.z < 7.5 else 30.75), "FLORIDA", font(FONT_L, 48), fill=(225, 215, 185), anchor="mm")
    if t >= C["c01"]:
        a = cam.to_screen(*PCOLA_PASS); b = cam.to_screen(*REEF)
        q = prog(t, C["c01"], C["c01"] + 1.0); bb = (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)
        d.line((a, bb), fill=AMBER, width=4); marker(d, *b, t, r=7)
        label_box(d, 80, 80, "24 MILES OFF THE FLORIDA COAST", font(FONT_L, 46))
    return im

@shot(S("c02"), S("c03"))
def s2(t):  # dive to the reef site; depth counts to 212 FT
    p = prog(t, S("c02"), S("c03")); cam = lerp_cam(PAN, DIVE, p); im = draw_map(cam); d = ImageDraw.Draw(im, "RGBA")
    text(d, cam.to_screen(*PCOLA), "PENSACOLA", font(FONT_L, 40), anchor="mm")
    marker(d, *cam.to_screen(*REEF), t)
    depth = int(212 * prog(t, S("c02"), S("c02") + 0.7))
    gx, gy0, gy1 = W - 170, 160, 860
    d.rectangle((gx - 6, gy0, gx + 6, gy1), fill=(255, 255, 255, 60)); d.rectangle((gx - 6, gy0, gx + 6, gy0 + (gy1 - gy0) * depth / 212), fill=AMBER)
    text(d, (gx - 30, gy0 + (gy1 - gy0) * depth / 212), f"{depth} FT", font(FONT_B, 90), anchor="rm", stroke=1)
    return im

@shot(S("c03"), S("c04"))
def s3(t):  # cross-section: the carrier on the bottom
    im = section(t); d = ImageDraw.Draw(im, "RGBA")
    text(d, (W / 2, 110), "USS ORISKANY (CV-34)", font(FONT_L, 58), anchor="mm")
    text(d, (60, 290 + 212 * FT - 20), "212 FT", font(FONT_B, 54), fill=AMBER, anchor="ls")
    return im

@shot(S("c04"), S("c05"))
def s4(t):  # nearly 900 ft long
    im = section(t, ruler=prog(t, S("c04"), S("c04") + 0.6)); d = ImageDraw.Draw(im, "RGBA")
    text(d, (W / 2, 110), "USS ORISKANY (CV-34)", font(FONT_L, 58), anchor="mm")
    card(d, "NEARLY 900 FT", S("c04"), t, size=110, y=1010, col=AMBER)
    return im

@shot(S("c05"), S("c06"))
def s5(t):
    im = film_frame("launch", t - S("c05")); d = ImageDraw.Draw(im, "RGBA")
    card(d, "KOREA  ·  VIETNAM", S("c05") + 0.35, t, size=96, y=930, col=WHITE)
    credit(d, "USS Oriskany, 1967 · U.S. Navy film, National Archives (public domain)"); return im

@shot(S("c06"), S("c07"))
def s6(t):
    im = film_frame("island", t - S("c06")); d = ImageDraw.Draw(im, "RGBA")
    credit(d, "USS Oriskany, 1967 · U.S. Navy film, National Archives (public domain)"); return im

@shot(S("c07"), S("c08"))
def s7(t):
    im = film_frame("island2", t - S("c07")); d = ImageDraw.Draw(im, "RGBA")
    card(d, "THE U.S. NAVY", S("c07") + 0.2, t, size=120, y=930)
    credit(d, "USS Oriskany, 1967 · U.S. Navy film, National Archives (public domain)"); return im

@shot(S("c08"), S("c09"))
def s8(t):
    im = draw_map(Cam(-87.0068, 30.06, 10.2)); im = Image.fromarray((np.asarray(im) * 0.45).astype(np.uint8)); d = ImageDraw.Draw(im, "RGBA")
    card(d, "ON PURPOSE.", S("c08"), t, size=200); return im

@shot(S("c09"), S("c10"))
def s9(t):
    p = prog(t, S("c09"), S("c10")); cam = Cam(-87.0068, 30.06 + 0.02 * p, 10.0 + 0.4 * p); im = draw_map(cam); d = ImageDraw.Draw(im, "RGBA")
    marker(d, *cam.to_screen(*REEF), t); text(d, cam.to_screen(-87.0068, 30.0426 + 0.012), "REEF SITE", font(FONT_L, 34), anchor="mb")
    card(d, "MAY 17, 2006", S("c09"), t, size=150, y=300); return im

@shot(S("c10"), S("c10", 1.7))
def s10(t):  # afloat at the site
    im = section(t, ship_keel_ft=30); d = ImageDraw.Draw(im, "RGBA")
    text(d, (W / 2, 70), "MAY 17, 2006 · OFF PENSACOLA", font(FONT_L, 46), fill=AMBER, anchor="mm"); return im

@shot(S("c10", 1.7), S("c11"))
def s11(t):  # charges fire
    im = section(t, ship_keel_ft=30, charges=1.0 + prog(t, S("c10", 1.7), S("c10", 2.0)), shake=1.0); d = ImageDraw.Draw(im, "RGBA")
    label_box(d, 80, 70, "EXPLOSIVE CHARGES INSIDE THE HULL", font(FONT_L, 44), col=RED); return im

@shot(S("c11"), S("c12"))
def s12(t):  # 37 minutes: she settles
    p = prog(t, S("c11"), S("c12") + 1.6); im = section(t, ship_keel_ft=30 + 70 * p, tilt=-0.05 * p); d = ImageDraw.Draw(im, "RGBA")
    mins = int(37 * prog(t, S("c11"), S("c11") + 0.8)); card(d, f"{mins} MINUTES", S("c11"), t, size=130, y=980, col=AMBER); return im

@shot(S("c12"), S("c13"))
def s13(t):  # she was gone
    p = prog(t, S("c12") - 1.8, S("c12") + 1.4); im = section(t, ship_keel_ft=100 + 112 * p, tilt=-0.05 * (1 - p)); d = ImageDraw.Draw(im, "RGBA")
    for i in range(14):  # bubbles
        bx = W / 2 + ((i * 137) % 900) - 450; by = 290 + ((t * 120 + i * 53) % 360)
        d.ellipse((bx - 5, by - 5, bx + 5, by + 5), outline=(200, 230, 240, 160), width=2)
    return im

@shot(S("c13"), S("c14"))
def s14(t):
    im = film_frame("sea", t - S("c13")); d = ImageDraw.Draw(im, "RGBA")
    card(d, "3 YEARS", S("c13"), t, size=170, y=H / 2)
    credit(d, "U.S. Navy film, National Archives (public domain)"); return im

@shot(S("c14"), S("c15"))
def s15(t):
    im = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(im, "RGBA")
    v = 20 * prog(t, S("c14"), S("c14") + 0.9); card(d, f"${v:.0f} MILLION", S("c14"), t, size=190, col=AMBER, sub="TO GET HER READY TO SINK")
    return im

@shot(S("c15"), S("c16"))
def s16(t):
    im = film_frame("deck", t - S("c15")); d = ImageDraw.Draw(im, "RGBA")
    credit(d, "USS Oriskany, 1967 · U.S. Navy film, National Archives (public domain)"); return im

@shot(S("c16"), S("c16", 3.0))
def s17(t):
    im = film_frame("wake", t - S("c16")); d = ImageDraw.Draw(im, "RGBA")
    credit(d, "USS Oriskany, 1967 · U.S. Navy film, National Archives (public domain)"); return im

@shot(S("c16", 3.0), S("c17"))
def s18(t):  # "to the bottom of the sea"
    im = section(t); d = ImageDraw.Draw(im, "RGBA"); text(d, (W / 2, 70), "THE BOTTOM OF THE SEA", font(FONT_L, 52), anchor="mm"); return im

def options(t, d):
    items = [("KEEP HER", "c17"), ("SCRAP HER", "c18")]
    y0 = 330
    for i, (s, cid) in enumerate(items):
        if t < C[cid]: continue
        f = font(FONT_B, 120); y = y0 + i * 170
        text(d, (W / 2, y), s, f, anchor="mm", fill=(150, 150, 150) if t > C[cid] + 1.0 else WHITE)
        p = prog(t, C[cid] + 1.0, C[cid] + 1.3)
        if p > 0:
            tw = d.textlength(s, font=f); d.line((W / 2 - tw / 2 - 20, y, W / 2 - tw / 2 - 20 + (tw + 40) * p, y), fill=RED, width=12)
    if t >= C["c18"] + 1.6:
        card(d, "SINK HER", C["c18"] + 1.6, t, size=130, y=y0 + 2 * 170 + 10, col=AMBER)
@shot(S("c17"), S("c19"))
def s19(t):
    im = draw_map(Cam(-87.0068, 30.06, 10.2)); im = Image.fromarray((np.asarray(im) * 0.35).astype(np.uint8)); d = ImageDraw.Draw(im, "RGBA")
    options(t, d); return im

@shot(S("c19"), S("c19", 1.8))
def s20(t):
    im = section(t, ship_keel_ft=30, xray=prog(t, S("c19") + 0.6, S("c19") + 1.4)); return im
@shot(S("c19", 1.8), S("c20"))
def s21(t):
    im = section(t, ship_keel_ft=30, xray=1.0); d = ImageDraw.Draw(im, "RGBA")
    text(d, (W / 2, 70), "WHAT WAS HIDDEN INSIDE HER?", font(FONT_L, 56), fill=AMBER, anchor="mm"); return im

@shot(S("c20"), S("c20", 2.6))
def s22(t):  # pan east along the coast toward Destin
    p = prog(t, S("c20"), S("c20", 2.6)); cam = lerp_cam((-87.0, 30.15, 9.7), (-86.75, 30.25, 9.6), p); im = draw_map(cam); d = ImageDraw.Draw(im, "RGBA")
    text(d, cam.to_screen(*PCOLA), "PENSACOLA", font(FONT_L, 36), anchor="mm"); text(d, cam.to_screen(*DESTIN), "DESTIN", font(FONT_L, 36), anchor="mm")
    marker(d, *cam.to_screen(*REEF), t); return im
@shot(S("c20", 2.6), S("c21"))
def s23(t):
    cam = lerp_cam((-86.75, 30.25, 9.6), (-86.85, 30.22, 9.8), prog(t, S("c20", 2.6), S("c21"))); im = draw_map(cam); d = ImageDraw.Draw(im, "RGBA")
    text(d, cam.to_screen(*DESTIN), "DESTIN", font(FONT_L, 36), anchor="mm"); marker(d, *cam.to_screen(*REEF), t)
    x, y = cam.to_screen(*SSUS_APPROX); marker(d, x, y, t, col=WHITE)
    label_box(d, x + 30, y - 110, "SS UNITED STATES · SCHEDULED, NOV 2026", font(FONT_L, 36), col=WHITE)
    text(d, (x + 30, y - 30), "approx. site, ~22 NM off Destin", font(FONT_L, 24), fill=(210, 210, 200))
    return im
@shot(S("c21"), END)
def s24(t):
    cam = Cam(-86.9, 30.12, 9.6); im = draw_map(cam); d = ImageDraw.Draw(im, "RGBA")
    a, b = cam.to_screen(*REEF), cam.to_screen(*SSUS_APPROX); d.line((a, b), fill=(255, 255, 255, 120), width=2)
    marker(d, *a, t); marker(d, *b, t, col=WHITE)
    text(d, (a[0] - 30, a[1] + 30), "ORISKANY · 2006", font(FONT_L, 34), anchor="rt"); text(d, (b[0] + 30, b[1] - 30), "SS UNITED STATES · 2026", font(FONT_L, 34), anchor="lb")
    card(d, "THE SAME REASON", S("c21"), t, size=120, y=200, col=AMBER)
    fade = prog(t, END - 0.6, END)
    if fade > 0: im = Image.fromarray((np.asarray(im) * (1 - fade)).astype(np.uint8))
    return im

def main():
    # film clips: (key, file, start s, duration)
    clips = [("launch", 316, S("c06") - S("c05")), ("island", 164, S("c07") - S("c06")), ("island2", 270, S("c08") - S("c07")),
             ("sea", 564, S("c14") - S("c13")), ("deck", 146, S("c16") - S("c15")), ("wake", 320, 3.0)]
    for k, ss, dur in clips: load_film(k, "doolittle1967.mp4", ss, dur)
    n = int(END * FPS); out = os.path.join(OUTD, "video_noaudio.mp4")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    only = [float(a) for a in sys.argv[1:]]  # optional: render stills at given times
    if only:
        for tt in only:
            for t0, t1, fn in SHOTS:
                if t0 <= tt < t1: fn(tt).convert("RGB").save(os.path.join(OUTD, f"still_{tt:05.2f}.jpg"), quality=88)
        ff.stdin.close(); ff.wait(); return
    for i in range(n):
        t = i / FPS
        for t0, t1, fn in SHOTS:
            if t0 <= t < t1: im = fn(t); break
        else: im = Image.new("RGB", (W, H))
        ff.stdin.write(im.convert("RGB").tobytes())
        if i % 150 == 0: print(f"{t:5.1f}s", flush=True)
    ff.stdin.close(); ff.wait(); print("wrote", out)

if __name__ == "__main__": main()
