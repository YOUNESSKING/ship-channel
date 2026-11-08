"""SOUND LOCK v2 for the ship channel (port of battle-maps tools/check_sound_lock.py, extended after the test v3 critique).

Static lock (runs before every SFX render, `check()`):
  * role LEVELS + min gaps = battle-maps STYLE_LOCK section 3 / 2a numbers (ship / horn: ship-channel roles);
  * every role plays a REAL recording from assets/sfx/epidemic/ (md5 locked in epidemic_md5.json; the synthesized
    kit/ship/sfx/out files are banned, STYLE_LOCK 2c-5 / 7);
  * mix_clip.py still has the locked section-5 chain (music 0.08 + fades, both sidechains, bus limiter 0.5,
    loudnorm I=-14 / TP=-1.5 / LRA=11, AAC 192k) AND the v2 fixes (voice compressor 2.5:1 @ -24 dB, voice limiter
    -9 dBFS, de-esser, 5/10 ms chunk-edge fades, 2c-9 gain + alimiter 0.84, the normalization_type == linear gate,
    stereo, audio padded to the video, 0.6 s fade-out, high-pass on music/beds 60-80 Hz).
Render checks (`python3 check_sound_lock.py --render WORK/master.json --cues placed.json --measure measure.json`):
  * loudnorm pass 2 reported "linear" and predicted TP <= -1.5; final -14 +/- 0.5 LUFS, TP <= -1.5 dBTP;
  * stereo, audio duration == video duration (+/- 1 frame);
  * LRA >= 5 LU for short tests, 1.7-8 LU for full-length masters > 5 min (owner 2026-11-05: 2-8; owner 2026-11-08: quieter SFX, 1.7); low end < 120 Hz >= 3 dB under the 300-3000 Hz voice band during clean speech; every big beat's momentary max >= 1 LU above the speech momentary median (owner 2026-11-08: quieter SFX; was 3);
  * music under speech -18..-28 dB re voice, music in gaps within 3 dB of the battle-maps reference estimate;
  * every cue's measured sync point <= 3 frames off its event, and no cue runs past its allowed end;
  * SFX_FIX_v4 (owner 2026-11-05): no cue rings > 1.5 s past its event unless designed ("ring" in the cue); at most 2 horns,
    each <= 2 s, never over a spoken word (--words build/words.json).
  * SFX_FIX_v5 (owner 2026-11-08: SFX -3 dB, ends with its shot): every event role 3 dB and every bed 2 dB under the v4 lock;
    no cue's audible tail (> -50 dBFS, measured on its rendered segment) passes the next picture cut after its event by more
    than 0.05 s (0.4 s for a whoosh whose event is the cut itself); beds start and stop on shot cuts with 0.25 s fades.
Changing any locked number is an OWNER decision."""
import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
# owner 2026-11-08: SFX -3 dB, ends with its shot. Every event role 3 dB under its 2026-11-05 lock (explosion -4, impact -7, hit -8,
# whoosh -12, jet -11, tick -20, boom -11, pop -20, riser -17, ship -13, horn -20); beds 2 dB under (projector -27, others -30).
# owner 2026-11-08: quieter SFX (critic CRITIQUE_SFX_v5 M3): jet -14 -> -17, plus a -6 dB peaking cut at 2.5 kHz on every jet cue.
LEVELS = {"explosion": (-7, 0.20), "impact": (-10, 0.25), "hit": (-11, 0.50), "whoosh": (-15, 0.50), "jet": (-17, 1.2),
          "tick": (-23, 0.12), "boom": (-14, 0.50), "pop": (-23, 0.12), "riser": (-20, 2.0),
          "ship": (-16, 0.5), "horn": (-23, 3.0)}   # horn: owner 2026-11-05: <= 2 s and -20 (was -14); owner 2026-11-08: -23
