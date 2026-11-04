# Oriskany test v3 (1-minute hook)

Owner feedback on v2: sound and music "way off" -> use the battle-maps locked levels and sync; more video than stills.

## What changed from v2
- Sound: the battle-maps mix tools ported to `tools/sound/` (locked role levels/gaps, music 0.08 ducked, SFX full level ducked
  lightly, limiter 0.5, -14 LUFS two-pass + 2c-9 trim, AAC 192k, `check_sound_lock.py`). Every cue comes from `build/sfx_cues.py`
  (word timings + shot starts). See `SOUND_REPORT.md`.
- Picture: 13 real NARA film shots (`build/films.py`), 2006 stills only for the 2006 events; options board over moving film
  (`bg_clip` in the chapter json); one font (Oswald, chapter key `"font": "oswald"`).
- Fixes: end map 4.3 s with the official coordinates and kit liner/carrier drawings; map seam removed (`mk/tools/bake_sea.py`:
  sea floor from one data source); depth gauge in world space so 0 FT sits on the drawn surface (`hero/sinking.js` `gaugeWorld`);
  the "1950s" photo is gone (replaced by labelled film).

## Build order
1. `python3 build/films.py` (film shots) ; photo shots and `m37_sequence` reused from v2 (`build/shots.py`)
2. `cd mk && SS=1 python3 tools/bake_sea.py pan_close 30.22 -86.85 11 && python3 tools/build_scene.py endmap pan_close endmap endmap`, render `mk/scenes/endmap`
3. `cd hero && npx hyperframes render . -o renders/hero.mp4`
4. copy `endmap.mp4`, `hero.mp4` into `segments/`, then `cd ../../../templates && python3 build_chapter.py ../videos/oriskany/test_v3/chapter/c01.json`, render `chapter/work/c01` -> `chapter/render_c01.mp4`
5. `python3 build/mix.py` (MUSIC=path to swap the theme) -> `oriskany_test_v3.mp4`; `python3 build/report.py` -> `SOUND_REPORT.md`
