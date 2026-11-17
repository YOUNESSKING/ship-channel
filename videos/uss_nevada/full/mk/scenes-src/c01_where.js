// BASEMAP: oahu_sw
// Oahu + open ocean to the SW: pulsing '?' far out at sea on 'where'; '70+ YEARS' on 'seventy'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const PH = P("PEARL"), WR = P("WRECK");
S.camera([[0, 1500, 760, 1.0], [END, 1330, 850, 1.2]]);
S.dot(PH, { t: 0.1, r: 9, color: "#f3eee2" }); S.label("PEARL HARBOR", PH, { t: 0.1, anchor: "r", size: 40, gap: 40, dy: 30, color: "#8fb0cc" });
S.icon("q", WR, { t: wt("where", 0.5), size: 90, color: "#D9572B", bob: 10 }); S.ring(WR, { t: wt("where", 0.5), r: 70, color: "#D9572B" });
S.tag("70+ YEARS", WR, { t: wt("seventy", 2.6), anchor: "r", size: 56, gap: 100, dy: 0, boxColor: "rgba(150,40,30,.92)" });
S.finish();
