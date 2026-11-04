// MOVE 2c (m2-6 .. m2-7), Arnold #17: the night of 11-12 October 1776 at Valcour. Map agent "va". NIGHT MODE, option 2.
//   python3 tools/va_inline.py m2c valcour_hd_lift m2-6 m2-7
// m2-6  the British anchor in a line across the south end of the channel (Pringle: "from the Island to the West Side of the Continent");
//       the American boats trapped behind it; card ABOUT 60 KILLED AND WOUNDED / NEARLY 3/4 OF THE AMMUNITION GONE on the words;
//       E.decide on "put yourself in Arnold's place" (each option lands on its own spoken words), 3 ticks on "Tell us in the comments".
// m2-7  reveal B on the paragraph start; 7 PM: Trumbull leads, the gondolas follow, Congress + Washington last, single file close along the
//       western (New York) shore past the end of the British line, no fire; Waterbury badge (initials); dawn: the channel empty.
// Facts: FACTCHECK_B (Arnold 12 Oct: "at 7 oClock ... Trumbull got under Way, the Gondolas & Small Vessells followed & the Congress &
// Washington brought up the Rear"; Waterbury via Mahan "entirely undiscovered"; ~60 killed and wounded; ammunition "Nearly three fourths spent").
// @@KIT
// @@DATA
const VZ = GD.maps.valcour;
const P6 = "m2-6", P7 = "m2-7";
const T_LINE = at(P6, "anchored in a line"), T_SOUTH = at(P6, "south end"), T_DAWN0 = at(P6, "finish him at dawn"), T_60 = at(P6, "sixty men"),
  T_34 = at(P6, "three quarters"), T_STOP = at(P6, "Now stop"), T_PUT = at(P6, "put yourself in Arnold's place"), T_TRAP = at(P6, "You are trapped"),
  T_FIGHT = at(P6, "Do you fight"), T_SLIP = at(P6, "slip past"), T_TELL = at(P6, "Tell us in the comments"), T_LISTEN = at(P6, "And then listen");
const T_P7 = B.T.paras[P7][0], T_7 = at(P7, "seven o'clock"), T_TRUM = at(P7, "Trumbull"), T_GOND = at(P7, "the gondolas"), T_CW = at(P7, "the Congress and the Washington"),
  T_ONE = at(P7, "One behind another"), T_CREPT = at(P7, "crept along the shore"), T_END = at(P7, "past the end"), T_WAT = at(P7, "David Waterbury"),
  T_UND = at(P7, "without being discovered"), T_MORN = at(P7, "In the morning"), T_EMPTY = at(P7, "channel empty");
// ---------- places (valcour map px; same as m2b) ----------
const SPT = [1446, 750];
const ARC = [[1338, 738], [1346, 716], [1360, 700], [1381, 693], [1402, 700], [1416, 716], [1424, 738]];
const NAM = ["g1", "g2", "g4", "trumbull", "congress", "washington", "revenge", "enterprise", "lee", "g9", "g10", "g11", "g12"];
const KIND = ["gondola", "gondola", "gondola", "galley", "galley", "galley", "schooner", "schooner", "galley", "gondola", "gondola", "gondola", "gondola"];
const SLOT = NAM.map((_, k) => posOn(ARC, k / 12));
// the escape route: close along the New York shore, south past the west end of the British line, out of the frame
const ROUTE = [[1338, 745], [1330, 775], [1326, 810], [1334, 860], [1346, 920], [1358, 990], [1372, 1070], [1390, 1170], [1410, 1290], [1430, 1420]];
// escape order: Trumbull first, gondolas + small vessels, Congress and Washington last
const ORDER = ["trumbull", "g1", "g2", "g4", "revenge", "enterprise", "lee", "g9", "g10", "g11", "g12", "congress", "washington"];
// ---------- layers ----------
living(VZ.meters_per_px, [], { n: 4, clouds: 0.08 });
const NL = GG.night(0.0, T_MORN, { dur: 1.4, outDur: 2.6 });
tl.getTweensOf(NL).filter((tw) => tw.startTime() < 0.05).forEach((tw) => tw.kill()); gsap.set(NL, { autoAlpha: 1 });   // night from frame 0 (m2b ends at dusk: no daylight flash at the cut)
const DW = GG.dawn(T_MORN - 0.2, END + 1);
// ---------- camera ----------
const sKeys = [[0, 1410, 790, 1.9], [T_STOP, 1405, 785, 2.05], [T_P7, 1405, 790, 2.0], [T_TRUM + 0.5, 1395, 860, 1.6], [T_END + 1, 1400, 930, 1.45],
  [T_UND, 1410, 900, 1.5], [T_MORN + 0.5, 1405, 790, 1.9], [END, 1400, 770, 2.05]];
