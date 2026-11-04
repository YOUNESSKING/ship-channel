// m1b (m1-2), Grant #16: 12 Feb 1862, Grant marches ~15,000 men overland from Fort Henry to Fort Donelson (about a dozen miles) before
// the Confederates can reinforce it; Floyd, Pillow and Buckner inside; "15,000 on the 8th > 50,000 a month later".
// Basemap donelson_hd_lift (z13, v11): Fort Henry at the left edge, Fort Donelson + Dover on the Cumberland. Option 2 (owner
// 2026-11-02: territory minimised; a battle map -> no ground tint): the two-colour front comes in where the columns reach the works.
// Built with: python3 tools/m1_build.py m1b donelson_hd_lift m1-2 m1-2
// @@BODY
const P2 = "m1-2";
const T_WANT = at(P2, "Grant wanted to hit"), T_REINF = at(P2, "could reinforce it"), T_12 = at(P2, "On the twelfth"), T_15K = at(P2, "fifteen thousand men marched"),
  T_ACROSS = at(P2, "marched across country"), T_TODON = at(P2, "to Fort Donelson"), T_INSIDE = at(P2, "Inside were Confederate generals"),
  T_FLOYD = at(P2, "Floyd, Pillow"), T_PILLOW = at(P2, "Pillow and Buckner"), T_BUCK = at(P2, "Buckner. Grant"), T_KNEW = at(P2, "Grant knew Pillow"),
  T_MEX = at(P2, "the Mexican War"), T_SMALL = at(P2, "however small"), T_GUNSHOT = at(P2, "within gunshot"), T_HOLD = at(P2, "given to hold"),
  T_EIGHTH = at(P2, "thousand men on the eighth"), T_50K = at(P2, "fifty thousand"), T_MONTH = at(P2, "a month later");
// ---------- places (donelson map px, tools/m1_proj.py) ----------
const FH = [392, 557], DON = [1400, 713], DOV = [1508, 756];
const WORKS = [[1540, 811], [1487, 832], [1429, 825], [1371, 796], [1312, 753], [1289, 702], [1307, 651], [1324, 630]];
const ULINE = [[1557, 854], [1487, 876], [1406, 869], [1330, 832], [1266, 775], [1243, 709], [1254, 644], [1289, 601]];
const ROAD_N = [[430, 540], [640, 512], [860, 540], [1040, 590], [1170, 630], [1250, 660]];      // Telegraph road (north)
const ROAD_S = [[430, 580], [640, 650], [880, 710], [1080, 770], [1230, 800], [1330, 845]];      // Ridge / Dover road (south)
const CUMB = [[1120, 0], [1180, 200], [1240, 340], [1320, 500], [1400, 620], [1480, 690], [1600, 680], [1720, 640], [1840, 624], [1980, 700], [2100, 820], [2200, 940], [2320, 1100], [2460, 1240], [2600, 1360], [2800, 1380]];
// ---------- map ----------
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.14 }); LV.shimmer([CUMB], { width: 1.4 }); LV.scaleBar(15.37); LV.north();
const LGD = now(legend(0, END + 1, true));
camera([[0, 900, 690, 0.9], [T_12, 880, 680, 0.95], [T_TODON + 0.5, 1080, 700, 1.15], [T_INSIDE + 0.3, 1390, 735, 2.0], [T_KNEW, 1395, 740, 2.2],
  [T_GUNSHOT, 1370, 740, 1.9], [T_EIGHTH, 1250, 720, 1.4], [END, 1220, 720, 1.35]]);
