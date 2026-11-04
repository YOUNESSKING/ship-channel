"""Who-controls-the-ground overlays for battle maps (STYLE_LOCK 2026-10-05: strong territory colours on every map).
Writes assets/media/<map>_ctl_<state>.png (map world px, 2880x1620): Allied #2e5cb2 / Axis #be3a2a, alpha 0.46 inside up to 0.66 at the
border, a two-colour front band where they meet, clipped to land (and off the water). Shapes per state are in map px below."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
W, H = 2880, 1620
COL = {"allied": (46, 92, 178), "axis": (190, 58, 42)}; LINE = {"allied": (44, 87, 183), "axis": (188, 37, 40)}
def mask(draw_fn):
    im = Image.new("L", (W, H), 0); draw_fn(ImageDraw.Draw(im)); return np.array(im) > 0
def holland_sep20(d):
    FRONT = [[0, 1390], [700, 1380], [950, 1345], [1200, 1330], [1450, 1340], [1700, 1320], [1950, 1300], [2880, 1290]]
    d.polygon([tuple(p) for p in FRONT] + [(2880, 1620), (0, 1620)], fill=255)          # Belgium / south of the old front
    ROAD = [(1240, 1370), (1250, 1300), (1290, 1220), (1309, 1091), (1316, 1035), (1336, 935), (1440, 790), (1506, 716), (1560, 680), (1593, 630)]
    d.line(ROAD, fill=255, width=96, joint="curve")                                      # the corridor along the road
    d.polygon([(1540, 640), (1650, 625), (1720, 660), (1730, 760), (1620, 790), (1540, 720)], fill=255)  # 82nd: Nijmegen + Groesbeek heights
    d.ellipse((1568, 452, 1604, 486), fill=255)                                           # British 1st Airborne pocket, Oosterbeek
def build(name, land, allied, water=None):
    m_al = allied & land; m_ax = land & ~allied
    if water is not None: m_al &= ~water; m_ax &= ~water
    out = np.zeros((H, W, 4), np.float32)
    for side, m, other in (("allied", m_al, m_ax), ("axis", m_ax, m_al)):
        dist = ndimage.distance_transform_edt(~other)
        a = np.where(m, 0.46 + 0.20 * np.exp(-dist / 50.0), 0).astype(np.float32)
        a = np.array(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), np.float32) / 255
        sel = a > 0.004; out[sel, :3] = COL[side]; out[sel, 3] = np.maximum(out[sel, 3], a[sel])
    for side, m, other in (("axis", m_ax, m_al), ("allied", m_al, m_ax)):
        band = m & ndimage.binary_dilation(other, iterations=4)
        out[band, :3] = LINE[side]; out[band, 3] = 0.9
    Image.fromarray(np.clip(out * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA").save(f"assets/media/{name}.png", optimize=True); print("wrote", name)
if __name__ == "__main__":
    hl = np.array(Image.open("assets/holland_land.png").convert("L")) > 127
    build("holland_ctl_sep20", hl, mask(holland_sep20))
    # Nijmegen: the south bank (city) Allied, the north bank German; after the crossing the north bank west of the road bridge is Allied
    water = np.array(Image.open("assets/nijmegen_water.png"))[..., 3] > 127
    land = ~water
    sep = land & ~ndimage.binary_dilation(water, iterations=2); sep[:6, :] = False; sep[:, -6:] = False; sep[:, :6] = False  # map edges as barriers
    lab, _ = ndimage.label(sep)
    south = lab == lab[1450, 1700]
    build("nijmegen_ctl_before", land, ndimage.binary_dilation(south, iterations=9), water)
    north_w = mask(lambda d: d.rectangle((0, 0, 1800, 1620), fill=255)) & ~south
    build("nijmegen_ctl_after", land, ndimage.binary_dilation(south, iterations=9) | north_w, water)
