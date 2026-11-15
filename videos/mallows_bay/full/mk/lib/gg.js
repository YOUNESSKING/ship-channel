// Map helpers shared by every scene (the Goose Green 'GG' block, unchanged): pins, labels, tag boxes, ships, arcs, cards,
// layers, night/dawn, method card. Usage in a scene: const GG = GGK(B);  (set GG.METHOD / GG.METHOD_TITLE first if needed)
window.GGK = function (B) {
  const NS = "http://www.w3.org/2000/svg";
  const tl = B.tl, pins = document.getElementById("pins"), world = document.getElementById("world");
  const svg = document.getElementById("overlay"), scene = document.getElementById("scene");
  const css = document.createElement("style");
  css.textContent = `
    .unit .tag { font-size: 12px; padding: 0 5px; margin-top: 2px; border-width: 0; }
    .bubble { font-size: 24px; padding: 10px 18px; }
    .gg-pin { position: absolute; left: 0; top: 0; }
    .gg-card.tr { left: auto; right: 70px; }
    .gg-card.tl { right: auto; left: 90px; }
    .gg-card.tr .inner { padding: 18px 36px; border-top-color: #9fc0ea; }
    #dim { background: rgba(8, 8, 10, 0.72); }
    .caption.r { justify-content: flex-end; padding-right: 70px; bottom: 70px; }
    .caption.r span { font-size: 38px; }
    .gg-lbl { position: absolute; white-space: nowrap; font-weight: 700; letter-spacing: 0.08em; color: #fbfaf6; text-shadow: 0 2px 4px rgba(0,0,0,0.9), 0 0 2px #000; }
    .gg-tagbox { position: absolute; white-space: nowrap; padding: 1px 8px; font-weight: 700; letter-spacing: 0.06em; color: #fff; border-radius: 3px; border: 2px solid #f3eee2; }
    .gg-card { position: absolute; left: 0; right: 0; display: flex; justify-content: center; }
    .gg-card .inner { padding: 30px 70px 34px; background: rgba(18, 16, 12, 0.9); color: #f4f1ea; border-top: 6px solid #c9b48a; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }
    .gg-method .k { font-size: 30px; letter-spacing: 0.4em; color: #c9b48a; text-align: center; margin-bottom: 14px; }
    .gg-method .row { display: flex; align-items: center; gap: 28px; font-size: 66px; font-weight: 700; letter-spacing: 0.08em; line-height: 1.4; }
    .gg-method .n { width: 60px; height: 60px; border-radius: 50%; border: 4px solid currentColor; display: flex; align-items: center; justify-content: center; font-size: 36px; flex: none; }
    .gg-method .row.off { color: rgba(244,241,234,0.22); }
    .gg-method .row.off .bar { width: 640px; height: 14px; background: rgba(244,241,234,0.14); border-radius: 7px; }
    .gg-method .row.lit { color: #fbfaf6; }
    .gg-list .row { font-size: 44px; font-weight: 700; letter-spacing: 0.08em; line-height: 1.5; }
    .gg-list .row b { color: #e3232f; margin-right: 18px; }
    .gg-list .h { font-size: 34px; letter-spacing: 0.4em; color: #c9b48a; text-align: center; margin-bottom: 10px; }
    .gstake.arg .face { box-shadow: 0 0 0 3px #c4121f, 0 6px 12px rgba(0,0,0,0.5); }
    .gstake.arg .nm { background: #c4121f; }
  `;
  document.head.appendChild(css);
  const hide = (el) => gsap.set(el, { autoAlpha: 0 });
  const fadeIn = (el, t, dur = 0.5, to = 1) => tl.fromTo(el, { autoAlpha: 0 }, { autoAlpha: to, duration: dur, ease: "power2.out" }, t);
  const fadeOut = (el, t, dur = 0.5) => tl.to(el, { autoAlpha: 0, duration: dur }, t);
  const G = {};
  // world-space element centred on (x, y)
  G.pin = (html, x, y, o = {}) => {
    const el = document.createElement("div");
    el.className = "gg-pin " + (o.cls || "");
    el.innerHTML = html;
    el.style.left = x + "px"; el.style.top = y + "px";
    pins.appendChild(el);
    gsap.set(el, { xPercent: o.anchor ? o.anchor[0] : -50, yPercent: o.anchor ? o.anchor[1] : -50 });
    hide(el);
    if (o.t != null) tl.fromTo(el, { autoAlpha: 0, scale: o.pop ? 0.4 : 1 }, { autoAlpha: 1, scale: 1, duration: 0.5, ease: o.pop ? "back.out(2)" : "power2.out" }, o.t);
    if (o.until != null) fadeOut(el, o.until);
    return el;
  };
  // small label (world px size); anchor default centred
  G.lbl = (text, x, y, o = {}) => G.pin(`<div class="gg-lbl" style="position:relative;font-size:${o.size || 20}px;${o.color ? `color:${o.color};` : ""}">${text}</div>`, x, y, o);
  G.tagbox = (text, x, y, color, o = {}) => G.pin(`<div class="gg-tagbox" style="position:relative;font-size:${o.size || 16}px;background:${color}">${text}</div>`, x, y, o);
  // ship silhouette (world coords), facing left or right
  G.ship = (x, y, o = {}) => {
    const w = o.w || 90, col = o.color || "#1f4fc4";
    return G.pin(`<svg width="${w}" height="${w * 0.36}" viewBox="0 0 100 36" style="display:block;overflow:visible;${o.flip ? "transform:scaleX(-1)" : ""}">
      <path d="M2 22 L96 22 L88 33 L10 33 Z" fill="${col}" stroke="#f3eee2" stroke-width="2.5"/>
      <path d="M30 22 L30 13 L46 13 L46 7 L56 7 L56 13 L66 13 L66 22 Z" fill="${col}" stroke="#f3eee2" stroke-width="2.5"/>
      <line x1="51" y1="7" x2="51" y2="0" stroke="#f3eee2" stroke-width="2.5"/><line x1="12" y1="22" x2="4" y2="17" stroke="#f3eee2" stroke-width="3"/></svg>`, x, y, o);
  };
  // muzzle flash / explosion pulses
  G.flash = (x, y, t, o = {}) => {
    const snd = o.sfx === undefined ? "impact" : o.sfx;
    for (let i = 0; i < (o.n || 3); i++) SFX(snd, t + i * (o.gap || 0.55));
    const r = o.r || 22, n = o.n || 3, gap = o.gap || 0.55;
    const el = document.createElement("div");
    el.style.cssText = `position:absolute;left:${x - r}px;top:${y - r}px;width:${2 * r}px;height:${2 * r}px;border-radius:50%;
      background:radial-gradient(circle, #fffbe6 0%, #ffd34d 30%, rgba(255,120,20,0.75) 55%, rgba(255,80,0,0) 72%);`;
    pins.appendChild(el); hide(el);
    for (let i = 0; i < n; i++) {
      tl.fromTo(el, { autoAlpha: 0, scale: 0.3 }, { autoAlpha: 1, scale: 1.1, duration: 0.12, ease: "power2.out", immediateRender: false }, t + i * gap);
      tl.to(el, { autoAlpha: 0, scale: 1.4, duration: 0.3, ease: "power1.in" }, t + i * gap + 0.12);
    }
    return el;
  };
  // ballistic arc (quadratic curve) drawn from A to B, impact flash, then fades
  G.arc = (x1, y1, x2, y2, t, o = {}) => {
    const h = o.h != null ? o.h : Math.hypot(x2 - x1, y2 - y1) * 0.35;
    const L = Math.hypot(x2 - x1, y2 - y1) || 1;
    let nx = (y2 - y1) / L, ny = -(x2 - x1) / L;              // unit normal
    if (ny > 0.15 || (Math.abs(ny) <= 0.15 && nx > 0)) { nx = -nx; ny = -ny; } // bulge up (or left when firing north-south)
    const mx = (x1 + x2) / 2 + nx * h, my = (y1 + y2) / 2 + ny * h;
    const d = `M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`;
    const g = document.createElementNS(NS, "g");
    const col = o.color || "#fff3c4", w = o.width || 4;
    g.innerHTML = `<path d="${d}" fill="none" stroke="rgba(0,0,0,0.5)" stroke-width="${w + 4}" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" ${o.dash ? `stroke-dasharray="${o.dash}"` : ""}/>`;
    svg.appendChild(g);
    const ps = g.querySelectorAll("path"), len = ps[0].getTotalLength(), dur = o.dur || 1.1;
    gsap.set(ps[0], { strokeDasharray: `${len} ${len}`, strokeDashoffset: len });
    if (!o.dash) gsap.set(ps[1], { strokeDasharray: `${len} ${len}`, strokeDashoffset: len });
    hide(g);
    tl.to(g, { autoAlpha: 1, duration: 0.01 }, t);
    tl.to(o.dash ? [ps[0]] : [ps[0], ps[1]], { strokeDashoffset: 0, duration: dur, ease: "power1.in" }, t);
    if (o.dash) { gsap.set(ps[1], { opacity: 0 }); tl.to(ps[1], { opacity: 1, duration: dur * 0.5 }, t); }
    // no built-in impact: scenes land every shell with K.impact (boom + locked shake), never with G.flash
    if (o.impact === true) G.flash(x2, y2, t + dur - 0.05, { r: o.r || 20, n: 1 });
    tl.to(g, { autoAlpha: 0, duration: 0.6 }, o.until != null ? o.until : t + dur + 0.5);
    return g;
  };
  // straight "missile" line with a travelling head
  G.polygon = (pts, fill, t, until, o = {}) => {
    const p = document.createElementNS(NS, "polygon");
    p.setAttribute("points", pts.map((q) => q.join(",")).join(" "));
    p.setAttribute("fill", fill); if (o.stroke) { p.setAttribute("stroke", o.stroke); p.setAttribute("stroke-width", o.sw || 4); p.setAttribute("stroke-dasharray", o.dash || "none"); }
    svg.insertBefore(p, svg.firstChild);
    hide(p); fadeIn(p, t, o.dur || 1.0, o.alpha || 1);
    if (until != null) fadeOut(p, until, 0.8);
    return p;
  };
  // gorse hedge: dark green dotted band
  G.gorse = (pts, t, until) => {
    const d = pts.map((q, i) => (i ? "L" : "M") + q[0] + " " + q[1]).join(" ");
    const g = document.createElementNS(NS, "g");
    g.innerHTML = `<path d="${d}" fill="none" stroke="rgba(20,40,16,0.55)" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="${d}" fill="none" stroke="#4f7a2e" stroke-width="12" stroke-linecap="round" stroke-dasharray="1 15" stroke-linejoin="round"/>
      <path d="${d}" fill="none" stroke="#8fbf4a" stroke-width="6" stroke-linecap="round" stroke-dasharray="1 15" stroke-linejoin="round"/>`;
    svg.insertBefore(g, svg.firstChild);
    hide(g); fadeIn(g, t, 1.2);
    if (until != null) fadeOut(g, until, 0.8);
    return g;
  };
  // world-space full-map layer between the relief and the overlay (units stay bright above it)
  G.layer = (style, t, until, o = {}) => {
    const el = document.createElement("div");
    el.style.cssText = `position:absolute;left:0;top:0;width:2880px;height:1620px;pointer-events:none;${style}`;
    if (o.html) el.innerHTML = o.html;
    world.insertBefore(el, svg);
    hide(el);
    tl.fromTo(el, { autoAlpha: 0 }, { autoAlpha: o.alpha || 1, duration: o.dur || 2.0, ease: "sine.inOut" }, t);
    if (until != null) tl.to(el, { autoAlpha: 0, duration: o.outDur || 2.0, ease: "sine.inOut" }, until);
    return el;
  };
  G.night = (t, until, o = {}) => {
    let seed = 7; const r = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    let stars = "";
    for (let i = 0; i < 170; i++) {
      const x = r() * 2880, y = r() * 1620, s = 1.5 + r() * 2.5;
      stars += `<div style="position:absolute;left:${x.toFixed(0)}px;top:${y.toFixed(0)}px;width:${s.toFixed(1)}px;height:${s.toFixed(1)}px;border-radius:50%;background:#e8eeff;opacity:${(0.35 + r() * 0.55).toFixed(2)}"></div>`;
    }
    return G.layer("background: radial-gradient(ellipse 70% 60% at 55% 50%, rgba(10,18,44,0.62), rgba(4,8,22,0.82));", t, until, { html: stars, dur: o.dur || 3.0, outDur: o.outDur || 3.0 });
  };
  G.dawn = (t, until) => G.layer("background: linear-gradient(to left, rgba(255,160,80,0.42), rgba(255,190,130,0.18) 55%, rgba(255,210,160,0.05));", t, until, { dur: 4.0, outDur: 4.0 });
  G.sun = (x, y, o = {}) => {
    const s = o.s || 90;
    let rays = "";
    for (let i = 0; i < 12; i++) rays += `<line x1="50" y1="6" x2="50" y2="18" stroke="#ffcf33" stroke-width="5" stroke-linecap="round" transform="rotate(${i * 30} 50 50)"/>`;
    return G.pin(`<svg width="${s}" height="${s}" viewBox="0 0 100 100" style="display:block;filter:drop-shadow(0 0 10px rgba(255,200,40,0.8))">${rays}<circle cx="50" cy="50" r="24" fill="#ffd84a" stroke="#fff4c2" stroke-width="3"/></svg>`, x, y, { ...o, pop: true });
  };
  // screen-space card
  G.card = (html, cls, top, t, until) => {
    const el = document.createElement("div");
    el.className = "gg-card " + cls; el.style.top = top + "px"; el.innerHTML = `<div class="inner">${html}</div>`;
    scene.insertBefore(el, document.getElementById("credit"));
    hide(el);
    tl.fromTo(el, { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.7, ease: "power3.out" }, t);
    if (until != null) fadeOut(el, until, 0.6);
    return el;
  };
  G.METHOD = ["LEAD FROM THE FRONT", "TAKE THE GROUND THAT DECIDES THE BATTLE", "ATTACK WHERE THEY'RE SURE YOU CAN'T"];
  // method card: rowsLit = number of lines shown lit; rowT = reveal times for lit lines
  G.method = (lit, t, until, rowT = []) => {
    const rows = G.METHOD.map((txt, i) => i < lit
      ? `<div class="row lit"><div class="n">${i + 1}</div><div>${txt}</div></div>`
      : `<div class="row off"><div class="n">${i + 1}</div><div class="bar"></div></div>`).join("");
    const el = G.card(`<div class="k">${G.METHOD_TITLE || "THE METHOD"}</div>${rows}`, "gg-method", lit === 3 ? 300 : 320, t, until);
    el.querySelectorAll(".row.lit").forEach((r, i) => tl.fromTo(r, { autoAlpha: 0, x: -40 }, { autoAlpha: 1, x: 0, duration: 0.6, ease: "power3.out" }, rowT[i] != null ? rowT[i] : t + 0.4 + i * 0.8));
    return el;
  };
  // artillery (NATO: filled dot) / mortar icons for an existing unit
  G.icon = (uidKey, kind) => {
    const s = B.units[uidKey].el.querySelector("svg");
    s.innerHTML = kind === "gun" ? `<circle cx="50" cy="50" r="17" fill="#f7f3ea"/>`
      : kind === "mortar" ? `<circle cx="50" cy="66" r="11" fill="none" stroke="#f7f3ea" stroke-width="8"/><line x1="50" y1="55" x2="50" y2="14" stroke="#f7f3ea" stroke-width="8"/><polyline points="34,30 50,12 66,30" fill="none" stroke="#f7f3ea" stroke-width="8"/>`
      : kind === "aa" ? `<path d="M10 90 Q50 5 90 90" fill="none" stroke="#f7f3ea" stroke-width="8"/><circle cx="50" cy="62" r="11" fill="#f7f3ea"/>`
      : kind === "hq" ? `<rect x="0" y="0" width="100" height="100" fill="none"/><line x1="0" y1="0" x2="100" y2="100" stroke="#f7f3ea" stroke-width="7"/><line x1="100" y1="0" x2="0" y2="100" stroke="#f7f3ea" stroke-width="7"/>`
      : s.innerHTML;
  };

  // typographic bio (no photo): flag + big NATO unit marker on one side, bio card on the other
  G.bioT = (o) => {
    const side = document.createElement("div");
    side.style.cssText = `position:absolute;top:170px;${o.mirror ? "right:130px" : "left:150px"};width:600px;height:760px;`;
    side.innerHTML = `<img src="${o.flag}" alt="" style="position:absolute;left:20px;top:0;width:560px;height:auto;box-shadow:0 14px 34px rgba(0,0,0,0.6);border:4px solid #f3eee2;transform:rotate(${o.mirror ? 3 : -3}deg)">
      <svg viewBox="0 0 300 200" style="position:absolute;left:120px;top:400px;width:360px;height:240px;filter:drop-shadow(0 10px 18px rgba(0,0,0,0.6))">
        <rect x="6" y="6" width="288" height="188" fill="${o.color || "#1f4fc4"}" stroke="#f3eee2" stroke-width="8"/>
        <line x1="6" y1="6" x2="294" y2="194" stroke="#f3eee2" stroke-width="9"/><line x1="294" y1="6" x2="6" y2="194" stroke="#f3eee2" stroke-width="9"/>
        ${o.airborne !== false ? `<path d="M110 186 Q150 146 190 186" fill="none" stroke="#f3eee2" stroke-width="9"/>` : ""}
      </svg>
      <div style="position:absolute;left:0;right:0;top:660px;text-align:center;font-size:44px;font-weight:700;letter-spacing:0.2em;color:#f4f1ea;text-shadow:0 3px 8px rgba(0,0,0,0.8)">${o.unit || ""}</div>`;
    scene.insertBefore(side, document.getElementById("credit")); hide(side);
    const card = document.createElement("div");
    card.className = "bio-card";
    card.innerHTML = `<div class="h">${o.name}</div><div class="rule"></div>${o.rows.map((r) => `<div class="row">${r}</div>`).join("")}`;
    if (o.mirror) Object.assign(card.style, { left: "110px", borderLeft: "none", borderRight: "10px solid var(--rome)" });
    card.style.top = (o.top || 300) + "px";
    scene.insertBefore(card, document.getElementById("credit")); hide(card);
    const dx = o.mirror ? 1 : -1;
    tl.fromTo(side, { autoAlpha: 0, x: 140 * dx }, { autoAlpha: 1, x: 0, duration: 1.0, ease: "power3.out" }, o.t);
    tl.to(side, { x: -30 * dx, duration: o.until - o.t - 1.0, ease: "none" }, o.t + 1.0);
    tl.fromTo(card, { autoAlpha: 0, x: -80 * dx }, { autoAlpha: 1, x: 0, duration: 0.9, ease: "power3.out" }, o.t + 0.4);
    tl.to(card, { x: 30 * dx, duration: o.until - o.t - 1.3, ease: "none" }, o.t + 1.3);
    card.querySelectorAll(".row").forEach((r, i) => tl.fromTo(r, { autoAlpha: 0, x: -24 }, { autoAlpha: 1, x: 0, duration: 0.5, ease: "power2.out" }, o.rowT ? o.rowT[i] : o.t + 1 + i * 0.6));
    tl.to([side, card], { autoAlpha: 0, duration: 0.7 }, o.until);
    return { side, card };
  };
  // small name plaque on a stake (world coords, (x,y) = foot of the pole)
  G.stake = (o) => {
    const col = o.side === "rome" ? "#c4121f" : "#1f4fc4", s = o.size || 1;
    const el = G.pin(`<div style="position:relative;width:${260 * s}px;height:${150 * s}px">
      <div style="position:absolute;left:${24 * s}px;top:${30 * s}px;width:${8 * s}px;height:${120 * s}px;background:linear-gradient(90deg,#4c3219,#8a6238 50%,#4c3219);border-radius:2px;box-shadow:0 3px 5px rgba(0,0,0,0.4)"></div>
      <div style="position:absolute;left:0;top:0;padding:${8 * s}px ${12 * s}px;background:var(--paper);border:${3 * s}px solid var(--stake);border-left:${9 * s}px solid ${col};box-shadow:0 6px 12px rgba(0,0,0,0.4);font-family:'Special Elite',monospace;color:var(--ink);white-space:nowrap">
        <div style="font-size:${22 * s}px;line-height:1.1">${o.name}</div>${o.role ? `<div style="font-size:${15 * s}px;margin-top:${4 * s}px;opacity:0.85">${o.role}</div>` : ""}</div></div>`, o.x, o.y, { anchor: [-10, -100] });
    tl.fromTo(el, { autoAlpha: 0, y: -80 * s }, { autoAlpha: 1, y: 0, duration: 0.8, ease: "bounce.out" }, o.t);
    if (o.until != null) fadeOut(el, o.until);
    return el;
  };
  // Web-Mercator projection for a basemap (zoom + origin_world_px from assets/<map>.json): GG.proj(z, ox, oy)(lat, lon) -> [x, y]
  G.proj = (z, ox, oy) => (lat, lon) => {
    const n = 256 * 2 ** z, r = (lat * Math.PI) / 180;
    return [+((lon + 180) / 360 * n - ox).toFixed(1), +((1 - Math.asinh(Math.tan(r)) / Math.PI) / 2 * n - oy).toFixed(1)];
  };
  // parachute mark (scattered drops)
  G.chute = (x, y, t, o = {}) => G.pin(`<svg width="${o.s || 46}" height="${o.s || 46}" viewBox="0 0 40 40" style="display:block;overflow:visible;filter:drop-shadow(0 2px 2px rgba(0,0,0,0.6))">
    <path d="M4 18 Q20 -4 36 18 Z" fill="${o.color || "#1f4fc4"}" stroke="#f3eee2" stroke-width="2.5"/><line x1="5" y1="18" x2="20" y2="34" stroke="#f3eee2" stroke-width="1.6"/><line x1="35" y1="18" x2="20" y2="34" stroke="#f3eee2" stroke-width="1.6"/><line x1="20" y1="18" x2="20" y2="34" stroke="#f3eee2" stroke-width="1.6"/><circle cx="20" cy="35" r="3.2" fill="#f3eee2"/></svg>`, x, y, { t, pop: true, until: o.until });
  // white flash cut (flash-forward / rewind)
  G.whiteFlash = (t) => {
    const w = document.createElement("div"); w.style.cssText = "position:absolute;inset:0;background:#fffdf6;pointer-events:none;";
    scene.insertBefore(w, document.getElementById("credit")); hide(w);
    tl.fromTo(w, { autoAlpha: 0 }, { autoAlpha: 0.9, duration: 0.12 }, t); tl.to(w, { autoAlpha: 0, duration: 0.6 }, t + 0.14);
  };
  // stamp card (punchline), red by default
  G.stamp = (text, t, until, o = {}) => {
    const c = o.color || "#e3232f";
    const el = G.card(`<div style="font-size:${o.size || 60}px;font-weight:700;letter-spacing:0.12em;color:${c};border:6px solid ${c};padding:6px 30px;transform:rotate(${o.rot || -4}deg)">${text}</div>`, "gg-stamp", o.top || 840, t, until);
    el.querySelector(".inner").style.cssText = "background:rgba(18,16,12,0.78);padding:18px 28px;border-top:none;";
    tl.fromTo(el, { scale: 1.6 }, { scale: 1, duration: 0.35, ease: "power4.in" }, t);
    if (window.SFX) SFX("hit", t + 0.3);
    return el;
  };
  // road: casing + light centre line (world coords)
  G.road = (pts, o = {}) => {
    const g = document.createElementNS(NS, "g"), d = pts.map((q, i) => (i ? "L" : "M") + q[0] + " " + q[1]).join(" ");
    g.innerHTML = `<path d="${d}" fill="none" stroke="rgba(40,30,16,0.55)" stroke-width="${o.w ? o.w + 6 : 11}" stroke-linejoin="round" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#efe6cf" stroke-width="${o.w || 5}" stroke-linejoin="round" stroke-linecap="round"/>`;
    svg.insertBefore(g, svg.children[1] || null);
    if (o.t != null) { hide(g); fadeIn(g, o.t, 1.0); }
    return g;
  };
  // world-space image layer (e.g. a water mask tinted blue): GG.water("assets/x_water.png", t)
  G.water = (mask, t, o = {}) => G.layer(`background:${o.color || "#86a9c9"};-webkit-mask-image:url(${mask});mask-image:url(${mask});-webkit-mask-size:2880px 1620px;mask-size:2880px 1620px;`, t, o.until, { alpha: o.alpha || 0.9, dur: o.dur || 0.01 });
  G.fadeIn = fadeIn; G.fadeOut = fadeOut; G.hide = hide;
  return G;
};
