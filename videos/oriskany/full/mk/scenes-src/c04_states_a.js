// BASEMAP: usse
// "Four bids came in, from five states." Gulf + South-East states outlined; '4 BIDS' on 'Four', '5 STATES' on 'five states'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const ST = window.GEO.states, five = ["Florida", "Mississippi", "Texas", "Georgia", "South Carolina"];
S.camera([[0, 1330, 930, 1.0], [END, 1300, 920, 1.08]]);
S.tag("4 BIDS", G(26.6, -89.6), { t: w("Four"), anchor: "l", gap: 12, size: 48 });
five.forEach((n, i) => S.poly(ST[n], { t: w("five") + i * 0.08, fill: 0.08, width: 3 }));
S.tag("5 STATES", G(26.6, -89.6), { t: w("five"), anchor: "r", gap: 12, size: 48, boxColor: "rgba(150,110,20,.95)" });
S.finish();
