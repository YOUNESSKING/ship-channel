// M3A (m3-1 .. m3-3), Benedict Arnold #17: September 1777, Bemis Heights, Freeman's Farm (19 Sep), the quarrel. Map agent ar3_.
// Built with: python3 tools/ar3_make_control.py hudson && python3 tools/ar3_inline.py m3a m3-1 m3-3
// World = saratoga map px (z15); `hudson` (z10) as a world group at its true place + scale for the opening wide shot (option 1, half
// strength); ONE continuous dive into `saratoga` with the colours dissolving (~2.8 s); the battle = option 2 (two glowing fronts).
// m3-1: title card MOVE 3 · THE OPEN BACK DOOR · 1777; SEPTEMBER 1777; Burgoyne's army on the Hudson (badge on his name); ~25 MILES to
//   ALBANY; Gates's army dug in on BEMIS HEIGHTS (badge); the bluffs + the river road; the dive; the British go round through the woods to the
//   west; 19 SEPTEMBER; FREEMAN'S FARM; the two armies meet.
// m3-2: Arnold's badge (the American left); out of the earthworks into the woods; Morgan's riflemen (badge on his name) then waves; dusk:
//   the Germans arrive from the river side; the British keep the clearing; casualty card NEARLY 600 vs 320; STUCK.
// m3-3: the camp: Gates and Arnold face each other; Morgan's counter slides to Gates's HQ; the shouting match; the verbatim quote card;
//   A PASS; he stays; his command lines fade on "no command at all".
// Facts: FACT_NOTES + FACTCHECK_C (NPS numbers; Morgan to HQ 22 Sep; Arnold's 22 Sep letter quoted verbatim).
// @@KIT
const P1 = "m3-1", P2 = "m3-2", P3 = "m3-3";
const T_SEP = at(P1, "By September"), T_BARMY = at(P1, "Burgoyne's army"), T_HUD = at(P1, "on the Hudson"), T_25 = at(P1, "twenty-five"), T_ALB = at(P1, "Albany"),
  T_GATES = at(P1, "Gates's army"), T_DUG = at(P1, "dug in"), T_BEMIS = at(P1, "Bemis Heights"), T_BLUFF = at(P1, "line of bluffs"), T_ROAD = at(P1, "river road"),
  T_AROUND = at(P1, "went around"), T_WEST = at(P1, "to the west"), T_19 = at(P1, "On the nineteenth"), T_CLEAR = at(P1, "a clearing"), T_FF = at(P1, "Freeman's Farm"),
  T_MET = at(P1, "two armies met");
const T_ARN = at(P2, "Arnold commanded"), T_LEFT = at(P2, "American left"), T_PUSH = at(P2, "He pushed"), T_WOODS = at(P2, "in the woods"),
  T_EARTH = at(P2, "behind the earthworks"), T_MORG = at(P2, "Daniel Morgan"), T_REG = at(P2, "regiment after regiment"), T_WAVES = at(P2, "in waves"),
  T_DUSK = at(P2, "At dusk"), T_GER = at(P2, "German reinforcements"), T_KEPT = at(P2, "kept the clearing"), T_LOST = at(P2, "lost nearly"),
  T_320 = at(P2, "three hundred and"), T_STUCK = at(P2, "they were stuck");
const T_TURN = at(P3, "turned on each"), T_TOOK = at(P3, "Gates took"), T_MR = at(P3, "Morgan's riflemen"), T_ACMD = at(P3, "of Arnold's command"),
  T_SHOUT = at(P3, "shouting match"), T_WROTE = at(P3, "wrote to Gates"), T_Q = at(P3, "did not know"), T_QEND = at(P3, "in the army."),
  T_PASS = at(P3, "a pass"), T_GOT = at(P3, "He got it"), T_STAY = at(P3, "then he stayed"), T_NEXT = at(P3, "When the next"), T_NOC = at(P3, "no command at all");
