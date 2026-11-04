# Oriskany test v3: sound, sync, voice, accuracy and rights critique

Reviewer lens: sound mix, sync, voice, narration and on-screen accuracy, rights and credits, YouTube policy. Story and visual editing are covered by the other critic.
File reviewed: `oriskany_test_v3.mp4`: 53.6 s, 1920x1080, 30 fps, AAC 192k, **mono**, 48 kHz.
How it was measured: ffmpeg ebur128 on the master. I rebuilt the stems through the exact `mix_clip.py` filter graph from `audio/voice.wav`, `sfx.wav` and `music_bed.wav`; the rebuild matches `audio/mix.wav` within 0.03 dB RMS. Then I ran numpy/scipy analysis at 0.1 s and 50 ms resolution, analysed each kit file, and checked frame strips around every cue. Scratch files are in `/tmp/claude-0/-home-user/e065d3fa-b63b-536b-bb86-8680d09491b8/scratchpad/critic_sound/`. Nothing was listened to: every finding below comes from a measurement.

---

## 1. Measured numbers

### Master loudness (ebur128, `peak=true`)
| metric | measured | target | verdict |
|---|---|---|---|
| Integrated | **-14.3 LUFS** | -14 (2c-9: -14.3 is OK) | pass |
| True peak | **-1.2 dBTP** | ≤ -1.0 / -1.5 | pass (sample peak -1.65 dBFS, 0 clipped samples) |
| LRA | **2.0 LU** | lock asks for LRA 11 linear | see below: heavily flattened |
| Short-term (3 s) range, 3-53 s | -16.4 to -13.1 LUFS | n/a | flat |
| Momentary max during the **big SFX beats** (explosion 9.0 s, sink 14.1 s, seabed 19.7 s, slam 24.7 s, end stamp 51.4 s) | -11.4 / -11.6 / -12.5 / -13.8 / -11.6 LUFS | should rise above speech | **fail**: speech-only stretch 31-40 s already peaks at -11.8 M (median -14.4). No beat is louder than the narration |
| Audio length vs video | 53.513 s vs 53.600 s | equal | **fail**: last 87 ms have no audio; the mix stops at the voice length (53.43 s) while the "THE SAME REASON" hit tail is still at **-21.6 dBFS peak** in the last 20 ms, an audible chop |
| Channels | mono | stereo master | **fail**: the stereo music bed and SFX are folded to mono by `amix` (the first input, the voice, is mono) |

**Root cause of the flat master.** The mix runs `alimiter=limit=0.5` (-6 dBFS ceiling). The voice stem peaks at -1.7 dBFS, so this limiter alone takes about 4.3 dB off the voice peaks. The linear loudnorm then needs +9.2 dB, but the input TP is -5.97, so the output would land at +3.2 dBTP. That is above the -1.5 TP bound, so **loudnorm silently fell back to `"normalization_type": "dynamic"`**: I re-ran its first pass on `audio/mix.wav` to check. The measured gain from mix to master swings **+5.6 to +12.4 dB** from one 0.5 s window to the next, which is AGC behaviour. The total peak reduction on the voice is about 8 dB (stem PLR 21.4 dB, master PLR 13.1 dB). `SOUND_REPORT.md` says "two-pass loudnorm ... (linear)", which is not what happened. The 2c-9 trim never ran, because the dynamic mode had already landed at -14.3. `check_sound_lock.py` only greps for strings, so it cannot catch this.

### Stems (rebuilt through the real chain; mix-bus scale, master is about +9 dB)
| stem | integrated | peak | notes |
|---|---|---|---|
| voice | -23.1 LUFS | -1.7 dBFS | Kokoro 24 kHz, 16-bit; nothing above 12 kHz (energy above 8 kHz is -24 dB re total) |
| SFX (after ducking) | -31.1 LUFS | -8.5 dBFS | LRA 16.9 |
| music (after ducking) | **-48.2 LUFS** | -27.8 dBFS | before ducking -42.4 LUFS |
| sound design (music + SFX) | -31.6 LUFS | | |

