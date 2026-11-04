// BASEMAP: usse
// "In November two thousand three, Congress gave the Navy the power to donate..." A gold arrow sweeps D.C. -> the Gulf coast.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const DC = S.P("DC"), GULF = G(29.6, -87.5);
S.clouds(5, 0.12);
S.camera([[0, DC[0] - 60, DC[1] + 40, 1.6], [w("Congress"), DC[0] - 260, DC[1] + 220, 1.15], [END, (DC[0] + GULF[0]) / 2, (DC[1] + GULF[1]) / 2 + 60, 0.95]]);
S.pin(DC, "WASHINGTON, D.C.", { t: 0.0, anchor: "r", rings: false });
S.date("NOV 2003", w("November"));
S.route(S.arcPts(DC, GULF, -0.18), { t: w("Congress"), dur: 1.7, width: 8, head: "dot", headSize: 1.2 });
S.pin(GULF, null, { t: w("Congress") + 1.6 });
S.label("GULF OF MEXICO", G(27.6, -90.0), { t: w("Navy"), anchor: "c", size: 44, color: "rgba(230,240,240,.9)" });
S.tag("WARSHIPS → REEFS", GULF, { t: w("donate"), anchor: "r", gap: 40, boxColor: "rgba(150,110,20,.95)" });
S.finish();
