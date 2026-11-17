// BASEMAP: bikini
// 25 JULY 1946 on 'twenty'; TEST BAKER stamp on 'Baker'; burst point ringed.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const AIM = P("AIM"), BB = P("BURSTB");
S.camera([[0, 1495, 832, 2.3], [END, 1505, 833, 2.5]]);
S.scatter(AIM, 38, 4600, 7, AIM, 450).forEach((p) => S.dot(p, { t: 0, r: 10, color: "#f3eee2" }));
S.dot(AIM, { t: 0.1, r: 11, color: "#D9572B" });
S.date("25 JULY 1946", wt("twenty", 0.6));
S.tag("TEST BAKER", S.off(AIM, 0, 3500), { t: wt("Baker", 3.4), anchor: "c", size: 84, boxColor: "rgba(150,40,30,.92)" });
S.ring(BB, { t: wt("Baker", 3.4), r: 44, color: "#f3eee2" });
S.finish();