HORN_MAX_N, HORN_MAX_S = 2, 2.0   # owner 2026-11-05: at most 2 horns per video, each <= ~2 s, in a voice gap, never under speech
RING_MAX = 1.5                    # SFX_FIX_v4: no cue rings on > 1.5 s past its picture event unless the cue designs it
BED_LEVELS = {"projector": -29, "drone": -32, "waves": -32, "underwater": -32}   # owner 2026-11-08: beds -2 dB
# owner 2026-11-08: no sound outlives its shot (SFX_FIX_v5)
AUDIBLE_DB = -50.0        # "audible" = above -50 dBFS on the cue's own rendered segment
CUT_SLACK = 0.05          # a cue's audible tail may pass the next cut after its event by at most this
CUT_TAIL_EXC = 0.4        # ... or this, for a whoosh whose event is the cut itself (event <= CUT_EVENT_WIN s before it)
CUT_EVENT_WIN = 0.1
CUT_FADE = (0.2, 0.3)     # the fade that ends on the cut
BED_FADE = 0.25
JET_EQ = [(2500.0, -6.0, 1.0)]   # owner 2026-11-08: quieter SFX (critic v5 M3): jets cut 6 dB at 2.5 kHz (Q 1)
# owner 2026-11-08: quieter SFX (critic v5 M1): the ONE-OFF hook-blast exception. The 2nd hook blast (explosion + boom @ 17.65) may run
# into the voice gap after its 0.33 s flash: <= GAP_CARRY_MAX s past its cut, faded, ending before the next word. No other cue may.
GAP_CARRY_CUES = {("explosion", 17.65), ("boom", 17.65)}
GAP_CARRY_MAX = 0.25
# owner 2026-11-08: quieter SFX. The floors below were written for the louder 2026-11-05 levels.
LRA_MIN_FULL = 1.7               # full-length masters: LRA 1.7-8 LU (was 2-8)
BEAT_MIN_LU = 1.0                # every big beat's momentary max >= +1 LU over the speech median (was +3)
CHAIN = ["MUSIC_VOL = 0.08", "afade=t=in:d=2", "afade=t=out:st={total - 3:.3f}:d=3",
         "sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400",
         "sidechaincompress=threshold=0.03:ratio=3:attack=10:release=300", "alimiter=limit=0.5:level=false",
         'LN = "loudnorm=I=-14:TP=-1.5:LRA=11"', '"-b:a", "192k"',
         # v2 fixes
         "acompressor=threshold=-24dB:ratio=2.5:attack=5:release=80", 'VOICE_CEIL = "-9dB"', "deesser=",
         "fi, fo = int(0.005 * sr), int(0.010 * sr)", "MASTER_LIMITS = (0.84,", "alimiter=limit={lim}:level=disabled",
         'm2.get("normalization_type") != "linear"', "linear=true", "pan=stereo|c0=c0|c1=c0", '"-ac", "2"',
         "apad=whole_dur={total:.3f}", "afade=t=out:st={total - 0.6:.3f}:d=0.6", "highpass=f={BED_HPF}",
         "highpass=f=35,lowshelf=f=100:g=-3", "highpass=f=80", "amix=inputs=5:normalize=0", "[4:a]aresample=48000", "TARGET_I, TARGET_TP = -14.0, -1.5"]
LOCKFILE = os.path.join(HERE, "epidemic_md5.json")
BANNED_DIR = os.path.join("kit", "ship", "sfx", "out")
FPS = 30


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def fail(errs, what):
    print("\n" + "!" * 70 + f"\nSOUND LOCK BROKEN ({what}). Build stopped.\n" + "!" * 70)
    for e in errs: print("  - " + e)
    sys.exit(1)


