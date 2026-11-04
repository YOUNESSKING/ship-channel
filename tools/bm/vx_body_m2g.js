// MOVE 2g (m2-11 .. m2-12), Grant #16: the 19 and 22 May assaults bounce off the Vicksburg works; Grant regretted the second; the siege (trenches,
// saps creeping in; the date scroll runs into June: the 35-star US flag from 1 June 1863, on the scroll and on the map); 4 July: white flags,
// Pemberton surrendered about 29,500 men and 172 cannon; Lincoln's line: ONE continuous zoom-out from the siege lines to the whole Mississippi
// (no cut), the river turns blue top to bottom; m2-12: the territory dissolves into July 1863 (the river Union, the Confederacy cut in two: no
// text, it is not spoken); method card line 2 on the spoken words. Map agent "vx".
// ONE world = vicksburg_siege map px (z12). The `mississippi` map (z8) sits in it at its true place and scale (16x; technique of
// tools/vk_body_m2a.js / patton hook-a): one camera drives the siege close-up (s 2.2 - 2.9, option 2: two glowing front bands, no fill) and the
// river overview (s ~0.042, option 1: territory); the mississippi layer fades in between s 0.35 and 0.12 over the edge-feathered siege map.
// Facts: FACTCHECK_B #23 (both assaults failed; Grant regretted the 22 May assault; no casualty figure), #27 (4 July, white flags at 10 a.m.,
// Pemberton), #28 (about 29,500), #29 (172 cannon), Lincoln (the script's reported wording, no quote marks: he wrote "goes", the script says "went").
// Built with: python3 tools/vx_inline.py m2g vicksburg_siege_hd_lift m2-11 m2-12
// @@KIT
// @@DATA
const SZ = GD.maps.vicksburg_siege, MZ = GD.maps.mississippi;
const L = GG.proj(12, SZ.origin_world_px[0], SZ.origin_world_px[1]);
const LL = (pts) => pts.map(([la, lo]) => L(la, lo));
const P1 = "m2-11", P2 = "m2-12";
const T_TWO = at(P1, "Two assaults"), T_19 = at(P1, "nineteenth"), T_22 = at(P1, "twenty-second of May"), T_FAIL = at(P1, "failed."), T_GW = at(P1, "Grant later wrote"),
  T_REG = at(P1, "regretted the second one"), T_SIEGE = at(P1, "So he settled in"), T_SG = at(P1, "for a siege"), T_JUL = at(P1, "the fourth of July"),
  T_PEM = at(P1, "Pemberton surrendered"), T_295 = at(P1, "twenty-nine and a half thousand"), T_172 = at(P1, "a hundred and seventy-two cannon"),
  T_LIN = at(P1, "Lincoln wrote"), T_FATHER = at(P1, "the Father of Waters"), T_SEA = at(P1, "unvexed to the sea");
const T_EVERY = at(P2, "Everyone had said"), T_SUP = at(P2, "without its supply line"), T_CUT = at(P2, "Grant cut it"), T_FED = at(P2, "fed his men off the land"),
  T_GATES = at(P2, "at the gates of Vicksburg"), T_UND = at(P2, "understood where he was"), T_FEW = at(P2, "fewer men than the Confederates");
// ---------- places (vicksburg_siege z12 world px; far places in the same px) ----------
const VKS = L(32.352, -90.878), MEM = L(35.149, -90.049), NO = L(29.951, -90.072), PH = L(30.678, -91.27), JAX = L(32.299, -90.185), GGF = L(32.033, -91.053),
  BRU = L(31.942, -91.157);
