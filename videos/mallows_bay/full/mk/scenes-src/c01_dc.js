// BASEMAP: potomac
// Hook end: from the bay back up the river to Washington; 'WASHINGTON' on 'Washington'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const WH = S.P("WH"), MB = S.P("MALLOWS");
S.camera([[0, MB[0], MB[1], 1.3], [END, WH[0] - 40, WH[1] + 60, 1.15]]);
S.pin(MB, "MALLOWS BAY", { t: 0.0, anchor: "l", rings: false, color: "#D9572B" });
S.route([MB, WH], { t: 0.1, dur: 2.2, dash: [14, 10], width: 5, color: "#f3eee2" });
S.pin(WH, null, { t: 1.9 });
S.label("WASHINGTON", WH, { t: wt("Washington", 2.2), anchor: "r", size: 52 });
S.finish();
