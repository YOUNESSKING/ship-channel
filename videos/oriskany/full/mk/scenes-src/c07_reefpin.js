// BASEMAP: gulf_pan
// "A reef was different." The wreck pin glows gold, small fish icons around it.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF");
S.camera([[0, REEF[0], REEF[1] - 20, 2.0], [END, REEF[0], REEF[1] - 15, 2.35]]);
S.pin(REEF, null, { t: 0.0, r: 14 });
S.ring(REEF, { t: 0.2, r: 70 });
[[-30, -20], [26, -26], [-6, 30], [34, 14], [-40, 16]].forEach((d, i) => S.icon("fish", [REEF[0] + d[0] / 1.4, REEF[1] + d[1] / 1.4], { t: w("reef") + i * 0.12, size: 48, bob: 4 }));
S.tag("REEF", REEF, { t: w("reef"), anchor: "t", gap: 64, size: 46, boxColor: "rgba(120,90,20,.92)" });
S.finish();
