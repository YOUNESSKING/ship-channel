// ending (end-1 + end-2), Grant #16. end-1: the three moves recapped on their own maps on the spoken words (`tennessee` Donelson Feb 1862 ->
// `mississippi` Vicksburg 1863 -> `richmond` the James June 1864), the nickname (his initials, 1862 -> 1865, "it described a method"),
// the three surrenders named only as spoken (Donelson garrison 1862, Pemberton's army 1863, Lee's army + APPOMATTOX 1865 on the words),
// then EACH TIME: the two method lines of the last sentence. end-2: E.final (One / Two / Three, 1, 2 OR 3?, family line, corner subscribe);
// the last ~20 s the card shrinks to a top band (dark backing lifts) so YouTube's end-screen elements fit over the living map (1b ending rules).
// 1c: every card/stamp text is a spoken word of its paragraph; one big card at a time, the legend steps out around each (declutter).
// Built with: python3 tools/m3_build.py ending tennessee end-1 end-2 mississippi richmond   (tennessee_hd_lift is the relief; the others ext_*.jpg)
// @@BODY
const G = GEO, P1 = "end-1", P2 = "end-2";
const T_DON = at(P1, "At Donelson"), T_STRUCK = at(P1, "he struck while"), T_VICK = at(P1, "At Vicksburg"), T_WENT = at(P1, "he went where the enemy said no"),
  T_LAND = at(P1, "lived off the land"), T_JAMES = at(P1, "On the James"), T_SLIP = at(P1, "he slipped a hundred thousand"), T_BREATH = at(P1, "no time to catch his breath"),
  T_NICK = at(P1, "The nickname the North"), T_INIT = at(P1, "a joke about his initials"), T_1865 = at(P1, "By eighteen sixty-five"),
  T_METH = at(P1, "it described a method"), T_SURR = at(P1, "Grant took the surrender"), T_SURW = at(P1, "the surrender"),
  T_DG = at(P1, "Donelson garrison"), T_D62 = at(P1, "eighteen sixty-two, of"), T_PEM = at(P1, "of Pemberton's army"), T_P63 = at(P1, "eighteen sixty-three, and"),
  T_LEE = at(P1, "of Lee's army"), T_APP = at(P1, "Appomattox in"), T_L65 = at(P1, "eighteen sixty-five. Each"),
  T_EACH = at(P1, "Each time"), T_MOVED = at(P1, "he moved before the enemy was ready"), T_COULD = at(P1, "and he went where the enemy said he could not go"),
  T_E1END = B.T.paras[P1][1];
const F_Q = at(P2, "So which was Grant's greatest move"), F_1 = at(P2, "One, the two river forts"), F_2 = at(P2, "Two, Vicksburg"), F_3 = at(P2, "Or three, the crossing"),
  F_TELL = at(P2, "Tell us in the comments"), F_FAM = at(P2, "And if someone in your family"), F_SUB = at(P2, "Subscribe, so you");
const T_X1 = T_DON - 0.9, T_X2 = T_VICK - 0.6, T_X3 = T_JAMES - 0.5;        // map dissolves (each lands on the spoken place)
// ---------- maps: tennessee relief (Feb 1862 layer) -> mississippi (July 1863) -> richmond (June 1864) ----------
const FL34 = "assets/media/us34_flag.png";
terr("assets/media/m1_ten_feb16_mx.png", 0, T_X2 + 0.2, 1.0, 0.9);
extImg("assets/ext_mississippi.jpg", T_X2, T_X3 + 1.0, { dur: 0.9, outDur: 0.01 });
extImg("assets/ext_richmond.jpg", T_X3, null, { dur: 0.9 });
terr("assets/media/m3_mis_jul_mx.png", T_X2, T_X3 + 0.9, 0.9, 0.9);
terr("assets/media/m3_ric_jun18_mx.png", T_X3, T_EACH + 0.4, 0.9, 2.8);   // owner 2026-11-02: colours only on the recap maps; dissolve (~2.8 s) before the final question (option 2)
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); LV.north();
const R = G.ric, AP = R.APPOMATTOX;
const KEYS = [[0, 1440, 905, 1.7], [T_X1 + 0.6, 1440, 900, 2.1], [T_X2 - 0.1, 1440, 905, 2.25], [T_X2 + 0.6, 1440, 990, 1.75], [T_X3 - 0.1, 1420, 980, 1.95],
  [T_X3 + 0.8, 1470, 905, 3.4], [T_NICK, 1470, 900, 3.6], [T_SURR, 1430, 905, 3.0], [T_LEE - 0.4, 1330, 900, 2.3], [T_APP + 0.3, 1200, 890, 2.05],
  [T_EACH, 1220, 890, 2.0], [F_Q, 1250, 885, 1.9], [END, 1260, 885, 1.85]];
