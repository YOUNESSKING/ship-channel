# Oriskany full video: build report (step 3)

**Output:** `videos/oriskany/full/oriskany_full_v1.mp4` (git-ignored, 1.05 GB). H.264 1920x1080, 30 fps, 26,544 frames;
AAC stereo 48 kHz. **Duration 884.8 s (14:44.8)** = 866.8 s narration + 18 s end screen. Audio length = video length.

## What changed in step 3

| item | what was done |
|---|---|
| Wikimedia fallbacks | The three photos are not in `footage/src/photos/`, so c07 s02 / s09 / s12 use `h_c07_wreck2008`, `h_c07_depths_c` and `h_c07_divers`. Switch: `build/make_shotlists.py` (`WIKI`): drop the .jpg in and re-run `make_shotlists.py` + `make_segments.py` + the c07 render; `WIKI_FALLBACK=0/1` forces either side. |
| Sale price (a) | GAO95: high bid "over $1.2 million"; narration says "just over a million dollars". The stamp in `h_c02_ledger_b` now reads **OVER $1 MILLION** (true and matches the words). Voice unchanged. |
| c05 hero a (b) | The old shot showed the carrier still afloat and sinking under "She settled upright on the bottom". It is now a plan view of the wreck **at rest on the sand**, seen from above: compass N up, "UPRIGHT ON THE SEABED" on "upright", arrow to the bow + "BOW → DUE SOUTH" on "south". Hero b (side view) is unchanged: **touchdown stays on "twelve"** (544.27 s). |
| Hook (owner) | c01 picture = the approved **test v4 picture**, first 1459 of its 1506 frames (0-48.625 s), not this build's re-render. |
| Cards | Clipless line / number cards sat empty for up to 3.9 s before their word (blackdetect on c03). Added `kicker_at` (kicker shows first, number/text still lands on its word). |
| Safe area | `templates/lib/safe_area.js` lifts lower thirds 12 px more so their drop-in entry also stays out of the bottom 10 %. `check_safe_text.js`: **PASS on all 7 chapters** (`chapter/safe_c0*.txt`). |
| Render script | `build/render_all.sh` (detached, resumable: stamp per chapter, `.part` files, cache cleared before each render, one retry). c07 failed twice with a **full disk** (the HyperFrames extract cache had grown to 4 GB). Fixed by clearing caches. |

## Hook timing (owner change 1)

- Voice: the full narration and the test v4 hook are the same recording. Word times match to within 1 ms over the hook.
- Picture: the test v4 render is 1506 frames (50.2 s). The join keeps frames 0-1458, so the cut into c02 lands at 48.633 s.
  That is frame 1459 = round(48.625 × 30), so there is no offset. The cut falls in the end map (shot s21, which starts at 45.80 s) and
  goes into the c02 aerial film. The test v4 0.6 s fade-out at 50.2 s is not used.
  This build's own c01 re-render matched the test v4 picture frame for frame. 73 of 1459 frames fall below 30 dB PSNR,
  from small text-position and render-noise differences.
- Sound: the hook cues are rebuilt with **identical cue times, files and levels** (`build/sfx_placed.json` vs
  `test_v4/build/sfx_placed.json`, 16 cues). There are two differences:
  1. The horn is **-14 dB, not -10**. This is the owner's locked change: the test v4 master on disk predates it.
  2. The end-map whoosh is trimmed at the chapter cut. It now ends at 48.745 s instead of 48.86 s.

  Beds are the same, with the waves under the end map ending at 48.625 s.
  The hook music bed is at the same level: -18.7 LUFS over 0-48.6 s in both `music_bed.wav` files.
- Hook loudness in the full master: -13.2 LUFS and LRA 3.4 LU over 0-48.6 s. Test v4 measured -13.9 LUFS and 5.7 LU.
  The reason is that the master gain is now set once for the whole 14:45 video, not for the hook alone.

## Loudness and sound (tools/sound v2 chain, `build/mix_full.py`)

