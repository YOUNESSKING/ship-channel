"""Control overlays (option 1, multiply look) for Grant #16 m2e-m2g (map agent vx). Same colours / land mask as tools/vk_make_control.py
(Union BLUE 110,160,255; Confederacy A4 lighter red 240,105,95 + bright rim; the river water itself left uncoloured).
Fronts hand-placed from FACTCHECK_B (#11, #14-#19, #24, #27) and Grant's Memoirs chs. XXXIV-XXXV; ~3-6 km precision on `vicksburg` (z10):
  vx_vick_may03_mx  ~1-3 May 1863: west bank (Milliken's Bend - Hard Times) + the bridgehead Bruinsburg - Port Gibson - Grand Gulf - Rocky Springs.
  vx_vick_may12_mx  12 May: + the corridor north-east by Utica to Raymond.
  vx_vick_may14_mx  14 May: + Clinton and Jackson.
  vx_vick_may16_mx  16-17 May: Jackson given up again (the army turned back west); + Bolton - Champion Hill - Edwards - Big Black.
  vx_vick_may18_mx  18 May: + the ground east and north of Vicksburg to Haines Bluff; the city inside its lines stays red (the pocket).
  vx_miss_apr_mx    `mississippi` spring 1863 = the vk 1 Apr ground (west-bank strip, Memphis/Helena north, New Orleans - Baton Rouge south).
  vx_miss_jul_mx    `mississippi` July 1863: the whole river Union (a corridor along both banks Memphis - Vicksburg - Port Hudson - New Orleans):
                    the Confederacy cut in two.
usage (from grant/): python3 tools/vx_make_control.py [vick] [miss]"""
import json, math, sys, os
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

def proj(base):
    J = json.load(open(f"assets/{base}_hd_lift.json")); Z, (OX, OY) = J["zoom"], J["origin_world_px"]
    def P(lat, lon):
        n = 256 * 2 ** Z; r = math.radians(lat)
        return ((lon + 180) / 360 * n - OX, (1 - math.asinh(math.tan(r)) / math.pi) / 2 * n - OY)
    return P

def land_of(base):
    e = np.load(f"assets/src/{base}_hd_elev.npy")
    land = np.array(Image.fromarray((e > 0.5).astype(np.uint8) * 255).resize((2880, 1620), Image.BILINEAR)) > 127
    rp = f"assets/media/{base}_det_riv.png"
    if os.path.exists(rp):
        w = np.array(Image.open(rp).convert("RGBA").resize((2880, 1620), Image.BILINEAR))[..., 3] > int(os.environ.get("WATER_A", "150"))
        w = ndimage.binary_opening(w, iterations=1)
        land &= ~w
    return land

