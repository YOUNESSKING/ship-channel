// BASEMAP: vietnam
// GULF OF TONKIN on 'waters'; SUMMER 1964 on 'summer'; carrier at Yankee Station.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const YS = P("YANKEE");
S.camera([[0, 1380, 780, 1.3], [END, 1400, 790, 1.5]]);
S.date("SUMMER 1964", wt("summer", 0.34));
S.label("GULF OF TONKIN", P("TONKIN"), { t: wt("waters", 3.3), anchor: "c", size: 54, color: ST });
S.label("VIETNAM", G(16.5, 106.3), { t: wt("Vietnam", 3.9), anchor: "c", size: 52 });
const cv = S.cv(G(15.5, 112), { t: wt("sailed", 2.6), len: 120, rot: 150 });
S.sail(cv, S.path([[15.5, 112], [16.5, 110], [17.5, 108.5]]), { t: wt("sailed", 2.6), dur: 1.2, ease: "power2.out" });
S.pin(YS, "YANKEE STATION", { t: wt("sailed", 2.6) + 1.2, color: RED, anchor: "r", size: 40, gap: 70, dy: 40, ringR: 40 });
S.finish();
