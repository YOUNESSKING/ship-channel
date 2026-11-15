// BASEMAP: atlantic
// 'Some of them did cross the Atlantic, carrying coal and cargo.' dashed routes with ship heads; tag on 'coal'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const NY = S.P("NYC"), FR = S.P("FRANCE"), UK = S.P("BRITAIN");
S.camera([[0, (NY[0] + FR[0]) / 2, NY[1] - 40, 0.85], [END, (NY[0] + FR[0]) / 2 + 20, NY[1] - 50, 0.9]]);
S.route(S.arcPts(NY, FR, -0.16), { t: 0.2, dur: 3.0, dash: [16, 10], head: "ship", headSize: 1.2 });
S.route(S.arcPts(G(36.8, -76.3), UK, -0.2), { t: 0.6, dur: 3.0, dash: [16, 10], head: "ship", headSize: 1.2 });
S.tag("COAL & CARGO", [(NY[0] + FR[0]) / 2, NY[1] + 110], { t: wt("coal", 2.8), anchor: "c" });
S.finish();
