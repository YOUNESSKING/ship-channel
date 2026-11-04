# Ice Age / North Atlantic map clips (test video)

Built on the user's real map-kit (copied from `battle-maps/map-kit`, original left untouched) following MAP_MAKING_GUIDE.md.
Outputs: `out/map_iceage.mp4` (6.0 s = "But what about the Ice Age ... whole north?", VO 13.0-19.0 s), `out/map_natlantic.mp4`
(4.7 s = "Okay, so the first ocean is the North Atlantic, twenty thousand years ago.", VO 33.6-38.3 s), both silent 1920x1080 30 fps; `out/sheet.jpg` = contact sheet.
(The VO spans are only 6.0 s and 4.7 s, so the clips are shorter than the ~9 s in the brief; the cut points follow the narration.)

## Bake a new place (python venv: `venv/bin/python`, needs numpy pillow scipy)
```
SEA_LEVEL=-120 venv/bin/python tools/bake.py  NAME LAT LON ZOOM [EXAG]     # assets/NAME.jpg + NAME.json (projection)
SEA_LEVEL=-120 venv/bin/python tools/bake_hd.py NAME [EXAG]                # assets/NAME_hd.jpg + NAME_hd_ref.jpg (dark grade, 5760x3240 shown at 2880x1620)
```
Leave SEA_LEVEL out for today's coast. Natlantic: `bake.py natlantic_lgm 55.5 -27 5 6`, then `bake_hd.py natlantic_lgm 2.5` (zoom 5, ~28N-70N, 90W-36E; z4 is too wide, z5 is the largest integer zoom that frames Newfoundland-Scandinavia).
Present-day twin: same commands with `natlantic_now` and no SEA_LEVEL; copy `assets/natlantic_now_hd_ref.jpg` to `assets/media/now.jpg` (build_scene copies assets/media/*.jpg).
Ice sheets: `venv/bin/python tools/make_ice.py natlantic_lgm_hd_ref` -> `assets/media/ice_*.png` (edit the lat/lon POLYS in the script; outlines are hand-placed, approximate).

## Make a scene
1. Timing: `python3 tools/words_to_timing.py WORDS.json audio/timing.json` (edit PARAS: id, first/last word time, scene start). Every word becomes a `sents` entry so `B.at(para, "phrase")` hits the exact word. A scene runs from its first paragraph to the START of the next paragraph, so add a following "marker" paragraph and build with FIRST=LAST.
2. Scene file `scenes-src/NAME.js` (see `iceage.js`, `natlantic.js`; shared set-up in `_ice_common.js` via `//@include`). Projection numbers = zoom + origin_world_px from the basemap json.
3. `python3 tools/build_scene.py NAME natlantic_lgm_hd_ref FIRST LAST`, then `cd scenes/NAME && npx hyperframes lint . && npx hyperframes snapshot . --at ...` (look at contact-sheet.jpg, max 3 rounds), then `npx hyperframes render . -o renders/NAME.mp4` (these two clips render in ~40 s each; `tools/render_all.sh` still works for long ones).

## What differs from the user's real kit (all small, marked "KIT CHANGE" in code)
- `tools/bake.py`, `tools/bake_hd.py`: `SEA_LEVEL` env (metres; elevation is shifted so anything above it is land; stored as `sea_level` in the json). bake_hd's dark grade now colours the sea by depth with a faint shore halo and tints exposed shelf (SEA_LEVEL < 0); the stock dark grade used one flat sea colour.
- `tools/build_scene.py`: `//@include FILE` in a scene file pulls a snippet from scenes-src/.
- New: `tools/words_to_timing.py` (human VO word times -> timing.json), `tools/make_ice.py`, `scenes-src/_ice_common.js`, `iceage.js`, `natlantic.js`.
- Nothing in lib/ (engine) was edited. The Ice Age scenes add their own small helpers in `_ice_common.js` (ice layers that are visible at t=0, a quick date tick, a dashed sea-ice line).
- Not used: geo layer (no OSM/Natural Earth, labels hand-placed), rivers shimmer, SFX cues beyond the engine's own.

## Clean map bakes for the template library (Video 01 rebuild)
`tools/bake_clean.py` (+ `bake_run.py`, `v01_map_shots.py`, `lgm_polys.py`, `v01_plan_times.py`) bakes **clean** 1920x1080 30 fps map videos for the `map_clip` template: terrain, moving coastline, ice growth on land, ocean darkening, camera move. **No text, no pin, no gauge** are drawn; the template does that. It needs no browser (numpy + OpenCV + ffmpeg), so it runs on a rented CPU pod: `tools/runpod-cpu/maps_job.py`.
- Look = the approved v9 North Atlantic map (dark teal sea, olive land, white relief-shaded ice, same colours as `bake_hd.py` / `make_ice_progress.py`).
- Coastline: real renders every 4 m from 0 to -120 m, cross-faded, so the shore moves; timed with the template gauge (`v01_map_plan.json`, made by `v01_plan_times.py` from the chapter JSONs: same ease `power2.inOut`, same start and length).
- Ice: per-pixel arrival-time field (grows from the dome outward, relief visible), only on land at the current sea level; Antarctic grounded ice may sit on the shelf; mountain glaciers above an LGM snowline; the ocean darkens instead of showing sea ice. Outlines are approximate (`lgm_polys.py`).
- Far-from-ice places get a small world inset with the ice sheets (rule 18), bottom-left; the json says where it is.
- Each `<id>.json` holds: the real pin position in the 1280x720 design space (`pin.template_param`, plus a `track` if the camera moves), the gauge start/length actually used, ice start/end, the km-per-pixel and px-per-degree scale (`scale`), the inset rectangle, and for MAP_03e2 the 59N/68N rows (`measure_frame`).
- Run: `python3 tools/bake_clean.py bake [ID ...] -j N` (env `MAP_CACHE`, `OUT_DIR`); `plan` lists the shots. The planner's tile "zoom" numbers (z3, z4) are far too wide for a 2880 px canvas, so each place has its own zoom in `v01_map_shots.py`.

## Video 02 map bakes (paleogeography)
`tools/bake_v02.py` bakes the 15 clean map clips of Video 02 (`videos/video02/maps/<id>.mp4` + `<id>.json`, same json pin fields as Video 01). Deep-time maps use the PALEOMAP PaleoDEMs (Scotese & Wright 2018, CC BY 4.0) in `maps/cache_v02/paleodem/` (git-ignored; fetch single members of the Zenodo zip with `tools/remote_zip.py URL _80Ma.nc -o DIR`); present-day maps use the Terrarium tiles as before (`sea` = sea level). Paleo pin positions come from the GPlates Web Service (model PALEOMAP). Python deps in `maps/cache_v02/venv` (numpy scipy opencv-python-headless h5py). Run: `taskset -c 0-2 maps/cache_v02/venv/bin/python maps/tools/bake_v02.py [ID ...] [--still]`; sheet: `tools/v02_sheet.py videos/video02/maps videos/video02/maps/maps_sheet.jpg [--pins]`. Credits: `videos/video02/maps/CREDITS.md`. Sharpness pass: 5760x3240 canvas, frames warped at 3840x2160 then area-downscaled + light unsharp; deep-time relief texture = high-passed real terrain (Terrarium z6, `TEX_BOX`) scaled by PaleoDEM height/slope; masters (crf 10) in `maps/cache_v02/masters/`, git copies <= 4.8 MB (2-pass when needed, `--deliver` re-encodes only); before/after sheet `tools/v02_before_after.py`.
