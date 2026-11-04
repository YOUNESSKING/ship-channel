// HOOK MAP (scene t=0 = "Off", narration 2.90 s): Gulf wide, fast eased dive onto the Oriskany reef.
const B = Battle(); const END = B.T.duration;
const K = FXK(B); const GG = GGK(B); const G = GG.proj(9, 32511, 53288);   // assets/gulf_pan.json
const GOLD = "#e3c27a";
const REEF = G(30.0427, -87.0067), PASS = G(30.33, -87.31);
document.getElementById("date").style.display = "none"; const LV = LivingK(B); LV.clouds({ n: 5, opacity: 0.16 });
// "Florida" is spoken at narration 3.75 -> scene 0.85
B.camera([[0, 1500, 780, 0.74], [0.35, 1500, 780, 0.80], [1.55, REEF[0], REEF[1] - 40, 3.2], [END, REEF[0], REEF[1] - 30, 3.45]]);
GG.lbl("GULF OF MEXICO", 1350, 1250, { size: 54, t: 0.05, until: 0.9, color: "rgba(230,240,240,.55)" });
GG.lbl("FLORIDA", ...G(30.55, -86.35), { size: 58, t: 0.75, until: 1.5, color: "#f3eee2" });
B.city("PENSACOLA", ...G(30.42, -87.22), { size: 26, t: 0.95 });
B.line([PASS, REEF], { dash: true, width: 5, t: 1.0, dur: 0.6 });
K.target(...REEF, 1.15, { r: 26, side: GOLD, until: END + 1 });
GG.pin(`<div style="width:16px;height:16px;border-radius:50%;background:${GOLD};box-shadow:0 0 18px ${GOLD}"></div>`, ...REEF, { t: 1.1, pop: true });
GG.tagbox("24 MILES OFF THE COAST", REEF[0] + 12, REEF[1] + 34, "rgba(10,24,38,.88)", { size: 15, t: 1.3, anchor: [-50, 0] });
B.finish();
