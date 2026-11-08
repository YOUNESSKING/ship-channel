# Critique: Oriskany full v5 sound-effects fix (independent, 2026-11-08)

Scope: `oriskany_full_v5.mp4` against `oriskany_full_v4.mp4`, measured from scratch. I did not use the builder's numbers.
- Masters: both decoded from the mp4s.
- v5 stems and buses: `audio/*.wav`, `audio/mix/*_bus.wav`.
- v4 placements: the builder's scratch copy `sfx_placed_v4.json`. The v4 stems no longer exist.
- Voice and music are identical in both versions: master gain is +14.82 dB in v4 and +14.93 dB in v5, and the music-only re-render below matches.

Tools: K-weighted momentary loudness (400 ms) and 100 ms frames on the buses, a 1-4 kHz band (speech consonants) of each bus,
10-30 ms RMS envelopes and spectrograms of both masters.
"SNR 1-4k" = voice bus over the effects buses (sfx + punch + beds) in 1-4 kHz, per word or per 100 ms frame where the voice is
active. Below about +3 dB a word is at risk of being masked.

**Verdict:** the brief was done as asked.
- Every level dropped 3.0 dB (checked: all 148 cues, `level_db` v4 → v5 = -3.0).
- Nothing outlives its shot: 0 of 244 cuts.
- Loudness is unchanged.

Not acceptable yet:
- One beat is now audibly broken: the 17.65 hook blast.
- Three places still have an effect as loud as the narration, masking the words: the hook "she was gone." at 19.85, and the jets at
  232, 236 and 326 s.

Both lock failures can be accepted with a rule note (see section 4). Neither needs anything made louder.

---

## MUST FIX

### M1. The 17.65 s hook blast is chopped. It sounds like an edit error, not an ending.
**Measured** (envelope, 30 ms RMS, gain-normalised; the voice gap runs 17.54-18.22):

| t (s) | 17.65 | 17.71 | 17.77 | 17.83 | 17.89 | 17.95 | 17.98 | 18.04-18.19 | 18.22 "Thirty" |
|---|---|---|---|---|---|---|---|---|---|
| v4 master | -23.2 | -23.8 | -23.3 | -23.5 | -24.6 | -27.4 | -26.3 | -30 → -33 (natural decay) | -33 |
| v5 master | -24.1 | -25.7 | -25.1 | -28.5 | -34.5 | -48.3 | -52.6 | **-50 to -53 (silence)** | -51 |

- The explosion and the boom have full body for about **0.12 s**. The 0.25 s cut-fade starts at 17.73, only 80 ms after the
  event, and the sound is 27 dB down by the cut at 17.98.
- Then come **240 ms of near-silence** before "Thirty" at 18.22. No voice is there to cover the cut-off, so the blast reads as
  clipped. It is the second WOW of the hook.
- The spectrogram shows the same thing: v4 has broadband energy to about 18.3 s, v5 is empty from about 17.9 s.
- The beat measures **+1.2 LU** over speech (v4: +4.4).

**Fix (audio only, minimal):** end explosion@17.65 and boom@17.65 at **18.22**, the onset of "Thirty", which is 0.24 s into s10.
- Use a **0.25 s fade ending at 18.22** (17.97 → 18.22).
- s10 (the "37 minutes" sinking sequence) shows the same event, and the tail sits only in the voice gap, so it does not linger
  under the next line.
- In `sfx_mix_lib` / `check_sound_lock`, add this as a named one-off exception: "carry ≤ 0.25 s into the next shot, inside a
  voice gap, faded". It works like the existing whoosh-on-cut exception.
- Expected beat about +1.4 LU, the v4 shape at -3 dB. No level increase.

*Alternative with no exception:* move the s09/s10 cut from 17.98 to **18.22** (s09 becomes 0.57 s long; the "37" still lands at
about 18.69). The blast then ends on its own cut. This needs a c01 picture re-render.

