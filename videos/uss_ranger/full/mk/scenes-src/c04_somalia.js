// BASEMAP: somalia
// SOMALIA on 'Somalia'; MOGADISHU pin; DECEMBER 1992 on 'December'; carrier offshore.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const MG = P("MOGADISHU"), CVp = G(1.5, 47.0);
S.camera([[0, 1420, 820, 1.4], [END, 1430, 815, 1.65]]);
S.date("DECEMBER 1992", wt("December", 0.36));
S.label("SOMALIA", G(3.9, 42.8), { t: wt("Somalia", 3.0), anchor: "c", size: 64 });
S.pin(MG, "MOGADISHU", { t: 0.9, color: RED, anchor: "l", size: 44, gap: 36, dy: 30, ringR: 32 });
S.cv(CVp, { t: wt("off", 2.8), len: 100, rot: 35 });
S.finish();
