"""Step 3 sound cues for the WHOLE video, on one timeline (tools/sound/sfx_mix_lib.py v2, locked roles + levels; v4: horn -20, <= 2 s, voice gaps only, every cue rings <= 1.5 s past its event;
v5 (owner 2026-11-08: SFX -3 dB, ends with its shot): every cue, the hook's included, is silent by the next picture cut after its event; beds start and stop with their shots).

  c01   = the approved test v4 hook cues + beds verbatim (test_v4/build/sfx_cues_v4.py; same shots, same voice samples)
  c02-7 = build/sfx_cNN.json. Every "@word" time is resolved with the chapter builder's own resolver (templates/build_chapter.py
          Ctx.t), so a sound lands where the text animation lands. Then every EVENT cue is re-timed to the frame of the beat
          the picture actually shows (build/anim_beats.json): hero scenes (main beat for "main graphic beat" cues, otherwise
          the nearest beat within 1 s) and the template blocks (gauge / options / x-ray / number counts, nearest within 0.6 s).
          The c05 hero a groan is dropped: since the step-3 re-cut that shot shows the wreck already at rest.
  beds  = projector ONLY under consecutive NARA film shots (film_shots; never under generic_video_shots), waves under the
          sinking-day photos / sea maps / tows and storms, underwater under the hero sinking + reef cross-sections and reef-fish
          / diver b-roll, drone under the PCB gauges and x-ray blocks.
Writes audio/sfx.wav, audio/punch.wav, audio/beds.wav, build/sfx_placed.json, build/SFX_RETIME.md (cue -> beat, frames)."""
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
sys.path.insert(0, os.path.join(ROOT, "tools/sound")); sys.path.insert(0, os.path.join(ROOT, "templates"))
sys.path.insert(0, os.path.join(ROOT, "videos/oriskany/test_v4/build"))
import sfx_mix_lib as L
import build_chapter as bc
FPS = 30
AB = json.load(open(os.path.join(HERE, "anim_beats.json")))
SEGS = {(s["chapter"], s["shot"], s["file"]): s for s in json.load(open(os.path.join(HERE, "segments.json")))}
KEYS = ["c01", "c02", "c03", "c04", "c05", "c06", "c07"]
CHJ = {k: json.load(open(os.path.join(FULL, "chapter", f"{k}.json"))) for k in KEYS}
TOTAL = round(CHJ["c07"]["audio_offset"] + CHJ["c07"]["duration"], 3)

# ---------------------------------------------------------------- global shot table "cNN:sMM" -> (start, end) absolute
SHOTS, LOCAL = [], {}
for k in KEYS:
    B = bc.Builder(os.path.join(FULL, "chapter", f"{k}.json"), media=False); ch = B.chapter; sh = ch["shots"]
    starts = []
    for s in sh:
        st = s.get("start", 0.0)
        starts.append(float(st) if isinstance(st, (int, float)) else bc.Ctx(B, s, starts[-1] if starts else 0.0, 0.0).t(st))
    ends = starts[1:] + [float(ch["duration"])]
    off = float(ch["audio_offset"])
    for s, a, b in zip(sh, starts, ends):
        SHOTS.append((f"{k}:{s['id']}", round(off + a, 3), round(off + b, 3)))
        LOCAL[(k, s["id"])] = (B, s, a, b)
ST = {s[0]: (s[1], s[2]) for s in SHOTS}
ORDER = [s[0] for s in SHOTS]

# ---------------------------------------------------------------- c01: the approved hook, verbatim
import sfx_cues_v4 as V4
CUES, BEDS, LOG = [], [], []
for c in V4.CUES:
    c = dict(c); c["shot"] = "c01:" + c["shot"]
    if "end_shot" in c: c["end_shot"] = "c01:" + c["end_shot"]
    if c["shot"] not in ST or c.get("end_shot", c["shot"]) not in ST: LOG.append(("c01", c["shot"], c["role"], "dropped (shot not in the 48.6 s hook)")); continue
    CUES.append(c)
