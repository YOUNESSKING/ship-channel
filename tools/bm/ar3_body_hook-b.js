// HOOK-B (hook-3 .. hook-4), Benedict Arnold #17. THE LOCKED HOOK (STYLE_LOCK 1a: back INTO the danger, the general enters as the TURN,
// name slam + 3 snap cuts + title; 1c: nothing before it is spoken, one big card at a time, visible fire only). Map agent ar3_.
// Built with: python3 tools/ar3_inline.py hook-b hook-3 hook-4      (world = saratoga map px; snap-cut maps `quebec`, `valcour` = full-size
// layers at the world origin, each shown only inside its cut; a black frame hides every camera jump)
// hook-3: frame 0 = hook-a's last frame (the British line broken at the German redoubt, the "?" badge); "But on the afternoon": rewind
//   (whoosh), the arrow pulls back, the British step back into their camp; 7 OCTOBER 1777 on the date; ~1,500 British + Germans march out
//   with cannon into the wheat field in front of the American left; "The general who had fought them hardest": the "?" in the American camp;
//   "quarrelled with his commander, Horatio Gates": Gates's badge + HQ, a red crack between them; WITHOUT A COMMAND; "When the guns opened":
//   the British guns fire (visible), musket volleys; "he rode out": the "?" rides out (dotted trail); "An officer was reportedly sent after
//   him": a second rider follows (REPORTEDLY), falls behind and stops.
// hook-4: the map dims, the "?" comes to the centre and becomes the portrait (initials until arnold_head.png exists); BENEDICT ARNOLD slams;
//   "Three years later": 1780; WEST POINT; TRAITOR (dark stamp) only on "traitor"; 3 snap cuts (whoosh + hit): 1 QUEBEC 1775 (snow, the
//   walled city), 2 VALCOUR ISLAND 1776 (the boats behind the island), 3 SARATOGA 1777 (blue arrow into the redoubt); title card (riser + boom).
// Facts: FACT_NOTES (7 Oct over 1,500; no command; Armstrong "reportedly"; West Point 1780). Nobody named before the narrator names him.
// @@KIT
const H3 = "hook-3", H4 = "hook-4", S4 = B.P(H4);
const T_AFT = at(H3, "the afternoon"), T_7 = at(H3, "seventh of October"), T_NOT = at(H3, "did not look like a victory"), T_1500 = at(H3, "fifteen hundred"),
  T_MARCH = at(H3, "had marched out"), T_CAN = at(H3, "with cannon"), T_FIELDS = at(H3, "into the fields"), T_LEFT = at(H3, "the American left"),
  T_GEN = at(H3, "The general who"), T_WEEKS = at(H3, "three weeks before"), T_QUAR = at(H3, "quarrelled"), T_GATES = at(H3, "Horatio Gates"),
  T_WITH = at(H3, "without a command"), T_GUNS = at(H3, "guns opened") + 0.25, T_RODE = at(H3, "he rode out"), T_ANY = at(H3, "anyway"),
  T_OFF = at(H3, "An officer"), T_REP = at(H3, "reportedly"), T_BACK = at(H3, "bring him back"), T_CATCH = at(H3, "did not catch up"), T_OVER = at(H3, "it was over");
const T_NAME = at(H4, "Benedict Arnold."), T_3Y = at(H4, "Three years later"), T_WP = at(H4, "West Point"), T_WORD = at(H4, "another word"),
  T_TRAIT = at(H4, "traitor"), T_BEFORE = at(H4, "But before that"), T_MAR = at(H4, "had marched an army"), T_QUE = at(H4, "to Quebec"),
  T_FLEET = at(H4, "He had built a fleet"), T_NAVY = at(H4, "the Royal Navy"), T_LAKE = at(H4, "Lake Champlain"), T_SAR = at(H4, "And at Saratoga"),
  T_BROKE = at(H4, "he broke"), T_THESE = at(H4, "These are"), T_GREAT = at(H4, "three greatest");
// =====================================================================================================================
// THE WORLD
// =====================================================================================================================
const layer = (src) => { const g = document.createElement("div"); g.style.cssText = "position:absolute;left:0;top:0;width:2880px;height:1620px;";
  const i = document.createElement("img"); i.src = src; i.alt = ""; i.style.cssText = "position:absolute;left:0;top:0;width:100%;height:100%;"; g.appendChild(i);
  WORLD.insertBefore(g, OVL); gsap.set(g, { autoAlpha: 0 }); return g; };
