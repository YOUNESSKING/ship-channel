// BASEMAP: brownsville
// 3 YARDS on 'three'; ship channel from Brazos Santiago to the port; BROWNSVILLE label; GULF OF MEXICO on 'Brownsville'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const PT = P("BROWNSVILLE"), BZ = P("BRAZOS");
S.camera([[0, 1470, 810, 1.15], [END, 1480, 800, 1.35]]);
[[25.945, -97.415], [25.957, -97.395], [25.94, -97.383]].forEach((q, i) => S.dot(G(...q), { t: wt("three", 0.32) + i * 0.12, r: 9, color: RED }));
S.tag("3 YARDS", PT, { t: wt("three", 0.32), anchor: "l", size: 52, gap: 50, dy: 30, boxColor: "rgba(150,40,30,.92)" });
S.route(S.path(S.CHAN), { t: 1.2, dur: 2.4, width: 7, color: ST, dash: [14, 10], ease: "none", head: "dot" });
S.label("BRAZOS SANTIAGO", BZ, { t: 1.2, anchor: "r", size: 34, gap: 40, dy: -30, color: ST });
S.label("BROWNSVILLE", PT, { t: wt("Brownsville", 3.06), anchor: "t", size: 54, gap: 70, dx: -40 });
S.label("GULF OF MEXICO", G(26.0, -96.85), { t: wt("Brownsville", 3.06), anchor: "c", size: 54, color: ST });
S.finish();
