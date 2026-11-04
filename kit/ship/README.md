# kit/ship: reusable ship assets (silhouettes, sinking animation, sea-floor maps, SFX)

The CLAUDE.md "Still to build" items, made once for every future video. Everything here is drawn or synthesized in-house:
no AI image generation, no downloaded art or sound. Heavy outputs (WAV, MP4, full-size map bakes) are git-ignored and can be
re-made with the scripts below. Dependencies: Python 3 with numpy, scipy, soundfile, Pillow, cairosvg (`pip install scipy cairosvg`),
Node 22 with the global `playwright` module, Chrome, ffmpeg.

| Piece | Make / re-make | Preview (committed) |
|---|---|---|
| Ship silhouettes (5 ships, side + top) | `node kit/ship/make_svgs.js && python3 kit/ship/make_pngs.py` | `preview/ships_sheet.png`, `preview/png/*.png`, `svg/*.svg` |
| Sinking animation + depth gauge | `bash kit/ship/sinking/make_preview.sh ["query"]` | `sinking/sinking_contact_sheet.jpg` (MP4 in `sinking/out/`, git-ignored) |
| Sea-floor map look | `python3 kit/ship/bathy/bake_bathy.py NAME LAT LON ZOOM --preview` | `preview/gulf_pensacola_preview.jpg`, `preview/bathy_palette_strip.jpg` |
| Ship SFX (49 files, 18 families) | `python3 kit/ship/sfx/make_sfx.py` (~40 s) | `sfx/listening_reel.mp3` + `sfx/reel_cues.txt`, `sfx/spectro_sheet.jpg` |

## 1. Ship silhouettes: `ships.js`

Five ships, each with a side profile and a top-down plan, drawn in feet from the published dimensions with public-domain US Navy
plans and photos used only as reference (NHHC, NavSource, HAER). Nothing is traced. They are simplified on purpose so they read
at 40-200 px on a map and still hold up at 1600 px in a cutaway.

