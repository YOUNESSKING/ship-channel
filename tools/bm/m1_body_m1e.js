// m1e (m1-7..m1-8), Grant #16: night 15-16 Feb: Floyd and Pillow leave on river steamers from the Dover landing, Forrest's cavalry rides
// out through the flooded backwater of Lick Creek, the command falls to Buckner; dawn 16 Feb: the letters (Grant's reply verbatim, hit on
// "immediate"), Buckner accepts, the US flag over the fort (option 2 throughout: owner 2026-11-02, no ground tint on close-ups); Grant's telegram
// (12,000-15,000 prisoners, 48 field guns, 17 heavy guns), U.S. = Unconditional Surrender Grant, the casualty card.
// Basemap donelson_hd_lift (z13, v11). Built with: python3 tools/m1_build.py m1e donelson_hd_lift m1-7 m1-8
// @@BODY
const P7 = "m1-7", P8 = "m1-8";
const T_FP = at(P7, "Generals Floyd and Pillow"), T_PIL = at(P7, "Pillow, the two"), T_STEAM = at(P7, "left on river steamers"), T_FLOYD2 = at(P7, "Floyd had been"),
  T_SEC = at(P7, "secretary of war"), T_FEAR = at(P7, "feared what the North"), T_FOR = at(P7, "Nathan Bedford Forrest"), T_SEV = at(P7, "several hundred cavalry"),
  T_BACKW = at(P7, "through the flooded backwater"), T_CMD = at(P7, "The command fell to"), T_BUCK = at(P7, "Simon Buckner"), T_DAWN = at(P7, "At dawn he wrote"),
  T_TERMS = at(P7, "asking for terms");
const T_ANS = at(P8, "Grant answered the same day"), T_NO = at(P8, "No terms except"), T_IMM = at(P8, "immediate surrender"), T_PROP = at(P8, "I propose to move"),
  T_BCALL = at(P8, "Buckner called the terms"), T_UNG = at(P8, "ungenerous and unchivalrous"), T_ACC = at(P8, "but he accepted"), T_TELE = at(P8, "Grant telegraphed Halleck"),
  T_TAKEN = at(P8, "taken Fort Donelson"), T_PRIS = at(P8, "twelve to fifteen thousand prisoners"), T_48 = at(P8, "forty-eight field guns"), T_17 = at(P8, "seventeen heavy guns"),
  T_LET = at(P8, "The North turned the letters"), T_US = at(P8, "U.S., into a joke"), T_NICK = at(P8, "then a nickname"), T_USG = at(P8, "Unconditional Surrender Grant"),
  T_LOSS = at(P8, "His own side's losses"), T_2800 = at(P8, "nearly twenty-eight hundred");
// ---------- places (donelson map px) ----------
const DON = [1388, 738], DOV = [1508, 756], LANDG = [1516, 724], GHQ = [1237, 825];
const WORKS = [[1540, 811], [1487, 832], [1429, 825], [1371, 796], [1312, 753], [1289, 702], [1307, 651], [1324, 630]];
const ULINE = [[1557, 854], [1487, 876], [1406, 869], [1330, 832], [1266, 775], [1243, 709], [1254, 644], [1289, 601]];
const MID = WORKS.map((q, i) => [(q[0] + ULINE[i][0]) / 2, (q[1] + ULINE[i][1]) / 2]);
const MID2 = MID.map((q, i) => i >= 5 ? [q[0] + [0, 0, 0, 36, 40, 30, 22, 10][i], q[1] + [0, 0, 0, 0, 0, 6, 14, 18][i]] : q);
const UPRIVER = [LANDG, [1600, 690], [1720, 650], [1840, 628], [1960, 680], [2060, 780], [2160, 900], [2260, 1040]];
const ESCAPE = [[1500, 805], [1556, 832], [1610, 878], [1660, 950], [1712, 1050], [1760, 1160], [1800, 1280]];
const CUMB = [[1120, 0], [1180, 200], [1240, 340], [1320, 500], [1400, 620], [1480, 690], [1600, 680], [1720, 640], [1840, 624], [1980, 700], [2100, 820]];
// ---------- map: option 2 (no territory fill) the whole scene ----------
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); LV.shimmer([CUMB], { width: 1.2 }); LV.scaleBar(15.37); LV.north();
const NW = nightWash(0, T_DAWN - 0.2, 0.5); gsap.set(NW, { autoAlpha: 1 }); tl.getTweensOf(NW).filter((tw) => tw.startTime() < 0.05).forEach((tw) => tw.kill());
dawnWash(T_DAWN - 0.3, T_TELE);
const LGD2 = now(legend(0, END + 1, true));
camera([[0, 1480, 760, 2.2], [T_STEAM + 0.4, 1560, 740, 2.0], [T_FEAR, 1600, 760, 1.9], [T_FOR, 1560, 860, 2.1], [T_BACKW + 0.6, 1590, 900, 2.0],
  [T_CMD, 1450, 770, 2.2], [T_DAWN + 0.3, 1380, 790, 1.8], [T_ANS + 0.4, 1370, 790, 1.8], [T_ACC, 1400, 760, 2.0], [T_TELE, 1380, 760, 1.35],
  [T_LET, 1360, 760, 1.2], [END, 1340, 760, 1.12]]);
