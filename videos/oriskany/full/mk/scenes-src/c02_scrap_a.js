// BASEMAP: pnw
// "So the Navy tried the scrapyard." Back at the Bremerton pin; tag 'FOR SCRAP' on 'scrapyard'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const BR = S.P("BREM");
S.clouds(5, 0.14);
S.camera([[0, BR[0] - 150, BR[1] + 30, 1.45], [END, BR[0] - 110, BR[1] + 20, 1.75]]);
S.pin(BR, "BREMERTON", { t: 0.0, anchor: "l" });
S.tag("FOR SCRAP", BR, { t: w("scrapyard"), anchor: "b", gap: 46, size: 46, boxColor: "rgba(110,30,30,.92)" });
S.finish();