### M2. 19.85-20.35, hook: "she was gone." is masked by the splash and the flood.
- impact@19.85 is `splash_a`, -9.8 dB, on the **punch bus, so it is not ducked**. ship@19.90 is `flood_a`, -15.8 dB.
- During the line, the effects stem runs **-24.5 to -28 dBFS against the voice's -28 to -32**: the effects are 3-4 dB louder
  than the narrator.
- 1-4 kHz SNR per word: **"she" +2.9, "was" -8.4, "gone" +1.9 dB**.
- This is the payoff line of the hook. Both files are broadband: 1-4 kHz is only 8-13 dB under their low end.

**Fix:**
- Add `lowpass=f=1200` (2-pole) to impact@19.85 and ship@19.90. It also reads more "underwater".
- Lower ship@19.90 by **3 dB** (-15.8 → **-18.8**).
- Keep the impact's level, so its low end and the beat stay. The beat is currently +3.4 to +3.7 LU, and a lowpass on a sound whose
  energy is mostly under 200 Hz costs well under 1 LU.
- Target: every word ≥ +6 dB SNR 1-4k. Re-measure.

### M3. The jets sit at voice level through whole phrases.

| cue | level | re voice median (400 ms) | 100 ms frames under 0 dB SNR 1-4k | worst words (SNR 1-4k) |
|---|---|---|---|---|
| jet@232.11 (`jet_a`) | -13.9 | +1.2 LU | 11 (232.65-233.35) | "more" -1.3, "than" +1.4 |
| jet@235.89 (`jet_b`, strongest 1-4k content) | -14.2 | -0.6 LU | **15** (235.85-236.80) | "A" -1.8, "record" +2.2, "for" -0.3, "one" -0.7 |
| jet@325.94 (`jet_c`) | -14.4 | 0.0 LU | 10 (325.90-327.00) | "One" -8.0, "the" -12.9, "of" +1.0, "pilots" +1.4 |

These are the longest stretches in the video where an effect really is "louder than the voice". They are probably what the owner
still hears.

**Fix:**
- Lower the jet role **3 dB** more: -14 → **-17** in `KINDS` and in the lock.
- Add `equalizer=f=2500:t=q:w=1:g=-6` on jet cues, which cuts the speech band only.
- Expected 1-4k SNR gain is about 9 dB, so every listed word is ≥ +6 dB. The launch roar keeps its low end and its >4 kHz hiss.

---

## SHOULD FIX

