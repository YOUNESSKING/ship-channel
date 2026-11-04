// HOOK-B (hook-3 .. hook-4), Ulysses S. Grant #16. THE LOCKED HOOK (STYLE_LOCK 1a: back INTO the danger, the twist as action, the general
// enters as the TURN, name slam + 3 snap cuts + title; 1c: nothing before it is spoken, one big card at a time, visible fire only).
// Map agent hook (prefix gh_). Built with:  python3 tools/gh_inline.py hook-b donelson_hd_lift hook-3 hook-4
// World = the donelson map px (the relief). Snap-cut maps are full-size layers at the world origin, each shown only inside its cut (a black
// frame hides every camera jump): `henry` (z11, option 2), `vicksburg_siege` (z12, night, option 2), `jamesriver` (z12, option 2).
// hook-3: frame 0 = hook-a's last frame (16 Feb, the pocket blue, the garrison grey); "But a week is not how it looked": the clock rolls back
//   (16 -> 15 FEB, ticks), the white flag drops, the units step back to their dawn places; "At dawn": dawn light,
//   push in to the Union right, the two glowing front lines (option 2); "burst out": red columns break out
//   south, musket volleys where the lines touch (no artillery), the front bulges; "broken the Union right": McClernand's brigades fall back
//   (BROKEN); "the road out stood open": the Forge road toward Nashville glows; "The Union commander": the "?" badge; "not even there": the
//   empty headquarters (NOT EVEN THERE); "away on a gunboat ... the admiral": the camera follows the river to the flagship, the "?" rides
//   there; "when he rode back": the "?" rides back along the line (dotted trail); "standing in knots, holding muskets": knots of blue men;
//   NO AMMUNITION; "tons of it, close at hand": ammunition crates glow behind the line (TONS OF IT · CLOSE AT HAND).
// hook-4: the map dims, the "?" badge comes to the centre and turns into the real photo, ULYSSES S. GRANT slams (hit + shake); "a few weeks
//   earlier his own superior had brushed off his plan": the plan sketch card + BRUSHED OFF; 3 snap cuts (whoosh + hit): 1 TWO RIVERS (henry
//   map, Feb 1862: gunboats up both rivers, both forts blue), 2 THE MISSISSIPPI (vicksburg_siege, night: gunboats run past the bluff batteries,
//   visible shots), 3 ACROSS A RIVER (jamesriver, June 1864: the pontoon bridge, blue columns crossing; Lee's badge on his name, his army
//   facing the other way); title card on "three greatest" (riser + boom).
// Facts: FACTCHECK_A #17 (Grant away at Foote's flagship, men "standing in knots", "tons of it close at hand"), FACT_NOTES (Halleck brushed
// him off in January; Vicksburg run 16 Apr 1863; James River bridge 14 Jun 1864). No unspoken names: the superior is not named (no badge).
// @@KIT
// @@DATA
const LD = GG.proj(13, 535372, 819244), HP = GG.proj(11, 132617, 204167), VP = GG.proj(...GD.maps.vicksburg_siege), JP = GG.proj(...GD.maps.jamesriver);
const go = (id, t, dur, p, ease) => B.move(id, t, dur, p[0], p[1], ease || "power1.inOut");
const H3 = "hook-3", H4 = "hook-4", S4 = B.P(H4);
const T_MORN = at(H3, "the morning"), T_15 = at(H3, "fifteenth of February"), T_DAWN = at(H3, "At dawn"), T_BURST = at(H3, "burst out"),
  T_BROKE = at(H3, "broken the Union right"), T_ROAD = at(H3, "the road out"), T_OPEN = at(H3, "stood open"), T_CMDR = at(H3, "The Union commander"),
  T_NOT = at(H3, "not even there"), T_AWAY = at(H3, "away on a gunboat"), T_ADM = at(H3, "the admiral"), T_RODE = at(H3, "when he rode back"),
  T_KNOTS = at(H3, "standing in knots"), T_MUSK = at(H3, "holding muskets"), T_NOAMMO = at(H3, "no ammunition"), T_TONS = at(H3, "tons of it"),
  T_HAND = at(H3, "close at hand");
const T_NAME = at(H4, "Ulysses S. Grant"), T_FEW = at(H4, "a few weeks earlier"), T_SUP = at(H4, "his own superior"), T_BRUSH = at(H4, "brushed off"),
  T_PLAN = at(H4, "his plan"), T_TWO = at(H4, "He took two rivers"), T_CITY = at(H4, "He took the city"), T_MISS = at(H4, "the Mississippi"),
  T_MARCH = at(H4, "And he marched"), T_ACROSS = at(H4, "across a river"), T_LEE = at(H4, "Robert E. Lee"), T_OTHER = at(H4, "looking the other way"),
  T_THESE = at(H4, "These are"), T_GREAT = at(H4, "three greatest");
// =====================================================================================================================
// THE WORLD
// =====================================================================================================================
const RELIEF = document.getElementById("relief");
const TG = document.createElement("div"); TG.style.cssText = "position:absolute;left:0;top:0;width:2880px;height:1620px;"; WORLD.insertBefore(TG, OVL);
// owner 2026-11-02 (territory minimised): every map in hook-b is a close-up -> option 2 only (front lines, no ground tint)
const layer = (src, ctl) => { const g = document.createElement("div"); g.style.cssText = "position:absolute;left:0;top:0;width:2880px;height:1620px;isolation:isolate;";
  const i = document.createElement("img"); i.src = src; i.alt = ""; i.style.cssText = "position:absolute;left:0;top:0;width:100%;height:100%;"; g.appendChild(i);
  if (ctl) { const c = terrImg(ctl, g, 0, null, 0.01); }
  WORLD.insertBefore(g, OVL); gsap.set(g, { autoAlpha: 0 }); return g; };