### Ducking and balance
| measurement | value |
|---|---|
| Music duck under speech (median / max) | **9.9 dB / 18.6 dB**; it recovers only 3.9 dB in gaps (400 ms release vs 0.3-1.1 s gaps) |
| Voice over music, under speech | **27.5 dB** (music about -43 dBFS RMS at master scale under words). Locked 0.08 is respected, but the bed is inaudible on phone speakers |
| SFX duck under speech (median / max) | **8.1 dB / 16 dB**, which is not "light". In gaps 0.9 dB |
| Voice over all sound design, under speech | 10.1 dB (rule 100 asks for 11-12 dB). The sound design rises 4.3 dB in pauses |
| Sound-design floor per second | drops to **-48 to -52 dBFS (mix bus) from 30 to 40 s**: a near-silent bed for 9 s (SOUND_REPORT admits "31-40 s is quiet") |
| Spectral balance, whole master | below 120 Hz: -4.6 dB re total; 120-300 Hz: -5.8; **300-3000 Hz: -5.0**; 3-8 kHz: -11.7; above 8 kHz: -21.2. The low end carries as much energy as the voice band |
| Voice stem tilt | 90-120 Hz -7.1, 120-200 Hz -4.5 dB re 300-3 kHz: chesty, with no high-pass |
| Kit "hit" files | `number_land_1/2/3` hold 82-93 % of their energy below 120 Hz, with 3.4-3.75 s tails. They are long sub booms, not card hits. Eight of them are stacked in 53 s |

### Words where an SFX reaches or masks the voice (300-3000 Hz band, SFX minus voice)
| t (s) | word | SFX re voice | culprit |
|---|---|---|---|
| 16.36 | "feet" (nine hundred **feet**) | **+3.6 dB** | flood_rush_1, which peaks at 16.48 |
| 22.24 | "The" (United States Navy) | -3.6 dB | catapult rush |
| 19.31 / 19.55 | "feet down." | -5.3 / -7.6 dB (broadband **+9.8 / +4.6**) | sink_whoomp_2 and number_land_1 stacked 46 ms apart |
| 21.46 / 23.04 | "her." / "Navy" | -5.4 / -6.3 dB | catapult rush |
| 41.14 | "The" (answer) | -5.7 dB | 40.65 hit tail |
| 8.16 | "inside" | -5.9 dB | charges sequence |

### Voice timing (Kokoro am_michael at speed 0.95)
- Overall **155 wpm** (133 words, 0.35-51.74 s): on target.
- **Articulation is uneven: 109-256 wpm per phrase.** The first 12 s are slow; the question block is rushed:
  - "just to get her ready to sink" **256 wpm**
  - "So why would the Navy pay millions..." 210 wpm
  - "or simply cutting her up for scrap?" 215 wpm
- **Mid-sentence silences inside one Kokoro chunk:**
  - 0.36 s at 6.18 s, around "set ... off"
  - 0.40 s at 8.46 s, around "charges ... inside ... a"
  - Both sit inside the 13-word sentence "Navy demolition divers set off explosive charges inside a retired American aircraft carrier." (109 wpm). Whisper stretched "set" to 0.86 s and "a" to 0.42 s around them. This reads as broken prosody.
  - Also 0.36 s at 33.64 s ("millions ... to send"), which is acceptable.
- 0.24 s gap at 1.28 s after "seventeenth,". Whisper's "two" timing (1.283) falls in silence; the real onset is about 1.52 s. Harmless here, but cues keyed to `w2`/`w3` would be 7 frames early.
- **Chunk edges are hard-cut** (no fades):
  - In the voice stem, edges sit at -42 to -50 dBFS: chunk ends at 4.48, 11.76, 14.79, 21.89, 24.03, 30.81, 38.44.
  - That becomes about -33 to -40 dBFS after the master gain: faint ticks, mostly masked by the SFX.
- Pronunciation risk: **"Oriskany" and "Pensacola" are never spoken in this test** (on screen only). Before the long version:
  - Test Kokoro on Or-ISS-kuh-nee (it tends to say or-iss-KAY-nee).
  - Add a phoneme override to `tts/PRONUNCIATION.md`.
  - Also check "Okaloosa", "Destin" and "Beaumont".