// =====================================================================================================================
// THE WORLD: hudson (wide, option 1 half strength) + saratoga (feathered) on one camera
// =====================================================================================================================
const HUD = mapGroup("hudson", 0); const HUD_C = terrImg("assets/media/ar3_ctl_hudson_1777.png", HUD, 0, null, 0.01);
const SAR = baseGroup(4); FADES.push([SAR, 0.1, 0.22]);
hudRiver();
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); const NA = LV.north(); NA.style.top = "330px";
// ---------- places (world = saratoga px) ----------
const ALB = LD(42.65, -73.75), FTE = LD(43.267, -73.585), SARV = LD(43.10, -73.588), BEM = [1790, 1288], FF = [1324, 714];
const HROAD = [FTE, LD(43.18, -73.575), SARV, LD(43.05, -73.60), [2250, 450]];
const AMLINE = [[1300, 1185], [1420, 1195], [1560, 1215], [1700, 1250], [1830, 1290]];
const RROAD = [[1600, 1560], [1720, 1330], [1880, 1050], [2060, 760], [2230, 480], [2330, 200]];
const BLUFF = [[1640, 1400], [1740, 1250], [1850, 1120], [1950, 980]];
// =====================================================================================================================
// m3-1: the Hudson (wide), Bemis Heights, the dive, round through the woods, Freeman's Farm
// =====================================================================================================================
const CW = [(ALB[0] + FTE[0]) / 2 + 600, (ALB[1] + FTE[1]) / 2 - 800], SW = 0.05;
camSet(CW, SW);
camTo(0, T_BLUFF - 0.6, [CW[0] + 300, CW[1] - 700], SW * 1.12, "sine.inOut");
const TTL = B.title("MOVE 3", "SARATOGA", "1777", 0.25, T_BARMY + 1.0);
SFX("ref:boom", 0.4);
B.showDate(T_SEP); dateSet("SEPTEMBER 1777", T_SEP + 0.05, T_19 - 0.05);
// flags inside the frame on their own ground (Union Flag beside Burgoyne's corridor, clear of the badge); they cross-fade with the close flags during the dive
const F1 = [flagS(FL.gb, "", ...LD(43.17, -73.48), 0.2, null), flagS(FL.us, "", ...LD(42.80, -73.40), 0.2, null)]; fadeS(F1, 0.12, 0.25, true);
// Burgoyne's army on the Hudson (red counters coming down the river road), his badge on his name
const RA = [0, 1, 2].map((k) => unitS("ra" + k, "rome", posOn(HROAD, 0.04 + k * 0.12), "infantry", "", { t: 0.3 + k * 0.1 }));
RA.forEach((id, k) => along(id, sub(HROAD, 0.04 + k * 0.12, 0.5 + k * 0.12, 10), 0.4, T_BLUFF - 0.5, 10));
arw({ pts: sub(HROAD, 0, 0.75, 8), side: "rome", t: T_HUD - 0.1, dur: 1.3, width: AW(SW, 12), until: T_BLUFF });
const BB = pbadge("JOHN BURGOYNE", "", "burgoyne", "rome", "tr", "JB", T_BARMY + 1.1, T_AROUND + 2.5);
// "about twenty-five miles above Albany": a dashed measure to ALBANY
const ALBT = town("ALBANY", ALB, "r", T_ALB - 0.05, { until: T_ALB + LBL_LIFE });
glowPath([[BEM[0], BEM[1] + 300], [ALB[0] + 200, ALB[1] - 300]], "#f3eee2", 3 / SW, T_25 - 0.1, T_ALB + 3.0, 0, 0.9, { dash: `${12 / SW} ${10 / SW}` });
tagL("~25 MILES", (BEM[0] + ALB[0]) / 2 + 1400, (BEM[1] + ALB[1]) / 2, T_25 + 0.1, null, 14);
// "Gates's army was dug in on Bemis Heights": the American line, Gates's badge, the label
const GB = pbadge("HORATIO GATES", "", "gates", "carth", "bl", "HG", T_GATES + 0.05, T_19);
const AU = [unitS("a1", "carth", [1380, 1170], "infantry", "", { t: T_GATES }), unitS("a2", "carth", [1560, 1200], "infantry", "", { t: T_GATES + 0.1 }),
  unitS("a3", "carth", [1720, 1240], "infantry", "", { t: T_GATES + 0.2 })];