camera(KEYS);
dateNow("JUNE 1864 – APRIL 1865", T_DON - 0.1); B.date("FEBRUARY 1862", T_DON, T_VICK - 0.1, 34); B.date("1863", T_VICK, T_JAMES - 0.1, 34); B.date("JUNE 1864", T_JAMES, T_1865 - 0.1, 34);
B.date("1865", T_1865, null, 34);
const LGD = now(legend(0, END + 1, false));
// ---------- 1: Donelson (tennessee map) ----------
flagS(FL34, 1430, 800, 0, T_X2 + 0.6, 100); flagS(FL.cs, 1500, 1030, 0, T_X2 + 0.6, 100);
const TEN_S = [[1390, 890], [1400, 1000], [1420, 1100], [1400, 1200]], CUMB = [[1456, 900], [1500, 920], [1560, 940], [1637, 888], [1700, 970], [1760, 1020], [1848, 1054]];
glowPath(TEN_S, "#6f9bff", 2.6, 0, T_X2 + 0.6, 2, 0.8); glowPath(CUMB, "#6f9bff", 2.6, 0, T_X2 + 0.6, 2, 0.8);
const GT = ship("iron", "carth", [1460, 905], 20, 0, T_X2 + 0.6, { L: 40 }); sail(GT, CUMB, 0, T_X2, 20);
[G.ten.FORT_HENRY, G.ten.FORT_DONELSON].forEach((p) => { fortIcon(p, 0, T_X2 + 0.6, { s: 18, col: "#4f8bff" }); });
poleFlag(FL34, [G.ten.FORT_DONELSON[0] + 3, G.ten.FORT_DONELSON[1] - 6], T_DON, T_X2 + 0.6, 30);
boxS("DONELSON", G.ten.FORT_DONELSON[0] + 30, G.ten.FORT_DONELSON[1] + 34, T_DON, null, { size: 28 });
K.target(G.ten.FORT_DONELSON[0], G.ten.FORT_DONELSON[1], T_DON + 0.1, { r: 30, side: "#ffd54a", until: T_X2 });
B.caption("HE STRUCK WHILE THE ENEMY WAS STILL DECIDING", T_STRUCK, T_VICK - 0.2, "carth");
// ---------- 2: Vicksburg (mississippi map) ----------
flagS(FL.us, 1392, 885, T_X2 + 0.4, T_X3 + 0.8, 100); flagS(FL.cs, 1600, 1010, T_X2 + 0.4, T_X3 + 0.8, 100);
const VK = G.mis.VICKSBURG;
boxS("VICKSBURG", VK[0] + 40, VK[1] - 40, T_VICK, null, { size: 28 });
K.target(VK[0], VK[1], T_VICK + 0.1, { r: 30, side: "#ffd54a", until: T_WENT });
arw({ pts: G.mis.VKS, side: "carth", t: T_WENT - 0.2, dur: 3.2, width: AW(1.9, 13), until: T_X3 - 0.3 });
unitS("va", "carth", G.mis.VKS[0], "infantry", null, { t: T_X2 + 0.3, size: "XXXX" });
unitS("vr", "rome", [VK[0] + 10, VK[1] + 4], "infantry", null, { t: T_X2 + 0.4, size: "XXX" });
along("va", G.mis.VKS, T_WENT - 0.1, 5.6, 24); hideU(["va", "vr"], T_X3 - 0.3);
B.caption("WHERE THE ENEMY SAID NO ARMY COULD GO", T_WENT + 0.2, T_LAND - 0.2, "carth");
B.caption("AND LIVED OFF THE LAND TO DO IT", T_LAND, T_JAMES - 0.2, "carth");
// ---------- 3: the James (richmond map) ----------
flagS(FL.us, 1590, 960, T_X3 + 0.5, T_LEE - 0.3, 100); flagS(FL.cs, 1350, 820, T_X3 + 0.5, T_LEE - 0.3, 100);
arw({ pts: R.MOVE, side: "carth", t: T_JAMES - 0.1, dur: 2.6, width: AW(3.4, 13), dash: "9 6", until: END + 1 });
glowPath([R.WEYANOKE, [R.WEYANOKE[0] - 1, R.WEYANOKE[1] + 5]], "#6f9bff", 2.0, T_JAMES + 0.8, END + 1, 3, 0.95, { top: true });
boxS("THE JAMES", R.WEYANOKE[0] + 14, R.WEYANOKE[1] + 14, T_JAMES, null, { size: 28, bg: "#dcecf8" });
frontS({ pts: R.CH_FRONT, sideA: "carth", sideB: "rome", t: T_X3 + 0.4, dur: 0.6, width: FWw(3.4), until: T_SLIP + 2.0 });
frontS({ pts: [[1440, 948], [1437, 962], [1430, 975], [1420, 985]], sideA: "carth", sideB: "rome", t: T_SLIP + 1.2, dur: 1.5, width: FWw(3.6), until: END + 1 });
B.caption("A HUNDRED THOUSAND MEN AWAY FROM A STALEMATE", T_SLIP + 0.2, T_BREATH - 0.2, "carth");
B.caption("NO TIME TO CATCH HIS BREATH", T_BREATH, T_NICK - 0.2, "rome");
// ---------- the nickname: his initials, 1862 -> 1865 "it described a method" (one card, spoken words) ----------
const NK = scr(`<div style="padding:16px 46px 18px;background:rgba(18,16,12,0.93);border-top:6px solid #c9b48a;font-family:Oswald;font-weight:700;color:#f7f3ea;text-align:center;box-shadow:0 20px 40px rgba(0,0,0,.55)">
  <div style="font-size:84px;letter-spacing:.08em"><span class="i1">U.</span> <span class="i2">S.</span> GRANT</div>
  <div style="position:relative;height:34px;min-width:640px;white-space:nowrap;font-size:26px;letter-spacing:.3em;color:#c9b48a"><span class="y62" style="position:absolute;left:0;right:0">1862</span><span class="y65" style="position:absolute;left:0;right:0;opacity:0">1865 · IT DESCRIBED A METHOD</span></div></div>`,
  "left:0;right:0;top:250px;display:flex;justify-content:center;", T_NICK + 0.2, T_SURR - 0.2, { autoAlpha: 0, y: 20 });