### SFX density
- 21 cues in 53.6 s = **23.5/min** raw. Counting stacks as one (19.26 + 19.31; 40.15 + 40.40 + 40.65), about 19/min.
- **Audible** cues: about 16/min. Rule 100's average of about 16 is met by accident, because 4 cues are inaudible:
  - horn: -12.7 dB under the voice
  - sonar ping: -10 to -18 dB under
  - two strike scrapes: -42 dBFS, 23 dB under the hit that covers them

---

## 2. Sync: every cue against the picture (30 fps; + means the sound is late)

The kit files have long build-ups, so the **onset** (first sample) is on time but the **loudest moment** is often 1.5-2.4 s later, over a different shot.

| cue t | role / file | visual event (measured on frames) | onset offset | loudest-50 ms offset | verdict |
|---|---|---|---|---|---|
| 0.35 | hit `number_land_1` | MAY 17, 2006 first visible 0.40, full at ~0.80 | -1.5 f | +5 f (0.56) | ok |
| 2.93 | whoosh `dive_whoosh_2` | map dive cut 2.93 (move to 4.60) | 0 f | +24 f, mid-move | ok |
| 7.40 | explosion `charges_seq_3` | blast photo + white flash at 7.40 | +1 f | **+73 f (9.84 s)**, over the 1966 Yankee Station film under "DECOMMISSIONED 1976" | **FAIL**: the boom is not on the impact (STYLE_LOCK 3) |
| 13.36 | hit `number_land_2` | "37" reached on screen at ~13.20 | +5 f | +14 f (13.67) | late. The 37 lands **30 f after the spoken "thirty-seven"** (12.21) |
| 13.80 | impact `sink_whoomp_1` | bow-high cut 13.80 | 0 f | +8 f (14.06) | ok, but its peak is 12 f after the 37-hit peak: a double sub boom |
| 14.10 | ship `flood_rush_1` | slip cut 14.10 (until 15.30) | +3 f | **+71 f (16.48 s)**, over the 1969 aerial / 900 FT card | **FAIL**, and it masks "feet" |
| 15.66 | hit `number_land_3` | 900 FT first visible ~15.70 | -1 f | +3 f | ok |
| 17.65 | ship `hull_groan_1` | hero sinking 17.50-20.55 | +11 f (352 ms fade-in) | peak 19.03, 7 f before touchdown | ok |
| 19.26 | impact `sink_whoomp_2` | hull touches seabed 19.27-19.33 | 0 f | +3 f | ok |
| 19.31 | hit `number_land_1` | **nothing lands**: "212 FT" is already on screen at 19.00 | n/a | n/a | **remove**: a redundant stacked boom over "feet down" |
| 21.00 | jet `catapult_launch_1` | A-4 shoots past the camera 21.00-21.40; shot ends 22.24 | 0 f (clank) | **+58 f (22.93 s)**, over the island "34" shot | **FAIL**: aircraft sound with no aircraft on screen (STYLE_LOCK 3) |
| 24.51 | slam `text_slam_1` | flash cut 24.33; "ON PURPOSE." fades in 24.43-24.83 (it does not slam) | +5 f after the cut | +6 f | minor: the text should snap in at 24.51, or the sound should move to the cut |
| 26.25 | hit | "3 years" first visible 26.30 | -1.5 f | +8 f | ok |
| 27.57 | hit | "$20 million" first visible ~27.75 | -5 f | -3 f | ok-ish (early) |
| 40.15 | tick `strike_scrape_1` | KEEP HER strike drawn at ~40.37 | -6 f | +18 f | late, and inaudible (-42.9 dBFS) |
| 40.40 | tick `strike_scrape_2` | SCRAP HER strike at ~40.83 | -13 f | +4 f | inaudible (-42.0 dBFS) |
| 40.65 | hit | gold box on SINK HER at 40.83 | -5 f | +1 f | ok |
| 42.62 | tick `sonar_ping_1` | ??? glow on "hidden" | 0 f | +2 f | timing ok, **inaudible** (S-V -10 to -18 dB) |
| 45.02 | ship `horn_distant_1` | SS United States on screen from 44.52 | +20 f after the shot cut | peak 46.57 on the funnels | **inaudible** (-36 dBFS RMS, -12.7 dB under the voice) |
| 49.30 | whoosh `dive_whoosh_3` | end-map pull-back cut 49.30 | 0 f | +18 f | ok |
| 51.32 | hit | THE SAME REASON stamp visible 51.40, settles ~51.65 | -2 f | 0 f | ok |