dateNow("15 FEB · NIGHT", T_DAWN - 0.1); B.date("16 FEB · DAWN", T_DAWN, T_ANS - 0.1, 34); B.date("16 FEBRUARY 1862", T_ANS, null, 34);
// ---------- flags ----------
flagS(FL.us, 1290, 880, 0, T_ACC + 1.6, 90); flagS(FL.cs, 1600, 640, 0, T_ACC + 1.6, 90);
flagS(FL.us, 1000, 620, T_ACC + 1.4, END + 1, 100); flagS(FL.cs, 1950, 980, T_ACC + 1.5, END + 1, 100);
// ---------- the pocket as m1d left it ----------
fortIcon(DON, 0, null, { s: 24 }); poleFlag(FL.cs, [DON[0] + 4, DON[1] - 8], 0, T_ACC + 0.4, 34); poleFlag(FL.us, [DON[0] + 4, DON[1] - 8], T_ACC + 0.45, END + 1, 38);
const FR = frontS({ pts: MID2, sideA: "carth", sideB: "rome", t: 0, dur: 0.01, width: FWc(2.1), until: T_ACC + 1.0 });
tl.to(FR, { opacity: 0, duration: 2.2, ease: "sine.inOut" }, T_ACC + 1.0);
[["sm1", [1305, 660]], ["sm2", [1302, 700]], ["wal", [1268, 790]], ["mc1", [1290, 885]], ["mc2", [1385, 935]], ["mc3", [1470, 945]]].forEach(([id, p]) => unitS(id, "carth", p, "infantry", null, { t: 0, size: "X" }));
const RED = [["bu", [1350, 712]], ["c1", [1352, 790]], ["c2", [1420, 805]], ["c3", [1490, 812]], ["c4", [1455, 780]]];
RED.forEach(([id, p]) => unitS(id, "rome", p, "infantry", null, { t: 0, size: "X" }));
tl.to(B.units.c2.el, { y: -3, duration: 0.7, yoyo: true, repeat: 3, ease: "sine.inOut" }, 0.1);
// ---------- Floyd and Pillow leave on the river steamers ----------
const CF = chip("floyd", "FLOYD", "rome", "right:200px;top:240px;", T_FP, T_CMD - 0.2), CP = chip("pillow", "PILLOW", "rome", "right:60px;top:240px;", T_PIL - 0.3, T_CMD - 0.2);
unitS("c5", "rome", [1530, 790], "infantry", null, { t: 0, size: "X" });
B.move("c5", T_STEAM - 0.6, 1.0, LANDG[0] + 4, LANDG[1] + 14); hideU(["c5"], T_STEAM + 0.5);
const ST = [0, 1].map((k) => { const s = ship("steamer", "rome", [LANDG[0] - 20 - k * 30, LANDG[1] + 10 + k * 6], -20, null, null, { L: 64, name: k ? "PILLOW" : "FLOYD", ny: k ? -44 : 20 });
  tl.set(s.el, { autoAlpha: 1 }, 0); gsap.set(s.name, { autoAlpha: 0 }); tl.to(s.name, { autoAlpha: 1, duration: 0.4 }, k ? T_PIL : T_FP); tl.to(s.name, { autoAlpha: 0, duration: 0.5 }, T_FEAR + 1.0);
  sail(s, UPRIVER.map((q) => [q[0], q[1] + k * 8]), T_STEAM + 0.2 + k * 1.8, T_CMD - T_STEAM + 1.0, 24); stackSmoke([LANDG[0] + 60, LANDG[1] - 20], T_STEAM + 0.8 + k * 0.6, T_STEAM + 4, 1.4); return s; });
