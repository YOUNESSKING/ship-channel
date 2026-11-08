# Oriskany full v5: sound-effects fix (2026-11-08)

**Owner complaint:** "the sound effects are a bit louder and they stay after the scene is over." Fixed for the whole video, the
approved hook (0-48.6 s) included: the owner's request overrides the earlier "don't touch the hook" rule for sound effects only.
**Audio-only remix.** `chapter/joined_silent.mp4` no longer exists, so `build/mix_full.py` now takes the picture from the v4 master
(`PICTURE_SRC`, default `oriskany_full_v4.mp4`). `mix_clip.py` copies that video stream (`-c:v copy`). The v5 video stream is
bit-identical to v4: same stream MD5 `0e4545f45d29a996c5f5fabb74ab1539`, 25,968 frames, 865.600 s.
Master: **`videos/oriskany/full/oriskany_full_v5.mp4`**. Voice and music levels are unchanged.

## 1. What changed

**Quieter** (owner 2026-11-08: SFX -3 dB, ends with its shot). The new levels are in `tools/sound/sfx_mix_lib.py` (KINDS / BEDS) and
are locked in `tools/sound/check_sound_lock.py`:

| role (sounds) | v4 lock | **v5 lock** |
|---|---|---|
| explosion (charges) | -4 | **-7** |
| impact | -7 | **-10** |
| hit (stamp, hook card) | -8 | **-11** |
| boom | -11 | **-14** |
| jet | -11 | **-14** |
| whoosh | -12 | **-15** |
| ship (groan, flood, bubbles) | -13 | **-16** |
| riser | -17 | **-20** |
| horn | -20 | **-23** |
| pop | -20 | **-23** |
| tick (option / map-beat tick, an event role on pop_a) | -20 | **-23** |
| bed: projector | -27 | **-29** |
| bed: drone | -30 | **-32** |
| bed: waves, underwater | -30 | **-32** (see note) |

Note: the brief named the beds "projector, drone". This video also uses waves (22 segments) and underwater (10 segments) beds, so all
four bed roles got the same -2 dB. Revert those two lines in BEDS / BED_LEVELS if the owner wants them at -30.

**No sound outlives its shot** (`sfx_mix_lib.render`, enforced by `check_sound_lock.check_shot_ends`):
- Every cue ends at the next picture cut after its event, whatever the cue's `end_shot` / `tail` say. If the 1.5 s ring cap ends
  it earlier, it ends there. A cue trimmed by the cut gets a **0.25 s fade ending exactly on the cut**. The horn keeps its longer,
  owner-approved 0.6 s fade, which also ends on the cut.
- Cutting a cue never makes the rest louder: the -3 dBFS peak normalisation is computed on the uncut cue.
- Exception: a **whoosh whose event is the cut** (event ≤ 0.1 s before it) may run ≤ 0.4 s into the next shot. **No cue in this
  video uses it** (0 transition cues): every whoosh event sits at or after the start of its own shot.
- The hook's uncapped rings (`"ring": None` in v4) are gone, so the 1.5 s cap applies to the hook too: whoosh 0.35 (2.05 → 1.50 s),
  groan 26.25 (2.34 → 1.50 s), whoosh 45.80 (2.95 → 1.50 s).
- Beds start and stop on shot cuts (no tail), with **0.25 s fades** in and out (v4: projector 0.15 s, others 0.4-1.0 s).
- The renderer records every cue's **audible end** (last sample above -50 dBFS on its own levelled, faded segment). The lock finds
  the cut itself from the shot table and **fails** on any cue audible more than 0.05 s past it (0.4 s for the whoosh exception). It
  also fails on any bed that does not start and stop on a cut, or that has a fade other than 0.25 s.

The 9 cues the cut now trims (v4 → v5 end):

| cue | event | v4 end (audible) | v5 end = cut (audible) |
|---|---|---|---|
| explosion, 2nd hook blast | 17.65 | 18.50 (18.48) | 17.98 (17.972) |
| boom layer, 2nd hook blast | 17.65 | 18.54 (18.48) | 17.98 (17.961) |
| impact, bow vertical | 19.85 | 20.70 (20.66) | 20.55 (20.508) |
| ship flood, bow slips under | 19.90 | 20.65 (20.64) | 20.55 (20.528) |
| ship bubbles, foam | 20.55 | 21.40 (21.36) | 21.25 (21.219) |
| boom, c05 charges | 526.27 | 527.56 (527.47) | 527.513 (527.371) |
| ship groan, hull settling | 532.80 | 534.30 (534.27) | 533.553 (533.538) |
| ship flood, water closes | 537.69 | 539.15 (539.14) | 539.033 (539.015) |
| horn, liner | 814.27 | 815.09 (815.06) | 815.022 (814.98) |

## 2. Loudness and lock