for b in V4.BEDS:
    b = dict(b); b["shot"] = "c01:" + b["shot"]
    if "end_shot" in b: b["end_shot"] = "c01:" + b["end_shot"]
    if b["shot"] in ST and b.get("end_shot", b["shot"]) in ST: BEDS.append(b)

# ---------------------------------------------------------------- c02-c07: resolve + re-time to the picture's beat frames
TPL = {}
for k, rows in AB["templates"].items():
    if isinstance(rows, list):
        for r in rows: TPL[(k, r["shot"])] = r["beats"]
HERO = {}
for name, sc in AB["scenes"].items(): HERO[(sc["chapter"], sc["shot"])] = (name, sc)
RET = []   # retime report rows
for k in KEYS[1:]:
    d = json.load(open(os.path.join(HERE, f"sfx_{k}.json")))
    for c in d["cues"]:
        B, s, a, b = LOCAL[(k, c["shot"])]
        C = bc.Ctx(B, s, a, b)
        ev = C.t(c["at"]) + float(c.get("offset_after", 0.0))          # chapter-local event time
        clip = (s.get("clip") or {}).get("file", "")
        if clip == "h_c05_hero_a.mp4" and c["role"] == "ship":
            LOG.append((k, c["shot"], c["role"], "dropped: hero a now shows the wreck at rest (no sinking on screen)")); continue
        src, beat = "-", None
        if (k, c["shot"]) in HERO:
            name, sc = HERO[(k, c["shot"])]
            bl = sc["beats"]
            if bl:
                if "main graphic beat" in c["note"] or "retime" in c["note"]:
                    beat = next((x for x in bl if x["main"]), bl[-1]); src = f"{name} main beat"
                else:
                    near = min(bl, key=lambda x: abs((a + x["t"]) - ev))
                    if abs(a + near["t"] - ev) <= 1.0: beat = near; src = f"{name} beat"
                if beat: beat_t = a + beat["t"]; bnote = beat["note"]
        elif (k, c["shot"]) in TPL and c["role"] not in ("riser", "whoosh"):
            bl = TPL[(k, c["shot"])]
            near = min(bl, key=lambda x: abs(x["chapter_t"] - ev))
            if abs(near["chapter_t"] - ev) <= 0.6: beat = near; beat_t = near["chapter_t"]; bnote = near["note"]; src = f"{s['template']} block"
        if beat is not None:
            new = round(round(beat_t * FPS) / FPS, 4)                   # on the beat's frame
            RET.append((k, c["shot"], c["role"], c["note"], round(ev, 3), new, round((ev - new) * FPS, 1), src, bnote))
            ev = new
        q = dict(shot=f"{k}:{c['shot']}", at=round(ev - a, 4), role=c["role"], note=c["note"])
        for f in ("file", "src", "len", "tail", "lead"):
            if f in c: q[f] = c[f]
        if "end_shot" in c: q["end_shot"] = f"{k}:{c['end_shot']}"
        CUES.append(q)

# ---------------------------------------------------------------- v2: critic B fix order (roles and levels unchanged: only WHICH
# cues play, and their timing). Times are absolute narration seconds (the same as in CRITIQUE_B; the v2 picture keeps every anchor).
HOOK_END = CHJ["c02"]["audio_offset"]
WHOOSH_KEEP = [153.66, 484.78, 686.84]               # M1: only the 3 biggest moves of the body (+ the approved hook pair)
RISER_KEEP = [266.17, 516.58, 565.88, 809.57]        # S5: first x-ray, 22 charges, PCBs, the answer
END_WHOOSH = 865.9                                   # S4: end-screen whoosh after "comments."
# v3: the ending cut (build/cuts_v3.json) moved every time after 805.4 s; the rules below stay written in v2 (critique) times
_CUTS = json.load(open(os.path.join(HERE, "cuts_v3.json")))["cuts"] if os.path.exists(os.path.join(HERE, "cuts_v3.json")) else []
def to_v2(t):
    for c in _CUTS:
        if t >= c["t0"] - 1e-6: t += c["dur"]
    return t
