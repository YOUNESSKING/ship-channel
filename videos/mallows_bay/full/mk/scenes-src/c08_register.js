// BASEMAP: baycl
// 'In April 2015, the wrecks were listed on...' date; bay pin.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const MB = S.P("MALLOWS");
S.camera([[0, MB[0], MB[1], 1.3], [END, MB[0], MB[1], 1.7]]);
S.date("APRIL 2015", wt("April", 0.3));
S.pin(MB, "MALLOWS BAY", { t: 0.3, anchor: "r", color: "#D9572B" });
S.finish();
