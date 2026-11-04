# Ship-channel SFX: credits and licence

**Every sound in this folder is synthesized in-house** by `make_sfx.py` (numpy + scipy). No recordings, samples, downloads,
AI audio services or third-party libraries are involved, so **no credit line is needed** and there is no licence or Content ID risk.
Nothing is reused or edited from the battle-maps or prehistory-channel SFX kits (owner rejected that on the Oriskany 1-min test).

How they are made (all in `make_sfx.py`, fixed seeds, so a re-run gives the same files):
- layered oscillators with pitch curves (horn, booms, risers), band-limited noise (FFT-shaped white / pink / brown),
- modal synthesis (banks of resonant steel modes) for groans, creaks, slams, scrapes, clanks; stick-slip pulse trains for friction,
- Minnaert-bubble synthesis (pitch-rising damped sines sized by bubble radius) for bubbles, glugs, air release,
- envelopes, time-varying low-pass sweeps, low-pass "underwater" versions with a soft resonance, sub-bass layers,
- convolution reverb from synthetic impulse responses (early taps + noise tail that darkens over time), stereo decorrelation,
- loudness normalised with an in-script ITU-R BS.1770 meter (gated integrated LUFS), peaks at or below -1 dBFS.

Levels (integrated LUFS per file, also in `levels.json`): beds -30, subtle cues (sonar -26, creak -22, distant horn -22),
hits / one-shots -18 (reveal -17), risers -20. The mixer still sets the final level (templates/mix_audio.py, -14 LUFS master).

If a future video mixes these with licensed sounds (Epidemic, freesound CC BY), only those other files need credits.
