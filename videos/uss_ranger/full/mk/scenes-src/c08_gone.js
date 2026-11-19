// BASEMAP: brownsville
// RANGER icon at the yard fades out on 'gone'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const PT = P("BROWNSVILLE");
S.camera([[0, 1380, 840, 2.6], [END, 1372, 846, 2.9]]);
S.pin(PT, "PORT OF BROWNSVILLE", { t: 0.1, color: WH, anchor: "b", size: 36, gap: 50, ringR: 26 });
const cv = S.cv(S.off(PT, 0, 300), { t: 0.05, len: 130, rot: 200 });
S.fade(cv.wrap, wt("gone", 1.42), 0.6);
S.finish();
