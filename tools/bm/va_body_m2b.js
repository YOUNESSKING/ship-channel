// MOVE 2b (m2-3 .. m2-5), Arnold #17: Valcour Island, 11 October 1776. Map agent "va". Basemap valcour_hd_lift (z13, 13.6 m/px).
//   python3 tools/va_inline.py m2b valcour_hd_lift m2-3 m2-5
// m2-3  dive into `valcour` (soft option-1 colours dissolve ~2.8 s): the island close to the NY shore, the narrow channel; the American
//       boats come up into the channel and anchor in a curved line (crescent) across it; a dashed sight line from the main lake is blocked
//       by the island (OUT OF SIGHT); Gates badge on his name.
// m2-4  11 OCT 1776; north-east wind; the British fleet sails down the open lake past the island, turns and tacks back up against the wind;
//       only the schooner CARLETON and the gunboats close in; the big ships stay out; ROYAL SAVAGE runs onto the south point and is lost;
//       from noon the two lines fight at close range (visible ship guns, option 2 two-colour front).
// m2-5  Arnold badge; the CONGRESS fires on "aimed" + small verbatim quote card; CARLETON hit, Pellew badge (initials), she swings round
//       and is towed out by two gunboats; dusk: INFLEXIBLE comes up and fires five broadsides; the gondola PHILADELPHIA sinks.
// Facts: FACTCHECK_B (NE wind, Royal Savage on the south point, Carleton towed off by two gunboats, five broadsides at dusk, Philadelphia sank
// an hour after); positions = DEM of the valcour map (island x 1372-1530, y 510-748; NY shore x ~1290-1340).
// @@KIT
// @@DATA
const VZ = GD.maps.valcour;
const P3 = "m2-3", P4 = "m2-4", P5 = "m2-5";
const T_PICK = at(P3, "Arnold had picked"), T_HALF = at(P3, "Halfway"), T_ISL = at(P3, "island of Valcour"), T_CHAN = at(P3, "narrow channel"),
  T_ANCH = at(P3, "He anchored"), T_CURVE = at(P3, "curved line"), T_SIGHT = at(P3, "out of sight"), T_WEEKS = at(P3, "Weeks earlier"), T_GATES = at(P3, "Gates");
const T_11 = at(P4, "eleventh of October"), T_NE = at(P4, "north-east"), T_PAST = at(P4, "sailed right past"), T_ATT = at(P4, "To attack"),
  T_WIND = at(P4, "against the wind"), T_CARL = at(P4, "Only the schooner Carleton"), T_BIG = at(P4, "Their biggest ships"), T_RS = at(P4, "Royal Savage"),
  T_AGR = at(P4, "ran aground"), T_LOST = at(P4, "was lost"), T_NOON = at(P4, "From about noon"), T_CLOSE = at(P4, "close range");
const T_P5 = B.T.paras[P5][0], T_AIM = at(P5, "aimed most"), T_GAL5 = at(P5, "his galley"), T_CONG = at(P5, "the Congress"), T_CHIT = at(P5, "The Carleton was hit"), T_PEL = at(P5, "Edward Pellew"),
  T_BOW = at(P5, "bowsprit"), T_TOW = at(P5, "towed out"), T_DUSK = at(P5, "At dusk"), T_FIVE = at(P5, "five broadsides"), T_PHIL = at(P5, "The gondola Philadelphia"),
  T_SANK = at(P5, "sank about"), T_STOP = at(P5, "guns stopped");
