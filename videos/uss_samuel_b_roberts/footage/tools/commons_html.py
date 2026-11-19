#!/usr/bin/env python3
"""commons_html.py - Commons discovery without the (429) API: scrapes category and file HTML pages (polite, 1.2 s apart).
  commons_html.py cat "Category:Name" [--sub]        -> lists file titles (and subcategories)
  commons_html.py info "File:Name.jpg" ...            -> one json line per file to stdout (licence cats, size, description, date, source) and scratch/commons_info.jsonl
  commons_html.py get OUTDIR META.jsonl "File:..."    -> downloads a standard-width thumbnail (<=3840 px) from upload.wikimedia.org (originals answer 429 to this IP), q90 JPEG
Only files whose page carries a PD / CC0 / CC BY / CC BY-SA licence marker are kept (see OKRE); NC/ND never."""
import sys, re, json, time, html, os, urllib.request, urllib.parse, subprocess, hashlib
UA = "ship-channel-research/1.0 (footage research; contact via repo owner)"
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.join(HERE, "..", "scratch"); os.makedirs(SCR, exist_ok=True)
def page(title):
    u = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe="/:()_,'!-.")
    for i in range(4):
        try:
            time.sleep(3.0)
            return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=60).read().decode("utf8", "replace")
        except urllib.error.HTTPError as e:
            err = e
            if e.code == 404: raise
            time.sleep(30 * (i + 1))
        except Exception as e: err = e; time.sleep(10)
    raise err
def cat(title):
    h = page(title); files = []; subs = []
    for m in re.finditer(r'href="/wiki/(File:[^"#?]+)"', h):
        t = urllib.parse.unquote(m.group(1)).replace("_", " ")
        if t not in files: files.append(t)
    for m in re.finditer(r'class="CategoryTreeLabel[^"]*"[^>]*href="/wiki/(Category:[^"#?]+)"', h):
        t = urllib.parse.unquote(m.group(1)).replace("_", " "); subs.append(t)
    nxt = re.search(r'href="([^"]*)"[^>]*>next page', h)
    return files, subs, (html.unescape(nxt.group(1)) if nxt else None)
OKRE = re.compile(r"PD[ -]|Public domain|CC0|CC[- ]BY(?![- ]N)", re.I)
def info(title):
    h = page(title)
    cfg = re.search(r'"wgCategories":(\[.*?\])', h); cats = json.loads(cfg.group(1)) if cfg else []
    txt = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)))
    txt = re.sub(r"\s+", " ", txt)
    sz = re.search(r"Original file\s*\(?([\d,]+)\s*[×x]\s*([\d,]+) pixels, file size: ([\d.,]+ [KMG]B)", txt)
    desc = re.search(r"Description (.*?) (?:Date|Source|Author|Permission)", txt)
    date = re.search(r"Date (.*?) (?:Source|Author|Permission|Credit)", txt)
    src = re.search(r"Source (.*?) (?:Author|Permission|Licensing|Other versions|Description)", txt)
    lic = re.search(r"Licensing \[ edit \] (.*?)(?: Cache expiry| Category| Captions|$)", txt)
    nc = bool(re.search(r"\bNC\b|NonCommercial|NoDerivs|\bND\b", " ".join(cats)))
    pdcats = [c for c in cats if OKRE.search(c) and "Non" not in c]
    return dict(title=title, url="https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe="/:()_,'!-."),
                w=int(sz.group(1).replace(",", "")) if sz else None, h=int(sz.group(2).replace(",", "")) if sz else None, size=sz.group(3) if sz else None,
                desc=(desc.group(1) if desc else "")[:500], date=(date.group(1) if date else "")[:80], source=(src.group(1) if src else "")[:200],
                licence=(lic.group(1) if lic else "")[:300], cats=cats, pdcats=pdcats, ok=bool(pdcats) and not nc)
def stem_for(title):
    t = title[5:]
    m = re.search(r"\((80-G-[A-Za-z0-9-]+|NH \d+|L4\d-[\d.]+|USN \d+|BS \d+|428-GX-[A-Z]+-\d+)\)", t) or re.match(r"^(80-G-[A-Za-z0-9-]+|NH \d+|428-GX-[A-Z]+-\d+|330-PSA-[\d-]+)", t)
    base = m.group(1) if m else re.sub(r"[^A-Za-z0-9]+", "_", re.sub(r"\.[A-Za-z]+$", "", t))[:48].strip("_")
    return "cm_" + re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_")
def thumb_url(title, width):
    name = title[5:].replace(" ", "_"); md5 = hashlib.md5(name.encode()).hexdigest()
    q = urllib.parse.quote(name, safe="_,-.!~")
    if name.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff")):
        return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{md5[0]}/{md5[:2]}/{q}/{width}px-{q}" + (".jpg" if name.lower().endswith((".tif", ".tiff")) else "") + ("" if not name.lower().endswith(".tif") else "")
if __name__ == "__main__":
    c = sys.argv[1]
    if c == "cat":
        t = sys.argv[2]; allf = []
        while True:
            f, s, n = cat(t); allf += f
            if not n or "--all" not in sys.argv: break
            t = n
        for x in allf: print(x)
        if "--sub" in sys.argv:
            for x in s: print("SUB", x)
    elif c == "info":
        o = open(os.path.join(SCR, "commons_info.jsonl"), "a")
        for t in sys.argv[2:]:
            try: r = info(t)
            except Exception as e: print("ERR", t, e); continue
            o.write(json.dumps(r) + "\n"); print(json.dumps({k: r[k] for k in ("title", "w", "h", "ok", "pdcats", "date")}))
    elif c == "get":
        # get OUTDIR META.jsonl INFO.jsonl TITLES.txt : download standard-width thumbnails for the titles listed (one per line) that are ok in INFO
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
        outdir, mf, inf, tf = sys.argv[2:6]; os.makedirs(outdir, exist_ok=True)
        INF = {}
        for l in open(inf):
            r = json.loads(l); INF[r["title"]] = r
        done = set()
        if os.path.exists(mf):
            for l in open(mf): done.add(json.loads(l)["title"])
        for t in [l.rstrip("\n") for l in open(tf, encoding="utf8") if l.strip()]:
            r = INF.get(t)
            if not r or not r["ok"] or t in done: continue
            stem = stem_for(t); f = os.path.join(outdir, stem + ".jpg"); w = min(r["w"] or 3840, 3840)
            ok = False
            for ww in (w, 3200, 2560, 1920, 1280):
                if ww > w: continue
                u = thumb_url(t, ww)
                if not u: break
                tmp = f + ".part"
                rc = subprocess.run(["curl", "-sS", "-L", "--retry", "2", "--retry-delay", "20", "-A", UA, "-o", tmp, "-w", "%{http_code}", u], capture_output=True, text=True)
                time.sleep(2.5)
                if rc.stdout.strip() == "200" and os.path.getsize(tmp) > 3000:
                    try:
                        im = Image.open(tmp); im.load(); im = im.convert("RGB"); im.save(f, "JPEG", quality=90); os.remove(tmp)
                        r["stem"] = stem; r["file"] = f; r["out_w"], r["out_h"] = im.size; r["thumb_w"] = ww; ok = True; break
                    except Exception as e: pass
                if os.path.exists(tmp): os.remove(tmp)
            if ok:
                open(mf, "a").write(json.dumps(r) + "\n"); print("ok", stem, r["out_w"], r["out_h"], flush=True)
            else: print("FAIL", t, flush=True)
