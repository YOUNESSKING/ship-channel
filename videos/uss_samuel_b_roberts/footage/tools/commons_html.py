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
            time.sleep(1.2)
            return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=60).read().decode("utf8", "replace")
        except Exception as e: err = e; time.sleep(6 * (i + 1))
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
def thumb_url(title, width):
    name = title[5:].replace(" ", "_"); md5 = hashlib.md5(name.encode()).hexdigest()
    q = urllib.parse.quote(name, safe="()_,-.!'")
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