| measure | full v1 | test v4 | target |
|---|---|---|---|
| integrated | **-14.0 LUFS** | -13.9 | -14 ± 0.5 |
| true peak | **-1.6 dBTP** | -1.5 | ≤ -1.5 |
| loudnorm | two-pass, **linear** (master limiter 0.78, gain +14.5 dB) | linear | linear |
| LRA | **2.4 LU** | 5.8 | ≥ 5 (**FAILS**, see leftovers) |
| **music under voice** | **-24.1 dB** re voice | **-22.0 dB** | -18..-28 |
| music in gaps (blind estimate) | -19.6 dB re speech (battle-maps refs -17.3; delta -2.3) | -18.1 (delta -0.8) | within 3 dB |
| big beats over speech | 9 / 9 ≥ +3 LU | 6 / 6 | ≥ +3 LU |
| SFX sync | max 1.1 frames off its event; 0 over 3 | — | ≤ 3 frames |

- **Music level (owner change 2):** the chain is unchanged and still checked by the lock: MUSIC_VOL 0.08, MUSIC_TRIM_DB -6,
  sidechain-ducked under the voice. Music under voice is **2.1 dB quieter** than test v4, not louder, so I made no change.
  The loud preview the owner heard was the coordinator's rough mix, with the music at 0.6.
- Music: Chris Zabriskie, *Music from Neptune Flux* (CC BY 4.0), with 5 s crossfades (`build/music_bed.json`):
  - "Stories About the World That Once Was" from 0 to 565.9 s, crossfading back into itself at 405 s;
  - "Your Mother's Daughter" from c06 (565.9 s) to 806.3 s;
  - "I Should Have Been More Human" for the last 60 s of narration plus the end screen.

  The album files were identified by length: 01 / 03 / 09.
- SFX: 197 cues (13.4/min) on one timeline (`build/sfx_full.py`). The roles and levels are the locked ones, with the horn at -14.
  66 event cues were moved onto the frame of their picture beat from `anim_beats.json`, so the offset is 0 frames by construction.
  The list is in `build/SFX_RETIME.md`. Six cues were dropped:
  - the c05 hero-a groan, because that shot no longer shows a sinking;
  - five option ticks that fell inside the 0.12 s minimum gap.
- Beds: 81 segments. The projector loop plays **only under NARA film**. Waves play under sea maps, tows and storms. Underwater plays
  under the sinking and the reef scenes. Drone plays under the PCB gauges and the x-rays.
- `check_sound_lock.py`: the static lock is **OK**. In the render checks, everything passes **except LRA**.

## Picture: film share per chapter (seconds on screen, from `build/shotlist_report.md`)

| chapter | NARA film % | generic US-Gov film % | photos % | maps % | hero % | anim + cards % | moving video % |
|---|---|---|---|---|---|---|---|
| c01 Hook (test v4) | 24 | 0 | 36 | 40 (maps + animation) | | | 24 |
| c02 Nobody Wanted Her | 5 | 15 | 15 | 34 | 13 | 18 | 27 |
| c03 The Mighty O | 50 | 0 | 10 | 25 | 0 | 14 | 50 |
| c04 The Bargain | 0 | 5 | 9 | 28 | 9 | 49 | 5 |
| c05 Thirty-Seven Minutes | 0 | 0 | 64 | 12 | 8 | 15 | 0 |
| c06 The Fish Test | 0 | 15 | 11 | 15 | 41 | 17 | 15 |
| c07 The Real Reason | 7 | 14 | 12 | 14 | 23 | 29 | 31 |

Longest shot: 5.93 s, ignoring the end screen. Every shot outside the hook is at least 1.24 s long. The two c05 shots under 1.5 s are the
"they fired" blast and "Then she was gone": deliberate punches.

## Checks run on the final file

