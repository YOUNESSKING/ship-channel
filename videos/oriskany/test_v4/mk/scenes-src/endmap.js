// v4 END MAP (scene t=0 = narration 45.80): "About thirteen nautical miles away." Zoom OUT from the Oriskany pin to the SS United States site.
// Coordinates: Oriskany FWC 30°02.555'N 87°00.397'W; SS United States Okaloosa County 30°07.148'N 86°46.755'W (fact-check C: 12.68 nmi).
const B = Battle(); const END = B.T.duration;
const K = FXK(B); const GG = GGK(B); const G = GG.proj(11, 134219, 215127);   // assets/pan_close.json
const GOLD = "#e3c27a", TEAL = "#7fd3d8";
const REEF = G(30.04258, -87.00662), SSUS = G(30.11913, -86.77925), PENS = G(30.42, -87.22), DESTIN = G(30.393, -86.496);
const t = (abs) => abs - 45.80;   // narration seconds -> scene seconds
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.14 }); LV.north();
const MID = [(REEF[0] + SSUS[0]) / 2, (REEF[1] + SSUS[1]) / 2];
// start close on Oriskany with Pensacola already in frame, pull back to show both sites (continuous move)
B.camera([[0, 1110, 850, 1.12], [t(47.6), 1300, 835, 1.05], [END, 1430, 830, 1.0]]);   // Pensacola + Oriskany in frame from frame 0, pull back to Destin
GG.pin(`<img src="assets/media/carrier_top.png" style="width:150px;display:block;filter:brightness(1.9) drop-shadow(0 0 12px rgba(227,194,122,.9))">`, REEF[0], REEF[1] - 34, { t: 0.02, pop: false });
K.target(...REEF, 0.02, { r: 40, side: GOLD, until: END + 1 });
GG.tagbox("USS ORISKANY", REEF[0], REEF[1] + 44, "rgba(10,24,38,.9)", { size: 40, t: 0.02, anchor: [-50, 0] });
B.line([REEF, [REEF[0] + 160, REEF[1] - 30], SSUS], { dash: true, width: 5, t: t(46.10), dur: 1.0 });
GG.pin(`<img src="assets/media/liner_top.png" style="width:170px;display:block;filter:drop-shadow(0 0 10px rgba(127,211,216,.8))">`, SSUS[0], SSUS[1] - 34, { t: t(46.9), pop: true });
K.target(...SSUS, t(46.95), { r: 40, side: TEAL, until: END + 1 });
GG.tagbox("SS UNITED STATES · NOV 12", SSUS[0], SSUS[1] - 118, "rgba(10,24,38,.92)", { size: 40, t: t(47.1), anchor: [-50, 0] });
GG.lbl("13 NAUTICAL MILES", MID[0] - 150, MID[1] - 40, { size: 40, t: t(46.10), color: "#f3eee2" });   // on "thirteen", along the dashed line
B.city("PENSACOLA", ...PENS, { size: 40, t: 0.02 });
B.city("DESTIN", ...DESTIN, { size: 40, t: t(47.6) });
{ const d = document.getElementById("date"); if (d) d.style.display = "none"; }
B.finish();
