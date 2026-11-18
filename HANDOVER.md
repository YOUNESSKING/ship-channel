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
- Video 3: **USS Nevada** (`videos/uss_nevada/`), built 2026-11-17/18 in session "Fleet's End v3" with every gate pre-approved by the
  owner; hook re-made on the owner's note ("not clear ... make it engaging": only HD colour film + 4K stills). Master v1 14:13, SOUND
  LOCK OK; record in `full/BUILD_REPORT_v1.md` (section 9 = open items). New tools: OSM water mask in `bake_sea.py` (WATERMASK=osm),
  depth model + deps in setup.sh.
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
