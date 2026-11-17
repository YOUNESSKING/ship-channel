// BASEMAP: pearl
// Ordered out of the channel: Nevada turns to the shore at Hospital Point; 09:10 on 'ten'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1490, 810, 1.16], [END, 1470, 840, 1.2]]);
const HOSP = S.G(21.3410, -157.9645), st = [1372, 1040];
const nv = S.ship("bb", st, { t: 0, len: 66, rot: 100, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
S.pin(HOSP, "HOSPITAL POINT", { t: wt("ordered", 1.0), anchor: "r", size: 44, color: "#f3eee2", gap: 40 });
const path = [st, [1385, 1000], [1412, 940], [1432, 895], [1436, 875]], go = wt("ordered", 1.0) + 0.4;
S.route(path, { t: go, dur: END - go - 0.5, color: "#D9572B", dash: [14, 10], width: 5 });
S.sail(nv, path, { t: go, dur: END - go - 0.5, ease: "power2.inOut" });
S.tag("09:10", HOSP, { t: wt("ten", 3.0), anchor: "l", size: 48, gap: 50, dy: 10, boxColor: "rgba(150,40,30,.92)" });
S.finish();
