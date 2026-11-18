"""Subject point per photo (owner 2026-11-18: "zoom in to the ship or the main object, not the white centre").
Densest-detail point: Sobel edge energy, heavy blur, borders (6 %) and the bottom 12 % (captions) ignored; clamped to 0.25-0.75.
Out: build/focus.json {photo stem: [fx, fy]}; manual overrides in build/focus_manual.json win."""
import json, os, sys
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE)
PH = os.path.join(FULL, "../footage/src/photos")
S = json.load(open(os.path.join(HERE, "segments.json")))
stems = sorted({s["photo"] for s in S if s["kind"] == "photo"})
out = {}
for st in stems:
    p = next((os.path.join(PH, f"{st}{e}") for e in (".jpg", ".png") if os.path.exists(os.path.join(PH, f"{st}{e}"))), None)
    if not p: continue
    g = cv2.imread(p, cv2.IMREAD_GRAYSCALE); h, w = g.shape; sc = 320 / w
    g = cv2.resize(g, (320, int(h * sc))).astype(np.float32)
    e = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0, 3), cv2.Sobel(g, cv2.CV_32F, 0, 1, 3))
    H, W = e.shape; m = np.zeros_like(e); m[int(.06 * H):int(.88 * H), int(.06 * W):int(.94 * W)] = 1; e *= m
    b = cv2.GaussianBlur(e, (0, 0), W / 10)
    y, x = np.unravel_index(np.argmax(b), b.shape)
    out[st] = [round(float(np.clip(x / W, .25, .75)), 3), round(float(np.clip(y / H, .25, .75)), 3)]
man = os.path.join(HERE, "focus_manual.json")
if os.path.exists(man): out.update(json.load(open(man)))
json.dump(out, open(os.path.join(HERE, "focus.json"), "w"), indent=0)
print(len(out), "photos")
if "sheet" in sys.argv:
    from PIL import Image, ImageDraw
    T = 300; cols = 10; rows = (len(out) + cols - 1) // cols
    sh = Image.new("RGB", (cols * T, rows * (T * 9 // 16 + 14)), (20, 20, 20)); d = ImageDraw.Draw(sh)
    for i, (st, (fx, fy)) in enumerate(sorted(out.items())):
        p = os.path.join(PH, st + ".jpg"); im = Image.open(p).convert("RGB"); im.thumbnail((T, T * 9 // 16))
        x0, y0 = (i % cols) * T, (i // cols) * (T * 9 // 16 + 14); sh.paste(im, (x0, y0))
        cx, cy = x0 + fx * im.width, y0 + fy * im.height
        d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), outline=(255, 40, 40), width=3); d.text((x0 + 2, y0 + T * 9 // 16), f"{i} {st[:34]}", fill=(255, 220, 80))
    sh.save("/dev/shm/focus_sheet.jpg", quality=80)