const LHE = layer("assets/media/gh_hen_relief.jpg"), LVK = layer("assets/media/gh_vks_relief.jpg"), LJA = layer("assets/media/gh_jam_relief.jpg");
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); const NA = LV.north();
// ---------- camera (every map is 2880 x 1620: clamped inside) ----------
const cam = { cx: 1430, cy: 800, s: 1.9 };     // = hook-a's last camera
const applyCam = () => { const s = Math.max(cam.s, 1920 / 2880), cx = Math.min(Math.max(cam.cx, 960 / s), 2880 - 960 / s), cy = Math.min(Math.max(cam.cy, 540 / s), 1620 - 540 / s);
  gsap.set(WORLD, { x: 960 - cx * s, y: 540 - cy * s, scale: s }); CAM_S = s; setInv(); };
const camTo = (t, dur, c, s, ease = "sine.inOut") => tl.to(cam, { cx: c[0], cy: c[1], s, duration: Math.max(dur, 0.01), ease, onUpdate: applyCam }, t);
applyCam();
const scr0 = (html, css) => { const el = document.createElement("div"); el.style.cssText = "position:absolute;" + css; el.innerHTML = html; SCN.insertBefore(el, document.getElementById("credit")); GG.hide(el); return el; };
const vis = (t0, t1) => (el) => { gsap.set(el, { autoAlpha: 0 }); tl.set(el, { autoAlpha: 1 }, t0); if (t1 != null) tl.set(el, { autoAlpha: 0 }, t1 - 0.01); return el; };
const PINS = document.getElementById("pins");
const snap = () => new Set([...OVL.children, ...PINS.children]);
const endScope = (s0, until) => { const els = [...OVL.children, ...PINS.children].filter((e) => !s0.has(e) && e.tagName.toLowerCase() !== "defs"); tl.set(els, { autoAlpha: 0 }, until - 0.01); };
// ---------- places (donelson map px) ----------
const FD = [1395, 758], DOV = [1505, 768], HQ = [1170, 700], BOATP = [1300, 470], LAND = [1255, 560];
const RING = [[1300, 735], [1290, 790], [1305, 850], [1360, 885], [1440, 900], [1520, 892], [1580, 860], [1600, 800]];
const RING2 = [[1300, 735], [1290, 790], [1300, 860], [1335, 930], [1405, 975], [1490, 995], [1565, 955], [1600, 800]];
const FORGE = [[1510, 775], [1525, 850], [1532, 930], [1522, 1010], [1502, 1090], [1484, 1180], [1474, 1290], [1470, 1400]];
// =====================================================================================================================
// FRAME 0 = hook-a's last frame (16 Feb 1862, after the surrender)
// =====================================================================================================================
const DS = document.getElementById("date"), d16 = document.createElement("div"); d16.className = "d"; d16.textContent = "16 FEBRUARY 1862"; d16.style.fontSize = "32px"; DS.appendChild(d16);
const FT = fortIcon(...FD, null, null, { s: 44 }); gsap.set(FT, { autoAlpha: 1 });
const GR = [unitS("g1", "rome", [1320, 810], "infantry", ""), unitS("g2", "rome", [1440, 845], "infantry", ""), unitS("g3", "rome", [1545, 815], "infantry", ""),
  unitS("g4", "rome", [1482, 726], "artillery", "", { w: 44, h: 29 })];
const GREY = "#77746c";
GR.forEach((id) => { const el = B.units[id].el, blk = el.querySelector(".blk"), c0 = getComputedStyle(blk).backgroundColor || "#c4121f";
  gsap.set(el, { autoAlpha: 0.6 }); gsap.set(blk, { backgroundColor: GREY });
  tl.to(blk, { backgroundColor: c0, duration: 0.8 }, 1.1); tl.to(el, { autoAlpha: 1, duration: 0.8 }, 1.1); });
const UB = [unitS("uSm", "carth", [1270, 760], "infantry", "", { size: "XX" }), unitS("uWa", "carth", [1300, 870], "infantry", "", { size: "XX" }), unitS("uMc", "carth", [1450, 925], "infantry", "", { size: "XX" })];
UB.forEach((id) => gsap.set(B.units[id].el, { autoAlpha: 1 }));
const WF = pinS(GG.pin(`<svg width="40" height="54" viewBox="0 0 40 54" style="display:block;overflow:visible;filter:drop-shadow(0 2px 3px rgba(0,0,0,.8))"><path d="M6 54 L6 2" stroke="#2a2420" stroke-width="3.5"/><path d="M7 3 C18 0 26 8 38 4 L38 24 C26 28 18 20 7 23 Z" fill="#fbfaf5" stroke="#2a2420" stroke-width="1.6"/></svg>`, FD[0] + 8, FD[1] - 48, {}));
gsap.set(WF, { autoAlpha: 1 });
const F3 = [flagS(FL.us, "", 1190, 905, null, null), flagS(FL.csa, "", 1760, 600, null, null)]; gsap.set(F3, { autoAlpha: 1 });
// =====================================================================================================================
// hook-3: "But a week is not how it looked..." -- the clock rolls back to dawn, 15 February
// =====================================================================================================================
SFX("ref:whoosh", 0.25);
tl.to(WF, { autoAlpha: 0, scale: 0.4, duration: 0.4 }, 0.5);
// the date scroll rolls back with ticks (16 -> 15 FEB on "the fifteenth of February"), DAWN on "At dawn"
tl.to(d16, { autoAlpha: 0, y: -14, duration: 0.3 }, T_15 - 0.35);
for (let k = 0; k < 3; k++) SFX("tick", T_15 - 0.6 + k * 0.13);
dateSet("15 FEBRUARY 1862", T_15 - 0.05, T_DAWN - 0.05);
dateSet("15 FEB 1862 · DAWN", T_DAWN, T_FEW - 0.05, 26);
// the units step back to their dawn places (rewind), McClernand's division splits into its three brigades on the right
go("uSm", 0.6, 1.6, [1250, 772]); go("uWa", 0.6, 1.6, [1268, 880]);
const MC = [unitS("m1", "carth", [1340, 935], "infantry", "", { t: 2.0, size: "X" }), unitS("m2", "carth", [1420, 950], "infantry", "", { t: 2.1, size: "X" }),
  unitS("m3", "carth", [1505, 940], "infantry", "", { t: 2.2, size: "X" })];
