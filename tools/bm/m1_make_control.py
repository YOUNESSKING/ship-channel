"""MOVE 1 control overlays (option 1, multiply look) for the Grant #16 move-1 scenes m1a/m1b/m1e/m1f.
Union = hero = BLUE (110,160,255); Confederates = RED (A4 lighter red 240,105,95) + a bright rim on the red side where they meet.
Water (det_riv mask) is left uncoloured. Fronts hand-placed from FACTCHECK_A (Memoirs ch. XXI-XXII) and the standard
campaign maps (Feb-Mar 1862): ~1 km accuracy on `donelson`, ~5 km on `henry`, ~20 km on `tennessee`.
  m1_henry_feb06a   6 Feb before the fall: Union north of the Kentucky-Tennessee line (landing above Fort Henry), Confederates south.
  m1_henry_feb06b   6 Feb after: Fort Henry and the river bend taken (Union).
  m1_don_feb12      12 Feb: Union around Fort Henry and the north; Confederates hold Donelson and the ground east.
  m1_don_feb13      13-15 Feb: the ring: Confederates inside the outer works + east of the Cumberland + the open south-east.
  m1_don_feb16      16 Feb after the surrender: the pocket Union; only the far south-east (toward Nashville) Confederate.
  m1_ten_feb06      6 Feb: the Columbus - Henry/Donelson - Bowling Green line (Mill Springs already lost, 19 Jan).
  m1_ten_mar        March 1862: Kentucky and much of middle Tennessee lost; the Tennessee River corridor Union.
usage (from grant/): python3 tools/m1_make_control.py"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m1_proj import proj
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def render(land, hero, name):
    hero = hero & land; un = land & ~hero
    out = np.zeros(land.shape + (4,), np.float32)
    d = ndimage.distance_transform_edt(~hero)
    out[un, :3] = (240, 105, 95); out[un, 3] = (0.62 + 0.25 * np.exp(-d / 40.0))[un]
    out[hero, :3] = (110, 160, 255); out[hero, 3] = 0.565
    rim = ndimage.gaussian_filter((un & ndimage.binary_dilation(hero, iterations=3)).astype(np.float32), 3) * 3.0
    rim = np.clip(rim, 0, 1) * land; sel = rim > 0.35
    out[sel, :3] = (255, 130, 115); out[sel, 3] = np.maximum(out[sel, 3], 0.85)
    Image.fromarray(np.clip(out * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA").save(f"{ROOT}/assets/media/{name}_mx.png", optimize=True)
    print("wrote", name, f"union {hero.mean():.0%}")

def poly(pts):
    im = Image.new("L", (2880, 1620), 0); ImageDraw.Draw(im).polygon([tuple(map(float, p)) for p in pts], fill=255); return np.array(im) > 0

def land_of(base):
    f = f"{ROOT}/assets/{base}_land.png"
    if os.path.exists(f): land = np.array(Image.open(f).convert("L").resize((2880, 1620))) > 127
    else: land = np.ones((1620, 2880), bool)
    rv = f"{ROOT}/assets/media/{base}_det_riv.png"
    if os.path.exists(rv):
        w = np.array(Image.open(rv).split()[-1].resize((2880, 1620), Image.BILINEAR)) > 200
        w = ndimage.binary_opening(w, iterations=2)          # keep the big water, drop hairline creeks
        land &= ~w
    return land

def henry():
    land = land_of("henry")
    a = [(0, 0), (2880, 0), (2880, 640), (2300, 660), (1900, 690), (1640, 720), (1480, 700), (1380, 706), (1330, 728), (1270, 735), (1100, 700), (600, 670), (0, 660)]
    render(land, poly(a), "m1_henry_feb06a")
    b = a[:7] + [(1480, 700), (1420, 740), (1400, 800), (1360, 840), (1300, 850), (1250, 820), (1230, 760), (1100, 700)] + a[-2:]
    render(land, poly(b), "m1_henry_feb06b")

def donelson():
    land = land_of("donelson")
    # 12 Feb: Union west of the ridge road / north
    u12 = [(0, 0), (1150, 0), (1180, 200), (1050, 300), (900, 420), (780, 600), (700, 800), (620, 1000), (560, 1300), (500, 1620), (0, 1620)]
    render(land, poly(u12), "m1_don_feb12")
    WORKS = [(1540, 811), (1487, 832), (1429, 825), (1371, 796), (1312, 753), (1289, 702), (1307, 651), (1324, 630)]
    # 13 Feb: Union = everything west/north of the works ring, bounded by the river to the north and the open south-east
    red = [(1324, 630), (1400, 600), (1480, 660), (1600, 650), (1720, 610), (1840, 590), (2000, 520), (2200, 400), (2500, 280), (2880, 230), (2880, 1620),
           (1800, 1620), (1700, 1200), (1620, 950)] + WORKS
    u13 = poly([(0, 0), (2880, 0), (2880, 1620), (0, 1620)]) & ~poly(red)
    render(land, u13, "m1_don_feb13")
    red16 = [(1720, 640), (1840, 600), (2000, 520), (2200, 400), (2500, 280), (2880, 230), (2880, 1620), (2100, 1620), (1950, 1250), (1850, 950), (1760, 760)]
    u16 = poly([(0, 0), (2880, 0), (2880, 1620), (0, 1620)]) & ~poly(red16)
    render(land, u16, "m1_don_feb16")

def tennessee():
    P = proj("tennessee"); land = land_of("tennessee"); L = lambda pts: [P(*q) for q in pts]
    # 6 Feb 1862: Union north of the Kentucky line; Confederates hold Columbus, Henry, Donelson, Bowling Green; Mill Springs (east) already lost
    n6 = L([(38.5, -92.5), (38.5, -83.0), (36.6, -83.0), (36.62, -84.2), (36.85, -85.2), (37.05, -86.0), (37.10, -86.5), (36.95, -87.2), (36.70, -87.75),
            (36.62, -88.05), (36.80, -88.55), (36.90, -88.95), (36.80, -89.30), (36.50, -89.60), (36.50, -92.5)])
    render(land, poly(n6), "m1_ten_feb06")
    # 16 Feb: both forts and the land between the rivers taken (the line is broken at the two rivers)
    pocket = L([(36.70, -88.15), (36.62, -88.20), (36.50, -88.12), (36.42, -88.05), (36.40, -87.85), (36.44, -87.72), (36.55, -87.68), (36.72, -87.70)])
    render(land, poly(n6) | poly(pocket), "m1_ten_feb16")
    # March 1862: Kentucky and much of middle Tennessee lost; west Tennessee (Memphis, Fort Pillow, Island No. 10) and east Tennessee still Confederate
    m3 = L([(38.5, -92.5), (38.5, -83.0), (36.6, -83.0), (36.55, -84.3), (36.0, -85.0), (35.6, -85.8), (35.45, -86.5), (35.35, -87.4), (35.25, -88.15),
            (35.6, -88.10), (36.1, -88.05), (36.45, -88.15), (36.52, -88.6), (36.52, -89.40), (36.58, -89.55), (36.50, -92.5)])
    render(land, poly(m3), "m1_ten_mar")

if __name__ == "__main__":
    for f in (sys.argv[1:] or ["henry", "donelson", "tennessee"]): globals()[f]()
