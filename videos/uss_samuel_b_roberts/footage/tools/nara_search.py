#!/usr/bin/env python3
"""nara_search.py - search the NARA catalog through the public proxy API (no key).
usage: nara_search.py "query" [--type photo|film|all] [--pages N] [--json out.jsonl]
Prints one line per hit: naId | localId | date | useRestriction | #digital | title.
Do NOT pass a limit param (breaks the proxy). Filter name is typesOfMaterials."""
import sys, json, urllib.request, urllib.parse, argparse, ssl
H = {"Content-Type": "application/json", "User-Agent": "ship-channel-research/1.0"}
T = {"photo": "Photographs and other Graphic Materials", "film": "Moving Images"}
def get(params):
    u = "https://catalog.archives.gov/proxy/records/search?" + urllib.parse.urlencode(params)
    for i in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
        except Exception as e:
            err = e
    raise err
def by_id(naid):
    d = get({"naId": naid})
    h = d["body"]["hits"]["hits"]
    return h[0]["_source"]["record"] if h else None
def summarize(r):
    dos = r.get("digitalObjects") or []
    dt = (r.get("productionDates") or r.get("coverageStartDate") or [{}])
    date = ""
    if isinstance(dt, list) and dt: date = (dt[0].get("logicalDate") or str(dt[0].get("year", "")))
    elif isinstance(dt, dict): date = dt.get("logicalDate", "")
    return dict(naId=r.get("naId"), local=r.get("localIdentifier"), title=r.get("title"), date=date,
                use=r.get("useRestriction"), dos=[(o.get("objectType"), o.get("objectUrl"), o.get("objectFileSize")) for o in dos],
                note=(r.get("scopeAndContentNote") or "")[:400])
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("q"); ap.add_argument("--type", default="all")
    ap.add_argument("--pages", type=int, default=1); ap.add_argument("--json"); ap.add_argument("--online", action="store_true")
    a = ap.parse_args(); out = open(a.json, "a") if a.json else None
    for p in range(1, a.pages + 1):
        prm = {"q": a.q, "page": p}
        if a.type in T: prm["typesOfMaterials"] = T[a.type]
        if a.online: prm["availableOnline"] = "true"
        d = get(prm); hs = d["body"]["hits"]["hits"]
        if p == 1: print("total", d["body"]["hits"]["total"], file=sys.stderr)
        for h in hs:
            s = summarize(h["_source"]["record"])
            print(s["naId"], "|", s["local"], "|", s["date"], "|", (s["use"] or {}).get("status"), "|", len(s["dos"]), "|", (s["title"] or "")[:110])
            if out: out.write(json.dumps(s) + "\n")
        if len(hs) < 20: break