B.caption("LEFT ON RIVER STEAMERS IN THE NIGHT", T_STEAM, T_FLOYD2 - 0.1, "rome");
B.caption("FLOYD: BUCHANAN'S SECRETARY OF WAR", T_SEC - 0.8, T_FOR - 0.2, "rome");
// ---------- Forrest's cavalry out through the flooded backwater ----------
const BW = pinS(GG.pin(`<div style="width:150px;height:90px;border-radius:50%;transform:rotate(40deg);background:radial-gradient(ellipse at center, rgba(120,170,215,.7) 0%, rgba(120,170,215,.4) 45%, rgba(120,170,215,0) 72%)"></div>`, 1585, 862, { t: T_BACKW - 0.6, until: T_DAWN + 1 }));
unitS("for", "rome", ESCAPE[0], "cavalry", "FORREST", { t: T_FOR }); cavIcon("for");
along("for", ESCAPE, T_SEV, T_CMD - T_SEV + 1.6, 20); hideU(["for"], T_CMD + 1.8);
arw({ pts: ESCAPE.slice(0, 6).map((q) => [q[0] + 16, q[1] - 6]), side: "rome", t: T_SEV - 0.2, dur: 2.4, width: AW(2.0, 11), dash: "10 8", until: T_CMD + 1.2 });
B.caption("SEVERAL HUNDRED CAVALRY · THE FLOODED BACKWATER", T_SEV, T_CMD - 0.1, "rome");
// ---------- the command falls to Buckner; at dawn he writes asking for terms ----------
const BB = badge({ name: "SIMON BUCKNER", role: "COMMAND FELL TO HIM", initials: "SB", photo: PHOTO("buckner"), flag: FL.cs, side: "rome", corner: "bl", t: T_BUCK, until: T_ANS - 0.3 });
pulseU("bu", T_BUCK + 0.2);
const LTR = `<svg width="34" height="24" viewBox="0 0 34 24" style="display:block;filter:drop-shadow(0 0 4px rgba(255,240,200,.9)) drop-shadow(0 2px 3px #000)"><rect x="1" y="1" width="32" height="22" rx="2" fill="#efe6cf" stroke="#1a1712" stroke-width="1.4"/><path d="M1 2 L17 13 L33 2" fill="none" stroke="#1a1712" stroke-width="1.4"/></svg>`;
const L1 = pinS(GG.pin(`<div style="transform:scale(1.4)">${LTR}</div>`, DOV[0], DOV[1], { t: T_DAWN, pop: true, until: T_TERMS + 2.0 }));
pinAlong(L1, [DOV, [1420, 790], [1330, 815], GHQ], T_DAWN + 0.4, 2.4, 16);
const HQ = pinS(GG.pin(`<div style="position:relative;width:0;height:0"><div style="position:absolute;left:-9px;top:-9px;width:18px;height:18px;transform:rotate(45deg);background:#1f4fc4;border:2px solid #f7f3ea;box-shadow:0 0 8px #1f4fc4"></div></div>`, GHQ[0], GHQ[1], { t: 0.2 }));
B.caption("ASKING FOR TERMS", T_TERMS, T_ANS - 0.1, "rome");
// ---------- Grant's answer (verbatim; quote marks) ----------
const GB = badge({ name: "ULYSSES S. GRANT", role: "BRIGADIER GENERAL", initials: "USG", photo: PHOTO("grant"), flag: FL.us, side: "carth", corner: "bl", t: T_ANS, until: T_BCALL - 0.3 });
const L2 = pinS(GG.pin(`<div style="transform:scale(1.4)">${LTR}</div>`, GHQ[0], GHQ[1], { t: T_ANS + 0.2, pop: true, until: T_BCALL + 0.5 }));
pinAlong(L2, [GHQ, [1330, 815], [1420, 790], DOV], T_ANS + 0.5, 2.0, 16);
const Q = quote(`“No terms except an unconditional and <b class="imm" style="color:#9fc0ea">immediate</b> surrender can be accepted.<span class="q2"> I propose to move immediately upon your works.”</span>`, "GRANT TO BUCKNER · 16 FEBRUARY 1862", T_NO - 0.1, T_BCALL - 0.2, { size: 44, mw: 1300 });
const Q2 = Q.querySelector(".q2"); gsap.set(Q2, { autoAlpha: 0 }); tl.to(Q2, { autoAlpha: 1, duration: 0.4 }, T_PROP - 0.1);
tl.fromTo(Q.querySelector(".imm"), { color: "#f7f3ea" }, { color: "#9fc0ea", duration: 0.2, immediateRender: false }, T_IMM); SFX("hit", T_IMM + 0.05); K.shake(T_IMM + 0.05, 5, 0.3);
// Buckner: ungenerous and unchivalrous, but he accepted
const UN = belief("UNGENEROUS AND UNCHIVALROUS", "BUCKNER ON THE TERMS", T_UNG - 0.1, T_ACC - 0.1, { size: 50 });
greyU(["bu", "c1", "c2", "c3", "c4"], T_ACC + 0.3);
wstampS("ACCEPTED", DON[0] + 10, DON[1] - 70, T_ACC + 0.1, null, "#9fc0ea", 26);
hideU(["bu", "c1", "c2", "c3", "c4", "mc1", "mc2", "mc3", "wal", "sm1", "sm2"], T_TELE + 0.4);
unitS("pr", "rome", [1440, 780], "infantry", "PRISONERS", { t: T_TELE + 0.4, size: "XX" }); greyU(["pr"], T_TELE + 0.4);
unitS("gA", "carth", [1270, 760], "infantry", "GRANT", { t: T_TELE + 0.5, size: "XXX" });
K.target(DON[0], DON[1], T_TAKEN, { r: 60, side: "#9fc0ea", until: END + 1 });
// ---------- the telegram to Halleck ----------
const TG = scr(`<div style="padding:18px 46px 20px;background:rgba(18,16,12,0.94);border-top:6px solid #c9b48a;font-family:Oswald;font-weight:700;color:#f7f3ea;text-align:center;box-shadow:0 20px 40px rgba(0,0,0,.55);min-width:720px">
  <div style="font-size:20px;letter-spacing:.32em;color:#c9b48a">GRANT TO HALLECK · TELEGRAM</div>
  <div style="font-size:30px;letter-spacing:.1em;margin-top:6px">TAKEN FORT DONELSON</div>
  <div class="r1" style="font-size:58px;letter-spacing:.04em;margin-top:6px;color:#ff8a80">12,000–15,000 <span style="font-size:30px;color:#f7f3ea">PRISONERS</span></div>
  <div class="r2" style="display:flex;justify-content:center;gap:44px;font-size:44px;margin-top:4px"><span class="a">48 <span style="font-size:24px">FIELD GUNS</span></span><span class="b">17 <span style="font-size:24px">HEAVY GUNS</span></span></div></div>`,
  "left:0;right:0;top:230px;display:flex;justify-content:center;", T_TAKEN - 0.2, T_LET - 0.2);
