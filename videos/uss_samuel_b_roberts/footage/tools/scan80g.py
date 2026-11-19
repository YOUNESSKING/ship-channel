#!/usr/bin/env python3
"""scan80g.py PREFIX START END : look up NARA localIdentifier PREFIX-N for N in range (exact), print hits with digital-object count. Appends to scratch/scan.jsonl"""
import sys, json, os
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from nara_search import get, summarize
pre, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
def one(n):
    lid = f"{pre}-{n}"
    try: hs = get({"localIdentifier": lid})["body"]["hits"]["hits"]
    except Exception as e: return (n, None)
    return (n, [summarize(h["_source"]["record"]) for h in hs])
out = open(os.path.join(os.path.dirname(__file__), "..", "scratch", "scan.jsonl"), "a")
with ThreadPoolExecutor(12) as ex:
    for n, r in ex.map(one, range(a, b + 1)):
        if r is None: print(n, "ERR"); continue
        for s in r:
            out.write(json.dumps(s) + "\n")
            print(s["local"], s["naId"], s["date"], len(s["dos"]), (s["title"] or "")[:110])
