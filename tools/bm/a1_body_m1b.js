// M1B (m1-5 .. m1-8), Benedict Arnold #17: QUEBEC, November 1775 - May 1776. Map agent a1_.
// Built with: python3 tools/a1_inline.py m1b m1-5 m1-8 quebec      (world = the quebec map px, z14, 6.5 m/px)
// Look: v11 + 2c: no ground tint (a city map: two-colour glowing fronts only), words leave after ~3.5 s; Continental Colours vs Union Flag 1606.
// m1-5: 9 NOVEMBER 1775; ~600 come out of the forest on the south bank (ABOUT 600 MEN); ST. LAWRENCE + QUEBEC on the words; THE MARCH ~350 MILES,
//   NEARLY TWICE THE 180 PLANNED; night 13 NOVEMBER: SOME 35 CANOES slip across between two red warships to Wolfe's Cove and up onto the
//   PLAINS OF ABRAHAM; the walls glow on "the walls of Quebec"; Arnold's badge on "Arnold had to wait".
// m1-6: DECEMBER 1775; Montgomery's column from upriver (badge on his name, ~300 MEN); ENLISTMENTS RUN OUT · END OF THE YEAR; night of
//   31 DECEMBER 1775; snow on "blizzard"; the two attack arrows on "they attacked"; the paper slip "Liberty or death" (handwriting) on its words.
// m1-7: close on the Lower Town, night + snow, option 2: Montgomery under Cape Diamond to the first barrier, the blockhouse gun fires (visible),
//   KILLED; his column falls back; Arnold along the waterfront to the SAULT-AU-MATELOT barricade, hit in the leg, helped back; Morgan over the
//   barricade, STALLED; a red column out of the Palace Gate behind them, the ring closes; casualty card (spoken numbers only).
// m1-8: grey dawn, wide: the hospital (PISTOLS LOADED / A SWORD ON HIS BED / THEY NEVER CAME); the blockade line through the winter (date scroll
//   to MAY 1776); RESULT QUEBEC HELD · THE MARCH ~350 MILES; ARNOLD'S METHOD: only line 1 (the re-voiced m1-8 speaks only "go where the enemy says no army can go").
// Facts: FACT_NOTES MOVE 1 + FACTCHECK_A (Pointe-Lévy 9 Nov; 35 canoes/dugouts past Lizard + Hunter 13-14 Nov to Wolfe's Cove; Montgomery ~300
//   early Dec; enlistments 31 Dec; "Liberty or death"; Près-de-Ville grapeshot; Sault-au-Matelot; Morgan; Palace Gate sortie; ~400 captured,
//   30-60 killed, defenders <20; Senter's pistols; blockade to May 1776).
// @@KIT
const P5 = "m1-5", P6 = "m1-6", P7 = "m1-7", P8 = "m1-8";
const T_9 = at(P5, "the ninth of November"), T_600 = at(P5, "six hundred men"), T_FOREST = at(P5, "out of the forest"), T_STL = at(P5, "St. Lawrence"),
  T_FROMQ = at(P5, "from Quebec"), T_350 = at(P5, "three hundred and fifty"), T_TWICE = at(P5, "nearly twice"), T_4N = at(P5, "Four nights later"),
  T_35 = at(P5, "thirty-five canoes"), T_SLIP = at(P5, "slipped across"), T_WAR = at(P5, "two British warships"), T_CLIMB = at(P5, "climbed onto"),
  T_PLAINS = at(P5, "the Plains of Abraham"), T_WORN = at(P5, "But six hundred"), T_WALLS = at(P5, "the walls of Quebec"), T_WAIT = at(P5, "Arnold had to wait");
const T_DEC = at(P6, "In early December"), T_RM = at(P6, "Richard Montgomery"), T_FROMM = at(P6, "from Montreal"), T_300 = at(P6, "three hundred"),
  T_DEAD = at(P6, "a deadline"), T_ENL = at(P6, "The enlistments"), T_EOY = at(P6, "the end of the year"), T_STORM = at(P6, "waited for a storm"),
  T_LAST = at(P6, "the last night"), T_BLIZ = at(P6, "blizzard"), T_ATT = at(P6, "they attacked"), T_PAPER = at(P6, "a piece of paper"),
  T_LIB = at(P6, "Liberty or");
