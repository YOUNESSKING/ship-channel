// BASEMAP: sandiego
// RANGER icon at the North Island carrier pier; JULY 1985 on 'weeks'; CORONADO label.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const NI = P("NORTHISLAND"), CO = P("CORONADO");
S.camera([[0, 1450, 815, 2.0], [END, 1452, 813, 2.3]]);
S.date("JULY 1985", wt("weeks", 0.66));
S.label("CORONADO", CO, { t: wt("Coronado", 2.1), anchor: "b", size: 44, gap: 50, color: ST });
const cv = S.cv(NI, { t: wt("Ranger", 3.3), len: 120, rot: -25 });
S.label("USS RANGER", NI, { t: wt("Ranger", 3.3) + 0.2, anchor: "t", size: 42, gap: 50 });
S.finish();
