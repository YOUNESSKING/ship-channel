# Oriskany full v4: sound-effects fix (2026-11-05)

**Owner complaint:** "the horn, that sound is too long and it's too loud." Plus: check and fix the sound effects in general.
Sound only: no picture render, no final mux (the visual agent owns `chapter/` and `oriskany_full_v4.mp4`). Running
`build/mix_full.py` now produces the v4 sound. `AUDIO_ONLY=/path/test.mp4 python3 build/mix_full.py` runs a sound-only test. It muxes the mix
onto a tiny colour proxy with the v3 frame count (25,968 frames). It does no join and no picture render.

How it was measured: `build/measure_cues.py` (new). Each placed cue is rendered **on its own** with the locked renderer (same file, region,
trims, fades and level). Overlapping cues therefore cannot inflate each other. Then the ducking the SFX stem really got in the mix is applied,
and the result is compared with the voice-bus momentary median inside words within ±5 s. "re voice" = the cue's 400 ms momentary max over its
span. "in words" = the max while a word is spoken.

## 1. Horn (owner decision 2026-11-05, overrides the -14 lock, applies to the hook too)

- `tools/sound/sfx_mix_lib.py`: the horn is now **-20 dB** (was -14). The region is **0.20-2.20 s** of `horn_a` (was 0.20-7.80): the
  onset plus its swell to the blast's peak, the best 2 s. It has its own **0.6 s natural fade-out** (`FADE_ROLE`) and may ring at most 2.0 s
  (`RING_ROLE`).
- `tools/sound/check_sound_lock.py`: the locked horn level is -20, noted "owner 2026-11-05: shorter (≤2 s) and 6 dB quieter". New
  render checks: **at most 2 horns**, each **≤ 2 s**, and **none overlaps a spoken word** (`--words build/words.json`, passed by
  `mix_full.py`).
- `build/sfx_full.py` (v4 block): a horn may only sit in a voice gap of at least 0.6 s, while the liner is on screen. It starts 60 ms after
  the last word and ends 20 ms before the next one. If no such gap exists, the horn is dropped.

| | horn | time (s) | plays | level | re voice (max) | under words? |
|---|---|---|---|---|---|---|
| **before (v3)** | hook, SS United States cut | 39.55-45.80 | **6.25 s** | -14 (-14.2) | **+3.4 LU** | yes: "On November twelfth, the ocean liner SS United States is scheduled to follow her down" (critic B: masks "down") |
| **before (v3)** | ending, liner film | 814.22-819.40 | **5.18 s** | -14 (-13.6) | **+3.2 LU** | yes: from the 0.92 s gap after "long." on through "On November twelfth, at ten in the morning, weather permitting" |
| **after (v4)** | hook | removed | | | | The liner shots (39.55-45.80) have no voice gap ≥ 0.6 s: the gaps are 39.55-39.59, 41.16-41.27 and 45.45-45.80. |
| **after (v4)** | ending, liner film | **814.25-815.09** | **0.84 s** (0.6 s fade) | **-20** (-19.7) | **-2.7 LU** | **no**: it sits in the gap 814.215 ("long.") to 815.138 ("On") |

Note on "825.86": critic B's 825.86 horn (v1 time) is the **same cue** as the v3 ending horn. In v2 it was already moved to 827.55 (v2 time) =
814.26 (v3 time, after the ending cut). Its original under-speech placement no longer exists. The v4 cue keeps only its voice-gap position,
now 0.84 s long. Result: **1 horn** in the whole video, down from 2. A second horn is allowed but none is placed: the only other liner gap is
818.56-819.40, which is 4 s after the first and would read as "again".

## 2. Every other effect (locked levels unchanged)

**New rule: ring ≤ 1.5 s past the picture event** (`RING_MAX` in the lib, checked by the lock). It does not apply to beds (projector, drone,
waves, underwater). A designed longer tail must be written in the cue (`"ring"`). The cues it shortened (0.25 s fade):

