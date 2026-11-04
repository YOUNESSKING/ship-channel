// m1c (m1-3..m1-4), Grant #16: Fort Donelson close-up, OPTION 2 (two-colour glowing front lines only, no fill).
// 14 Feb 3 pm: Foote's four ironclads against the water batteries; the flagship hit ~60 times, two ironclads drift back, Foote wounded;
// night: rain and snow, Grant's men without blankets. 15 Feb dawn (new angle, from the Union right): the breakout against the Union right,
// three days' rations, the road out glows; the right wing breaks, no cartridges.
// Basemap donelson_hd_lift (z13, v11). Built with: python3 tools/m1_build.py m1c donelson_hd_lift m1-3 m1-4
// @@BODY
const P3 = "m1-3", P4 = "m1-4";
const T_14 = at(P3, "On the fourteenth"), T_FOOTE = at(P3, "Foote brought"), T_BATTER = at(P3, "to batter the fort"), T_HIT = at(P3, "hit his flagship"),
  T_60 = at(P3, "about sixty times"), T_DRIFT = at(P3, "Two of the ironclads drifted"), T_HELP = at(P3, "helpless"), T_WOUND = at(P3, "Foote himself was wounded"),
  T_NIGHT = at(P3, "That night"), T_RAIN = at(P3, "rain and snow"), T_FREEZE = at(P3, "freezing and thawing"), T_BLANK = at(P3, "thrown away their blankets");
const T_CHANCE = at(P4, "The Confederates saw their chance"), T_DAWN = at(P4, "At dawn on the fifteenth"), T_STRUCK = at(P4, "they struck the Union right"),
  T_MOST = at(P4, "most of their garrison"), T_RATIONS = at(P4, "three days of rations"), T_HAVER = at(P4, "in their haversacks"),
  T_LAST = at(P4, "not planning a last stand"), T_LEAVE = at(P4, "planning to leave"), T_ROAD = at(P4, "if the road opened"),
  T_KNOW = at(P4, "Grant did not know that yet"), T_BREAK = at(P4, "his right wing was breaking"), T_MUSK = at(P4, "muskets but no cartridges"), T_NOC = at(P4, "no cartridges");
// ---------- places (donelson map px) ----------
const DON = [1388, 738], DOV = [1508, 756], WB = [[1368, 704], [1410, 702]];
const WORKS = [[1540, 811], [1487, 832], [1429, 825], [1371, 796], [1312, 753], [1289, 702], [1307, 651], [1324, 630]];
const ULINE = [[1557, 854], [1487, 876], [1406, 869], [1330, 832], [1266, 775], [1243, 709], [1254, 644], [1289, 601]];
const MID = WORKS.map((q, i) => [(q[0] + ULINE[i][0]) / 2, (q[1] + ULINE[i][1]) / 2]);
const PUSH = MID.map((q, i) => i < 4 ? [q[0] - [10, 20, 38, 46][i], q[1] + [60, 66, 58, 40][i]] : (i === 4 ? [q[0] - 14, q[1] + 12] : q));   // the breakout bulge
const RIVER_N = [[1180, 200], [1240, 340], [1300, 460], [1340, 540], [1360, 590]];
const ROAD_OUT = [[1500, 800], [1480, 880], [1462, 980], [1450, 1100], [1470, 1250], [1500, 1420], [1520, 1600]];
const CUMB = [[1120, 0], [1180, 200], [1240, 340], [1320, 500], [1400, 620], [1480, 690], [1600, 680], [1720, 640], [1840, 624], [1980, 700], [2100, 820]];
// ---------- map (option 2: no territory fill) ----------
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); LV.shimmer([CUMB], { width: 1.2 }); LV.scaleBar(15.37); LV.north();
const LGD = now(legend(0, END + 1, true));
camera([[0, 1360, 640, 2.2], [T_FOOTE, 1355, 650, 2.4], [T_HIT, 1365, 655, 2.7], [T_DRIFT + 0.4, 1330, 600, 2.3], [T_WOUND + 0.4, 1340, 640, 2.2],
  [T_NIGHT + 0.4, 1350, 720, 1.9], [T_BLANK, 1300, 740, 2.0], [T_CHANCE - 0.6, 1310, 760, 2.0],
  [T_DAWN + 0.6, 1420, 850, 2.4], [T_RATIONS, 1420, 860, 2.5], [T_LEAVE, 1460, 940, 2.0], [T_KNOW, 1440, 900, 2.1], [T_BREAK + 0.4, 1410, 880, 2.5], [END, 1400, 880, 2.45]]);
