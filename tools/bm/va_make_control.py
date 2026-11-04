"""Map agent va: option-1 territory overlay (multiply) for the 1776 lake maps.
usage: python3 tools/va_make_control.py MAP [BORDER_LAT]  -> assets/media/va_<MAP>_ctl_mx.png
Land = DEM above the lake (elev > 29.8 m; Lake Champlain ~29 m), so the islands (Valcour, Grand Isle...) are land too.
Blue (110,160,255) = American ground south of BORDER_LAT (default 45.02: the Canadian line); red (240,105,95) = British Canada north of it."""
import json, math, sys
import numpy as np
from PIL import Image
from scipy import ndimage
m = sys.argv[1]; blat = float(sys.argv[2]) if len(sys.argv) > 2 else 45.02
J = json.load(open(f"assets/{m}_hd_lift.json")); z = J["zoom"]; ox, oy = J["origin_world_px"]
e = np.load(f"assets/src/{m}_hd_elev.npy"); H2, W2 = e.shape
land = ndimage.binary_opening(e > 29.8, iterations=2)
land = np.array(Image.fromarray(land.astype(np.uint8) * 255).resize((2880, 1620), Image.BILINEAR)).astype(np.float32) / 255
n = 256 * 2 ** z
yb = (1 - math.asinh(math.tan(math.radians(blat))) / math.pi) / 2 * n - oy   # map px row of the border
yy = np.arange(1620)[:, None] * np.ones((1, 2880))
red = (yy < yb)
out = np.zeros((1620, 2880, 4), np.uint8)
out[..., :3] = np.where(red[..., None], np.array([240, 105, 95]), np.array([110, 160, 255]))
out[..., 3] = (land * np.where(red, 158, 144)).astype(np.uint8)
Image.fromarray(out).save(f"assets/media/va_{m}_ctl_mx.png"); print(f"assets/media/va_{m}_ctl_mx.png border y={yb:.0f}")
# audit #35 (2026-11-03): soft version = a wavy, feathered border (no flat band, no hard edge), a cooler (less orange) red, lower alpha
xx = np.arange(2880)[None, :] * np.ones((1620, 1))
wav = 9 * np.sin(xx / 97.0) + 6 * np.sin(xx / 41.0 + 1.3) + 4 * np.sin(xx / 23.0 + 0.4)
fr = 1 / (1 + np.exp(-((yb + wav) - yy) / 16.0))          # 1 = British (north), 0 = American, feathered over ~60 px
rgb = fr[..., None] * np.array([214, 108, 122]) + (1 - fr[..., None]) * np.array([118, 160, 240])
al = land * (fr * 112 + (1 - fr) * 104)
out2 = np.zeros((1620, 2880, 4), np.uint8); out2[..., :3] = rgb.astype(np.uint8); out2[..., 3] = al.astype(np.uint8)
Image.fromarray(out2).save(f"assets/media/va_{m}_ctl_soft.png"); print(f"assets/media/va_{m}_ctl_soft.png")
