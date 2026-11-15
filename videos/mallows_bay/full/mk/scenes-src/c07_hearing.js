// BASEMAP: potomac
// 'In 1970, at a hearing in Congress, a vice-president...' date; Washington; 'HOUSE HEARING' on 'hearing'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const WH = S.P("WH");
S.camera([[0, WH[0], WH[1] + 80, 1.3], [END, WH[0], WH[1] + 40, 1.6]]);
S.date("JULY 1970", wt("seventy", 0.4));
S.pin(WH, "WASHINGTON", { t: 0.2, anchor: "r" });
S.tag("HOUSE HEARING", WH, { t: wt("hearing", 1.6), anchor: "b", gap: 56, size: 46, boxColor: "rgba(150,40,30,.92)" });
S.finish();
