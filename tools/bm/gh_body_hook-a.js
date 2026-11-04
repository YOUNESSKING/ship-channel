// HOOK-A (hook-1 .. hook-2), Ulysses S. Grant #16. THE LOCKED HOOK (STYLE_LOCK 1a UPDATED 2026-10-31 + 1c; MAP LOOK v11 + CLEAN SCREEN 2b).
// Map agent hook (prefix gh_). Built with:  python3 tools/gh_make_control.py && python3 tools/gh_inline.py hook-a donelson_hd_lift hook-1 hook-2
// ONE world = donelson map px (z13). Three maps on ONE camera at their true place and scale (technique: patton/cleburne hook-a):
//   `tennessee` (z9, 16x, the overview), `henry` (z11, 4x, feathered, fades in 0.12x-0.24x) and `donelson` (z13, the relief, feathered,
//   fades in 0.38x-0.72x). Owner 2026-11-02 (territory minimised): option 1 (subtle tint) ONLY on the wide theatre shot (tennessee + henry
//   feb62, tools/gh_make_control.py); it dissolves (~2.8 s, sine.inOut) during the dive; the donelson close-up is option 2 (front lines only).
// hook-1 (stakes): frame 0 = the theatre (Cairo - Nashville), territory Feb 1862, both flags, blue gunboats + columns already moving up the
//   rivers, red columns reinforcing; FEBRUARY 1862 on "eighteen sixty-two"; "two rivers": the Tennessee and the Cumberland light up from
//   the Ohio; "open doors": blue arrows run up both rivers (OPEN DOORS); "heart of the Confederacy": Nashville pulses; "two forts": two red
//   forts slam on the rivers; "held them shut": red bars across both rivers, the boats stop (HELD SHUT); ONE continuous zoom (whoosh, no cut,
//   no flash) from the theatre down the Cumberland onto FORT DONELSON, landing on the words "Fort Donelson".
// hook-2: blue columns march over from the Tennessee and close the ring, gunboats come up the river; 12,000+ card slams on "twelve
//   thousand" (ticks), CONFEDERATE SOLDIERS lights on its words; SURRENDERED on "surrendered" (the garrison greys, a
//   white flag over the fort, prisoners); the "?" badge on "a general"; FIRST MAJOR VICTORY on its words; "a disaster": red pulse, the
//   camera pushes in on the Union right (hook-b starts there).
// Facts: research/FACT_NOTES.md + FACTCHECK_A (forts, ring, 12,000-15,000 prisoners). Nothing on screen before it is spoken (1c).
// @@KIT
// @@DATA
const LD = GG.proj(13, 535372, 819244);
const go = (id, t, dur, p, ease) => B.move(id, t, dur, p[0], p[1], ease || "power1.inOut");
const H1 = "hook-1", H2 = "hook-2", S2 = B.P(H2);
const T_1862 = at(H1, "eighteen sixty-two"), T_RIV = at(H1, "two rivers"), T_DOORS = at(H1, "open doors"), T_HEART = at(H1, "heart of the Confederacy"),
  T_FORTS = at(H1, "two forts"), T_SHUT = at(H1, "held them shut"), T_ONE = at(H1, "One of them"), T_CUMB = at(H1, "Cumberland River"), T_FD = at(H1, "Fort Donelson");
const T_WEEK = at(H2, "Within a week"), T_12 = at(H2, "twelve thousand"), T_CSOL = at(H2, "Confederate soldiers"), T_SURR = at(H2, "surrendered"),
  T_GEN = at(H2, "to a general"), T_NOBODY = at(H2, "almost nobody"), T_NORTH = at(H2, "It was the North"), T_FIRST = at(H2, "first major victory"),
  T_BEGAN = at(H2, "began as a disaster"), T_DIS = at(H2, "disaster");