// ---------- places (valcour map px) ----------
const SPT = [1446, 750];                                   // the island's south point (Royal Savage aground)
const CH = [[1322, 470], [1330, 540], [1338, 610], [1352, 680], [1372, 740]];   // the channel behind the island
// the crescent across the channel, horns to the south (the side the enemy must come from)
const ARC = [[1338, 738], [1346, 716], [1360, 700], [1381, 693], [1402, 700], [1416, 716], [1424, 738]];
const NAM = ["g1", "g2", "phil", "g4", "trumbull", "congress", "washington", "rsavage", "revenge", "enterprise", "lee", "g9", "g10", "g11", "g12"];
const KIND = ["gondola", "gondola", "gondola", "gondola", "galley", "galley", "galley", "schooner", "schooner", "schooner", "galley", "gondola", "gondola", "gondola", "gondola"];
const SLOT = NAM.map((_, k) => posOn(ARC, k / 14));
// ---------- layers ----------
living(VZ.meters_per_px, [], { n: 5, clouds: 0.1 });
const TC = terr0("assets/media/va_valcour_ctl_mx.png"); TC.style.filter = SOFT;   // American shores (both sides of the lake were American in Oct 1776)
tl.to(TC, { autoAlpha: 0, duration: 2.8, ease: "sine.inOut" }, 0.3);          // option 1 -> option 2 during the dive
// ---------- camera ----------
const sKeys = [[0, 1440, 810, 0.72], [3.4, 1420, 760, 1.15, "power2.inOut"], [T_ISL, 1405, 700, 1.7], [T_ANCH, 1385, 712, 2.3], [T_WEEKS, 1388, 712, 2.4],
  [T_P5 - 34, 1420, 720, 1.8], [T_NE, 1560, 560, 0.85], [T_ATT + 1, 1560, 760, 0.9], [T_BIG, 1470, 820, 1.35], [T_AGR, 1430, 780, 1.8], [T_CLOSE, 1400, 770, 2.0],
  [T_AIM + 0.5, 1385, 745, 2.35], [T_CHIT + 0.5, 1392, 772, 2.15], [T_TOW + 0.5, 1415, 805, 1.85], [T_DUSK + 1.2, 1440, 820, 1.6], [END, 1425, 800, 1.85]];
const sAt = (t) => { for (let i = 1; i < sKeys.length; i++) if (t <= sKeys[i][0]) { const [a, , , sa] = sKeys[i - 1], [b, , , sb] = sKeys[i], u = (t - a) / Math.max(0.01, b - a); return sa + (sb - sa) * u; } return sKeys[sKeys.length - 1][3]; };
camera(sKeys);
SFX("whoosh", 0.2);
// ---------- HUD ----------
B.showDate(0); B.date("OCTOBER 1776", 0, T_11 - 0.1, 32); date0(); B.date("11 OCTOBER 1776", T_11, T_NOON - 0.1, 32);
B.date("11 OCT 1776 · NOON", T_NOON, T_DUSK - 0.1, 32); B.date("11 OCT 1776 · DUSK", T_DUSK, END + 1, 32);
const LGD = legend(4.2, END + 1, true);
// audit #11/#12/#16 (2026-11-03): both flags on LAND on the New York shore, in frame and clear of the legend, badges, date scroll, boats and labels at every
// camera position (placed with tools/va_flagsolve.py from the frame probe): the Union Flag on the shore beside the channel (British troops and their Native
// allies were landed on the shore and the island), the Continental Colours on the shore south of the fight
flagS(FL.cs, "", 1050, 677, 0, END + 1); flagS(FL.us, "", 1040, 851, 0, END + 1);
// ---------- m2-3: the American boats come up into the channel and anchor in a crescent ----------
const APPROACH = (k) => [[1395 + (k % 3) * 8, 1150 + k * 26], [1380, 960 + k * 6], [1372, 800 + k * 2], SLOT[k]];
const AM = NAM.map((nm, k) => ship(KIND[k], APPROACH(k), 0, T_ANCH + 0.8 - k * 0.05, null, { s: 22, t0: 0, ease: (u) => 1 - (1 - u) * (1 - u) }));
// once at anchor, every boat points its bow south (toward the only way in): a short swing
AM.forEach((b, k) => tl.to(b.sv, { rotation: 90, duration: 1.2, ease: "sine.inOut" }, T_ANCH + 0.9 + k * 0.03));
boxL("VALCOUR ISLAND", 1545, 600, T_ISL, null, { size: 13 });
glowPath(CH, "#8fc3ff", 3, T_CHAN - 0.2, T_ANCH + 2.5, 2, 0.6, { draw: 1.4 });
boxL("CHANNEL", 1250, 560, T_CHAN + 0.1, null, { size: 11 });
glowPath(ARC.map(([x, y]) => [x, y - 12]), "#6f9bff", 2.0, T_CURVE - 0.1, T_SIGHT + 3.5, 2, 0.95, { draw: 1.0 });
// "out of sight of anyone sailing down the main lake": a dashed sight line from the open lake, stopped by the island
const EYE = [1640, 560], STOP = [1515, 625];
const SL = trail([EYE, STOP], "#ff8a80", 2.2, T_SIGHT - 0.1, 0.9, T_WEEKS + 1.2, "6 6");
const XM = pinS(GG.pin(`<svg width="30" height="30" viewBox="-10 -10 20 20" style="display:block;overflow:visible;filter:drop-shadow(0 0 4px #000)"><path d="M-7 -7 L7 7 M7 -7 L-7 7" stroke="#e3232f" stroke-width="3.2" stroke-linecap="round"/></svg>`, STOP[0], STOP[1], { t: T_SIGHT + 0.9, until: T_WEEKS + 1.2 }));
boxL("OUT OF SIGHT", 1585, 520, T_SIGHT + 0.6, null, { size: 12, bg: "#f3d6c8" });
const GB = cmd("gates", "HORATIO GATES", "GENERAL · TICONDEROGA", "carth", "tr", T_GATES + 0.1, B.T.paras[P4][0]);
// ---------- m2-4: the British fleet runs down the lake past the island, then beats back up against the wind ----------
const DOWN = [[1640, -80], [1650, 200], [1660, 480], [1665, 760], [1630, 980], [1580, 1060]];
const TACK = (end) => [[1580, 1060], [1500, 1010], [1560, 960], [1490, 915], [1530, 870], end];
const T0 = T_11 - 0.6, TD = T_ATT + 0.8 - T0, TT = T_CARL + 3.5 - (T_ATT + 0.8);
const BR = [   // [kind, name, final position, delay, size]
  ["schooner", "carleton", [1398, 792], 0.0, 24], ["gunboat2", "gb1", [1345, 806], 0.4, 20], ["gunboat2", "gb2", [1374, 814], 0.6, 20], ["gunboat2", "gb3", [1428, 812], 0.8, 20],
  ["gunboat2", "gb4", [1458, 800], 1.0, 20], ["gunboat2", "gb5", [1356, 842], 1.2, 20], ["gunboat2", "gb6", [1410, 846], 1.4, 20], ["gunboat2", "gb7", [1446, 838], 1.6, 20],
  ["schooner", "maria", [1585, 925], 1.8, 25], ["ship", "inflexible", [1555, 975], 2.2, 28], ["gondola", "convert", [1615, 1010], 2.6, 22], ["radeau", "thunderer", [1650, 1110], 3.0, 28]];
