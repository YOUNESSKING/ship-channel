"""MANIFEST.md + CREDITS.md generator for one video build (CLAUDE.md rights rules; STYLE_LOCK 6: credits without links).

Reads
  - the chapter shot list(s) (chapter/*.json): which segment files are ON SCREEN (clip.file and bg_clip.file);
  - the cut lists build/films.py (FILMS: id, clip, ss, dur, label) and build/shots.py (SHOTS: id, NARA id, ...; MONTAGE; FILMS),
    read with `ast` (never executed);
  - footage/FOOTAGE_LIST.md (per item: title, NARA URL, rights field, in point, shows, does NOT show);
  - footage/CREDITS_DRAFT.md (per file: author, date, licence, credit line).
Writes
  - MANIFEST.md: every film clip used | source reel (NARA ID + title) | in/out in the reel | what it shows | what it does NOT show |
    date confidence (HIGH = NARA catalog date stands; MED = the list says to hedge, e.g. a slate disagrees; LOW = undated / verify);
  - CREDITS.md: ONLY the items used, with author / date / licence / credit-line columns, NO URLs (IDs as plain text), plus the
    short description block; non-archive sections (## Music, ## Sound effects, ## Narration, ## Maps and graphics) are kept from the
    existing CREDITS.md with links stripped.

  python3 tools/film/make_paperwork.py videos/oriskany/test_v3            # defaults: chapter/*.json, build/films.py, build/shots.py, ../footage/
  options: --footage DIR  --out-manifest PATH  --out-credits PATH  --dry (print only)
"""
import ast, glob, json, os, re, sys

URL = re.compile(r"(https?://\S+|www\.\S+|\b[\w-]+\.(?:com|org|net|gov|io)(?:/\S*)?)")


def literal(path, name):
    """value of a top-level `NAME = [...]` literal in a python file (not executed)"""
    if not os.path.exists(path): return None
    for node in ast.parse(open(path).read()).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            try: return ast.literal_eval(node.value)
            except Exception: return None
    return None


def md_rows(path):
    """all markdown table rows as lists of cells"""
    rows = []
    for line in open(path):
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def footage_index(path):
    idx = {}
    for r in md_rows(path):
        if len(r) < 9 or r[0] in ("#", "") or r[2] not in ("film", "photo"): continue
        m = re.search(r"src/(?:clips|photos)/([\w.-]+)", r[8])
        if not m: continue
        nid = re.search(r"/id/(\d+)", r[3])
        idx[m.group(1)] = {"title": r[1], "type": r[2], "nara": nid.group(1) if nid else "", "rights": r[4], "inpt": r[5], "shows": r[6], "not": r[7]}
    return idx


def credits_index(path):
    idx = {}
    for r in md_rows(path):
        if len(r) >= 7 and r[0].startswith("src/"):
            idx[os.path.basename(r[0])] = {"what": r[1], "author": r[2], "date": r[3], "licence": r[5], "credit": r[6]}
    return idx


def date_conf(fl, cr):
    txt = (fl.get("not", "") + " " + fl.get("inpt", "")).lower()
    d = (cr or {}).get("date", "")
    if not d or d.lower() in ("undated", "?") or "verify" in txt or "undated" in txt or "not on the print" in txt: return "LOW (undated: no year on screen)"
    if "slate" in txt or 'say "' in txt or "check" in txt: return "MED (" + (re.search(r'say "[^"]+"', fl.get("not", "")) or re.search(r"slate[^;.]*", fl.get("not", "")) or [""])[0] + ")"
    return f"HIGH (NARA catalog date {d})"


