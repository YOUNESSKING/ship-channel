// BASEMAP: usa
// dashed line Bremerton south to San Diego; 1985 on 'eighty'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const BR = P("BREMERTON"), SD = P("SANDIEGO");
S.camera([[0, 900, 765, 1.5], [END, 910, 770, 1.6]]);
S.pin(BR, "BREMERTON", { t: 0.2, color: WH, anchor: "r", size: 42, gap: 32, ringR: 30 });
const t1 = wt("back", 2.6);
S.route(S.path([[47.557, -122.632], [48.2, -123.3], [48.4, -124.9], [46.3, -125.0], [42, -125.4], [37, -123.9], [33.5, -119.6], [32.7, -117.2]]), { t: t1, dur: 2.5, dash: [16, 12], width: 6, color: RED, head: "dot" });
S.pin(SD, "SAN DIEGO", { t: t1 + 2.4, color: RED, anchor: "r", size: 46, gap: 34, ringR: 34 });
S.date("1985", wt("eighty", 4.0));
S.finish();
