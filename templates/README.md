# Template library for the prehistory channel

Build a chapter from a short **JSON shot list**. No hand-written HTML or animation code.
The look and the motion are copied from the approved test video **v9** (style C: Cormorant Garamond, Jost caps, gold `#C9A45C` hairlines, no film look).

## 1. Build a chapter in 4 steps

```bash
cd templates
python3 build_chapter.py my_project/c01.json            # writes my_project/work/c01/index.html + sfx_events.json
npx hyperframes@0.8.188 snapshot my_project/work/c01 --at 3,7.5,12      # look at single frames (fast)
./render_chapters.sh my_project/work c01 c02            # renders each chapter (skips unchanged ones), joins them
python3 mix_audio.py my_project/work/c01 --voice narration.mp3 --offset 33.6   # sound effects + voice
./mux.sh my_project/work/c01 my_project/rendered/c01.mp4 my_project/final/c01.mp4   # loudness -14 LUFS + mux
```

Other useful commands:
- `python3 build_chapter.py --list` shows every template, its variants and parameters.
- `python3 build_chapter.py c01.json --res 1080` builds for the final 1080p render (default is 720p for drafts).
- `python3 build_chapter.py c01.json --no-media` checks the shot list without touching any clip (fast).
- `python3 make_docs.py` rewrites `TEMPLATES.md` (the full parameter list).

The builder prints **warnings**: a gap between shots, a shot longer than 6 s (rule 22), a clip shorter than its shot (rule 28), a parameter name it does not know (a typo). Read them.

## 2. Folder map

| file | job |
|---|---|
| `build_chapter.py` | shot list JSON -> HyperFrames project (one chapter = one project) |
| `blocks/*.py` | the templates (one file each) |
| `lib/` | style.css (from v9), blocks.css, runtime.js (the v9 animation helpers), fonts, hf_template |
| `render_chapters.sh` | renders chapters with hash skipping, then joins them (plumbing from the Video 01 pipeline) |
| `mix_audio.py`, `sfx_voices.py` | builds the sound-effect bed from `sfx_events.json` and mixes it under the narration |
| `mux.sh` | loudness (about -14 LUFS) and mux, same chain as v9 |
| `TEMPLATES.md` | all templates and parameters (auto-made) |
| `demo/` | the demo: North Atlantic section of v9 rebuilt from JSON, compare frames, gallery of all variants |

## 3. The chapter JSON

```json
{
  "key": "c01",
  "title": "Chapter 1 North Atlantic",
  "words": "narration_words.json",
  "audio_offset": 33.6,
  "clips_dir": "clips",
  "duration": 27.6,
  "fade_out": 0.5,
  "res": 720,
  "shots": [ { ... }, { ... } ]
}
```

| field | meaning |
|---|---|
| `key` | chapter name. The project is written to `work/<key>/`. |
| `words` | the narration words file (the ElevenLabs word list: `[{"w":"Say","start":0.16,"end":0.32}, ...]`). |
| `audio_offset` | seconds of the narration file where this chapter starts. Chapter time = narration time - `audio_offset`. Use 0 if each chapter has its own audio file. |
| `clips_dir` | folder for clip files named in the shots (relative to the JSON file). |
| `duration` | length of the chapter in seconds. Optional if the last shot has `end`/`dur`. |
| `fade_out`, `fade_in` | optional black fade in seconds. |
| `res` | 720 (drafts, default) or 1080 (final). Same as the `--res` flag. |

### One shot

```json
{ "id": "zero", "template": "number_clip", "variant": "right",
  "start": "w117",
  "clip": { "file": "t2_12_pack_ice_edge.mp4", "in": 0.0, "push": [1.0, 1.08, "30% 50%"],
            "jumps": [ { "at": "@zero", "scale": 1.2 } ] },
  "params": { "kicker": "Near the ice", "number": "0°C", "number_at": "w123" },
  "sfx": [ { "cue": "click", "at": "w123", "gain": 0.4 } ],
  "ambience": { "cue": "wind", "gain": 0.3 } }
```

