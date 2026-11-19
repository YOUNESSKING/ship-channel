// BASEMAP: persian
// DECEMBER 1990 on 'December'; carrier sails through Hormuz into the Persian Gulf; Persian Gulf label.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const path = S.path([[22.5, 61.5], [24.6, 59.2], [25.4, 57.0], [26.5, 56.3], [26.5, 54.0], [26.6, 52.5], [27.3, 50.8], [28.2, 49.8]]);
S.camera([[0, 1700, 950, 0.95], [3.0, 1600, 880, 1.15], [END, 1480, 800, 1.35]]);
S.date("DECEMBER 1990", wt("December", 0.26));
const t0 = wt("left", 2.3) - 0.2, cv = S.cv(path[0], { t: t0, len: 120, rot: 0 });
S.sail(cv, path, { t: t0, dur: END - t0 - 0.5, ease: "power1.inOut" });
S.label("(FROM SAN DIEGO)", path[0], { t: wt("San", 2.54), anchor: "b", size: 34, gap: 50, color: ST, until: 3.6 });
S.label("PERSIAN GULF", G(25.9, 52.6), { t: wt("Persian", 3.68), anchor: "c", size: 56, color: ST });
S.label("STRAIT OF HORMUZ", P("HORMUZ"), { t: wt("Gulf", 3.98), anchor: "r", size: 36, gap: 40, dy: 36 });
S.finish();
