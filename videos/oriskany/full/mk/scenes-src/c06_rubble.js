// BASEMAP: gulf_pan
// "That reef was eight miles away." FACTCHECK_B: control rubble reef 8 miles from the wreck (exact position not published:
// shown as a dashed 8-mile ring with the reef marked on it, direction illustrative).
const S = ShipK(), B = S.B, G = S.G, w = S.w, END = S.END;
const REEF = S.P("REEF"), MPP = S.B.T.map.meters_per_px, R = 8 * 1609.34 / MPP;
const RUB = [REEF[0] - R * 0.8, REEF[1] - R * 0.6];
S.camera([[0, REEF[0] - 20, REEF[1] - 30, 2.0], [END, REEF[0] - 40, REEF[1] - 40, 2.25]]);
S.pin(REEF, "USS ORISKANY", { t: 0.0, anchor: "b", box: true, gap: 34 });
const ring = []; for (let i = 0; i <= 64; i++) { const a = (i / 64) * Math.PI * 2 + Math.PI * 1.2; ring.push([REEF[0] + R * Math.cos(a), REEF[1] + R * Math.sin(a)]); }
S.route(ring, { t: w("eight") - 0.2, dur: 1.2, dash: [10, 10], width: 3, color: "rgba(243,238,226,.75)" });
S.pin(RUB, "RUBBLE REEF", { t: w("reef") - 0.05, color: "#9fc6cf", anchor: "t", box: true, gap: 34 });
S.route([REEF, RUB], { t: w("eight") - 0.15, dur: 0.7, dash: [14, 10], width: 5 });
S.tag("8 MI", [(REEF[0] + RUB[0]) / 2, (REEF[1] + RUB[1]) / 2], { t: w("eight"), anchor: "r", gap: 30, size: 44 });
S.finish();
