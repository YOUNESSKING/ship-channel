// MOVE 2d (m2-8 .. m2-9), Arnold #17: the chase south (12-13 Oct 1776), the burning at Arnold's Bay, the walk to Crown Point; then the whole
// lake: the cost, the British at Crown Point, Ticonderoga, 2 Nov first snow, back to Canada; method card. Map agent "va".
//   python3 tools/va_inline.py m2d champsouth_hd_lift m2-8 m2-9
// ONE world = champsouth map px (z11). The `champlain` map (z9) sits in it at its true place and scale (4x; vk_body_m2a technique): one camera
// drives the champsouth close-ups (s 1.1 - 1.7) and zooms out to the whole lake (s ~0.24); the champlain layer fades in between s 0.56 and 0.27
// over the edge-feathered champsouth relief (no cut, no white flash).
// m2-8  date 12 OCT -> 13 OCT; the American boats run south, the red ships close in; WASHINGTON greys on "surrendered"; CONGRESS + 4 gondolas run
//       into the bay on the Vermont shore and burn with their flags flying; a dotted blue line walks through the woods to CROWN POINT; a red
//       ambush marker on the road behind them on "an ambush".
// m2-9  zoom out to `champlain`; cost card (each line on its words; British column on "The British lost fewer"); A DEFEAT stamp; the British take
//       Crown Point, look at Ticonderoga (card TICONDEROGA · 9,000 DEFENDERS); 2 NOVEMBER 1776, snow; red arrows back north to Canada.
//       "More than a century later" .. "on Lake Champlain." is covered by the main session's archive insert: nothing essential there.
//       Method card on "Arnold had chosen the place".
// Facts: FACTCHECK_B (Washington struck about noon 13 Oct; Congress + 4 gondolas burned "in a small Creek ten Miles from Crown Point on the
// East Side"; ~200 walked to Crown Point, ambush laid ~2 hours after; ten or eleven of 15 vessels, "Eighty odd" K&W, ~110 prisoners; British
// under 40; ~9,000 at Ticonderoga; British left for Canada 2 Nov, first snow).
// @@KIT
// @@DATA
const SZ = GD.maps.champsouth, CZ = GD.maps.champlain;
const L = GG.proj(11, SZ.origin_world_px[0], SZ.origin_world_px[1]);
const LL = (pts) => pts.map(([la, lo]) => L(la, lo));
const P8 = "m2-8", P9 = "m2-9";
const T_CHASE = at(P8, "chased him south"), T_2D = at(P8, "two days"), T_BATT = at(P8, "battered boats"), T_NOON = at(P8, "Around noon"), T_13 = at(P8, "thirteenth"),
  T_WCAU = at(P8, "the Washington was caught"), T_SURR = at(P8, "surrendered"), T_FOUGHT = at(P8, "Arnold fought on"), T_4G = at(P8, "four gondolas"),
  T_2H = at(P8, "more than two hours"), T_ASH = at(P8, "ran them ashore"), T_VT = at(P8, "Vermont side"), T_FIRE = at(P8, "set them on fire"), T_FLAGS = at(P8, "flags still flying"),
  T_200 = at(P8, "about two hundred men"), T_WOODS = at(P8, "through the woods"), T_CP = at(P8, "Crown Point"), T_AMB = at(P8, "an ambush"), T_AFTER = at(P8, "just after they went by");
const T_P9 = B.T.paras[P9][0], T_1011 = at(P9, "ten or eleven"), T_80 = at(P9, "eighty men"), T_100 = at(P9, "more than a hundred captured"), T_BR40 = at(P9, "The British lost fewer"),
  T_SEA = at(P9, "As a sea battle"), T_DEF = at(P9, "a defeat"), T_TOOK = at(P9, "But the British took Crown Point"), T_TIC = at(P9, "looked at Ticonderoga"),
  T_9000 = at(P9, "nine thousand"), T_LATE = at(P9, "too late in the year"), T_NOV = at(P9, "second of November"), T_SNOW = at(P9, "first snow"), T_CAN = at(P9, "back to Canada"),
  T_ARCH = at(P9, "More than a century later"), T_ARCH1 = at(P9, "on Lake Champlain."), T_CHOSE = at(P9, "Arnold had chosen the place"),
  T_PART2 = at(P9, "the second part of his method"), T_LET = at(P9, "let the ground and the weather fight for you");
