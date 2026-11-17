// BASEMAP: pearl
// 08:40 on 'twenty', NO TUGS on 'tugs', Nevada backs away from F-8 on 'backed'. Shared frame with c03_run / block / hospital / waipio.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
S.camera([[0, 1490, 800, 1.12], [END, 1490, 800, 1.14]]);
S.rowShips({ t: 0, len: 30 });
const nv = S.ship("bb", P("NV"), { t: 0, len: 66, rot: 135, fill: "#f3eee2", stroke: "#D9572B", sw: 3.4 });
S.ring(P("NV"), { t: 0, r: 46, color: "#D9572B" });
S.tag("08:40", P("NV"), { t: wt("twenty", 1.0), anchor: "r", gap: 80, dy: -80, size: 48, boxColor: "rgba(150,40,30,.92)" });
S.tag("NO TUGS", P("NV"), { t: wt("tugs", 2.0), anchor: "r", gap: 80, dy: -5, size: 42 });
S.label("NEVADA", P("NV"), { t: wt("Nevada", 2.5), anchor: "r", gap: 80, dy: 70 });
const path = S.path(S.RUN.slice(0, 12)), b = wt("backed", 3.2);
S.sail(nv, [path[0], path[1]], { t: b, dur: Math.max(0.8, END - b - 0.1), keepRot: true, ease: "power1.inOut" });
S.finish();
