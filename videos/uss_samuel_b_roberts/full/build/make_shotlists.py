"""Mallows Bay full video (copied from the Oriskany v8 builder): shot lists c01..c08 (templates/build_chapter.py format, as test v4), per-chapter sound cue lists,
segment specs for the render step, and a report (pacing, film %, clip reuse).

Every beat below = (anchor, sources, options). The anchor is the narration phrase the cut lands on (searched after the
previous shot start). A beat longer than ~4.2 s with several sources is split into pieces (one per source, cut on the
word nearest the even split), so the picture changes every 1.5-4 s. Sources:
  F:<clip>.mp4   real NARA film, from build/film_windows.json (same continuous, vetted shot; never across a cut)
  P:<NARA id> or P:<file stem>   archive photo (footage/src/photos), 2.5D move via archive_shots.py
  M:<scene>      map-kit scene (built in step 2; what it shows = "map" option -> RENDER_PLAN.md)
  H:<scene>      kit/ship hero animation (sinking, cross-sections, tally ...; "hero" option)
  CARD           text_card (option "card")
  A:<template>   anim block rendered by the chapter builder (anim_options / anim_xray / anim_gauge)
Options: num (number_clip), swap (number_clip strike_swap), lt (lower_third kicker_line), card, params (anim), map, hero,
label (film/photo baked label), dim, move (photo), sfx [(role, at, note, extra)], fallback (owner-download fallback note).
Out: chapter/cNN.json, build/sfx_cNN.json, build/segments.json, build/shotlist_report.md
"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
W = json.load(open(os.path.join(HERE, "words.json")))
CH = {c["key"]: c for c in json.load(open(os.path.join(FULL, "chapters.json")))["chapters"]}
sys.path.insert(0, HERE)
from beats import FILMS, B
FW = {}
_CUTS = json.load(open(os.path.join(HERE, "film_cuts.json"))) if os.path.exists(os.path.join(HERE, "film_cuts.json")) else {}
def _split(reel, wins):   # Ranger: never across a detected cut (build/film_cuts.py); pieces under 1.6 s dropped
    out = []
    for a, b in wins:
        cs = [c for c in _CUTS.get(reel, []) if a < c < b]
        edges = [a] + [x for c in cs for x in (c - 0.15, c + 0.2)] + [b]
        for i in range(0, len(edges), 2):
            if edges[i + 1] - edges[i] >= 1.6: out.append([round(edges[i], 2), round(edges[i + 1], 2)])
    return out or wins
_BAD = json.load(open(os.path.join(HERE, "film_bad.json"))) if os.path.exists(os.path.join(HERE, "film_bad.json")) else {}
def _drop_bad(reel, wins):   # SBR: white-outs / blank frames found by build/film_bad.py are cut out like scene cuts
    out = []
    for a, b in wins:
        segs = [[a, b]]
        for x, y in _BAD.get(reel, []):
            nxt = []
            for p, q in segs:
                if y <= p or x >= q: nxt.append([p, q]); continue
                if x - p >= 1.6: nxt.append([p, round(x, 2)])
                if q - y >= 1.6: nxt.append([round(y, 2), q])
            segs = nxt
        out += segs
    return out
for _k, _v in FILMS.items():
    _r, _w, _t = _v[:3]; _w = _drop_bad(_r, _split(_r, _w))
    FW[_k + ".mp4"] = {"reel": _r, "clip_in": 0.0, "windows": _w, "tag": _t, "slow": _v[3] if len(_v) > 3 else None}
def wiki_src(src): return src, None
json.dump(FW, open(os.path.join(HERE, "film_windows.json"), "w"), indent=1)
END_SCREEN = 18.0          # end-screen hold after the last word (music bed + end map)
SPLIT_AT = 4.2             # beats longer than this get split across their sources
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
NW = [norm(x["w"]) for x in W]


def find(phrase, after):
    toks = [norm(x) for x in phrase.replace("-", " ").split() if norm(x)]
    for i in range(len(W) - len(toks) + 1):
        if W[i]["start"] >= after - 0.05 and NW[i:i + len(toks)] == toks:
            return i
    near = " ".join(x["w"] for x in W if abs(x["start"] - after) < 5)
    raise SystemExit(f'anchor "{phrase}" not found after {after:.2f}: {near}')


# ------------------------------------------------------------------------------------------------------------------ build
segments = []; uses = {}; report = []; film_ptr = {}; REEL_USED = {}
mv_i = 0; MOVES = ["in", "out"]   # Nevada (owner 2026-11-18): zoom toward the subject (build/focus.json), no centre pans; mv_i = 0


def film_window(clip, dur, used_at, win=None, reel_in=None):
    """next clean sub-window of the vetted continuous shot (advances, so a reuse shows different frames); win = force window index.
    A clip with "slow" plays slowed down: the window only has to hold need / slow source seconds (the segment keeps its length)."""
    w = FW[clip]["windows"]; need = dur + 0.4
    if reel_in is not None:   # v2: a vetted in-point forced from the frames (c03 Panther / Corsair)
        REEL_USED.setdefault(FW[clip]["reel"], []).append((reel_in, reel_in + need)); return round(reel_in, 2), round(need, 2), ""
    if FW[clip].get("slow"):
        a, b = w[0]; return round(a, 2), round(need, 2), ""
    if win is not None:
        a, b = w[win]; start = a + 0.15; REEL_USED.setdefault(FW[clip]["reel"], []).append((start, start + need))
        return round(start, 2), round(min(need, b - a - 0.2), 2), "" if b - a - 0.2 >= need else "SHORT"
    p = film_ptr.get(clip)
    cand = []
    for a, b in w:
        if b - a >= need: cand.append((a, b))
    if not cand:
        a, b = max(w, key=lambda x: x[1] - x[0]); return a + 0.1, min(b - a - 0.2, need), "SHORT"
    if p is None:
        a, b = max(cand, key=lambda x: x[1] - x[0]); start = a + 0.15
    else:
        start = None
        for a, b in cand:
            s = max(a + 0.15, p + 0.1)
            if s + need <= b: start = s; break
        if start is None: a, b = cand[0]; start = a + 0.15
    # never overlap reel seconds already used by ANY clip of the same reel (b1 launch / b2 Panther-Corsair share reel spans)
    reel = FW[clip]["reel"]; used = REEL_USED.setdefault(reel, [])
    tries = 0
    while any(not (start + need <= u0 or start >= u1) for u0, u1 in used) and tries < 400:
        start += 0.25; tries += 1
        a_ok = [w_ for w_ in cand if w_[0] <= start and start + need <= w_[1]]
        if not a_ok:
            nxt = [w_ for w_ in cand if w_[0] > start]
            if not nxt: break
            start = nxt[0][0] + 0.15
    used.append((start, start + need))
    film_ptr[clip] = start + need
    return round(start, 2), round(need, 2), ""


def piece_times(t0, t1, n, after):
    """split [t0,t1] into n pieces cutting at word starts nearest the even split"""
    cuts = [t0]
    for k in range(1, n):
        target = t0 + (t1 - t0) * k / n
        ws = [x["start"] for x in W if cuts[-1] + 1.2 < x["start"] < t1 - 1.2]
        if not ws: break
        cuts.append(min(ws, key=lambda s: abs(s - target)) - 0.08)
    return cuts


def kind(src): return src.split(":")[0] if ":" in src else src


all_chapters = {}
for ck in ["c01", "c02", "c03", "c04", "c05", "c06", "c07", "c08"]:
    ch = CH[ck]; c0 = ch["start"]; cend = ch["end"] + (END_SCREEN if ck == "c08" else 0.0)
    beats = B[ck]; after = c0
    # resolve beat start times (absolute narration seconds); the first beat starts at the chapter start
    starts = []
    for i, b in enumerate(beats):
        wi = find(b["anchor"], after)
        t = W[wi]["start"] - 0.12
        if i == 0: t = c0
        starts.append(t); after = W[wi]["start"] + 0.05
    shots = []; cues = []; n = 0
    for i, b in enumerate(beats):
        t0 = starts[i]; t1 = starts[i + 1] if i + 1 < len(beats) else cend
        srcs = b["src"]
        npieces = 1
        if (t1 - t0) > SPLIT_AT and len(srcs) > 1: npieces = min(len(srcs), max(2, math.ceil((t1 - t0) / 3.2)))
        pts = piece_times(t0, t1, npieces, after) if npieces > 1 else [t0]
        bounds = pts + [t1]
        for k in range(len(pts)):
            a, z = bounds[k], bounds[k + 1]; src = srcs[k % len(srcs)]; n += 1
            src, fb_shows = wiki_src(src)
            sid = f"s{n:02d}"; kd = kind(src); dur = round(z - a, 3)
            shot = {"id": sid, "start": f"t{a - c0:.2f}", "sfx": False}
            if k == 0 and b.get("tag"): shot["tag"] = b["tag"]          # v2: film date tag (drawn on top by build_chapter)
            clipfile = None
            seg = None
            if kd in ("F", "G"):
                clip = src[2:] if kd == "F" else f"g_{src[2:]}.mp4"; ss, need, flag = film_window(clip, dur, a, b.get("win") if k == 0 else None, b.get("reel_in") if k == 0 else None)
                clipfile = f"f_{ck}_{sid}.mp4"
                seg = dict(file=clipfile, kind="film", clip=clip, reel=FW[clip]["reel"], reel_in=ss, dur=need, label=b.get("label") if k == 0 else None,
                           note=flag)
                if FW[clip].get("slow"): seg["slow"] = FW[clip]["slow"]   # short clean window played slowed (segment keeps the shot length)
                if kd == "G": seg.update(generic=True, tag=FW[clip]["tag"]); shot["tag"] = FW[clip]["tag"]   # v2: tag drawn on top, not burned in
                elif FW[clip].get("tag") and not shot.get("tag"): shot["tag"] = FW[clip]["tag"]   # Mallows: every archive film shot is tagged
                uses.setdefault(clip, []).append(a)
            elif kd == "P":
                pid = src[2:]; move = b.get("move") or MOVES[mv_i % 2]; mv_i += 1
                clipfile = f"p_{ck}_{sid}.mp4"
                seg = dict(file=clipfile, kind="photo", photo=pid, dur=round(dur + 0.35, 2), move=move, depth=True,
                           label=b.get("label") if k == 0 else None, shake=b.get("shake"), fallback=b.get("fallback"))
                uses.setdefault(pid, []).append(a)
            elif kd == "M":
                clipfile = f"m_{src[2:]}.mp4"
                seg = dict(file=clipfile, kind="map", scene=src[2:], dur=round(dur + (0.0 if b.get("endscreen") else 0.35), 2), t0_abs=round(a, 3),
                           narration=" ".join(x["w"] for x in W if a <= x["start"] < z), shows=b.get("map"))
            elif kd == "H":
                clipfile = f"h_{src[2:]}.mp4"
                seg = dict(file=clipfile, kind="hero", scene=src[2:], dur=round(dur + 0.35, 2), t0_abs=round(a, 3),
                           narration=" ".join(x["w"] for x in W if a <= x["start"] < z), shows=fb_shows or b.get("hero"))
                if fb_shows: seg.update(dur=round(dur, 3), replaces=f"p_{ck}_{sid}.mp4")
            elif kd == "MS":   # v4: a slowly pushed still of a rendered map / hero frame ("MS:<segment file>@<sec>|end")
                mf, mt = src[3:].split("@"); clipfile = f"s_{ck}_{sid}.mp4"
                seg = dict(file=clipfile, kind="still", src=mf, at=mt, dur=round(dur + 0.35, 2), move=b.get("move") or "in")
            if seg: segments.append(dict(chapter=ck, shot=sid, **seg))
            bgfile = None
            if b.get("bg") and (k == 0 or kd == "A") and kd in ("A", "CARD"):   # generic US-Gov film UNDER a card (card -> its lower-third / number layout over the film) or an anim (bg_clip)
                bclip = f"g_{b['bg'][2:]}.mp4" if b["bg"].startswith("G:") else b["bg"][2:]; bss, bneed, bflag = film_window(bclip, dur, a, None, b.get("bg_reel_in"))
                bgfile = f"b_{ck}_{sid}.mp4"
                segments.append(dict(chapter=ck, shot=sid, file=bgfile, kind="film", clip=bclip, reel=FW[bclip]["reel"], reel_in=bss, dur=bneed,
                                     label=None, note=bflag, generic=bclip.startswith("g_"), tag=FW[bclip]["tag"], under=kd, **({"slow": FW[bclip]["slow"]} if FW[bclip].get("slow") else {})))
                uses.setdefault(bclip, []).append(a); shot["tag"] = FW[bclip]["tag"]
            if b.get("cbg") and kd == "CARD":   # v4 (owner 2026-11-05: no plain dark text cards): a dimmed MOVING background under a card,
                # the card keeps its centred layout. G: tagged generic film, F: NARA film, P: photo push, MS: pushed map/hero still
                cs = b["cbg"]; ck_ = kind(cs); bgfile = f"b_{ck}_{sid}.mp4"; mv = b.get("cbg_move", "in")
                if ck_ in ("G", "F"):
                    bclip = f"g_{cs[2:]}.mp4" if ck_ == "G" else cs[2:]
                    bss, bneed, bflag = film_window(bclip, dur, a, None, None)
                    sg = dict(chapter=ck, shot=sid, file=bgfile, kind="film", clip=bclip, reel=FW[bclip]["reel"], reel_in=bss, dur=bneed, label=None, note=bflag, under=kd)
                    if ck_ == "G": sg.update(generic=True, tag=FW[bclip]["tag"]); shot["tag"] = FW[bclip]["tag"]
                    elif b.get("cbg_tag"): shot["tag"] = b["cbg_tag"]
                    uses.setdefault(bclip, []).append(a)
                elif ck_ == "P":
                    sg = dict(chapter=ck, shot=sid, file=bgfile, kind="photo", photo=cs[2:], dur=round(dur + 0.35, 2), move=mv, depth=True,
                              label=b.get("cbg_label"), shake=None, fallback=None, under=kd)
                    uses.setdefault(cs[2:], []).append(a)
                else:
                    mf, mt = cs[3:].split("@")
                    sg = dict(chapter=ck, shot=sid, file=bgfile, kind="still", src=mf, at=mt, dur=round(dur + 0.35, 2), move=mv, under=kd)
                segments.append(sg)
            # template
            if kd == "CARD":
                c = dict(b["card"]); var = c.pop("variant")
                shot.update(template="text_card", variant=var, card=True, params=c)
                if bgfile: shot["clip"] = {"file": bgfile, "push": None}
                if b.get("cbg") and var in ("word", "pair", "line"): shot["card_bg"] = True   # centred card over the dimmed background
                if var in ("line", "number") and c.get("kicker") and "kicker_at" not in c:
                    shot["params"]["kicker_at"] = 0.15   # step 3: a card on a dark picture never sits empty until its word (blackdetect found 3.3 s)
            elif kd == "A":
                tpl = src[2:]; p = dict(b["params"]); var = p.pop("variant", None) or {"anim_options": "list", "anim_xray": "animal", "anim_gauge": "bars"}[tpl]
                shot.update(template=tpl, variant=var, params=p)
                if bgfile: shot["bg_clip"] = {"file": bgfile, "show": 0.8}   # Mallows: the moving film must read clearly under the block (no dark cards)
            elif "num" in b and k == 0:
                p = dict(b["num"]); var = p.pop("variant")
                if var == "right": p.pop("dim", None)
                shot.update(template="number_clip", variant=var, clip={"file": clipfile, "push": None}, params=p)
            elif "swap" in b and k == 0:
                p = dict(b["swap"]); shot.update(template="number_clip", variant="strike_swap", clip={"file": clipfile, "push": None}, params=p)
            elif "lt" in b and k == 0:
                p = dict(b["lt"]); shot.update(template="lower_third", variant="kicker_line", clip={"file": clipfile, "push": None}, params=p)
            elif kd == "M":
                shot.update(template="map_clip", variant="baked", clip={"file": clipfile, "push": None}, params={})
            else:
                pr = {"dim": b["dim"]} if b.get("dim") else {}
                shot.update(template="clip_plain", variant="push", clip={"file": clipfile, "push": None}, params=pr)
            if b.get("flash") and k == 0: shot["flash"] = True
            shots.append(shot)
            # ---- sound cues (test v4 roles; density ~16/min; nothing without its picture)
            if b.get("sensitive") or b.get("sfx_none"): pass
            elif k == 0 and b.get("sfx"):
                for role, at, note, extra in b["sfx"]: cues.append(dict(shot=sid, at=at, role=role, note=note, **{k2: (sid if v2 is True else v2) for k2, v2 in extra.items()}))
            elif k == 0 and (kd == "M") and (i == 0 or kind(beats[i - 1]["src"][0]) != "M"):
                cues.append(dict(shot=sid, at=0.3, role="whoosh", note=f"map move starts ({src[2:]})"))
            if k == 0 and shot["template"] == "number_clip" and not b.get("sfx_none") and "number_at" in shot["params"]:
                cues.append(dict(shot=sid, at=shot["params"]["number_at"], role="pop", note=f"number lands: {shot['params'].get('number')}"))
            if k == 0 and shot["template"] == "text_card" and shot["variant"] in ("number", "number_left"):
                cues.append(dict(shot=sid, at=shot["params"]["number_at"], role="pop", note=f"card number lands: {shot['params'].get('number')}"))
            if k == 0 and shot["template"] == "text_card" and shot["variant"] == "word":
                cues.append(dict(shot=sid, at=shot["params"]["at"], role="hit", note=f"stamp: {shot['params'].get('text')}"))
            if k == 0 and not (b.get("sensitive") or b.get("sfx_none")):
                pr = shot.get("params", {}); tpl = shot["template"]
                if tpl == "lower_third": cues.append(dict(shot=sid, at=pr.get("at", 0.3), role="tick", note=f"label: {pr.get('text')}"))
                if tpl == "text_card" and shot["variant"] in ("line", "pair"): cues.append(dict(shot=sid, at=pr.get("at", 0.3), role="pop", note=f"card: {pr.get('text')}"))
                if tpl == "anim_options":
                    for it in pr.get("items", []):
                        cues.append(dict(shot=sid, at=it["at"], role="tick", note=f"option appears: {it['text']}"))
                        if "strike_at" in it: cues.append(dict(shot=sid, at=it["strike_at"], role="tick", note=f"option struck: {it['text']}"))
                        if it.get("chosen"): cues.append(dict(shot=sid, at=it["at"], role="boom", note=f"the answer: {it['text']}"))
                if tpl == "anim_xray":
                    prev = shots[-2]["template"] if len(shots) > 1 else ""
                    if prev != "anim_xray": cues.append(dict(shot=sid, at=0.0, role="riser", note="reverse riser INTO the x-ray", lead=True))
                    if isinstance(pr.get("organ_at"), str): cues.append(dict(shot=sid, at=pr["organ_at"], role="tick", note=f"x-ray mark: {pr.get('organ_label')}"))
                    for r_ in pr.get("readouts", []): cues.append(dict(shot=sid, at=r_["at"], role="tick", note=f"readout: {r_['text']}"))
                if tpl == "anim_gauge":
                    if "count_at" in pr: cues.append(dict(shot=sid, at=pr["count_at"], role="pop", note=f"gauge counts: {pr.get('label')}"))
                    for it in pr.get("items", []):
                        if it.get("hero"): cues.append(dict(shot=sid, at=it["count_at"], role="hit", note=f"gauge hero bar lands: {it['label']}", offset_after=it.get("dur", 1.0)))
                if kd == "M" and i > 0 and kind(beats[i - 1]["src"][0]) == "M": cues.append(dict(shot=sid, at=0.1, role="tick", note=f"map beat ({src[2:]})"))
            # (Nevada, owner 2026-11-18: no hull-groan cues on the sinking film; the Mallows 'steamer going down' rule is removed)
            report.append((ck, sid, round(a, 2), round(dur, 2), shot["template"], src + (f" + bg {b.get('bg') or b.get('cbg')}" if bgfile else ""), b["anchor"]))
    # signature beats per chapter (picture-locked)
    beds = []
    film_shots = [g["shot"] for g in segments if g["chapter"] == ck and g["kind"] == "film" and not g.get("generic")]   # NARA archive film only
    generic_shots = [g["shot"] for g in segments if g["chapter"] == ck and g.get("generic")]
    chj = {"key": ck, "title": f"USS Ranger · {ch['title']}", "words": "../build/words.json", "audio_offset": round(c0, 3),
           "clips_dir": "../segments", "duration": round(cend - c0, 3), "fade_out": 0.6 if ck == "c08" else 0.0, "res": 1080,
           "anim_theme": {"hue": 205, "sat": 0.85}, "font": "oswald", "shots": shots}
    json.dump(chj, open(os.path.join(FULL, "chapter", f"{ck}.json"), "w"), indent=1, ensure_ascii=False)
    json.dump({"chapter": ck, "cues": cues, "film_shots": film_shots, "generic_video_shots": generic_shots,
               "beds_hint": "projector loop under consecutive NARA film shots only (-27; never under the modern generic_video_shots, which get the bed of their scene: sea/waves for tows and storms, underwater for reef fish/divers, room tone for the lab); waves under sea photos/maps; underwater under hero sinking/cross-sections; drone under the fish-test gauges and the x-ray question blocks (-30)"},
              open(os.path.join(HERE, f"sfx_{ck}.json"), "w"), indent=1, ensure_ascii=False)
    all_chapters[ck] = (c0, cend, shots, cues)

# c01 = the approved hook: since v8 (Archive voice) written by build/hook_v8.py (test v4 shots, re-timed to the new words)
json.dump(segments, open(os.path.join(HERE, "segments.json"), "w"), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------------------------------------------------------ report
L = ["# Shot-list report (generated by build/make_shotlists.py)", ""]
tot = {"film": 0, "photo": 0, "map": 0, "hero": 0, "anim": 0, "card": 0}
FILMTOT = {}
L.append("| chapter | dur s | shots | film % | photo % | map % | hero % | anim % | card % | of which NARA film % | generic US-Gov film % | anim over moving film % | **moving video total %** | longest shot | cues/min |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for ck, (c0, cend, shots, cues) in all_chapters.items():
    d = {k: 0.0 for k in tot}
    ss = [r for r in report if r[0] == ck]
    nara = gen = undr = 0.0
    for _, sid, a, du, tpl, src, anc in ss:
        k = kind(src.split(" + bg ")[0]); bg = " + bg " in src
        key = {"F": "film", "G": "film", "P": "photo", "M": "map", "MS": "map", "H": "hero", "A": "anim", "CARD": "card"}[k]
        if key == "card" and bg: key = "film"          # the card's text now sits over moving film (lower-third / number layout)
        if ck == "c08" and src == "M:c08_endscreen": du = max(0.0, du - END_SCREEN)
        d[key] += du
        if k == "F": nara += du
        if k == "G" or (k == "CARD" and bg): gen += du
        if k == "A" and bg: undr += du
    T = sum(d.values()); [tot.__setitem__(k, tot[k] + d[k]) for k in d]
    lg = max(ss, key=lambda r: r[3] if r[5] != "M:c08_endscreen" else 0)
    FILMTOT[ck] = (T, nara, gen, undr)
    L.append(f"| {ck} | {cend - c0:.1f} | {len(ss)} | " + " | ".join(f"{100 * d[k] / T:.0f}" for k in tot)
             + f" | {100 * nara / T:.0f} | {100 * gen / T:.0f} | {100 * undr / T:.0f} | **{100 * (nara + gen + undr) / T:.0f}** | {lg[3]:.1f} s ({lg[1]}) | {len(cues) / ((cend - c0) / 60):.1f} |")
T = sum(tot.values())
_n, _g, _u = (sum(v[i] for v in FILMTOT.values()) for i in (1, 2, 3))
L.append(f"| **c01-c08** | | | " + " | ".join(f"**{100 * tot[k] / T:.0f}**" for k in tot) + f" | **{100 * _n / T:.0f}** | **{100 * _g / T:.0f}** | **{100 * _u / T:.0f}** | **{100 * (_n + _g + _u) / T:.0f}** | | |")
L += ["", "## Pacing flags (shots > 6.0 s or < 1.2 s; end screen excluded)", ""]
for r in report:
    if (r[3] > 6.0 and r[5] != "M:c08_endscreen") or r[3] < 1.2: L.append(f"- {r[0]} {r[1]} {r[3]} s {r[4]} {r[5]} ('{r[6]}')")
L += ["", "## Clip / photo reuse (rule: at most twice, 3+ min apart; hook uses counted from test v4)", ""]
HOOK_USES = {}
for k_ in sorted(set(uses) | set(HOOK_USES)):
    allt = sorted(HOOK_USES.get(k_, []) + uses.get(k_, []))
    bad = len(allt) > 2 or any(b - a < 180 for a, b in zip(allt, allt[1:]))
    if bad: L.append(f"- **{k_}** used at {', '.join(f'{t:.0f}s' for t in allt)}")
REELS = {}
for k_, ts in uses.items():
    if k_.startswith("g_") and k_ in FW: REELS.setdefault(FW[k_]["reel"], []).extend((t, k_) for t in ts)
L += ["", "## Generic reels with more than one use (v2 rule for the DVIDS hull reels: at most 2 uses per reel, 3+ min apart)", ""]
for r_, ts in sorted(REELS.items()):
    ts = sorted(ts)
    if len(ts) > 1: L.append(f"- {r_}: " + ", ".join(f"{t:.0f}s {c}" for t, c in ts) + ("  **CHECK**" if r_ in ("dvids_828554", "dvids_791060") and (len(ts) > 2 or any(y[0] - x[0] < 180 for x, y in zip(ts, ts[1:]))) else ""))
L += ["", "## All shots", "", "| ch | shot | start (abs s) | dur | template | source | cut on |", "|---|---|---|---|---|---|---|"]
L += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |" for r in report]
open(os.path.join(HERE, "shotlist_report.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L[:14]))
print(len(report), "shots c01-c08;", len(segments), "segments")