def to_v3(t):
    d = 0.0
    for c in _CUTS:
        if t >= c["t1"]: d += c["dur"]
    return t - d
def T(c): return to_v2(ST[c["shot"]][0] + c["at"])
def shot_at(t): return next(s for s, a, b in SHOTS if a <= t < b)
def clip_of(shot):
    k, sid = shot.split(":"); s = LOCAL[(k, sid)][1]; return (s.get("clip") or {}).get("file", "")
V2 = []; out = []
for c in CUES:
    t = T(c)
    if t < HOOK_END - 0.01: out.append(c); continue   # (t = v2 time)                      # the approved hook: untouched
    r, note = c["role"], c["note"]
    if r == "whoosh":
        if any(abs(t - w) < 1.0 for w in WHOOSH_KEEP): out.append(c)
        elif t > 860 and not any(x.get("_end") for x in out):
            ew = to_v3(END_WHOOSH); sh = shot_at(ew); c = dict(c, shot=sh, at=round(ew - ST[sh][0], 3), _end=True); out.append(c); V2.append((t, r, f"moved to {END_WHOOSH} (S4)"))
        else: V2.append((t, r, "dropped (M1: whoosh only on the 3 biggest moves)"))
        continue
    if r == "jet" and "b1_launch" in note:
        V2.append((t, r, "dropped (M2: 1945 ship launch, no aircraft on screen)")); continue
    if r == "hit" and ("gauge hero bar" in note or abs(t - 106.2) < 0.6):
        c = dict(c, role="pop"); V2.append((t, "hit", "re-roled to pop (M3)"))
    if r == "riser" and not any(abs(t - w) < 1.5 for w in RISER_KEEP):
        V2.append((t, r, "dropped (S5: riser on 4 key x-rays only)")); continue
    if r == "ship" and "air bursting out" in note:
        V2.append((t, r, "dropped (N3: inaudible bubbles)")); continue
    if r == "ship" and "flood" in note and t > 850:
        V2.append((t, r, "dropped (S4: closing question stays clean)")); continue
    if r == "ship" and "groan" in note and 530 < t < 537:
        if 530 < t < 532:     # S3: groan 1 after "minutes.", runs on through the stern-first shot
            nxt = ORDER[ORDER.index(c["shot"]) + 1]
            c = dict(c, at=round(to_v3(532.80) - ST[c["shot"]][0], 3), end_shot=nxt); V2.append((t, r, "moved to 532.80 (S3)"))
        else: V2.append((t, r, "dropped (S3: groan 2 masked 'down stern first')")); continue
    if r == "horn" and 824 < t < 827:   # N4: the horn in the voice gap before "On November twelfth"
        nxt = ORDER[ORDER.index(c["shot"]) + 1]
        c = dict(c, at=round(to_v3(827.55) - ST[c["shot"]][0], 3), end_shot=nxt); V2.append((t, r, "moved to 827.55 (N4)"))
    out.append(c)
    if r == "explosion" and 525.5 < t < 527:   # S3: boom layer under the c05 charges, as the hook does at 17.65 (locked boom level)
        out.append(dict(shot=c["shot"], at=c["at"], role="boom", note="charges fire: boom layer (as the hook)")); V2.append((t, "boom", "added (S3)"))
CUES = [{k: v for k, v in c.items() if k != "_end"} for c in out]
LOG += [("v2", f"{t:.2f}", r, w) for t, r, w in V2]

# minimum gaps (locked): a later cue that breaks its role's gap is dropped and logged
CUES.sort(key=lambda c: ST[c["shot"]][0] + c["at"])
last, keep = {}, []
for c in CUES:
    t = ST[c["shot"]][0] + c["at"]; gap = L.KINDS[c["role"]][2]
    if t - last.get(c["role"], -99) < gap: LOG.append((c["shot"].split(":")[0], c["shot"], c["role"], f"dropped: {gap} s min gap ({c['note']})")); continue
    last[c["role"]] = t; keep.append(c)
CUES = keep