const LQU = layer("assets/ar3_quebec.jpg"), LVA = layer("assets/ar3_valcour.jpg");
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); const NA = LV.north(); NA.style.top = "330px";
CLAMP = true;
const scr0 = (html, css) => { const el = document.createElement("div"); el.style.cssText = "position:absolute;" + css; el.innerHTML = html; SCN.insertBefore(el, document.getElementById("credit")); GG.hide(el); return el; };
const vis = (t0, t1) => (el) => { gsap.set(el, { autoAlpha: 0 }); tl.set(el, { autoAlpha: 1 }, t0); if (t1 != null) tl.set(el, { autoAlpha: 0 }, t1 - 0.01); return el; };
const PINS = document.getElementById("pins");
const snap = () => new Set([...OVL.children, ...PINS.children]);
const endScope = (s0, until) => { const els = [...OVL.children, ...PINS.children].filter((e) => !s0.has(e) && e.tagName.toLowerCase() !== "defs"); tl.set(els, { autoAlpha: 0 }, until - 0.01); };
// ---------- places (saratoga px) ----------
const BRY = [1338, 542], LIR = [1417, 651], WF = [1205, 955];
const AMLINE = [[1300, 1185], [1420, 1195], [1560, 1215], [1700, 1250], [1830, 1290]];
const CAMPL = [[1440, 655], [1560, 668], [1700, 660], [1850, 640], [2000, 610], [2150, 560]];
const QCAMP = [1540, 1250], HQ = [1745, 1320];
// =====================================================================================================================
// FRAME 0 = hook-a's last frame (keep in sync with tools/ar3_body_hook-a.js): the British line broken at the German redoubt
// =====================================================================================================================
const CE = [1420, 860], SE = 1.35;
camSet(CE, SE);
const DS = document.getElementById("date"), d0 = document.createElement("div"); d0.className = "d"; d0.textContent = "OCTOBER 1777"; d0.style.fontSize = "32px"; DS.appendChild(d0);
const RB = redoubt(...BRY, null, null, { s: 56, open: "n" }), RL = redoubt(...LIR, null, null, { s: 56 }); gsap.set([RB, RL], { autoAlpha: 1 });
const CL = glowPath(CAMPL, "#bc2528", 5 / SE, 0, null, 0, 0.7); tl.set(CL, { opacity: 0.7 }, 0); gsap.set(CL, { opacity: 0.7 });
const AL = glowPath(AMLINE, "#2c57b7", 5 / SE, 0, null, 0, 0.7); tl.set(AL, { opacity: 0.7 }, 0); gsap.set(AL, { opacity: 0.7 });
const R0 = { r1: [1300, 575], r2: [1400, 690], r3: [1480, 690], rg: [1450, 655] };
Object.entries(R0).forEach(([id, p]) => { unitS(id, "rome", p, id === "rg" ? "artillery" : "infantry", "", id === "rg" ? { w: 44, h: 29 } : {}); gsap.set(B.units[id].el, { autoAlpha: 1 }); });
const AU = [unitS("a1", "carth", [1380, 1170], "infantry", ""), unitS("a2", "carth", [1560, 1200], "infantry", ""), unitS("a3", "carth", [1700, 1235], "infantry", "")];
AU.forEach((id) => gsap.set(B.units[id].el, { autoAlpha: 1 }));
const F0 = [flagS(FL.us, "", 1800, 1140, null, T_GEN + 0.2), flagS(FL.gb, "", 1760, 560, null, T_GEN + 0.2)]; gsap.set(F0, { autoAlpha: 1 });
const QB = atZero(qBadge("THE MAN", "", 0, null, { corner: "bl" }), null);
const LGD = atZero(legend(0, null, true), null);
// =====================================================================================================================
// hook-3: rewind to the afternoon of 7 October
// =====================================================================================================================
go("r1", 0.5, 1.4, [1320, 690]); go("r2", 0.55, 1.4, [1360, 705]); go("r3", 0.6, 1.4, [1400, 715]); go("rg", 0.6, 1.4, [1360, 735]);
tl.to(d0, { autoAlpha: 0, y: -14, duration: 0.3 }, T_7 - 0.3); for (let k = 0; k < 3; k++) SFX("tick", T_7 - 0.5 + k * 0.13);
dateSet("7 OCTOBER 1777", T_7, T_3Y - 0.05);
camTo(0, T_1500, [1330, 880], 1.5, "sine.inOut");
pulse(T_NOT + 0.4); SFX("ref:pop", T_NOT + 0.4);
// ~1,500 British and German troops march out of the camp, with cannon, into the fields in front of the American left
const N15 = numCard("ABOUT", "1,500", "BRITISH AND GERMAN", "right:110px;top:300px;", T_1500 - 0.05, T_1500 + 2.6, { col: "#e3232f", lc: "#ff8a80", vs: 56 });
const LINE = { r1: [1110, 930], r2: [1200, 952], r3: [1292, 975], rg: [1205, 912] };
Object.entries(LINE).forEach(([id, p], k) => go(id, T_MARCH - 0.1 + k * 0.12, 3.4, p));
[[[1320, 720], [1200, 860], [1120, 915]], [[1370, 730], [1300, 880], [1285, 955]]].forEach((pts, k) => arw({ pts, side: "rome", t: T_MARCH + k * 0.15, dur: 1.4, width: AW(1.5, 12), until: T_GEN }));
tl.fromTo(B.units.rg.el.querySelector(".blk"), { scale: 1 }, { scale: 1.35, duration: 0.2, yoyo: true, repeat: 1, immediateRender: false }, T_CAN); SFX("ref:pop", T_CAN);
const WFP = [[1060, 905], [1170, 880], [1320, 905], [1345, 990], [1240, 1025], [1080, 1005]];
const wf = document.createElementNS(NS, "polygon"); wf.setAttribute("points", WFP.map((q) => q.join(",")).join(" ")); wf.setAttribute("fill", "rgba(232,200,90,0.32)");
wf.setAttribute("stroke", "#e8c85a"); wf.setAttribute("stroke-width", 2.4 / 1.5); wf.setAttribute("stroke-dasharray", "6 4"); OVL.insertBefore(wf, OVL.firstChild); gsap.set(wf, { opacity: 0 });
tl.to(wf, { opacity: 1, duration: 0.6 }, T_FIELDS - 0.05); tl.to(wf, { opacity: 0.5, duration: 1 }, T_FIELDS + 3);
glowPath(AMLINE.slice(0, 3), "#8fb2ff", 9 / 1.5, T_LEFT - 0.05, T_GEN + 1, 2, 0.95, { draw: 0.6, top: true });
tagL("THE AMERICAN LEFT", 1330, 1140, T_LEFT, null, 15);
// "The general who had fought them hardest three weeks before": the "?" in the American camp
camTo(T_GEN - 0.5, 2.2, [1440, 1060], 1.55, "sine.inOut");
// both flags stay through the name slam (dimmed with the map) until the first snap cut; the Union Flag on the British side, clear of the legend
const F1 = [flagS(FL.us, "", 1620, 1360, T_GEN - 0.2, null), flagS(FL.gb, "", 1180, 880, T_GEN - 0.2, null)];
const QM = pinS(GG.pin(RIDER("?", "#1f4fc4", 72), ...QCAMP, { t: T_GEN + 0.1, pop: true, until: T_NAME - 1.4 }));
SFX("ref:pop", T_GEN + 0.15);
tl.to(QB, { scale: 1.06, duration: 0.25, yoyo: true, repeat: 1, transformOrigin: "0% 100%" }, T_GEN + 0.1);
tl.to(QM.firstElementChild, { scale: 1.2, duration: 0.25, yoyo: true, repeat: 1 }, T_WEEKS);
// "had quarrelled with his commander, Horatio Gates": Gates's HQ + badge, a red crack between the two
const GM = faceMarker("gates", "HG", "carth", ...HQ, T_GATES - 0.05, T_NAME - 1.4, 76);
const GB = pbadge("HORATIO GATES", "", "gates", "carth", "tr", "HG", T_GATES, T_NAME - 1.4);
const CRACK = glowPath([[QCAMP[0] + 40, QCAMP[1] + 10], [1590, 1290], [1620, 1265], [1650, 1305], [1690, 1290], [HQ[0] - 38, HQ[1] - 4]], "#ff3b30", 4 / 1.55, T_QUAR - 0.05, T_GUNS, 2, 1, { draw: 0.5, top: true });
SFX("hit", T_QUAR + 0.1); K.shake(T_QUAR + 0.1, 2, 0.2);
const WC = sstamp("WITHOUT A COMMAND", 760, T_WITH - 0.05, { size: 64, until: T_GUNS - 0.15, shake: 4 });
pulse(T_WITH + 0.2);
tl.to(QM.firstElementChild, { filter: "grayscale(1) brightness(0.7)", duration: 0.4 }, T_WITH + 0.1);
// "When the guns opened": the British guns in the wheat field fire (visible), volleys along the line
camTo(T_GUNS - 0.4, 2.0, [1350, 1060], 1.5, "sine.inOut");
// the red guns fire on "opened": big readable muzzle flashes + smoke at the gun (2 shots, 2.2 s apart), then musket volleys along the line
[T_GUNS, T_GUNS + 2.2].forEach((t) => { K.gun(LINE.rg[0], LINE.rg[1], t, { unit: "rg", dx: 6, dy: 10 }); flashW(LINE.rg[0] + 4, LINE.rg[1] + 14, t, 6.5); flashW(LINE.rg[0] + 10, LINE.rg[1] + 22, t + 0.06, 4.0);
  smokeLine([LINE.rg[0] - 6, LINE.rg[1] + 22], [LINE.rg[0] + 22, LINE.rg[1] + 28], t + 0.08, 3, 34); tl.fromTo(B.units.rg.el.querySelector(".blk"), { x: 0 }, { x: -5, duration: 0.08, yoyo: true, repeat: 1, immediateRender: false }, t); });
