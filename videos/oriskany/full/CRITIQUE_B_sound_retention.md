# Oriskany full v1: critique B (sound and retention)

**File checked:** `oriskany_full_v1.mp4` (884.8 s). Critic B, 2026-11-05. I took no claim on trust. I measured everything below
myself:
- ffmpeg `ebur128` on the final mp4, per chapter on `audio/mix/master.wav`, and on the test v4 mp4;
- K-weighted momentary loudness (400 ms) of every bus stem in `audio/mix/*_bus.wav`, scaled to the master (+14.48 dB);
- 18 frame strips around cues (5–30 fps);
- frame grabs every 10 s (89 frames);
- faster-whisper `base.en` on the master and on the clean voice stem. Where the master transcript differs from the stem, that is evidence of masking.

Chapter 1 (0–48.6 s) is the owner-approved hook. Issues there are marked **approved hook — owner decision**.

## Measurements

| measure | full v1 (my measurement) | test v4 (approved) | note |
|---|---|---|---|
| Integrated | **-14.0 LUFS** | -13.9 | OK |
| True peak | **-1.6 dBTP** | -1.5 | OK |
| LRA | **2.4 LU** (low -15.4 / high -12.9) | 5.8 | per chapter: c01 3.4, c02 2.2, c03 2.5, c04 2.1, c05 2.1, c06 1.7, c07 2.8 |
| Short-term over time | 10 s medians stay between -12.8 and -15.5 LUFS from 0 to 866 s | | flat, as expected for narration |
| End screen 866.8–884.8 | **-33.2 LUFS** | n/a | 19 LU below the programme |
| Music under voice (whole video) | **-24.1 dB** re voice | -22.0 | the build report's figure is correct |
| Music under voice, c01–c05 (10 s windows) | -21 to -25 dB | | |
| Music under voice, c06–c07 (566–806 s) | **-26 to -31 dB** | | barely audible (S1) |
| Music under voice, 370–400 s | -28, -31, **-40**, -27 dB | | the music almost disappears (S2) |
| Loudest music under voice | -18.1 dB (350–360 s, the c03→c04 swell) | | still inside the -18..-28 band |
| Hook speech (momentary median) | -13.1 LUFS | -14.4 | the whole-video gain makes the hook 1.3 dB hotter |

**Verdict on the owner's "music too loud" complaint:** it does not apply to this master. Nowhere does the music compete with the
voice. The real music problem is the opposite: in two stretches the music is effectively missing (S1, S2).

**Cue loudness by role** (SFX momentary max re the local voice median, ±5 s):

| role | n | median | max | comment |
|---|---|---|---|---|
| hit (gauge bars, stamps) | 11 | **+6.3 LU** | **+8.5** | louder than the sinking blast (M3) |
| explosion | 3 | +5.2 | +8.2 | c05 "they fired" is only +5.0 |
| impact | 3 | +3.6 | +4.8 | |
| boom | 3 | +5.8 | +8.2 | |
| jet | 7 | +3.2 | +6.6 | 3 of the 7 play with no aircraft on screen (M2) |
| whoosh | 37 | -0.6 | +3.1 | as loud as the voice, every ~22 s (M1) |
| riser | 11 | -2.5 | -1.8 | |
| ship | 8 | -1.8 | +4.8 | the bubbles at 559.14 are -8.8 LU, so they cannot be heard |
| horn | 2 | -1.2 | -1.0 | |
| pop / tick | 65 / 47 | -13.0 / -14.4 | | fine |

**Sync, checked on 18 cues** (106.20, 145.30, 172.91, 181.41, 188.17, 232.11, 242.24, 266.17, 325.94, 401.00, 474.44, 526.27, 537.69,
544.28, 613.75, 730.83, 776.77, 815.14, 825.86, 837.27, 861.89): every cue sits within about 2 frames of its picture event. The
exceptions are the jet cues on a ship-launch film (M2) and the 212 FT counter (N7). The sync claim in the build report holds. The problems are
**which** sounds play and **how loud**, not when.

---

## MUST FIX

