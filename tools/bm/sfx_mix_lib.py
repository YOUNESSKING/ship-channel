"""Shared SFX renderer: cue list [[t, kind, scene], ...] -> stereo wav. Used by sfx_mix.py and make_clip.py."""
import os
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
D = os.path.join(HERE, "..", "assets", "media", "sfx")
KINDS = {  # kind: (clips, level dB, min gap between two cues of this kind in s)
    "fire":      (["gun_fire.wav"], -24, 0.35),
    "mortar":    (["mortar_thump.wav"], -24, 0.30),
    "impact":    (["candidates/cand3_hit.wav", "candidates/cand1_hit.wav"], -7, 0.25),  # real distant artillery (CC BY, see SFX_CREDITS)
    "explosion": (["candidates/cand2_hit.wav", "candidates/cand4_hit.wav"], -4, 0.20),  # real distant explosions (CC BY / CC0)
    "missile":   (["missile_launch_hit.wav"], -9, 0.80),
    "mg":        (["mg_burst.wav"], -18, 1.00),
    "whoosh":    (["zoom_whoosh.wav"], -12, 0.50),  # locked zoom sound (owner 2026-09-30): Mixkit "Cinematic tunnel reverb woosh", only on the biggest camera moves
    "hit":       (["hit.wav"], -8, 0.50),
    "static":    (["radio_static.wav"], -21, 3.00),
    "tick":      (["counter_tick.wav"], -20, 0.12),
    "jet":       (["jet_flyby.wav"], -11, 1.2),
    "prop":      (["prop_flyby.wav"], -13, 1.5),
    "heli":      (["heli_flyby.wav"], -14, 2.0),
}


def render(cues, total, out):
    import check_sound_lock  # stops the build if a locked sound, level or the music was changed (owner rule)
    check_sound_lock.check(KINDS)
    clips = {}
    for kind, (files, _, _) in KINDS.items():
        arr = []
        for f in files:
            a, sr = sf.read(f"{D}/{f}", dtype="float32", always_2d=True)
            assert sr == SR, f
            arr.append(a.mean(axis=1))
        clips[kind] = arr
    out_arr = np.zeros(int((total + 5) * SR), dtype="float32")
    rng = np.random.default_rng(7)
    last, used, count = {}, {k: 0 for k in KINDS}, 0
    for t, kind, _scene in cues:
        if kind not in KINDS:
            continue
        _, db, gap = KINDS[kind]
        if t - last.get(kind, -99) < gap:
            continue
        last[kind] = t
        clip = clips[kind][used[kind] % len(clips[kind])]; used[kind] += 1
        gain = 10 ** ((db + rng.uniform(-2.0, 1.0)) / 20)
        i = int(t * SR)
        n = min(len(clip), len(out_arr) - i)
        out_arr[i:i + n] += clip[:n] * gain
        count += 1
    peak = np.abs(out_arr).max() or 1
    if peak > 0.89:
        out_arr *= 0.89 / peak
    sf.write(out, np.stack([out_arr, out_arr], axis=1)[: int(total * SR)], SR, subtype="PCM_16")
    return count
