// MOVE 2a (m2-1 .. m2-2), Grant #16: Vicksburg on its bluff; the winter of failed attempts from the north; Grant's idea (march down the
// west bank, cross below, run the boats past the guns). Map agent "vk". Built with: python3 tools/vk_inline.py m2a vicksburg_hd_lift m2-1 m2-2
// ONE world = vicksburg map px (z10). The `mississippi` map (z8) sits in it at its true place and scale (4x; technique of
// patton/tools/pc_body_hook-a.js): one camera drives the theatre overview (s 1/6) and the Vicksburg map (s 0.9 - 2.4); the mississippi layer
// fades out between s 0.27 and 0.56 over the edge-feathered vicksburg layers (no cut, no white flash).
//   m2-1  title MOVE 2 · THE MISSISSIPPI · 1863 on "Mississippi"; option 1 territory 1 Apr 1863 (tools/vk_make_control.py); the river glows;
//         Vicksburg ringed on its bluff, red batteries; Union gunboats stopped above it; the link to the western states (red rail line +
//         arrows across the river); WINTER 1862-63: the attempts from the north (Chickasaw Bayou, Yazoo Pass, Steele's Bayou) draw and grey;
//         dive onto the Vicksburg map: the canal across De Soto Point, Lake Providence, gunboats stuck in the bayou; NOTHING WORKED;
//         belief card RUN OUT OF IDEAS.
//   m2-2  20 APRIL 1863: Grant badge; the march down the west bank (Milliken's Bend - Richmond - New Carthage - Hard Times, bayous bridged),
//         the Union ground spreads down the west bank (apr1 -> apr20); the dashed crossing below the city; the boats needed on the south side
//         (ghost outlines); the run past the guns: the boats above the city, the batteries fire; push in on Vicksburg (hand-off to m2b, night).
// Facts: FACTCHECK_B #5 (orders 20 Apr; Milliken's Bend - Richmond - Perkins' - Hard Times; three bayous bridged), FACT_NOTES.
// @@KIT
// @@DATA
const MZ = GD.maps.mississippi, VZ = GD.maps.vicksburg;
const L = GG.proj(10, VZ.origin_world_px[0], VZ.origin_world_px[1]);
const LL = (pts) => pts.map(([la, lo]) => L(la, lo));
const P1 = "m2-1", P2 = "m2-2";
const T_MS = at(P1, "Mississippi, sat"), T_BLUFF = at(P1, "sat on a bluff"), T_RIV = at(P1, "Mississippi River."), T_HELD = at(P1, "As long as the Confederates"),
  T_FREE = at(P1, "could not use the river freely"), T_LINK = at(P1, "the South stayed linked"), T_WEST = at(P1, "western states"), T_WINT = at(P1, "All winter"),
  T_NORTH = at(P1, "from the north"), T_FAIL = at(P1, "had failed in the swamps"), T_CAN = at(P1, "Canals dug in the mud"), T_BAY = at(P1, "bayous cleared for gunboats"),
  T_STUCK = at(P1, "boats stuck among the trees"), T_NOTH = at(P1, "nothing worked"), T_MANY = at(P1, "Many in the North"), T_IDEAS = at(P1, "run out of ideas");
const T_DIFF = at(P2, "Grant had a different idea"), T_MARCH = at(P2, "march his army down the west bank"), T_LA = at(P2, "through the Louisiana swamps"),
  T_CROSS = at(P2, "cross the river below the city"), T_NEED = at(P2, "he needed boats and transports"), T_SOUTH = at(P2, "on the south side"),
  T_ONLY = at(P2, "the only way to get them there"), T_RUN = at(P2, "run them past the guns");
