// M3B (m3-4 .. m3-8), Benedict Arnold #17: 7 OCTOBER 1777 at Saratoga (Bemis Heights). Map agent ar3_.
// Built with: python3 tools/ar3_inline.py m3b m3-4 m3-8     (world = saratoga map px, z15; `hudson` z10 behind it for the retreat)
// Look: v11 + 2c: close-ups = option 2 (two glowing fronts, no ground tint); words leave after ~3.5 s; flags 13-star US vs Union Flag 1606.
// m3-4: 7 OCT; the British reconnaissance (~1,500, guns) moves out into the wheat field; Americans hit both ends; Morgan on the British right;
//   Fraser rides the line, shot (MORTALLY WOUNDED); the British fall back into two redoubts.
// m3-5: Arnold on the field; ACCOUNTS DIFFER (spoken alternatives only); regiments gather, hit the Light Infantry redoubt; IT HELD.
// m3-6: close on the gap: two log cabins + Canadians; Breymann's redoubt, open at the back; the ride between the two firing lines
//   ("by several accounts"); the cabins cleared; Arnold's small group round the open side.
// m3-7: the wound (leg) + horse down; the redoubt blue; Breymann dead; Gates's report (verbatim quote card); the camp open from the side.
// m3-8: casualty card 7 OCT (British over 630 / Americans about 150); night; zoom out (hudson) north to SARATOGA; the ring; 17 OCT;
//   SURRENDERED ~6,000; FRANCE (alliance); method card (line 3 on the closing words).
// Facts: FACT_NOTES + FACTCHECK_C (NPS numbers, Wilkinson's cabins + ride, Gates 12 Oct report). Fraser's shooter not named.
// @@KIT
const P4 = "m3-4", P5 = "m3-5", P6 = "m3-6", P7 = "m3-7", P8 = "m3-8";
const T_7 = at(P4, "the seventh of October"), T_BURG = at(P4, "Burgoyne tried"), T_OUT = at(P4, "sent his men out"),
  T_WHEAT = at(P4, "wheat field"), T_PROBE = at(P4, "probe the American left"), T_BOTH = at(P4, "hit both ends"),
  T_BRR = at(P4, "On the British right"), T_MORG = at(P4, "Morgan's riflemen"), T_FRAS = at(P4, "Simon Fraser"), T_HOLD = at(P4, "hold the line together"),
  T_SHOT = at(P4, "was shot"), T_MORT = at(P4, "mortally wounded"), T_FELL = at(P4, "fell back"), T_FORTS = at(P4, "two big log forts"), T_REDS = at(P4, "their redoubts");
const T_ARN = at(P5, "Arnold was"), T_MID = at(P5, "middle of it"), T_ACC = at(P5, "Accounts differ"), T_LET = at(P5, "Gates let him go"),
  T_WENT = at(P5, "simply went"), T_CHARGE = at(P5, "took charge"), T_THREW = at(P5, "threw them"), T_LI = at(P5, "British light infantry"),
  T_HELD = at(P5, "It held"), T_WEAK = at(P5, "a weak point");
const T_GAP = at(P6, "was a gap"), T_CAN = at(P6, "Canadian troops"), T_CAB = at(P6, "two log cabins"), T_SEC = at(P6, "second redoubt"),
  T_BREY = at(P6, "Colonel Breymann"), T_BACK = at(P6, "open at the back"), T_SEV = at(P6, "By several accounts"), T_GAL = at(P6, "galloped"),
  T_LINES = at(P6, "two firing lines"), T_CLEAR = at(P6, "cleared the cabins"), T_IN = at(P6, "Arnold went in"), T_SIDE = at(P6, "open side");
const T_BALL = at(P7, "A ball broke"), T_SAME = at(P7, "the same leg"), T_QUE = at(P7, "Quebec"), T_HORSE = at(P7, "horse was killed"),
  T_TAKEN = at(P7, "redoubt was taken"), T_DEAD = at(P7, "Breymann was dead"), T_DEADW = at(P7, "dead."), T_GATES = at(P7, "Gates himself"), T_Q = at(P7, "the Gallant"),
  T_QEND = at(P7, "Breast Work"), T_GONE = at(P7, "redoubt gone"), T_CAMP = at(P7, "whole British camp"), T_OPEN = at(P7, "open from the side");
