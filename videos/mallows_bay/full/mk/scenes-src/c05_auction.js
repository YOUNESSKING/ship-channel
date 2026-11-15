// BASEMAP: potomac
// 'On 12 Sept 1922, the government gave up.' Washington pin; date on 'twelfth'; 'AUCTION' on 'gave'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const WH = S.P("WH");
S.camera([[0, WH[0], WH[1] + 120, 1.0], [END, WH[0], WH[1] + 60, 1.3]]);
S.date("12 SEPT 1922", wt("twelfth", 0.4));
S.pin(WH, "WASHINGTON", { t: 0.2, anchor: "r" });
S.tag("AUCTION", WH, { t: wt("gave", 3.2), anchor: "b", gap: 56, size: 50, boxColor: "rgba(150,40,30,.92)" });
S.finish();
