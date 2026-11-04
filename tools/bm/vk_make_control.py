"""Control overlays (option 1, multiply look) for Grant #16 move 2a/2c (map agent for m2a-m2d, Vicksburg).
Union = hero = BLUE (110,160,255); Confederacy = RED (A4 lighter red 240,105,95) + bright rim on the red side where they meet.
Land = HD elevation > 0.5 m minus the river water of the v11 detail layer (assets/media/<map>_det_riv.png), so the Mississippi
itself stays uncoloured and visibly splits the two banks. Fronts are hand-placed (~10-20 km on `mississippi`, ~3 km on `vicksburg`):
  vk_miss_ctl_apr1_mx.png  1 Apr 1863: Union = Kentucky / West + Middle Tennessee (front south of Murfreesboro, Corinth, La Grange, Memphis),
                           north + NW Arkansas and Helena, the Louisiana west bank Lake Providence - Milliken's Bend - Young's Point
                           (Grant's army), New Orleans - Baton Rouge - Brashear City (Banks). Confederacy: Mississippi, East TN,
                           Alabama, the river Vicksburg - Port Hudson, Louisiana, south Arkansas, Texas.
  vk_miss_ctl_apr1b_mx.png the same ground, B1 raid look (approved 2026-10-29): no Confederate fill, only a faint red glow where the
                           sides touch (Grierson's raid deep in enemy land).
  vk_vick_ctl_apr20_mx.png 20 Apr 1863 on `vicksburg`: Union on the Louisiana west bank from Milliken's Bend down to New Carthage /
                           Perkins' plantation; Confederacy: the east bank (Vicksburg, Grand Gulf, Port Gibson) and west Louisiana.
usage (from grant/): python3 tools/vk_make_control.py [miss] [vick]"""
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

def west_of_river(base):
    """True west of the main Mississippi channel (largest water body of the detail layer), row by row."""
    a = np.array(Image.open(f"assets/media/{base}_det_riv.png").convert("RGBA").resize((2880, 1620), Image.BILINEAR))[..., 3] > 150
    lab, n = ndimage.label(ndimage.binary_dilation(a, iterations=3))
    big = lab == (np.argmax(np.bincount(lab.ravel())[1:]) + 1)
    xs = np.arange(2880)[None, :].repeat(1620, 0)
    cnt = big.sum(1); xr = np.where(cnt > 0, (xs * big).sum(1) / np.maximum(cnt, 1), np.nan)
    ok = ~np.isnan(xr); xr = np.interp(np.arange(1620), np.arange(1620)[ok], xr[ok])
    xr = ndimage.uniform_filter1d(xr, 9)
    return xs < xr[:, None]

def render(land, hero, name, raid=False):
    hero = hero & land; un = land & ~hero
    out = np.zeros(land.shape + (4,), np.float32)
    d = ndimage.distance_transform_edt(~hero)
    out[un, :3] = (240, 105, 95)
    out[un, 3] = ((0.55 * np.exp(-d / 22.0)) if raid else (0.62 + 0.25 * np.exp(-d / 40.0)))[un]
    out[hero, :3] = (110, 160, 255); out[hero, 3] = 0.565
    if not raid:
        rim = ndimage.gaussian_filter((un & ndimage.binary_dilation(hero, iterations=3)).astype(np.float32), 3) * 3.0
        rim = np.clip(rim, 0, 1) * land; sel = rim > 0.35
        out[sel, :3] = (255, 130, 115); out[sel, 3] = np.maximum(out[sel, 3], 0.85)
    Image.fromarray(np.clip(out * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA").save(f"assets/media/{name}", optimize=True)
    print("wrote", name)

def mask(P, polys):
    im = Image.new("L", (2880, 1620), 0); dr = ImageDraw.Draw(im)
    for pts in polys: dr.polygon([tuple(P(*q)) for q in pts], fill=255)
    return np.array(im) > 0

def miss():
    P = proj("mississippi"); land = land_of("mississippi")
    north = [(38.0, -100.0), (38.0, -80.0), (36.75, -80.0), (36.70, -84.30), (36.20, -85.40), (35.80, -86.10), (35.62, -86.60), (35.40, -87.30),
             (35.10, -87.90), (34.82, -88.45), (34.80, -88.80), (34.95, -89.25), (34.98, -89.75), (34.85, -90.20),   # Corinth - La Grange - Memphis
             (34.62, -90.42), (34.42, -90.62), (34.58, -90.95), (35.05, -91.35), (35.45, -92.10), (35.62, -93.20), (35.72, -94.40), (35.75, -100.0)]
    westbank = [(33.22, -91.10), (33.05, -91.12), (32.80, -91.16), (32.60, -91.12), (32.48, -91.06), (32.40, -91.00), (32.36, -90.97), (32.33, -90.97),
                (32.33, -91.30), (32.70, -91.42), (33.00, -91.40), (33.22, -91.34)]   # east edge = the river (the z8 water layer is too broken to trace)
    south = [(30.66, -91.32), (30.56, -91.05), (30.50, -90.75), (30.33, -90.45), (30.22, -90.10), (30.20, -89.60), (30.30, -89.25), (28.0, -89.0),
             (28.0, -92.0), (29.55, -91.75), (29.95, -91.55), (30.30, -91.50), (30.52, -91.45)]
    hero = mask(P, [north, south, westbank])
    render(land, hero, "vk_miss_ctl_apr1_mx.png")
    render(land, hero, "vk_miss_ctl_apr1b_mx.png", raid=True)

def vick():
    P = proj("vicksburg"); land = land_of("vicksburg")
    W = west_of_river("vicksburg")
    apr1 = [(33.40, -90.60), (32.33, -90.60), (32.33, -91.30), (32.55, -91.40), (32.90, -91.45), (33.40, -91.47)]          # Lake Providence - Young's Point
    apr20 = [(33.40, -90.60), (32.02, -90.60), (32.02, -91.25), (32.25, -91.42), (32.55, -91.45), (32.90, -91.47), (33.40, -91.50)]   # + down to New Carthage
    render(land, mask(P, [apr1]) & W, "vk_vick_ctl_apr1_mx.png")
    render(land, mask(P, [apr20]) & W, "vk_vick_ctl_apr20_mx.png")

if __name__ == "__main__":
    a = sys.argv[1:] or ["miss", "vick"]
    if "miss" in a: miss()
    if "vick" in a: vick()
