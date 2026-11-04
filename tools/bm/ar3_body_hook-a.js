// HOOK-A (hook-1 .. hook-2), Benedict Arnold #17. THE LOCKED HOOK (STYLE_LOCK 1a: stakes -> ONE continuous zoom -> number -> promise by
// 10-15 s; 1c: clean first frame, nothing before it is spoken, one big card at a time). Map agent ar3_.
// Built with: python3 tools/ar3_make_control.py northeast hudson && python3 tools/ar3_inline.py hook-a hook-1 hook-2
// ONE world = saratoga map px (z15). Three maps on ONE camera at their true place and scale (technique: meade/grant hook-a):
//   `northeast` (z8, 128x, the overview, option 1 territory at half strength), `hudson` (z10, 32x, feathered, fades in 2x-4x the overview's
//   native scale, its own half-strength territory) and `saratoga` (z15, feathered, fades in at s 0.1-0.2). The colours dissolve (~2.8 s)
//   during the dive; the battlefield close-up is option 2.
// hook-1 v2 (owner 2026-11-03, new stakes line): frame 0 = the theatre, units moving (British at the north end of the lake and at New York,
//   Americans in New England), both flags, territory; 1777 on the year; "going badly": GOING BADLY + red pulse; "New York": ring, label,
//   flag; "Philadelphia, the American capital": an edge marker at the SW map edge (the city is off the map); "a second British army": the
//   column starts down Lake Champlain; "coming down from Canada": the red arrow + the ONE continuous zoom (whoosh, no cut, no flash),
//   landing on "Saratoga". No CUT IN TWO (no longer spoken).
// hook-2: OCTOBER 1777; ABOUT 6,000 slams on "six thousand" (ticks); "lay down their arms there": grey + white flag at Saratoga; FRANCE on
//   "France"; "the man who broke the British line that day": push in to the battlefield, the blue arrow breaks the line at the German
//   redoubt; the "?" badge on "no command at all". hook-b starts on this last frame (keep in sync with tools/ar3_body_hook-b.js).
// Facts: FACT_NOTES (Burgoyne from Canada down Champlain/Hudson toward Albany; ~6,000 surrendered at Saratoga 17 Oct; France 1778).
// @@KIT
const H1 = "hook-1", H2 = "hook-2", S2 = B.P(H2);
const T_1777 = at(H1, "seventeen seventy-seven"), T_REV = at(H1, "the Revolution"), T_BADLY = at(H1, "going badly"), T_HELD = at(H1, "The British held"),
  T_NY = at(H1, "New York"), T_PHIL = at(H1, "Philadelphia"), T_CAP = at(H1, "the American capital"), T_ARMY = at(H1, "a second British army"),
  T_DOWN = at(H1, "coming down from Canada"), T_TOWARD = at(H1, "toward a village"), T_SARA = at(H1, "Saratoga");
const T_WEEKS = at(H2, "Within weeks"), T_6000 = at(H2, "six thousand"), T_SOLD = at(H2, "soldiers"), T_ARMS = at(H2, "lay down their arms"),
  T_VIC = at(H2, "The victory"), T_FR = at(H2, "France"), T_MAN = at(H2, "And the man"), T_BROKE = at(H2, "broke the British line"),
  T_DAY = at(H2, "that day"), T_NOCMD = at(H2, "no command at all");
// =====================================================================================================================
// THE WORLD: three maps, one camera
// =====================================================================================================================
const NE = mapGroup("northeast", 0); const NE_C = terrImg("assets/media/ar3_ctl_northeast_1777.png", NE, 0, null, 0.01);
const HUD = mapGroup("hudson", 6); const HUD_C = terrImg("assets/media/ar3_ctl_hudson_1777.png", HUD, 0, null, 0.01);
const SAR = baseGroup(4);
FADES.push([HUD, 0.0156, 0.031], [SAR, 0.1, 0.2]);
hudRiver();
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); const NA = LV.north(); NA.style.top = "330px";
// ---------- places (world = saratoga px) ----------
const STJ = LD(45.30, -73.26), VAL = LD(44.611, -73.40), CRP = LD(44.027, -73.424), TIC = LD(43.843, -73.387), SKN = LD(43.555, -73.404),
  FTE = LD(43.267, -73.585), SARV = LD(43.10, -73.588), ALB = LD(42.65, -73.75), NYC = LD(40.70, -74.02), NENG = LD(43.6, -71.6), MTL = LD(45.50, -73.57);
