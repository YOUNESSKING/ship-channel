"""SOUND LOCK: the owner-approved sounds (Goose Green, 2026-09-30). Runs automatically before every SFX render
(sfx_mix_lib.render, used by assemble_full.py and make_clip.py) and stops the build if anything was changed.

usage (from the project folder): python3 tools/check_sound_lock.py
Locked: artillery fire + shell impacts (field guns AND ships' guns: both use K.gun -> arc -> K.impact), mortars,
bombs from aircraft (K.impact r >= 20 -> "explosion"), aircraft engine sounds, their levels, and the music.
Reference to listen to: reference/style-reference-30s.mp4. Details: STYLE_LOCK.md.
Changing a sound is an OWNER decision: test it (1-min clip), get approval, then update this file in the same commit.
"""
import hashlib, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SFX = os.path.join(ROOT, "assets", "media", "sfx")
FILES = {  # file: md5 (locked recordings / synths)
    "candidates/cand3_hit.wav": "9ad3a3f20f13cd632dfe9c12d9c41c1b",  # artillery / ship shell impact (real, CC BY)
    "candidates/cand1_hit.wav": "b33096334625786af4ec98bc7e506861",  # artillery / ship shell impact (real, CC BY)
    "candidates/cand2_hit.wav": "21b5f5bec92605a4e2e2bdf9eebd9781",  # bomb / big explosion (real, CC BY)
    "candidates/cand4_hit.wav": "2f961855b9977b1764855a774f23f773",  # bomb / big explosion (real, CC0)
    "gun_fire.wav": "22e2e9f43bdf56c6c4f947a41b0949f3",  # gun / ship gun firing (quiet)
    "mortar_thump.wav": "42af7d38e2c59ae0ec748f20ea1d3cee",
    "jet_flyby.wav": "4b73b86411c241c214d2ccc2c0bcb98d",
    "prop_flyby.wav": "cdf6d13c8763630a0c50d86a26ba4510",  # owner 2026-10-06: Mixkit 'Low airplane flying over' (sound B)
    "heli_flyby.wav": "5e676f62c6416bed04ce54b7e59eb0d4",
    "zoom_whoosh.wav": "38bfd2c2af2cf624366bb9a01e306d88",  # zoom sound on the biggest camera moves (owner pick 2026-09-30)
}
KINDS = {  # kind: (clips, dB, min gap)
    "fire": (["gun_fire.wav"], -24, 0.35),
    "mortar": (["mortar_thump.wav"], -24, 0.30),
    "impact": (["candidates/cand3_hit.wav", "candidates/cand1_hit.wav"], -7, 0.25),
    "explosion": (["candidates/cand2_hit.wav", "candidates/cand4_hit.wav"], -4, 0.20),
    "jet": (["jet_flyby.wav"], -11, 1.2),
    "prop": (["prop_flyby.wav"], -13, 1.5),
    "heli": (["heli_flyby.wav"], -14, 2.0),
    "whoosh": (["zoom_whoosh.wav"], -12, 0.50),
}
MUSIC = {
    "music_src_long-note-one.mp3": "def03d2a1a998201a3e191a265961ae6",
    "music_src_wounded.mp3": "b6fb0154fd7d41f854a04c50fbc05fc0",
    "music_src_long-note-two.mp3": "b87ff3dcb1e4b3886c8bf30efaec7c69",
    "music_src_anguish.mp3": "6eb07ca9b6a1ca03656ac3227a784840",
}
FX_JS = [  # automatic sounds in lib/fx.js: the boom is on the impact, bombs are explosions, every aircraft has its engine
    'SFX(o.sfx || (r >= 20 ? "explosion" : "impact"), t)',
    'SFX(o.sfx || "fire", t)',
    '{ jet: "jet", turboprop: "prop", heli: "heli" }[o.kind]',
    # the SHAKE: explosions shake the screen (bombs 6, shells 3), and every bombing run shakes on its first bomb
    'if (o.shake !== false) K.shake(t, o.shake || (r >= 20 ? 6 : 3));',
    'K.shake = (t, amp = 5, dur = 0.35) =>',
    'K.impact(b[0], b[1], t0 + 1.55 + k * 0.25, { r: 20, shake: k ? false : 5 })',
]


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def check(kinds=None):
    errs = []
    for f, h in FILES.items():
        p = os.path.join(SFX, f)
        if not os.path.exists(p):
            errs.append(f"missing locked sound {f} (copy assets/media/sfx/ from goosegreen/)")
        elif md5(p) != h:
            errs.append(f"locked sound {f} was replaced")
    if kinds is None:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import sfx_mix_lib
        kinds = sfx_mix_lib.KINDS
    for k, v in KINDS.items():
        if tuple(kinds.get(k, ())) != v:
            errs.append(f"sound '{k}' changed: {kinds.get(k)} (locked: {v})")
    for f, h in MUSIC.items():
        p = os.path.join(ROOT, "assets", "media", f)
        if not os.path.exists(p) or md5(p) != h:
            errs.append(f"locked music {f} missing or replaced")
    fx = open(os.path.join(ROOT, "lib", "fx.js")).read()
    errs += [f"lib/fx.js changed (locked sound/shake): {s}" for s in FX_JS if s not in fx]
    af = open(os.path.join(ROOT, "tools", "assemble_full.py")).read()
    if not re.search(r"^MUSIC_VOL = 0\.08\b", af, re.M):
        errs.append("MUSIC_VOL in assemble_full.py is not 0.08")
    if "volume=0.08" not in open(os.path.join(ROOT, "tools", "make_clip.py")).read():
        errs.append("music level in make_clip.py is not 0.08")
    if errs:
        print("\n" + "!" * 70 + "\nSOUND LOCK BROKEN: the owner-approved sounds were changed. Build stopped.\n" + "!" * 70)
        for e in errs:
            print("  - " + e)
        print("Fix: restore goosegreen's files (see STYLE_LOCK.md, reference/style-reference-30s.mp4).\n"
              "Only the owner can change a locked sound (test clip -> approval -> update tools/check_sound_lock.py).")
        sys.exit(1)
    print("SOUND LOCK OK: locked artillery / ship-gun / bomb / aircraft sounds, bombing SHAKE, levels and music (see STYLE_LOCK.md)")


if __name__ == "__main__":
    check()