go("uMc", 0.6, 1.4, [1420, 950]); B.hideUnits(["uMc"], 1.9, 0.3);
// the camera: hold, then push in on the Union right at dawn; the two glowing front lines (option 2)
const CC = [1440, 905], SC = 2.7;
camTo(0, T_15 - 0.2, [1432, 815], 1.98, "sine.inOut");
camTo(T_15 - 0.2, T_BURST - T_15 + 0.2, CC, SC, "sine.inOut");
GG.dawn(T_DAWN - 0.2, T_CMDR + 1.0);
const LG2 = legend(T_DAWN + 1.4, null, true);                 // two glowing lines (option 2), after the camera has arrived
const RF = front2(RING, SC, T_DAWN, { dur: 1.2, to: RING2, moveT: T_BURST + 0.2, moveDur: 2.6 });
// flags for the close-up (option 2: each on its side of the front)
tl.to(F3, { autoAlpha: 0, duration: 0.4 }, T_DAWN + 0.4);
const F4 = [flagS(FL.us, "", 1255, 1010, T_DAWN + 0.3, T_CMDR - 0.2), flagS(FL.csa, "", 1455, 815, T_DAWN + 0.3, T_CMDR - 0.2)];
// the Confederate columns (Pillow's attack on the Union right; Forrest's horse on the flank)
const CP = [unitS("cP1", "rome", [1420, 872], "infantry", "", { t: T_DAWN - 0.4 }), unitS("cP2", "rome", [1500, 862], "infantry", "", { t: T_DAWN - 0.3 }),
  unitS("cF", "rome", [1565, 880], "infantry", "", { t: T_DAWN - 0.2 })];
cavIcon("cF");
B.hideUnits(["g2", "g3"], T_DAWN - 0.4, 0.4);
// "burst out of the fort": red arrows break out south, the columns follow; volleys where the lines touch (visible, no artillery)
const BA = [[[1420, 875], [1400, 945], [1350, 995]], [[1500, 868], [1490, 950], [1445, 1012]], [[1565, 885], [1568, 960], [1540, 1040]]];
BA.forEach((pts, k) => arw({ pts, side: "rome", t: T_BURST - 0.15 + k * 0.18, dur: 1.2, width: AW(SC, 13), until: T_ROAD + 0.2 }));
SFX("ref:whoosh", T_BURST - 0.15);
go("cP1", T_BURST, 3.0, [1395, 965]); go("cP2", T_BURST + 0.1, 3.0, [1478, 990]); go("cF", T_BURST + 0.2, 3.0, [1560, 1005]);
[[T_BURST + 0.2, [1395, 935], [1445, 950]], [T_BURST + 1.3, [1460, 945], [1515, 945]], [T_BROKE + 0.5, [1360, 965], [1405, 985]], [T_ROAD + 0.2, [1440, 1000], [1490, 1010]]]
  .forEach(([t, a, b]) => { volley(a, b, t, 6, 0.9); smokeLine(a, b, t + 0.05, 4, 24); });
