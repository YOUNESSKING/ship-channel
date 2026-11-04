// BASEMAP: vietnam
// "Between May and December nineteen sixty five," Gulf of Tonkin; pin YANKEE STATION (~17°30'N 108°30'E); date 1965 (MAY-DEC).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const YK = S.P("YANKEE");
S.clouds(6, 0.14);
S.camera([[0, 1440, 760, 0.85], [END, YK[0] - 120, YK[1] - 60, 1.35]]);
S.label("GULF OF TONKIN", G(19.9, 107.6), { t: 0.12, anchor: "c", size: 44, color: "rgba(230,240,240,.9)" });
S.date("MAY–DEC 1965", w("May"));
S.pin(YK, "YANKEE STATION", { t: w("December") - 0.2, anchor: "r", box: true, size: 42 });
S.finish();
