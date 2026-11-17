// BASEMAP: pacific
// Tow line KWAJALEIN -> PEARL HARBOR; MAY 1947 on 'May'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const KW = P("KWAJ"), PH = P("PEARL"), MID = [(KW[0] + PH[0]) / 2, (KW[1] + PH[1]) / 2];
S.camera([[0, MID[0], MID[1], 2.1], [END, MID[0] + 15, MID[1] - 10, 2.25]]);
S.date("MAY 1947", wt("May", 0.5));
S.pin(KW, "KWAJALEIN", { t: 0.2, color: "#f3eee2", anchor: "r", size: 40, gap: 30, dy: 40, ringR: 30 });
const a = wt("towed", 2.0) - 0.4, d = END - a - 0.5;
S.route([KW, ...S.arcPts(KW, PH, -0.08, 12).slice(1)], { t: a, dur: d, dash: [16, 12], width: 5, color: "#D9572B", head: "ship" });
S.pin(PH, "PEARL HARBOR", { t: wt("Pearl", 3.2), color: "#f3eee2", anchor: "l", size: 48, gap: 40, dy: -30, ringR: 32 });
S.finish();