const T_L7 = at(P8, "On the seventh"), T_630 = at(P8, "six hundred and thirty"), T_150 = at(P8, "hundred and fifty"), T_NIGHT = at(P8, "That night"),
  T_BUR8 = at(P8, "Burgoyne abandoned"), T_SARA = at(P8, "to Saratoga"), T_CLOSE = at(P8, "closed in"), T_17 = at(P8, "seventeenth of October"),
  T_SURR = at(P8, "surrendered"), T_6000 = at(P8, "six thousand"), T_FR = at(P8, "France"), T_HOSP = at(P8, "Arnold spent"),
  T_DOOR = at(P8, "He had found"), T_THRU = at(P8, "gone through it himself"), T_ALLI = at(P8, "an alliance"),
  T_THIRD = at(P8, "That was the third part"), T_LEAD = at(P8, "lead from the front");
// =====================================================================================================================
// THE WORLD: saratoga relief (feathered) over the hudson map (for the retreat north)
// =====================================================================================================================
const HUD = mapGroup("hudson", 4);
const SAR = baseGroup(3); FADES.push([SAR, 0.3, 0.8]);
hudRiver();
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); const NA = LV.north(); NA.style.top = "330px";
// ---------- places (saratoga px) ----------
const BRY = [1338, 542], LIR = [1417, 651], GAP = [1380, 600], WF = [1205, 955], SARV = LD(43.10, -73.588);
const AMLINE = [[1300, 1185], [1420, 1195], [1560, 1215], [1700, 1250], [1830, 1290]];
const CAMPL = [[1440, 655], [1560, 668], [1700, 660], [1850, 640], [2000, 610], [2150, 560]];
// camera keys
const C1 = [1330, 930], S1 = 1.45;
camSet([1300, 900], 1.38); CLAMP = true;
camTo(0, 6, C1, S1, "sine.inOut");
// date scroll + flags + legend
B.showDate(T_7 - 0.15); dateSet("7 OCTOBER 1777", T_7, T_NIGHT - 0.05);
const F1 = [flagS(FL.us, "", 1590, 1110, 0.2, T_ARN + 1.0), flagS(FL.gb, "", 1560, 760, 0.2, T_ARN + 1.0)];   // Union Flag clear of the corner badges
const LGD = legend(1.2, null, true);
// the American line on Bemis Heights (earthworks) and the British camp line (both drawn faint, they stay)
const AL = glowPath(AMLINE, "#2c57b7", 5 / S1, 0.1, T_NIGHT, 0, 0.7, { top: false }); gsap.set(AL, { opacity: 0.7 }); tl.set(AL, { opacity: 0.7 }, 0);
const CL = glowPath(CAMPL, "#bc2528", 5 / S1, 0.1, T_NIGHT, 0, 0.7, { top: false }); tl.set(CL, { opacity: 0.7 }, 0);
const AU = [unitS("a1", "carth", [1380, 1170], "infantry", ""), unitS("a2", "carth", [1540, 1195], "infantry", ""), unitS("a3", "carth", [1700, 1230], "infantry", "")];
AU.forEach((id) => gsap.set(B.units[id].el, { autoAlpha: 1 }));
// =====================================================================================================================
// m3-4: the reconnaissance in force, the wheat field, both ends hit, Fraser, back into the redoubts
// =====================================================================================================================
const R = [unitS("r1", "rome", [1310, 760], "infantry", ""), unitS("r2", "rome", [1345, 745], "infantry", ""), unitS("r3", "rome", [1380, 765], "infantry", "")];
R.forEach((id) => gsap.set(B.units[id].el, { autoAlpha: 1 }));
const RG = unitS("rg", "rome", [1350, 790], "artillery", "", { w: 44, h: 29, t: T_OUT - 0.3 });
const LINE = { r1: [1110, 930], r2: [1200, 952], r3: [1292, 975], rg: [1205, 912] };
Object.entries(LINE).forEach(([id, p], k) => go(id, T_OUT - 0.2 + k * 0.12, 3.2, p));
[[[1310, 790], [1200, 880], [1120, 915]], [[1350, 800], [1290, 900], [1280, 955]]].forEach((pts, k) => arw({ pts, side: "rome", t: T_OUT - 0.1 + k * 0.15, dur: 1.4, width: AW(S1, 12), until: T_BOTH }));
// (no ABOUT 1,500 card here: the number is no longer spoken in m3-4; the beat is "sent his men out into a wheat field")
// the wheat field: a pale-gold field outline on the words
const WFP = [[1060, 905], [1170, 880], [1320, 905], [1345, 990], [1240, 1025], [1080, 1005]];
const WFF = GG.polygon ? null : null;
const wf = document.createElementNS(NS, "polygon"); wf.setAttribute("points", WFP.map((q) => q.join(",")).join(" ")); wf.setAttribute("fill", "rgba(232,200,90,0.32)");
wf.setAttribute("stroke", "#e8c85a"); wf.setAttribute("stroke-width", 2.4 / S1); wf.setAttribute("stroke-dasharray", "6 4"); OVL.insertBefore(wf, OVL.firstChild); gsap.set(wf, { opacity: 0 });
tl.to(wf, { opacity: 1, duration: 0.6 }, T_WHEAT - 0.05); tl.to(wf, { opacity: 0.45, duration: 1.0 }, T_WHEAT + 4); tl.to(wf, { opacity: 0, duration: 1 }, T_FORTS);
tagL("WHEAT FIELD", 1035, 1060, T_WHEAT, null, 15);
// "to probe the American left": a dashed red probe toward the west end of the American line, the line's left end glows
arw({ pts: [[1250, 985], [1300, 1060], [1330, 1130]], side: "rome", t: T_PROBE, dur: 0.9, width: AW(S1, 9), dash: "10 8", until: T_BOTH + 0.3 });
K.target(1310, 1185, T_PROBE + 0.3, { r: 30, side: "carth", until: T_BOTH + 0.5 });
// "The Americans hit both ends of the line": Poor on the British left (east), riflemen on the British right (west); volleys where they touch
const AP = unitS("aP", "carth", [1420, 1150], "infantry", "", { t: T_BOTH - 0.5 }), AM = unitS("aM", "carth", [930, 1110], "infantry", "", { t: T_BOTH - 0.4 }),
  AL2 = unitS("aL", "carth", [1210, 1150], "infantry", "", { t: T_BOTH - 0.3 });
