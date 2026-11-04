// M1A (m1-1 .. m1-4), Benedict Arnold #17: MOVE 1 · THE MARCH TO QUEBEC · 1775, the march up the Kennebec. Map agent a1_.
// Built with: python3 tools/a1_make_control.py maine northeast && python3 tools/a1_inline.py m1a m1-1 m1-4 maine
// World = the maine map px (z9). `northeast` (z8, 2x) lies ON TOP at its true place for the wide opening (option 1 territory, half strength),
// then dissolves (~2.8 s) during the dive into `maine` (close-ups: no ground tint). A sand underlay fills any corner outside the maps.
// m1-1: title card; two invasion routes: blue arrow up Lake Champlain to MONTREAL (on the words), Arnold's dotted route up the KENNEBEC, over the
//   mountains, down the CHAUDIÈRE to QUEBEC (labels on the words); SEPTEMBER 1775 on "late September"; ABOUT 1,100 MEN; dive onto the
//   Kennebec; bateaux on "bateaux"; THE PLAN ~180 MILES / ~20 DAYS on the spoken words.
// m1-2: pull out west: the British at St. Johns facing the lake, the first American army coming up it; MAINE WOODS; THE BACK DOOR stamp on
//   "back door"; FRONT DOOR on the lake on "front door".
// m1-3: close on the Great Carrying Place + the Dead River: spoiled barrels, the carry (dotted, boats + barrels hauled), 12 MILES; night of
//   21 OCTOBER 1775, storm (rain), trees down, the river swells (8-10 FEET), boats sink, men lost.
// m1-4: three companies at the rear turn back (grey) on "turned back" (ABOUT 450 MEN), with food; the rest go on; Arnold's small party down the
//   Chaudière rapids to SARTIGAN; cattle + flour back up the trail; Dearborn (initials); the hunger card, one line per spoken item.
// Facts: FACT_NOTES MOVE 1 + FACTCHECK_A (1,100; ~200 bateaux; 180 mi / 20 days; 12 mi carry; 21 Oct storm, 8-10 ft; 3 companies ~450;
//   Sartigan; Dearborn's dog; Senter's list). 1775 river courses drawn by hand (no modern reservoirs).
// @@KIT
const P1 = "m1-1", P2 = "m1-2", P3 = "m1-3", P4 = "m1-4";
const T_ONE = at(P1, "One American army"), T_NORTH = at(P1, "go north up"), T_CHAMP = at(P1, "Lake Champlain"), T_MTL = at(P1, "Montreal."),
  T_ARN = at(P1, "Arnold's would"), T_KEN = at(P1, "Kennebec River"), T_MTN = at(P1, "over the mountains"), T_CHAU = at(P1, "the Chaudière River"),
  T_QUE = at(P1, "to Quebec"), T_FORT = at(P1, "fortress city"), T_SEP = at(P1, "late September"), T_1100 = at(P1, "eleven hundred"),
  T_200 = at(P1, "two hundred flat-bottomed"), T_BAT = at(P1, "bateaux"), T_PLAN = at(P1, "The plan said"), T_180 = at(P1, "a hundred and eighty miles"),
  T_20 = at(P1, "twenty days");
const T_BRIT = at(P2, "The British in Canada"), T_LAKE = at(P2, "watching the lake"), T_FIRST = at(P2, "first American army"),
  T_NOB = at(P2, "Nobody expected"), T_WOODS = at(P2, "Maine woods"), T_IDEA = at(P2, "That was the idea"), T_BACK = at(P2, "back door"),
  T_FRONT = at(P2, "the front door"), T_ATT = at(P2, "attention");
const T_KILL = at(P3, "nearly killed them"), T_LEAK = at(P3, "boats leaked"), T_SPOIL = at(P3, "spoiled"), T_GCP = at(P3, "the Great Carrying Place"),
  T_HAUL = at(P3, "haul boats"), T_12 = at(P3, "twelve miles"), T_POND = at(P3, "ponds and bog"), T_NIGHT = at(P3, "the night"),
  T_21 = at(P3, "twenty-first of October"), T_STORM = at(P3, "storm hit"), T_DEAD = at(P3, "Dead River"), T_TREES = at(P3, "Trees came down"),
  T_MORN = at(P3, "by morning"), T_FEET = at(P3, "eight to ten feet"), T_SANK = at(P3, "Boats sank"), T_WASH = at(P3, "washed away"),
  T_LOST = at(P3, "lost their way"), T_FLOOD = at(P3, "flooded woods");
