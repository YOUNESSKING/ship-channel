// BASEMAP: potomac
// 'On the Maryland shore of the Potomac, in Charles County': state labels, river label, county on 'Charles'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const MB = S.P("MALLOWS"), WH = S.P("WH");
S.clouds(5, 0.12);
S.camera([[0, WH[0] + 60, WH[1] + 260, 0.9], [END, MB[0] + 60, MB[1] - 60, 1.15]]);
S.label("MARYLAND", G(38.62, -76.95), { t: wt("Maryland", 0.2), anchor: "c", size: 56 });
S.label("VIRGINIA", G(38.55, -77.55), { t: wt("Maryland", 0.2) + 0.3, anchor: "c", size: 56 });
S.label("POTOMAC RIVER", G(38.62, -77.18), { t: wt("Potomac", 1.0), anchor: "c", size: 40, color: "#cfe3ea" });
S.tag("CHARLES COUNTY", G(38.5, -77.12), { t: wt("Charles", 2.2), anchor: "c" });
S.finish();