- `tools/film/check_clips.py --no-cuts oriskany_full_v1.mp4` exits 1 with 104 flags (`build/check_clips_final.txt`). I checked them by eye:
  - **96 BLOB flags**: dark graphics (gauges, x-rays, cross-sections, the end map) in c07 and similar scenes. These are drawn dark
    backgrounds, not film obstructions.
  - **8 FLASH flags**:
    - 4.30, 17.67 and 526.3 s are the intentional blast flashes (hook ×2, c05 "they fired");
    - 211.5, 238.9, 317.3, 355.9 and 788.1 s are hard cuts between a bright shot and a dark one (map/film, gauge/film). I looked
      at the frames on both sides: there are no burns.
- Black frames (`build/blackdetect_final.txt`, 8 spans of 1.2-4.1 s): all are the dark text cards (for example "3 bids", "67 jobs", "½+").
  The kicker or number is on screen in every one, and there are **no true black frames**. Since step 3 the cards with the longest leads
  show their kicker first: PRESS, SINKING DAY / FLORIDA SENATE (3.4 s), A PROTEST (3.9 s), RELEASED · MARCH 1973 (3.4 s).
- Contact sheet: `full/FINAL_SHEET.jpg`, one frame every 10 s (89 frames). I looked at it and at per-chapter sheets every 4 s, and found:
  - no wrong-era film in the wrong place;
  - every generic clip carries its ILLUSTRATIVE tag;
  - the new c05 plan view and the "OVER $1 MILLION" stamp are correct.
- Captions vs narration: every number and label is anchored to its spoken word by the builder (`@word`). The builder stops the
  build if the word is missing. I checked by eye that these values appear on screen, from the sheets: $1M (fixed), 212 FT (lands on
  "twelve"), $3.7 million, ≈ $20 / ≈ $21, NOV 12, 13 nautical miles, 254 fish and 8 rounds. I have not done a full
  caption-by-caption read against the script.
- `check_safe_text.js`: PASS on c01-c07.
- Paperwork, regenerated for the final cut (`build/paperwork.py`):
  - `MANIFEST.md`: 67 film rows. Hook rows come from test v4, with what each clip does not show.
  - `CREDITS.md`: 97 items, plus the music (3 × CC BY 4.0), the map data and the illustrative note.
    - Map data: Mapzen / AWS Terrain Tiles open data, and US Census boundaries, which are public domain.
    - The illustrative note covers the tow routes, Yankee Station, the 1952 fight position and the rubble-reef direction.
  - `YOUTUBE_DESCRIPTION_DRAFT.md`: chapter timestamps, the credits block and the "altered or synthetic content: Yes" note.

## Known leftovers

1. **LRA 2.4 LU < 5: `check_sound_lock.py` fails on this one check.**
   - The ≥ 5 LU rule was set on the 50 s hook test.
   - A 15-minute narrated master on the locked chain (voice compressor 2.5:1, limiter, fixed bed and music levels) comes out at
     2.4 LU. The three battle-maps reference videos the lock uses measure 2.2-2.5 LU.
   - Raising it would mean changing locked levels or dynamics, which is an owner decision. I did not do it.
2. The hook in the full master is 0.7 LU louder than the test v4 master, and its LRA is 3.4 instead of 5.7, because of the
   whole-video master gain. The horn plays at -14 dB as the owner approved, not the -10 dB of the test v4 file.
3. Generic b-roll under the "254 fish" card in c06: the card's dark shade makes the ILLUSTRATIVE tag hard to read.
4. Short shots: c05 has two punches of 1.24 s and 1.39 s. The approved hook has its own short shots: 0.33 s and 0.7 s.
5. The Wikimedia photos are still owner downloads. The fallbacks are in the cut, and their CC BY-SA credits must be added if
   the photos are swapped back in.
6. Disk: the container has about 1.7 GB free. The HyperFrames history cache, the per-scene map render copies and the chapter work
   folders were deleted; all of them can be rebuilt. Each chapter render and the mix need about 1 GB and 3 GB of temp space.
7. Not done here, per CLAUDE.md gates: vidIQ title scoring and Test & Compare thumbnails (they cost credits).