| key | ship | length |
|---|---|---|
| `carrier` | Essex-class angled-deck carrier: USS Oriskany (CV-34) after SCB-27A / SCB-125A (hurricane bow, angled deck, starboard island, SPS-43 radar) | 911 ft |
| `battleship` | WWII fast battleship, Iowa-class style (3 triple 16" turrets, 2 funnels, 5"/38 twins) | 887 ft |
| `de` | Destroyer escort, John C. Butler class (two 5"/38 singles, one funnel) | 306 ft |
| `sub` | Fleet submarine, Gato / Balao (cut-down fairwater, 5"/25 deck gun, limber holes) | 312 ft |
| `liner` | SS United States (two winged funnels in red / white / blue, black hull, red boot-topping) | 990 ft |

Two paints:
- `paint: "side"` (default) is the **map-kit counter look**. The side colour (`col: "blue"` #1f4fc4, `"red"` #c4121f, `"grey"`, or any hex)
  is drawn with a cream keyline #f3eee2 on side views (like `G.ship`) and a light rim on top views (like va_kit `SHIPSVG`).
  It also gets the same coloured drop-shadow glow. Carrier flight decks are dark, with white landing lines.
- `paint: "livery"` uses realistic flat colours: Navy haze grey with red below the waterline, the liner's own colours, and a black sub.
  Use it for cutaways and the sinking animation.

```html
<script src="kit/ship/ships.js"></script>   <!-- defines window.ShipKit; in Node: require("./kit/ship/ships.js") -->
```
```js
ShipKit.svg("carrier", "top", { w: 120 });                       // SVG string; w = on-screen px of the ship's length
ShipKit.svg("liner", "side", { w: 900, paint: "livery" });       // other options: col, keyline (px), glow:false, flip:true, below:false, colors:{role:hex}
ShipKit.meta("carrier");                                          // feet: L, beam, draught, keel points, side/top extents (for animations)

// in a map-kit / HyperFrames scene, after const GG = GGK(B):
const S = ShipKit.map(GG, { tl: B.tl, posOn, pinS });            // posOn / pinS from va_kit (optional; pinS keeps a constant on-screen size)
const cv = S.pin("carrier", "top", 1450, 800, { w: 70, t: 2, rot: -30 });
const de = S.sail("de", [[900, 700], [1200, 760], [1500, 690]], 3, 6, 12, { w: 40, col: "red", wake: true });   // heading follows the path
S.sinkTop(cv, 9, { dur: 3 });                                     // on-map sinking: list, darken, settle, rings + bubbles; SFX("sink_whoomp", ...) if SFX exists
```
Standalone files: `svg/<ship>_<view>.svg` (livery) and `svg/<ship>_<view>_blue.svg` (map paint, no glow), 1200 px wide.

## 2. Sinking animation: `sinking/`

`sinking.js` (`ShipSink(stage, cfg)`) shows a side-profile ship floating, then the demolition charges flash along the waterline
and throw up spray. The ship settles stern-first, goes under, and lands upright on the seabed. On landing the gauge "lands"
(flash, gold ring, number pop), and a silt cloud and bubbles rise. Everything is a pure function of time on one GSAP timeline
(`window.__timelines.main`), so it seeks in any order, like map-kit scenes.

- **Gauge**: it reuses the `anim_gauge` "meter" idea (track, ticks, gold fill and dot, a count that lands with a flash and an
  expanding ring) in the channel's Oswald / cream / gold type. `anim_gauge.py` itself only runs inside the prehistory
  `build_chapter` context, so it could not be dropped in as-is. If the whole water column fits on screen (Oriskany, 212 ft),
  the gauge is a **true-scale ruler** in the world, and its ticks are the real depths next to the ship. For deep wrecks it becomes
  a fixed instrument and the camera follows the ship down. The readout is **KEEL DEPTH** (it starts at the draught, e.g. 31 ft, because that is true).
- **Parameters** (URL query or `window.SINK_CFG`): `ship`, `depth` (ft), `dur` (s), `mode` (`stern` / `upright` / `bow`), `pitch`
  (deg), `units` (`ft` / `m`), `title`, `sub`, `paint`, `col`, `charges=0`. In JS: also `scale`, `sinkStart`, `landAt`, `gaugeMax`, `kicker`.
- **Sound**: the page exports `window.__sink.cues` (kit SFX names + times: charges, groan, whoomp, creak, sonar pings, landing
  boom, swell then underwater beds). `make_preview.sh` mixes them on with `mix_cues.py`, as a preview mix only.

```bash
bash kit/ship/sinking/make_preview.sh                                                   # Oriskany, 212 ft, 7.5 s (default)
bash kit/ship/sinking/make_preview.sh "ship=liner&depth=180&dur=8&mode=upright&title=SS%20UNITED%20STATES"
```
Output: `sinking/out/sinking_preview.mp4` (with sound), `sinking/sinking_contact_sheet.jpg`.
In a video, use `sinking.html` as a HyperFrames composition. Copy `ships.js`, `sinking.js`, `gsap.min.js` and the Oswald fonts
next to it and fix the three script paths, or render it to a clip with `tools/render_frames.js`.

## 3. Sea-floor map look: `bathy/`

`palette.json` holds the bathymetry ramp: deep navy at 5000 m, a teal shelf at 30-150 m, and sand-tinted shallows and a sand
beach at the coast. Isobaths are drawn at 20/50/100/200/500/1000/2000/3000 m, and there is a soft sea-floor hillshade.
Land is muted in the battle-maps LIFT hue ((24,31,31) to (190,202,184), as in `bake_hd.py LIFT=1`), with a darker median so
the sea stays the hero. `bake_bathy.py` writes the same `NAME.jpg` (2880x1620) and `NAME.json` projection files as
`tools/maps/bake.py`. That means map-kit scenes, `make_control.py` overlays and the camera work unchanged: use
`out/NAME.jpg` as `assets/relief.jpg`. Tiles: AWS Terrarium (open data; credit line in the JSON). The cache is in `bathy/.tiles/` (git-ignored).

```bash
python3 kit/ship/bathy/bake_bathy.py gulf_pensacola 29.75 -87.0 9 --preview     # Mobile to Panama City, Mississippi delta, DeSoto Canyon
python3 kit/ship/bathy/bake_bathy.py oriskany_reef 30.04 -87.0 12 --preview     # close-up of the reef site
```

## 4. Ship SFX: `sfx/`

There are 18 families with 2-3 variations each: 48 kHz / 24-bit stereo WAV in `sfx/out/` (git-ignored), loudness-normalised
(levels in `sfx/levels.json`). Re-make them with `python3 kit/ship/sfx/make_sfx.py`. To re-make only some families:
`python3 kit/ship/sfx/make_sfx.py horn sonar reel`.

| family | files | use |
|---|---|---|
| `horn_close`, `horn_distant` | 3 + 3 | deep ship horn (v2 two-tone, v3 two short blasts); distant = air absorption + long echo |
| `hull_groan`, `metal_creak` | 3 + 3 | underwater hull stress; rivet / plate creak with pops |
| `sink_whoomp` | 3 | the hull goes under: whoomp + air release + rising bubbles |
| `charges_seq` | 3 | demolition charges as muffled underwater thumps in sequence (v2 distant, v3 rapid cascade) |
| `flood_rush` | 3 | flooding: inside the hull / heard underwater / a hatch bursts |
| `swell_bed`, `underwater_bed` | 2 + 2 | 60 s **seamless loops** (circular noise; modulators with whole cycles) |
| `sonar_ping` | 3 | subtle ping for the depth gauge |
| `dive_whoosh` | 3 | wet map / camera dive (splash, muffled down-sweep, bubble trail): not an airy whoosh |
| `number_land` | 3 | number-landing hit: low tonal boom (A1 / G1 / C2) with a water tail |
| `text_slam`, `strike_scrape` | 3 + 3 | heavy steel impact for cards; steel-edge scrape for strike-outs |
| `riser_4s`, `riser_8s` | 2 + 2 | tension builds with a hard stop (v2 adds hull groan) |
| `reveal_hit` | 3 | sub boom + steel clang + water tail (v3 dry) |
| `catapult_launch` | 2 | steam catapult: shuttle clank, rush, water-brake slam, hiss |

**Listening reel**: `sfx/listening_reel.mp3` (45 s, one variation of each, gaps between) and `sfx/reel_cues.txt` (what plays when).
`sfx/spectro_sheet.jpg` (`spectro_sheet.py`) is a quick visual check after a re-make. Credits: `sfx/SFX_CREDITS.md`
(in-house, no credit needed).

## Needs the owner's eye
- **Sound**: the battle-maps owner once rejected invented "ref" sounds (STYLE_LOCK 2c-5). This channel asked for its own
  engineered kit, so audition the reel before any sound becomes a default. The horn and the charges are the hardest to fake.
- **Silhouettes**: simplified drawings, not plans. Check the Oriskany island / mast and the elevator layout against NHHC photos
  before a close-up. For the sinking, the real ship's mast was cut down before scuttling, so a reef-accurate shot may want a mast-less variant.
- **Map look**: the navy / teal sea departs from the battle-maps rule "never navy/blue on day shots". This channel asked for it (CLAUDE.md wins);
  lock it with a test sheet. The Mississippi delta comes out speckled at z9 (marsh at about 0 m).