dateNow("12 FEBRUARY 1862", T_14 + 0.1); B.date("14 FEB · 3 PM", T_14 + 0.2, T_NIGHT - 0.1, 34); B.date("14 FEB · NIGHT", T_NIGHT, T_DAWN - 0.1, 34); B.date("15 FEB · DAWN", T_DAWN, null, 34);
// ---------- flags (both on every frame) ----------
flagS(FL.us, 1210, 560, 0, T_NIGHT + 0.6, 90); flagS(FL.cs, 1480, 760, 0, T_NIGHT + 0.6, 90);
flagS(FL.us, 1215, 820, T_NIGHT + 0.4, END + 1, 90); flagS(FL.cs, 1470, 690, T_NIGHT + 0.5, T_DAWN + 0.6, 90);
flagS(FL.cs, 1560, 760, T_DAWN + 0.4, END + 1, 90);
// ---------- the lines (option 2: the two-colour glowing front where the sides touch) ----------
fortIcon(DON, 0, null, { s: 24 }); poleFlag(FL.cs, [DON[0] + 4, DON[1] - 8], 0, null, 34);
WB.forEach((p) => unitS("wb" + p[0], "rome", p, "artillery", null, { t: 0, w: 40, h: 27 }));
const FR = frontS({ pts: MID, to: PUSH, moveT: T_STRUCK + 0.2, moveDur: 3.0, sideA: "carth", sideB: "rome", t: 0, dur: 0.01, width: FWc(2.3), until: END + 1 });
const UN = [["sm1", [1250, 660]], ["sm2", [1243, 720]], ["wal", [1268, 790]], ["mc1", [1340, 858]], ["mc2", [1420, 893]], ["mc3", [1500, 893]]];
UN.forEach(([id, p]) => unitS(id, "carth", p, "infantry", null, { t: 0, size: "X" }));
const RD = [["bu", [1318, 700]], ["c1", [1360, 770]], ["c2", [1430, 800]], ["c3", [1490, 808]]];
RD.forEach(([id, p]) => unitS(id, "rome", p, "infantry", null, { t: 0, size: "X" }));
tl.to(B.units.c2.el, { y: -3, duration: 0.7, yoyo: true, repeat: 5, ease: "sine.inOut" }, 0.1);
// ---------- 14 Feb: Foote's ironclads against the water batteries ----------
const FB = badge({ name: "ANDREW FOOTE", role: "FLAG OFFICER · UNION GUNBOATS", initials: "AF", photo: PHOTO("foote"), flag: FL.us, side: "carth", corner: "bl", t: T_FOOTE, until: T_NIGHT + 0.2 });
const SH = [[1304, 584], [1326, 596], [1350, 604], [1372, 612]].map((p, k) => {
  const s = ship("iron", "carth", [p[0] - 120, p[1] - 220], 62, null, null, { L: 58, name: k === 1 ? "FLAGSHIP" : null, ny: 22 });
  tl.set(s.el, { autoAlpha: 1 }, 0); if (s.name) { gsap.set(s.name, { autoAlpha: 0 }); tl.to(s.name, { autoAlpha: 1, duration: 0.4 }, T_HIT); tl.to(s.name, { autoAlpha: 0, duration: 0.5 }, T_HIT + LBL_LIFE); }
  sail(s, [[p[0] - 120, p[1] - 220], [p[0] - 80, p[1] - 130], [p[0] - 30, p[1] - 50], p], 0, T_BATTER + 0.2 + k * 0.15, 12); return { s, p }; });
[[1270, 520], [1292, 510]].forEach((p, k) => { const s = ship("timber", "carth", [p[0] - 110, p[1] - 220], 62, null, null, { L: 50 }); tl.set(s.el, { autoAlpha: 1 }, 0);
  sail(s, [[p[0] - 110, p[1] - 220], [p[0] - 60, p[1] - 110], p], 0, T_BATTER + 0.6, 10); });
