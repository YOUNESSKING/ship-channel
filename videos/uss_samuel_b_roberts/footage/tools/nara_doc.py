#!/usr/bin/env python3
"""nara_doc.py OUTDIR META.jsonl naId [maxpages] : download every page image of a NARA multi-page record (war diary / action report), cap 3840 px, stems nara_<naId>_pNN"""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from nara_search import by_id
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
outdir, mf, nid = sys.argv[1:4]; mx = int(sys.argv[4]) if len(sys.argv) > 4 else 999
r = by_id(nid); dos = [o for o in r["digitalObjects"] if "Image" in (o.get("objectType") or "")][:mx]; os.makedirs(outdir, exist_ok=True)
for i, o in enumerate(dos, 1):
    stem = f"nara_{nid}_p{i:02d}"; f = os.path.join(outdir, stem + ".jpg")
    if not os.path.exists(f):
        tmp = f + ".part"; subprocess.run(["curl", "-sS", "-L", "--retry", "3", "-A", "ship-channel-research/1.0", "-o", tmp, o["objectUrl"]], check=True)
        im = Image.open(tmp); im.load(); im = im.convert("RGB"); s = 3840 / max(im.size)
        if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        im.save(f, "JPEG", quality=88); os.remove(tmp)
    w, h = Image.open(f).size
    open(mf, "a").write(json.dumps(dict(stem=stem, naId=nid, page=i, pages=len(dos), title=r["title"], use=r.get("useRestriction"), note=(r.get("scopeAndContentNote") or "")[:300], obj=o["objectUrl"], w=w, h=h, file=f)) + "\n")
print("ok", nid, len(dos))
