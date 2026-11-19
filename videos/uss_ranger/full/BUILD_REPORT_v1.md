# USS Ranger full video: build report v1 (2026-11-19)

**Output:** `videos/uss_ranger/full/uss_ranger_full_v1.mp4` (git-ignored). H.264 1920x1080, 30 fps, AAC stereo 48 kHz, **851.3 s (14:11)**
= narration 833.3 s + 18 s end screen. 720p preview: `uss_ranger_preview_720p.mp4` (git-ignored). Video #4 of Fleet's End, built in the
locked style (STYLE_LOCK.md incl. the USS Nevada owner rules) with the USS Nevada scripts copied and adapted.
**Approvals:** the owner's pre-approval of every gate reached this session only as a relay from another session (HANDOVER.md, "Video 4").
The build went past the hook and shot-list gates (reversible work). The two outward actions were **not** taken: no vidIQ credits spent,
no Gofile upload. Both are one step once the owner says yes (section 9).

## 1. Research (`research/`)
- No Gemini key: dossier by a research agent: `RESEARCH.md`, `FACT_SHEET.md` (103 rows). Three independent fact-checks:
  `FACTCHECK_A_ship_service_films.md`, `FACTCHECK_B_disposal_penny.md`, `FACTCHECK_C_tow_scrap.md`. NHHC/NAVSEA/NVR/defense.gov were
  unreachable (503/403) all session: the Navy texts were read through verbatim reprints (Navy Times, Marine Log, MarineLink, DVIDS captions).
- Corrections that changed the story: the one-cent contract was **22 Dec 2014** (not 2017); tow **5 Mar - 12 Jul 2015**; scrapping done
  **1 Nov 2017**. **Top Gun's main carrier was USS Enterprise**: Ranger "was one of them" (never "the Top Gun carrier").
  **Not a sale:** NAVSEA: "This is not a sales contract, it is a procurement contract" = the mid-video reversal ("the Ranger was never sold").
  Constellation cost the Navy $3M (not a cent); Forrestal, Saratoga, Kitty Hawk, JFK one cent. Donation hold ended **Sep 2012**. Navy counted
  **$105,000** raised vs ~$31.85M (the Foundation said $600,000+: both said). Ocean tow by **Crosby Tugs** (Crosby Leader), harbour tugs Foss.
  Route said only as "around the southern tip" (Cape Horn vs Magellan unverified). The 1983 fire started at **9:50 a.m.** (UPI) and the yard's
  2017 moment of silence was at 9:50 (EMR): the closing beat.
- Not said (unverified): Ranger's exact Top Gun scenes, bell/anchor location, scrap value, the river-bridge position (map says APPROX.),
  "first/only" claims (angled deck, only West Coast carrier in Desert Storm), 13 battle stars.

## 2. Script and voice
- `script/NARRATION_v1.txt` (2,247 words), 8 chapters: Hook 0:00 · One Cent 0:39 · Hollywood's Carrier 1:56 · Thirty-Six Years 3:26 ·
  The Museum That Never Was 6:13 · The Penny 8:27 · The Last Voyage 10:25 · What's Left 11:49.
- Line 1 = the stakes ("...let go of an aircraft carrier for one cent"), title promise "sold for a penny" at 8.4 s, first frame a map,
  no résumé before 3:26 (films first, as the "why her?" flashback), reversal at 8:27, answer held to the last act (cut up in Brownsville;
  the last section out 34 years to the day after the fire), closing question, ending 35 s after the answer.
- Archive voice (bm_fable 0.40 + am_michael 0.40 + bm_lewis 0.20, speed 0.92). Pronunciation gate: 21 whisper diffs, all homophones /
  number formats except "wore" (heard "war": reworded). Names clip: `voice_sample/names_ranger.mp3` (34 names).

