// BASEMAP: bikini
// Array of dots; one ORANGE dot pulses; NEVADA on 'chose', crosshair + BULL'S-EYE on "bull's", AIM POINT on 'aim'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const AIM = P("AIM");
S.camera([[0, 1500, 832, 2.0], [END, 1512, 834, 2.5]]);
S.scatter(AIM, 38, 4200, 7, AIM, 450).forEach((p) => S.dot(p, { t: 0, r: 8, color: "#f3eee2" }));
S.dot(AIM, { t: 0.1, r: 12, color: "#D9572B" }); S.ring(AIM, { t: 0.1, r: 40, color: "#D9572B" });
S.label("NEVADA", AIM, { t: wt("chose", 0.8), anchor: "r", size: 52, gap: 70, dy: 70, color: "#f7f3ea" });
S.cross(AIM, { t: wt("bull's", 1.8), r: 52, color: "#f3eee2" });
S.tag("BULL'S-EYE", AIM, { t: wt("bull's", 1.8), anchor: "l", size: 48, gap: 130, dy: -70, boxColor: "rgba(150,40,30,.92)" });
S.label("AIM POINT", AIM, { t: wt("aim", 3.8), anchor: "l", size: 46, gap: 130, dy: 20 });
S.finish();
