// m3a (m3-1..m3-2), Grant #16 MOVE 3 opens: the armies in their trenches at Cold Harbor outside Richmond (12 Jun 1864), Lee's lines hold;
// south across the James lies Petersburg where the railroads meet (title card on "the wide James River"); m3-2: the plan to disappear:
// Sheridan's cavalry west, Lee's cavalry after it (wide), after dark on the 12th Warren's Fifth Corps crosses the Chickahominy and faces
// Richmond while the rest of the army slips out south by back roads, Meade's Army of the Potomac in the lead.
// Basemap richmond_hd_lift (z9, v11; quick preview bake m3x_ric until it is baked). Option 1 territory 12 JUN (tools/m3_make_control.py).
// Built with: python3 tools/m3_build.py m3a richmond m3-1 m3-2
// @@BODY
const P1 = "m3-1", P2 = "m3-2", G = GEO.ric;
const T_JUNE = at(P1, "second week of June"), T_TRENCH = at(P1, "sat in trenches"), T_RICH = at(P1, "outside Richmond"), T_GRANT = at(P1, "Grant could not"),
  T_LEE = at(P1, "Lee's lines"), T_NOT = at(P1, "So he decided not to try"), T_SOUTH = at(P1, "South of Richmond"), T_JAMES = at(P1, "the wide James River"),
  T_PET = at(P1, "lay Petersburg"), T_RR = at(P1, "where the railroads"), T_FED = at(P1, "fed Lee's army"), T_TOG = at(P1, "came together"),
  T_IF = at(P1, "If Grant could take it"), T_STARVE = at(P1, "Richmond would starve");
const T_PLAN = at(P2, "The plan was to disappear"), T_TELL = at(P2, "Grant did not tell the enemy"), T_NEED = at(P2, "he did not need to"),
  T_LOOK = at(P2, "He only needed Lee"), T_WRONG = at(P2, "in the wrong place"), T_SHER = at(P2, "Philip Sheridan"), T_WEST = at(P2, "off to the west"),
  T_LCAV = at(P2, "Lee sent his own cavalry"), T_DARK = at(P2, "After dark"), T_12 = at(P2, "twelfth of June"), T_WAR = at(P2, "Gouverneur Warren"),
  T_CHICK = at(P2, "crossed the Chickahominy"), T_FACED = at(P2, "faced toward Richmond"), T_REST = at(P2, "the rest of the army slipped out"),
  T_SOUTH2 = at(P2, "marched south by back roads"), T_MEADE = at(P2, "General Meade"), T_LEAD = at(P2, "in the lead");
// ---------- map: option 1 (12 JUN 1864), living map ----------
terr("assets/media/m3_ric_jun12_mx.png", 0, null);
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); LV.shimmer([G.JAMES, G.CHICK, G.APPOM], { width: 0.9 }); LV.scaleBar(242.2); LV.north();
camera([[0, 1432, 812, 5.6], [T_TRENCH, 1430, 816, 6.0], [T_GRANT + 1.0, 1436, 818, 6.2], [T_SOUTH, 1432, 860, 5.0], [T_PET, 1428, 915, 4.7], [T_TOG, 1428, 925, 4.9],
  [T_STARVE + 0.6, 1430, 880, 4.6], [T_TELL + 1.0, 1428, 840, 4.9], [T_LOOK + 0.8, 1400, 800, 3.6], [T_SHER, 1320, 740, 2.35], [T_LCAV + 2.2, 1318, 744, 2.3],
  [T_12 + 0.4, 1470, 855, 4.5], [T_CHICK + 1.5, 1475, 868, 4.9], [T_REST + 0.6, 1490, 880, 4.3], [T_LEAD, 1495, 888, 4.1], [END, 1497, 890, 4.05]]);