// =====================================================================================================================
// THE WORLD: three maps, one camera
// =====================================================================================================================
const RELIEF = document.getElementById("relief");
const group = (r, fe) => { const g = document.createElement("div");
  g.style.cssText = `position:absolute;left:${r[0]}px;top:${r[1]}px;width:${r[2]}px;height:${r[3]}px;isolation:isolate;`;
  if (fe) { const F = `linear-gradient(to right, transparent 0%, #000 ${fe}%, #000 ${100 - fe}%, transparent 100%), linear-gradient(to bottom, transparent 0%, #000 ${fe * 1.6}%, #000 ${100 - fe * 1.6}%, transparent 100%)`;
    g.style.webkitMaskImage = F; g.style.maskImage = F; g.style.webkitMaskComposite = "source-in"; g.style.maskComposite = "intersect"; }
  WORLD.insertBefore(g, RELIEF); return g; };
const gimg = (src, parent) => { const i = document.createElement("img"); i.src = src; i.alt = ""; i.style.cssText = "position:absolute;left:0;top:0;width:100%;height:100%;"; parent.appendChild(i); return i; };
const TEN = group([-21900, -13756, 46080, 25920], 0); gimg("assets/media/gh_ten_relief.jpg", TEN); const TEN_C = terrImg("assets/media/gh_tennessee_ctl_feb62_mx.png", TEN, 0, null, 0.01);
const HEN = group([-4904, -2576, 11520, 6480], 6); gimg("assets/media/gh_hen_relief.jpg", HEN); const HEN_C = terrImg("assets/media/gh_henry_ctl_feb62_mx.png", HEN, 0, null, 0.01);
const DON = group([0, 0, 2880, 1620], 5); RELIEF.style.cssText += "position:absolute;left:0;top:0;width:100%;height:100%;"; DON.appendChild(RELIEF);
// ---------- the camera ----------
const cam = { cx: 0, cy: 0, s: 1 };
const smooth = (a) => a * a * (3 - 2 * a), ramp = (s, a, b) => smooth(Math.min(Math.max(Math.log(s / a) / Math.log(b / a), 0), 1));
const applyCam = () => { const s = cam.s; gsap.set(WORLD, { x: 960 - cam.cx * s, y: 540 - cam.cy * s, scale: s });
  HEN.style.opacity = ramp(s, 0.12, 0.24).toFixed(3); DON.style.opacity = ramp(s, 0.38, 0.72).toFixed(3); CAM_S = s; setInv(); };
const camTo = (t, dur, c, s, ease = "sine.inOut") => tl.to(cam, { cx: c[0], cy: c[1], s, duration: Math.max(dur, 0.01), ease, onUpdate: applyCam }, t);
// continuous geographic zoom: the scale changes log-linearly, the anchor P slides on a straight screen path (no cut, no flash)
const zoom = (t, dur, c0, s0, c1, s1, P, ease = "power2.inOut") => {
  const d0 = [(P[0] - c0[0]) * s0, (P[1] - c0[1]) * s0], d1 = [(P[0] - c1[0]) * s1, (P[1] - c1[1]) * s1], q = { u: 0 };
  tl.fromTo(q, { u: 0 }, { u: 1, duration: dur, ease, immediateRender: false, onUpdate: () => { const u = q.u, s = Math.exp(Math.log(s0) + (Math.log(s1) - Math.log(s0)) * u);
    cam.s = s; cam.cx = P[0] - (d0[0] + (d1[0] - d0[0]) * u) / s; cam.cy = P[1] - (d0[1] + (d1[1] - d0[1]) * u) / s; applyCam(); } }, t); };
// ---------- places (world = donelson map px) ----------
const FD = [1395, 758], DOV = [1505, 768], WB = [1425, 742], FH = LD(36.515, -88.035), NASH = LD(36.1627, -86.7816), SMITH = LD(37.139, -88.40), PAD = LD(37.0834, -88.60),
  CLK = LD(36.5298, -87.3595), BGR = LD(36.9685, -86.48), COL = LD(36.76, -89.10), CAI = LD(37.0053, -89.1765);
