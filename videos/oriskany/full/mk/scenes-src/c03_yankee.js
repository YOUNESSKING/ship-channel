// BASEMAP: vietnam
// "On the morning of the twenty sixth of October, nineteen sixty six," Gulf of Tonkin; pin YANKEE STATION; date 26 OCT 1966 (FACTCHECK_A C3).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const YK = S.P("YANKEE");
S.clouds(6, 0.14);
S.camera([[0, YK[0] - 260, YK[1] - 140, 1.0], [END, YK[0] - 40, YK[1] - 30, 1.6]]);
S.label("GULF OF TONKIN", G(19.9, 107.6), { t: 0.12, anchor: "c", size: 44, color: "rgba(230,240,240,.9)" });
S.img("assets/media/carrier_top.png", YK, { t: 0.3, w: 120, rot: -30, filter: "brightness(1.8) drop-shadow(0 0 12px rgba(227,194,122,.9))" });
S.ring(YK, { t: 0.3, r: 50 });
S.label("YANKEE STATION", YK, { t: 0.5, anchor: "b", gap: 56, box: true, size: 42 });
S.date("26 OCT 1966", w("twenty"));
S.finish();