def check(kinds=None, beds=None):
    sys.path.insert(0, HERE)
    import sfx_mix_lib as L
    kinds = kinds or L.KINDS; beds = beds or L.BEDS
    errs = []
    for k, (db, gap) in LEVELS.items():
        if k not in kinds or (kinds[k][1], kinds[k][2]) != (db, gap):
            errs.append(f"role '{k}' level/gap changed: {kinds.get(k, (None, None, None))[1:3]} (locked {db} dB, {gap} s)")
    for k in kinds:
        if k not in LEVELS: errs.append(f"role '{k}' is not in the lock (owner decision)")
    for k, db in BED_LEVELS.items():
        if k not in beds or beds[k][1] != db: errs.append(f"bed '{k}' level changed (locked {db} dB)")
    if os.path.abspath(L.D) != os.path.join(ROOT, "assets", "sfx", "epidemic") or BANNED_DIR in L.D:
        errs.append(f"SFX folder is {L.D}: only the real recordings in assets/sfx/epidemic are allowed")
    lock = json.load(open(LOCKFILE)) if os.path.exists(LOCKFILE) else {}
    for files in [v[0] for v in kinds.values()] + [v[0] for v in beds.values()]:
        for f in files:
            p = os.path.join(L.D, f)
            if f not in lock: errs.append(f"{f} is not a catalogued Epidemic recording (assets/sfx/EPIDEMIC_SFX.md)")
            elif not os.path.exists(p): errs.append(f"missing {f}: re-download it (IDs in assets/sfx/EPIDEMIC_SFX.md)")
            elif md5(p) != lock[f]: errs.append(f"{f} was replaced (md5 differs from the catalogue)")
    if L.PEAK_NORM_DB != -3.0: errs.append("one-shot normalisation is not the battle-maps -3 dBFS peak")
    if not CUT_FADE[0] <= getattr(L, "CUT_FADE", 0) <= CUT_FADE[1]: errs.append(f"CUT_FADE must be {CUT_FADE[0]}-{CUT_FADE[1]} s (owner 2026-11-08)")
    if getattr(L, "CUT_TAIL_EXC", 99) > CUT_TAIL_EXC or getattr(L, "CUT_EVENT_WIN", 99) > CUT_EVENT_WIN or tuple(getattr(L, "CUT_EXC_ROLES", ("?",))) != ("whoosh",):
        errs.append(f"the transition exception must be a whoosh on the cut, <= {CUT_TAIL_EXC} s into the next shot (owner 2026-11-08)")
    if abs(getattr(L, "BED_FADE", 0) - BED_FADE) > 1e-9: errs.append(f"bed fades must be {BED_FADE} s (owner 2026-11-08)")
    if [tuple(x) for x in getattr(L, "ROLE_EQ", {}).get("jet", [])] != JET_EQ: errs.append("jet cues must carry the -6 dB @ 2.5 kHz cut (owner 2026-11-08)")
    if getattr(L, "GAP_CARRY_MAX", 99) > GAP_CARRY_MAX: errs.append(f"hook-blast gap carry must be <= {GAP_CARRY_MAX} s")
    if getattr(L, "AUDIBLE_DB", 0) > AUDIBLE_DB: errs.append(f"the renderer's audible threshold must be <= {AUDIBLE_DB} dBFS")
    if getattr(L, "RING_MAX", 99) > RING_MAX: errs.append(f"RING_MAX must be <= {RING_MAX} s (SFX_FIX_v4)")
    if getattr(L, "RING_ROLE", {}).get("horn", 99) > HORN_MAX_S or L.REGION["horn_a__463af07a.wav"][1] > HORN_MAX_S:
        errs.append(f"horn longer than {HORN_MAX_S} s (owner 2026-11-05)")
    mix = open(os.path.join(HERE, "mix_clip.py")).read()
    errs += [f"mix chain changed (missing: {s})" for s in CHAIN if s not in mix]
    m = re.search(r"^BED_HPF = (\d+)", mix, re.M)
    if not m or not 60 <= int(m.group(1)) <= 80: errs.append("music/bed high-pass must be 60-80 Hz")
    m = re.search(r"^MUSIC_TRIM_DB = (-?[\d.]+)", mix, re.M)
    if not m or abs(float(m.group(1))) > 6: errs.append("MUSIC_TRIM_DB missing or > 6 dB (re-calibrate vs the reference)")
    m = re.search(r"^VOICE_LUFS = (-?[\d.]+)", mix, re.M)
    if not m or not -30 <= float(m.group(1)) <= -23: errs.append("VOICE_LUFS missing or outside -30..-23")
    if errs: fail(errs, "static")
    print("SOUND LOCK OK (static): role levels + gaps, real Epidemic recordings (md5), music 0.08 + ducking, voice "
          "compressor/limiter/de-ess/edge fades, 2c-9 gain + alimiter 0.84, loudnorm linear gate, stereo, pad, fade-out, HPF")