const T_PLAN = at(P7, "The plan was"), T_LOWER = at(P7, "the Lower"), T_CLIFFS = at(P7, "below the cliffs"), T_BOTH = at(P7, "both sides"),
  T_MCAME = at(P7, "Montgomery came"), T_CAPE = at(P7, "Cape"), T_BARR = at(P7, "the first barrier"), T_GRAPE = at(P7, "grapeshot fired"),
  T_KILLED = at(P7, "Montgomery was killed"), T_FELL = at(P7, "His column fell back"), T_NORTH = at(P7, "On the north side"), T_ALED = at(P7, "Arnold led"),
  T_WATER = at(P7, "the waterfront"), T_BARRI = at(P7, "a barricade"), T_SAULT = at(P7, "Sault-au-Matelot"), T_LEG = at(P7, "in the leg"),
  T_REAR = at(P7, "helped to the rear"), T_RIFLE = at(P7, "His rifle captain"), T_DM = at(P7, "Daniel Morgan"), T_OVER = at(P7, "got over the barricade"),
  T_STALL = at(P7, "stalled"), T_WET = at(P7, "powder was wet"), T_GATE = at(P7, "came out of"), T_BEHIND = at(P7, "a gate behind them"),
  T_400 = at(P7, "About four hundred"), T_CAPT = at(P7, "were captured"), T_3060 = at(P7, "between thirty and"), T_DEF = at(P7, "The defenders"),
  T_20 = at(P7, "fewer than twenty");
const T_HOSP = at(P8, "In the hospital"), T_PIST = at(P8, "pistols"), T_SWORD = at(P8, "a sword"), T_KILLAS = at(P8, "he would kill"),
  T_NEVER = at(P8, "They never came"), T_FEW = at(P8, "With a few hundred"), T_SIEGE = at(P8, "under siege"), T_WINTER = at(P8, "rest of the winter"),
  T_NOTF = at(P8, "The city had not fallen"), T_SHOWN = at(P8, "But Arnold had"), T_HOW = at(P8, "how he fought"), T_GO = at(P8, "go where the enemy");
// =====================================================================================================================
// THE WORLD: the quebec relief; places (quebec px)
// =====================================================================================================================
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); const NA = LV.north(); LV.scaleBar(6.54);
const L = (a, b) => LD(a, b);
const WOLFE = [1238, 1118], LEVIS = L(46.800, -71.180), PLAINS = [1235, 905], QUE = L(46.8115, -71.2105), PDV = L(46.803, -71.207), SAULT = L(46.8161, -71.2017),
  PALACE = L(46.817, -71.208), CAPE = L(46.8065, -71.2065), STROCH = L(46.8145, -71.2230);
