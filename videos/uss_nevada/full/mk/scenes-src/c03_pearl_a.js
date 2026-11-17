// BASEMAP: pearl
// 'Pearl Harbor. The seventh of December, nineteen forty one.' Pearl Harbor label on 'Pearl', date on 'seventh', Ford Island label.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1500, 700, 0.95], [END, 1490, 800, 1.12]]);
S.label("PEARL HARBOR", [1215, 560], { t: wt("Pearl", 0.2), anchor: "c", size: 56 });
S.date("7 DECEMBER 1941", wt("seventh", 1.2));
S.label("FORD ISLAND", P("FORD"), { t: wt("nineteen", 3.2), anchor: "c", size: 40, color: "#8fb0cc" });
S.finish();