const TW = (pts) => pts.map(([x, y]) => [-21900 + 16 * x, -13756 + 16 * y]);           // tennessee map px -> world
const RCUM = TW(GD.riv.cumberland).reverse(), RTEN = TW(GD.riv.tennessee).reverse();   // both upstream: from the Ohio into the South
const near = (pts, p) => { let bi = 0, bd = 1e18; pts.forEach((q, i) => { const d = (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2; if (d < bd) { bd = d; bi = i; } }); return bi; };
const upTo = (pts, p) => pts.slice(0, near(pts, p) + 1);
const iFH = near(RTEN, FH), iFD = near(RCUM, FD);
const FHR = RTEN[iFH], FDR = RCUM[iFD];                                                     // the forts' points on the overview rivers
// the Cumberland at the fort, traced on the donelson relief (map px)
const CUMB_D = [[1150, 150], [1200, 300], [1245, 410], [1290, 520], [1335, 605], [1385, 660], [1450, 695], [1520, 705], [1600, 690], [1700, 665], [1830, 625]];
// =====================================================================================================================
// hook-1 (0 - S2): THE THEATRE, FEBRUARY 1862 (option 1); the rivers; ONE continuous zoom onto Fort Donelson
// =====================================================================================================================
const C0 = [1600, 0], S0 = 0.1, C0b = [1450, 150], S0b = 0.112;
cam.cx = C0[0]; cam.cy = C0[1]; cam.s = S0; applyCam();
const TZ0 = T_ONE - 0.3, TZ1 = T_FD + 0.05;                 // the dive: lands on "Fort Donelson"
const CF = [1395, 745], SF = 1.1;                           // arrival: the fort, the river, Dover
camTo(0, TZ0, C0b, S0b, "sine.inOut");
const K0 = 1 / S0;
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); const NA = LV.north();
// date scroll: in on the spoken year, never leaves
B.showDate(T_1862 - 0.1); dateSet("FEBRUARY 1862", T_1862 - 0.05, T_SURR + 0.05);
// flags (no names, v11): overview pair on each side's ground
const F0 = [flagS(FL.us, "", ...LD(37.05, -87.60), null, TZ0 + 0.9), flagS(FL.csa, "", ...LD(36.15, -87.25), null, TZ0 + 0.9)];
gsap.set(F0, { autoAlpha: 1 });   // on screen from frame 0
// ---------- units already moving at frame 0 (no names: nothing spoken yet) ----------
// Union gunboats steam up the Tennessee and the Cumberland from the Ohio; blue columns follow up the Tennessee; red columns reinforce the forts
const B1 = upTo(RTEN, FH), B2 = upTo(RCUM, FD);
const GBT = [gunboat(B1.slice(0, Math.round(B1.length * 0.75)), 0, T_SHUT + 0.3, TZ0 + 0.8, { s: 18 }),
  gunboat(B1.slice(0, Math.round(B1.length * 0.62)), 0, T_SHUT + 0.2, TZ0 + 0.8, { s: 18 }),
  gunboat(B2.slice(0, Math.round(B2.length * 0.78)), 0, T_SHUT + 0.3, TZ0 + 0.8, { s: 18 })];
