// BASEMAP: westcoast
// "In nineteen ninety six, she was towed down from Bremerton to San Francisco Bay." (FACTCHECK_A D6c)
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const BR = S.P("BREM"), SF = S.P("SF");
const R = S.path([[47.565, -122.627], [48.0, -122.55], [48.2, -123.2], [48.35, -124.4], [48.2, -125.0], [46.5, -124.7], [44.0, -124.75], [41.5, -124.75], [39.5, -124.1], [38.2, -123.3], [37.81, -122.52], [37.8, -122.38]]);
S.clouds(6, 0.14);
S.camera([[0, BR[0] - 120, BR[1] + 100, 1.25], [w("towed"), BR[0] - 160, BR[1] + 300, 1.0], [END, SF[0] - 100, SF[1] - 200, 1.0]]);
S.pin(BR, null, { t: 0.05, rings: false });
S.date("1996", w("nineteen"));
S.label("BREMERTON", BR, { t: w("Bremerton"), anchor: "r" });
S.route(R, { t: w("towed"), dur: w("Bay") - w("towed") + 0.3, dash: [16, 10], head: "ship", headSize: 1.2 });
S.pin(SF, "SAN FRANCISCO BAY", { t: w("San"), anchor: "r" });
S.finish();
