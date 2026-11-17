// BASEMAP: marshalls
// Hook frame 0: clean map + Bikini pin; camera pushes in on the atoll. '1 JULY 1946' on 'July', 'BIKINI ATOLL' on 'nineteen'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const BK = P("BIKINI");
S.camera([[0, BK[0] + 150, BK[1] + 120, 0.9], [END, BK[0] + 15, BK[1] + 10, 2.0]]);
S.pin(BK, null, { t: 0.0, color: "#D9572B", ringR: 40 });
S.date("1 JULY 1946", wt("July", 1.0));
S.label("BIKINI ATOLL", BK, { t: wt("nineteen", 2.2), anchor: "r", size: 52, gap: 50, dy: -30 });
S.finish();
