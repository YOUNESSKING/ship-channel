// BASEMAP: bikini_close
// Hook: orange NEVADA dot = aim point; burst star west of her; dashed line + '≈ 1/3 MILE' on 'third'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const AIM = P("AIM"), BU = P("BURSTA"), MID = [(AIM[0] + BU[0]) / 2, (AIM[1] + BU[1]) / 2];
S.camera([[0, MID[0], MID[1], 3.8], [END, MID[0] + 4, MID[1], 4.0]]);
S.dot(AIM, { t: 0.1, r: 14, color: "#D9572B" }); S.ring(AIM, { t: 0.1, r: 40, color: "#D9572B" });
S.label("NEVADA · AIM POINT", AIM, { t: wt("her", 1.6), anchor: "r", size: 44, gap: 40, dy: 50 });
S.burst(BU, wt("bomb", 0.8) + 0.2, { r: 46 });
S.label("BURST", BU, { t: wt("bomb", 0.8) + 0.2, anchor: "l", size: 44, gap: 50, dy: 50 });
S.route([BU, AIM], { t: wt("about", 1.8), dur: 0.9, dash: [14, 10], width: 5, color: "#f3eee2" });
S.tag("≈ 1/3 MILE", MID, { t: wt("third", 2.4), anchor: "t", size: 48, gap: 90, boxColor: "rgba(150,40,30,.92)" });
S.finish();