const T_FEW = at(P4, "A few days later"), T_3C = at(P4, "three companies"), T_COUN = at(P4, "a council"), T_TURN = at(P4, "turned back"),
  T_450 = at(P4, "four hundred and fifty"), T_SHARE = at(P4, "more than their share"), T_REST = at(P4, "The rest kept going"),
  T_PUSH = at(P4, "Arnold pushed ahead"), T_RAP = at(P4, "rapids of the"), T_CHA4 = at(P4, "Chaudière to"), T_FARM = at(P4, "first French farms"),
  T_CATTLE = at(P4, "cattle and flour"), T_BEH = at(P4, "Behind him"), T_DEAR = at(P4, "Henry Dearborn"), T_DOG = at(P4, "his dog"),
  T_EATEN = at(P4, "eaten it"), T_SOAP = at(P4, "shaving soap"), T_LIP = at(P4, "lip salve"), T_SHOE = at(P4, "the leather of their shoes"),
  T_CART = at(P4, "cartridge boxes");
// =====================================================================================================================
// THE WORLD: maine relief (base) + northeast on top for the wide opening; rivers of 1775 drawn by hand
// =====================================================================================================================
const NE = mapTop("northeast", "t", 4); const NE_C = terrImg("assets/media/a1_ctl_northeast_1775.png", NE, 0, null, 0.01);
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); const NA = LV.north();
const L = (a, b) => LD(a, b);
// places
const FTW = L(44.31, -69.77), CARRY0 = L(45.17, -70.0), DEAD0 = L(45.19, -70.18), HL = L(45.39, -70.80), MEGS = L(45.45, -70.87), MEGN = L(45.585, -70.885),
  SART = L(46.12, -70.67), STM = L(46.44, -71.03), LEVIS = L(46.80, -71.18), QUE = L(46.812, -71.21), STJ = L(45.30, -73.26), MTL = L(45.50, -73.57),
  CRP = L(44.027, -73.424), VALC = L(44.611, -73.43);
// 1775 rivers (lat/lon, smoothed): the Kennebec, the Dead River (the winding river under today's Flagstaff Lake), the Arnold River, the Chaudière
const KEN = smoothP([[44.05, -69.79], [44.23, -69.77], [44.31, -69.77], [44.45, -69.68], [44.55, -69.63], [44.66, -69.66], [44.765, -69.72], [44.713, -69.79],
  [44.80, -69.88], [44.95, -69.86], [45.05, -69.88], [45.12, -69.95], [45.17, -69.995], [45.23, -69.99], [45.34, -69.97]].map((q) => L(...q)), 2);
const DEADR = smoothP([[45.34, -69.97], [45.30, -70.04], [45.24, -70.10], [45.19, -70.18], [45.16, -70.22], [45.15, -70.26], [45.15, -70.30], [45.17, -70.34],
  [45.19, -70.38], [45.21, -70.42], [45.22, -70.48], [45.25, -70.53], [45.29, -70.58], [45.33, -70.63], [45.36, -70.70], [45.39, -70.77]].map((q) => L(...q)), 3);
const ARNR = smoothP([[45.39, -70.80], [45.41, -70.83], [45.43, -70.85], [45.45, -70.87]].map((q) => L(...q)), 2);
const CHAU = smoothP([[45.585, -70.885], [45.70, -70.85], [45.80, -70.80], [45.92, -70.74], [46.03, -70.70], [46.12, -70.67], [46.21, -70.78], [46.30, -70.87],
  [46.37, -70.92], [46.44, -71.03], [46.52, -71.10], [46.59, -71.21], [46.68, -71.26], [46.74, -71.28]].map((q) => L(...q)), 3);
const MEG = smoothP([[45.585, -70.885], [45.56, -70.872], [45.52, -70.868], [45.48, -70.874], [45.45, -70.87], [45.43, -70.90], [45.47, -70.925], [45.52, -70.935],
  [45.56, -70.92], [45.585, -70.885]].map((q) => L(...q)), 2);
