"""Who-controls-the-ground overlays (option 1, multiply look) for the Grant #16 hook (map agent hook, prefix gh_; other agents may reuse
them read-only). SIDES: Union (hero) = BLUE (110,160,255) alpha 0.565; Confederates = RED, A4 lighter red (240,105,95), 0.62 + 0.2 near
the border; a two-colour rim where the sides touch (blue on the Union side, red on the Confederate side). Water (det_riv) is left clear.
One lat/lon definition per date, rendered into every map's pixel space so the maps match during the continuous zoom:
  feb62   early Feb 1862, before Fort Henry: Confederate line Columbus (Mississippi) - Hopkinsville - Bowling Green in southern Kentucky
          (Grant, Memoirs ch. XXI: "a line running from the Mississippi River at Columbus to Bowling Green and Mill Springs"; Mill Springs
          lost 19 Jan), New Madrid pocket (Missouri bootheel) Confederate; Paducah, Smithland, Cairo Union; Tennessee, Arkansas,
          Mississippi, Alabama Confederate. Approximate to ~5-10 km (fine for z9/z11).
  feb14   (donelson map) the Union corridor from Fort Henry to the ring round the fort; the pocket (outer works, fort, Dover) Confederate.
  feb16   (donelson map) after the surrender: the whole Dover side of the Cumberland Union; the far bank Confederate.
-> assets/media/gh_<map>_ctl_<date>_mx.png (2880 x 1620)
usage (from grant/): python3 tools/gh_make_control.py [map:date ...]"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

STATES = "/home/user/battle-maps/sherman/assets/src/south_ne_states.geojson"
W, H = 2880, 1620

def proj(m):
    J = json.load(open(f"assets/{m}_hd_lift.json")); Z = J["zoom"]; OX, OY = J["origin_world_px"]
    def P(lat, lon):
        n = 256 * 2 ** Z; r = math.radians(lat)
        return ((lon + 180) / 360 * n - OX, (1 - math.asinh(math.tan(r)) / math.pi) / 2 * n - OY)
    return P

def rings(g):
    return [g["coordinates"][0]] if g["type"] == "Polygon" else [p[0] for p in g["coordinates"]]

def poly_mask(P, polys):
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im)
    for poly in polys: d.polygon([P(*q) for q in poly], fill=255)
    return np.array(im) > 0

UNION_STATES = {"Illinois", "Indiana", "Ohio", "Missouri", "Kentucky", "West Virginia", "Pennsylvania", "Maryland"}
# Confederate-held southern Kentucky (south of this line), Feb 1862
KY_CSA = [(36.95, -89.40), (36.88, -89.12), (36.84, -88.90), (36.78, -88.62), (36.71, -88.32), (36.72, -88.05), (36.85, -87.72),
          (36.98, -87.45), (37.10, -87.08), (37.18, -86.62), (37.20, -86.20), (37.08, -85.85), (36.85, -85.55), (36.62, -85.35),
          (36.40, -85.35), (36.40, -89.60)]
NEW_MADRID = [(35.90, -90.60), (36.62, -90.60), (36.74, -90.10), (36.66, -89.40), (35.90, -89.40)]   # the bootheel + New Madrid
# Fort Donelson (donelson map): the Confederate pocket inside the outer works (Hickman Creek - west arc - Indian/Lick Creek), lat/lon
POCKET = [(36.4985, -87.8565), (36.4962, -87.8700), (36.4950, -87.8790), (36.4890, -87.8835), (36.4815, -87.8800), (36.4755, -87.8705),
          (36.4720, -87.8575), (36.4712, -87.8440), (36.4740, -87.8330), (36.4820, -87.8290), (36.4900, -87.8300), (36.4960, -87.8420)]
# Union corridor Fort Henry -> Donelson (13-14 Feb): west edge of the map to the ring
CORRIDOR = [(36.565, -88.20), (36.540, -87.98), (36.520, -87.90), (36.505, -87.880), (36.500, -87.866), (36.4985, -87.8565),
            (36.4962, -87.8420), (36.4900, -87.8300) , (36.4820, -87.8290), (36.4740, -87.8330), (36.4690, -87.8450), (36.455, -87.880),
            (36.440, -87.940), (36.420, -88.20)]
# Union ground 12-14 Feb: the roads from Fort Henry (Tennessee River) to the ring, and the ring itself (outside the pocket, to the river)
ROADS14 = [(36.513, -88.06), (36.505, -87.99), (36.497, -87.94), (36.490, -87.900)]
RINGOUT = [(36.507, -87.860), (36.505, -87.890), (36.495, -87.905), (36.478, -87.900), (36.466, -87.880), (36.462, -87.855), (36.466, -87.835),
           (36.4715, -87.8440), (36.4740, -87.8330), (36.4820, -87.8290), (36.4900, -87.8300), (36.4985, -87.8565)]
# after the surrender: the Dover (south-west) side of the Cumberland. The river line (north -> Dover -> east edge), traced on the relief
CUMB_SW = [(36.62, -87.97), (36.56, -87.92), (36.525, -87.885), (36.505, -87.866), (36.4975, -87.8560), (36.4935, -87.8460),
           (36.4895, -87.8380), (36.4910, -87.8250), (36.4975, -87.8100), (36.5010, -87.7900), (36.4950, -87.7700), (36.4800, -87.7500),
           (36.4600, -87.7300), (36.4300, -87.7100), (36.3500, -87.7000), (36.3500, -88.20), (36.62, -88.20)]

def water(m):
    f = f"assets/media/{m}_det_riv.png"
    if not os.path.exists(f): return np.zeros((H, W), bool)
    a = np.array(Image.open(f).convert("RGBA").resize((W, H), Image.BILINEAR))[:, :, 3]
    return a > 110

def build(m, date):
    P = proj(m)
    land = ~water(m)
    if date == "feb62":
        SM = {f["properties"]["name"]: poly_mask(P, [[(la, lo) for lo, la in r] for r in rings(f["geometry"])]) for f in json.load(open(STATES))["features"]}
        allst = np.zeros((H, W), bool)
        for v in SM.values(): allst |= v
        un = np.zeros((H, W), bool)
        for s in UNION_STATES: un |= SM.get(s, np.zeros((H, W), bool))
        un &= ~(SM["Kentucky"] & poly_mask(P, [KY_CSA]))
        un &= ~(SM["Missouri"] & poly_mask(P, [NEW_MADRID]))
        # states not in the file (north of the frame edge etc.): leave them to the nearest state's side
        if (~allst).any():
            idx = ndimage.distance_transform_edt(~allst, return_distances=False, return_indices=True)
            un = un[idx[0], idx[1]]
    elif date == "feb05":
        un = np.zeros((H, W), bool)
    elif date == "feb14":   # a band round the roads Fort Henry -> Donelson (~7 km wide) closing on the ring; the pocket stays Confederate
        im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im); J = json.load(open(f"assets/{m}_hd_lift.json"))
        wpx = 7000 / J["meters_per_px"]
        path = [P(*q) for q in ROADS14]
        d.line(path, fill=255, width=int(wpx), joint="curve")
        for q in (path[0], path[-1]): d.ellipse([q[0] - wpx / 2, q[1] - wpx / 2, q[0] + wpx / 2, q[1] + wpx / 2], fill=255)
        ring = [P(*q) for q in RINGOUT]; d.polygon(ring, fill=255)
        un = (ndimage.gaussian_filter((np.array(im) > 0).astype(np.float32), max(2, wpx / 8)) > 0.5) & ~poly_mask(P, [POCKET])
    elif date == "feb16":
        un = poly_mask(P, [CUMB_SW])
    if m == "donelson" and date != "feb05":   # round the hand-drawn corners (the pocket stays within ~100 m)
        un = ndimage.gaussian_filter(un.astype(np.float32), 6) > 0.5
    un = un & land; csa = land & ~un
    out = np.zeros((H, W, 4), np.float32)
    k = 1.0 if m == "donelson" else (0.5 if m == "henry" else 0.3)        # rim width in map px scales with the map zoom
    dU = ndimage.distance_transform_edt(~csa); dC = ndimage.distance_transform_edt(~un)
    out[un, :3] = (110, 160, 255); out[un, 3] = 0.565
    out[csa, :3] = (240, 105, 95); out[csa, 3] = (0.62 + 0.2 * np.exp(-dC / (40.0 * k)))[csa]
    if un.any() and csa.any():
        rimU = un & (dU < 7 * max(k, 0.6)); rimC = csa & (dC < 7 * max(k, 0.6))
        out[rimU, :3] = (70, 120, 235); out[rimU, 3] = 0.85
        out[rimC, :3] = (215, 60, 55); out[rimC, 3] = 0.88
    # soft edge so the colour fades in, not a hard cut-out, around the water
    a = ndimage.gaussian_filter(out[:, :, 3], 1.0)
    out[:, :, 3] = np.where(land, np.maximum(a, out[:, :, 3] * 0.9), a * 0.5)
    Image.fromarray(np.clip(out * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA").save(f"assets/media/gh_{m}_ctl_{date}_mx.png", optimize=True)
    print("wrote", f"gh_{m}_ctl_{date}_mx.png", int(un.sum()), int(csa.sum()))

if __name__ == "__main__":
    for a in sys.argv[1:] or ["tennessee:feb62", "henry:feb62", "donelson:feb05", "donelson:feb14", "donelson:feb16"]:
        m, d = a.split(":"); build(m, d)
