// BASEMAP: usa
// dashed tow line from San Diego up the coast to Bremerton; 1994 date.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const SD = P("SANDIEGO"), BR = P("BREMERTON");
S.camera([[0, 850, 765, 1.4], [END, 860, 770, 1.5]]);
S.date("1994", wt("towed", 0.75));
S.pin(SD, "SAN DIEGO", { t: 0.2, color: WH, anchor: "r", size: 42, gap: 30, ringR: 30 });
S.route(S.path([[32.7, -117.2], [33.4, -119.0], [34.2, -121.0], [36, -122.5], [38, -123.5], [40.4, -124.9], [43, -125.0], [46.3, -124.8], [48.4, -125.0], [48.2, -123.2], [47.557, -122.632]]),
  { t: wt("towed", 0.75), dur: 2.6, dash: [16, 12], width: 6, color: RED, head: "ship" });
S.pin(BR, "BREMERTON", { t: wt("Bremerton", 1.71) + 0.9, color: RED, anchor: "r", size: 44, gap: 32, ringR: 32 });
S.finish();