const UB = [unitS("ub1", "carth", CAI, "infantry", ""), unitS("ub2", "carth", LD(37.05, -88.75), "infantry", "")];
UB.forEach((id) => gsap.set(B.units[id].el, { autoAlpha: 1 }));
along("ub1", [CAI, PAD, B1[Math.round(B1.length * 0.3)]], 0, TZ0 - 0.4, 20);
along("ub2", [LD(37.05, -88.75), ...B1.slice(0, Math.round(B1.length * 0.5))], 0, TZ0 - 0.4, 20);
const UR = [unitS("ur1", "rome", COL, "infantry", ""), unitS("ur2", "rome", BGR, "infantry", ""), unitS("ur3", "rome", FH, "infantry", "")];
UR.forEach((id) => gsap.set(B.units[id].el, { autoAlpha: 1 }));
along("ur2", [BGR, LD(36.80, -86.95), CLK, LD(36.50, -87.60)], 0, TZ0 + 0.3, 20);   // Bowling Green -> Clarksville -> the fort (reinforcing)
go("ur3", 0, 4, [FH[0] - 120, FH[1] + 250]);
B.hideUnits([...UB, ...UR], TZ0 + 0.5, 0.4);
// ---------- "two rivers": the Tennessee and the Cumberland light up from the Ohio (drawn upstream) ----------
const RW = 5 / S0;
const GT = glowPath(RTEN, "#bfe2ff", RW, T_RIV - 0.2, TZ0 + 1.0, 2, 0.8, { draw: 1.3 });
const GC = glowPath(RCUM, "#bfe2ff", RW, T_RIV, TZ0 + 1.2, 2, 0.8, { draw: 1.3 });
SFX("ref:pop", T_RIV);
// ---------- "open doors": blue arrows run up both rivers into the South ----------
const DA1 = arw({ pts: RTEN.filter((_, i) => i % 6 === 0).slice(0, Math.round(RTEN.length / 6 * 0.7)), side: "carth", t: T_DOORS - 0.1, dur: 1.5, width: AW(S0, 13), until: T_SHUT - 0.05 });
const DA2 = arw({ pts: RCUM.filter((_, i) => i % 6 === 0), side: "carth", t: T_DOORS + 0.1, dur: 1.5, width: AW(S0, 13), until: T_SHUT - 0.05 });
SFX("ref:whoosh", T_DOORS - 0.1);
const DOORS = sstamp("OPEN DOORS", 820, T_DOORS + 0.05, { size: 66, color: "#9fc0ea", until: T_FORTS - 0.25, shake: 3 });
// "heart of the Confederacy": Nashville pulses red
K.target(...NASH, T_HEART, { r: 60 / S0, side: "rome", until: TZ0 + 0.4 });
SFX("ref:pop", T_HEART + 0.05);
// ---------- "two forts": two red forts slam onto the rivers; "held them shut": red bars across both rivers ----------
const FTH = fortIcon(...FHR, T_FORTS - 0.05, TZ0 + 1.0, { s: 44 }), FTD = fortIcon(...FDR, T_FORTS + 0.15, null, { s: 44 });
tl.to(FTD, { left: FD[0], top: FD[1], duration: 2.0, ease: "sine.inOut" }, TZ0 + 1.5);   // onto the fort itself as the donelson map comes in
[FTH, FTD].forEach((el, k) => { tl.fromTo(el.querySelector(".fi"), { scale: 2.4 }, { scale: 1, duration: 0.22, ease: "power4.in", immediateRender: false }, T_FORTS - 0.05 + k * 0.2); });
SFX("hit", T_FORTS + 0.15); K.shake(T_FORTS + 0.15, 4, 0.3);
const bar = (pts, i) => { const a = pts[Math.max(0, i - 3)], b = pts[Math.min(pts.length - 1, i + 3)], dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, h = 26 / S0;
  const p = pts[i]; return [[p[0] - dy / L * h, p[1] + dx / L * h], [p[0] + dy / L * h, p[1] - dx / L * h]]; };
