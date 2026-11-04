// MOVE 2f (m2-8 .. m2-10), Grant #16: the real choice (cut loose), Sherman's warning and Grant's reply, the march inland between Pemberton and
// Johnston, five battles in eighteen days (Port Gibson, Raymond, Jackson, Champion Hill, Big Black River), the numbers, Pemberton shut inside
// Vicksburg. Map agent "vx". Basemap vicksburg_hd_lift (z10), option 1 territory by date (tools/vx_make_control.py: may03 -> may12 -> may14 ->
// may16 -> may18), one wide campaign shot -> push-ins on Champion Hill / Big Black -> wide -> push onto Vicksburg (hand-off to m2g).
//   m2-8   frame 0 = the m2e decision card; B lights on "cut loose" (the real choice spoken), A greys; the supply line back to Grand Gulf flickers
//          and goes; SHERMAN badge + card on his name (spoken words, no quote marks: not verbatim in the script); GRANT ANSWERED card: hard bread,
//          coffee and salt + the verbatim "MAKE THE COUNTRY FURNISH THE BALANCE"; about two days of food; beef + corn icons along the way.
//   m2-9   the wedge between PEMBERTON (Vicksburg) and JOHNSTON (Jackson); one stamp per spoken name + date; the date scroll runs 1 -> 17 MAY;
//          Champion Hill: 15,000 vs 25,000 card, one Union division loses more than a third, a Confederate division CUT OFF; Big Black River:
//          18 guns + 1,700+ prisoners.
//   m2-10  numbers card (Grant's own count): over 60,000 Confederates vs about 33,000; IN EIGHTEEN DAYS; five battles cost him fewer than 4,500
//          (Grant's table 695 + 3,425 + 259 = 4,379); 18 MAY: Pemberton's army shut inside Vicksburg, the ring closes.
// Facts: FACTCHECK_B #13, #14, #15-#19, #21, #22, #25. Built with: python3 tools/vx_inline.py m2f vicksburg_hd_lift m2-8 m2-10
// @@KIT
// @@DATA
const VZ = GD.maps.vicksburg;
const L = GG.proj(10, VZ.origin_world_px[0], VZ.origin_world_px[1]);
const LL = (pts) => pts.map(([la, lo]) => L(la, lo));
const P8 = "m2-8", P9 = "m2-9", P10 = "m2-10";
const T_DEC = at(P8, "Grant decided"), T_CUTL = at(P8, "cut loose from his base"), T_SH = at(P8, "Sherman warned"), T_ROAD = at(P8, "one road could not"),
  T_ANS = at(P8, "Grant answered"), T_FULL = at(P8, "full rations"), T_BREAD = at(P8, "hard bread"), T_COF = at(P8, "coffee and salt"),
  T_FURN = at(P8, "make the country furnish"), T_SET = at(P8, "The army set out"), T_TWO = at(P8, "about two days of food"), T_BEEF = at(P8, "found beef and corn"),
  T_CORN = at(P8, "corn along the way");
const T_INL = at(P9, "Grant marched inland"), T_WEDGE = at(P9, "wedged his army"), T_PEM = at(P9, "Pemberton's at Vicksburg"), T_JOH = at(P9, "Joseph Johnston's"),
  T_ONE = at(P9, "He beat them one at a time"), T_PG = at(P9, "Port Gibson"), T_RAY = at(P9, "Raymond on the twelfth"), T_JAX = at(P9, "He seized Jackson"),
  T_WEST = at(P9, "turned back west"), T_CH = at(P9, "At Champion Hill"), T_BEAT = at(P9, "he beat Pemberton"), T_BIG = at(P9, "the biggest fight"),
  T_15 = at(P9, "about fifteen thousand men"), T_25 = at(P9, "about twenty-five thousand"), T_DIV = at(P9, "One Union division"), T_THIRD = at(P9, "more than a third"),
  T_CUTOFF = at(P9, "a whole Confederate division was cut off"), T_NEVER = at(P9, "never made it back"), T_NEXT = at(P9, "The next day"),
  T_BB = at(P9, "at the Big Black River"), T_18G = at(P9, "eighteen guns"), T_1700 = at(P9, "seventeen hundred prisoners");
const T_COUNT = at(P10, "Grant himself counted"), T_60 = at(P10, "over sixty thousand"), T_33 = at(P10, "about thirty-three thousand"), T_18D = at(P10, "In eighteen days"),
  T_DETAIL = at(P10, "beat them in detail"), T_FIVE = at(P10, "the five battles cost him"), T_4500 = at(P10, "fewer than forty-five hundred"),
  T_18M = at(P10, "By the eighteenth of May"), T_SHUT = at(P10, "shut inside Vicksburg");
