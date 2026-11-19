# USS Nevada full video: build report v1 (2026-11-17/18)

**Output:** `videos/uss_nevada/full/uss_nevada_full_v1.mp4` (git-ignored). H.264 1920x1080, 30 fps, AAC stereo 48 kHz 192k,
**852.9 s (14:13)** = narration 834.9 s + 18 s end screen. 720p preview: `uss_nevada_preview_720p.mp4` (git-ignored).
Video #3 of Fleet's End, built in the locked style (STYLE_LOCK.md, Oriskany v8 + Mallows Bay notes) with the Mallows Bay scripts
copied and adapted. The owner pre-approved every gate for this build (2026-11-17, `OWNER_NOTES.md`); the hook was re-made once on
the owner's note during the build (section 4).

## 1. Research (`research/`)
- No Gemini key: dossier written by a research agent from official sources: `RESEARCH.md`, `FACT_SHEET.md` (~90 rows).
- Three independent fact-checks: `FACTCHECK_A_pearl_war.md` (Nevada's 1941 action report, CinCPac, NHHC/Wallin salvage history,
  Normandy/Okinawa records), `FACTCHECK_B_crossroads.md` (Bombs at Bikini 1947, BuShips Able/Baker inspection reports, BuAer
  distance tables, DNA 1982 ship sheet, NPS 1991), `FACTCHECK_C_end_wreck.md` (DNA, 1948 AP stories, 2022 J. Maritime Archaeology
  paper, SEARCH Inc.).
