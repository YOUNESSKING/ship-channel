// BASEMAP: marshalls
// KWAJALEIN pin on 'Kwajalein'; a B-29 icon flies a dashed line NW to Bikini.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const KW = P("KWAJ"), BK = P("BIKINI"), MID = [(KW[0] + BK[0]) / 2, (KW[1] + BK[1]) / 2];
S.camera([[0, MID[0] + 20, MID[1], 1.35], [END, MID[0] - 10, MID[1], 1.45]]);
S.pin(KW, "KWAJALEIN", { t: wt("Kwajalein", 0.4), color: "#f3eee2", anchor: "r", size: 52, gap: 40, ringR: 36 });
const a = wt("hours", 1.4), d = END - a - 0.3;
S.route([KW, BK], { t: a, dur: d, dash: [16, 12], width: 5, color: "#f3eee2", ease: "power1.inOut" });
const jet = S.ship("b29", KW, { t: a, len: 80, rot: 0, fill: "#f3eee2", stroke: "#D9572B", sw: 3 });
S.sail(jet, [KW, BK], { t: a, dur: d, ease: "power1.inOut" });
S.pin(BK, "BIKINI", { t: a + d - 0.4, color: "#D9572B", anchor: "l", size: 48, gap: 40, dy: -20, ringR: 36 });
S.finish();