const RB = {};
BR.forEach(([kind, nm, end, dl, s]) => {
  const off = (dl * 18) % 40 - 20, d = DOWN.map(([x, y]) => [x + off, y - dl * 70]);
  const big = nm === "inflexible" || nm === "thunderer" || nm === "maria" || nm === "convert";
  const path = big ? [...d, [end[0] + 30, end[1] + 40], end] : [...d, ...TACK(end).slice(1)];
  RB[nm] = ship(kind, path, T0 + dl * 0.5, TD + TT - dl * 0.3 + (big ? 2 : 0), null, { side: "rome", s, t0: T0 + dl * 0.5 });
});
// the wind: a big arrow from the north-east, on the spoken words
const WA = arw({ pts: [[1980, 230], [1870, 340], [1760, 450]], side: "rome", t: T_NE - 0.1, dur: 1.0, width: AW(0.85, 16) });
WA.querySelectorAll("path,polygon").forEach((p) => { p.setAttribute("stroke", "#f3eee2"); p.setAttribute("fill", p.tagName === "polygon" ? "#f3eee2" : "none"); });
tl.to(WA, { autoAlpha: 0, duration: 0.6 }, T_ATT + 3);
boxL("WIND FROM THE NORTH-EAST", 2150, 420, T_NE, null, { size: 14 });   // audit #36: clear of the legend
boxL("AGAINST THE WIND", 1360, 1010, T_WIND, null, { size: 13, bg: "#f3d6c8" });
boxL("CARLETON", 1300, 850, T_CARL + 0.6, null, { size: 12, bg: "#f3d6c8" });
boxL("INFLEXIBLE", 1650, 975, T_BIG + 0.2, null, { size: 12, bg: "#f3d6c8" });
// Royal Savage falls to leeward and runs onto the south point of the island; lost
{ const rs = AM[7], q0 = SLOT[7]; tl.to(rs.el, { left: (q0[0] + SPT[0]) / 2 + 6, top: q0[1] + 14, duration: 1.0, ease: "sine.in" }, T_RS - 0.3);
  tl.to(rs.el, { left: SPT[0] - 6, top: SPT[1] - 4, duration: 1.2, ease: "power2.out" }, T_RS + 0.7); tl.to(rs.sv, { rotation: 35, duration: 2.0 }, T_RS - 0.2);
  tl.to(rs.sv, { filter: "grayscale(1) brightness(0.65)", duration: 0.6 }, T_LOST); }
