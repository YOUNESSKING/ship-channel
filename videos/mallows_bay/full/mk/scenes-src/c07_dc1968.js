// BASEMAP: potomac
// 'In 1968, Congress ordered the wrecks removed,' date; Washington; tag on 'removed'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const WH = S.P("WH"), MB = S.P("MALLOWS");
S.camera([[0, WH[0], WH[1] + 140, 1.1], [END, (WH[0] + MB[0]) / 2, (WH[1] + MB[1]) / 2, 0.95]]);
S.date("1968", wt("sixty", 0.5));
S.pin(WH, "CONGRESS", { t: 0.2, anchor: "r" });
S.route([WH, MB], { t: wt("ordered", 1.6), dur: 1.4, dash: [14, 10], width: 5, color: "#f3eee2" });
S.tag("REMOVE THE WRECKS", MB, { t: wt("removed", 2.8), anchor: "l", gap: 40, boxColor: "rgba(150,40,30,.92)" });
S.finish();
