// BASEMAP: atlantic
// 'In April 1920, as many as 240 of them were in service.' date; ship icons on the Atlantic; '240 IN SERVICE' on 'forty'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const NY = S.P("NYC"), FR = S.P("FRANCE");
S.camera([[0, (NY[0] + FR[0]) / 2, NY[1] - 20, 0.85], [END, (NY[0] + FR[0]) / 2, NY[1] - 20, 0.92]]);
S.date("APRIL 1920", wt("April", 0.2));
[[38,-60],[42,-45],[46,-30],[40,-25],[35,-50],[44,-55],[48,-18],[36,-35]].forEach((p, i) => S.icon("tag", G(p[0], p[1]), { t: 0.6 + i * 0.2, size: 40, color: "#f3eee2" }));
S.tag("240 IN SERVICE", [(NY[0] + FR[0]) / 2, NY[1] + 130], { t: wt("forty", 3.0), anchor: "c", size: 48, boxColor: "rgba(150,40,30,.92)" });
S.finish();
