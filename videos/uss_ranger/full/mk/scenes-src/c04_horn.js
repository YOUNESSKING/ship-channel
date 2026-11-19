// BASEMAP: americas
// 1958 route Norfolk -> Atlantic -> Cape Horn -> San Diego; '1958' on 'summer'; CAPE HORN on 'Horn'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const NF = P("NORFOLK"), SD = P("SANDIEGO"), CH = P("CAPEHORN");
S.camera([[0, 1440, 810, 0.667], [END, 1440, 810, 0.7]]);
S.date("1958", wt("summer", 0.44));
S.pin(NF, "NORFOLK", { t: 0.3, color: WH, anchor: "r", size: 40, gap: 28, ringR: 26 });
const route58 = [[36.95, -76.3], [31, -72], [24, -66], [12, -53], [0, -38.5], [-12, -33.5], [-24, -41], [-36, -52], [-48, -60], [-55, -64], [-56.2, -67.3], [-55, -73], [-46, -77.5], [-36, -75], [-26, -73], [-16, -77], [-8, -82.3], [-1, -82.8], [5, -85.5], [10, -91], [14, -98.5], [17.5, -106.5], [23.2, -112.2], [28.3, -117.2], [32.7, -117.2]];
S.route(S.path(route58), { t: wt("sailed", 1.1) - 0.1, dur: 4.6, dash: [16, 12], width: 6, color: RED, head: "ship", ease: "none" });
S.label("CAPE HORN", CH, { t: wt("Horn", 2.98) + 0.2, anchor: "l", size: 46, gap: 30, dy: -34, color: WH });
S.dot(CH, { t: wt("Horn", 2.98) + 0.2, r: 8, color: WH });
S.pin(SD, "SAN DIEGO", { t: wt("join", 5.0), color: RED, anchor: "r", size: 40, gap: 28, ringR: 26 });
S.finish();
