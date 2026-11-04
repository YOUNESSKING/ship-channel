// ---------- gh kit (Grant #16 map agent hook: hook-a, hook-b), inlined by tools/gh_inline.py. Copied from patton/tools/pc_kit.js ----------
// Copied from the cleburne m23 kit (sherman move1_kit + the approved A1/A2 constant-size story layer, sherman/scenes-src/test-A2-labels.js).
// SIDES (grant/SCENES.md): Union / Grant = BLUE "carth" + US 34 stars (Feb 1862); Confederates = RED "rome" + First National (13 stars).
const B = Battle();
const { at } = B;
const END = B.T.duration;
const K = FXK(B);
const GG = GGK(B);
const E = EngageK(B);
const FL = { us: "assets/media/us34_flag.png", us35: "assets/media/us35_flag.png", csa: "assets/media/csa1_13_flag.png" };
const PHOTO = (n) => `assets/media/${n}_head.png`;
const SCN = document.getElementById("scene");
const NS = "http://www.w3.org/2000/svg";
const tl = B.tl;
const WORLD = document.getElementById("world"), OVL = document.getElementById("overlay");
const box = (txt, x, y, t, size = 16, until, o = {}) => { if (o.sfx !== false && t > 0) SFX("ref:pop", t); return GG.pin(`<div style="background:${o.bg || "#f1eee6"};color:${o.col || "#111"};font-family:Oswald;font-weight:500;letter-spacing:.2em;padding:${(size * 0.2).toFixed(1)}px ${(size * 0.35).toFixed(1)}px ${(size * 0.2).toFixed(1)}px ${(size * 0.55).toFixed(1)}px;font-size:${size}px;white-space:nowrap;box-shadow:0 ${size * 0.1}px ${size * 0.4}px rgba(0,0,0,.6)">${txt}</div>`, x, y, { t, until }); };
const flag = (src, name, x, y, t, until, w = 76) => GG.pin(`<div style="display:flex;flex-direction:column;align-items:center"><img src="${src}" style="width:${w}px;display:block;border:${Math.max(0.6, w / 60).toFixed(1)}px solid #1a1712;box-shadow:0 ${w * 0.025}px ${w * 0.07}px rgba(0,0,0,0.55)"></div>`, x, y, { t, pop: true, until });   // CLEAN SCREEN v11: no country name
const unit = (id, side, p, icon, label, o = {}) => {
  const w = o.w || 22, h = o.h || 15;
  B.unit({ id, side, x: p[0], y: p[1], w, h, t: o.t, label });
  K.counter(id, { icon, flag: o.flag || (side === "carth" ? FL.us : FL.csa), size: o.size });
  const u = B.units[id]; u.el.querySelector(".blk").style.borderWidth = Math.max(0.6, w / 14).toFixed(2) + "px";
  const tg = u.el.querySelector(".tag"); if (tg) Object.assign(tg.style, { fontSize: (o.tag || h * 0.55).toFixed(1) + "px", padding: `0 ${(h * 0.22).toFixed(1)}px`, marginTop: (h * 0.12).toFixed(1) + "px", whiteSpace: "nowrap" });
  const sz = u.el.querySelector(".fxk-size"); if (sz) sz.style.fontSize = Math.max(3, h * 0.42).toFixed(1) + "px";
  if (o.until != null) B.hideUnits([id], o.until);
  return id;
};
const arw = (o) => { const g = B.arrow(o), w = o.width || 22, ps = g.querySelectorAll("path");
  ps[0].setAttribute("stroke-width", (w + Math.min(10, w * 0.6)).toFixed(1)); if (o.dash) ps[0].setAttribute("stroke-dasharray", o.dash);
  const hd = g.querySelector("polygon"); if (hd) hd.setAttribute("stroke-width", Math.min(5, w * 0.3).toFixed(1)); return g; };
// legend: UNION (blue) / CONFEDERACY (red); opt2 = two short glowing lines instead of squares
const legend = (t, until, opt2) => GG.card(`<div style="display:flex;gap:26px;font-size:20px;letter-spacing:0.1em;align-items:center">${[["#2e5cb2", "#2c57b7", "UNION"], ["#be3a2a", "#bc2528", "CONFEDERACY"]].map(([sq, ln, nm]) => `<span><b style="display:inline-block;width:${opt2 ? 30 : 20}px;height:${opt2 ? 7 : 20}px;background:${opt2 ? ln : sq};${opt2 ? `box-shadow:0 0 8px ${ln},0 0 3px #fff;vertical-align:4px;` : "vertical-align:-3px;border:1px solid #f7f3ea;"}margin-right:8px"></b>${nm}</span>`).join("")}</div>`, "", 34, t, until);
const ctlImg = (file, t, until, dur = 1.0) => { const el = B.image(file, 0, 0, 2880, 1620, { t, dur, until }); el.style.mixBlendMode = "multiply"; return el; };
const posOn = (pts, f) => { let Lt = 0; const seg = []; for (let j = 1; j < pts.length; j++) { const d = Math.hypot(pts[j][0] - pts[j - 1][0], pts[j][1] - pts[j - 1][1]); seg.push(d); Lt += d; }
  let d = f * Lt; for (let j = 0; j < seg.length; j++) { if (d <= seg[j]) { const a = pts[j], b = pts[j + 1], k = d / seg[j]; return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]; } d -= seg[j]; }
  return pts[pts.length - 1]; };
