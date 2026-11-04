// BASEMAP: usse
// "In April two thousand four, the Navy picked Florida as the best value." Only Florida stays lit; date APRIL 2004; 'BEST VALUE'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const ST = window.GEO.states, FL = G(28.3, -81.7);
S.camera([[0, 1320, 900, 1.16], [w("Florida"), FL[0] - 120, FL[1] - 80, 1.45], [END, FL[0] - 140, FL[1] - 90, 1.55]]);
["Mississippi", "Texas", "Georgia", "South Carolina"].forEach((n) => S.poly(ST[n], { t: 0.0, dur: 0.01, fill: 0.4, width: 4.5, dimAt: w("April") + 0.2, dimTo: 0.12 }));
S.poly(ST["Florida"], { t: 0.0, dur: 0.01, fill: 0.4, width: 4.5 });
S.poly(ST["Florida"], { t: w("Florida"), fill: 0.2, width: 9 });
S.date("APRIL 2004", w("April"));
S.label("FLORIDA", FL, { t: w("Florida"), anchor: "c", size: 52 });
S.tag("BEST VALUE", FL, { t: w("best"), anchor: "b", gap: 50, size: 46, boxColor: "rgba(150,110,20,.95)" });
S.finish();