# ---------------------------------------------------------------- v4: SFX_FIX_v4 (owner 2026-11-05: "the horn, that sound is too long
# and it's too loud"; see build/SFX_FIX_v4.md). Horn: -20 dB and <= 2 s (sfx_mix_lib), at most 2 per video, and ONLY in a voice gap
# while the liner is on screen, never under a word (this applies to the hook too). Every other cue: the lib caps its ring at 1.5 s
# past the picture event; the approved hook keeps its own cue lengths (ring uncapped) apart from the horn.
WORDS = json.load(open(os.path.join(HERE, "words.json"))); WORDS = WORDS["words"] if isinstance(WORDS, dict) else WORDS
HORN_GAP_MIN, HORN_MAX, HORN_PAD = 0.6, 2.0, 0.06     # usable gap >= 0.6 s; event 60 ms after the word, end 20 ms before the next
def voice_gaps(t0, t1):
    """voice gaps (a, b) clipped to [t0, t1]"""
    ends = [0.0] + [w["end"] for w in WORDS]; starts = [w["start"] for w in WORDS] + [1e9]
    return [(max(a, t0), min(b, t1)) for a, b in zip(ends, starts) if min(b, t1) > max(a, t0)]
V4 = []; out = []
for c in CUES:
    t = ST[c["shot"]][0] + c["at"]
    if c["role"] == "jet" and "b3_aerial_launching" in c["note"]:   # measured +6.7 LU over the voice on "the man who led" (jet role
        V4.append((t, "jet", "dropped: +6.7 LU over the words 'the man who led' (jet median +2.8; a 0.9 s slice peak-normalised hot)")); continue
    if c["role"] != "horn":
        # SFX_FIX_v5 (owner 2026-11-08: "the sound effects are a bit louder and they stay after the scene is over"; this overrides the
        # "don't touch the hook" rule for sound effects only): the hook cues lose their uncapped ring, so the 1.5 s ring cap and the
        # lib's shot-end rule (silent by the next cut after the event) apply to the whole video.
        out.append(c); continue
    i0 = ORDER.index(c["shot"]); i1 = ORDER.index(c.get("end_shot", c["shot"]))
    lo, hi = ST[c["shot"]][0], ST[ORDER[i1]][1]                      # the liner shots this horn belongs to
    g = [(a, b) for a, b in voice_gaps(lo, hi + HORN_MAX) if a < hi and b - a - HORN_PAD - 0.02 >= HORN_GAP_MIN]
    g = [x for x in g if x[0] >= t - 2.0] or g
    if not g or len([x for x in out if x["role"] == "horn"]) >= 2:
        V4.append((t, "horn", f"dropped: no voice gap >= {HORN_GAP_MIN} s on the liner shots {c['shot']}..{ORDER[i1]} "
                               f"({', '.join(f'{a:.2f}-{b:.2f}' for a, b in voice_gaps(lo, hi)) or 'none'}): it played under speech"))
        continue
    a, b = g[0]; ev = round(a + HORN_PAD, 3); ln = round(min(HORN_MAX, b - 0.02 - ev), 3)
    sh = shot_at(ev); last = shot_at(min(ev + ln, ST[ORDER[-1]][1] - 1e-3))
    c = dict(c, shot=sh, at=round(ev - ST[sh][0], 3), len=ln, end_shot=last, tail=0.0, note=c["note"].replace("-14", "-20, voice gap"))
    V4.append((t, "horn", f"moved to {ev:.2f}, {ln:.2f} s in the voice gap {a:.2f}-{b:.2f} (fade 0.6 s, -20 dB)"))
    out.append(c)
CUES = out
LOG += [("v4", f"{t:.2f}", r, w) for t, r, w in V4]

