// BASEMAP: americas
// end screen: full tow line in red on the left half; right half clear; slow drift.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BR = P("BREMERTON"), BV = P("BROWNSVILLE");
S.camera([[0, 1583, 890, 0.74], [END, 1500, 850, 0.74]]);
S.pin(BR, "BREMERTON", { t: 0.3, color: WH, anchor: "r", size: 40, gap: 28, ringR: 26 });
S.route(S.path(S.TOW), { t: 0.4, dur: 4.5, width: 6, color: RED, head: "ship", ease: "none" });
S.pin(BV, "BROWNSVILLE", { t: 4.5, color: RED, anchor: "l", size: 40, gap: 28, dy: 20, ringR: 28 });
S.finish();