// the Confederate works (Fort Hill on the river - Stockade Redan - 3rd Louisiana Redan - Great Redoubt - 2nd Texas Lunette - Railroad Redoubt -
// Square Fort - South Fort) and the Union siege line ~700 m outside (approx., NPS Vicksburg tour map)
const CSL = LL([[32.382, -90.884], [32.373, -90.864], [32.364, -90.853], [32.352, -90.847], [32.340, -90.850], [32.329, -90.856], [32.318, -90.864], [32.309, -90.877], [32.303, -90.890]]);
const USL = LL([[32.392, -90.876], [32.382, -90.853], [32.368, -90.839], [32.352, -90.833], [32.336, -90.837], [32.322, -90.845], [32.309, -90.858], [32.297, -90.873], [32.290, -90.888]]);
const FRT = LL([[32.387, -90.880], [32.378, -90.858], [32.366, -90.846], [32.352, -90.840], [32.338, -90.843], [32.325, -90.850], [32.313, -90.861], [32.303, -90.875], [32.296, -90.889]]);
// the Mississippi Memphis -> New Orleans (approx. 1863 course; for the glow and the shimmer)
const RIVM = LL([[35.15, -90.07], [34.80, -90.30], [34.53, -90.58], [34.15, -90.85], [33.75, -91.05], [33.40, -91.08], [33.05, -91.12], [32.80, -91.16], [32.60, -91.12],
  [32.48, -91.06], [32.40, -91.00], [32.375, -90.93], [32.37, -90.895], [32.345, -90.893], [32.30, -90.90], [32.247, -90.935], [32.13, -91.04], [32.04, -91.07],
  [31.95, -91.16], [31.80, -91.30], [31.56, -91.42], [31.20, -91.58], [31.00, -91.62], [30.70, -91.32], [30.45, -91.20], [30.20, -91.08], [29.95, -90.07], [29.6, -89.75], [29.2, -89.3]]);
const RIVN = LL([[37.0, -89.18], [36.6, -89.5], [36.0, -89.7], [35.5, -90.0], [35.15, -90.07]]);
const RIVS = LL([[32.42, -90.96], [32.375, -90.93], [32.37, -90.895], [32.345, -90.893], [32.30, -90.90], [32.247, -90.935]]);
// ---------- the world: mississippi layers under the feathered siege relief + on top of it ----------
const AR = [MZ.origin_world_px[0] * 16 - SZ.origin_world_px[0], MZ.origin_world_px[1] * 16 - SZ.origin_world_px[1], 46080, 25920];
const group = (parent, before) => { const g = document.createElement("div"); g.style.cssText = `position:absolute;left:${AR[0]}px;top:${AR[1]}px;width:${AR[2]}px;height:${AR[3]}px;isolation:isolate;`; parent.insertBefore(g, before); return g; };
const gimg = (src, parent, mx) => { const i = document.createElement("img"); i.src = src; i.alt = ""; i.style.cssText = `position:absolute;left:0;top:0;width:100%;height:100%;${mx ? `mix-blend-mode:multiply;filter:${SOFT};` : ""}`; parent.appendChild(i); return i; };   // owner 2026-11-02: the river-overview fill kept (Confederacy cut in two), subtler
const RELIEF = document.getElementById("relief");
const PU = group(WORLD, RELIEF); gimg("assets/media/vx_miss_relief.jpg", PU, false);
const PW = group(WORLD, OVL); gimg("assets/media/vx_miss_relief.jpg", PW, false);
const CA = gimg("assets/media/vx_miss_apr_mx.png", PW, true), CJ = gimg("assets/media/vx_miss_jul_mx.png", PW, true);
gsap.set(CJ, { autoAlpha: 0 }); tl.to(CJ, { autoAlpha: 1, duration: 2.2, ease: "sine.inOut" }, T_EVERY - 0.2); tl.to(CA, { autoAlpha: 0, duration: 2.2, ease: "sine.inOut" }, T_EVERY - 0.2);
living(SZ.meters_per_px, [RIVS], { n: 5, clouds: 0.12, sw: 5 });
const FEATHER = "linear-gradient(to right, transparent 0%, #000 8%, #000 92%, transparent 100%), linear-gradient(to bottom, transparent 0%, #000 8%, #000 92%, transparent 100%)";
let maskOn = null;
const setMask = (on) => { if (on === maskOn) return; maskOn = on; [RELIEF].forEach((el) => { const v = on ? FEATHER : "none"; el.style.webkitMaskImage = v; el.style.maskImage = v; el.style.webkitMaskComposite = on ? "source-in" : ""; el.style.maskComposite = on ? "intersect" : ""; }); };
// ---------- the one camera ----------
const OVS = 1920 / AR[2];
const cam = { cx: 0, cy: 0, s: 2.6 };
const clampK = (s) => Math.min(1, Math.max(0, (s - 0.6) / 0.25));
const applyCam = () => { let s = cam.s, cx = cam.cx, cy = cam.cy; const cl = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
  const k = clampK(s); if (k > 0) { const ccx = cl(cx, 960 / s, 2880 - 960 / s), ccy = cl(cy, 540 / s, 1620 - 540 / s); cx += (ccx - cx) * k; cy += (ccy - cy) * k; }
  if (s < 0.9) { const mx = cl(cx, AR[0] + 960 / s, AR[0] + AR[2] - 960 / s), my = cl(cy, AR[1] + 540 / s, AR[1] + AR[3] - 540 / s); const j = 1 - k; cx += (mx - cx) * j; cy += (my - cy) * j; }
  gsap.set(WORLD, { x: 960 - cx * s, y: 540 - cy * s, scale: s }); CAM_S = s; setInv();
  const op = s >= 0.35 ? 0 : s <= 0.12 ? 1 : Math.log(0.35 / s) / Math.log(0.35 / 0.12);
  PW.style.opacity = op.toFixed(3); setMask(s < 0.8); };
