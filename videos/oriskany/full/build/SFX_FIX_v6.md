# Oriskany full v6: sound-effects fix after the v5 critique (2026-11-08)

Input: `build/CRITIQUE_SFX_v5.md` (independent critic). The coordinator ordered all M1-M3, S1-S6 and the two lock floors.
Owner direction: quieter SFX, nothing hanging over scenes.
- Audio-only remix. The picture is the v5 video stream, copied; v4 = v5 = v6 picture (stream MD5 `0e4545f45d29a996c5f5fabb74ab1539`).
- Master: **`videos/oriskany/full/oriskany_full_v6.mp4`**. Voice and music are unchanged.
- `check_sound_lock.py` passes **fully**: static and render.

## 1. Changes

Per-cue changes are in `build/sfx_full.py` (v6 block). The renderer is `tools/sound/sfx_mix_lib.py`; its new cue options are `gain`
(≤ 0 only), `lowpass`, `cut_fade` and `gap_carry`, plus `ROLE_EQ`. Every per-cue option only removes sound, except M1.

| # | cue | change |
|---|---|---|
| M1 | explosion + boom @17.65 (hook, 2nd blast) | end at **18.217** (the onset of "Thirty"), 0.237 s past the 17.98 cut, 0.25 s fade ending there (`gap_carry`). One-off exception in the lock: `GAP_CARRY_CUES`, ≤ 0.25 s, must end before the next word. |
| M2 | impact @19.85 (splash), flood @19.90 | lowpass 1200 Hz on both; flood -3 dB (-15.8 → -18.8). The impact keeps its level. |
| M3 | jet role (232.11, 235.89, 325.94) | role **-14 → -17 dB** (KINDS + lock), and `ROLE_EQ` jet = peaking **-6 dB at 2.5 kHz, Q 1** (locked as `JET_EQ`) |
| S1 | groan @26.25 | -3 dB (-16.6 → -19.6) |
| S2 | impact @28.70 | lowpass 1000 Hz |
| S3 | flood @537.69 | lowpass 1200 Hz, -3 dB (-16.2 → -19.2) |
| S4 | whoosh @45.80 | ring 0.8 s (now ends 46.60, 0.25 s fade) |
| S5 | the 40 listed pops and ticks (33 `pop_b`, 7 `pop_a`) | deleted: 148 → **108 cues**. A deleted cue still uses its jitter draw, so no other cue's level moved (checked: the remaining cues keep their v5 `level_db`). |
| S6 | groan @532.80 | 0.4 s fade, ending on the 533.553 cut |
| lock | `check_sound_lock.py` | LRA floor for full-length masters 2.0 → **1.7**; big beats ≥ **+1** LU over speech (was +3). Both are noted "owner 2026-11-08: quieter SFX" there and in CLAUDE.md. |

Filters run after the level and after the peak normalisation, so they can only remove energy.
The mix stems for this run were written to `/dev/shm` (`MIX_WORK`), because the disk had 1.7 GB free.

## 2. Loudness and lock

| measure | v5 | **v6** | target |
|---|---|---|---|
| integrated | -14.0 | **-14.0 LUFS** | -14 ± 0.5 ✓ |
| true peak | -2.0 | **-1.9 dBTP** | ≤ -1.5 ✓ |
| loudnorm | linear, alimiter 0.76 | linear, alimiter 0.76, gain +14.94 dB | ✓ |
| LRA | 1.8 | **1.8 LU** | ≥ 1.7 ✓ (new floor) |
| music under voice | -24.1 | -24.1 dB | ✓ |
| sound design under voice | -21.4 | -21.6 dB | |
| length | 865.600 | 865.600 audio = video, stereo | ✓ |

Big beats over speech (v5 → v6): 4.30 +4.0 → +3.9 · 10.24 +4.5 → +4.5 · **17.65 +1.5 → +3.1** (M1 restores the blast's
body) · 19.85 +3.7 → +3.4 · 28.70 +2.5 → +2.4 · 526.27 +3.2 → +3.2 · 544.28 +2.9 → +2.9 · 805.51 +4.4 → +4.4.
All are ≥ +1 ✓, and none was raised.

`check_sound_lock.py` render: **SOUND LOCK OK**. 108 cues within 3 frames (max 1.2). Every cue is silent by its shot end, with the
one-off hook-blast exception (ends 18.199 audible, before "Thirty" at 18.217). 70 beds sit on shot cuts.

## 3. The hook blast window, 17.5-18.6 s (master, 30 ms RMS)

| t (s) | 17.65 | 17.71 | 17.77 | 17.83 | 17.89 | 17.95 | 17.98 | 18.04 | 18.10 | 18.16 | 18.19 | 18.22 | 18.28 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v5 master dBFS (30 ms RMS) | -6.1 | -7.7 | -7.2 | -10.6 | -16.5 | -30.3 | -34.7 | -32.0 | -33.5 | -29.8 | -35.1 | -33.1 | -17.1 |
| **v6** | -6.1 | -7.7 | -6.7 | -7.8 | -8.8 | -12.4 | -11.7 | -18.0 | -23.3 | -28.4 | -33.7 | -33.3 | -17.1 |

