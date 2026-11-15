// BASEMAP: atlantic
// 'Then, on 11 Nov 1918, the war ended.' date on 'eleventh'; 'ARMISTICE' on 'ended'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const FR = S.P("ARMEUR");
S.clouds(6, 0.14);
S.camera([[0, FR[0] - 200, FR[1] + 40, 1.05], [END, FR[0] - 120, FR[1] + 20, 1.25]]);
S.date("11 NOV 1918", wt("eleventh", 0.5));
S.pin(FR, "FRANCE", { t: 0.2, anchor: "r" });
S.tag("ARMISTICE", FR, { t: wt("ended", 3.6), anchor: "t", gap: 54, size: 50, boxColor: "rgba(150,40,30,.92)" });
S.finish();