const WALL = [[46.8060, -71.2075], [46.8085, -71.2130], [46.8110, -71.2150], [46.8135, -71.2140], [46.8155, -71.2110], [46.8170, -71.2080]].map((q) => L(...q));
const MPATH = [WOLFE, [1300, 1062], [1370, 1010], [1430, 965], [PDV[0] - 22, PDV[1] + 12]];
const APATH = [STROCH, [1370, 692], [1469, 676], [1510, 684], [SAULT[0] - 10, SAULT[1] - 6]];
const LOWER = [[PDV[0] + 4, PDV[1] + 4], [1505, 880], [1532, 810], [1550, 750], [SAULT[0] + 4, SAULT[1] + 2], [1500, 690]];
// the walled Upper Town: the land wall (brown) + British garrison (red)
const WALLP = glowPath(WALL, "#6b4a2a", 9, 0, null, 0, 0.9, {}); gsap.set(WALLP, { opacity: 0.9 }); tl.set(WALLP, { opacity: 0.9 }, 0);
const WALLR = glowPath(WALL, "#c4121f", 3.5, 0, null, 0, 0.9, { dash: "8 5", top: true }); gsap.set(WALLR, { opacity: 0.9 }); tl.set(WALLR, { opacity: 0.9 }, 0);
const GAR = [unitS("g1", "rome", [QUE[0] + 20, QUE[1] - 10], "infantry", ""), unitS("g2", "rome", [QUE[0] + 80, QUE[1] - 70], "infantry", "")];
GAR.forEach((id) => gsap.set(B.units[id].el, { autoAlpha: 1 }));
// =====================================================================================================================
// m1-5: the south bank; the night crossing to Wolfe's Cove and the Plains of Abraham
// =====================================================================================================================
const C5 = [1460, 990], S5 = 0.85;
camSet([1480, 1000], 0.82); camTo(0, 12, C5, S5, "sine.inOut");
const F0 = [flagS(FL.gb, "", QUE[0] - 40, QUE[1] - 150, null, T_PLAN + 1.4), flagS(FL.us, "", 2050, 1250, null, T_DEC + 1.0)]; gsap.set(F0, { autoAlpha: 1 });
dateHold("NOVEMBER 1775", T_9); dateRun([["9 NOVEMBER 1775", T_9, T_4N - 0.1], ["13 NOVEMBER 1775", T_4N, T_DEC - 0.1], ["DECEMBER 1775", T_DEC, T_LAST - 0.1], ["31 DECEMBER 1775", T_LAST, T_WINTER - 0.35]]);
const LGD = legend(T_STL + 0.6, null, true);
// "about six hundred men came out of the forest on the bank of the St. Lawrence"
const SB = ["s1", "s2", "s3"].map((id, k) => unitS(id, "carth", [2120 + k * 60, 1500 + k * 30], "infantry", "", { t: T_FOREST - 0.6 + k * 0.15 }));
SB.forEach((id, k) => go(id, T_FOREST - 0.4 + k * 0.15, 3.2, [[LEVIS[0] + 10, LEVIS[1] + 100], [LEVIS[0] + 90, LEVIS[1] + 60], [LEVIS[0] - 40, LEVIS[1] + 150]][k]));
arw({ pts: [[2150, 1480], [2000, 1300], [1880, 1140]], side: "carth", t: T_FOREST - 0.3, dur: 1.4, width: AW(S5, 13), until: T_TWICE });
SFX("ref:whoosh", T_FOREST - 0.3);
const N600 = numCard("ABOUT", "600 MEN", "", "right:110px;top:240px;", T_600 - 0.05, T_STL - 0.2, { col: "#2e5cb2", vs: 62 });
boxL("ST. LAWRENCE", 1330, 1185, T_STL + 0.05, null, { size: 15, bg: "#dcecf8" });
const TQ = town("QUEBEC", [QUE[0] - 10, QUE[1] - 30], "l", T_FROMQ, { until: T_FROMQ + LBL_LIFE });
// "about three hundred and fifty miles, nearly twice the distance on the plan"
const MARCH_OUT = T_TWICE + 2.4;   // big cards on the right: the Union Flag over the city stays in view
const MARCH = listCard("THE MARCH", [["~350 MILES", T_350 + 0.3], ["NEARLY TWICE THE 180 PLANNED", T_TWICE + 0.2]], "right:90px;top:240px;display:flex;justify-content:flex-end;", T_350 + 0.1, MARCH_OUT, { size: 44, mw: 480, col: "#2e5cb2", kc: "#9fc0ea" });
// "Four nights later, in some thirty-five canoes and dugouts, they slipped across the river between two British warships"
const NW1 = nightWash(T_4N, T_WORN + 0.4, 0.5);
const N35_OUT = T_35 + 2.9;
const N35 = numCard("SOME", "35 CANOES", "AND DUGOUTS", "right:110px;top:240px;", T_35 - 0.05, N35_OUT, { col: "#2e5cb2", vs: 54 });
const SHIPA = [1495, 1040], SHIPB = [1330, 1235];
const WS = [craft("ship", [SHIPA, [SHIPA[0] + 2, SHIPA[1] - 1]], T_WAR - 0.4, 3, T_WORN + 1.0, { s: 34, side: "rome" }), craft("ship", [SHIPB, [SHIPB[0] + 2, SHIPB[1] - 1]], T_WAR - 0.25, 3, T_WORN + 1.0, { s: 34, side: "rome" })];
SFX("ref:pop", T_WAR);
const CROSS = [[1668, 1072], [1560, 1094], [1450, 1110], [1340, 1120], [WOLFE[0] + 16, WOLFE[1] + 4]];
const CAN = [0, 1, 2, 3, 4, 5].map((k) => craft("canoe", CROSS.map(([x, y]) => [x + (k % 3) * 22 - 22, y + Math.floor(k / 3) * 20 - 10]), T_35 + 0.3 + k * 0.25, T_CLIMB - T_35 - 0.4, T_PLAINS + 0.6, { s: 36 }));
SFX("ref:whoosh", T_SLIP);
// "and climbed onto the Plains of Abraham"
const PU = ["p1", "p2", "p3"].map((id, k) => unitS(id, "carth", [WOLFE[0] + k * 20, WOLFE[1]], "infantry", "", { t: T_CLIMB - 0.1 + k * 0.1 }));
PU.forEach((id, k) => go(id, T_CLIMB + 0.1 + k * 0.1, 2.0, [[PLAINS[0] - 40, PLAINS[1] + 30], [PLAINS[0] + 30, PLAINS[1] - 10], [PLAINS[0] - 10, PLAINS[1] + 90]][k]));
arw({ pts: [[WOLFE[0] - 4, WOLFE[1] - 14], [1225, 1010], [PLAINS[0] - 10, PLAINS[1] + 50]], side: "carth", t: T_CLIMB, dur: 1.0, width: AW(S5, 12), until: T_WAIT });
hideU(["s1", "s2", "s3"], T_CLIMB + 0.5);
boxL("PLAINS OF ABRAHAM", PLAINS[0] - 120, PLAINS[1] - 70, T_PLAINS + 0.1, null, { size: 15 });
// "could not storm the walls of Quebec": the wall pulses red
const WG = glowPath(WALL, "#ff6b5e", 8, T_WALLS - 0.05, T_DEC, 2, 0.95, { top: true });
SFX("ref:pop", T_WALLS);
const AB = pbadge("BENEDICT ARNOLD", "", "arnold", "carth", "bl", "BA", T_WAIT, T_DEC + 0.4);
// =====================================================================================================================
// m1-6: Montgomery arrives; the deadline; the blizzard; "Liberty or death"
// =====================================================================================================================
const C6 = [1250, 1000], S6 = 0.8;
camTo(T_DEC - 0.6, 3.0, C6, S6, "sine.inOut");
const F1 = [flagS(FL.us, "", 900, 960, T_DEC + 0.2, T_PLAN + 1.0)];
const MPTS = [[200, 1500], [508, 1236], [800, 1110], [1000, 1010], [PLAINS[0] - 90, PLAINS[1] + 40]];
const MC = ["mc1", "mc2"].map((id, k) => unitS(id, "carth", MPTS[0], "infantry", "", { t: T_RM - 0.4 + k * 0.2 }));
MC.forEach((id, k) => along(id, sub(MPTS, 0, 1 - k * 0.04, 14).map(([x, y]) => [x - k * 40, y + k * 20]), T_RM - 0.3 + k * 0.2, T_DEAD - T_RM, 14));
arw({ pts: MPTS, side: "carth", t: T_RM - 0.2, dur: 2.4, width: AW(S6, 13), until: T_EOY });
SFX("ref:whoosh", T_RM - 0.2);
const MB = pbadge("RICHARD MONTGOMERY", "GENERAL", "rmontgomery", "carth", "tr", "RM", T_RM + 0.1, T_KILLED + 2.4);
const N300 = tagL("~300 MEN", 820, 1180, T_300 + 0.05, null, 16);
// "The enlistments ... ran out at the end of the year": the calendar card
const CAL = `<svg width="64" height="64" viewBox="0 0 64 64" style="display:block"><rect x="6" y="10" width="52" height="48" rx="4" fill="#f3eee2" stroke="#c9b48a" stroke-width="3"/><rect x="6" y="10" width="52" height="13" rx="4" fill="#c4121f"/><text x="32" y="51" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="24" fill="#1b1812">31</text><rect x="16" y="4" width="5" height="12" rx="2" fill="#8a867c"/><rect x="43" y="4" width="5" height="12" rx="2" fill="#8a867c"/></svg>`;
const EOY = placeCard("ENLISTMENTS RUN OUT", "THE END OF THE YEAR", "right:90px;top:240px;display:flex;justify-content:flex-end;", T_EOY - 0.05, T_STORM + 0.6, CAL);
SFX("hit", T_EOY + 0.1);
// "on the last night of seventeen seventy-five, in a blizzard, they attacked"
const NW2 = nightWash(T_LAST, T_HOSP + 0.2, 0.55);
B.snow(T_BLIZ - 0.1, T_NEVER);
SFX("ref:whoosh", T_ATT);
const A1p = arw({ pts: [[PLAINS[0] - 60, PLAINS[1] + 60], [1250, 1030], [1380, 975], [PDV[0] - 20, PDV[1] + 10]], side: "carth", t: T_ATT, dur: 1.2, width: AW(S6, 12), dash: "12 9", until: T_PLAN + 1.2 });
const A2p = arw({ pts: [[PLAINS[0] - 20, PLAINS[1] - 60], [STROCH[0], STROCH[1] + 40], [1420, 680], [SAULT[0] - 20, SAULT[1] - 10]], side: "carth", t: T_ATT + 0.15, dur: 1.2, width: AW(S6, 12), dash: "12 9", until: T_PLAN + 1.2 });
// the paper slip in every cap: blank on "a piece of paper ... in his cap", the words on "Liberty or death" (~4 s in all)
const SLIP_IN = T_PAPER + 1.0, SLIP_OUT = T_LIB + 2.6;
const SLIP = scr(`<div style="transform:rotate(-3deg);padding:26px 60px 30px;background:linear-gradient(170deg,#f6efdc,#e6d8b4);box-shadow:0 18px 40px rgba(0,0,0,.6);border:1px solid #b9a77c;min-width:520px;text-align:center">
  <div class="lw" style="font-family:'Special Elite',monospace;font-size:66px;color:#2a2018;letter-spacing:.02em">&ldquo;Liberty or death.&rdquo;</div></div>`,
  "right:90px;top:600px;display:flex;justify-content:flex-end;", SLIP_IN, SLIP_OUT, { autoAlpha: 0, y: 40, rotation: 6 });