const camTo = (t, dur, c, s, ease = "sine.inOut") => tl.to(cam, { cx: c[0], cy: c[1], s, duration: Math.max(dur, 0.01), ease, onUpdate: applyCam }, t);
const zoom = (t, dur, c0, s0, c1, s1, P, ease = "power2.inOut") => {   // log-scale zoom that keeps P moving smoothly on screen
  const d0 = [(P[0] - c0[0]) * s0, (P[1] - c0[1]) * s0], d1 = [(P[0] - c1[0]) * s1, (P[1] - c1[1]) * s1], q = { u: 0 };
  tl.fromTo(q, { u: 0 }, { u: 1, duration: dur, ease, immediateRender: false, onUpdate: () => { const u = q.u, s = Math.exp(Math.log(s0) + (Math.log(s1) - Math.log(s0)) * u);
    cam.s = s; cam.cx = P[0] - (d0[0] + (d1[0] - d0[0]) * u) / s; cam.cy = P[1] - (d0[1] + (d1[1] - d0[1]) * u) / s; applyCam(); } }, t); };
const C0 = L(32.348, -90.862), S0 = 2.6;                 // the siege lines (hand-off from m2f: the ring round Vicksburg)
const C1 = L(32.345, -90.855), S1 = 2.85;
const OC = [AR[0] + AR[2] / 2, AR[1] + AR[3] / 2];
const C2 = L(32.6, -90.6), S2 = OVS * 1.12;              // the whole river, Memphis to the Gulf
const C3 = L(32.45, -90.75), S3 = OVS * 1.65;            // m2-12: slow push toward Vicksburg
cam.cx = C0[0]; cam.cy = C0[1]; cam.s = S0; applyCam();
camTo(0, T_SIEGE - 0.2, C1, S1, "sine.inOut");
camTo(T_SIEGE - 0.2, T_LIN - T_SIEGE, [C1[0] - 20, C1[1] + 6], S1 * 0.92, "sine.inOut");
const TZ0 = T_LIN - 0.1, TZ1 = T_SEA + 0.8;
zoom(TZ0, TZ1 - TZ0, [C1[0] - 20, C1[1] + 6], S1 * 0.92, C2, S2, VKS, "power2.inOut"); SFX("whoosh", TZ0 - 0.05);
camTo(TZ1 + 0.02, END - TZ1, C3, S3, "sine.inOut");
const sAt = (t) => t < TZ0 ? S1 : t > TZ1 ? S2 : Math.exp(Math.log(S1) + (Math.log(S2) - Math.log(S1)) * (t - TZ0) / (TZ1 - TZ0));
// ---------- HUD: legend (option 2 lines on the close-up), the date scroll (35-star flag from 1 June) ----------
const LGD = now(legend(0, T_LIN + 1.2, true)); const LG1 = legend(TZ1 - 0.2, END + 1, false);
const D0 = dateNow("18 MAY 1863", T_19 - 0.05);
B.date("19 MAY 1863", T_19, T_22 - 0.05, 32); B.date("22 MAY 1863", T_22, T_SIEGE - 0.05, 32);
const dateF = (html, t, until) => { const box = document.getElementById("date"), d = document.createElement("div"); d.className = "d"; d.style.fontSize = "32px"; d.style.gap = "14px"; d.innerHTML = html; box.appendChild(d);
  gsap.set(d, { autoAlpha: 0 }); tl.fromTo(d, { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.4, immediateRender: false }, t); if (until != null) tl.to(d, { autoAlpha: 0, y: -14, duration: 0.35 }, until); return d; };
