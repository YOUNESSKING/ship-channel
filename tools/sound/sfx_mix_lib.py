"""Ship-channel SFX renderer v2 (battle-maps STYLE_LOCK sections 3 / 3a / 2a sound-design table, real recordings only).

What changed from v1 (critics, videos/oriskany/test_v3/CRITIQUE_SOUND_ACCURACY.md):
  * the synthesized kit (kit/ship/sfx/out) is gone: every role plays a REAL Epidemic Sound recording
    (assets/sfx/epidemic/, git-ignored; catalog + re-download list: assets/sfx/EPIDEMIC_SFX.md);
  * the kit files are levelled the battle-maps way: every one-shot segment is peak-normalised to -3 dBFS (all
    battle-maps kit files cand1-4_hit, hit, zoom_whoosh, jet_flyby... peak at -3 dBFS), then the locked role dB is
    applied; beds (loops) are RMS-normalised to -20 dBFS first, then their role dB;
  * cues are placed from the VISUAL EVENT FRAME: event = shot start + offset (from the chapter's shot timeline). The
    sound's own sync point (its loudest 50 ms for hits/booms/blasts/jets/risers, its onset for whooshes, rushes,
    groans, horns and beds) is measured from the audio and put on that frame;
  * every cue is trimmed to its shot: it may not run past the end of `end_shot` (default: its own shot) + `tail`
    (default 0.12 s, a fade that ends ~4 frames after the cut). A designed tail must be written in the cue;
  * after rendering, every cue's sync point is MEASURED again on the trimmed, faded segment and reported in frames
    (check_sound_lock.check_cues fails the build on > 3 frames).

Cue dict: {"shot": id, "at": s after shot start, "role": kind, "file": optional, "src": s into the file where the
usable region starts (optional), "len": max s, "tail": s, "end_shot": id, "lead": True (may start before its
shot, only for risers INTO a reveal), "ring": max s past the event (default RING_MAX, None = uncapped), "fade": fade-out s,
"note": text}
"""
import hashlib, json, os
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SR = 48000
FPS = 30
D = os.path.join(ROOT, "assets", "sfx", "epidemic")
PEAK_NORM_DB = -3.0     # battle-maps kit convention (every locked kit file peaks at -3 dBFS)
BED_RMS_DB = -20.0      # beds: RMS-normalised, then their role level
TAIL_DEFAULT = 0.12
# SFX_FIX_v4 (owner 2026-11-05, "the horn is too long"): no effect rings on more than RING_MAX s past its picture event
# (beds excluded: they are not cues). A longer, designed ring must be written in the cue ("ring": s, or None = no cap).
RING_MAX = 1.5
RING_ROLE = {"horn": 2.0}           # the horn: at most ~2 s in all (owner 2026-11-05)
FADE_ROLE = {"horn": 0.6}           # a short natural fade-out (s); other roles keep min(0.25 s, 35 % of the cue)
# Big beats (blasts, impacts, key booms) go to their own "punch" stem that the voice does NOT duck, so they read
# momentarily louder than speech (target: momentary max >= +3 LU over speech). Every other cue stays on the SFX stem,
# ducked lightly under the voice (STYLE_LOCK 5). A cue can opt out with "punch": False.
PUNCH_ROLES = ("explosion", "impact", "boom")

