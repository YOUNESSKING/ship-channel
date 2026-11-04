# SOUND REPORT: Oriskany test v4 (measured, not listened to)

Chain: `build/mix.py` = test_v3 `mix_v2.py` adapted: `sfx_cues_v4.py` (real Epidemic recordings, cues on the visual event frame, trimmed to the shot) -> `make_music_bed.py` (Chris Zabriskie, CC BY 4.0) -> `tools/sound/mix_clip.py` v2 (voice stem chain, MUSIC_VOL 0.08 + MUSIC_TRIM_DB -6, unducked punch stem, oversampled limiter + linear loudnorm) -> `measure_mix.py` -> `check_sound_lock.py --render`.

## Master

| integrated | true peak | LRA | music under voice | music in gaps | music duck | sound design under voice | blind gap vs battle-maps refs |
|---|---|---|---|---|---|---|---|
| -13.9 LUFS | -1.5 dBTP | 5.8 LU | -22.0 dB | -19.7 dB | 2.3 dB | -15.1 dB | -18.1 dB (refs -17.3) |

## Big beats vs speech (momentary max over the speech median, target >= +3 LU)

| t | role | above speech | what |
|---|---|---|---|
| 4.30 | explosion | +4.6 LU | WOW 1: blast photo cut + white flash + shake |
| 10.24 | boom | +6.3 LU | ON PURPOSE. lands on 'purpose' |
| 17.65 | explosion | +5.4 LU | second blast photo + flash (smoke, in the voice gap); designed 0.6 s tail into the 37 montage |
| 17.65 | boom | +5.4 LU | second blast: cinematic boom layer under the charge (key beat) |
| 19.85 | impact | +5.1 LU | bow standing vertical: water closing over the hull |
| 28.70 | impact | +3.1 LU | hull touches the seabed on 'floor' (underwater thump) |

## Every cue (sync measured on the rendered segment, frames at 30 fps)

