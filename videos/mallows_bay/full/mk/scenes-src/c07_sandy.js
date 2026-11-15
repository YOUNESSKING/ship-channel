// BASEMAP: baycl
// 'Then, in October 1963,' date; pin SANDY POINT.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const SP = S.P("SANDY"), MB = S.P("MALLOWS");
S.camera([[0, MB[0], MB[1], 1.4], [END, SP[0], SP[1] + 20, 1.9]]);
S.date("OCT 1963", wt("October", 0.3));
S.hulls([MB[0] - 34, MB[1] - 10], { t: 0.0, rows: 5, cols: 7, len: 22, rot: 25, ragged: true, stagger: 0.0 });
S.pin(SP, "SANDY POINT", { t: 0.6, anchor: "r" });
S.finish();
