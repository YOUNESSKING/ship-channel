// BASEMAP: baycl
// 'On 7 Nov 1925...' date on 'seventh'; Sandy Point, Mallows Bay, Quantico across the river.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const MB = S.P("MALLOWS"), Q = S.P("QUANTICO"), SP = S.P("SANDY");
S.camera([[0, MB[0] - 40, MB[1] - 40, 1.0], [END, MB[0] - 20, MB[1] - 20, 1.3]]);
S.date("7 NOV 1925", wt("seventh", 0.4));
S.pin(MB, "MALLOWS BAY", { t: 0.3, anchor: "r", color: "#D9572B" });
S.label("SANDY POINT", SP, { t: 0.8, anchor: "r", size: 38 });
S.pin(Q, "QUANTICO", { t: 1.2, anchor: "l", rings: false });
S.finish();
