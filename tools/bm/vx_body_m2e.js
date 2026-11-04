// MOVE 2e (m2-7), Grant #16: the ONE "What would you do?" card (STYLE_LOCK 1b, E.decide, B3 form: lighter dim, slow camera push, arrows keep
// drawing, options pulse on their words, a beat every <= 2.5 s, black outline on the card text). Map agent "vx".
// Basemap vicksburg_hd_lift (z10), option 1 (tools/vx_make_control.py vx_vick_may03: the west bank + the bridgehead Bruinsburg - Port Gibson -
// Grand Gulf). Early May 1863: the army across the river, deep in enemy country (red all round); Banks far off at Alexandria on the Red River,
// he cannot reach Port Hudson (off the map, south) before the tenth of May, and only with fifteen thousand men.
//   A = WAIT FOR BANKS · B = CUT LOOSE (spoken words only). NO reveal here: the real choice is spoken in m2-8 ("cut loose from his base"), so
//   m2f opens on this same card and lights B there. The decision card is the only big card; legend + badges step out (filter: opacity).
// Facts: FACTCHECK_B #14 (Banks could not reach Port Hudson before 10 May, then with only 15,000 men; Grant at Grand Gulf about 3 May), #11.
// Built with: python3 tools/vx_inline.py m2e vicksburg_hd_lift m2-7 m2-7
// @@KIT
// @@DATA
const VZ = GD.maps.vicksburg;
const L = GG.proj(10, VZ.origin_world_px[0], VZ.origin_world_px[1]);
const LL = (pts) => pts.map(([la, lo]) => L(la, lo));
const P7 = "m2-7";
const T_STOP = at(P7, "Now stop for a moment"), T_PLACE = at(P7, "Grant's place"), T_ACROSS = at(P7, "across the river"), T_DEEP = at(P7, "deep in enemy country"),
  T_BANKS = at(P7, "General Banks"), T_JOIN = at(P7, "might have joined him"), T_PH = at(P7, "Port Hudson"), T_TENTH = at(P7, "the tenth of May"),
  T_15K = at(P7, "fifteen thousand men"), T_DO = at(P7, "Do you wait for Banks"), T_WAIT = at(P7, "wait for Banks"), T_CUT = at(P7, "cut loose"),
  T_INL = at(P7, "go inland alone"), T_TELL = at(P7, "Tell us in the comments"), T_WHAT = at(P7, "what you would have done"), T_THEN = at(P7, "And then");
// ---------- places (vicksburg z10 px) ----------
const VKS = L(32.352, -90.878), GGF = L(32.033, -91.053), BRU = L(31.942, -91.157), PG = L(31.961, -90.984), JAX = L(32.299, -90.185),
  EDW = L(32.33, -90.605), ALX = L(31.50, -92.15), PHX = L(30.678, -91.27);
const RIV = LL([[33.05, -91.12], [32.80, -91.16], [32.60, -91.12], [32.48, -91.06], [32.40, -91.00], [32.375, -90.93], [32.37, -90.895], [32.345, -90.893],
  [32.30, -90.90], [32.247, -90.935], [32.13, -91.04], [32.04, -91.07], [31.95, -91.16], [31.80, -91.30], [31.56, -91.42], [31.25, -91.58]]);
// ---------- map ----------
// owner 2026-11-02: no territory fill on this close-up (option 2: two glowing front bands, on screen from frame 0)
// may03 ground (tools/vx_make_control.py vick(): west bank + the bridgehead Bruinsburg - Port Gibson - Grand Gulf) as option 2 fronts:
// the west edge of the west-bank strip, round the bridgehead, then up the river (Union inside / west, red band on the Confederate side)
const F03P = LL([[33.40, -91.52], [32.90, -91.50], [32.55, -91.48], [32.25, -91.45], [32.02, -91.42], [31.96, -91.20], [31.90, -91.20], [31.87, -91.05], [31.90, -90.93],
  [31.97, -90.86], [32.06, -90.76], [32.12, -90.80], [32.15, -90.92], [32.10, -91.00], [32.045, -91.06], [32.06, -91.08], [32.12, -91.02], [32.20, -90.98], [32.28, -90.93],
  [32.32, -90.90], [32.36, -90.93], [32.47, -91.02], [32.62, -91.11], [32.82, -91.13], [33.05, -91.12], [33.40, -91.18]]);