go("aP", T_BOTH, 2.4, [1335, 1010]); go("aM", T_BOTH + 0.1, 3.6, [1040, 965]); go("aL", T_BOTH + 0.4, 3.0, [1200, 1030]);
arw({ pts: [[1440, 1140], [1380, 1060], [1320, 1005]], side: "carth", t: T_BOTH - 0.1, dur: 1.1, width: AW(S1, 12), until: T_FELL });
arw({ pts: [[930, 1100], [990, 1010], [1075, 950]], side: "carth", t: T_BOTH + 0.1, dur: 1.1, width: AW(S1, 12), until: T_FELL });
[[T_BOTH + 1.3, [1300, 995], [1330, 1005]], [T_BRR + 0.4, [1080, 945], [1060, 965]], [T_MORG + 1.0, [1090, 935], [1055, 960]], [T_HOLD, [1190, 975], [1225, 990]]]
  .forEach(([t, a, b]) => { volley(a, b, t, 5, 1.0); smokeLine(a, b, t + 0.05, 3, 26); });
// Morgan: badge on his name, his counter takes his name
const MB = pbadge("DANIEL MORGAN", "RIFLEMEN", "morgan", "carth", "tr", "DM", T_MORG + 0.1, T_FRAS - 0.4);
tagL("MORGAN", 975, 1010, T_MORG + 0.15, null, 14);
// Fraser: a red rider marker riding along the line, his badge on his name; shot, MORTALLY WOUNDED
const FB = pbadge("SIMON FRASER", "BRITISH GENERAL", "fraser", "rome", "tr", "SF", T_FRAS, T_FELL + 0.6);
const FM = faceMarker("fraser", "SF", "rome", 1180, 905, T_FRAS + 0.1, T_FELL + 1.2, 50);
pinAlong(FM, [[1180, 905], [1140, 905], [1110, 900]], T_HOLD - 0.3, 1.6, 8);
hitAt(1110, 900, T_SHOT + 0.05, { k: 2.2 }); K.shake(T_SHOT + 0.1, 3, 0.25);
tl.to(FM.firstElementChild, { filter: "grayscale(1) brightness(0.6)", rotation: -25, duration: 0.5 }, T_SHOT + 0.2);
badgeStamp(FB, "MORTALLY WOUNDED", T_MORT, { size: 22 });
pulse(T_MORT + 0.2);
// the British fall back into the two redoubts; the redoubts slam onto the map
camTo(T_FELL - 0.8, 3.0, [1360, 760], 1.6, "sine.inOut");
go("r1", T_FELL, 3.0, [1310, 570]); go("r2", T_FELL + 0.1, 3.0, [1400, 680]); go("r3", T_FELL + 0.2, 3.0, [1450, 690]); go("rg", T_FELL + 0.1, 3.0, [1430, 640]);
[[[1110, 920], [1200, 760], [1310, 590]], [[1260, 955], [1340, 800], [1405, 680]]].forEach((pts, k) => arw({ pts, side: "rome", t: T_FELL + k * 0.15, dur: 1.4, width: AW(1.6, 12), until: T_ARN + 0.5 }));
go("aM", T_FELL + 0.4, 3.0, [1180, 760]); go("aL", T_FELL + 0.5, 3.0, [1290, 800]); go("aP", T_FELL + 0.6, 3.0, [1440, 780]);
const RB = redoubt(...BRY, T_FORTS - 0.05, null, { s: 62, open: "n" }), RL = redoubt(...LIR, T_FORTS + 0.15, null, { s: 62 });
SFX("hit", T_FORTS + 0.2); K.shake(T_FORTS + 0.2, 3, 0.25);
tagL("REDOUBT", BRY[0] - 20, BRY[1] + 58, T_REDS, null, 14); tagL("REDOUBT", LIR[0] + 40, LIR[1] - 8, T_REDS + 0.1, null, 14);
// =====================================================================================================================
// m3-5: Arnold on the field; accounts differ; the regiments he could reach; the Light Infantry redoubt holds
// =====================================================================================================================
const C5 = [1420, 760], S5 = 1.9;
camTo(T_ARN - 0.6, 2.6, C5, S5, "sine.inOut");
const F2 = [flagS(FL.us, "", 1560, 900, T_ARN + 0.4, T_GAP + 0.6), flagS(FL.gb, "", 1650, 600, T_ARN + 0.4, T_GAP + 0.6)];   // on the British side of the camp line, clear of the labels + cards
const AB = pbadge("BENEDICT ARNOLD", "", "arnold", "carth", "bl", "BA", T_ARN + 0.05, T_BALL + 2.5);
const AMK = faceMarker("arnold", "BA", "carth", 1490, 860, T_MID - 0.1, null, 58);
SFX("ref:pop", T_MID);
pinAlong(AMK, [[1490, 860], [1460, 820], [1445, 790]], T_MID, 2.0, 8);
// "Accounts differ": two spoken alternatives, small, one after the other
const ACC = scr(`<div style="padding:12px 30px 14px;background:rgba(18,16,12,0.92);border-top:5px solid #c9b48a;font-family:Oswald;font-weight:700;color:#f7f3ea;text-align:center">
  <div style="font-size:18px;letter-spacing:.32em;color:#c9b48a">ACCOUNTS DIFFER</div>
  <div style="display:flex;gap:26px;margin-top:6px;font-size:34px;letter-spacing:.06em"><span class="o1">GATES LET HIM GO?</span><span style="color:#8a8170">/</span><span class="o2">HE SIMPLY WENT?</span></div></div>`,
  "left:0;right:0;top:240px;display:flex;justify-content:center;", T_ACC - 0.05, T_WENT + 1.6);
