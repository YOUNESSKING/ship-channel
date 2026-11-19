// BASEMAP: americas
// line continues north up the Atlantic, into the Gulf of Mexico to Brownsville.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BV = P("BROWNSVILLE");
S.camera([[0, 1500, 900, 0.8], [END, 1380, 640, 1.0]]);
S.route(S.path(S.TOW_PAC), { t: 0, dur: 0.01, width: 6, color: RED });
S.route(S.path(S.TOW_ATL), { t: 0.15, dur: END - 1.0, width: 7, color: RED, head: "ship", ease: "none" });
S.label("ATLANTIC OCEAN", G(-8, -24), { t: wt("Atlantic", 1.24), anchor: "c", size: 54, color: ST });
S.label("GULF OF MEXICO", G(24, -90), { t: wt("Gulf", 2.78), anchor: "c", size: 46, color: ST });
S.pin(BV, "BROWNSVILLE", { t: END - 0.9, color: RED, anchor: "l", size: 40, gap: 28, dy: 20, ringR: 28 });
S.finish();
