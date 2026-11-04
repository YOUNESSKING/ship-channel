"""Option 2 (owner 2026-10-06): trace the two-colour front lines from a control overlay (axis red / allied blue pixels) instead of
filling territory. Output: JSON list of polylines in map px, oriented so the allied side is on the LEFT of travel (K.front sideA).
usage: python3 tools/make_front_lines.py OVERLAY.png OUT.json [MINLEN]"""
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage
from skimage import measure
im = np.array(Image.open(sys.argv[1]).convert("RGBA")).astype(int); MINLEN = float(sys.argv[3]) if len(sys.argv) > 3 else 120
on = im[..., 3] > 20
axis = on & (im[..., 0] > im[..., 2] + 40); ally = on & (im[..., 2] > im[..., 0] + 40)
axis = ndimage.binary_opening(axis, iterations=6)  # drop the thin red coast rim; ally = ndimage.binary_opening(ally, iterations=2)
near_ally = ndimage.binary_dilation(ally, iterations=7)
lines = []
for c in measure.find_contours(axis.astype(float), 0.5):
    keep = near_ally[np.clip(c[:, 0].astype(int), 0, axis.shape[0] - 1), np.clip(c[:, 1].astype(int), 0, axis.shape[1] - 1)]
    # split the contour into runs that touch allied ground
    runs, cur = [], []
    for p, k in zip(c, keep):
        if k: cur.append(p)
        elif cur: runs.append(cur); cur = []
    if cur: runs.append(cur)
    for r in runs:
        r = np.array(r)
        if len(r) < 2 or np.hypot(*np.diff(r, axis=0).T).sum() < MINLEN: continue
        r = measure.approximate_polygon(r, tolerance=2.5)
        # light smoothing (Chaikin x2) so the band reads as a drawn front, not pixel steps
        for _ in range(2):
            q = [r[0]]
            for a, b in zip(r[:-1], r[1:]): q += [0.75 * a + 0.25 * b, 0.25 * a + 0.75 * b]
            r = np.array(q + [r[-1]])
        pts = [[round(float(p[1]), 1), round(float(p[0]), 1)] for p in r]
        # orient: allied side on the left of travel
        sc = 0
        for (x0, y0), (x1, y1) in zip(pts[:-1:3], pts[1::3]):
            dx, dy = x1 - x0, y1 - y0; L = np.hypot(dx, dy) or 1
            lx, ly = int(x0 + dy / L * 12), int(y0 - dx / L * 12)   # left normal in screen coords (y down)
            if 0 <= ly < axis.shape[0] and 0 <= lx < axis.shape[1]: sc += (1 if ally[ly, lx] else 0) - (1 if axis[ly, lx] else 0)
        lines.append(pts if sc >= 0 else pts[::-1])
json.dump(lines, open(sys.argv[2], "w"))
print(len(lines), "front lines,", sum(len(l) for l in lines), "points")
