#!/usr/bin/env python3
"""nara_download.py - download NARA items by naId from the catalog proxy; stills capped to 3840 px long side, JPEG q90 (as Nevada).
usage: nara_download.py photo|film OUTDIR META.jsonl naId [naId ...]  (also reads naIds from stdin if none given)
Writes one meta line per item: naId, local id, title, date, useRestriction (verbatim), digital object, w/h, file."""
import sys, os, json, subprocess, io
sys.path.insert(0, os.path.dirname(__file__))
from nara_search import by_id
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
kind, outdir, mf = sys.argv[1:4]; ids = sys.argv[4:] or sys.stdin.read().split(); os.makedirs(outdir, exist_ok=True)
UA = "ship-channel-research/1.0"
for nid in ids:
    try:
        r = by_id(nid); dos = r.get("digitalObjects") or []
        if kind == "photo":
            c = [o for o in dos if "Image" in (o.get("objectType") or "")]
            o = max(c, key=lambda o: o.get("objectFileSize") or 0)
        else:
            c = [o for o in dos if "MP4" in (o.get("objectType") or "") or "Video" in (o.get("objectType") or "")]
            o = max(c, key=lambda o: o.get("objectFileSize") or 0)
        stem = "nara_" + str(nid); ext = ".jpg" if kind == "photo" else ".mp4"; f = os.path.join(outdir, stem + ext)
        if not os.path.exists(f):
            tmp = f + ".part"
            subprocess.run(["curl", "-sS", "-L", "-C", "-", "--retry", "3", "-A", UA, "-o", tmp, o["objectUrl"]], check=True)
            if kind == "photo":
                im = Image.open(tmp); im.load()
                if im.mode not in ("RGB", "L"): im = im.convert("RGB")
                s = 3840 / max(im.size)
                if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
                im.save(f, "JPEG", quality=90); os.remove(tmp)
            else: os.rename(tmp, f)
        m = dict(stem=stem, naId=nid, local=r.get("localIdentifier"), title=r.get("title"), use=r.get("useRestriction"),
                 date=[ (r.get("productionDates") or [{}])[0].get("logicalDate") ] if r.get("productionDates") else None,
                 note=(r.get("scopeAndContentNote") or "")[:600], obj=o.get("objectUrl"), objtype=o.get("objectType"), objsize=o.get("objectFileSize"), file=f)
        if kind == "photo": im2 = Image.open(f); m["w"], m["h"] = im2.size
        open(mf, "a").write(json.dumps(m) + "\n"); print("ok", nid, m.get("w", ""), m.get("h", ""), (r.get("title") or "")[:60])
    except Exception as e: print("FAIL", nid, e)
