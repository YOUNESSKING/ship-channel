# How we make animated maps (handover for another channel)

This is the method behind the animated maps of the battle-maps channel, written so another agent can reuse it for **any**
topic (history, travel, geography, trade routes, expeditions, explainers). Nothing here is war-specific unless marked *(optional)*.
Everything is code: maps are HTML pages animated with GSAP and rendered to MP4 frame by frame with HyperFrames, timed to a
narration file. Same input = same video, every time.

The kit next to this file (`map-kit/`) contains the engine, the tools, a sample basemap and a tested example scene.

---

## 1. What a finished map looks like (the style)
- **A real place, real terrain:** shaded relief baked from open elevation data (mountains, valleys, coasts), never a stock map.
  Two grades: parchment (`<map>_hd.jpg`) and the dark "documentary" grade (`<map>_hd_ref.jpg`, our default since Oct 2026).
- **Geography layer on top:** rivers, lakes, forests and only the **big** towns, small clean labels that never collide,
  names of the period when the story is historical.
- **A living map:** slow cloud shadows drifting over the land, a gentle shimmer on rivers, a scale bar and a north arrow.
- **Camera:** flat 2D (no 3D tilt, no globe), slow eased moves: a wide establishing shot, a push-in to the place the narrator is
  talking about, a pull-out for the result. One wide -> close -> wide arc per section.
- **Things happen on the spoken word:** a label appears when its name is said, a route draws itself while the narrator describes
  the journey, a number card slams in on the number. Never more than ~4 s without something changing on screen.
- **On-screen text:** Oswald (condensed, bold) for labels/cards, Special Elite (typewriter) for the date scroll; captions
  bottom-centre, title cards centre, date scroll top-left, credits bottom-right (small).
- **Finish:** vignette + film grain over everything, 1920x1080, 30 fps.
- **Colours:** two story sides = blue `#1f4fc4` / red `#c4121f` (counters, arrows); muted line colours `#2c57b7` / `#bc2528`;
  neutral grey `#77746c`; gold `#c9b48a`; text `#f7f3ea`. For a non-war channel pick your own pair, but keep ONE palette per channel.

