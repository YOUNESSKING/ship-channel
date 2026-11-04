// ================= Arnold #17 additions (map agent ar3_: hook-a, hook-b, m3a, m3b), appended after tools/gh_kit.js by tools/ar3_inline.py =================
// SIDES (arnold/SCENES.md): Americans = BLUE "carth" + US 13-star flag (1777); British + their German troops = RED "rome" + Union Flag 1606.
GG.METHOD = ["GO WHERE THE ENEMY SAYS NO ARMY CAN GO", "LET THE GROUND AND THE WEATHER FIGHT FOR YOU", "LEAD FROM THE FRONT, AT THE POINT WHERE IT IS DECIDED"];
GG.METHOD_TITLE = "ARNOLD'S METHOD";
// base world = the saratoga map px (z15). LD(lat, lon) -> world px for ANY place (other maps are groups at their true place and scale)
const BZ = GD.base[0], LD = GG.proj(...GD.base);
const go = (id, t, dur, p, ease) => B.move(id, t, dur, p[0], p[1], ease || "power1.inOut");
const RELIEF = document.getElementById("relief");
RELIEF.style.cssText += "position:absolute;left:0;top:0;width:100%;height:100%;";
// a map as a world group at its true place + scale (feathered edges fe %), optional option-1 territory layer (terrImg, half strength)
const mapGroup = (name, fe = 6, o = {}) => { const [z, ox, oy] = GD.maps[name], k = 2 ** (BZ - z), [bx, by] = [GD.base[1], GD.base[2]];
  const r = [ox * k - bx, oy * k - by, 2880 * k, 1620 * k];
  const g = document.createElement("div"); g.style.cssText = `position:absolute;left:${r[0]}px;top:${r[1]}px;width:${r[2]}px;height:${r[3]}px;isolation:isolate;`;
  if (fe) { const F = `linear-gradient(to right, transparent 0%, #000 ${fe}%, #000 ${100 - fe}%, transparent 100%), linear-gradient(to bottom, transparent 0%, #000 ${fe * 1.6}%, #000 ${100 - fe * 1.6}%, transparent 100%)`;
    g.style.webkitMaskImage = F; g.style.maskImage = F; g.style.webkitMaskComposite = "source-in"; g.style.maskComposite = "intersect"; }
  const i = document.createElement("img"); i.src = `assets/ar3_${name}.jpg`; i.alt = ""; i.style.cssText = "position:absolute;left:0;top:0;width:100%;height:100%;"; g.appendChild(i);
  WORLD.insertBefore(g, o.before || RELIEF); g.rect = r; g.k = k; return g; };
// the saratoga relief itself as a feathered group (so a wider map can show around it)
const baseGroup = (fe = 5) => { const g = document.createElement("div"); g.style.cssText = "position:absolute;left:0;top:0;width:2880px;height:1620px;isolation:isolate;";
  const F = `linear-gradient(to right, transparent 0%, #000 ${fe}%, #000 ${100 - fe}%, transparent 100%), linear-gradient(to bottom, transparent 0%, #000 ${fe * 1.6}%, #000 ${100 - fe * 1.6}%, transparent 100%)`;
  g.style.webkitMaskImage = F; g.style.maskImage = F; g.style.webkitMaskComposite = "source-in"; g.style.maskComposite = "intersect";
  WORLD.insertBefore(g, RELIEF); g.appendChild(RELIEF); return g; };