SFX("hit", T_NICK + 0.4);
tl.to([NK.querySelector(".i1"), NK.querySelector(".i2")], { color: "#ffd54a", textShadow: "0 0 18px rgba(255,213,74,.8)", duration: 0.4 }, T_INIT);
SFX("ref:pop", T_INIT);
tl.to(NK.querySelector(".y62"), { opacity: 0, y: -12, duration: 0.3 }, T_1865 + 0.1);
const Y65 = NK.querySelector(".y65"); Y65.innerHTML = `<span class="a">1865</span><span class="b" style="opacity:0"> · IT DESCRIBED A METHOD</span>`;
tl.fromTo(Y65, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: false }, T_1865 + 0.2);
tl.to(Y65.querySelector(".b"), { opacity: 1, color: "#ffd54a", duration: 0.35 }, T_METH); SFX("ref:boom", T_METH + 0.1);
// ---------- the three surrenders, each named only as it is spoken ----------
const row = (cls, name) => `<div class="${cls}" style="display:flex;justify-content:space-between;gap:30px;padding:8px 6px;border-top:1px solid rgba(201,180,138,.35);opacity:0"><span>${name}</span><span class="y" style="color:#c9b48a;opacity:0"></span></div>`;
const SC = scr(`<div style="width:900px;padding:16px 40px 18px;background:rgba(18,16,12,0.92);border-top:6px solid #4f8bff;font-family:Oswald;font-weight:700;color:#f7f3ea;box-shadow:0 20px 40px rgba(0,0,0,.55)">
  <div style="font-size:30px;letter-spacing:.4em;color:#c9b48a;text-align:center;margin-bottom:6px">THE SURRENDER</div>
  <div style="font-size:44px;letter-spacing:.05em">${row("r1", "THE DONELSON GARRISON")}${row("r2", "PEMBERTON'S ARMY · VICKSBURG")}${row("r3", "LEE'S ARMY")}</div></div>`,
  "left:0;right:0;top:250px;display:flex;justify-content:center;", T_SURW, T_EACH - 0.2, { autoAlpha: 0, y: 20 });