const sub = (pts, f0, f1, n = 16) => [...Array(n + 1)].map((_, k) => posOn(pts, f0 + (f1 - f0) * k / n));
// artillery shot: the gun fires (quiet), shell arc, the impact carries the boom + the locked shake (never switched off)
const shoot = (from, to, t, o = {}) => {
  K.gun(from[0], from[1], t, { unit: o.unit, dx: o.dx || 0, dy: o.dy || -2 });
  const dur = o.dur || 1.0;
  GG.arc(from[0], from[1], to[0], to[1], t + 0.05, { dur, width: o.width || 1.2, h: o.h, impact: false, color: o.color });
  K.impact(to[0], to[1], t + 0.05 + dur, { r: o.r || 5, puffs: 2 });
};
const badge = (o) => {   // K.badge + initials (shown if no photo / photo missing)
  const el = K.badge(o), ring = el.querySelector("div[style*='border-radius:50%']"), img = ring.querySelector("img");
  if (img) { const ini = document.createElement("div"); ini.style.cssText = "position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle, rgba(10,12,24,0.78) 0%, rgba(10,12,24,0.45) 100%);font-size:60px;font-weight:700;color:#f7f3ea;text-shadow:0 3px 6px #000";
    ini.textContent = o.initials || ""; ini.style.display = "none"; ring.insertBefore(ini, img); img.addEventListener("error", () => { img.style.display = "none"; ini.style.display = "flex"; }); }
  return el;
};
const stampHTML = (txt, c, size, rot, sub) => `<div style="transform:rotate(${rot}deg);display:inline-block;text-align:center;font-family:Oswald;font-weight:700;color:${c};border:${Math.max(1, Math.round(size / 9))}px solid ${c};padding:${(size * 0.1).toFixed(1)}px ${(size * 0.5).toFixed(1)}px ${(size * 0.14).toFixed(1)}px;background:rgba(14,12,10,0.78);box-shadow:0 ${size * 0.2}px ${size * 0.5}px rgba(0,0,0,.55);white-space:nowrap"><div style="font-size:${size}px;letter-spacing:0.12em;line-height:1.1;-webkit-text-stroke:${c === "#f7f3ea" ? "1.5px #000" : "0"}">${txt}</div>${sub ? `<div style="font-size:${(size * 0.34).toFixed(1)}px;letter-spacing:0.2em;color:#f7f3ea;margin-top:${size * 0.05}px">${sub}</div>` : ""}</div>`;
// grey a badge + slam a small stamp on it (RESIGNED / SUPPRESSED)
const badgeStamp = (el, txt, t, o = {}) => {
  const ring = el.querySelector("div[style*='border-radius:50%']");
  if (o.grey !== false) tl.to(ring, { filter: "grayscale(1) brightness(0.6)", duration: 0.4 }, t);
  const st = document.createElement("div"); st.innerHTML = stampHTML(txt, o.color || "#e3232f", o.size || 30, -8);
  st.style.cssText = "position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:5";
  ring.style.overflow = "visible"; ring.appendChild(st);
  tl.fromTo(st, { autoAlpha: 0, scale: 2.2 }, { autoAlpha: 1, scale: 1, duration: 0.22, ease: "power4.in", immediateRender: false }, t);
  SFX("hit", t + 0.2); K.shake(t + 0.2, 3, 0.25); return st;
};
const glowPath = (pts, col, w, t, until, pulses = 3, op = 0.95, o = {}) => {   // glowing stroke (creek, road, ridge, railroad), pulses then holds
  const p = document.createElementNS(NS, "path");
  p.setAttribute("d", "M" + pts.map((q) => q.join(" ")).join(" L")); p.setAttribute("fill", "none"); p.setAttribute("stroke", col);
  p.setAttribute("stroke-width", w); p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-linejoin", "round"); p.style.filter = `drop-shadow(0 0 ${w}px ${col})`;
  if (o.dash) p.setAttribute("stroke-dasharray", o.dash);
  if (o.top) OVL.appendChild(p); else OVL.insertBefore(p, OVL.firstChild); gsap.set(p, { opacity: 0 });
  if (o.draw) { let Lt = 0; for (let j = 1; j < pts.length; j++) Lt += Math.hypot(pts[j][0] - pts[j - 1][0], pts[j][1] - pts[j - 1][1]);
    gsap.set(p, { strokeDasharray: `${Lt} ${Lt + 10}`, strokeDashoffset: Lt }); tl.to(p, { strokeDashoffset: 0, duration: o.draw, ease: "power1.inOut" }, t); }
  tl.to(p, { opacity: op, duration: 0.5 }, t); if (pulses) tl.to(p, { opacity: op * 0.45, duration: 0.5, yoyo: true, repeat: pulses, ease: "sine.inOut" }, t + 0.5 + (o.draw || 0));
  if (until != null) tl.to(p, { opacity: 0, duration: 0.6 }, until); return p;
};
const scr = (html, css, t, until, from = { autoAlpha: 0, y: 30 }) => {   // screen-space element (above the map, under the credit)
  const el = document.createElement("div"); el.style.cssText = "position:absolute;" + css; el.innerHTML = html;
  SCN.insertBefore(el, document.getElementById("credit")); GG.hide(el);
  tl.fromTo(el, from, { autoAlpha: 1, y: 0, x: 0, duration: 0.5, ease: "power3.out" }, t); if (until != null) tl.to(el, { autoAlpha: 0, duration: 0.5 }, until); return el;
};
const trail = (pts, col, w, t, dur, until, dash = "2 9") => {   // a dotted trail drawn along a path over [t, t + dur]
  const p = document.createElementNS(NS, "path");
  p.setAttribute("d", "M" + pts.map((q) => q.join(" ")).join(" L")); p.setAttribute("fill", "none"); p.setAttribute("stroke", col);
  p.setAttribute("stroke-width", w); p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-linejoin", "round");
  p.style.filter = `drop-shadow(0 0 ${w * 0.8}px ${col})`; OVL.appendChild(p);
  let Lt = 0; for (let j = 1; j < pts.length; j++) Lt += Math.hypot(pts[j][0] - pts[j - 1][0], pts[j][1] - pts[j - 1][1]);
  const m = document.createElementNS(NS, "mask"), id = "trm" + (window.__trm = (window.__trm || 0) + 1);
  m.setAttribute("id", id); m.setAttribute("maskUnits", "userSpaceOnUse");
  const mp = p.cloneNode(); mp.setAttribute("stroke", "#fff"); mp.style.filter = ""; mp.setAttribute("stroke-width", w * 4); mp.removeAttribute("stroke-dasharray");
  m.appendChild(mp); OVL.appendChild(m); p.setAttribute("stroke-dasharray", dash); p.setAttribute("mask", `url(#${id})`);
  gsap.set(mp, { strokeDasharray: `${Lt} ${Lt + 20}`, strokeDashoffset: Lt }); gsap.set(p, { opacity: 0 });
  tl.set(p, { opacity: 1 }, t); tl.to(mp, { strokeDashoffset: 0, duration: dur, ease: "none" }, t);
  if (until != null) tl.to(p, { opacity: 0, duration: 0.6 }, until); return p;
};
const along = (id, pts, t, dur, n = 24) => { for (let k = 1; k <= n; k++) { const q = posOn(pts, k / n); B.move(id, t + (k - 1) * dur / n, dur / n, q[0], q[1], "none"); } };
// a counter that ticks up (screen space)
const ticker = (label, to, suffix, css, t, dur, until, n = 8, o = {}) => {
  const el = scr(`<div style="padding:10px 26px 12px;background:rgba(18,16,12,0.9);border-top:5px solid ${o.col || "#c9b48a"};font-family:Oswald;font-weight:700;color:#f7f3ea;text-align:center">
    <div style="font-size:18px;letter-spacing:.3em;color:${o.col || "#c9b48a"}">${label}</div><div class="v" style="font-size:54px;letter-spacing:.04em">${o.pre || ""}0${suffix}</div>${o.sub ? `<div style="font-size:15px;letter-spacing:.22em;color:#d8cfb8">${o.sub}</div>` : ""}</div>`, css, t, until);
  const v = el.querySelector(".v"), st = { x: 0 };
  tl.to(st, { x: to, duration: dur, ease: "none", onUpdate: () => { v.textContent = (o.pre || "") + Math.round(st.x).toLocaleString("en-US") + suffix; } }, t + 0.2);
  for (let k = 0; k < n; k++) SFX("tick", t + 0.2 + (k * dur) / n);
  return el;
};
// rifle volley: little tracer dashes (mg sound), sparingly
const mg = (a, b, t, n = 5, w = 1.1) => { SFX("mg", t);
  for (let k = 0; k < n; k++) { const g = document.createElementNS(NS, "line"), j = ((k * 7) % 5 - 2) * 1.5 * w;
    g.setAttribute("x1", a[0]); g.setAttribute("y1", a[1]); g.setAttribute("x2", b[0] + j); g.setAttribute("y2", b[1] - j);
    g.setAttribute("stroke", "#ffe28a"); g.setAttribute("stroke-width", w); g.setAttribute("stroke-linecap", "round"); g.setAttribute("stroke-dasharray", `${3 * w} ${26 * w}`);
    g.style.filter = `drop-shadow(0 0 ${2 * w}px #ffb347)`; OVL.appendChild(g); GG.hide(g);
    const len = Math.hypot(b[0] - a[0], b[1] - a[1]) + 29 * w;
    tl.fromTo(g, { autoAlpha: 1, strokeDashoffset: 0 }, { strokeDashoffset: -len, duration: 0.4, ease: "none", immediateRender: false }, t + k * 0.1);
    tl.to(g, { autoAlpha: 0, duration: 0.05 }, t + k * 0.1 + 0.4); } };
