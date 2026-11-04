// MOVE 2a (move1-sub, m2-1, m2-2), Arnold #17: Lake Champlain, summer - October 1776. Map agent "va". Basemap champlain_hd_lift (z9, 218 m/px).
//   python3 tools/va_inline.py m2a champlain_hd_lift move1-sub m2-2
// move1-sub  option 1 (half strength): the Americans pull back south out of Canada (blue arrows down the lake); red ship counters gather at
//            St. Johns on "building a fleet"; Arnold badge (initials until arnold_head.png exists) on "Arnold had no navy"; E.subscribe on the
//            subscribing clause; NEXT: MOVE 2 on "Here's how".
// m2-1       title MOVE 2 · THE FLEET FROM A FOREST · 1776; push in on St. Johns: red ships multiply; the Inflexible taken apart, carried past the
//            Chambly rapids in pieces and put back together (INFLEXIBLE · 18 GUNS); card 28 DAYS; a red arrow down the lake to Ticonderoga and on
//            toward the Hudson; New England glows on "cut New England off".
// m2-2       Skenesborough: blue boats appear one by one (gondolas, galleys); card 15 VESSELS · ABOUT 700 MEN; red card ABOUT 25 ARMED VESSELS ·
//            ABOUT 700 SEAMEN; red troop boats behind them (MORE THAN 1,000 SOLDIERS IN BOATS); the camera ends on Valcour (hand-off to m2b).
// Facts: FACT_NOTES move 2, FACTCHECK_B (Inflexible 18 guns, 28 days keel to sailing, 15 vs ~25, ~700 each, "Upwards of One thousand Men in Batteaus").
// @@KIT
// @@DATA
const CZ = GD.maps.champlain;
const L = GG.proj(9, CZ.origin_world_px[0], CZ.origin_world_px[1]);
const LL = (pts) => pts.map(([la, lo]) => L(la, lo));
const PS = "move1-sub", P1 = "m2-1", P2 = "m2-2";
const T_OUT = at(PS, "driven out of Canada"), T_FLEET = at(PS, "building a fleet"), T_NONAVY = at(PS, "Arnold had no navy"), T_HOW = at(PS, "So how do you stop"),
  T_FOREST = at(PS, "a forest"), T_KIND = at(PS, "That's the kind"), T_SUBS = at(PS, "subscribing"), T_HERE = at(PS, "Here's how");
const T_P1 = B.T.paras[P1][0], T_SUM = at(P1, "summer of"), T_NORTH = at(P1, "north end"), T_WAR = at(P1, "building warships"), T_APART = at(P1, "took one ship apart"),
  T_RAP = at(P1, "past the rapids"), T_BACK = at(P1, "put her back together"), T_INF = at(P1, "Inflexible"), T_18 = at(P1, "eighteen guns"), T_28 = at(P1, "twenty-eight days"),
  T_ROAD = at(P1, "The lake was the road"), T_TIC = at(P1, "Fort Ticonderoga"), T_HUD = at(P1, "the Hudson"), T_WHO = at(P1, "Whoever held it"), T_NE = at(P1, "cut New England off");
const T_P2 = B.T.paras[P2][0], T_SKE = at(P2, "Skenesborough"), T_TREES = at(P2, "fresh-cut trees"), T_GOND = at(P2, "flat-bottomed gondolas"), T_GAL = at(P2, "galleys"),
  T_OCT = at(P2, "By October"), T_15 = at(P2, "fifteen vessels"), T_700 = at(P2, "seven hundred men"), T_NEVER = at(P2, "never fired"), T_AGAINST = at(P2, "Coming against"),
  T_25 = at(P2, "twenty-five armed"), T_SEA = at(P2, "seven hundred seamen"), T_1000 = at(P2, "more than a thousand"), T_BOARD = at(P2, "ready to board");
// ---------- places (champlain z9 px) ----------
const STJ = L(45.30, -73.26), CHA = L(45.45, -73.28), IAN = L(45.12, -73.29), VAL = L(44.61, -73.43), CRP = L(44.027, -73.424), TIC = L(43.843, -73.387),
  SKE = L(43.555, -73.404), FTE = L(43.27, -73.58), MTL = L(45.50, -73.57);
// the lake (approx.), north to south, and on to the Hudson
const LKP = LL([[45.30, -73.26], [45.12, -73.29], [45.0, -73.35], [44.85, -73.35], [44.69, -73.39], [44.61, -73.43], [44.45, -73.33], [44.27, -73.32], [44.12, -73.39],
  [44.03, -73.42], [43.85, -73.39], [43.70, -73.40], [43.555, -73.404]]);
