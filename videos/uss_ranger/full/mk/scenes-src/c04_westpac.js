// BASEMAP: pacific
// arcs from San Diego west to the Western Pacific; WESTERN PACIFIC on 'Western'; 20+ DEPLOYMENTS on 'twenty'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P, G = S.G;
const RED = "#D9572B", WH = "#f3eee2", ST = "#8fb0cc";
const SD = P("SANDIEGO"), JP = G(35.3, 139.7), OK = G(26.3, 127.8), PH = G(14.6, 120.6);
S.camera([[0, 1650, 720, 1.0], [END, 1600, 710, 1.1]]);
S.pin(SD, "SAN DIEGO", { t: 0.1, color: RED, anchor: "l", size: 44, gap: 34, ringR: 30 });
const arcs = [[JP, 0.14], [PH, 0.12], [JP, 0.24], [OK, 0.18], [PH, 0.22]];
arcs.forEach(([to, b], i) => S.route(S.arcPts(SD, to, b), { t: 0.2 + i * 0.35, dur: 1.4, dash: [14, 10], width: 4, color: i % 2 ? WH : RED, head: "dot", headSize: 0.6 }));
S.label("WESTERN PACIFIC", G(24, 130), { t: wt("Western", 0.84), anchor: "c", size: 56, color: ST });
S.tag("20+ DEPLOYMENTS", G(41, -165), { t: wt("twenty", 2.18), anchor: "c", size: 54, boxColor: "rgba(150,40,30,.92)" });
S.finish();
