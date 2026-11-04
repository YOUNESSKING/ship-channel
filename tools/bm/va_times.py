"""Map agent va: scene-relative time of phrases (same formula as B.at) straight from audio/timing.json.
usage: python3 tools/va_times.py FIRST_TAG "tag:phrase" ...   (FIRST_TAG = the scene's first paragraph)"""
import json, sys
P = json.load(open("audio/timing.json"))["paragraphs"]
key = lambda p: p["tag"].split("|")[0].replace("MAP:", "").strip()
D = {key(p): p for p in P}; t0 = D[sys.argv[1]]["start"]
for a in sys.argv[2:]:
    k, ph = a.split(":", 1); p = D[k]; s0, s1 = p["start"] - t0, p["end"] - t0; i = p["text"].find(ph)
    print(f"{s0 + (s1 - s0) * i / len(p['text']):7.2f}" if i >= 0 else "MISSING", k, ph)
