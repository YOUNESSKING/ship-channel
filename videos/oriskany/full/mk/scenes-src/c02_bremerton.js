// BASEMAP: pnw
// "In September nineteen seventy six, the Navy decommissioned her." Pacific Northwest -> Puget Sound; pin BREMERTON (FACTCHECK_A D1: 30 Sep 1976, laid up at Bremerton).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const BR = S.P("BREM");
S.clouds(6, 0.16);
S.camera([[0, 1440, 810, 0.70], [1.6, BR[0] - 200, BR[1] + 40, 1.3], [END, BR[0] - 120, BR[1] + 20, 1.7]]);
S.pin(BR, "BREMERTON, WASHINGTON", { t: 0.15, anchor: "l" });
S.date("SEPT 1976", w("September"));
S.tag("DECOMMISSIONED", BR, { t: w("decommissioned"), anchor: "b", gap: 46, size: 44, boxColor: "rgba(110,30,30,.92)" });
S.finish();