dateNow("6 FEBRUARY 1862", T_12 - 0.1); B.date("12 FEBRUARY 1862", T_12, null, 34);
// ---------- flags (both on every frame) ----------
flagS(FL.us, 520, 380, 0, T_INSIDE + 0.6); flagS(FL.cs, 1760, 980, 0, T_INSIDE + 0.6);
flagS(FL.us, 1180, 600, T_INSIDE + 0.4, END + 1, 90); flagS(FL.cs, 1560, 640, T_INSIDE + 0.5, END + 1, 90);
// ---------- the forts ----------
fortIcon(FH, 0, null, { s: 22, col: "#4f8bff" }); poleFlag(FL.us, [FH[0] + 4, FH[1] - 8], 0, null, 34);
fortIcon(DON, 0, null, { s: 26 }); poleFlag(FL.cs, [DON[0] + 4, DON[1] - 8], 0, null, 38);
boxS("FORT DONELSON", DON[0] - 20, DON[1] - 60, T_WANT + 0.8, null, { size: 26 });
K.target(DON[0], DON[1], T_WANT + 0.6, { r: 44, side: "#9fc0ea", until: T_INSIDE });
// Confederate reinforcements on their way in (from up the Cumberland, the Nashville side)
unitS("rf", "rome", [2150, 900], "infantry", null, { t: 0 });
along("rf", [[2150, 900], [1980, 790], [1800, 760], [1620, 770], [1520, 790]], 0.1, T_INSIDE - 0.3, 16); hideU(["rf"], T_INSIDE);
arw({ pts: [[2200, 960], [2040, 830], [1840, 790], [1640, 790]], side: "rome", t: T_REINF - 0.6, dur: 1.6, width: AW(1.0, 12), dash: "12 8", until: T_15K });
B.caption("HIT THE NEXT FORT BEFORE IT IS REINFORCED", T_WANT + 0.2, T_12 - 0.2, "carth");
// ---------- the march (two columns, about a dozen miles) ----------
unitS("mc", "carth", [ROAD_S[0][0] + 20, ROAD_S[0][1] + 20], "infantry", null, { t: 0, size: "XX" });
unitS("sm", "carth", [ROAD_N[0][0] + 10, ROAD_N[0][1] - 26], "infantry", null, { t: 0, size: "XX" });
tl.to(B.units.mc.el, { y: -4, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut" }, 0.2);   // idling at Fort Henry
along("mc", [[ROAD_S[0][0] + 20, ROAD_S[0][1] + 20], ...ROAD_S.slice(1), [1360, 880]], T_15K, T_INSIDE + 1.8 - T_15K, 24);
along("sm", [[ROAD_N[0][0] + 10, ROAD_N[0][1] - 26], ...ROAD_N.slice(1), [1262, 620]], T_15K + 0.3, T_INSIDE + 2.2 - T_15K, 24);
arw({ pts: ROAD_S, side: "carth", t: T_15K, dur: 3.0, width: AW(1.0, 11), until: T_INSIDE + 0.8 });
arw({ pts: ROAD_N, side: "carth", t: T_15K + 0.3, dur: 3.0, width: AW(1.0, 11), until: T_INSIDE + 0.8 });
const TK = ticker("GRANT'S ARMY", 15000, "", "right:70px;top:240px;", T_15K - 0.1, 1.2, T_INSIDE - 0.2, 6, { col: "#9fc0ea", sub: "MEN · 12 FEBRUARY" });
B.caption("ACROSS COUNTRY TO FORT DONELSON", T_ACROSS, T_INSIDE - 0.2, "carth");
// ---------- inside: Floyd, Pillow, Buckner ----------
const WL = glowPath(WORKS, "#ff6a5a", 3.2, T_INSIDE, END + 1, 2, 0.85, { draw: 1.2, dash: "6 4" });
unitS("fl", "rome", [1440, 742], "infantry", "FLOYD", { t: T_FLOYD });
unitS("pi", "rome", [1462, 800], "infantry", "PILLOW", { t: T_PILLOW });
unitS("bu", "rome", [1340, 700], "infantry", "BUCKNER", { t: T_BUCK });
const CH = [chip("floyd", "FLOYD", "rome", "right:330px;top:240px;", T_FLOYD, T_EIGHTH - 0.4), chip("pillow", "PILLOW", "rome", "right:195px;top:240px;", T_PILLOW, T_EIGHTH - 0.4),
  chip("buckner", "BUCKNER", "rome", "right:60px;top:240px;", T_BUCK, T_EIGHTH - 0.4)];
tl.fromTo(CH[1].querySelector(".ring"), { scale: 1 }, { scale: 1.18, duration: 0.3, yoyo: true, repeat: 3, immediateRender: false }, T_KNEW + 0.3);
pulseU("pi", T_KNEW + 0.3);
B.caption("GRANT KNEW PILLOW FROM THE MEXICAN WAR", T_KNEW, T_SMALL - 0.1, "carth");
// "with any force, however small ... right up to within gunshot": the blue columns walk right up to the works
[[[1240, 790], [1300, 812], [1345, 815]], [[1250, 690], [1275, 700], [1296, 706]], [[1270, 630], [1296, 640], [1310, 652]]].forEach((pts, k) =>
  arw({ pts, side: "carth", t: T_GUNSHOT - 0.4 + k * 0.25, dur: 0.8, width: AW(1.9, 11), until: T_EIGHTH }));
B.caption("RIGHT UP TO WITHIN GUNSHOT", T_GUNSHOT - 0.2, T_EIGHTH - 0.3, "carth");
const UL = frontS({ pts: ULINE.map((q, i) => [(q[0] + WORKS[i][0]) / 2, (q[1] + WORKS[i][1]) / 2]), sideA: "carth", sideB: "rome", t: T_GUNSHOT + 0.6, dur: 2.0, width: FWw(1.6), until: END + 1 });
unitS("wa", "carth", [1225, 760], "infantry", null, { t: T_HOLD });
// ---------- 15,000 on the 8th > 50,000 a month later (one big card; the HUD steps out) ----------
const CMP = scr(`<div style="display:flex;align-items:center;gap:40px;padding:24px 50px 26px;background:rgba(18,16,12,0.93);border-top:6px solid #c9b48a;font-family:Oswald;font-weight:700;color:#f7f3ea;box-shadow:0 20px 40px rgba(0,0,0,.55)">
  <div style="text-align:center"><div style="font-size:78px;color:#9fc0ea">15,000</div><div style="font-size:24px;letter-spacing:.24em">ON THE 8TH</div></div>
  <div class="gt" style="font-size:90px;color:#c9b48a">&gt;</div>
  <div class="r" style="text-align:center"><div style="font-size:78px;color:#a8a294">50,000</div><div style="font-size:24px;letter-spacing:.24em">A MONTH LATER</div></div></div>`,
  "left:0;right:0;top:230px;display:flex;justify-content:center;", T_EIGHTH + 0.1, END - 0.1);
const R50 = CMP.querySelector(".r"), GT = CMP.querySelector(".gt"); gsap.set([R50, GT], { autoAlpha: 0 });
tl.to(R50, { autoAlpha: 1, duration: 0.4 }, T_50K); tl.fromTo(GT, { autoAlpha: 0, scale: 2 }, { autoAlpha: 1, scale: 1, duration: 0.25, immediateRender: false }, T_MONTH + 0.3);
SFX("hit", T_MONTH + 0.5);
declutter([LGD, ...CH, TK], [[T_EIGHTH + 0.1, END + 1]]);
fixImgs();
K.raiseTerritory();
B.finish();
