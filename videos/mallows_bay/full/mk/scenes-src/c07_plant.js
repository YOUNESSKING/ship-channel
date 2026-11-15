// BASEMAP: baycl
// 'The power company had been quietly buying the land beside the fleet for a new power plant.' farm outline; tag on 'plant'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const SP = S.P("SANDY"), MB = S.P("MALLOWS");
S.camera([[0, MB[0], MB[1], 1.7], [END, SP[0], SP[1] + 20, 2.1]]);
S.hulls([MB[0] - 34, MB[1] - 10], { t: 0.0, rows: 5, cols: 7, len: 22, rot: 25, ragged: true, stagger: 0.0 });
S.poly([[[-77.268, 38.479], [-77.252, 38.483], [-77.244, 38.494], [-77.258, 38.499], [-77.270, 38.492], [-77.268, 38.479]]], { t: wt("land", 1.8), color: "#e3c27a", fill: 0.22 });
S.tag("PEPCO LAND", SP, { t: wt("land", 1.8), anchor: "r", gap: 70 });
S.tag("PLANNED POWER PLANT", SP, { t: wt("plant", 4.4), anchor: "r", gap: 70, dy: 64, boxColor: "rgba(150,40,30,.92)" });
S.finish();
