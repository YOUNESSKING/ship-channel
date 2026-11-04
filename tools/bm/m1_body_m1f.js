// m1f (m1-9 + move1-sub), Grant #16: zoom out from the two fallen forts over the theatre (tennessee map, option 1 subtle, fading in on the pull-out): the two rivers glow
// blue and the gunboats steam far into Tennessee; the Kentucky line collapses (E2: the lost ground turns pale first, then blue);
// method card line 1 on "attacked the moment the enemy hesitated". move1-sub: woven subscribe (E.subscribe on the subscribing clause),
// a dark-to-bluff transition on the question (a fortress on a high bluff, the supply river under its guns; no place name: it is not spoken),
// NEXT: MOVE 2.  Basemap tennessee_hd_lift (z9, v11). Built with: python3 tools/m1_build.py m1f tennessee_hd_lift m1-9 move1-sub
// @@BODY
const P9 = "m1-9", PS = "move1-sub";
const T_TWO = at(P9, "Two river forts had fallen"), T_TEN = at(P9, "in ten days"), T_GONE = at(P9, "Grant had gone from"), T_SNUB = at(P9, "a snubbed brigadier"),
  T_TALK = at(P9, "the man the whole North"), T_BOATS = at(P9, "The Union gunboats could now"), T_INTO = at(P9, "far into Tennessee"),
  T_FALL = at(P9, "The Confederates had to fall back"), T_KY = at(P9, "from Kentucky"), T_MIDT = at(P9, "much of middle Tennessee"),
  T_WAIT = at(P9, "Grant had not won by waiting"), T_FAST = at(P9, "He moved fast"), T_HIT2 = at(P9, "hit the second fort"), T_ATT = at(P9, "attacked the moment");
const T_ONLY = at(PS, "Donelson was only the beginning"), T_HOW = at(PS, "So how do you take a fortress"), T_BLUFF = at(PS, "built on a high bluff"),
  T_RIVER = at(PS, "the river that carries your supplies"), T_GUNS = at(PS, "runs right under its guns"), T_KIND = at(PS, "That's the kind of question"),
  T_SUBS = at(PS, "and subscribing is how"), T_HERE = at(PS, "Here's how Grant did it");
// ---------- places (tennessee map px, tools/m1_proj.py) ----------
const FH = [1393, 895], FD = [1456, 904], CLK = [1637, 888], NSH = [1848, 1054], BG = [1957, 689], COL = [1002, 783], PAD = [1186, 636], CAI = [976, 672];
const TENN_S = [[1190, 640], [1300, 700], [1360, 800], [1390, 890], [1400, 1000], [1420, 1100], [1400, 1200], [1360, 1400], [1320, 1560], [1330, 1620]];
const CUMB_E = [[1257, 611], [1360, 650], [1400, 750], [1440, 830], [1456, 900], [1500, 920], [1560, 940], [1637, 888], [1700, 970], [1760, 1020], [1848, 1054]];
// ---------- map: option 1 (16 Feb -> March 1862, E2 pale-first). Owner 2026-11-02 (territory minimised): the (subtle) colours only on
// this wide overview: they fade in (~2.2 s) as the camera pulls out over the theatre (m1e ends on the close-up without tint) ----------
const T_TIN = T_BOATS - 0.4;
const TA = terr("assets/media/m1_ten_feb16_mx.png", T_TIN, null, 2.2);
tl.to(TA, { opacity: 0.4 * TERR_A, duration: 1.3, ease: "sine.inOut" }, T_FALL);
terr("assets/media/m1_ten_mar_mx.png", T_KY + 0.6, null, 1.0, 2.2); tl.to(TA, { autoAlpha: 0, duration: 1.0 }, T_KY + 0.8);
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.14 }); LV.shimmer([TENN_S, CUMB_E], { width: 2.0 }); LV.scaleBar(245.14); LV.north();
const LGD2 = now(legend(0, T_TIN + 1.2, true)), LGD = legend(T_TIN + 1.4, T_HOW + 0.4, false);
camera([[0, 1430, 900, 2.1], [T_TEN + 0.6, 1440, 905, 1.9], [T_TALK, 1500, 930, 1.6], [T_INTO + 0.6, 1520, 1000, 1.05], [T_KY + 0.8, 1470, 920, 0.85],
  [T_MIDT + 1.2, 1460, 940, 0.82], [T_ONLY, 1400, 960, 0.9], [T_HOW + 2.5, 1000, 1250, 1.25], [END, 980, 1270, 1.3]]);