[[T_GUNS + 1.1, [1120, 950], [1290, 990]], [T_OFF + 0.6, [1130, 955], [1280, 990]], [T_CATCH, [1110, 950], [1295, 995]]]
  .forEach(([t, a, b]) => { volley(a, b, t, 6, 1.9); smokeLine([a[0], a[1] + 14], [b[0], b[1] + 14], t + 0.05, 4, 28); });
// "he rode out to the fighting anyway": the "?" rides out (dotted trail)
tl.to(QM.firstElementChild, { filter: "grayscale(0) brightness(1)", duration: 0.3 }, T_RODE - 0.1);
const RIDE = [QCAMP, [1490, 1180], [1420, 1120], [1350, 1070], [1290, 1035], [1250, 1010]];
pinAlong(QM, RIDE, T_RODE, T_OFF - T_RODE + 0.6, 16);
trail(RIDE, "#9fc0ea", 2.4 / 1.5, T_RODE, T_OFF - T_RODE + 0.6, T_NAME - 1.4, "3 7");
// "An officer was reportedly sent after him": a second, plain rider follows from the HQ, falls behind and stops
const OM = pinS(GG.pin(RIDER(HORSE(38), "#1f4fc4", 58), ...HQ, { t: T_OFF - 0.05, pop: true, until: T_NAME - 1.4 }));
const OR = [HQ, [1650, 1250], [1580, 1215], [1520, 1180], [1480, 1150]];
pinAlong(OM, OR, T_OFF + 0.1, T_CATCH - T_OFF + 1.0, 14);
trail(OR, "#c9d6ea", 1.8 / 1.5, T_OFF + 0.1, T_CATCH - T_OFF + 1.0, T_NAME - 1.4, "2 8");
tagL("REPORTEDLY", 1600, 1170, T_REP, null, 14);
tl.to(OM.firstElementChild, { opacity: 0.55, duration: 0.6 }, T_OVER);
camTo(T_OFF - 0.3, T_OVER - T_OFF + 0.6, [1380, 1080], 1.45, "sine.inOut");
// =====================================================================================================================
// hook-4: the name slam (the "?" becomes the portrait), 1780, WEST POINT, TRAITOR
// =====================================================================================================================
const DK = scr0("", "inset:0;background:rgba(5,7,13,0.62);"); tl.fromTo(DK, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.5, immediateRender: false }, S4 - 0.2);
const BDG = scr0(`<div style="position:relative;width:300px;height:300px;border-radius:50%;overflow:hidden;border:9px solid #f3e7c4;box-shadow:0 0 0 7px #1f4fc4,0 24px 48px rgba(0,0,0,0.75);background:url(${FL.us}) center/cover">
  <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle, rgba(10,12,24,0.8), rgba(10,12,24,0.55));font-family:Oswald;font-weight:700;font-size:120px;color:#f7f3ea">BA</div>
  <img src="${PHOTO("arnold")}" onload="this.previousElementSibling.style.display='none'" style="position:absolute;left:0;right:0;bottom:0;margin:auto;height:112%;filter:grayscale(1) contrast(1.1)">
  <div class="q" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle, rgba(10,12,24,1), rgba(10,12,24,0.94));font-family:Oswald;font-weight:700;font-size:180px;color:#f7f3ea">?</div></div>`,
  "left:810px;top:130px;transform-origin:50% 50%;");