def main(vdir, footage=None, out_m=None, out_c=None, dry=False):
    vdir = os.path.abspath(vdir); footage = footage or os.path.join(vdir, "..", "footage")
    used = set()
    for cj in glob.glob(os.path.join(vdir, "chapter", "*.json")):
        for s in json.load(open(cj)).get("shots", []):
            for c in (s.get("clip") or {}, s.get("bg_clip") or {}):
                if c.get("file"): used.add(os.path.splitext(os.path.basename(c["file"]))[0])
    films = (literal(os.path.join(vdir, "build", "films.py"), "FILMS") or []) + (literal(os.path.join(vdir, "build", "shots.py"), "FILMS") or [])
    shots = literal(os.path.join(vdir, "build", "shots.py"), "SHOTS") or []
    mont = literal(os.path.join(vdir, "build", "shots.py"), "MONTAGE")
    if mont and mont[0] in used: used |= set(mont[1])
    FL = footage_index(os.path.join(footage, "FOOTAGE_LIST.md")); CR = credits_index(os.path.join(footage, "CREDITS_DRAFT.md"))
    # ---- film clips on screen
    man, items, missing = [], {}, []
    for f in films:
        sid, clip = f[0], f[1]
        if len(f) > 3 and isinstance(f[3], (int, float)): ss, dur = float(f[2]), float(f[3])            # (id, clip, ss, dur, label)
        else: ss, dur = 0.0, (float(f[2]) if len(f) > 2 and isinstance(f[2], (int, float)) else None)  # (id, clip, dur, label)
        if sid not in used: continue
        fl = FL.get(clip, {}); cr = CR.get(clip)
        if not fl: missing.append(clip)
        m = re.search(r"from\s+(\d+(?:\.\d+)?)s", fl.get("inpt", "")); base = float(m.group(1)) if m else None
        io = f"{base + ss:.1f}-{base + ss + dur:.1f} s" if base is not None and dur else f"clip {ss:.1f}+{dur or 0:.1f} s"
        label = next((x for x in f[2:] if isinstance(x, str) and x), "")
        man.append(f"| {sid} (`{clip}`) | NARA {fl.get('nara', '?')}: {fl.get('title', '?')} | {io} | {fl.get('shows', '?')}" + (f"; on-screen label \"{label}\"" if label else "")
                   + f" | {fl.get('not', '-') or '-'} | {date_conf(fl, cr)} |")
        items[clip] = (fl, cr)
    # ---- photos on screen
    for s in shots:
        if s[0] in used:
            fn = f"nara_{s[1]}.jpg"; items[fn] = (FL.get(fn, {}), CR.get(fn))
            if fn not in FL: missing.append(fn)
    # ---- MANIFEST
    M = ["# MANIFEST: archive film on screen (generated by tools/film/make_paperwork.py; do not edit by hand)", "",
         f"Video build: `{os.path.relpath(vdir, os.path.join(vdir, '../../..'))}`. One row per film segment that the chapter shot list puts on screen. "
         "In/out = seconds in the full NARA reel (FOOTAGE_LIST in-point + the cut list's offset). Rights: US Navy film, NARA, public domain (federal work).", "",
         "| clip | source reel (NARA ID: title) | in/out (reel) | what it shows | what it does NOT show | date confidence |", "|---|---|---|---|---|---|"] + man
    if missing: M += ["", "Not found in FOOTAGE_LIST.md (fix before publishing): " + ", ".join(sorted(set(missing)))]
    # ---- CREDITS (no links)
    def nolink(s):   # "(creativecommons.org/licenses/by/4.0/)" and bare links go; the licence words stay
        s = re.sub(r"\s*\(\s*(?:https?://)?[\w.-]+\.(?:com|org|net|gov|io)(?:/[^)\s]*)?\s*\)", "", s)
        return re.sub(r"\s{2,}", " ", URL.sub("", s)).rstrip(" .;,") + ("." if s.rstrip().endswith(".") else "")
    C = ["# Credits (generated by tools/film/make_paperwork.py from FOOTAGE_LIST.md + CREDITS_DRAFT.md; only items on screen; no links, STYLE_LOCK 6)", "",
         "## Archive photos and film", "", "| item | what | author | date | licence | credit line |", "|---|---|---|---|---|---|"]
    authors = set()
    for fn in sorted(items, key=lambda x: (not x.endswith(".mp4"), x)):
        fl, cr = items[fn]; cr = cr or {}
        lic = nolink(cr.get("licence") or ("public domain (US Gov work); " + fl.get("rights", "")))
        C.append(f"| NARA {fl.get('nara', '?')} ({'film' if fn.endswith('.mp4') else 'photo'}) | {nolink(cr.get('what') or fl.get('title', '?'))} | "
                 f"{cr.get('author') or '?'} | {cr.get('date') or '?'} | {lic} | {cr.get('credit') or '?'} |")
        if cr.get("credit"): authors.add(cr["credit"])
    C += ["", "Description block: Archive film and photos: " + "; ".join(sorted(authors)) + ". All public domain (US federal government works)."]
    old = os.path.join(vdir, "CREDITS.md")
    if os.path.exists(old):
        keep, on = [], False
        for line in open(old).read().splitlines():
            if line.startswith("## "): on = any(k in line for k in ("Music", "Sound", "Narration", "Maps"))
            if on: keep.append(nolink(line) if not line.startswith("|") else line if not URL.search(line) else nolink(line))
        if keep: C += [""] + keep
    out_m = out_m or os.path.join(vdir, "MANIFEST.md"); out_c = out_c or os.path.join(vdir, "CREDITS.md")
    if dry: print("\n".join(M)); print(); print("\n".join(C)); return
    open(out_m, "w").write("\n".join(M) + "\n"); open(out_c, "w").write("\n".join(C) + "\n")
    print(f"wrote {out_m} ({len(man)} film clips) and {out_c} ({len(items)} items)" + (f"; MISSING in FOOTAGE_LIST: {sorted(set(missing))}" if missing else ""))


if __name__ == "__main__":
    a = sys.argv[1:]; kw = {}
    for k in ("--footage", "--out-manifest", "--out-credits"):
        if k in a: i = a.index(k); kw[{"--footage": "footage", "--out-manifest": "out_m", "--out-credits": "out_c"}[k]] = a[i + 1]; del a[i:i + 2]
    dry = "--dry" in a; a = [x for x in a if x != "--dry"]
    main(a[0], dry=dry, **kw)
