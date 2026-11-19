// BASEMAP: americas
// second dashed line (grey-blue) Bremerton -> around South America -> Brownsville; INDEPENDENCE 2017 on 'voyage'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BR = P("BREMERTON"), BV = P("BROWNSVILLE"), tow = S.path(S.TOW);
S.camera([[0, 1440, 810, 0.667], [END, 1440, 810, 0.7]]);
S.route(tow, { t: 0, dur: 0.01, width: 6, color: "rgba(217,87,43,.8)" });
S.pin(BR, "BREMERTON", { t: 0.1, color: WH, anchor: "r", size: 40, gap: 28, ringR: 26 });
S.pin(BV, "BROWNSVILLE", { t: 0.1, color: WH, anchor: "l", size: 40, gap: 28, dy: 20, ringR: 26 });
S.route(S.offsetPath(tow, 16), { t: wt("voyage", 0.68), dur: END - 1.5, dash: [14, 10], width: 6, color: "#9fc3e0", head: "ship", ease: "none" });
S.tag("INDEPENDENCE · 2017", G(-14, -108), { t: wt("voyage", 0.68), anchor: "c", size: 52, boxColor: "rgba(40,70,100,.94)" });
S.tag("RANGER · 2015", G(-22, -100), { t: wt("voyage", 0.68), anchor: "c", size: 44, dy: 50, boxColor: "rgba(150,40,30,.92)" });
S.finish();
