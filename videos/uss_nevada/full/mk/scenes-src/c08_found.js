// BASEMAP: oahu_sw
// WRECK pin 'USS NEVADA' in the box; dashed line to Pearl Harbor, 65 NAUTICAL MILES on 'sixty'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const WR = P("WRECK"), PH = P("PEARL"), h = S.mpx(18520) / 2, MID = [(WR[0] + PH[0]) / 2, (WR[1] + PH[1]) / 2];
S.camera([[0, 1200, 930, 1.9], [END, 1330, 880, 1.3]]);
S.poly([[[WR[0] - h, WR[1] - h], [WR[0] + h, WR[1] - h], [WR[0] + h, WR[1] + h], [WR[0] - h, WR[1] + h]]], { px: true, t: 0, color: "#8fb0cc", fill: 0.16, width: 4 });
S.pin(WR, "USS NEVADA", { t: wt("lies", 0.6), color: "#D9572B", anchor: "l", size: 52, gap: 50, dy: 60, ringR: 36 });
S.tag("APPROX.", WR, { t: wt("lies", 0.6) + 0.2, anchor: "l", size: 38, gap: 50, dy: 120, boxColor: "rgba(30,64,92,.92)" });
S.route([WR, PH], { t: wt("sixty", 1.6), dur: 1.6, dash: [16, 12], width: 5, color: "#f3eee2" });
S.tag("65 NAUTICAL MILES", MID, { t: wt("sixty", 1.6) + 0.4, anchor: "t", size: 48, gap: 60, boxColor: "rgba(150,40,30,.92)" });
S.pin(PH, "PEARL HARBOR", { t: wt("Pearl", 4.2), color: "#f3eee2", anchor: "l", size: 44, gap: 40, dy: 10, ringR: 30 });
S.finish();