// ---------- the multi-scale camera (no clamp while several maps are in play; clamp to the saratoga map when o.clamp) ----------
const cam = { cx: 1440, cy: 810, s: 1 }; const FADES = [];   // [group, sLo, sHi]: opacity ramps in (log scale) between sLo and sHi
const smooth = (a) => a * a * (3 - 2 * a), ramp = (s, a, b) => smooth(Math.min(Math.max(Math.log(s / a) / Math.log(b / a), 0), 1));
let CLAMP = false;
const applyCam = () => { let s = cam.s, cx = cam.cx, cy = cam.cy;
  if (CLAMP) { s = Math.max(s, 1920 / 2880); cx = Math.min(Math.max(cx, 960 / s), 2880 - 960 / s); cy = Math.min(Math.max(cy, 540 / s), 1620 - 540 / s); }
  gsap.set(WORLD, { x: 960 - cx * s, y: 540 - cy * s, scale: s, force3D: false });
  FADES.forEach(([g, a, b, inv]) => { const r = ramp(s, a, b); g.style.opacity = (inv ? 1 - r : r).toFixed(3); });
  FADEF.forEach(([g, a, b, inv]) => { const r = ramp(s, a, b); g.style.filter = `opacity(${(inv ? 1 - r : r).toFixed(3)})`; });
  SCALEFIX.forEach((q) => q(s)); CAM_S = s; setInv(); };
// FADEF: like FADES but through filter:opacity (safe on elements gsap also fades with autoAlpha); SCALEFIX: callbacks(s) per camera update
const FADEF = [], SCALEFIX = [];
const fadeS = (els, a, b, inv) => [].concat(els).forEach((g) => { if (g) FADEF.push([g.el || g, a, b, inv]); });
// keep a world-space arrow (arw) at a constant on-screen size: its widths and head are rescaled by s0 / s while the camera moves
const arrowFix = (g, s0) => { const ps = [...g.querySelectorAll("path")], w = ps.map((p) => +p.getAttribute("stroke-width")), hg = g.querySelector("g"), tr = hg ? hg.getAttribute("transform") : "";
  SCALEFIX.push((s) => { const f = s0 / s; ps.forEach((p, i) => p.setAttribute("stroke-width", (w[i] * f).toFixed(2))); if (hg) hg.setAttribute("transform", `${tr} scale(${f.toFixed(4)})`); }); return g; };
const camTo = (t, dur, c, s, ease = "sine.inOut") => tl.to(cam, { cx: c[0], cy: c[1], s, duration: Math.max(dur, 0.01), ease, onUpdate: applyCam }, t);
const camSet = (c, s) => { cam.cx = c[0]; cam.cy = c[1]; cam.s = s; applyCam(); };
// continuous geographic zoom: log-linear scale, the anchor P slides on a straight screen path (no cut, no flash)
const zoom = (t, dur, c0, s0, c1, s1, P, ease = "power2.inOut") => {
  const d0 = [(P[0] - c0[0]) * s0, (P[1] - c0[1]) * s0], d1 = [(P[0] - c1[0]) * s1, (P[1] - c1[1]) * s1], q = { u: 0 };
  tl.fromTo(q, { u: 0 }, { u: 1, duration: dur, ease, immediateRender: false, onUpdate: () => { const u = q.u, s = Math.exp(Math.log(s0) + (Math.log(s1) - Math.log(s0)) * u);
    cam.s = s; cam.cx = P[0] - (d0[0] + (d1[0] - d0[0]) * u) / s; cam.cy = P[1] - (d0[1] + (d1[1] - d0[1]) * u) / s; applyCam(); } }, t); };