// ---------- places (vicksburg z10 world px) ----------
const VKS = L(32.352, -90.878), MEM = L(35.149, -90.049), BR = L(30.451, -91.187), JAX = L(32.299, -90.185), NO = L(29.951, -90.072), HEL = L(34.527, -90.586),
  MIL = L(32.48, -91.07), YP = L(32.385, -91.0), RICH = L(32.393, -91.176), NCAR = L(32.09, -91.13), HT = L(32.07, -91.085), GG_ = L(32.033, -91.053),
  LP = L(32.804, -91.170), MON = L(32.503, -92.116), SHV = L(32.525, -93.750), LR = L(34.746, -92.29), PH = L(30.678, -91.27), NAT = L(31.56, -91.403),
  WAR = L(32.247, -90.928), HB = L(32.516, -90.785), GWD = L(33.516, -90.18), RF = L(32.906, -90.878);
// the Mississippi (approx. 1863 course, for the glow and the boats): Memphis -> Helena -> Lake Providence -> Milliken's Bend -> Vicksburg -> Natchez -> Baton Rouge
const RIV = LL([[35.15, -90.07], [34.80, -90.30], [34.53, -90.58], [34.15, -90.85], [33.75, -91.05], [33.40, -91.08], [33.05, -91.12], [32.80, -91.16], [32.60, -91.12],
  [32.48, -91.06], [32.40, -91.00], [32.375, -90.93], [32.37, -90.895], [32.345, -90.893], [32.30, -90.90], [32.247, -90.935], [32.13, -91.04], [32.04, -91.07],
  [31.95, -91.16], [31.80, -91.30], [31.56, -91.42], [31.20, -91.58], [31.00, -91.62], [30.70, -91.32], [30.45, -91.20], [30.20, -91.08], [29.95, -90.07]]);
// the 1863 hairpin round De Soto Point (the river cut through the neck in 1876; the modern cut-off is hidden under a land-coloured stroke)
const LOOP63 = LL([[32.402, -90.994], [32.394, -90.960], [32.387, -90.930], [32.381, -90.903], [32.376, -90.889], [32.367, -90.884], [32.352, -90.887], [32.336, -90.894], [32.321, -90.903]]);
const CUT = LL([[32.383, -91.001], [32.366, -91.003], [32.352, -90.975], [32.343, -90.945], [32.334, -90.922], [32.327, -90.909]]);
// ---------- the world: mississippi copy UNDER the vicksburg relief (shows beyond the feathered edges), vicksburg layers, mississippi layer on top ----------
const AR = [MZ.origin_world_px[0] * 4 - VZ.origin_world_px[0], MZ.origin_world_px[1] * 4 - VZ.origin_world_px[1], 11520, 6480];
const group = (parent, before) => { const g = document.createElement("div"); g.style.cssText = `position:absolute;left:${AR[0]}px;top:${AR[1]}px;width:${AR[2]}px;height:${AR[3]}px;isolation:isolate;`; parent.insertBefore(g, before); return g; };
const gimg = (src, parent, mx) => { const i = document.createElement("img"); i.src = src; i.alt = ""; i.style.cssText = `position:absolute;left:0;top:0;width:100%;height:100%;${mx ? `mix-blend-mode:multiply;filter:${SOFT};` : ""}`; parent.appendChild(i); return i; };
const RELIEF = document.getElementById("relief");
const PU = group(WORLD, RELIEF); gimg("assets/media/vk_miss_relief.jpg", PU, false); gimg("assets/media/vk_miss_ctl_apr1_mx.png", PU, true);
// owner 2026-11-02: territory colours ONLY on the theatre wide shot (the river splits the Confederacy); the Vicksburg close-ups are option 2
// (two glowing front bands round the Union west-bank ground, no fill). The colours dissolve over ~2.8 s during the dive (defined below at TZ0).
const VC1 = terr0("assets/media/vk_vick_ctl_apr1_mx.png"); VC1.style.filter = SOFT;
const CUE = T_MARCH + 0.4;
const PW = group(WORLD, OVL); gimg("assets/media/vk_miss_relief.jpg", PW, false); gimg("assets/media/vk_miss_ctl_apr1_mx.png", PW, true);
landPatch(CUT, 16); riverLine(LOOP63, 6.5);
const RLINE = riverLine(RIV, 9);   // the river on the theatre layer (that map shows no water); fades out with it
living(VZ.meters_per_px, [], { n: 5, clouds: 0.12 });
const FEATHER = "linear-gradient(to right, transparent 0%, #000 10%, #000 90%, transparent 100%), linear-gradient(to bottom, transparent 0%, #000 10%, #000 90%, transparent 100%)";
const BL = [RELIEF, VC1];
let maskOn = null;
const setMask = (on) => { if (on === maskOn) return; maskOn = on; BL.forEach((el) => { const v = on ? FEATHER : "none"; el.style.webkitMaskImage = v; el.style.maskImage = v; el.style.webkitMaskComposite = on ? "source-in" : ""; el.style.maskComposite = on ? "intersect" : ""; }); };
// ---------- the one camera (clamped inside the vicksburg map once the mississippi layer is gone) ----------
const OVS = 1920 / AR[2];
const cam = { cx: 0, cy: 0, s: OVS };
const applyCam = () => { let s = cam.s, cx = cam.cx, cy = cam.cy;
  if (s >= 0.6) { const k = Math.min(1, (s - 0.6) / 0.2), cl = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
    const ccx = cl(cx, 960 / s, 2880 - 960 / s), ccy = cl(cy, 540 / s, 1620 - 540 / s); cx += (ccx - cx) * k; cy += (ccy - cy) * k; }
  gsap.set(WORLD, { x: 960 - cx * s, y: 540 - cy * s, scale: s }); CAM_S = s; setInv();
  const op = s <= 0.27 ? 1 : s >= 0.56 ? 0 : 1 - Math.log(s / 0.27) / Math.log(0.56 / 0.27);
  PW.style.opacity = op.toFixed(3); RLINE.style.opacity = op.toFixed(3); setMask(s < 0.75); };
