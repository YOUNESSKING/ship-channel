# Fleet's End: HANDOVER (as of 2026-11-20)

Read in this order: `CLAUDE.md` → this file → `STYLE_LOCK.md` → `reference/battle-maps/HANDOVER.md` and
`reference/battle-maps/STYLE_LOCK.md` (parent rules) → `PLAN.md` → `research/FIRST_5_VIDEOS.md` →
`research/FORGOTTEN_FLEET_STUDY.md` (last section) → `videos/oriskany/full/BUILD_REPORT_v8.md`.

## Where things stand
- Channel: **Fleet's End** (@FleetsEnd). Brand final in `assets/brand/final/` (logo D "Last light", banner, wordmark),
  channel description `assets/brand/CHANNEL_DESCRIPTION.md`.
- Video 1, USS Oriskany: v8 master built and checked (Archive voice). Not published yet: its SS United States lines
  (sinking planned 12 Nov 2026) must be rewritten to what happened, then v9 (fast path in BUILD_REPORT_v8.md §6). That
  work is handled in the original session, not here.
- Video 2: **Mallows Bay**, built in session "Fleet's End v2" (`videos/mallows_bay/`, `full/BUILD_REPORT_v1.md` incl. §9
  owner notes for v2). Delivered 2026-11-16. Read its §9 and its thumbnail critiques: they are the latest owner feedback.
- Video 3: **USS Nevada** (`videos/uss_nevada/`), built 2026-11-17/18 in session "Fleet's End v3" with every gate pre-approved by the
  owner; hook re-made on the owner's note ("not clear ... make it engaging": only HD colour film + 4K stills). Master v1 14:13, SOUND
  LOCK OK; record in `full/BUILD_REPORT_v1.md` (section 9 = open items). New tools: OSM water mask in `bake_sea.py` (WATERMASK=osm),
  depth model + deps in setup.sh.

- Video 4: **USS Ranger** ("The Top Gun Carrier Sold for One Cent", thumbnail SOLD FOR 1¢), plan in `research/FIRST_5_VIDEOS.md` §4.
  Folder: `videos/uss_ranger/`. Built in session "Fleet's End v4" with **every gate pre-approved by the owner (2026-11-19)**: do not stop
  at the hook or shot list; finished video by the next morning. Copy the USS Nevada scripts (`videos/uss_nevada/full/build/`, `mk/`),
  which carry the latest fixes (focus.py, no groan rule, film-window checks). Read `videos/uss_nevada/full/BUILD_REPORT_v1.md` (sections
  4, 8, 10, 11) for the lessons. No Top Gun film clips: titles/names only.
  **Status 2026-11-19:** built (master v1 14:11, SOUND LOCK OK), record in `videos/uss_ranger/full/BUILD_REPORT_v1.md`. vidIQ scoring and Gofile
  upload done 2026-11-19 (owner asked): https://gofile.io/d/35cTkSsB. vidIQ scoring still waits for the owner's direct OK. New tools: `build/film_cuts.py` (split film
  windows at detected cuts), `build/window_sheet.py` (one-sheet frame check of every window); DVIDS video skips the ship grade.

- Video 5: **USS Samuel B. Roberts** ("The Deepest Shipwreck Ever Found", thumbnail 22,000 FT DOWN), plan in `research/FIRST_5_VIDEOS.md` §5.
  Folder: `videos/uss_samuel_b_roberts/`. Built in session "Fleet's End v5". **Owner approval given directly by the owner on 2026-11-19 in
  session Fleet's End v4** (recorded in `videos/uss_samuel_b_roberts/OWNER_NOTES.md`): all gates pre-approved (hook, shot list / test render),
  vidIQ credits up to ~400 for titles + thumbnails, Gofile upload of master + upload kit PDF + thumbnails at the end; finished video by the
  next morning. Copy the **USS Ranger** scripts (`videos/uss_ranger/full/build/`, `full/mk/`): they are the newest (see lessons below).
  The 2022 dive footage/stills (Caladan Oceanic / Victor Vescovo) are copyrighted: describe only, never show.

  **Status 2026-11-20:** built overnight (master v1 15:24, SOUND LOCK OK, blackdetect 0), record in `videos/uss_samuel_b_roberts/full/BUILD_REPORT_v1.md`. Delivered on Gofile (master + kit PDF + thumbnails, md5 checked): https://gofile.io/d/fxwCBlSe. vidIQ: 30 credits (titles).

### Lessons from USS Samuel B. Roberts (video 5, read before building video 6)
1. Copy the SBR `full/build/` (newest): `film_bad.py` (fast white-out / blank-frame scan; make_shotlists cuts those spans like scene cuts),
   `window_sheet_used.py` (frame sheet of the windows the shots actually use), NARA 480i timecode crop and NOAA "keep colour" in `make_segments.py`,
   `sfx_full.py` drops cues that fall on their own shot's cut (the sound lib crashed on a 0-length cue).
2. **Card brightness audit before rendering**: measure the luma of every built card background (`b_*.mp4`, see BUILD_REPORT §4); anything under
   ~90 renders as a dim card. about 25 backgrounds had to be swapped here (NOAA seabed video and night/smoke film read dark once dimmed).
3. NOAA Ocean Exploration video carries burned-in title cards and species captions: pick caption-free windows (skip the first ~10 s, detect
   white text per second) and never use 720p clips that need a big crop (the octopus clips came out as blank colour).