// ---------- Arnold-specific symbols ----------
const FLG = { us: FL.us, gb: FL.gb };
// redoubt (log fort) icon in world space, constant on screen; open = which side has no wall ("n" | null); side colour
const REDOUBT = (s, side, open) => { const c = side === "carth" ? "#1f4fc4" : "#c4121f", g = side === "carth" ? "#8fb2ff" : "#ff8a80";
  const walls = { n: "M-40 -22 L-40 26 L40 26 L40 -22", none: "M-40 -26 L40 -26 L40 26 L-40 26 Z" }[open || "none"];
  return `<div><svg class="rd" width="${s * 1.6}" height="${s}" viewBox="-50 -32 100 64" style="display:block;overflow:visible;filter:drop-shadow(0 0 ${s * 0.1}px ${g}) drop-shadow(0 3px 4px rgba(0,0,0,.7))">
  <path class="rf" d="M-40 -26 L40 -26 L40 26 L-40 26 Z" fill="${c}" opacity="0.35" stroke="none"/>
  <path class="rw" d="${walls}" fill="none" stroke="#6b4a2a" stroke-width="11" stroke-linejoin="round"/><path class="rw2" d="${walls}" fill="none" stroke="${c}" stroke-width="5" stroke-dasharray="7 4" stroke-linejoin="round"/>${open === "n" ? `<path class="ro" d="M-44 -26 L44 -26" fill="none" stroke="#ffd54a" stroke-width="10" stroke-linecap="round" opacity="0" style="filter:drop-shadow(0 0 6px #ffd54a)"/>` : ""}</svg></div>`; };
