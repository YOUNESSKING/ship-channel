#!/usr/bin/env python3
"""make_polar_overlays.py  (NEW) -> assets/media/southern_band_0..6.png : smooth winter sea-ice ring around Antarctica, crisp slightly irregular outer edge,
gentle inner gradient; frame k has outer radius 601 px (today's winter edge) -> ~748 px (Ice Age, ~2x area) in 6 steps. Cross-fade them in the scene."""
import numpy as np, json
from PIL import Image
from scipy import ndimage
J = json.load(open("assets/southern_hd_ref.json")); CX, CY = J["center_px"]
ice = np.load("assets/src/southern_hd_ice.npy").reshape(1620, 2, 2880, 2).mean((1, 3)) > 0.5
H, W = ice.shape; yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); dx, dy = xx-CX, yy-CY; r = np.hypot(dx, dy); th = np.arctan2(dx, -dy)
rng = np.random.default_rng(4)
c = rng.normal(0, 1, 40); f = np.zeros_like(th)
for i in range(1, 12): f += (c[2*i]*np.cos(i*th) + c[2*i+1]*np.sin(i*th))/i**1.1
f = f/f.std()
def noise(sc):
    n = rng.normal(0, 1, (H//sc+3, W//sc+3)).astype(np.float32); return ndimage.zoom(n, sc, order=3)[:H, :W]
fine = noise(40)*0.7 + noise(18)*0.3
d = ndimage.distance_transform_edt(~ice)
for k in range(7):
    R = 601 + (748-601)*k/6
    edge = R + 7*f*(0.4+0.6*k/6) + 1.6*fine
    inner = np.clip((edge - r)/ (edge - 0.5*(edge.min()) + 1), 0, 1)
    a = np.clip((edge - r)/2.5 + 0.5, 0, 1)                        # crisp outer edge (~2.5 px feather)
    grad = 0.46 + 0.34*np.clip((r - 380)/(R - 380), 0, 1)           # brighter toward the outer edge
    rim = np.clip(1 - (edge - r)/9, 0, 1)*(edge > r)*0.12            # faint bright rim on the outer edge
    al = a*(grad + rim + 0.015*fine)*np.clip(d/4, 0, 1)
    rgb = np.broadcast_to(np.array([232, 243, 253], np.float32), (H, W, 3))
    Image.fromarray(np.dstack([rgb, np.clip(al, 0, 0.9)*255]).astype(np.uint8), "RGBA").save(f"assets/media/southern_band_{k}.png")
print("ok")
