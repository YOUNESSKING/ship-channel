"""Mallows Bay sound cues for the whole video, one timeline (tools/sound/sfx_mix_lib.py v2: locked roles + levels, real Epidemic
recordings; every cue silent by the next picture cut after its event; beds start/stop with their shots).
Cues come from build/sfx_cNN.json (make_shotlists.py); every "@word" time is resolved with the chapter builder's own resolver
(templates/build_chapter.py Ctx.t), so a sound lands where the text animation lands.
Rules carried over from the Oriskany v8 fixes (SFX_FIX_v4-v6): whooshes only on a few big map moves; no horn (no liner here);
locked min gaps per role (a later cue that breaks one is dropped and logged).
Beds: projector loop under consecutive archive-film shots; waves (river) under today's aerials / NOAA photos of the bay;
drone under the price / cost gauges. Writes audio/sfx.wav, punch.wav, beds.wav, build/sfx_placed.json, build/SFX_PLACED.md."""
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
sys.path.insert(0, os.path.join(ROOT, "tools/sound")); sys.path.insert(0, os.path.join(ROOT, "templates"))
import sfx_mix_lib as L
import build_chapter as bc
FPS = 30
SEGS = {(s["chapter"], s["shot"], s["file"]): s for s in json.load(open(os.path.join(HERE, "segments.json")))}
KEYS = ["c01", "c02", "c03", "c04", "c05", "c06", "c07", "c08"]
CHJ = {k: json.load(open(os.path.join(FULL, "chapter", f"{k}.json"))) for k in KEYS}
TOTAL = round(CHJ["c08"]["audio_offset"] + CHJ["c08"]["duration"], 3)

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

CUES, BEDS, LOG = [], [], []
WHOOSH_MAX = 6
for k in KEYS:
    d = json.load(open(os.path.join(HERE, f"sfx_{k}.json")))
    for c in d["cues"]:
        B, s, a, b = LOCAL[(k, c["shot"])]
        ev = bc.Ctx(B, s, a, b).t(c["at"]) + float(c.get("offset_after", 0.0))
        q = dict(shot=f"{k}:{c['shot']}", at=round(round((ev - a) * FPS) / FPS, 4), role=c["role"], note=c["note"])
        for f in ("file", "src", "len", "tail", "lead"):
            if f in c: q[f] = c[f]
        if "end_shot" in c: q["end_shot"] = f"{k}:{c['end_shot']}"
        CUES.append(q)
# whooshes: only on the first map of a chapter (big moves), at most WHOOSH_MAX
out, nw = [], 0
for c in CUES:
    if c["role"] == "whoosh":
        k = c["shot"].split(":")[0]; first = CHJ[k]["shots"][0]["id"]
        if nw >= WHOOSH_MAX or not any(x["id"] == c["shot"].split(":")[1] for x in CHJ[k]["shots"][:3]):
            LOG.append((k, c["shot"], "whoosh", "dropped (whoosh only on the big chapter-opening map moves)")); continue
        nw += 1
    out.append(c)
CUES = out
CUES.sort(key=lambda c: ST[c["shot"]][0] + c["at"])
last, keep = {}, []
for c in CUES:
    t = ST[c["shot"]][0] + c["at"]; gap = L.KINDS[c["role"]][2]
    if t - last.get(c["role"], -99) < gap: LOG.append((c["shot"].split(":")[0], c["shot"], c["role"], f"dropped: {gap} s min gap ({c['note']})")); continue
    last[c["role"]] = t; keep.append(c)
CUES = keep

TODAY = re.compile(r"^(p|b)_c0\d_s\d+\.mp4$")
def bed_of(k, s):
    clip = ((s.get("clip") or {}).get("file") or "")
    seg = SEGS.get((k, s["id"], clip)); tpl = s.get("template")
    if tpl == "anim_gauge": return "drone"
    if seg and seg["kind"] == "film": return "projector"
    if seg and seg["kind"] == "photo" and re.match(r"(aer_|naip_|usgs_|noaa_)", seg["photo"]) and "ghost_fleet_nara" not in seg["photo"]: return "waves"
    return None
SRC = {"projector": 0.0, "waves": 0.0, "drone": 0.0}
for k in KEYS:
    run = None
    for s in CHJ[k]["shots"]:
        bd = bed_of(k, s); sid = f"{k}:{s['id']}"
        if run and run["role"] == bd: run["end_shot"] = sid; continue
        if run: BEDS.append(run)
        run = None
        if bd:
            SRC[bd] = (SRC[bd] + 37.0) % 100.0
            run = dict(role=bd, shot=sid, end_shot=sid, note={"projector": "projector loop under archive film", "waves": "water under today's bay pictures",
                                                               "drone": "low tension drone (price / cost gauges)"}[bd], fade=0.15 if bd == "projector" else 0.4, src=SRC[bd])
    if run: BEDS.append(run)

if __name__ == "__main__":
    A = os.path.join(FULL, "audio"); os.makedirs(A, exist_ok=True)
    placed, pb = L.render(CUES, SHOTS, TOTAL, os.path.join(A, "sfx.wav"), BEDS, os.path.join(A, "beds.wav"), punch_out=os.path.join(A, "punch.wav"))
    json.dump({"cues": placed, "beds": pb, "shots": SHOTS, "total": TOTAL}, open(os.path.join(HERE, "sfx_placed.json"), "w"), indent=1, ensure_ascii=False)
    bad = [p for p in placed if abs(p["offset_frames"]) > 3]
    R = ["# SFX placed (generated by build/sfx_full.py)", "",
         f"{len(placed)} cues over {TOTAL:.1f} s = {len(placed) / TOTAL * 60:.1f}/min; {len(pb)} bed segments. "
         f"Rendered sync: max |offset| {max(abs(p['offset_frames']) for p in placed):.1f} frames, {len(bad)} cue(s) over 3 frames.", ""]
    R += ["## Dropped", ""] + [f"- {a} {b} {c}: {d}" for a, b, c, d in LOG]
    R += ["", "## Beds", "", "| role | start | end | dB |", "|---|---|---|---|"] + [f"| {b['role']} | {b['start']:.2f} | {b['end']:.2f} | {b['level_db']} |" for b in pb]
    open(os.path.join(HERE, "SFX_PLACED.md"), "w").write("\n".join(R) + "\n")
    print(R[2]); print(len(LOG), "dropped")
    if bad: sys.exit("cues more than 3 frames off: " + ", ".join(f"{p['shot']} {p['role']} {p['offset_frames']}" for p in bad))
