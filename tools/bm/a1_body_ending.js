// ENDING (end-1 .. end-2), Benedict Arnold #17. Map agent a1_.
// Built with: python3 tools/a1_inline.py ending end-1 end-2 northeast     (world = the northeast map px, z8; `maine` on top, feathered, so the
//   ground north of Quebec is real map; a sand underlay beyond). Flags: 13-star US flag vs Union Flag 1606; territory (1775 overlay = Canada
//   British) at half strength on this wide overhead shot.
// end-1: the three places light up in turn ONLY as named: QUEBEC (the march redrawn on "took an army where no one believed an army could go"),
//   LAKE CHAMPLAIN (the channel ring, the wind arrow on "the wind fought on his side", A WHOLE YEAR), SARATOGA (the line broken on "the one weak
//   point ... went through it himself"); push toward Saratoga; the boot card (photo of the monument, no name text) on "a boot".
// end-2: E.final (QUEBEC 1775 / VALCOUR ISLAND 1776 / SARATOGA 1777 on the spoken numbers; 1, 2 OR 3? on "Tell us in the comments"; the
//   "which commander next" line on its words; corner subscribe); the last part the card shrinks to a top band so the end screen fits over the map.
// @@KIT
const P1 = "end-1", P2 = "end-2";
const T_LOOK = at(P1, "Look at the three"), T_QUE = at(P1, "At Quebec"), T_TOOK = at(P1, "he took an army"), T_CHAMP = at(P1, "On Lake Champlain"),
  T_CHAN = at(P1, "a channel"), T_WIND = at(P1, "the wind fought"), T_YEAR = at(P1, "a whole year"), T_SARA = at(P1, "And at Saratoga"),
  T_NOCMD = at(P1, "no command at all"), T_WEAK = at(P1, "the one weak point"), T_THRU = at(P1, "went through it himself"), T_TODAY = at(P1, "Today, on"),
  T_MON = at(P1, "a monument"), T_BOOT = at(P1, "a boot"), T_NAME = at(P1, "carry his name"), T_E1END = B.T.paras[P1][1];
const F_Q = at(P2, "So which was"), F_1 = at(P2, "One, the march"), F_2 = at(P2, "Two, Valcour"), F_3 = at(P2, "Or three, Saratoga"),
  F_TELL = at(P2, "Tell us in the comments"), F_NEXT = at(P2, "which commander"), F_SUB = at(P2, "Subscribe, so you");
// ---------- the world ----------
const ME = mapTop("maine", "tblr", 5);
const NE_C = terrImg("assets/media/a1_ctl_northeast_1775.png", document.getElementById("world"), 0, null, 0.01);
WORLD.insertBefore(NE_C, ME);
const LV = LivingK(B); LV.clouds({ n: 6, opacity: 0.12 }); LV.north();
const L = (a, b) => LD(a, b);
const QUE = L(46.812, -71.21), VALC = L(44.611, -73.43), SARA = L(43.0, -73.635), STJ = L(45.30, -73.26), CRP = L(44.027, -73.424);
const ROUTE = smoothP([[44.05, -69.79], [44.31, -69.77], [44.55, -69.63], [44.765, -69.72], [44.713, -69.79], [44.95, -69.86], [45.12, -69.95], [45.17, -70.0],
  [45.18, -70.12], [45.19, -70.18], [45.15, -70.28], [45.22, -70.48], [45.33, -70.63], [45.39, -70.80], [45.45, -70.87], [45.585, -70.885], [45.80, -70.80],
  [46.12, -70.67], [46.30, -70.87], [46.44, -71.03], [46.60, -71.12], [46.80, -71.18]].map((q) => L(...q)), 2);