| field | meaning |
|---|---|
| `id` | short unique name (letters, numbers, `_`). |
| `template`, `variant` | which block and which look. If `variant` is missing, the first variant is used. |
| `start` | when the shot starts. A **number = seconds in the chapter**. Or a word: `"w117"` (see below). |
| `end` / `dur` | optional. By default a shot ends where the next shot starts (like v9: cuts on the first spoken word). The last shot needs `end`, `dur`, or the chapter `duration`. |
| `clip.file` | video file. Trim with `in` (start second inside the file). The builder cuts and conforms it (1280x720 or 1920x1080, 30 fps, no grade, no grain). |
| `clip.push` | `[from, to, "origin"]` slow zoom. Every template has a good default. `null` = no push. |
| `clip.jumps` | list of instant zoom steps `{ "at": time, "scale": 1.2 }`. |
| `params` | the template's own settings (see TEMPLATES.md). |
| `sfx` | **adds** sound cues: `{ "cue": "click", "at": time, "gain": 0.5 }`. `"sfx": false` removes the template's own default sounds. |
| `ambience` | a bed under the whole shot: `{"cue":"wind"|"ocean"|"bubbles"|"icecrunch"|"heli","gain":0.3}`. |

### Time values

Everywhere a template says "time spec" you can write:

| you write | meaning |
|---|---|
| `0.5` (a number) | 0.5 s **after the shot starts** (inside `params`/`sfx`/`jumps`) |
| `"w123"` | the start of word number 123 in the words file (same numbers as `timing.py` in v9) |
| `"w123e"` | the end of word 123 |
| `"@zero"` | the first time the word "zero" is spoken after the shot starts. Phrases work: `"@pass out"`. Second time: `"@zero#2"` |
| `"t38.3"` | an exact chapter time |
| `"end"`, `"start"` | the shot's end or start |
| add or subtract | `"w123-0.05"`, `"@zero+0.2"`, `"end-0.5"` |

The rule from v9 stays: **a cut sits on the first spoken word of its line, and text or icons appear on the word they show.**

## 4. The templates

All templates have 2-3 variants so chapters do not look the same. Full parameter lists are in `TEMPLATES.md`. Gallery pictures of every variant: `demo/gallery_1.jpg` ... `gallery_8.jpg`, icons and silhouettes: `demo/gallery_icons.jpg`.

| # | template | variants | use it for (rule) |
|---|---|---|---|
| a | `number_clip` | `right`, `center_bars`, `left_stack`, `strike_swap` | a number on a clip of the danger (rules 2, 15a). `count` animates a number (0 -> -1.8). `strike_swap` strikes out the wrong number and shows the true one. |
| b | `lower_third` | `italic_word`, `two_part`, `kicker_line` | one italic word or a joke on a clip (rules 4, 15b). |
| c | `extinct_plate` | `right`, `center`, `left` | gold plate: EXTINCT + date (rules 6, 15c). `word` can be another word, e.g. UNKNOWN. |
| d | `title_card` | `center_bars`, `left_plate`, `minimal` | chapter name + date, whoosh + thud (rule 52). |
| e | `stick_timer` | `gasp`, `hand`, `lights_out` | the cold chain on the timer bar: 1 min, 10 min, 30 min (rules 3, 14). `labels` changes the bar for heat, thirst, salt. |
| e | `stick_rope` | `rope_slip` | thrower in a boat, rope arcs over, slips away: "can't hold it". |
| e | `stick_water` | `sea`, `ice` | treading water + beats: "you", crossed-out items (NO BOAT, NO WETSUIT), "100 yards" to shore. Beats are a list. |
| e | `stick_gag` | `text_right`, `icon_pair` | generic gag: stick + number + icon (+ timer). 25 built-in icons (the gallery `demo/gallery_icons.jpg` shows all of them). |
| f | `scale_ruler` | `silhouette`, `water`, `clip` | scale picture with a true-to-scale ruler (rule 54). |
| g | `problem_counter` | `corner_badge`, `center_line`, `pips` | "problem one / problem two", the deciding one in gold (rule 55). |
| e | `stick_land` | `grass`, `snow` | the figure falls from the top and lands on dry ground instead of water: soft thud, dust puff, label on its word. |
| e | `stick_walk` | `channel`, `bridge` | the figure walks across a dry crossing (valley between two cliffs, or a flat land bridge) with two caps labels, a label on its word and an italic result word. |
| h | `tier_board` | `roadmap`, `drop`, `final`, `final_wide` | empty board with ALL chapter tiles named (rules 43, 58); the tile drag-and-drop on the verdict word (rule 7), optionally with a NEW tier row sliding in first (`add_tier_at`, the "Days" row); the finished board with a camera move, a glowing row and lifted tiles (`final`), or the whole board fixed (`final_wide`). |
| i | `map_clip` | `baked`, `labeled`, `gauge` | plays a pre-baked map mp4; optional pin + name + date line + sea-level gauge in style C (rules 1, 18-21). Extra overlays on any variant: `measure` (gold distance bar), `inset` (world map with the Ice Age ice sheets, rule 18), `polar` (rings by latitude + pin by lat/lon on a south-polar bake). |
| k | `outro` | `question`, `card`, `end_screen` | "Do you agree?" over the dimmed finished board (or a plain card), then the 12 s end screen: 2 video slots, subscribe circle, music only, fade to black. |
| l | `text_card` | `word`, `pair`, `line`, `number`, `number_left` | a text beat with no clip (dark textured card): used to split a long line into two cuts. Counts as its own template for rule 16. |
| j | `clip_plain` | `push`, `pull`, `jump` | full-bleed clip, trim, slow push, optional zoom step. |
| - | `black` | `hold` | the silent black drop (rule 30). |

