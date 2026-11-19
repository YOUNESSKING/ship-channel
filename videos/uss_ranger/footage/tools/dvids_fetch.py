#!/usr/bin/env python3
"""dvids_fetch.py - fetch DVIDS item pages (public domain US gov works), read metadata + licence line, download the best file.
usage: dvids_fetch.py OUTDIR META.jsonl URL [URL ...]
Images: DVIDS CDN serves max 2000w_q95.jpg without a login (the 'Download' button needs an account) - resolution of the original is
recorded from the page ('Resolution:'). Videos: best progressive mp4 up to 1920x1080 (names taken from the page's m3u8 ladder)."""
import sys, re, json, os, subprocess, html, urllib.request
UA = "Mozilla/5.0 (X11; Linux x86_64) ship-channel-research"
def fetch(u, binary=False):
    for i in range(3):
        try:
            d = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=60).read()
            return d if binary else d.decode("utf8", "replace")
        except Exception as e: err = e
    raise err
def td(h, label):
    m = re.search(r"<td>\s*" + re.escape(label) + r"\s*</td>\s*<td>\s*(.*?)\s*</td>", h, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
def one(url, outdir):
    h = fetch(url); typ = "video" if "/video/" in url else "image"
    iid = re.search(r"/(?:video|image)/(\d+)", url).group(1)
    title = html.unescape(re.search(r'og:title" content="([^"]*)"', h).group(1))
    desc = html.unescape(re.search(r'og:description" content="([^"]*)"', h).group(1))
    lic = "PUBLIC DOMAIN" if "PUBLIC DOMAIN" in h else ("UNKNOWN: " + (re.search(r"asset_license[^>]*>([^<]*)", h) or [0, ""])[1])
    cr = re.search(r'class="copyright_info">(.*?)</p>', h, re.S)
    cr = html.unescape(re.sub(r"<[^>]+>", "", cr.group(1))).strip() if cr else ""
    meta = dict(id=iid, type=typ, url=url.split("?")[0], title=title, desc=desc, date=td(h, "Date Taken:"), virin=td(h, "VIRIN:"),
                resolution_page=td(h, "Resolution:"), length=td(h, "Length:"), location=td(h, "Location:"), licence=lic, copyright_line=cr[:300])
    pre = f"dvids_{typ[:3]}_{iid}"
    if typ == "image":
        f = os.path.join(outdir, pre + ".jpg"); b = fetch(f"https://d1ldvf68ux039x.cloudfront.net/thumbs/photos/1503/{iid}/2000w_q95.jpg", True)
        open(f, "wb").write(b); meta["file"] = f
    else:
        m3 = fetch(f"https://www.dvidshub.net/video/{iid}.m3u8")
        lad = re.findall(r"RESOLUTION=(\d+)x(\d+).*?\n(https://\S+?)-hls\.m3u8", m3)
        lad = sorted([(int(w), int(hh), u) for w, hh, u in lad if int(w) <= 1920], reverse=True)
        w, hh, u = lad[0]; f = os.path.join(outdir, pre + ".mp4")
        subprocess.run(["curl", "-sS", "-L", "-A", UA, "-o", f, u + ".mp4"], check=True)
        meta["file"] = f; meta["w"], meta["h"] = w, hh; meta["ladder"] = [f"{a}x{b}" for a, b, _ in lad]
    return meta
if __name__ == "__main__":
    outdir, mf = sys.argv[1], sys.argv[2]; os.makedirs(outdir, exist_ok=True)
    for u in sys.argv[3:]:
        try: m = one(u, outdir)
        except Exception as e: print("FAIL", u, e); continue
        open(mf, "a").write(json.dumps(m) + "\n"); print(m["id"], m["type"], m["licence"], m["date"], m["resolution_page"] or m["length"], m["title"][:70])