// "broken the Union right": the three brigades fall back west, BROKEN
go("m3", T_BROKE - 0.3, 2.2, [1330, 1015]); go("m2", T_BROKE - 0.2, 2.2, [1300, 985]); go("m1", T_BROKE - 0.1, 2.2, [1272, 945]);
const BRK = sstamp("BROKEN", 800, T_BROKE + 0.15, { size: 84, sub: "THE UNION RIGHT", until: T_ROAD - 0.15, shake: 5 });
pulse(T_BROKE + 0.35);
// "the road out stood open": the Forge road glows south toward Nashville, a red arrow runs down it
const ROADG = glowPath(FORGE, "#ffd54a", 7 / SC, T_ROAD - 0.05, T_CMDR + 2.5, 2, 0.95, { draw: 0.9, top: false });
boxL("THE ROAD OUT", 1600, 1030, T_ROAD, null, { size: 15 });
arw({ pts: FORGE.slice(2), side: "rome", t: T_OPEN, dur: 1.0, width: AW(SC, 10), dash: "10 8", until: T_CMDR + 1.0 });
SFX("ref:pop", T_OPEN + 0.05);
// =====================================================================================================================
// "The Union commander was not even there": the "?" badge, the empty headquarters
// =====================================================================================================================
const CH = [1300, 800], SH = 2.15;
camTo(T_CMDR - 0.5, 1.4, CH, SH, "sine.inOut");
const QB = qBadge("THE UNION COMMANDER", "", T_CMDR + 0.05, T_NAME - 1.0, { corner: "bl" });
const F5 = [flagS(FL.us, "", 1110, 820, T_CMDR - 0.3, T_RODE + 0.2), flagS(FL.csa, "", 1455, 815, T_CMDR - 0.3, T_RODE + 0.2)];
const HQU = unitS("hq", "carth", HQ, "hq", "", { t: T_CMDR + 0.2 });
tl.to(B.units.hq.el, { autoAlpha: 0.35, duration: 0.5 }, T_NOT);
K.target(...HQ, T_NOT, { r: 40, side: "carth", until: T_AWAY });
wstampL("NOT EVEN THERE", HQ[0], HQ[1] + 58, T_NOT + 0.05, null, "#e3232f", 30);
// "away on a gunboat, in a conference with the admiral": up the river to the flagship; the "?" marker sits on it
const CB = [1280, 565], SB = 2.0;
camTo(T_AWAY - 0.6, 1.5, CB, SB, "sine.inOut");
const FLG = [gunboat([[BOATP[0] - 8, BOATP[1] - 70], BOATP], T_AWAY - 0.7, 1.2, T_RODE + 2.5, { s: 17 }), gunboat([[BOATP[0] - 30, BOATP[1] - 150], [BOATP[0] - 22, BOATP[1] - 80]], T_AWAY - 0.6, 1.2, T_RODE + 2.5, { s: 15 })];
const QM = pinS(GG.pin(`<div style="width:58px;height:58px;border-radius:50%;background:radial-gradient(circle, rgba(10,12,24,0.95), rgba(10,12,24,0.8));border:4px solid #f3e7c4;box-shadow:0 0 0 3px #1f4fc4,0 6px 14px rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center;font-family:Oswald;font-weight:700;font-size:38px;color:#f7f3ea">?</div>`, BOATP[0], BOATP[1] - 46, { t: T_AWAY + 0.05, pop: true, until: T_KNOTS + 1.2 }));
SFX("ref:pop", T_AWAY + 0.1);
K.target(...BOATP, T_AWAY + 0.1, { r: 34, side: "carth", until: T_RODE });
boxL("A GUNBOAT", BOATP[0] + 125, BOATP[1] + 8, T_AWAY + 0.2, T_ADM - 0.1, { size: 14 });
boxL("THE ADMIRAL", BOATP[0] + 130, BOATP[1] + 8, T_ADM, T_RODE - 0.1, { size: 14 });
// "when he rode back": the "?" rides back along the line to the broken right (dotted trail), the camera follows
const RIDE = [[BOATP[0], BOATP[1] - 46], [LAND[0], LAND[1] - 30], [1215, 640], [HQ[0] + 10, HQ[1] - 30], [1205, 800], [1250, 880], [1290, 915]];
pinAlong(QM, RIDE, T_RODE, T_KNOTS - T_RODE + 0.1, 24);
trail(RIDE.map(([x, y]) => [x, y + 46]), "#9fc0ea", 2.4 / SB, T_RODE, T_KNOTS - T_RODE + 0.1, T_TONS + 0.5, "3 7");
SFX("ref:whoosh", T_RODE);
const CK = [1305, 930], SK = 2.55;
camTo(T_RODE + 0.2, T_KNOTS - T_RODE, CK, SK, "sine.inOut");
const F6 = [flagS(FL.us, "", 1150, 1010, T_RODE + 0.4, T_NAME - 1.0), flagS(FL.csa, "", 1430, 860, T_RODE + 0.4, T_NAME - 1.0)];
// "standing in knots, holding muskets": knots of blue men round the broken brigades
const KN = [[1262, 935], [1296, 975], [1330, 1005], [1235, 985], [1365, 960]];
KN.forEach(([x, y], k) => { const dots = [...Array(7)].map((_, i) => { const a = i / 7 * 6.2832 + k, r = i ? 9 : 0; return `<circle cx="${(15 + Math.cos(a) * r).toFixed(1)}" cy="${(15 + Math.sin(a) * r).toFixed(1)}" r="3.4" fill="#2e5cb2" stroke="#f3eee2" stroke-width="1.1"/>`; }).join("");
  const el = pinS(GG.pin(`<svg width="46" height="46" viewBox="0 0 30 30" style="display:block;overflow:visible;filter:drop-shadow(0 1px 2px rgba(0,0,0,.8))">${dots}${[0, 1, 2].map((i) => `<line x1="${8 + i * 7}" y1="${6 + (i % 2) * 3}" x2="${12 + i * 7}" y2="${-4 + (i % 2) * 3}" stroke="#3a2a1a" stroke-width="1.4"/>`).join("")}</svg>`, x, y, { t: T_KNOTS + k * 0.12, pop: true, until: T_NAME - 1.0 }));
  tl.to(el.firstElementChild, { y: -2, duration: 0.3, yoyo: true, repeat: 3 }, T_MUSK + k * 0.06); });
