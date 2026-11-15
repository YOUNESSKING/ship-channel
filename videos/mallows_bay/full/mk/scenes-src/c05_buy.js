// BASEMAP: baycl
// 'In April 1924, it bought land...' date; bay pin; tag 'BOUGHT' on 'bought'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const MB = S.P("MALLOWS"), WW = S.P("WIDEWATER");
S.camera([[0, MB[0] - 60, MB[1], 1.0], [END, MB[0] + 20, MB[1], 1.35]]);
S.date("APRIL 1924", wt("April", 0.3));
S.label("WIDEWATER", WW, { t: 0.0, anchor: "l", size: 40 });
S.pin(MB, null, { t: 0.4, color: "#D9572B" });
S.tag("BOUGHT", MB, { t: wt("bought", 2.0), anchor: "r", gap: 50, size: 46, boxColor: "rgba(150,40,30,.92)" });
S.finish();
