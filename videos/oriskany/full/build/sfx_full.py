"""Step 3 sound cues for the WHOLE video, on one timeline (tools/sound/sfx_mix_lib.py v2, locked roles + levels, horn -14).

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

# minimum gaps (locked): a later cue that breaks its role's gap is dropped and logged
CUES.sort(key=lambda c: ST[c["shot"]][0] + c["at"])
last, keep = {}, []
for c in CUES:
    t = ST[c["shot"]][0] + c["at"]; gap = L.KINDS[c["role"]][2]
    if t - last.get(c["role"], -99) < gap: LOG.append((c["shot"].split(":")[0], c["shot"], c["role"], f"dropped: {gap} s min gap ({c['note']})")); continue
    last[c["role"]] = t; keep.append(c)
CUES = keep

# ---------------------------------------------------------------- beds c02-c07
def bed_of(k, s):
    clip = ((s.get("clip") or {}).get("file") or "")
    seg = SEGS.get((k, s["id"], clip))
    tpl = s.get("template")
    if seg and seg["kind"] == "film" and not seg.get("generic"): return "projector"
    if tpl in ("anim_gauge", "anim_xray"): return "drone"
    gen = seg["clip"] if seg and seg.get("generic") else None
    if not gen and (s.get("bg_clip") or (tpl == "text_card" and clip.startswith("b_"))):
        bfile = (s.get("bg_clip") or s.get("clip"))["file"]; bs = SEGS.get((k, s["id"], bfile)); gen = bs["clip"] if bs else None
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
