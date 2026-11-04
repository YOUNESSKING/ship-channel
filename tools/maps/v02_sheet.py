#!/usr/bin/env python3
"""v02_sheet.py OUT_DIR SHEET.jpg [--pins] : contact sheet of the Video 02 map clips, 3 frames per map (start, middle, end).
--pins draws the json pin track (review only; the delivered sheet is clean)."""
import sys, os, json, subprocess, numpy as np, cv2
d, out = sys.argv[1], sys.argv[2]; pins = "--pins" in sys.argv
ids = ["R04", "C01-02", "C02-02", "C03-02", "C04-02", "C05-02", "C06-02", "C07-02", "C07-25", "C08-02", "C09-02", "C09-16", "C10-02", "C11-02", "C12-02"]
tw, th = 480, 270; rows = []
for sid in ids:
    j = json.load(open(os.path.join(d, sid + ".json"))); n = j["frames"]; row = []
    for i in (0, n // 2, n - 1):
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(d, sid + ".mp4"), "-vf", f"select=eq(n\\,{i})", "-vframes", "1", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
        im = np.frombuffer(raw, np.uint8).reshape(1080, 1920, 3).copy()
        if pins:
            if "pin" in j:
                tr = min(j["pin"]["track"], key=lambda r: abs(r[0] - i / 30)); cv2.circle(im, (int(tr[1] * 1.5), int(tr[2] * 1.5)), 18, (0, 215, 255), 4)
            for p in j.get("pins", []):
                f = i / (n - 1); x = p["x_start"] + (p["x"] - p["x_start"]) * f; y = p["y_start"] + (p["y"] - p["y_start"]) * f
                cv2.circle(im, (int(x * 1.5), int(y * 1.5)), 14, (0, 215, 255), 4)
        im = cv2.resize(im, (tw, th), interpolation=cv2.INTER_AREA)
        cv2.putText(im, f"{sid}  f{i}", (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (230, 230, 230), 1, cv2.LINE_AA)
        row.append(im)
    rows.append(np.hstack([np.pad(r, ((2, 2), (2, 2), (0, 0))) for r in row]))
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
