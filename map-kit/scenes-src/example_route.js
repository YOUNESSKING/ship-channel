// EXAMPLE SCENE (generic, not war): a journey drawn across a region, timed to the narration.
// Basemap: assets/kursk_hd_ref.jpg (z9 dark HD relief, from bake.py + bake_hd.py). Paragraphs intro-1 .. intro-2 of audio/timing.json.
// Build: python3 tools/build_scene.py example_route kursk_hd_ref intro-1 intro-2
const B = Battle();               // engine: timeline (B.tl), camera, labels, arrows, cards, timing helpers
const { at, P: PS } = B;
const END = B.T.duration;
const K = FXK(B);                 // effects: pulsing targets, smoke, shake, counters, aircraft...
const GG = GGK(B);                // helpers: pins, label boxes, stamps, polygons, projection
const G = GG.proj(9, 77312, 42277);   // lat/lon -> map px; numbers = zoom + origin_world_px from assets/<basemap>.json

// ---------- beats: the moment each phrase is spoken ----------
const T_LEFT = at("intro-1", "left the old city"), T_STEPPE = at("intro-1", "two hundred kilometres");
const S2 = PS("intro-2"), T_RIVER = at("intro-2", "followed the river"), T_REACH = at("intro-2", "they reached Kursk");

// ---------- places ----------
const OREL = G(52.967, 36.069), KURSK = G(51.730, 36.193), FATEZH = G(52.090, 35.860), KROMY = G(52.687, 35.790);

// ---------- living map: slow cloud shadows, scale bar, north arrow ----------
const LV = LivingK(B);
LV.clouds({ n: 6, opacity: 0.22 });
LV.scaleBar(186.76); LV.north();   // metres per px from the basemap json

// ---------- camera: [time, x, y, scale]; scale 0.667 = whole 2880x1620 map, 2-3 = close-up; keep it inside the map ----------
B.camera([[0, 1440, 810, 0.70], [T_LEFT, OREL[0], OREL[1] + 120, 1.6], [T_STEPPE, 1350, 800, 1.05],
          [T_RIVER, (OREL[0] + KURSK[0]) / 2, (OREL[1] + KURSK[1]) / 2, 1.25], [T_REACH, KURSK[0], KURSK[1] - 80, 1.9], [END, KURSK[0], KURSK[1] - 60, 2.0]]);

// ---------- text on screen ----------
B.showDate(0.3); B.date("SPRING", 0.5);
B.title("PART 1", "THE ROAD SOUTH", "OREL TO KURSK", 0.6, 4.4);
B.city("OREL", ...OREL, { size: 30, t: 1.2 });
B.city("KROMY", ...KROMY, { size: 22, t: T_STEPPE });
B.city("FATEZH", ...FATEZH, { size: 22, t: T_RIVER + 0.5 });
B.city("KURSK", ...KURSK, { size: 30, t: T_REACH - 0.6 });
B.caption("200 KM OF OPEN STEPPE", T_STEPPE, S2 - 0.3);
B.caption("DAY 12 · KURSK", T_REACH + 0.3, END - 0.2);

// ---------- the route: an arrow that draws itself along the spoken beat ----------
B.arrow({ side: "white", pts: [OREL, KROMY, FATEZH, KURSK], width: 18, t: T_RIVER - 0.3, dur: T_REACH - T_RIVER + 0.2 });
K.target(...OREL, T_LEFT, { r: 34 });          // pulsing rings on the start and the goal
K.target(...KURSK, T_REACH, { r: 40 });
B.finish();