SFX("ref:pop", T_KNOTS + 0.1);
tl.to(["m1", "m2", "m3"].map((id) => B.units[id].el), { autoAlpha: 0.45, duration: 0.5 }, T_KNOTS);
const NOAM = sstamp("NO AMMUNITION", 800, T_NOAMMO - 0.05, { size: 76, until: T_TONS - 0.15, shake: 5 });
pulse(T_NOAMMO + 0.2);
// "while tons of it lay close at hand": ammunition crates glow just behind the line
const CRATE = `<svg width="34" height="26" viewBox="0 0 34 26" style="display:block;overflow:visible;filter:drop-shadow(0 0 5px #ffd54a) drop-shadow(0 2px 2px rgba(0,0,0,.8))"><rect x="1" y="4" width="32" height="20" fill="#8a6a44" stroke="#2a2420" stroke-width="2"/><path d="M1 4 L33 24 M33 4 L1 24" stroke="#5a4428" stroke-width="1.6"/><rect x="1" y="1" width="32" height="5" fill="#a07c50" stroke="#2a2420" stroke-width="1.5"/></svg>`;
const CR = [[1190, 925], [1212, 950], [1182, 952], [1205, 975]];
CR.forEach(([x, y], k) => pinS(GG.pin(CRATE, x, y, { t: T_TONS + k * 0.1, pop: true, until: T_NAME - 1.0 })));
SFX("ref:pop", T_TONS + 0.05);
const TONS = sstamp("TONS OF IT", 800, T_TONS + 0.05, { size: 76, color: "#ffd54a", sub: "CLOSE AT HAND", until: S4 - 0.3, shake: 4 });
arw({ pts: [[1215, 945], [1245, 950], [1270, 955]], side: "carth", t: T_HAND, dur: 0.6, width: AW(SK, 7), dash: "6 6", until: T_NAME - 1.0 });
// =====================================================================================================================
// hook-4: the name slam (the "?" turns into the real photo)
// =====================================================================================================================
const DK = scr0("", "inset:0;background:rgba(5,7,13,0.62);"); tl.fromTo(DK, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.5, immediateRender: false }, S4 - 0.2);
const BDG = scr0(`<div style="position:relative;width:300px;height:300px;border-radius:50%;overflow:hidden;border:9px solid #f3e7c4;box-shadow:0 0 0 7px #1f4fc4,0 24px 48px rgba(0,0,0,0.75);background:url(${FL.us}) center/cover">
  <img src="${PHOTO("grant")}" style="position:absolute;left:0;right:0;bottom:0;margin:auto;height:112%;filter:grayscale(1) contrast(1.1)">
  <div class="q" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle, rgba(10,12,24,1), rgba(10,12,24,0.94));font-family:Oswald;font-weight:700;font-size:180px;color:#f7f3ea">?</div></div>`,
  "left:810px;top:150px;transform-origin:50% 50%;");
tl.fromTo(BDG, { autoAlpha: 0, scale: 0.4, x: -620, y: 520 }, { autoAlpha: 1, scale: 1, x: 0, y: 0, duration: 0.55, ease: "power3.out", immediateRender: false }, S4 - 0.1);
SFX("ref:whoosh", T_NAME - 0.5);
tl.to(BDG.querySelector(".q"), { autoAlpha: 0, duration: 0.15 }, T_NAME - 0.2);
const NAME = scr(`<div style="padding:12px 44px 14px;background:rgba(18,16,12,0.95);border-top:7px solid #1f4fc4;color:#f7f3ea;font-family:Oswald;font-weight:700;text-align:center;box-shadow:0 14px 30px rgba(0,0,0,.6)"><div style="font-size:90px;letter-spacing:0.08em;line-height:1.1">ULYSSES S. GRANT</div><div style="font-size:24px;letter-spacing:0.26em;color:#d8cfb8">THE UNION COMMANDER</div></div>`,
  "left:0;right:0;top:500px;display:flex;justify-content:center;transform-origin:50% 40%;", T_NAME - 0.1, null, { autoAlpha: 0 });
slam(NAME, T_NAME - 0.1, { from: 1.9, shake: 6, until: T_FEW - 0.1 }); pulse(T_NAME + 0.15);
// "a few weeks earlier his own superior had brushed off his plan": the plan sketch + BRUSHED OFF (the superior is not named: no badge)
tl.to(BDG, { x: -560, y: 60, scale: 0.72, duration: 0.5, ease: "power3.inOut" }, T_FEW - 0.1);
dateSet("JANUARY 1862", T_FEW, T_TWO - 0.1);
const PLAN = scr(`<div style="position:relative;width:640px;height:400px;background:#ece3cc;border:2px solid #b9a77f;box-shadow:0 22px 46px rgba(0,0,0,.7);transform:rotate(-2deg);font-family:'Special Elite',monospace;color:#2a2420">
  <svg width="640" height="400" viewBox="0 0 640 400" style="position:absolute;left:0;top:0">
    <path d="M40 70 C160 60 260 80 360 70 C470 60 560 75 610 60" fill="none" stroke="#6f8fb5" stroke-width="7"/>
    <path d="M250 75 C245 150 230 220 238 300 C242 340 236 370 230 395" fill="none" stroke="#6f8fb5" stroke-width="6"/>
    <path d="M420 68 C430 140 470 190 520 240 C560 280 590 330 600 395" fill="none" stroke="#6f8fb5" stroke-width="6"/>
    <path class="a1" d="M250 90 C246 150 236 210 238 280" fill="none" stroke="#1f4fc4" stroke-width="5" stroke-dasharray="10 7"/><path d="M226 270 L238 300 L252 270 Z" fill="#1f4fc4"/>
    <path class="a2" d="M425 85 C440 150 480 195 520 235" fill="none" stroke="#1f4fc4" stroke-width="5" stroke-dasharray="10 7"/><path d="M503 236 L528 248 L522 220 Z" fill="#1f4fc4"/>
    <g fill="#c4121f" stroke="#2a2420" stroke-width="1.5"><path d="M238 205 l7 14 15 1 -11 10 4 15 -15 -8 -15 8 4 -15 -11 -10 15 -1 Z"/><path d="M462 182 l7 14 15 1 -11 10 4 15 -15 -8 -15 8 4 -15 -11 -10 15 -1 Z"/></g>
  </svg>
  <div class="tt" style="position:absolute;left:24px;top:330px;font-size:44px;letter-spacing:.06em">HIS PLAN</div></div>`,
  "left:700px;top:360px;", T_BRUSH - 0.25, T_TWO - 0.12, { autoAlpha: 0, x: 120 });
gsap.set(PLAN.querySelector(".tt"), { autoAlpha: 0 }); tl.to(PLAN.querySelector(".tt"), { autoAlpha: 1, duration: 0.2 }, T_PLAN - 0.05);
SFX("ref:pop", T_BRUSH - 0.2);
const BOFF = scr(stampHTML("BRUSHED OFF", "#e3232f", 70, -9), "left:870px;top:520px;transform-origin:50% 50%;", T_BRUSH, null, { autoAlpha: 0 });
slam(BOFF, T_BRUSH, { from: 2.2, shake: 5, until: T_TWO - 0.12 }); pulse(T_BRUSH + 0.2);
// "his own superior": an unnamed officer (no name is spoken, so no photo and no name plate)
const SUP = scr(`<div style="display:flex;align-items:center;gap:18px;flex-direction:row-reverse"><div style="position:relative;width:170px;height:170px;border-radius:50%;overflow:hidden;border:6px solid #f3e7c4;box-shadow:0 0 0 4px #1f4fc4,0 12px 26px rgba(0,0,0,0.6);background:radial-gradient(circle at 50% 40%, #3a4458, #10141c)">
  <svg width="170" height="170" viewBox="0 0 100 100" style="position:absolute;left:0;top:0"><circle cx="50" cy="40" r="17" fill="#0a0d13"/><path d="M14 100 C16 72 32 62 50 62 C68 62 84 72 86 100 Z" fill="#0a0d13"/><path d="M30 70 L36 64 M70 70 L64 64" stroke="#c9b48a" stroke-width="3"/></svg></div>
  <div style="padding:10px 20px 12px;background:rgba(18,16,12,0.9);border-right:6px solid #1f4fc4;color:#f7f3ea;font-weight:700;font-family:Oswald"><div style="font-size:34px;letter-spacing:0.06em;white-space:nowrap">HIS OWN SUPERIOR</div></div></div>`,
  "right:90px;top:330px;", T_SUP - 0.05, T_BRUSH - 0.3, { autoAlpha: 0, x: 80 });
SFX("ref:pop", T_SUP);
// =====================================================================================================================
// the three snap cuts (whoosh + hit; a black frame hides each camera jump)
// =====================================================================================================================
const CUTB = scr0("", "inset:0;background:#030406;");
const cut = (t, lay, until, c, s, drift) => {
  tl.fromTo(CUTB, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.05, immediateRender: false }, t - 0.06); tl.to(CUTB, { autoAlpha: 0, duration: 0.16 }, t + 0.04);
  if (lay) { tl.set(lay, { autoAlpha: 1 }, t - 0.01); tl.set(lay, { autoAlpha: 0 }, until - 0.01); }
  camTo(t, 0.01, c, s); camTo(t + 0.02, until - t - 0.05, [c[0] + drift[0], c[1] + drift[1]], s * (drift[2] || 1.06), "sine.out");
  SFX("ref:whoosh", t - 0.2); SFX("hit", t + 0.02); K.shake(t + 0.02, 3, 0.25); };
const T1 = T_TWO - 0.08, T2 = T_CITY - 0.08, T3 = T_MARCH - 0.08, T4 = T_THESE - 0.1;
tl.set([DK, BDG, PLAN, BOFF, SUP, TG, RELIEF], { autoAlpha: 0 }, T1 - 0.01);
// everything of the Donelson story leaves at the first cut
const S0 = snap(); tl.set([...S0].filter((e) => e.tagName.toLowerCase() !== "defs"), { autoAlpha: 0 }, T1 - 0.01);
tl.set(Object.values(B.units).map((u) => u.el), { autoAlpha: 0 }, T1 - 0.01);
const PB = badge({ name: "ULYSSES S. GRANT", role: "", photo: PHOTO("grant"), flag: FL.us, side: "carth", corner: "bl", initials: "USG", t: T1 + 0.15, until: T4 - 0.1 });
const ringN = (p, txt, n, t, until, dx, dy) => { K.target(p[0], p[1], t, { r: 34 / CAM_S0, until });
  const el = GG.pin(`<div style="display:flex;align-items:center;gap:8px;font-family:Oswald;font-weight:700;color:#ffd54a;text-shadow:0 2px 4px #000,0 0 3px #000"><span style="display:inline-flex;width:38px;height:38px;border-radius:50%;border:3px solid #ffd54a;align-items:center;justify-content:center;font-size:21px">${n}</span><span style="font-size:36px;letter-spacing:.1em;white-space:nowrap">${txt}</span></div>`, p[0] + dx, p[1] + dy, { t: t + 0.1, pop: true, until });
  pinS(el); SFX("ref:pop", t + 0.12); return el; };
