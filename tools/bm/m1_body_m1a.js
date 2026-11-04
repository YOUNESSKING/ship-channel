// m1a (m1-1), Grant #16: MOVE 1 opens. Fort Henry, 6 Feb 1862: Foote's gunboats steam up the Tennessee, the fort half under water,
// Tilghman has sent his garrison off toward Donelson and gives the fort to the navy with ~90 men; Grant's columns are still on the road.
// Basemap henry_hd_lift (z11, v11 look). Option 2 (owner 2026-11-02: territory minimised, a close-up -> no ground tint; the fort flag says who holds it).
// Built with: python3 tools/m1_build.py m1a henry_hd_lift m1-1 m1-1     (kit: tools/m1_kit.js, body: tools/m1_body_m1a.js)
// @@BODY
const P1 = "m1-1";
const T_SIXTH = at(P1, "sixth of February"), T_FEB = at(P1, "February"), T_FOOTE = at(P1, "Foote's gunboats"), T_STEAM = at(P1, "steamed up the Tennessee"),
  T_FIRE = at(P1, "opened fire on Fort Henry"), T_FHN = at(P1, "Fort Henry"), T_FLOOD = at(P1, "The river was in flood"), T_TWO = at(P1, "two feet deep in water"),
  T_CMDR = at(P1, "The Confederate commander"), T_TIL = at(P1, "Lloyd Tilghman"), T_MARCH = at(P1, "had already marched most"),
  T_SURR = at(P1, "He surrendered to the navy"), T_NINETY = at(P1, "about ninety men"), T_GRANT = at(P1, "Grant had not needed"), T_STORM = at(P1, "storm the fort");
// ---------- places (henry map px, from tools/m1_proj.py) ----------
const FH = [1324, 783], FHEI = [1298, 763], LAND = [1350, 711], DON = [1576, 822];
const TENN = [[1100, 0], [1150, 200], [1230, 400], [1268, 600], [1282, 700], [1285, 780], [1272, 960], [1350, 1100], [1420, 1300], [1420, 1620]];
const CUMB = [[1400, 0], [1440, 200], [1500, 400], [1560, 640], [1590, 790], [1700, 860], [1800, 960], [1900, 1000], [2050, 900], [2150, 820], [2250, 760], [2400, 860], [2540, 1140], [2800, 1320]];
// ---------- map: option 2 (no territory fill), living map ----------
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.14 }); LV.shimmer([TENN, CUMB], { width: 1.6 }); LV.scaleBar(61.44); LV.north();
// ---------- camera: wide (both rivers) -> push in on Fort Henry for the fight -> ease back to show the garrison leaving ----------
camera([[0, 1330, 640, 1.2], [T_STEAM, 1320, 700, 1.6], [T_FIRE, 1300, 748, 2.6], [T_FLOOD + 0.6, 1308, 768, 3.0], [T_CMDR, 1330, 772, 2.7],
  [T_MARCH + 1.6, 1420, 790, 2.1], [T_SURR + 0.6, 1360, 780, 2.5], [T_GRANT, 1350, 760, 2.3], [END, 1340, 750, 2.2]]);
// ---------- date (comes in on the spoken date) + title card ----------
B.showDate(T_SIXTH); B.date("6 FEBRUARY 1862", T_SIXTH + 0.1, null, 34);
const TT = B.title("MOVE 1", "FORT HENRY", "6 FEBRUARY", T_FHN, T_FHN + 2.6); SFX("ref:boom", T_FHN + 0.15);
const LGD = legend(T_FHN + 3.0, END + 1, true);
// ---------- flags (both on every frame; re-placed for the close-up) ----------
flagS(FL.us, 1760, 430, 0, T_STEAM + 0.8); flagS(FL.cs, 1760, 1010, 0, T_STEAM + 0.8);
flagS(FL.us, 1500, 590, T_STEAM + 0.6, END + 1, 96); flagS(FL.cs, 1480, 905, T_STEAM + 0.7, END + 1, 96);
// ---------- the fort, half under water ----------
const FLOOD = pinS(GG.pin(`<div style="width:120px;height:90px;border-radius:50%;background:radial-gradient(ellipse at center, rgba(120,170,215,.75) 0%, rgba(120,170,215,.45) 45%, rgba(120,170,215,0) 72%)"></div>`, FH[0] - 6, FH[1] + 2, { t: T_FLOOD - 0.2 }));
tl.to(FLOOD.firstElementChild, { scale: 1.12, opacity: 0.8, duration: 0.9, yoyo: true, repeat: 9, ease: "sine.inOut" }, T_FLOOD + 0.4);
fortIcon(FH, 0, null, { s: 26 });
const FHF = poleFlag(FL.cs, [FH[0] + 4, FH[1] - 8], 0.2, T_SURR + 0.5, 40);
poleFlag(FL.us, [FH[0] + 4, FH[1] - 8], T_SURR + 0.55, END + 1, 40);
boxS("FORT HENRY", FH[0] - 62, FH[1] + 34, T_FHN + 2.8, null, { size: 26 });
boxS("TENNESSEE RIVER", 1210, 600, T_STEAM + 0.2, null, { size: 22, bg: "#dcecf8", sfx: false });
// ---------- Foote's flotilla: four ironclads abreast, three timberclads behind (Memoirs: seven gunboats) ----------
const OFF = [-24, -8, 8, 24], IRON = [], WOOD = [];
OFF.forEach((dx, k) => { const path = TENN.slice(0, 5).map((q) => [q[0] + dx, q[1]]); path[4] = [1282 + dx, 700]; path.push([1284 + dx, 745]);
  const f0 = 0.38 + k * 0.03, p0 = posOn(path, f0);
  const s = ship("iron", "carth", p0, 90, null, null, { L: 58, name: k === 1 ? "FOOTE" : null, ny: 26 });
  tl.set(s.el, { autoAlpha: 1 }, 0); IRON.push({ s, path: sub(path, f0, 1, 20) });
  sail(s, sub(path, f0, 1, 20), 0, T_FIRE - 0.4 - k * 0.1, 20);
  if (s.name) { gsap.set(s.name, { autoAlpha: 0 }); tl.to(s.name, { autoAlpha: 1, duration: 0.4 }, T_FOOTE); tl.to(s.name, { autoAlpha: 0, duration: 0.5 }, T_FOOTE + LBL_LIFE); }
});
[-20, 0, 20].forEach((dx, k) => { const path = TENN.slice(0, 5).map((q) => [q[0] + dx, q[1]]);
  const f0 = 0.3 + k * 0.03, s = ship("timber", "carth", posOn(path, f0), 90, null, null, { L: 50 });
  tl.set(s.el, { autoAlpha: 1 }, 0); WOOD.push(s); sail(s, sub(path, f0, 1, 20), 0, T_FIRE + 0.2, 20); });
