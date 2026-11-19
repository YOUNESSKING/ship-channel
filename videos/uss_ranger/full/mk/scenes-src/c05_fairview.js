// BASEMAP: pnw
// COLUMBIA RIVER traced from the mouth on 'Columbia'; PORTLAND label; FAIRVIEW, OREGON pin on 'Fairview'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const FV = P("FAIRVIEW"), PO = P("PORTLAND"), MO = P("COLMOUTH");
S.camera([[0, 1480, 1030, 1.9], [END, 1440, 1010, 1.7]]);
S.pin(FV, "FAIRVIEW, OREGON", { t: wt("Fairview", 1.56), color: RED, anchor: "r", size: 44, gap: 36, dy: 36, ringR: 34 });
S.route(S.path(S.COL), { t: wt("Columbia", 3.34) - 0.9, dur: 2.3, width: 7, color: ST, ease: "none" });
S.label("COLUMBIA RIVER", G(46.17, -123.4), { t: wt("Columbia", 3.34), anchor: "t", size: 44, gap: 28, color: ST });
S.dot(MO, { t: wt("Columbia", 3.34) - 0.9, r: 9, color: WH });
S.label("PORTLAND", PO, { t: wt("Portland", 4.5), anchor: "l", size: 42, gap: 36, dy: 8 });
S.finish();