const LAKE = [LD(45.45, -73.25), STJ, LD(45.05, -73.32), LD(44.85, -73.33), VAL, LD(44.35, -73.36), LD(44.15, -73.40), CRP, TIC, LD(43.70, -73.39), SKN];
const HUDR = [...HUDSON_LL.slice(1).map((q) => LD(...q)), LD(41.39, -73.96), LD(41.0, -73.90), NYC];
const BRY = [1338, 542], LIR = [1417, 651];
const AMLINE = [[1300, 1185], [1420, 1195], [1560, 1215], [1700, 1250], [1830, 1290]];
const CAMPL = [[1440, 655], [1560, 668], [1700, 660], [1850, 640], [2000, 610], [2150, 560]];
// =====================================================================================================================
// hook-1: frame 0 = the theatre (option 1, half strength), units already moving
// =====================================================================================================================
const NEP = (x, y) => [NE.rect[0] + x * NE.k, NE.rect[1] + y * NE.k];        // northeast map px -> world
const C0 = NEP(1390, 840), S0 = 0.70 / NE.k, C0b = NEP(1380, 835), S0b = 0.71 / NE.k;   // whole map height in frame: Canada (top) to New York (bottom edge)
camSet(C0, S0);
const TZ0 = T_DOWN + 0.25, TZ1 = T_SARA + 0.1;   // the dive starts on "coming down from Canada", lands on "Saratoga"
camTo(0, TZ0, C0b, S0b, "sine.inOut");
const K0 = 1 / S0;
const OV_A = S0b * 6, OV_B = S0b * 14, CL_A = S0b * 8, CL_B = S0b * 16;   // overview overlays cross-fade out / close layer in (log scale)
// flags (no names, v11): on each side's ground
const F0 = [flagS(FL.gb, "", ...NEP(1495, 330), null, null), flagS(FL.us, "", ...LD(43.0, -71.3), null, null)]; gsap.set(F0, { autoAlpha: 1 }); fadeS(F0, OV_A, OV_B, true);
// New England (soft blue glow on the right, world-sized)
const NEG = GG.pin(`<div style="width:${360 * 128}px;height:${300 * 128}px;border-radius:50%;background:radial-gradient(ellipse at center, rgba(120,170,255,0.32) 0%, rgba(120,170,255,0.14) 45%, rgba(120,170,255,0) 70%)"></div>`, ...NENG, {});
gsap.set(NEG, { autoAlpha: 1 }); tl.to(NEG, { autoAlpha: 0.55, duration: 1.2, yoyo: true, repeat: 3, ease: "sine.inOut" }, 0.5); fadeS(NEG, S0b * 2, S0b * 5, true);
// units already moving at frame 0: British boats + a column at the north end of the lake (they start south on "a second British army"),
// a red garrison at New York with ships, blue troops in New England and on the Hudson
const BT = [0, 1, 2, 3].map((k) => gunboat(sub(LAKE, 0.0 + k * 0.035, 0.12 + k * 0.035, 6), 0, T_ARMY, null, { s: 15, side: "rome" }));
gsap.set(BT, { autoAlpha: 1 });
const BT2 = [0, 1, 2, 3].map((k) => gunboat(sub(LAKE, 0.12 + k * 0.035, 0.6 + k * 0.08, 12), T_ARMY, TZ0 + 1.0 - T_ARMY, null, { s: 15, side: "rome" }));
BT.forEach((el) => tl.set(el, { autoAlpha: 0 }, T_ARMY)); fadeS(BT2, OV_A, OV_B, true);
const RC = [unitS("rc1", "rome", posOn(LAKE, 0.06), "infantry", ""), unitS("rc2", "rome", MTL, "infantry", "")];
RC.forEach((id) => gsap.set(B.units[id].el, { autoAlpha: 1 }));
go("rc2", 0, T_ARMY, posOn(LAKE, 0.02));
const SH = (pts, dx) => pts.map(([x, y]) => [x + dx, y]);
along("rc1", SH(sub(LAKE, 0.06, 0.7, 12), 2600), T_ARMY, TZ0 + 0.6 - T_ARMY, 12); along("rc2", SH(sub(LAKE, 0.02, 0.6, 12), -2600), T_ARMY + 0.2, TZ0 + 0.6 - T_ARMY, 12);
const NYP = LD(40.71, -74.0), NYU = NEP(1185, 1515);
const RNY = unitS("rny", "rome", NYU, "infantry", ""); gsap.set(B.units.rny.el, { autoAlpha: 1 });
const NYS = [0, 1].map((k) => gunboat([LD(40.62 - k * 0.04, -73.55 + k * 0.3), LD(40.60 - k * 0.03, -73.85 + k * 0.25)], 0, T_NY + 1.5, null, { s: 15, side: "rome" })); gsap.set(NYS, { autoAlpha: 1 }); fadeS(NYS, OV_A, OV_B, true);
const UB = [unitS("ub1", "carth", LD(42.95, -73.65), "infantry", ""), unitS("ub2", "carth", LD(43.0, -71.9), "infantry", ""), unitS("ub3", "carth", LD(41.6, -73.9), "infantry", "")];
UB.forEach((id) => gsap.set(B.units[id].el, { autoAlpha: 1 }));
go("ub2", 0, TZ0, LD(43.0, -72.9)); go("ub3", 0, TZ0, LD(42.2, -73.6));
fadeS(["rc1", "rc2", "ub1", "ub2", "ub3", "rny"].map((id) => B.units[id].el), OV_A, OV_B, true);
// "By seventeen seventy-seven": the date scroll (stays from now on)
B.showDate(T_1777 - 0.1); dateSet("1777", T_1777 - 0.05, T_WEEKS - 0.05);
// "the Revolution was going badly": red edge pulse + GOING BADLY (spoken words)
const BAD = sstamp("GOING BADLY", 820, T_BADLY - 0.05, { size: 72, until: T_NY - 0.2, shake: 5 });
pulse(T_BADLY + 0.2);
// "The British held New York": the red ring + label + flag at New York
K.target(...NYP, T_NY, { r: 55 * K0, side: "rome", until: T_PHIL + 0.6 }); SFX("ref:pop", T_NY + 0.05);
const TNY = boxL("NEW YORK", ...NEP(1020, 1480), T_NY, null, { size: 16 });          // label above the city (the city sits on the map's bottom edge)
const FNY = flagS(FL.gb, "", ...LD(40.86, -72.95), T_NY + 0.1, null); fadeS(FNY, OV_A, OV_B, true);   // on Long Island (British-held)
tl.to(B.units.rny.el.firstElementChild, { scale: 1.35, duration: 0.22, yoyo: true, repeat: 1 }, T_NY + 0.1);
// "and Philadelphia, the American capital": off the map to the south-west -> an edge marker with an arrow, ring + label
const PHE = LD(41.45, -76.55);   // the map's south-west edge, in the direction of Philadelphia (39.95, -75.16)
const PH = pinS(GG.pin(`<div style="display:flex;align-items:center;gap:10px;font-family:Oswald;font-weight:700;color:#f0ece2;text-shadow:0 0 6px #0a0e10,0 2px 4px #000">
  <svg width="46" height="46" viewBox="-23 -23 46 46" style="display:block;overflow:visible;filter:drop-shadow(0 0 6px #ff3b30)"><circle r="17" fill="rgba(196,18,31,0.9)" stroke="#f3eee2" stroke-width="3"/><path d="M8 -8 L-9 9 M-9 1 L-9 9 L-1 9" fill="none" stroke="#f3eee2" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <div><div style="font-size:34px;letter-spacing:.06em;line-height:1">PHILADELPHIA</div><div class="cap" style="font-size:18px;letter-spacing:.24em;color:#ff8a80">THE AMERICAN CAPITAL</div></div></div>`, ...PHE, { t: T_PHIL - 0.05, pop: true, until: Math.min(T_PHIL + LBL_LIFE + 1.0, TZ0 + 0.3) }));