IRON.forEach(({ s }, k) => stackSmoke([1284 + OFF[k], 735], T_FIRE, T_CMDR + 2));
// the duel: ironclads' bow guns -> the fort; the fort's guns -> the river (visible, ~1 shot / 1.3 s)
const BOW = (k) => [1284 + OFF[k], 756];
const HITS = [[FH[0] - 8, FH[1] - 4], [FH[0] + 6, FH[1] + 6], [FH[0] - 2, FH[1] - 10], [FH[0] + 10, FH[1] - 2], [FH[0] - 10, FH[1] + 8], [FH[0] + 2, FH[1] + 2]];
[[T_FIRE + 0.2, 0], [T_FIRE + 0.9, 2], [T_FIRE + 2.0, 1], [T_FLOOD + 0.9, 3], [T_TWO + 0.6, 0], [T_CMDR + 0.4, 2], [T_TIL + 0.6, 1]].forEach(([t, k], i) =>
  shoot(BOW(k), HITS[i % HITS.length], t, { r: 6, width: 0.9, dur: 0.55, h: 10, dx: 0, dy: 3 }));
[[T_FIRE + 1.5, [1268, 752]], [T_FLOOD + 0.3, [1302, 744]], [T_TWO + 0.1, [1288, 760]], [T_CMDR + 1.0, [1258, 748]]].forEach(([t, to]) =>
  shoot([FH[0] - 14, FH[1] - 12], to, t, { r: 5, width: 0.9, dur: 0.55, h: 10, color: "#ffd1b8" }));
B.caption("TWO FEET DEEP IN WATER", T_TWO - 0.1, T_CMDR - 0.2, "rome");
// ---------- Tilghman had already sent his men away (toward Fort Donelson); he gives the fort to the navy ----------
const TB = badge({ name: "LLOYD TILGHMAN", role: "CONFEDERATE COMMANDER", initials: "LT", photo: PHOTO("tilghman"), flag: FL.cs, side: "rome", corner: "bl", t: T_TIL - 0.05, until: T_GRANT - 0.3 });
unitS("gar", "rome", [FH[0] + 44, FH[1] + 14], "infantry", null, { t: 0.3 });
const OUT = [[FH[0] + 44, FH[1] + 14], [1400, 806], [1470, 818], [1530, 826], [1600, 836]];
along("gar", OUT, T_MARCH - 0.2, 3.4, 18); hideU(["gar"], T_MARCH + 3.6);
arw({ pts: [[FH[0] + 40, FH[1] + 2], [1410, 798], [1500, 812], [1560, 824]], side: "rome", t: T_MARCH, dur: 2.0, width: AW(2.2, 12), dash: "12 8", until: T_SURR + 2.5 });
wstampS("SURRENDERED", FH[0] - 70, FH[1] - 20, T_SURR + 0.15, null, "#9fc0ea", 26);
boxS("ABOUT 90 MEN", FH[0] - 6, FH[1] + 50, T_NINETY, null, { size: 22, bg: "#f3d6d0" });
// ---------- Grant had not needed to storm the fort: his columns, still on the road from the landing ----------
const GB = badge({ name: "ULYSSES S. GRANT", role: "BRIGADIER GENERAL", initials: "USG", photo: PHOTO("grant"), flag: FL.us, side: "carth", corner: "bl", t: T_GRANT + 0.25, until: END + 1 });
unitS("g1", "carth", [LAND[0] + 6, LAND[1] - 20], "infantry", null, { t: 0.2 }); unitS("g2", "carth", [LAND[0] + 40, LAND[1] - 4], "infantry", null, { t: 0.3 });
along("g1", [[LAND[0] + 6, LAND[1] - 20], [1352, 730], [1352, 742]], 0.6, T_SURR, 10);
along("g2", [[LAND[0] + 40, LAND[1] - 4], [1382, 726], [1385, 744]], 0.8, T_SURR, 10);
arw({ pts: [[1356, 728], [1352, 752], [1342, 770]], side: "carth", t: T_GRANT + 0.2, dur: 1.2, width: AW(2.3, 11), dash: "10 7", until: END + 1 });
B.caption("GRANT HAD NOT NEEDED TO STORM THE FORT", T_STORM - 0.9, END + 1, "carth r");
K.target(FH[0], FH[1], T_STORM, { r: 26, side: "#9fc0ea", until: END + 1 });
// ---------- clean screen: the title card is up -> the legend/badges step out (the date scroll stays) ----------
declutter([LGD, TB, GB], [[T_FHN, T_FHN + 2.6]]);
fixImgs();
K.raiseTerritory();
B.finish();
