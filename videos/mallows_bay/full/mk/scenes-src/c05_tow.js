// BASEMAP: chesa
// 'The company towed the ships up the Potomac.' tow line James River -> up the bay -> Potomac.
const S = ShipK(), B = S.B, G = S.G, w = S.w, wt = S.wt, END = S.END;

const J = S.P("JAMES"), AL = S.P("ALEX");
const R = S.path([[37.13, -76.65], [37.0, -76.35], [37.4, -76.15], [37.95, -76.25], [38.05, -76.4], [38.2, -76.85], [38.35, -77.05], [38.45, -77.3], [38.6, -77.2], [38.8048, -77.0469]]);
S.camera([[0, 1440, 810, 0.72], [END, AL[0] - 40, AL[1] + 160, 0.95]]);
S.pin(J, "JAMES RIVER", { t: 0.0, anchor: "r", rings: false });
S.route(R, { t: 0.1, dur: END - 0.4, dash: [16, 10], head: "ship", headSize: 1.3, ease: "sine.inOut" });
S.label("POTOMAC", G(38.25, -76.95), { t: wt("Potomac", 1.6), anchor: "c", size: 44, color: "#cfe3ea" });
S.finish();