const HUD = LL([[43.555, -73.404], [43.40, -73.48], [43.27, -73.58], [43.05, -73.58], [42.75, -73.70]]);
// ---------- layers ----------
living(CZ.meters_per_px, [], { n: 6, clouds: 0.12 });
const TC = terr0("assets/media/va_champlain_ctl_soft.png"); TC.style.filter = SOFT;   // audit #35: feathered wavy border, cooler red, lower alpha
const BY = L(45.02, -73.3)[1];
const FR = front2([[1180, BY + 14], [1260, BY + 4], [1340, BY + 10], [1420, BY - 2], [1500, BY + 6], [1580, BY - 4], [1660, BY + 8], [1740, BY + 2]], 2.0, 0.0, { dur: 0.01 });
on0(FR);
// ---------- camera ----------
const sKeys = [[0, 1430, 830, 0.95], [T_FLEET - 0.5, 1470, 790, 1.0], [T_P1 - 0.4, 1450, 720, 1.12], [T_P1 + 2.6, 1450, 700, 1.2], [T_WAR, 1450, 455, 2.1, "power2.inOut"], [T_BACK + 0.5, 1452, 440, 2.2],
  [T_ROAD, 1450, 430, 2.1], [T_HUD + 0.5, 1430, 900, 0.9, "power2.inOut"], [T_P2 - 0.2, 1480, 900, 0.85], [T_GAL + 1.0, 1440, 930, 0.9], [T_AGAINST, 1440, 880, 0.88],
  [END, 1430, 830, 0.95]]   // audit #15/#16: Canada stays in frame (the Union Flag on its own ground);
camera(sKeys);
// ---------- HUD ----------
B.showDate(0); B.date("SUMMER 1776", 0.0, T_OCT - 0.1, 32); date0(); B.date("OCTOBER 1776", T_OCT, END + 1, 32);
const LGD = legend(0.8, END + 1);
// flags (both on every frame): Union Flag on Canada, Continental Colours on the American shore (two pairs: wide, and the St. Johns close-up)
// audit #11-#16 (2026-11-03): ONE flag each for the whole scene, both on their own land and in frame at every camera position (checked with tools/va_probe.js):
// Union Flag on Canada east of the Richelieu (lat ~45.2), clear of the legend and the corner badge; Continental Colours on northern Vermont
flagS(FL.cs, "", 1750, 515, 0, END + 1); flagS(FL.us, "", 1640, 640, 0, END + 1);
// big towns (small labels, leave after ~3.5 s)
townL("ST. JOHNS", STJ, "r", T_NORTH); townL("TICONDEROGA", TIC, "r", T_TIC); townL("SKENESBOROUGH", SKE, "r", T_SKE);
// =================== move1-sub: out of Canada; the British fleet at St. Johns; the subscribe beat ===================
unitS("am1", "carth", L(45.25, -73.32), "infantry", "", { size: "XX", t: 0 }); unitS("am2", "carth", L(45.08, -73.40), "infantry", "", { size: "XX", t: 0 });
["am1", "am2"].forEach((id) => gsap.set(B.units[id].el, { autoAlpha: 1 })); B.hideUnits(["am1", "am2"], T_P2 - 0.5, 0.6);
along("am1", LL([[45.25, -73.32], [44.9, -73.42], [44.4, -73.42], [44.05, -73.50]]), 0, 9.0, 16); along("am2", LL([[45.08, -73.40], [44.7, -73.50], [44.2, -73.50], [43.90, -73.48]]), 0, 9.5, 16);
arw({ pts: LL([[45.28, -73.22], [44.9, -73.30], [44.4, -73.30], [44.1, -73.36]]), side: "carth", t: 0.3, dur: 4.0, width: AW(0.95, 13), until: T_HOW });
arw({ pts: LL([[45.45, -73.42], [45.0, -73.50], [44.5, -73.55], [44.15, -73.55]]), side: "carth", t: T_OUT - 0.2, dur: 4.0, width: AW(0.95, 13), until: T_HOW });
// the British fleet gathers at St. Johns (frame of the whole lake)
const RF = [[45.31, -73.25, "schooner"], [45.27, -73.25, "gunboat2"], [45.24, -73.27, "gunboat2"], [45.20, -73.27, "schooner"], [45.17, -73.28, "gunboat2"], [45.14, -73.29, "gondola"]];
const RFS = RF.map(([la, lo, kind], k) => ship(kind, [L(la, lo)], T_FLEET + k * 0.35, 0.01, null, { side: "rome", s: 20, rot: 90 }));
const AB = cmd("arnold", "BENEDICT ARNOLD", "NO NAVY", "carth", "tr", T_NONAVY + 0.1, T_KIND - 0.2);
E.subscribe(T_SUBS - 1.1, T_HERE - 0.3);
const NX = scr(`<div style="padding:10px 26px 12px;background:rgba(18,16,12,0.9);border-left:6px solid #c9b48a;font-family:Oswald;font-weight:700;color:#f7f3ea;font-size:30px;letter-spacing:.14em">NEXT: <span style="color:#c9b48a">MOVE 2</span></div>`,
  "left:90px;bottom:150px;", T_HERE + 0.1, T_P1 - 0.2, { autoAlpha: 0, x: -60 });