const LAKEP = [CRP, L(44.25, -73.36), VALC, L(44.85, -73.33), L(45.05, -73.32), STJ, L(45.42, -73.27), L(45.48, -73.40), MTL];
[KEN, DEADR, ARNR, CHAU].forEach((p) => river(p, 1.5));
const megL = document.createElementNS(NS, "path"); megL.setAttribute("d", "M" + MEG.map((q) => q.join(" ")).join(" L") + " Z");
megL.setAttribute("fill", "rgb(122,160,190)"); megL.setAttribute("stroke", "rgba(150,128,90,0.6)"); megL.setAttribute("stroke-width", "1.2"); OVL.insertBefore(megL, OVL.firstChild);
LV.shimmer([KEN, DEADR, CHAU], { width: 0.9 });
// Arnold's route: up the Kennebec, the carry, up the Dead River, over the height of land, the lake, down the Chaudière, overland to Point Lévis
const iN = (pts, p) => { let b = 0, bd = 1e9; pts.forEach((q, i) => { const d = Math.hypot(q[0] - p[0], q[1] - p[1]); if (d < bd) { bd = d; b = i; } }); return b; };
const KEN_UP = KEN.slice(0, iN(KEN, CARRY0) + 1), CARRY = [CARRY0, L(45.17, -70.05), L(45.165, -70.09), L(45.175, -70.13), DEAD0];
const DEAD_UP = DEADR.slice(iN(DEADR, DEAD0)), CHAU_DN = CHAU.slice(0, iN(CHAU, STM) + 1);
const ROUTE = [...KEN_UP, ...CARRY.slice(1), ...DEAD_UP.slice(1), ...ARNR.slice(1), L(45.52, -70.90), MEGN, ...CHAU_DN.slice(1), L(46.60, -71.12), L(46.74, -71.17), LEVIS];
const fR = (p) => { let Lt = 0, best = 0, bd = 1e9, acc = 0; for (let j = 1; j < ROUTE.length; j++) Lt += Math.hypot(ROUTE[j][0] - ROUTE[j - 1][0], ROUTE[j][1] - ROUTE[j - 1][1]);
  for (let j = 0; j < ROUTE.length; j++) { if (j) acc += Math.hypot(ROUTE[j][0] - ROUTE[j - 1][0], ROUTE[j][1] - ROUTE[j - 1][1]); const d = Math.hypot(ROUTE[j][0] - p[0], ROUTE[j][1] - p[1]); if (d < bd) { bd = d; best = acc / Lt; } } return best; };
