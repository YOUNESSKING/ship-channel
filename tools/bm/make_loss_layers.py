# Owner-approved 2026-10-29 (test E2): ground about to be lost turns PALER first, then changes side when the front moves.
# Splits a BEFORE -> AFTER territory change into three multiply layers in assets/media/:
#   <prefix>_<before>_rest_mx.png   unchanged ground (before colours)
#   <prefix>_<before>_lostR_mx.png  the ground that will be lost, in its BEFORE colour (fade it to opacity 0.4 over ~1.3 s on the cue)
#   <prefix>_<after>_lostB_mx.png   the same ground in its AFTER colour (fade it in over ~1 s when the front moves)
# Usage: python3 tools/make_loss_layers.py <ctl_prefix> <before> <after> [<before> <after> ...]
#   e.g. python3 tools/make_loss_layers.py atlanta_ctl jul03 jul10 jul10 jul22   (reads assets/media/atlanta_ctl_jul03_mx.png ...)
# Scene pattern: scenes-src/test-E2-lose.js (the `lay` / `loss` helpers).
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

prefix, pairs = sys.argv[1], sys.argv[2:]
assert pairs and len(pairs) % 2 == 0, __doc__
def load(d): return np.asarray(Image.open(f"assets/media/{prefix}_{d}_mx.png").convert("RGBA")).copy()
red = lambda X: (X[..., 0].astype(int) > X[..., 2].astype(int) + 40) & (X[..., 3] > 30)
blue = lambda X: (X[..., 2].astype(int) > X[..., 0].astype(int) + 40) & (X[..., 3] > 30)
def part(X, w):
    Y = X.copy(); Y[..., 3] = (Y[..., 3] * w).astype(np.uint8); return Y
for a, b in zip(pairs[::2], pairs[1::2]):
    A, B = load(a), load(b)
    lost = ndimage.binary_opening((red(A) & blue(B)) | (blue(A) & red(B)), iterations=2)
    soft = np.clip(ndimage.gaussian_filter(lost.astype(np.float32), 2.0), 0, 1)
    for nm, img in ((f"{prefix}_{a}_rest_mx.png", part(A, 1 - soft)), (f"{prefix}_{a}_lostR_mx.png", part(A, soft)),
                    (f"{prefix}_{b}_lostB_mx.png", part(B, soft))):
        Image.fromarray(img, "RGBA").save("assets/media/" + nm, optimize=True)
    print(a, "->", b, "changed px", int(lost.sum()))