const sAt = (t) => { for (let i = 1; i < sKeys.length; i++) if (t <= sKeys[i][0]) { const [a, , , sa] = sKeys[i - 1], [b, , , sb] = sKeys[i], u = (t - a) / Math.max(0.01, b - a); return sa + (sb - sa) * u; } return sKeys[sKeys.length - 1][3]; };
camera(sKeys);
// ---------- HUD ----------
B.showDate(0); B.date("11 OCT 1776 · NIGHT", 0, T_7 - 0.1, 32); date0(); B.date("11 OCT 1776 · 7 PM", T_7, T_MORN - 0.1, 32); B.date("12 OCTOBER 1776 · DAWN", T_MORN, END + 1, 32);
const LGD = legend(0.6, END + 1, true);
flagS(FL.cs, "", 982, 725, 0, END + 1); flagS(FL.us, "", 982, 847, 0, END + 1);   // audit #11/#16/#19: same places as m2b (New York shore), clear of the date scroll, badges, boats and labels (tools/va_flagsolve.py)
// ---------- the American boats in their crescent (at anchor, bows south) ----------
const AM = {};
NAM.forEach((nm, k) => { AM[nm] = ship(KIND[k], [SLOT[k]], 0, 0.01, null, { s: 22, rot: 90, t0: 0 }); });
// the Royal Savage hulk burns on the island's point all night
fireGlowS(SPT[0] - 6, SPT[1] - 4, 26, 0, T_MORN + 1);
for (let tt = 0.2; tt < T_MORN; tt += 0.9) K.smoke(SPT[0] - 6, SPT[1] - 8, tt, { n: 1, r: 8, rise: 26, life: 2.6, alpha: 0.5, drift: 10 });
// ---------- m2-6: the British close the south end in a line (from the island's point toward the west shore, ending short of it) ----------
const LINE = [[1372, 836], [1394, 830], [1416, 824], [1438, 818], [1460, 812], [1484, 806], [1512, 800], [1546, 796], [1584, 800], [1620, 812]];
const BRK = ["gunboat2", "gunboat2", "gunboat2", "ship", "gunboat2", "gunboat2", "schooner", "gondola", "gunboat2", "radeau"];
const START = [[1350, 900], [1380, 930], [1420, 880], [1520, 980], [1450, 940], [1500, 900], [1585, 925], [1615, 1010], [1600, 880], [1650, 1110]];
const RB = BRK.map((kind, k) => ship(kind, [START[k], [(START[k][0] + LINE[k][0]) / 2, (START[k][1] + LINE[k][1]) / 2 + 8], LINE[k]], 0, T_SOUTH + 1.2 + k * 0.1, null,
  { side: "rome", s: kind === "gunboat2" ? 20 : kind === "gondola" ? 22 : 26, t0: 0, ease: (u) => 1 - (1 - u) * (1 - u) }));