const F03 = on0(front2(F03P, 1.25, 0, { flip: true, dur: 0.01 }));
living(VZ.meters_per_px, [RIV], { n: 6, clouds: 0.13, sw: 4 });
const LGD = now(legend(0, END + 1, true));
dateNow("MAY 1863", null);
// ---------- camera (B3: keeps moving under the card) ----------
const K0 = [1310, 940, 1.55], K1 = [1350, 900, 1.3], K2 = [1150, 1100, 0.86], K3 = [1240, 1000, 1.0], K4 = [1290, 960, 1.22];
camera([[0, ...K0], [T_ACROSS, ...K0], [T_DEEP + 0.4, ...K1], [T_BANKS + 0.2, ...K1], [T_PH + 0.3, ...K2], [T_DO - 0.2, ...K2], [T_DO + 1.6, ...K3], [END, ...K4]]);
// ---------- flags (both visible on every frame) ----------
now(flagS(FL.us, "", 1010, 880, 0, END + 1)); now(flagS(FL.cs, "", 1700, 960, 0, END + 1));
// ---------- units: the army in the bridgehead, Confederates all round (no names: none spoken here) ----------
U("u13", "carth", L(31.985, -90.955), "XIII", "XXX"); U("u17", "carth", L(32.075, -90.905), "XVII", "XXX"); U("u15", "carth", L(32.18, -91.17), "XV", "XXX");
along("u15", [L(32.18, -91.17), L(32.10, -91.13), L(32.06, -91.10)], 0.2, 12, 12);   // Sherman's corps still coming down the west bank
const RED = [["r1", L(32.36, -90.84), "XX"], ["r2", L(32.33, -90.64), "XX"], ["r3", L(32.30, -90.24), "XX"], ["r4", L(32.18, -90.75), "XX"]];
RED.forEach(([id, p, sz]) => U(id, "rome", p, "", sz));
B.move("r2", 0.4, 10, ...L(32.30, -90.70)); B.move("r4", 0.6, 12, ...L(32.14, -90.80));
// Banks' column on the Red River (Alexandria), far from Port Hudson
unitS("bk", "carth", ALX, "infantry", "BANKS", { t: T_BANKS + 0.1, size: "XX" });
// ---------- m2-7 beats ----------
const GRB = cmd("grant", "ULYSSES S. GRANT", "ARMY OF THE TENNESSEE", "carth", "bl", T_PLACE - 0.1, T_BANKS - 0.2);
// across the river: the crossing pulses; deep in enemy country: red rings close round the bridgehead
const XR = arw({ pts: [L(31.99, -91.24), L(31.965, -91.18), L(31.955, -91.13)], side: "carth", t: T_ACROSS - 0.1, dur: 0.9, width: AW(1.4, 12), until: T_BANKS });
K.target(...L(32.02, -90.96), T_ACROSS + 0.4, { r: 40, side: "carth", until: T_DEEP + 2.5 });
[[VKS, 0], [EDW, 0.4], [L(32.18, -90.75), 0.8], [JAX, 1.2]].forEach(([p, d]) => K.target(p[0], p[1], T_DEEP + d, { r: 26, side: "rome", until: T_DEEP + 2.6 + d }));
// General Banks: his badge on his name; the hoped-for join (dashed, from Port Hudson up the river) greys out
const BKB = cmd("banks", "NATHANIEL P. BANKS", "GENERAL", "carth", "tr", T_BANKS, T_DO - 0.3);
const JOIN = arw({ pts: LL([[31.25, -91.58], [31.56, -91.42], [31.80, -91.28], [31.93, -91.17]]), side: "carth", t: T_JOIN - 0.1, dur: 1.2, width: AW(0.86, 11), dash: "14 10", until: END + 1 });
B.greyArrow(JOIN, T_PH + 0.2, T_TENTH + 0.6);
const PHB = boxL("PORT HUDSON ▼", PHX[0] - 10, 1560, T_PH, null, { size: 20 });
const BKA = arw({ pts: [ALX, L(31.38, -91.95), L(31.29, -91.62)], side: "carth", t: T_PH + 0.1, dur: 2.0, width: AW(0.86, 11), dash: "14 10", until: END + 1 });
B.caption("NOT BEFORE THE TENTH OF MAY", T_TENTH, T_15K - 0.1, "carth r");
B.caption("ONLY FIFTEEN THOUSAND MEN", T_15K, T_DO - 0.25, "carth r");
tl.fromTo(B.units.bk.el.querySelector(".blk"), { scale: 1 }, { scale: 1.3, duration: 0.22, yoyo: true, repeat: 1, immediateRender: false }, T_15K + 0.1);
// ---------- E.decide (B3) on "Do you wait for Banks" ----------
const DEC = E.decide({ sub: "ACROSS THE RIVER · DEEP IN ENEMY COUNTRY", a: "WAIT FOR BANKS", b: "CUT LOOSE", real: 1, t: T_DO - 0.2, tCount: T_TELL, tReveal: END + 0.9, until: END + 1 });
const OA = DEC.querySelector(".o0"), OB = DEC.querySelector(".o1");
DEC.style.webkitTextStroke = "2px #000"; DEC.style.paintOrder = "stroke fill"; DEC.style.textShadow = "0 2px 6px rgba(0,0,0,0.9)";
const BACK = DEC.previousElementSibling;
tl.to(BACK, { autoAlpha: 0.56, duration: 0.8 }, T_DO + 0.4);                       // lighter dim: the moving map shows through
const pulse = (el, t, col = "#ffd54a") => { tl.to(el, { scale: 1.07, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }, t);
  tl.fromTo(el, { boxShadow: "0 0 0px rgba(255,213,74,0)" }, { boxShadow: `0 0 28px ${col}`, duration: 0.2, yoyo: true, repeat: 1, immediateRender: false }, t); SFX("tick", t); };