// =================== m2-1: the fleet from St. Johns; the Inflexible in pieces; 28 days; the road south ===================
const TT2 = B.title("MOVE 2", "THE FLEET FROM A FOREST", "1776", T_P1 + 0.1, T_P1 + 2.9); TT2.style.top = "600px";   // below both flags SFX("ref:boom", T_P1 + 0.2);
// more warships appear on "building warships"
const RF2 = [[45.285, -73.235, "gunboat2"], [45.255, -73.29, "gunboat2"], [45.225, -73.24, "gunboat2"], [45.19, -73.30, "gunboat2"], [45.29, -73.29, "gondola"]];
RF2.forEach(([la, lo, kind], k) => ship(kind, [L(la, lo)], T_WAR + 0.2 + k * 0.3, 0.01, null, { side: "rome", s: 20, rot: 90 }));
boxL("WARSHIPS", STJ[0] + 46, STJ[1] + 20, T_WAR + 0.4, null, { size: 10, bg: "#f3d6c8" });
// the Inflexible: taken apart at Chambly, carried past the rapids in pieces, put back together at St. Johns
const RAPIDS = LL([[45.45, -73.28], [45.40, -73.27], [45.35, -73.265], [45.31, -73.26]]);
boxL("RAPIDS", CHA[0] + 30, CHA[1] - 6, T_RAP, null, { size: 10 });
const PIECE = (k) => pinS(GG.pin(`<svg width="18" height="8" viewBox="0 0 18 8" style="display:block;filter:drop-shadow(0 0 3px #ff7a6a)"><rect x="0.5" y="0.5" width="17" height="7" fill="#b9935f" stroke="#c4121f" stroke-width="1.2"/></svg>`, CHA[0], CHA[1], {}));
const shipA = ship("ship", [CHA], T_APART - 0.4, 0.01, T_APART + 0.6, { side: "rome", s: 26, rot: 90 });
[0, 1, 2, 3, 4].forEach((k) => { const el = PIECE(k), q = RAPIDS.map(([x, y]) => [x + (k - 2) * 6, y + (k % 2) * 4]);
  gsap.set(el, { left: q[0][0], top: q[0][1] }); tl.set(el, { autoAlpha: 1 }, T_APART + 0.4); pinAlong(el, q, T_RAP - 0.3 + k * 0.25, T_BACK - T_RAP - 0.2, 12);
  tl.to(el, { left: STJ[0] + 18, top: STJ[1] + 10, duration: 0.5 }, T_BACK + 0.1 + k * 0.12); tl.to(el, { autoAlpha: 0, duration: 0.2 }, T_BACK + 0.6 + k * 0.12); });
