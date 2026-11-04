// BASEMAP: gulf7
// "On the twenty second of March, two thousand six, she came back to Pensacola" Beaumont -> Pensacola (FACTCHECK_B B26: arrived 22 Mar 2006).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const BEAU = S.P("BEAU"), NASP = S.P("NASP");
const R = S.path([[30.08, -94.1], [29.9, -93.95], [29.7, -93.85], [29.4, -93.75], [28.95, -92.5], [28.8, -90.5], [28.85, -89.1], [29.3, -88.6], [30.1, -87.6], [30.32, -87.31], [30.35, -87.29]]);
S.clouds(5, 0.14);
S.camera([[0, BEAU[0] + 200, BEAU[1] + 60, 1.25], [w("Pensacola"), 1500, 700, 1.05], [END, NASP[0] - 40, NASP[1] + 60, 1.3]]);
S.pin(BEAU, "BEAUMONT", { t: 0.0, rings: false, anchor: "t", gap: 30 });
S.date("22 MAR 2006", w("twenty"));
S.route(R, { t: 0.8, dur: w("Pensacola") - 0.7, dash: [16, 10], head: "ship", headSize: 1.2 });
S.pin(NASP, "NAS PENSACOLA", { t: w("Pensacola"), anchor: "t", gap: 30 });
S.finish();
