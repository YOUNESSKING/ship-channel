// BASEMAP: brownsville
// icon creeps up the ship channel to the yard; ~4 KNOTS on 'four'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const path = S.path(S.CHAN), PT = P("BROWNSVILLE");
S.camera([[0, 1520, 770, 2.2], [END, 1420, 830, 2.2]]);
S.route(path, { t: 0, dur: 0.01, width: 6, color: ST, dash: [14, 10] });
const cv = S.cv(path[0], { t: 0.1, len: 100, rot: 0 });
const at = S.sail(cv, path, { t: 0.2, dur: END - 0.5, ease: "none" });
const mid = at((wt("four", 3.36) - 0.2) / (END - 0.5));
S.tag("≈4 KNOTS", mid.slice(0, 2), { t: wt("four", 3.36), anchor: "t", size: 56, gap: 70, boxColor: "rgba(150,40,30,.92)" });
S.pin(PT, "PORT OF BROWNSVILLE", { t: 0.4, color: WH, anchor: "b", size: 36, gap: 40, ringR: 26 });
S.finish();
