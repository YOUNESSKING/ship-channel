// BASEMAP: usa
// 'The first one slid into the water in Oregon on 1 Dec 1917.' pin NORTH BEND, OREGON; date on 'first'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const NB = S.P("NORTHBEND");
S.camera([[0, NB[0] + 300, NB[1], 1.0], [END, NB[0] + 220, NB[1], 1.5]]);
S.pin(NB, "NORTH BEND, OREGON", { t: wt("Oregon", 1.6), anchor: "r", color: "#D9572B" });
S.date("1 DEC 1917", wt("December", 3.0));
S.finish();
