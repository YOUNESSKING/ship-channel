#!/usr/bin/env python3
"""make_bering_ice.py (NEW) -> assets/media/beringia_seaice_0..3.png : perennial sea ice of the SE Bering Sea at the LGM as a smooth, crisp-edged pale band
hugging the new shelf-edge coast (distance-to-land band, irregular outer edge, gentle gradient); 4 growth frames to cross-fade. Prints the band centroid (map px)."""
import numpy as np, json, math
from PIL import Image
from scipy import ndimage
J = json.load(open("assets/beringia_lgm.json")); ox, oy = J["origin_world_px"]; N = 256*2**J["zoom"]
lg = np.load("assets/src/beringia_lgm_hd_elev.npy").reshape(1620, 2, 2880, 2).mean((1, 3))
land = lg > 0.5; H, W = land.shape
d = ndimage.distance_transform_edt(~land)
lon = ((ox + np.arange(W) + .5)/N*360 - 180)[None, :]*np.ones((H, 1))
rows = oy + np.arange(H) + .5; lat = np.degrees(np.arctan(np.sinh(math.pi*(1-2*rows/N))))[:, None]*np.ones((1, W))
rng = np.random.default_rng(8)
def noise(sc):
    n = rng.normal(0, 1, (H//sc+3, W//sc+3)).astype(np.float32); return ndimage.zoom(n, sc, order=3)[:H, :W]
irr = noise(90)*0.65 + noise(34)*0.35; fine = noise(30)
east = np.clip((lon + 190)/10, 0, 1)                      # fades out toward the Siberian/western end: the ice was a SE Bering feature
sea = ~land & (lat > 51) & (lat < 63)
for k in range(8):
    R = 40 + 150*k/7
    edge = R*(0.85 + 0.35*east) + 14*irr
    a = np.clip((edge - d)/2.5 + 0.5, 0, 1)*sea*east
    grad = 0.50 + 0.32*np.clip(d/np.maximum(edge, 1), 0, 1)
    al = a*(grad + 0.02*fine)*np.clip(d/3, 0, 1)
    rgb = np.broadcast_to(np.array([234, 244, 253], np.float32), (H, W, 3))
    Image.fromarray(np.dstack([rgb, np.clip(al, 0, 0.9)*255]).astype(np.uint8), "RGBA").save(f"assets/media/beringia_seaice_{k}.png")
m = (al > 0.3); ys, xs = np.nonzero(m); print("centroid", int(xs.mean()), int(ys.mean()), "bbox", xs.min(), xs.max(), ys.min(), ys.max())