def render(land, hero, name):
    hero = hero & land; un = land & ~hero
    out = np.zeros(land.shape + (4,), np.float32)
    d = ndimage.distance_transform_edt(~hero)
    out[un, :3] = (240, 105, 95); out[un, 3] = (0.62 + 0.25 * np.exp(-d / 40.0))[un]
    out[hero, :3] = (110, 160, 255); out[hero, 3] = 0.565
    rim = ndimage.gaussian_filter((un & ndimage.binary_dilation(hero, iterations=3)).astype(np.float32), 3) * 3.0
    rim = np.clip(rim, 0, 1) * land; sel = rim > 0.35
    out[sel, :3] = (255, 130, 115); out[sel, 3] = np.maximum(out[sel, 3], 0.85)
    Image.fromarray(np.clip(out * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA").save(f"assets/media/{name}", optimize=True)
    print("wrote", name)

def mask(P, polys, lines=(), circles=()):
    im = Image.new("L", (2880, 1620), 0); dr = ImageDraw.Draw(im)
    for pts in polys: dr.polygon([tuple(P(*q)) for q in pts], fill=255)
    for pts, w in lines: dr.line([tuple(P(*q)) for q in pts], fill=255, width=int(w), joint="curve")
    for (la, lo), r in circles: x, y = P(la, lo); dr.ellipse([x - r, y - r, x + r, y + r], fill=255)
    return np.array(im) > 0

def vick():
    P = proj("vicksburg"); land = land_of("vicksburg")
    westbank = [(33.40, -91.18), (33.05, -91.12), (32.82, -91.13), (32.62, -91.11), (32.47, -91.02), (32.36, -90.93), (32.32, -90.90),
                (32.28, -90.93), (32.20, -90.98), (32.12, -91.02), (32.06, -91.08), (32.02, -91.12), (31.96, -91.20),
                (32.02, -91.42), (32.25, -91.45), (32.55, -91.48), (32.90, -91.50), (33.40, -91.52)]
    bridge = [(31.90, -91.20), (31.945, -91.17), (32.00, -91.10), (32.045, -91.06), (32.10, -91.00), (32.15, -90.92), (32.12, -90.80),
              (32.06, -90.76), (31.97, -90.86), (31.90, -90.93), (31.87, -91.05)]
    to_ray = [(32.15, -90.92), (32.20, -90.80), (32.27, -90.50), (32.30, -90.40), (32.24, -90.36), (32.15, -90.48), (32.05, -90.65), (32.06, -90.76), (32.12, -90.80)]
    to_jax = [(32.30, -90.46), (32.37, -90.36), (32.36, -90.24), (32.37, -90.12), (32.27, -90.10), (32.22, -90.22), (32.24, -90.36)]
    west = [(32.20, -90.80), (32.30, -90.74), (32.375, -90.70), (32.385, -90.55), (32.37, -90.45), (32.30, -90.40), (32.27, -90.50)]
    lines = [(32.20, -90.90), (32.24, -90.80), (32.33, -90.79), (32.40, -90.80), (32.47, -90.82), (32.50, -90.78), (32.45, -90.70), (32.375, -90.70), (32.30, -90.74), (32.20, -90.80), (32.15, -90.92)]
    render(land, mask(P, [westbank, bridge]), "vx_vick_may03_mx.png")
    render(land, mask(P, [westbank, bridge, to_ray]), "vx_vick_may12_mx.png")
    render(land, mask(P, [westbank, bridge, to_ray, to_jax]), "vx_vick_may14_mx.png")
    render(land, mask(P, [westbank, bridge, to_ray, west]), "vx_vick_may16_mx.png")
    hero = mask(P, [westbank, bridge, to_ray, west, lines])
    # the pocket: Vicksburg inside its lines (about 4-5 km round the city, open to the river)
    pocket = mask(P, [[(32.405, -90.885), (32.40, -90.845), (32.37, -90.83), (32.33, -90.835), (32.30, -90.855), (32.285, -90.885), (32.30, -90.91),
                       (32.34, -90.90), (32.38, -90.91)]])
    render(land, hero & ~pocket, "vx_vick_may18_mx.png")

def miss():
    P = proj("mississippi"); land = land_of("mississippi")
    north = [(38.0, -100.0), (38.0, -80.0), (36.75, -80.0), (36.70, -84.30), (36.20, -85.40), (35.80, -86.10), (35.62, -86.60), (35.40, -87.30),
             (35.10, -87.90), (34.82, -88.45), (34.80, -88.80), (34.95, -89.25), (34.98, -89.75), (34.85, -90.20),
             (34.62, -90.42), (34.42, -90.62), (34.58, -90.95), (35.05, -91.35), (35.45, -92.10), (35.62, -93.20), (35.72, -94.40), (35.75, -100.0)]
    westbank = [(33.22, -91.16), (33.05, -91.10), (32.82, -91.13), (32.62, -91.12), (32.45, -91.02), (32.33, -90.97), (32.30, -91.06),
                (32.42, -91.30), (32.70, -91.42), (33.00, -91.40), (33.22, -91.34)]
    south = [(30.66, -91.32), (30.56, -91.05), (30.50, -90.75), (30.33, -90.45), (30.22, -90.10), (30.20, -89.60), (30.30, -89.25), (28.0, -89.0),
             (28.0, -92.0), (29.55, -91.75), (29.95, -91.55), (30.30, -91.50), (30.52, -91.45)]
    render(land, mask(P, [north, westbank, south]), "vx_miss_apr_mx.png")
    # July 1863: the river corridor (Memphis -> New Orleans), ~12-15 km each side, plus the Vicksburg - Jackson ground of the campaign
    riv = [(35.15, -90.07), (34.80, -90.30), (34.53, -90.58), (34.15, -90.85), (33.75, -91.05), (33.40, -91.08), (33.05, -91.12), (32.80, -91.16),
           (32.60, -91.12), (32.48, -91.06), (32.40, -91.00), (32.37, -90.90), (32.30, -90.90), (32.13, -91.04), (31.95, -91.16), (31.56, -91.42),
           (31.20, -91.58), (31.00, -91.62), (30.70, -91.32), (30.45, -91.20), (30.20, -91.08), (29.95, -90.07)]
    J = json.load(open("assets/mississippi_hd_lift.json")); w = 2 * 13000 / J["meters_per_px"]
    vj = [(32.45, -90.95), (32.42, -90.70), (32.36, -90.40), (32.20, -90.40), (32.20, -90.95)]
    render(land, mask(P, [north, westbank, south, vj], lines=[(riv, w)]), "vx_miss_jul_mx.png")

if __name__ == "__main__":
    a = sys.argv[1:] or ["vick", "miss"]
    if "vick" in a: vick()
    if "miss" in a: miss()