# kind: (default files, level dB, min gap s, sync type)
# Levels: battle-maps STYLE_LOCK section 3 (explosion -4, impact -7, hit -8, jet -11, whoosh -12, tick -20) and the
# section 2a sound-design table (pop -20, boom -11, riser -17, projector -27, drone bed -30). "ship" and "horn" are
# ship-channel roles (no battle-maps equivalent): ship = the on-screen vehicle level (prop flyby, -13); horn = the
# signature horn, -20, in a voice gap only, never under speech (owner 2026-11-04: -14, 4 dB quieter than the -10 test;
# owner 2026-11-05: shorter (<= 2 s) and 6 dB quieter, at most 2 horns per video). Owner-approved.
KINDS = {
    "explosion": (["charges_c__f6f10ea4.wav", "charges_a__955e7371.wav", "charges_b__0ecb5c38.wav"], -4, 0.20, "peak"),
    "impact":    (["splash_a__1d6949d6.wav", "charges_b__0ecb5c38.wav", "splash_b__3ba7bd2a.wav"], -7, 0.25, "peak"),
    "hit":       (["boom_a__2f0a40ab.wav"], -8, 0.50, "peak"),
    "boom":      (["boom_a__2f0a40ab.wav"], -11, 0.50, "peak"),
    "pop":       (["pop_b__844f57e0.wav"], -20, 0.12, "peak"),
    "whoosh":    (["whoosh_a__689b1489.wav", "whoosh_b__8d9712d2.wav"], -12, 0.50, "onset"),
    "riser":     (["riser_a__fd98cb0b.wav", "riser_b__dbd5c65b.wav"], -17, 2.0, "peak"),
    "jet":       (["jet_a__9fc48bf0.wav", "jet_b__da6a1527.wav", "jet_c__d47bee57.wav"], -11, 1.2, "peak"),
    "ship":      (["groan_a__7c63fd7c.wav", "flood_a__db95b348.wav", "bubbles_a__e58b390c.wav", "groan_b__2bc7c5e1.wav",
                   "groan_c__87dfc4bf.wav", "flood_b__3e14e767.wav", "bubbles_b__18fdc570.wav"], -13, 0.5, "onset"),
    "horn":      (["horn_a__463af07a.wav"], -20, 3.0, "onset"),   # owner 2026-11-05: shorter (<= 2 s) and 6 dB quieter
    "tick":      (["pop_a__9da883ac.wav"], -20, 0.12, "peak"),
}
BEDS = {  # bed role: (default files, level dB)   (STYLE_LOCK 2a: projector loop under film -27, low drone bed -30)
    "projector":  (["projector_b__5648e70b.wav", "projector_a__6f4d59cf.wav"], -27),
    "drone":      (["drone_a__244a55e9.wav"], -30),
    "waves":      (["waves_a__3d49f79f.wav"], -30),
    "underwater": (["underwater_a__127d88ce.wav"], -30),
}
# default usable region per file: (src s, max len s). Picked from the measured envelopes (EPIDEMIC_SFX.md).
REGION = {
    "charges_c__f6f10ea4.wav": (1.70, 1.2),    # 2nd detonation of the real distant sequence (crack at 1.80)
    "charges_a__955e7371.wav": (17.0, 2.0),    # real underwater thunderflash thump
    "charges_b__0ecb5c38.wav": (17.45, 1.6),   # real underwater thump, crack at 17.62
    "splash_a__1d6949d6.wav":  (0.0, 1.2),
    "splash_b__3ba7bd2a.wav":  (0.0, 1.2),
    "boom_a__2f0a40ab.wav":    (0.0, 1.4),
    "boom_b__240e5b47.wav":    (0.0, 1.4),
    "pop_b__844f57e0.wav":     (0.0, 0.25),
    "pop_a__9da883ac.wav":     (0.45, 0.21),
    "whoosh_a__689b1489.wav":  (0.15, 2.3),
    "whoosh_b__8d9712d2.wav":  (0.20, 3.2),
    "riser_a__fd98cb0b.wav":   (0.0, 2.26),
    "riser_b__dbd5c65b.wav":   (0.0, 5.0),
    "jet_a__9fc48bf0.wav":     (4.00, 3.0),
    "jet_b__da6a1527.wav":     (4.0, 3.0),
    "jet_c__d47bee57.wav":     (7.0, 4.0),
    "groan_a__7c63fd7c.wav":   (7.55, 3.0),
    "flood_a__db95b348.wav":   (0.70, 3.0),
    "bubbles_a__e58b390c.wav": (2.95, 1.6),
    "horn_a__463af07a.wav":    (0.20, 2.0),    # owner 2026-11-05: the best 2 s of the 1st blast = its onset + swell (was 7.6 s)
}


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def load(f):
    p = os.path.join(D, f)
    if not os.path.exists(p):
        raise SystemExit(f"missing Epidemic SFX {f}: re-download it (assets/sfx/EPIDEMIC_SFX.md lists the IDs)")
    a, sr = sf.read(p, dtype="float32", always_2d=True)
    assert sr == SR, f
    if a.shape[1] == 1:
        a = np.repeat(a, 2, axis=1)
    return a[:, :2]