const BARS = [bar(RTEN, iFH), bar(RCUM, iFD)].map((pts, k) => glowPath(pts, "#ff3b30", 9 / S0, T_SHUT - 0.05 + k * 0.12, k ? TZ0 + 1.4 : TZ0 + 0.8, 1, 1.0, { top: true }));
SFX("hit", T_SHUT + 0.1);
const SHUT = sstamp("HELD SHUT", 820, T_SHUT + 0.05, { size: 70, until: TZ0 - 0.05, shake: 5 });
pulse(T_SHUT + 0.25);
// ---------- ONE CONTINUOUS ZOOM (whoosh) from the theatre down the Cumberland onto Fort Donelson ----------
SFX("whoosh", TZ0 - 0.05);
zoom(TZ0, TZ1 - TZ0, C0b, S0b, CF, SF, FD, "power2.inOut");
// option 1 -> option 2: the (subtle) theatre colours dissolve smoothly during the dive; the close-up shows front lines only
tl.to([TEN_C, HEN_C], { autoAlpha: 0, duration: 2.8, ease: "sine.inOut" }, TZ0 + 0.2);
// the Cumberland is named on its words (donelson scale), then the river label leaves (v11)
glowPath(CUMB_D, "#bfe2ff", 6 / SF, T_CUMB - 0.1, S2 + 1.0, 1, 0.55, { draw: 0.9 });
boxL("CUMBERLAND RIVER", 1385, 470, T_CUMB, null, { size: 15 });
// mid-zoom flags: the Union flag rides the gunboats coming up the Cumberland; the Confederate flag on Tennessee ground east of the river
const BOATR = [[1150, 150], [1200, 300], [1240, 400], [1275, 480]];
const BOATR2 = [...BOATR, [1300, 545]];
const GB2 = [0, 1].map((k) => gunboat(BOATR2.map(([x, y]) => [x - k * 22, y - k * 60]), TZ0 + 0.8, T_WEEK + 3.0 - (TZ0 + 0.8), null, { s: 17 }));
const FB = flagS(FL.us, "", 1060, 230, TZ0 + 0.8, TZ1 - 0.3); pinAlong(FB, [[1060, 230], [1110, 380]], TZ0 + 0.8, 6.0, 8);
const FM = flagS(FL.csa, "", ...LD(36.40, -87.72), TZ0 + 0.8, TZ1 + 0.4);
// arriving on Fort Donelson (donelson map, option 2: no ground tint): the fort, its water batteries, Dover
const TA = TZ1 - 0.6;
const F2 = [flagS(FL.us, "", 900, 690, TZ1 - 0.5, null), flagS(FL.csa, "", 1745, 445, TZ1 - 0.5, null)];
const FDL = boxL("FORT DONELSON", FD[0] - 175, FD[1] - 8, T_FD - 0.05, null, { size: 18 });
K.target(...FD, T_FD + 0.05, { r: 60, side: "rome", until: T_FD + 3.2 });
SFX("hit", TZ1); K.shake(TZ1, 4, 0.3);
const TDV = town("DOVER", DOV, "r", TZ1 + 0.2, { until: TZ1 + 0.2 + LBL_LIFE });
// the garrison in the fort and at Dover (red), the batteries above the river
const GR = [unitS("g1", "rome", [1320, 810], "infantry", "", { t: TZ1 - 0.5 }), unitS("g2", "rome", [1440, 845], "infantry", "", { t: TZ1 - 0.4 }),
  unitS("g3", "rome", [1545, 815], "infantry", "", { t: TZ1 - 0.3 }), unitS("g4", "rome", [1482, 726], "artillery", "", { t: TZ1 - 0.35, w: 44, h: 29 })];
// =====================================================================================================================
// hook-2: within a week -- the ring closes; 12,000+; SURRENDERED; the "?" general; first major victory; a disaster
// =====================================================================================================================
const LGD = legend(TZ1 + 0.4, null, true);     // two glowing lines (option 2); who is who, first shown after the camera has arrived (1c)
// the Union columns march over from the Tennessee (Fort Henry) and take their places round the fort: Smith left, Wallace centre, McClernand right
const CW = [1060, 730], SW = 0.95, CR = [1430, 800], SR = 1.55;
camTo(TZ1 + 0.02, T_WEEK - TZ1 + 0.1, [CF[0] - 25, CF[1] + 5], SF * 1.04, "sine.out");
camTo(T_WEEK + 0.1, 2.2, CW, SW, "sine.inOut");
const RD1 = [[FH[0] + 60, FH[1] + 30], [700, 640], [1000, 700], [1180, 760], [1250, 760]], RD2 = [[FH[0] + 60, FH[1] + 60], [700, 700], [1000, 820], [1200, 870], [1290, 880]],
  RD3 = [[FH[0] + 40, FH[1] + 90], [650, 780], [950, 920], [1250, 960], [1420, 945]];
