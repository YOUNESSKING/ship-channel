// m3c (m3-5), Grant #16: the first attack on Petersburg, 15 Jun 1864. Close-up OPTION 2 (two-colour glowing fronts only) on the Dimmock Line east
// of the city: about 14,000 men of W. F. Smith's corps, Hinks's division of Black soldiers in the lead, against about 2,200 under Beauregard;
// a stretch of the defences about two miles wide breaks (Batteries 3-11, NPS "two mile-long hole"); Smith stops for the night (night wash),
// faint ghost arrows to the open city he did not take.
// Basemap petersburg_hd_lift (z12, v11; preview m3x_pet until baked). Built with: python3 tools/m3_build.py m3c petersburg m3-5 m3-5
// @@BODY
const P5 = "m3-5", G = GEO.pet;
const T_ATT = at(P5, "The first attack on Petersburg"), T_PB = at(P5, "on Petersburg"), T_15 = at(P5, "fifteenth of June"), T_14K = at(P5, "fourteen thousand"),
  T_SMITH = at(P5, "William F. Smith"), T_BLACK = at(P5, "a division of Black soldiers"), T_HINKS = at(P5, "Edward Hinks"), T_LEAD = at(P5, "in the lead"),
  T_FACED = at(P5, "They faced"), T_22 = at(P5, "twenty-two hundred"), T_BEAU = at(P5, "under General P."), T_BROKE = at(P5, "and broke through"),
  T_TWO = at(P5, "about two miles wide"), T_STOP = at(P5, "But Smith stopped"), T_NIGHT = at(P5, "for the night"), T_WAIT = at(P5, "waited for the morning");
// ---------- the lines ----------
const DL = G.DIMMOCK.slice(0, 8);                                   // the eastern face of the Dimmock Line (Appomattox -> south)
const DL2 = DL.map((q, i) => i >= 1 && i <= 5 ? [q[0] - [0, 18, 30, 34, 30, 14][i], q[1] + [0, 4, 2, 0, -2, -4][i]] : q);   // after the breach
// ---------- map: option 2 (fronts only), living map ----------
const LV = LivingK(B); LV.clouds({ n: 5, opacity: 0.12 }); LV.shimmer([G.APPOM], { width: 1.2 }); LV.scaleBar(30.4); LV.north();
const LGD = now(legend(0, END + 1, true));
camera([[0, 1560, 790, 2.6], [T_14K, 1540, 805, 2.9], [T_HINKS, 1525, 825, 3.2], [T_22, 1510, 820, 3.0], [T_BROKE + 0.4, 1495, 822, 3.3], [T_STOP, 1480, 830, 3.0],
  [T_WAIT, 1450, 840, 2.6], [END, 1445, 842, 2.55]]);
