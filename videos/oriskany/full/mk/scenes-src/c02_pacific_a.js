// BASEMAP: pacific
// "Then, in the early nineteen nineties, an offer came from across the Pacific." Dashed arc starts at Bremerton and draws west.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const BR = S.P("BREM"), TK = S.P("TOKYO");
const ARC = S.arcPts(BR, TK, 0.12, 40);
S.clouds(7, 0.14);
S.camera([[0, BR[0] - 250, BR[1] + 120, 1.25], [END, (BR[0] + TK[0]) / 2 + 120, BR[1] + 80, 0.95]]);
S.pin(BR, "BREMERTON", { t: 0.05, anchor: "r" });
S.date("EARLY 1990s", w("early"));
S.route(ARC.slice(0, 25), { t: w("offer"), dur: END - w("offer"), dash: [18, 12], width: 6, head: "dot", ease: "power1.in" });
S.label("PACIFIC OCEAN", G(38, -160), { t: w("Pacific"), anchor: "c", size: 50, color: "rgba(230,240,240,.92)" });
S.finish();