SH.forEach(({ p }) => stackSmoke([p[0] - 6, p[1] - 6], T_BATTER, T_DRIFT + 3, 1.7));
// the duel (visible, big): bow guns -> batteries; batteries -> ships (plunging fire from the bluff)
const bow = (k) => [SH[k].p[0] + 8, SH[k].p[1] + 10];
[[T_BATTER + 0.3, 0, 0], [T_BATTER + 1.4, 2, 1], [T_HIT + 1.2, 3, 0], [T_60 + 1.6, 0, 1], [T_DRIFT + 0.4, 3, 1]].forEach(([t, k, w]) =>
  shoot(bow(k), [WB[w][0] + 6, WB[w][1] + 4], t, { r: 6, width: 0.9, dur: 0.5, h: 10 }));
[[T_BATTER + 0.8, 0, 1], [T_HIT + 0.1, 1, 1], [T_HIT + 0.8, 0, 1], [T_60 + 0.3, 1, 1], [T_60 + 1.0, 1, 0], [T_DRIFT - 0.3, 0, 3], [T_HELP, 1, 1]].forEach(([t, w, k]) =>
  shoot([WB[w][0] - 4, WB[w][1] - 8], [SH[k].p[0] + 2, SH[k].p[1]], t, { r: 6, width: 0.9, dur: 0.6, h: 14, color: "#ffd1b8" }));
const HITS = ticker("HITS ON THE FLAGSHIP", 60, "", "right:70px;top:240px;", T_60 - 0.3, 1.6, T_DRIFT + 1.0, 8, { col: "#ff8a80", pre: "~", sub: "ABOUT" });
// two ironclads drift back down the river, helpless (turning, smoking)
[1, 0].forEach((k, j) => { const { s, p } = SH[k];
  sail(s, [p, [p[0] - 40, p[1] - 70], [p[0] - 90, p[1] - 170], [p[0] - 130, p[1] - 260]], T_DRIFT + 0.3 + j * 0.3, 7.5, 16, { keepRot: true });
  tl.to(s.rot, { rotation: "+=140", duration: 7.5, ease: "sine.inOut" }, T_DRIFT + 0.3 + j * 0.3);
  [0, 1.5, 3, 4.5].forEach((d) => K.smoke(p[0] - 30 - d * 10, p[1] - 50 - d * 22, T_DRIFT + 0.6 + d, { n: 3, r: 7, rise: 18, life: 2.4 })); });
[2, 3].forEach((k) => sail(SH[k].s, [SH[k].p, [SH[k].p[0] - 50, SH[k].p[1] - 110]], T_WOUND + 0.4, 4, 8, { keepRot: true }));
B.caption("TWO IRONCLADS DRIFT BACK, HELPLESS", T_DRIFT + 0.2, T_WOUND - 0.1, "carth");
badgeStamp(FB, "WOUNDED", T_WOUND + 0.4);
// ---------- night: rain and snow; blankets thrown away on the march ----------
nightWash(T_NIGHT - 0.2, T_DAWN - 0.4, 0.5);
B.snow(T_RAIN - 0.3, T_DAWN + 0.6);
B.caption("RAIN AND SNOW · FREEZING AND THAWING", T_RAIN, T_BLANK - 0.2, "");
const BLK = `<svg width="26" height="18" viewBox="0 0 26 18" style="display:block;filter:drop-shadow(0 1px 2px #000)"><path d="M2 4 Q8 1 13 4 Q18 7 24 3 L24 14 Q18 17 13 14 Q8 11 2 14 Z" fill="#8d7a5e" stroke="#efe6cf" stroke-width="1.2"/><path d="M5 8 L21 8 M5 11 L21 11" stroke="#5a4a36" stroke-width="1"/></svg>`;
[[1150, 640], [1100, 610], [1040, 590], [1180, 760], [1120, 740], [1060, 720], [990, 700]].forEach((p, k) => pinS(GG.pin(`<div style="transform:scale(1.5)">${BLK}</div>`, p[0], p[1], { t: T_BLANK + k * 0.15, pop: true, until: T_CHANCE + 0.4 })));
B.caption("BLANKETS THROWN AWAY ON THE MARCH", T_BLANK + 0.1, T_CHANCE - 0.1, "carth");
// ---------- 15 Feb dawn: the breakout against the Union right ----------
dawnWash(T_DAWN - 0.2, END + 1);
[[[1440, 820], [1430, 870], [1410, 925]], [[1495, 825], [1500, 880], [1490, 940]], [[1380, 800], [1345, 845], [1300, 880]]].forEach((pts, k) =>
  arw({ pts, side: "rome", t: T_STRUCK - 0.1 + k * 0.3, dur: 1.4, width: AW(2.4, 14), until: END + 1 }));