// ---------- places (vicksburg z10 px) ----------
const VKS = L(32.352, -90.878), GGF = L(32.033, -91.053), PG = L(31.961, -90.984), RAY = L(32.259, -90.422), JAX = L(32.299, -90.185), CH = L(32.333, -90.535),
  EDW = L(32.33, -90.605), BBR = L(32.347, -90.716), CLI = L(32.341, -90.322), BOL = L(32.35, -90.459), UTI = L(32.108, -90.623), RS = L(32.087, -90.80);
const RIV = LL([[33.05, -91.12], [32.80, -91.16], [32.60, -91.12], [32.48, -91.06], [32.40, -91.00], [32.375, -90.93], [32.37, -90.895], [32.345, -90.893],
  [32.30, -90.90], [32.247, -90.935], [32.13, -91.04], [32.04, -91.07], [31.95, -91.16], [31.80, -91.30], [31.56, -91.42], [31.25, -91.58]]);
// ---------- owner 2026-11-02: territory fills ONLY on the wide five-battles shot (the wedge between the two Confederate armies), subtler;
// m2-8 (continuing m2e) and the Champion Hill / Big Black close-ups and the end are option 2 (glowing front bands, no fill) ----------
// may03 ground (tools/vx_make_control.py vick(): west bank + the bridgehead Bruinsburg - Port Gibson - Grand Gulf) as option 2 fronts:
// the west edge of the west-bank strip, round the bridgehead, then up the river (Union inside / west, red band on the Confederate side)
const F03P = LL([[33.40, -91.52], [32.90, -91.50], [32.55, -91.48], [32.25, -91.45], [32.02, -91.42], [31.96, -91.20], [31.90, -91.20], [31.87, -91.05], [31.90, -90.93],
  [31.97, -90.86], [32.06, -90.76], [32.12, -90.80], [32.15, -90.92], [32.10, -91.00], [32.045, -91.06], [32.06, -91.08], [32.12, -91.02], [32.20, -90.98], [32.28, -90.93],
  [32.32, -90.90], [32.36, -90.93], [32.47, -91.02], [32.62, -91.11], [32.82, -91.13], [33.05, -91.12], [33.40, -91.18]]);
const F03 = on0(front2(F03P, 1.25, 0, { flip: true, dur: 0.01 }));
const T_T0 = T_INL - 0.2, T_T1 = T_CH - 0.3;                      // fill in over ~2.2 s as the camera opens out; dissolves ~2.8 s into the Champion Hill dive
tl.to(F03, { opacity: 0, duration: 2.2, ease: "sine.inOut" }, T_T0);
const TC = [["may03", T_T0], ["may12", T_RAY + 0.2], ["may14", T_JAX + 0.2], ["may16", T_WEST + 0.3]];
TC.forEach(([d, t], k) => { const nx = TC[k + 1], el = terr(`assets/media/vx_vick_${d}_mx.png`, t, nx ? nx[1] : T_T1, k ? 1.0 : 2.2, nx ? 1.0 : 2.8); el.style.filter = SOFT; });
living(VZ.meters_per_px, [RIV], { n: 6, clouds: 0.12, sw: 4 });
const LGD = now(legend(0, T_T0, true)), LGS = legend(T_T0 + 0.6, T_T1 + 0.8, false), LGL = legend(T_T1 + 1.4, END + 1, true);
// ---------- date scroll (never leaves): MAY 1863 -> 1 / 12 / 14 / 16 / 17 / 18 MAY ----------
const DS = [["MAY 1863", null], ["1 MAY 1863", T_PG], ["12 MAY 1863", T_RAY], ["14 MAY 1863", T_JAX + 0.3], ["16 MAY 1863", T_CH + 0.3], ["17 MAY 1863", T_NEXT + 0.2], ["MAY 1863", T_COUNT], ["18 MAY 1863", T_18M + 0.3]];
DS.forEach(([txt, t], k) => { const nx = DS[k + 1]; if (t == null) dateNow(txt, nx[1] - 0.05); else B.date(txt, t, nx ? nx[1] - 0.05 : null, 32); });
// ---------- camera ----------
const KA = [1290, 960, 1.22], KB = [1300, 930, 1.5], KW = [1540, 820, 1.72], KC = [1615, 700, 2.7], KBB = [1520, 700, 2.7], KW2 = [1560, 810, 1.7], KV = [1450, 700, 2.5];
camera([[0, ...KA], [T_CUTL + 1.6, ...KA], [T_SH + 0.6, ...KB], [T_SET, ...KB], [T_WEDGE + 0.8, ...KW], [T_CH - 0.3, ...KW], [T_BEAT + 0.8, ...KC], [T_NEXT, ...KC],
  [T_BB + 0.6, ...KBB], [T_1700 + 2.0, ...KBB], [T_60 + 0.4, ...KW2], [T_18M - 0.2, ...KW2], [T_SHUT + 1.2, ...KV], [END, KV[0] - 6, KV[1] + 2, KV[2] * 1.03]]);
