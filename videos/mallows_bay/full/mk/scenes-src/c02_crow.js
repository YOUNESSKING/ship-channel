// BASEMAP: potomac
// 'The bay is thirty-two miles from the White House, as the crow flies.' straight line + tag on 'thirty'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const WH = S.P("WH"), MB = S.P("MALLOWS"); const MID = [(WH[0] + MB[0]) / 2, (WH[1] + MB[1]) / 2];
S.camera([[0, MID[0], MID[1], 0.92], [END, MID[0] - 30, MID[1] + 10, 1.0]]);
S.pin(MB, "MALLOWS BAY", { t: 0.0, anchor: "l", color: "#D9572B" });
S.pin(WH, "THE WHITE HOUSE", { t: 0.3, anchor: "r" });
S.route([MB, WH], { t: wt("thirty", 0.8) - 0.3, dur: 1.0, width: 5, color: "#f3eee2" });
S.tag("32 MILES", MID, { t: wt("thirty", 0.8), anchor: "r", gap: 40, size: 46, boxColor: "rgba(150,40,30,.92)" });
S.label("AS THE CROW FLIES", MID, { t: wt("crow", 2.5), anchor: "r", gap: 40, dy: 58, size: 34 });
S.finish();
