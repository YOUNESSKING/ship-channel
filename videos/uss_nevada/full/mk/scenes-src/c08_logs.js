// BASEMAP: oahu_sw
// Three scattered 1948 log positions appear on 'rough'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const WR = P("WRECK");
S.camera([[0, 1250, 900, 1.5], [END, 1250, 900, 1.52]]);
S.icon("q", WR, { t: 0, size: 90, color: "#D9572B", bob: 10 });
const L = [S.off(WR, -11000, 9000), S.off(WR, 12000, 6000), S.off(WR, 1500, -13000)];
L.forEach((p, i) => { const t = wt("rough", 3.0) + i * 0.4; S.dot(p, { t, r: 12, color: "#f3eee2" }); S.ring(p, { t, r: 34, color: "#f3eee2" }); S.label("1948 LOG", p, { t, anchor: "r", size: 40, gap: 40 }); });
S.tag("ROUGH POSITIONS", S.off(WR, 0, 8500), { t: wt("rough", 3.0), anchor: "c", size: 46, boxColor: "rgba(150,40,30,.92)" });
S.finish();