# ---------------------------------------------------------------- v6: SFX_FIX_v6 (critic build/CRITIQUE_SFX_v5.md; owner 2026-11-08: quieter
# SFX, nothing hanging over the scenes). Every change only takes sound away, except M1, which gives the 2nd hook blast back the voice
# gap after its 0.33 s flash (a one-off exception, listed in check_sound_lock.GAP_CARRY_CUES). Matched by (role, event s).
def _next_word(t): return min(w["start"] for w in WORDS if w["start"] > t)
V6 = {   # (role, event): (changes, why)
    ("explosion", 17.65): (dict(gap_carry="word"), "M1: ends on 'Thirty' (18.22), 0.25 s fade, inside the voice gap"),
    ("boom", 17.65):      (dict(gap_carry="word"), "M1: ends on 'Thirty' (18.22), 0.25 s fade, inside the voice gap"),
    ("impact", 19.85):    (dict(lowpass=800, gain=-3.0), "M2 + v7: lowpass 800 Hz, -3 dB under 'she was gone.' ('was' still masked in v6)"),
    ("jet", 232.11):      (dict(gain=-3.0), "v7: jet -3 dB ('more' / 'than')"),
    ("jet", 235.89):      (dict(gain=-3.0), "v7: jet -3 dB ('one' at 236.45)"),
    ("jet", 325.94):      (dict(gain=-3.0), "v7: jet -3 dB ('the' at 326.10)"),
    ("ship", 19.90):      (dict(lowpass=1200, gain=-3.0), "M2: flood lowpass 1200 Hz, -3 dB"),
    ("ship", 26.25):      (dict(gain=-3.0), "S1: groan -3 dB under 'millions to put'"),
    ("impact", 28.70):    (dict(lowpass=1000), "S2: lowpass 1000 Hz on 'floor?'"),
    ("whoosh", 45.80):    (dict(ring=0.8), "S4: ring 0.8 s under 'About thirteen'"),
    ("ship", 532.80):     (dict(cut_fade=0.4), "S6: 0.4 s fade ending on the 533.553 cut"),
    ("ship", 537.69):     (dict(lowpass=1200, gain=-3.0), "S3: flood lowpass 1200 Hz, -3 dB under 'Then she was gone.'"),
}
# S5: the 40 pops / ticks the critic measured > 10 dB under the rest of the mix (masked by speech): deleted, nothing raised
S5_DROP = [18.69, 22.79, 61.52, 90.99, 94.25, 96.42, 106.20, 116.16, 119.44, 127.11, 141.70, 148.59, 182.56, 202.94, 268.74, 284.04,
           417.56, 426.41, 429.49, 467.50, 474.44, 477.63, 529.38, 549.92, 556.13, 569.48, 592.44, 610.88, 649.44, 685.11, 706.88, 724.60,
           730.83, 743.59, 757.44, 760.95, 763.88, 774.18, 786.01, 815.21]
V6LOG, out, hit6, drop6 = [], [], set(), set()
for c in CUES:
    t = ST[c["shot"]][0] + c["at"]
    d = next((x for x in S5_DROP if abs(x - t) < 0.02), None)
    if d is not None and c["role"] in ("pop", "tick"):
        drop6.add(d); V6LOG.append((t, c["role"], "dropped (S5: > 10 dB under the mix, masked)")); out.append(dict(c, drop=True)); continue
    k = next((k for k in V6 if k[0] == c["role"] and abs(k[1] - t) < 0.02), None)
    if k:
        ch, why = V6[k]; ch = dict(ch); hit6.add(k)
        if ch.get("gap_carry") == "word":
            cut = next(b for s_, a_, b in SHOTS if a_ <= t + 1e-4 < b)
            ch["gap_carry"] = round(_next_word(t) - cut, 3)
        c = dict(c, **ch); V6LOG.append((t, c["role"], why))
    out.append(c)
assert len(drop6) == len(S5_DROP), sorted(set(S5_DROP) - drop6)
assert len(hit6) == len(V6), set(V6) - hit6
CUES = out
LOG += [("v6", f"{t:.2f}", r, w) for t, r, w in V6LOG]

