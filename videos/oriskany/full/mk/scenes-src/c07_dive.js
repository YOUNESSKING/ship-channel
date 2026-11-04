// BASEMAP: gulf_pan
// "To answer that, go back down to the wreck." Like the hook dive, slower, from the east: wide Gulf -> the Oriskany pin.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = G(30.04258, -87.00662);   // FWC 30°02.555'N 87°00.397'W
S.clouds(5, 0.16);
S.camera([[0, 2150, 800, 0.72], [w("go"), 1800, 820, 1.1], [END, REEF[0] + 10, REEF[1] - 20, 2.8]]);
S.dot(REEF, { t: w("wreck") - 0.1, r: 12 }); S.ring(REEF, { t: w("wreck") - 0.1, r: 36 });
S.tag("USS ORISKANY", REEF, { t: w("wreck"), anchor: "b", gap: 40 });
S.finish();