const slam = (el, t, o = {}) => {
  tl.fromTo(el, { autoAlpha: 0, scale: o.from || 2.2 }, { autoAlpha: 1, scale: 1, duration: o.dur || 0.24, ease: "power4.in", immediateRender: false }, t);
  const tHit = t + (o.dur || 0.24) - 0.02;
  if (o.sfx !== false) SFX(o.sfx || "hit", tHit);
  if (o.shake !== false) K.shake(tHit, o.shake || 4, 0.3);
  if (o.until != null) tl.to(el, { autoAlpha: 0, duration: 0.35 }, o.until);
  return el;
};
const sstamp = (txt, top, t, o = {}) => { const el = scr(stampHTML(txt, o.color || "#e3232f", o.size || 60, o.rot || -5, o.sub), `left:0;right:0;top:${top}px;display:flex;justify-content:center;`, t, null, { autoAlpha: 0 }); return slam(el, t, o); };
const wstamp = (txt, x, y, t, until, c = "#e3232f", size = 9, sub) => { const el = GG.pin(stampHTML(txt, c, size, -6, sub), x, y, {});
  tl.fromTo(el, { autoAlpha: 0, scale: 2 }, { autoAlpha: 1, scale: 1, duration: 0.2, ease: "power4.in", immediateRender: false }, t);
  SFX("hit", t + 0.18); K.shake(t + 0.18, 3, 0.25); if (until != null) tl.to(el, { autoAlpha: 0, duration: 0.3 }, until); return el; };
// quote card (screen space): verbatim quote + attribution (quote marks only on verbatim text)
const quote = (txt, who, t, until, o = {}) => scr(`<div style="max-width:${o.mw || 1280}px;padding:22px 46px 22px;background:rgba(18,16,12,0.93);border-left:8px solid ${o.col || "#1f4fc4"};font-family:Oswald;color:#f7f3ea;box-shadow:0 20px 40px rgba(0,0,0,.55)">
  <div style="font-size:${o.size || 40}px;font-weight:500;line-height:1.28;letter-spacing:.02em">${txt}</div><div style="font-size:19px;font-weight:700;letter-spacing:.24em;color:#9fc0ea;margin-top:12px">${who}</div></div>`,
  `left:0;right:0;top:${o.top || 150}px;display:flex;justify-content:center;`, t, until);
// belief card (red, what the enemy thought)
const belief = (txt, sub, t, until, o = {}) => scr(`<div style="padding:16px 40px 18px;background:rgba(18,16,12,0.93);border-top:6px solid #c4121f;font-family:Oswald;font-weight:700;color:#f7f3ea;text-align:center;box-shadow:0 20px 40px rgba(0,0,0,.55)">
  <div style="font-size:17px;letter-spacing:.32em;color:#ff8a80">${sub}</div><div style="font-size:${o.size || 46}px;letter-spacing:.08em;margin-top:4px">${txt}</div></div>`,
  `left:0;right:0;top:${o.top || 150}px;display:flex;justify-content:center;`, t, until);
const fixImgs = () => document.querySelectorAll("img").forEach((im) => { im.addEventListener("error", () => { im.style.display = "none"; }, { once: true }); });
// small locomotive (side view, glowing headlamp) running along a rail polyline
const pinAlong = (el, pts, t, dur, n = 24) => { for (let k = 1; k <= n; k++) { const q = posOn(pts, k / n); tl.to(el, { left: q[0], top: q[1], duration: dur / n, ease: "none" }, t + (k - 1) * dur / n); } };
const wagon = (pts, t, dur, until, o = {}) => { const s = o.s || 14;   // supply wagon (side view)
  const el = GG.pin(`<svg width="${s * 2}" height="${s * 1.3}" viewBox="0 0 40 26" style="display:block;overflow:visible;filter:drop-shadow(0 0 ${s * 0.25}px ${o.glow || "#9fc0ff"})">
    <path d="M6 14 Q6 2 20 2 Q34 2 34 14 Z" fill="#efe6cf" stroke="#2a2420" stroke-width="1.6"/><rect x="4" y="13" width="32" height="5" fill="#6b4a2a" stroke="#2a2420" stroke-width="1.2"/>
    <circle cx="11" cy="21" r="4" fill="none" stroke="#efe6cf" stroke-width="2"/><circle cx="29" cy="21" r="4" fill="none" stroke="#efe6cf" stroke-width="2"/></svg>`, pts[0][0], pts[0][1], { t, until });
  pinAlong(el, pts, t, dur, 24); return el; };
