// BASEMAP: atlantic
// Route from the US east coast across to Britain; ATLANTIC OCEAN on 'Atlantic'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const NF = P("NORFOLK"), BR = P("BANGOR"), MID = [(NF[0] + BR[0]) / 2, (NF[1] + BR[1]) / 2];
S.camera([[0, MID[0], MID[1] + 20, 1.05], [END, MID[0], MID[1] + 20, 1.15]]);
S.pin(NF, "U.S. EAST COAST", { t: 0.1, color: "#f3eee2", anchor: "r", size: 40, gap: 30, dy: 50, ringR: 30 });
S.route(S.arcPts(NF, BR, -0.12), { t: wt("crossed", 0.6), dur: 1.5, width: 6, color: "#D9572B", head: "ship" });
S.label("ATLANTIC OCEAN", S.G(44, -42), { t: wt("Atlantic", 1.6), anchor: "c", size: 56 });
S.pin(BR, "BRITAIN", { t: wt("Atlantic", 1.6) + 0.7, color: "#f3eee2", anchor: "l", size: 44, gap: 30, dy: -10, ringR: 30 });
S.finish();
