// BASEMAP: gulf7
// "In June two thousand five, she was towed back to Texas to hide from it." Pensacola -> Beaumont tow (west); hurricane symbol in the Gulf.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const NASP = S.P("NASP"), BEAU = S.P("BEAU");
const R = S.path([[30.35, -87.29], [30.32, -87.31], [30.1, -87.6], [29.3, -88.6], [28.85, -89.1], [28.8, -90.5], [28.95, -92.5], [29.4, -93.75], [29.7, -93.85], [29.9, -93.95], [30.08, -94.1]]);
S.clouds(5, 0.14);
S.camera([[0, 1560, 760, 1.0], [END, 1300, 740, 1.08]]);
S.pin(NASP, "PENSACOLA", { t: 0.0, rings: false, anchor: "t", gap: 30 });
S.date("JUNE 2005", w("June"));
S.route(R, { t: w("towed") - 0.1, dur: 2.2, dash: [16, 10], head: "ship", headSize: 1.2 });
S.pin(BEAU, null, { t: w("Texas") - 0.1 });
S.label("TEXAS", G(31.0, -95.4), { t: w("Texas"), anchor: "c", size: 48 });
const HP = S.path([[26.7, -88.2]]);
S.icon("hurricane", HP[0], { t: 0.3, size: 110, spin: 600, color: "#f3eee2" });
S.label("HURRICANE SEASON", HP[0], { t: w("hide"), anchor: "r", gap: 70, size: 42 });
S.finish();
