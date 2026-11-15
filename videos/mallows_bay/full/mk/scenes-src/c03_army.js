// BASEMAP: atlantic
// 'Now it had to send an army across the Atlantic.' arc from the US east coast to France.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const NY = S.P("NYC"), FR = S.P("FRANCE");
S.camera([[0, (NY[0] + FR[0]) / 2, NY[1] - 40, 0.85], [END, (NY[0] + FR[0]) / 2 + 40, NY[1] - 60, 0.92]]);
S.pin(NY, null, { t: 0.0, rings: false });
S.route(S.arcPts(NY, FR, -0.18), { t: wt("send", 0.4), dur: 2.4, dash: [16, 10], head: "ship", headSize: 1.3 });
S.pin(FR, "FRANCE", { t: wt("Atlantic", 2.4), anchor: "r" });
S.tag("AN ARMY", [(NY[0] + FR[0]) / 2, NY[1] - 90], { t: wt("army", 1.2), anchor: "t", gap: 10 });
S.finish();