const camTo = (t, dur, c, s, ease = "sine.inOut") => tl.to(cam, { cx: c[0], cy: c[1], s, duration: Math.max(dur, 0.01), ease, onUpdate: applyCam }, t);
const zoom = (t, dur, c0, s0, c1, s1, P, ease = "power2.inOut") => {
  const d0 = [(P[0] - c0[0]) * s0, (P[1] - c0[1]) * s0], d1 = [(P[0] - c1[0]) * s1, (P[1] - c1[1]) * s1], q = { u: 0 };
  tl.fromTo(q, { u: 0 }, { u: 1, duration: dur, ease, immediateRender: false, onUpdate: () => { const u = q.u, s = Math.exp(Math.log(s0) + (Math.log(s1) - Math.log(s0)) * u);
    cam.s = s; cam.cx = P[0] - (d0[0] + (d1[0] - d0[0]) * u) / s; cam.cy = P[1] - (d0[1] + (d1[1] - d0[1]) * u) / s; applyCam(); } }, t); };
const OC0 = [AR[0] + AR[2] / 2, AR[1] + AR[3] / 2];
const S0 = OVS * 1.04, C0 = [OC0[0], OC0[1]];
const C1 = L(32.75, -90.85), S1 = 0.215;                         // the delta north of Vicksburg (Yazoo Pass to the city)
const C2 = L(32.52, -90.98), S2 = 0.92;                          // the Vicksburg map, wide (Lake Providence, Steele's Bayou, De Soto Point)
const C3 = L(32.30, -91.02), S3 = 1.25;                          // m2-2: Milliken's Bend to Hard Times
const C4 = L(32.345, -90.90), S4 = 2.35;                         // the push onto Vicksburg (hand-off to m2b)
cam.cx = C0[0]; cam.cy = C0[1]; applyCam();
camTo(0, T_WINT - 0.2, [C0[0] + (VKS[0] - C0[0]) * 0.35, C0[1] + (VKS[1] - C0[1]) * 0.35], OVS * 1.16, "sine.inOut");
camTo(T_WINT - 0.2, T_CAN - 0.6 - T_WINT + 0.2, C1, S1, "sine.inOut");
const TZ0 = T_CAN - 0.6, TZ1 = T_CAN + 1.5;
zoom(TZ0, TZ1 - TZ0, C1, S1, C2, S2, L(32.42, -90.95), "power2.inOut"); SFX("whoosh", TZ0 - 0.05);
tl.to(VC1, { autoAlpha: 0, duration: 2.8, ease: "sine.inOut" }, TZ0);   // option 1 -> option 2, seamless during the dive
camTo(TZ1 + 0.02, T_DIFF - TZ1, [C2[0] - 10, C2[1] + 30], S2 * 1.05, "sine.inOut");
camTo(T_DIFF, T_CROSS - T_DIFF, C3, S3, "sine.inOut");
camTo(T_CROSS, T_ONLY - T_CROSS, [C3[0] + 20, C3[1] - 10], S3 * 1.08, "sine.inOut");
camTo(T_ONLY, END - T_ONLY, C4, S4, "sine.inOut");
// ---------- HUD ----------
B.title("MOVE 2", "THE MISSISSIPPI", "1863", T_MS, T_MS + 3.0); SFX("ref:boom", T_MS + 0.1);
B.showDate(T_WINT); B.date("WINTER 1862 - 63", T_WINT + 0.05, T_DIFF - 0.1, 32); B.date("20 APRIL 1863", T_DIFF, END + 1, 32);
const LGD = legend(T_MS + 3.4, TZ0 + 1.0), LGD2 = legend(TZ0 + 1.5, END + 1, true);   // squares on the wide shot, glowing lines on the close-ups
// ---------- flags: overview pair, delta pair, Vicksburg-map pair (both on every frame) ----------
flagS(FL.us, "", ...L(35.45, -88.9), 0, T_WINT + 0.6); flagS(FL.cs, "", ...L(32.2, -89.0), 0, T_WINT + 0.6);
flagS(FL.us, "", ...L(32.36, -91.38), T_WINT + 0.5, TZ0 + 1.1); flagS(FL.cs, "", ...L(32.95, -89.7), T_WINT + 0.55, TZ0 + 1.1);
flagS(FL.us, "", ...L(32.62, -91.36), TZ0 + 1.2, T_DIFF - 0.2); flagS(FL.cs, "", ...L(32.58, -90.45), TZ0 + 1.25, T_DIFF - 0.2);
flagS(FL.us, "", ...L(32.44, -91.40), T_DIFF - 0.1, T_ONLY + 0.4); flagS(FL.cs, "", ...L(32.20, -90.62), T_DIFF - 0.05, T_ONLY + 0.4);
flagS(FL.us, "", ...L(32.42, -91.20), T_ONLY + 0.5, END + 1); flagS(FL.cs, "", ...L(32.30, -90.80), T_ONLY + 0.55, END + 1);
// ---------- big towns (A2, constant ~36 px; names leave after ~3.5 s, clean screen) ----------
townL("MEMPHIS", MEM, "r", 0.6); townL("NEW ORLEANS", NO, "l", 0.8); townL("JACKSON", JAX, "r", T_LINK + 0.2);
townL("VICKSBURG", VKS, "r", 0.15); townL("VICKSBURG", VKS, "r", TZ1 + 0.2); townL("VICKSBURG", VKS, "l", T_RUN - 0.3, { shrink: [[T_RUN - 0.3, null]] });
// =================== m2-1 ===================
// frame 0: the river war already moving: Union gunboats come down from Memphis; Grant's army above the city; the batteries on the bluff
const FYP = nearestF(RIV, YP);
const GBN = [0, 1, 2].map((k) => ship("gunboat", sub(RIV, 0.03 + k * 0.03, FYP - 0.012 - k * 0.012, 20), 0, T_FREE + 0.8, TZ0 + 0.6, { s: 20, t0: 0 }));
// overview: one army counter each side (spread apart); the corps counters appear when the camera reaches the Vicksburg map
unitS("oa", "carth", L(32.95, -91.75), "infantry", "", { size: "XXXX" }); unitS("ov", "rome", L(32.30, -90.20), "infantry", "", { size: "XXXX" });
["oa", "ov"].forEach((id) => gsap.set(B.units[id].el, { autoAlpha: 1 })); B.hideUnits(["oa", "ov"], TZ0 + 0.3, 0.4);
along("oa", LL([[32.95, -91.75], [32.80, -91.55]]), 0, 10, 10);
unitS("ga", "carth", L(32.62, -91.25), "infantry", "XV", { size: "XXX", t: TZ0 + 1.0 }); unitS("gb", "carth", L(32.95, -91.30), "infantry", "XVII", { size: "XXX", t: TZ0 + 1.1 });
unitS("gc", "carth", L(32.46, -91.24), "infantry", "XIII", { size: "XXX", t: TZ0 + 1.2 });
along("gb", LL([[32.95, -91.30], [32.85, -91.26]]), 0, 8, 10); along("ga", LL([[32.62, -91.25], [32.56, -91.20]]), 0, 9, 10);
unitS("vk", "rome", L(32.44, -90.62), "infantry", "", { size: "XXX", t: TZ0 + 1.0 });
along("vk", LL([[32.44, -90.62], [32.42, -90.70]]), 0, 6, 10);

