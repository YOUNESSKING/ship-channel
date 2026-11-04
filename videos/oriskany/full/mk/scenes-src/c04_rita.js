// BASEMAP: gulf7
// "She rode out Hurricane Rita at Beaumont." Rita track (Sept 2005, approx. NHC best track) to the Texas-Louisiana line; pin BEAUMONT.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const BEAU = S.P("BEAU");
const RT = S.path([[24.3, -84.6], [24.6, -86.8], [25.2, -88.6], [26.0, -90.3], [27.0, -91.9], [28.2, -93.0], [29.7, -93.7], [30.9, -94.1]]);
S.camera([[0, 1300, 820, 0.95], [END, BEAU[0] + 120, BEAU[1] + 120, 1.35]]);
const h = S.hurricane(RT, { t: 0.0, dur: END - 0.2, size: 110 });
S.tag("RITA · 2005", RT[4], { t: w("Rita"), anchor: "r", gap: 70, boxColor: "rgba(120,30,30,.92)" });
S.pin(BEAU, "BEAUMONT", { t: w("Beaumont") - 0.1, anchor: "l" });
S.finish();