| # | where | measured | fix |
|---|---|---|---|
| S1 | ship groan@26.25, "millions to put" | 8 frames under 0 dB SNR 1-4k (26.35-27.30); "millions" +2.8, "to" +3.3. The groan's energy is 200-1 kHz, so it competes with the voice's own band. | groan **-3 dB** (-16.6 → **-19.6**) |
| S2 | impact@28.70, "sea floor?" (punch, not ducked) | "floor?" SNR **+0.2**; 100 ms K-weighted effect over the voice +10 | `lowpass=f=1000` on this cue only (`charges_b`: 99 % of its energy is under 200 Hz, so the beat (now +2.1 to +2.5) loses under 0.5 LU) |
| S3 | ship flood@537.69, "Then she was gone." (the c05 echo of the hook) | "was" **-1.3**, "Then" +5.9 | same treatment as M2: `lowpass=f=1200`, -3 dB (-16.2 → -19.2) |
| S4 | whoosh@45.80, "About thirteen nautical miles" | 7 frames under 0 dB (46.25-46.90); the hook cap raised its ring from uncapped to 1.5 s | ring **0.8 s** (end 46.60, 0.25 s fade) or -3 dB |
| S5 | pops and ticks are now pointless in 40 of 117 cues | Measured the loudest 30 ms of each cue above 300 Hz, the effect against the rest of the mix: **33 of 71 `pop_b` and 7 of 46 `pop_a` sit more than 10 dB under** (worst: 474.44 -20.5, 61.52 -19.9, 127.11 -18.7, 549.92 -18.2). `pop_b` is 300-1000 Hz, the voice's own band, so speech masks it. 22 of the 33 were already more than 10 dB under in v4. | Don't raise them. **Delete these 40 cues:** 18.69 22.79 61.52 90.99 94.25 96.42 106.20 116.16 119.44 127.11 141.70 148.59 182.56 202.94 268.74 284.04 417.56 426.41 429.49 467.50 474.44 477.63 529.38 549.92 556.13 569.48 592.44 610.88 649.44 685.11 706.88 724.60 730.83 743.59 757.44 760.95 763.88 774.18 786.01 815.21. That takes clutter out of the mix and nothing is lost. If a number landing must keep a sound, swap `pop_b` → `pop_a` at the same level (more 1-4 kHz click, so it is heard without being louder). |
| S6 | ship groan@532.80, cut 533.553 | The 0.25 s cut-fade (533.30 -35 → 533.55 -50 dBFS) falls in an exposed 0.56 s voice gap (533.11-533.67). v4 held about -31 to 534.3. It sounds like a short groan, not a broken one. | Optional: lengthen the fade to **0.4 s** (533.15 → 533.553). It still ends on the cut. |
| S7 | builder's per-cue table (`cue_levels_v5.json`) | The isolated renders skip the punch bus's highpass 35 Hz + lowshelf -3 dB at 100 Hz, so the boom and explosion "in words" figures are 1.5-2.2 LU high. On the real buses: 10.24 +1.9 (report +4.1), 805.51 +2.8 (+5.0), 4.30 +1.8 (+3.2). 526.27 is +4.7 on the bus (report +3.0, because the explosion and boom overlap). | Measure on the real buses (`audio/mix/*_bus.wav`), or apply the punch EQ in `measure_cues.iso`. Documentation only. |

---

## OK (verified)

**Levels.**
- All 148 cues are exactly -3.0 dB. The 70 beds are -2 dB, all with 0.25 s fades, starting and ending on cuts.

**Under the voice, overall.**
- 100 ms speech frames where effects exceed the voice: v4 105 (estimated as v5 stems +3 dB, exact apart from trimmed cues, since
  the duck depends only on the voice key) → **v5 56 of 11,065**.
- 1-4k SNR below 0 dB: 158 → **106**.
- Almost all of what is left is M2, M3 and S1-S4. The rest are single 100 ms frames under pop transients, which are harmless.
- The mix is clearly more balanced than v4.

**The deliberate on-word punches stay intelligible.** Their energy is low-frequency, so the 1-4 kHz consonants come through:

| cue | 100 ms K-weighted effect over voice | 1-4k SNR |
|---|---|---|
| 2.22 "feet" | +10 | min +16.1 |
| 10.24 "purpose" | +7.3 | +18.6 |
| 145.30 "default" | +11 | +9.1 |
| 805.51 "The bottom" | +5.7 | +9.3 |
| 526.27 "they fired" | +7.6 | +6.0 / per word +5.3 |
| 4.30 "lies" | +4.7 | per word ≥ +6 |

Keep them as they are.

**Sound past the cut.** I checked every one of the 244 cuts on the v5 stems: sfx + punch RMS between the cut and the first cue
that starts in the new shot.
- **0 cuts above -50 dBFS.** The two hits, 34.90 and 516.583, are reverse risers that peak *on* the cut by design. They stop 60 ms
  later, and their event belongs to the new shot.
- On the masters (v4 - v5 difference after gain matching), v4's carry-overs are real and gone in v5:
  - 17.98: after the cut -29.3 (v4) → -32.2 dBFS (v5), difference signal -32 dB.
  - 533.553: -30.2 → -32.3, difference -34 dB.
  - The control windows give -58 to -64 dB.
- Where energy follows a cut in v5, it is the new shot's own beds or cues.
- 78 cuts are crossed by a continuing bed: the waves bed at 9.98-21.25, the projector bed at 271.91-312.01 and so on. These are
  ambiences under one continuous location, so they are not "effects staying after the scene".

