// BASEMAP: baycl
// 'But the wrecks were right in front of its land.' hulls highlighted in front of the farm.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const SP = S.P("SANDY"), MB = S.P("MALLOWS");
S.camera([[0, (SP[0] + MB[0]) / 2, (SP[1] + MB[1]) / 2, 2.2], [END, (SP[0] + MB[0]) / 2, (SP[1] + MB[1]) / 2, 2.5]]);
S.poly([[[-77.268, 38.479], [-77.252, 38.483], [-77.244, 38.494], [-77.258, 38.499], [-77.270, 38.492], [-77.268, 38.479]]], { t: 0.0, color: "#e3c27a", fill: 0.22 });
S.hulls([MB[0] - 34, MB[1] - 10], { t: 0.1, rows: 6, cols: 8, len: 24, rot: 25, ragged: true, color: "rgba(217,87,43,.95)" });
S.tag("THE WRECKS", MB, { t: wt("wrecks", 0.6), anchor: "b", gap: 100, boxColor: "rgba(150,40,30,.92)" });
S.finish();
