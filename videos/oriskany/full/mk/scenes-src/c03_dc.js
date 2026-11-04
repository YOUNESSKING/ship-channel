// BASEMAP: usse
// "Then, in two thousand three, Congress changed the rules." Washington, D.C. pin; date 2003; 'CONGRESS' tag on 'Congress'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const DC = S.P("DC");
S.clouds(5, 0.12);
S.camera([[0, DC[0] - 200, DC[1] + 120, 1.3], [END, DC[0] - 60, DC[1] + 40, 1.7]]);
S.pin(DC, "WASHINGTON, D.C.", { t: 0.05, anchor: "l" });
S.date("2003", w("two"));
S.tag("CONGRESS", DC, { t: w("Congress"), anchor: "b", gap: 50, size: 46 });
S.finish();