const INF = ship("ship", [[STJ[0] + 18, STJ[1] + 10]], T_BACK + 0.8, 0.01, null, { side: "rome", s: 32, rot: 90 });
tl.fromTo(INF.sv, { scale: 0.3 }, { scale: 1, duration: 0.6, ease: "back.out(2)", immediateRender: false }, T_BACK + 0.8); SFX("hit", T_BACK + 1.2);
boxL("INFLEXIBLE · 18 GUNS", STJ[0] + 60, STJ[1] + 46, T_18, null, { size: 12, bg: "#f3d6c8" });
const C28 = placeCard("SAILED AFTER HER KEEL WAS LAID", "28 DAYS", "left:0;right:0;top:200px;display:flex;justify-content:center;", T_28 - 0.05, T_ROAD - 0.3);
SFX("hit", T_28 + 0.1);
// the road south: down the lake to Ticonderoga and on toward the Hudson
glowPath(LKP, "#ff6a5a", 6, T_ROAD - 0.1, T_NE + 3.0, 2, 0.75, { draw: 2.0 });
arw({ pts: [...LKP.slice(2), ...HUD.slice(1)], side: "rome", t: T_TIC - 0.4, dur: 2.6, width: AW(0.9, 15), until: T_P2 + 1.0 });
boxL("HUDSON", HUD[3][0] - 150, HUD[3][1], T_HUD + 0.1, null, { size: 14 });
// New England glows on "cut New England off"
const NEG = GG.layer(`background:radial-gradient(ellipse 22% 30% at ${(L(43.6, -71.7)[0] / 28.8).toFixed(1)}% ${(L(43.6, -71.7)[1] / 16.2).toFixed(1)}%, rgba(130,180,255,0.75), rgba(130,180,255,0) 72%);mix-blend-mode:screen;`, T_NE - 0.1, T_P2 + 1.5, { dur: 0.8, outDur: 1.2 });
boxL("NEW ENGLAND", ...L(43.9, -71.9), T_NE + 0.1, null, { size: 16 });
// =================== m2-2: Skenesborough; the American fleet; the numbers ===================
const BLUE = [["gondola", 43.60, -73.40], ["gondola", 43.66, -73.41], ["gondola", 43.72, -73.40], ["galley", 43.78, -73.40], ["galley", 43.85, -73.38], ["gondola", 43.93, -73.40]];
const AMF = BLUE.map(([kind, la, lo], k) => { const tk = kind === "galley" ? T_GAL + (k - 3) * 0.4 : T_TREES + k * 0.45;
  const b = ship(kind, [SKE, L(la, lo), L(44.05 + k * 0.03, -73.41)], tk, Math.max(1.5, T_15 + 3 - tk), null, { side: "carth", s: 22 });
  return b; });
boxL("GONDOLAS", SKE[0] + 50, SKE[1] - 70, T_GOND, null, { size: 12 }); boxL("GALLEYS", SKE[0] + 60, SKE[1] - 150, T_GAL + 0.1, null, { size: 12 });
// the fleet moves north to its station (more boats appear on "fifteen vessels")
[[44.15, -73.40, "schooner"], [44.22, -73.37, "galley"], [44.30, -73.36, "gondola"]].forEach(([la, lo, kind], k) => ship(kind, [L(la - 0.15, lo), L(la, lo)], T_15 + k * 0.3, 2.5, null, { side: "carth", s: 22 }));
const N15 = placeCard("AMERICANS", "15 VESSELS<br><span class='m7'>ABOUT 700 MEN</span>", "left:110px;top:430px;", T_15 - 0.05, T_AGAINST - 0.3);
{ const m7 = N15.querySelector(".m7"); gsap.set(m7, { autoAlpha: 0 }); tl.fromTo(m7, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3, immediateRender: false }, T_700); }
N15.firstElementChild.style.borderTopColor = "#1f4fc4"; SFX("hit", T_15 + 0.1);
// the British fleet moves south from St. Johns
RFS.forEach((b, k) => { const p = L(RF[k][0], RF[k][1]); tl.to(b.el, { top: p[1] + 120, duration: 6, ease: "sine.inOut" }, T_AGAINST + k * 0.1); });
const N25 = placeCard("BRITISH", "ABOUT 25 ARMED VESSELS<br><span class='m7'>ABOUT 700 SEAMEN</span>", "left:110px;top:430px;", T_25 - 0.05, T_1000 - 0.3);
{ const m7 = N25.querySelector(".m7"); gsap.set(m7, { autoAlpha: 0 }); tl.fromTo(m7, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3, immediateRender: false }, T_SEA); }
N25.firstElementChild.style.borderTopColor = "#c4121f"; SFX("hit", T_25 + 0.1);
// more than a thousand soldiers in boats, behind the warships
[[45.32, -73.28], [45.33, -73.24], [45.35, -73.26], [45.36, -73.29], [45.37, -73.245], [45.39, -73.27]].forEach(([la, lo], k) => ship("bateau", [L(la, lo), L(la - 0.22, lo - 0.02)], T_1000 + k * 0.15, 4.5, null, { side: "rome", s: 18 }));
boxL("MORE THAN 1,000 SOLDIERS IN BOATS", STJ[0] - 230, STJ[1] + 70, T_1000 + 0.3, null, { size: 13, bg: "#f3d6c8" });
// ---------- 1c declutter ----------
declutter([LGD, AB], [[T_P1 + 0.1, T_P1 + 2.9], [T_28 - 0.05, T_ROAD - 0.3], [T_15 - 0.05, T_AGAINST - 0.3], [T_25 - 0.05, T_1000 - 0.3]]);
fixImgs();
K.raiseTerritory();
B.finish();