The blast now decays through the voice gap: -12 dBFS at the cut, -23 at 18.10, -34 at 18.19. "Thirty" follows at 18.22 (rising
from 18.25). v5 was near-silent from 17.95.

## 4. Speech-band SNR (1-4 kHz, voice bus over sfx + punch + beds buses, per word; `build/snr_words.py`, real buses)

Every word in the M2/M3/S1-S4 windows that was under +6 dB in v5 or v6:

| place | word (s) | v5 SNR 1-4k dB | v6 | ≥ +6 target |
|---|---|---|---|---|
| M2 hook 'she was gone.' (impact@19.85 + flood@19.90) | she (19.85) | +2.9 | **+7.4** | ✓ |
| M2 hook 'she was gone.' (impact@19.85 + flood@19.90) | was (20.01) | -8.4 | **-3.6** | ✗ under +3 |
| M2 hook 'she was gone.' (impact@19.85 + flood@19.90) | gone. (20.11) | +1.9 | **+7.6** | ✓ |
| S1 groan@26.25 'millions to put' | millions (26.78) | +2.8 | **+5.8** | ≥ +3 |
| S1 groan@26.25 'millions to put' | to (27.22) | +3.3 | **+6.3** | ✓ |
| S2 thump@28.70 'sea floor?' | floor? (28.72) | +0.2 | **+7.0** | ✓ |
| M3 jet@232.11 | flew (232.29) | +4.3 | **+9.3** | ✓ |
| M3 jet@232.11 | more (232.62) | -1.3 | **+5.2** | ≥ +3 |
| M3 jet@232.11 | than (232.95) | +1.4 | **+7.9** | ✓ |
| M3 jet@235.89 | record (235.87) | +2.2 | **+6.8** | ✓ |
| M3 jet@235.89 | for (236.15) | -0.3 | **+3.9** | ≥ +3 |
| M3 jet@235.89 | one (236.45) | -0.7 | **+2.4** | ✗ under +3 |
| M3 jet@325.94 | of (326.00) | +1.0 | **+8.3** | ✓ |
| M3 jet@325.94 | the (326.10) | -12.9 | **-5.5** | ✗ under +3 |
| M3 jet@325.94 | pilots (326.20) | +1.4 | **+7.4** | ✓ |
| S3 flood@537.69 'Then she was gone.' | Then (537.76) | +5.9 | **+14.3** | ✓ |
| S3 flood@537.69 'Then she was gone.' | was (538.10) | -1.3 | **+6.9** | ✓ |

Full data: `build/snr_v5.json` and `build/snr_v6.json`.
- Every word improved; the jets gained +5 to +7 dB.
- **Still under the critic's +6 target:**
  - **"was" @20.01 (-3.6).** It is a 0.10 s, very quiet word. In 1-4 kHz the voice is -47.9 dBFS against **-44.6 from the punch
    bus**: the splash's residue above 1.2 kHz, which is not ducked. The flood (-57.6) and the waves bed (-63.4) no longer matter.
    "she" and "gone." are now +7.4 and +7.6.
  - **"the" @326.10 (-5.5)** and **"one" @236.45 (+2.4)**: the jets at their peak. "the" is a 0.10 s function word, -42.5 voice
    against -43.9 jet in the band.
  - Next step if the owner wants these clean, not done here because they were not on the ordered list: impact@19.85 -3 dB or a
    lowpass at 800 Hz; jets@235.89 / 325.94 a further -3 dB.

## 5. Cut tails, all 244 cuts (`build/cut_tails.py`)

- v5: 0 cuts with an earlier shot's cue audible (> -50 dBFS) past the cut.
- **v6: 1**, the M1 exception at 17.980. explosion + boom audible to 18.199 (+0.22 s), inside the voice gap, faded, before
  "Thirty".
- No other cut has any carry-over. Data: `build/cut_tails_v6.json`.

## 6. Every cue measured again (`build/measure_cues.py` → `build/cue_levels_v6.json`)

Isolated renders, so the punch-bus EQ is not included (critic S7). The SNR table above is the bus-true measure.

