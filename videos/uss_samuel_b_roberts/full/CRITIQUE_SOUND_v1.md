# Sound critique v1: USS Samuel B. Roberts full master

Verdict (plain English)
1. The owner is right about the big effects. Hit, boom, impact and explosion cues are 2 to 5 LU louder than the speech around them, and all of them play while the narrator is talking.
2. The worst are the hits and booms in the hook and the story beats: 12.8 s (SAMUEL B. ROBERTS bar), 355 s (the twist), 411 s (first hit), 129 s (first salvo) and 522 s (St. Lo).
3. The three explosions are not loud by loudness but by shape. Their peaks reach +4 to +6 dBFS before the limiter, so the limiter takes 7 to 9 dB off them in one blow. That is a hard, clipped bang that also dips the voice.
4. Beds are NOT the problem: projector sits 14 to 20 LU under speech and underwater 24 LU under. Pops, ticks and whooshes are fine, with one exception (pop stacked on a hit at 395.9 s). The 15 loudest master moments are 14 voice, 1 hit.
5. Fix: cut hit, boom and impact by 2 to 4 dB and explosion by 4 to 5 dB. That keeps every big beat still at least +1 LU over speech (the locked floor) and keeps the master at -14 LUFS, because the mix normalises (voice gains only about 0.1 dB).

Method: master.wav and the per-bus stems in audio/mix (voice, music, sfx, punch, beds) read with 400 ms momentary BS.1770 loudness. Stem levels are put at master scale (+14.73 dB). Speech reference = median voice momentary level within +/-6 s of the cue, where voice is above -22 LUFS (about -14.4 overall). Master: integrated -14.0, true peak -1.9, LRA 2.2, speech momentary median -13.3, p95 -10.7.

## Loudest problem cues
"Over speech" = SFX (sfx + punch stems) momentary maximum minus the median speech level around the cue, in LU. "Peak" = SFX stem sample peak at master scale, before the limiter.

| Time (s) | Role | Note | SFX M (LUFS) | Over speech | Peak (dBFS) | Recommended cut |
|---|---|---|---|---|---|---|
| 410.98 | impact (punch) | first hit | -9.6 | +5.1 | +1.2 | -4 dB |
| 12.77 | hit | gauge bar SAMUEL B. ROBERTS (hook) | -9.7 | +4.9 | -1.0 | -3.5 dB |
| 354.94 | hit | the twist | -9.8 | +4.8 | -1.9 | -3.5 dB |
| 129.05 | boom (punch) | first salvo | -10.6 | +4.1 | -3.5 | -2.5 dB |
| 522.07 | explosion (punch) | St. Lo | -10.3 | +3.9 | +4.1 | -4.5 dB (limiter takes 7 dB) |
| 776.76 | hit | gauge bar TITANIC | -10.7 | +3.8 | -4.1 | -2.5 dB |
| 479.66 | boom (punch) | turn | -11.0 | +3.3 | -3.8 | -2 dB |
| 766.80 | boom (punch) | depth lands | -11.5 | +2.9 | -4.4 | -1.5 dB |
| 424.61 | explosion (punch) | salvo | -11.7 | +2.4 | +4.3 | -4 dB (limiter takes 7.7 dB) |
| 395.92 | hit + pop | 608 (two cues on the same instant) | -12.1 | +2.3 (pop adds 1.8 alone) | -4.4 | hit -2 dB, drop the pop on this cue or -6 dB |
| 33.40 | impact (punch) | splashes (hook) | -13.0 | +1.9 | -0.7 | -1.5 dB |
| 302.95 | hit | quote (pop on top) | -12.4 | +1.9 | -3.0 | -1.5 dB |
| 338.21 | hit | three torpedoes | -12.5 | +1.7 | -7.3 | -1 dB |
| 702.83 | hit | gauge bar USS JOHNSTON | -12.2 | +1.7 | -6.0 | -1 dB |
| 131.13 | impact (punch) | straddle | -13.3 | +1.5 | +1.0 | -1.5 dB |
| 44.00 | explosion (punch) | St. Lo blast (hook) | -14.9 | -1.2 | +5.6 | -4 dB (limiter takes 8.8 dB) |