const AL = glowPath(AMLINE, "#2c57b7", 4, T_DUG - 0.1, null, 0, 0.75, { draw: 1.0 });
const BMT = town("BEMIS HEIGHTS", BEM, "r", T_BEMIS - 0.05, { until: T_BEMIS + LBL_LIFE });
// ---------- the dive (whoosh) into the saratoga map; the colours dissolve ----------
const TZ0 = T_BLUFF - 0.5, TZ1 = T_ROAD + 0.6, CS = [1560, 1000], SS = 0.95;
SFX("ref:whoosh", TZ0 - 0.05);   // quiet dive (the locked whoosh is kept for the hook dive + the big zoom-out)
zoom(TZ0, TZ1 - TZ0, [CW[0] + 300, CW[1] - 700], SW * 1.12, CS, SS, BEM, "power2.inOut");
tl.to(HUD_C, { autoAlpha: 0, duration: 2.8, ease: "sine.inOut" }, TZ0 + 0.2);
glowPath(BLUFF, "#ffd54a", 6 / SS, T_BLUFF + 0.4, T_AROUND + 1.0, 2, 0.85, { draw: 0.8, top: true });
glowPath(RROAD, "#e8d9b0", 5 / SS, T_ROAD, T_AROUND + 2.0, 1, 0.85, { draw: 0.9 });
tagL("RIVER ROAD", 2010, 900, T_ROAD + 0.1, null, 14);
// mid-dive flags (between the wide flags and the close flags)
const FMID = [flagS(FL.gb, "", BEM[0] - 700, BEM[1] - 2700, null, null), flagS(FL.us, "", BEM[0] + 900, BEM[1] + 700, null, null)]; gsap.set(FMID, { autoAlpha: 1 });
SCALEFIX.push((s) => { const v = ramp(s, 0.07, 0.1) * (1 - ramp(s, 0.28, 0.42)); FMID.forEach((g) => { g.style.filter = `opacity(${v.toFixed(3)})`; }); });
const F2 = [flagS(FL.us, "", 1560, 1380, 0.2, T_19 + 0.3), flagS(FL.gb, "", 1150, 700, 0.2, T_19 + 0.3)]; fadeS(F2, 0.2, 0.38);
// "So Burgoyne went around, through the woods to the west": red columns swing west, then south
const RC = { rw: [[2080, 560], [1800, 430], [1500, 430], [1330, 560], [1300, 650]], rc: [[2080, 600], [1850, 560], [1600, 600], [1420, 680]], re: [[2150, 640], [2050, 760], [1950, 820]] };
Object.entries(RC).forEach(([id, pts], k) => { unitS(id, "rome", pts[0], "infantry", "", { t: T_AROUND - 0.4 + k * 0.1 }); along(id, pts, T_AROUND + k * 0.15, T_CLEAR - T_AROUND, 14);
  arw({ pts, side: "rome", t: T_AROUND + k * 0.15, dur: 1.6, width: AW(SS, 12), until: T_MET + 0.5 }); });
