# Ship Channel

Faceless naval / ship-history YouTube channel: "what happened to this ship" documentaries, 14–24 min,
AI narration, public-domain archival photos and film (NARA, NHHC, DVIDS, US Navy), animated maps.

Built by reusing the tooling of the owner's two other channels, battle-maps and prehistory-channel.
Start with `PLAN.md`, then `CLAUDE.md`.

| Folder | What it is | Came from |
|---|---|---|
| `map-kit/` | HyperFrames + GSAP map engine, routes, ships, aircraft, impacts | battle-maps |
| `tools/bm/` | newest battle-maps kits (`va_kit.js` boats on paths, `vk_kit.js` steamers, `narrate.py` ...) | battle-maps `arnold/tools` |
| `tools/maps/` | terrain bake (`bake.py`), `archive_shots.py` (photo/film moves, parallax, date cards) | prehistory `maps/tools` |
| `tools/film/` | `cut_clips.sh` archive.org NARA downloader/cropper + MANIFEST example | battle-maps `patton` |
| `templates/` | `build_chapter.py` JSON shot-list engine, blocks (`number_clip`, `anim_gauge`, `anim_options`, `anim_xray` ...), `mix_audio.py`, `mux.sh` | prehistory |
| `templates-bm/` | battle-maps video templates | battle-maps |
| `tts/` | Kokoro voice (free), pronunciation gate, ElevenLabs recorder | both |
| `assets/sfx/` | SFX credits (the .wav files are git-ignored; copy by hand) | battle-maps |
| `research/` | data rules, packaging guide, Gemini brief, judge brief, channel scan tool | battle-maps |
| `.claude/skills/` | `video-thumbnail`, `watch` | prehistory |
| `reference/` | full handovers, style locks, gold standard, and the reuse notes | both |
| `videos/` | one folder per video | new |
