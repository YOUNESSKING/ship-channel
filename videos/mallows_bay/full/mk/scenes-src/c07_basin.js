// BASEMAP: baycl
// 'Bethlehem built a basin at the edge of the bay, with dams and gates.' basin outlined on 'basin'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const BA = S.P("BASIN"), MB = S.P("MALLOWS");
S.camera([[0, MB[0], MB[1], 2.2], [END, BA[0], BA[1], 3.0]]);
S.hulls([MB[0] - 34, MB[1] - 10], { t: 0.0, rows: 6, cols: 8, len: 22, rot: 25, ragged: true, stagger: 0.0 });
S.ring(BA, { t: wt("basin", 1.0), r: 46, color: "#D9572B" });
S.tag("BURNING BASIN", BA, { t: wt("basin", 1.0), anchor: "r", gap: 60, boxColor: "rgba(150,40,30,.92)" });
S.label("DAMS + GATES", BA, { t: wt("gates", 3.6), anchor: "b", gap: 70, size: 38 });
S.finish();
