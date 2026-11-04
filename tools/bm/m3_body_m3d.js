// m3d (m3-6..m3-7), Grant #16: 16-18 Jun at Petersburg (option 1, 18 JUN): Smith's men and Hancock's corps ready to renew the attack, Lee's
// veterans hurry south over the James into the new line; the assaults bounce; THE UNION LOST ABOUT 11,400 MEN IN FOUR DAYS; the trenches freeze;
// Grant years later: Petersburg could have been easily captured (indirect speech in the script -> no quote marks).
// m3-7: ONE continuous zoom-out from `petersburg` onto the `richmond` overview (both maps driven by the same camera at true position and scale,
// the petersburg map feathered and cross-faded out): the army's whole move from Cold Harbor over the James (the pontoon bridge glows),
// the siege lines grow from Richmond to south of Petersburg, MORE THAN NINE MONTHS; method card lit on the spoken words of m3-7.
// Basemap petersburg_hd_lift + richmond_hd_lift (previews m3x_pet / m3x_ric until baked).
// Built with: python3 tools/m3_build.py m3d petersburg m3-6 m3-7 richmond
// @@BODY
const P6 = "m3-6", P7 = "m3-7", G = GEO.pet, BOX = GEO.box_ric_in_pet;
const T_SMITH = at(P6, "By the time Smith's men"), T_HAN = at(P6, "Hancock's corps"), T_VET = at(P6, "Lee's veterans were arriving"), T_18 = at(P6, "By the eighteenth"),
  T_LOST = at(P6, "eleven thousand four hundred"), T_FOUR = at(P6, "four days of assaults"), T_GONE = at(P6, "the chance was gone"), T_WROTE = at(P6, "Grant wrote years later"),
  T_EASY = at(P6, "easily captured");
const T_EVEN = at(P7, "Even so"), T_CHG = at(P7, "the move changed the war"), T_ACROSS = at(P7, "was across the James"), T_PIN = at(P7, "pinned in a siege"),
  T_NINE = at(P7, "more than nine months"), T_ABAN = at(P7, "abandon both Petersburg and Richmond"), T_STALE = at(P7, "out of a stalemate"), T_RIVER = at(P7, "over a river"),
  T_INIT = at(P7, "the initiative again"), T_ASK = at(P7, "He had stopped asking"), T_FOLLOW = at(P7, "where Lee could not follow");
// ---------- camera over BOTH maps (petersburg world px; the richmond map sits at its true place and scale, 8x) ----------
const camera2 = (keys) => {
  const cam = { cx: keys[0][1], cy: keys[0][2], s: keys[0][3] }, cl = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
  const apply = () => { const L = BOX[0], T = BOX[1], R = BOX[0] + BOX[2], Bt = BOX[1] + BOX[3], s = Math.max(cam.s, 1920 / (R - L));
    const cx = cl(cam.cx, L + 960 / s, R - 960 / s), cy = cl(cam.cy, T + 540 / s, Bt - 540 / s);
    gsap.set(WORLD, { x: 960 - cx * s, y: 540 - cy * s, scale: s }); CAM_S = s; setInv(); };
  apply();
  for (let i = 1; i < keys.length; i++) { const [t0] = keys[i - 1], [t1, cx, cy, s] = keys[i];
    tl.to(cam, { cx, cy, s, duration: Math.max(t1 - t0, 0.01), ease: keys[i][4] || "sine.inOut", onUpdate: apply }, t0); }
  tl.call(apply, null, 0); };
// ---------- maps: richmond (under) + its 18 JUN territory; petersburg relief + 18 JUN territory on top, feathered out on the zoom ----------
extImg("assets/ext_richmond.jpg", 0, null, { box: BOX, under: true });
extImg("assets/media/m3_ric_jun18_mx.png", 0, null, { box: BOX, under: true, mx: true });
const REL = document.getElementById("relief");
const T_Z0 = T_CHG - 0.4, T_Z1 = T_PIN + 1.0;
// owner 2026-11-02: the 16-18 June close-up is option 2 (fronts only); the 18 JUN colours fade in (~2.2 s) only as the final zoom-out begins
const PT = terr("assets/media/m3_pet_jun18_mx.png", T_EVEN, null, 2.2);
tl.set(REL, { webkitMaskImage: "radial-gradient(ellipse 62% 62% at 50% 50%, #000 70%, transparent 100%)", maskImage: "radial-gradient(ellipse 62% 62% at 50% 50%, #000 70%, transparent 100%)" }, T_Z0);
tl.to([REL, PT], { opacity: 0, duration: 2.6, ease: "sine.inOut" }, T_Z0 + 1.2);
const LV = LivingK(B); LV.clouds({ n: 5, opacity: 0.12 }); LV.shimmer([G.APPOM, G.JAMES], { width: 1.2 }); LV.north();
camera2([[0, 1480, 835, 2.2], [T_VET - 0.6, 1470, 700, 1.6], [T_VET + 1.0, 1440, 560, 1.15], [T_18 + 0.4, 1470, 850, 2.1], [T_GONE, 1460, 850, 2.0], [T_WROTE + 1.0, 1440, 850, 1.75],
  [T_EVEN, 1480, 760, 1.5], [T_Z0 + 0.6, 1500, 700, 1.3], [T_Z1 + 1.4, 1760, 230, 0.55, "power2.inOut"], [T_ABAN + 1.0, 1700, 260, 0.56], [END, 1720, 250, 0.53]]);
