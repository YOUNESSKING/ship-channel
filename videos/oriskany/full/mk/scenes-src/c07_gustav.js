// BASEMAP: gulf7
// "Among them was Hurricane Gustav, in two thousand eight." Gustav track (Sept 2008, approx. NHC best track) across the Gulf, west of the wreck pin.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF");
const GT = S.path([[22.6, -83.4], [23.9, -85.0], [25.3, -86.6], [26.6, -88.1], [27.9, -89.5], [29.1, -90.7], [30.6, -91.7]]);
S.camera([[0, 1700, 900, 0.95], [END, 1640, 800, 1.1]]);
S.pin(REEF, "USS ORISKANY", { t: 0.0, anchor: "r", box: true, size: 40 });
S.hurricane(GT, { t: 0.05, dur: END, size: 110 });
S.tag("GUSTAV · 2008", GT[2], { t: w("Gustav"), anchor: "l", gap: 70, boxColor: "rgba(120,30,30,.92)" });
S.finish();
