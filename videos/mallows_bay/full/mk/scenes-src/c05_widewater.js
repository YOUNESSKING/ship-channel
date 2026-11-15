// BASEMAP: potomac
// 'Most were anchored off Widewater, Virginia, near the Marine base at Quantico.' pins on their words.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const WW = S.P("WIDEWATER"), Q = S.P("QUANTICO");
S.camera([[0, WW[0] + 60, WW[1] - 40, 1.2], [END, WW[0] + 40, WW[1] - 30, 1.7]]);
S.pin(WW, "WIDEWATER, VIRGINIA", { t: wt("Widewater", 0.6), anchor: "l", color: "#D9572B" });
S.pin(Q, "MARINE BASE, QUANTICO", { t: wt("Quantico", 3.8), anchor: "l", rings: false });
S.finish();
