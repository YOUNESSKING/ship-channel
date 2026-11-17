// BASEMAP: bikini
// 1 JULY 1946 on 'July'; TEST ABLE stamp on 'Able'; orange aim-point dot in the array.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const AIM = P("AIM");
S.camera([[0, 1495, 832, 2.3], [END, 1505, 833, 2.5]]);
S.scatter(AIM, 38, 4600, 7, AIM, 450).forEach((p) => S.dot(p, { t: 0, r: 10, color: "#f3eee2" }));
S.dot(AIM, { t: 0.1, r: 12, color: "#D9572B" }); S.ring(AIM, { t: 0.1, r: 40, color: "#D9572B" });
S.date("1 JULY 1946", wt("July", 1.0));
S.tag("TEST ABLE", S.off(AIM, 0, 3500), { t: wt("Able", 3.4), anchor: "c", size: 84, boxColor: "rgba(150,40,30,.92)" });
S.finish();
