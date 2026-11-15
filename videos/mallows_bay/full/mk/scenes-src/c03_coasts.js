// BASEMAP: usa
// 'On the Pacific coast, on the Gulf coast and along the Atlantic.' coast labels on their words.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

S.camera([[0, 1440, 820, 0.78], [END, 1440, 820, 0.8]]);
const Y = [[46.97,-123.8],[45.6,-122.7],[46.2,-123.8],[47.6,-122.3],[43.4,-124.2],[47.25,-122.4],[37.8,-122.3],[30.1,-93.7],[30.7,-88.0],[29.9,-90.1],[30.4,-89.1],[31.2,-81.5],[32.1,-81.1],[30.3,-81.6],[29.7,-95.0],[30.35,-90.1],[43.85,-70.1],[44.1,-69.1],[34.2,-77.9],[36.8,-76.3],[39.9,-75.1],[40.7,-74.1],[38.3,-76.4],[44.4,-68.9]];
Y.forEach((p) => S.dot(G(p[0], p[1]), { t: 0.0, r: 9 }));
S.tag("PACIFIC COAST", G(42, -129), { t: wt("Pacific", 0.3), anchor: "c" });
S.tag("GULF COAST", G(26.5, -90), { t: wt("Gulf", 1.6), anchor: "c" });
S.tag("ATLANTIC COAST", G(37, -68), { t: wt("Atlantic", 3.0), anchor: "c" });
S.finish();
