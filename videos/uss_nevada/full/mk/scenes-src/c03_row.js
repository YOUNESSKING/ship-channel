// BASEMAP: pearl_row
// 'battleships, most of them moored in pairs.' Pairs of battleship icons appear along Ford Island's east shore.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1345, 840, 1.9], [END, 1350, 835, 2.0]]);
const L = S.sl(183, 0, 1.0), rot = 135, ST = { fill: "#8fb0cc", stroke: "#0c1218", sw: 2.2 };
const mk = (k, kind, t) => S.ship(kind, P(k), { t, len: kind === "tr" ? L * 0.8 : L, rot, ...ST });
mk("CA", "bb", wt("battleships", 0.3));
mk("MD", "bb", wt("most", 1.0)); mk("OK", "bb", wt("most", 1.0) + 0.15);
mk("TN", "bb", wt("moored", 1.8)); mk("WV", "bb", wt("moored", 1.8) + 0.15);
mk("AZ", "bb", wt("pairs", 2.6)); mk("AZ_O", "tr", wt("pairs", 2.6) + 0.15);
S.label("BATTLESHIP ROW", S.off(P("OK"), 330, -100), { t: wt("battleships", 0.3), anchor: "r", size: 46, gap: 20 });
S.label("FORD ISLAND", S.off(P("TN"), -330, 150), { t: wt("battleships", 0.3) + 0.6, anchor: "c", size: 40, color: "#8fb0cc" });
S.tag("MOORED IN PAIRS", S.off(P("OK"), 330, -100), { t: wt("pairs", 2.6), anchor: "r", size: 42, gap: 20, dy: 70, boxColor: "rgba(150,40,30,.92)" });
S.finish();
