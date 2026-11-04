// BASEMAP: sfbay
// "Pegasus planned to break her up at the old Mare Island yard." Zoom into the bay; pin 'MARE ISLAND, VALLEJO' on 'Mare Island'.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const MI = S.P("MARE"), GGt = S.P("GG");
S.clouds(5, 0.12);
S.camera([[0, GGt[0] + 120, GGt[1] - 60, 0.95], [END, MI[0] - 40, MI[1] + 60, 1.8]]);
S.label("SAN FRANCISCO BAY", G(37.72, -122.27), { t: 0.12, anchor: "c", size: 46 });
S.pin(MI, "MARE ISLAND, VALLEJO", { t: w("Mare"), anchor: "r" });
S.tag("SCRAP YARD", MI, { t: w("break"), anchor: "b", gap: 50, size: 42, boxColor: "rgba(110,30,30,.92)" });
S.finish();