gsap.set(PH.querySelector(".cap"), { autoAlpha: 0 }); tl.to(PH.querySelector(".cap"), { autoAlpha: 1, duration: 0.25 }, T_CAP);
SFX("ref:pop", T_PHIL); SFX("hit", T_CAP + 0.05); K.shake(T_CAP + 0.05, 3, 0.25);
// "and a second British army": the red column in Canada pulses and starts down Lake Champlain
tl.to(RC.map((id) => B.units[id].el.firstElementChild), { scale: 1.3, duration: 0.22, yoyo: true, repeat: 1 }, T_ARMY + 0.1);
K.target(...posOn(LAKE, 0.08), T_ARMY + 0.05, { r: 60 * K0, side: "rome", until: T_DOWN + 1.0 }); SFX("ref:pop", T_ARMY + 0.1);
// "was coming down from Canada": the red arrow down the lake toward Saratoga
const DOWN = [...sub(LAKE, 0, 1, 10), FTE, SARV];
const DA = arrowFix(arw({ pts: DOWN, side: "rome", t: T_DOWN - 0.1, dur: 1.4, width: AW(S0b, 13), until: null }), S0b); fadeS(DA, OV_A, OV_B, true);   // constant on-screen size through the dive
// ---------- ONE CONTINUOUS ZOOM (whoosh) down the Hudson onto Saratoga ----------
const C1 = [SARV[0] - 250, SARV[1] + 700], S1 = 0.22;
SFX("whoosh", TZ0 - 0.05);  // ONE zoom, ONE whoosh (no ref:whoosh on the arrow)
zoom(TZ0, TZ1 - TZ0, C0b, S0b, C1, S1, SARV, "power2.inOut");
tl.to([NE_C, HUD_C], { autoAlpha: 0, duration: 2.8, ease: "sine.inOut" }, TZ0 + 0.4);
// the Hudson glows on its word (hudson scale), its label leaves after ~3.5 s
glowPath(HUDR.slice(0, 7), "#bfe2ff", 3 / 0.04, TZ0 + 0.6, S2 + 0.5, 1, 0.6, { draw: 0.9 });
// mid-zoom flags (hudson scale)
// mid-dive flags (hudson scale): in while the overview flags scroll off, out before the close flags
const FMID = [flagS(FL.gb, "", ...LD(43.42, -73.95), null, null), flagS(FL.us, "", ...LD(42.72, -73.28), null, null)]; gsap.set(FMID, { autoAlpha: 1 });
SCALEFIX.push((s) => { const v = ramp(s, S0b * 1.1, S0b * 1.8) * (1 - ramp(s, S0b * 8, S0b * 13)); FMID.forEach((g) => { g.style.filter = `opacity(${v.toFixed(3)})`; }); });
// close-layer flags (they come in with the close units before the overview flags leave, and stay on the landed Saratoga shot)
const FM = [flagS(FL.gb, "", SARV[0] - 1700, SARV[1] - 700, null, T_MAN + 0.6), flagS(FL.us, "", SARV[0] + 1700, SARV[1] + 1500, null, T_MAN + 0.6)]; gsap.set(FM, { autoAlpha: 1 }); fadeS(FM, S0b * 6, S0b * 11);
// arriving on "Saratoga": the village, the British army camped near it, the American lines south of it
const ST = town("SARATOGA", SARV, "r", T_SARA - 0.05, { until: T_SARA + LBL_LIFE });
K.target(...SARV, T_SARA + 0.05, { r: 60 / S1, side: "rome", until: T_SARA + 3.0 });
SFX("hit", TZ1); K.shake(TZ1, 4, 0.3);
const XR = [unitS("x0", "rome", [SARV[0] - 300, SARV[1] + 200], "infantry", ""), unitS("x1", "rome", [SARV[0] + 200, SARV[1] + 380], "infantry", ""),
  unitS("x2", "rome", [SARV[0] - 80, SARV[1] + 650], "infantry", "")];
