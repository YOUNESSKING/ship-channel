// BASEMAP: persian
// IRAN on 'Iran'; 1980 on 'eighty'; ARABIAN SEA on 'Arabian'; carrier in the Arabian Sea.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const AR = G(17.5, 63);
S.camera([[0, 1580, 860, 0.85], [END, 1650, 930, 1.0]]);
S.date("1980", wt("eighty", 0.61));
S.label("IRAN", P("IRAN"), { t: wt("Iran", 1.72), anchor: "c", size: 64 });
S.label("ARABIAN SEA", G(14.5, 63), { t: wt("Arabian", 4.48), anchor: "c", size: 60, color: ST });
const cv = S.cv(AR, { t: wt("waited", 3.7), len: 130, rot: 20 });
S.ring(AR, { t: wt("waited", 3.7), r: 70, color: RED });
S.finish();
