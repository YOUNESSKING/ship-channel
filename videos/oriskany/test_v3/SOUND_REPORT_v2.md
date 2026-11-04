# Oriskany test v3: NEW SOUND (sound report v2)

**Master:** `oriskany_test_v3_newsound.mp4`. It is git-ignored; rebuild it with `python3 build/mix_v2.py`.
- Picture: the same picture as `oriskany_test_v3.mp4`. Its video stream is copied bit for bit.
- Voice and timing: the same `audio/voice.wav`, `build/words.json` and `build/chunks.json`.
- Music: the same Zabriskie track ("Stories About the World That Once Was", CC BY 4.0).
- What is new: the mix chain (`tools/sound/` v2) and real Epidemic Sound recordings. They are listed in
  `assets/sfx/EPIDEMIC_SFX.md`.

**How the numbers were measured** (none were assumed):
- `tools/sound/measure_mix.py` measured the encoded master and every stem at master scale. The results are in
  `audio/v2/measure.json` and `audio/v2/master.json`.
- The "before" numbers are the critic's (`CRITIQUE_SOUND_ACCURACY.md`). Where marked, they were re-measured with
  the same tool.
- Nobody has listened to this mix yet. **The owner's ear decides.**

## 1. Before / after

| metric | v3 (before) | v3 new sound (after) | target |
|---|---|---|---|
| Integrated | -14.3 LUFS | **-14.1 LUFS** | -14 ± 0.5 |
| True peak | -1.2 dBTP | **-1.6 dBTP** | ≤ -1.5 |
| loudnorm mode | **dynamic** (silent AGC fallback, gain rode +5.6 to +12.4 dB) | **linear** (pass 2 JSON `normalization_type: linear`, predicted TP -2.42) | linear, else FAIL |
| LRA | 2.0 LU | **5.1 LU** | ≥ 5 |
| Channels | mono | **stereo** | stereo |
| Audio vs video length | 53.513 vs 53.600 s (87 ms chop) | **53.600 = 53.600 s**, 0.6 s fade-out | equal |
| Speech momentary median | -14.1 LUFS (re-measured) | -15.8 LUFS | n/a |
| Explosion 7.40 s, momentary max re speech | +1.5 LU (re-measured; the critic found no beat above speech) | **+4.6 LU** | ≥ +3 |
| Big beats, re speech (all) | +0.3 to +2.5 LU | **+4.6 to +7.1 LU** (table below) | ≥ +3 |
| Music under voice, during words (stems) | -27.5 dB (critic) | **-21.9 dB** | -18 to -28; battle-maps level |
| Music in gaps re the voice, from stems | about -23.6 dB (critic: recovers only 3.9 dB) | **-19.2 dB** | about -18 to -20 |
| Blind gap estimate re speech (same tool on both) | -10.4 dB (inflated by the dynamic loudnorm lifting the pauses) | **-17.2 dB** | battle-maps mean -17.3 (Δ **+0.1 dB**) |
| Sound design (music + SFX + beds) under the voice in speech | -10.1 dB (critic) | **-13.9 dB** | voice clearly on top |
| Sound-design floor in gaps (10th percentile, M) | -48 to -52 dBFS dead air at 30-40 s | **-39.3 LUFS**; the 30-40 s block has a drone bed | no dead air |
| Low end < 120 Hz, during clean speech, re total | -5.0 dB, with the voice band at -4.8 dB (rivals it) | **-8.0 dB**, with the voice band at **-3.1 dB** | ≥ 3 dB under the voice band |
| Low end < 120 Hz, whole file | -4.4 dB | -4.2 dB, which is the blasts and booms themselves | n/a |
| SFX cues more than 3 frames off their visual event | 4 cues peaked 58-73 frames late | **0 of 22** (worst +1.1 frames) | ≤ 3 frames |
| Synthesized SFX | 19 of 19 files | **0**: every file is a real Epidemic recording (md5-locked) | 0 |

### The battle-maps reference

The reference mixes have no stems. So the same blind estimator was run on the reference mixes and on our master:
- it takes the 50 ms RMS of the gap frames at the 30th percentile;
- it compares that with the speech median;
- the words come from faster-whisper.

| reference mix | blind gap re speech | I | LRA | TP |
|---|---|---|---|---|
| style-reference-rokossovsky-v8.mp4 | -17.4 dB | -14.3 | 2.5 | -2.4 |
| hook-reference-rokossovsky-v2.mp4 | -15.0 dB | -15.0 | 2.2 | -4.2 |
| hook-reference-meade-v3.mp4 | -19.5 dB | -14.9 | 2.3 | -4.2 |
| **mean** | **-17.3 dB** | | | |
| **our new master** | **-17.2 dB** | -14.1 | 5.1 | -1.6 |

