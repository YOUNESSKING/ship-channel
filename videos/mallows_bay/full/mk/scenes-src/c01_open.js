// BASEMAP: potomac
// Hook frame 0: White House pin; dashed line down-river to Mallows Bay on 'thirty'; '≈ 30 MILES' tag.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const WH = S.P("WH"), MB = S.P("MALLOWS"); const MID = [(WH[0] + MB[0]) / 2, (WH[1] + MB[1]) / 2];
S.clouds(5, 0.12);
S.camera([[0, WH[0] - 60, WH[1] + 120, 1.25], [END, MID[0] - 40, MID[1] + 70, 0.98]]);
S.pin(WH, "THE WHITE HOUSE", { t: 0.0, anchor: "r" });
S.route([WH, MB], { t: wt("thirty", 0.6), dur: 1.4, dash: [14, 10], width: 5, color: "#f3eee2" });
S.pin(MB, "MALLOWS BAY", { t: wt("thirty", 0.6) + 1.2, anchor: "l", color: "#D9572B" });
S.tag("≈ 30 MILES", MID, { t: wt("thirty", 0.6) + 0.1, anchor: "r", gap: 40, boxColor: "rgba(150,40,30,.92)" });
S.finish();
