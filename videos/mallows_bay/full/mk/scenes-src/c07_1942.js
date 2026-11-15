// BASEMAP: baycl
// 'In 1942, the government hired one of the biggest steel companies in the country.' date; bay pin.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const MB = S.P("MALLOWS");
S.camera([[0, MB[0], MB[1], 1.2], [END, MB[0], MB[1], 1.7]]);
S.date("1942", wt("forty", 0.5));
S.pin(MB, "MALLOWS BAY", { t: 0.2, anchor: "r", color: "#D9572B" });
S.hulls([MB[0] - 34, MB[1] - 10], { t: 0.0, rows: 6, cols: 8, len: 24, rot: 25, ragged: true, stagger: 0.004 });
S.tag("STEEL FOR THE WAR", MB, { t: wt("steel", 3.5), anchor: "b", gap: 90 });
S.finish();
