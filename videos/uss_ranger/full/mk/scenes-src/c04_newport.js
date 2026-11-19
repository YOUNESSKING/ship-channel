// BASEMAP: hampton
// NEWPORT NEWS pin on 'Newport'; VIRGINIA label on 'Virginia'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const NN = P("NEWPORTNEWS"), NF = P("NORFOLK");
S.camera([[0, 1430, 830, 1.5], [END, 1428, 826, 1.7]]);
S.pin(NN, "NEWPORT NEWS", { t: wt("Newport", 1.25), color: RED, anchor: "l", size: 48, gap: 36, dy: -20, ringR: 34 });
S.label("VIRGINIA", G(37.25, -76.9), { t: wt("Virginia", 2.55), anchor: "c", size: 60, color: ST });
S.finish();