---

## 3. Accuracy of narration and on-screen text (against FACTCHECK_A/B/C)

| item | where | check | verdict |
|---|---|---|---|
| "May seventeenth, two thousand six" / card MAY 17, 2006 | 0.35 | C-A "Date" | correct |
| "OFF PENSACOLA, FLORIDA", "FINAL CHECK · GULF OF MEXICO" | 0-2.9 | C: 22.5 nmi SE of Pensacola Pass; NARA 6698609 caption | correct |
| "Navy demolition divers ... a retired American aircraft carrier" | 4.6 | C-E1 corrected wording used | correct |
| "NAVY EOD TEAM · MAY 2006" (detcord photo, 13 May 2006) | 4.6 | NARA 6698576 | correct |
| "USS Oriskany / DECOMMISSIONED 1976" | 9.7-10.6 | A-D1: 30 Sep 1976 | fact correct. The footage under it is Oct 1966 Yankee Station, so the caption can be read as the footage's date. Low |
| "Thirty-seven minutes later" / "37 minutes from the first charge" | 12.2 | C: 10:25 to 11:02, NAVREL/MARAD07 | correct. The counter shows "**1 minutes**" at 12.4 (grammar) and passes "32 minutes" at 13.0, after the narrator has already said 37 |
| "About nine hundred feet of warship" / "USS Oriskany · 1969 · about 900 ft" | 15.3 | C-E3 (888 / 911 ft), film NARA 87411 dated 10 Sep 1969 | correct |
| "two hundred and twelve feet down" / gauge 212 FT | 17.6 | C: seafloor 212 ft | correct |
| "USS ORISKANY · 1968" (f12 launch, reel 428-NPC-39916) | 20.6-22.2 | FOOTAGE_LIST row 8: "NARA date Jan 1968 but slate reads 1-3-67 / 1-5-67: say '1967-68'" | **WRONG / unsafe**: the label may be a year off. Use "1967-68" or drop the year. Medium |
| "Preparing her to sink · 3 years" | 26.0-27.5 | kicker sits over **1952 San Diego film** (King Faisal reel, 428-NPC-16662) | **misleading**: the 2003-06 preparation is shown with 1952 footage. Use the 2006 prep stills (6698569 deck cut, 6698553 weld). Medium |
| "three years and about twenty million dollars" / "About $20 million" | 26-29 | C-E4, B15-B17 | correct |
| "budgeted at under $3 million" (subline) | 27.6 | B17: $2.8M was Congress's starting commitment, not a full budget | acceptable but loose. **Not spoken** (2c-7: cards use only words the narrator says). Change to "CONGRESS COMMITTED $2.8M" and say it, or drop it. Low-Med |
| "USS ORISKANY · OFF VIETNAM, 1966" (A-4 "314", reel 428-NPC-37479, 1 Oct 1966) | 31.4-33.8 | FOOTAGE_LIST row 1 | correct |
| "So why would the Navy pay millions..." | 31.4 | consistent with "about $20M" | correct |
| "The answer starts with what was hidden inside her." | 41.1 | B18/B19 (about 700 lb PCBs in cabling) | correct as a tease |
| "SS UNITED STATES · 1968" (reel 428-NPC-39181, Feb 1968) | 44.5 | FOOTAGE_LIST rows 1-7 | correct (Norfolk, N&W Coal Pier 4 is visible: not a "Pacific" scene) |
| "**And this month**, a second famous American ship is scheduled to go down off the same coast" | 44.5 | C-C: 12 Nov 2026, weather permitting; C-E5 | **time-bombed**: true only if published 1-11 Nov 2026 (today is 4 Nov). After the 12th it must become past tense. High if the publish date slips |
| "for the very same reason." + "THE SAME REASON" stamp | 50.5 | Both were reefed as artificial reefs (OKA, FWC) | true. But it directly follows "what was hidden inside her" (PCBs), so viewers may read "same reason" as "same toxic cargo". Make sure the long video's payoff says reef / cost, not PCBs. Low-Med |
| End map: "SS UNITED STATES · SCHEDULED NOV 12, 2026", "13 NAUTICAL MILES APART", "USS ORISKANY · SUNK 2006" | 49.3 | C: 12.68 nmi; FWC / OKA coordinates | correct |
| v13 island shot | 22.30-22.40 | head of the clip still shows the S-2 "**13**" for 2-3 frames before the "34" | trim ss +0.15 s. Low |

