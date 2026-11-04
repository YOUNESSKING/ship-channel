// END MAP (scene t=0 = "And", narration 44.50 s): Oriskany reef -> SS United States site off Destin -> both, "the same reason".
const B = Battle(); const END = B.T.duration;
const K = FXK(B); const GG = GGK(B); const G = GG.proj(11, 134219, 215127);   // assets/pan_close.json
const GOLD = "#e3c27a", TEAL = "#7fd3d8";
const REEF = G(30.0427, -87.0067), SSUS = G(30.13, -86.80), DESTIN = G(30.393, -86.496), PENS = G(30.42, -87.22);
const t = (abs) => abs - 44.50;   // narration seconds -> scene seconds
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.14 }); LV.scaleBar(66.0); LV.north();
const MID = [(REEF[0] + SSUS[0]) / 2, (REEF[1] + SSUS[1]) / 2];
B.camera([[0, REEF[0] + 140, REEF[1] - 90, 1.6], [t(45.48), REEF[0] + 170, REEF[1] - 100, 1.62], [t(46.7), SSUS[0] - 60, SSUS[1] - 70, 1.6],
          [t(49.0), SSUS[0] - 80, SSUS[1] - 90, 1.5], [t(50.4), MID[0] + 40, MID[1] - 190, 1.1], [END, MID[0] + 40, MID[1] - 200, 1.06]]);
// Oriskany already there
GG.pin(`<div style="width:14px;height:14px;border-radius:50%;background:${GOLD};box-shadow:0 0 16px ${GOLD}"></div>`, ...REEF, { t: 0.0 });
K.target(...REEF, 0.05, { r: 40, side: GOLD, until: END + 1 });
GG.tagbox("USS ORISKANY · REEF SINCE 2006", REEF[0], REEF[1] + 40, "rgba(10,24,38,.88)", { size: 26, t: 0.2, anchor: [-50, 0] });
B.city("PENSACOLA", ...PENS, { size: 34, t: 0.3 });
// "this month" -> date chip
B.showDate(t(44.76)); B.date("NOVEMBER 2026", t(44.76));
// "a second" -> dashed line east along the coast
B.line([REEF, [REEF[0] + 300, REEF[1] - 40], SSUS], { dash: true, width: 4, t: t(45.48), dur: 1.1 });
B.city("DESTIN", ...DESTIN, { size: 34, t: t(45.9) });
// "famous American ship" -> liner marker + name
GG.ship(SSUS[0], SSUS[1] - 44, { w: 120, color: "#1c3346", t: t(46.04), pop: true });
K.target(...SSUS, t(46.2), { r: 40, side: TEAL, until: END + 1 });
GG.tagbox("SS UNITED STATES", SSUS[0], SSUS[1] + 40, "rgba(10,24,38,.9)", { size: 30, t: t(46.5), anchor: [-50, 0] });
// "scheduled"
GG.tagbox("SCHEDULED · NOV 2026 · APPROX. SITE", SSUS[0], SSUS[1] + 92, "#8a6a2c", { size: 20, t: t(47.72), anchor: [-50, 0] });
// "same coast" -> coast name
GG.lbl("FLORIDA PANHANDLE", ...G(30.62, -86.95), { size: 52, t: t(49.4), color: "rgba(243,238,226,.8)" });
// "reason" -> stamp
GG.stamp("THE SAME REASON", t(51.32), END + 1, { color: GOLD, size: 64, rot: -3, top: 300 });
B.finish();
