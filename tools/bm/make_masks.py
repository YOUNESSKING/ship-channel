"""Build translucent North/South Korea overlay PNGs (split at lat 38, the 1950 line) for assets/korea.jpg.

usage: python3 tools/make_masks.py   (run from /home/user/battle-maps/ridgway; uses cached tiles only)
writes assets/korea_north.png, assets/korea_south.png (2880x1620 RGBA, feathered) and
assets/korea_land.npy (bool land mask inside the Korea polygon, for checking unit placement).
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
P = json.load(open(f"{ROOT}/assets/korea.json"))
Z, (OX, OY), (W, H) = P["zoom"], P["origin_world_px"], P["size"]
N = 256 * 2 ** Z


def px(lat, lon):
    return (lon + 180) / 360 * N - OX, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * N - OY


def tile(x, y):
    a = np.asarray(Image.open(f"{HERE}/.tiles/{Z}_{x}_{y}.png").convert("RGB"), float)
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768


tx0, ty0, tx1, ty1 = OX // 256, OY // 256, (OX + W) // 256, (OY + H) // 256
mosaic = np.vstack([np.hstack([tile(tx, ty) for tx in range(tx0, tx1 + 1)]) for ty in range(ty0, ty1 + 1)])
elev = mosaic[OY - ty0 * 256:OY - ty0 * 256 + H, OX - tx0 * 256:OX - tx0 * 256 + W]
land = elev > 0.5

# Korea polygon: Yalu + Tumen border in the north, open sea elsewhere (keeps out China, Shandong, Tsushima, Japan)
KOREA = [(39.70, 124.05), (39.95, 124.30), (40.10, 124.40), (40.30, 124.72), (40.46, 124.96), (40.70, 125.35),
         (40.95, 125.85), (41.15, 126.29), (41.45, 126.55), (41.75, 126.85), (41.62, 127.15), (41.55, 127.55), (41.45, 127.95),
         (41.40, 128.18), (41.75, 128.10), (42.2, 128.1), (42.2, 131.2),
         (41.0, 131.2), (38.5, 131.2), (36.5, 131.2), (35.35, 129.75), (34.6, 128.95), (33.8, 128.0),
         (33.0, 126.8), (33.0, 125.5), (34.2, 124.6), (36.5, 124.4), (37.8, 124.3), (38.6, 124.5), (39.3, 123.9)]
poly = Image.new("L", (W, H), 0)
ImageDraw.Draw(poly).polygon([px(la, lo) for la, lo in KOREA], fill=255)
korea = land & (np.asarray(poly) > 0)
np.save(f"{ROOT}/assets/korea_land.npy", korea)

y38 = px(38.0, 127)[1]
rows = np.arange(H)[:, None]


def overlay(sel, rgb, alpha, name):
    m = Image.fromarray((sel * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5))
    a = (np.asarray(m, float) / 255 * alpha * 255).astype(np.uint8)
    out = np.zeros((H, W, 4), np.uint8)
    out[..., :3] = rgb
    out[..., 3] = a
    Image.fromarray(out, "RGBA").save(f"{ROOT}/assets/{name}.png", optimize=True)
    print(name, "land px", int(sel.sum()))


overlay(korea & (rows < y38), (196, 24, 32), 0.42, "korea_north")
overlay(korea & (rows >= y38), (36, 86, 200), 0.34, "korea_south")
