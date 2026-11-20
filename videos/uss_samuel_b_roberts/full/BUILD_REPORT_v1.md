# USS Samuel B. Roberts full video: build report v1 (2026-11-20)

**Output:** `videos/uss_samuel_b_roberts/full/uss_samuel_b_roberts_full_v1.mp4` (git-ignored). H.264 1920x1080, 30 fps, AAC stereo 48 kHz,
**924.5 s (15:24)** = narration 906.5 s + 18 s end screen. 720p preview: `uss_samuel_b_roberts_preview_720p.mp4` (git-ignored).
Video #5 of Fleet's End, built in the locked style (STYLE_LOCK.md incl. the USS Nevada owner rules) with the USS Ranger scripts copied and adapted.
**Approvals:** given by the owner directly on 2026-11-19 (`OWNER_NOTES.md`): every gate pre-approved, vidIQ up to ~400 credits for titles +
thumbnails, Gofile upload of master + upload kit PDF + thumbnails. No other spend.

## 1. Research (`research/`)
- No Gemini key: dossier by a research agent (`RESEARCH.md`, `FACT_SHEET.md`), then three independent fact-checks:
  `FACTCHECK_A_ship_crew_honors.md`, `FACTCHECK_B_samar_battle.md`, `FACTCHECK_C_discovery_record.md`. history.navy.mil, navy.mil and USNI
  were unreachable (503/403) all session; DANFS read via the HyperWar mirror.
