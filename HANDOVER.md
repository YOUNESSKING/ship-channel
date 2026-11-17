# Fleet's End: HANDOVER (as of 2026-11-15)

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
- Video 3: **USS Nevada** ("The Battleship That Survived Two Atomic Bombs", thumbnail SURVIVED 2 A-BOMBS), plan in
  `research/FIRST_5_VIDEOS.md` §3. Folder: `videos/uss_nevada/`. Built in session "Fleet's End v3".

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
