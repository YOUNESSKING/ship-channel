// BASEMAP: baycl
// 'a company called Idamont bought the farm on Sandy Point, right beside the bay.' farm outline; 'IDAMONT' on 'Idamont'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const SP = S.P("SANDY"), MB = S.P("MALLOWS");
S.camera([[0, SP[0], SP[1] + 20, 1.9], [END, SP[0] + 10, SP[1] + 30, 2.2]]);
S.hulls([MB[0] - 34, MB[1] - 10], { t: 0.0, rows: 5, cols: 7, len: 22, rot: 25, ragged: true, stagger: 0.0 });
S.poly([[[-77.268, 38.479], [-77.252, 38.483], [-77.244, 38.494], [-77.258, 38.499], [-77.270, 38.492], [-77.268, 38.479]]], { t: wt("farm", 1.8), color: "#e3c27a", fill: 0.22 });
S.tag("IDAMONT", SP, { t: wt("Idamont", 0.8), anchor: "r", gap: 70, size: 48, boxColor: "rgba(150,40,30,.92)" });
S.label("THE FARM", SP, { t: wt("farm", 1.8), anchor: "r", gap: 70, dy: 64, size: 36 });
S.finish();