let CAM_S0 = 1;
// ---------- CUT 1: TWO RIVERS (henry map, Feb 1862, option 2, no tint): gunboats up both rivers, both forts blue ----------
const FHh = HP(36.515, -88.035), FDh = HP(36.4935, -87.861), S1c = 1.2, C1 = [(FHh[0] + FDh[0]) / 2 + 20, FDh[1] - 10];
cut(T1, LHE, T2, C1, S1c, [6, -4, 1.07]); CAM_S0 = S1c;
dateSet("FEBRUARY 1862", T1, T2 - 0.05);
const SC1 = snap();
[flagS(FL.us, "", (FHh[0] + FDh[0]) / 2, (FHh[1] + FDh[1]) / 2 + 8, T1, T2), flagS(FL.csa, "", FDh[0] + 330, FDh[1] + 210, T1, T2)].forEach(vis(T1, T2));
[[FHh, [FHh[0] - 12, FHh[1] - 330]], [FDh, [FDh[0] - 60, FDh[1] - 320]]].forEach(([p, a], k) => {
  [0, 1].forEach((j) => { const el = gunboat([[a[0] + j * 6, a[1] - 60 - j * 40], [p[0] - 6 + j * 4, p[1] - 30 - j * 26]], T1 + j * 0.15, 1.3, T2 - 0.01, { s: 15 }); vis(T1, T2)(el); });
  arw({ pts: [[a[0], a[1] - 40], [(a[0] + p[0]) / 2, (a[1] + p[1]) / 2], [p[0], p[1] - 20]], side: "carth", t: T1 + 0.05, dur: 0.7, width: AW(S1c, 12), until: T2 - 0.01 });
  vis(T1, T2)(fortIcon(p[0], p[1], null, null, { s: 40, side: "carth" })); });
