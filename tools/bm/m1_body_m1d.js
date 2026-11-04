// m1d (m1-5..m1-6), Grant #16: Fort Donelson close-up, option 2. 15 Feb: Grant rides back along the line, does not panic;
// "whoever attacks first now will win" (paraphrase card, no quote marks); the cartridge boxes are filled, the right re-forms ("acted like a charm");
// the Confederates pull back inside the ring; the first counterattack on the LEFT: C. F. Smith leads his division through the abatis
// and takes the outer works; night: the Confederate council decides to give up.
// Basemap donelson_hd_lift (z13, v11). Built with: python3 tools/m1_build.py m1d donelson_hd_lift m1-5 m1-6
// @@BODY
const P5 = "m1-5", P6 = "m1-6";
const T_RODE = at(P5, "Grant rode along the line"), T_PANIC = at(P5, "did not panic"), T_TOLD = at(P5, "He told an officer"), T_WHO = at(P5, "whoever attacked first"),
  T_HURRY = at(P5, "in a hurry"), T_FILL = at(P5, "fill their cartridge boxes"), T_BACK = at(P5, "get back into line"), T_CHARM = at(P5, "acted like a charm"),
  T_REPORT = at(P5, "In his official report"), T_GREAT = at(P5, "as great as his own"), T_POSS = at(P5, "possibly greater"), T_GONE = at(P5, "had gone out to break the ring"),
  T_PULLED = at(P5, "pulled back inside it"), T_COUNTER = at(P5, "Grant ordered counterattacks"), T_LEFT = at(P5, "the first would come on the left");
const T_SMITH = at(P6, "General C. F. Smith"), T_UP = at(P6, "led his division up the hill"), T_FRONT = at(P6, "going in front himself"),
  T_FELLED = at(P6, "through the felled trees"), T_TOOK = at(P6, "took the outer works"), T_NIGHT = at(P6, "That night"), T_COUNCIL = at(P6, "held a council"),
  T_GIVE = at(P6, "the choice was to give up"), T_GU = at(P6, "give up");
// ---------- places (donelson map px) ----------
const DON = [1388, 738], DOV = [1508, 756];
const WORKS = [[1540, 811], [1487, 832], [1429, 825], [1371, 796], [1312, 753], [1289, 702], [1307, 651], [1324, 630]];
const ULINE = [[1557, 854], [1487, 876], [1406, 869], [1330, 832], [1266, 775], [1243, 709], [1254, 644], [1289, 601]];
const MID = WORKS.map((q, i) => [(q[0] + ULINE[i][0]) / 2, (q[1] + ULINE[i][1]) / 2]);
const PUSH = MID.map((q, i) => i < 4 ? [q[0] - [10, 20, 38, 46][i], q[1] + [60, 66, 58, 40][i]] : (i === 4 ? [q[0] - 14, q[1] + 12] : q));
const MID2 = MID.map((q, i) => i >= 5 ? [q[0] + [0, 0, 0, 36, 40, 30, 22, 10][i], q[1] + [0, 0, 0, 0, 0, 6, 14, 18][i]] : q);   // Smith's lodgement
const CUMB = [[1120, 0], [1180, 200], [1240, 340], [1320, 500], [1400, 620], [1480, 690], [1600, 680], [1720, 640], [1840, 624], [1980, 700], [2100, 820]];
const RIDE = [[1215, 560], [1205, 640], [1200, 720], [1215, 800], [1260, 880], [1320, 935], [1390, 960]];
// ---------- map (option 2) ----------
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); LV.shimmer([CUMB], { width: 1.2 }); LV.scaleBar(15.37); LV.north();
const LGD = now(legend(0, END + 1, true));
dawnWash(0, T_NIGHT); { const d = document.getElementById("fx").lastElementChild; gsap.set(d, { autoAlpha: 1 }); tl.getTweensOf(d).filter((tw) => tw.startTime() < 0.05).forEach((tw) => tw.kill()); }
camera([[0, 1300, 820, 2.0], [T_TOLD, 1300, 860, 2.1], [T_FILL, 1360, 900, 2.4], [T_REPORT, 1400, 870, 2.2], [T_PULLED + 0.6, 1380, 820, 2.0],
  [T_LEFT + 0.4, 1290, 670, 2.5], [T_FELLED, 1285, 655, 2.9], [T_TOOK + 1.2, 1300, 670, 2.7], [T_NIGHT + 0.3, 1400, 720, 2.2], [END, 1420, 730, 2.15]]);