- Corrections that changed the script: the bomb missed by **about a third of a mile** (sources 1,500-2,130 ft; "700 yards" had one
  source); yields said as **about twenty kilotons**; **at least six bombs** at Pearl Harbor; dead **close to sixty**, wounded **more
  than a hundred**; she was **ordered** out of the channel (not "the crew chose"); grounded at Hospital Point ~09:10 and again at
  Waipio Point 10:45; Cherbourg **straddled more than twenty times**; the "oldest battleship in service" claim is **false** (now "one
  of the oldest"); decommissioned **at Kwajalein**; final blow = **several torpedoes, then one amidships** (not "a single torpedo");
  the sinking day is said as "her last day" (31 July in DANFS/DNA/NARA, but the AP story dated 31 July says "yesterday"); the Arizona
  guns are attributed to the 2022 archaeologists; **never "the only ship to survive two atomic bombs"** (New York and Pennsylvania
  did too: the script says so in c06). Ross's ashes, the band at colours and "Gilda" were cut (single or no official source).
- 2020 wreck imagery is © Ocean Infinity / SEARCH Inc. with no free licence: **described only, not shown**.

## 2. Script and voice
- `script/NARRATION_v1.txt` (2,197 words), 8 chapters: Hook 0:00 · The Bull's-Eye 0:52 · The Ship That Moved 2:31 · Back From the
  Mud 5:25 · Test Able 7:33 · Test Baker 9:04 · Four Days 10:52 · Found 12:42.
- Line 1 = the stakes ("...the United States dropped an atomic bomb on one of its own battleships"); title promise "She survived them
  both" at 10.5 s; first frame a map; Pearl Harbor and D-Day only as flashbacks (c03-c04) answering "why this ship?"; reversal in
  c06 ("this time, surviving was the problem"); answer held to the last act ("So that is what sank her. Her own navy." 12:39, the
  2020 find 13:18); closing question; ending 35 s after the answer.
- Voice: Archive blend, speed 0.92, `build/voice.py`. Pronunciation gate `build/PRONUNCIATION_GATE.md` (boatswain = BOH-sun,
  forecastle = FOHK-sul, Kwajalein, Waipio, Cherbourg, Toulon, Sakawa, Nagato, Attu, Carlisle fixed). Names clip for the owner:
  `voice_sample/names_nevada.mp3` (50 s).

## 3. Footage and rights (`footage/`, `full/CREDITS.md`, `full/MANIFEST.md`)
- 126 stills + 38 films (NARA, US Navy, LoC, DoD); rights read on every record and quoted in `footage/FOOTAGE_LIST.md`.
- Best material: the US Navy colour film *Operation Crossroads: Able and Baker Day Tests* (MN-6517, 1080p scan on archive.org; windows
  cut over HTTP, never the whole 33 GB file). Its faded print of the orange Nevada is **colour-restored** toward the documented
  "international orange" (tag says "COLOUR RESTORED"). The 1948 sinking reels 428-NPC-3646/3647 are 1080p.
- NARA marks most Navy reels "Undetermined" (its default for Navy film; federal works). Four reels carry NARA's generic "Restricted -
  Possibly" note (the DoD Pearl Harbor film, the kamikaze reel...): US Government productions, logged; **owner check** listed in
  `footage/FOOTAGE_LIST.md`. Not used: John Ford's "December 7th" re-creations, staged outtakes, Wikimedia uploads of unclear origin.
- Every film shot carries a top-left tag; non-Nevada or later shots are named (e.g. "ILLUSTRATIVE · USS IOWA FIRING, 1984": no 1948
  Iowa film exists). Film windows were trimmed off slates, leaders and the NARA end logo after a per-window frame check.

## 4. Picture
- 49 map scenes (`mk/scenes-src/`, new sea-floor basemaps incl. Pearl Harbor with an OpenStreetMap water mask, since the elevation
  tiles show the harbour as land; Bikini close, Marshalls, North Pacific, Atlantic, Oahu SW). Approximate positions are labelled
  APPROX. Battleship Row: Nevada at the NE end, Arizona just ahead of her (berth F-8).
- **Hook v2 (owner 2026-11-17: "the hook is filled with videos and photos that are not clear ... I want it engaging")**: rebuilt from
  only the 1080p colour Crossroads film, the 1080p 1948 film and 4K stills; no shot starts on a white-out or an empty horizon; 19
  shots in 52.6 s (a cut every ~2.8 s).
- 248 shots, **0 over 6 s** (end screen excepted), clip/photo reuse clean (`build/shotlist_report.md`), 26 numbers each on its spoken
  word (`build/check_numbers.py`). Cards sit on moving backgrounds; the one card that read near-black (c07 "287") now sits on a photo.

## 5. Sound
- 30 locked Epidemic SFX (md5 match) through `tools/sound/`; beds: projector under archive film, drone under gauges/lists,
  underwater under the c08 depth gauges. Music: Chris Zabriskie, *Music from Neptune Flux* (CC BY 4.0) tracks 01 → 03 (Pearl Harbor)
  → 02 (the comeback) → 04 (Test Able) → 01 → 09 (from the answer).

## 6. Checks
| check | result |
|---|---|
| `check_sound_lock.py` static + render | **SOUND LOCK OK** (section 8) |
| safe-text (every chapter, 0.5 s) | **PASS** c01-c08 (`chapter/safe_c0*.txt`) |
| shots over 6 s / numbers on words | 0 / 26 of 26 |
| clip / photo reuse | clean |
| blackdetect 0.25 s / 0.06 | **0** |

## 7. Packaging (`thumbnails/`, `script/TITLES_THUMBS.md`, `full/YOUTUBE_DESCRIPTION_DRAFT.md`, `full/upload_kit/`)
- Titles scored in vidIQ (40 credits): **"Two Atomic Bombs Couldn't Sink Her. Then What Did?" 94**, "This Battleship Was the
  Bull's-Eye for an Atomic Bomb" 92, "The Navy Dropped an Atomic Bomb on Its Own Battleship" 89.
- Thumbnails (real Navy film frames, sea-only grade, white word on a red box, checked at sidebar size and in greyscale): V1
  SURVIVED 2 A-BOMBS (main), V3 THEY MISSED, V2 BULL'S-EYE; critique in `thumbnails/CRITIQUE_1.md`.
- Description with chapters, sources, credits (incl. OSM attribution), tags and pinned comment; upload kit HTML + PDF.

## 8. Final master
- `uss_nevada_full_v1.mp4`, 852.93 s, 25,588 frames, md5 `2483993e6a69965509d1eda207b44ea2` (`build/master_md5.txt`).
- **SOUND LOCK OK** (static + render): -14.0 LUFS, TP -1.5 dBTP, LRA 2.3 LU (floor 1.7), linear loudnorm, music under speech -24.8 dB,
  12 big beats >= +1 LU over speech, 100 cues within 3 frames (max 1.4), every cue silent by its shot end, 46 beds on cuts.
- ebur128 on the mp4 (`build/ebur128_v1.txt`): -14.0 LUFS, true peak -1.5 dBFS, LRA 2.3 LU. blackdetect: 0 (`build/blackdetect_v1.txt`).
- `tools/film/check_clips.py --no-cuts` (`build/check_clips_v1.txt`, run on the master before the last two card fixes): 100 BLOB (dark
  archive scenes and card shades, the Oriskany/Mallows pattern) + 21 one-frame FLASH = bright/dark cuts (looked at, no glitches).
- Contact sheet `FINAL_SHEET_v1.jpg` (one frame every 10 s) looked at. Three cards that read near-black were re-backed with bright
  photos (c06 "5 of ≈90", c07 "287", c08 "April 2020"; the c08 background is blurred by hand in `segments/b_c08_s06.mp4`: if
  make_segments.py rebuilds it, re-apply `gblur=sigma=10,eq=brightness=-0.05:saturation=0.85`).
- Disk: the container restarted four times during the build (render/mix stems in /dev/shm were lost twice); the last mix reused the
  joined picture (PICTURE_SRC) and re-ran only the sound.

## 9. Open items for the owner
1. Watch the master; listen to `voice_sample/names_nevada.mp3`.
2. Thumbnail V3 "THEY MISSED" (true for the first bomb only): OK or swap for V2 as the second Test & Compare image.
3. Rights notes: four NARA reels carry NARA's generic "Restricted - Possibly" note (US Government productions; listed in
   `footage/FOOTAGE_LIST.md`); the colour Crossroads master on archive.org has no licence field (US Navy production, end card MN 6517).
