// BASEMAP: baycl
// 'Over the next years, the burned hulls were packed into Mallows Bay.' hull ovals fill the bay in rows.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const MB = S.P("MALLOWS");
S.camera([[0, MB[0], MB[1], 2.0], [END, MB[0] - 10, MB[1], 2.6]]);
S.hulls([MB[0] - 34, MB[1] - 10], { t: wt("packed", 1.5) - 0.6, rows: 7, cols: 9, len: 30, rot: 25, ragged: true });
S.tag("MALLOWS BAY", MB, { t: 0.2, anchor: "r", gap: 120 });
S.finish();
