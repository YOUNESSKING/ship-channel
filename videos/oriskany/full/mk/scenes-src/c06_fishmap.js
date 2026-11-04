// BASEMAP: gulf_pan
// "There was a condition. Florida had to keep catching fish on the wreck and testing them." Fish icons on the wreck pin; 'TEST' tag on 'testing'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF"), PENS = S.P("PENS");
S.clouds(5, 0.14);
S.camera([[0, REEF[0] - 40, REEF[1] - 120, 1.45], [END, REEF[0] + 10, REEF[1] - 50, 2.05]]);
S.pin(PENS, "PENSACOLA", { t: 0.0, rings: false, anchor: "l" });
S.pin(REEF, null, { t: 0.0 });
S.tag("USS ORISKANY", REEF, { t: 0.1, anchor: "b", gap: 44 });
S.tag("CONDITION", REEF, { t: w("condition"), anchor: "t", gap: 60, boxColor: "rgba(120,80,10,.9)", until: w("Florida") + 0.3 });
[[-34, -28], [30, -36], [-4, -58], [44, -6], [-48, 4]].forEach((d, i) => S.icon("fish", [REEF[0] + d[0] / 1.2, REEF[1] + d[1] / 1.2], { t: w("catching") + i * 0.18, size: 54, bob: 5 }));
S.tag("TEST", REEF, { t: w("testing"), anchor: "t", gap: 70, boxColor: "rgba(160,110,20,.95)" });
S.finish();