### Examples

Number counting from 0 to -1.8:
```json
{ "id": "n1", "template": "number_clip", "variant": "right", "start": "w125",
  "clip": { "file": "frazil.mp4" },
  "params": { "kicker": "The water", "number": "0", "count": { "from": 0, "to": -1.8, "decimals": 1, "dur": 1.2, "suffix": "°C", "at": "@zero" } } }
```

Cold chain, same bar every time:
```json
{ "id": "k1", "template": "stick_timer", "variant": "gasp", "start": "@first minute",
  "params": { "kicker": "Cold shock", "number": "1", "unit": "minute", "line": "can't control your breathing", "line_at": "@control" } }
```

Crossed-out items and distance in one shot:
```json
{ "id": "rules", "template": "stick_water", "variant": "sea", "start": "w87", "end": "w100",
  "params": { "beats": [
    { "kind": "you", "label": "you" },
    { "kind": "items", "at": "w90", "items": [ { "icon": "boat", "label": "NO BOAT", "at": "w91" }, { "icon": "wetsuit", "label": "NO WETSUIT", "at": "w93" } ] },
    { "kind": "distance", "at": "w94", "label": "100 yards", "label_at": "w95" } ] } }
```

Scale picture (rule 54): `length_m` makes the animal exactly that long next to a 1.75 m figure.
```json
{ "id": "size", "template": "scale_ruler", "variant": "silhouette", "start": "@as long as",
  "params": { "animal": "shark", "length_m": 6, "name": "Great white shark", "ruler_at": "@six metres" } }
```
Built-in silhouettes: `shark`, `orca`, `bear`, `mammoth`, `leopard_seal` (3 m), `crocodile` (6 m). Your own: `"svg": "<path .../>"` (drawn in a 1000-unit-wide box, baseline at y=0, facing right). On a clip, use variant `clip` and tell it where the animal is: `"span": {"x0":150,"x1":1180,"y":120}`.

Problem counter:
```json
{ "id": "p1", "template": "problem_counter", "variant": "corner_badge", "start": "@one problem",
  "clip": { "file": "swimmer.mp4" }, "params": { "n": 1, "title": "the cold" } }
{ "id": "p2", "template": "problem_counter", "variant": "center_line", "start": "@second problem",
  "clip": { "file": "empty_sea.mp4" }, "params": { "n": 2, "title": "the food", "decider": true } }
```

Roadmap board (all chapter tiles named) and the verdict drop:
```json
{ "id": "road", "template": "tier_board", "variant": "roadmap", "start": "@Okay", "end": "+5",
  "params": { "tiles": [ {"name":"North Atlantic","image":"thumbs/c01.jpg"}, {"name":"Southern Ocean","image":"thumbs/c02.jpg"} ] } }
{ "id": "verdict", "template": "tier_board", "variant": "drop", "start": "w177", "end": "end",
  "params": { "tile": {"name":"North Atlantic","image":"thumbs/c01.jpg"}, "tier": "Minutes", "drop_at": "@Minutes",
              "placed": [], "n_total": 11 } }
```
`n_total` more than 6 switches to a compact board so that all tiles fit. Pass `placed` (tiles from earlier chapters, each with its `tier`) so the board grows chapter by chapter.

