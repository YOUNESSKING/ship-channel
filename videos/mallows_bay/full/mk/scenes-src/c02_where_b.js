// BASEMAP: baycl
// 'near a place called Nanjemoy, there is a small bay. Mallows Bay.' NANJEMOY on 'Nanjemoy'; pin MALLOWS BAY on 'Mallows'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const MB = S.P("MALLOWS"), NJ = S.P("NANJ");
S.camera([[0, MB[0] + 200, MB[1], 0.9], [END, MB[0] + 40, MB[1], 1.6]]);
S.label("NANJEMOY", NJ, { t: wt("Nanjemoy", 0.3), anchor: "c", size: 50 });
S.label("POTOMAC RIVER", G(38.43, -77.31), { t: 0.2, anchor: "c", size: 38, color: "#cfe3ea" });
S.pin(MB, null, { t: wt("bay", 1.8), color: "#D9572B" });
S.tag("MALLOWS BAY", MB, { t: wt("Mallows", 3.6), anchor: "l", gap: 44, size: 46, boxColor: "rgba(150,40,30,.92)" });
S.finish();