const F35 = `<img src="assets/media/us35_flag.png" style="height:30px;border:1px solid #1a1712;box-shadow:0 1px 3px rgba(0,0,0,.5)">`;
dateF(`${F35}<span>JUNE 1863</span>`, T_SIEGE + 0.2, T_JUL - 0.05);
dateF(`${F35}<span>4 JULY 1863</span>`, T_JUL, null);
// ---------- the siege lines (option 2: two glowing bands where the sides touch; no fill) ----------
const FR = on0(front2(FRT, S1, 0, { dur: 0.01, flip: true, until: T_JUL + 1.6 }));
tl.set(FR, { autoAlpha: 1 }, 0);
// flags: US (34 stars until 31 May, 35 from 1 June) outside the lines, the Confederacy inside the city
const FUS34 = now(flagS(FL.us, "", ...L(32.36, -90.81), 0, T_SIEGE + 0.3));
const FUS35 = flagS("assets/media/us35_flag.png", "", ...L(32.36, -90.81), T_SIEGE + 0.2, null);
const FCS = now(flagS(FL.cs, "", ...L(32.335, -90.872), 0, null)); tl.to(FCS, { opacity: 0.55, duration: 0.8 }, T_PEM + 0.6);
// units: three Union corps outside, Pemberton's army inside (his name tag from his spoken name)
U("u15", "carth", L(32.390, -90.842), "XV", "XXX"); U("u17", "carth", L(32.358, -90.826), "XVII", "XXX"); U("u13", "carth", L(32.318, -90.836), "XIII", "XXX");
U("rp", "rome", L(32.357, -90.866), "PEMBERTON", "XX", 0, { tagAt: T_PEM + 0.1 }); U("r2", "rome", L(32.375, -90.875), "", "XX"); U("r3", "rome", L(32.318, -90.874), "", "XX");
// ---------- 19 and 22 May: the assaults bounce off ----------
const AS = (pts, t, back = 1.2) => { const a = arw({ pts: LL(pts), side: "carth", t, dur: 0.7, width: AW(S1, 12), until: t + back + 0.6 }); tl.to(a, { opacity: 0.25, duration: 0.25, yoyo: true, repeat: 1 }, t + 0.8); return a; };
const A19 = [[[32.385, -90.848], [32.378, -90.856], [32.372, -90.862]], [[32.372, -90.836], [32.368, -90.846], [32.365, -90.851]]];
const A22 = [[[32.382, -90.846], [32.376, -90.857], [32.371, -90.863]], [[32.355, -90.828], [32.353, -90.839], [32.352, -90.845]], [[32.336, -90.831], [32.337, -90.842], [32.339, -90.848]],
  [[32.324, -90.840], [32.327, -90.850], [32.329, -90.854]]];
A19.forEach((p, k) => AS(p, T_19 - 0.2 + k * 0.3));
A22.forEach((p, k) => AS(p, T_22 - 0.1 + k * 0.25));
// the works fire at the attackers (visible guns, ~1 shot per second, the boom + shake on the impact)
[[T_19 + 0.5, [32.366, -90.857], [32.377, -90.852]], [T_22 + 0.6, [32.352, -90.849], [32.353, -90.838]], [T_22 + 1.5, [32.330, -90.858], [32.333, -90.842]]].forEach(([t, a, b]) => shootS(L(...a), L(...b), t, S1, { dur: 0.55, h: 26, r: 9 }));
[[T_19 + 0.9, [32.370, -90.858], [32.376, -90.850]], [T_22 + 1.0, [32.340, -90.851], [32.338, -90.843]]].forEach(([t, a, b]) => mg(L(...a), L(...b), t, 5, 1.1 / S1 * 2.2));
const FAIL = wstampL("FAILED", ...L(32.335, -90.812), T_FAIL, null, "#e3232f", 40);
// Grant later wrote that he regretted the second one (paraphrase: no quote marks)
const GRB = cmd("grant", "ULYSSES S. GRANT", "ARMY OF THE TENNESSEE", "carth", "bl", T_GW - 0.1, T_SIEGE - 0.2);
B.caption("HE REGRETTED THE SECOND ONE", T_REG - 0.2, T_SIEGE - 0.2, "carth r");
// ---------- the siege: saps creep toward the works; gunboats shell the city from the river ----------
const SAPS = [[[32.380, -90.853], [32.378, -90.857], [32.376, -90.856], [32.374, -90.860]], [[32.366, -90.840], [32.364, -90.845], [32.362, -90.844], [32.360, -90.849]],
  [[32.352, -90.834], [32.352, -90.839], [32.350, -90.840], [32.350, -90.845]], [[32.336, -90.838], [32.337, -90.843], [32.335, -90.845], [32.336, -90.849]],
  [[32.322, -90.846], [32.323, -90.851], [32.321, -90.853], [32.322, -90.857]]];
