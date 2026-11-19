// BASEMAP: sandiego
// SAN DIEGO BAY on 'San'; SUMMER 1985 on 'film'; NORTH ISLAND label.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const NI = P("NORTHISLAND");
S.camera([[0, 1448, 812, 1.2], [END, 1450, 812, 1.4]]);
S.date("SUMMER 1985", wt("film", 2.1));
S.label("SAN DIEGO BAY", G(32.69, -117.135), { t: wt("San", 0.45), anchor: "r", size: 50, gap: 20, dy: 30 });
S.pin(NI, "NORTH ISLAND", { t: 1.0, color: RED, anchor: "l", size: 44, gap: 40, dy: -30, ringR: 30 });
S.finish();