---

## 4. Rights, credits and policy

| item | finding | severity |
|---|---|---|
| 2006 NARA photos (22 listed) | all USN photographers (JO1, PH2, PHAN); **no CIV credit**; useRestriction "Unrestricted"; PD | ok |
| Unused photos in CREDITS | 6698597, 6698569, 6698583, 6698555, 6698618-20 are listed but not used in v3 (p11, p13, p16, p18, p05*); the header still says "copied to test_v2/assets/" | Low: trim to what is used |
| v3 film table (f06-f23) | **no licence or rights column and no author**. Every reel is NARA useRestriction **"Undetermined"** (RG 428 default). The PD basis (US Navy film = federal work) is stated only in FOOTAGE_LIST, not per row in CREDITS | Med: add "US Navy / NARA RG 428; public domain (federal work); NARA useRestriction Undetermined" to each row |
| `MANIFEST.md` | **missing** in test_v3. CLAUDE.md requires every film clip in MANIFEST.md with what it does NOT show | Med (rule fail) |
| Content ID | NARA Navy reels (428-NPC) are often **claimed by footage resellers** who uploaded the same PD reels. Keep the NARA catalog IDs ready for disputes. Music: Zabriskie says he does not claim; ASCAP is not Content ID: low | Med (process) |
| Music credit | "Stories About the World That Once Was" by Chris Zabriskie, *Music from Neptune Flux*, CC BY 4.0: correct and complete. The text includes "creativecommons.org/licenses/by/4.0/" and "chriszabriskie.com", which YouTube auto-links; STYLE_LOCK 6 says **no links in the description**. Use "licensed under Creative Commons Attribution 4.0" only | Low |
| SFX | all synthesized in-house (SFX_CREDITS.md), so no licence risk | ok (rights) / **FAIL (style rule, see §5)** |
| Depth Anything V2 | `/opt/models/depth_anything_v2_small.onnx` = Small = Apache 2.0 (Base/Large are CC BY-NC: never swap) | ok |
| Kokoro v1.0 / am_michael | Apache 2.0 | ok |
| Mapzen / AWS Terrain Tiles | on-map attribution present ("Terrain & bathymetry: Mapzen / AWS Terrain Tiles (open data)"); the Gulf sources (SRTM, ETOPO1, NOAA CRM, USGS) are PD | ok |
| YouTube altered/synthetic | AI voice, so tick **Yes** (CLAUDE.md, PLAN.md). The description should also say "Narration voice: AI-generated" (notes_battle_maps). The 2.5D depth moves on real 2006 photos do not alter events | ok if ticked |
| Inauthentic content | n/a for a test. For the long version, the fact-checked original script and the 2-3 per week cadence are the mitigation | ok |

---

## 5. Rules compliance checklist