SAPS.forEach((p, k) => glowPath(LL(p), "#7fb0ff", 2.4, T_SG + k * 0.18, T_LIN + 1.0, 0, 0.9, { draw: 1.6 }));
wstampL("SIEGE", ...L(32.30, -90.83), T_SG + 0.1, null, "#9fc0ea", 36);
// ---------- 4 July: white flags, Pemberton surrendered ----------
const WFL = [];
const WF = `<svg width="30" height="34" viewBox="0 0 30 34" style="display:block;overflow:visible;filter:drop-shadow(0 0 4px #fff) drop-shadow(0 1px 2px #000)"><line x1="3" y1="2" x2="3" y2="34" stroke="#3a2c1c" stroke-width="2.4"/><path d="M4 3 Q12 0 19 4 Q24 6 28 4 L28 17 Q22 19 18 16 Q11 13 4 16 Z" fill="#fbfaf4" stroke="#8a8478" stroke-width="0.8"/></svg>`;
[[32.380, -90.866], [32.365, -90.856], [32.350, -90.851], [32.334, -90.855], [32.318, -90.867], [32.306, -90.881]].forEach(([la, lo], k) => {
  const el = pinS(GG.pin(WF, ...L(la, lo), { t: T_JUL + 0.15 + k * 0.18, pop: true })); WFL.push(el); SFX("ref:pop", T_JUL + 0.2 + k * 0.18); });
const PB = cmd("pemberton", "JOHN C. PEMBERTON", "CONFEDERATE ARMY", "rome", "tr", T_PEM - 0.1, T_295 - 0.3);
wstampL("SURRENDERED", ...L(32.345, -90.866), T_PEM + 0.4, null, "#f7f3ea", 34);
["rp", "r2", "r3"].forEach((id, k) => B.grey([id], T_PEM + 0.6 + k * 0.1, 0.8));
const POLE = poleFlag("assets/media/us35_flag.png", L(32.352, -90.880), T_172 + 0.6, END + 1, 46);
// RESULT card (STYLE_LOCK 0b: no reliable Union figure is spoken, FACTCHECK_B #23): about 29,500 men (#28) and 172 cannon (#29); spoken words only
const NUM = scr(`<div style="padding:22px 52px 22px;background:rgba(18,16,12,0.94);border-top:6px solid #c9b48a;font-family:Oswald;font-weight:700;color:#f7f3ea;text-align:center;box-shadow:0 20px 40px rgba(0,0,0,.55)">
  <div style="font-size:21px;letter-spacing:.3em;color:#c9b48a">RESULT · 4 JULY 1863</div>
  <div style="font-size:30px;letter-spacing:.12em;margin-top:6px;color:#ff8a80">PEMBERTON SURRENDERED</div>
  <div style="display:flex;gap:56px;justify-content:center;margin-top:8px">
  <div class="a"><div class="v" style="font-size:62px;line-height:1.05">~0</div><div style="font-size:20px;letter-spacing:.26em;color:#c9b48a">MEN</div></div>
  <div class="b"><div style="font-size:62px;line-height:1.05">172</div><div style="font-size:20px;letter-spacing:.26em;color:#c9b48a">CANNON</div></div></div></div>`,
  "left:0;right:0;top:215px;display:flex;justify-content:center;", T_295 - 0.2, T_LIN - 0.2);
