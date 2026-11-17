// BASEMAP: pearl
// If she sank in the narrow channel: channel highlighted, Nevada icon in the neck gets a red X on 'sank'.
const S = ShipK(), END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1490, 800, 1.14], [END, 1490, 810, 1.16]]);
const NECK = [[1318, 860], [1345, 900], [1350, 960], [1356, 1010], [1385, 1060], [1458, 1060], [1418, 1010], [1402, 960], [1402, 910], [1447, 860]];
const nv = S.ship("bb", [1378, 975], { t: wt("she", 2.3), len: 52, rot: 90, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
S.xmark([1378, 975], wt("sank", 3.0), { r: 26 });
S.fade(nv.inner, wt("sank", 3.0) + 0.3, 0.6, 0.55);
S.poly([NECK], { px: true, t: wt("narrow", 3.2), color: "#D9572B", fill: 0.28, width: 4 });
S.label("THE NARROW CHANNEL", [1420, 1010], { t: wt("narrow", 3.2), anchor: "r", size: 42, gap: 50 });
S.finish();
