// BASEMAP: americas
// tow line draws from Bremerton down the Pacific coast; NORTH / SOUTH AMERICA labels on 'two continents'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BR = P("BREMERTON");
S.camera([[0, 1440, 810, 0.667], [END, 1440, 810, 0.7]]);
S.pin(BR, "BREMERTON", { t: 0.1, color: WH, anchor: "r", size: 40, gap: 28, ringR: 26 });
S.route(S.path(S.TOW_PAC), { t: 0.3, dur: END - 0.8, width: 7, color: RED, head: "ship", ease: "none" });
S.label("NORTH AMERICA", G(40, -104), { t: wt("two", 4.47), anchor: "c", size: 50, color: ST });
S.label("SOUTH AMERICA", G(-12, -58), { t: wt("continents", 4.73), anchor: "c", size: 50, color: ST });
S.finish();
