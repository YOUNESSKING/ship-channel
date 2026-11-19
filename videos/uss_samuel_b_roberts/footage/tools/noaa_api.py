#!/usr/bin/env python3
"""noaa_api.py - NOAA Ocean Exploration media via the site's WordPress REST API (public).
  noaa_api.py search TERM [per_page]   -> id | mime | WxH | title | caption(first 160) | url   (appends to scratch/noaa_found.jsonl)
  noaa_api.py get OUTDIR META.jsonl ID... -> download source_url (video mp4 as is; images capped 3840 long side q90), meta line with caption/credit
Rights: oceanexplorer.noaa.gov/about/media-kit/ 'Usage and Credit': credit NOAA Ocean Exploration; items whose caption contains 'copyright' need extra permission."""
import sys, json, re, os, urllib.request, urllib.parse, subprocess
UA = "ship-channel-research/1.0"; B = "https://oceanexplorer.noaa.gov/wp-json/wp/v2/media"
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.join(HERE, "..", "scratch")
F = "id,link,source_url,mime_type,title,caption,description,date,alt_text,media_details,post"
def api(**p):
    u = B + "?" + urllib.parse.urlencode(p)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=60))
clean = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()
if __name__ == "__main__":
    if sys.argv[1] == "search":
        n = sys.argv[3] if len(sys.argv) > 3 else "20"
        for m in api(search=sys.argv[2], per_page=n, _fields=F):
            md = m.get("media_details") or {}
            r = dict(id=m["id"], mime=m["mime_type"], w=md.get("width"), h=md.get("height"), title=clean(m["title"]["rendered"]), caption=clean(m["caption"]["rendered"]), desc=clean(m["description"]["rendered"])[:600], date=m["date"][:10], url=m["source_url"], page=m["link"])
            open(os.path.join(SCR, "noaa_found.jsonl"), "a").write(json.dumps(r) + "\n")
            print(r["id"], "|", r["mime"], "|", r["w"], "x", r["h"], "|", r["title"][:40], "|", (r["caption"] or r["desc"])[:170], "|", r["url"][-48:])
    else:
        from PIL import Image
        outdir, mf = sys.argv[2:4]; os.makedirs(outdir, exist_ok=True)
        for i in sys.argv[4:]:
            m = api(include=i, _fields=F)[0]; md = m.get("media_details") or {}
            vid = m["mime_type"].startswith("video"); stem = "noaa_" + str(m["id"]); f = os.path.join(outdir, stem + (".mp4" if vid else ".jpg"))
            if not os.path.exists(f):
                tmp = f + ".part"; subprocess.run(["curl", "-sS", "-L", "--retry", "3", "-A", UA, "-o", tmp, m["source_url"]], check=True)
                if vid: os.rename(tmp, f)
                else:
                    im = Image.open(tmp); im.load(); im = im.convert("RGB"); s = 3840 / max(im.size)
                    if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
                    im.save(f, "JPEG", quality=90); os.remove(tmp)
            r = dict(stem=stem, id=m["id"], mime=m["mime_type"], w=md.get("width"), h=md.get("height"), title=clean(m["title"]["rendered"]), caption=clean(m["caption"]["rendered"]), desc=clean(m["description"]["rendered"])[:800], date=m["date"][:10], url=m["source_url"], page=m["link"], file=f)
            open(mf, "a").write(json.dumps(r) + "\n"); print("ok", stem, r["title"][:50])
