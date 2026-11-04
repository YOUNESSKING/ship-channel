"""MOVE 3 control overlays (option 1, multiply look, same colours as tools/m1_make_control.py) for m3a-m3d + ending.
Union = BLUE (110,160,255); Confederates = RED (A4 240,105,95) + a bright rim on the red side; contested ground = no fill.
Polygons in lat/lon (FACTCHECK_C + the standard June 1864 campaign maps; ~2 km accuracy on the z12 maps, ~10 km on richmond z9).
  m3_ric_jun12  12 Jun: the Army of the Potomac at Cold Harbor + the Peninsula, Bermuda Hundred / City Point, the North, West Virginia.
  m3_ric_jun18  18 Jun: the army is south of the James (City Point to the lines east of Petersburg); Cold Harbor given up.
  m3_jam_jun14  14 Jun: north bank east of Warren's screen + the crossing; Bermuda Hundred; the Petersburg side contested (no fill).
  m3_pet_jun18  18 Jun: Union east of the new Confederate line at Petersburg, Bermuda Hundred, City Point.
usage (from grant/): python3 tools/m3_make_control.py   (uses <map>_hd_lift.json + <map>_land.png when baked, else the m3x_/ghx_ previews)"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m3_proj import proj
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PREV = {"richmond": "m3x_ric", "petersburg": "m3x_pet", "jamesriver": "ghx_jam", "mississippi": "m3x_mis"}

def base_of(m):
    return m if os.path.exists(f"{ROOT}/assets/{m}_hd_lift.json") else PREV[m]

def land_of(m):
    b = base_of(m); f = f"{ROOT}/assets/{m}_land.png"
    if not os.path.exists(f): f = f"{ROOT}/assets/{b}_land.png"
    land = np.array(Image.open(f).convert("L").resize((2880, 1620))) > 127 if os.path.exists(f) else np.ones((1620, 2880), bool)
    rv = f"{ROOT}/assets/media/{m}_det_riv.png"
    if os.path.exists(rv):
        w = np.array(Image.open(rv).split()[-1].resize((2880, 1620), Image.BILINEAR)) > 200
        land &= ~ndimage.binary_opening(w, iterations=2)
    return land

def render(land, hero, enemy, name):
    hero = hero & land; un = enemy & land & ~hero
    out = np.zeros(land.shape + (4,), np.float32)
    d = ndimage.distance_transform_edt(~hero)
    out[un, :3] = (240, 105, 95); out[un, 3] = (0.62 + 0.25 * np.exp(-d / 40.0))[un]
    out[hero, :3] = (110, 160, 255); out[hero, 3] = 0.565
    rim = ndimage.gaussian_filter((un & ndimage.binary_dilation(hero, iterations=3)).astype(np.float32), 3) * 3.0
    rim = np.clip(rim, 0, 1) * un; sel = rim > 0.35
    out[sel, :3] = (255, 130, 115); out[sel, 3] = np.maximum(out[sel, 3], 0.85)
    Image.fromarray(np.clip(out * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA").save(f"{ROOT}/assets/media/{name}_mx.png", optimize=True)
    print("wrote", name, f"union {hero.mean():.0%} conf {un.mean():.0%}")

def poly(P, pts):
    im = Image.new("L", (2880, 1620), 0); ImageDraw.Draw(im).polygon([tuple(map(float, P(*q))) for q in pts], fill=255); return np.array(im) > 0

ALL = [(60, -100), (60, -60), (20, -60), (20, -100)]
NORTH = [(38.0, -76.25), (38.4, -77.1), (38.7, -77.3), (38.9, -77.6), (39.2, -78.0), (39.35, -78.6), (39.0, -79.3), (38.5, -79.7), (38.0, -80.2),
         (37.5, -81.0), (37.2, -81.9), (36.6, -83.7), (40, -90), (45, -90), (45, -70), (38.0, -75.9)]
SHORE_E = [(38.0, -75.9), (37.0, -75.95), (36.9, -76.0), (36.6, -76.3), (36.55, -75.5), (38.3, -74.0)]      # Eastern Shore + Norfolk
NORFOLK = [(37.0, -76.62), (36.80, -76.62), (36.60, -76.45), (36.55, -75.8), (37.0, -75.8)]
CH_ARMY = [(37.80, -77.33), (37.66, -77.31), (37.60, -77.29), (37.55, -77.28), (37.50, -77.22), (37.45, -77.17), (37.40, -77.07), (37.33, -76.98),
           (37.24, -76.88), (37.20, -76.70), (37.05, -76.45), (36.95, -76.30), (37.10, -76.15), (37.35, -76.20), (37.55, -76.30), (37.57, -77.00), (37.72, -77.18)]
PENIN = [(37.24, -76.88), (37.36, -76.93), (37.48, -76.80), (37.55, -76.30), (37.35, -76.20), (37.10, -76.15), (36.95, -76.30), (37.05, -76.45), (37.20, -76.70)]
BERMUDA = [(37.392, -77.336), (37.36, -77.345), (37.31, -77.345), (37.295, -77.32), (37.30, -77.265), (37.33, -77.255), (37.37, -77.275), (37.40, -77.30)]
SOUTH18 = [(37.305, -77.345), (37.262, -77.362), (37.246, -77.372), (37.225, -77.378), (37.20, -77.382), (37.18, -77.37), (37.175, -77.25), (37.19, -77.10),
           (37.22, -76.98), (37.29, -77.03), (37.32, -77.10), (37.34, -77.20), (37.33, -77.27)]
NBANK14 = [(37.60, -77.21), (37.52, -77.20), (37.44, -77.225), (37.39, -77.235), (37.335, -77.17), (37.31, -77.10), (37.29, -77.05), (37.24, -76.88), (37.36, -76.93), (37.60, -76.50)]
SBANK14 = [(37.31, -77.13), (37.29, -77.13), (37.24, -77.12), (37.20, -77.05), (37.22, -76.95), (37.27, -77.0), (37.29, -77.06)]

def richmond():
    P = proj(base_of("richmond")); land = land_of("richmond"); A = poly(P, ALL)
    u = poly(P, NORTH) | poly(P, SHORE_E) | poly(P, NORFOLK) | poly(P, BERMUDA)
    render(land, u | poly(P, CH_ARMY), A, "m3_ric_jun12")
    render(land, u | poly(P, PENIN) | poly(P, SOUTH18), A, "m3_ric_jun18")

def jamesriver():
    P = proj(base_of("jamesriver")); land = land_of("jamesriver")
    u = poly(P, BERMUDA) | poly(P, NBANK14) | poly(P, SBANK14) | poly(P, PENIN)
    # red: north of the James west of Warren's screen, the Howlett line west of Bermuda Hundred, Petersburg and its ring
    red = poly(P, [(37.70, -77.60), (37.70, -77.235), (37.44, -77.245), (37.39, -77.25), (37.40, -77.31), (37.392, -77.336), (37.36, -77.35), (37.31, -77.35),
                   (37.262, -77.362), (37.246, -77.355), (37.21, -77.355), (37.17, -77.40), (36.9, -77.45), (36.9, -77.60)])
    render(land, u, red, "m3_jam_jun14")

def petersburg():
    P = proj(base_of("petersburg")); land = land_of("petersburg"); A = poly(P, ALL)
    u = poly(P, BERMUDA) | poly(P, SOUTH18) | poly(P, NBANK14) | poly(P, PENIN)
    # contested: north bank between Warren's old screen and the Bermuda Hundred front stays red (Lee's side of the river)
    render(land, u, A, "m3_pet_jun18")

def mississippi():
    P = proj(base_of("mississippi")); land = land_of("mississippi"); A = poly(P, ALL)
    im = Image.new("L", (2880, 1620), 0); d = ImageDraw.Draw(im)
    R = [(35.15, -90.06), (34.53, -90.59), (33.9, -91.1), (33.41, -91.06), (32.8, -91.17), (32.35, -90.90), (31.95, -91.20), (31.56, -91.40), (30.69, -91.27), (30.45, -91.19), (29.95, -90.07), (29.3, -89.6)]
    d.line([tuple(map(float, P(*q))) for q in R], fill=255, width=70, joint="curve")
    north = poly(P, [(35.0, -95), (35.0, -88.2), (34.9, -86), (36.6, -83.7), (40, -83), (40, -95)])     # July 1863: Union north of the Memphis-Corinth line
    gulf = poly(P, [(30.2, -92.5), (30.2, -89.8), (29.0, -89.0), (28.5, -92.5)])                          # New Orleans / lower Louisiana
    render(land, (np.array(im) > 0) | north | gulf, A, "m3_mis_jul")

if __name__ == "__main__":
    for f in (sys.argv[1:] or ["richmond", "jamesriver", "petersburg"]): globals()[f]()