const UC = [unitS("uSm", "carth", RD1[0], "infantry", "", { t: T_WEEK - 0.4, size: "XX" }), unitS("uWa", "carth", RD2[0], "infantry", "", { t: T_WEEK - 0.3, size: "XX" }),
  unitS("uMc", "carth", RD3[0], "infantry", "", { t: T_WEEK - 0.2, size: "XX" })];
[RD1, RD2, RD3].forEach((pts, k) => { along(UC[k], pts, T_WEEK - 0.2 + k * 0.15, 3.6, 16); arw({ pts, side: "carth", t: T_WEEK - 0.1 + k * 0.15, dur: 1.6, width: AW(SR, 10), until: T_12 - 0.3 }); });
SFX("ref:whoosh", T_WEEK);
const FH_I = fortIcon(FH[0] + 25, FH[1] - 10, T_WEEK - 0.2, T_SURR + 1.0, { s: 40, side: "carth" });     // Fort Henry already taken (blue)
// the gunboats come up the river and fire on the water batteries (visible, on screen)
shoot([1290, 520], [WB[0] - 6, WB[1] - 8], T_WEEK + 3.1, { r: 7, h: 30, width: 1.4, dur: 0.6 });
// push in on the fort as the ring closes; the two-colour front round the pocket (option 2)
camTo(T_12 - 0.6, 2.4, CR, SR, "sine.inOut");
const RING = [[1300, 735], [1290, 790], [1305, 850], [1360, 885], [1440, 900], [1520, 892], [1580, 860], [1600, 800]];
const RF = front2(RING, SR, T_WEEK + 2.2, { dur: 1.4, until: T_SURR + 0.4 });
// the big number card: slams on "twelve thousand", ticks; CONFEDERATE SOLDIERS lights on its words
const BIG = scr(`<div style="text-align:center;font-family:Oswald;font-weight:700;padding:14px 60px 18px;background:rgba(14,12,10,0.9);border-top:8px solid #e3232f;box-shadow:0 22px 44px rgba(0,0,0,.6)">
  <div style="font-size:26px;letter-spacing:0.36em;color:#d8cfb8">MORE THAN</div>
  <div class="n" style="font-size:132px;line-height:1;color:#f7f3ea;letter-spacing:0.02em">0</div>
  <div class="w0" style="font-size:40px;letter-spacing:0.14em;color:#6e675c">CONFEDERATE SOLDIERS</div></div>`, "left:0;right:0;top:120px;display:flex;justify-content:center;transform-origin:50% 40%;", T_12 - 0.15, T_SURR - 0.2, { autoAlpha: 0 });
slam(BIG, T_12 - 0.15, { from: 1.9, dur: 0.22, shake: 6 });
const tickN = (el, sel, n, t0, t1, fmt) => { const v = { v: 0 }, e = el.querySelector(sel);
  tl.to(v, { v: n, duration: t1 - t0, ease: "power2.out", onUpdate: () => { e.textContent = fmt(v.v); } }, t0); for (let t = t0; t < t1 - 0.05; t += 0.13) SFX("tick", t); };
