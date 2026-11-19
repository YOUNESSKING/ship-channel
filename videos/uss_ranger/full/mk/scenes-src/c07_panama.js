// BASEMAP: americas
// PANAMA CANAL pin with red X on 'Panama'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const PA = P("PANAMA"), BV = P("BROWNSVILLE"), BR = P("BREMERTON");
S.camera([[0, 1400, 610, 1.1], [END, 1420, 640, 1.2]]);
S.dot(BR, { t: 0.1, r: 8, color: WH }); S.label("BREMERTON", BR, { t: 0.1, anchor: "r", size: 36, gap: 28, color: ST });
S.pin(PA, "PANAMA CANAL", { t: wt("Panama", 1.38), color: WH, anchor: "r", size: 48, gap: 40, dy: 36, ringR: 30 });
S.xmark(PA, wt("Canal", 1.78) + 0.1, { r: 30 });
S.pin(BV, "BROWNSVILLE", { t: wt("Texas", 4.0), color: RED, anchor: "l", size: 40, gap: 30, ringR: 28 });
S.finish();
