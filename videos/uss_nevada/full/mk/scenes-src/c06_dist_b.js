// BASEMAP: bikini_close
// Baker, distances from the burst (APPROX. POSITIONS). Shared frame c06_dist_a/b.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const C = P("BURSTB"), ON = (rM, ang) => S.off(C, rM * Math.cos(ang * Math.PI / 180), rM * Math.sin(ang * Math.PI / 180));
S.camera([[0, C[0] + 70, C[1] - 2, 3.4], [END, C[0] + 70, C[1], 3.45]]);
S.burst(C, 0, { r: 40 });
S.tag("APPROX. POSITIONS", [C[0] + 70, C[1] - 112], { t: 0.3, anchor: "c", size: 38, boxColor: "rgba(30,64,92,.92)" });
const AK = S.yd(240), SA = S.yd(380), NV = S.yd(1060);
S.circ(C, AK, { t: 0, color: "#f3eee2", dur: 0.01 });
S.ship("bb", ON(AK, 135), { t: 0, len: 62, rot: 0, fill: "#b3cadf", stroke: "#0c1218", sw: 2.2 });
S.label("ARKANSAS · 240 YD", ON(AK, 135), { t: 0, anchor: "l", size: 44, gap: 50 });
S.circ(C, SA, { t: wt("Nevada", 0.3), color: "#8fb0cc" });
S.ship("bb", ON(SA, 225), { t: wt("Nevada", 0.3), len: 80, rot: 0, fill: "#b3cadf", stroke: "#0c1218", sw: 2.2 });
S.label("SARATOGA · 380 YD", ON(SA, 225), { t: wt("Nevada", 0.3) + 0.2, anchor: "l", size: 44, gap: 50 });
S.circ(C, NV, { t: wt("thousand", 1.6), color: "#D9572B", dur: 0.9 });
S.ship("bb", ON(NV, 0), { t: wt("thousand", 1.6) + 0.3, len: 90, rot: 0, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
S.label("NEVADA · 1,060 YD", ON(NV, 0), { t: wt("thousand", 1.6) + 0.3, anchor: "r", size: 46, gap: 60, dy: -10 });
S.finish();
