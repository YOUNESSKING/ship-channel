// BASEMAP: chesa
// 'The biggest gathering was in the James River, in Virginia.' pin JAMES RIVER on 'James'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const J = S.P("JAMES");
S.clouds(5, 0.12);
S.camera([[0, J[0] + 100, J[1] - 200, 0.95], [END, J[0] + 40, J[1] - 40, 1.4]]);
S.label("VIRGINIA", G(37.5, -77.6), { t: wt("Virginia", 2.8), anchor: "c", size: 52 });
S.pin(J, "JAMES RIVER", { t: wt("James", 2.0), anchor: "r", color: "#D9572B" });
S.tag("LAID UP", J, { t: wt("gathering", 0.8), anchor: "b", gap: 50 });
S.finish();
