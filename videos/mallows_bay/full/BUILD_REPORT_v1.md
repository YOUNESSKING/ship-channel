# Mallows Bay full video: build report v1 (2026-11-15, overnight build)

**Output:** `videos/mallows_bay/full/mallows_bay_full_v1.mp4` (git-ignored). H.264 1920x1080, 30 fps, 25,680 frames, **856.0 s (14:16)**,
AAC stereo 48 kHz 192k. Narration 838.0 s + 18 s end screen. 720p preview: `mallows_bay_preview_720p.mp4` (git-ignored).
Video #2 of Fleet's End, built in the locked Oriskany v8 style (STYLE_LOCK.md), with the Oriskany v8 scripts copied and adapted.

The owner approved everything up front for this build ("I approve everything from now", 2026-11-15) and went to sleep, so the
hook and shot-list gates were not stopped at. **No money was spent**: vidIQ title scoring was skipped (credits); see section 7.

## 1. Research (`research/`)
- No Gemini key in the container, so the dossier was written from official sources by a research agent: `RESEARCH.md`, `FACT_SHEET.md`
  (National Register nomination 2015, 84 FR 32586 + FEIS 2019, NOAA, MD DNR, Chronicling America, Shipping Board reports).
- Three independent fact-checks: `FACTCHECK_A_program.md` (1917-22 program; Shipping Board annual reports), `FACTCHECK_B_salvage.md`
  (1922-1970; period newspapers, the 1936 court ruling, the full 1970 House hearing), `FACTCHECK_C_today.md` (location, counts, sanctuary).
- Corrections that changed the script: sale = **$750,000 for 233 ships (12 Sept 1922 auction)**, ~$3,200 a ship (not $862,000 / $3,300);
  92 ships delivered by 31 Oct 1918; Widewater fire April 1923 = 5 ships destroyed; the Aberdeen burned there, was raised and burned
  again; PEPCO story told as the 1970 sworn testimony shows ("a dummy corporation"; oil-fired plant; PEPCO denied any part in the
  removal push; the cheap stone-pinning fix was refused by the landowner; Congress 1968 removal conditional on Maryland paying half,
  Maryland would not); rats attributed to "one reporter"; "hundreds of Marines turned out" cut (unverified) and replaced by the
  verified Quantico sentries' "red ball of the sun"; brothels/stills told as a legend with the survey author's "no evidence".
- **Title truth:** the bay is 32.0 mi from the White House in a straight line (43 mi by road). The hook says "about thirty miles";
  c02 says "thirty-two miles, as the crow flies".

## 2. Script and voice
- `script/NARRATION_v1.txt` (2,232 words), 8 chapters: Hook 0:00 · The Ghost Fleet 0:52 · A Fleet of Wood 1:36 · Too Late 3:28 ·
  Sold for Scrap 5:08 · The Great Burn 7:11 · One More War 9:00 · Why They Stayed 11:29.
- Line 1 = the stakes ("Right now, about thirty miles from the White House, more than a hundred ships are rotting..."), title promise
  spoken by 6 s, answer held to c08 ("So that is the answer" at 12:45), mid-video reversals (Bethlehem's WWII salvage fails; the PEPCO
  twist), closing question, **ending 40 s** after the answer (first draft was 89 s: the sanctuary/kayak lines were moved before it).
- Voice: Archive blend, speed 0.92 (`full/build/voice.py`). Pronunciation gate (`build/PRONUNCIATION_GATE.md`): fixed "bass" (said
  "base") and "largemouth"; Accomac = AK-uh-mak. Names clip: `voice_sample/names_mallows.mp3` (24 s) **for the owner's ear**.