The music now sits where battle-maps has it: within 0.1 dB on this estimator.

The battle-maps references themselves have an LRA of 2.2-2.5 LU. That means their masters were flattened the same
way (the dynamic loudnorm fallback). Our master is more dynamic than the locked reference, as this task asked.

### Big beats (master momentary max in [event - 0.1, event + 0.6] s, re the speech median -15.8 LUFS)

| t (s) | beat | M max (LUFS) | re speech |
|---|---|---|---|
| 0.40 | MAY 17, 2006 stamp (boom) | -8.7 | +7.1 |
| 6.85 | first charge, plume photo (explosion) | -9.5 | +6.3 |
| 7.40 | main blast + flash (explosion) | -11.2 | **+4.6** |
| 13.80 | bow-high photo, hull into the water (impact) | -10.5 | +5.3 |
| 19.27 | hull touches the seabed (underwater thump + boom layer) | -10.0 | +5.8 |
| 24.33 | ON PURPOSE flash cut (boom) | -10.7 | +5.1 |
| 40.83 | gold box on SINK HER (boom) | -9.3 | +6.5 |
| 51.40 | THE SAME REASON stamp (boom) | -9.9 | +5.9 |

## 2. The chain (tools/sound, used by every video)

1. **Voice stem.** The steps, in order:
   - 5 ms fade-in and 10 ms fade-out at every Kokoro chunk edge, from `chunks.json`. This removes the critic's
     -42 to -50 dBFS edge ticks.
   - High-pass at 80 Hz, and -2 dB at 160 Hz (the voice was chesty).
   - De-esser (`deesser=i=0.25`).
   - Gain to **-29 LUFS** (stem gain -5.9 dB).
   - Compressor `acompressor=threshold=-24dB:ratio=2.5:attack=5:release=80`.
   - Limiter `alimiter=limit=-9dB` (measured voice stem peak -13.6 dBFS, so the limiter is a safety ceiling only).
   - Padded to the video length and centred in stereo.
2. **Mix.** The locked section-5 settings are kept:
   - music at `MUSIC_VOL = 0.08` with a 2 s fade-in and a 3 s fade-out, ducked 0.03 / 6 / 20 / 400;
   - SFX at full level, ducked 0.03 / 3 / 10 / 300;
   - the bus limiter at 0.5 (the bus peak is -8.0 dBFS, so it never acts).

   New in v2:
   - **`MUSIC_TRIM_DB = -6`**. It moves the music by the same amount as the voice, so the music:voice ratio
     stays at the battle-maps balance (see the reference table above).
   - Beds (projector, drone, waves, underwater) are ducked like the SFX.
   - Music and beds are high-passed at **70 Hz**. SFX are high-passed at 35 Hz, with a **-3 dB shelf below
     100 Hz**.
   - **Big beats (explosion, impact, boom) go on an unducked "punch" stem**, so they read momentarily louder
     than speech.
   - The output is stereo `amix`, with a 0.6 s fade-out.
3. **Master (2c-9).**
   - Measure I (mix -26.8 LUFS).
   - Apply one linear gain (+13.02 dB) and a 4x-oversampled `alimiter`. The ceiling starts at 0.84 and steps
     down only while the AAC encode overshoots the true peak:
     - 0.84: skipped, because the predicted TP was -1.27, so loudnorm would have gone dynamic;
     - 0.82 to 0.76: the encoded TP was -0.9 to -1.2;
     - **0.74**: passed.
   - Then run the two-pass `loudnorm=I=-14:TP=-1.5:LRA=11` with the `measured_*` values and `linear=true`.
   - **The build fails if:**
     - loudnorm's JSON says anything but `linear`;
     - the predicted TP is above -1.5;
     - the encoded master is outside -14 ± 0.5 LUFS, or its TP is above -1.5 dBTP.
4. **SFX placement** (`sfx_mix_lib.py` v2):
   - Each cue is defined as `shot + offset`, which is the visual event frame.
   - The sound's sync point is measured from the audio: the loudest 50 ms for blasts, booms, pops, jets and
     risers; the onset for whooshes, rushes, groans, the horn and beds. That point is put on the event frame.
   - Each cue is trimmed to its shot, plus a 0.12 s tail, unless the cue declares a designed tail or `end_shot`.
   - The sync is measured again on the trimmed, faded segment.
5. **`check_sound_lock.py`** stops the build on any of the following:
   - **Static checks:**
     - the role levels or gaps have changed;
     - a file is not a catalogued Epidemic recording, or its md5 differs;
     - the chain is missing any of the pieces above;
     - VOICE_LUFS is outside -30 to -23, or MUSIC_TRIM_DB is beyond ±6;
     - the music/bed high-pass is outside 60-80 Hz.
   - **Render checks:**
     - loudnorm did not run linear;
     - the loudness or true peak is off target;
     - the master is not stereo;
     - the audio and video lengths differ;
     - the LRA is below 5;
     - a big beat is less than +3 LU above speech;
     - the low end comes within 3 dB of the voice band during speech;
     - the music under speech is outside -18 to -28 dB;
     - the music in gaps is more than 3 dB away from the battle-maps reference;
     - **any cue is more than 3 frames off its event**, or runs past its allowed end.