// fire glow over a burning bridge / place
const fireGlow = (x, y, r, t, until) => { const el = GG.pin(`<div style="width:${r * 2}px;height:${r * 2}px;border-radius:50%;background:radial-gradient(circle,rgba(255,200,90,.85) 0%,rgba(255,110,20,.55) 35%,rgba(200,40,0,.25) 60%,rgba(120,20,0,0) 75%);mix-blend-mode:screen"></div>`, x, y, { t, until });
  tl.to(el.firstElementChild, { scale: 1.15, opacity: 0.75, duration: 0.35, yoyo: true, repeat: Math.max(1, Math.round(((until || t + 8) - t) / 0.35)), ease: "sine.inOut" }, t + 0.5); return el; };
const nightWash = (t, until, a = 0.5) => { const el = document.createElement("div"); el.style.cssText = `position:absolute;inset:0;background:rgba(6,10,26,${a});pointer-events:none`;
  document.getElementById("fx").appendChild(el); gsap.set(el, { autoAlpha: 0 }); tl.to(el, { autoAlpha: 1, duration: 1.2 }, t); if (until != null) tl.to(el, { autoAlpha: 0, duration: 1.5 }, until); return el; };
// cavalry counter icon (owner-approved, sherman/scenes-src/cavalry_icon.js)
const CAV_SVG = `<g fill="#f7f3ea" stroke="none">
  <path d="M25 43 C16 41 9 47 5 56 C11 52 17 50 24 50 Z"/>
  <path d="M24 44 C28 37 40 36 52 38 L66 37 C70 34 74 28 78 22 L84 17 L86 11 L88.5 18.5 L96 29 L94.5 34.5 L88 33 L82.5 32 C80.5 38 78.5 44 76.5 48 C76.5 54 72 58 66 58 L36 58 C30 58 25 54 24 48 Z"/>
  <path d="M46 38.5 L54 38.5 L58 23 L47.5 20 Z"/>
  <circle cx="52" cy="14" r="5"/><ellipse cx="51.5" cy="9.6" rx="7" ry="2.2"/></g>
  <g fill="none" stroke="#f7f3ea" stroke-linecap="round" stroke-linejoin="round">
  <path d="M69 55 L81 63 L90 61" stroke-width="5"/><path d="M64 56 L73 66 L72 75" stroke-width="5"/>
  <path d="M35 55 L23 63 L13 65" stroke-width="5"/><path d="M41 56 L37 68 L41 76" stroke-width="5"/>
  <path d="M51 35 L59 43 L57 51" stroke-width="5"/>
  <path d="M54 25 L65 20" stroke-width="4.5"/><path d="M65 20 L79 3" stroke-width="2.6"/></g>`;
const cavIcon = (id, o = {}) => { const sv = B.units[id].el.querySelector(".blk svg");
  sv.setAttribute("viewBox", "0 0 100 80"); sv.setAttribute("preserveAspectRatio", "xMidYMid meet");
  sv.innerHTML = o.flip ? `<g transform="translate(100 0) scale(-1 1)">${CAV_SVG}</g>` : CAV_SVG; };
// K.front with its OWN blur filter (lib/fx.js shares one blur filter sized by the first front; HANDOVER Sherman lesson 4)
let __FID = 0;
const frontS = (o) => { const g = K.front(o), id = "pcblur" + (++__FID), f = document.createElementNS(NS, "filter");
  f.setAttribute("id", id); f.setAttribute("x", "-20%"); f.setAttribute("y", "-20%"); f.setAttribute("width", "140%"); f.setAttribute("height", "140%");
  f.innerHTML = `<feGaussianBlur stdDeviation="${((o.width || 15) * 0.35).toFixed(2)}"/>`; OVL.querySelector("defs").appendChild(f);
  g.querySelectorAll("[filter]").forEach((p) => p.setAttribute("filter", `url(#${id})`)); return g; };
// the method card (one line per move): PATTON'S METHOD (script end-1)
GG.METHOD = ["ATTACK WHILE THE ENEMY IS STILL DECIDING", "GO WHERE HE SAYS YOU CANNOT", "NEVER GIVE HIM THE TIME TO CATCH HIS BREATH"];
GG.METHOD_TITLE = "GRANT'S METHOD";
const method = (lit, t, until, tLine) => { const mc = GG.method(lit, t, until, [...Array(lit)].map((_, i) => (i === lit - 1 ? tLine : t + 0.2)));
  mc.querySelectorAll(".row").forEach((r) => { r.style.fontSize = "52px"; });
  tl.fromTo(mc.querySelectorAll(".row.lit")[lit - 1], { scale: 1 }, { scale: 1.06, color: "#8fb2ff", duration: 0.3, yoyo: true, repeat: 1, immediateRender: false }, tLine + 0.5);
  SFX("hit", tLine + 0.5); return mc; };
// the OLD clean casualty card (lib/fx.js K.casualties; owner 2026-10-29): column A = Allies (blue), B = Germans (red); + a small source line
const casualties = (rows, foot, t, until, top = 230) => { const el = K.casualties({ rows, flagA: FL.us, headA: "UNION", flagB: FL.csa, headB: "CONFEDERATE", t, until, top });
  const f = document.createElement("div"); f.style.cssText = "font-family:Oswald;font-size:16px;letter-spacing:.2em;color:#a8a294;text-align:center;margin-top:10px;width:100%";
  f.textContent = foot; const inner = el.firstElementChild; inner.style.flexWrap = "wrap"; inner.style.maxWidth = "900px"; inner.style.justifyContent = "center"; inner.appendChild(f);
  return el; };