const F_CARRY = fR(CARRY0), F_DEAD = fR(DEAD0), F_HL = fR(HL), F_MEGN = fR(MEGN), F_SART = fR(SART), F_STM = fR(STM);
// =====================================================================================================================
// m1-1: the two invasion routes (northeast on top, option 1 at half strength)
// =====================================================================================================================
const C0 = [1440, 760], S0 = 0.68;
camSet(C0, S0);
camTo(0.2, T_200 - 0.2, [1450, 770], 0.70, "sine.inOut");
const TTL = B.title("MOVE 1", "THE MARCH TO QUEBEC", "1775", 0.25, T_NORTH - 0.1);   // words spoken in hook-4 ("marched ... to Quebec") SFX("ref:boom", 0.35);
// both flags on their own land at a spot that stays inside the frame for the whole wide shot, the dive and m1-2 (audit #15/#16)
const F0 = [flagS(FL.gb, "", 1120, 1060, null, T_KILL + 1.8), flagS(FL.us, "", ...L(44.55, -71.25), null, T_KILL + 1.8)]; gsap.set(F0, { autoAlpha: 1 });
dateHold("1775", T_SEP - 0.1);
const LGD = legend(T_NORTH + 0.4, null, false);
// "One American army would go north up Lake Champlain toward Montreal"
const MB = unitS("mg", "carth", posOn(LAKEP, 0.02), "infantry", "", { t: T_ONE + 0.2 });
along("mg", sub(LAKEP, 0.02, 0.62, 12), T_NORTH, T_ARN - T_NORTH + 1.0, 12);
arw({ pts: LAKEP, side: "carth", t: T_NORTH + 0.1, dur: 2.2, width: AW(S0, 13), until: T_200 + 0.6 });
SFX("ref:whoosh", T_NORTH + 0.1);
boxL("LAKE CHAMPLAIN", VALC[0] + 60, VALC[1] - 250, T_CHAMP + 0.05, null, { size: 15 });
const TMTL = town("MONTREAL", MTL, "r", T_MTL - 0.05, { until: T_MTL + LBL_LIFE });
// "Arnold's would go up the Kennebec River in Maine, over the mountains, and down the Chaudière River to Quebec"
const AB = pbadge("BENEDICT ARNOLD", "", "arnold", "carth", "bl", "BA", T_ARN, T_FORT + 0.6);
const TR = trail(ROUTE, "#e6f0ff", 4.5 / S0, T_KEN - 0.4, T_QUE - T_KEN + 0.6, null, `${9 / S0} ${7 / S0}`);
SFX("ref:whoosh", T_KEN - 0.3);
boxL("KENNEBEC", KEN[6][0] + 40, KEN[6][1], T_KEN + 0.05, null, { size: 15 });
glowPath(sub(ROUTE, F_CARRY, F_HL, 10), "#bfe2ff", 2.2 / S0, T_MTN, T_MTN + 2.6, 1, 0.6, {});
boxL("CHAUDIÈRE", CHAU[20][0] + 40, CHAU[20][1], T_CHAU + 0.25, null, { size: 15 });
const TQ = town("QUEBEC", QUE, "l", T_QUE + 0.05, { until: T_QUE + LBL_LIFE + 1.0 });
K.target(...QUE, T_QUE + 0.1, { r: 34 / S0, side: "rome", until: T_SEP });
// "the fortress city that held Canada": the fortress on its cliff
const FQ = fortIcon(QUE[0] + 6, QUE[1] + 30, T_FORT - 0.05, T_200 + 1.0, { s: 44, side: "rome" }); SFX("ref:pop", T_FORT);
// "He set out in late September with about eleven hundred men"
dateRun([["SEPTEMBER 1775", T_SEP - 0.1, T_21 - 0.1]]);
const AC = unitS("ac", "carth", posOn(ROUTE, 0.0), "infantry", "", { t: T_SEP + 0.2 }); along("ac", sub(ROUTE, 0, 0.06, 6), T_SEP + 0.4, 3.0, 6);
const N1100 = bigNum("ABOUT", 1100, "MEN", T_1100 - 0.1, T_200 - 0.15, { tick: 0.9, col: "#2e5cb2", wc: "#9fc0ea", top: 190 });
// ---------- the dive onto the Kennebec (northeast + its colours dissolve ~2.8 s) ----------
const CK = [1600, 1235], SK = 1.55;
SFX("whoosh", T_200 - 0.05);
zoom(T_200, 3.4, [1450, 770], 0.70, CK, SK, FTW, "power2.inOut");
fadeL(NE, T_200 + 0.3, 2.8, 0); fadeL(NE_C, T_200 + 0.1, 2.8, 0);
tl.to(TR, { opacity: 0, duration: 0.8 }, T_200 + 2.0); tl.to(B.units.mg.el, { autoAlpha: 0, duration: 0.4 }, T_200 + 0.9); hideU(["ac"], T_200 + 1.0);
// "flat-bottomed boats called bateaux": the boats push upriver from Fort Western (rapids on the way)
const BOATS = [0, 1, 2, 3, 4, 5].map((k) => craft("bateau", sub(KEN_UP, 0.25 - k * 0.035, 0.98 - k * 0.05, 30), T_BAT - 0.2 + k * 0.12, T_KILL + 2.0 - T_BAT, T_KILL + 2.6, { s: 30 }));
SFX("ref:pop", T_BAT);
const RP = [[KEN_UP[iN(KEN_UP, L(44.765, -69.72))], 30], [KEN_UP[iN(KEN_UP, L(44.713, -69.79))], 0], [KEN_UP[iN(KEN_UP, L(45.05, -69.88))], -60]].map(([p, a]) => rapids(p[0] + 4, p[1], T_BAT + 0.6, T_KILL + 1.0, a, 34));
// "The plan said about a hundred and eighty miles, in about twenty days"
const PLAN_IN = T_180 - 0.1, PLAN_OUT = T_20 + 2.2;
const PLAN = listCard("THE PLAN", [["~180 MILES", T_180 + 0.2], ["~20 DAYS", T_20]], "left:0;right:0;top:170px;display:flex;justify-content:center;", PLAN_IN, PLAN_OUT, { size: 58, mw: 440 });
// =====================================================================================================================
// m1-2: the front door (the lake) and the back door (the Maine woods)
// =====================================================================================================================
const CW = [1360, 860], SW = 0.72;
camTo(T_BRIT - 0.3, 2.8, CW, SW, "sine.inOut");
// the British at St. Johns, facing the lake; the first American army coming up it
const RS = [unitS("rs1", "rome", [STJ[0] - 20, STJ[1] + 10], "infantry", "", { t: T_BRIT + 0.2 }), unitS("rs2", "rome", [STJ[0] + 40, STJ[1] - 40], "infantry", "", { t: T_BRIT + 0.35 }),
  unitS("rs3", "rome", [MTL[0] + 30, MTL[1] + 10], "infantry", "", { t: T_BRIT + 0.5 })];