### M1. A whoosh on every map move: 37 cues, against the lock and the approved reference
- **Where:** 51.59, 79.56, 100.19, 107.56, 131.59, 153.66, 177.04, 196.19, 208.53, 213.45, 229.19, 239.25, 247.68, 258.52, 312.31, 329.96,
  356.27, 360.27, 371.97, 391.51, 441.21, 454.33, 484.78, 510.78, 563.67, 580.29, 599.18, 654.46, 686.84, 701.11, 738.33, 832.86, 843.03,
  854.24 and 864.70.
- **What is wrong:**
  - STYLE_LOCK §3 (owner 2026-09-30) says the zoom sound goes "only on the BIGGEST camera moves… no zoom sound on ordinary camera moves".
  - The approved test v4 has exactly 2 whooshes, labelled "biggest move #1 / #2".
  - This build has 35 in the body, one about every 22 s.
- **Evidence:** the whoosh role is at a median -0.6 LU re the local voice, and peaks at +3.1 LU. It is a voice-level swish under narration, over and
  over. In the master, whisper heard "tore the wing off" (331 s) as "toward", where the stem is clean. The 329.96 whoosh sits on top of it.
- **Fix:** in `build/sfx_full.py`, keep the whoosh only on the 2–3 biggest moves in the body: **153.66** (tow around South America),
  **484.78** (c05 opener, back to Pensacola) and **686.84** (c07 dive to the wreck). Keep the hook pair. Delete the rest. This is an audio-only remix.

### M2. Jet sounds over a 1945 ship-launch film, with no aircraft on screen
- **Where:** 172.91, 181.41 and 188.17 (`b1_launch_crowd`, `b1_launch_hull` and `b1_launch_bow` = NARA 39085, carrier launching).
- **What is wrong:** the frames from 172.5 to 189 s show the bow and stem on the launching stand at the Navy Yard. There is no aircraft. The builder
  read "launch" in the file names as an aircraft launch. This breaks the owner rule (2026-10-06): "Aircraft sounds only when an aircraft is
  on screen". A viewer hears jet engines over a hull sliding down the ways, in a WWII-era passage.
- **Fix:** delete all 3 jet cues. If the hull visibly moves, a `ship` groan (-13) on that frame is the right role. Otherwise leave it silent with
  the projector bed. Also check **325.94** (`b3_a4e_launch_1968`). In the strip from 325.4 to 327.8 s I see deck crew but no aircraft in frame.
  Keep that cue only if the A-4 is visible.

### M3. Bar-chart booms are louder than the carrier being blown up
- **Where:** `hit` cues at 401.00, 474.44, 477.63, 776.77, 781.24, 786.01, 799.31 and 819.08 (gauge bars landing), and 106.20 / 145.30 (DEFAULTED stamps).
- **Evidence:**
  - The hits run +3.6 to **+8.5 LU** over the voice: 781.24 +8.5, 145.30 +8.3, 799.31 +7.5, 776.77 +7.0.
  - All of them play **under words**, for example "…the Navy still called her a bargain".
  - The c05 climax is quieter: the charges at 526.27 are +5.0, and the seabed thump at 544.28 is +3.6.
  - Master momentary max: 781.24 = **-7.2 LUFS**; 526.27 "they fired" = **-11.1 LUFS**.
  - The loudest moment of the second half is a bar chart. c07 alone has 5 booms in 43 s (776–819).
- **Fix (no level change, role choice only):**
  - Re-role the 8 gauge-bar cues to `pop` (-20).
  - Keep `hit` only on the second DEFAULTED stamp (145.30, the payoff), and re-role 106.20 to `pop`.
  - The answer boom at 815.14 is then the single big beat of the last act, which is where it belongs.

### M4. Publish window: the stakes expire on 12 November
- **Where:** 39–47 s (hook) and 822–857 s: "is scheduled to follow her down", "plans to sink the SS United States", "about to take her title".
- **What is wrong:** today is 5 November. After the 12th, the line "it matters right now" and the whole ending are false, and the promise of the title and thumbnail
  goes stale. This is also DO #2 in the study: "ship time-sensitive ones fast".
- **Fix:** publish by about 9 November at the latest. That leaves sound fixes M1–M3 and S1–S4 as one audio-only remix (`mix_full.py` steps 2–5,
  with no picture render). Re-voicing the hook lines is an **approved hook — owner decision**.

---

## SHOULD FIX

