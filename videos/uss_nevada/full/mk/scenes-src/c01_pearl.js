// BASEMAP: pearl
// Hook: Nevada leaves F-8 and runs down the channel on 'got under way'; 'THE ONLY BATTLESHIP UNDER WAY' on 'only'.
const S = ShipK(), END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1490, 800, 1.12], [END, 1490, 800, 1.14]]);
S.date("PEARL HARBOR · 7 DEC 1941", wt("Pearl", 0.2));
S.rowShips({ t: 0.2, len: 30 });
const nv = S.ship("bb", P("NV"), { t: 0.2, len: 48, rot: 135, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
S.ring(P("NV"), { t: 0.4, r: 36, color: "#D9572B" });
S.label("NEVADA", P("NV"), { t: wt("Nevada", 0.5), anchor: "r", gap: 70, dy: -50 });
const go = wt("got", 3.6), path = S.path(S.RUN);
S.tag("THE ONLY BATTLESHIP UNDER WAY", [1470, 900], { t: wt("only", 2.6), anchor: "r", size: 40, boxColor: "rgba(150,40,30,.92)" });
S.route(path.slice(1), { t: go, dur: END - go - 0.25, ease: "power1.inOut", color: "#D9572B", dash: [14, 10], width: 5 });
S.sail(nv, path, { t: go, dur: END - go - 0.25, ease: "power1.inOut" });
S.finish();