// ---------- flags (both on every frame; re-placed when the camera changes ground) ----------
const FX = (a, b) => [a, b];
const FLS = [[[1010, 880], [1700, 960], -1, T_INL + 0.3], [[1100, 760], [1770, 600], T_INL, T_CH + 0.3], [[1560, 800], [1680, 600], T_CH, T_1700 + 2.2], [[1180, 650], [1720, 860], T_1700 + 2.0, END + 1]];
FLS.forEach(([us, cs, t, u]) => { const a = flagS(FL.us, "", us[0], us[1], Math.max(0, t), u), b = flagS(FL.cs, "", cs[0], cs[1], Math.max(0, t), u); if (t < 0) { now(a); now(b); } });
// ---------- units ----------
U("u13", "carth", L(31.985, -90.955), "XIII", "XXX"); U("u17", "carth", L(32.075, -90.905), "XVII", "XXX"); U("u15", "carth", L(32.06, -91.10), "XV", "XXX");
U("rv", "rome", L(32.36, -90.84), "PEMBERTON", "XX", 0, { tagAt: T_PEM + 0.1 }); U("re", "rome", L(32.30, -90.70), "", "XX"); U("rj", "rome", L(32.30, -90.24), "JOHNSTON", "XX", 0, { tagAt: T_JOH + 0.3 }); U("rs", "rome", L(32.14, -90.80), "", "XX");
// ---------- m2-8: the real choice ----------
const DEC = E.decide({ sub: "ACROSS THE RIVER · DEEP IN ENEMY COUNTRY", a: "WAIT FOR BANKS", b: "CUT LOOSE", real: 1, t: 0, tReveal: T_CUTL, until: T_CUTL + 1.35 });
const BACK = DEC.previousElementSibling, OA = DEC.querySelector(".o0"), OB = DEC.querySelector(".o1");
[DEC, BACK, OA, OB].forEach((el) => tl.getTweensOf(el).filter((tw) => tw.startTime() < 1.0).forEach((tw) => tw.kill()));
gsap.set(DEC, { autoAlpha: 1, scale: 1 }); gsap.set([OA, OB], { autoAlpha: 1, y: 0 }); gsap.set(BACK, { autoAlpha: 0.56 }); dropCues(0, 1.0);
DEC.style.webkitTextStroke = "2px #000"; DEC.style.paintOrder = "stroke fill"; DEC.style.textShadow = "0 2px 6px rgba(0,0,0,0.9)";
// the supply line back to Grand Gulf (the base) flickers and is cut
const SUP = [GGF, L(32.07, -90.99), L(32.13, -90.92), L(32.10, -90.86), L(32.04, -90.93), L(31.995, -90.955)];
const SUPL = glowPath(SUP, "#6f9bff", 4.5, 0, null, 0, 0.9, { dash: "10 7" }); tl.set(SUPL, { opacity: 0.9 }, 0);
const GGB = boxL("GRAND GULF", GGF[0] - 120, GGF[1] + 40, T_CUTL + 1.4, null, { size: 18 });
tl.to(SUPL, { opacity: 0.15, duration: 0.08, yoyo: true, repeat: 5, ease: "none" }, T_CUTL + 1.5); tl.to(SUPL, { opacity: 0, duration: 0.4 }, T_CUTL + 2.4);
const CUTS = wstampL("CUT LOOSE", ...L(32.12, -90.99), T_CUTL + 1.6, null, "#9fc0ea", 28);
// Sherman's warning: one road, the wagons bunch on it
const SHB = null;   // Sherman's photo sits in his card (a corner badge would have to step out for the card at once)
const ROADP = [GGF, L(32.07, -90.99), L(32.13, -90.92), L(32.10, -90.86), L(32.09, -90.80)];
const RD = glowPath(ROADP, "#ffd27a", 4, T_ROAD - 0.2, T_SET + 0.5, 2, 0.85, { draw: 1.2 });
const WG = [0, 1, 2, 3, 4].map((k) => wagon(sub(ROADP, 0, 0.30 + k * 0.13, 10), T_ROAD - 0.3 + k * 0.2, 2.6, T_SET + 0.4, { s: 17 }));
const SHC = belief("ONE ROAD COULD NOT FEED THE ARMY", "SHERMAN WARNED", T_ROAD - 0.1, T_ANS - 0.2, { size: 50, top: 215 });
SHC.firstElementChild.style.borderTopColor = "#1f4fc4"; SHC.firstElementChild.firstElementChild.style.color = "#9fc0ea";
{ const c = SHC.firstElementChild, ph = document.createElement("div"); c.style.display = "flex"; c.style.alignItems = "center"; c.style.gap = "26px"; c.style.textAlign = "left";
  const txt = document.createElement("div"); while (c.firstChild) txt.appendChild(c.firstChild); c.appendChild(ph); c.appendChild(txt);
  ph.style.cssText = `width:96px;height:96px;border-radius:50%;overflow:hidden;position:relative;flex:none;border:4px solid #f3e7c4;box-shadow:0 0 0 3px #1f4fc4;background:url(${FL.us}) center/cover`;
  ph.innerHTML = `<img src="${PHOTO("sherman")}" style="position:absolute;left:0;right:0;bottom:0;margin:auto;height:112%;filter:grayscale(1) contrast(1.1)">`; }