### S1. The music fades out of the tension chapters (c06–c07, 566–806 s)
- **Evidence:**
  - Music under voice is -26 to -31 dB in the 10 s windows, and -25 to -30 dB in the gaps.
  - c02–c05 sit at -21 to -25 dB.
  - The bed itself is uneven: in `music_bed.wav`, 0–360 s = -19.3 LUFS, but 566–806 s = **-22.5 LUFS** (LRA 9.0).
  - Cause: `build/music_bed.py` runs one `loudnorm` over the whole concatenated bed, so "Your Mother's Daughter" comes out about 3 dB under the first track.
- **Fix:** run loudnorm to -20 LUFS on **each piece** before the crossfades. That is what STYLE_LOCK §4 describes ("fits each track to its chapter… -20 LUFS").
  - Expected change: about +2.5 dB on the track-03 pieces and -0.7 dB on track 01.
  - c06/c07 then land at about -24 to -28 dB under the voice. That is still quieter than test v4 (-22), so the owner's complaint stays respected.
  - MUSIC_VOL 0.08, MUSIC_TRIM_DB -6 and the ducking are unchanged.

### S2. An unplanned music hole at 368–402 s, then the opening theme restarts
- **Evidence:**
  - Piece 1 plays track 01 to src 407.5 of 414.7 s, which runs into the track's own outro.
  - The music in the master falls to -42 / -47 / **-53 to -59 LUFS** from 384 to 400 s, so it is gone. Then the same piece restarts from src 90 at 402.5 s.
  - It lands under "Corpus Christi… two point eight million", which is not a moment that needs silence.
  - It also falls in the slowest stretch of the video (S6).
- **Fix (`build/music_bed.json`):**
  - piece 1: plays 0 → 362.5 (src 0–362.5, before the outro that starts at about 368);
  - piece 2: src 90, plays_from 357.5 → 568.4 (src_end about 301).
  - The crossfade then sits on the c03/c04 chapter cut (359.97 s, "Then, in two thousand three, Congress changed the rules"), which is a real turn.

### S3. The climax (c05) is masked and has no room to breathe
- **Evidence:**
  - The groans at 531.20–533.67 and 533.55–536.49 sit under "She took thirty-seven minutes. She went down stern first".
  - Whisper heard the master as "She went **downstairs** first". The clean stem reads "down stern first".
  - The pause after "they fired." is 0.74 s. After "Then she was gone." it is 0.69 s.
  - c05 is the **fastest** chapter (167 wpm, against 151–161 elsewhere).
  - The music keeps playing straight through the sinking.
- **Fix (audio only):**
  - Start groan 1 at 532.80, after "minutes.".
  - Drop groan 2, or start it at 535.05, in the gap before "her bow".
  - Dip the music to silence (automation, about -12 dB) from 538.46 to 540.6, so "Then she was gone" lands in silence.
  - Add a `boom` layer under the 526.27 charges, as the hook does at 17.65 (locked role and level). That lifts the mid-video blast from +5.0 to about +8 LU, so
    it matches the hook.
- **Better, at the next voice and picture pass:** add 1.2 s after "thirty-seven minutes." and 1.5 s after "gone.".

### S4. A flood rush under the closing question
- **Where:** 861.89–864.52. The `ship` flood is at -1.8 LU re voice, under "Or just the cheapest way to let her go?". A whoosh starts at 864.46 on top of "Tell us".
- **Fix:** delete the flood cue. The closing question should be the cleanest line in the video. Keep the end-screen whoosh, or move it to 865.9 after
  "comments.".

### S5. The x-ray riser plays 11 times
- **Where:** risers at 266.17, 389.42, 436.44, 479.66, 516.58, 565.88, 571.91, 678.16, 745.45 and 809.57, plus the hook. Each is 2–5 s long, at -2.5 LU re voice, under speech.
  The dark drawn-carrier x-ray recurs about 8 times on the 10 s sheet as well.
- **What is wrong:**
  - Two risers come within 6 s of each other (565.9 and 571.9).
  - The 266.17 riser peaks right after "Gulf of Tonkin" (the word ends at 265.79) and swells over it.
  - Repeating the same sound with the same picture tells a viewer "this again".
- **Fix:** keep the risers at 266 (first use), 517 (22 charges), 566 (PCBs) and 810 (wiring = the answer). Drop the risers at 389, 436, 480, 572, 678 and 745.