| rule | source | result |
|---|---|---|
| -14 LUFS with a measured trim | CLAUDE.md, STYLE_LOCK 2c-9 | **PASS on the number** (-14.3 / -1.2 dBTP), **FAIL on method**: loudnorm fell back to dynamic and the 2c-9 trim never ran |
| Two-pass loudnorm, linear, LRA 11 | STYLE_LOCK 5 | **FAIL** (dynamic; LRA 2.0) |
| Music 0.08, 2 s in, 3 s out, sidechain 0.03 / 6 / 20 / 400 | STYLE_LOCK 5 | PASS (0.08; ducked 9.9 dB median). Note: 27.5 dB under the voice, inaudible |
| SFX full level, ducked lightly 0.03 / 3 / 10 / 300 | STYLE_LOCK 5 | PASS on settings (measured duck 8.1 dB median, which is not "light" at this voice level) |
| Limiter 0.5, AAC 192k | STYLE_LOCK 5 | PASS |
| Role levels explosion -4, impact -7, hit -8, jet -11, whoosh -12, tick -20 | STYLE_LOCK 3 | PASS numerically. **The numbers are meaningless here:** the kit files are normalised to -18 to -26 LUFS each, not to the battle-maps files' levels, so "-4 dB explosion" ≠ the locked loudness |
| New roles "slam" and "ship" | STYLE_LOCK 3 table | **FAIL**: not in the locked table; the checker locks them as if owner-approved |
| No synthesized sounds; real recordings for booms | STYLE_LOCK 2c-5, §7 ("Synthesized artillery booms" rejected), notes_battle_maps l.66 ("Get them from Epidemic or freesound. Don't synthesize") | **FAIL**: every sound is synthesized, including the explosion and impact booms. "Nobody has listened to them yet" (SOUND_REPORT). CLAUDE.md still lists ship SFX as "still to build" |
| Boom on the impact | STYLE_LOCK 3 | **FAIL** at 7.40 (peak +2.4 s) |
| Aircraft sound only with aircraft on screen | STYLE_LOCK 3 | **FAIL** at 22.24-23.5 (catapult rush over the island shot) |
| Whoosh only on the 2-3 biggest moves | STYLE_LOCK 3 | PASS (2) |
| ~16 SFX/min in bursts, calmer minutes | RULES 100 | PASS-ish (23.5 raw, ~16 audible) |
| Voice ~11-12 dB above the sound design | RULES 100 | marginal (10.1 dB under speech) |
| Bed never goes silent / no silence after board drops | RULES 99/100 | **FAIL** 30-40 s (sound design at -48 to -52 dBFS on the mix bus) |
| One signature sound planted and paid off | RULES 100 | **FAIL**: none (the horn would be the natural one, but it is inaudible) |
| Count-up lands with flash + ring + deep hit | RULES 98 | partial: hit present, 14 f late |
| A number lands on its spoken word | CLAUDE.md | PASS for 900, 212, 3, $20M; **FAIL for 37** (+1.0 s) |
| Cards use only words the narrator says | STYLE_LOCK 2c-7 | **FAIL**: "budgeted at under $3 million", "Preparing her to sink", "from the first charge" |
| Archive film `GRADE=none`, 4:3 fills or pillarboxes, leaders trimmed | CLAUDE.md | PASS mostly; the f13 head shows 2-3 frames of the "13" |
| Rights PD/CC0/CC BY only, no NC/ND | CLAUDE.md | PASS |
| Every file in CREDITS.md with licence | CLAUDE.md | **FAIL** (the v3 film rows have no licence column) |
| Every film clip in MANIFEST.md with what it does NOT show | CLAUDE.md | **FAIL** (no MANIFEST.md) |
| No CIV photographers | brief | PASS |
| Altered/synthetic = Yes | CLAUDE.md | PASS if ticked at upload |
| No links in description | STYLE_LOCK 6 | **FAIL** in the prepared credit text |
| First frame is a map | CLAUDE.md, STYLE_LOCK 7 | **FAIL** (SH-3 photo; for the visual critic) |
| Renders detached and resumable; commit after each step | CLAUDE.md | not assessable from the files |

---

## 6. Timestamped issue table

