// BASEMAP: oahu_sw
// 26 JULY 1948 on 'twenty'; tow line from Pearl Harbor out to sea toward the SW.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const PH = P("PEARL"), WR = P("WRECK");
S.camera([[0, 1560, 760, 1.25], [END, 1420, 810, 1.3]]);
S.date("26 JULY 1948", wt("twenty", 0.5));
S.pin(PH, "PEARL HARBOR", { t: 0.2, color: "#f3eee2", anchor: "r", size: 44, gap: 40, dy: 30, ringR: 32 });
const a = wt("twenty", 0.5) + 0.4, d = END - a - 0.3, path = [PH, S.G(21.2, -158.2), S.G(21.05, -158.6), WR];
S.route(path, { t: a, dur: d, dash: [16, 12], width: 5, color: "#D9572B", ease: "power1.inOut" });
const nv = S.ship("bb", PH, { t: a - 0.2, len: 60, rot: 180, fill: "#f3eee2", stroke: "#D9572B", sw: 3.2 }); S.sail(nv, path, { t: a, dur: d, ease: "power1.inOut" });
S.finish();