| event t | role | level dB | file | start-end | offset (frames) | what |
|---|---|---|---|---|---|---|
| 0.35 | whoosh | -12.1 | whoosh_a__689b1489.wav | 0.11-2.40 | +0.0 | map dive starts moving (biggest move #1) |
| 2.22 | hit | -7.7 | boom_a__2f0a40ab.wav | 2.11-3.31 | +0.0 | 212 FT card lands on 'feet' |
| 4.30 | explosion | -3.8 | charges_c__f6f10ea4.wav | 4.30-5.45 | +0.8 | WOW 1: blast photo cut + white flash + shake |
| 10.24 | boom | -11.7 | boom_a__2f0a40ab.wav | 10.12-11.42 | +0.0 | ON PURPOSE. lands on 'purpose' |
| 17.65 | explosion | -4.5 | charges_c__f6f10ea4.wav | 17.65-18.50 | +0.8 | second blast photo + flash (smoke, in the voice gap); designed 0.6 s tail into the 37 montage |
| 17.65 | boom | -10.7 | boom_a__2f0a40ab.wav | 17.65-18.54 | +1.1 | second blast: cinematic boom layer under the charge (key beat) |
| 18.69 | pop | -21.0 | pop_b__844f57e0.wav | 18.67-18.92 | +0.0 | 37 lands (count ends on 'thirty-seven') |
| 19.85 | impact | -6.8 | splash_a__1d6949d6.wav | 19.85-20.70 | +1.1 | bow standing vertical: water closing over the hull |
| 19.90 | ship | -12.8 | flood_a__db95b348.wav | 19.90-20.65 | +0.0 | flood rush as the bow slips under (to the foam cut) |
| 20.55 | ship | -13.3 | bubbles_a__e58b390c.wav | 20.55-21.40 | +0.0 | only foam left: air bursting out |
| 22.79 | pop | -20.5 | pop_b__844f57e0.wav | 22.77-23.02 | +0.0 | 3+ YEARS lands on 'three' |
| 26.25 | ship | -13.6 | groan_a__7c63fd7c.wav | 26.19-28.59 | +0.0 | drawn carrier going down: hull groan (until touchdown) |
| 28.70 | impact | -7.6 | charges_b__0ecb5c38.wav | 28.55-29.55 | +0.0 | hull touches the seabed on 'floor' (underwater thump) |
| 34.90 | riser | -17.3 | riser_a__fd98cb0b.wav | 32.70-34.97 | +0.0 | reverse riser INTO the x-ray reveal (peaks on the cut) |
| 39.55 | horn | -10.2 | horn_a__463af07a.wav | 39.55-45.80 | +0.0 | SS United States on screen: liner horn (signature sound) |
| 45.80 | whoosh | -12.2 | whoosh_b__8d9712d2.wav | 45.80-48.86 | +0.3 | end map pull-back (biggest move #2) |

Beds:

- waves 0.00-4.30 s at -30 dB (Gulf of Mexico: sea under the map dive)
- waves 9.98-21.25 s at -30 dB (foam / sea photos of the sinking day)
- underwater 26.00-32.70 s at -30 dB (drawn sinking: underwater ambience)
- drone 29.60-39.55 s at -30 dB (the question block: low tension drone)
- waves 45.80-50.20 s at -30 dB (end map: sea)
- projector 6.38-9.98 s at -27 dB (projector loop under archive film)
- projector 32.70-34.90 s at -27 dB (projector loop under archive film)
- projector 39.55-45.80 s at -27 dB (projector loop under archive film)

Density: 16 cues in 50.2 s = 19.1 per minute (target ~16; the small pops on 22 / $20 / ? / 13 and the option ticks are left out on purpose).

## check_sound_lock output

```
SOUND LOCK OK (static): role levels + gaps, real Epidemic recordings (md5), music 0.08 + ducking, voice compressor/limiter/de-ess/edge fades, 2c-9 gain + alimiter 0.84, loudnorm linear gate, stereo, pad, fade-out, HPF
SOUND LOCK OK (static): role levels + gaps, real Epidemic recordings (md5), music 0.08 + ducking, voice compressor/limiter/de-ess/edge fades, 2c-9 gain + alimiter 0.84, loudnorm linear gate, stereo, pad, fade-out, HPF
SOUND LOCK OK (render): -13.9 LUFS, TP -1.5 dBTP, LRA 5.8 LU, loudnorm linear, stereo, audio = video length, music under speech -22.0 dB, 6 big beats >= +3 LU over speech, 16 cues within 3 frames
```

## Screen time

Film (real NARA motion picture) 12.0 s = 24 % · moving stills (2006 Navy photos, 3D push) 18.1 s = 36 % · maps + animation 20.1 s = 40 %.

| shot | time | dur | template | segment | type |
|---|---|---|---|---|---|
| s01 | 0.00-4.30 | 4.30 | number_clip | dive.mp4 | map/anim |
| s02 | 4.30-6.38 | 2.08 | clip_plain | p02_blast.mp4 | still |
| s03 | 6.38-7.98 | 1.60 | clip_plain | f03_catapult.mp4 | film |
| s04 | 7.98-9.98 | 2.00 | clip_plain | f04_island.mp4 | film |
| s05 | 9.98-11.50 | 1.52 | number_clip | p05_foam.mp4 | still |
| s06 | 11.50-13.75 | 2.25 | lower_third | p06_detcord.mp4 | still |
| s07 | 13.75-15.95 | 2.20 | number_clip | p07_inside.mp4 | still |
| s08 | 15.95-17.65 | 1.70 | lower_third | p08_helo.mp4 | still |
| s09 | 17.65-17.98 | 0.33 | clip_plain | p09_smoke.mp4 | still |
| s10 | 17.98-19.85 | 1.87 | number_clip | m37_sequence.mp4 | still |
| s11 | 19.85-20.55 | 0.70 | clip_plain | p11_bow.mp4 | still |
| s11b | 20.55-21.25 | 0.70 | clip_plain | p11b_foam.mp4 | still |
| s12 | 21.25-23.84 | 2.59 | number_clip | p12_cut.mp4 | still |
| s13 | 23.84-26.00 | 2.16 | number_clip | p13_weld.mp4 | still |
| s14 | 26.00-29.60 | 3.60 | clip_plain | hero_a.mp4 | map/anim |
| s15 | 29.60-32.70 | 3.10 | anim_options | (animation) | map/anim |
| s16 | 32.70-34.90 | 2.20 | clip_plain | f16_anchor.mp4 | film |
| s17 | 34.90-37.80 | 2.90 | anim_xray | (animation) | map/anim |
| s18 | 37.80-39.55 | 1.75 | map_clip | gulfpin.mp4 | map/anim |
| s19 | 39.55-41.55 | 2.00 | clip_plain | f19_stacks.mp4 | film |
| s20 | 41.55-43.70 | 2.15 | lower_third | f20_bow.mp4 | film |
| s20c | 43.70-45.80 | 2.10 | clip_plain | f20b_profile.mp4 | film |
| s21 | 45.80-50.20 | 4.40 | map_clip | endmap.mp4 | map/anim |
