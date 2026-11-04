You are building animated battle-map scenes for a faceless YouTube documentary: "<GENERAL>'s Top 3 Legendary Tactical Moves" (Tactical Genius style: parchment shaded-relief maps, NATO-ish unit blocks, sweeping arrows, slow camera moves, plaques/portrait stakes, captions and stat cards). Project: /home/user/battle-maps/<name> (must stay at this absolute path).

Read first:
- /home/user/battle-maps/HANDOVER.md sections 5 and 6 (pipeline + lessons learned — follow them).
- /home/user/battle-maps/<name>/SCENES.md (scene list, projection, colours, media) and <name>/script.md (the [MAP: id | notes] tag of each paragraph is the visual brief; the text after it is the narration).
- The engine: <name>/lib/battle.js + battle.css (read fully; B.at(para, phrase) gives the time a phrase is spoken — now sentence-accurate; B.method(t, until, {rowT, dim}) shows the Morgan method card) and the reference scenes in morgan/scenes-src/ (reuse their helpers — copy, don't reinvent): hook2.js / ending.js (bio card, portrait stake, glowing markers), saratoga2.js (range ring, crosshair target, cross-out, muzzle-flash fire line, rifleman dots, redoubt, tree), cowpens2.js / cowpens3.js (battle lines, volleys, encirclement ring, stat rows timed to speech), cowpens1.js / guilford1.js (regional chases, rivers from Natural Earth), guilford2.js (three-line battlefield). Water overlays: morgan/assets/*_water.png.
- Timing is in <name>/audio/timing.json (voice already recorded — do NOT regenerate it). Basemaps are already baked in <name>/assets/*.jpg + *.json — do not re-bake.

Workflow per scene:
1. Write <name>/scenes-src/SCENE.js.
2. python3 tools/build_scene.py SCENE BASEMAP FIRST_TAG LAST_TAG (from <name>/).
3. cd scenes/SCENE && hyperframes lint . ; then hyperframes snapshot . --at <one time per paragraph + key moments>. USAGE BUDGET: combine the snapshots into ONE contact sheet (ffmpeg/PIL tile, e.g. 4x3 at 640x360) and Read that single image instead of each snapshot; at most 3 review rounds per scene, then render. Only open a full-size snapshot to check a specific problem. Fix overlapping labels, units bunched together, things off-screen, black edges (camera must stay clamped inside the 2880x1620 map), text too small to read at 1080p, anything contradicting the narration. Iterate until it looks like a professional documentary map. Historical accuracy matters: place units, rivers and places at their real positions (use your knowledge; Nominatim works for place coordinates; Overpass FAILS through the proxy — use Natural Earth 10m rivers/lakes instead). Battlefield maps may exaggerate spacing slightly for readability.
4. Render: cd scenes/SCENE && hyperframes render . -o renders/SCENE.mp4 (run it in the background, check the log for "Render complete"; other agents render at the same time on this 4-core machine, so run only ONE render at a time yourself). Rendering is ~3-5x real time. Then verify the mp4 duration with ffprobe matches the scene duration printed by build_scene, and extract 3-4 frames with ffmpeg to eyeball.

Style rules: Americans = side "carth" (blue), British = side "rome" (red). Every paragraph should have motion (camera move, arrows, units moving) — no static 20-second holds. Captions/labels in CAPS, short. Title card at the start of each Move (B.title). Keep date scroll updated (B.date). Use portrait stakes (B.portraitStake with assets/media/*_head.png + flag us_flag_13star.png / gb_flag_1707.png) for commanders where the narration names them. Portraits and flags should already be in <name>/assets/media/ (the image agent runs BEFORE the map agents); if one is missing, use a plaque (B.plaque).
You may add small generic helpers to lib/battle.js/css if truly needed, but other agents use the same files concurrently: only ADD new functions (never change existing signatures/behaviour), and re-read the file right before editing.

Do NOT git commit or push (the main session does). Do not touch audio/, script.md, or other agents' scenes. When finished, reply briefly: scene → render path, duration, and anything you could not do.

DETAILED MAP STYLE — MANDATORY (owner-approved; HANDOVER §9). Reference scene: /home/user/battle-maps/thomas/scenes-src/demo3.js (read it first; copy its patterns). All helpers are in lib/battle.js:
- Battlefield scenes (the main fight of each Move):
  - Opening: `B.satIntro({ base: BASEMAP, cam: [cx, cy, s<=1], title, date })` at the start of the FIRST battlefield scene of each Move (needs `python3 tools/sat.py --intro BASEMAP`; the main session or you run it once per basemap). Start B.camera at the same [cx, cy, s].
  - `B.tilt([[t, rotX, scale, dur], ...])` (≈20° normally, ≈30° at the decisive moment, back to ≈15°) + `B.scorched(t)`.
  - Ground: `B.terrain(fields)` with the period farm fields (from Library of Congress / NPS battlefield maps; woods everywhere else), `B.road(pts, w, dash)` for period roads, `B.river` for creeks, `B.scaleBar(x, y, metersPerPx)` (metersPerPx from assets/BASEMAP.json).
  - `B.territory(line, { west, t, labels })` for the ground each side holds; on every retreat call `.retreat({ to, loser, tFade, tSpread, lost: [text, x, y, until] })` — the loser's colour FADES off the lost ground first, then the winner's colour spreads.
  - Units: `B.brigade({ id, side, name, x, y, col, rot, t })` (line = long thin block, column = deep block; brigade level where the narration zooms in), `B.march`, `B.brigadeLoss`, `B.flee(pts, t)` for routed fragments, `B.trail`. NO soldier figures (owner rejected them).
  - Fire: `B.volley(pts, t, reps, gap)`, `B.burst(x, y, t)`, `B.puff`, `B.cannon(x, y, side, t)` for batteries.
- Every scene where it fits:
  - HUD: `B.clock([[t, "11:00"], ...], { date })` in battle scenes (hits the exact narrated time), `B.minimap(src, caption, shows)` (image from `python3 tools/minimap.py BASEMAP WIDER_BASEMAP TOWN LAT LON`), `B.compass(t)`, `B.legend(B.legendItems(), t, until)` once per Move.
  - `B.bars(title, rows, t, until)` for strength comparisons, `B.note(kicker, text, t, until)` for orders/telegrams, `B.belief(title, quote, t, until)` for "what the enemy believed".
  - `B.pip(src, title, t, until, { fit: "contain" })`: framed portrait (assets/media/*_head.png) or painting (archive/*.jpg) popping in top-left whenever the narration names a commander or a painting — the map keeps moving underneath.
  - Enemy commanders: `B.portraitStake({ ..., side: "rome" })` for the red ring/tag.
Rendering is ~6x real time in this style: queue renders one at a time (`flock /tmp/render.lock hyperframes render ...`).

Keep helpers local to your scene JS rather than editing lib/battle.js. Keep your final report short (under 200 words).

YOUR SCENES:
