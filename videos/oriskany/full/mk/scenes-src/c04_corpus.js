// BASEMAP: gulf7
// "The work was done in Corpus Christi, Texas, and took eleven months." Pin CORPUS CHRISTI; '11 MONTHS' on 'eleven' (FACTCHECK_B B7).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const CC = S.P("CORPUS");
S.clouds(5, 0.14);
S.camera([[0, 1000, 760, 0.9], [w("Corpus") + 0.6, CC[0] + 160, CC[1] - 60, 1.6], [END, CC[0] + 140, CC[1] - 50, 1.75]]);
S.pin(CC, "CORPUS CHRISTI", { t: w("Corpus"), anchor: "r" });
S.label("TEXAS", G(30.6, -98.2), { t: w("Texas"), anchor: "c", size: 48, color: "rgba(243,238,226,.9)" });
S.tag("11 MONTHS", CC, { t: w("eleven"), anchor: "b", gap: 50, size: 46, boxColor: "rgba(150,110,20,.95)" });
S.finish();
