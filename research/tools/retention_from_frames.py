import numpy as np, json
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
def read(frame, D):
    path = f"/tmp/gf3/full/{frame}.png"
    im = np.array(Image.open(path).convert("RGB")).astype(int)
    r, _ = ocr(path)
    ys = {}
    for b, t, s in r:
        tt = t.strip()
        if tt in ("100%", "0%"):
            cy = (b[0][1] + b[2][1]) / 2
            if cy > 1500: ys.setdefault(tt, []).append(cy)   # graph labels sit low on the screen
    y100, y0 = min(ys["100%"]), max(ys["0%"])
    reg = im[int(y100) - 25:int(y0) + 8, 40:1000]
    R, G, B = reg[..., 0], reg[..., 1], reg[..., 2]
    mask = (R > 170) & (G < 110) & (B > 90) & (B < 200)
    cols = np.where(mask.any(axis=0))[0]
    x0, x1 = cols.min(), cols.max()
    yy = {}
    for x in range(x0, x1 + 1):
        ys_ = np.where(mask[:, x])[0]
        if len(ys_): yy[x] = ys_.mean() + int(y100) - 25
    def at(t):
        x = x0 + (t / D) * (x1 - x0)
        xs = [k for k in yy if abs(k - x) <= 1.5]
        if not xs: return None
        y = np.mean([yy[k] for k in xs])
        return round((y0 - y) / (y0 - y100) * 100, 1)
    return at(30), at(60)
tests = [("Gavin", "g_054", 842, "51.6 / 31.9"), ("Morgan", "g_041", 1060, "68.0 / 45.5"), ("Greene", "g_067", 886, "63.9 / 39.3"), ("2 Para", "g_032", 1029, "65.5 / 30.4"),
         ("Smith", "g_019", 970, "?"), ("Thomas", "g_008", 1131, "?")]
for n, f, D, ref in tests:
    try: print(n, read(f, D), "Studio:", ref)
    except Exception as e: print(n, "error", e)