const LAKEP = [L(43.843, -73.387), CRP, L(44.25, -73.36), VALC, L(44.85, -73.33), L(45.05, -73.32), STJ];
const C0 = [1420, 560], S0 = 0.9;
camSet(C0, S0); camTo(0, T_TODAY, [1420, 566], 0.92, "sine.inOut");
// flags on their own ground, inside the frame for the whole scene and the end screen (Union Flag on Canada, clear of the date scroll and of the top band)
const F0 = [flagS(FL.gb, "", ...L(46.3, -73.9), null, null), flagS(FL.us, "", ...L(43.6, -71.6), null, null)]; gsap.set(F0, { autoAlpha: 1 }); const F1 = flagS(FL.gb, "", 1800, 470, T_TODAY + 0.6, null); tl.to(F0[0], { autoAlpha: 0, duration: 0.5 }, T_TODAY + 0.3);   // hand-over: the first Union Flag would leave through the top edge
B.showDate(0.2); dateRun([["1775 – 1777", 0.25, null]]);
// QUEBEC: lights up on its name; the march redrawn
// QUEBEC sits near the top of this shot: its label goes below-right of the city (never on the frame edge), a smaller ring
const TQ = boxL("QUEBEC", QUE[0] + 80 / S0, QUE[1] + 62 / S0, T_QUE, null, { size: 16 });
K.target(...QUE, T_QUE + 0.1, { r: 34 / S0, side: "#ffd54a", until: T_CHAMP });
trail(ROUTE, "#e6f0ff", 4.5 / S0, T_TOOK, 3.0, T_SARA, `${9 / S0} ${7 / S0}`); SFX("ref:whoosh", T_TOOK);
arw({ pts: ROUTE.slice(-6), side: "carth", t: T_TOOK + 2.6, dur: 0.6, width: AW(S0, 12), until: T_SARA });
// LAKE CHAMPLAIN: the lake glows on its name; the channel; the wind; a whole year
glowPath(LAKEP, "#ffd54a", 5 / S0, T_CHAMP, T_SARA + 0.4, 1, 0.8, { draw: 0.8 });
boxL("LAKE CHAMPLAIN", VALC[0] + 40, VALC[1] + 30, T_CHAMP + 0.1, null, { size: 15 });
K.target(...VALC, T_CHAN + 0.05, { r: 34 / S0, side: "#ffd54a", until: T_SARA });
const WIND = arw({ pts: [[VALC[0] + 120, VALC[1] - 220], [VALC[0] + 60, VALC[1] - 110], [VALC[0] + 12, VALC[1] - 30]], side: "carth", t: T_WIND, dur: 0.9, width: AW(S0, 10), dash: "12 9", until: T_SARA });
gsap.set(WIND, { filter: "grayscale(1) brightness(2.2)" }); SFX("ref:whoosh", T_WIND);
wstampL("A WHOLE YEAR", VALC[0] - 150, VALC[1] + 70, T_YEAR + 0.05, null, "#9fc0ea", 22);
// SARATOGA: lights up on its name; the weak point; through it
const TS = town("SARATOGA", SARA, "r", T_SARA + 0.1, { until: T_SARA + LBL_LIFE });
K.target(...SARA, T_SARA + 0.2, { r: 34 / S0, side: "#ffd54a", until: T_TODAY });
const RL = glowPath([[SARA[0] - 60, SARA[1] - 40], [SARA[0] - 20, SARA[1] - 8], [SARA[0] + 20, SARA[1] + 6], [SARA[0] + 60, SARA[1] + 10]], "#c4121f", 6 / S0, T_WEAK - 0.2, T_BOOT, 0, 0.9, { draw: 0.6, top: true });
const BR = arw({ pts: [[SARA[0] - 30, SARA[1] + 70], [SARA[0] - 22, SARA[1] + 10], [SARA[0] - 14, SARA[1] - 60]], side: "carth", t: T_THRU - 0.3, dur: 0.8, width: AW(S0, 12), until: T_BOOT });
SFX("hit", T_THRU + 0.4); K.shake(T_THRU + 0.4, 3, 0.25);
// "Today, on the battlefield at Saratoga": push toward it; the boot card on "a boot" (no name on it)
const CF = [SARA[0] + 122, SARA[1] - 165], SF = 1.1;   // the end-screen shot: Saratoga with Canada (British) along the top, both flags in frame
camTo(T_TODAY, 5.0, CF, SF, "sine.inOut");
camTo(T_TODAY + 5.0, END - T_TODAY - 5.0, [CF[0] + 20, CF[1] - 10], SF * 1.05, "none");   // a slow living drift to the last frame
// "It shows a boot.": a SMALL framed archive card (projector-style frame, sepia, slow push inside), no name on it, beside Saratoga
const BOOT = scr(`<div style="padding:10px;background:#15120d;border:2px solid #c9b48a;box-shadow:0 0 0 6px rgba(21,18,13,0.92),0 22px 44px rgba(0,0,0,.65);transform:rotate(-1.5deg)">
  <div style="position:relative;width:400px;height:300px;overflow:hidden;outline:1px solid rgba(201,180,138,0.5)"><div class="bi" style="position:absolute;inset:0;background:url(assets/media/arch_boot_monument.jpg) 52% 40%/auto 128% no-repeat;filter:grayscale(0.9) sepia(0.35) contrast(1.12) brightness(0.95)"></div>
  <div style="position:absolute;inset:0;box-shadow:inset 0 0 60px rgba(0,0,0,0.75)"></div></div></div>`,
  "right:170px;top:300px;transform-origin:50% 50%;", T_BOOT - 0.05, F_Q - 0.2, { autoAlpha: 0, scale: 0.85 });
