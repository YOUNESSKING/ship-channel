"""SOUND LOCK for the ship channel (port of battle-maps tools/check_sound_lock.py).
Locks: the battle-maps role LEVELS and min gaps (STYLE_LOCK section 3), music 0.08 + the mix chain (section 5),
and the md5 of every kit sound in use (kit/ship/sfx/out). Changing any of these is an OWNER decision."""
import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEVELS = {"explosion": (-4, 0.20), "impact": (-7, 0.25), "hit": (-8, 0.50), "slam": (-8, 0.50), "whoosh": (-12, 0.50),
          "jet": (-11, 1.2), "ship": (-13, 1.5), "tick": (-20, 0.12)}
CHAIN = ["volume=0.08", "afade=t=in:d=2", "sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400",
         "sidechaincompress=threshold=0.03:ratio=3:attack=10:release=300", "alimiter=limit=0.5:level=false",
         "loudnorm=I=-14:TP=-1.5:LRA=11", "-b:a\", \"192k"]
LOCKFILE = os.path.join(HERE, "kit_md5.json")


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def check(kinds=None):
    sys.path.insert(0, HERE)
    import sfx_mix_lib as L
    kinds = kinds or L.KINDS
    errs = []
    for k, (db, gap) in LEVELS.items():
        if k not in kinds or (kinds[k][1], kinds[k][2]) != (db, gap):
            errs.append(f"role '{k}' level/gap changed: {kinds.get(k, (None, None, None))[1:]} (locked {db} dB, {gap} s)")
    lock = json.load(open(LOCKFILE)) if os.path.exists(LOCKFILE) else {}
    for k, (files, _, _) in kinds.items():
        for f in files:
            p = os.path.join(L.D, f)
            if not os.path.exists(p): errs.append(f"missing kit sound {f}")
            elif f in lock and md5(p) != lock[f]: errs.append(f"kit sound {f} was replaced")
    mix = open(os.path.join(HERE, "mix_clip.py")).read()
    errs += [f"mix chain changed (missing: {s})" for s in CHAIN if s not in mix]
    if not re.search(r"^MUSIC_VOL = 0\.08\b", mix, re.M): errs.append("MUSIC_VOL in mix_clip.py is not 0.08")
    if errs:
        print("\n" + "!" * 70 + "\nSOUND LOCK BROKEN. Build stopped.\n" + "!" * 70)
        for e in errs: print("  - " + e)
        sys.exit(1)
    print("SOUND LOCK OK: battle-maps role levels + gaps, music 0.08, sidechain ducking, limiter 0.5, -14 LUFS / TP -1.5 / LRA 11, AAC 192k, kit md5")


if __name__ == "__main__":
    if "--write-md5" in sys.argv:   # owner-approved kit -> lock its files
        sys.path.insert(0, HERE); import sfx_mix_lib as L
        json.dump({f: md5(os.path.join(L.D, f)) for fs, _, _ in L.KINDS.values() for f in fs}, open(LOCKFILE, "w"), indent=1)
        print("wrote", LOCKFILE)
    check()