| cue | event (s) | v3 length | v4 length | re voice v3 → v4 |
|---|---|---|---|---|
| whoosh, tow around South America | 153.66 | 2.29 | 1.74 | +0.6 → +0.3 |
| jet, A-4 catapult | 232.11 | 2.31 | 1.70 | +3.2 → +4.2 (the ducking estimate; still inside the jet range) |
| jet, F-8 launch | 235.89 | 1.94 | 1.70 | +2.4 → +2.4 |
| jet, A-4E launch (the shot is now shorter) | 325.94 | 2.31 | 0.94 | +1.0 → +3.0 |
| whoosh, c05 back to Pensacola | 484.78 | 3.20 | 1.64 | -3.0 → -3.5 |
| groan, hull settling (now ends 534.30, not 535.74: less under "down stern first") | 532.80 | 3.00 | 1.56 | +1.5 → +1.7 (its peak is in the gap after "minutes.") |
| whoosh, dive to the wreck | 686.84 | 2.29 | 1.74 | -0.6 → -1.8 |
| whoosh, end screen (no voice) | 846.68 | 3.20 | 1.64 | +1.1 → +0.3 |

**Cut (sat on words louder than its role allows):**
- **jet 242.24** (`b3_aerial_launching`): it measured **+6.7 LU over the words "the man who led"**, 4 dB above the jet role's median (+2.8). It was
  a 0.9 s slice, peak-normalised hot. Dropped.

**Spot-check by role (v4, isolated, re voice):** pop median -13.5 (max -8.9) · tick -15.2 (max -12.2) · riser -3.5 (in words ≤ -4.5) · whoosh
-0.8 (max +0.3) · ship -1.9 (in words ≤ -0.9) · jet +3.0 (max +4.2) · impact +4.8 · explosion +6.0 · boom +6.8 · hit (the stamp + the hook
card) +6.4. No pop or tick comes within 8.9 LU of the voice. In the v3 bus-stem measure, pops at 233.3 and 815.2 and a tick at 327.1 seemed to
reach 0 LU; the isolated render shows that was the overlapping jet and horn, not the pops. Big beats (explosion, impact, boom, hit) are the
designed loud moments and are left as they are.

**Approved hook (0-48.6 s): only the horn changed.** These hook cues still ring past 1.5 s as approved: whoosh 0.35 (2.05 s), groan 26.25
(2.34 s), whoosh 45.80 (2.95 s). They are left for the owner (they carry `"ring": None`).

Other: `sfx_full.py` bed lookup now accepts the visual agent's new card-background segments (kind `still`, no `clip` key).
148 cues (v3: 150; minus 1 horn, minus 1 jet), sync max 1.1 frames, 0 over 3 frames.

## 3. Test mix (audio-only, v3 picture length, the visual agent's chapter JSONs as of this run)

| measure | v3 | **v4 test** | target |
|---|---|---|---|
| integrated | -14.0 | **-14.0 LUFS** | -14 ± 0.5 ✓ |
| true peak | -1.7 | **-1.5 dBTP** | ≤ -1.5 ✓ |
| LRA | 2.1 | **1.9 LU** (ebur128; exact 10-95 % short-term spread 2.00) | 2-8 ✗ by 0.1 |
| music under voice | -24.1 | -24.1 dB | -18..-28 ✓ |
| hook thump 28.70 | +2.9 | +2.8 LU | known hook note |

`check_sound_lock.py`: static OK. The new horn, ring and word checks pass. Render: **2 notes**:
1. the known hook thump (+2.8 LU);
2. **LRA 1.9 < 2**. This comes from the owner's own fix. The two 5-6 s horns at +3 LU were the loudest sustained non-speech sounds in the
   programme. With them gone, the short-term 95th percentile drops 0.1 LU (-13.2 → -13.3), while the 10th percentile stays at -15.3. The
   number was not gamed. Owner options:
   - accept 1.9 for this master;
   - lower the band's floor to 1.8 (the critic's note: LRA cannot see this mix's dynamics);
   - add the critic's S3 voice pauses at the next voice render, which lifts LRA naturally.