tagL("WOODS", 1520, 360, T_WEST, null, 14);
hideU(RA, TZ0 + 1.0);
// "On the nineteenth, at a clearing called Freeman's Farm, the two armies met"
dateSet("19 SEPTEMBER 1777", T_19, T_TURN - 0.05); dateSet("SEPTEMBER 1777", T_TURN, null);
camTo(T_19 - 0.4, 2.6, [1360, 880], 1.45, "sine.inOut");
const CLR = GG.pin(`<div style="width:150px;height:110px;border-radius:50%;background:radial-gradient(ellipse, rgba(232,200,90,0.35), rgba(232,200,90,0.12) 60%, rgba(232,200,90,0) 72%);border:2px dashed rgba(232,200,90,0.8)"></div>`, ...FF, { t: T_CLEAR, until: T_TURN });
tagL("FREEMAN'S FARM", FF[0] - 100, FF[1] - 90, T_FF, null, 16);
go("a1", T_CLEAR, 2.4, [1280, 900]); go("a2", T_CLEAR + 0.1, 2.4, [1380, 930]);
[[T_MET + 0.1, [1290, 780], [1360, 790]]].forEach(([t, a, b]) => { volley(a, b, t, 6, 1.0); smokeLine(a, b, t + 0.05, 4, 26); });
// =====================================================================================================================
// m3-2: Arnold on the American left; into the woods; Morgan then the waves; the Germans at dusk; the losses; stuck
// =====================================================================================================================
const C2 = [1345, 930], S2 = 1.6;
camTo(T_ARN - 0.4, 2.0, C2, S2, "sine.inOut");
const F3 = [flagS(FL.us, "", 1500, 1080, T_19 - 0.3, T_TURN), flagS(FL.gb, "", 1520, 690, T_19 - 0.3, T_TURN)];
const LGD = legend(T_ARN + 1.0, null, true);
const AB = pbadge("BENEDICT ARNOLD", "THE AMERICAN LEFT", "arnold", "carth", "bl", "BA", T_ARN + 0.05, T_TURN);
const AM = faceMarker("arnold", "BA", "carth", 1250, 1010, T_LEFT - 0.1, null, 72);
// the clearing held by the British (red), the front (option 2)
go("rw", T_ARN, 1.6, [1290, 700]); go("rc", T_ARN, 1.6, [1340, 690]); go("re", T_ARN, 1.6, [1395, 715]);
const FRP = [[1220, 780], [1280, 770], [1340, 772], [1400, 785], [1450, 800]];
const FR = front2(FRP, S2, T_ARN + 0.4, { dur: 1.2, until: T_TURN - 0.2, to: FRP.map(([x, y]) => [x, y + 8]), moveT: T_KEPT, moveDur: 1.5 });
// "He pushed Gates to fight in the woods, instead of waiting behind the earthworks"
glowPath(AMLINE.slice(0, 3), "#8fb2ff", 7 / S2, T_EARTH - 0.1, T_EARTH + 2.2, 1, 0.9, { top: true });
tagL("EARTHWORKS", 1330, 1150, T_EARTH, null, 14);
arw({ pts: [[1300, 1080], [1290, 960], [1300, 860]], side: "carth", t: T_WOODS - 0.1, dur: 1.0, width: AW(S2, 12), until: T_MORG });
// "he sent in Daniel Morgan's riflemen": one counter, MORGAN badge after the name
const MB = pbadge("DANIEL MORGAN", "RIFLEMEN", "morgan", "carth", "tr", "DM", T_MORG + 0.1, T_REG + 1.0);
unitS("mo", "carth", [1240, 960], "infantry", "MORGAN", { t: T_MORG, tag: 15 });
go("mo", T_MORG + 0.1, 1.6, [1270, 815]);
arw({ pts: [[1240, 950], [1255, 880], [1270, 830]], side: "carth", t: T_MORG + 0.1, dur: 0.9, width: AW(S2, 11), until: T_REG + 0.3 });
volley([1250, 800], [1300, 795], T_MORG + 1.2, 5, 1.0);
// "and then regiment after regiment, in waves, all afternoon": three waves, one after another
const WV = [[1330, 1000], [1400, 1010], [1200, 1000]];
WV.forEach((p, k) => { const t = T_REG - 0.2 + k * 0.9; const id = unitS("w" + k, "carth", [p[0], p[1] + 60], "infantry", "", { t });
  go(id, t + 0.1, 1.4, [p[0] - 10, 820]); arw({ pts: [[p[0], p[1] + 40], [p[0] - 5, 900], [p[0] - 10, 835]], side: "carth", t: t + 0.05, dur: 0.8, width: AW(S2, 11), until: t + 2.4 });
  volley([p[0] - 30, 800], [p[0] + 20, 798], t + 1.3, 5, 1.0); smokeLine([p[0] - 30, 790], [p[0] + 20, 788], t + 1.35, 3, 24); });