def envelope(a, win=0.05, hop=0.01):
    m = a.mean(axis=1) if a.ndim == 2 else a
    w, h = int(win * SR), int(hop * SR)
    if len(m) < w:
        m = np.pad(m, (0, w - len(m)))
    c = np.concatenate([[0.0], np.cumsum(m.astype("float64") ** 2)])
    n = (len(m) - w) // h + 1
    e = (c[np.arange(n) * h + w] - c[np.arange(n) * h]) / w
    return 10 * np.log10(e + 1e-12)          # frame i covers [i*hop, i*hop+win]


def sync_point(a, kind):
    """Sync point in seconds from the segment start: centre of the loudest 50 ms ('peak') or the first 10 ms frame
    within 20 dB of the segment's loudest 50 ms ('onset')."""
    e = envelope(a)
    if kind == "peak":
        return float(np.argmax(e) * 0.01 + 0.025)
    return float(np.argmax(e > e.max() - 20) * 0.01)


def shot_table(chapter, words):
    """[(id, start, end)] from a chapter json (start = number | 't12.3' | 'w17' = word index)."""
    def st(s):
        s = s["start"]
        if isinstance(s, (int, float)): return float(s)
        return float(s[1:]) if s[0] == "t" else float(words[int(s[1:])]["start"])
    S = chapter["shots"]; out = []
    for i, s in enumerate(S):
        out.append((s["id"], st(s), st(S[i + 1]) if i + 1 < len(S) else float(chapter["duration"])))
    return out