tl.fromTo(BDG, { autoAlpha: 0, scale: 0.4, x: -620, y: 520 }, { autoAlpha: 1, scale: 1, x: 0, y: 0, duration: 0.55, ease: "power3.out", immediateRender: false }, S4 - 0.1);
tl.to(QB, { autoAlpha: 0, duration: 0.2 }, S4 - 0.1);
SFX("ref:whoosh", S4 - 0.1);
tl.to(BDG.querySelector(".q"), { autoAlpha: 0, duration: 0.15 }, T_NAME - 0.25);
const NAME = scr(`<div style="padding:12px 44px 14px;background:rgba(18,16,12,0.95);border-top:7px solid #1f4fc4;color:#f7f3ea;font-family:Oswald;font-weight:700;text-align:center;box-shadow:0 14px 30px rgba(0,0,0,.6)"><div style="font-size:96px;letter-spacing:0.08em;line-height:1.1">BENEDICT ARNOLD</div></div>`,
  "left:0;right:0;top:480px;display:flex;justify-content:center;transform-origin:50% 40%;", T_NAME - 0.15, null, { autoAlpha: 0 });
slam(NAME, T_NAME - 0.15, { from: 1.9, shake: 6, until: T_3Y - 0.1 }); pulse(T_NAME + 0.1);
// "Three years later ... West Point ... traitor"
tl.to(BDG, { x: -520, y: 80, scale: 0.8, duration: 0.5, ease: "power3.inOut" }, T_3Y - 0.1);
dateSet("1780", T_3Y, T_MAR - 0.12);
for (let k = 0; k < 3; k++) SFX("tick", T_3Y - 0.3 + k * 0.12);
const WPC = placeCard("THREE YEARS LATER", "WEST POINT", "right:200px;top:330px;", T_WP - 0.05, T_TRAIT - 0.2);
SFX("ref:pop", T_WP);
const TRA = scr(stampHTML("TRAITOR", "#1a1a1a", 120, -7).replace("background:rgba(14,12,10,0.78)", "background:rgba(200,190,170,0.92)"), "left:0;right:0;top:420px;display:flex;justify-content:center;transform-origin:50% 50%;", T_TRAIT - 0.05, null, { autoAlpha: 0 });
slam(TRA, T_TRAIT - 0.05, { from: 2.4, shake: 7, until: T_MAR - 0.15 }); pulse(T_TRAIT + 0.2);
tl.to(BDG, { filter: "grayscale(1) brightness(0.55)", duration: 0.3 }, T_TRAIT + 0.1); tl.to(BDG, { filter: "none", duration: 0.4 }, T_BEFORE);
// =====================================================================================================================
// the three snap cuts (whoosh + hit; a black frame hides each camera jump)
// =====================================================================================================================
const CUTB = scr0("", "inset:0;background:#030406;");
const cut = (t, lay, until, c, s, drift) => {
  tl.fromTo(CUTB, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.05, immediateRender: false }, t - 0.06); tl.to(CUTB, { autoAlpha: 0, duration: 0.16 }, t + 0.04);
  if (lay) { tl.set(lay, { autoAlpha: 1 }, t - 0.01); tl.set(lay, { autoAlpha: 0 }, until - 0.01); }
  camTo(t, 0.01, c, s); camTo(t + 0.02, until - t - 0.05, [c[0] + drift[0], c[1] + drift[1]], s * (drift[2] || 1.06), "sine.out");
  SFX("ref:whoosh", t - 0.2); SFX("hit", t + 0.02); K.shake(t + 0.02, 3, 0.25); };
