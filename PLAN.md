# Ship-History Channel: Reuse Plan (from battle-maps + prehistory-channel)

Full notes:
- /tmp/claude-0/-home-user/e065d3fa-b63b-536b-bb86-8680d09491b8/scratchpad/notes_battle_maps.md
- /tmp/claude-0/-home-user/e065d3fa-b63b-536b-bb86-8680d09491b8/scratchpad/notes_prehistory.md

## Base to copy
- **Skeleton:** battle-maps `patton/` (WWII + archive film) for the folder layout, with the newer tools from `arnold/tools/`.
- **Build chain:** prehistory `templates/build_chapter.py` (JSON shot lists timed to spoken words) and video02's `make_plan.py → build_all.sh → mix_all.sh → build_final.sh`.
- **Fix first:** battle-maps scripts hard-code `/home/user/battle-maps`. Symlink that path or patch it.

## Reuse as-is
| Need | Tool / path |
|---|---|
| Maps, ship tracks, camera moves | `map-kit/` + `MAP_MAKING_GUIDE.md`; `scenes-src/example_route.js`; `GG.ship`, `K.aircraft`, `K.bombRun`, `K.impact` |
| Ship counters on paths | `arnold/tools/va_kit.js`, `vk_kit.js`; ocean map in `goosegreen/scenes-src/hook-atlantic.js` |
| Archive film download / crop | `patton/assets/film/cut_clips.sh` (archive.org NARA IDs) + `MANIFEST.md` honesty notes |
| Photo / film moves, parallax, date cards | `maps/tools/archive_shots.py`, `tools/restore_film.py` |
| Number counters, labels, cards | template blocks `number_clip`, `lower_third`, `title_card`, `text_card`, `scale_ruler` |
| Animations | `anim_gauge` (sinking to 212 ft), `anim_options` (scrap/museum/reef struck out), `anim_xray` (hull cutaway), with `anim_theme` |
| Voice (free) | Kokoro `am_michael` via `tools/narrate.py`; pronunciation gate `tts/PRONUNCIATION.md` |
| Voice (paid, better) | ElevenLabs "Will" via `videos/video02/voice/record.py` (needs a paid plan for commercial use) |
| Sound mix | `templates/mix_audio.py` (4 layers, voice ducking) + `templates/mux.sh` (-14 LUFS, measured trim) |
| SFX | `goosegreen/assets/media/sfx/`; video02 ElevenLabs set (`deep_boom`, `splash_big`, `sink_bubbles`…); `*.wav` is git-ignored, so copy by hand |
| Music | Kevin MacLeod CC BY 4.0 via `make_music_bed.py`; Epidemic catalog only while subscribed |
| Fact-check | Gemini dossier, then 3 Sonnet checkers on official texts (`patton/research/FACTCHECK_*.md` format) |
| Thumbnails | `video-thumbnail` skill + `tools/make_thumb.py` (Anton, white + one red word) |
| Competitor study | `watch` skill / `gemini_watch.py`, `research/tools/yt_channel_scan.py @forgottenfleet1` |

## Must build or adapt
- Sea-first map look: re-grade `bake.py` (Terrarium tiles already include sea depth) to shade the sea floor; NOAA/GEBCO data for the reef site; lock the look with one test sheet.
- New art: top-down modern carrier silhouette, a sinking animation.
- New SFX: horn, sea swell, catapult, hull groan.
- Turn off the "Deep Time" grade (`GRADE=none`); add pillarbox/upscale handling for old NARA film; trim film leaders.
- Drop the survival-game parts (tier board, "you" verdicts, lo-fi music).
- New `brand-style.md` for ships.

## Rules that carry over word for word
- Line 1 states the stakes. The title's promise is spoken by 10–15 s, and the first frame is a map.
- No ship résumé ("laid down in 1944…") in the first 2 minutes: stay inside the crisis story.
- Every shot proves the spoken words; something new on screen every 1.5–4 s; hard cap of 6 s per shot.
- A place or date gets a map; a number lands on the spoken word; a clip is reused at most twice, 3+ min apart.
- A wow moment early, then every 30 s for the first 3 min; a mid-video reversal; a closing question; ending ≤ 45 s.
- Gates: one fact sheet, hook approved first, shot-list gate before render, ask before any spend, commit after every step.
- Rights: PD / CC0 / CC BY / CC BY-SA only, never NC/ND; read each NARA/NHHC/DVIDS item's rights field; log every file in `CREDITS.md`.
- YouTube "altered or synthetic content" box: Yes (AI voice).

## Packaging
- 3 titles scored ≥ 85 in vidIQ + 2–3 thumbnails in Test & Compare. Thumbnail: 1–3 true words, a real photo cut out, a dark scene.
- Check the thumbnail at YouTube sidebar size (Arnold flopped at 2.85% CTR there).
- Growth gauge: about 18 s of watch time per impression, and 3.5%+ Suggested CTR.
- Log days 1–3 in `CHANNEL_LOG.md`.

## Time and cost
- About 1.5–2 h of agent work per video, plus 2.5–4 h of rendering (run detached and resumable; the machine reboots when idle).
- Prehistory: $16–19 cash per AI-heavy video; archive-based should be cheaper.
- Kokoro voice is free; ElevenLabs Creator is $22/mo for about 6 videos.

## Open issues
- Rotate the API keys that were pasted into chat in earlier sessions.
- vidIQ credits and RunPod balance are low.
- Wikimedia, Freesound and Pixabay block cloud downloads, so the owner downloads those.
- prehistory-channel has no recorded views/CTR, so there's no data on what worked there.

## Video #1
**"Why the Navy Sank Its Own Aircraft Carrier" — USS Oriskany.** Publish by **Nov 11**, before the SS United States is sunk at the same reef area on Nov 12.
