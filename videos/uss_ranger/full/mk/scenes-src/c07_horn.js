// BASEMAP: magellan
// 2015 tow line rounds the southern tip; faint 1958 ghost line; SOUTHERN TIP label.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const CH = P("CAPEHORN");
S.camera([[0, 1400, 780, 0.75], [END, 1500, 860, 0.85]]);
const tow = S.path([[-48.5, -77.8], [-52.5, -78.0], [-55.8, -75.5], [-57.3, -70.5], [-57.3, -65.5], [-55.6, -61.5], [-52, -57.8], [-49, -55.8]]);
S.route(tow, { t: 0.1, dur: Math.max(1.0, END - 0.7), width: 8, color: RED, head: "ship", ease: "none" });
S.label("SOUTHERN TIP OF SOUTH AMERICA", G(-51.2, -66.5), { t: wt("southern", 0.58), anchor: "c", size: 46, color: WH });
const tg = Math.min(wt("same", 1.5), END - 0.5);
S.route(S.path(S.GHOST58), { t: tg, dur: 0.5, width: 5, color: "rgba(243,238,226,.6)", dash: [12, 10] });
S.dot(CH, { t: tg, r: 8, color: WH }); S.label("CAPE HORN · 1958", CH, { t: tg, anchor: "t", size: 38, gap: 40, color: WH, dx: -20 });
S.finish();
