// BASEMAP: gulf_pan
// "On the morning of the seventeenth of May," Pensacola -> the reef site (FWC 30°02.555'N 87°00.397'W); ~22.5 nmi SE of Pensacola Pass (FACTCHECK_C).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const PENS = S.P("PENS"), PASS = G(30.32, -87.31), REEF = S.P("REEF");
S.clouds(5, 0.14);
S.camera([[0, PENS[0] + 40, PENS[1] + 40, 1.6], [END, REEF[0] + 10, REEF[1] - 120, 1.85]]);
S.pin(PENS, "PENSACOLA", { t: 0.05, rings: false, anchor: "l" });
S.date("17 MAY 2006", w("seventeenth"));
S.route([PENS, PASS, G(30.2, -87.2), REEF], { t: 0.3, dur: 1.6, dash: [16, 10], head: "ship", headSize: 1.1 });
S.pin(REEF, null, { t: 1.8 });
S.tag("≈ 22 NM OUT", [(PASS[0] + REEF[0]) / 2, (PASS[1] + REEF[1]) / 2], { t: 2.0, anchor: "r", gap: 30 });
S.finish();
