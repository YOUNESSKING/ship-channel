// v4 (scene t=0 = narration 37.80): "And it matters right now." Gulf of Mexico, the Oriskany wreck pin glowing; slow push (no held frame).
const B = Battle(); const END = B.T.duration;
const K = FXK(B); const GG = GGK(B); const G = GG.proj(9, 32511, 53288);   // assets/gulf_pan.json
const GOLD = "#e3c27a";
const REEF = G(30.04258, -87.00662), PENS = G(30.42, -87.22);
document.getElementById("date").style.display = "none"; const LV = LivingK(B); LV.clouds({ n: 4, opacity: 0.14 });
B.camera([[0, REEF[0] + 60, REEF[1] - 60, 1.55], [END, REEF[0] + 40, REEF[1] - 40, 1.85]]);
K.target(...REEF, 0.0, { r: 34, side: GOLD, until: END + 1 });
GG.pin(`<img src="assets/media/carrier_top.png" style="width:120px;display:block;filter:brightness(1.9) drop-shadow(0 0 14px rgba(227,194,122,.95))">`, REEF[0], REEF[1] - 30, { t: 0.0, pop: true });
B.city("PENSACOLA", ...PENS, { size: 40, t: 0.0 });
B.finish();