tickN(BIG, ".n", 12000, T_12 + 0.1, T_CSOL + 0.2, (v) => (Math.round(v / 100) * 100).toLocaleString("en-US"));
tl.to(BIG.querySelector(".w0"), { color: "#ef8a82", duration: 0.15 }, T_CSOL); SFX("ref:pop", T_CSOL + 0.02);
// "surrendered": the garrison greys, a white flag over the fort, prisoners
const SURR = sstamp("SURRENDERED", 760, T_SURR - 0.05, { size: 92, shake: 6, until: T_GEN - 0.05 });
pulse(T_SURR + 0.2);
dateSet("16 FEBRUARY 1862", T_SURR + 0.1, null);
B.grey(GR, T_SURR + 0.1, 0.8);
const WF = pinS(GG.pin(`<svg width="40" height="54" viewBox="0 0 40 54" style="display:block;overflow:visible;filter:drop-shadow(0 2px 3px rgba(0,0,0,.8))"><path d="M6 54 L6 2" stroke="#2a2420" stroke-width="3.5"/><path d="M7 3 C18 0 26 8 38 4 L38 24 C26 28 18 20 7 23 Z" fill="#fbfaf5" stroke="#2a2420" stroke-width="1.6"/></svg>`, FD[0] + 8, FD[1] - 48, { t: T_SURR + 0.2, pop: true }));
SFX("ref:pop", T_SURR + 0.25);
const PRI = bars(FD[0] + 95, FD[1] + 40, T_SURR + 0.6, T_SURR + 0.6 + LBL_LIFE, 46);
// the ring closes on the river: the blue arrows press in, the counters step up to the works
[["uSm", [1270, 760]], ["uWa", [1300, 870]], ["uMc", [1450, 925]]].forEach(([id, p], k) => go(id, T_SURR - 0.6 + k * 0.1, 1.4, p));
// "to a general almost nobody in the North had heard of": the "?" badge
const QB = qBadge("A GENERAL", "", T_GEN + 0.25, null, { corner: "bl" });
tl.to(QB, { scale: 1.06, duration: 0.25, yoyo: true, repeat: 1, transformOrigin: "0% 100%" }, T_NOBODY); SFX("ref:pop", T_NOBODY + 0.05);
K.target(1270, 760, T_GEN + 0.3, { r: 34, side: "carth", until: T_NORTH });
// "the North's first major victory of the war"
const FIRST = sstamp("FIRST MAJOR VICTORY", 760, T_FIRST - 0.05, { size: 78, color: "#9fc0ea", sub: "OF THE WAR", until: T_BEGAN - 0.2, shake: 5 });
SFX("ref:boom", T_FIRST + 0.2);
K.target(...FD, T_FIRST + 0.1, { r: 70, side: "carth", until: T_BEGAN });
// "it began as a disaster": red pulse, the camera pushes in on the Union right, where it began (hook-b starts on this frame)
const CE = [1430, 800], SE = 1.9;                          // hook-b's first camera (keep in sync with gh_body_hook-b.js)
camTo(T_BEGAN - 0.4, END - T_BEGAN + 0.4, CE, SE, "sine.inOut");
const DIS = sstamp("A DISASTER", 760, T_DIS - 0.1, { size: 84, until: END - 0.4, shake: 6 });
pulse(T_DIS + 0.15);
// flags for the close push (both on the screen to the end; hook-b starts with this pair)
tl.to(F2, { autoAlpha: 0, duration: 0.4 }, T_12 + 0.6);
const F3 = [flagS(FL.us, "", 1190, 905, T_12 + 0.5, null), flagS(FL.csa, "", 1760, 600, T_12 + 0.5, null)];
// the HUD steps out while a big card is up (1c); the date scroll stays
declutter([LGD, QB], [[T_DOORS + 0.05, T_FORTS - 0.25], [T_SHUT + 0.05, TZ0 - 0.05], [T_12 - 0.15, T_SURR - 0.2], [T_SURR - 0.05, T_GEN - 0.05], [T_FIRST - 0.05, T_BEGAN - 0.2], [T_DIS - 0.1, END + 1]]);
K.raiseTerritory();
B.finish();