// ---------- places (champsouth z11 px; checked on the DEM: Valcour island x 1365-1406 y 367-427, Schuyler island ~1446,646) ----------
const VAL = L(44.61, -73.43), SCH = [1446, 646], SPL = L(44.27, -73.32), BAY = [1478, 1285], CRP = L(44.027, -73.424), TIC = L(43.843, -73.387), STJ = L(45.30, -73.26),
  SKE = L(43.555, -73.404), MTL = L(45.50, -73.57);
// the run south (lake centre line), 12-13 Oct
const RUN = [[1370, 440], [1400, 520], [1446, 610], [1470, 700], [1470, 800], [1500, 900], [1530, 1000], [1540, 1080], [1530, 1160], [1505, 1230], [1488, 1272]];
const WALK = [[1492, 1290], [1500, 1350], [1497, 1420], [1478, 1490], [1445, 1550], [1410, 1590], [1388, 1606]];
// ---------- world: champlain copy under the relief (beyond the feathered edges), the champsouth layers, champlain layer on top ----------
const AR = [CZ.origin_world_px[0] * 4 - SZ.origin_world_px[0], CZ.origin_world_px[1] * 4 - SZ.origin_world_px[1], 11520, 6480];
const group = (parent, before) => { const g = document.createElement("div"); g.style.cssText = `position:absolute;left:${AR[0]}px;top:${AR[1]}px;width:${AR[2]}px;height:${AR[3]}px;isolation:isolate;`; parent.insertBefore(g, before); return g; };
const gimg = (src, parent, mx) => { const i = document.createElement("img"); i.src = src; i.alt = ""; i.style.cssText = `position:absolute;left:0;top:0;width:100%;height:100%;${mx ? `mix-blend-mode:multiply;filter:${SOFT};` : ""}`; parent.appendChild(i); return i; };
const RELIEF = document.getElementById("relief");
const PU = group(WORLD, RELIEF); gimg("assets/media/va_champlain_relief.jpg", PU, false); gimg("assets/media/va_champlain_ctl_soft.png", PU, true);
const PW = group(WORLD, OVL); gimg("assets/media/va_champlain_relief.jpg", PW, false); const PWC = gimg("assets/media/va_champlain_ctl_soft.png", PW, true);
living(SZ.meters_per_px, [], { n: 5, clouds: 0.1 });
const FEATHER = "linear-gradient(to right, transparent 0%, #000 10%, #000 90%, transparent 100%), linear-gradient(to bottom, transparent 0%, #000 10%, #000 90%, transparent 100%)";
let maskOn = null;
const setMask = (on) => { if (on === maskOn) return; maskOn = on; [RELIEF].forEach((el) => { const v = on ? FEATHER : "none"; el.style.webkitMaskImage = v; el.style.maskImage = v; el.style.webkitMaskComposite = on ? "source-in" : ""; el.style.maskComposite = on ? "intersect" : ""; }); };
// ---------- the one camera ----------
const cam = { cx: 1450, cy: 700, s: 1.1 };
const applyCam = () => { let s = cam.s, cx = cam.cx, cy = cam.cy;
  if (s >= 0.6) { const k = Math.min(1, (s - 0.6) / 0.2), cl = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
    const ccx = cl(cx, 960 / s, 2880 - 960 / s), ccy = cl(cy, 540 / s, 1620 - 540 / s); cx += (ccx - cx) * k; cy += (ccy - cy) * k; }
  gsap.set(WORLD, { x: 960 - cx * s, y: 540 - cy * s, scale: s }); CAM_S = s; setInv();
  const op = s <= 0.27 ? 1 : s >= 0.56 ? 0 : 1 - Math.log(s / 0.27) / Math.log(0.56 / 0.27);
  PW.style.opacity = op.toFixed(3); setMask(s < 0.75); };