def check_shot_ends(placed, shots, beds=None, words=None):
    """SFX_FIX_v5 (owner 2026-11-08): every cue has faded below -50 dBFS by the next picture cut after its event (+0.05 s), a
    whoosh whose event is the cut by +0.4 s; every bed starts and stops on a shot cut with 0.25 s fades. The cut is found
    here from the shot table (not taken from the renderer)."""
    import bisect
    errs = []
    sh = sorted(shots, key=lambda s: s[1]); st = [s[1] for s in sh]; total = sh[-1][2]
    for p in placed:
        if "audible_end" not in p: errs.append(f"cue {p['role']} @ {p['event']:.2f}: no measured audible end (old renderer)"); continue
        s = sh[max(0, bisect.bisect_right(st, p["event"] + 1e-4) - 1)]; cut = s[2]
        trans = p["role"] == "whoosh" and cut - p["event"] <= CUT_EVENT_WIN and cut < total - 1e-3
        lim = CUT_TAIL_EXC if trans else CUT_SLACK
        if p.get("gap_carry"):   # the one-off hook-blast exception (owner 2026-11-08: quieter SFX, critic v5 M1)
            if not any(p["role"] == r and abs(p["event"] - t) < 0.02 for r, t in GAP_CARRY_CUES):
                errs.append(f"cue {p['role']} @ {p['event']:.2f} uses gap_carry: only the hook blast {sorted(GAP_CARRY_CUES)} may")
            elif p["gap_carry"] > GAP_CARRY_MAX + 1e-6:
                errs.append(f"cue {p['role']} @ {p['event']:.2f}: gap_carry {p['gap_carry']} > {GAP_CARRY_MAX} s")
            else:
                lim = p["gap_carry"] + CUT_SLACK
                nw = min([w["start"] for w in words or [] if w["start"] > p["event"]] or [1e9])
                if words and p["audible_end"] > nw + 1e-3:
                    errs.append(f"cue {p['role']} @ {p['event']:.2f}: audible to {p['audible_end']:.3f}, into the word at {nw:.3f} (voice gap only)")
        if p["audible_end"] > cut + lim + 1e-4:
            errs.append(f"cue {p['role']} @ {p['event']:.2f} ({p['note'][:40]}): audible until {p['audible_end']:.3f}, "
                        f"{p['audible_end'] - cut:+.3f} s past its shot end {cut:.3f} (max {lim}; owner 2026-11-08)")
    ends = {round(s[2], 3) for s in sh}; begs = {round(s[1], 3) for s in sh}
    for b in beds or []:
        if round(b["end"], 3) not in ends: errs.append(f"bed {b['role']} {b['start']:.2f}-{b['end']:.2f} does not stop on a shot cut")
        if round(b["start"], 3) not in begs: errs.append(f"bed {b['role']} {b['start']:.2f}-{b['end']:.2f} does not start on a shot cut")
        if "fade" not in b or (abs(b["fade"] - BED_FADE) > 1e-3 and abs(b["fade"] - (b["end"] - b["start"]) / 3) > 1e-3):
            errs.append(f"bed {b['role']} {b['start']:.2f}-{b['end']:.2f}: fade {b.get('fade')} s (owner 2026-11-08: {BED_FADE} s)")
    return errs


def check_cues(placed, words=None):
    errs = []
    horns = [p for p in placed if p["role"] == "horn"]
    if len(horns) > HORN_MAX_N: errs.append(f"{len(horns)} horns (owner 2026-11-05: at most {HORN_MAX_N})")
    for p in horns:
        if p["end"] - p["start"] > HORN_MAX_S + 0.05: errs.append(f"horn @ {p['event']:.2f} plays {p['end'] - p['start']:.2f} s (max {HORN_MAX_S})")
        for w in words or []:
            if w["start"] < p["end"] and w["end"] > p["start"]:
                errs.append(f"horn @ {p['event']:.2f} ({p['start']:.2f}-{p['end']:.2f}) plays under the word '{w['w']}' (owner: never under speech)"); break
    for p in placed:
        rm = p.get("ring_max", RING_MAX)
        if rm is not None and p["end"] - p["event"] > rm + 1e-3:
            errs.append(f"cue {p['role']} @ {p['event']:.2f} rings {p['end'] - p['event']:.2f} s past its event (max {rm})")
        if abs(p["offset_frames"]) > 3:
            errs.append(f"cue {p['role']} @ {p['event']:.2f} ({p['note']}): sync point {p['offset_frames']:+.1f} frames off its event")
        if p["end"] > p["end_allowed"] + 1e-3:
            errs.append(f"cue {p['role']} @ {p['event']:.2f} runs past its allowed end {p['end_allowed']}")
    return errs