RB.forEach((b, k) => tl.to(b.sv, { rotation: -90, duration: 1.4, ease: "sine.inOut" }, T_SOUTH + 1.3 + k * 0.1));   // anchored, bows north
const BLINE = glowPath(LINE.map(([x, y]) => [x, y + 16]), "#ff6a5a", 2.0, T_LINE + 0.2, T_P7 - 0.5, 2, 0.75, { draw: 1.6, dash: "6 5" });
// the trap: the two-colour front band between the crescent and the British line (night palette)
const FR = front2([[1324, 772], [1360, 768], [1395, 766], [1430, 770], [1466, 778]], 2.0, 0.0, { flip: true, dur: 0.01 });
on0(FR); K.night({ lines: [FR], tOn: 0, tOff: T_MORN });
tl.to(FR, { autoAlpha: 0, duration: 1.2 }, T_TRUM);
const T_CARD_OUT = Math.min(T_STOP - 0.2, T_34 + 2.4);   // audit #22: the card holds ~3 s
const LOSS = scr(`<div style="padding:16px 44px 18px;background:rgba(18,16,12,0.93);border-top:6px solid #1f4fc4;font-family:Oswald;font-weight:700;color:#f7f3ea;text-align:center;box-shadow:0 20px 40px rgba(0,0,0,.55)">
  <div style="font-size:46px;letter-spacing:.06em">ABOUT 60 KILLED AND WOUNDED</div><div class="l2" style="font-size:40px;letter-spacing:.06em;color:#ffd9a0;margin-top:6px">NEARLY 3/4 OF THE AMMUNITION GONE</div></div>`,
  "left:0;right:0;top:200px;display:flex;justify-content:center;", T_60 - 0.1, T_CARD_OUT);
{ const l2 = LOSS.querySelector(".l2"); gsap.set(l2, { autoAlpha: 0 }); tl.fromTo(l2, { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.4, immediateRender: false }, T_34); }
SFX("hit", T_60); SFX("ref:pop", T_34);
// ---------- the decision card (each option lands on its own spoken words; B revealed on the paragraph start) ----------
const DC = E.decide({ sub: "VALCOUR · THE NIGHT OF 11 OCTOBER", a: "FIGHT AT DAWN", b: "SLIP PAST IN THE DARK", real: 1, t: T_PUT, tCount: T_TELL + 0.2, tReveal: T_P7 + 0.25, until: T_P7 + 2.6 });
{ const os = [DC.querySelector(".o0"), DC.querySelector(".o1")];
  os.forEach((o) => tl.getTweensOf(o).filter((tw) => tw.startTime() < T_PUT + 1.5).forEach((tw) => tw.kill()));
  gsap.set(os, { autoAlpha: 0 });
  tl.fromTo(os[0], { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.4, immediateRender: false }, T_FIGHT);
  tl.fromTo(os[1], { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.4, immediateRender: false }, T_SLIP - 0.6); }
// audit #18: the date scroll stays above the decision card's dim layer
SCN.insertBefore(document.getElementById("date"), document.getElementById("credit"));
// ---------- m2-7: 7 PM, single file along the shore, past the end of the British line, undiscovered ----------
const T_GO = T_TRUM - 0.2, GAP = 0.85, DUR = 15.0;
ORDER.forEach((nm, k) => { const b = AM[nm], t = T_GO + (nm === "congress" || nm === "washington" ? Math.max(k * GAP, T_CW - T_GO + (nm === "washington" ? GAP : 0)) : k * GAP);
  const p = [SLOT[NAM.indexOf(nm)], ...ROUTE];
  for (let j = 1; j <= 24; j++) { const q = posOn(p, j / 24), q0 = posOn(p, (j - 1) / 24);
    tl.to(b.el, { left: q[0], top: q[1], duration: DUR / 24, ease: "none" }, t + (j - 1) * DUR / 24);
    tl.to(b.sv, { rotation: Math.atan2(q[1] - q0[1], q[0] - q0[0]) * 180 / Math.PI, duration: 0.3, ease: "none" }, t + (j - 1) * DUR / 24); }
  tl.to(b.el, { autoAlpha: 0, duration: 0.6 }, t + DUR - 0.4); });
trail(ROUTE, "#8fb2ff", 2.2, T_GO, 9.0, T_MORN - 0.3, "3 8");
boxL("TRUMBULL", 1190, 790, T_TRUM + 0.4, null, { size: 12 });
boxL("CONGRESS · WASHINGTON", 1160, 760, T_CW + 0.6, null, { size: 12 });
boxL("PAST THE END OF THE BRITISH LINE", 1080, 900, T_END, null, { size: 12 });
const WB = badge({ name: "DAVID WATERBURY", role: "SECOND IN COMMAND", photo: "assets/media/waterbury_head.png", flag: FL.us, side: "carth", corner: "tr", initials: "DW", t: T_WAT + 0.1, until: T_MORN - 0.2 });
B.caption("WENT THROUGH WITHOUT BEING DISCOVERED", T_UND - 0.1, T_MORN - 0.2, "carth");
// dawn: the British ships still at anchor across the south end; the channel behind them empty
K.target(1372, 700, T_EMPTY - 0.3, { r: 34, side: "#ffd54a", until: END + 1 });
// ---------- 1c declutter ----------
declutter([LGD, WB], [[T_60 - 0.1, T_CARD_OUT], [T_PUT, T_P7 + 2.6]]);
fixImgs();
K.raiseTerritory();
B.finish();
