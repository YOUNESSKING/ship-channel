"""v8 check: every number on screen lands on its spoken word, and no shot runs over 6 s.
For every number card / number clip / count / strike-swap / gauge count in chapter/c01-c07.json, the land time the chapter builder
resolves (templates/build_chapter.py Ctx.t, the same resolver the render uses) is compared with the start of the word it names
in build/words.json, and must sit inside its own shot. Also lists every shot over 6.0 s (the end screen excluded).
usage: python3 build/check_numbers.py  -> build/check_numbers_v8.json; exit 1 on a failure"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
sys.path.insert(0, os.path.join(ROOT, "templates"))
import build_chapter as bc
W = json.load(open(os.path.join(HERE, "words.json")))
KEYS = ["c01", "c02", "c03", "c04", "c05", "c06", "c07"]
FIELDS = ["number_at", "swap_at", "count_at", "land_at"]
rows, long_, fails = [], [], []
for k in KEYS:
    B = bc.Builder(os.path.join(FULL, "chapter", f"{k}.json"), media=False); ch = B.chapter; sh = ch["shots"]; off = float(ch["audio_offset"])
    starts = []
    for s in sh:
        st = s.get("start", 0.0)
        starts.append(float(st) if isinstance(st, (int, float)) else bc.Ctx(B, s, starts[-1] if starts else 0.0, 0.0).t(st))
    ends = starts[1:] + [float(ch["duration"])]
    for i, (s, a, b) in enumerate(zip(sh, starts, ends)):
        last = k == "c07" and i == len(sh) - 1
        if b - a > 6.0 + 1e-6 and not last: long_.append(dict(shot=f"{k}:{s['id']}", start=round(off + a, 2), dur=round(b - a, 2)))
        p = s.get("params", {}); specs = []
        for f in FIELDS:
            if isinstance(p.get(f), str) and "@" in p[f]: specs.append((f, p[f], p.get("number") or p.get("new") or p.get("label")))
        if isinstance(p.get("count"), dict) and "@" in str(p["count"].get("land_at", "")): specs.append(("count.land_at", p["count"]["land_at"], p.get("number")))
        for it in p.get("items", []) if isinstance(p.get("items"), list) else []:
            if isinstance(it, dict) and isinstance(it.get("count_at"), str) and "@" in it["count_at"]: specs.append(("items.count_at", it["count_at"], it.get("label")))
        if not specs: continue
        C = bc.Ctx(B, s, a, b)
        for f, spec, what in specs:
            t = C.t(spec)
            m = re.match(r"@([^#+-]+)", spec); txt = m.group(1).strip()
            mo = re.search(r"([+-]\d+(\.\d+)?)$", spec); o = float(mo.group(1)) if mo else 0.0
            inside = a - 1e-3 <= t <= b + 1e-3
            r = dict(shot=f"{k}:{s['id']}", what=str(what), field=f, spec=spec, lands=round(off + t, 3), word_start=round(off + t - o, 3),
                     offset=o, in_shot=inside, shot_span=[round(off + a, 2), round(off + b, 2)])
            rows.append(r)
            if not inside: fails.append(r)
json.dump(dict(numbers=rows, over_6s=long_, fails=fails), open(os.path.join(HERE, "check_numbers_v8.json"), "w"), indent=1, ensure_ascii=False)
for r in rows:
    wd = next((x["w"] for x in W if abs(x["start"] - r["word_start"]) < 1e-3), "?")
    r["word"] = wd
    print(f"{r['shot']:9s} {r['what'][:22]:22s} {r['spec']:22s} lands {r['lands']:8.3f} on '{wd}' {r['word_start']:8.3f} {r['offset']:+.2f}  {'OK' if r['in_shot'] else 'OUTSIDE ITS SHOT'}")
json.dump(dict(numbers=rows, over_6s=long_, fails=fails), open(os.path.join(HERE, "check_numbers_v8.json"), "w"), indent=1, ensure_ascii=False)
print(len(rows), "numbers;", len(fails), "outside their shot;", len(long_), "shots over 6 s", long_)
sys.exit(1 if fails or long_ else 0)