Map with overlays (only for a **clean** bake; the v9 map bakes already contain pin, name and date line, so use `baked` for those):
```json
{ "id": "map", "template": "map_clip", "variant": "gauge", "start": 0,
  "clip": { "file": "maps/bering_clean.mp4" },
  "params": { "gauge": { "from": 0, "to": -120, "at": "@four hundred", "dur": 1.7, "x": 930, "y": 150, "label_ft": "(-400 ft)" },
              "date": "Sea level -120 m (-400 ft)", "date_at": "@four hundred" } }
```

### Spliced narration inserts (extra recorded lines)

A line recorded later (for example the kelp line in chapter 3) is cut into the chapter at a word border:
```json
"inserts": [ { "id": "kelp", "audio": "../voice/insert_kelp.mp3", "words": "../voice/insert_kelp_words.json", "after_word": 986 } ]
```
The insert goes in after word 986 (in the middle of the gap to the next word, or at `"cut": seconds`). Every later word moves later by the insert length, so all `"w123"` and `"@word"` times in the same chapter stay right. The insert's own words are `"kelp.3"` (start of its word 3), `"kelp.3e"` (end), `"kelp.end"`; text search `"@Some scientists"` also finds them. The chapter `duration` is the narration length WITHOUT inserts (the builder adds them). `sfx_events.json` carries an `inserts` list and `mix_audio.py` cuts the audio in at the same point (12 ms fades, level matched to the voice before the cut).

### Text cards and long lines

To split a long line into two cuts without a second clip (a clip is never used twice, not even as a crop): a second map moment, a stick gag beat, or `text_card` (no clip, dark card). `"card": true` in a shot, with no clip, does the same for `lower_third` and `number_clip`.

### Plan tools

`plan_tools.py refresh PLAN_DIR` rebuilds every chapter JSON in a plan folder (no media) and writes the real shot lengths, video times and spoken lines back into each shot's `plan` block; `plan_tools.py audit PLAN_DIR > audit.md` writes the audit (shots, average, longest, wow and joke beats, HERO gaps, rule 16).

## 5. Sound

Every template adds its own default sound cues (number thud, X click, strike scratch + ding, gasp, rope swoosh, stamp, tile click + drop thud ...). They are written to `work/<key>/sfx_events.json` as `{ "t", "cue", "gain" }`.
`mix_audio.py` makes the sounds with the same synthesised voices as v9 and mixes them under the narration slice (SFX about 9 dB under the voice). A music bed can be added with `--music file.wav --music-db -20`.
Cue names: thud, thud_soft, title, stamp, click, tick, tok, swoosh, swoosh_rope, scratch, ding, ding_hi, ding_low, gasp, splash, downsweep, slide_down, icecrunch, heli, wind, ocean, bubbles.
The black drop template adds no sound: silence is part of the joke (rule 30).

## 6. The demo and the proof

`demo/natlantic.json` rebuilds v9 from 33.6 s to 61.2 s (map, 0 C, -1.8 C strike, slush, 1 / 10 / 30 minute gags, rope, EXTINCT) using **only** templates and the v9 clips and audio. `demo/tier.json` rebuilds the tier drop (61.2 s to 66.4 s).
Side-by-side frames (v9 on the left, template build on the right): `demo/compare_*.jpg`. Make them again with `demo/make_compare.py`.
`demo/gallery.json` has one shot for every variant of every template (45 shots, gap templates included); `demo/gallery_sheets.py` makes the contact sheets `gallery_1.jpg` ... `gallery_8.jpg` and `gallery_icons.jpg` (all icons and silhouettes). Thumbnails for the boards: `make_thumbs.py` (not committed, media); the world inset data: `make_world_inset.py`.

## 7. Known gaps

- The map bakes themselves are a separate job. `map_clip` plays any mp4. The old v9 / first Video 01 bakes already contain pin, name and date line, so the overlays are meant for clean bakes (without labels).
- `polar` and `measure` overlays need the position of the bake in the frame (`center`, `two_r`, bar end points); they are exact only when the bake has a fixed camera.
- The world inset uses Natural Earth 110m land and hand-placed, approximate ice sheets.
- Only 1280x720 design space; 1080 is made by scaling the stage (works, tested with snapshots).
- Silhouettes are simple shapes. For a better look, give your own `svg` or use the `clip` variant.
- The end screen only draws the layout; YouTube puts the real video and subscribe elements on top.