- 10 voice chunks had Kokoro clicks (single-sample jumps up to 1.0) that made the AAC encode overshoot (+1.0 dBTP at 9:44, "It did
  not work."); de-clicked in the chunk cache (25-sample linear bridge on each jump > 0.9), timing unchanged.

## 3. Footage and rights (`footage/FOOTAGE_LIST.md`, `full/CREDITS.md`, `full/MANIFEST.md`)
- 108 stills + 10 films found by an agent; rights read on every record (NARA "Unrestricted", LoC "No known restrictions",
  Chronicling America, NOAA staff photos, USGS/NAIP). Everything on screen is PD / no known restrictions (US federal or pre-1931).
- **No film of the 1925 burn exists** (NARA's own note on 111-H-1166): the burn is told with the five Signal Corps aerials
  111-SC-94283..87 and the Evening Star pages.
- Caught: `aerial_mallows_1936_a` is Little Falls 1933, not Mallows Bay: not used. The real 8 Apr 1936 aerial (18-AA-70-44) is.
- Film windows: every reel's shot windows were re-cut by frame classification + scene detection (the agent's windows were up to a few
  seconds off; Bridge of Ships is 60 fps); three internal cuts found by `check_clips.py` were fixed (Hog Island crowd, torch reel).
- Every film shot carries a top-left tag; steel-yard / Ford / non-wooden shots are tagged ILLUSTRATIVE.
- Modern "today" pictures: 7 NOAA staff photos + crops of USGS/NAIP orthophotos (graded for contrast). Because there are few of them,
  some shots are **different crops of the same NOAA photo** (`*_L` / `*_R`, three shots in c08): a judgement call, flagged here.
- **Owner check:** the Ford-collection films (Hog Island 1917, scrapping 1926-27, Washington 1921) are marked "Restricted - Possibly"
  in NARA's field; all are pre-1931 and should be US public domain by age.

## 4. Picture
- 41 map scenes (`full/mk/scenes-src/`, sea-floor basemaps baked from AWS Terrain Tiles: potomac, baycl, dcwide, chesa, usa, atlantic);
  every date and place is a map. Sanctuary outline and hull shapes are approximate ("BOUNDARY APPROXIMATE" on screen).
- 247 shots, **none over 6 s** except the end-screen map (closing question + 18 s hold, as Oriskany). No reuse violations
  (`build/shotlist_report.md`). Cards sit on dimmed moving backgrounds (film, photo pushes or pushed map stills).
- Animation blocks over film now use `show: 0.8` (the first hook render showed the options block nearly black).
- Checks: safe-text **PASS** in all 8 chapters; blackdetect **0**; `check_clips.py` on every film segment: 0 internal cuts after the fix,
  BLOB flags = dark archive scenes (board room, sawmill, U-boat interiors), the same pattern as Oriskany v8;
  contact sheet `FINAL_SHEET_v1.jpg` looked at: every frame is the intended shot.

## 5. Sound
- 30 locked Epidemic SFX re-downloaded (md5 match), Zabriskie Neptune Flux tracks 01/02/03/09; `build/sfx_full.py` (rewritten for this
  video: no horn, whooshes only on chapter-opening map moves), `build/music_bed.py` (main -> hopeful (sale) -> tension (burn) -> main ->
  outro from the answer).
- See section 8 for the final lock numbers.

## 6. Packaging (`full/YOUTUBE_DESCRIPTION_DRAFT.md`, `full/upload_kit/`, `thumbnails/`)
- Thumbnails (real photos, Anton white + one red word, checked at sidebar size): T1 GHOST FLEET (1936 aerial), T2 GHOST FLEET (NOAA
  kayaker among the hulls), T3 SET ON FIRE (1925 burn aerial).
- Description with chapters, credits, sources; upload kit HTML + PDF.

## 7. Open items for the owner
1. **Titles:** not scored in vidIQ (costs credits). Rule: 3 titles >= 85 before publishing. Ask to spend.
2. Listen to `voice_sample/names_mallows.mp3` (Nanjemoy, Accomac, Idamont, PEPCO...).
3. Owner rights check on the Ford-collection films (section 3).
4. Space the upload from Oriskany (2-3 a week max, different cluster: OK).

## 8. Final checks (master `mallows_bay_full_v1.mp4`, 14:16)
| check | result |
|---|---|
| `check_sound_lock.py` static + render | **SOUND LOCK OK**: -14.0 LUFS, TP -1.9 dBTP, LRA 2.2 LU (floor 1.7), linear loudnorm, music under speech -24.4 dB, 3 big beats >= +1 LU, 100 cues within 3 frames, every cue silent by its shot end, 54 beds on cuts |
| safe-text (every chapter, 0.5 s) | **PASS** c01-c08 (`chapter/safe_c0*.txt`) |
| blackdetect 0.25 s / 0.06 | **0** |
| film segments, `tools/film/check_clips.py` | 0 internal cuts; BLOB = dark archive scenes (`build/check_clips_segments.txt`) |
| shots over 6 s | 0 (end-screen map excepted) · clip reuse clean |
| contact sheet | `FINAL_SHEET_v1.jpg` looked at |

## 9. Update v2 (2026-11-15, owner notes: "hook more engaging, high quality footage"; "don't reuse the same photos, 2 times tops")
- **Hook v2** (`script/NARRATION_v2.txt`): tighter, faster lines, then/now wipe (1936 aerial -> today), 50.7 s. Whole video now **854.0 s (14:14)**;
  chapters 0:00 · 0:50 · 1:34 · 3:26 · 5:06 · 7:09 · 8:58 · 11:27 (description updated).
- **HQ modern footage:** public-domain video of the bay today: DVIDS (US DoD, Mallows Bay, Oct 2015) and NOAA Office of National Marine
  Sanctuaries staff video (audio stripped). Every shot tagged on screen. NOAA homepage loop avoided (may be non-federal drone footage).
- **Reuse by source photo:** crops of one photo now count as the same photo. Every source is used at most twice; only the 1936 aerial
  is used 3x (then/now wipe + its two story shots). The `*_L` / `*_R` crop note in section 3 no longer applies.
- **Checks (v2 master):** SOUND LOCK OK (-14.0 LUFS, TP -2.7 dBTP, LRA 2.2 LU, 97 cues, 52 beds); safe-text PASS c01-c08; blackdetect 0;
  contact sheet `FINAL_SHEET_v2.jpg` looked at.
- **Owner check:** NOAA wk240 shots (heron, bird on wreck) are ground/telephoto shots credited to NOAA; confirm they are NOAA staff footage.
- **Thumbnails v2** (`thumbnails/make_thumbs_v2.py`), built to `research/thumbnails/THUMBNAIL_STUDY.md`: colour, blue sea (sea-only
  grade, study s10), bright, wrecks as subject, one true number, one then/now split, Anton white + red #E0352B, corners clear.
  V1 GHOST FLEET (NOAA drone, hull rows + rusty wreck; upload with this), V2 1936 | TODAY split (NARA 18-AA-70-44 | NOAA drone),
  V3 $3,200 A SHIP (NOAA kayaker photo; $750,000 / 233 ships). The v1 T1-T3 (two B&W) are kept but not used.
- **Thumbnails v2, after two critiques** (`thumbnails/CRITIQUE_1_ctr.md`, `CRITIQUE_2_truth_rights_design.md`): red element is now a white
  word on a red box (red text vanished in the greyscale test), stroke 9 + shadow, crops that show a hull shape, sharpen <= 1.1.
  Main **V3 "$3,200 A SHIP"**; Test & Compare **V2 "1936 | 2020"** (frames' own dates: the NOAA drone film is from Nov 2020, so not
  "TODAY") and **V1 "TOO LATE"** (owner OK needed; fallback "BURNED"). "GHOST FLEET" dropped (repeats the title; never spoken).
  Critique notes left for the owner: the foreground hulk in the NOAA drone shot is NOT the Accomac (HQ_FOOTAGE label wrong); the hook
  says "about three thousand dollars", line 77 says "three thousand two hundred" (thumbnail matches line 77); the 1936 aerial was
  flown 6 Mar 1936 (8 Apr = print date).
