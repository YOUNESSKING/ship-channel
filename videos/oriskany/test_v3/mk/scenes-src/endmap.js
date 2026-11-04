// END MAP v3 (scene t=0 = narration 49.30 s, "same coast"): both reefs off the Florida Panhandle, "the same reason". <= 6 s.
// Coordinates: Oriskany FWC 30°02.555'N 87°00.397'W; SS United States Okaloosa County 30°07.148'N 86°46.755'W (fact-check C).
const B = Battle(); const END = B.T.duration;
const K = FXK(B); const GG = GGK(B); const G = GG.proj(11, 134219, 215127);   // assets/pan_close.json
const GOLD = "#e3c27a", TEAL = "#7fd3d8";
const REEF = G(30.04258, -87.00662), SSUS = G(30.11913, -86.77925), DESTIN = G(30.393, -86.496), PENS = G(30.42, -87.22);
const t = (abs) => abs - 49.30;   // narration seconds -> scene seconds
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.14 }); LV.scaleBar(66.0); LV.north();
const MID = [(REEF[0] + SSUS[0]) / 2, (REEF[1] + SSUS[1]) / 2];
// one continuous pull-back: close on the pair -> wide coast (never a held frame)
B.camera([[0, MID[0] + 20, MID[1] - 60, 1.45], [t(50.5), MID[0] + 40, MID[1] - 150, 1.18], [END, MID[0] + 40, MID[1] - 210, 1.02]]);
GG.pin(`<img src="assets/media/carrier_top.png" style="width:150px;display:block;filter:brightness(1.9) drop-shadow(0 0 12px rgba(227,194,122,.9))">`, REEF[0], REEF[1] - 34, { t: 0.0, pop: true });
K.target(...REEF, 0.05, { r: 40, side: GOLD, until: END + 1 });
GG.tagbox("USS ORISKANY · SUNK 2006", REEF[0], REEF[1] + 40, "rgba(10,24,38,.88)", { size: 26, t: 0.15, anchor: [-50, 0] });
GG.pin(`<img src="assets/media/liner_top.png" style="width:170px;display:block;filter:drop-shadow(0 0 10px rgba(127,211,216,.8))">`, SSUS[0], SSUS[1] - 34, { t: 0.25, pop: true });
K.target(...SSUS, 0.3, { r: 40, side: TEAL, until: END + 1 });
GG.tagbox("SS UNITED STATES · SCHEDULED NOV 12, 2026", SSUS[0], SSUS[1] - 110, "rgba(10,24,38,.9)", { size: 24, t: 0.45, anchor: [-50, 0] });
{ const d = document.getElementById("date"); if (d) d.style.display = "none"; }   // one font family (Oswald): no typewriter date scroll
B.line([REEF, [REEF[0] + 160, REEF[1] - 30], SSUS], { dash: true, width: 4, t: 0.3, dur: 0.8 });
GG.lbl("13 NAUTICAL MILES APART", MID[0] - 150, MID[1] - 40, { size: 22, t: 1.0, color: "rgba(243,238,226,.85)" });
B.city("PENSACOLA", ...PENS, { size: 34, t: 0.2 });
B.city("DESTIN", ...DESTIN, { size: 34, t: 0.35 });
GG.lbl("FLORIDA PANHANDLE", ...G(30.62, -86.95), { size: 52, t: t(49.58), color: "rgba(243,238,226,.8)" });
GG.stamp("THE SAME REASON", t(51.32), END + 1, { color: GOLD, size: 64, rot: -3, top: 300 });
B.finish();