// ================= A1/A2 constant on-screen story layer (sherman/scenes-src/test-A2-labels.js, owner-approved 2026-10-29) =================
const SCL = []; let CAM_S = 1;
const setInv = () => { const k = (1 / CAM_S).toFixed(4); SCL.forEach((el) => { el.style.transform = `scale(${k})`; }); };
const CAM = { cx: 1440, cy: 810, s: 1 };
const camera = (keys) => {
  const cam = CAM; cam.cx = keys[0][1]; cam.cy = keys[0][2]; cam.s = keys[0][3]; const clamp = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
  const apply = () => { const s = Math.max(cam.s, 1920 / 2880), cx = clamp(cam.cx, 960 / s, 2880 - 960 / s), cy = clamp(cam.cy, 540 / s, 1620 - 540 / s);
    gsap.set(WORLD, { x: 960 - cx * s, y: 540 - cy * s, scale: s }); CAM_S = s; setInv(); };
  apply();
  for (let i = 1; i < keys.length; i++) { const [t0] = keys[i - 1], [t1, cx, cy, s] = keys[i];
    tl.to(cam, { cx, cy, s, duration: Math.max(t1 - t0, 0.01), ease: keys[i][4] || "sine.inOut", onUpdate: apply }, t0); }
  tl.call(apply, null, 0);
};
const reg = (el, origin = "50% 50%") => { el.style.transformOrigin = origin; SCL.push(el); return el; };
const pinS = (el) => { reg(el.firstElementChild); return el; };
const boxS = (txt, x, y, t, until, o = {}) => pinS(box(txt, x, y, t, 2 * (o.size || 16) * 0.9, until, o));   // story-place labels (~29 px)
const flagS = (src, name, x, y, t, until) => pinS(flag(src, name, x, y, t, until, 104));                   // ~104 px flag on screen (no name: v11)
const wstampS = (txt, x, y, t, until, c, size = 22, sub) => pinS(wstamp(txt, x, y, t, until, c, size, sub));
const unitS = (id, side, p, icon, label, o = {}) => {                               // counter 54 x 36 px, name 19 px, on screen
  const W0 = o.w || 54, H0 = o.h || 36;
  unit(id, side, p, icon, label, { ...o, w: W0, h: H0, tag: o.tag || 19 });
  const el = B.units[id].el, inner = document.createElement("div");
  inner.style.cssText = `position:relative;width:${W0}px;display:flex;flex-direction:column;align-items:center;overflow:visible`;
  while (el.firstChild) inner.appendChild(el.firstChild); el.appendChild(inner); reg(inner, `50% ${H0 / 2}px`);
  return id;
};
// A2 town label: dot + ~36 px name, constant on screen; shrinks to the old small size (o.small) when troops come near
const town = (nm, p, side = "r", t = 0, o = {}) => { const lft = side === "l";
  const el = GG.pin(`<div style="position:relative;width:0;height:0"><div style="position:absolute;left:-7px;top:-7px;width:14px;height:14px;border-radius:50%;background:#f0ece2;box-shadow:0 0 0 3px rgba(10,14,16,.75)"></div><div class="tn" style="position:absolute;top:-24px;${lft ? "right:16px" : "left:16px"};font-family:Oswald;font-weight:700;font-size:36px;letter-spacing:.06em;color:#f0ece2;white-space:nowrap;text-shadow:0 0 6px #0a0e10,0 0 3px #0a0e10,0 2px 4px #000;transform-origin:${lft ? "100%" : "0%"} 50%">${nm}</div></div>`, p[0], p[1], { t });
  tl.set(el, { autoAlpha: 1 }, t); pinS(el);
  if (o.shrink) o.shrink.forEach(([t0, t1]) => { const tn = el.querySelector(".tn"); tl.to(tn, { scale: 0.5, opacity: 0.7, duration: 0.6 }, t0); if (t1 != null) tl.to(tn, { scale: 1, opacity: 1, duration: 0.6 }, t1); });
  if (o.until != null) tl.to(el, { autoAlpha: 0, duration: 0.5 }, o.until);
  return el; };
