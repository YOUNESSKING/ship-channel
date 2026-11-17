// BASEMAP: pearl
// ...block it and trap the whole fleet inside Pearl Harbor: fleet icons inside, channel stays blocked, CHANNEL BLOCKED? on 'trap'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1490, 810, 1.16], [END, 1490, 800, 1.14]]);
const NECK = [[1318, 860], [1345, 900], [1350, 960], [1356, 1010], [1385, 1060], [1458, 1060], [1418, 1010], [1402, 960], [1402, 910], [1447, 860]];
S.poly([NECK], { px: true, t: 0, color: "#D9572B", fill: 0.3, width: 4 });
const nv = S.ship("bb", [1378, 975], { t: 0, len: 66, rot: 90, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 }); S.fade(nv.inner, 0.01, 0.01, 0.55);
S.xmark([1378, 975], 0.02, { r: 26 });
S.rowShips({ t: wt("fleet", 2.2), len: 30 });
const more = [[1640, 650, "cru"], [1672, 628, "cru"], [1700, 600, "dd"], [1560, 505, "bb"], [1600, 520, "cru"], [1640, 535, "dd"], [1520, 455, "dd"], [1700, 650, "dd"], [1420, 430, "cru"], [1470, 480, "dd"]];
more.forEach((m, i) => S.ship(m[2], [m[0], m[1]], { t: wt("fleet", 2.2) + 0.12 * i, len: m[2] === "bb" ? 30 : 24, rot: 120, fill: "#8fb0cc", stroke: "#0c1218", sw: 2.2 }));
S.label("THE FLEET", [1640, 560], { t: wt("fleet", 2.2), anchor: "r", size: 42, gap: 60, dy: -40 });
S.tag("CHANNEL BLOCKED?", [1420, 1010], { t: wt("trap", 3.8), anchor: "r", size: 44, gap: 50, boxColor: "rgba(150,40,30,.92)" });
S.finish();