4. The footage agent's window notes can be wrong (a "destroyer at speed" window was a crowd of sailors): check every used window on the sheet.
5. Two chapter renders can run in parallel only with separate TMPDIRs: `render_all.sh` deletes `/tmp/hyperframes-extract-cache-*` before each
   render (a second job would wipe the first job's cache). Copy with `rm -rf "$TMPDIR"/...` (see `full/logs/render_all_b.sh`). ~1 h 30 for 15 min.
6. Primary documents beat press: Copeland's action report was on NARA (catalog id 78682556) and fixed several numbers and the crew quote.
7. vidIQ thumbnail scoring needs a public image URL (the image library upload returns only an id): titles were scored, thumbnails not.

### Lessons from USS Ranger (video 4, read before building video 5)
1. Copy `videos/uss_ranger/full/build/` (not Nevada): it has `film_cuts.py` (scdet cuts; `make_shotlists.py` splits film windows at
   them), `window_sheet.py` (one sheet: start/middle/end of every film window), DVIDS video skipping the ship grade (the grade read a grey
   colour video as B&W), `paperwork.py` / `make_kit.py` / `music_bed.py` already de-Nevada'd. Grep every copied script for the old ship name.
2. scdet misses cuts between similar shots: after `make_segments.py film`, ALWAYS look at `build/seg_sheet.py` sheets of every film
   segment (Ranger had a missed cut, a slate, an "End of Recording" card and a TV presenter); fix by hand in `build/film_cuts.json`.
3. Text cards: put `dim="lt"` on every number card and back every card with a BRIGHT photo; check card brightness on the first contact
   sheet (Ranger needed a full re-render because cards read near-black).
4. `make_segments.py` loads segments.json at start: after any beats change, kill running segment jobs, delete the changed segments
   (compare old/new segments.json), restart. Photo segments are slow (~40 s each): run 3 workers on disjoint file lists. Stills (`s_*`)
   are built only when you pass their file names. Never edit a shell script that is running (bash reads it as it goes).
5. mix_full.py: never delete `chapter/joined_silent.mp4` before a full re-mix (it would reuse the OLD master picture via PICTURE_SRC).
6. Basemaps: check every bake (Hampton Roads with WATERMASK=osm came out inverted; re-baked without it). Map agent did 31 scenes well.
7. Fact-check catches on Ranger: dates in the plan were wrong, "the Top Gun carrier" overclaimed, "sold" was not a sale. Expect the plan
   in FIRST_5_VIDEOS to have errors: the 3 checkers decide, not the plan.
8. Script length: 2,250 words = 14:11 with the Archive voice. Aim 2,300-2,500.

## Per-video pipeline (Oriskany is the worked example; copy its scripts, do not rewrite from scratch)
1. Research: Gemini dossier (`research/GEMINI_BRIEF_v3.md` pattern) → `FACT_SHEET.md` → 3 independent fact-checkers on
   official sources (`FACTCHECK_A/B/C_*.md` pattern). Gemini invents claims; nothing unverified goes in the script.
2. Hook (`script/HOOK_v1.md` pattern) → **stop, owner approves the hook**.
3. Full script + `NARRATION_v*.txt` (one paragraph per line), titles/thumb ideas in `script/TITLES_THUMBS.md`.
4. Footage list + downloads + CREDITS/MANIFEST (`videos/oriskany/footage/` pattern; rights field read for every item).
5. Voice in Archive + pronunciation gate + names clip (`full/build/voice.py`, `voice_gate.py`, `names_clip.py`).
6. Shot lists (`full/build/make_shotlists.py`) → **stop, owner approves the shot list / test hook render** before the
   full render.
7. Maps (`full/mk/`), hero animations (`make_anims.py`), segments (`make_segments.py`), chapters (`render_all.sh`),
   SFX + music + mix (`sfx_full.py`, `music_bed.py`, `mix_full.py`), all checks from STYLE_LOCK.md.
8. Packaging: titles (vidIQ, ask before spend), thumbnails, description, upload kit PDF.
9. Owner review of the finished video (720p preview sent; Gofile only if the owner asks).

## Fresh-container setup
- `bash setup.sh` (ffmpeg, hyperframes, kokoro-onnx, Kokoro model files). `pip install faster-whisper av==15.1.0`.
- Paths: copied tools may still hard-code `/home/user/battle-maps` or `/home/user/prehistory-channel`; patch them to
  repo-relative paths. Oriskany scripts hard-code `videos/oriskany/...`; copy and point them at the new video folder.
- Not in git (re-fetch): Epidemic SFX (`assets/sfx/EPIDEMIC_SFX.md`, Epidemic MCP), Chris Zabriskie music (CC BY,
  `assets/music/MUSIC_OPTIONS.md`), archive film and photos (per `footage/` lists), Kokoro model files.
- Disk is a small per-session allowance: keep stems in `/dev/shm`, delete rebuildable caches, never keep more than
  one old master.

## Owner rules for working
- Commit after every step, author YOUNESSKING; never commit keys or licensed/heavy media; push to `main` unless told
  otherwise. Never edit or delete the source repos (battle-maps, prehistory-channel).
- Ask before any spend (vidIQ credits, paid APIs). Public uploads (Gofile etc.) only when the owner asks.
- Stop for the owner only at: hook approval, shot-list/test approval, spending, and the finished video.
- Owner writes short, quick messages; reply in plain, short English.