const T1 = T_MAR - 0.08, T2 = T_FLEET - 0.08, T3 = T_SAR - 0.08, T4 = T_THESE - 0.1;
tl.set([DK, BDG, RELIEF], { autoAlpha: 0 }, T1 - 0.01);
const S0 = snap(); tl.set([...S0].filter((e) => e.tagName.toLowerCase() !== "defs"), { autoAlpha: 0 }, T1 - 0.01);
tl.set(Object.values(B.units).map((u) => u.el), { autoAlpha: 0 }, T1 - 0.01);
tl.set(LGD, { autoAlpha: 0 }, T1 - 0.01);
// Arnold's corner badge: Continental Colours behind him for the 1775 / 1776 cuts, the 13-star flag from the Saratoga 1777 cut on (instant swap)
const PB = badge({ name: "BENEDICT ARNOLD", role: "", photo: PHOTO("arnold"), flag: "assets/media/continental_colours.png", side: "carth", corner: "bl", initials: "BA", t: T1 + 0.15 });
tl.set(PB, { autoAlpha: 0 }, T3 - 0.01);
const PB3 = badge({ name: "BENEDICT ARNOLD", role: "", photo: PHOTO("arnold"), flag: FL.us, side: "carth", corner: "bl", initials: "BA", t: T3 });
tl.getTweensOf(PB3).forEach((tw) => tw.kill()); gsap.set(PB3, { autoAlpha: 0 }); tl.set(PB3, { autoAlpha: 1, x: 0 }, T3 - 0.01); tl.to(PB3, { autoAlpha: 0, duration: 0.4 }, T4 - 0.1);
let CAM_S0 = 1;
const ringN = (p, txt, n, t, until, dx, dy, sub) => { K.target(p[0], p[1], t, { r: 34 / CAM_S0, until });
  const el = GG.pin(`<div style="display:flex;align-items:center;gap:8px;font-family:Oswald;font-weight:700;color:#ffd54a;text-shadow:0 2px 4px #000,0 0 3px #000"><span style="display:inline-flex;width:38px;height:38px;border-radius:50%;border:3px solid #ffd54a;align-items:center;justify-content:center;font-size:21px">${n}</span><span style="font-size:36px;letter-spacing:.1em;white-space:nowrap">${txt}</span>${sub ? `<span style="font-size:24px;letter-spacing:.14em;color:#f3eee2;margin-left:6px">${sub}</span>` : ""}</div>`, p[0] + dx, p[1] + dy, { t: t + 0.1, pop: true, until });
  pinS(el); SFX("ref:pop", t + 0.12); return el; };