### S6. Retention: 6:00–8:05 (360–484 s) is the most likely place to lose viewers
- **Evidence:**
  - There are about 17 numbers in 124 s: 2003, 4 bids, 5 states, April 2004, 2 years, 11 months, $2.8M, $2.1M, $7.6M, ½, $3.7M, June 2005, $800k, $12.7M, $20M,
    $21M and 7×.
  - The picture is mostly dark cards and gauges. On my 10 s grabs, about 6:45 is an empty dark card, about 7:45 an empty gauge, and about 7:55 the "FLORIDA SENATE" kicker on black.
  - The S2 music hole falls in the same place.
- **Fix:**
  - The S2 fix restores the music here, at no cost.
  - If the video is re-cut, merge the two totals into one line: "Press reports on sinking day put the total at about twenty million, almost all of it Navy money" (cut the
    Florida-legislature $21M sentence, about 6 s, and one card).
  - Also cut "Congress had committed two point eight million… Two point one million of it was for removing contaminants" (396–403 s). The "seven times" payoff at about 477 s can then
    say "about seven times the original budget".

### S7. Retention: the résumé creeps in at 2:57–6:00 (c03)
- **What is wrong:** this is a 3-minute service history. It is allowed after 2 min, it has a good bridge ("what kind of ship ends up like this?"), and the fire and the comment prompt
  (301 s, the first emotional peak, as rule A12 says) are strong. But "In August 1947 the work stopped… rushed her to completion" (193–200 s) and the "twelve thousand
  combat sorties" paragraph (230.6–238 s) are pure résumé.
- **Fix at a re-cut:** cut the sorties paragraph, and shorten 1947/1950 to "The work stopped after the war. Korea brought her back." This saves about 15–20 s. If the video is not
  re-cut, accept it as it is.

---

## NICE

- **N1. End screen 866.8–884.8 s at -33.2 LUFS.** That is 19 LU below the programme, and it sounds like the video has died. Lift the music only for those 18 s (no voice to duck) by about
  8 dB, to about -25 LUFS, with the fade kept. This changes music level on the end screen, so it is the owner's call.
- **N2. "Mighty O" (207.07).** The tick for the THE MIGHTY O label (206.85) lands on the nickname. Whisper heard the master as "the mighty old"; the stem reads "Mighty O".
  Move the tick to 207.6, or drop it.
- **N3. The bubbles at 559.14 cannot be heard** (-8.8 LU re voice). Drop the cue; it adds nothing.
- **N4. The ending horn at 825.86** plays under "She will not be the biggest for long" (-1.4 LU re voice). The role note says "in a voice gap". The words stay
  intelligible. If the liner shot is long enough, start the horn at 827.55, in the gap before "On November twelfth".
- **N5. Voice, to check by ear** (base.en is not conclusive):
  - "Mare Island" (138.93): the stem was transcribed "Mayor Island". The correct sound is one syllable, "mair".
  - "Gustav" heard as "Gustave" (702.38).
  - "porgies" heard as "porkeys" (637.92).
  - "Oriskany" heard as "O'Riscany" / "Oriskani" in both the stem and the master (17.10, 304.39, 367.92).
  - Longest pause in the video: 1.53 s in the middle of a fact, at 612.2 ("…eight rounds of fish. ‖ Two hundred and fifty-four fish"). It reads as a stall. Use 0.6 s at the next voice render.
  - Delivery is evenly paced (151–167 wpm) with no slow-down at the peaks. See S3.
- **N6. Script repetition.** "In the early nineteen nineties" opens two paragraphs back to back (80.5 and 102.9 s). Make the second "Then the Navy tried the scrapyard. She was sold
  for scrap…".
- **N7. The 212 FT counter lands late.** The 544.28 thump is on the "ON THE SEABED" label flip, but the counter reads 81 FT there and only reaches 212 at about 544.58 (+9 frames). It lands
  after "twelve" (544.27). This is a picture fix: end the count on 544.28.
- **N8. The reversal works but undoes itself.** "It looked like the perfect ending. But her sinking came with a condition" (559.27) is strong. It is placed at 63 % and the
  track change follows 4 s later. Two improvements:
  - start the "Your Mother's Daughter" crossfade about 2 s earlier, so it enters on "But" (about 561.5);
  - "Then the numbers came down… No advisory was ever issued" (660–672) resolves the threat within about 100 s. The question at 673–686 saves the chapter. Keep it as it is.