SFX("whoosh", T_Z0 + 0.8);
dateNow("15 JUNE 1864", T_18 - 0.1); B.date("18 JUNE 1864", T_18, T_PIN, 34); B.date("JUNE 1864 – APRIL 1865", T_PIN + 0.1, null, 30);
const LGD = now(legend(0, END + 1, false));
// ---------- flags (both on every frame, re-placed for the overview) ----------
flagS(FL.us, 1690, 905, 0, T_Z1 - 1.0, 100); flagS(FL.cs, 1270, 720, 0, T_Z1 - 1.0, 100);
flagS(FL.us, 2200, 1000, T_Z1 - 1.2, END + 1, 110); flagS(FL.cs, 600, 900, T_Z1 - 1.2, END + 1, 110);
// ---------- 16-18 June: Smith's men and Hancock's corps; Lee's veterans arrive; the assaults fail ----------
const NL = G.NEWLINE;
const FR = frontS({ pts: NL, sideA: "carth", sideB: "rome", t: 0, dur: 0.01, width: FWw(2.1), until: T_Z0 + 1.0 });
[["s1", [1500, 785]], ["s2", [1497, 835]]].forEach(([id, p]) => unitS(id, "carth", p, "infantry", null, { t: 0, size: "XXX" }));
unitS("h2", "carth", [1660, 900], "infantry", "HANCOCK", { t: T_HAN - 0.2, size: "XXX" }); B.move("h2", T_HAN, 3.2, 1488, 900);
const HB = badge({ name: "WINFIELD S. HANCOCK", role: "", initials: "WSH", photo: PHOTO("hancock"), flag: FL.us, side: "carth", corner: "bl", t: T_HAN - 0.1, until: T_LOST - 0.4 });
unitS("pr", "rome", [1445, 820], "infantry", null, { t: 0, size: "X" });
const VET = [["v1", [1455, 770]], ["v2", [1450, 830]], ["v3", [1440, 890]], ["v4", [1425, 950]]];
VET.forEach(([id, p], k) => { unitS(id, "rome", G.LEE_S[0], "infantry", null, { t: T_VET - 0.3 + k * 0.4, size: "XXX" });
  along(id, [...G.LEE_S, p], T_VET - 0.2 + k * 0.4, 5.0, 22); });
[0, 1].forEach((k) => arw({ pts: G.LEE_S.map((q) => [q[0] + (k ? 26 : -20), q[1]]), side: "rome", t: T_VET - 0.2 + k * 0.5, dur: 2.6, width: AW(1.6, 14), until: T_GONE }));
B.caption("LEE'S VETERANS WERE ARRIVING", T_VET + 0.1, T_18 - 0.1, "rome");
// the assaults of the 16th-18th bounce off the line (visible guns, impacts)
[[1560, 790], [1560, 850], [1550, 910]].forEach((p, k) => { const t = T_18 + 0.4 + k * 1.1;
  const a = arw({ pts: [p, [p[0] - 50, p[1] + 2], [p[0] - 78, p[1] + 4]], side: "carth", t, dur: 0.8, width: AW(2.1, 13), until: t + 1.6 }); });
shoot([1452, 790], [1490, 792], T_18 + 0.9, { r: 4, width: 0.6, dur: 0.5, h: 6 });
shoot([1446, 860], [1484, 866], T_18 + 2.0, { r: 4, width: 0.6, dur: 0.5, h: 6 });
shoot([1438, 915], [1478, 916], T_18 + 3.1, { r: 4, width: 0.6, dur: 0.5, h: 6 });
// casualty card (the OLD clean K.casualties card, STYLE_LOCK 0b; real numbers only: FACTCHECK_C #9, ~11,400 Union, 15-18 Jun). Union column only:
// the Confederate loss is not spoken, so column B is removed.
const NC = K.casualties({ rows: [["", "~11,400"]], flagA: FL.us, headA: "UNION", flagB: FL.cs, t: T_LOST - 0.1, until: T_GONE - 0.1, top: 250 });
{ const inner = NC.firstElementChild; inner.removeChild(inner.lastElementChild); inner.style.flexWrap = "wrap"; inner.style.maxWidth = "520px"; inner.style.justifyContent = "center"; inner.style.background = "rgba(18,16,12,0.96)";
  const h = document.createElement("div"); h.style.cssText = "width:100%;text-align:center;font-size:22px;letter-spacing:.3em;color:#c9b48a;order:-1;margin-bottom:-30px"; h.textContent = "FOUR DAYS OF ASSAULTS"; inner.insertBefore(h, inner.firstChild);
  const f = document.createElement("div"); f.style.cssText = "width:100%;text-align:center;font-size:15px;letter-spacing:.22em;color:#a8a294;margin-top:-26px"; f.textContent = "MEN LOST"; inner.appendChild(f); }