// ---------- CUT 1: QUEBEC 1775 (quebec map, winter): a column through the snowy woods to the walled city ----------
const C1 = [1400, 900], S1c = 1.35;
cut(T1, LQU, T2, C1, S1c, [12, -10, 1.08]); CAM_S0 = S1c;
dateSet("1775", T1, T2 - 0.05);
const SC1 = snap();
const SNW = scr0("", "inset:0;background:rgba(225,232,240,0.18);"); vis(T1, T2)(SNW);
B.snow(T1, T2 - 0.02);
const WALL = [[1370, 700], [1440, 670], [1510, 700], [1525, 780], [1480, 860], [1420, 880], [1365, 830]];
vis(T1, T2)(glowPath([...WALL, WALL[0]], "#c4121f", 5 / S1c, T1, null, 0, 1.0, { top: false }));
vis(T1, T2)(flagS(FL.gb, "", 1470, 760, null, null)); vis(T1, T2)(flagS("assets/media/continental_colours.png", "", 1000, 1000, null, null));
const QCOL = [[980, 1240], [1090, 1150], [1200, 1060], [1300, 980], [1350, 930]];
[0, 1, 2].forEach((k) => { const id = unitS("q" + k, "carth", QCOL[0], "infantry", "", { flag: "assets/media/continental_colours.png" }); vis(T1, T2)(B.units[id].el); along(id, sub(QCOL, 0, 0.75 - k * 0.12, 10), T1 + k * 0.2, T2 - T1 - 0.4, 10); });
arw({ pts: QCOL, side: "carth", t: T1 + 0.2, dur: 1.4, width: AW(S1c, 12), until: T2 - 0.01 });
ringN([1460, 780], "QUEBEC", 1, T_QUE - 0.35, T2 - 0.01, 70, -70, "1775");
endScope(SC1, T2);
// ---------- CUT 2: VALCOUR ISLAND 1776 (valcour map): the line of small boats behind the island, the British fleet on the open lake ----------
const C2 = [1520, 760], S2c = 1.35;
cut(T2, LVA, T3, C2, S2c, [-10, 8, 1.07]); CAM_S0 = S2c;
dateSet("1776", T2, T3 - 0.05);
const SC2 = snap();
vis(T2, T3)(flagS("assets/media/continental_colours.png", "", 1200, 640, null, null)); vis(T2, T3)(flagS(FL.gb, "", 1900, 560, null, null));
const CRES = [[1362, 560], [1373, 592], [1379, 624], [1380, 656], [1376, 688], [1366, 718]];
CRES.forEach((p, k) => vis(T2, T3)(gunboat([[p[0] - 1, p[1] - 1], p], T2, 0.2, null, { s: 14, side: "carth" })));
[[[1980, 420], [1860, 640], [1780, 760]], [[2080, 480], [1960, 700], [1850, 820]], [[2040, 330], [1900, 560], [1800, 700]]].forEach((pts, k) =>
  vis(T2, T3)(gunboat(pts, T2 + k * 0.15, T3 - T2 - 0.3, null, { s: 19, side: "rome" })));