- **Primary source found by the footage agent:** Lt Cdr Copeland's *Combined Action Report ... and Report of Loss of USS Samuel B. Roberts*
  (20 Nov 1944, NARA, 23 pages, `footage/src/photos/nara_78682556_p01..p23`). Read for the script: torpedo attack from 4,000 yd, 3 torpedoes
  ("getting one hit": the crew's claim), **608 rounds** of 5-inch, first hit **08:51**, ~20 hits from 5-, 8- and 14-inch shells by 09:07,
  sank **10:05 "stern down, bow up"**, ~50 hours in the water, his words to the crew (p.14: "a fight against overwhelming odds from which survival
  could not be expected, during which time we would do what damage we could") and his crew ("newly inducted, married, unaccustomed to navy ways
  and with an average of less than one year's service").
- Corrections that changed the script: depth **6,895 m first announced, 6,865 m after Guinness recalibration** (said as "almost six thousand nine
  hundred metres / almost twenty-three thousand feet"); **"Parry Shen" does not exist** (the historian is Parks Stephenson); **Paul Carr got the
  Silver Star, not the Medal of Honor** (the script quotes the citation: "tried, unassisted, to load and ram the last projectile"); the wreck is in
  **two pieces**, not three; **hull number 413 visible: unverified, cut**; "Philippine Trench" as the wreck's location unverified (said "off
  Samar"); the **Chokai torpedo hit is contested** (crew + 1944 Navy said yes; Japanese records do not back it) = the mid-video reversal; Kongo,
  not Yamato, sank her; Kurita turned at ~09:20; ~90 killed of ~220 (89/90 conflict); rescue date (26/27 Oct) not said; "the destroyer escort
  that fought like a battleship" has no traceable source (not used); "deepest shipwreck ever found" is true per Guinness ("deepest shipwreck
  found to date"), no deeper wreck found 2022-Nov 2026 (re-check before publishing).

## 2. Script and voice
- `script/NARRATION_v1.txt` (2,365 words), 8 chapters: Hook 0:00 · Taffy Three 0:53 · The Little Ship 2:40 · The Torpedo Run 4:17 · The Duel 5:53 ·
  Fifty Hours 9:03 · The Search 10:29 · Found 13:18.
- Line 1 = the stakes ("Almost twenty-three thousand feet under the Philippine Sea, there is a small American warship that once charged a fleet of
  battleships"), title promise "the deepest shipwreck ever found" at ~9 s, first frame a map, no résumé before 2:40 (the ship's build is the
  "why her?" flashback), reversal at 5:53 ("Did it hit?") plus the second turn (Kurita turns away), answer held to the last act (13:18: what the
  cameras saw), closing question (keep searching for Taffy 3's last ships, or leave them in the dark), ending 31 s after the answer section's last fact.
- Archive voice (bm_fable 0.40 + am_michael 0.40 + bm_lewis 0.20, speed 0.92). Pronunciation gate `full/build/PRONUNCIATION_GATE.md`: Samar,
  Leyte, coxswain, Checotah, Morizet, Kurita, Chokai, Takeo, Gambier, Guadalcanal fixed. Names clip: `voice_sample/names_sbr.mp3` (36 names).

## 3. Footage and rights (`footage/`, `full/CREDITS.md`, `full/MANIFEST.md`)
- 180 stills + 44 films (NARA Navy reels RG 428, Commons copies of NARA/NHHC 80-G / NH photos with PD markers, NARA USAAF photos, NOAA Ocean
  Exploration video and stills). Rights read per item and quoted in `footage/FOOTAGE_LIST.md`.
- **No photo or film of the Samuel B. Roberts in action exists**: battle shots are other Taffy 3 ships (named: St. Lo, Gambier Bay, Heermann,
  White Plains, Fanshaw Bay, Kitkun Bay) or ILLUSTRATIVE. The Roberts herself: NH 96011 (Oct 1944), NH 90603 (1944), her launch (Jan 1944), her
  Sept 1944 war diary, Copeland's report. **The 2022 wreck images (Caladan Oceanic) are not shown**; deep-sea NOAA video is labelled ILLUSTRATIVE.
- Film checks: scene cuts (`build/film_cuts.py`), white-outs/blank spans (`build/film_bad.py`, new: fast 2 fps scan, spans cut like cuts),
  NOAA burned-in captions (caption-free windows in `build/noaa_clean.json`), NARA burned-in timecode cropped (`make_segments.py`: crop
  700:380:10:22 on the 480i reels). Window sheet of every used window (`build/WINDOW_SHEET.jpg`, `build/window_sheet_used.py`, new) and a sheet of
  every built film segment (`build/SEG_SHEET_film.jpg`) looked at: a "HEADS" slate, two blank-white windows, a white-out, a crowd shot under
  "sent his small ships", and two over-cropped 720p octopus clips were removed.

## 4. Picture
- 250 shots, **0 over 6 s** (end screen excepted), clip/photo reuse clean (2 max, 3+ min apart: `build/shotlist_report.md`), 37 numbers each on
  its spoken word (`build/check_numbers.py`). Hook: maps, 1920-3840 px stills and 1080p NOAA video only; a cut every ~3 s.
- Photo moves aim at the subject (`build/focus.py`, crosshair sheet `build/FOCUS_SHEET.jpg` looked at).
- 22 map scenes (map agent; `mk/MAPS_SHEET.jpg`) on new deep-ocean basemaps (`bake_sea.py DEEP=1`: wpac, leyte, samar, trench; + gulf_houston,
  solomons, persian). All battle and wreck positions labelled APPROX.
- Gauges: depth bars (Titanic / Johnston / Roberts), pressure meter (~700x), depth meter (6,900 m).
- Cards: a brightness audit of every card background (luma of the built background) replaced about 25 dark backgrounds with bright photos (some after a first render) before the
  final renders.

## 5. Sound
- 30 Epidemic SFX re-downloaded (md5 30/30). Beds: projector under NARA film, underwater under NOAA video and every gauge; no horn, no hull-groan
  / sinking cues. Music (Zabriskie, Neptune Flux, CC BY 4.0): 01 (hook-c03) -> 03 (torpedo run) -> 04 (the duel / reversal) -> 02 (survivors)
  -> 01 from 200 s (the search) -> 09 (from the answer).

## 6-8. Checks, packaging, final master
(filled in below after the final mix)
