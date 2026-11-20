"""SBR: white-out / black / blank spans of every NARA reel in beats.FILMS (mean luma and contrast every 0.5 s of the
timecode-cropped picture). Out: build/film_bad.json {reel: [[a, b], ...]}; make_shotlists drops these spans like cuts."""
import cv2, json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from beats import FILMS
FT = os.path.join(HERE, "../../footage/src/film"); OUT = os.path.join(HERE, "film_bad.json")
res = {}
for reel in sorted({v[0] for v in FILMS.values()}):
    cap = cv2.VideoCapture(os.path.join(FT, reel + ".mp4")); fps = cap.get(5) or 30; n = int(cap.get(7)); bad = []
    for i in range(0, n, max(1, int(fps / 2))):
        cap.set(1, i); ok, fr = cap.read()
        if not ok: break
        h, w = fr.shape[:2]; g = cv2.cvtColor(fr[int(h * .05):int(h * .8), int(w * .05):int(w * .95)], cv2.COLOR_BGR2GRAY)
        m, sd = float(g.mean()), float(g.std())
        if (m > 185 and sd < 30) or m < 22 or sd < 9: bad.append(round(i / fps, 2))
    spans = []
    for t in bad:
        if spans and t - spans[-1][1] <= 0.6: spans[-1][1] = t
        else: spans.append([t, t])
    res[reel] = [[round(a - 0.5, 2), round(b + 0.5, 2)] for a, b in spans]
    print(reel, res[reel][:12], flush=True)
json.dump(res, open(OUT, "w"), indent=0)