# ---------------------------------------------------------------- beds c02-c07
def bed_of(k, s):
    clip = ((s.get("clip") or {}).get("file") or "")
    seg = SEGS.get((k, s["id"], clip))
    tpl = s.get("template")
    if seg and seg["kind"] == "film" and not seg.get("generic"): return "projector"
    if tpl in ("anim_gauge", "anim_xray"): return "drone"
    gen = seg.get("clip") if seg and seg.get("generic") else None
    if not gen and (s.get("bg_clip") or (tpl == "text_card" and clip.startswith("b_"))):
        bfile = (s.get("bg_clip") or s.get("clip"))["file"]; bs = SEGS.get((k, s["id"], bfile)); gen = bs.get("clip") if bs else None   # v4: card backgrounds of kind "still" have no clip
    if gen:
        if re.search(r"snap_|reef_fish|keys_diver|navy_wreck", gen): return "underwater"
        if re.search(r"kh_|fm_|rita|gustav|recfish", gen): return "waves"
        return None
    if clip.startswith("h_c06_"): return "drone"
    if clip.startswith("h_c05_") or clip.startswith("h_c07_") and "tally" not in clip: return "underwater"
    if k == "c05" and (clip.startswith("p_") or clip.startswith("m_")): return "waves"
    if re.match(r"m_(c02_(tow_sf|horn_)|c04_(tow_pens|hurricane|rita)|c06_(fishmap|rubble|tag)|c07_(dive|gustav))", clip): return "waves"
    return None
SRC = {"projector": 0.0, "waves": 0.0, "underwater": 0.0, "drone": 0.0}
for k in KEYS[1:]:
    run = None
    for s in CHJ[k]["shots"]:
        bd = bed_of(k, s); sid = f"{k}:{s['id']}"
        if run and run["role"] == bd: run["end_shot"] = sid; continue
        if run: BEDS.append(run)
        run = None
        if bd:
            SRC[bd] = (SRC[bd] + 37.0) % 120.0
            run = dict(role=bd, shot=sid, end_shot=sid, note={"projector": "projector loop under NARA archive film", "waves": "sea", "underwater": "underwater ambience",
                                                               "drone": "low tension drone (PCB gauges / x-ray)"}[bd], fade=0.15 if bd == "projector" else 0.4, src=SRC[bd])
    if run: BEDS.append(run)

if __name__ == "__main__":
    A = os.path.join(FULL, "audio"); os.makedirs(A, exist_ok=True)
    placed, pb = L.render(CUES, SHOTS, TOTAL, os.path.join(A, "sfx.wav"), BEDS, os.path.join(A, "beds.wav"), punch_out=os.path.join(A, "punch.wav"))
    json.dump({"cues": placed, "beds": pb, "shots": SHOTS, "total": TOTAL}, open(os.path.join(HERE, "sfx_placed.json"), "w"), indent=1, ensure_ascii=False)
    bad = [p for p in placed if abs(p["offset_frames"]) > 3]
    R = ["# SFX re-timing to the animation beat frames (generated by build/sfx_full.py)", "",
         f"{len(placed)} cues over {TOTAL:.1f} s = {len(placed) / TOTAL * 60:.1f}/min; {len(pb)} bed segments. "
         f"Rendered sync: max |offset| {max(abs(p['offset_frames']) for p in placed):.1f} frames, {len(bad)} cue(s) over 3 frames.", "",
         "## Cues moved onto a beat frame (anim_beats.json)", "", "| chapter | shot | role | was (chapter s) | now (chapter s) | moved (frames) | beat source | beat |", "|---|---|---|---|---|---|---|---|"]
    for r in RET: R.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[4]:.3f} | {r[5]:.3f} | {r[6]:+.1f} | {r[7]} | {r[8]} |")
    R += ["", "## Dropped / changed", ""] + [f"- {a} {b} {c}: {d}" for a, b, c, d in LOG]
    R += ["", "## Beds", "", "| role | start | end | dB |", "|---|---|---|---|"] + [f"| {b['role']} | {b['start']:.2f} | {b['end']:.2f} | {b['level_db']} |" for b in pb]
    open(os.path.join(HERE, "SFX_RETIME.md"), "w").write("\n".join(R) + "\n")
    print(R[2]); print(len(RET), "cues re-timed to beats;", len(LOG), "dropped")
    if bad: sys.exit("cues more than 3 frames off: " + ", ".join(f"{p['shot']} {p['role']} {p['offset_frames']}" for p in bad))