boxL("ROYAL SAVAGE", SPT[0] + 20, SPT[1] - 40, T_RS + 0.1, null, { size: 12 });
wstampL("LOST", SPT[0] + 28, SPT[1] + 18, T_LOST, null, "#e3232f", 18);
// noon to dusk: the two lines fight at close range (option 2 two-colour band across the channel's south end)
const FR = front2([[1324, 768], [1360, 764], [1395, 762], [1430, 766], [1466, 774]], 2.0, T_NOON - 0.2, { flip: true, dur: 1.4 });
// visible ship guns, ~1 shot per 1.5 s: [time, from (american slot k | british name), to]
const amAt = (k) => AM[k].at(T_ANCH + 99);
const brAt = (nm) => (t) => RB[nm].at(t);
// audit #24 (2026-11-03): no barrage of tiny shells: SIX readable shots from noon to the tow (big flash + smoke, thick arc, big impact), >= 2 s apart
const BIG = { dur: 0.7, h: 26, r: 15, fl: 34, aw: 2.8 };
const FIRE = [[T_NOON + 0.4, "carleton", 6], [T_CLOSE + 0.4, 8, "gb4"]];
FIRE.forEach(([t, a, b]) => { const from = typeof a === "number" ? amAt(a) : RB[a].at(t), to = typeof b === "number" ? amAt(b) : RB[b].at(t + 0.7);
  shootS(from, [to[0] + 2, to[1] + (typeof b === "number" ? 4 : -3)], t, sAt(t), BIG); });
// ---------- m2-5: Arnold aims the Congress's guns; quote card; the Carleton hit, Pellew, towed out; dusk: the Inflexible; Philadelphia sinks ----------
const AB = cmd("arnold", "BENEDICT ARNOLD", "GALLEY CONGRESS", "carth", "tr", T_P5 + 0.2, T_DUSK - 0.4);
{ const role = [...AB.querySelectorAll("div")].find((d) => d.textContent === "GALLEY CONGRESS"); gsap.set(role, { autoAlpha: 0 });   // audit #38: sub-line on "his galley, the Congress"
  tl.fromTo(role, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3, immediateRender: false }, T_GAL5); }
boxL("CONGRESS", amAt(5)[0] - 70, amAt(5)[1] - 40, T_CONG, null, { size: 11 });
K.target(amAt(5)[0], amAt(5)[1], T_AIM - 0.2, { r: 16, side: "carth", until: T_CHIT });
// the Congress fires (Arnold aims): two shots into the Carleton (audit #9: the never-spoken quote card is gone)
[[T_AIM + 0.2, "carleton"], [T_CONG + 0.3, "carleton"]].forEach(([t, b]) => { shootS(amAt(5), RB[b].at(t + 0.7), t, sAt(t), BIG);
  tl.fromTo(RB.carleton.sv, { filter: "brightness(1)" }, { filter: "brightness(2.3)", duration: 0.08, yoyo: true, repeat: 1, immediateRender: false }, t + 0.75); });
// the Carleton hit hard; Pellew on the bowsprit swings her round; two gunboats tow her out
[[T_CHIT + 0.9, 4], [T_PEL + 0.3, 9]].forEach(([t, k]) => { shootS(amAt(k), RB.carleton.at(t + 0.7), t, sAt(t), BIG);
  tl.fromTo(RB.carleton.sv, { filter: "brightness(1)" }, { filter: "brightness(2.3)", duration: 0.08, yoyo: true, repeat: 1, immediateRender: false }, t + 0.6); });
