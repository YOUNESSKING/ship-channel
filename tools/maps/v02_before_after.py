#!/usr/bin/env python3
"""v02_before_after.py OLD_DIR NEW_DIR OUT.jpg : per map, start/middle/end frames, old row above new row (full frames downscaled)
plus a 1:1 centre crop of the middle frame (old | new) so sharpness is visible."""
import sys, os, json, subprocess, numpy as np, cv2
old, new, out = sys.argv[1:4]
ids = ["R04", "C01-02", "C02-02", "C03-02", "C04-02", "C05-02", "C06-02", "C07-02", "C07-25", "C08-02", "C09-02", "C09-16", "C10-02", "C11-02", "C12-02"]
def grab(p, i):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", p, "-vf", f"select=eq(n\\,{i})", "-vframes", "1", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1080, 1920, 3)
def lab(im, t): im = im.copy(); cv2.putText(im, t, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 1, cv2.LINE_AA); return im
tw, th = 400, 225; blocks = []
for sid in ids:
    n = json.load(open(os.path.join(new, sid + ".json")))["frames"]; rows = []
    for tag, d in (("OLD", old), ("NEW", new)):
        fr = [grab(os.path.join(d, sid + ".mp4"), i) for i in (0, n // 2, n - 1)]
        th_ = [lab(cv2.resize(f, (tw, th), interpolation=cv2.INTER_AREA), f"{sid} {tag}") for f in fr]
        crop = fr[1][540 - 112:540 + 113, 960 - 200:960 + 200]
        rows.append(np.hstack(th_ + [lab(crop, f"{tag} 1:1 crop")]))
    blocks.append(np.vstack(rows + [np.zeros((6, rows[0].shape[1], 3), np.uint8)]))
cv2.imwrite(out, np.vstack(blocks), [cv2.IMWRITE_JPEG_QUALITY, 82])
