// BASEMAP: usa
// 'In Aberdeen, Washington, a yard claimed a record.' pin ABERDEEN on 'Aberdeen'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const AB = S.P("ABERDEEN");
S.camera([[0, AB[0] + 220, AB[1] + 40, 1.4], [END, AB[0] + 200, AB[1] + 30, 1.6]]);
S.pin(AB, "ABERDEEN, WASHINGTON", { t: wt("Aberdeen", 0.2), anchor: "r", color: "#D9572B" });
S.tag("A RECORD?", AB, { t: wt("record", 2.4), anchor: "b", gap: 50 });
S.finish();