Notes:
- Explosion at 44.0 s: loudness is fine, but the burst peaks at +5.6 dBFS and the limiter cuts 8.8 dB. The cut is about shape, not level.
- Limiter gain reduction on punch cues: 7.1 to 8.8 dB on explosions, 3.5 to 5.4 dB on impact and boom, 2 to 4.9 dB on hits. Pre-limiter mix peak is +6.2 dBFS (measure.json: -8.5 at mix scale).
- Hook (first 53 s): whoosh 0.3 s is OK (-1 LU vs speech). Underwater bed 8.7 to 17.6 s is -38 LUFS, 24 LU under voice. The loud things are the 12.8 hit (+4.9) and the 44.0 blast (peak). The hit sits at the moment the voice dips (voice -14.5 there), so it reads as louder than the narrator. The 33.4 splash is about equal to speech.
- Time of hits vs voice at the same instant: 12.77 +4.8, 129.05 +3.5, 354.94 +3.0, 522.07 +3.9, 776.76 +3.7, 766.80 +2.2, 479.66 +2.6.

## 15 loudest master moments (400 ms, master.wav)
Result: 14 of 15 are the narrator's own emphasis (voice stem -8.6 to -9.6 LUFS). The SFX are not what makes the master peak. Only the hit at 355 s is an SFX peak.

| # | Time (s) | Master M | Cause |
|---|---|---|---|
| 1 | 832.3 | -8.9 | voice only (emphasis, nothing else) |
| 2 | 355.0 | -9.0 | hit "the twist" (SFX -9.8) over voice -13.1: the one SFX-caused peak |
| 3 | 4.2 | -9.1 | voice only (hook line) |
| 4 | 384.9 | -9.3 | voice only |
| 5 | 12.9 | -9.3 | hit on the hero bar, over voice -16.9 (underwater bed under it, -42) |
| 6 | 734.3 | -9.4 | voice only |
| 7 | 448.3 | -9.4 | voice only |
| 8 | 396.0 | -9.4 | hit + pop "608" on voice -11.7 |
| 9 | 371.6 | -9.4 | voice only |
| 10 | 475.7 | -9.5 | voice only |
| 11 | 806.9 | -9.5 | voice only (pop is -33) |
| 12 | 131.1 | -9.5 | impact "straddle" with voice -10.4: SFX adds on top of already loud speech |
| 13 | 719.5 | -9.5 | voice only |
| 14 | 857.0 | -9.5 | voice only |
| 15 | 418.1 | -9.5 | voice only |

The narration itself is hot in places (p95 -10.7 LUFS vs median -13.3). That is outside the SFX brief, but it is why SFX riding +3 to +5 over the median feels like "too loud" next to a narrator who is already at -9 to -10.

## Recommended changes (cuts only, master stays -14 LUFS)
Role defaults (KINDS in tools/sound/sfx_mix_lib.py; the sound lock in tools/sound/check_sound_lock.py would need the same numbers):

| Role | Now | New | Cut |
|---|---|---|---|
| hit | -11 | -14 | -3 dB (hero bars 12.77, 776.76 and the twist 354.94 -3.5/-2.5 per cue; quieter hits 338/702 only -1) |
| boom | -14 | -16 | -2 dB |
| impact | -10 | -13 | -3 dB (411 first hit -4) |
| explosion | -7 | -11.5 | -4.5 dB, and ease the peak: add a 5 ms attack soft-clip or lowpass at 6 kHz on the punch bus so the limiter stops taking 7 to 9 dB |
| whoosh | -15 | keep | 0 |
| pop / tick | -23 | keep | 0 (but drop or -6 dB the pop that lands with a hit at 302.9 and 395.9) |
| beds (projector -29, drone/waves -32, underwater -32) | | keep | 0. Optional -2 dB on the projector if the owner still hears it under film: its peaks reach -28 LUFS, 14 LU under speech |

Alternative if the lock should stay untouched: use per-cue `gain_db` (allowed, cuts only): 410.98 -4, 12.77 -3.5, 354.94 -3.5, 522.07 -4.5, 424.61 -4, 44.00 -4, 129.05 -2.5, 776.76 -2.5, 479.66 -2, 395.92 hit -2, 766.80 -1.5, 33.40 -1.5, 302.95 -1.5, 131.13 -1.5, 338.21 -1, 702.83 -1.

After these cuts the big beats land at about +1 to +1.5 LU over speech (still meeting the locked "big beats at least +1 LU" floor) and LRA falls from 2.2 to about 1.8 to 2.0 (the floor is 1.7, so do not cut more than this in total). Re-run the mix and measure.json to confirm: biggest beat is at most +1.5 LU over speech, explosion limiter reduction at most 3 dB, integrated -14.0.

Not measured: the SFX in the video's own film audio (none present in the stems) and phone-speaker playback, where the 100 to 300 Hz weight of the boom_a file (shared by hit and boom) would add to the harshness.