// Grant's reply (verbatim in the script: quote marks only on that line)
const GRB = cmd("grant", "ULYSSES S. GRANT", "ARMY OF THE TENNESSEE", "carth", "bl", T_ANS - 0.1, T_SET - 0.2);
B.caption("NOT WITH FULL RATIONS", T_FULL - 0.2, T_BREAD - 0.6, "carth");
WG.forEach((w, k) => tl.to(w, { autoAlpha: 0.25, duration: 0.6 }, T_FULL + 0.3 + k * 0.1));
const ICO = { bread: `<svg width="46" height="34" viewBox="0 0 46 34"><rect x="3" y="5" width="40" height="25" rx="4" fill="#e3c88f" stroke="#2a2420" stroke-width="2"/>${[12, 23, 34].map((x) => [12, 22].map((y) => `<circle cx="${x}" cy="${y}" r="2" fill="#8a6a3a"/>`).join("")).join("")}</svg>`,
  coffee: `<svg width="40" height="38" viewBox="0 0 40 38"><path d="M6 10 L30 10 L28 34 L8 34 Z" fill="#b9a27a" stroke="#2a2420" stroke-width="2"/><path d="M30 15 Q38 16 36 23 Q34 28 29 27" fill="none" stroke="#2a2420" stroke-width="2.5"/><path d="M13 7 Q11 3 14 0 M20 7 Q18 3 21 0" stroke="#efe6cf" stroke-width="2" fill="none"/></svg>`,
  salt: `<svg width="34" height="40" viewBox="0 0 34 40"><path d="M5 12 Q5 4 17 4 Q29 4 29 12 L27 38 L7 38 Z" fill="#f3eee2" stroke="#2a2420" stroke-width="2"/><rect x="5" y="16" width="24" height="6" fill="#c9b48a"/></svg>` };
const GRC = scr(`<div style="max-width:1400px;padding:18px 46px 22px;background:rgba(18,16,12,0.93);border-left:8px solid #1f4fc4;font-family:Oswald;color:#f7f3ea;box-shadow:0 20px 40px rgba(0,0,0,.55);text-align:center">
  <div style="font-size:19px;font-weight:700;letter-spacing:.3em;color:#9fc0ea">GRANT ANSWERED</div>
  <div class="l1" style="display:flex;gap:26px;justify-content:center;align-items:center;font-size:40px;font-weight:600;letter-spacing:.06em;margin-top:8px">
    <span class="i0" style="display:flex;align-items:center;gap:10px">${ICO.bread}HARD BREAD</span><span class="i1" style="display:flex;align-items:center;gap:10px">${ICO.coffee}COFFEE</span><span class="i2" style="display:flex;align-items:center;gap:10px">${ICO.salt}SALT</span></div>
  <div class="l2" style="font-size:52px;font-weight:700;line-height:1.15;letter-spacing:.03em;margin-top:12px">“MAKE THE COUNTRY FURNISH THE BALANCE”</div></div>`,
  "left:0;right:0;top:215px;display:flex;justify-content:center;", T_BREAD - 0.2, T_SET - 0.3);
[[".i0", T_BREAD - 0.1], [".i1", T_COF - 0.1], [".i2", T_COF + 0.6], [".l2", T_FURN - 0.1]].forEach(([q, t]) => { const e = GRC.querySelector(q); gsap.set(e, { autoAlpha: 0 });
  tl.fromTo(e, { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.35, immediateRender: false }, t); SFX(q === ".l2" ? "hit" : "ref:pop", t + 0.05); });
