// BASEMAP: gulf7
// "From Texas, she was towed to Pensacola. Then came hurricane season." Corpus Christi -> Pensacola tow along the coast.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const CC = S.P("CORPUS"), NASP = S.P("NASP");
const R = S.path([[27.8, -97.4], [27.82, -97.05], [27.7, -96.5], [28.3, -95.2], [28.85, -93.5], [28.75, -91.5], [28.8, -89.8], [28.85, -89.0], [29.6, -88.2], [30.25, -87.45], [30.32, -87.31], [30.35, -87.29]]);
S.clouds(5, 0.14);
S.camera([[0, CC[0] + 300, CC[1] - 80, 1.25], [w("Pensacola") + 0.5, 1500, 690, 0.95], [END, 1560, 760, 1.0]]);
S.pin(CC, "CORPUS CHRISTI", { t: 0.0, rings: false, anchor: "r", dy: 40 });
S.route(R, { t: 0.15, dur: w("Pensacola") + 0.2, dash: [16, 10], head: "ship", headSize: 1.2 });
S.pin(NASP, "PENSACOLA", { t: w("Pensacola"), anchor: "t", gap: 30 });
S.icon("hurricane", G(26.9, -89.0), { t: w("hurricane") - 0.1, size: 90, spin: 540, color: "#f3eee2" });
S.tag("HURRICANE SEASON", G(26.9, -89.0), { t: w("hurricane"), anchor: "r", gap: 60, boxColor: "rgba(120,30,30,.92)" });
S.finish();
