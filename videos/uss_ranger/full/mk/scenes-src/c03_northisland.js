// BASEMAP: sandiego
// NORTH ISLAND pin; 3 DAYS on 'three'; STAR TREK IV date.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const NI = P("NORTHISLAND");
S.camera([[0, 1470, 800, 1.5], [END, 1455, 812, 1.8]]);
S.date("STAR TREK IV · 1986", wt("days", 1.0));
S.dot(NI, { t: 0.2, r: 11, color: RED }); S.ring(NI, { t: 0.2, color: RED, r: 34 });
S.tag("3 DAYS", NI, { t: wt("three", 0.7), anchor: "r", size: 56, gap: 70, dy: 40, boxColor: "rgba(150,40,30,.92)" });
S.label("NORTH ISLAND", NI, { t: wt("North", 1.9), anchor: "l", size: 46, gap: 40, dy: -30 });
S.label("SAN DIEGO", G(32.75, -117.13), { t: wt("San", 3.1), anchor: "r", size: 40, color: ST, dy: -40 });
S.finish();