ringN([C1[0] - 20, C1[1] + 60], "TWO RIVERS", 1, T_TWO + 0.35, T2 - 0.01, 0, 0);
endScope(SC1, T2);
// ---------- CUT 2: THE MISSISSIPPI (vicksburg_siege, night, option 2): the gunboats run past the bluff batteries ----------
const VKS = VP(32.3526, -90.8779), S2c = 1.5;
const RUN = [VP(32.41, -90.935), VP(32.385, -90.905), VP(32.365, -90.888), VP(32.345, -90.886), VP(32.322, -90.895), VP(32.30, -90.912)];
const C2 = [VKS[0] - 40, VKS[1] + 20];
cut(T2, LVK, T3, C2, S2c, [-8, 10, 1.06]); CAM_S0 = S2c;
dateSet("APRIL 1863", T2, T3 - 0.05);
const SC2 = snap();
const NW = scr0("", "inset:0;background:rgba(6,10,30,0.52);"); vis(T2, T3)(NW);
[flagS(FL.us, "", RUN[2][0] - 260, RUN[2][1] + 60, T2, T3), flagS(FL.csa, "", VKS[0] + 230, VKS[1] - 40, T2, T3)].forEach(vis(T2, T3));
front2(RUN.map(([x, y]) => [x + 40, y]), S2c, T2, { dur: 0.01, until: T3 - 0.01 });
town("VICKSBURG", VKS, "r", T2, { until: T3 - 0.01 });
[0, 1, 2].forEach((k) => { const el = gunboat(sub(RUN, 0.12 + k * 0.08, 0.62 + k * 0.08), T2 + k * 0.25, T3 - T2 - 0.3, T3 - 0.01, { s: 21 }); vis(T2, T3)(el); });
const BAT = [[VKS[0] + 70, VKS[1] - 50], [VKS[0] + 80, VKS[1] + 60]];
BAT.forEach((p, k) => vis(T2, T3)(pinS(GG.pin(`<div style="width:50px;height:33px;background:#c4121f;border:2px solid #f3eee2;display:flex;align-items:center;justify-content:center"><svg width="40" height="25" viewBox="2 18 96 78"><g fill="#f3eee2"><rect x="30" y="44" width="58" height="11" rx="3" transform="rotate(-24 36 52)"/><circle cx="38" cy="64" r="15" fill="none" stroke="#f3eee2" stroke-width="7"/></g></svg></div>`, p[0], p[1], {}))));
shoot(BAT[0], posOn(RUN, 0.38), T2 + 0.5, { r: 10 / S2c, h: 30, width: 1.6 / S2c, dur: 0.6 });
shoot(BAT[1], posOn(RUN, 0.55), T_MISS + 0.1, { r: 10 / S2c, h: 30, width: 1.6 / S2c, dur: 0.6 });
fireGlow(RUN[2][0] + 70, RUN[2][1] - 20, 40, T2 + 0.2, T3 - 0.01);
ringN([VKS[0] - 60, VKS[1] + 120], "THE MISSISSIPPI", 2, T_MISS, T3 - 0.01, 0, 0);
endScope(SC2, T3);
// ---------- CUT 3: ACROSS A RIVER (jamesriver, June 1864, option 2): the pontoon bridge, Lee's army facing the other way ----------
// the bridge: Weyanoke Point (the tip of the north-bank peninsula) -> Windmill Point (south bank), traced on the jamesriver relief (map px)
const WEY = [1403, 874], WIN = [1412, 905], S3c = 1.2, S3b = 2.4;
const LEEP = JP(37.41, -77.25), C3 = [LEEP[0] + 280, LEEP[1] + 190], C3b = [1415, 865];
// close on the bridge first ("marched a whole army across a river"), then pull back to show Lee ("while Robert E. Lee...")
tl.fromTo(CUTB, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.05, immediateRender: false }, T3 - 0.06); tl.to(CUTB, { autoAlpha: 0, duration: 0.16 }, T3 + 0.04);
tl.set(LJA, { autoAlpha: 1 }, T3 - 0.01);
camTo(T3, 0.01, C3b, S3b); camTo(T3 + 0.02, T_LEE - 0.7 - T3, [C3b[0], C3b[1] + 15], S3b * 1.06, "sine.out");
camTo(T_LEE - 0.6, 1.3, C3, S3c, "power2.inOut"); camTo(T_LEE + 0.75, T4 - T_LEE, [C3[0] - 10, C3[1] - 8], S3c * 1.03, "sine.out");
SFX("ref:whoosh", T3 - 0.2); SFX("hit", T3 + 0.02); K.shake(T3 + 0.02, 3, 0.25); CAM_S0 = S3b;
dateSet("JUNE 1864", T3, null);
const SC3 = snap();
[flagS(FL.us35, "", WEY[0] + 140, WEY[1] - 95, T3, null), flagS(FL.csa, "", WIN[0] - 60, WIN[1] + 95, T3, T_LEE - 0.4)].forEach(vis(T3, null));   // the south bank was still Confederate country
flagS(FL.csa, "", LEEP[0] - 40, LEEP[1] + 270, T_LEE - 0.6, null);
glowPath([WEY, WIN], "#e3cf9a", 5 / S3b, T3, null, 0, 1.0, { top: true }); glowPath([WEY, WIN], "#5a4428", 1.6 / S3b, T3, null, 0, 1.0, { top: true, dash: "2 2.5" });
const XR = [[1470, 700], [1440, 780], [1412, 840], WEY, WIN, [1416, 960], [1402, 1040]];
[0, 1, 2].forEach((k) => { const id = unitS("j" + k, "carth", XR[0], "infantry", "", { t: T3 + k * 0.3, flag: FL.us35 }); along(id, XR, T3 + k * 0.45, 4.2, 24); });
arw({ pts: XR, side: "carth", t: T3 + 0.2, dur: 1.4, width: AW(S3b, 12), until: T_LEE - 0.5 });
arw({ pts: XR, side: "carth", t: T_LEE - 0.4, dur: 0.01, width: AW(S3c, 11), until: null });
ringN(WIN, "ACROSS A RIVER", 3, T_ACROSS, null, 150, 40);
// Lee (badge on his name) and his army, facing the other way (north, toward Richmond)
const LR = [unitS("l0", "rome", LEEP, "infantry", "", { t: T3 + 0.1, flag: FL.csa, until: T4 }), unitS("l1", "rome", [LEEP[0] + 120, LEEP[1] - 30], "infantry", "", { t: T3 + 0.2, flag: FL.csa, until: T4 })];
const LB = badge({ name: "ROBERT E. LEE", role: "", photo: PHOTO("lee"), flag: FL.csa, side: "rome", corner: "tr", initials: "REL", t: T_LEE - 0.05, until: T4 - 0.1 });
[[LEEP, [LEEP[0] - 40, LEEP[1] - 200]], [[LEEP[0] + 120, LEEP[1] - 30], [LEEP[0] + 110, LEEP[1] - 230]]].forEach(([a, b], k) => arw({ pts: [a, b], side: "rome", t: T_OTHER + k * 0.15, dur: 0.7, width: AW(S3c, 11), dash: "10 8", until: T4 }));
wstampL("LOOKING THE OTHER WAY", LEEP[0] + 150, LEEP[1] + 80, T_OTHER + 0.1, T4 - 0.1, "#e3232f", 30);
// =====================================================================================================================
// the title (riser + boom): the James River shot dims, the three moves in one line
// =====================================================================================================================
SFX("ref:riser", T4 + 0.1);
const TDIM = scr("", "inset:0;background:radial-gradient(ellipse at center, rgba(5,7,13,0.45), rgba(5,7,13,0.82));", T4, null, { autoAlpha: 0 });
const TITLE = scr(`<div style="text-align:center;font-family:Oswald;font-weight:700;padding:16px 64px 22px;background:rgba(14,12,10,0.9);border-top:7px solid #c9b48a;box-shadow:0 24px 50px rgba(0,0,0,.6)">
  <div style="font-size:30px;letter-spacing:0.42em;color:#c9b48a">ULYSSES S. GRANT'S</div>
  <div style="font-size:84px;letter-spacing:0.06em;line-height:1.08;color:#f7f3ea">3 GREATEST TACTICAL MOVES</div>
  <div style="font-size:28px;letter-spacing:0.3em;color:#ffd54a;margin-top:8px">1 TWO RIVERS · 2 THE MISSISSIPPI · 3 ACROSS A RIVER</div></div>`, "left:0;right:0;top:300px;display:flex;justify-content:center;", T_GREAT - 0.26, null, { autoAlpha: 0 });
tl.fromTo(TITLE, { autoAlpha: 0, scale: 1.7 }, { autoAlpha: 1, scale: 1, duration: 0.26, ease: "power4.in", immediateRender: false }, T_GREAT - 0.26);
SFX("ref:boom", T_GREAT); K.shake(T_GREAT, 6, 0.4);
// the HUD steps out while a big card is up (1c); the date scroll stays
declutter([LG2, QB, PB, LB], [[T_BROKE + 0.15, T_ROAD - 0.15], [T_NOAMMO - 0.05, T_TONS - 0.15], [T_TONS + 0.05, S4 - 0.3], [S4 - 0.2, T1], [T4, END + 1]]);
tl.set(LG2, { autoAlpha: 0 }, T1 - 0.01);
K.raiseTerritory();
B.finish();
