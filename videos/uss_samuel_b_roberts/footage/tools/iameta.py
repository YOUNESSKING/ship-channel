#!/usr/bin/env python3
"""iameta.py ID... : archive.org item metadata: title, licenseurl, creator, date, files (name,size,format,length,w,h)"""
import sys, json, urllib.request
for i in sys.argv[1:]:
    try: d = json.load(urllib.request.urlopen(urllib.request.Request("https://archive.org/metadata/" + i, headers={"User-Agent": "ship-channel-research/1.0"}), timeout=60))
    except Exception as e: print(i, "ERR", e); continue
    m = d.get("metadata", {})
    if not m: print(i, "NOT FOUND"); continue
    print("##", i, "|", m.get("title"), "|", m.get("licenseurl"), "|", m.get("creator"), "|", m.get("date") or m.get("year"), "|", m.get("rights"), "|", m.get("possible-copyright-status"))
    print("   ", (m.get("description") or "")[:300].replace("\n", " "))
    for f in d.get("files", []):
        if f.get("name", "").lower().endswith((".mp4", ".mpg", ".mpeg", ".ogv", ".mov", ".avi", ".mkv")): print("   ", f["name"], f.get("size"), f.get("format"), f.get("length"), f.get("width"), f.get("height"))