const showU = (ids, t) => ids.forEach((id) => tl.to(B.units[id].el, { autoAlpha: 1, duration: 0.4 }, t));
const hideU = (ids, t) => ids.forEach((id) => tl.to(B.units[id].el, { autoAlpha: 0, duration: 0.4 }, t));
const AW = (s, px = 13) => +(px / s).toFixed(2);        // arrow width ~13 px on screen at camera scale s
const FW = (s) => +(15 * 1.3 / s).toFixed(2);           // locked front width 15 on screen (15 * 1.3 / s on close-ups)
// brush pile icon (cut brush hiding the guns), world space, constant on screen
const brush = (x, y, t, until, s = 40) => pinS(GG.pin(`<svg width="${s}" height="${s * 0.7}" viewBox="0 0 40 28" style="display:block;overflow:visible;filter:drop-shadow(0 2px 3px rgba(0,0,0,.7))">
  ${[[8, 18, 9], [18, 13, 11], [29, 17, 9], [14, 21, 7], [25, 22, 8]].map(([cx, cy, r]) => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="#3f5a2a" stroke="#9fc06a" stroke-width="1.3"/>`).join("")}
  ${[[6, 10, 12, 22], [20, 4, 20, 22], [33, 9, 28, 22], [12, 6, 16, 20], [27, 5, 24, 20]].map(([a, b, c, d]) => `<line x1="${a}" y1="${b}" x2="${c}" y2="${d}" stroke="#6b4a2a" stroke-width="1.6"/>`).join("")}</svg>`, x, y, { t, pop: true, until }));
// prisoners icon (bars)
const bars = (x, y, t, until, s = 40) => pinS(GG.pin(`<svg width="${s}" height="${s}" viewBox="0 0 100 100" style="display:block;filter:drop-shadow(0 2px 3px rgba(0,0,0,.7))"><rect x="8" y="8" width="84" height="84" rx="6" fill="rgba(20,16,12,.85)" stroke="#f7f3ea" stroke-width="7"/><g fill="#f7f3ea"><rect x="28" y="8" width="8" height="84"/><rect x="46" y="8" width="8" height="84"/><rect x="64" y="8" width="8" height="84"/></g></svg>`, x, y, { t, pop: true, until }));
// fallen counter (grey, small): the dead in the ravine
const fallen = (x, y, t, until) => pinS(GG.pin(`<div style="width:30px;height:19px;background:#8a867c;border:2px solid #1e1a14;opacity:.9;box-shadow:0 2px 4px rgba(0,0,0,.6);transform:rotate(${(x * 7) % 40 - 20}deg)"></div>`, x, y, { t, until }));
// camera-relative helper: world point at screen (sx, sy) for a camera key [cx, cy, s]
const W2 = (c, sx, sy) => { const s = Math.max(c[2], 1920 / 2880), cx = Math.min(Math.max(c[0], 960 / s), 2880 - 960 / s), cy = Math.min(Math.max(c[1], 540 / s), 1620 - 540 / s); return [cx + (sx - 960) / s, cy + (sy - 540) / s]; };
// ---------- end of kit ----------
// ================= Patton move 2 additions (map agent B) =================
// rivers traced from the DEM (GD from tools/m2b_inline.py): streams faint, rivers + shimmer (living map)
const drawRivers = (o = {}) => {
  const add = (pts, col, w) => { const p = document.createElementNS(NS, "path"); p.setAttribute("d", "M" + pts.map((q) => q.join(" ")).join(" L"));
    p.setAttribute("fill", "none"); p.setAttribute("stroke", col); p.setAttribute("stroke-width", w); p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-linejoin", "round"); OVL.insertBefore(p, OVL.firstChild); };
  if (o.streams !== false) (GD.streams || []).forEach((pts) => add(pts, "rgba(120,170,215,0.42)", o.sw || 0.8));
  (GD.rivers || []).forEach((pts) => add(pts, "rgba(120,170,215,0.85)", o.rw || 1.7));
  const LV = LivingK(B); LV.clouds({ n: 6, opacity: o.clouds != null ? o.clouds : 0.14 }); LV.shimmer(GD.rivers || [], { width: (o.rw || 1.7) * 0.6 });
  if (o.mpp) LV.scaleBar(o.mpp); LV.north(); return LV;
};
// option-2 front (two glowing colour bands, Confederate on side A = left of travel) with its own blur, constant on-screen width at camera s
const front2 = (pts, s, t, o = {}) => frontS({ pts, sideA: o.flip ? "carth" : "rome", sideB: o.flip ? "rome" : "carth", width: o.width || FW(s), t, dur: o.dur || 1.6, until: o.until, to: o.to, moveT: o.moveT, moveDur: o.moveDur });
// vehicle (top view) with glowing headlights driving a path (constant on screen); heading follows the road
const VEH = (s, lights) => `<div><svg width="${s * 2.4}" height="${s * 1.2}" viewBox="-20 -10 40 20" style="display:block;overflow:visible">
  ${lights ? `<defs><radialGradient id="hl" cx="0" cy="0.5" r="1"><stop offset="0" stop-color="rgba(255,240,180,0.85)"/><stop offset="1" stop-color="rgba(255,240,180,0)"/></radialGradient></defs><polygon points="8,-4 24,-9 24,9 8,4" fill="url(#hl)"/>` : ""}
  <rect x="-11" y="-4.5" width="20" height="9" rx="2" fill="#e9eef8" stroke="#1f4fc4" stroke-width="1.8" style="filter:drop-shadow(0 0 2px #6f9bff)"/><rect x="2" y="-3.6" width="6" height="7.2" rx="1" fill="#1f4fc4" opacity="0.8"/>
  ${lights ? `<circle cx="9" cy="-2.6" r="1.5" fill="#fff6c8" style="filter:drop-shadow(0 0 2px #ffe9a0)"/><circle cx="9" cy="2.6" r="1.5" fill="#fff6c8" style="filter:drop-shadow(0 0 2px #ffe9a0)"/>` : ""}</svg></div>`;
const vehicle = (pts, t, dur, until, o = {}) => {
  const el = GG.pin(VEH(o.s || 12, o.lights !== false), pts[0][0], pts[0][1], { t, until }); pinS(el);
  const inner = el.firstElementChild, n = o.n || 30;
  for (let k = 1; k <= n; k++) { const a = posOn(pts, (k - 1) / n), b = posOn(pts, k / n), ang = Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI;
    if (k === 1) gsap.set(inner.querySelector("svg"), { rotation: ang });
    tl.to(el, { left: b[0], top: b[1], duration: dur / n, ease: "none" }, t + (k - 1) * dur / n);
    tl.to(inner.querySelector("svg"), { rotation: ang, duration: Math.min(0.3, dur / n), ease: "none" }, t + (k - 1) * dur / n); }
  return el; };
// supply bundle under a parachute: pops under a passing plane, drifts down onto the ground, then fades
const bundle = (x, y, t, until, o = {}) => { const s = o.s || 30, c = o.color || "#f3eee2";
  const el = pinS(GG.pin(`<svg width="${s}" height="${s * 1.15}" viewBox="0 0 40 46" style="display:block;overflow:visible;filter:drop-shadow(0 2px 2px rgba(0,0,0,.7))"><path d="M4 18 Q20 -4 36 18 Z" fill="${c}" stroke="#1f4fc4" stroke-width="2.4"/><line x1="5" y1="18" x2="20" y2="34" stroke="#f3eee2" stroke-width="1.4"/><line x1="35" y1="18" x2="20" y2="34" stroke="#f3eee2" stroke-width="1.4"/><rect x="14" y="33" width="12" height="10" fill="#8a6a44" stroke="#f3eee2" stroke-width="1.4"/></svg>`, x, y, { t: null, until }));
  tl.fromTo(el, { autoAlpha: 0, scale: 0.3, y: -18 }, { autoAlpha: 1, scale: 1, y: 0, duration: 1.4, ease: "power1.out", immediateRender: false }, t);
  return el; };
// rain streaks over the screen (fog + rain beat): deterministic, finite repeats
const rain = (t, until, op = 0.5) => { const layer = document.createElement("div"); layer.style.cssText = "position:absolute;inset:0;overflow:hidden;pointer-events:none";
  const tall = document.createElement("div"); tall.style.cssText = "position:absolute;left:0;top:0;width:2200px;height:2160px;";
  let sd = 31; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < 320; i++) { const x = r() * 2200 - 140, y = r() * 1080, h = 18 + r() * 26;
    for (const dy of [0, 1080]) { const f = document.createElement("div"); f.style.cssText = `position:absolute;left:${x.toFixed(0)}px;top:${(y + dy).toFixed(0)}px;width:1.6px;height:${h.toFixed(0)}px;background:rgba(220,230,240,0.55);transform:rotate(14deg)`; tall.appendChild(f); } }
  layer.appendChild(tall); document.getElementById("fx").appendChild(layer); GG.hide(layer);
  tl.to(layer, { autoAlpha: op, duration: 0.8 }, t); const per = 0.9, reps = Math.max(0, Math.ceil((until - t) / per) - 1);
  tl.fromTo(tall, { y: -1080, x: 0 }, { y: 0, x: -260, duration: per, ease: "none", repeat: reps }, t); tl.to(layer, { autoAlpha: 0, duration: 1.0 }, until); return layer; };
// fog bank (screen space, drifting)
const fogBank = (t, until, op = 0.6) => { const el = document.createElement("div");
  el.style.cssText = "position:absolute;left:-200px;top:0;width:2320px;height:1080px;pointer-events:none;background:radial-gradient(ellipse 50% 38% at 25% 55%, rgba(214,218,222,0.9), rgba(214,218,222,0) 70%), radial-gradient(ellipse 45% 40% at 72% 40%, rgba(214,218,222,0.85), rgba(214,218,222,0) 70%), radial-gradient(ellipse 40% 30% at 55% 85%, rgba(214,218,222,0.8), rgba(214,218,222,0) 70%), rgba(200,204,208,0.32)";
  document.getElementById("fx").appendChild(el); GG.hide(el);
  tl.fromTo(el, { autoAlpha: 0, x: -60 }, { autoAlpha: op, x: 0, duration: 2.2, ease: "sine.out", immediateRender: false }, t);
  tl.to(el, { x: 120, duration: Math.max(1, until - t), ease: "none" }, t + 2.2); tl.to(el, { autoAlpha: 0, duration: 2.0 }, until); return el; };
// phone call card (screen): telephone icon + caller line, radio static
const PHONE = `<svg width="44" height="44" viewBox="0 0 24 24" style="display:block;filter:drop-shadow(0 2px 3px #000)"><path fill="#f7f3ea" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>`;
const phone = (who, css, t, until) => { const el = scr(`<div style="display:flex;align-items:center;gap:14px;padding:10px 22px 10px 16px;background:rgba(18,16,12,0.92);border-left:6px solid #c9b48a;font-family:Oswald;font-weight:700;color:#f7f3ea;letter-spacing:.14em;font-size:24px">${PHONE}<span>${who}</span></div>`, css, t, until, { autoAlpha: 0, x: -80 });
  tl.to(el.querySelector("svg"), { rotation: 12, duration: 0.07, yoyo: true, repeat: 9, ease: "none" }, t + 0.2); SFX("static", t + 0.1); return el; };
// small screen card: kicker + big text (e.g. VERDUN · 11:00)
const placeCard = (kick, txt, css, t, until, icon = "") => scr(`<div style="display:flex;align-items:center;gap:16px;padding:12px 26px 14px;background:rgba(18,16,12,0.92);border-top:5px solid #c9b48a;font-family:Oswald;font-weight:700;color:#f7f3ea;box-shadow:0 14px 30px rgba(0,0,0,.6)">${icon}<div><div style="font-size:17px;letter-spacing:.32em;color:#c9b48a">${kick}</div><div style="font-size:40px;letter-spacing:.06em;line-height:1.1">${txt}</div></div></div>`, css, t, until);
// counter card (screen): label + number ticking up + sub (ticks)
const tickCard = (label, to, css, t, dur, until, o = {}) => ticker(label, to, o.suffix || "", css, t, dur, until, o.n || 8, o);
// Allied fighter-bombers (P-47s): the locked K.bombRun with the glowing C-47 symbol in blue (collins move3b), shake on the first bomb
const bomber = (pts, t, n = 4, dur = 4.0, size = 30) => { const bombs = []; for (let k = 0; k < n; k++) bombs.push(posOn(pts, (1.55 + k * 0.25) / dur).map((v, i) => v + (i ? (k % 2 ? 4 : -4) : 0)));
  K.bombRun({ kind: "c47g", side: "carth", size, alt: 9, dur, pts, t, bombs }); };
// transport C-47 (c47g) crossing a drop zone: bundles fall where it passes (prop sound from K.aircraft); planes leave the map
const transport = (pts, t, dur, drops, size = 34) => { K.aircraft({ kind: "c47g", side: "carth", size, alt: 12, pts, t, dur, until: t + dur });
  drops.forEach(([f, dx, dy]) => { const q = posOn(pts, f); bundle(q[0] + dx, q[1] + dy, t + f * dur, t + f * dur + 3.4, { s: 26 }); }); };
// a set of option-2 fronts (lists of polylines) drawn for camera scale s, visible [t, until]
const fset = (lines, s, t, until, dur = 0.8) => lines.map((pts) => front2(pts, s, t, { dur, until }));
// ================= Grant #16 additions (map agent hook) =================
// CLEAN SCREEN v11 (templates/clean_screen_v11.js): words on screen leave after ~3.5 s
const LBL_LIFE = 3.5;
const _cap0 = B.caption.bind(B); B.caption = (txt, t, until, ...r) => _cap0(txt, t, Math.min(until ?? 1e9, t + LBL_LIFE), ...r);
const boxL = (txt, x, y, t, until, o = {}) => boxS(txt, x, y, t, Math.min(until ?? 1e9, t + LBL_LIFE), o);
const wstampL = (txt, x, y, t, until, c, size = 22, sub) => wstampS(txt, x, y, t, Math.min(until ?? 1e9, t + LBL_LIFE), c, size, sub);
// option 1 territory layer (multiply). Owner 2026-11-02: territory only on wide shots where it helps, and SUBTLER there:
// about half the old opacity (TERR_A) and less saturated / orange (TERR_F, inline, overrides battle.css img.terr)
const TERR_A = 0.5, TERR_F = "saturate(0.4)";
const terrImg = (file, parent, t, until, dur = 1.0, outDur = dur) => { const el = document.createElement("img"); el.className = "terr"; el.src = file; el.alt = "";
  el.style.cssText = `position:absolute;left:0;top:0;width:100%;height:100%;mix-blend-mode:multiply;filter:${TERR_F};`; parent.appendChild(el); gsap.set(el, { autoAlpha: 0 });
  if (t != null && t <= 0) gsap.set(el, { autoAlpha: TERR_A }); else if (t != null) tl.fromTo(el, { autoAlpha: 0 }, { autoAlpha: TERR_A, duration: dur, immediateRender: false }, t);
  if (until != null) tl.to(el, { autoAlpha: 0, duration: outDur, ease: "sine.inOut" }, until); return el; };
// top-down ironclad gunboat (dark casemate, blue keyline + pennant, smoke from the stack), constant size on screen; heading follows the river
const BOAT = (s, side) => { const c = side === "rome" ? "#c4121f" : "#1f4fc4", g = side === "rome" ? "#ff8a80" : "#8fb2ff";
  return `<div><svg width="${s * 3.2}" height="${s * 1.5}" viewBox="-32 -15 64 30" style="display:block;overflow:visible;filter:drop-shadow(0 0 ${s * 0.18}px ${g}) drop-shadow(0 ${s * 0.1}px ${s * 0.15}px rgba(0,0,0,.7))">
  <path d="M-26 -7 L18 -7 L28 0 L18 7 L-26 7 Z" fill="#2a2f3a" stroke="${c}" stroke-width="2.6"/><path d="M-18 -4.5 L12 -4.5 L17 0 L12 4.5 L-18 4.5 Z" fill="#454c5a" stroke="#f3eee2" stroke-width="1.1"/>
  <circle cx="-2" cy="-1.8" r="2.4" fill="#151820" stroke="#f3eee2" stroke-width="0.9"/><circle cx="4" cy="1.8" r="2.4" fill="#151820" stroke="#f3eee2" stroke-width="0.9"/>
  <path d="M-26 0 L-34 0" stroke="#f3eee2" stroke-width="1.4"/><path d="M-34 0 L-34 -9 L-25 -6 L-34 -3" fill="${c}" stroke="#f3eee2" stroke-width="0.9"/></svg></div>`; };
const gunboat = (pts, t, dur, until, o = {}) => { const el = GG.pin(BOAT(o.s || 14, o.side), pts[0][0], pts[0][1], { t, until }); pinS(el);
  const inner = el.firstElementChild.querySelector("svg"), n = o.n || 20;
  for (let k = 1; k <= n; k++) { const a = posOn(pts, (k - 1) / n), b = posOn(pts, k / n), ang = Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI;
    if (k === 1) gsap.set(inner, { rotation: ang });
    tl.to(el, { left: b[0], top: b[1], duration: dur / n, ease: o.ease || "none" }, t + (k - 1) * dur / n);
    tl.to(inner, { rotation: ang, duration: Math.min(0.4, dur / n), ease: "none" }, t + (k - 1) * dur / n); }
  return el; };
// small fort (star earthwork) icon on the map, constant on screen
const fortIcon = (x, y, t, until, o = {}) => { const s = o.s || 46, c = o.side === "carth" ? "#1f4fc4" : "#c4121f";
  return pinS(GG.pin(`<div style="width:${s}px;height:${s}px"><svg class="fi" width="${s}" height="${s}" viewBox="-50 -50 100 100" style="display:block;overflow:visible;filter:drop-shadow(0 0 ${s * 0.12}px ${c}) drop-shadow(0 3px 4px rgba(0,0,0,.7))">
  <path d="M0 -44 L14 -16 L44 -14 L22 8 L30 40 L0 24 L-30 40 L-22 8 L-44 -14 L-14 -16 Z" fill="${c}" stroke="#f3eee2" stroke-width="6" stroke-linejoin="round"/>
  <circle cx="0" cy="0" r="9" fill="#f3eee2"/></svg></div>`, x, y, { t, pop: true, until })); };
// musket volley: muzzle flashes along a short line (one "mg" crackle), only where the troops are on screen (1c rule 4)
const flashW = (x, y, t, k = 1) => { const f = GG.pin(`<div style="width:${12 * k}px;height:${12 * k}px;border-radius:50%;background:radial-gradient(circle,#fff6c8 0%,#ffb020 45%,rgba(255,120,0,0) 72%)"></div>`, x, y, {}); pinS(f);
  tl.fromTo(f, { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1.2, duration: 0.06, immediateRender: false }, t); tl.to(f, { autoAlpha: 0, duration: 0.25 }, t + 0.08); };
const volley = (p0, p1, t, n = 6, k = 1, sfx = true) => { for (let i = 0; i < n; i++) { const f = i / (n - 1); flashW(p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f, t + (i % 3) * 0.07, k); } if (sfx) SFX("mg", t); };
// musket smoke puffs along a line (white, drift, fade)
const smokeLine = (p0, p1, t, n = 5, s = 26) => { for (let i = 0; i < n; i++) { const f = i / Math.max(1, n - 1), x = p0[0] + (p1[0] - p0[0]) * f, y = p0[1] + (p1[1] - p0[1]) * f;
  const el = pinS(GG.pin(`<div style="width:${s}px;height:${s}px;border-radius:50%;background:radial-gradient(circle,rgba(240,238,230,.7),rgba(240,238,230,0) 70%)"></div>`, x, y, {}));
  tl.fromTo(el, { autoAlpha: 0, scale: 0.5 }, { autoAlpha: 1, scale: 1.4, duration: 0.5, immediateRender: false }, t + i * 0.05); tl.to(el, { autoAlpha: 0, scale: 2, x: 12, duration: 1.4 }, t + 0.5 + i * 0.05); } };
// red edge pulse (screen)
const RED_EDGE = (() => { const el = document.createElement("div"); el.style.cssText = "position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center, rgba(200,20,30,0) 40%, rgba(200,20,30,0.45) 100%);";
  SCN.insertBefore(el, document.getElementById("credit")); gsap.set(el, { autoAlpha: 0 }); return el; })();
const pulse = (t) => { tl.fromTo(RED_EDGE, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.06, immediateRender: false }, t); tl.to(RED_EDGE, { autoAlpha: 0, duration: 0.5 }, t + 0.08); };
// the "?" mystery badge (screen, corner) with a name plate of spoken words only
const qBadge = (name, role, t, until, o = {}) => { const el = badge({ name, role, photo: null, flag: FL.us, side: "carth", corner: o.corner || "bl", initials: "?", t, until });
  const q = el.querySelector("div[style*='border-radius:50%'] div"); if (q) q.style.fontSize = "110px"; return el; };
// date scroll entries (the scroll itself never disappears once shown)
const dateSet = (txt, t, until, size = 32) => B.date(txt, t, until, size);
// HUD declutter (1c rule 3): the legend / corner badges step out (filter: opacity) while a big card is up
const declutter = (huds, wins) => { const M = []; wins.slice().sort((a, b) => a[0] - b[0]).forEach(([a, b]) => { const L2 = M[M.length - 1]; if (L2 && a - L2[1] < 0.9) L2[1] = Math.max(L2[1], b); else M.push([a, b]); });
  huds.forEach((el) => { gsap.set(el, { filter: "opacity(1)" });
    M.forEach(([a, b]) => { tl.to(el, { filter: "opacity(0)", duration: 0.15, ease: "none", immediateRender: false }, a - 0.15); tl.to(el, { filter: "opacity(1)", duration: 0.3, ease: "none", immediateRender: false }, b + 0.3); }); }); };