tl.fromTo(BOOT.querySelector(".bi"), { scale: 1 }, { scale: 1.08, duration: F_Q - T_BOOT, ease: "none", immediateRender: false }, T_BOOT);
SFX("ref:pop", T_BOOT);
// end-2: the final question
const FC = E.final({ moves: [["QUEBEC", "1775"], ["VALCOUR ISLAND", "1776"], ["SARATOGA", "1777"]], tShow: F_Q, tNums: [F_1, F_2, F_3], tAsk: F_TELL, tFamily: F_NEXT, tSub: F_SUB, until: END + 1 });
FC.querySelector(".fam").innerHTML = `WHICH COMMANDER SHOULD WE COVER NEXT? <span style="color:#c9b48a">TELL US IN THE COMMENTS</span>`;
FC.style.top = "210px";                                       // below the date scroll
document.getElementById("date").style.zIndex = 40;           // the date scroll stays above the dim layer
// nothing before it is spoken: the kicker waits for "Tell us in the comments"; each numbered card pops ONLY on its number (one entrance each)
const KICK = FC.firstElementChild; gsap.set(KICK, { autoAlpha: 0 }); tl.set(KICK, { autoAlpha: 0 }, 0); tl.to(KICK, { autoAlpha: 1, duration: 0.3 }, F_TELL);
[F_1, F_2, F_3].forEach((tt, i) => { const c = FC.querySelector(".m" + i); tl.getTweensOf(c).forEach((tw) => tw.kill()); gsap.set(c, { autoAlpha: 0 }); tl.set(c, { autoAlpha: 0 }, 0);
  tl.fromTo(c, { autoAlpha: 0, scale: 1.25, y: 0 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, tt);
  tl.to(c, { borderColor: "#ffd54a", duration: 0.25 }, tt + 0.3); tl.to(c, { borderColor: "rgba(201,180,138,0.6)", duration: 0.4 }, (i < 2 ? [F_2, F_3][i] : F_TELL)); });
// right after "Subscribe, so you don't miss the next one": the card shrinks to the top band, the subscribe button leaves, the map is clean + alive to END
const tBand = B.T.paras[P2][1] + 0.15;
tl.to(FC, { scale: 0.5, y: -125, duration: 0.8, ease: "power2.inOut", transformOrigin: "50% 0%" }, tBand);
const back = FC.previousElementSibling; if (back) tl.to(back, { autoAlpha: 0, duration: 0.8 }, tBand);
const SUBB = [...SCN.children].find((e) => e.querySelector && e.querySelector(".lab")); if (SUBB) tl.to(SUBB, { autoAlpha: 0, x: 120, duration: 0.5, ease: "power2.in" }, tBand);
fixImgs();
B.finish();