const camTo = (t, dur, c, s, ease = "sine.inOut") => tl.to(cam, { cx: c[0], cy: c[1], s, duration: Math.max(dur, 0.01), ease, onUpdate: applyCam }, t);
const sAt = (t) => cam.s;   // (shots below happen only on the champsouth close-ups; their scale is given explicitly)
applyCam();
const CW = L(44.5, -73.38);                       // the whole-lake view centre (champlain map, wide)
camTo(0, T_NOON - 0.5, [1470, 820], 1.15);
// (T_NOON - 0.5 .. T_SURR + 1.2: the camera holds on the WASHINGTON; set below, once her position is known)
camTo(T_SURR + 1.2, T_FIRE - T_SURR - 1.2, [1490, 1240], 1.7);
camTo(T_FIRE, T_CP - T_FIRE, [1470, 1360], 1.5);
camTo(T_CP, T_P9 - T_CP, [1450, 1380], 1.45);
SFX("whoosh", T_P9 - 0.1);
camTo(T_P9 - 0.2, 3.8, [CW[0], CW[1] - 200], 0.235, "power2.inOut");
camTo(T_P9 + 3.6, T_TOOK - T_P9 - 3.6, [CW[0], CW[1] - 260], 0.24);
camTo(T_TOOK, T_CAN - T_TOOK, [CW[0], CW[1] + 300], 0.26);
camTo(T_CAN, END - T_CAN, [CW[0], CW[1] - 500], 0.23);
// ---------- HUD ----------
B.showDate(0); B.date("12 OCTOBER 1776", 0, T_13 - 0.1, 32); date0(); B.date("13 OCTOBER 1776", T_13, T_NOV - 0.1, 32); B.date("2 NOVEMBER 1776", T_NOV, END + 1, 32);
const LGD = legend(0.6, T_P9 + 1.0, true), LGD2 = legend(T_P9 + 3.6, END + 1);
// flags (both on every frame): close-ups = Continental Colours on the New York shore, Union Flag out on the lake with the British ships;
// whole lake = Union Flag on Canada, Continental Colours on the American side
// audit #11/#12/#15/#16 (2026-11-03): flags on their own LAND, in frame, clear of the boats, labels, legend, badge and date scroll (tools/va_flagsolve.py):
// close-ups: the Union Flag on the New York shore north of the fight, the Continental Colours on the Vermont shore; whole lake: Union Flag on Canada,
// Continental Colours on Vermont. During the zoom-out each pair cross-fades.
flagS(FL.cs, "", 1349, 1095, 0, 31.4); flagS(FL.us, "", 1645, 1082, 0, 29.5);
flagS(FL.cs, "", 3720, -788, 30.6, END + 1); flagS(FL.us, "", 2051, 1138, 28.9, END + 1);
// =================== m2-8: the chase ===================
// the American boats (ahead) and the red ships (behind), frame 0 already moving
const AMK = ["galley", "gondola", "gondola", "gondola", "gondola", "galley", "schooner", "galley"];   // Congress = index 5, Washington = index 7 (the rear)
const AMB = AMK.map((kind, k) => ship(kind, sub(RUN, Math.max(0, 0.30 - k * 0.04), 0.60 - k * 0.035, 30), 0, T_NOON + 1, null, { s: 22, t0: 0 }));
const RDK = ["schooner", "ship", "schooner", "gunboat2", "gunboat2", "gunboat2"];
const RD = RDK.map((kind, k) => ship(kind, sub(RUN.map(([x, y]) => [x + 14, y]), Math.max(0, 0.02 - k * 0.0), 0.50 - k * 0.025, 30).map(([x, y], j) => [x + ((k % 2) ? 22 : -10), y - k * 18]), 0, T_NOON + 2, null, { side: "rome", s: kind === "ship" ? 26 : 22, t0: 0 }));
boxL("SCHUYLER ISLAND", SCH[0] + 40, SCH[1] - 30, 0.8, null, { size: 10 });
arw({ pts: [[1590, 560], [1600, 760], [1590, 960]], side: "rome", t: T_CHASE, dur: 2.2, width: AW(1.15, 12), until: T_NOON + 1 });
// 13 Oct: the Washington caught and surrendered (about noon)
const WAS = AMB[7], CON = AMB[5];
const wq = WAS.at(T_NOON + 1);
camTo(T_NOON - 0.5, T_SURR + 1.2 - T_NOON + 0.5, [wq[0] + 70, wq[1] + 170], 1.4);   // fix: the WASHINGTON's capture stays in frame (it was under the legend)
tl.to(WAS.el, { left: wq[0] + 4, top: wq[1] + 30, duration: T_SURR - T_NOON, ease: "sine.out" }, T_NOON + 1.0);
// audit #25 (2026-11-03): only three readable broadsides in the whole chase (two into the WASHINGTON, one into the CONGRESS), nothing unseen
const BIG = { dur: 0.7, h: 26, r: 15, fl: 34, aw: 2.8 };
// red ships: after T_NOON + 2 they follow their own pinAlong path (below), so positions come from that path
const rdPath = (k) => { const q = RD[k].at(T_NOON + 2); return [q, [1545 + (k % 3) * 18, 1150 + k * 10], [1520 + (k % 3) * 22, 1215 + (k % 2) * 16]]; };
const rdAt = (k, t) => t <= T_NOON + 2 ? RD[k].at(t) : posOn(rdPath(k), Math.min(1, (t - T_NOON - 2) / (T_ASH + 1 - T_NOON - 2)));
[[T_WCAU - 1.4, 0], [T_WCAU + 0.6, 2]].forEach(([t, k]) => shootS(rdAt(k, t), [wq[0] + 6, wq[1] + 22], t, 1.45, BIG));
tl.to(WAS.sv, { filter: "grayscale(1) brightness(0.7)", duration: 0.5 }, T_SURR);
boxL("WASHINGTON", wq[0] - 150, wq[1] + 30, T_WCAU, null, { size: 12 });
wstampL("SURRENDERED", wq[0] + 60, wq[1] + 70, T_SURR, null, "#e3232f", 18);
// Arnold fights on in the Congress with four gondolas, then runs them ashore in the bay and burns them, flags flying
const AB = cmd("arnold", "BENEDICT ARNOLD", "GALLEY CONGRESS", "carth", "tr", T_FOUGHT, T_P9 - 0.3);
const FIVE = [5, 1, 2, 3, 4], BAYP = [[1480, 1278], [1470, 1268], [1490, 1266], [1466, 1288], [1488, 1292]];
FIVE.forEach((k, j) => { const b = AMB[k], q = b.at(T_NOON + 1), path = [q, [1505, 1180 + j * 6], [1495, 1235], BAYP[j]];
  pinAlong(b.el, path, T_FOUGHT + 0.2, T_ASH + 1.0 - T_FOUGHT, 14); });
{ const cp = [CON.at(T_NOON + 1), [1505, 1180], [1495, 1235], BAYP[0]], ct = posOn(cp, Math.min(1, (T_2H + 0.7 - T_FOUGHT - 0.2) / (T_ASH + 1.0 - T_FOUGHT)));
  shootS(rdAt(1, T_2H), ct, T_2H, 1.6, BIG); }
