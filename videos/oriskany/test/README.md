# Oriskany 1-minute test

Rebuild (from this folder): `cd build && python3 voice.py && python3 bake.py && python3 render.py && python3 mix.py`
Needs the source film + music/SFX in `src/` (see CREDITS.md; `src/` is git-ignored).
- `build/voice.py` Kokoro am_michael at 0.95, one chunk per phrase → `audio/voice.wav` + `build/timing.json`
- `build/bake.py` sea-first basemaps from Terrarium tiles (bathymetry shaded)
- `build/render.py` PIL frames → ffmpeg; every shot starts on a chunk from timing.json. `python3 render.py 12.5 30` renders stills only
- `build/mix.py` voice + ducked music + SFX, measured trim to -14 LUFS, limiter, mux → `oriskany_test_1min.mp4`