| measure | v4 | **v5** | target |
|---|---|---|---|
| integrated | -14.0 | **-14.0 LUFS** | -14 ± 0.5 ✓ |
| true peak | -1.5 | **-2.0 dBTP** | ≤ -1.5 ✓ |
| loudnorm | linear | linear (alimiter 0.76, gain +14.93 dB) | linear ✓ |
| LRA | 1.9 | **1.8 LU** | 2-8 ✗ |
| music under voice | -24.1 | -24.1 dB | -18..-28 ✓ |
| sound design under voice | -20.7 | -21.4 dB | |
| audio / video length | 865.600 / 865.600 | 865.600 / 865.600, stereo | ✓ |

`check_sound_lock.py`: **static OK** (new levels, cut fade, exception, bed fade). Render: loudness, TP, linear, stereo, length, music,
sync (148 cues, max 1.1 frames), horn rules and the **new shot-end rule all pass** (0 cues audible past their cut, 70 beds on cuts).
**The lock still fails on LRA and on 4 big beats.** Per the brief, these are reported and the beats were not raised back:

| big beat | v4 over speech | **v5** | why |
|---|---|---|---|
| 17.65 2nd hook blast (explosion + boom) | +4.9 LU | **+1.5 LU** | -3 dB, and the shot (s09) is only 0.33 s long, so the blast now stops at the cut. The 400 ms momentary window no longer holds the full blast. |
| 28.70 hook seabed thump | +2.8 (known note) | **+2.5 LU** | -3 dB; partly masked by the voice (it was already under +3 in v4) |
| 544.28 c05 seabed thump | +3.1 | **+2.9 LU** | -3 dB |
| 4.30 / 10.24 / 19.85 / 526.27 / 805.51 | +4.4 / +5.9 / +4.2 / +4.6 / +5.8 | +4.0 / +4.5 / +3.7 / +3.2 / +4.4 | still ≥ +3 ✓ |

LRA 1.8 (v4 1.9): the -3 dB SFX take a little more off the loud end of the short-term distribution. It was already under 2 in v4;
the owner options in SFX_FIX_v4 §3 still apply.

## 3. Every cue measured again (`build/measure_cues.py`, isolated render + the mix's real ducking, LU re the voice-bus median)

v4: `build/cue_levels_v4.json` (measured on the v4 build before any change). v5: `build/cue_levels_v5.json`. The 10 loudest cues of v4:

| # | cue (event s) | role | level dB v4 → v5 | length s v4 → v5 | re voice LU v4 → v5 | Δ | in words LU v4 → v5 | punch |
|---|---|---|---|---|---|---|---|---|
| 1 | the answer: The bottom of the Gulf (805.51) | boom | -11.4 → -14.4 | 1.40 → 1.40 | +8.0 → +5.0 | -3.0 | +8.0 → +5.0 | yes |
| 2 | ON PURPOSE. lands on 'purpose' (10.24) | boom | -11.7 → -14.7 | 1.30 → 1.30 | +7.1 → +4.1 | -3.0 | +7.1 → +4.1 | yes |
| 3 | stamp: DEFAULTED. (145.30) | hit | -8.7 → -11.7 | 1.40 → 1.40 | +6.9 → +3.9 | -3.0 | +6.9 → +3.9 | no |
| 4 | second blast: cinematic boom layer under the charge (ke (17.65) | boom | -10.7 → -13.7 | 0.89 → 0.33 | +6.6 → +2.3 | -4.3 | -7.1 → gap | yes |
| 5 | WOW 1: blast photo cut + white flash + shake (4.30) | explosion | -3.8 → -6.8 | 1.15 → 1.15 | +6.2 → +3.2 | -3.0 | +6.2 → +3.2 | yes |
| 6 | charges fire: blast photo + flash (2nd use of the hook  (526.27) | explosion | -4.6 → -7.6 | 0.94 → 0.94 | +6.0 → +3.0 | -3.0 | +6.0 → +3.0 | yes |
| 7 | 212 FT card lands on 'feet' (2.22) | hit | -7.7 → -10.7 | 1.20 → 1.20 | +5.9 → +2.9 | -3.0 | +5.9 → +2.9 | no |
| 8 | charges fire: boom layer (as the hook) (526.27) | boom | -11.9 → -14.9 | 1.28 → 1.24 | +5.8 → +2.8 | -3.0 | +5.8 → +2.8 | yes |
| 9 | second blast photo + flash (smoke, in the voice gap); d (17.65) | explosion | -4.5 → -7.5 | 0.85 → 0.33 | +5.7 → +1.6 | -4.1 | -5.5 → gap | yes |
| 10 | bow standing vertical: water closing over the hull (19.85) | impact | -6.8 → -9.8 | 0.85 → 0.70 | +5.1 → +2.1 | -3.0 | +5.1 → +2.1 | yes |

All 148 cues: re-voice change median -3.0 LU, range -4.3 to -3.0 (every cue is at least 3 dB quieter). The ones more than 3.5 LU down
were trimmed by the cut: the hook blast pair at 17.65 (-4.1 / -4.3), bubbles at 20.55 (-3.6) and flood at 537.69 (-4.3).
By role (v4 → v5 re-voice median): boom +6.8 → +3.4, explosion +6.0 → +3.0, hit +6.4 → +3.4, impact +4.8 → +1.8, jet +3.0 → 0.0,
whoosh -0.8 → -3.8, ship -1.9 → -6.2, riser -3.5 → -6.5, horn -2.7 → -6.2, pop -13.5 → -16.5, tick -15.2 → -18.2.

## 4. Spot-check: 10 cuts, sound energy in the 0.5 s after the cut (`build/cut_tails.py`)

Cuts chosen: v4 had a placed effect running past these 8 cuts: 17.98, 20.55, 21.25, 48.625, 527.513, 533.553, 539.033 and 815.022.
Six were audible past the cut; at 48.625 and 527.513 the tail had already faded under -50 dBFS. Two bed-boundary cuts were added:
266.172 and 812.572. "Effects" = sfx + punch + beds stems before the mix; "bus" = the same after ducking and filtering. Carry-over =
a cue from an earlier shot that is still audible (> -50 dBFS) after the cut.
**Across all 244 cuts of the video, v4 had 6 cuts with an audible carry-over (max 0.72 s, the 532.80 groan); v5 has 0.**
Full data: `build/cut_tails_v4_v5.json`.

| cut (s) | v4: what ran into the next shot (audible past the cut) | v4 effects 0.5 s after cut RMS / peak dBFS (bus RMS) | v5 carry-over | v5 effects 0.5 s after cut RMS / peak dBFS (bus RMS) | sounds that belong to the new shot |
|---|---|---|---|---|---|
| 17.980 | explosion @17.65 placed to 18.50, audible to 18.48 (+0.50 s); boom @17.65 placed to 18.54, audible to 18.48 (+0.50 s) | -30.4 / -18.3 (-33.1) | none | -57.4 / -41.6 (-59.6) | waves 9.98-21.25 |
| 20.550 | impact @19.85 placed to 20.70, audible to 20.66 (+0.11 s); ship @19.90 placed to 20.65, audible to 20.64 (+0.09 s) | -35.3 / -16.4 (-37.1) | none | -38.4 / -19.5 (-40.2) | ship@20.55, waves 9.98-21.25 |
| 21.250 | ship @20.55 placed to 21.40, audible to 21.36 (+0.11 s) | -46.9 / -23.4 (-47.1) | none | silent / silent (-109.8) | waves 9.98-21.25 |
| 48.625 | whoosh @45.80 placed to 48.74, audible to 47.79 (-0.83 s) | -46.5 / -32.1 (-46.5) | none | -49.4 / -34.1 (-49.4) | waves 45.80-48.62, projector 48.62-51.28 |
| 266.172 | bed boundary (projector out, drone in); the x-ray riser leads INTO this cut and peaks on it (event = the cut, +0.02 s) | -46.1 / -20.5 (-46.5) | none | -48.7 / -23.5 (-49.3) | projector 262.56-266.17, drone 266.17-271.91 |
| 527.513 | boom @526.27 placed to 527.56, audible to 527.47 (-0.04 s) | -49.3 / -31.4 (-53.4) | none | -51.3 / -33.4 (-55.4) | waves 526.27-539.03 |
| 533.553 | ship @532.80 placed to 534.30, audible to 534.27 (+0.72 s) | -30.5 / -17.3 (-33.5) | none | -58.8 / -41.3 (-62.4) | waves 526.27-539.03 |
| 539.033 | ship @537.69 placed to 539.15, audible to 539.14 (+0.11 s) | -50.6 / -28.7 (-52.4) | none | -57.7 / -42.6 (-64.3) | waves 526.27-539.03, underwater 539.03-545.93 |
| 812.572 | bed boundary: underwater 805.31-812.57, projector 812.57-819.28 | -46.2 / -29.8 (-49.5) | none | -49.0 / -31.8 (-52.9) | underwater 805.31-812.57, projector 812.57-819.28 |
| 815.022 | horn @814.27 placed to 815.09, audible to 815.06 (+0.04 s) | -45.3 / -23.5 (-50.7) | none | -48.2 / -26.6 (-53.6) | pop@815.21, projector 812.57-819.28 |


Where energy remains after a v5 cut, it belongs to the new shot: the hook's waves bed runs across shots s05-s11b, the bubbles cue
starts on the 20.55 cut, the beds start on 48.625, 266.172 and 812.572, and the pop lands at 815.21.

## 5. Not fixed / for the owner
- **Big beats under +3 LU** (17.65 at +1.5, 28.70 at +2.5, 544.28 at +2.9) and **LRA 1.8**: see §2. The 17.65 blast is the second
  WOW of the hook. Under the new rule it now lasts only as long as its 0.33 s photo flash. If it reads too thin, the fix is in the
  picture (a longer s09) or a "whoosh-on-cut" style exception for that blast. That is an owner decision; neither was done here.
- `oriskany_full_v4.mp4` is **kept**. v5 does not pass `check_sound_lock` cleanly (the LRA and big-beat items above), so the
  "delete v4 only after v5 passes" condition is not met. v4 is the only copy of the approved v4 sound. Delete it
  (`rm videos/oriskany/full/oriskany_full_v4.mp4`, 1.09 GB) once the owner accepts v5. v5 holds the identical picture.