// the river glows on "Mississippi River"; Vicksburg ringed on "a bluff"
glowPath(RIV, "#8fc3ff", 6.5 / 0.185, T_RIV - 0.3, T_WEST + 0.5, 2, 0.95, { draw: 1.6, top: true });
K.target(VKS[0], VKS[1], T_BLUFF, { r: 230, side: "#ff3b30", until: T_WINT + 0.4 });
// "As long as the Confederates held it": the batteries pulse, a shot at the lead gunboat; the boats stop short of the city
unitS("bt0", "rome", L(32.42, -90.80), "artillery", "", { t: T_HELD - 0.2, w: 44, h: 29, until: TZ0 + 0.5 });
shootS(L(32.42, -90.80), GBN[0].at(T_FREE + 1.2), T_FREE + 0.3, 0.183, { dur: 0.9, h: 50, r: 12 });
B.caption("THE UNION COULD NOT USE THE RIVER FREELY", T_FREE - 0.1, T_LINK - 0.1, "rome");
// "the South stayed linked to its western states": the rail line Monroe - De Soto Point - Vicksburg - Jackson, red arrows across the river
const LINK = LL([[32.525, -93.75], [32.50, -92.12], [32.40, -91.50], [32.33, -90.95], [32.352, -90.878], [32.33, -90.55], [32.30, -90.19]]);
glowPath(LINK, "#ff6a5a", 3.4 / 0.19, T_LINK - 0.2, T_WINT + 0.6, 2, 0.9, { draw: 1.6, top: true });
[[[32.0, -94.4], [32.25, -92.9], [32.36, -91.6], [32.35, -90.95]], [[33.6, -93.6], [33.0, -92.4], [32.55, -91.4], [32.38, -90.95]], [[31.2, -93.6], [31.7, -92.4], [32.2, -91.5], [32.33, -90.97]]]
  .forEach((q, k) => arw({ pts: LL(q), side: "rome", t: T_LINK + 0.1 + k * 0.25, dur: 1.4, width: AW(OVS * 1.12, 12), until: T_WINT + 0.5 }));
