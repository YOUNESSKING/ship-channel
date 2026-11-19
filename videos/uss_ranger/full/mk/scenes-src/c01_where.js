// BASEMAP: usa
// dashed question line from Bremerton south (off-screen); pulsing ? over the Texas Gulf coast on 'left'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BR = P("BREMERTON"), BV = P("BROWNSVILLE"), TX = G(27.6, -97.2);
S.camera([[0, 1100, 760, 0.95], [END, 1200, 900, 1.1]]);
S.dot(BR, { t: 0.1, r: 9, color: WH }); S.label("BREMERTON", BR, { t: 0.1, anchor: "r", size: 40, gap: 30, color: ST });
S.route(S.arcPts(BR, BV, -0.12), { t: 0.15, dur: 1.2, dash: [16, 12], width: 5, color: "rgba(243,238,226,.75)" });
S.icon("q", TX, { t: wt("left", 0.7), size: 100, color: RED, bob: 10 }); S.ring(TX, { t: wt("left", 0.7), r: 70, color: RED });
S.finish();