def render(cues, shots, total, out, beds=(), beds_out=None, check=True, seed=7, punch_out=None):
    """cues -> stereo SFX stem (+ the unducked punch stem when punch_out is given); beds -> stereo bed stem.
    Returns (placed, placed_beds)."""
    if check:
        import check_sound_lock
        check_sound_lock.check(KINDS, BEDS)
    S = {sid: (a, b) for sid, a, b in shots}
    rng = np.random.default_rng(seed)
    buf = np.zeros((int((total + 2) * SR), 2), "float32"); pbuf = np.zeros_like(buf)
    last, placed, used = {}, [], {}
    for c in sorted(cues, key=lambda c: S[c["shot"]][0] + c["at"]):
        kind = c["role"]; files, db, gap, stype = KINDS[kind]
        event = S[c["shot"]][0] + c["at"]
        if event - last.get(kind, -99) < gap:
            raise SystemExit(f"cue {kind} at {event:.2f} breaks the {gap} s minimum gap (move or drop it)")
        last[kind] = event
        f = c.get("file") or files[used.get(kind, 0) % len(files)]; used[kind] = used.get(kind, 0) + 1
        src0, maxlen = REGION.get(f, (0.0, 2.0))
        src = c.get("src", src0); maxlen = c.get("len", maxlen)
        a = load(f)
        reg = a[int(src * SR): int((src + maxlen) * SR)].copy()
        rel = sync_point(reg, stype)
        start = event - rel
        if start < S[c["shot"]][0] - 1e-6 and not c.get("lead"):   # never sound before the event's own shot
            cut = S[c["shot"]][0] - start; reg = reg[int(cut * SR):]; start = S[c["shot"]][0]; rel -= cut
        end_shot = c.get("end_shot", c["shot"]); tail = c.get("tail", TAIL_DEFAULT)
        end_allowed = S[end_shot][1] + tail
        ring = c.get("ring", RING_ROLE.get(kind, RING_MAX))
        if ring is not None: end_allowed = min(end_allowed, event + ring)
        L = min(len(reg) / SR, end_allowed - start, total - start)
        seg = reg[: int(L * SR)].copy()
        fi = min(int(0.005 * SR), len(seg) // 4) if stype == "peak" else min(int(0.02 * SR), len(seg) // 4)
        fo = min(int(c.get("fade", FADE_ROLE.get(kind, 0.25)) * SR), int(len(seg) * (0.67 if kind in FADE_ROLE or "fade" in c else 0.35)))
        if stype == "peak":   # the fade-out never touches the sync point (a riser ends ON its peak)
            fo = max(int(0.01 * SR), min(fo, len(seg) - int((rel + 0.04) * SR)))
        if fi: seg[:fi] *= np.linspace(0, 1, fi)[:, None]
        if fo: seg[-fo:] *= np.linspace(1, 0, fo)[:, None]
        pk = np.abs(seg).max() or 1.0
        seg *= 10 ** (PEAK_NORM_DB / 20) / pk
        lev = db + rng.uniform(-1.0, 0.5)        # small level jitter (battle-maps keeps one, narrower here)
        seg *= 10 ** (lev / 20)
        punch = bool(punch_out) and c.get("punch", kind in PUNCH_ROLES)
        i = int(round(start * SR)); n = min(len(seg), len(buf) - i)
        (pbuf if punch else buf)[i:i + n] += seg[:n]
        meas = start + sync_point(seg, stype)
        placed.append({"event": round(event, 3), "shot": c["shot"], "at": c["at"], "role": kind, "file": f,
                       "src": round(src, 3), "start": round(start, 3), "end": round(start + L, 3),
                       "end_allowed": round(end_allowed, 3), "ring_max": ring, "level_db": round(lev, 1), "sync": stype, "punch": punch,
                       "measured": round(meas, 3), "offset_frames": round((meas - event) * FPS, 2),
                       "note": c.get("note", "")})
    pk = np.abs(buf + pbuf).max()
    if pk > 0.89:
        raise SystemExit(f"SFX stem peaks at {20*np.log10(pk):.1f} dBFS: too many stacked cues (> -1 dBFS); thin them out")
    sf.write(out, buf[: int(total * SR)], SR, subtype="FLOAT")
    if punch_out: sf.write(punch_out, pbuf[: int(total * SR)], SR, subtype="FLOAT")
    pb = []
    if beds_out:
        bb = np.zeros_like(buf)
        for b in beds:
            files, db = BEDS[b["role"]]; f = b.get("file") or files[0]
            a = load(f); t0 = S[b["shot"]][0] + b.get("at", 0.0)
            t1 = S[b.get("end_shot", b["shot"])][1] + b.get("tail", 0.0)
            n = int((t1 - t0) * SR); src = int(b.get("src", 0.0) * SR)
            reps = int(np.ceil((src + n) / len(a))) + 1
            seg = np.tile(a, (reps, 1))[src: src + n].copy()
            rms = np.sqrt((seg ** 2).mean()) or 1.0
            seg *= 10 ** (BED_RMS_DB / 20) / rms * 10 ** (db / 20)
            fl = min(int(b.get("fade", 0.4) * SR), n // 3)
            seg[:fl] *= np.linspace(0, 1, fl)[:, None]; seg[-fl:] *= np.linspace(1, 0, fl)[:, None]
            i = int(t0 * SR); bb[i:i + n] += seg[: len(bb) - i]
            pb.append({"role": b["role"], "file": f, "start": round(t0, 3), "end": round(t1, 3), "level_db": db,
                       "note": b.get("note", "")})
        sf.write(beds_out, bb[: int(total * SR)], SR, subtype="FLOAT")
    return placed, pb