// "At dusk German reinforcements arrived": dusk light, a red column from the river side
const DUSK = nightWash(T_DUSK - 0.1, null, 0.22);
const GER = unitS("ge", "rome", [1700, 700], "infantry", "GERMANS", { t: T_GER - 0.2, tag: 14 });
go("ge", T_GER, 2.2, [1450, 740]); arw({ pts: [[1720, 690], [1580, 720], [1460, 745]], side: "rome", t: T_GER, dur: 1.2, width: AW(S2, 12), until: T_LOST });
volley([1420, 780], [1460, 790], T_GER + 1.6, 5, 1.0);
// "the British kept the clearing": the waves pull back a little
["w0", "w1", "w2", "mo"].forEach((id, k) => go(id, T_KEPT + k * 0.08, 1.4, [[1320, 880], [1390, 890], [1190, 880], [1260, 870]][k]));
// "But they had lost nearly six hundred men, against three hundred and twenty Americans"
const CAS = casualties([["", "320", "NEARLY 600"]], "19 SEPTEMBER 1777 · MEN LOST", T_LOST - 0.1, T_STUCK - 0.2, 240);
const STK = wstampL("STUCK", FF[0] + 170, FF[1] + 10, T_STUCK, null, "#e3232f", 30);
// =====================================================================================================================
// m3-3: the quarrel in the American camp
// =====================================================================================================================
const HQ = [1745, 1320], C3 = [1560, 1200], S3 = 1.7;
camTo(T_TURN - 1.0, 2.2, C3, S3, "sine.inOut");
tl.to(DUSK, { autoAlpha: 0, duration: 1.2 }, T_TURN - 1.0);
const F4 = [flagS(FL.us, "", 1250, 1330, T_TURN - 0.4, null), flagS(FL.gb, "", 1680, 1010, T_TURN - 0.4, null)];
// the armies back in their lines; Arnold's division on the left with Morgan, Gates's HQ on the right
hideU(["rw", "rc", "re", "ge", "w0", "w1", "w2"], T_TURN - 0.9);
const RW = [unitS("b1", "rome", [1330, 740], "infantry", "", { t: T_TURN - 0.4 }), unitS("b2", "rome", [1460, 720], "infantry", "", { t: T_TURN - 0.3 })];
go("a1", T_TURN - 0.8, 1.2, [1330, 1180]); go("a2", T_TURN - 0.8, 1.2, [1430, 1195]); go("a3", T_TURN - 0.8, 1.2, [1650, 1240]);
go("mo", T_TURN - 0.8, 1.4, [1380, 1120]);
tl.to(AM, { left: 1400, top: 1250, duration: 1.2, ease: "sine.inOut" }, T_TURN - 0.8);
const GM = faceMarker("gates", "HG", "carth", ...HQ, T_TURN - 0.1, null, 76);
const AB2 = pbadge("BENEDICT ARNOLD", "", "arnold", "carth", "bl", "BA", T_TURN, null);
const GB2 = pbadge("HORATIO GATES", "", "gates", "carth", "tr", "HG", T_TURN + 0.1, null);
SFX("ref:pop", T_TURN);
// Arnold's command lines (dashed blue) to his regiments and to Morgan
const CMD = [[1330, 1180], [1430, 1195], [1380, 1120]].map((p, k) => glowPath([[1400, 1250], p], "#8fb2ff", 4.5 / S3, T_TURN + 0.3 + k * 0.1, k === 2 ? T_MR + 0.3 : T_NOC, 0, 0.9, { dash: "5 4", top: true }));
const CRACK = glowPath([[1440, 1255], [1520, 1300], [1560, 1270], [1610, 1320], [1660, 1300], [HQ[0] - 40, HQ[1]]], "#ff3b30", 4 / S3, T_TURN + 0.4, T_WROTE, 2, 1, { draw: 0.5, top: true });
SFX("hit", T_TURN + 0.5); K.shake(T_TURN + 0.5, 2, 0.2);
// "Gates took Morgan's riflemen out of Arnold's command": Morgan's counter slides to Gates's HQ, a new command line to Gates
go("mo", T_MR, 2.2, [HQ[0] - 60, HQ[1] - 50]);
glowPath([[HQ[0], HQ[1]], [HQ[0] - 60, HQ[1] - 50]], "#8fb2ff", 4.5 / S3, T_ACMD + 0.4, null, 0, 0.9, { dash: "5 4", top: true });
// "The two men had a shouting match": the crack flares, both markers shake
tl.to(CRACK, { opacity: 1, strokeWidth: 7 / S3, duration: 0.2, yoyo: true, repeat: 3 }, T_SHOUT - 0.1);
[AM, GM].forEach((m, k) => tl.to(m.firstElementChild, { x: 3, duration: 0.06, yoyo: true, repeat: 7 }, T_SHOUT + k * 0.1)); SFX("hit", T_SHOUT + 0.1); K.shake(T_SHOUT + 0.1, 3, 0.25);
// the verbatim quote card (small): Arnold's letter quoting Gates
const QC = quote("&ldquo;did not know I was a Major-general or had any command in the army.&rdquo;", "ARNOLD'S LETTER TO GATES", T_Q - 0.15, T_QEND + 1.0, { size: 40, top: 200, mw: 1200 });
SFX("ref:pop", T_Q - 0.1);
// "Arnold asked for a pass to leave the army. He got it, and then he stayed."
const PASS = wstampL("A PASS", 1400, 1330, T_PASS, null, "#f7f3ea", 24);
tl.to(AM, { left: 1300, top: 1360, duration: 0.9, ease: "sine.inOut" }, T_GOT - 0.2); tl.to(AM, { left: 1400, top: 1250, duration: 0.8, ease: "sine.inOut" }, T_STAY);
SFX("ref:pop", T_STAY + 0.1);
// "When the next battle came, he had no command at all": his command lines fade, NO COMMAND
tl.to(AM.firstElementChild, { filter: "grayscale(1) brightness(0.7)", duration: 0.5 }, T_NOC);
wstampL("NO COMMAND", 1400, 1330, T_NOC - 0.05, null, "#e3232f", 26);
// HUD steps out under the big cards (1c); the date scroll stays
declutter([LGD, BB, GB, AB, MB, AB2, GB2], [[T_LOST - 0.1, T_STUCK - 0.2], [T_Q - 0.15, T_QEND + 1.0]]);
fixImgs();
K.raiseTerritory();
B.finish();