| cue (event s) | role | v5 re voice LU | v6 | length s |
|---|---|---|---|---|
| the answer: The bottom of the Gulf (805.51) | boom | +5.0 | +5.0 | 1.40 → 1.40 |
| ON PURPOSE. lands on 'purpose' (10.24) | boom | +4.1 | +4.1 | 1.30 → 1.30 |
| stamp: DEFAULTED. (145.30) | hit | +3.9 | +3.9 | 1.40 → 1.40 |
| WOW 1: blast photo cut + white flash + shake (4.30) | explosion | +3.2 | +3.2 | 1.15 → 1.15 |
| charges fire: blast photo + flash (2nd use of the  (526.27) | explosion | +3.0 | +3.0 | 0.94 → 0.94 |
| 212 FT card lands on 'feet' (2.22) | hit | +2.9 | +2.9 | 1.20 → 1.20 |
| charges fire: boom layer (as the hook) (526.27) | boom | +2.8 | +2.8 | 1.24 → 1.24 |
| second blast: cinematic boom layer under the charg (17.65) | boom | +2.3 | +3.5 | 0.33 → 0.57 |
| bow standing vertical: water closing over the hull (19.85) | impact | +2.1 | +0.8 | 0.70 → 0.70 |
| hull touches the seabed (underwater thump) (544.28) | impact | +1.8 | +1.8 | 1.60 → 1.60 |
| aircraft launches on screen (b3_a4_catapult_1966.m (232.11) | jet | +1.2 | -2.5 | 1.70 → 1.70 |
| aircraft launches on screen (b3_f8_launch_1966.mp4 (235.89) | jet | -0.6 | -5.2 | 1.70 → 1.70 |
| aircraft launches on screen (b3_a4e_launch_1968.mp (325.94) | jet | +0.0 | -6.1 | 0.94 → 0.94 |
| flood rush as the bow slips under (to the foam cut (19.90) | ship | -6.5 | -11.9 | 0.65 → 0.65 |
| drawn carrier going down: hull groan (until touchd (26.25) | ship | -4.0 | -7.0 | 1.56 → 1.56 |
| water closes over the hull: flood (537.69) | ship | -6.2 | -12.1 | 1.34 → 1.34 |
| hull touches the seabed on 'floor' (underwater thu (28.70) | impact | +1.7 | +1.5 | 1.00 → 1.00 |
| end map pull-back (biggest move #2) (45.80) | whoosh | -6.6 | -6.6 | 1.50 → 0.80 |

By role, v6 re-voice median: boom +3.8, explosion +3.0, hit +3.4, impact +1.5, jet **-5.2** (v5 0.0), ship -9.4, whoosh -3.8,
riser -6.5, horn -6.2, pop -15.2 (38 left), tick -17.9 (39 left).

## 7. Disk
`oriskany_full_v4.mp4` and `oriskany_full_v5.mp4` are deleted after v6 passed (see the report for the exact state). The v6 buses
were moved from `/dev/shm` to `audio/mix/`, replacing the stale v5 buses, so the measurements can be re-run.

## 8. v7: the last masked words (coordinator, 2026-11-08)

Master: **`videos/oriskany/full/oriskany_full_v7.mp4`**. It is an audio-only remix on the v6 picture (stream MD5
`0e4545f45d29a996c5f5fabb74ab1539`, unchanged). Every change makes a cue quieter or softer. The edits are in the v6 table of
`build/sfx_full.py`:
- splash (impact) @19.85: lowpass **800 Hz** (was 1200) and **-3 dB**;
- jets @232.11, @235.89 and @325.94: **-3 dB** each, as a per-cue `gain`. The jet role stays at -17 dB with its 2.5 kHz cut, so the
  lock is unchanged.

| measure | v6 | **v7** |
|---|---|---|
| integrated | -14.0 | **-14.0 LUFS** |
| true peak | -1.9 | **-1.7 dBTP** (≤ -1.5 ✓) |
| LRA | 1.8 | **1.8 LU** (≥ 1.7 ✓) |
| loudnorm | linear, alimiter 0.76 | linear, alimiter 0.78, gain +14.70 dB |
| music under voice | -24.1 | -24.1 dB |
| big beats over speech | 19.85 +3.4, others +2.4 … +4.5 | 19.85 **+3.2**, 17.65 +3.2, 28.70 +2.5, all others +3.0 … +4.7 (≥ +1 ✓) |

`check_sound_lock.py`: **SOUND LOCK OK** (static + render). 108 cues within 3 frames, every cue silent by its shot end (the
hook-blast exception only), 70 beds on shot cuts.

Speech-band SNR, 1-4 kHz, voice bus over the effects buses, per word (`build/snr_v7.json`):

| word (s) | v5 | v6 | **v7** |
|---|---|---|---|
| was (20.01) | -8.4 | -3.6 | **+2.4** |
| she (19.85) | +2.9 | +7.4 | **+14.1** |
| gone. (20.11) | +1.9 | +7.6 | **+11.5** |
| more (232.62) | -1.3 | +5.2 | **+8.1** |
| for (236.15) | -0.3 | +3.9 | **+5.6** |
| one (236.45) | -0.7 | +2.4 | **+3.4** |
| the (326.10) | -12.9 | -5.5 | **-2.8** |
| millions (26.78) | +2.8 | +5.8 | **+5.8** |
| floor? (28.72) | +0.2 | +7.0 | **+7.0** |
| was (538.10) | -1.3 | +6.9 | **+6.9** |

Still under +6, measured in 1-4 kHz on the v7 buses:
- **"was" @20.01 (+2.4).** The splash is down 7 dB there (punch -44.6 → -51.6 dBFS). The word itself is very quiet (-47.9) and
  0.1 s long.
- **"the" @326.10 (-2.8).** A 0.1 s function word at -50.3 dBFS, against the jet at -48.2. The jet is down 3 dB, as ordered.
- **"one" @236.45 (+3.4).** It is now limited by the projector bed (-52.9), not by the jet (-57.7).

Further cuts on these would mean removing the cues, or a voice fix ("the" and "was" are quiet in the TTS take).
