// ---------- ShipSink: side-profile ship scuttled / sinking down a water column to the seabed, with a depth gauge.
// HyperFrames-safe: one GSAP timeline, every frame is a pure function of time (render(t) from a proxy tween's onUpdate, like
// map-kit's camera / board.js); no DOM measurement, no randomness at render time (seeded), works with tl.seek(t) in any order.
//
//   const S = ShipSink(document.getElementById("stage"), { ship: "carrier", depthFt: 212, duration: 7.5, mode: "stern" });
//   window.__timelines = { main: S.tl };   S.cues -> [{t, kind}] sound cues (kit/ship/sfx names), S.landT = touchdown time
//
// Config (all optional):
//   ship: "carrier" | "battleship" | "de" | "sub" | "liner" (kit/ship/ships.js)   depthFt: seabed depth (default 212)
//   duration: total seconds (default 7.5)    mode: "stern" (stern-first, lands upright) | "upright" | "bow"
//   pitch: max pitch in degrees (default 8)  units: "ft" | "m" (big number; the other one is shown small)
//   title / sub: optional caption card ("USS ORISKANY", "GULF OF MEXICO · 17 MAY 2006"), shown 0.3 s - 3.8 s
//   charges: true = demolition flashes at the waterline before it goes (default true)   paint: "livery" | "side"
//   scale: px per foot (default: the ship fills ~72 % of the width)   sinkStart / landAt: fractions of duration (0.12 / 0.78)
//   gaugeMax: depth at the bottom of the gauge (default: depth rounded up to a nice number)   sonar: pings while sinking (true)
(function (root) {
  "use strict";
  const W = 1920, H = 1080;
  const GOLD = "#c9b48a", CREAM = "#f7f3ea";
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, k) => a + (b - a) * k;
  const smooth = (k) => { k = clamp(k, 0, 1); return k * k * (3 - 2 * k); };
  const rnd = (seed) => { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); };
  const niceStep = (d) => { const c = [5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500, 5000]; return c.find((s) => d / s <= 5) || 10000; };

  function ShipSink(stage, cfg = {}) {
    const gsap = root.gsap, K = root.ShipKit;
    const C = Object.assign({ ship: "carrier", depthFt: 212, duration: 7.5, mode: "stern", pitch: 8, units: "ft", charges: true,
      paint: "livery", sinkStart: 0.12, landAt: 0.78, sonar: true }, cfg);
    const D = C.duration, M = K.meta(C.ship), L = M.L, depth = C.depthFt;
    const s = C.scale || (W * 0.72) / L;                                  // px per foot
    const SY = 520;                                                        // surface, world px
    const SB = SY + depth * s;                                             // seabed, world px
    const shipX = W * 0.58;
    const dir = C.mode === "bow" ? 1 : C.mode === "upright" ? 0 : -1;      // -1 = stern down (SVG rotation is clockwise)
    const pitchMax = dir * Math.min(C.pitch, Math.asin(clamp((depth - M.draught) / (L * 0.55), 0, 0.99)) * 180 / Math.PI);
    const t1 = D * C.sinkStart, tL = D * C.landAt, tCh = Math.max(0.15, t1 - 0.55);
    const H0 = depth - M.draught;                                          // waterline datum depth when upright on the seabed

    // ---------------- motion model (feet, degrees)
    function rawState(t) {
      let h, th;
      if (t < t1) { h = 0.6 * Math.sin(t * 2.1); th = 0.4 * Math.sin(t * 1.3 + 0.5); }
      else {
        const p = clamp((t - t1) / (tL - t1), 0, 1.4);
        h = H0 * 1.06 * Math.pow(Math.min(p, 1.3), 1.55);                  // accelerating, still moving when it hits
        const up = smooth((t - t1) / ((tL - t1) * 0.32)), down = smooth((t - (tL - (tL - t1) * 0.18)) / (D * 0.12));
        th = pitchMax * up * (1 - down) + dir * 0.6 * down + (dir === 0 ? 0.8 * Math.sin(t * 0.9) * (1 - down) : 0);
      }
      return { h, th };
    }
    function lowest(h, th) {   // deepest keel point (feet below the surface)
      const r = th * Math.PI / 180; let m = -1e9;
      for (const [kx, ky] of M.keel) m = Math.max(m, h + (kx - L / 2) * Math.sin(r) + ky * Math.cos(r));
      return m;
    }
    function state(t) {
      const r = rawState(t); let low = lowest(r.h, r.th);
      if (low > depth) { r.h -= low - depth; low = depth; r.ground = true; }
      r.low = low; return r;
    }
    let landT = D; for (let t = t1; t < D; t += 1 / 240) if (state(t).ground) { landT = t; break; }
    const keelEndDepth = M.draught;   // gauge starts at the draught (the keel is already that deep while afloat)

    // ---------------- DOM
    stage.innerHTML = "";
    stage.style.cssText = `position:absolute;left:0;top:0;width:${W}px;height:${H}px;overflow:hidden;background:#0b141c;font-family:Oswald,sans-serif`;
    const el = (tag, css, html, parent = stage) => { const e = document.createElement(tag); if (css) e.style.cssText = css; if (html != null) e.innerHTML = html; parent.appendChild(e); return e; };
    const worldH = SB + 600;
    const world = el("div", `position:absolute;left:0;top:0;width:${W}px;height:${worldH}px;transform-origin:0 0`);
    // sky
    el("div", `position:absolute;left:0;top:${SY - 900}px;width:${W}px;height:900px;background:linear-gradient(180deg,#121b22 0%,#26333c 70%,#3a4852 100%)`, null, world);
    // water column: colour by depth (teal near the surface -> navy -> black in the deep)
    const wcol = (d) => { const st = [[0, [38, 98, 110]], [60, [24, 70, 86]], [200, [14, 44, 62]], [800, [8, 24, 40]], [3000, [4, 10, 18]]];
      for (let k = 1; k < st.length; k++) if (d <= st[k][0]) { const a = st[k - 1], b = st[k], q = (d - a[0]) / (b[0] - a[0]); return a[1].map((v, i) => Math.round(lerp(v, b[1][i], q))); }
      return st[st.length - 1][1]; };
    const grad = [0, 0.15, 0.35, 0.6, 1].map((q) => `rgb(${wcol(q * depth).join(",")}) ${(q * 100).toFixed(0)}%`).join(",");
    el("div", `position:absolute;left:0;top:${SY}px;width:${W}px;height:${SB - SY + 600}px;background:linear-gradient(180deg,${grad})`, null, world);
    // light rays from the surface
    const R = rnd(7);
    const rays = [];
    for (let k = 0; k < 6; k++) {
      const x = 150 + k * 300 + R() * 120, w = 60 + R() * 110, len = Math.min(SB - SY, 900);
      rays.push(el("div", `position:absolute;left:${x}px;top:${SY}px;width:${w}px;height:${len}px;transform-origin:50% 0;transform:skewX(${-14 + R() * 8}deg);
        background:linear-gradient(180deg,rgba(190,235,230,${0.10 + R() * 0.06}) 0%,rgba(190,235,230,0) 100%);filter:blur(6px)`, null, world));
    }
    // marine snow
    const snow = [];
    for (let k = 0; k < 90; k++) snow.push({ e: el("div", `position:absolute;left:0;top:0;width:3px;height:3px;border-radius:50%;background:rgba(220,235,230,${0.18 + R() * 0.3})`, null, world),
      x: R() * W, y: SY + 20 + R() * (SB - SY), v: 6 + R() * 10, ph: R() * 6 });
    // seabed (cross-section): sand surface + sediment layers + a few rocks
    let bed = `M0 ${SB + 6}`; for (let x = 0; x <= W; x += 60) bed += ` L${x} ${(SB + 6 + 7 * Math.sin(x / 170) + 4 * Math.sin(x / 53)).toFixed(1)}`;
    bed += ` L${W} ${SB + 600} L0 ${SB + 600} Z`;
    let layers = ""; for (let k = 1; k < 7; k++) { let d = `M0 ${SB + 6 + k * 44}`; for (let x = 0; x <= W; x += 80) d += ` L${x} ${(SB + 6 + k * 44 + 6 * Math.sin(x / (140 + k * 30) + k)).toFixed(1)}`; layers += `<path d="${d}" fill="none" stroke="rgba(30,24,16,0.45)" stroke-width="2" stroke-dasharray="${10 + k * 3} ${6 + k}"/>`; }
    let rocks = ""; for (let k = 0; k < 14; k++) { const x = R() * W, r = 4 + R() * 9; rocks += `<ellipse cx="${x.toFixed(0)}" cy="${(SB + 8 + 7 * Math.sin(x / 170)).toFixed(0)}" rx="${(r * 1.6).toFixed(1)}" ry="${r.toFixed(1)}" fill="#3f382c"/>`; }
    el("div", `position:absolute;left:0;top:0;width:${W}px;height:${worldH}px`, `<svg width="${W}" height="${worldH}" style="position:absolute;left:0;top:0">
      <defs><linearGradient id="sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8c7a58"/><stop offset="0.12" stop-color="#6b5c43"/><stop offset="1" stop-color="#2c261d"/></linearGradient></defs>
      <path d="${bed}" fill="url(#sand)"/>${layers}${rocks}<path d="${bed.split(" L" + W + " " + (SB + 600))[0]}" fill="none" stroke="#b9a57c" stroke-width="2.5" opacity="0.8"/></svg>`, world);
    // the ship
    const svgW = s * (L + 2 * M.pad), ax = (L / 2 + M.pad) * s, ay = (0 - (M.sideY0 - M.pad)) * s;
    const shipEl = el("div", `position:absolute;left:${shipX - ax}px;top:${SY - ay}px;transform-origin:${ax}px ${ay}px;will-change:transform`,
      K.svg(C.ship, "side", { w: svgW, paint: C.paint, col: C.col, glow: false, keyline: 1.6, id: "sink" }), world);
    // charges (flashes) + bubbles + sediment
    const flashes = [];
    if (C.charges) for (let k = 0; k < 7; k++) {
      const fx = (0.08 + k * 0.13) * L, at = tCh + k * 0.07 + R() * 0.05;
      flashes.push({ fx, at, e: el("div", `position:absolute;left:0;top:0;width:90px;height:90px;margin:-45px 0 0 -45px;border-radius:50%;opacity:0;
        background:radial-gradient(circle,#fffbe6 0%,#ffd34d 28%,rgba(255,120,20,.7) 52%,rgba(255,80,0,0) 72%);mix-blend-mode:screen`, null, world),
        spray: el("div", `position:absolute;left:0;top:0;width:26px;height:120px;margin-left:-13px;opacity:0;transform-origin:50% 100%;
        background:linear-gradient(0deg,rgba(235,245,245,.85),rgba(235,245,245,0));border-radius:50% 50% 20% 20%;filter:blur(1.5px)`, null, world) });
    }
    const bubbles = [];
    for (let k = 0; k < 140; k++) bubbles.push({ e: el("div", `position:absolute;left:0;top:0;border-radius:50%;border:1.5px solid rgba(220,240,240,.75);background:rgba(220,240,240,.12);opacity:0`, null, world),
      born: t1 + R() * (Math.min(landT + 1.2, D) - t1), fx: R(), r: 3 + R() * 9, sp: 90 + R() * 120, wob: R() * 6 });
    const silt = [];
    for (let k = 0; k < 16; k++) silt.push({ e: el("div", `position:absolute;left:0;top:0;border-radius:50%;background:radial-gradient(ellipse,rgba(150,132,98,.55) 0%,rgba(150,132,98,0) 70%);opacity:0;filter:blur(4px)`, null, world),
      fx: k < 8 ? R() * 0.3 : 0.3 + R() * 0.7, vx: (R() - 0.5) * 160, r: 60 + R() * 90, d: R() * 0.3 });
    // water tint IN FRONT of the ship (so it darkens as it goes down) + surface line
    const tintTop = `rgba(${wcol(0).join(",")},0.18)`, tintBot = `rgba(${wcol(depth).join(",")},${clamp(0.25 + depth / 900, 0.3, 0.75).toFixed(2)})`;
    el("div", `position:absolute;left:0;top:${SY}px;width:${W}px;height:${SB - SY + 600}px;background:linear-gradient(180deg,${tintTop} 0%,${tintBot} ${((SB - SY) / (SB - SY + 600) * 100).toFixed(0)}%,${tintBot} 100%)`, null, world);
    const wave = (amp, per, y) => { let d = `M-200 ${y}`; for (let x = -200; x < W + 400; x += per) d += ` q${per / 4} ${-amp} ${per / 2} 0 t${per / 2} 0`; return d; };
    const surf = el("div", `position:absolute;left:0;top:${SY - 20}px;width:${W + 400}px;height:40px`, `<svg width="${W + 400}" height="40" style="overflow:visible">
      <path d="${wave(5, 140, 20)}" fill="none" stroke="rgba(235,245,240,.85)" stroke-width="3"/><path d="${wave(3, 90, 24)}" fill="none" stroke="rgba(235,245,240,.35)" stroke-width="2"/></svg>`, world);
    // vignette + grain-ish
    el("div", `position:absolute;inset:0;background:radial-gradient(ellipse at 55% 50%,rgba(0,0,0,0) 50%,rgba(0,0,0,.6) 100%);pointer-events:none`);

    // ---------------- gauge (screen-fixed, left) in the anim_gauge "meter" look: track, ticks, fill + dot, big count, land flash + ring
    const gMax = C.gaugeMax || Math.ceil(depth * 1.12 / niceStep(depth)) * niceStep(depth), step = niceStep(gMax);
    const GX = 170, GW = !!C.gaugeWorld, GY0 = GW ? SY : 250, GY1 = GW ? SY + gMax * s : 930, gy = (d) => GY0 + (GY1 - GY0) * clamp(d / gMax, 0, 1);   // v3: gaugeWorld = ruler lives in the world (0 FT exactly on the drawn surface, true scale, moves with the camera)
    const U = C.units === "m" ? { k: 0.3048, u: "M", k2: 1, u2: "FT" } : { k: 1, u: "FT", k2: 0.3048, u2: "M" };
    let gs = `<rect x="${GX - 16}" y="${GY0 - 12}" width="32" height="${GY1 - GY0 + 24}" rx="16" fill="rgba(247,243,234,.07)" stroke="rgba(247,243,234,.35)" stroke-width="2"/>`;
    for (let d = 0; d <= gMax + 1e-6; d += step) gs += `<line x1="${GX - 40}" y1="${gy(d)}" x2="${GX - 22}" y2="${gy(d)}" stroke="rgba(247,243,234,.6)" stroke-width="2"/>
      <text x="${GX - 48}" y="${gy(d) + 8}" text-anchor="end" font-size="22" fill="rgba(247,243,234,.75)" letter-spacing="1">${Math.round(d * U.k)}</text>`;
    const sbY = gy(depth);
    gs += `<line x1="${GX + 22}" y1="${sbY}" x2="${GX + 150}" y2="${sbY}" stroke="${GOLD}" stroke-width="2" stroke-dasharray="7 6"/>
      <text x="${GX + 30}" y="${sbY - 10}" font-size="19" fill="${GOLD}" letter-spacing="3">SEABED</text>
      <line id="sk-fill" x1="${GX}" y1="${GY0}" x2="${GX}" y2="${GY0}" stroke="${GOLD}" stroke-width="18" stroke-linecap="round"/>
      <circle id="sk-ring" cx="${GX}" cy="${sbY}" r="12" fill="none" stroke="${GOLD}" stroke-width="4" opacity="0"/>
      <circle id="sk-dot" cx="${GX}" cy="${GY0}" r="11" fill="${GOLD}" stroke="#14110b" stroke-width="2"/>`;
    const GHH = GW ? worldH : H; const gauge = el("div", `position:absolute;left:0;top:0;width:${W}px;height:${GHH}px`, `<svg width="${W}" height="${GHH}" style="position:absolute;left:0;top:0;font-family:Oswald;font-weight:500;filter:drop-shadow(0 2px 6px rgba(0,0,0,.6))">${gs}</svg>`, GW ? world : stage);
    const kick = el("div", `position:absolute;left:${GX - 60}px;top:70px;font-size:22px;letter-spacing:.32em;color:${GOLD};font-weight:500;text-shadow:0 2px 10px rgba(0,0,0,.8)`, "DEPTH");
    const big = el("div", `position:absolute;left:${GX - 62}px;top:100px;font-size:92px;font-weight:700;color:${CREAM};line-height:1;letter-spacing:.02em;text-shadow:0 3px 18px rgba(0,0,0,.75);transform-origin:0 50%;white-space:nowrap`);
    const small = el("div", `position:absolute;left:${GX + 250}px;top:150px;font-size:26px;font-weight:500;color:rgba(247,243,234,.7);letter-spacing:.12em;white-space:nowrap`);
    [gauge, kick, big, small].forEach((e) => e.classList.add('sink-gauge'));
    const flashScr = el("div", `position:absolute;inset:0;background:#fff3d6;opacity:0;mix-blend-mode:screen;pointer-events:none`);
    // caption card (map-kit placeCard look)
    let card = null;
    if (C.title) card = el("div", `position:absolute;right:90px;top:80px;padding:12px 26px 14px;background:rgba(18,16,12,.92);border-top:5px solid ${GOLD};color:${CREAM};font-weight:700;box-shadow:0 14px 30px rgba(0,0,0,.6);opacity:0`,
      `<div style="font-size:17px;letter-spacing:.32em;color:${GOLD}">${C.sub || ""}</div><div style="font-size:44px;letter-spacing:.06em;line-height:1.1">${C.title}</div>`);
    const gFill = gauge.querySelector("#sk-fill"), gDot = gauge.querySelector("#sk-dot"), gRing = gauge.querySelector("#sk-ring");

    // ---------------- render(t): everything is a function of t
    const camStart = SY - 600, camEnd = Math.max(camStart, SB - 860);
    function render(t) {
      const st = state(t);
      const k = clamp((st.low - keelEndDepth) / Math.max(1, depth - keelEndDepth), 0, 1);
      const shake = t > landT && t < landT + 0.5 ? Math.sin((t - landT) * 70) * 7 * (1 - (t - landT) / 0.5) : 0;
      const cam = lerp(camStart, camEnd, smooth(k)) + shake;
      const push = 1 + 0.035 * (t / D);
      world.style.transform = `translate(${(W / 2) * (1 - push)}px, ${-cam * push - (H / 2) * (push - 1)}px) scale(${push})`;
      shipEl.style.transform = `translate(0px, ${(st.h * s).toFixed(2)}px) rotate(${st.th.toFixed(3)}deg)`;
      surf.style.transform = `translateX(${(-((t * 38) % 140)).toFixed(1)}px)`;
      rays.forEach((r, i) => { r.style.opacity = (0.75 + 0.25 * Math.sin(t * 0.9 + i * 1.7)).toFixed(3); r.style.marginLeft = (12 * Math.sin(t * 0.5 + i)).toFixed(1) + "px"; });
      snow.forEach((p) => { const y = SY + 20 + ((p.y - SY + p.v * t) % (SB - SY - 20)); p.e.style.transform = `translate(${(p.x + 8 * Math.sin(t * 0.7 + p.ph)).toFixed(1)}px,${y.toFixed(1)}px)`; });
      // hull point (feet along the hull, at a depth below the waterline) -> world px
      const r = st.th * Math.PI / 180, hullPt = (fx, fy) => { const x = fx - L / 2; return [shipX + (x * Math.cos(r) - fy * Math.sin(r)) * s, SY + st.h * s + (x * Math.sin(r) + fy * Math.cos(r)) * s]; };
      flashes.forEach((f) => { const a = t - f.at; const [x, y] = hullPt(f.fx, M.draught * 0.4);
        const o = a < 0 ? 0 : a < 0.08 ? a / 0.08 : Math.max(0, 1 - (a - 0.08) / 0.35);
        f.e.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) scale(${(0.5 + Math.min(a, 0.4) * 2).toFixed(2)})`; f.e.style.opacity = o.toFixed(3);
        const so = a < 0 ? 0 : Math.max(0, 1 - a / 1.1), sh = a < 0 ? 0 : Math.min(1, a / 0.25);
        f.spray.style.transform = `translate(${x.toFixed(1)}px,${(SY - 120).toFixed(1)}px) scaleY(${(0.2 + sh).toFixed(2)})`; f.spray.style.opacity = so.toFixed(3); });
      bubbles.forEach((b) => { const a = t - b.born; if (a < 0 || a > 2.6) { b.e.style.opacity = 0; return; }
        const st0 = state(b.born), r0 = st0.th * Math.PI / 180, x0 = b.fx * L - L / 2, fy = -10;
        const bx = shipX + (x0 * Math.cos(r0) - fy * Math.sin(r0)) * s, by = SY + st0.h * s + (x0 * Math.sin(r0) + fy * Math.cos(r0)) * s;
        const y = by - b.sp * a - 30 * a * a; if (y < SY + 4) { b.e.style.opacity = 0; return; }
        const rr = b.r * (1 + a * 0.25);
        b.e.style.width = b.e.style.height = (2 * rr).toFixed(1) + "px";
        b.e.style.transform = `translate(${(bx + 10 * Math.sin(a * 5 + b.wob) - rr).toFixed(1)}px,${(y - rr).toFixed(1)}px)`;
        b.e.style.opacity = (Math.min(1, a / 0.15) * Math.max(0, 1 - a / 2.6)).toFixed(3); });
      silt.forEach((p, i) => { const a = t - landT - p.d * 0.4; if (a < 0) { p.e.style.opacity = 0; return; }
        const x = shipX + (p.fx - 0.5) * L * s + p.vx * Math.min(a, 2.5) * 0.6, rr = p.r * (0.4 + Math.min(a, 3) * 0.5);
        p.e.style.width = (rr * 2.6).toFixed(0) + "px"; p.e.style.height = (rr * 1.2).toFixed(0) + "px";
        p.e.style.transform = `translate(${(x - rr * 1.3).toFixed(1)}px,${(SB - rr * 0.9 - a * 8).toFixed(1)}px)`;
        p.e.style.opacity = (Math.min(1, a / 0.3) * Math.max(0, 1 - (a - 0.3) / 3.5) * 0.9).toFixed(3); });
      // gauge
      const shown = t >= landT ? depth : st.low, yv = gy(shown);
      gFill.setAttribute("y2", yv.toFixed(1)); gDot.setAttribute("cy", yv.toFixed(1));
      const pre = t < t1 ? 1 + 0.25 * Math.max(0, Math.sin(t * 7)) : 1; gDot.setAttribute("r", (11 * pre).toFixed(2));
      big.innerHTML = `${Math.round(shown * U.k).toLocaleString("en-US")}<span style="font-size:40px;color:${GOLD};margin-left:10px;font-weight:500">${U.u}</span>`;
      small.textContent = `${Math.round(shown * U.k2).toLocaleString("en-US")} ${U.u2}`;
      const la = t - landT;
      const pop = la >= 0 && la < 0.4 ? 1.18 - 0.18 * smooth(la / 0.4) : 1;
      big.style.transform = `scale(${pop.toFixed(3)})`;
      gRing.setAttribute("opacity", la >= 0 && la < 1.0 ? (1 - la).toFixed(3) : 0); gRing.setAttribute("r", la >= 0 ? (12 + 70 * Math.min(la, 1)).toFixed(1) : 12);
      flashScr.style.opacity = la >= 0 && la < 0.25 ? (0.22 * (1 - la / 0.25)).toFixed(3) : 0;
      if (card) card.style.opacity = clamp(Math.min((t - 0.3) / 0.4, (3.8 - t) / 0.4), 0, 1).toFixed(3);
    }

    // ---------------- timeline + sound cues
    const tl = gsap.timeline({ paused: true });
    const proxy = { t: 0 };
    tl.to(proxy, { t: D, duration: D, ease: "none", onUpdate: () => render(proxy.t) }, 0);
    tl.eventCallback("onUpdate", () => render(proxy.t));
    render(0);
    const cues = [{ t: 0, kind: "swell_bed_1", bed: true, until: t1 + 1.0 }, { t: Math.max(0, t1 - 0.2), kind: "underwater_bed_2", bed: true, until: D }];
    if (C.charges) cues.push({ t: tCh, kind: "charges_seq_3" });
    cues.push({ t: t1 + 0.2, kind: "hull_groan_1" }, { t: t1 + 0.9, kind: "sink_whoomp_1" }, { t: t1 + (tL - t1) * 0.5, kind: "metal_creak_2" });
    if (C.sonar) for (let tt = t1 + 0.8; tt < landT - 0.6; tt += 1.6) cues.push({ t: tt, kind: "sonar_ping_3" });
    cues.push({ t: landT, kind: "number_land_1" });
    return { tl, cues: cues.sort((a, b) => a.t - b.t), landT, duration: D, render, config: C };
  }
  root.ShipSink = ShipSink;
})(typeof window !== "undefined" ? window : globalThis);
