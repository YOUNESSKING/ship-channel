// BASEMAP: nyc
// "Her keel was laid in Brooklyn in May nineteen forty four." New York harbour; pin NEW YORK NAVY YARD, BROOKLYN; date MAY 1944.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const NY = S.P("BNY");
S.clouds(5, 0.12);
S.camera([[0, 1440, 900, 0.8], [END, NY[0] - 60, NY[1] + 40, 1.6]]);
S.label("NEW YORK", G(40.79, -73.96), { t: 0.12, anchor: "c", size: 46, until: w("Brooklyn") });
S.pin(NY, "NEW YORK NAVY YARD<br><span style='font-size:40px;color:#e3c27a'>BROOKLYN</span>", { t: w("Brooklyn"), anchor: "r" });
S.date("MAY 1944", w("May"));
S.finish();
