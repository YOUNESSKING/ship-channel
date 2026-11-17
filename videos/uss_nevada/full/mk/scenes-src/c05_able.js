// BASEMAP: bikini
// 1 JULY 1946 on 'July'; TEST ABLE stamp on 'Able'; orange aim-point dot in the array.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const AIM = P("AIM");
S.camera([[0, 1480, 826, 1.8], [END, 1500, 832, 2.0]]);
S.scatter(AIM, 38, 4200, 7, AIM, 450).forEach((p) => S.dot(p, { t: 0, r: 8, color: "#f3eee2" }));
S.dot(AIM, { t: 0.1, r: 12, color: "#D9572B" }); S.ring(AIM, { t: 0.1, r: 40, color: "#D9572B" });
S.date("1 JULY 1946", wt("July", 1.0));
S.tag("TEST ABLE", S.off(AIM, 0, 3200), { t: wt("Able", 3.4), anchor: "c", size: 84, boxColor: "rgba(150,40,30,.92)" });
S.finish();