shoot([1790, 750], [1372, 720], T_NAVY + 0.1, { r: 7, h: 26, width: 1.2, dur: 0.6 });
ringN([1500, 760], "VALCOUR ISLAND", 2, T_NAVY - 0.2, T3 - 0.01, 60, 190, "1776");
endScope(SC2, T3);
// ---------- CUT 3: SARATOGA 1777 (saratoga): the blue arrow into the redoubt ----------
const C3 = [1360, 600], S3c = 2.2;
tl.set(RELIEF, { autoAlpha: 1 }, T3 - 0.01);
cut(T3, null, T4 + 1.0, C3, S3c, [8, -6, 1.06]); CAM_S0 = S3c;
dateSet("7 OCTOBER 1777", T3, null);
const SC3 = snap();
vis(T3, null)(flagS(FL.us, "", 1460, 700, null, null)); vis(T3, null)(flagS(FL.gb, "", 1470, 520, null, null));
const RB3 = vis(T3, null)(redoubt(...BRY, null, null, { s: 60, open: "n" }));
const R3 = unitS("z1", "rome", [BRY[0] + 40, BRY[1] + 6], "infantry", ""); vis(T3, null)(B.units.z1.el);
arw({ pts: [[1240, 680], [1268, 600], [1300, 525], [1338, 505], [BRY[0], BRY[1] - 4]], side: "carth", t: T_BROKE - 0.1, dur: 0.9, width: AW(S3c, 12), until: null });
recolor(RB3, "carth", T_BROKE + 0.7); B.grey(["z1"], T_BROKE + 0.7, 0.5); SFX("hit", T_BROKE + 0.75); K.shake(T_BROKE + 0.75, 4, 0.3);
ringN([1300, 640], "SARATOGA", 3, T_SAR + 0.2, null, 40, 120, "1777");
// =====================================================================================================================
// the title (riser + boom)
// =====================================================================================================================
SFX("ref:riser", T4 + 0.1);
const TDIM = scr("", "inset:0;background:radial-gradient(ellipse at center, rgba(5,7,13,0.45), rgba(5,7,13,0.82));", T4, null, { autoAlpha: 0 });
const TITLE = scr(`<div style="text-align:center;font-family:Oswald;font-weight:700;padding:16px 64px 22px;background:rgba(14,12,10,0.9);border-top:7px solid #c9b48a;box-shadow:0 24px 50px rgba(0,0,0,.6)">
  <div style="font-size:30px;letter-spacing:0.42em;color:#c9b48a">BENEDICT ARNOLD'S</div>
  <div style="font-size:84px;letter-spacing:0.06em;line-height:1.08;color:#f7f3ea">3 GREATEST TACTICAL MOVES</div>
  <div style="font-size:28px;letter-spacing:0.3em;color:#ffd54a;margin-top:8px">1 QUEBEC · 2 VALCOUR ISLAND · 3 SARATOGA</div></div>`, "left:0;right:0;top:300px;display:flex;justify-content:center;", T_GREAT - 0.26, null, { autoAlpha: 0 });
tl.fromTo(TITLE, { autoAlpha: 0, scale: 1.7 }, { autoAlpha: 1, scale: 1, duration: 0.26, ease: "power4.in", immediateRender: false }, T_GREAT - 0.26);
SFX("ref:boom", T_GREAT); K.shake(T_GREAT, 6, 0.4);
// the HUD steps out while a big card is up (1c); the date scroll stays
declutter([LGD, QB, GB, PB, PB3], [[T_1500 - 0.05, T_1500 + 2.6], [T_WITH - 0.05, T_GUNS - 0.15], [S4 - 0.2, T1], [T4, END + 1]]);
fixImgs();
K.raiseTerritory();
B.finish();
