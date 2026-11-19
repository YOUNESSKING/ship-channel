#!/usr/bin/env python3
"""commons_fetch.py - Wikimedia Commons discovery + download for US federal works (reads each file's licence from extmetadata).
usage: commons_fetch.py search "query" [--cat "Category:..."] [--n 30]      -> prints pageid | w x h | licence | title | credit
       commons_fetch.py get OUTDIR META.jsonl [--video] pageid [pageid ...]   -> downloads (stills capped 3840 px long side, JPEG q90), meta line per item
Only licences PD-USGov*/CC0/CC BY/CC BY-SA are accepted (anything else is printed and skipped). Use a polite UA and sleeps (API is rate limited)."""
import sys, os, re, json, time, html, subprocess, urllib.request, urllib.parse, io
UA = "ship-channel-research/1.0 (footage research; contact via repo owner)"
API = "https://commons.wikimedia.org/w/api.php"
OK = re.compile(r"^(pd|public domain|cc0|cc[- ]by)", re.I)
def api(**p):
    p["format"] = "json"; u = API + "?" + urllib.parse.urlencode(p)
    for i in range(5):
        try:
            time.sleep(1.0); return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=60))
        except Exception as e: err = e; time.sleep(5 * (i + 1))
    raise err
def info(ids=None, titles=None):
    p = dict(action="query", prop="imageinfo", iiprop="url|size|extmetadata|mime|mediatype", iiextmetadatafilter="LicenseShortName|UsageTerms|Credit|ImageDescription|DateTimeOriginal|Artist|Copyrighted|AttributionRequired")
    if ids: p["pageids"] = "|".join(map(str, ids))
    else: p["titles"] = "|".join(titles)
    out = []
    for pg in api(**p).get("query", {}).get("pages", {}).values():
        ii = (pg.get("imageinfo") or [None])[0]
        if not ii: continue
        em = {k: html.unescape(re.sub(r"<[^>]+>", "", v.get("value", ""))).strip() for k, v in ii.get("extmetadata", {}).items()}
        out.append(dict(pageid=pg["pageid"], title=pg["title"], url=ii["url"], w=ii["width"], h=ii["height"], mime=ii["mime"], size=ii.get("size"), em=em))
    return out
def search(q, cat=None, n=30):
    ids = []
    if cat:
        d = api(action="query", list="categorymembers", cmtitle=cat, cmtype="file", cmlimit=n)
        ids = [m["pageid"] for m in d["query"]["categorymembers"]]
    else:
        d = api(action="query", list="search", srsearch=q, srnamespace=6, srlimit=n)
        ids = [m["pageid"] for m in d["query"]["search"]]
    r = []
    for i in range(0, len(ids), 40): r += info(ids[i:i + 40])
    return r
if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "search":
        a = sys.argv[2:]; cat = a[a.index("--cat") + 1] if "--cat" in a else None; n = int(a[a.index("--n") + 1]) if "--n" in a else 30
        for r in search(a[0] if a and not a[0].startswith("--") else "", cat, n):
            em = r["em"]; print(r["pageid"], "|", f'{r["w"]}x{r["h"]}', "|", em.get("LicenseShortName", "?"), "|", r["title"][5:80], "|", em.get("Credit", "")[:50], "|", r["mime"].split("/")[1])
    else:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
        outdir, mf = sys.argv[2:4]; rest = sys.argv[4:]; video = "--video" in rest; ids = [x for x in rest if x != "--video"]; os.makedirs(outdir, exist_ok=True)
        for r in info(ids):
            lic = r["em"].get("LicenseShortName", "")
            if not OK.match(lic): print("SKIP licence", r["pageid"], lic, r["title"]); continue
            stem = "commons_" + str(r["pageid"]); ext = os.path.splitext(r["url"])[1].lower()
            f = os.path.join(outdir, stem + (".jpg" if not video else ext)); tmp = f + ".part"
            if not os.path.exists(f):
                subprocess.run(["curl", "-sS", "-L", "--retry", "5", "--retry-delay", "10", "-A", UA, "-o", tmp, r["url"]], check=True)
                if not video:
                    im = Image.open(tmp); im.load(); im = im.convert("RGB"); s = 3840 / max(im.size)
                    if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
                    im.save(f, "JPEG", quality=90); os.remove(tmp); r["out_w"], r["out_h"] = im.size
                else: os.rename(tmp, f)
            r["stem"] = stem; r["file"] = f; r["licence"] = lic
            open(mf, "a").write(json.dumps(r) + "\n"); print("ok", stem, r["w"], r["h"], lic, r["title"][5:70]); time.sleep(2)
