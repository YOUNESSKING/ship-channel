// BASEMAP: bikini_close
// Cross-section inset: landing ship LSM-60 on the surface, the bomb hanging below; '90 FT' on 'ninety'.
const S = ShipK(), B = S.B, END = S.END, wt = S.wt, P = S.P;
const BB = P("BURSTB");
S.camera([[0, BB[0] + 250, BB[1], 2.4], [END, BB[0] + 230, BB[1] + 6, 2.5]]);
S.burst(BB, 0, { r: 1 }); S.ring(BB, { t: 0.2, r: 40, color: "#f3eee2" });
const html = `<div style="position:relative;width:900px;height:560px">
<svg width="900" height="560" viewBox="0 0 900 560" style="display:block">
 <rect x="0" y="150" width="900" height="410" fill="#1f5a70" opacity=".55"/>
 <path d="M0 150 Q 75 134 150 150 T 300 150 T 450 150 T 600 150 T 750 150 T 900 150" fill="none" stroke="#f3eee2" stroke-width="5"/>
 <g id="lsm"><path d="M250 150 L270 108 L620 108 L650 130 L650 150 Z" fill="#f3eee2" stroke="#D9572B" stroke-width="5"/><rect x="300" y="82" width="90" height="26" fill="#f3eee2" stroke="#D9572B" stroke-width="4"/></g>
 <g id="bomb"><line x1="450" y1="150" x2="450" y2="300" stroke="#f3eee2" stroke-width="4" stroke-dasharray="10 8"/><ellipse cx="450" cy="335" rx="46" ry="34" fill="#D9572B" stroke="#f3eee2" stroke-width="4"/></g>
 <g id="dim"><line x1="760" y1="150" x2="760" y2="335" stroke="#f3eee2" stroke-width="4"/><path d="M748 164 L760 150 L772 164 M748 321 L760 335 L772 321" fill="none" stroke="#f3eee2" stroke-width="4"/></g>
</svg>
<div id="tLsm" style="position:absolute;left:300px;top:20px;font-size:44px;letter-spacing:.08em">LSM-60</div>
<div id="tBomb" style="position:absolute;left:330px;top:360px;font-size:44px;letter-spacing:.08em;color:#D9572B">THE BOMB</div>
<div id="tFt" style="position:absolute;left:668px;top:430px;font-size:64px;letter-spacing:.08em">90 FT</div>
<div style="position:absolute;left:0;top:178px;font-size:34px;letter-spacing:.2em;color:#8fb0cc">LAGOON SURFACE</div></div>`;
const card = S.card(html, 0.3, { left: 110, top: 230, width: 900 });
card.style.padding = "20px 20px 10px"; card.style.width = "auto";
const hide = (id, t) => { const e = card.querySelector(id); gsap.set(e, { autoAlpha: 0 }); B.tl.to(e, { autoAlpha: 1, duration: 0.4 }, t); };
hide("#tLsm", wt("landing", 0.6)); hide("#lsm", wt("landing", 0.6)); hide("#bomb", wt("hung", 0.3)); hide("#tBomb", wt("hung", 0.3)); hide("#dim", wt("ninety", 2.2)); hide("#tFt", wt("ninety", 2.2));
S.finish();