dateNow("16 FEBRUARY 1862", T_FALL - 0.1); B.date("FEBRUARY–MARCH 1862", T_FALL, null, 30);
// ---------- flags ----------
flagS(FL.us, 1430, 800, 0, T_TALK + 0.5, 84); flagS(FL.cs, 1470, 1020, 0, T_TALK + 0.5, 84);
flagS(FL.us, 1500, 560, T_TALK + 0.3, END + 1, 110); flagS(FL.cs, 1280, 1360, T_TALK + 0.4, T_HOW + 1.8, 110);
flagS(FL.cs, 820, 1400, T_HOW + 1.6, END + 1, 110);
// ---------- the two forts, both Union now ----------
[FH, FD].forEach((p, k) => { fortIcon(p, 0, null, { s: 20, col: "#4f8bff" }); poleFlag(FL.us, [p[0] + 3, p[1] - 6], 0, null, 30); });
B.caption("TWO RIVER FORTS · TEN DAYS", T_TWO + 0.2, T_GONE - 0.1, "carth");
const GB = badge({ name: "ULYSSES S. GRANT", role: "FROM A SNUBBED BRIGADIER", initials: "USG", photo: PHOTO("grant"), flag: FL.us, side: "carth", corner: "bl", t: T_SNUB - 0.3, until: T_WAIT - 0.3 });
B.caption("THE MAN THE WHOLE NORTH WAS TALKING ABOUT", T_TALK, T_BOATS - 0.1, "carth r");
// ---------- the rivers open: the gunboats steam far into Tennessee ----------
glowPath(TENN_S.slice(3), "#6f9bff", 5, T_BOATS - 0.1, END + 1, 3, 0.85, { draw: 2.4 });
glowPath(CUMB_E.slice(4), "#6f9bff", 5, T_BOATS + 0.2, END + 1, 3, 0.85, { draw: 2.4 });
const GT = ship("iron", "carth", [1392, 920], 90, T_BOATS, T_HOW + 1.0, { L: 46 }); sail(GT, TENN_S.slice(3, 9), T_BOATS + 0.2, 9.0, 20);
const GC = ship("iron", "carth", [1470, 912], 20, T_BOATS + 0.3, T_HOW + 1.0, { L: 46 }); sail(GC, CUMB_E.slice(4), T_BOATS + 0.5, 8.0, 20);
boxS("TENNESSEE RIVER", 1520, 1250, T_BOATS + 0.4, null, { size: 24, bg: "#dcecf8", sfx: false });
// ---------- the Kentucky line collapses ----------
const KYL = glowPath([COL, [1200, 840], FH, FD, [1700, 830], BG], "#ff6a5a", 4, T_FALL - 0.4, T_KY + 1.2, 1, 0.9, { dash: "10 7" });
gsap.set(town("KENTUCKY", [1640, 560], T_KY, "r", { size: 34 }).el.querySelector(".dt"), { autoAlpha: 0 });
gsap.set(town("TENNESSEE", [1700, 1250], T_MIDT, "r", { size: 34 }).el.querySelector(".dt"), { autoAlpha: 0 });
[[BG, [1880, 900], [1840, 1060], [1880, 1300]], [COL, [990, 900], [960, 1050]], [[1840, 1060], [1860, 1220], [1900, 1380]]].forEach((pts, k) =>
  arw({ pts, side: "rome", t: T_FALL + 0.2 + k * 0.5, dur: 2.2, width: AW(0.85, 14), until: T_WAIT + 1.5 }));
