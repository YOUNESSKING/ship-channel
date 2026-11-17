// BASEMAP: pacific
// Camera from Hawaii west to the Marshall Islands; PACIFIC OCEAN, MARSHALL ISLANDS on 'Marshall', BIKINI ATOLL pin on 'Bikini'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const BK = P("BIKINI"), PH = P("PEARL");
S.camera([[0, PH[0] - 40, PH[1] + 20, 2.0], [END, BK[0] + 60, BK[1] - 30, 3.2]]);
S.label("PACIFIC OCEAN", S.G(17, 190), { t: 0.2, anchor: "c", size: 52 });
S.dot(PH, { t: 0.3, r: 9, color: "#f3eee2" }); S.label("HAWAII", PH, { t: 0.3, anchor: "r", size: 40, gap: 30, color: "#8fb0cc" });
S.label("MARSHALL ISLANDS", S.G(9.0, 168), { t: wt("Marshall", 2.2), anchor: "r", size: 44, gap: 20, dy: 90 });
S.pin(BK, "BIKINI ATOLL", { t: wt("Bikini", 0.9), color: "#D9572B", anchor: "l", size: 52, gap: 40, dy: -30, ringR: 40 });
S.finish();