gsap.set(SLIP.querySelector(".lw"), { autoAlpha: 0 }); tl.to(SLIP.querySelector(".lw"), { autoAlpha: 1, duration: 0.5 }, T_LIB - 0.05); SFX("ref:pop", SLIP_IN); SFX("hit", T_LIB + 0.1);
// =====================================================================================================================
// m1-7: the Lower Town at night in the snow (option 2: two glowing fronts only)
// =====================================================================================================================
const C7 = [1440, 830], S7 = 2.15;
camTo(T_PLAN - 0.2, 3.0, C7, S7, "power2.inOut");
hideU(["mc1", "mc2", "p1", "p2", "p3"], T_PLAN + 0.2);
const F2 = [flagS(FL.gb, "", QUE[0] - 30, QUE[1] - 40, T_PLAN + 1.4, T_HOSP + 0.6), flagS(FL.us, "", 1250, 900, T_PLAN + 1.4, T_HOSP + 0.6)];
const LT = glowPath(LOWER, "#ffd54a", 5 / S7, T_LOWER, T_BOTH + 2.0, 2, 0.8, { draw: 1.0, top: true });
boxL("LOWER TOWN", 1590, 820, T_LOWER + 0.1, null, { size: 15 });
SFX("ref:pop", T_LOWER + 0.1);
glowPath(WALL, "#f3eee2", 4 / S7, T_CLIFFS, T_CLIFFS + 2.2, 1, 0.6, {});
// Montgomery's column under Cape Diamond to the first barrier
const MCOL = unitS("mk", "carth", MPATH[1], "infantry", "", { t: T_MCAME - 0.2, w: 44, h: 29 });
along("mk", sub(MPATH, 0.15, 1, 12), T_MCAME, T_BARR - T_MCAME + 0.4, 12);
const MF = faceMarker("rmontgomery", "RM", "carth", ...MPATH[1], T_MCAME - 0.1, T_FELL + 1.2, 44);
pinAlong(MF, sub(MPATH, 0.15, 0.95, 12).map(([x, y]) => [x - 6, y + 34]), T_MCAME, T_BARR - T_MCAME + 0.4, 12);
boxL("CAPE DIAMOND", CAPE[0] + 40, CAPE[1] - 10, T_CAPE, null, { size: 15 });
const BH = redoubt(PDV[0] + 4, PDV[1] - 6, T_BARR, null, { s: 34 });
const FP = front2([[PDV[0] - 10, PDV[1] - 22], [PDV[0] - 2, PDV[1] + 4], [PDV[0] + 8, PDV[1] + 26]], S7, T_BARR + 0.1, { dur: 0.6, flip: true });
// "a cannon loaded with grapeshot fired": the blockhouse gun, visible, and the grapeshot spray
shoot([PDV[0] - 2, PDV[1] - 2], [PDV[0] - 26, PDV[1] + 13], T_GRAPE + 0.4, { dur: 0.25, r: 7 });
mg([PDV[0] - 4, PDV[1]], [PDV[0] - 40, PDV[1] + 18], T_GRAPE + 0.45, 7, 1.0);
pulse(T_GRAPE + 0.7);
badgeStamp(MB, "KILLED", T_KILLED + 0.4, { size: 30 }); greyM(MF, T_KILLED + 0.3);
// "His column fell back"
B.grey(["mk"], T_FELL, 0.5); go("mk", T_FELL + 0.1, 2.0, MPATH[1]); hideU(["mk"], T_FELL + 2.2);   // gone before it reaches the frame edge
const MBACK = arw({ pts: [[PDV[0] - 30, PDV[1] + 20], MPATH[2], MPATH[1]], side: "carth", t: T_FELL, dur: 1.0, width: AW(S7, 10), dash: "10 7", until: T_SAULT });
gsap.set(MBACK, { filter: "grayscale(1) brightness(1.15)" });
// Arnold's column along the waterfront to the barricade at Sault-au-Matelot
const AK = ["ak1", "ak2"].map((id, k) => unitS(id, "carth", APATH[1], "infantry", "", { t: T_NORTH + k * 0.15, w: 44, h: 29 }));
AK.forEach((id, k) => along(id, sub(APATH, 0.2, 1 - k * 0.1, 12).map(([x, y]) => [x - k * 6, y + 12 + k * 6]), T_ALED, T_SAULT - T_ALED, 12));
const AB2 = pbadge("BENEDICT ARNOLD", "", "arnold", "carth", "bl", "BA", T_ALED, T_REAR + 1.4);
const AF = faceMarker("arnold", "BA", "carth", ...APATH[1], T_ALED, T_REAR + 1.6, 44);
pinAlong(AF, sub(APATH, 0.2, 0.92, 12).map(([x, y]) => [x, y - 30]), T_ALED, T_SAULT - T_ALED, 12);
SFX("ref:whoosh", T_ALED);
const BARR = icon(ICO.barricade(), SAULT[0] + 6, SAULT[1] + 4, T_BARRI, null, { k: 1.6 });
const FS = front2([[SAULT[0] + 18, SAULT[1] - 14], [SAULT[0] + 8, SAULT[1] + 6], [SAULT[0] - 2, SAULT[1] + 24]], S7, T_BARRI + 0.1, { dur: 0.6, until: T_OVER + 0.6 });
const TSM = town("SAULT-AU-MATELOT", [SAULT[0] + 30, SAULT[1] - 40], "r", T_SAULT, { until: T_SAULT + LBL_LIFE });
// "A ball hit him in the leg, and he had to be helped to the rear"
hitAt(SAULT[0] - 10, SAULT[1] - 30, T_LEG + 0.15, { k: 2.2 }); K.shake(T_LEG + 0.2, 4, 0.3); pulse(T_LEG + 0.2);
badgeStamp(AB2, "WOUNDED", T_LEG + 0.4, { grey: false, size: 24 });
tl.to(AF.firstElementChild, { rotation: -30, filter: "brightness(0.75)", duration: 0.3 }, T_LEG + 0.2);
pinAlong(AF, [[SAULT[0] - 10, SAULT[1] - 30], [APATH[2][0], APATH[2][1] - 30], [APATH[1][0], APATH[1][1] - 30]], T_REAR, 1.6, 6);
// "His rifle captain, Daniel Morgan, took over and got over the barricade"
const MOB = pbadge("DANIEL MORGAN", "RIFLE CAPTAIN", "morgan", "carth", "tr", "DM", T_DM + 0.05, T_400 - 0.2);
const MOF = faceMarker("morgan", "DM", "carth", SAULT[0] - 30, SAULT[1] - 24, T_DM + 0.1, T_400, 44);
const OVERA = arw({ pts: [[SAULT[0] - 30, SAULT[1] - 2], [SAULT[0] + 4, SAULT[1] + 6], [SAULT[0] + 28, SAULT[1] + 36]], side: "carth", t: T_OVER, dur: 0.8, width: AW(S7, 11), until: T_STALL + 1.2 });
SFX("ref:whoosh", T_OVER); volley([SAULT[0] - 4, SAULT[1] + 2], [SAULT[0] + 12, SAULT[1] + 10], T_OVER + 0.5, 4, 1.0);
tl.to(BARR.querySelectorAll(".bc"), { attr: { stroke: "#1f4fc4" }, duration: 0.4 }, T_OVER + 0.8);
go("ak1", T_OVER + 0.3, 1.4, [SAULT[0] + 26, SAULT[1] + 40]); go("ak2", T_OVER + 0.5, 1.4, [SAULT[0] + 6, SAULT[1] + 22]);
pinAlong(MOF, [[SAULT[0] - 30, SAULT[1] - 24], [SAULT[0] + 30, SAULT[1] + 12]], T_OVER + 0.3, 1.4, 4);
// "But the attack stalled in the narrow streets, the powder was wet"
const STL = wstampL("STALLED", SAULT[0] + 70, SAULT[1] + 70, T_STALL + 0.05, null, "#e3232f", 24);
[0, 1].forEach((k) => tl.to(B.units["ak" + (k + 1)].el.firstElementChild, { x: 3, duration: 0.06, yoyo: true, repeat: 5 }, T_STALL + 0.2 + k * 0.1));
// "and British troops came out of a gate behind them": the Palace Gate sortie, the ring closes
const RS = ["rg1", "rg2"].map((id, k) => unitS(id, "rome", [PALACE[0] - 10, PALACE[1] + 10], "infantry", "", { t: T_GATE - 0.1 + k * 0.15, w: 44, h: 29 }));
go("rg1", T_GATE + 0.1, 2.2, [PALACE[0] + 30, PALACE[1] - 20]); go("rg2", T_GATE + 0.3, 2.2, [SAULT[0] - 30, SAULT[1] - 18]);
const SORT = arw({ pts: [[PALACE[0] - 5, PALACE[1] + 4], [PALACE[0] + 10, PALACE[1] - 18], [SAULT[0] - 40, SAULT[1] - 22]], side: "rome", t: T_GATE, dur: 1.0, width: AW(S7, 11), until: T_DEF });
SFX("ref:whoosh", T_GATE); K.target(PALACE[0], PALACE[1], T_BEHIND, { r: 22, side: "rome", until: T_400 });
const RING = front2([...Array(13)].map((_, k) => { const a = k / 12 * 6.2832; return [SAULT[0] + 12 + Math.cos(a) * 64, SAULT[1] + 18 + Math.sin(a) * 50]; }), S7, T_BEHIND + 0.6, { dur: 1.4, flip: true, until: T_HOSP + 0.4 });
// the casualty card (spoken numbers only, each on its words)
B.grey(["ak1", "ak2"], T_CAPT, 0.6);
const BARS = bars(SAULT[0] + 50, SAULT[1] + 30, T_CAPT + 0.1, T_HOSP + 0.4, 36);
// "About four hundred Americans were captured": on the map, by the prisoners' bars; the card only from "between thirty and sixty" (audit #22: short)
const CAPL = wstampL("~400 CAPTURED", SAULT[0] + 50, SAULT[1] + 78, T_400 + 0.6, T_3060 - 0.1, "#9fc0ea", 20);
const CAS_IN = T_3060 + 0.1, CAS_OUT = T_20 + 2.3;
const CAS = casCard([["ABOUT 400 CAPTURED", CAS_IN + 0.1], ["30–60 KILLED", T_3060 + 0.4]], [["FEWER THAN 20 LOST", T_20]], "QUEBEC · 31 DECEMBER 1775", CAS_IN, CAS_OUT, "right:60px;top:590px;display:flex;justify-content:flex-end;");   // over the river: clear of both flags and the ring
// =====================================================================================================================
// m1-8: grey dawn; the hospital; the blockade through the winter; result; the method
// =====================================================================================================================
const C8 = [1400, 880], S8 = 0.9;
camTo(T_HOSP - 0.2, 3.2, C8, S8, "sine.inOut");
hideU(["mk", "ak1", "ak2", "rg1", "rg2"], T_HOSP); tl.to([BH, BARR, MOF], { autoAlpha: 0, duration: 0.5 }, T_HOSP);
const GREY = document.createElement("div"); GREY.style.cssText = "position:absolute;inset:0;background:rgba(150,156,166,0.22);pointer-events:none"; document.getElementById("fx").appendChild(GREY);
gsap.set(GREY, { autoAlpha: 0 }); tl.to(GREY, { autoAlpha: 1, duration: 1.2 }, T_HOSP); tl.to(GREY, { autoAlpha: 0, duration: 2.0 }, T_FEW);
// the Union Flag on the walled city itself, the Continental Colours on the American-held country to the west (clear of the blockade line and the cards)
const F3 = [flagS(FL.gb, "", QUE[0] + 55, QUE[1] + 45, T_HOSP + 0.8, null), flagS(FL.us, "", 778, 647, T_HOSP + 0.8, null)];
const AB3 = pbadge("BENEDICT ARNOLD", "", "arnold", "carth", "bl", "BA", T_HOSP + 0.2, T_SHOWN);
const PISTOL = `<svg width="70" height="34" viewBox="0 0 70 34" style="display:inline-block;vertical-align:middle;margin-right:14px"><path d="M4 8 L50 8 L56 4 L62 6 L58 12 L30 12 L26 30 L14 30 L18 14 L4 14 Z" fill="#f3eee2" stroke="#c9b48a" stroke-width="1.5"/><path d="M28 12 Q30 20 36 16" fill="none" stroke="#c9b48a" stroke-width="2"/></svg>`;
const HOS_OUT = T_SWORD + 2.6;
const HOS = listCard(`${PISTOL}IN THE HOSPITAL`, [["PISTOLS LOADED", T_PIST + 0.1], ["A SWORD ON HIS BED", T_SWORD + 0.3]],
  "right:90px;top:240px;display:flex;justify-content:flex-end;", T_PIST - 0.05, HOS_OUT, { size: 52, mw: 600 });