const TRA = trench(NL.map((q) => [q[0] + 7, q[1]]), T_GONE - 0.2, 2.0, null, 2.0), TRB = trench(NL.map((q) => [q[0] - 7, q[1]]), T_GONE, 2.0, null, 2.0);
wstampS("THE CHANCE WAS GONE", 1400, 990, T_GONE + 0.1, null, "#e3232f", 26);
const GB = badge({ name: "ULYSSES S. GRANT", role: "YEARS LATER", initials: "USG", photo: PHOTO("grant"), flag: FL.us, side: "carth", corner: "bl", t: T_WROTE - 0.1, until: T_EVEN + 0.6 });
const PET = town("PETERSBURG", G.PETERSBURG, T_EASY - 1.2, "l", { size: 34 });
const QG = quote("PETERSBURG COULD HAVE BEEN EASILY CAPTURED AT THAT TIME", "GRANT WROTE YEARS LATER", T_EASY - 0.3, T_EVEN + 0.2, { col: "#1f4fc4", size: 40 });
// ---------- m3-7: the zoom-out. The army across the James (the whole move + the bridge), the siege lines grow, more than nine months ----------
const MOVE = G.MOVE;
arw({ pts: MOVE, side: "carth", t: T_ACROSS - 0.4, dur: 3.0, width: 15, dash: "40 24", until: END + 1 });
glowPath([[2347, 657], [2329, 679]], "#6f9bff", 14, T_ACROSS - 0.2, END + 1, 4, 0.95, { top: true });
boxS("THE JAMES", 2200, 470, T_ACROSS, null, { size: 26, bg: "#dcecf8" });
const W5 = FWw(0.55);
frontS({ pts: G.SIEGE_N, sideA: "carth", sideB: "rome", t: T_PIN, dur: 2.0, width: W5, until: END + 1 });
frontS({ pts: G.HOWLETT, sideA: "carth", sideB: "rome", t: T_PIN + 0.4, dur: 1.6, width: W5, until: END + 1 });
frontS({ pts: [...NL, ...G.SIEGE_S.slice(1)], sideA: "carth", sideB: "rome", t: T_PIN + 0.6, dur: 3.0, width: W5, until: END + 1 });
const NM = numCard("A SIEGE", "MORE THAN NINE MONTHS", "", "left:0;right:0;top:250px;display:flex;justify-content:center;", T_NINE - 0.1, T_ABAN - 0.2, { col: "#c4121f", lc: "#ff8a80" });
const RT = town("RICHMOND", G.RICHMOND, T_ABAN + 0.4, "l", { size: 36 }); const PT2 = town("PETERSBURG", G.PETERSBURG, T_ABAN + 0.1, "l", { size: 36 });
K.target(G.RICHMOND[0], G.RICHMOND[1], T_ABAN + 0.5, { r: 44, side: "#ffd54a", until: T_STALE + 1.5 });
K.target(G.PETERSBURG[0], G.PETERSBURG[1], T_ABAN + 0.2, { r: 44, side: "#ffd54a", until: T_STALE + 1.5 });
hideU(["s1", "s2", "h2", "pr", "v1", "v2", "v3", "v4"], T_Z1 - 1.5);
// method card on the spoken words of m3-7
GG.METHOD_TITLE = "GRANT'S METHOD";
GG.METHOD = ["OUT OF A STALEMATE", "OVER A RIVER", "WHERE LEE COULD NOT FOLLOW"];   // spoken words only (m3-7)
const MC = GG.method(3, T_STALE - 0.3, END + 1, [T_STALE, T_RIVER, T_FOLLOW]); SFX("ref:boom", T_FOLLOW + 0.2);
// ---------- clean screen ----------
declutter([LGD, HB, GB], [[T_LOST - 0.1, T_GONE - 0.1], [T_EASY - 0.3, T_EVEN + 0.2], [T_NINE - 0.1, T_ABAN - 0.2], [T_STALE - 0.3, END + 1]]);
fixImgs();
K.raiseTerritory();
B.finish();
