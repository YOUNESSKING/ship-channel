// BASEMAP: gulfmex
// Brownsville -> Corpus Christi line; USS LEXINGTON MUSEUM on 'Lexington'; 5+ TONS on 'five'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BV = P("BROWNSVILLE"), CC = P("LEXMUS");
S.camera([[0, 1130, 690, 3.0], [END, 1128, 688, 3.4]]);
S.dot(BV, { t: 0.1, r: 10, color: RED }); S.label("BROWNSVILLE", BV, { t: 0.1, anchor: "r", size: 40, gap: 34, dy: -20 });
S.tag("5+ TONS", BV, { t: wt("five", 0.56), anchor: "r", size: 54, gap: 100, dy: 50, boxColor: "rgba(150,40,30,.92)" });
S.route([BV, G(26.8, -97.5), G(27.4, -97.5), CC], { t: wt("went", 2.38), dur: 0.9, dash: [14, 10], width: 5, color: RED, head: "dot" });
S.pin(CC, "USS LEXINGTON MUSEUM", { t: wt("Lexington", 3.24), color: WH, anchor: "r", size: 40, gap: 34, ringR: 30 });
S.label("TEXAS", G(27.2, -98.8), { t: 0.4, anchor: "c", size: 52, color: ST });
S.finish();