boxL("WESTERN STATES", ...L(32.2, -94.9), T_WEST - 0.1, null, { size: 20 });
// "All winter, every attempt from the north failed in the swamps": three routes draw, stop short and grey
const TRY = [[[34.40, -90.62], [34.10, -90.40], [33.80, -90.30], [33.56, -90.20]],                                   // Yazoo Pass -> Fort Pemberton
  [[32.42, -91.00], [32.60, -90.92], [32.80, -90.86], [32.92, -90.86]],                                               // Steele's Bayou (up the bayous)
  [[32.40, -90.97], [32.44, -90.88], [32.47, -90.82]]];                                                                // Chickasaw Bayou (Dec 1862)
const TRYA = TRY.map((q, k) => arw({ pts: LL(q), side: "carth", t: T_WINT + 0.3 + k * 0.55, dur: 1.2, width: AW(0.2, 13), dash: k === 0 ? "18 10" : null, until: TZ0 + 0.6 }));
TRYA.forEach((g, k) => B.greyArrow(g, T_FAIL + 0.1 + k * 0.2, TZ0 + 0.6));
TRY.forEach((q, k) => { const p = L(...q[q.length - 1]); pinS(GG.pin(`<svg width="34" height="34" viewBox="-10 -10 20 20" style="display:block;filter:drop-shadow(0 0 3px #000)"><path d="M-7 -7 L7 7 M7 -7 L-7 7" stroke="#ff4a3d" stroke-width="3.4" stroke-linecap="round"/></svg>`, p[0], p[1], { t: T_FAIL + 0.15 + k * 0.2, pop: true, until: TZ0 + 0.4 })); });
wstampL("FAILED IN THE SWAMPS", ...L(33.2, -90.0), T_FAIL + 0.2, null, "#e3232f", 26);
// =================== the dive onto the Vicksburg map ===================
// "Canals dug in the mud": the canal across De Soto Point; "bayous cleared for gunboats": Lake Providence + Steele's Bayou; "boats stuck among the trees"
const CANAL = LL([[32.375, -90.925], [32.355, -90.928], [32.335, -90.925], [32.318, -90.918]]);
const cn = glowPath(CANAL, "#c9a26a", 7, T_CAN, T_DIFF - 0.3, 1, 0.95, { draw: 1.0, dash: "10 6", top: true });
boxL("CANAL", ...L(32.33, -91.10), T_CAN + 0.2, null, { size: 18 });
const LPR = LL([[32.80, -91.17], [32.72, -91.30], [32.60, -91.42], [32.45, -91.52], [32.30, -91.55]]);
glowPath(LPR, "#8fc3ff", 6, T_BAY - 0.1, T_DIFF - 0.3, 1, 0.8, { draw: 1.4, dash: "4 7" });
const STEE = LL([[32.42, -90.98], [32.55, -90.93], [32.68, -90.90], [32.80, -90.88], [32.86, -90.87]]);
glowPath(STEE, "#8fc3ff", 6, T_BAY + 0.2, T_DIFF - 0.3, 1, 0.8, { draw: 1.4, dash: "4 7" });
const STK = [0, 1, 2].map((k) => ship("gunboat", sub(STEE, 0.1 + k * 0.08, 0.62 + k * 0.1, 10), T_BAY + 0.1, T_STUCK - T_BAY + 0.2, T_DIFF - 0.4, { s: 20, t0: T_BAY + 0.1 }));
STK.forEach((b, k) => tl.to(b.sv, { rotation: `+=${k % 2 ? 9 : -9}`, duration: 0.22, yoyo: true, repeat: 7, ease: "sine.inOut" }, T_STUCK + 0.2 + k * 0.1));
boxL("STUCK", ...L(32.80, -90.70), T_STUCK + 0.2, null, { size: 18, bg: "#f3d6c8" });
const NOTH = sstamp("NOTHING WORKED", 760, T_NOTH, { size: 76, shake: 4, until: T_NOTH + 1.6 });
// "Many in the North believed Grant had run out of ideas" (belief card; Grant's badge waits until it leaves)
const BEL = belief("RUN OUT OF IDEAS", "WHAT MANY IN THE NORTH BELIEVED", T_IDEAS - 0.7, T_DIFF - 0.15, { top: 160, size: 52 });
// ---------- option 2 fronts (close-ups): the Union west-bank ground (1 Apr: Lake Providence - Young's Point; 20 Apr: down to New Carthage),
// red band on the Confederate side; same ground as tools/vk_make_control.py vick(). Cross-fades instead of the old apr1 -> apr20 fill.
const RIVN_ = [[32.40, -91.00], [32.48, -91.06], [32.60, -91.12], [32.80, -91.16], [33.05, -91.12], [33.40, -91.08]];   // the river, south -> north
const FA = front2(LL([[33.40, -91.47], [32.90, -91.45], [32.55, -91.40], [32.33, -91.30], [32.33, -91.10], [32.33, -90.898], [32.345, -90.893], [32.37, -90.895], [32.375, -90.93], ...RIVN_]),
  1.0, TZ0 + 0.7, { flip: true, dur: 1.8, until: CUE });