const PB = badge({ name: "EDWARD PELLEW", role: "THE CARLETON", photo: "assets/media/pellew_head.png", flag: FL.cs, side: "rome", corner: "bl", initials: "EP", t: T_PEL + 0.1, until: T_DUSK - 0.4 });
tl.to(RB.carleton.sv, { rotation: "+=70", duration: 2.2, ease: "sine.inOut" }, T_BOW);
boxL("BOWSPRIT", 1340, 845, T_BOW + 0.2, null, { size: 11, bg: "#f3d6c8" });
const TOWP = [[1398, 788], [1420, 840], [1470, 900], [1520, 950], [1560, 1010]];
tl.to(RB.gb3.el, { left: 1410, top: 800, duration: 1.0 }, T_TOW - 1.2); tl.to(RB.gb4.el, { left: 1414, top: 778, duration: 1.0 }, T_TOW - 1.2);
pinAlong(RB.carleton.el, TOWP, T_TOW, 6.0, 16); pinAlong(RB.gb3.el, TOWP.map(([x, y]) => [x + 14, y + 22]), T_TOW, 6.0, 16); pinAlong(RB.gb4.el, TOWP.map(([x, y]) => [x + 22, y + 8]), T_TOW, 6.0, 16);
tl.to([RB.gb3.sv, RB.gb4.sv], { rotation: 60, duration: 0.8 }, T_TOW);
boxL("TOWED OUT", 1480, 870, T_TOW + 0.4, null, { size: 12, bg: "#f3d6c8" });
// dusk: the Inflexible comes up and fires five broadsides into the American line (five visible flashes)
const DU = GG.layer("background:linear-gradient(to bottom, rgba(40,30,70,0.38), rgba(255,130,60,0.22));mix-blend-mode:multiply;", T_DUSK - 0.3, END + 1, { dur: 2.5 });
const INF = RB.inflexible; tl.to(INF.el, { left: 1452, top: 858, duration: T_FIVE - T_DUSK - 0.3, ease: "sine.inOut" }, T_DUSK); tl.to(INF.sv, { rotation: 175, duration: 2.0 }, T_DUSK + 0.4);
const ipos = [1452, 858];
[0, 1, 2, 3, 4].forEach((k) => { const t = T_FIVE + k * 0.85;
  const fl = pinS(GG.pin(`<div style="width:46px;height:20px;border-radius:50%;background:radial-gradient(ellipse,#fff6c8 0%,#ffb020 45%,rgba(255,120,0,0) 72%)"></div>`, ipos[0], ipos[1] - 12, {}));
  tl.fromTo(fl, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.05, immediateRender: false }, t); tl.to(fl, { autoAlpha: 0, duration: 0.3 }, t + 0.08);
  K.smoke(ipos[0], ipos[1] - 10, t + 0.1, { n: 2, r: 8, rise: 12, life: 2.4, alpha: 0.5, drift: 8 });
  shootS(ipos, amAt([2, 6, 9, 3, 11][k]), t, sAt(t), { dur: 0.6, h: 16, r: 8 }); });
const FIVE = sstamp("FIVE BROADSIDES", 760, T_FIVE + 0.1, { size: 54, shake: 4, until: T_FIVE + 2.6 });
// the Royal Savage burns on the point at dusk
fireGlowS(SPT[0] - 6, SPT[1] - 4, 26, T_DUSK + 0.8, END + 1);
for (let tt = T_DUSK + 1.0; tt < END - 0.5; tt += 0.8) K.smoke(SPT[0] - 6, SPT[1] - 8, tt, { n: 1, r: 8, rise: 26, life: 2.6, alpha: 0.55, drift: 10 });
// the Philadelphia, holed, sinks after the guns stop
boxL("PHILADELPHIA", amAt(2)[0] - 115, amAt(2)[1] + 26, T_PHIL + 0.3, null, { size: 11 });
const PH = AM[2];
tl.to(PH.sv, { filter: "brightness(0.55)", duration: 0.6 }, T_PHIL + 0.5);
tl.to(PH.el, { autoAlpha: 0, duration: 1.6, ease: "power1.in" }, T_SANK + 0.2); tl.to(PH.sv, { scale: 0.55, rotation: "+=30", duration: 1.6 }, T_SANK + 0.2);
{ const q = amAt(2), rip = pinS(GG.pin(`<div style="width:40px;height:40px;border-radius:50%;border:2.5px solid rgba(200,225,255,.85)"></div>`, q[0], q[1], {})), r = rip.firstElementChild.firstElementChild || rip.firstElementChild;
  gsap.set(rip, { autoAlpha: 0 }); tl.set(rip, { autoAlpha: 1 }, T_SANK + 0.5); tl.fromTo(r, { opacity: 0.9, scale: 0.3 }, { opacity: 0, scale: 2.2, duration: 1.8, immediateRender: false }, T_SANK + 0.5); }
// ---------- 1c declutter (legend + corner badges step out under the big cards) ----------
declutter([LGD, GB, AB, PB], [[T_FIVE + 0.1, T_FIVE + 2.6]]);
fixImgs();
K.raiseTerritory();
B.finish();