const [R1, RA, RB] = [TG.querySelector(".r1"), TG.querySelector(".a"), TG.querySelector(".b")]; gsap.set([R1, RA, RB], { autoAlpha: 0 });
[[R1, T_PRIS], [RA, T_48], [RB, T_17]].forEach(([el, t]) => { tl.fromTo(el, { autoAlpha: 0, scale: 1.4 }, { autoAlpha: 1, scale: 1, duration: 0.25, immediateRender: false }, t); SFX("tick", t + 0.1); });
// ---------- U.S. -> UNCONDITIONAL SURRENDER GRANT ----------
const NN = scr(`<div style="padding:20px 56px 24px;background:rgba(18,16,12,0.94);border-top:6px solid #1f4fc4;font-family:Oswald;font-weight:700;color:#f7f3ea;text-align:center;box-shadow:0 20px 40px rgba(0,0,0,.55)">
  <div class="us" style="font-size:110px;letter-spacing:.12em;line-height:1;color:#c9b48a">U.S.</div>
  <div class="full" style="font-size:66px;letter-spacing:.06em;line-height:1.1"><b style="color:#c9b48a">U</b>NCONDITIONAL <b style="color:#c9b48a">S</b>URRENDER GRANT</div></div>`,
  "left:0;right:0;top:230px;display:flex;justify-content:center;", T_US - 0.3, T_LOSS - 0.2);
const US = NN.querySelector(".us"), FULL = NN.querySelector(".full"); gsap.set(FULL, { autoAlpha: 0, height: 0 });
tl.to(US, { autoAlpha: 0, height: 0, duration: 0.3 }, T_USG - 0.2); tl.to(FULL, { autoAlpha: 1, height: "auto", duration: 0.01 }, T_USG - 0.05);
slam(FULL, T_USG - 0.05, { shake: 5 });
// ---------- casualty card (the old clean K.casualties card; real numbers only: FACTCHECK_A #11, #12) ----------
const CAS = K.casualties({ rows: [["", "~2,800", "12,000–15,000"]], flagA: FL.us, flagB: FL.cs, headA: "UNION", headB: "CONFEDERATE", t: T_LOSS, until: END + 1, top: 250 });
{ const inner = CAS.firstElementChild; inner.style.flexWrap = "wrap"; inner.style.maxWidth = "980px";
  const h = document.createElement("div"); h.style.cssText = "width:100%;text-align:center;font-size:22px;letter-spacing:.3em;color:#c9b48a;order:-1;margin-bottom:-30px"; h.textContent = "FORT DONELSON"; inner.insertBefore(h, inner.firstChild);
  const f = document.createElement("div"); f.style.cssText = "width:100%;text-align:center;font-size:15px;letter-spacing:.22em;color:#a8a294;margin-top:-26px"; f.textContent = "UNION: LOSSES · CONFEDERATE: PRISONERS"; inner.appendChild(f); }
// ---------- clean screen ----------
declutter([LGD2, CF, CP, BB, GB], [[T_NO - 0.1, T_BCALL - 0.2], [T_UNG - 0.1, T_ACC - 0.1], [T_TAKEN - 0.2, END + 1]]);
fixImgs();
K.raiseTerritory();
B.finish();