const frB = (s) => front2(LL([[33.40, -91.50], [32.90, -91.47], [32.55, -91.45], [32.25, -91.42], [32.02, -91.25], [32.02, -91.09], [32.04, -91.07], [32.13, -91.04], [32.247, -90.935],
  [32.30, -90.90], [32.345, -90.893], [32.37, -90.895], [32.375, -90.93], ...RIVN_]), s, 0, { flip: true, dur: 0.01 });
const FB = frB(1.5), FC = frB(2.1);
gsap.set([FB, FC], { opacity: 0 }); tl.to(FB, { opacity: 1, duration: 2.4, ease: "sine.inOut" }, CUE); tl.to(FB, { opacity: 0, duration: 2.0, ease: "sine.inOut" }, T_ONLY + 0.3);
tl.to(FC, { opacity: 1, duration: 2.0, ease: "sine.inOut" }, T_ONLY + 0.3);
// =================== m2-2: Grant's idea ===================
const GB = cmd("grant", "ULYSSES S. GRANT", "ARMY OF THE TENNESSEE", "carth", "bl", T_DIFF + 0.3, T_RUN + 0.2);
// "march his army down the west bank, through the Louisiana swamps": Milliken's Bend - Richmond - Perkins' plantation - Hard Times
const MARCH = LL([[32.48, -91.08], [32.42, -91.15], [32.39, -91.18], [32.28, -91.20], [32.16, -91.17], [32.09, -91.13], [32.07, -91.09]]);
tl.to(B.units.gb.el, { autoAlpha: 0, duration: 0.4 }, T_DIFF);
along("gc", [L(32.46, -91.24), MARCH[0]], T_DIFF - 0.2, 1.0, 6); along("gc", MARCH, T_MARCH, T_CROSS + 1.2 - T_MARCH, 24);
along("ga", [L(32.56, -91.20), L(32.53, -91.13)], T_DIFF, 1.2, 6); along("ga", [L(32.53, -91.13), ...sub(MARCH, 0, 0.7, 16)], T_MARCH + 1.4, T_CROSS + 1.6 - T_MARCH, 20);
arw({ pts: MARCH, side: "carth", t: T_MARCH, dur: 2.6, width: AW(S3, 14), until: T_ONLY + 0.6 });
boxL("MILLIKEN'S BEND", MIL[0] + 70, MIL[1] - 30, T_MARCH - 0.1, null, { size: 16 });
boxL("LOUISIANA SWAMPS", ...L(32.25, -91.40), T_LA, null, { size: 16, bg: "#dcecf8" });
// three large bayous bridged on the way (pontoon icons)
[[32.40, -91.17, 70], [32.22, -91.195, 60], [32.12, -91.16, 40]].forEach(([la, lo, a], k) => pinS(GG.pin(`<svg width="40" height="22" viewBox="0 0 40 22" style="display:block;overflow:visible;transform:rotate(${a}deg);filter:drop-shadow(0 0 3px rgba(120,170,255,.9))">${[0, 1, 2, 3, 4, 5].map((j) => `<ellipse cx="${3.3 + j * 6.7}" cy="11" rx="2.2" ry="7" fill="#3a3024" stroke="#c9b48a" stroke-width="0.8"/>`).join("")}<rect x="0" y="7" width="40" height="8" fill="#e9dcc0" stroke="#1f4fc4" stroke-width="1.4"/></svg>`, ...L(la, lo), { t: T_LA + 0.3 + k * 0.4, pop: true, until: END + 1 })));
boxL("HARD TIMES", HT[0] + 60, HT[1] + 26, T_CROSS - 0.6, null, { size: 16 });
// "and cross the river below the city": the dashed crossing (east bank target)
arw({ pts: [L(32.06, -91.10), L(32.00, -91.06), L(31.97, -91.02)], side: "carth", t: T_CROSS, dur: 1.0, width: AW(S3, 12), dash: "14 10", until: T_ONLY + 0.6 });
K.target(...L(31.98, -91.02), T_CROSS + 0.5, { r: 30, side: "carth", until: T_ONLY + 1 });
// "he needed boats and transports on the south side": ghost outlines below the city at Hard Times
const GHOST = [[32.085, -91.075], [32.06, -91.065], [32.035, -91.075]].map(([la, lo], k) => { const s = ship(k === 1 ? "transport" : "gunboat", [L(la, lo)], T_NEED + k * 0.25, 1, T_ONLY + 1.4, { s: 20 });
  tl.set(s.el, { autoAlpha: 1 }, T_NEED + k * 0.25); tl.fromTo(s.el, { opacity: 0 }, { opacity: 0.45, duration: 0.4, yoyo: true, repeat: 5, immediateRender: false }, T_NEED + k * 0.25); gsap.set(s.sv, { rotation: 100 }); return s; });
