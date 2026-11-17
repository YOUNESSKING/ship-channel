// BASEMAP: bikini
// Nevada (orange-outline icon) sails in from the SW reef gap to her mooring; 28 MAY 1946 on 'May'; CREW: 403 on 'four'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const AIM = P("AIM");
S.camera([[0, 1400, 880, 1.6], [END, 1470, 850, 1.9]]);
S.scatter(AIM, 20, 3200, 11, AIM, 450).forEach((p) => S.dot(p, { t: 0.2, r: 7, color: "#8fb0cc" }));
S.date("28 MAY 1946", wt("May", 0.9));
const path = [S.G(11.54, 165.36), S.G(11.555, 165.43), S.G(11.572, 165.48), AIM];
const nv = S.ship("bb", path[0], { t: 0.2, len: 80, rot: 0, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
S.route(path, { t: 0.5, dur: END - 1.2, ease: "power1.inOut", color: "#D9572B", dash: [14, 10], width: 5 });
S.sail(nv, path, { t: 0.5, dur: END - 1.2, ease: "power1.inOut" });
S.tag("CREW: 403", AIM, { t: wt("four", 3.4), anchor: "r", size: 48, gap: 90, dy: -60, boxColor: "rgba(150,40,30,.92)" });
S.label("NEVADA", AIM, { t: wt("sailed", 2.0), anchor: "r", size: 44, gap: 90, dy: 30 });
S.finish();
