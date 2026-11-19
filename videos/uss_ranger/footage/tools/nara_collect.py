#!/usr/bin/env python3
"""nara_collect.py - run many NARA queries, keep items whose title/note mention Ranger CV-61 (or any if --any), dedupe into a jsonl."""
import sys, json, re, os
sys.path.insert(0, os.path.dirname(__file__))
from nara_search import get, summarize, T
out = sys.argv[1]; kind = sys.argv[2]; pages = int(sys.argv[3]); pat = re.compile(sys.argv[4], re.I); queries = sys.argv[5:]
seen = {}
if os.path.exists(out):
    for l in open(out): seen[json.loads(l)["naId"]] = 1
f = open(out, "a"); n = 0
for q in queries:
    for p in range(1, pages + 1):
        prm = {"q": q, "page": p}
        if kind in T: prm["typesOfMaterials"] = T[kind]
        try: hs = get(prm)["body"]["hits"]["hits"]
        except Exception as e: print("ERR", q, p, e); break
        for h in hs:
            s = summarize(h["_source"]["record"])
            if s["naId"] in seen or not s["dos"] or len(s["dos"]) > 3: continue
            if not pat.search((s["title"] or "") + " " + s["note"] + " " + str(s["local"])): continue
            seen[s["naId"]] = 1; n += 1; f.write(json.dumps(s) + "\n")
        if len(hs) < 20: break
print("added", n, "total", len(seen))