const RSH = craft("ship", [[STJ[0] + 5, STJ[1] + 60], [STJ[0] + 2, STJ[1] + 75]], T_BRIT + 0.3, 2, T_KILL, { s: 26, side: "rome" });
K.target(...posOn(LAKEP, 0.35), T_LAKE + 0.1, { r: 40, side: "rome", until: T_NOB }); SFX("ref:pop", T_LAKE + 0.1);
const MU = unitS("mu", "carth", posOn(LAKEP, 0.0), "infantry", "", { t: T_FIRST - 0.2 });
along("mu", sub(LAKEP, 0.0, 0.38, 10), T_FIRST, 6.0, 10);
arw({ pts: sub(LAKEP, 0.0, 0.45, 10), side: "carth", t: T_FIRST, dur: 1.4, width: AW(SW, 12), until: T_KILL });
// "Nobody expected an army to come out of the Maine woods": the woods pulse round the route
const WOODS = GG.pin(`<div style="width:520px;height:620px;border-radius:50%;background:radial-gradient(ellipse at center, rgba(80,130,70,0.35) 0%, rgba(80,130,70,0.14) 50%, rgba(80,130,70,0) 72%)"></div>`, 1520, 1150, {});
gsap.set(WOODS, { autoAlpha: 0 }); tl.to(WOODS, { autoAlpha: 1, duration: 0.8 }, T_NOB + 0.4); tl.to(WOODS, { autoAlpha: 0.5, duration: 0.7, yoyo: true, repeat: 3 }, T_NOB + 1.2); tl.to(WOODS, { autoAlpha: 0, duration: 0.8 }, T_KILL);
boxL("MAINE WOODS", 1600, 1180, T_WOODS + 0.05, null, { size: 15 });
// "come in through the back door": the route re-drawn bright to Quebec, THE BACK DOOR (stamp ~3 s)
const TR2 = trail(ROUTE, "#e6f0ff", 4.5 / SW, T_IDEA + 0.2, T_BACK - T_IDEA, T_KILL + 0.8, `${9 / SW} ${7 / SW}`);
arw({ pts: sub(ROUTE, 0.82, 1.0, 8), side: "carth", t: T_BACK - 0.3, dur: 0.8, width: AW(SW, 13), until: T_KILL });
const BD = sstamp("THE BACK DOOR", 180, T_BACK - 0.05, { size: 78, color: "#9fc0ea", until: T_BACK + 3.0, shake: 5 });
K.target(...QUE, T_BACK + 0.1, { r: 50, side: "carth", until: T_ATT + 0.8 });
// "while the front door held everyone's attention"
glowPath(LAKEP, "#ffd54a", 5 / SW, T_FRONT, T_KILL, 2, 0.8, { draw: 0.8 });
wstampL("FRONT DOOR", VALC[0] + 70, VALC[1] - 60, T_FRONT + 0.15, null, "#ffd54a", 20);
// =====================================================================================================================
// m1-3: the Great Carrying Place and the Dead River (close, no ground tint)
// =====================================================================================================================
const CG = [1585, 1045], SG = 2.6;
camTo(T_KILL - 0.6, 3.2, CG, SG, "power2.inOut");
hideU(["rs1", "rs2", "rs3", "mu"], T_KILL - 0.4);
const F3 = [flagS(FL.us, "", 1700, 1150, T_KILL + 0.8, T_FEW + 1.2), flagS(FL.gb, "", 1300, 960, T_KILL + 0.8, T_FEW + 1.2)];
// boats at the carry start; barrels inside them spoil (go green-grey)
const B3 = [0, 1, 2].map((k) => craft("bateau", sub(KEN_UP, 0.86 + k * 0.03, 0.95 + k * 0.02, 6), T_KILL + 1.4 + k * 0.15, T_LEAK + 1.6 - T_KILL, T_HAUL + 0.4, { s: 30 }));
const BAR = [[1650, 1060], [1662, 1048], [1640, 1072], [1668, 1066]].map((p, k) => icon(ICO.barrel(), p[0], p[1], T_LEAK + 0.6 + k * 0.1, T_HAUL + 0.5));
BAR.forEach((el) => tl.to(el.firstElementChild, { filter: "hue-rotate(60deg) saturate(0.6) brightness(0.8)", duration: 0.6 }, T_SPOIL));
SFX("ref:pop", T_SPOIL + 0.1);
// the Great Carrying Place: the ponds, the dotted carry, boats and barrels hauled across
const PONDS = [L(45.17, -70.05), L(45.165, -70.09), L(45.175, -70.13)].map((p, k) => { const e = document.createElementNS(NS, "ellipse");
  e.setAttribute("cx", p[0]); e.setAttribute("cy", p[1]); e.setAttribute("rx", [4, 3, 3.6][k]); e.setAttribute("ry", [2.6, 2.2, 2.4][k]); e.setAttribute("fill", "rgb(122,160,190)");
  e.setAttribute("stroke", "rgba(150,128,90,0.7)"); e.setAttribute("stroke-width", 0.6); OVL.appendChild(e); gsap.set(e, { opacity: 0 }); tl.to(e, { opacity: 1, duration: 0.6 }, T_GCP + 0.2); return e; });
