#!/usr/bin/env python3
"""ia.py QUERY [rows] : archive.org advancedsearch -> identifier | mediatype | year | licenseurl | creator | title"""
import sys, json, urllib.request, urllib.parse
q = sys.argv[1]; rows = sys.argv[2] if len(sys.argv) > 2 else "25"
u = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode([("q", q), ("fl[]", "identifier"), ("fl[]", "title"), ("fl[]", "mediatype"), ("fl[]", "licenseurl"), ("fl[]", "creator"), ("fl[]", "year"), ("fl[]", "collection"), ("rows", rows), ("output", "json")])
d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ship-channel-research/1.0"}), timeout=60))
for r in d["response"]["docs"]:
    print(r.get("identifier"), "|", r.get("mediatype"), "|", r.get("year"), "|", r.get("licenseurl"), "|", str(r.get("creator"))[:30], "|", str(r.get("title"))[:90], "|", str(r.get("collection"))[:60])