// date scroll on the spoken date (clean first frame: nothing before it)
B.showDate(T_JUNE + 0.6); B.date("JUNE 1864", T_JUNE + 0.7, T_12 - 0.1, 34); B.date("12 JUNE 1864", T_12, null, 34);
// ---------- flags (US 35-star + CSA first national, both on every frame) ----------
flagS(FL.us, 1588, 868, 0, T_LOOK + 1.2, 100); flagS(FL.cs, 1335, 800, 0, T_SOUTH + 1.0, 100);
flagS(FL.cs, 1318, 948, T_SOUTH + 0.6, T_LOOK + 1.2, 100);
flagS(FL.us, 1640, 850, T_LOOK + 0.9, T_DARK + 1.4, 110); flagS(FL.cs, 1210, 800, T_LOOK + 0.9, T_DARK + 1.4, 110);
flagS(FL.us, 1620, 866, T_DARK + 1.1, END + 1, 100); flagS(FL.cs, 1350, 905, T_DARK + 1.1, END + 1, 100);
// ---------- Cold Harbor: the two lines (option 1 + the two-colour front where the sides touch), trenches ----------
const FR = frontS({ pts: G.CH_FRONT, sideA: "carth", sideB: "rome", t: 0, dur: 0.01, width: FWw(5.6), until: T_REST + 2.0 });
const TR1 = trench(G.CH_FRONT.map((q) => [q[0] + 5.5, q[1]]), T_TRENCH - 0.1, 1.4, T_REST + 2.0, 5.6);
const TR2 = trench(G.CH_FRONT.map((q) => [q[0] - 5.5, q[1]]), T_TRENCH + 0.2, 1.4, T_REST + 6.0, 5.6);
const BU = [["u2", [1456, 796]], ["u6", [1458, 812.5]], ["u18", [1455, 829]]], RU = [["r1", [1426, 794]], ["r2", [1429, 811]], ["r3", [1426, 828]]];
BU.forEach(([id, p]) => unitS(id, "carth", p, "infantry", null, { t: 0, size: "XXX" }));
RU.forEach(([id, p]) => unitS(id, "rome", p, "infantry", null, { t: 0, size: "XXX" }));
unitS("v5", "carth", [1470, 822], "infantry", null, { t: 0, size: "XXX" });            // Warren's Fifth Corps in reserve
unitS("rr", "rome", [1398, 822], "infantry", null, { t: 0, size: "XXX" }); B.move("rr", 0, 4.0, 1414, 818);   // moving at frame 0
B.move("v5", 0.3, 3.5, 1468, 818);
// Grant cannot break through Lee's lines: a probe that bounces, the guns of the line fire (visible, close)
const GB = badge({ name: "ULYSSES S. GRANT", role: "", initials: "USG", photo: PHOTO("grant"), flag: FL.us, side: "carth", corner: "bl", t: T_GRANT - 0.1, until: T_NOT + 1.2 });
const LB = badge({ name: "ROBERT E. LEE", role: "", initials: "REL", photo: PHOTO("lee"), flag: FL.cs, side: "rome", corner: "br", t: T_LEE - 0.1, until: T_NOT + 1.2 });
const PRB = arw({ pts: [[1466, 806], [1452, 808], [1444, 810]], side: "carth", t: T_GRANT + 0.1, dur: 0.9, width: AW(6.2, 13), until: T_NOT + 0.4 });
shoot([1426, 802], [1450, 808], T_GRANT + 0.9, { r: 2.2, width: 0.35, dur: 0.5, h: 3 });
shoot([1428, 820], [1453, 815], T_LEE + 0.5, { r: 2.2, width: 0.35, dur: 0.5, h: 3 });
wstampS("COULD NOT BREAK THROUGH", 1440, 846, T_GRANT + 1.3, null, "#e3232f", 24);
// ---------- south across the wide James lies Petersburg; the railroads meet there ----------
const RICH = town("RICHMOND", G.RICHMOND, T_RICH, "l", { size: 34 });
glowPath(G.JAMES, "#7fb0ff", 1.3, T_JAMES - 0.2, T_PLAN + 1.0, 2, 0.85, { draw: 1.8 });
const TT = B.title("MOVE 3", "THE JAMES RIVER", "JUNE 1864", T_JAMES, T_JAMES + 2.6); SFX("ref:boom", T_JAMES + 0.15);
const LGD = legend(T_JAMES + 3.0, END + 1, false);
const PETL = town("PETERSBURG", G.PETERSBURG, T_PET, "l", { size: 34 });
K.target(G.PETERSBURG[0], G.PETERSBURG[1], T_PET + 0.2, { r: 30, side: "#ffd54a", until: T_STARVE + 1.6 });
const RRS = [G.RR_RP, G.RR_SS, G.RR_W, G.RR_NP, G.RR_CP].map((pts, k) => { const q = pts.slice().reverse();
  glowPath(q, "#2a2118", 1.1, T_RR + 0.1 + k * 0.35, T_PLAN + 0.6, 0, 0.95, { draw: 1.6, top: true });
  return glowPath(q, "#ffd54a", 0.5, T_RR + 0.1 + k * 0.35, T_PLAN + 0.6, 2, 0.9, { draw: 1.6, dash: "1.2 1.6", top: true }); });
