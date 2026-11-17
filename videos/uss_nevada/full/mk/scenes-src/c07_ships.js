// BASEMAP: oahu_sw
// Target pin NEVADA; cruisers ASTORIA and PASADENA appear on their names, IOWA later; gun flashes.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const WR = P("WRECK");
S.camera([[0, 1250, 900, 1.5], [END, 1230, 905, 1.55]]);
S.pin(WR, "NEVADA · TARGET", { t: 0.2, color: "#D9572B", anchor: "l", size: 44, gap: 40, dy: 60, ringR: 40 });
const AS = S.off(WR, 30000, 12000), PA = S.off(WR, 27000, -14000), IO = S.off(WR, -30000, 22000);
const ship = (kind, pt, nm, t, len, rot, anchor) => { S.ship(kind, pt, { t, len, rot, fill: "#b3cadf", stroke: "#0c1218", sw: 2.2 }); S.label(nm, pt, { t, anchor, size: 42, gap: 60, dy: -10 }); };
ship("cru", AS, "ASTORIA", wt("Astoria", 2.0), 70, 215, "r");
ship("cru", PA, "PASADENA", wt("Pasadena", 3.0), 70, 150, "r");
S.route([AS, WR], { t: wt("fire", 4.0), dur: 0.5, ease: "none", color: "#f3eee2", width: 4, dash: [10, 8] });
S.route([PA, WR], { t: wt("fire", 4.0) + 0.2, dur: 0.5, ease: "none", color: "#f3eee2", width: 4, dash: [10, 8] });
S.flashAt(WR, wt("fire", 4.0) + 0.6, { r: 40 }); S.flashAt(S.off(WR, 300, 200), wt("fire", 4.0) + 0.9, { r: 36 });
ship("bb", IO, "IOWA", wt("Iowa", END - 1.4), 90, 300, "r");
S.finish();