SFX("hit", T_295 - 0.05);
{ const v = NUM.querySelector(".v"), st = { x: 0 }; tl.to(st, { x: 29500, duration: 1.0, ease: "none", onUpdate: () => { v.textContent = "~" + (Math.round(st.x / 100) * 100).toLocaleString("en-US"); } }, T_295);
  for (let k = 0; k < 6; k++) SFX("tick", T_295 + k * 0.17);
  const b = NUM.querySelector(".b"); gsap.set(b, { autoAlpha: 0 }); tl.fromTo(b, { autoAlpha: 0, scale: 1.2 }, { autoAlpha: 1, scale: 1, duration: 0.3, immediateRender: false }, T_172 - 0.1); SFX("hit", T_172); }
// ---------- Lincoln: the one zoom-out; the river turns blue top to bottom ----------
glowPath(RIVN.concat(RIVM), "#5f9bff", 260, TZ1 - 1.6, END + 1, 0, 0.75, { draw: 3.0 });   // drawn top to bottom once the camera is out
const LINC = scr(`<div style="max-width:1300px;padding:20px 44px 22px;background:rgba(18,16,12,0.93);border-left:8px solid #1f4fc4;font-family:Oswald;color:#f7f3ea;box-shadow:0 20px 40px rgba(0,0,0,.55)">
  <div style="font-size:19px;font-weight:700;letter-spacing:.3em;color:#9fc0ea">LINCOLN WROTE</div><div style="font-size:48px;font-weight:600;line-height:1.2;letter-spacing:.03em;margin-top:6px">THE FATHER OF WATERS AGAIN WENT UNVEXED TO THE SEA</div></div>`,
  "left:0;right:0;bottom:130px;display:flex;justify-content:center;", T_FATHER - 0.2, T_EVERY - 0.3);
// flags on the river map: the US north and on the river, the Confederacy on both sides of it (cut in two from July)
const MFL = [flagS("assets/media/us35_flag.png", "", ...L(33.55, -91.0), T_FATHER, END + 1), flagS(FL.cs, "", ...L(31.6, -94.2), T_FATHER + 0.1, END + 1), flagS(FL.cs, "", ...L(32.3, -87.6), T_FATHER + 0.2, END + 1)];
// ---------- m2-12: the supply line he cut; method card line 2 on the spoken words ----------
K.target(VKS[0], VKS[1], T_GATES, { r: 30 / S3, side: "carth", until: T_GATES + 2.6 });
GG.METHOD_TITLE = "GRANT'S METHOD";
GG.METHOD = ["ATTACKED THE MOMENT THE ENEMY HESITATED", "CUT HIS SUPPLY LINE · FED HIS MEN OFF THE LAND", ""];   // line 1 = move 1 (m1-9), line 2 = spoken here (m2-12)
const MC = GG.method(2, T_CUT - 0.2, T_FEW - 0.2, [T_CUT - 0.1, T_CUT + 0.1]); MC.querySelectorAll(".row").forEach((r) => { r.style.fontSize = "46px"; });
{ const r1 = MC.querySelectorAll(".row.lit")[0]; r1.style.opacity = "0.6"; }
SFX("ref:pop", T_CUT); SFX("ref:boom", T_FED);
const FEW = [L(32.35, -90.88), L(32.30, -90.19)];
K.target(FEW[0][0], FEW[0][1], T_FEW + 0.3, { r: 28 / S3, side: "carth", until: END + 0.5 });
// the siege close-up layer leaves as the camera goes out (units, flags, white flags, the pole flag stay readable only up close)
const CLOSE = [...["u15", "u17", "u13", "rp", "r2", "r3"].map((id) => B.units[id].el), FUS35, FCS, ...WFL];
CLOSE.forEach((el) => tl.to(el, { autoAlpha: 0, duration: 0.6 }, T_FATHER + 0.4));   // after the river-map flags are up (both flags on every frame)
// ---------- 1c declutter ----------
declutter([LGD, LG1, GRB, PB], [[T_295 - 0.2, T_LIN - 0.2], [T_FATHER - 0.2, T_EVERY - 0.3], [T_CUT - 0.2, T_FEW - 0.2]]);
fixImgs();
K.raiseTerritory();
B.finish();
