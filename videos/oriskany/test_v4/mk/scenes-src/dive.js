// v4 HOOK MAP (scene t = narration t): "Right now, two hundred and twelve feet under the Gulf of Mexico," -> cut to the blast at 4.30.
// Frame 0 = clean map (nothing on it). Labels appear on their words: "Gulf" 3.05, "Mexico" 3.49. No unspoken text.
const B = Battle(); const END = B.T.duration;
const K = FXK(B); const GG = GGK(B); const G = GG.proj(9, 32511, 53288);   // assets/gulf_pan.json
const GOLD = "#e3c27a";
const REEF = G(30.04258, -87.00662);   // FWC 30°02.555'N 87°00.397'W
document.getElementById("date").style.display = "none"; const LV = LivingK(B); LV.clouds({ n: 5, opacity: 0.16 });
// continuous dive: wide Gulf -> the wreck pin (never a held frame); "right now" (0.68) the pin pulses
B.camera([[0, 1500, 780, 0.74], [0.3, 1500, 780, 0.78], [2.4, REEF[0], REEF[1] - 30, 2.6], [END, REEF[0], REEF[1] - 20, 3.6]]);
K.target(...REEF, 0.68, { r: 30, side: GOLD, until: END + 1 });
GG.pin(`<div style="width:20px;height:20px;border-radius:50%;background:${GOLD};box-shadow:0 0 22px ${GOLD}"></div>`, ...REEF, { t: 0.68, pop: true });
GG.lbl("GULF OF MEXICO", REEF[0] - 20, REEF[1] + 58, { size: 15, t: 3.05, color: "rgba(243,238,226,.9)" });
B.finish();