[["r1", BG, [1880, 1330]], ["r2", COL, [960, 1060]]].forEach(([id, a, b], k) => { unitS(id, "rome", a, "infantry", null, { t: 0, size: "XXX" }); B.move(id, T_FALL + 0.4 + k * 0.5, 4.0, b[0], b[1]); });
B.caption("THE CONFEDERATES FALL BACK", T_FALL + 0.2, T_WAIT - 0.1, "rome r");
// ---------- method card: line 1 lit on "attacked the moment the enemy hesitated" ----------
GG.METHOD_TITLE = "GRANT'S METHOD";
GG.METHOD = ["HE MOVED FAST", "HIT THE SECOND FORT BEFORE HELP COULD COME", "ATTACKED THE MOMENT THE ENEMY HESITATED"];   // spoken words only (m1-9)
const MC = GG.method(3, T_FAST - 0.1, T_ONLY + 1.4, [T_FAST, T_HIT2, T_ATT]); MC.querySelectorAll(".row").forEach((r) => { r.style.fontSize = "50px"; });
SFX("ref:pop", T_FAST + 0.1); SFX("ref:pop", T_HIT2 + 0.1); SFX("ref:boom", T_ATT + 0.2);
// ---------- move1-sub: only the beginning; the question (dark-to-bluff transition); subscribe; NEXT ----------
B.caption("DONELSON WAS ONLY THE BEGINNING", T_ONLY + 1.5, T_HOW - 0.1, "carth");
const DK = document.createElement("div"); DK.style.cssText = "position:absolute;inset:0;background:radial-gradient(ellipse at 50% 55%, rgba(8,10,16,0.94) 0%, rgba(4,6,10,0.98) 75%);pointer-events:none";
document.getElementById("fx").appendChild(DK); gsap.set(DK, { autoAlpha: 0 }); tl.to(DK, { autoAlpha: 1, duration: 1.6, ease: "sine.inOut" }, T_HOW - 0.2);
// the bluff scene (screen space): a river bending under a high bluff, guns on the crest, a supply steamer under them
const RIV = "M -40 250 C 400 300 700 200 860 420 C 1000 610 760 760 900 900 C 1000 1000 1300 980 1960 1040";
const BLF = "M 820 160 C 980 300 1100 420 1060 600 C 1030 720 980 800 1060 880 C 1140 950 1300 930 1500 960";
const BS = scr(`<svg width="1920" height="1080" viewBox="0 0 1920 1080" style="display:block">
  <defs><filter id="bfg" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9"/></filter></defs>
  <path d="${RIV}" fill="none" stroke="#2c3a48" stroke-width="120" stroke-linecap="round"/><path d="${RIV}" fill="none" stroke="#4a6378" stroke-width="96" stroke-linecap="round"/>
  <path class="rsh" d="${RIV}" fill="none" stroke="rgba(220,238,255,.45)" stroke-width="3" stroke-dasharray="14 60"/>
  <path d="M 900 120 C 1080 280 1190 420 1150 600 C 1120 730 1080 800 1150 860 C 1240 920 1400 900 1960 900 L 1960 120 Z" fill="#3a352a"/>
  <path class="bg" d="${BLF}" fill="none" stroke="#ff6a5a" stroke-width="16" stroke-linecap="round" filter="url(#bfg)" opacity="0"/>
  <path class="bl" d="${BLF}" fill="none" stroke="#e8d9b8" stroke-width="5" stroke-linecap="round" opacity="0"/>
  <g class="guns">${[[930, 270], [1040, 400], [1075, 560], [1020, 760], [1110, 905]].map(([x, y]) => `<g transform="translate(${x} ${y})"><rect x="-16" y="-9" width="32" height="18" fill="#c4121f" stroke="#f7f3ea" stroke-width="2.5"/><circle class="fl" cx="-24" cy="0" r="14" fill="#ffd27a" opacity="0"/></g>`).join("")}</g>
  </svg>`, "left:0;top:0;width:1920px;height:1080px;", T_HOW + 0.4, END + 1, { autoAlpha: 0 });