## 2. Tools you need
| What | Install |
|---|---|
| HyperFrames (HTML -> MP4 renderer with headless Chrome) | `npm install -g hyperframes` then `hyperframes browser ensure` |
| ffmpeg | `apt-get install -y ffmpeg` |
| Python | `pip install numpy pillow scipy scikit-image soundfile kokoro-onnx` (+ `pysheds affine` only for rivers-from-terrain) |
| Narration timing (optional TTS) | Kokoro: `kokoro-v1.0.onnx` + `voices-v1.0.bin` from github.com/thewh1teagle/kokoro-onnx releases |
| GSAP | already in `vendor/gsap.min.js` (renders can't load CDNs: everything must be a local file) |
Network: the terrain tool downloads elevation tiles from `s3.amazonaws.com/elevation-tiles-prod` (open data, no key).

## 3. Folder layout of a project
```
project/
  script.md            narration, one paragraph per beat, each starting with a tag: [MAP: id | what the map shows]
  audio/timing.json    start/end of every paragraph AND every sentence (from tools/narrate.py)
  assets/<map>.jpg + <map>.json     baked relief + its projection (zoom, origin_world_px, metres per px)
  assets/media/        overlays (geo layer, territory/region PNGs, flags, photos, rivers json)
  assets/fonts/, assets/grain.png
  lib/                 the engine: battle.js (core), fx.js, gg.js, living.js, battle.css (+ globe/flyover/board = experiments)
  scenes-src/<scene>.js   ONE file per map scene: the only thing you write per video
  tools/               bake.py, bake_hd.py, build_scene.py, render_all.sh, ...
  scenes/<scene>/      generated, renderable HyperFrames project (don't edit; rebuild)
```

## 4. The pipeline, step by step
### 4.1 Narration and timing (the clock everything hangs on)
1. Write `script.md`: sections `## NAME`, paragraphs starting with `[MAP: scene-para-id | visual notes]` (or `[ARCHIVE: ...]` for photos).
2. `KOKORO_DIR=/path/to/models python3 tools/narrate.py am_michael` -> `audio/voice.wav` + `audio/timing.json`.
   It voices **one clip per sentence**, so `timing.json` has `sents: [[charStart, t0, t1], ...]` per paragraph. That makes
   `B.at("para", "phrase")` land on the right word (proportional estimates drift by seconds).
   Pronunciation: check a name with `k.tokenizer.phonemize("Name", "en-us")`, add respellings to the `SAY` dict.
   Using a human voice-over instead: write `timing.json` yourself (or with a forced aligner) in the same format.
3. A **scene** = one unbroken run of `[MAP]` paragraphs (an `[ARCHIVE]` paragraph in between = cut to photos = new scene).

### 4.2 Terrain (the basemap)
```
python3 tools/bake.py NAME LAT LON ZOOM [EXAGGERATION]   -> assets/NAME.jpg (2880x1620) + assets/NAME.json
python3 tools/bake_hd.py NAME [EXAG]                    -> assets/NAME_hd.jpg (parchment) + assets/NAME_hd_ref.jpg (dark grade)
```
- The image is 2880x1620 = 1.5x the screen, so the camera can zoom in and still be sharp (`bake_hd` builds it from one zoom level
  deeper: 5760x3240 shown at 2880x1620).
- Zoom guide (Web-Mercator tiles): 6-7 = a country / large region, 8-9 = a province, 12-13 = a city and surroundings,
  15-16 = a town / a few km (16 is upsampled from 15). Exaggeration: 2 for mountains, 4-6 for gentle hills.
- Colours by height (lowland -> highland -> peaks), sea coloured by depth, coastline ink line, grain. The NAME.json keeps the
  projection: `zoom`, `origin_world_px`, `meters_per_px`.
- **Projection** (any lat/lon -> map px), used in every scene:
  `G = GG.proj(zoom, origin_x, origin_y)` then `const [x, y] = G(lat, lon)`
  (`x = (lon+180)/360 * 256*2^z - ox`, `y = (1 - asinh(tan(lat))/pi)/2 * 256*2^z - oy`).

### 4.3 Geography layer (rivers, lakes, forests, towns)
- `python3 tools/fetch_osm.py NAME "S,W,N,E"` -> OpenStreetMap features (Overpass API; credit "(c) OpenStreetMap contributors").
  If Overpass is blocked (it is from our cloud machine), use **Natural Earth** 10m rivers/lakes (public domain) or trace rivers
  from the terrain itself: `python3 tools/make_rivers_dem.py NAME` (water flows downhill).
- `python3 tools/make_geo_layer.py NAME ref "SKIP1,SKIP2"` -> `assets/media/NAME_geo_ref.png` (transparent, 2x) +
  `NAME_rivers.json` (for the shimmer). Rules: only big towns (population threshold), small labels, period names, labels never
  collide, names you will animate yourself go in SKIP. Put this layer ABOVE any colour fill (else it turns pink).
- Place coordinates for single labels: Nominatim (`nominatim.openstreetmap.org/search?q=...&format=json`), polite User-Agent.

### 4.4 Region colours *(optional: "who/what is where")*
- Coloured regions = a transparent PNG per date/state (`tools/make_control.py` pattern: polygons in map px, alpha 0.46 inside,
  up to 0.66 at the border, clipped to land with a land mask from `tools/make_land.py`), placed with
  `B.image(png, 0, 0, 2880, 1620, {t, dur})` and `el.style.mixBlendMode = "multiply"` so the relief shows through.
  Cross-fade to the next PNG (1 s) when the narration moves to a new date.
- Lines between regions: `K.front({ pts, sideA, sideB, width: 15, glow: 0.47, t, dur })` (two-colour glowing band);
  trace them from a region PNG with `tools/make_front_lines.py`. Wide shots = fills; close-ups = lines only (fills hide detail).
- Works the same for non-war uses: language areas, empires, climate zones, sales territories.

### 4.5 Write the scene (`scenes-src/<scene>.js`)
Start from `scenes-src/example_route.js` (tested). Skeleton:
```js
const B = Battle(); const { at, P: PS } = B; const END = B.T.duration;
const K = FXK(B); const GG = GGK(B); const G = GG.proj(9, 77312, 42277);   // from assets/<map>.json
const T_X = at("para-1", "spoken phrase");                                // beats = times of spoken words
B.camera([[0, 1440, 810, 0.70], [T_X, x, y, 1.8], [END, x, y, 2.0]]);     // [t, centre x, centre y, scale]
B.city("NAME", ...G(lat, lon), { size: 28, t: T_X });
B.arrow({ side: "white", pts: [A, B2, C], width: 18, t: T_X, dur: 3 });   // draws itself
B.caption("SHORT CAPS TEXT", T_X, T_X + 4);
B.finish();
```
Build it: `python3 tools/build_scene.py SCENE BASEMAP FIRST_PARA LAST_PARA` (copies engine, assets, timing into `scenes/SCENE/`).

### 4.6 Check before rendering (always)
```
cd scenes/SCENE && hyperframes lint .                 # 0 errors (the nested-structure warning is normal)
hyperframes snapshot . --at 2,6,10,14,...             # one time per paragraph + every key moment
```
Look at the contact sheet (`snapshots/contact-sheet.jpg`), not 30 single frames. Check: overlapping labels, things off-screen,
black edges (camera outside the map), text too small at 1080p, units/markers bunched, anything that contradicts the narration.
At most 3 fix rounds per scene, then render. `tools/phrase_t.py SCENE "para:phrase"` prints when a phrase is spoken.

### 4.7 Render
`bash tools/render_all.sh "SCENE BASEMAP FIRST LAST" ["..."]` renders scenes **one at a time**, detached (survives the tool shell),
logs to `logs/render_all.log`, writes `logs/render_all.done`. Speed: ~3-8x slower than real time on 4 CPU cores. Check
`scenes/SCENE/render.log` for "Render complete" and the mp4 duration (ffprobe) = the scene duration from build_scene.
Then cut the renders together with your photo/archive segments and the audio (ffmpeg concat + mix; loudness -14 LUFS for YouTube).

## 5. Engine reference (what you can call)
**Core (`B = Battle()`, lib/battle.js)** - time helpers: `B.P(para)` start, `B.end(para)`, `B.at(para, phrase, offset)`.
Camera: `B.camera([[t, x, y, scale], ...])` (eased; scale 0.667 = whole map). Map: `B.image(src,x,y,w,h,{t,dur,until})`,
`B.river(pts,width)`, `B.line(pts,{dash,width,t,dur})`, `B.highlight(pts,t,until)`, `B.label(text,x,y,{cls,size,t,until})`,
`B.city(name,x,y,{size,left,t,until})`. Movement: `B.arrow({side,pts,width,t,dur,until})`, `B.unit({...})` + `B.move(id,t,dur,x,y)`,
`B.hideUnits`, `B.grey`. Screen text: `B.caption(text,t,until)`, `B.title(kicker,name,sub,t,until)`, `B.stat(rows,t,until)`,
`B.date(text,t,until)` + `B.showDate(t)`, `B.bubble(text,x,y,t,until)`, `B.plaque({...})`, `B.bio({photo,name,rows,rowT,t,until})`
(full-length photo cut-out + info card), `B.portraitStake({img,flag,name,x,y,t})`, `B.dim(t,until)`. Weather: `B.snow`, `B.fog`.
**Helpers (`GG = GGK(B)`, lib/gg.js):** `proj`, `pin`, `lbl`, `tagbox`, `stamp` (text slams in), `card`, `polygon`, `road`, `water`,
`layer`, `night`/`dawn`/`sun`, `arc`, `flash`, `whiteFlash`, `ship`, `method` (list card that lights one line at a time).
**Effects (`K = FXK(B)`, lib/fx.js):** `target` (pulsing rings), `smoke`, `shake`, `badge` (round photo badge with name),
`counter` (unit block with icon/flag/size), `front`, `frontTint`, `territory`, `lose`, `shift`, `grid`, `night`;
*(optional, war)* `gun`, `impact`, `aircraft`, `bombRun`, `casualties`.
**Living map (`L = LivingK(B)`, lib/living.js):** `L.clouds({n, opacity})`, `L.shimmer(riverPolylines)`, `L.scaleBar(metresPerPx)`, `L.north()`.
Sound cues: scenes can call `SFX(kind, t)`; a mixer reads them later (our kit: whoosh only on the 2-3 biggest camera moves, hit on
slams/stamps, tick on counters).

## 6. Rules that make it look professional (learned the hard way)
- Everything time-based goes on the ONE paused GSAP timeline (`B.tl`); never use setTimeout / real time / DOM measuring inside
  callbacks (pre-compute paths). That's what keeps renders deterministic.
- All assets local (fonts via @font-face inside the page, GSAP from vendor/): headless Chrome can't load CDNs while rendering.
- Keep the camera inside the 2880x1620 map at every key (else black edges).
- Text: CAPS, short, readable at phone size; big towns only; never two labels on top of each other; remove a label when the
  camera leaves it.
- Something new every 2-4 s (camera move, label, arrow, card). A static map for 10+ s loses viewers.
- First second of a video: a map with things already moving (never a photo or a black screen).
- Start every move from a readable framing: show the whole area, THEN push in.
- One promise per scene: the map shows exactly what the narrator says, at the moment he says it.
- Render scenes one at a time; long renders die if started from a short-lived shell (use render_all.sh). Cloud machines reboot:
  make every long job resumable (skip finished outputs).
- Licences: terrain = open data (credit "Terrain: Mapzen / AWS Terrain Tiles"), OSM = ODbL (credit on screen),
  Natural Earth = public domain. Photos: only public domain / CC0 / CC BY / CC BY-SA with credits; never NC/ND.

## 7. Effort
A 1-2 minute map scene: ~30-60 min to write + 2-3 snapshot rounds, then ~10-20 min to render. A full 16-minute video has
~10 scenes; with 2-3 agents writing scenes in parallel (each one only writes + snapshots, one renderer renders) it fits in a
few hours. Use a strong model for complex scenes, a cheaper one for simple overview maps.

## 8. Kit contents (`map-kit/`)
- `lib/`, `vendor/` - the engine (latest version, with sentence-accurate `B.at`).
- `tools/` - bake.py, bake_hd.py, make_land.py, fetch_osm.py, make_geo_layer.py, make_rivers_dem.py, make_control.py,
  make_front_lines.py, build_scene.py, render_all.sh (use without `--assemble`), scene_template.html, make_sheet.py, phrase_t.py,
  narrate.py, archive_shots.py (photo segments: 3D-depth moves, labels, date cards), fonts.
- `assets/` - fonts, grain, a sample dark HD basemap (`kursk_hd_ref.jpg` + json, central Russia, zoom 9).
- `audio/timing.json` - a 24 s fake timing for the example.
- `scenes-src/example_route.js` - tested generic example (journey Orel -> Kursk: title, labels, camera, self-drawing route,
  pulsing targets, captions); `examples/example_route_sheet.jpg` is its snapshot sheet.
- `examples/advanced_kursk_scene.js` - a full real scene (7 minutes of map: territory overlays, fronts, living map, camera
  choreography over 10 paragraphs) to copy patterns from.
Quick test: `python3 tools/build_scene.py example_route kursk_hd_ref intro-1 intro-2 && cd scenes/example_route && hyperframes snapshot . --at 2,9,14,20,23`
