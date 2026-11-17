// BASEMAP: pearl
// Nevada runs down the channel toward the entrance; TO THE OPEN SEA on 'open'. Starts where c03_underway ended.
const S = ShipK(), END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1490, 800, 1.14], [END, 1490, 800, 1.14]]);
S.rowShips({ t: 0, len: 30 });
const path = S.path(S.RUN).slice(1);
const nv = S.ship("bb", path[0], { t: 0, len: 48, rot: 135, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
const go = wt("headed", 1.4), dur = END - go - 0.3;
S.route(path, { t: go, dur, ease: "power1.inOut", color: "#D9572B", dash: [14, 10], width: 5 });
S.sail(nv, path, { t: go, dur, ease: "power1.inOut" });
S.label("THE CHANNEL", [1348, 950], { t: wt("channel", 2.4), anchor: "l", size: 42, gap: 40 });
S.tag("TO THE OPEN SEA", [1430, 1100], { t: wt("open", 3.4), anchor: "r", size: 42, gap: 30, boxColor: "rgba(150,40,30,.92)" });
S.finish();
