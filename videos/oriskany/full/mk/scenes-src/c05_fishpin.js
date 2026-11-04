// BASEMAP: gulf_pan
// "And Florida had to keep checking it." Wreck pin off Pensacola; a fish icon on the pin, then a gold '?' on 'checking'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF"), PENS = S.P("PENS");
S.clouds(4, 0.14);
S.camera([[0, REEF[0] + 30, REEF[1] - 90, 1.7], [END, REEF[0] + 10, REEF[1] - 60, 2.1]]);
S.pin(PENS, "PENSACOLA", { t: 0.0, rings: false, anchor: "l" });
S.pin(REEF, null, { t: 0.0 });
S.icon("fish", [REEF[0] - 18, REEF[1] - 30], { t: w("Florida"), size: 58, bob: 6 });
S.icon("q", [REEF[0] + 24, REEF[1] - 34], { t: w("checking"), size: 70, bob: 5 });
S.finish();