dateNow("15 FEB · DAWN", T_RODE + 0.4); B.date("15 FEBRUARY 1862", T_RODE + 0.5, T_NIGHT - 0.1, 34); B.date("15 FEB · NIGHT", T_NIGHT, null, 34);
// ---------- flags ----------
flagS(FL.us, 1150, 760, 0, END + 1, 90); flagS(FL.cs, 1520, 690, 0, END + 1, 90);
// ---------- the lines and units as m1c left them ----------
fortIcon(DON, 0, null, { s: 24 }); poleFlag(FL.cs, [DON[0] + 4, DON[1] - 8], 0, null, 34);
const F1 = frontS({ pts: PUSH, to: MID, moveT: T_PULLED - 0.3, moveDur: 3.0, sideA: "carth", sideB: "rome", t: 0, dur: 0.01, width: FWc(2.2), until: T_TOOK - 0.3 });
const F2 = frontS({ pts: MID, to: MID2, moveT: T_TOOK - 0.6, moveDur: 2.6, sideA: "carth", sideB: "rome", t: T_TOOK - 0.4, dur: 0.01, width: FWc(2.8), until: END + 1 });
[["sm1", [1250, 660]], ["sm2", [1243, 720]], ["wal", [1268, 790]]].forEach(([id, p]) => unitS(id, "carth", p, "infantry", null, { t: 0, size: "X" }));
[["mc1", [1250, 950]], ["mc2", [1350, 1000]], ["mc3", [1440, 1015]]].forEach(([id, p]) => unitS(id, "carth", p, "infantry", null, { t: 0, size: "X" }));
greyU(["mc1", "mc2", "mc3"], 0); tl.set(["mc1", "mc2", "mc3"].map((id) => B.units[id].el.querySelector(".blk")), { filter: "grayscale(1) brightness(0.75)" }, 0);
const RED = [["bu", [1318, 700], [1318, 700]], ["c1", [1310, 860], [1352, 790]], ["c2", [1410, 905], [1420, 805]], ["c3", [1490, 910], [1490, 812]], ["c4", [1440, 860], [1455, 780]], ["c5", [1500, 860], [1525, 790]]];
RED.forEach(([id, p]) => unitS(id, "rome", p, "infantry", null, { t: 0, size: "X" }));
// ---------- Grant rides back along the line ----------
unitS("gr", "carth", RIDE[0], "infantry", "GRANT", { t: 0 }); cavIcon("gr");
along("gr", RIDE, 0.2, T_FILL - 0.4, 20);
const GB = now(badge({ name: "ULYSSES S. GRANT", role: "BRIGADIER GENERAL", initials: "USG", photo: PHOTO("grant"), flag: FL.us, side: "carth", corner: "bl", t: 0, until: T_SMITH - 0.4 }));
B.caption("HE DID NOT PANIC", T_PANIC, T_WHO - 0.3, "carth");
const C1 = belief("WHOEVER ATTACKS FIRST NOW WILL WIN", "GRANT TO AN OFFICER", T_WHO, T_FILL - 0.4, { col: "#1f4fc4", subc: "#9fc0ea", size: 54 });
SFX("hit", T_WHO + 0.3);
// fill the cartridge boxes, back into line: "it acted like a charm" (narrated; the caption carries no quote marks)
const CBOX = `<svg width="26" height="20" viewBox="0 0 26 20" style="display:block;filter:drop-shadow(0 1px 2px #000)"><rect x="2" y="3" width="22" height="15" rx="2" fill="#2a2420" stroke="#efe6cf" stroke-width="1.4"/><rect x="2" y="3" width="22" height="5" fill="#4a3c2c" stroke="#efe6cf" stroke-width="1.2"/><circle cx="13" cy="12" r="2.6" fill="#c9b48a"/></svg>`;
[[1265, 925], [1365, 975], [1455, 990], [1300, 960], [1405, 985]].forEach((p, k) => pinS(GG.pin(`<div style="transform:scale(1.5)">${CBOX}</div>`, p[0], p[1], { t: T_FILL + k * 0.18, pop: true, until: T_CHARM + 2.5 })));
SFX("ref:pop", T_FILL + 0.2);
ungreyU(["mc1", "mc2", "mc3"], T_BACK);
[["mc1", [1290, 885]], ["mc2", [1385, 935]], ["mc3", [1470, 945]]].forEach(([id, p], k) => B.move(id, T_BACK + 0.1 + k * 0.15, 2.0, p[0], p[1]));
B.caption("FILL YOUR CARTRIDGE BOXES · BACK INTO LINE", T_FILL, T_CHARM - 0.1, "carth");
B.caption("IT ACTED LIKE A CHARM", T_CHARM, T_REPORT - 0.1, "carth");
// the official report: the confusion on the Confederate side as great as his own, possibly greater
const C2 = belief("AS GREAT AS HIS OWN · POSSIBLY GREATER", "GRANT'S OFFICIAL REPORT · CONFUSION ON THE CONFEDERATE SIDE", T_GREAT - 0.2, T_GONE - 0.2, { col: "#c4121f", size: 46 });
["c1", "c2", "c3", "c4", "c5"].forEach((id, k) => tl.to(B.units[id].el.querySelector(".blk"), { rotation: k % 2 ? 8 : -8, duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }, T_GREAT + k * 0.12));
// they had gone out to break the ring, then pulled back inside it
[[1310, 900], [1410, 950], [1490, 955]].forEach((p, k) => arw({ pts: [[p[0], p[1] - 70], [p[0] + 4, p[1] - 30]], side: "rome", t: T_GONE + k * 0.2, dur: 0.6, width: AW(2.2, 11), dash: "8 6", until: T_PULLED + 0.4 }));
RED.forEach(([id, , q], k) => { if (id !== "bu") B.move(id, T_PULLED - 0.2 + k * 0.1, 2.8, q[0], q[1]); });
[[1440, 880], [1360, 860]].forEach((p, k) => arw({ pts: [p, [p[0] + 6, p[1] - 60]], side: "rome", t: T_PULLED + 0.1 + k * 0.3, dur: 1.0, width: AW(2.1, 12), until: T_COUNTER + 0.6 }));
B.caption("BACK INSIDE THE RING", T_PULLED + 0.2, T_COUNTER - 0.1, "rome");
// counterattacks: the first on the left
K.target(1300, 655, T_LEFT, { r: 40, side: "#9fc0ea", until: T_TOOK });
boxS("THE LEFT", 1180, 610, T_LEFT + 0.2, null, { size: 26, bg: "#dcecf8" });
// ---------- C. F. Smith storms the abatis and takes the outer works ----------
const SB = badge({ name: "C. F. SMITH", role: "UNION DIVISION · THE LEFT", initials: "CFS", photo: PHOTO("csmith"), flag: FL.us, side: "carth", corner: "bl", t: T_SMITH, until: T_NIGHT + 0.2 });
const ABT = `<svg width="18" height="12" viewBox="0 0 18 12" style="display:block"><path d="M1 10 L9 2 L17 10 M5 10 L9 5 L13 10" fill="none" stroke="#5b4a30" stroke-width="2.2" stroke-linecap="round"/><path d="M1 10 L9 2 L17 10" fill="none" stroke="#cdb98e" stroke-width="0.9" stroke-linecap="round"/></svg>`;
[[1290, 690], [1286, 676], [1290, 662], [1296, 648], [1302, 636], [1310, 624], [1282, 704], [1284, 716]].forEach((p, k) => pinS(GG.pin(`<div style="transform:scale(1.3)">${ABT}</div>`, p[0] - 16, p[1], { t: T_FELLED - 0.4 + k * 0.06, pop: true, until: T_NIGHT + 1 })));
B.caption("THROUGH THE FELLED TREES", T_FELLED, T_TOOK - 0.1, "carth");
[[[1225, 640], [1262, 648], [1300, 650]], [[1220, 690], [1258, 690], [1296, 684]], [[1240, 610], [1275, 622], [1310, 632]]].forEach((pts, k) =>
  arw({ pts, side: "carth", t: T_UP + k * 0.35, dur: 1.6, width: AW(2.8, 15), until: T_NIGHT + 0.6 }));
