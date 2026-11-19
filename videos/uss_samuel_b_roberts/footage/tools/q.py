#!/usr/bin/env python3
"""q.py - NARA query helper: q.py [--film] [--pages N] [--re REGEX] query... ; prints hits whose localIdentifier is set and has 1-3 digital objects; saves to scratch/nara_cand.jsonl"""
import sys, json, re, os
sys.path.insert(0, os.path.dirname(__file__))
from nara_search import get, summarize, T
a = sys.argv[1:]; kind = "photo"; pages = 2; pat = None; loc = None
while a and a[0].startswith("--"):
    o = a.pop(0)
    if o == "--film": kind = "film"
    elif o == "--any": kind = "any"
    elif o == "--pages": pages = int(a.pop(0))
    elif o == "--re": pat = re.compile(a.pop(0), re.I)
    elif o == "--loc": loc = re.compile(a.pop(0), re.I)
out = open(os.path.join(os.path.dirname(__file__), "..", "scratch", "nara_cand.jsonl"), "a")
seen = set()
for q in a:
    print("==", q)
    for p in range(1, pages + 1):
        try: hs = get(dict({"q": q, "page": p}, **({"typesOfMaterials": T[kind]} if kind in T else {})))["body"]["hits"]["hits"]
        except Exception as e: print("ERR", e); break
        for h in hs:
            s = summarize(h["_source"]["record"])
            if s["naId"] in seen or not s["local"] or (loc and not loc.search(str(s["local"]))) or not s["dos"] or len(s["dos"]) > 3: continue
            txt = (s["title"] or "") + " " + s["note"]
            if pat and not pat.search(txt): continue
            seen.add(s["naId"]); out.write(json.dumps(s) + "\n")
            print(s["naId"], "|", s["local"], "|", s["date"], "|", (s["use"] or {}).get("status"), "|", (s["title"] or "")[:130])
        if len(hs) < 20: break
