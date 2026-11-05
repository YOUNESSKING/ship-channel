"""Per-cue loudness against the voice, measured (SFX_FIX_v4, 2026-11-05).

Every placed cue (build/sfx_placed.json) is rendered ALONE with the locked renderer (tools/sound/sfx_mix_lib.render, same
file, same region, same trim, its placed level), so overlapping cues do not pollute each other. The mix's ducking is then
applied as measured: G(t) = momentary(audio/mix/sfx_bus.wav) - momentary(audio/sfx.wav) (the sidechain + filters the
SFX stem really got; 0 for punch cues, which are not ducked). Reported per cue, in LU re the voice-bus momentary median
inside words within +-5 s of the event:
  re_voice     = the cue's momentary max (400 ms) over its whole span
  in_words     = the cue's momentary max over the frames where a word is spoken (None: the cue sits in a gap)
  ring         = cue end - picture event (s)
  words        = the words the cue overlaps
usage: python3 build/measure_cues.py [OUT.json]   (needs audio/sfx.wav + audio/mix/{voice,sfx}_bus.wav of the SAME build)"""
import json, os, sys
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
sys.path.insert(0, os.path.join(ROOT, "tools/sound"))
import sfx_mix_lib as L
from measure_mix import momentary, HOP, WIN

PL = json.load(open(os.path.join(HERE, "sfx_placed.json")))
WORDS = json.load(open(os.path.join(HERE, "words.json")))
WORDS = WORDS["words"] if isinstance(WORDS, dict) else WORDS
SHOTS = [tuple(s) for s in PL["shots"]]
PAD = 12.0


def iso(c, p, tmp):
    """render cue c (the build's own cue dict, file pinned to the placed one) alone on a short timeline, every shot shifted so
    the event sits at PAD s: the same region, sync point, shot trims, fades and peak normalisation as in the build."""
    off = p["event"] - PAD
    sh = [(s, a - off, b - off) for s, a, b in SHOTS]
    pl, _ = L.render([dict(c, file=p["file"])], sh, 2 * PAD + 30, tmp, check=False)
    assert abs(pl[0]["start"] + off - p["start"]) < 2e-3 and abs(pl[0]["end"] + off - p["end"]) < 2e-3, (c, pl[0], p)
    a, _ = sf.read(tmp, dtype="float64", always_2d=True)
    a *= 10 ** ((p["level_db"] - pl[0]["level_db"]) / 20)   # the build's level jitter
    return off, momentary(a)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "cue_levels.json")
    A = os.path.join(FULL, "audio"); W = os.path.join(A, "mix")
    rd = lambda p: momentary(sf.read(p, dtype="float64", always_2d=True)[0])
    MV, MB, MS = rd(f"{W}/voice_bus.wav"), rd(f"{W}/sfx_bus.wav"), rd(f"{A}/sfx.wav")
    n = min(len(MV), len(MB), len(MS)); MV, MB, MS = MV[:n], MB[:n], MS[:n]
    G = np.where(MS > -70, np.clip(MB - MS, -30, 3), 0.0)    # duck + filter gain the SFX stem really got
    centre = np.arange(n) * HOP + WIN / 2
    inword = np.zeros(n, bool)
    for w in WORDS: inword |= (centre >= w["start"]) & (centre <= w["end"])
    tmp = os.path.join(os.environ.get("TMPDIR", "/tmp"), f"_cue_{os.getpid()}.wav")
    import sfx_full
    cues = sorted(sfx_full.CUES, key=lambda c: sfx_full.ST[c["shot"]][0] + c["at"])
    assert len(cues) == len(PL["cues"]), "sfx_placed.json is not from the current sfx_full.py: run it first"
    rows = []
    for c, p in zip(cues, PL["cues"]):
        assert c["shot"] == p["shot"] and c["role"] == p["role"], (c, p)
        off, m = iso(c, p, tmp)
        j = np.arange(len(m)); tabs = off + j * HOP + WIN / 2
        sel = (tabs >= p["start"]) & (tabs <= p["end"] + WIN / 2)
        gi = np.clip(np.round((tabs - WIN / 2) / HOP).astype(int), 0, n - 1)
        mm = m + (0.0 if p["punch"] else G[gi])
        loc = inword & (np.abs(centre - p["event"]) < 5)
        vm = float(np.median(MV[loc])) if loc.any() else float(np.median(MV[inword]))
        sw = sel & inword[gi]
        rows.append(dict(role=p["role"], event=p["event"], start=p["start"], end=p["end"], len=round(p["end"] - p["start"], 2),
                         ring=round(p["end"] - p["event"], 2), level_db=p["level_db"], punch=p["punch"],
                         re_voice=round(float(mm[sel].max()) - vm, 1),
                         in_words=round(float(mm[sw].max()) - vm, 1) if sw.any() else None,
                         words=" ".join(w["w"] for w in WORDS if w["start"] < p["end"] and w["end"] > p["start"]), note=p["note"]))
    os.remove(tmp)
    json.dump(rows, open(out, "w"), indent=1, ensure_ascii=False)
    by = {}
    for r in rows: by.setdefault(r["role"], []).append(r)
    for k, v in sorted(by.items()):
        x = [r["re_voice"] for r in v]; iw = [r["in_words"] for r in v if r["in_words"] is not None]
        print(f"{k:10s} n={len(v):3d} re_voice median {np.median(x):+6.1f} max {max(x):+6.1f} | in words max "
              f"{(max(iw) if iw else float('nan')):+6.1f} | ring max {max(r['ring'] for r in v):.2f}")
    print("wrote", out)


if __name__ == "__main__":
    main()