| time | issue | severity | concrete fix |
|---|---|---|---|
| whole | loudnorm fell back to **dynamic**: gain rides +5.6 to +12.4 dB, about 8 dB of peak limiting on the voice, LRA 2.0, no beat louder than speech | **High** | 1) Put a voice peak stage before `amix`: `acompressor=threshold=-24dB:ratio=2.5:attack=5:release=80:makeup=3dB,alimiter=limit=0.35:attack=2:release=40` on `[vo]` (stem peaks -1.7 → about -9 dBFS), so `alimiter 0.5` and loudnorm stop limiting. 2) Use the 2c-9 route as the master stage: measure I, apply `volume=(-14.2-I)dB,alimiter=limit=0.84:level=disabled`, re-measure. 3) In `mix_clip.py`, parse loudnorm's JSON and **fail the build if `normalization_type` ≠ `linear`**; add that to `check_sound_lock.py`. Target: LRA ≥ 4 LU, big-beat M ≥ +2.5 LU above the speech M median (-14.4) |
| whole | master is **mono**: the stereo music and SFX are folded down | Med | `[0:a]aresample=48000,pan=stereo\|c0=c0\|c1=c0,asplit=3...` and `aformat=channel_layouts=stereo` after `amix`. Keep the voice centred |
| 0.35-53.4 | kit hits (`number_land_*`) are 3.4-3.75 s sub booms (82-93 % below 120 Hz); 8 of them; master low end ≈ voice band | Med | cut each hit to 0.8 s with c[4]=0.8 (0.4 s fade); add `highpass=f=80,equalizer=f=160:t=q:w=1:g=-2` on the voice; high-pass the SFX bus at 35 Hz |
| 6.18 / 8.46 | Kokoro mid-sentence pauses of 0.36 s and 0.40 s inside the 13-word sentence (109 wpm phrase) | Med | split the chunk: "Navy demolition divers set off explosive charges" (gap 0.12 s) + "inside a retired American aircraft carrier." Regenerate and re-align |
| 7.40 | explosion loudest **+73 f** (9.84 s) over the 1966 steaming film; ducked about 8 dB because it falls mid-sentence on "charges" | **High** | cut `charges_seq_3` to **0.9 s** (c[4]=0.9, so it ends 8.30 with a 0.4 s fade), or use a single-blast recording whose peak is ≤ 66 ms (2 f) from the onset. Add a **0.5 s voice pause after "charges"** so the boom plays in the clear |
| 12.21-13.36 | "37" lands 1.0 s after the spoken "thirty-seven"; the counter shows "1 minutes" | Med | start a06 at 11.52 (end of "carrier.") with count dur 0.7 s → it lands at 12.22-12.49 on "thirty-seven"; start the count at 2, or use "MIN"; then move the hit to the land frame |
| 13.36 + 13.80 | two sub booms whose peaks are 12 f apart (37 hit + whoomp) | Low-Med | drop the 13.36 hit, or cut it to 0.4 s; keep the impact on the 13.80 cut |
| 14.10 | flood rush loudest **+71 f** (16.48) over the 1969 aerial; masks "feet" by +3.6 dB in the voice band | **High** | c[4]=**1.2** (ends 15.30 at the cut) with the 0.4 s fade, level -13 → -16 dB; or `flood_rush_3` (peak at 0.0 s) |
| 19.31 | redundant hit 46 ms after the seabed impact; no visual event (212 FT is already on screen); broadband +9.8 dB over "feet" | Med | **delete the cue**. If the gauge should "land", animate it to land at 19.31 first |
| 21.00 | catapult rush loudest **+58 f** (22.93) over the island "34" shot; masks "The", "her.", "Navy" by -3.6 to -6.3 dB | **High** | c[4]=**1.25** (ends 22.25 at the cut), or re-pick a recording whose rush peaks within 0.3 s; level -12 → -14 dB under speech |
| 22.30 | 2-3 frames of the S-2 "13" before the "34" | Low | f13 ss 2.3 → 2.45 s |
| 24.33-24.83 | "ON PURPOSE." fades in; the slam plays at 24.51, 5 f after the flash cut | Low | snap the text in at 24.51 (0.1 s scale 1.15 → 1.0), or move the slam to 24.33 |
| 26.0-27.5 | "Preparing her to sink" over 1952 San Diego footage | Med | swap in 2006 prep stills 6698569 / 6698553 (already credited) |
| 27.6 | "budgeted at under $3 million" is not spoken and loosely worded | Low-Med | "CONGRESS COMMITTED $2.8M" plus a spoken line, or drop it |
| 20.6-22.2 | label "USS ORISKANY · 1968" on a reel whose slates read Jan 1967 | Med | "USS ORISKANY · 1967-68", or no year |
| 29.2-40.2 | question block rushed (210-256 wpm) | Med | Kokoro speed 0.95 → **0.88** for chunks 13-16, or add 0.15 s at "sink.", "sea," and "her," |
| 30-40 | sound design floor -48 to -52 dBFS (mix bus): dead air apart from the voice | Med | let the music recover in gaps (release 400 → 800 ms is locked, so ask the owner), or add a -30 LUFS swell/underwater bed (real recording) under the board |
| 40.15 / 40.40 | strike scrapes at -42 dBFS, inaudible; the first is late by 18 f | Low | delete, or raise to -14 dB and cue on the drawn strike (40.37 / 40.83) |
| 42.62 | sonar ping inaudible (-10 to -18 dB under the voice) | Low | raise to -12 dB, or move it into the 43.86 gap (0.66 s) |
| 45.02 | SS United States horn inaudible (-12.7 dB under the voice); the natural signature sound is wasted | Med | place a real horn recording in the **43.92-44.52 voice gap** at -10 dB over the cut, peak on the 44.52 cut; or open a 0.6 s pause before "And this month" |
| 44.5 | "this month" is true only up to 11 Nov 2026 | **High (deadline)** | publish by 11 Nov, or re-voice as "On November 12th" / past tense after the sinking; re-check against OKA/USCG on publish day |
| 50.5 | "for the very same reason" right after "hidden inside her" (PCBs) | Low-Med | make sure the long video's payoff says "to become a reef" (and why reefing beats scrapping), not PCBs |
| 53.43-53.60 | audio ends 87 ms early, chopping the SFX tail at -21.6 dBFS | Med | `apad=whole_dur=53.6` on the voice before `asplit` (the sidechain stops at the shortest input); master `afade=t=out:st=53.0:d=0.6` to match the 0.6 s video fade |
| chunk ends | hard trims at -42 to -50 dBFS (stem), about -35 dBFS at master scale | Low | 5 ms fade-in / 10 ms fade-out on every Kokoro chunk in `voice.py` |
| CREDITS / MANIFEST | film rows lack licence and author; MANIFEST.md missing; unused photos listed; links in the music credit | Med | add a rights column ("US Navy film, NARA RG 428, public domain; useRestriction Undetermined"); write MANIFEST.md (clip, NARA ID, in/out, what it does NOT show); trim unused rows; remove the URLs |

