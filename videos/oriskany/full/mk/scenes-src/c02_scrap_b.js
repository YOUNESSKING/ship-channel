// BASEMAP: pnw
// "She never even left Navy custody." Same Bremerton pin, closer; tag 'STILL NAVY PROPERTY' on 'custody'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const BR = S.P("BREM");
S.clouds(5, 0.14);
S.camera([[0, BR[0] - 90, BR[1] + 20, 1.9], [END, BR[0] - 70, BR[1] + 15, 2.25]]);
S.pin(BR, "BREMERTON", { t: 0.0, anchor: "l" });
S.icon("q", [BR[0] + 26 / 1.9, BR[1] - 26 / 1.9], { t: w("left"), size: 60 , until: w("custody") });
S.tag("STILL NAVY PROPERTY", BR, { t: w("custody"), anchor: "b", gap: 46, size: 44 });
S.finish();
