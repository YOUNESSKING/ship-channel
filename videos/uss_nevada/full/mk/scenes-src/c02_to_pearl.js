// BASEMAP: pacific
// Dashed line from Bikini back east to Hawaii; HAWAII on 'Hawaii'; '1941' on 'Sunday'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const BK = P("BIKINI"), PH = P("PEARL"), MID = [(BK[0] + PH[0]) / 2, (BK[1] + PH[1]) / 2];
S.camera([[0, MID[0] - 40, MID[1] + 10, 2.1], [END, MID[0] + 40, MID[1], 2.3]]);
S.pin(BK, "BIKINI", { t: 0.1, color: "#D9572B", anchor: "l", size: 44, gap: 40, ringR: 36 });
S.route(S.arcPts(BK, PH, 0.12), { t: wt("go", 2.4), dur: 2.2, dash: [16, 12], width: 5, color: "#f3eee2", head: "dot" });
S.date("1941", wt("Sunday", 3.8));
S.pin(PH, "HAWAII", { t: wt("Hawaii", 4.6), color: "#f3eee2", anchor: "r", size: 52, gap: 40, ringR: 36 });
S.finish();
