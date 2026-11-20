"""SBR: white-out / black / blank spans inside every NARA window in beats.FILMS (2 fps, 96x64 grey frames via ffmpeg; mean and
contrast of the timecode-free area). Out: build/film_bad.json {reel: [[a, b], ...]}; make_shotlists drops these spans like cuts."""
import json, os, subprocess, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from beats import FILMS
FT = os.path.join(HERE, "../../footage/src/film"); OUT = os.path.join(HERE, "film_bad.json")
res = json.load(open(OUT)) if os.path.exists(OUT) else {}
wins = {}
for k, v in FILMS.items():
    if v[0].startswith("nara_"): wins.setdefault(v[0], []).extend(v[1])
for reel, ws in sorted(wins.items()):
    if reel in res: continue
    a, b = min(w[0] for w in ws), max(w[1] for w in ws); W_, H_ = 96, 64
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a), "-to", str(b), "-i", os.path.join(FT, reel + ".mp4"), "-vf", f"fps=2,scale={W_}:{H_},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H_, W_)[:, 3:51, 5:91].astype(float)
    bad = [round(a + i / 2, 2) for i, f in enumerate(fr) if (f.mean() > 185 and f.std() < 30) or f.mean() < 22 or f.std() < 9]
    spans = []
    for t in bad:
        if spans and t - spans[-1][1] <= 0.6: spans[-1][1] = t
        else: spans.append([t, t])
    res[reel] = [[round(x - 0.6, 2), round(y + 0.6, 2)] for x, y in spans]
    print(reel, res[reel], flush=True); json.dump(res, open(OUT, "w"))