gsap.set([ACC.querySelector(".o1"), ACC.querySelector(".o2")], { autoAlpha: 0 });
tl.to(ACC.querySelector(".o1"), { autoAlpha: 1, duration: 0.25 }, T_LET - 0.05); tl.to(ACC.querySelector(".o2"), { autoAlpha: 1, duration: 0.25 }, T_WENT - 0.4);
SFX("ref:pop", T_LET); SFX("ref:pop", T_WENT - 0.35);
// "took charge of whatever regiments he could reach": blue counters gather behind him
go("aP", T_CHARGE - 0.2, 1.6, [1470, 760]); go("aL", T_CHARGE - 0.1, 1.6, [1415, 770]);
const AX = unitS("aX", "carth", [1530, 860], "infantry", "", { t: T_CHARGE }); go("aX", T_CHARGE + 0.1, 1.6, [1505, 790]);
K.target(1450, 790, T_CHARGE + 0.2, { r: 46, side: "carth", until: T_THREW });
// "threw them at the first redoubt": arrows into the Light Infantry redoubt; its fire (visible); the attack recoils, IT HELD
const LIA = [[[1470, 750], [1445, 700], [1425, 665]], [[1415, 765], [1410, 715], [1410, 672]], [[1505, 775], [1475, 715], [1440, 670]]];
LIA.forEach((pts, k) => arw({ pts, side: "carth", t: T_THREW + k * 0.15, dur: 1.0, width: AW(S5, 11), until: T_HELD + 0.4 }));
go("aP", T_THREW + 0.2, 1.6, [1450, 700]); go("aL", T_THREW + 0.3, 1.6, [1405, 700]); go("aX", T_THREW + 0.4, 1.6, [1480, 705]);
pinAlong(AMK, [[1445, 790], [1440, 730]], T_THREW + 0.2, 1.6, 6);
tagL("LIGHT INFANTRY REDOUBT", LIR[0] + 40, LIR[1] - 50, T_LI, null, 14);
[[T_THREW + 1.4, [1395, 668], [1440, 668]], [T_LI - 0.2, [1395, 670], [1440, 672]], [T_HELD - 0.4, [1400, 668], [1438, 670]]].forEach(([t, a, b]) => { volley(a, b, t, 6, 1.1); smokeLine([a[0], a[1] + 8], [b[0], b[1] + 8], t + 0.05, 3, 24); });
K.gun(LIR[0] + 10, LIR[1] + 8, T_LI + 0.6, { dx: 0, dy: 6 });
go("aP", T_HELD, 1.2, [1475, 760]); go("aL", T_HELD + 0.05, 1.2, [1410, 765]); go("aX", T_HELD + 0.1, 1.2, [1515, 770]);
pinAlong(AMK, [[1440, 730], [1450, 780]], T_HELD, 1.0, 4);
const HELD = wstampL("IT HELD", LIR[0] + 10, LIR[1] + 70, T_HELD + 0.05, null, "#e3232f", 26);
// "So he looked for a weak point": the camera eases west along the British line toward the gap
camTo(T_WEAK - 0.4, 2.4, [1395, 640], 2.25, "sine.inOut");
glowPath([[1430, 655], [1400, 625], [1375, 600], [1350, 570]], "#ffd54a", 4 / 2.25, T_WEAK, T_GAP + 1.5, 2, 0.8, { draw: 0.9, top: true, dash: "6 6" });
SFX("ref:pop", T_WEAK + 0.1);
// =====================================================================================================================
// m3-6: the gap, the two cabins, Breymann's open redoubt, the ride between the lines, round the open side
// =====================================================================================================================
const C6 = [1385, 620], S6 = 2.6;
camTo(T_GAP - 0.5, 2.0, C6, S6, "sine.inOut");
const F3 = [flagS(FL.us, "", 1540, 720, T_GAP + 0.3, T_NIGHT + 0.6), flagS(FL.gb, "", 1270, 470, T_GAP + 0.3, T_CAMP - 0.3)];
// option 2 front: the British line (redoubt - gap - redoubt) facing the Americans to the south
const FR6 = front2([[1290, 585], [1330, 568], [1365, 600], [1395, 618], [1440, 668], [1490, 690]], S6, T_GAP - 0.2, { dur: 1.2, until: T_TAKEN });
K.target(...GAP, T_GAP + 0.1, { r: 26, side: "#ffd54a", until: T_CAN });
const CAN = unitS("rC", "rome", [1378, 612], "infantry", "CANADIANS", { t: T_CAN, tag: 15 });
const CB = [cabin(1360, 578, T_CAB - 0.05, T_THRU), cabin(1404, 590, T_CAB + 0.15, T_THRU)];
SFX("ref:pop", T_CAB);
// the second redoubt: the Germans (red), Breymann's badge on his name, the open back glows
const RGm = unitS("rB", "rome", [BRY[0] + 44, BRY[1] + 4], "infantry", "", { t: T_SEC - 0.1 }); B.hideUnits(["r1"], T_SEC - 0.1, 0.3);
K.target(...BRY, T_SEC + 0.1, { r: 34, side: "rome", until: T_BREY });
tagL("BREYMANN", BRY[0] - 120, BRY[1] - 18, T_BREY, null, 15);
const BB = pbadge("BREYMANN", "COLONEL", null, "rome", "tr", "HB", T_BREY + 0.05, T_DEAD + 2.6);
openGlow(RB, T_BACK, T_IN + 1.0);
SFX("ref:pop", T_BACK + 0.1);
// "By several accounts, Arnold galloped straight across the field between the two firing lines": dotted ride, volleys on either side
const sev = tagL("BY SEVERAL ACCOUNTS", 1440, 760, T_SEV, T_GAL + 2.2, 13);
const RIDE = [[1450, 780], [1450, 720], [1430, 690], [1395, 662], [1360, 640], [1325, 625], [1295, 610], [1282, 585]];
pinAlong(AMK, RIDE, T_GAL, T_CLEAR - T_GAL - 0.3, 20);
trail(RIDE, "#9fc0ea", 2.2 / S6, T_GAL, T_CLEAR - T_GAL - 0.3, T_TAKEN, "2 6");
const LA = [[1420, 640], [1375, 615], [1335, 595]], LB = [[1430, 705], [1385, 680], [1340, 655]];   // British line (north) / American line (south) flashes
for (let k = 0; k < 3; k++) { flashW(...LA[k], T_GAL + 0.6 + k * 0.9, 1.1); flashW(...LB[k], T_GAL + 0.95 + k * 0.9, 1.1); }
SFX("mg", T_GAL + 0.6); SFX("mg", T_LINES + 0.3);
// the American infantry closes up behind him
go("aP", T_GAL, 2.5, [1435, 700]); go("aL", T_GAL + 0.1, 2.5, [1395, 660]); go("aX", T_GAL + 0.2, 2.5, [1460, 720]);
// "The Americans cleared the cabins": a blue arrow into the gap, the Canadians go
arw({ pts: [[1405, 680], [1395, 640], [1385, 608]], side: "carth", t: T_CLEAR - 0.1, dur: 0.8, width: AW(S6, 10), until: T_BALL });
go("aL", T_CLEAR, 1.4, [1385, 612]); volley([1370, 615], [1400, 612], T_CLEAR + 0.4, 5, 1.0);
go("rC", T_CLEAR + 0.3, 1.6, [1395, 545]); B.hideUnits(["rC"], T_CLEAR + 1.6, 0.6);
// "Arnold went in with a small group around the open side of the German redoubt"
const SG = unitS("aS", "carth", [1300, 615], "infantry", "", { t: T_IN - 0.2, w: 44, h: 29 });
const ROUND = [[1282, 585], [1300, 545], [1318, 515], [1338, 508], [BRY[0], BRY[1] - 8]];
pinAlong(AMK, ROUND, T_IN, T_BALL - T_IN - 0.2, 12); along("aS", ROUND.map(([x, y]) => [x + 6, y + 14]), T_IN + 0.2, T_BALL - T_IN - 0.3, 12);
arw({ pts: ROUND.slice(0, 4), side: "carth", t: T_SIDE - 0.2, dur: 0.9, width: AW(S6, 9), until: T_TAKEN + 0.4 });
camTo(T_IN - 0.3, 3.0, [1350, 570], 2.9, "sine.inOut");
// =====================================================================================================================
// m3-7: the wound, the horse, the redoubt taken, Breymann dead, Gates's report, the camp open
// =====================================================================================================================
hitAt(BRY[0] + 2, BRY[1] - 16, T_BALL + 0.05, { k: 2.4 }); hitAt(BRY[0] - 10, BRY[1] - 4, T_BALL - 0.15, { k: 1.4, sfx: false });
K.shake(T_BALL + 0.1, 6, 0.35); pulse(T_BALL + 0.15); SFX("hit", T_BALL + 0.1);
tl.to(AMK.firstElementChild, { rotation: 80, y: 12, filter: "brightness(0.75)", duration: 0.35, ease: "power2.in" }, T_BALL + 0.15);
badgeStamp(AB, "WOUNDED", T_BALL + 0.4, { grey: false, size: 24 });
const SAME = wstampL("THE SAME LEG", BRY[0] + 70, BRY[1] + 46, T_SAME, null, "#f7f3ea", 20, "QUEBEC");
const HR = pinS(GG.pin(HORSE(36, "#8a867c"), BRY[0] + 22, BRY[1] - 26, { t: T_HORSE - 0.1, pop: true, until: T_GONE }));
tl.fromTo(HR.firstElementChild, { rotation: 0 }, { rotation: 100, y: 8, duration: 0.45, ease: "power2.in", immediateRender: false }, T_HORSE + 0.1);
SFX("hit", T_HORSE + 0.4);
// the redoubt taken (blue), the Germans grey, Breymann dead
recolor(RB, "carth", T_TAKEN); SFX("ref:pop", T_TAKEN + 0.05);
go("aS", T_TAKEN - 0.2, 0.9, [BRY[0] + 4, BRY[1] + 2]); go("aL", T_TAKEN - 0.1, 1.2, [BRY[0] + 30, BRY[1] + 30]);
go("rB", T_TAKEN, 1.2, [BRY[0] + 50, BRY[1] - 30]); B.grey(["rB"], T_TAKEN + 0.2, 0.8); B.hideUnits(["rB"], T_DEAD + 1.4);
badgeStamp(BB, "DEAD", T_DEADW - 0.1, { size: 30 }); tl.to(BB.querySelectorAll("div[style*='border-radius:50%'] *"), { filter: "grayscale(1) brightness(0.6)", duration: 0.4 }, T_DEADW - 0.1);   // greys on "dead"
// (no Gates quote card here: the main session covers "Gates himself reported ... Breast Work." with an archive insert)
// "With the German redoubt gone, the whole British camp lay open from the side"
camTo(T_GONE - 0.6, 2.8, [1640, 620], 1.55, "sine.inOut");
const CAMPG = glowPath(CAMPL, "#ff6b5e", 7 / 1.55, T_CAMP - 0.1, T_NIGHT + 0.5, 2, 0.9, { draw: 1.0, top: true });
arw({ pts: [[BRY[0] + 30, BRY[1] + 30], [1450, 610], [1600, 640], [1750, 640]], side: "carth", t: T_OPEN - 0.2, dur: 1.2, width: AW(1.55, 12), dash: "12 8", until: T_L7 + 1.0 });
wstampL("OPEN FROM THE SIDE", 1620, 720, T_OPEN + 0.1, null, "#9fc0ea", 26);
const F4 = [flagS(FL.gb, "", 1760, 450, T_CAMP - 0.3, null)]; fadeS(F4, 0.75, 1.1);
// the night zoom-out keeps a Union Flag on screen: one on the retreat road (mid scale), then the one at Saratoga
const FMID = flagS(FL.gb, "", 1300, 300, null, null); gsap.set(FMID, { autoAlpha: 1 });
SCALEFIX.push((sc) => { const v = (1 - ramp(sc, 0.75, 1.0)) * ramp(sc, 0.25, 0.32); FMID.style.filter = `opacity(${v.toFixed(3)})`; });
// =====================================================================================================================
// m3-8: the casualty card; that night north to Saratoga; the ring; 17 OCT surrender; France; the method
// =====================================================================================================================
const T_CAS0 = T_630 - 0.3, T_CAS1 = Math.min(T_150 + 0.9, T_NIGHT - 0.3);   // ~3 s, on the spoken numbers
const CAS = casualties([["", "ABOUT 150", "OVER 630"]], "7 OCTOBER 1777 · MEN LOST", T_CAS0, T_CAS1, 240);
// that night: night wash, the date, zoom out (whoosh) north to Saratoga on the hudson map
nightWash(T_NIGHT - 0.2, T_17 - 0.5, 0.45);
dateSet("NIGHT, 8 OCTOBER", T_NIGHT, T_17 - 0.05, 28);
const BU = pbadge("JOHN BURGOYNE", "", "burgoyne", "rome", "tr", "JB", T_BUR8 + 0.05, T_SURR + 1.4);
const ZC = [(1600 + SARV[0]) / 2, (650 + SARV[1]) / 2 + 150], ZS = 0.24;
CLAMP = false;
SFX("whoosh", T_NIGHT + 0.2);
zoom(T_NIGHT + 0.3, T_SARA - T_NIGHT + 0.3, [1640, 620], 1.55, ZC, ZS, [1600, 650], "power2.inOut");
// the British army marches north up the river road (red counters, night), the camp left behind
const ROAD = [[1700, 640], [2050, 380], [2250, -200], [2380, -900], [2520, -1600], [SARV[0] - 40, SARV[1] + 120]];
const RET = [0, 1, 2].map((k) => unitS("x" + k, "rome", ROAD[0], "infantry", "", { t: T_BUR8 - 0.2 + k * 0.15 }));
RET.forEach((id, k) => along(id, sub(ROAD, 0, 0.96 - k * 0.05, 16), T_BUR8 + k * 0.2, T_CLOSE - T_BUR8 - 0.3, 16));
arw({ pts: sub(ROAD, 0.05, 0.98, 10), side: "rome", t: T_BUR8 + 0.3, dur: 2.0, width: AW(ZS, 12), until: T_17 });
hideU(["a1", "a2", "a3", "aP", "aL", "aX", "aS", "aM", "r1", "r2", "r3", "rg"], T_NIGHT + 0.8);
tl.to([RB, RL, AMK, ...CB], { autoAlpha: 0, duration: 0.5 }, T_NIGHT + 0.8);
const ST = town("SARATOGA", SARV, "r", T_SARA, { until: T_SARA + LBL_LIFE });
const F5 = [flagS(FL.gb, "", SARV[0] - 330, SARV[1] + 150, T_NIGHT + 0.3, null), flagS(FL.us, "", 1500, 900, T_NIGHT + 0.3, T_SARA + 0.6), flagS(FL.us, "", SARV[0] + 1100, SARV[1] + 1100, T_SARA - 0.2, null)]; fadeS(F5[0], 0.3, 0.42, true);
// "The Americans closed in around him": blue counters converge on the village, the ring
const RINGP = [[-1, -1], [1, -1], [1, 1], [-1, 1], [0, 1.4], [-1.4, 0]].map(([dx, dy]) => [SARV[0] + dx * 700, SARV[1] + dy * 500]);
const RING = RINGP.map((p, k) => unitS("u" + k, "carth", [p[0] + (p[0] - SARV[0]) * 0.8, p[1] + (p[1] - SARV[1]) * 0.8], "infantry", "", { t: T_CLOSE - 0.4 + k * 0.08 }));
RING.forEach((id, k) => go(id, T_CLOSE + k * 0.08, 2.6, RINGP[k]));
camTo(T_CLOSE - 0.2, 2.8, [SARV[0], SARV[1] + 80], 0.3, "sine.inOut");
const RGF = front2([...[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map((k) => { const a = k / 12 * 6.2832; return [SARV[0] + Math.cos(a) * 560, SARV[1] + 60 + Math.sin(a) * 420]; })], 0.3, T_CLOSE + 1.0, { dur: 1.6, flip: true });
dateSet("17 OCTOBER 1777", T_17, null);
SFX("tick", T_17 - 0.3); SFX("tick", T_17 - 0.17);
// "he surrendered, about six thousand men": the red grey, a white flag, the number card
B.grey(RET, T_SURR + 0.1, 0.8);
whiteFlag(SARV[0] + 40, SARV[1] - 60, T_SURR + 0.2, null); SFX("ref:pop", T_SURR + 0.25);
// the headline result: ticks fast, then HOLDS ~2.5 s on ABOUT 6,000, high on the screen, clear of the ring and the flags; FRANCE only after it
const SUR = bigNum("SURRENDERED · ABOUT", 6000, "MEN", T_6000 - 0.1, T_ALLI - 0.2, { tick: 0.7, top: 100 });
pulse(T_6000 + 0.1);
// "France signed an alliance": small stamp on the word
const FRA = sstamp("FRANCE", 330, T_ALLI - 0.05, { size: 70, color: "#9fc0ea", sub: "AN ALLIANCE", until: T_HOSP - 0.1, shake: 4 });
// "Arnold spent the winter in a hospital bed": his badge, quietly
const AB2 = pbadge("BENEDICT ARNOLD", "", "arnold", "carth", "bl", "BA", T_HOSP + 0.1, null);
// method card: line 3 lit on the closing words
// method card on "That was the third part of his method": lines 1-2 shown DIM (moves 1 + 2), line 3 lights on "lead from the front"
const MC = GG.method(3, T_THIRD - 0.1, END + 1, [T_THIRD + 0.1, T_THIRD + 0.2, T_LEAD - 0.1]);
MC.querySelectorAll(".row").forEach((r, i) => { r.style.fontSize = "48px"; if (i < 2) r.style.filter = "opacity(0.42) saturate(0.3)"; });
tl.fromTo(MC.querySelectorAll(".row.lit")[2], { scale: 1 }, { scale: 1.06, color: "#8fb2ff", duration: 0.3, yoyo: true, repeat: 1, immediateRender: false }, T_LEAD + 0.4);
SFX("hit", T_LEAD); SFX("ref:boom", T_LEAD + 0.1);
// HUD steps out under the big cards (1c); the date scroll stays
declutter([LGD, MB, FB, AB, BB, BU, AB2], [[T_ACC - 0.05, T_WENT + 1.6], [T_CAS0, T_CAS1], [T_6000 - 0.1, T_HOSP - 0.1], [T_THIRD - 0.1, END + 1]]);
fixImgs();
K.raiseTerritory();
B.finish();
