// BASEMAP: gulf_pan
// "And tagging suggested the snapper tend to stay on the wreck." A tagged fish circles the wreck pin.
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF");
S.camera([[0, REEF[0], REEF[1] - 10, 2.3], [END, REEF[0], REEF[1] - 5, 2.7]]);
S.pin(REEF, null, { t: 0.0, r: 10 });
const R = 26, orb = []; for (let i = 0; i <= 96; i++) { const a = (i / 48) * Math.PI * 2; orb.push([REEF[0] + R * Math.cos(a), REEF[1] + R * 0.8 * Math.sin(a)]); }
S.route(orb, { t: w("tagging"), dur: END - w("tagging"), ease: "none", dash: [6, 8], width: 2, color: "rgba(227,194,122,.55)", head: "fish", headSize: 1.1 });
S.icon("tag", [REEF[0] + 30, REEF[1] - 34], { t: w("tagging") + 0.05, size: 48, bob: 4 });
S.label("SNAPPER", REEF, { t: w("snapper"), anchor: "t", gap: 70, size: 46 });
S.tag("STAY ON THE WRECK", REEF, { t: w("stay"), anchor: "b", gap: 70, size: 42 });
S.finish();
