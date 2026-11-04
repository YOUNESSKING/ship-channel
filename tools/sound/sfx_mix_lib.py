"""Ship-channel SFX renderer, ported from battle-maps tools/sfx_mix_lib.py (owner-approved, STYLE_LOCK section 3).
Same engine and the SAME locked roles / levels / minimum gaps; only the sound files are the channel's own engineered kit
(kit/ship/sfx/out, synthesized in-house). cue list [[t, kind, note], ...] -> stereo wav.

Role mapping (battle-maps kind -> ship-channel sound):
  explosion -4 dB  : demolition charges going off (charges_seq)          = "big blasts"
  impact    -7 dB  : hull hitting the water / the seabed (sink_whoomp)   = "shell landing"
  hit       -8 dB  : a card / number / stamp landing (number_land, text_slam for the big slam)
  whoosh   -12 dB  : ONLY the 2-3 biggest camera moves (dive_whoosh)      (zoom sound rule)
  jet      -11 dB  : an aircraft launching ON SCREEN (catapult_launch)   (aircraft sound only when on screen)
  ship     -13 dB  : a ship sound for the ship ON SCREEN (hull groan, flood rush, liner horn) = the flyby/engine level
  tick     -20 dB  : small graphic beats (strike-through scrape, sonar ping on a reveal) = the counter-tick level
Locked rules kept: the boom is on the impact frame, sounds only for what is on screen, no extra synthesized "reference"
sounds (no risers, drones, pops, projector loops: STYLE_LOCK 2c-5)."""
import os
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
D = os.path.join(HERE, "..", "..", "kit", "ship", "sfx", "out")
KINDS = {  # kind: (clips, level dB, min gap s)   levels/gaps = battle-maps STYLE_LOCK section 3 (same numbers)
    "explosion": (["charges_seq_3.wav", "charges_seq_1.wav"], -4, 0.20),
    "impact":    (["sink_whoomp_1.wav", "sink_whoomp_2.wav"], -7, 0.25),
    "hit":       (["number_land_1.wav", "number_land_2.wav", "number_land_3.wav"], -8, 0.50),
    "slam":      (["text_slam_1.wav"], -8, 0.50),          # = locked "hit" level, the heavy steel version for the one big slam
    "whoosh":    (["dive_whoosh_2.wav", "dive_whoosh_3.wav"], -12, 0.50),
    "jet":       (["catapult_launch_1.wav", "catapult_launch_2.wav"], -11, 1.2),
    "ship":      (["hull_groan_1.wav", "flood_rush_1.wav", "horn_distant_1.wav", "metal_creak_2.wav"], -13, 1.5),
    "tick":      (["strike_scrape_1.wav", "strike_scrape_2.wav", "sonar_ping_1.wav"], -20, 0.12),
}


def render(cues, total, out, check=True):
    if check:
        import check_sound_lock   # stops the build if a locked level / music level / mix chain was changed
        check_sound_lock.check(KINDS)
    rng = np.random.default_rng(7)
    out_arr = np.zeros(int((total + 9) * SR), dtype="float32")
    last, placed = {}, []
    for c in sorted(cues, key=lambda c: c[0]):
        t, kind = c[0], c[1]
        files, db, gap = KINDS[kind]
        f = c[3] if len(c) > 3 and c[3] else files[sum(1 for p in placed if p[1] == kind) % len(files)]
        if t - last.get(kind, -99) < gap:
            continue
        last[kind] = t
        a, sr = sf.read(os.path.join(D, f), dtype="float32", always_2d=True)
        assert sr == SR, f
        a = a.mean(axis=1)
        if len(c) > 4 and c[4]:   # optional cut length (s) with a 0.4 s fade (long sounds like the horn)
            n = int(c[4] * SR); a = a[:n].copy(); fl = min(len(a) // 2, int(0.4 * SR)); a[-fl:] *= np.linspace(1, 0, fl)
        lev = db + rng.uniform(-2.0, 1.0)   # same small level jitter as battle-maps
        i = int(t * SR); n = min(len(a), len(out_arr) - i)
        out_arr[i:i + n] += a[:n] * 10 ** (lev / 20)
        placed.append((round(t, 3), kind, f, round(lev, 1), c[2] if len(c) > 2 else ""))
    peak = np.abs(out_arr).max() or 1
    if peak > 0.89:
        out_arr *= 0.89 / peak
    sf.write(out, np.stack([out_arr, out_arr], axis=1)[: int(total * SR)], SR, subtype="PCM_16")
    return placed