// glow the open side of an open redoubt (pulses), on its spoken words
const openGlow = (el, t, until) => { const p = el.querySelector(".ro"); if (!p) return; tl.to(p, { opacity: 1, duration: 0.3 }, t); tl.to(p, { opacity: 0.35, duration: 0.45, yoyo: true, repeat: 5, ease: "sine.inOut" }, t + 0.3); if (until != null) tl.to(p, { opacity: 0, duration: 0.4 }, until); };
// a person on the map: round portrait (initials until the photo exists), side-coloured ring, world space, constant on screen
const faceMarker = (who, ini, side, x, y, t, until, sz = 58) => { const c = side === "carth" ? "#1f4fc4" : "#c4121f";
  return pinS(GG.pin(`<div class="fm" style="position:relative;width:${sz}px;height:${sz}px;border-radius:50%;overflow:hidden;border:${(sz * 0.07).toFixed(1)}px solid #f3e7c4;box-shadow:0 0 0 3px ${c},0 6px 14px rgba(0,0,0,.7);background:radial-gradient(circle,#2a3142,#0d1018);display:flex;align-items:center;justify-content:center;font-family:Oswald;font-weight:700;font-size:${(sz * 0.4).toFixed(0)}px;color:#f7f3ea"><span>${ini}</span>${who ? `<img src="${PHOTO(who)}" onload="this.previousElementSibling.style.display='none'" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.1)">` : ""}</div>`, x, y, { t, pop: true, until })); };
const redoubt = (x, y, t, until, o = {}) => { const el = pinS(GG.pin(REDOUBT(o.s || 40, o.side || "rome", o.open), x, y, { t, pop: true, until })); return el; };
const recolor = (el, side, t) => { const c = side === "carth" ? "#1f4fc4" : "#c4121f";
  tl.to(el.querySelectorAll(".rf"), { attr: { fill: c }, duration: 0.6 }, t); tl.to(el.querySelectorAll(".rw2"), { attr: { stroke: c }, duration: 0.6 }, t);
  tl.to(el.querySelector(".rd"), { filter: `drop-shadow(0 0 5px ${side === "carth" ? "#8fb2ff" : "#ff8a80"}) drop-shadow(0 3px 4px rgba(0,0,0,.7))`, duration: 0.6 }, t); };
// log cabin icon
const CABIN = `<svg width="26" height="22" viewBox="0 0 26 22" style="display:block;filter:drop-shadow(0 2px 2px rgba(0,0,0,.8))"><path d="M2 10 L13 2 L24 10 Z" fill="#5a3e22" stroke="#f3eee2" stroke-width="1.2"/><rect x="4" y="10" width="18" height="11" fill="#8a6a44" stroke="#f3eee2" stroke-width="1.2"/><path d="M4 13 H22 M4 16 H22 M4 19 H22" stroke="#5a3e22" stroke-width="1"/></svg>`;
const cabin = (x, y, t, until) => pinS(GG.pin(CABIN, x, y, { t, pop: true, until }));
// rider (mounted officer marker): a round marker with a horse-head silhouette or "?" text, world space, constant on screen
const RIDER = (txt, col, sz = 52) => `<div style="width:${sz}px;height:${sz}px;border-radius:50%;background:radial-gradient(circle, rgba(10,12,24,0.95), rgba(10,12,24,0.8));border:${(sz * 0.07).toFixed(1)}px solid #f3e7c4;box-shadow:0 0 0 3px ${col},0 6px 14px rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center;font-family:Oswald;font-weight:700;font-size:${(sz * 0.62).toFixed(0)}px;color:#f7f3ea;overflow:hidden">${txt}</div>`;
const HORSE = (s = 40, col = "#f3eee2") => `<svg width="${s}" height="${s * 0.8}" viewBox="0 0 100 80" style="display:block;overflow:visible;filter:drop-shadow(0 2px 3px rgba(0,0,0,.8))"><g fill="${col}">${CAV_SVG.replace(/#f7f3ea/g, col)}</g></svg>`;
// a badge's photo (or initials if the portrait does not exist yet)
const pbadge = (name, role, who, side, corner, initials, t, until) => badge({ name, role, photo: who ? PHOTO(who) : null, flag: side === "carth" ? FL.us : FL.gb, side, corner, initials, t, until });
// a small hand-drawn label in world space that lives LBL_LIFE (v11) — same as boxL but with a side colour bar
const tagL = (txt, x, y, t, until, size = 15) => boxL(txt, x, y, t, until, { size });
// white flag (surrender) world space
const whiteFlag = (x, y, t, until) => pinS(GG.pin(`<svg width="40" height="54" viewBox="0 0 40 54" style="display:block;overflow:visible;filter:drop-shadow(0 2px 3px rgba(0,0,0,.8))"><path d="M6 54 L6 2" stroke="#2a2420" stroke-width="3.5"/><path d="M7 3 C18 0 26 8 38 4 L38 24 C26 28 18 20 7 23 Z" fill="#fbfaf5" stroke="#2a2420" stroke-width="1.6"/></svg>`, x, y, { t, pop: true, until }));
// big number card (screen) that slams on its word and ticks up
const tickN = (el, sel, n, t0, t1, fmt) => { const v = { v: 0 }, e = el.querySelector(sel);
  tl.to(v, { v: n, duration: Math.max(0.3, t1 - t0), ease: "power2.out", onUpdate: () => { e.textContent = fmt(v.v); } }, t0); for (let t = t0; t < t1 - 0.05; t += 0.13) SFX("tick", t); };
const bigNum = (kick, n, words, t, until, o = {}) => { const el = scr(`<div style="text-align:center;font-family:Oswald;font-weight:700;padding:14px 60px 18px;background:rgba(14,12,10,0.9);border-top:8px solid ${o.col || "#e3232f"};box-shadow:0 22px 44px rgba(0,0,0,.6)">
  <div style="font-size:26px;letter-spacing:0.36em;color:#d8cfb8">${kick}</div>
  <div class="n" style="font-size:132px;line-height:1;color:#f7f3ea;letter-spacing:0.02em">${o.from0 === false ? n.toLocaleString("en-US") : 0}</div>
  <div class="w0" style="font-size:40px;letter-spacing:0.14em;color:${o.wc || "#ef8a82"}">${words}</div></div>`, `left:0;right:0;top:${o.top || 170}px;display:flex;justify-content:center;transform-origin:50% 40%;`, t, null, { autoAlpha: 0 });
  slam(el, t, { from: 1.9, dur: 0.22, shake: o.shake || 6, until });
  if (o.from0 !== false) tickN(el, ".n", n, t + 0.25, t + (o.tick || 1.3), (v) => (Math.round(v / (o.step || 100)) * (o.step || 100)).toLocaleString("en-US"));
  return el; };
// screen card for a result (kicker + big line + sub), slams
const resultCard = (kick, txt, sub, t, until, o = {}) => { const el = scr(`<div style="text-align:center;font-family:Oswald;font-weight:700;padding:14px 56px 18px;background:rgba(14,12,10,0.92);border-top:7px solid ${o.col || "#c9b48a"};box-shadow:0 22px 44px rgba(0,0,0,.6)">
  <div style="font-size:24px;letter-spacing:0.36em;color:${o.kc || "#c9b48a"}">${kick}</div><div style="font-size:${o.size || 84}px;line-height:1.08;color:#f7f3ea;letter-spacing:0.05em">${txt}</div>${sub ? `<div style="font-size:26px;letter-spacing:0.26em;color:#d8cfb8;margin-top:6px">${sub}</div>` : ""}</div>`,
  `left:0;right:0;top:${o.top || 200}px;display:flex;justify-content:center;transform-origin:50% 40%;`, t, null, { autoAlpha: 0 });
  slam(el, t, { from: 1.8, dur: 0.24, shake: o.shake || 4, until }); return el; };
// cross-hatched hit: musket flash + small red/blue pulse at a point (visible only)
const hitAt = (x, y, t, o = {}) => { flashW(x, y, t, o.k || 1.6); if (o.sfx !== false) SFX("mg", t); };
// (copied from tools/m3_kitx.js)
// small screen-space number card (big value, label above, sub below) with an optional tick-up; spoken words only
const numCard = (label, value, sub, css, t, until, o = {}) => { const el = scr(`<div style="padding:10px 30px 12px;background:rgba(18,16,12,0.92);border-top:6px solid ${o.col || "#2e5cb2"};font-family:Oswald;font-weight:700;color:#f7f3ea;text-align:center;box-shadow:0 16px 34px rgba(0,0,0,.55)">
  <div style="font-size:20px;letter-spacing:.3em;color:${o.lc || "#9fc0ea"}">${label}</div><div class="v" style="font-size:${o.vs || 62}px;letter-spacing:.04em;line-height:1.1">${value}</div>${sub ? `<div style="font-size:19px;letter-spacing:.22em;color:#c9c2b2">${sub}</div>` : ""}</div>`, css, t, until);
  if (o.slam !== false) slam(el, t, { sfx: "hit", shake: 3 }); return el; };
fixImgs();
// the Hudson drawn over the wide maps (the hudson bake has no river line): faded out where the saratoga relief shows its own river
const HUDSON_LL = [[43.35, -73.60], [43.267, -73.585], [43.18, -73.570], [43.10, -73.572], [43.05, -73.588], [43.02, -73.598], [43.0, -73.606], [42.975, -73.626], [42.94, -73.65], [42.90, -73.685], [42.82, -73.68], [42.78, -73.685],
  [42.73, -73.69], [42.65, -73.745], [42.55, -73.77], [42.40, -73.785], [42.20, -73.86], [42.0, -73.93], [41.80, -73.95]];
const hudRiver = (sLo = 0.5, sHi = 0.9) => { const g = document.createElementNS(NS, "g"), pts = HUDSON_LL.map((q) => LD(...q)), d = "M" + pts.map((q) => q.map((v) => v.toFixed(0)).join(" ")).join(" L");
  g.innerHTML = `<path d="${d}" fill="none" stroke="rgba(60,58,50,0.55)" stroke-width="190" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" fill="none" stroke="#9fb0b4" stroke-width="150" stroke-linecap="round" stroke-linejoin="round"/>`;
  OVL.insertBefore(g, OVL.firstChild); FADES.push([g, sLo, sHi, true]); return g; };
// ---------- end of Arnold additions ----------
// an element that must already be on screen at frame 0 (it continues from the previous scene): drop its entry tween, show it, fade at until
const atZero = (el, until) => { tl.getTweensOf(el).forEach((tw) => tw.kill()); gsap.set(el, { autoAlpha: 1, x: 0, y: 0 }); if (until != null) tl.to(el, { autoAlpha: 0, duration: 0.4 }, until); return el; };