## 3. Every cue (30 fps; offset = measured sync point minus visual event)

| event (s) | shot + offset | role | Epidemic file | level dB | plays (allowed end) | sync | measured | offset (frames) | what is on screen |
|---|---|---|---|---|---|---|---|---|---|
| 0.40 | a01 +0.40 | boom | boom_a__2f0a40ab | -11.1 | 0.28-1.49 (3.05) | peak | 0.400 | +0.0 | MAY 17, 2006 card first visible |
| 2.93 | a02 +0.00 | whoosh | whoosh_a__689b1489 | -11.7 | 2.93-4.72 (4.72) | onset | 2.927 | +0.0 | map dive cut (biggest move #1) |
| 6.85 | a03b +0.00 | explosion | charges_c__f6f10ea4 (crack 1) | -3.8 | 6.85-7.33 (7.52) | peak | 6.875 | +0.8 | first charge: water plume photo |
| 7.40 | a04 +0.00 | explosion | charges_c__f6f10ea4 (crack 2) | -4.7 | 7.40-8.19 (8.35) | peak | 7.425 | +0.8 | main blast + white flash, 0.9 s trim |
| 13.20 | a06 +0.99 | pop | pop_b__844f57e0 | -20.5 | 13.18-13.43 | peak | 13.201 | +0.0 | 37 reached on screen |
| 13.80 | a07 +0.00 | impact | splash_a__1d6949d6 | -6.7 | 13.80-14.40 (14.40) | peak | 13.835 | +1.1 | bow-high photo, hull into the water |
| 14.10 | a08 +0.00 | ship | flood_a__db95b348 | -14.0 | 14.10-14.85 (14.85) | onset | 14.100 | +0.0 | flood rush as she slips under |
| 14.70 | a08b +0.00 | ship | bubbles_a__e58b390c | -12.8 | 14.70-15.42 (15.42) | onset | 14.700 | +0.0 | boil photo: air bursting out |
| 15.70 | v10 +0.40 | pop | pop_b__844f57e0 | -19.8 | 15.68-15.93 | peak | 15.700 | +0.0 | ABOUT 900 FT first visible |
| 17.65 | a09 +0.15 | ship | groan_a__7c63fd7c | -13.3 | 17.59-19.34 (20.55) | onset | 17.650 | +0.0 | hull groan while the drawn carrier sinks |
| 19.27 | a09 +1.77 | impact | charges_b__0ecb5c38 | -7.5 | 19.12-20.32 (20.67) | peak | 19.270 | +0.0 | hull touches the seabed |
| 19.27 | a09 +1.77 | boom | boom_a__2f0a40ab | -11.6 | 19.16-20.36 (20.67) | peak | 19.270 | +0.0 | (layer under the seabed thump) |
| 21.20 | v12 +0.65 | jet | jet_a__9fc48bf0 | -11.6 | 20.55-22.34 (22.34) | peak | 21.205 | +0.1 | A-4 shoots past the camera |
| 24.33 | a12 +0.00 | boom | boom_a__2f0a40ab | -11.3 | 24.33-25.62 | peak | 24.367 | +1.1 | ON PURPOSE flash cut |
| 26.30 | a13 +0.29 | pop | pop_b__844f57e0 | -20.2 | 26.27-26.52 | peak | 26.296 | +0.0 | 3 YEARS first visible |
| 27.75 | a14 +0.20 | pop | pop_b__844f57e0 | -20.2 | 27.73-27.98 | peak | 27.750 | +0.0 | $20 MILLION first visible |
| 40.37 | a17 +4.49 | pop | pop_b__844f57e0 | -19.5 | 40.34-40.59 | peak | 40.370 | +0.0 | KEEP HER struck through |
| 40.83 | a17 +4.95 | boom | boom_a__2f0a40ab | -10.8 | 40.72-41.26 (41.26) | peak | 40.830 | +0.0 | gold box lands on SINK HER |
| 42.62 | a19 +0.00 | riser | riser_a__fd98cb0b | -17.1 | 40.43-42.69 (lead-in) | peak | 42.623 | +0.0 | reverse riser peaks on the x-ray reveal |
| 44.52 | v23a +0.00 | horn | horn_a__463af07a | -9.5 | 44.52-48.42 (48.42) | onset | 44.517 | +0.0 | SS United States on screen (signature horn) |
| 49.30 | a20 +0.00 | whoosh | whoosh_a__689b1489 | -12.7 | 49.30-51.35 | onset | 49.300 | +0.0 | end-map pull-back (biggest move #2) |
| 51.40 | a20 +2.10 | boom | boom_a__2f0a40ab | -11.8 | 51.28-52.69 | peak | 51.400 | +0.0 | THE SAME REASON stamp visible |

Notes on the cue table:
- **Allowed end** = the end of `end_shot` plus the tail. When it is not shown, the cue ended before it.
- **Density:** 22 cues in 53.6 s (24.6/min). Counting stacks as one, there are 21 (23.5/min). The 6 pops are at
  -20 dB; a pop is a small tick, not a sub boom.

### Beds

| bed | file | level | span |
|---|---|---|---|
| waves | waves_a__3d49f79f | -30 | 0.00-4.60 (opening photo + map dive), 49.30-53.60 (end map) |
| underwater | underwater_a__127d88ce | -30 | 17.50-20.55 (hero sinking) |
| low tension drone | drone_a__244a55e9 | -30 | 29.40-41.14 (the question block, dead air before) |
| projector loop | projector_b__5648e70b | -27 | under every archive-film shot: 8.10-12.21, 15.30-17.50, 20.55-24.33, 26.01-27.55, 31.36-35.88, 41.14-42.62, 44.52-49.30 |

## 4. The critic's sync fixes, applied

| critic finding | fix |
|---|---|
| Explosion peaked +73 frames late, over the 1966 film | Real 2-charge sequence: crack 1 on the plume photo (6.85), crack 2 on the blast cut (7.40). Trimmed to end at 8.19 (allowed 8.35). Offset +0.8 frames each. |
| Flood rush peaked +71 frames late and masked "feet" | Real rush from 14.10, ending at the a08b cut (14.85, with a 0.15 s crossfade). The boil photo gets real bubbles. Nothing plays over "feet" (16.36): the 900 FT pop ends at 15.93. |
| Catapult rush peaked +58 frames late, with no aircraft on screen | Real military-jet pass. Its loudest moment is on 21.20, while the A-4 passes (21.00-21.40). It ends at the v12 cut (22.24, +0.1 s fade). |
| Redundant hit at 19.31 | Deleted. The seabed touchdown is one thump plus a boom layer on 19.27. |
| Slam 5 frames after the flash cut | Moved onto the cut (24.33). |
| Horn inaudible (-12.7 dB under the voice) | Real liner horn, onset on the SS United States cut, -9.5 dB, held over both SS United States shots. |
| Strike scrapes and sonar inaudible | Replaced: a pop on the KEEP HER strike, a boom on the SINK HER box, and a riser into the x-ray reveal. |
| 30-40 s dead air | Low tension drone bed, plus the projector loop on the film shots. |
| "37" lands 1.0 s after the spoken word | **Skipped** (picture fix). The pop sits on the frame where 37 lands (13.20). |

## 5. Passing check output

```
$ python3 tools/sound/check_sound_lock.py --render audio/v2/master.json --cues build/sfx_placed_v2.json --measure audio/v2/measure.json
SOUND LOCK OK (static): role levels + gaps, real Epidemic recordings (md5), music 0.08 + ducking, voice compressor/limiter/de-ess/edge fades, 2c-9 gain + alimiter 0.84, loudnorm linear gate, stereo, pad, fade-out, HPF
SOUND LOCK OK (render): -14.1 LUFS, TP -1.6 dBTP, LRA 5.1 LU, loudnorm linear, stereo, audio = video length, music under speech -21.9 dB, 9 big beats >= +3 LU over speech, 22 cues within 3 frames
```

The gate works: the first run of this build stopped with
`LOUDNESS FAIL: loudnorm went dynamic (pred TP -1.12); build stopped`. Later calibration runs stopped with
`LRA 4.7 LU < 5`, and `big beat @ 19.27 only +1.0 LU above speech`.

## 6. Owner decisions still open

- **New roles.** "ship" (-13), "horn" (-10), and the unducked punch stem for big beats are new. None of them is
  in battle-maps STYLE_LOCK.
- **2a sound design.** Pop, boom, riser, projector and drone now play real Epidemic library recordings. STYLE_LOCK
  2c-5 banned only the synthesized versions. Listen before locking.
- **Voice level.** The voice stem sits at -29 LUFS on the bus, with the music trimmed -6 dB to keep the battle-maps
  music:voice ratio. This is what gives LRA ≥ 5 and beats at +4.6 to +7 LU.
- **Not done** (voice-timing changes, out of scope because the voice and timing were reused):
  - the critic's 0.5 s pause after "charges";
  - splitting the 13-word sentence;
  - the speed-0.88 question block.