boxL("THE SOUTH SIDE", ...L(32.00, -91.24), T_SOUTH, null, { size: 16 });
// "run them past the guns of Vicksburg": the boats wait above the city (Young's Point), the batteries along the bluff, two visible shots
const BAT = LL([[32.378, -90.872], [32.351, -90.877], [32.324, -90.886]]).map((p) => [p[0] + 12, p[1]]);
BAT.forEach((p, k) => unitS("bat" + k, "rome", p, "artillery", "", { t: T_ONLY + k * 0.15, w: 44, h: 29 }));
const UP = [0, 1, 2, 3].map((k) => ship(k === 3 ? "transport" : "gunboat", sub(LL([[32.45, -91.02], [32.42, -91.0], [32.402, -90.994], [32.394, -90.960], [32.387, -90.930]]), 0.3 - k * 0.1, 0.85 - k * 0.12, 8), T_ONLY - 0.3 + k * 0.2, 3.0, END + 1, { s: 20 }));
trail([...sub(LOOP63, 0.25, 1, 12), ...LL([[32.30, -90.917], [32.27, -90.957], [32.24, -90.975]])], "#8fb2ff", 3.2, T_RUN - 0.2, 1.8, END + 1, "4 9");
shootS(BAT[0], L(32.386, -90.925), T_RUN + 0.2, 2.2, { dur: 0.7, h: 30, r: 9 });
shootS(BAT[1], L(32.382, -90.905), T_RUN + 1.3, 2.3, { dur: 0.7, h: 30, r: 9 });
B.hideUnits(["ga", "gc"], T_ONLY + 1.0, 0.6);
// ---------- 1c declutter: the legend + the corner badge step out while a big card is up (the date scroll stays) ----------
declutter([LGD, LGD2, GB], [[T_NOTH, T_NOTH + 1.6], [T_IDEAS - 0.7, T_DIFF - 0.15]]);
fixImgs();
K.raiseTerritory();
B.finish();