---

## 7. Top 5 fixes (ranked)

1. **Fix the master stage.** Loudnorm went dynamic, so the master has about 8 dB of limiting on the voice, LRA 2.0, and an explosion that is no louder than a sentence.
   - Peak-control the voice before the mix (compressor 2.5:1 at -24 dB plus a limiter at -9 dBFS).
   - Do the final -14 with the 2c-9 gain + `alimiter=0.84`.
   - Fail the build unless loudnorm reports `linear`.
   - While there: output stereo, `apad` the voice to the video length, and add a 0.6 s master fade-out.
2. **Re-sync the long SFX so their loudest frame is on the picture.**
   - Explosion: cut to 0.9 s, plus a 0.5 s voice pause after "charges".
   - Flood rush: 1.2 s.
   - Catapult: 1.25 s.
   - Delete the 19.31 hit.
   - Land the 37 on "thirty-seven" (a06 at 11.52, count 0.7 s).
   - Today three sounds peak 58-73 frames late, over the wrong film, and mask "feet" and "Navy".
3. **Replace the synthesized kit with real recordings for the beats that matter**: charges, hull hitting the water, catapult, liner horn. STYLE_LOCK §7 and 2c-5 and notes_battle_maps l.66 all reject synthesized booms, and nobody has listened to this kit.
   - The Epidemic Sound subscription is active (no new spend); freesound CC0/CC BY is the fallback.
   - Re-level by ear, because kit files at -18 LUFS make the "locked" dB numbers meaningless.
   - Make the horn audible as the signature (in the 43.92-44.52 gap).
   - Get owner approval before re-locking the md5s and before adding the "slam" and "ship" roles.
4. **Correct the on-screen claims.**
   - "USS ORISKANY · 1968" → "1967-68".
   - "Preparing her to sink" must sit over 2006 stills, not 1952 film.
   - "budgeted at under $3 million" → spoken "Congress committed $2.8 million", or drop it.
   - Counter: no "1 minutes".
   - Lock the publish date to ≤ 11 Nov 2026, or re-voice "this month".
5. **Voice pacing and credits hygiene.**
   - Split the 13-word sentence to kill the 0.36 s and 0.40 s mid-phrase pauses.
   - Slow chunks 13-16 to speed 0.88 (now 210-256 wpm).
   - Add 5-10 ms fades on the chunk edges.
   - Add a rights column to the v3 film credits.
   - Create MANIFEST.md.
   - Drop the URLs from the music credit.
   - Run a Kokoro test of "Oriskany" and "Pensacola" before the full script.