[[".r1", T_DG, T_D62, "1862"], [".r2", T_PEM, T_P63, "1863"], [".r3", T_LEE, T_L65, "1865"]].forEach(([c, tn, ty, yr]) => {
  const r = SC.querySelector(c), y = r.querySelector(".y"); y.textContent = yr;
  tl.fromTo(r, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.4, immediateRender: false }, tn + 0.1); SFX("hit", tn + 0.1);
  tl.to(y, { opacity: 1, duration: 0.3 }, ty); });
const R3 = SC.querySelector(".r3 span"); const AT = document.createElement("span"); AT.textContent = " AT APPOMATTOX"; AT.style.opacity = 0; R3.appendChild(AT);
tl.to(AT, { opacity: 1, duration: 0.3 }, T_APP);
// Appomattox on the map, only on its spoken word (the card stays up; the place stamp + 1865 sit on the map, left of the card)
boxS("APPOMATTOX", AP[0] + 10, AP[1] + 40, T_APP, null, { size: 30 }); wstampS("1865", AP[0] + 10, AP[1] + 78, T_L65, null, "#9fc0ea", 30);
K.target(AP[0], AP[1], T_APP + 0.1, { r: 26, side: "#ffd54a", until: T_APP + 3.0 });
flagS(FL.us, 1100, 1010, T_LEE - 0.3, END + 1, 100); flagS(FL.cs, 1010, 790, T_LEE - 0.3, END + 1, 100);
// ---------- each time: the method, in the last sentence's own words ----------
GG.METHOD_TITLE = "EACH TIME";
GG.METHOD = ["HE MOVED BEFORE THE ENEMY WAS READY", "HE WENT WHERE THE ENEMY SAID HE COULD NOT GO"];
const MC = GG.method(2, T_EACH, T_E1END + 0.4, [T_MOVED, T_COULD]); MC.querySelectorAll(".row").forEach((r) => { r.style.fontSize = "46px"; });
SFX("ref:pop", T_MOVED); SFX("ref:pop", T_COULD);
const WIN = [[T_NICK + 0.2, T_SURR - 0.2], [T_SURW, T_EACH - 0.2], [T_EACH, T_E1END + 0.4]];
// ---------- end-2: the final question ----------
const E = EngageK(B);
const FC = E.final({ moves: [["THE TWO RIVER FORTS", "FEB 1862"], ["VICKSBURG", "1863"], ["THE JAMES", "JUNE 1864"]], tShow: F_Q, tNums: [F_1, F_2, F_3], tAsk: F_TELL,
  tFamily: F_FAM, tSub: F_SUB, until: END + 1 });
FC.querySelector(".fam").innerHTML = `SOMEONE IN YOUR FAMILY SERVED IN THE CIVIL WAR? <span style="color:#c9b48a">TELL US THEIR STORY · WE READ EVERY ONE</span>`;
// end screen: the last ~20 s the card shrinks to a top band and the dark backing lifts, the map alive under it
const tBand = Math.max(F_TELL + 1.2, END - 20);
tl.to(FC, { scale: 0.5, y: -125, duration: 0.8, ease: "power2.inOut", transformOrigin: "50% 0%" }, tBand);
const back = FC.previousElementSibling; if (back) tl.to(back, { autoAlpha: 0.12, duration: 0.8 }, tBand);
WIN.push([F_Q, END + 1]);
// ---------- clean screen ----------
declutter([LGD], WIN);
fixImgs();
K.raiseTerritory();
B.finish();