tl.fromTo(GRC.querySelector(".l2"), { scale: 1.15 }, { scale: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, T_FURN - 0.1);
// about two days of food; beef and corn found along the way (forage icons pop on the road inland)
B.caption("ABOUT TWO DAYS OF FOOD", T_TWO - 0.1, T_BEEF - 0.2, "carth");
const COW = `<svg width="64" height="45" viewBox="0 0 40 28" style="display:block;overflow:visible;filter:drop-shadow(0 0 4px #ffd27a) drop-shadow(0 1px 2px #000)"><path d="M4 9 Q4 5 9 5 L28 5 Q31 2 34 3 L37 6 Q39 9 35 10 L33 11 L33 18 L30 18 L30 25 L27 25 L27 18 L12 18 L12 25 L9 25 L9 18 Q4 17 4 13 Z" fill="#6b4a2a" stroke="#f3eee2" stroke-width="1.4"/><circle cx="18" cy="11" r="3" fill="#f3eee2"/></svg>`;
const CORN = `<svg width="34" height="59" viewBox="0 0 22 38" style="display:block;overflow:visible;filter:drop-shadow(0 0 4px #ffd27a) drop-shadow(0 1px 2px #000)"><ellipse cx="11" cy="14" rx="6" ry="12" fill="#f1c84a" stroke="#6b4a1a" stroke-width="1.4"/>${[6, 10, 14, 18, 22].map((y) => `<line x1="6" y1="${y}" x2="16" y2="${y}" stroke="#b8902a" stroke-width="1"/>`).join("")}<path d="M11 36 Q3 26 4 12 Q8 24 11 30 Q14 24 18 12 Q19 26 11 36 Z" fill="#6c8a3a" stroke="#2a3a1a" stroke-width="1"/></svg>`;
const ICP = [[COW, L(32.05, -90.84), T_BEEF], [CORN, L(32.11, -90.74), T_CORN - 0.2], [COW, L(32.16, -90.66), T_CORN + 0.4], [CORN, L(32.03, -90.73), T_CORN + 0.9], [COW, L(32.12, -90.58), T_INL + 0.3]];
const ICE = ICP.map(([svg, p, t]) => { const el = pinS(GG.pin(svg, p[0], p[1], { t, pop: true, until: T_PG })); SFX("ref:pop", t + 0.05); return el; });
const MV0 = T_SET + 0.2;
arw({ pts: [L(31.99, -90.95), L(32.04, -90.84), L(32.09, -90.74)], side: "carth", t: MV0, dur: 2.2, width: AW(1.5, 12), until: T_PG });
B.move("u13", MV0, 5, ...L(32.06, -90.82)); B.move("u17", MV0 + 0.3, 5, ...L(32.12, -90.72)); B.move("u15", MV0 + 0.6, 5, ...L(32.02, -90.92));
// ---------- m2-9: the wedge between Pemberton and Johnston ----------
const W1 = arw({ pts: LL([[32.08, -90.80], [32.13, -90.65], [32.21, -90.50], [32.27, -90.42]]), side: "carth", t: T_WEDGE - 0.4, dur: 2.0, width: AW(1.72, 14), until: T_WEST + 0.5 });
B.move("u17", T_WEDGE - 0.3, 3.5, ...L(32.20, -90.54)); B.move("u13", T_WEDGE - 0.1, 3.5, ...L(32.17, -90.68)); B.move("u15", T_WEDGE + 0.1, 4, ...L(32.10, -90.70));
B.move("rs", T_WEDGE, 2.5, ...L(32.27, -90.74));
K.target(VKS[0], VKS[1], T_PEM, { r: 30, side: "rome", until: T_PEM + 2.4 }); K.target(JAX[0], JAX[1], T_JOH + 0.2, { r: 30, side: "rome", until: T_JOH + 2.6 });
const JTW = townL("JACKSON", JAX, "r", T_JOH + 0.2); const VTW = townL("VICKSBURG", VKS, "l", T_PEM);
// two red armies cannot join: dashed red arrows toward each other, blocked by the wedge
const J1 = arw({ pts: [L(32.29, -90.26), L(32.29, -90.36), L(32.28, -90.44)], side: "rome", t: T_ONE - 0.4, dur: 1.0, width: AW(1.72, 11), dash: "12 9", until: T_PG + 1 });
const J2 = arw({ pts: [L(32.33, -90.80), L(32.31, -90.68), L(32.29, -90.60)], side: "rome", t: T_ONE - 0.2, dur: 1.0, width: AW(1.72, 11), dash: "12 9", until: T_PG + 1 });
B.greyArrow(J1, T_ONE + 0.9, T_PG + 0.8); B.greyArrow(J2, T_ONE + 1.0, T_PG + 0.8);
// the five battles: one stamp per spoken name + its date (dates under the names = the narrator's dates)
const BAT = (txt, p, t, sub, dx = 0, dy = -34) => { K.target(p[0], p[1], t, { r: 26, side: "rome", until: t + 2.6 }); return wstampL(txt, p[0] + dx, p[1] + dy, t, null, "#e3232f", 30, sub); };
BAT("PORT GIBSON", PG, T_PG, "1 MAY");
BAT("RAYMOND", RAY, T_RAY, "12 MAY", 0, 40);
B.move("u17", T_RAY - 0.4, 1.4, ...L(32.25, -90.44));
B.move("rj", T_RAY + 0.3, 1.0, ...L(32.27, -90.30));
const AJ = arw({ pts: [L(32.25, -90.43), L(32.29, -90.33), L(32.30, -90.22)], side: "carth", t: T_JAX - 0.4, dur: 1.0, width: AW(1.72, 14), until: T_WEST + 0.6 });
B.move("u17", T_JAX - 0.2, 1.2, ...L(32.30, -90.21)); B.move("u15", T_JAX - 0.3, 1.6, ...L(32.27, -90.24));
B.move("rj", T_JAX + 0.1, 1.6, ...L(32.45, -90.10));
BAT("JACKSON", JAX, T_JAX + 0.1, "14 MAY", 0, -62);
tl.to(B.units.rj.el, { autoAlpha: 0, duration: 0.6 }, T_WEST);
const AW1 = arw({ pts: LL([[32.30, -90.21], [32.34, -90.32], [32.35, -90.46], [32.34, -90.52]]), side: "carth", t: T_WEST - 0.1, dur: 1.4, width: AW(1.72, 14), until: T_CH + 2 });
// Champion Hill layout (spaced for reading at s 2.7): Confederates west of the hill on a N-S line, the Union on and east of it
B.move("u17", T_WEST, 2.0, ...L(32.335, -90.515)); B.move("u15", T_WEST + 0.3, 2.4, ...L(32.40, -90.47)); B.move("u13", T_WEST + 0.2, 2.0, ...L(32.29, -90.53));
B.move("rv", T_WEST, 1.8, ...L(32.36, -90.585)); B.move("re", T_WEST + 0.2, 1.8, ...L(32.325, -90.59)); B.move("rs", T_WEST + 0.2, 1.8, ...L(32.29, -90.595));
// ---------- Champion Hill (16 May): close-up ----------
// option 2 front between the lines (Union east, red west); slides west as the Confederates are pushed off the hill
const FCH = front2(LL([[32.405, -90.563], [32.37, -90.565], [32.335, -90.567], [32.30, -90.570], [32.265, -90.572]]), KC[2], T_BEAT - 0.2,
  { flip: true, dur: 1.4, until: T_NEXT - 0.3, to: LL([[32.405, -90.625], [32.37, -90.628], [32.335, -90.632], [32.30, -90.630], [32.265, -90.620]]), moveT: T_CUTOFF - 1.0, moveDur: 2.2 });
BAT("CHAMPION HILL", L(32.40, -90.60), T_CH + 0.1, "16 MAY", 0, 0);
const CHB = cmd("pemberton", "JOHN C. PEMBERTON", "CONFEDERATE ARMY", "rome", "tr", T_BEAT - 0.1, T_15 - 0.3);
const sCH = KC[2];
U("hv", "carth", L(32.375, -90.52), "", "XX", T_BIG - 0.4); B.move("hv", T_BIG - 0.3, 2.0, ...L(32.365, -90.545));
B.move("u17", T_BIG, 2.0, ...L(32.33, -90.545)); B.move("u13", T_BIG, 2.5, ...L(32.29, -90.55));
[[T_BEAT + 0.6, [32.335, -90.522], [32.36, -90.58]], [T_BIG + 0.8, [32.332, -90.535], [32.325, -90.585]], [T_BIG + 2.0, [32.29, -90.545], [32.29, -90.59]], [T_15 - 0.6, [32.365, -90.54], [32.36, -90.58]]]
  .forEach(([t, a, b]) => mg(L(...a), L(...b), t, 5, 1.1 / sCH * 2.2));   // musketry between the lines (positions at that moment)
shootS(L(32.33, -90.505), L(32.335, -90.575), T_BEAT + 1.4, sCH, { dur: 0.7, h: 30, r: 9 });
shootS(L(32.32, -90.60), L(32.345, -90.54), T_BIG + 1.6, sCH, { dur: 0.7, h: 30, r: 9 });
// 15,000 fully engaged vs 25,000 Confederates
const vs = (kick, aNum, aSub, bNum, bSub, t, tA, tB, until, o = {}) => {   // o.redFirst: the red column on the left
  const el = scr(`<div style="background:rgba(18,16,12,0.93);border-top:5px solid #c9b48a;font-family:Oswald;font-weight:700;color:#f7f3ea;box-shadow:0 20px 40px rgba(0,0,0,.55);text-align:center"><div style="padding-top:10px;font-size:19px;letter-spacing:.32em;color:#c9b48a">${kick}</div><div style="display:flex;gap:0">
    <div class="a" style="padding:14px 40px 16px;border-bottom:6px solid ${o.redFirst ? "#be3a2a" : "#2e5cb2"};min-width:360px"><div style="font-size:58px;letter-spacing:.03em;line-height:1.05">${aNum}</div><div style="font-size:18px;letter-spacing:.24em;color:${o.redFirst ? "#ff8a80" : "#9fc0ea"}">${aSub}</div></div>
    <div style="align-self:center;font-size:30px;color:#c9b48a;padding:0 10px">VS</div>
    <div class="b" style="padding:14px 40px 16px;border-bottom:6px solid ${o.redFirst ? "#2e5cb2" : "#be3a2a"};min-width:360px"><div style="font-size:58px;letter-spacing:.03em;line-height:1.05">${bNum}</div><div style="font-size:18px;letter-spacing:.24em;color:${o.redFirst ? "#9fc0ea" : "#ff8a80"}">${bSub}</div></div></div></div>`,
    o.css || "left:0;right:0;bottom:150px;display:flex;justify-content:center;", t, until);
  [[".a", tA], [".b", tB]].forEach(([q, tt]) => { const e = el.querySelector(q); gsap.set(e, { autoAlpha: 0 }); tl.fromTo(e, { autoAlpha: 0, scale: 1.2 }, { autoAlpha: 1, scale: 1, duration: 0.3, immediateRender: false }, tt); SFX("hit", tt + 0.1); });
  return el; };
const V1 = vs("CHAMPION HILL", "ABOUT 15,000", "FULLY ENGAGED", "ABOUT 25,000", "CONFEDERATES", T_15 - 0.2, T_15 - 0.1, T_25, T_DIV - 0.3);
// one Union division lost more than a third of its men
const hvB = B.units.hv.el.querySelector(".blk");
tl.to(hvB, { scale: 1.35, duration: 0.25, yoyo: true, repeat: 3 }, T_DIV + 0.1);
const DRN = pinS(GG.pin(`<div style="width:72px;height:12px;background:#1f4fc4;border:2px solid #f3eee2;box-shadow:0 1px 4px #000;position:relative;overflow:hidden"><div class="d" style="position:absolute;right:0;top:0;bottom:0;width:0;background:#77746c"></div></div>`, ...L(32.3835, -90.545), { t: T_DIV + 0.1, until: T_CUTOFF + 0.2 }));
tl.to(DRN.querySelector(".d"), { width: "38%", duration: 1.0, ease: "power2.out" }, T_THIRD);
B.caption("MORE THAN A THIRD OF ITS MEN", T_THIRD - 0.1, T_CUTOFF - 0.3, "carth");
// a whole Confederate division cut off: it is pushed south-east, its road back to Vicksburg greys
B.move("rv", T_CUTOFF - 1.0, 2.2, ...L(32.36, -90.66)); B.move("re", T_CUTOFF - 0.9, 2.2, ...L(32.325, -90.665));
B.move("rs", T_CUTOFF - 0.2, 2.6, ...L(32.245, -90.575));
arw({ pts: [L(32.345, -90.60), L(32.345, -90.63), L(32.35, -90.655)], side: "rome", t: T_CUTOFF - 1.0, dur: 1.0, width: AW(sCH, 11), until: T_NEXT });
const NEV = arw({ pts: [L(32.245, -90.59), L(32.27, -90.66), L(32.30, -90.74)], side: "rome", t: T_NEVER - 0.3, dur: 1.0, width: AW(sCH, 11), dash: "12 9", until: T_NEXT + 0.4 });
B.greyArrow(NEV, T_NEVER + 0.9, T_NEXT + 0.4);
wstampL("CUT OFF", ...L(32.215, -90.545), T_CUTOFF + 0.5, null, "#e3232f", 30);
tl.to(B.units.rs.el, { autoAlpha: 0, duration: 0.8 }, T_NEXT + 0.4);
// ---------- Big Black River (17 May) ----------
const BBRIV = LL([[32.47, -90.62], [32.42, -90.67], [32.38, -90.70], [32.347, -90.716], [32.31, -90.74], [32.27, -90.78]]);
B.move("rv", T_NEXT - 0.4, 1.4, ...L(32.36, -90.70)); B.move("re", T_NEXT - 0.3, 1.4, ...L(32.325, -90.705));
B.move("u13", T_NEXT, 1.8, ...L(32.36, -90.66)); B.move("u17", T_NEXT + 0.2, 1.8, ...L(32.32, -90.655)); tl.to(B.units.hv.el, { autoAlpha: 0, duration: 0.5 }, T_NEXT);
BAT("BIG BLACK RIVER", L(32.405, -90.715), T_BB - 0.1, "THE NEXT DAY", 0, 0);
mg(L(32.36, -90.665), L(32.36, -90.70), T_BB + 0.6, 5, 1.1 / KBB[2] * 2.2); shootS(L(32.34, -90.67), L(32.347, -90.712), T_BB + 1.0, KBB[2], { dur: 0.6, h: 30, r: 9 });
fireGlowS(BBR[0] - 2, BBR[1], 10, T_BB + 1.4, T_1700 + 2.0);
// option 2: once the Confederates are back across, the Big Black River is the line (Union east, red west)
front2(BBRIV, KBB[2], T_18G - 0.1, { flip: true, dur: 1.4, until: T_COUNT + 0.4 });
B.move("rv", T_18G - 0.2, 1.6, ...L(32.37, -90.78)); B.move("re", T_18G, 1.6, ...L(32.33, -90.785));
const BBC = scr(`<div style="display:flex;gap:40px;padding:14px 40px 16px;background:rgba(18,16,12,0.93);border-top:5px solid #2e5cb2;font-family:Oswald;font-weight:700;color:#f7f3ea;box-shadow:0 20px 40px rgba(0,0,0,.55);text-align:center">
  <div class="a"><div style="font-size:60px;line-height:1.05">18</div><div style="font-size:18px;letter-spacing:.26em;color:#9fc0ea">GUNS</div></div>
  <div class="b"><div style="font-size:60px;line-height:1.05">1,700+</div><div style="font-size:18px;letter-spacing:.26em;color:#9fc0ea">PRISONERS</div></div></div>`,
  "left:0;right:0;top:215px;display:flex;justify-content:center;", T_18G - 0.2, T_COUNT - 0.3);
{ const b = BBC.querySelector(".b"); gsap.set(b, { autoAlpha: 0 }); tl.fromTo(b, { autoAlpha: 0, scale: 1.2 }, { autoAlpha: 1, scale: 1, duration: 0.3, immediateRender: false }, T_1700 - 0.5); SFX("hit", T_18G); SFX("hit", T_1700 - 0.4); }
// ---------- m2-10: the numbers ----------
const V2 = vs("GRANT HIMSELF COUNTED", "OVER 60,000", "CONFEDERATES IN MISSISSIPPI", "ABOUT 33,000", "OF HIS OWN", T_60 - 0.3, T_60 - 0.2, T_33, T_18D - 0.2, { redFirst: true });
B.caption("IN EIGHTEEN DAYS", T_18D, T_FIVE - 0.2, "carth");
[PG, RAY, JAX, CH, BBR].forEach((p, k) => K.target(p[0], p[1], T_DETAIL + k * 0.35, { r: 22, side: "carth", until: T_DETAIL + 2.2 + k * 0.35 }));
const CK = ticker("THE FIVE BATTLES COST HIM", 4500, "", "right:110px;top:260px;display:flex;justify-content:center;", T_FIVE - 0.1, 1.2, T_18M - 0.2, 7, { col: "#7fb0ff", sub: "MEN · FEWER THAN" });
{ const v = CK.querySelector(".v"), sb = CK.querySelector(".v").nextElementSibling; sb.textContent = "MEN"; const pre = document.createElement("div");
  pre.style.cssText = "font-size:20px;letter-spacing:.3em;color:#f7f3ea"; pre.textContent = "FEWER THAN"; v.parentNode.insertBefore(pre, v); gsap.set(pre, { autoAlpha: 0 });
  tl.to(pre, { autoAlpha: 1, duration: 0.3 }, T_4500 - 0.1); }
// 18 May: Pemberton's army shut inside Vicksburg; the ring closes
B.move("u13", T_COUNT, 6, ...L(32.33, -90.80)); B.move("u17", T_COUNT + 0.3, 6, ...L(32.37, -90.80)); B.move("u15", T_COUNT + 0.5, 6, ...L(32.42, -90.82));
B.move("rv", T_COUNT + 1, 5, ...L(32.345, -90.852)); tl.to(B.units.re.el, { autoAlpha: 0, duration: 0.8 }, T_COUNT + 3);
const RING = LL([[32.405, -90.875], [32.40, -90.835], [32.37, -90.82], [32.335, -90.825], [32.30, -90.845], [32.28, -90.88], [32.29, -90.905]]);
glowPath(RING, "#4f8bff", 5, T_18M + 0.3, END + 1, 0, 0.95, { draw: T_SHUT - T_18M + 0.4 });
wstampL("SHUT INSIDE VICKSBURG", ...L(32.43, -90.66), T_SHUT + 0.2, null, "#e3232f", 28);
const VTW2 = townL("VICKSBURG", L(32.352, -90.878), "l", T_18M + 0.3);
// ---------- 1c declutter: one big card at a time ----------
declutter([LGD, LGS, LGL, GRB, CHB], [[0.2, T_ANS - 0.2], [T_BREAD - 0.2, T_SET - 0.3], [T_15 - 0.2, T_DIV - 0.3], [T_18G - 0.2, T_COUNT - 0.3],
  [T_60 - 0.3, T_18D - 0.2], [T_FIVE - 0.1, T_18M - 0.2]]);
gsap.set(LGD, { filter: "opacity(0)" });   // frame 0: the m2e decision card is still up, the legend is stepped out
fixImgs();
K.raiseTerritory();
B.finish();
