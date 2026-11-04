// BASEMAP: pacific
// "Japanese investors wanted her as the centrepiece of an attraction in Tokyo Bay." Arc lands in Tokyo Bay (FACTCHECK_A D4).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const BR = S.P("BREM"), TK = S.P("TOKYO");
const ARC = S.arcPts(BR, TK, 0.12, 40);
S.clouds(7, 0.14);
S.camera([[0, (BR[0] + TK[0]) / 2 + 120, BR[1] + 80, 0.95], [w("Tokyo"), TK[0] + 120, TK[1] - 10, 1.7], [END, TK[0] + 90, TK[1], 1.95]]);
S.pin(BR, "BREMERTON", { t: 0.0, anchor: "r", rings: false, until: 2.0 });
S.route(ARC.slice(0, 25), { t: 0.0, dur: 0.01, dash: [18, 12], width: 6, scaleAt: 0 });
S.route(ARC.slice(24), { t: 0.1, dur: w("Tokyo") - 0.3, dash: [18, 12], width: 6, head: "dot", scaleAt: 0, ease: "power1.out" });
S.label("JAPAN", G(40.0, 140.6), { t: w("Japanese"), anchor: "c", size: 48 });
S.tag("PLANNED ATTRACTION", TK, { t: w("attraction"), anchor: "b", gap: 50, size: 42, boxColor: "rgba(150,110,20,.95)" });
S.pin(TK, "TOKYO BAY", { t: w("Tokyo") - 0.05, anchor: "r" });
S.finish();
