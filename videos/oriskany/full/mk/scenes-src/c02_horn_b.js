// BASEMAP: americas
// "All the way around South America. To a reserve fleet at Beaumont, Texas." The camera follows the tow; pin BEAUMONT. No mileage.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const BEAU = S.P("BEAU");
const R = S.path(window.HORN);
S.route(R.slice(0, 4), { t: 0.0, dur: 0.01, dash: [16, 10] });
S.camera([[0, 1300, 900, 1.0], [1.5, 1500, 1350, 0.72], [3.2, 1500, 900, 0.72], [END, BEAU[0] + 80, BEAU[1] + 150, 1.15]]);
S.route(R.slice(3), { t: 0.1, dur: w("reserve") - 0.1, dash: [16, 10], head: "ship", headSize: 1.3, ease: "sine.inOut" });
S.label("SOUTH AMERICA", G(-12, -60), { t: w("South"), anchor: "c", size: 50 });
S.pin(BEAU, null, { t: w("reserve") });
S.label("BEAUMONT, TEXAS", BEAU, { t: w("Beaumont"), anchor: "r" });
S.tag("RESERVE FLEET", BEAU, { t: w("reserve"), anchor: "t", gap: 46, size: 42 });
S.finish();