[["c1", [1310, 860]], ["c2", [1410, 905]], ["c3", [1490, 910]]].forEach(([id, p], k) => B.move(id, T_STRUCK + 0.2 + k * 0.2, 3.0, p[0], p[1]));
[["c4", [1460, 790]], ["c5", [1520, 790]]].forEach(([id, p], k) => { unitS(id, "rome", p, "infantry", null, { t: T_MOST + k * 0.2, size: "X" }); B.move(id, T_MOST + 0.6, 2.4, p[0] - 20, p[1] + 70); });
mg([1430, 880], [1410, 900], T_STRUCK + 1.6, 5, 1.0); mg([1495, 885], [1495, 905], T_MOST + 0.6, 5, 1.0);
[["mc1", [1280, 905]], ["mc2", [1380, 950]], ["mc3", [1470, 965]]].forEach(([id, p], k) => B.move(id, T_STRUCK + 0.6 + k * 0.2, 3.0, p[0], p[1]));
// the haversack card (one big card; the HUD steps out)
const HAV = `<svg width="70" height="70" viewBox="0 0 100 100"><path d="M18 34 Q50 18 82 34 L78 86 Q50 96 22 86 Z" fill="#9a8460" stroke="#f7f3ea" stroke-width="4"/><path d="M18 34 Q50 56 82 34" fill="#b49c74" stroke="#f7f3ea" stroke-width="4"/><path d="M30 30 Q50 -6 70 30" fill="none" stroke="#f7f3ea" stroke-width="5"/></svg>`;
const RAT = scr(`<div style="display:flex;align-items:center;gap:26px;padding:20px 46px 22px;background:rgba(18,16,12,0.93);border-top:6px solid #c4121f;font-family:Oswald;font-weight:700;color:#f7f3ea;box-shadow:0 20px 40px rgba(0,0,0,.55)">${HAV}
  <div><div style="font-size:64px;letter-spacing:.06em;line-height:1">THREE DAYS OF RATIONS</div><div class="s2" style="font-size:24px;letter-spacing:.3em;color:#ff8a80;margin-top:6px">IN THEIR HAVERSACKS</div></div></div>`,
  "left:0;right:0;top:230px;display:flex;justify-content:center;", T_RATIONS, T_LAST - 0.3);
SFX("hit", T_RATIONS + 0.3); const S2 = RAT.querySelector(".s2"); gsap.set(S2, { autoAlpha: 0 }); tl.to(S2, { autoAlpha: 1, duration: 0.3 }, T_HAVER);
// not a last stand: they meant to leave, if the road opened (the road out glows; a dashed red arrow toward Nashville)
const RO = glowPath(ROAD_OUT, "#ffb08a", 4, T_LEAVE - 0.2, END + 1, 4, 0.9, { draw: 1.4, top: true });
arw({ pts: ROAD_OUT.slice(1, 6).map((q) => [q[0] + 18, q[1]]), side: "rome", t: T_ROAD, dur: 1.8, width: AW(2.0, 12), dash: "12 9", until: END + 1 });
boxS("THE ROAD", ROAD_OUT[3][0] + 90, ROAD_OUT[3][1], T_ROAD + 0.3, null, { size: 26, bg: "#f3d6d0" });
B.caption("NOT A LAST STAND: THEY PLANNED TO LEAVE", T_LAST, T_KNOW - 0.1, "rome");
// Grant did not know that yet; his right wing breaking, no cartridges
const GB = badge({ name: "ULYSSES S. GRANT", role: "DID NOT KNOW THAT YET", initials: "USG", photo: PHOTO("grant"), flag: FL.us, side: "carth", corner: "bl", t: T_KNOW, until: END + 1 });
greyU(["mc1", "mc2", "mc3"], T_BREAK + 0.2);
[["mc1", [1250, 950]], ["mc2", [1350, 1000]], ["mc3", [1440, 1015]]].forEach(([id, p], k) => B.move(id, T_BREAK + 0.3 + k * 0.15, 2.2, p[0], p[1]));
wstampS("BREAKING", 1360, 990, T_BREAK + 0.3, null, "#e3232f", 24);
B.caption("MUSKETS BUT NO CARTRIDGES", T_MUSK, END + 1, "carth");
// ---------- clean screen ----------
declutter([LGD, FB, GB, HITS], [[T_RATIONS, T_LAST - 0.3]]);
fixImgs();
K.raiseTerritory();
B.finish();
