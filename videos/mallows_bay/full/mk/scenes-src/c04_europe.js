// BASEMAP: atlantic
// 'not one of the wooden ships reached a port in Europe while the fighting lasted' dashed arc stops short; tag.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const NY = S.P("NYC"), FR = S.P("FRANCE");
const A = S.arcPts(NY, FR, -0.18);
S.camera([[0, (NY[0] + FR[0]) / 2, NY[1] - 40, 0.85], [END, (NY[0] + FR[0]) / 2 + 30, NY[1] - 50, 0.9]]);
S.pin(FR, "EUROPE", { t: 0.0, anchor: "r", rings: false });
S.route(A.slice(0, 15), { t: 0.2, dur: 1.8, dash: [16, 10], head: "ship", headSize: 1.3, color: "#e3c27a" });
S.tag("NO WOODEN SHIP IN A EUROPEAN PORT IN WARTIME", [(NY[0] + FR[0]) / 2, NY[1] + 120], { t: wt("not", 2.4), anchor: "c", size: 38, boxColor: "rgba(150,40,30,.92)" });
S.finish();