B.move("sm1", T_FRONT, 3.0, 1305, 660); B.move("sm2", T_FRONT + 0.3, 3.0, 1302, 700);
[0, 0.9].forEach((d) => mg([1262, 662], [1300, 668], T_FELLED + 0.2 + d, 5, 0.9)); mg([1318, 700], [1278, 690], T_UP + 0.6, 4, 0.9);
B.move("bu", T_TOOK - 0.2, 2.2, 1350, 712);
wstampS("TOOK THE OUTER WORKS", 1300, 610, T_TOOK + 0.1, null, "#9fc0ea", 24);
// ---------- night: the Confederate council chooses to give up ----------
nightWash(T_NIGHT - 0.2, null, 0.5);
const COUN = pinS(GG.pin(`<div style="width:60px;height:60px;border-radius:50%;background:radial-gradient(circle,rgba(255,220,140,.95) 0%,rgba(255,170,60,.55) 35%,rgba(255,120,20,0) 72%);mix-blend-mode:screen"></div>`, DOV[0] - 6, DOV[1] - 8, { t: T_COUNCIL - 0.3, until: END + 1 }));
tl.to(COUN.firstElementChild, { scale: 1.2, opacity: 0.7, duration: 0.3, yoyo: true, repeat: 9, ease: "sine.inOut" }, T_COUNCIL);
boxS("COUNCIL", DOV[0] + 70, DOV[1] - 20, T_COUNCIL, null, { size: 24, bg: "#f3d6d0" });
const GU = sstamp("GIVE UP", 250, T_GU - 0.05, { size: 84, sub: "THE CONFEDERATE COUNCIL", until: END - 0.1 });
// ---------- clean screen ----------
declutter([LGD, GB, SB], [[T_WHO, T_FILL - 0.4], [T_GREAT - 0.2, T_GONE - 0.2], [T_GU - 0.05, END + 1]]);
fixImgs();
K.raiseTerritory();
B.finish();