dateNow("17 JUNE 1864", T_15 - 0.1); B.date("15 JUNE 1864", T_15, null, 34);
// ---------- flags ----------
flagS(FL.us, 1600, 950, 0, END + 1, 100); flagS(FL.cs, 1345, 740, 0, END + 1, 100);
// ---------- front (two colour: blue east of the line), the batteries ----------
const FR = frontS({ pts: DL, to: DL2, moveT: T_BROKE + 0.3, moveDur: 3.0, sideA: "carth", sideB: "rome", t: 0, dur: 0.01, width: FWc(2.9), until: END + 1 });
const BAT = [[1494, 778], [1500, 808], [1503, 838], [1508, 868]];
BAT.forEach((p, k) => unitS("bt" + k, "rome", p, "artillery", null, { t: 0, w: 40, h: 27 }));
unitS("ri", "rome", [1470, 820], "infantry", null, { t: 0, size: "X" });
const PET = town("PETERSBURG", G.PETERSBURG, T_PB, "l", { size: 34 });
// Smith's corps comes down the City Point road (moving at frame 0)
const SU = [["s1", [1640, 640], [1560, 760]], ["s2", [1660, 700], [1565, 815]], ["hk", [1650, 770], [1562, 860]]];
SU.forEach(([id, a, b], k) => { unitS(id, "carth", a, "infantry", id === "hk" ? "HINKS" : null, { t: 0, size: "XX" }); B.move(id, 0, T_FACED - 0.5, b[0], b[1]); });
if (B.units.hk) { const tg = B.units.hk.el.querySelector(".tag"); if (tg) { gsap.set(tg, { autoAlpha: 0 }); tl.to(tg, { autoAlpha: 1, duration: 0.4 }, T_HINKS); } }
arw({ pts: G.CPROAD.slice(1), side: "carth", t: 0.2, dur: 3.0, width: AW(2.6, 13), dash: "10 7", until: T_BROKE });
boxS("ABOUT 14,000", 1650, 700, T_14K, null, { size: 26, bg: "#dcecf8" });
const SB = badge({ name: "WILLIAM F. SMITH", role: "", initials: "WFS", photo: PHOTO("wfsmith"), flag: FL.us, side: "carth", corner: "bl", t: T_SMITH - 0.1, until: T_HINKS - 0.2 });
const HB = badge({ name: "EDWARD HINKS", role: "IN THE LEAD", initials: "EH", photo: PHOTO("hinks"), flag: FL.us, side: "carth", corner: "bl", t: T_HINKS + 0.2, until: T_BROKE + 2.0 });
pulseU("hk", T_LEAD); pulseU("hk", T_LEAD + 0.6);
boxS("ABOUT 2,200", 1440, 870, T_22, null, { size: 26, bg: "#f3d6d0" });
const BB = badge({ name: "P. G. T. BEAUREGARD", role: "", initials: "PGT", photo: PHOTO("beauregard"), flag: FL.cs, side: "rome", corner: "br", t: T_BEAU + 0.6, until: T_STOP - 0.3 });
// ---------- the breakthrough: the batteries fire (visible), the line gives, about two miles wide ----------
shoot([1494, 778], [1560, 770], T_FACED + 0.4, { r: 4, width: 0.6, dur: 0.6, h: 8 });
shoot([1503, 838], [1556, 850], T_22 + 0.4, { r: 4, width: 0.6, dur: 0.6, h: 8 });
shoot([1508, 868], [1560, 866], T_BROKE - 0.2, { r: 4, width: 0.6, dur: 0.6, h: 8 });
mg([1556, 852], [1512, 852], T_BROKE + 0.1, 5, 0.9); mg([1552, 800], [1505, 805], T_BROKE + 0.7, 5, 0.9);
[["s1", [1494, 790]], ["s2", [1490, 828]], ["hk", [1496, 862]]].forEach(([id, p], k) => B.move(id, T_BROKE + 0.3 + k * 0.2, 2.6, p[0], p[1]));
[[[1580, 770], [1540, 780], [1480, 790]], [[1585, 820], [1540, 822], [1470, 828]], [[1585, 868], [1540, 864], [1478, 862]]].forEach((pts, k) =>
  arw({ pts, side: "carth", t: T_BROKE + 0.2 + k * 0.25, dur: 1.4, width: AW(3.3, 13), until: T_STOP + 0.4 }));
greyU(["bt0", "bt1", "bt2", "bt3"], T_BROKE + 1.6); hideU(["bt0", "bt1", "bt2", "bt3"], T_STOP - 0.4);
B.move("ri", T_BROKE + 1.0, 2.5, 1440, 830);
glowPath(G.BREACH.map((q) => [q[0] + 10, q[1]]), "#ffd54a", 1.4, T_TWO - 0.3, T_STOP + 1.0, 2, 0.95, { draw: 1.0, top: true });
boxS("ABOUT TWO MILES WIDE", 1600, 790, T_TWO - 0.1, null, { size: 26 });
// ---------- Smith stops for the night; the open road to the city he did not take ----------
nightWash(T_STOP, null, 0.45, 1.6); K.night({ lines: [FR], tOn: T_STOP });
const SB2 = badge({ name: "WILLIAM F. SMITH", role: "", initials: "WFS", photo: PHOTO("wfsmith"), flag: FL.us, side: "carth", corner: "bl", t: T_STOP - 0.1, until: END + 1 });
badgeStamp(SB2, "STOPPED", T_STOP + 0.5);
[[[1470, 800], [1420, 820], [1385, 845]], [[1468, 840], [1430, 860], [1395, 870]]].forEach((pts, k) => {
  const a = arw({ pts, side: "carth", t: T_WAIT - 0.2 + k * 0.3, dur: 1.2, width: AW(2.6, 11), dash: "6 8", until: END + 1 }); tl.to(a, { opacity: 0.4, duration: 0.6, yoyo: true, repeat: 3 }, T_WAIT + 1.2); });
PET.grow(T_WAIT); tl.to(PET.el.querySelector(".nm"), { autoAlpha: 1, duration: 0.3 }, T_WAIT);
B.caption("SMITH STOPPED FOR THE NIGHT, AND WAITED FOR THE MORNING", T_NIGHT, END + 1, "carth");
// ---------- clean screen ----------
declutter([LGD, SB, HB, BB, SB2], []);
fixImgs();
B.finish();