- **Approved hook — owner decision:**
  - The whole-video gain makes hook speech 1.3 dB hotter than in test v4 (-13.1 vs -14.4 LUFS). The beats over the hook speech lost 0.4–0.9 LU (the seabed thump at 28.7 is +1.8 LU over hook speech, against +2.3 in v4).
  - Hook LRA is 3.4, against 5.7 in v4.
  - The horn masks "follow her **down**": the master transcribes as "follow her dad", the stem as "down".
  - The 17.65 blast lands on "Thirty" of "thirty-seven".

---

## The LRA failure (2.4 LU, rule ≥ 5): does it matter?

**No, not for a 15-minute narrated video.** The reasons:

1. **The references sit at the same level.** The three battle-maps reference masters measure 2.2–2.5 LU. Per chapter here, the range is 1.7–2.8.
2. **The metric can't see what makes this mix dynamic.** EBU LRA is computed from 3 s short-term values. The 0.5–1.5 s pauses and the 1 s blasts hardly move it. A long narration
   through a 2.5:1 voice compressor always measures 2–3 LU. The 5.8 of test v4 came from its 50 s length, its dense beats and its fade.
3. **Reaching 5 would hurt the video.** It would need passages of 3 s or more that are 5+ LU quieter or louder: long silences, or loud set pieces. That is worse on
   phones, and it runs against the owner's complaint about loud music.
4. **YouTube normalises integrated loudness only (-14).** LRA plays no part in that.

**Minimal safe fix:** change the check, not the mix. For full-length masters, replace "LRA ≥ 5" with "LRA 2–8 LU" (the reference band) and keep the
existing per-beat test (every big beat ≥ +3 LU over speech; this build passes 9/9). Note that a "hook only ≥ 5" rule would also fail: the hook in this master
is 3.4. The rule change needs the owner's sign-off, because the check is part of the lock. The S3 silences will lift LRA slightly as a side effect. Don't chase the number beyond that.

---

## Retention summary (as a viewer)

- **Likely drop points, ranked:**
  1. 6:00–8:05, the budget numbers (S6);
  2. 3:10–3:58, the résumé (S7);
  3. 12:50–13:45, four gauge cards in a row, each with a boom (M3);
  4. 10:20–11:00, PCB charts;
  5. 1:40–2:20, the sale paperwork.
- **Wows in the first 3 min:**
  - 0:48–3:00 holds up: theme park in Japan (about 1:28), sold above appraisal (about 1:55), DEFAULTED ×2 (1:46, 2:25), dragged around South America (about 2:35),
    "a WWII carrier that never fought in WWII" (about 3:05).
  - After 3:00 the gaps between wows grow until the fire (4:20).
- **The answer is held back:**
  - The hook's "what was still inside her" is answered by about 7:15 (PCBs left aboard). That is half-way, which is acceptable as a partial reveal.
  - The real answer (the PCBs are in the wiring, and only scrapping could reach them, and scrapping had already failed) is held until 12:25–13:40. ✓
  - No museum answer. ✓ No ship résumé before 2:00. ✓
- **The ending:**
  - The voice ends at 865.8 s, 43.8 s after "She is still the only…" (822.05). That is within the 45 s limit. ✓
  - The twist ("about to take her title", about 853 s) works. ✓
  - The closing question comes at 856.8. ✓ It should be heard clean (S4).
  - The comment CTA at 5:01 matches study rule A12. ✓
- **Against the DO / DON'T lists:**
  - DO #2 (be first, time-sensitive) requires M4.
  - DON'T #12 (pronunciation gate) means checking N5 before upload.
  - Everything else on the lists is met.

## Fix order (one audio-only remix, no re-render)

1. M1, M2, M3, S3 (cues), S4 and S5 in `build/sfx_full.py`.
2. S1 and S2 in `build/music_bed.py` / `music_bed.json`.
3. Re-run `build/mix_full.py` steps 2–5. The join is already up to date.
4. Re-measure, and confirm in the new master:
   - c06–c07 music at -24..-28 dB under voice;
   - no `hit` above +6 LU outside the stamp;
   - 526.27 is the loudest beat after the hook.
5. Publish before 12 November.
