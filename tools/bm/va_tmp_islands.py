"""Map agent va, TEMPORARY until logs/<map>_p2.done: the first bake painted the lake islands (Valcour, Grand Isle...) as water.
Paint them back as land (DEM above the lake, sand colour + hillshade + dark rim) into ONE scene's copy of the relief (never the shared asset).
usage: python3 tools/va_tmp_islands.py MAP SCENE"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
m, scene = sys.argv[1:3]
if os.path.exists(f"logs/{m}_p2.done"): print("p2 bake present: nothing to do"); sys.exit()
e = np.load(f"assets/src/{m}_hd_elev.npy")
dst = f"scenes/{scene}/assets/relief.jpg"; im = np.array(Image.open(f"assets/{m}_hd_lift.jpg").convert("RGB")).astype(np.float32)
land = e > 29.8; lab, n = ndimage.label(land)
gray = np.abs(im[..., 0] - im[..., 2]) < 30   # water in the bake is grey (r ~ b); land is sand (r >> b)
sz = ndimage.sum(np.ones_like(e), lab, range(1, n + 1)); wf = ndimage.sum(gray.astype(float), lab, range(1, n + 1)) / sz
isl = np.isin(lab, [i + 1 for i in range(n) if sz[i] > 300 and wf[i] > 0.6]); isl = ndimage.binary_opening(isl, iterations=3)
sand = np.median(im[(~gray) & land][::50], axis=0)
gy, gx = np.gradient(ndimage.gaussian_filter(e, 2) * 3 / 7.8); hs = np.clip(1 + (-gx * 0.7 + gy * 0.7) * 0.5, 0.75, 1.2)
col = sand[None, None, :] * hs[..., None]
a = ndimage.gaussian_filter(isl.astype(np.float32), 1.2)
rim = np.clip(ndimage.gaussian_filter(isl.astype(np.float32), 2.5) - a, 0, 1) * 0 + (np.abs(a - 0.5) < 0.35) * 1.0
out = im * (1 - a[..., None]) + col * a[..., None]
out = out * (1 - 0.45 * ndimage.gaussian_filter(rim, 1.0)[..., None])
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(dst, quality=92); print("temporary islands painted into", dst, int(isl.sum()), "px")