B.caption("WHERE THE RAILROADS THAT FED LEE'S ARMY CAME TOGETHER", T_FED - 0.4, T_IF - 0.2, "rome");
// if Grant could take it, Richmond would starve: the Petersburg ring turns blue, the line to Richmond goes dark
K.target(G.PETERSBURG[0], G.PETERSBURG[1], T_IF + 0.2, { r: 22, side: "#2e5cb2", until: T_PLAN + 0.5 });
tl.to(RRS[0], { stroke: "#e3232f", duration: 0.5 }, T_STARVE - 0.2);
RICH.grow(T_STARVE); tl.to(RICH.el.querySelector(".nm"), { autoAlpha: 1, duration: 0.3 }, T_STARVE);
B.caption("IF GRANT COULD TAKE IT, RICHMOND WOULD STARVE", T_IF, T_PLAN - 0.2, "carth");
// ---------- m3-2: the plan was to disappear ----------
B.caption("THE PLAN WAS TO DISAPPEAR", T_PLAN + 0.1, T_TELL + 1.5, "carth");
BU.concat([["v5"]]).forEach(([id], k) => tl.to(B.units[id].el, { opacity: 0.45, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut" }, T_PLAN + 0.2 + k * 0.15));
// Lee looks in the wrong place: his line watches the trenches; question marks over the empty ground to the north-west
const LB2 = badge({ name: "ROBERT E. LEE", role: "", initials: "REL", photo: PHOTO("lee"), flag: FL.cs, side: "rome", corner: "br", t: T_LOOK + 0.4, until: T_SHER - 0.3 });
[[1402, 790], [1388, 772], [1416, 770]].forEach((p, k) => { const q = pinS(GG.pin(`<div style="font-family:Oswald;font-weight:700;font-size:44px;color:#ff8a7a;text-shadow:0 0 8px #000,0 2px 4px #000">?</div>`, p[0], p[1], { t: T_WRONG - 0.3 + k * 0.25 }));
  tl.to(q, { autoAlpha: 0, duration: 0.5 }, T_SHER - 0.2); });
B.caption("LEE LOOKS IN THE WRONG PLACE", T_WRONG, T_SHER - 0.3, "rome");
// Sheridan's cavalry off to the west; Lee's cavalry after it
const SB = badge({ name: "PHILIP SHERIDAN", role: "CAVALRY", initials: "PS", photo: PHOTO("sheridan"), flag: FL.us, side: "carth", corner: "bl", t: T_SHER - 0.1, until: T_DARK - 0.3 });
unitS("sh", "carth", G.SHERIDAN[0], "infantry", "SHERIDAN", { t: T_SHER - 0.3, size: "XX" }); cavIcon("sh", { flip: true });
along("sh", G.SHERIDAN, T_SHER + 0.2, 5.5, 20);
arw({ pts: G.SHERIDAN, side: "carth", t: T_SHER + 0.2, dur: 5.0, width: AW(2.35, 13), until: T_DARK + 0.6 });
unitS("hc", "rome", G.HAMPTON[0], "infantry", null, { t: T_LCAV - 0.2, size: "XX" }); cavIcon("hc", { flip: true });
along("hc", G.HAMPTON, T_LCAV + 0.2, 4.4, 18);
arw({ pts: G.HAMPTON, side: "rome", t: T_LCAV + 0.2, dur: 4.0, width: AW(2.35, 13), until: T_DARK + 0.6 });
hideU(["sh", "hc"], T_DARK + 0.4);
B.caption("LEE SENT HIS OWN CAVALRY AFTER IT", T_LCAV + 0.2, T_DARK - 0.2, "rome");
// ---------- after dark on the 12th: Warren crosses the Chickahominy and faces Richmond; the rest slips out south ----------
nightWash(T_DARK, null, 0.42, 1.6);
K.night({ lines: [FR], tOn: T_DARK });
const WB = badge({ name: "GOUVERNEUR WARREN", role: "FIFTH CORPS", initials: "GKW", photo: PHOTO("warren"), flag: FL.us, side: "carth", corner: "bl", t: T_WAR - 0.1, until: T_MEADE - 0.4 });
const CHG = glowPath(G.CHICK.slice(2, 9), "#7fb0ff", 1.3, T_CHICK - 0.2, T_CHICK + 4.0, 2, 0.9, { draw: 1.2 });
boxS("CHICKAHOMINY RIVER", G.CHICK[5][0] + 12, G.CHICK[5][1] - 14, T_CHICK, null, { size: 24, bg: "#dcecf8" });
along("v5", [[1468, 818], ...G.WARREN.slice(1)], T_CHICK - 0.3, 4.2, 18);
arw({ pts: G.WARREN.slice(0, 5), side: "carth", t: T_CHICK - 0.2, dur: 3.6, width: AW(4.6, 12), dash: "9 6", until: T_REST + 3 });
const WF = frontS({ pts: [[1452, 878], [1449, 890], [1451, 902]], sideA: "carth", sideB: "rome", t: T_FACED, dur: 1.2, width: FWw(4.6), until: END + 1 });
K.night({ lines: [WF], tOn: T_FACED });
unitS("rw", "rome", [1432, 889], "infantry", null, { t: T_FACED + 0.3, size: "XXX" });
arw({ pts: [[1460, 892], [1446, 890], [1436, 887]], side: "carth", t: T_FACED + 0.2, dur: 0.9, width: AW(4.6, 11), until: T_REST + 2.5 });
B.caption("FACED TOWARD RICHMOND", T_FACED + 0.1, T_REST - 0.2, "carth");
// the rest of the army slips out of the trenches and marches south by back roads (Cold Harbor line given up; the red line stays and watches)
[["u2", G.MARCH1], ["u6", G.MARCH2], ["u18", G.MARCH1.map((q) => [q[0] - 6, q[1] + 4])]].forEach(([id, pts], k) => along(id, [B.units[id] ? [BU[k][1][0], BU[k][1][1]] : pts[0], ...pts.slice(1)], T_REST + 0.2 + k * 0.6, 6.0, 22));
arw({ pts: G.MARCH1, side: "carth", t: T_SOUTH2 - 0.6, dur: 3.0, width: AW(4.3, 12), dash: "9 6", until: END + 1 });
arw({ pts: G.MARCH2, side: "carth", t: T_SOUTH2 - 0.2, dur: 3.0, width: AW(4.3, 12), dash: "9 6", until: END + 1 });
B.caption("MARCHED SOUTH BY BACK ROADS", T_SOUTH2, T_MEADE - 0.2, "carth");
const MB = badge({ name: "GEORGE G. MEADE", role: "ARMY OF THE POTOMAC", initials: "GGM", photo: PHOTO("meade"), flag: FL.us, side: "carth", corner: "bl", t: T_MEADE - 0.1, until: END + 1 });
pulseU("u2", T_LEAD); boxS("ARMY OF THE POTOMAC", 1528, 905, T_LEAD - 0.4, null, { size: 22 });
// ---------- clean screen: title card up -> legend + badges step out (the date scroll stays) ----------
declutter([LGD, GB, LB, LB2, SB, WB, MB], [[T_JAMES, T_JAMES + 2.6]]);
fixImgs();
K.raiseTerritory();
B.finish();
