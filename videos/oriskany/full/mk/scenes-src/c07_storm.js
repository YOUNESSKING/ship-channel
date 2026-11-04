// BASEMAP: gulf_pan
// "The storms saw to that." Wreck pin; a generic storm swirl passes over it (no name, no date).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF");
S.camera([[0, REEF[0] + 20, REEF[1] - 60, 1.4], [END, REEF[0], REEF[1] - 40, 1.6]]);
S.pin(REEF, null, { t: 0.0 });
S.storm([REEF[0] + 520, REEF[1] + 200], [REEF[0] - 380, REEF[1] - 120], { t: 0.0, dur: END, size: 760 });
S.label("STORMS", REEF, { t: w("storms"), anchor: "t", gap: 90, size: 52 });
S.finish();