// "They never came": its own short stamp (the hospital card has long gone)
const NEVER_OUT = T_NEVER + 2.4;
const NEV = sstamp("THEY NEVER CAME", 190, T_NEVER + 0.05, { size: 54, color: "#f7f3ea", until: NEVER_OUT });
// "With a few hundred men, he kept Quebec under siege for the rest of the winter"
const BU = [[1180, 1060], [1215, 900], [1250, 760], [1330, 640], [1790, 1010]].map((p, k) => unitS("b" + k, "carth", p, "infantry", "", { t: T_FEW + k * 0.12 }));
const BLOCK = front2([[1150, 1110], [1190, 980], [1225, 860], [1255, 760], [1300, 680], [1360, 625], [1430, 600]], S8, T_SIEGE - 0.1, { dur: 1.6, flip: true });
SFX("ref:whoosh", T_SIEGE);
dateRun([["JANUARY 1776", T_WINTER - 0.3, T_WINTER + 0.35], ["MARCH 1776", T_WINTER + 0.4, T_WINTER + 1.05], ["MAY 1776", T_WINTER + 1.1, null]], 30);
for (let k = 0; k < 3; k++) SFX("tick", T_WINTER - 0.3 + k * 0.7);
// "The city had not fallen": the result card
const RES = resultCard("RESULT", "QUEBEC HELD", "THE MARCH · ~350 MILES", T_NOTF - 0.05, T_SHOWN + 0.9, { size: 80, top: 640 });
// the method: move 1 lights ONLY line 1, on its spoken words (lines 2 and 3 stay dim bars for moves 2 and 3)
const MCD = GG.method(1, T_HOW - 0.1, END + 1, [T_GO]); MCD.querySelectorAll(".row").forEach((r) => { r.style.fontSize = "48px"; }); MCD.style.top = "600px";
SFX("ref:pop", T_GO); SFX("ref:boom", T_GO + 0.4);
// the HUD steps out while a big card is up (1c); the date scroll stays
declutter([LGD, AB, MB, AB2, MOB, AB3], [[T_600 - 0.1, T_STL - 0.2], [T_350 + 0.1, MARCH_OUT], [T_35 - 0.05, N35_OUT], [T_EOY - 0.05, T_STORM + 0.6], [SLIP_IN, SLIP_OUT],
  [CAS_IN, CAS_OUT], [T_PIST - 0.05, HOS_OUT], [T_NEVER + 0.05, NEVER_OUT], [T_NOTF - 0.05, END + 1]]);
fixImgs();
B.finish();