4. Space the upload from Mallows Bay (2-3 a week max). Gofile upload only if you ask.

## 10. Delivered (owner asked, 2026-11-18)
Master (14:13, md5 2483993e6a69965509d1eda207b44ea2) + upload kit PDF + thumbnails V1-V3 + names clip in one Gofile folder:
https://gofile.io/d/LIT4BWXL (all md5 checked).

## 11. v2 (owner 2026-11-18)
- Owner: "the sinking sound at 11:36, 12:01, 12:07 ... annoying, not in its place": the Mallows rule that put a hull-groan cue on every
  sinking-film shot is removed, plus the two explicit groans (Arkansas, she rolls over): 9 cues gone, 91 left.
- Owner: "you zoom into the white centre, not the ship": every photo now zooms in/out toward its subject (`build/focus.py`: densest-detail
  point, 7 manual fixes in `build/focus_manual.json`), no centre pans; all 88 photo segments rebuilt, all chapters re-rendered (safe-text PASS).
- Master `uss_nevada_full_v2.mp4` 852.93 s, md5 1c06b00f6e36bec9561e5c1a3f1036a4: **SOUND LOCK OK** -14.0 LUFS, TP -1.6, LRA 2.2,
  91 cues within 3 frames; blackdetect 0; `FINAL_SHEET_v2.jpg` looked at. v1 deleted (disk).
- Delivered: https://gofile.io/d/MHsM1Jd8 (master v2 + upload kit PDF + thumbnails; md5 checked).

## 12. Thumbnails v2 (owner approved vidIQ spend, 2026-11-19)
10 new real-frame thumbnails (`thumbnails/N*`, `NOTES_v2.md`, `CRITIQUE_2.md`), scored in vidIQ against title 1: main **N10 [2 A-BOMBS] 91**, Test & Compare
N6 90 and N11 [SURVIVED] 91 (old V1 72). 151 credits used (5,703 -> 5,481; 71 more in that window were another session). Scores used a stand-in
video ID (the video is not uploaded yet): compare them with each other only. AI1/AI2 are vidIQ-generated, labelled AI, not used.
Upload kit updated. Thumbnails + PDF: https://gofile.io/d/8AD26sR7 (md5 checked); master stays at https://gofile.io/d/MHsM1Jd8.

## 13. vidIQ thumbnails (owner: "make them with vidIQ", 2026-11-19)
Generated with vidiq_generate_thumbnail using our real N10 frame (real 1946 Nevada + real Able cloud) as the reference, so the ship keeps
Nevada's look: **AI3 SHE SURVIVED (vidIQ self-score 97)**, AI4 split 2 A-BOMBS (91, closest to the real ship), AI5 2 A-BOMBS wide (82).
AI images (STYLE_LOCK says real photos; owner asked for vidIQ here). Artistic licence: she was at anchor, not under way. 66 credits.
https://gofile.io/d/3cg5jhcP (AI3-AI5 + N10, md5 checked).