**No other abrupt cut-offs.** A scan of the whole fx stem for drops > 20 dB within 10 ms from above -40 dBFS finds only the
designed riser stops (266.18, 565.89, both unchanged from v4) and one transient inside a whoosh (687.7). The beds show none.
- **526-528:** the charges boom decays naturally to -50 dBFS by 527.35, before the 527.513 cut. The cut-fade touches nothing
  audible. Fine.
- **805-807:** boom@805.51 is not trimmed (shot s34 runs 805.312-808.642). It decays naturally to -55 dBFS by 806.75. Fine.

**Loudness** (ffmpeg ebur128 on both mp4s):

| | v4 | v5 |
|---|---|---|
| Integrated | -14.0 LUFS | -14.0 LUFS |
| True peak | -1.5 dBTP | **-2.0 dBTP** |
| LRA | 1.9 (exact 1.93) | **1.8 (exact 1.79**, p10 -15.21, p95 -13.42) |
| Speech momentary median | -13.93 | -13.88 |

- Music under voice: **-24.1 dB**, from my own re-render of the ducked music against the voice bus. In voice gaps: -22.1.
- Audio and video are both 865.600 s, AAC stereo, 48 kHz.

**Nothing sounds worse than v4 except M1 (and S6, marginally).**

---

## The two lock failures

**LRA 1.8 against the 2-8 rule. Recommendation: accept, and note the owner's decision in the lock.**
- The exact value moved 1.93 → 1.79. The effects only trimmed the top 5 % of short-term loudness (p95 -13.32 → -13.42), and 0.14 LU
  is inaudible.
- On a 14-minute narration, LRA is set by the voice. The v4 critic already noted that LRA does not capture this mix's dynamics.
- The only ways to raise it are louder peaks (against the owner's request) or a quieter floor, for example deeper music dips,
  which costs engagement.
- Minimal change: set the full-length floor in `check_sound_lock.py` to **1.7 LU** with "owner 2026-11-08 (quieter SFX)", or
  record a one-off waiver for this master.
- The real fix stays the one already on file: S3 voice pauses at the next voice render.

**Big beats under +3 LU** (my values: 17.65 +1.2, 28.70 +2.1, 544.28 +2.3; the builder's +1.5 / +2.5 / +2.9).
**Recommendation: accept, and lower the beat floor to +1.0 LU.**
- The +3 rule was written for the v4 levels. The owner's "quieter" request on 2026-11-08 overrides it by definition: every beat
  lost 1.2-3.2 LU.
- 28.70 and 544.28 land *on* words ("floor", "twelve feet"). Raising them would bring back the masking found in S2.
- 17.65 is the only pause beat. After M1 it should be about +1.4, and its problem is shape, not level.
- In `check_sound_lock.py`, change `< 3` to `< 1`, with the owner's date. **Do not raise any cue.**

---

Note: CLAUDE.md now locks the 2026-11-08 role levels (jet -14 and so on). M3's jet -17, the per-cue trims, the M1 exception and
the lock-floor changes all go *below* or outside the locked levels. They still change the lock, so they need the owner's OK and a CLAUDE.md line.

## Fix list in order (all audio-only except the M1 alternative; re-run `mix_full.py`, `measure_cues.py`, `cut_tails.py`, lock)
1. M1: explosion and boom @17.65 end at 18.22, with a 0.25 s fade ending there, plus the one-off lock exception.
2. M2: lowpass 1200 on impact@19.85 and flood@19.90, and flood -3 dB.
3. M3: jet role -17 dB, plus a -6 dB EQ at 2.5 kHz on jets.
4. S1-S4: groan@26.25 -3 dB; lowpass 1000 on impact@28.70; flood@537.69 gets lowpass 1200 and -3 dB; whoosh@45.80 ring 0.8 s.
5. S5: delete the 40 masked pop and tick cues.
6. Lock: LRA floor 1.7 and beat floor +1.0, both as owner notes. Then expect a clean pass.
