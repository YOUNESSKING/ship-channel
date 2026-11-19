// BASEMAP: americas
// dashed route Bremerton -> around South America -> Brownsville draws on 'tow'; 16,000 MILES on 'sixteen'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BR = P("BREMERTON"), BV = P("BROWNSVILLE");
S.camera([[0, 1440, 810, 0.667], [END, 1440, 810, 0.72]]);
S.pin(BR, "BREMERTON", { t: 0.2, color: WH, anchor: "r", size: 40, gap: 28, ringR: 26 });
S.route(S.path(S.TOW), { t: wt("tow", 1.52), dur: 4.2, dash: [16, 12], width: 6, color: RED, head: "ship", ease: "none" });
S.tag("≈16,000 MILES", G(-12, -104), { t: wt("sixteen", 2.2), anchor: "c", size: 62, boxColor: "rgba(150,40,30,.92)" });
S.pin(BV, "BROWNSVILLE", { t: wt("tow", 1.52) + 4.0, color: RED, anchor: "l", size: 40, gap: 28, dy: 20, ringR: 28 });
S.finish();
