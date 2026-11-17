// BASEMAP: bikini_close
// Baker, distances from the burst (APPROX. POSITIONS). Shared frame c06_dist_a/b.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const C = P("BURSTB"), ON = (rM, ang) => S.off(C, rM * Math.cos(ang * Math.PI / 180), rM * Math.sin(ang * Math.PI / 180));
S.camera([[0, C[0], C[1] - 4, 3.0], [END, C[0], C[1] - 2, 3.05]]);
S.burst(C, 0, { r: 40 });
S.tag("APPROX. POSITIONS", [C[0], C[1] + 120], { t: 0.3, anchor: "c", size: 38, boxColor: "rgba(30,64,92,.92)" });
const AK = S.yd(240);
S.circ(C, AK, { t: wt("two", 1.8), color: "#f3eee2" });
S.ship("bb", ON(AK, 135), { t: wt("Arkansas", 1.0), len: 62, rot: 0, fill: "#b3cadf", stroke: "#0c1218", sw: 2.2 });
S.label("ARKANSAS · 240 YD", ON(AK, 135), { t: wt("two", 1.8), anchor: "l", size: 44, gap: 50 });
S.finish();
