# Fleet's End: STYLE LOCK (locked at Oriskany v8, 2026-11-11)

This is the house style every Fleet's End video must match. The reference build is
`videos/oriskany/full/` (v8, the Archive voice), with `BUILD_REPORT_v8.md` as its record. The approved hook look/sound
is `videos/oriskany/test_v4/`. If this file and `CLAUDE.md` disagree, `CLAUDE.md` wins. The battle-maps rulebooks
(`reference/battle-maps/STYLE_LOCK.md`, `HANDOVER.md`) are the parent rules: read them too; this file says what Fleet's
End changed or added.

## 1. Format
- 14–24 min, 1920x1080, 30 fps, H.264 + AAC 192k stereo 48 kHz. 7-ish chapters, timestamps in the description.
- Structure: hook (~45–50 s, owner-approved before the script) → chapters → reversal mid-video → answer held to the last
  act → closing question → end screen 18 s (end-screen map with room for subscribe + 1 video). Ending ≤ 45 s.
- Line 1 = the stakes. Title promise spoken by 10–15 s. First frame is a map. No ship résumé in the first 2 min; service
  history only as flashbacks that serve the question.
- A wow early, then every 30 s for the first 3 min.

## 2. Voice (owner pick 2026-11-10)
- "Archive": Kokoro style blend bm_fable 0.40 + am_michael 0.40 + bm_lewis 0.20, speed 0.92 (questions 0.852).
  Style vector: `tts/voices/archive_style.npy` (committed; rebuild with `tts/design_voice.py` if lost).
- Chunked by sentence/phrase; pauses 0.3 / 0.6 / 0.9 s. Cache chunks as float and scale the take by 0.5 (the raw blend
  peaks above 0 dBFS); the mix normalises voice to its locked level.
- Pronunciation gate (`tts/PRONUNCIATION.md`): transcribe the full take with faster-whisper **small.en**
  (`pip install av==15.1.0` if it errors on `metadata_errors`), diff against the script, respell / phoneme-fix every
  miss, then make a names clip (`voice_sample/names_<topic>.mp3`) for the owner's ear. Reference: `full/build/voice_gate.py`,
  `full/build/names_clip.py`.
- Word timings: small.en, aligned to script words, snapped to pauses. Everything on screen is anchored to words, never to
  absolute seconds.

## 3. Picture
- Every shot proves the spoken words. Something new every 1.5–4 s; **hard cap 6 s per shot**.
- A place or a date = a map (HyperFrames/GSAP map kit, `map-kit/`, Oriskany scenes in `full/mk/`). Numbers land on their
  spoken word (checker: `full/build/check_numbers.py`).
- **No plain black/dark text cards**: every text or number card sits on a dimmed moving background (matching film,
  tagged generic b-roll, or a moving map/photo).
- Archive film: `GRADE=none` (no Deep Time grade); `ARCHIVE_GRADE=ship` where the Oriskany build used it; pillarbox or
  upscale 4:3; trim leaders. Generic footage that is not the subject ship is marked ILLUSTRATIVE on screen.
- A clip **or photo** is used at most twice, 3+ min apart (owner 2026-11-15: "don't reuse the same photos, 2 times tops";
  `build/shotlist_report.md`).
- Hook must be engaging and use the highest-quality footage available (owner 2026-11-15, Mallows Bay v2 notes).
- Text: Anton / Oswald, white with one red accent (#D9572B family / red), steel-blue secondary. No gold/yellow.
  Safe-area checker `templates/check_safe_text.js` must pass every chapter.
- Contact sheet (one frame every 10 s) looked at before delivery; blackdetect clean; `tools/film/check_clips.py --no-cuts`.

## 4. Sound (locked by the owner 2026-11-04/05/08; enforced by `tools/sound/check_sound_lock.py`)
- Master: **-14.0 LUFS integrated**, true peak ≤ -1.5 dBTP, LRA floor 1.7 LU for full-length masters, music under speech
  ≈ -24 dB, big beats ≥ +1 LU over speech. Linear loudnorm with a measured trim. Renders and mixes run detached
  (nohup) and resumable; keep stems in `/dev/shm` when disk is low.
- SFX are real Epidemic Sound recordings (`assets/sfx/EPIDEMIC_SFX.md`; files git-ignored, re-download with the Epidemic
  MCP; md5 lock in `tools/sound/epidemic_md5.json`) through the v2 chain in `tools/sound/` (reference mix:
  `videos/oriskany/full/build/mix_full.py`, `sfx_full.py`).
- Role levels (dB): explosion/charges -7, impact -10, hit/stamp -11, boom -14, jet -17 (+ -6 dB at 2.5 kHz), whoosh -15,
  ship (groan/flood/bubbles) -16, riser -20, horn -23, pop -23, tick -23; beds: projector -29, drone/waves/underwater -32.
- Every effect is silent by the next picture cut after its event (0.25 s fade ending on the cut; a whoosh on the cut may
  run ≤ 0.4 s into the next shot). Beds start and stop with their shots (0.25 s fades). No effect rings > 1.5 s past
  its event. Horn ≤ 2 s, ≤ 2 per video, never under speech. Per-cue trims may only cut (gain ≤ 0, lowpass, longer fade).
- Speech-band SNR check per word under effects (`full/build/snr_words.py`); cut or move a cue that masks a word.
- Music: Chris Zabriskie, *Music from Neptune Flux* (CC BY 4.0), credited in the description; bed built by
  `tools/sound/make_music_bed.py` / `full/build/music_bed.py` pattern.

## 5. Rights and paperwork
- PD / CC0 / CC BY / CC BY-SA only, never NC/ND; read each item's rights field. Every file in the video's `CREDITS.md`,
  every film clip in `MANIFEST.md` with what it does NOT show.
- Description credits block in the Oriskany format (`full/YOUTUBE_DESCRIPTION_DRAFT.md`), "Narration: AI voice (Kokoro TTS)",
  "Altered or synthetic content" = Yes.

## 6. Packaging
- 3 titles scored ≥ 85 in vidIQ (ask before spending credits) + 2–3 thumbnails for Test & Compare.
- Thumbnails: real archive photos only (no AI repaint of the ship); sea-only colour grade allowed (blue ocean, see
  `videos/oriskany/thumbnails/make_thumbs_v3.py`); 1–3 true words, white Anton with one red word; bottom-right corner
  clear (timestamp); check at sidebar size. Study: `research/thumbnails/THUMBNAIL_STUDY.md`.
- Upload kit: HTML → PDF (title, thumbnails, settings, description with chapters, tags, pinned comment, checklist), as
  `videos/oriskany/full/upload_kit/`.