pulse(OA, T_WAIT + 0.5); pulse(OB, T_CUT + 0.2); pulse(OB, T_INL + 0.2); pulse(DEC.querySelector(".cd"), T_WHAT, "#c9b48a"); pulse(OA, T_THEN - 0.2); pulse(OB, T_THEN + 0.3);
// the map keeps moving under the card: the inland ghost arrows draw (toward Jackson / toward Vicksburg), Banks' column crawls, rings
const GH1 = arw({ pts: LL([[32.02, -90.93], [32.12, -90.72], [32.22, -90.50], [32.28, -90.30]]), side: "carth", t: T_CUT + 0.1, dur: 3.2, width: AW(1.1, 12), dash: "16 12", until: END + 1 });
const GH2 = arw({ pts: LL([[32.08, -90.89], [32.20, -90.82], [32.30, -90.80]]), side: "carth", t: T_INL + 0.3, dur: 2.6, width: AW(1.1, 12), dash: "16 12", until: END + 1 });
B.move("bk", T_DO + 0.4, END - T_DO, ...L(31.36, -92.12));
const RINGS = [[L(32.02, -90.96), "carth"], [JAX, "rome"], [VKS, "rome"], [L(32.02, -90.96), "carth"]];
for (let k = 0, tt = T_DO + 0.9; tt < END - 0.6 && k < RINGS.length; k++, tt += 2.4) K.target(RINGS[k][0][0], RINGS[k][0][1], tt, { r: 26, side: RINGS[k][1], until: tt + 1.8 });
// ---------- 1c declutter: the decision card is the only big card ----------
declutter([LGD, GRB, BKB], [[T_DO - 0.2, END + 1]]);
fixImgs();
K.raiseTerritory();
B.finish();