const GCPL = boxL("GREAT CARRYING PLACE", CARRY0[0] + 10, CARRY0[1] - 40, T_GCP + 0.1, null, { size: 15 });
const CT = trail(CARRY, "#f3eee2", 4 / SG, T_HAUL - 0.2, T_POND - T_HAUL + 0.5, T_STORM, `${9 / SG} ${7 / SG}`);
const HB = craft("bateau", CARRY, T_HAUL, T_NIGHT - T_HAUL + 1.0, T_STORM - 0.2, { s: 28 });
const HBR = icon(ICO.barrel(), CARRY[0][0], CARRY[0][1] + 8, T_HAUL + 0.3, T_STORM - 0.2); pinAlong(HBR, CARRY.map(([x, y]) => [x, y + 8]), T_HAUL + 0.4, T_NIGHT - T_HAUL + 1.2, 16);
SFX("ref:whoosh", T_HAUL);
const M12 = wstampL("12 MILES", (CARRY[0][0] + CARRY[4][0]) / 2, CARRY[2][1] + 28, T_12 + 0.05, null, "#f7f3ea", 22);
// the boats wait on the Dead River above the carry
const DB = [0, 1, 2, 3].map((k) => craft("bateau", sub(DEAD_UP, 0.0 + k * 0.035, 0.16 + k * 0.04, 8), T_POND + 0.2 + k * 0.2, 4.0, T_REST, { s: 28 }));
// "on the night of the twenty-first of October": night, the date; "a storm hit the Dead River": rain, flicker, wind
const NW = nightWash(T_NIGHT, T_MORN, 0.5);
dateRun([["21 OCTOBER 1775", T_21, T_FEW - 0.1], ["OCTOBER 1775", T_FEW, null]]);
const RN = rain(T_STORM - 0.1, T_MORN + 1.6, 0.55);
const FLASH = document.createElement("div"); FLASH.style.cssText = "position:absolute;inset:0;background:rgba(220,230,255,0.22);pointer-events:none"; document.getElementById("fx").appendChild(FLASH); gsap.set(FLASH, { autoAlpha: 0 }); [T_STORM + 0.25, T_TREES + 0.1].forEach((t) => { tl.to(FLASH, { autoAlpha: 1, duration: 0.05 }, t); tl.to(FLASH, { autoAlpha: 0, duration: 0.25 }, t + 0.07); });
SFX("ref:boom", T_STORM + 0.3); K.shake(T_STORM + 0.3, 3, 0.4);
const DR = glowPath(sub(DEADR, 0.12, 0.82, 30), "#bfe2ff", 1.4 / SG * 2, T_DEAD - 0.05, T_FEW, 2, 0.75);
boxL("DEAD RIVER", 1470, 1065, T_DEAD + 0.1, null, { size: 15 });
// "Trees came down"
const TREES = [[1530, 1012], [1500, 1052], [1470, 1000], [1545, 1050], [1440, 1020]].map((p, k) => icon(ICO.tree, p[0], p[1], T_TREES + 0.1 + k * 0.18, T_FEW, { k: 2.5 }));
tl.from(TREES.map((e) => e.firstElementChild), { rotation: -70, duration: 0.3, stagger: 0.18, immediateRender: false }, T_TREES + 0.1);
SFX("hit", T_TREES + 0.3);
// "by morning the river had risen eight to ten feet": the river swells (a flood band grows along it)
const FLD = document.createElementNS(NS, "path"); FLD.setAttribute("d", "M" + sub(DEADR, 0.05, 0.85, 40).map((q) => q.join(" ")).join(" L"));
FLD.setAttribute("fill", "none"); FLD.setAttribute("stroke", "rgba(110,150,185,0.6)"); FLD.setAttribute("stroke-width", 1.5); FLD.setAttribute("stroke-linecap", "round"); FLD.setAttribute("stroke-linejoin", "round");
OVL.insertBefore(FLD, OVL.firstChild.nextSibling); gsap.set(FLD, { opacity: 0 });
tl.to(FLD, { opacity: 1, duration: 0.6 }, T_MORN); tl.to(FLD, { attr: { "stroke-width": 9 }, duration: 3.0, ease: "power1.inOut" }, T_MORN + 0.3); tl.to(FLD, { opacity: 0.55, duration: 1.5 }, T_FEW + 1);
tl.to(FLD, { opacity: 0, duration: 1.2 }, T_BEH);
const FEET_OUT = T_FEET + 2.9;
const FEET = numCard("THE RIVER ROSE", "8–10 FEET", "", "right:110px;top:250px;", T_FEET - 0.05, FEET_OUT, { col: "#6f9bff", vs: 58 });
// "Boats sank, supplies washed away, and men lost their way in the flooded woods"
DB.slice(0, 2).forEach((el, k) => { tl.to(el, { autoAlpha: 0.25, duration: 0.12, yoyo: true, repeat: 3 }, T_SANK + k * 0.25); tl.to(el, { autoAlpha: 0, scale: 0.5, duration: 0.5 }, T_SANK + 0.6 + k * 0.25); });
SFX("ref:pop", T_SANK + 0.1);
const WB = [[1530, 1020], [1515, 1035], [1495, 1030]].map((p, k) => icon(ICO.barrel(), p[0], p[1], T_WASH - 0.6, T_WASH + 2.2, {}));
WB.forEach((el, k) => tl.to(el, { left: "+=" + (30 + k * 12), top: "+=" + (-6 + k * 4), rotation: 80, duration: 2.0, ease: "power1.in" }, T_WASH));
const MEN = [[1480, 1060], [1500, 1075], [1460, 1078], [1520, 1068]].map((p, k) => icon(ICO.man, p[0], p[1], T_LOST - 0.1 + k * 0.1, T_FEW + 1.0, { pop: false }));
MEN.forEach((el, k) => pinAlong(el, [[[1480, 1060], [1468, 1084], [1490, 1096]], [[1500, 1075], [1515, 1095], [1500, 1110]], [[1460, 1078], [1440, 1070], [1432, 1090]], [[1520, 1068], [1540, 1088], [1528, 1100]]][k], T_LOST + 0.1, 3.0, 6));
const QS = [[1475, 1100], [1525, 1105]].map((p, k) => icon(ICO.q, p[0], p[1], T_FLOOD + k * 0.2, T_FEW + 1.0));
// =====================================================================================================================
// m1-4: three companies turn back; the rest go on; Arnold ahead down the Chaudière; cattle + flour; the hunger
// =====================================================================================================================
const C4 = [1440, 745], S4 = 1.55;   // SARTIGAN + the farms stay clear of the legend
camTo(T_FEW - 0.3, 2.8, C4, S4, "sine.inOut");
const F4 = [flagS(FL.us, "", 1640, 1000, T_FEW + 1.0, null), flagS(FL.gb, "", 1200, 700, T_FEW + 1.0, null)];
const fpos = (f) => posOn(ROUTE, f);
// the column on the Dead River: three companies at the rear (east), the rest ahead
const REAR = ["c1", "c2", "c3"].map((id, k) => unitS(id, "carth", fpos(F_DEAD + 0.01 + k * 0.018), "infantry", "", { t: T_FEW + 0.2 + k * 0.1, w: 44, h: 29 }));
const AHEAD = ["c4", "c5", "c6"].map((id, k) => unitS(id, "carth", fpos(F_DEAD + 0.09 + k * 0.025), "infantry", "", { t: T_FEW + 0.1 + k * 0.1, w: 44, h: 29 }));
K.target(...fpos(F_DEAD + 0.028), T_3C + 0.1, { r: 30, side: "carth", until: T_TURN + 0.5 });
tl.to(REAR.map((id) => B.units[id].el.firstElementChild), { scale: 1.25, duration: 0.2, yoyo: true, repeat: 1 }, T_COUN + 0.1); SFX("ref:pop", T_COUN + 0.1);
// "turned back for home": grey, back down the carry and the Kennebec, with food
B.grey(REAR, T_TURN, 0.6);
REAR.forEach((id, k) => along(id, [fpos(F_DEAD + 0.01 + k * 0.018), DEAD0, ...CARRY.slice().reverse().slice(1), ...KEN_UP.slice().reverse().slice(0, 30 - k * 4)], T_TURN + 0.3 + k * 0.15, T_REST - T_TURN + 1.5, 16));
const ARWG = arw({ pts: [DEAD0, CARRY[2], CARRY0, KEN_UP[KEN_UP.length - 12]], side: "carth", t: T_TURN + 0.2, dur: 1.4, width: AW(S4, 10), dash: "10 7", until: T_PUSH });
gsap.set(ARWG, { filter: "grayscale(1) brightness(1.15)" });
const N450_OUT = T_450 + 2.9;
const N450 = numCard("TURNED BACK · ABOUT", "450 MEN", "", "right:110px;top:240px;", T_450 - 0.1, N450_OUT, { col: "#8a867c", lc: "#c9c2b2", vs: 58 });
const FB = [0, 1, 2].map((k) => icon(ICO.barrel(), DEAD0[0] + 8 + k * 6, DEAD0[1] + 10, T_SHARE, T_REST + 2.0));
FB.forEach((el, k) => pinAlong(el, [[DEAD0[0] + 8 + k * 6, DEAD0[1] + 10], [CARRY[2][0] + k * 6, CARRY[2][1] + 10], [CARRY0[0] + k * 6, CARRY0[1] + 10]], T_SHARE + 0.2, 3.0, 8));
SFX("ref:pop", T_SHARE + 0.1);
// "The rest kept going": up the Dead River toward the height of land
AHEAD.forEach((id, k) => along(id, sub(ROUTE, F_DEAD + 0.09 + k * 0.025, F_HL - 0.02 + k * 0.012, 14), T_REST, T_DEAR - T_REST, 14));
arw({ pts: sub(ROUTE, F_DEAD + 0.1, F_HL + 0.02, 10), side: "carth", t: T_REST + 0.1, dur: 1.4, width: AW(S4, 12), until: T_DOG });
// "Arnold pushed ahead with a small party, down the rapids of the Chaudière to the first French farms"
const AB2 = pbadge("BENEDICT ARNOLD", "", "arnold", "carth", "bl", "BA", T_PUSH, T_BEH);
const AM = faceMarker("arnold", "BA", "carth", ...fpos(F_HL + 0.03), T_PUSH + 0.1, T_BEH + 1.5, 46);
pinAlong(AM, sub(ROUTE, F_HL + 0.03, F_SART, 20), T_PUSH + 0.6, T_FARM - T_PUSH - 0.2, 20);
trail(sub(ROUTE, F_HL + 0.03, F_SART, 20), "#e6f0ff", 4 / S4, T_PUSH + 0.6, T_FARM - T_PUSH - 0.2, T_DOG, `${9 / S4} ${7 / S4}`);
SFX("ref:whoosh", T_PUSH + 0.6);
[0.35, 0.55, 0.75].forEach((f, k) => { const p = posOn(CHAU_DN, f); rapids(p[0] + 4, p[1], T_RAP + k * 0.15, T_BEH, -70, 30); });
boxL("CHAUDIÈRE", CHAU[12][0] + 26, CHAU[12][1] + 10, T_CHA4 - 0.05, null, { size: 15 });
const TS = town("SARTIGAN", SART, "r", T_FARM, { until: T_FARM + LBL_LIFE });
const HS = [[16, -22], [-24, -16], [6, 26]].map(([dx, dy], k) => icon(ICO.house, SART[0] + dx, SART[1] + dy, T_FARM + 0.2 + k * 0.12, null));
// "and sent back cattle and flour": cattle + sacks move back up the trail toward the column
const BACKP = sub(ROUTE, F_SART, F_HL + 0.02, 18).map(([x, y]) => [x - 12, y]);
const COWS = [0, 1, 2].map((k) => icon(ICO.cow, ...BACKP[0], T_CATTLE + k * 0.25, T_EATEN + 1.0));
COWS.forEach((el, k) => pinAlong(el, BACKP.slice(0, 18 - k * 2), T_CATTLE + 0.3 + k * 0.3, T_DOG - T_CATTLE, 18));
const SACK = icon(ICO.sack, ...BACKP[0], T_CATTLE + 0.5, T_EATEN + 1.0); pinAlong(SACK, BACKP.slice(0, 13), T_CATTLE + 0.8, T_DOG - T_CATTLE, 14);
SFX("ref:pop", T_CATTLE + 0.1);
// "Behind him, one of his captains, Henry Dearborn": back to the column (initials badge)
camTo(T_BEH - 0.2, 3.0, [1395, 880], 1.75, "sine.inOut");
const DB2 = pbadge("HENRY DEARBORN", "CAPTAIN", "dearborn", "carth", "tr", "HD", T_DEAR + 0.05, T_DOG + 2.2);
// the hunger card: one line per spoken item, only the last two stay (finished lines drop, audit #22)
const HUNG = listCard("EATEN", [["HIS DOG", T_DOG + 0.2], ["SHAVING SOAP", T_SOAP], ["LIP SALVE", T_LIP], ["SHOE LEATHER", T_SHOE + 0.5], ["CARTRIDGE BOXES", T_CART]],
  "left:0;right:0;top:150px;display:flex;justify-content:center;", T_DOG + 0.15, END + 1, { size: 50, mw: 520, kickT: T_EATEN, col: "#c4121f", kc: "#ff8a80", keep: 2 });
// the HUD steps out under the big cards (1c); the date scroll stays
declutter([LGD, AB, AB2, DB2], [[0.25, T_NORTH - 0.1], [T_QUE, T_QUE + LBL_LIFE + 1.0], [T_1100 - 0.1, T_200 - 0.15], [PLAN_IN, PLAN_OUT], [T_BACK - 0.05, T_BACK + 3.0], [T_FEET - 0.05, FEET_OUT],
  [T_450 - 0.1, N450_OUT], [T_FARM - 0.3, T_BEH + 0.3], [T_DOG + 0.15, END + 1]]);   // + the legend steps out while SARTIGAN sits under it
fixImgs();
B.finish();
