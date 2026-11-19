// BASEMAP: usa
// 22 DECEMBER 2014 on 'December'; BREMERTON pin; BROWNSVILLE, TX pin on 'future'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BR = P("BREMERTON"), BV = P("BROWNSVILLE");
S.camera([[0, 880, 600, 1.4], [3.4, 1100, 830, 0.95], [END, 1140, 850, 0.9]]);
S.date("22 DECEMBER 2014", wt("December", 1.26));
S.pin(BR, "BREMERTON, WA", { t: 0.2, color: WH, anchor: "r", size: 42, gap: 32, ringR: 30 });
S.route(S.arcPts(BR, BV, -0.12), { t: wt("Navy", 3.4), dur: 1.0, dash: [16, 12], width: 5, color: RED });
S.pin(BV, "BROWNSVILLE, TX", { t: wt("future", 4.3), color: RED, anchor: "r", size: 46, gap: 36, ringR: 36 });
S.finish();
