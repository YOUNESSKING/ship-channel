"""ar3_: print estimated word times (scene-relative, B.at's proportional rule) for paragraphs FIRST..LAST.  usage: python3 tools/ar3_times.py FIRST LAST"""
import json, re, sys
P = json.load(open("audio/timing.json"))["paragraphs"]; key = lambda p: p["tag"].split("|")[0].replace("MAP:", "").strip()
ks = [key(p) for p in P]; i0, i1 = ks.index(sys.argv[1]), ks.index(sys.argv[2]); t0 = P[i0]["start"]
for p in P[i0:i1 + 1]:
    s0, s1, tx = p["start"] - t0, p["end"] - t0, p["text"]; print(f"== {key(p)} {s0:.2f}-{s1:.2f}")
    print(" ".join(f"{w}[{s0 + (s1 - s0) * m.start() / len(tx):.1f}]" if i % 3 == 0 else w for i, (m, w) in enumerate((m, m.group()) for m in re.finditer(r"\S+", tx))))