const XB = [unitS("y0", "carth", [SARV[0] - 900, SARV[1] + 1300], "infantry", ""), unitS("y1", "carth", [SARV[0] + 900, SARV[1] + 900], "infantry", "")];
[...XR, ...XB].forEach((id) => { gsap.set(B.units[id].el, { autoAlpha: 1 }); fadeS(B.units[id].el, CL_A, CL_B); });   // close units fade in with the zoom (no pop)
// =====================================================================================================================
// hook-2: ~6,000; laid down their arms; France; the line broken; the "?"
// =====================================================================================================================
camTo(TZ1 + 0.02, T_MAN - TZ1, [C1[0] + 150, C1[1] - 200], S1 * 1.08, "sine.out");
const LGD = legend(TZ1 + 0.6, null, true);
dateSet("OCTOBER 1777", T_WEEKS, null);
for (let k = 0; k < 3; k++) SFX("tick", T_WEEKS - 0.3 + k * 0.12);
// the Americans close round the village (within weeks)
go("y0", T_WEEKS, 2.4, [SARV[0] - 600, SARV[1] + 800]); go("y1", T_WEEKS + 0.1, 2.4, [SARV[0] + 650, SARV[1] + 500]);
const NUM = bigNum("ABOUT", 6000, "SOLDIERS", T_6000 - 0.12, T_ARMS + 0.5, { tick: 1.0, top: 600 });
tl.to(NUM.querySelector(".w0"), { color: "#ef8a82", duration: 0.15 }, T_SOLD);
// "would lay down their arms there": grey + white flag at Saratoga
B.grey(XR, T_ARMS + 0.1, 0.8);
whiteFlag(SARV[0] + 60, SARV[1] - 160, T_ARMS + 0.15, T_MAN + 0.3); SFX("ref:pop", T_ARMS + 0.2);
pulse(T_ARMS + 0.3);
// "would bring France into the war"
const FRA = sstamp("FRANCE", 330, T_FR - 0.05, { size: 84, color: "#9fc0ea", sub: "INTO THE WAR", until: T_MAN - 0.15, shake: 5 });
SFX("ref:boom", T_FR + 0.2);
// "And the man who broke the British line that day": push in to the battlefield (saratoga map, option 2), the line breaks at the redoubt
const CE = [1420, 860], SE = 1.35;                         // hook-b's first camera (keep in sync)
camTo(T_MAN - 0.2, 0.9, [1500, 1000], S1, "sine.inOut"); camTo(T_MAN + 0.7, T_BROKE - T_MAN + 0.1, CE, SE, "power2.inOut");
hideU(["x0", "x1", "x2", "y0", "y1"], T_MAN + 0.3);
const RB = redoubt(...BRY, T_MAN + 0.4, null, { s: 56, open: "n" }), RL = redoubt(...LIR, T_MAN + 0.5, null, { s: 56 });
const CL = glowPath(CAMPL, "#bc2528", 5 / SE, T_MAN + 0.3, null, 0, 0.7, { draw: 0.8 });
const AL = glowPath(AMLINE, "#2c57b7", 5 / SE, T_MAN + 0.3, null, 0, 0.7, { draw: 0.8 });
const R0 = { r1: [1300, 575], r2: [1400, 690], r3: [1480, 690], rg: [1450, 655] };
Object.entries(R0).forEach(([id, p], k) => unitS(id, "rome", p, id === "rg" ? "artillery" : "infantry", "", id === "rg" ? { w: 44, h: 29, t: T_MAN + 1.0 } : { t: T_MAN + 0.9 + k * 0.08 }));
const AU = [unitS("a1", "carth", [1380, 1170], "infantry", "", { t: T_MAN + 0.5 }), unitS("a2", "carth", [1560, 1200], "infantry", "", { t: T_MAN + 0.55 }), unitS("a3", "carth", [1700, 1235], "infantry", "", { t: T_MAN + 0.6 })];
const F0b = [flagS(FL.us, "", 1800, 1140, T_MAN + 0.3, null), flagS(FL.gb, "", 1760, 560, T_MAN + 0.3, null)];
// the battlefield layer comes in with the push (scale), so nothing sits on top of anything while the camera is still wide
fadeS([RB, RL, ...Object.keys(R0).map((id) => B.units[id].el), ...AU.map((id) => B.units[id].el)], 0.45, 0.85);
const FRB = front2([[1240, 600], [1300, 560], [1338, 560], [1380, 610], [1417, 670], [1480, 710], [1560, 700]], SE, T_MAN + 0.6, { dur: 1.0, until: END - 0.6 });
arw({ pts: [[1240, 700], [1270, 610], [1320, 545], [1400, 520]], side: "carth", t: T_BROKE + 0.1, dur: 0.8, width: AW(SE, 13), until: END - 0.6 });
SFX("hit", T_BROKE + 0.85); K.shake(T_BROKE + 0.85, 4, 0.3); pulse(T_BROKE + 0.9);
// "had no command at all": the "?" badge (hook-b keeps it)
const QB = qBadge("THE MAN", "", T_NOCMD - 0.05, null, { corner: "bl" });
tl.to(QB, { scale: 1.06, duration: 0.25, yoyo: true, repeat: 1, transformOrigin: "0% 100%" }, T_NOCMD + 0.6); SFX("ref:pop", T_NOCMD);
// the HUD steps out while a big card is up (1c); the date scroll stays
declutter([LGD], [[T_6000 - 0.12, T_ARMS + 0.5], [T_FR - 0.05, T_MAN - 0.15]]);
fixImgs();
K.raiseTerritory();
B.finish();