tl.to(BS.querySelector(".rsh"), { strokeDashoffset: -300, duration: 12, ease: "none" }, T_HOW + 0.4);
gsap.set(BS.querySelector(".guns"), { autoAlpha: 0 });
tl.to([BS.querySelector(".bg"), BS.querySelector(".bl")], { opacity: 1, duration: 0.8 }, T_BLUFF - 0.1);
tl.to(BS.querySelector(".bg"), { opacity: 0.4, duration: 0.6, yoyo: true, repeat: 5, ease: "sine.inOut" }, T_BLUFF + 0.8);
const FLB = flag(FL.cs, 0, 0, null, null, 92); SCN.insertBefore(FLB, document.getElementById("credit")); FLB.classList.remove("gg-pin");
Object.assign(FLB.style, { position: "absolute", left: "1360px", top: "330px" }); gsap.set(FLB, { autoAlpha: 0, xPercent: 0, yPercent: 0 }); tl.to(FLB, { autoAlpha: 1, duration: 0.5 }, T_BLUFF);
const FLU = flag(FL.us, 0, 0, null, null, 92); SCN.insertBefore(FLU, document.getElementById("credit")); FLU.classList.remove("gg-pin");
Object.assign(FLU.style, { position: "absolute", left: "300px", top: "560px" }); gsap.set(FLU, { autoAlpha: 0, xPercent: 0, yPercent: 0 }); tl.to(FLU, { autoAlpha: 1, duration: 0.5 }, T_RIVER);
B.caption("A FORTRESS ON A HIGH BLUFF", T_BLUFF, T_RIVER - 0.1, "rome");
// the supply steamer (blue) comes down the river, right under the guns
const SUP = document.createElement("div"); SUP.style.cssText = "position:absolute;left:0;top:0;width:0;height:0"; SUP.innerHTML = `<div style="position:absolute;left:-55px;top:-19px;width:110px">${shipSVG("steamer", "carth", 110)}</div>`;
SCN.insertBefore(SUP, document.getElementById("credit")); gsap.set(SUP, { autoAlpha: 0 });
const RP = [[-60, 252], [300, 285], [600, 260], [800, 360], [880, 520], [820, 700], [880, 880], [1050, 990], [1300, 1010]];
tl.set(SUP, { autoAlpha: 1, left: RP[0][0], top: RP[0][1] }, T_RIVER - 0.2);
for (let k = 1; k <= 24; k++) { const a = posOn(RP, (k - 1) / 24), b = posOn(RP, k / 24), tt = T_RIVER - 0.2 + (k - 1) * 0.3;
  tl.to(SUP, { left: b[0], top: b[1], duration: 0.3, ease: "none" }, tt); tl.to(SUP.firstElementChild, { rotation: Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI, duration: 0.3, ease: "none" }, tt); }
tl.to(SUP, { autoAlpha: 0, duration: 0.6 }, END - 0.4);
B.caption("THE RIVER THAT CARRIES YOUR SUPPLIES", T_RIVER, T_GUNS - 0.1, "carth");
tl.to(BS.querySelector(".guns"), { autoAlpha: 1, duration: 0.4 }, T_GUNS - 0.3);
[...BS.querySelectorAll(".fl")].forEach((f, k) => { [0, 1.6, 3.2].forEach((d) => { const t = T_GUNS + 0.2 + k * 0.28 + d;
  tl.fromTo(f, { opacity: 1, scale: 0.4 }, { opacity: 0, scale: 1.6, duration: 0.35, immediateRender: false, transformOrigin: "50% 50%" }, t); if (d === 0) SFX("fire", t); }); });
B.caption("RIGHT UNDER ITS GUNS", T_GUNS, T_KIND - 0.1, "rome");
// woven subscribe: small button bottom-right, cursor click, bell; never a full-screen card
const E = EngageK(B); E.subscribe(T_SUBS - 1.0, T_HERE + 0.2);
scr(`<div style="padding:10px 26px 12px;background:#dcecf8;color:#111;font-family:Oswald;font-weight:500;letter-spacing:.2em;font-size:34px;box-shadow:0 6px 20px rgba(0,0,0,.6)">NEXT: MOVE 2 →</div>`, "right:80px;bottom:150px;", T_HERE + 0.3, END + 1);
SFX("ref:pop", T_HERE + 0.3);
// ---------- clean screen ----------
declutter([LGD2, LGD, GB], [[T_FAST - 0.1, T_ONLY + 1.4]]);
fixImgs();
K.raiseTerritory();
B.finish();