boxL("CONGRESS + 4 GONDOLAS", 1180, 1210, T_4G, null, { size: 12 });
boxL("MORE THAN TWO HOURS", 1180, 1150, T_2H + 0.2, null, { size: 11 });
// the red ships follow down the lake and stand off the bay
RD.forEach((b, k) => { const q = b.at(T_NOON + 2); pinAlong(b.el, [q, [1545 + (k % 3) * 18, 1150 + k * 10], [1520 + (k % 3) * 22, 1215 + (k % 2) * 16]], T_NOON + 2, T_ASH + 1 - T_NOON - 2, 12); });
boxL("VERMONT", 1640, 1300, T_VT, null, { size: 13 });
// fire + smoke columns over the beached boats; each keeps its flag on the hull (a small Continental Colours on a mast)
BAYP.forEach((p, j) => { fireGlowS(p[0], p[1], 18, T_FIRE + j * 0.25, END + 1); for (let tt = T_FIRE + 0.3 + j * 0.25; tt < T_P9 + 3; tt += 0.9) K.smoke(p[0], p[1] - 4, tt, { n: 1, r: 8, rise: 34, life: 3.0, alpha: 0.55, drift: 10 }); });
const HF = BAYP.map((p) => pinS(GG.pin(`<div style="position:relative;width:0;height:0"><div style="position:absolute;left:-1px;top:-30px;width:2px;height:30px;background:#2a2420"></div><img src="${FL.us}" style="position:absolute;left:1px;top:-30px;width:20px;border:0.5px solid #1a1712"></div>`, p[0], p[1], { t: T_FLAGS - 0.1, until: T_P9 + 1.2 })));
boxL("FLAGS STILL FLYING", 1560, 1240, T_FLAGS, null, { size: 12 });
// about two hundred men walk through the woods to Crown Point; an ambush on the road behind them
trail(WALK, "#8fb2ff", 2.6, T_200 - 0.2, T_CP + 1.0 - T_200, T_P9 + 1.0, "3 7");
unitS("walk", "carth", WALK[0], "infantry", "~200", { t: T_200 - 0.2 }); along("walk", WALK, T_200, T_CP + 1.0 - T_200, 16); B.hideUnits(["walk"], T_P9 + 0.8, 0.4);
boxL("CROWN POINT", CRP[0] + 70, CRP[1] - 62, T_CP, null, { size: 13 });   // audit #36: the place sits on the map's bottom edge: label above it, inside the frame
const AMBP = WALK[2];
const AMK2 = pinS(GG.pin(`<svg width="34" height="34" viewBox="-17 -17 34 34" style="display:block;overflow:visible;filter:drop-shadow(0 0 5px #ff3b30)"><circle r="13" fill="rgba(196,18,31,0.85)" stroke="#f7f3ea" stroke-width="2"/><path d="M-6 -6 L6 6 M6 -6 L-6 6" stroke="#f7f3ea" stroke-width="2.6"/></svg>`, AMBP[0] + 24, AMBP[1], { t: T_AMB, until: T_P9 + 1.0 }));
boxL("AMBUSH", AMBP[0] + 60, AMBP[1] - 10, T_AMB + 0.2, null, { size: 12, bg: "#f3d6c8" });
// =================== m2-9: the whole lake ===================
// cost card: each line on its spoken words
// audit #22 (2026-11-03): no 9 s card: two short American cards on their words, then the casualty card (both sides) ~3.5 s
const CA = placeCard("AMERICANS", "10 - 11 OF 15 VESSELS LOST", "left:0;right:0;top:220px;display:flex;justify-content:center;", T_1011 - 0.1, T_80 - 0.35); CA.firstElementChild.style.borderTopColor = "#1f4fc4"; SFX("hit", T_1011 + 0.1);
const CB = placeCard("AMERICANS", "~80 KILLED AND WOUNDED<span class='c2'> · 100+ CAPTURED</span>", "left:0;right:0;top:220px;display:flex;justify-content:center;", T_80 - 0.15, T_BR40 - 0.35); CB.firstElementChild.style.borderTopColor = "#1f4fc4"; SFX("hit", T_80 + 0.05);
{ const c2 = CB.querySelector(".c2"); gsap.set(c2, { autoAlpha: 0 }); tl.fromTo(c2, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3, immediateRender: false }, T_100); SFX("ref:pop", T_100); }
const COST = scr(`<div style="display:flex;gap:56px;padding:26px 48px 28px;background:rgba(18,16,12,0.93);border-top:6px solid #c9b48a;font-family:Oswald;font-weight:700;color:#f7f3ea;box-shadow:0 20px 40px rgba(0,0,0,.55)">
  <div style="min-width:420px"><div style="display:flex;align-items:center;gap:12px;padding-bottom:10px;margin-bottom:10px;border-bottom:3px solid #1f4fc4"><img src="${FL.us}" style="height:34px;border:1px solid #f7f3ea"><div style="font-size:30px;letter-spacing:.08em">AMERICANS</div></div>
    <div class="r1" style="font-size:36px;line-height:1.5">10 - 11 OF 15 VESSELS LOST</div><div class="r2" style="font-size:36px;line-height:1.5">~80 KILLED AND WOUNDED</div><div class="r3" style="font-size:36px;line-height:1.5">100+ CAPTURED</div></div>
  <div class="bc" style="min-width:330px"><div style="display:flex;align-items:center;gap:12px;padding-bottom:10px;margin-bottom:10px;border-bottom:3px solid #c4121f"><img src="${FL.cs}" style="height:34px;border:1px solid #f7f3ea"><div style="font-size:30px;letter-spacing:.08em">BRITISH</div></div>
    <div style="font-size:36px;line-height:1.5">FEWER THAN 40 LOST</div></div></div>`, "left:0;right:0;top:220px;display:flex;justify-content:center;", T_BR40 - 0.15, T_DEF - 0.25);
{ const el = COST.querySelector(".bc"); gsap.set(el, { autoAlpha: 0 }); tl.fromTo(el, { autoAlpha: 0, x: -20 }, { autoAlpha: 1, x: 0, duration: 0.4, immediateRender: false }, T_BR40); SFX("hit", T_BR40 + 0.1); }
// audit #36: the stamp high on the screen, clear of the CROWN POINT label (which comes in on "took Crown Point")
const DEF = sstamp("A DEFEAT", 250, T_DEF, { size: 70, shake: 4, until: T_DEF + 2.2 });
// the British take Crown Point and look at Ticonderoga
const RCP = ship("ship", LL([[44.75, -73.36], [44.35, -73.33], [44.06, -73.42]]), T_SEA, T_TOOK + 1.5 - T_SEA, T_CAN + 0.2, { side: "rome", s: 26 });
unitS("brcp", "rome", L(44.04, -73.46), "infantry", "", { size: "XX", t: T_TOOK + 0.2 });
townL("CROWN POINT", CRP, "l", T_TOOK + 0.1); townL("TICONDEROGA", TIC, "l", T_TIC);
unitS("tic", "carth", L(43.84, -73.36), "infantry", "", { size: "XX", t: T_TIC + 0.2 });
arw({ pts: LL([[44.02, -73.44], [43.95, -73.42], [43.88, -73.40]]), side: "rome", t: T_TIC + 0.2, dur: 1.4, width: AW(0.25, 12), dash: "10 8", until: T_LATE + 1 });
const C9 = placeCard("TICONDEROGA", "9,000 DEFENDERS", "left:0;right:0;top:220px;display:flex;justify-content:center;", T_9000 - 0.05, T_LATE - 0.1); C9.firstElementChild.style.borderTopColor = "#1f4fc4";
SFX("hit", T_9000 + 0.05);
boxL("TOO LATE IN THE YEAR", ...L(44.25, -73.95), T_LATE, null, { size: 14, bg: "#f3d6c8" });
// 2 November: first snow; the British go back north to Canada
B.snow(T_SNOW - 0.2, END + 1);
tl.to(B.units.brcp.el, { autoAlpha: 0, duration: 0.6 }, T_CAN - 0.2);
arw({ pts: LL([[44.03, -73.40], [44.40, -73.30], [44.80, -73.36], [45.25, -73.27]]), side: "rome", t: T_CAN - 0.1, dur: 3.0, width: AW(0.24, 15) });
ship("ship", LL([[44.06, -73.42], [44.5, -73.32], [45.0, -73.35], [45.28, -73.26]]), T_CAN, 9.0, null, { side: "rome", s: 26 });
townL("ST. JOHNS", STJ, "r", T_CAN + 2.6);
// method card (after the archive insert), line 2 = this move
GG.METHOD_TITLE = "ARNOLD'S METHOD";
// audit #20 (2026-11-03): line 1 (move 1) shown dim from the start, line 2 lit on its spoken words "let the ground and the weather fight for you", nothing else; ~3.5 s
GG.METHOD = ["GO WHERE HE SAYS NO ARMY CAN GO", "LET THE GROUND AND THE WEATHER FIGHT FOR YOU"];
const T_MC0 = T_LET - 0.6, T_MC1 = Math.min(END - 0.6, T_LET + 3.4);
const MC = GG.method(2, T_MC0, T_MC1, [T_MC0, T_LET]); MC.style.top = "400px";   // between the two flags MC.querySelectorAll(".row").forEach((r) => { r.style.fontSize = "38px"; });
{ const r1 = MC.querySelectorAll(".row")[0]; tl.getTweensOf(r1).forEach((tw) => tw.kill()); gsap.set(r1, { autoAlpha: 0.38, x: 0 }); }
SFX("ref:pop", T_LET);
// ---------- 1c declutter ----------
declutter([LGD, LGD2, AB], [[T_1011 - 0.1, T_DEF + 2.2], [T_9000 - 0.05, T_LATE - 0.1], [T_MC0, T_MC1]]);
fixImgs();
K.raiseTerritory();
B.finish();