## 3. Footage and rights (`footage/`, `full/CREDITS.md`, `full/MANIFEST.md`)
- 212 stills + 44 films (NARA DoD/DVIC and Navy stills, NARA RG 428 reels, DVIDS). Rights read per item. NARA RG 428 reels = "Undetermined"
  (Navy film, same basis as Nevada). No Top Gun / Star Trek / Flight of the Intruder imagery. Non-Ranger items labelled on screen
  (ILLUSTRATIVE or the ship's name).
- Reality: **no public-domain HD film of Ranger in service** (all NARA film is 480i); the only HD Ranger film is the DVIDS 2015 tow video.
  No Brownsville arrival or scrapping imagery exists in PD sources: stand-ins are labelled (ex-JFK 2025, 1990 Bremerton layup, 1969 yard welding).
  Wikimedia Commons was rate-limited (it holds a 6622 px Ranger tow photo): see `footage/OWNER_DOWNLOADS.md`.

## 4. Picture
- 229 shots, **0 over 6 s** (end screen excepted), clip/photo reuse clean (2 max, 3+ min apart), 31 numbers each on its spoken word
  (`build/check_numbers.py`). Hook: only the 1080p tow video, 3000 px stills and maps; a cut every ~2.3 s.
- Photo moves aim at the subject (`build/focus.py`, 3 manual fixes; crosshair sheet looked at). Film windows split at detected cuts
  (`build/film_cuts.py`, new) and frame-checked on one sheet (`build/window_sheet.py`, new): a slate (A-7 reel), an "End of Recording" card,
  a TV presenter (Forrestal clip) and two missed cuts were trimmed. Modern DVIDS video keeps its colour (`make_segments.py`: grade none).
- 31 map scenes (map agent; `mk/MAPS_SHEET.jpg`); Hampton Roads basemap re-baked without the broken OSM water mask.
- Cards: after the first master the contact sheet showed dim cards: all 23 number cards switched to the light shade, 7 dark backgrounds
  replaced by bright photos; re-rendered.

## 5. Sound
- 30 Epidemic SFX re-downloaded (md5 30/30). Projector bed only under old NARA film, water bed under the 2015 DVIDS video; no horn,
  no hull-groan/sinking cues. Music (Zabriskie, Neptune Flux, CC BY 4.0): 01 -> 03 (c04 service/fire) -> 01 (c05) -> 04 (c06 reversal)
  -> 02 (c07 tow) -> 09 (from the answer).

## 6. Checks (master v1, first build; re-run on the final build in section 8)
| check | result |
|---|---|
| `check_sound_lock.py` static + render | **SOUND LOCK OK**: -14.0 LUFS, TP -1.9 dBTP, LRA 2.3 LU, music under speech -24.8 dB, 98 cues within 3 frames |
| safe-text (every chapter, 0.5 s) | **PASS** c01-c08 |
| shots over 6 s / numbers on words | 0 / 31 of 31 |
| blackdetect 0.25 s / 0.06 | **0** |
| contact sheet `FINAL_SHEET_v1.jpg` | looked at: dim cards found and fixed (section 4) |

## 7. Packaging
- Thumbnails (`thumbnails/`, critique `CRITIQUE_1.md`): V3 "ONE CENT" (main), V1 "1¢" split, V2 "FOR 1¢". "SOLD FOR 1¢" not used (not a sale).
- Titles: `script/TITLES_THUMBS.md` (unscored). Recommended: "Why the Navy Paid One Cent to Scrap a Top Gun Carrier".
- Description, tags, pinned comment: `full/YOUTUBE_DESCRIPTION_DRAFT.md`; upload kit `full/upload_kit/` (HTML + PDF).

## 8. Final master
(filled after the card re-render: see the end of this file)

## 9. Open items for the owner
1. Say yes/no to the **vidIQ title scoring** (~40 credits) and the **Gofile upload** (master + kit PDF + thumbnails): not done without your direct OK.
2. Title choice: your working title overclaims twice (main Top Gun carrier was Enterprise; the Navy says it was no sale).
3. Watch the master; listen to `voice_sample/names_ranger.mp3`.
4. Space the upload from USS Nevada (2-3 a week max).