def check_render(master, placed, meas, words=None, shots=None, beds=None):
    errs = []
    t = master["tries"][-1]
    if master.get("normalization_type") != "linear" or t["loudnorm_pass2"].get("normalization_type") != "linear":
        errs.append(f"loudnorm was not linear ({master.get('normalization_type')})")
    if t["predicted_tp"] > -1.5: errs.append(f"predicted TP {t['predicted_tp']} > -1.5 (loudnorm would go dynamic)")
    f = master["final"]
    if abs(f["I"] + 14) > 0.5: errs.append(f"integrated {f['I']} LUFS (target -14 +/- 0.5)")
    if f["TP"] > -1.5: errs.append(f"true peak {f['TP']} dBTP > -1.5")
    au = [s for s in master["streams"] if s["codec_type"] == "audio"][0]
    vi = [s for s in master["streams"] if s["codec_type"] == "video"][0]
    if au["channels"] != 2: errs.append(f"master has {au['channels']} channel(s), not stereo")
    if abs(float(au["duration"]) - float(vi["duration"])) > 1.0 / FPS + 0.025:   # + one AAC frame
        errs.append(f"audio {au['duration']} s vs video {vi['duration']} s")
    # LRA rule, OWNER DECISION 2026-11-05 (Oriskany full v3): a full-length master (> 5 min) must sit in the battle-maps reference
    # band, 2-8 LU (a 15-min narration on the locked chain measures 2-3 LU; the references measure 2.2-2.5). Short tests keep >= 5 LU.
    if float(vi["duration"]) > 300:
        if not LRA_MIN_FULL <= meas["lra"] <= 8: errs.append(f"LRA {meas['lra']} LU outside {LRA_MIN_FULL}-8 (full-length master, owner 2026-11-08: quieter SFX)")
    elif meas["lra"] < 5: errs.append(f"LRA {meas['lra']} LU < 5 (short test)")
    for b in meas["beats"]:
        if b["above_speech_lu"] < BEAT_MIN_LU: errs.append(f"big beat @ {b['t']:.2f} ({b['what']}) only {b['above_speech_lu']:+.1f} LU above speech")
    b = meas.get("bands_in_speech_re_total_db")
    if b and b["<120"] > b["300-3k"] - 3:
        errs.append(f"low end < 120 Hz ({b['<120']} dB) within 3 dB of the voice band ({b['300-3k']} dB) while the narrator speaks")
    mu = meas["music_under_voice_db"]
    if not -28 <= mu <= -18: errs.append(f"music under speech {mu} dB re voice (target -18..-28)")
    if meas.get("ref_gap_delta_db") is not None and abs(meas["ref_gap_delta_db"]) > 3:
        errs.append(f"music in gaps {meas['ref_gap_delta_db']:+.1f} dB vs the battle-maps reference (> 3 dB)")
    return errs + check_cues(placed, words) + (check_shot_ends(placed, shots, beds, words) if shots else ["no shot table: the shot-end rule was not checked"])


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    if "--write-md5" in sys.argv:   # catalogue the downloaded recordings (owner-approved set) -> lock their files
        import sfx_mix_lib as L
        files = sorted(f for f in os.listdir(L.D) if f.endswith(".wav"))
        json.dump({f: md5(os.path.join(L.D, f)) for f in files}, open(LOCKFILE, "w"), indent=1)
        print("wrote", LOCKFILE, len(files), "files")
    check()
    if "--render" in sys.argv:
        a = sys.argv
        master = json.load(open(a[a.index("--render") + 1]))
        PL = json.load(open(a[a.index("--cues") + 1])); placed = PL["cues"]
        meas = json.load(open(a[a.index("--measure") + 1]))
        words = None
        if "--words" in a:
            words = json.load(open(a[a.index("--words") + 1])); words = words["words"] if isinstance(words, dict) else words
        errs = check_render(master, placed, meas, words, PL.get("shots"), PL.get("beds"))
        if errs: fail(errs, "render")
        f = master["final"]
        print(f"SOUND LOCK OK (render): {f['I']} LUFS, TP {f['TP']} dBTP, LRA {meas['lra']} LU, loudnorm linear, stereo, "
              f"audio = video length, music under speech {meas['music_under_voice_db']} dB, "
              f"{len(meas['beats'])} big beats >= +{BEAT_MIN_LU} LU over speech, {len(placed)} cues within 3 frames, every cue silent by its shot end, "
              f"{len(PL.get('beds', []))} beds on shot cuts")
