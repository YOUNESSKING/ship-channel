// BASEMAP: potomac
// 'In April 1923, fire broke out again, this time at Widewater.' date; fire flash at Widewater on 'fire'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const WW = S.P("WIDEWATER");
S.camera([[0, WW[0] + 40, WW[1] - 20, 1.4], [END, WW[0] + 30, WW[1] - 10, 1.8]]);
S.date("APRIL 1923", wt("April", 0.3));
S.pin(WW, "WIDEWATER", { t: 0.0, anchor: "l", rings: false });
S.flashAt(WW, wt("fire", 2.0), { r: 44, keep: true, sfx: false });
S.tag("FIRE AGAIN", WW, { t: wt("again", 2.6), anchor: "t", gap: 60, boxColor: "rgba(150,40,30,.92)" });
S.finish();
