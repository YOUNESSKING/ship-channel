// SHIP KIT for the full Oriskany map scenes (on top of the test v4 map-kit: battle.js / gg.js / fx.js / living.js).
// const S = ShipK();  ->  S.G(lat, lon) map px · S.w("word", n, off) scene time of a spoken word (words.json) ·
// S.camera([[t, x, y, scale], ...]) · S.pin / S.label / S.tag / S.date / S.route / S.arc / S.poly / S.icon / S.storm / S.card
// Screen text (labels, tags, date line) lives in SCREEN space (constant 40-48 px at 1080p whatever the zoom) and follows
// its map point; the camera and the followers are computed from one timeline tween (deterministic, no DOM reads at render time).
// 1999 tow, San Francisco -> round South America (Cape Horn) -> Beaumont (FACTCHECK_A D8; route drawn offshore, illustrative)
window.HORN = [[37.8, -122.4], [37.81, -122.52], [36.0, -122.6], [32.0, -119.0], [24.0, -113.5], [16, -102], [8, -88], [-2, -83], [-15, -78.5], [-30, -73.5],
  [-45, -77.0], [-53, -77.0], [-56.6, -70], [-56.5, -66], [-54, -62], [-45, -58], [-36, -52], [-25, -42], [-12, -33.5], [-2, -35], [6, -48], [11, -58],
  [13.5, -68], [16, -77], [19.5, -84], [21.8, -85.8], [25, -89], [28.5, -93], [29.7, -93.85], [30.08, -94.1]];
// 18 Nov 1952 air fight, schematic: four blue tracks north from the carrier (TF 77 off NE Korea), seven red tracks from the north
window.MIG = { blue: [0, 1, 2, 3].map((i) => [[40.6, 132.2], [41.2, 132.0 - i * 0.05], [41.8, 131.75 - i * 0.1 + i * 0.25], [42.4, 131.2 + i * 0.32]]),
  red: [0, 1, 2, 3, 4, 5, 6].map((i) => [[44.6, 130.6 + i * 0.45], [43.4, 130.9 + i * 0.3], [42.6, 131.1 + i * 0.2]]) };
window.ShipK = function () {
  const T = window.SCENE_TIMING, M = T.map, END = T.duration;
  const B = Battle(); const tl = B.tl;
  const world = document.getElementById("world"), fx = document.getElementById("fx"), svg = document.getElementById("overlay");
  const NS = "http://www.w3.org/2000/svg";
  const S = { B, tl, END, GOLD: "#e3c27a", TEAL: "#7fd3d8", BLUE: "#4f8df0", RED: "#e0403a", INK: "#f3eee2", BOX: "rgba(10,24,38,.9)" };
  const css = document.createElement("style");
  css.textContent = `
    .sk-f { position:absolute; left:0; top:0; will-change: transform; }
    .sk-lbl { position:absolute; white-space:nowrap; font-family:Oswald; font-weight:700; letter-spacing:.08em; color:#f7f3ea;
              text-shadow:0 2px 6px rgba(0,0,0,.95), 0 0 3px #000; }
    .sk-box { padding:2px 14px; background:rgba(10,24,38,.9); border:2px solid #f3eee2; border-radius:3px; text-shadow:none; }
    .sk-date { position:absolute; left:90px; top:78px; font-family:Oswald; font-weight:700; font-size:46px; letter-spacing:.16em;
               color:#e3c27a; text-shadow:0 2px 8px rgba(0,0,0,.9); white-space:nowrap; }
    .sk-date .rule { height:3px; background:#e3c27a; margin-top:6px; transform-origin:0 50%; box-shadow:0 1px 4px rgba(0,0,0,.7); }
    .sk-card { position:absolute; font-family:Oswald; font-weight:700; color:#f4f1ea; background:rgba(12,18,26,.9);
               border-top:6px solid #e3c27a; padding:26px 48px 30px; box-shadow:0 20px 40px rgba(0,0,0,.5); text-align:center; }
    #credit { font-family: Oswald; }`;
  document.head.appendChild(css);
  // ---- projection (lon wrapped into the bake's range, so Pacific bakes work across the antimeridian) ----
  const n = 256 * Math.pow(2, M.zoom), lonC = M.center[1];
  S.G = (lat, lon) => {
    while (lon - lonC > 180) lon -= 360; while (lon - lonC < -180) lon += 360;
    const x = (lon + 180) / 360 * n - M.origin_world_px[0];
    const y = (1 - Math.asinh(Math.tan(lat * Math.PI / 180)) / Math.PI) / 2 * n - M.origin_world_px[1];
    return [x, y];
  };
  // places (lat, lon). Reef + SS United States: FACTCHECK_C (FWC / Okaloosa County); others: city / yard centres.
  S.PL = { REEF: [30.04258, -87.00662], SSUS: [30.11913, -86.77925], PENS: [30.42, -87.22], NASP: [30.35, -87.29], DESTIN: [30.393, -86.496],
    BREM: [47.565, -122.627], SF: [37.80, -122.40], GG: [37.81, -122.52], MARE: [38.09, -122.27], TOKYO: [35.45, 139.85],
    BEAU: [30.08, -94.10], SABINE: [29.70, -93.85], CORPUS: [27.80, -97.40], DC: [38.90, -77.03], ATL: [33.75, -84.39],
    BNY: [40.7003, -73.9729], HANOI: [21.03, 105.85], TRUCBACH: [21.047, 105.838], YANKEE: [17.5, 108.5] };
  S.P = (k) => S.G(...S.PL[k]);
  S.path = (ll) => ll.map((p) => S.G(p[0], p[1]));
  // ---- spoken words -> scene seconds ----
  const norm = (s) => s.toLowerCase().replace(/[^a-z0-9']/g, "").replace(/'s$/, "");
  S.w = (word, k = 0, off = 0) => {
    const ws = T.words.filter((q) => norm(q[0]) === norm(word) && q[1] > -0.05);
    if (!ws[k]) throw new Error(`word "${word}" #${k} not spoken in this scene`);
    return Math.max(0, ws[k][1] + off);
  };
  // ---- camera (same eased key scheme as B.camera) + screen followers ----
  const ease = gsap.parseEase("sine.inOut");
  let keys = [[0, 1440, 810, 0.667]];
  S.camera = (k) => { keys = k; };
  const camAt = (t) => {
    if (t <= keys[0][0]) return keys[0].slice(1);
    for (let i = 1; i < keys.length; i++) {
      const a = keys[i - 1], b = keys[i];
      if (t <= b[0]) { const u = ease((t - a[0]) / Math.max(0.01, b[0] - a[0])); return [1, 2, 3].map((j) => a[j] + (b[j] - a[j]) * u); }
    }
    return keys[keys.length - 1].slice(1);
  };
  const fol = [];
  const place = (t) => {
    let [cx, cy, s] = camAt(t);
    s = Math.max(s, 1920 / 2880);
    cx = Math.min(Math.max(cx, 960 / s), 2880 - 960 / s); cy = Math.min(Math.max(cy, 540 / s), 1620 - 540 / s);
    const X = 960 - cx * s, Y = 540 - cy * s;
    world.style.transform = `translate(${X.toFixed(2)}px,${Y.toFixed(2)}px) scale(${s.toFixed(5)})`;
    for (const f of fol) { const p = typeof f.pt === "function" ? f.pt(t) : f.pt; f.el.style.transform = `translate(${(X + p[0] * s).toFixed(1)}px,${(Y + p[1] * s).toFixed(1)}px)`; }
    S.scale = s;
  };
  S.scaleAt = (t) => Math.max(camAt(t)[2], 1920 / 2880);
  const follow = (el, pt) => { const w = document.createElement("div"); w.className = "sk-f"; w.appendChild(el); fx.appendChild(w); fol.push({ el: w, pt }); return w; };
  const show = (el, t, o = {}) => {
    tl.fromTo(el, { autoAlpha: 0, ...(o.from || { y: 14 }) }, { autoAlpha: 1, y: 0, x: 0, scale: 1, duration: o.dur || 0.45, ease: o.ease || "power2.out", immediateRender: true }, t);
    if (o.until != null) tl.to(el, { autoAlpha: 0, duration: 0.35 }, o.until);
  };
  // anchor: where the text sits relative to the point: r (right), l (left), t (above), b (below), c (centre)
  const ANC = { r: [0, -50], l: [-100, -50], t: [-50, -100], b: [-50, 0], c: [-50, -50] };
  S.label = (text, pt, o = {}) => {
    const el = document.createElement("div"); el.className = "sk-lbl" + (o.box ? " sk-box" : "");
    el.innerHTML = text; el.style.fontSize = (o.size || 44) + "px"; if (o.color) el.style.color = o.color;
    if (o.boxColor) el.style.background = o.boxColor; if (o.border) el.style.borderColor = o.border;
    const a = ANC[o.anchor || "r"], gap = o.gap != null ? o.gap : 26;
    const off = { r: [gap, 0], l: [-gap, 0], t: [0, -gap], b: [0, gap], c: [0, 0] }[o.anchor || "r"];
    gsap.set(el, { xPercent: a[0], yPercent: a[1] });
    el.style.left = (off[0] + (o.dx || 0)) + "px"; el.style.top = (off[1] + (o.dy || 0)) + "px";
    follow(el, pt); show(el, o.t || 0, o); return el;
  };
  S.tag = (text, pt, o = {}) => S.label(text, pt, { size: 40, box: true, ...o });
  S.date = (text, t, o = {}) => {
    const el = document.createElement("div"); el.className = "sk-date"; el.innerHTML = `${text}<div class="rule"></div>`;
    if (o.top) el.style.top = o.top + "px";
    document.getElementById("scene").insertBefore(el, document.getElementById("credit"));
    show(el, t, { from: { x: -40 }, dur: 0.5 });
    tl.fromTo(el.querySelector(".rule"), { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power2.out", immediateRender: true }, t + 0.15);
    if (o.until != null) tl.to(el, { autoAlpha: 0, duration: 0.35 }, o.until);
    return el;
  };
  S.card = (html, t, o = {}) => {
    const el = document.createElement("div"); el.className = "sk-card"; el.innerHTML = html;
    Object.assign(el.style, { left: (o.left || 120) + "px", top: (o.top || 380) + "px", width: (o.width || 760) + "px" });
    document.getElementById("scene").insertBefore(el, document.getElementById("credit"));
    show(el, t, { from: { y: 40, scale: 0.96 }, dur: 0.6 });
    return el;
  };
  // ---- world things ----
  S.dot = (pt, o = {}) => {   // glowing pin dot (world space; size given in SCREEN px at the scale it appears)
    const s = S.scaleAt(o.t || 0), r = (o.r || 11) / s, c = o.color || S.GOLD;
    const el = document.createElement("div");
    el.style.cssText = `position:absolute;left:${pt[0] - r}px;top:${pt[1] - r}px;width:${2 * r}px;height:${2 * r}px;border-radius:50%;background:${c};border:${2 / s}px solid #10161c;box-shadow:0 0 ${18 / s}px ${c}`;
    document.getElementById("pins").appendChild(el);
    tl.fromTo(el, { autoAlpha: 0, scale: 0.2 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)", immediateRender: true }, o.t || 0);
    if (o.until != null) tl.to(el, { autoAlpha: 0, duration: 0.3 }, o.until);
    return el;
  };
  S.ring = (pt, o = {}) => {  // pulsing rings (screen size r) from t to the end
    const t = o.t || 0, s = S.scaleAt(t), r = (o.r || 34) / s, c = o.color || S.GOLD, until = o.until || END + 1;
    for (let k = 0; k < 2; k++) {
      const el = document.createElement("div");
      el.style.cssText = `position:absolute;left:${pt[0] - r}px;top:${pt[1] - r}px;width:${2 * r}px;height:${2 * r}px;border-radius:50%;border:${3 / s}px solid ${c};box-shadow:0 0 ${10 / s}px ${c}`;
      document.getElementById("pins").appendChild(el); gsap.set(el, { autoAlpha: 0 });
      const rep = Math.max(0, Math.round((until - t) / 1.6) - 1);
      tl.fromTo(el, { autoAlpha: 0.95, scale: 0.55 }, { autoAlpha: 0, scale: 1.7, duration: 1.6, repeat: rep, ease: "sine.out", immediateRender: false }, t + k * 0.8);
    }
  };
  S.pin = (pt, name, o = {}) => {   // dot + rings + name (screen label)
    S.dot(pt, o); if (o.rings !== false) S.ring(pt, { t: o.t, color: o.color, r: o.ringR });
    if (name) return S.label(name, pt, { t: (o.lt != null ? o.lt : o.t || 0), anchor: o.anchor || "r", size: o.size || 44, box: o.box, dx: o.dx, dy: o.dy, until: o.until, gap: o.gap });
  };
  S.img = (src, pt, o = {}) => {   // world-space picture (ship tops etc.), width in screen px at time t
    const s = S.scaleAt(o.t || 0), w = (o.w || 120) / s;
    const el = document.createElement("img"); el.src = src; el.alt = "";
    el.style.cssText = `position:absolute;left:${pt[0] - w / 2}px;top:${pt[1]}px;width:${w}px;transform:translateY(-50%) rotate(${o.rot || 0}deg);${o.filter ? "filter:" + o.filter : ""}`;
    document.getElementById("pins").appendChild(el);
    tl.fromTo(el, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.45, immediateRender: true }, o.t || 0);
    if (o.until != null) tl.to(el, { autoAlpha: 0, duration: 0.3 }, o.until);
    return el;
  };
  // route: smooth path through map points that draws itself (dash = dashed line). o.head = "ship" | "dot" | "jet" | "missile" | null
  const smooth = (pts) => { let d = `M${pts[0][0]},${pts[0][1]}`; for (let i = 0; i < pts.length - 1; i++) { const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
      d += ` C${p1[0] + (p2[0] - p0[0]) / 6},${p1[1] + (p2[1] - p0[1]) / 6} ${p2[0] - (p3[0] - p1[0]) / 6},${p2[1] - (p3[1] - p1[1]) / 6} ${p2[0]},${p2[1]}`; } return d; };
  let mid = 0;
  S.route = (pts, o = {}) => {
    const t = o.t || 0, dur = o.dur || 2, s = S.scaleAt(o.scaleAt != null ? o.scaleAt : t), w = (o.width || 6) / s, c = o.color || S.GOLD, d = smooth(pts);
    const g = document.createElementNS(NS, "g"); const id = "skm" + (++mid);
    const dash = o.dash ? `stroke-dasharray="${(o.dash[0] || 18) / s} ${(o.dash[1] || 12) / s}"` : "";
    g.innerHTML = `<mask id="${id}" maskUnits="userSpaceOnUse" x="-6000" y="-6000" width="20000" height="20000"><path d="${d}" fill="none" stroke="#fff" stroke-width="${w * 4}" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></mask>
      <g mask="url(#${id})"><path d="${d}" fill="none" stroke="rgba(0,0,0,.5)" stroke-width="${w + 4 / s}" ${dash} stroke-linecap="round"/>
      <path d="${d}" fill="none" stroke="${c}" stroke-width="${w}" ${dash} stroke-linecap="round" style="filter:drop-shadow(0 0 ${4 / s}px ${c})"/></g>`;
    svg.appendChild(g);
    const mp = g.querySelector("mask path"), probe = g.querySelectorAll("path")[1], L = probe.getTotalLength();
    const N = 160, samp = []; for (let i = 0; i <= N; i++) { const q = probe.getPointAtLength(L * i / N); samp.push([q.x, q.y]); }
    const at = (p) => { const f = Math.min(N, Math.max(0, p * N)), i = Math.min(N - 1, Math.floor(f)), u = f - i; return [samp[i][0] + (samp[i + 1][0] - samp[i][0]) * u, samp[i][1] + (samp[i + 1][1] - samp[i][1]) * u, Math.atan2(samp[i + 1][1] - samp[i][1], samp[i + 1][0] - samp[i][0]) * 180 / Math.PI]; };
    let head = null;
    if (o.head) {
      head = document.createElement("div"); head.style.cssText = "position:absolute;left:0;top:0;"; document.getElementById("pins").appendChild(head);
      const hs = (o.headSize || 1) / s;
      const H = {
        ship: `<svg width="${46 * hs}" height="${16 * hs}" viewBox="0 0 46 16" style="display:block;transform:translate(-50%,-50%);overflow:visible"><path d="M1 8 L8 2 L42 3 L45 8 L42 13 L8 14 Z" fill="${c}" stroke="#0c1218" stroke-width="1.5"/><rect x="26" y="3.5" width="6" height="4" fill="#0c1218"/></svg>`,
        dot: `<div style="width:${18 * hs}px;height:${18 * hs}px;border-radius:50%;background:${c};box-shadow:0 0 ${14 * hs}px ${c};transform:translate(-50%,-50%)"></div>`,
        jet: `<svg width="${34 * hs}" height="${34 * hs}" viewBox="-17 -17 34 34" style="display:block;transform:translate(-50%,-50%);overflow:visible"><path d="M15 0 L-6 -4 L-10 -14 L-14 -14 L-11 -3 L-15 -2 L-15 2 L-11 3 L-14 14 L-10 14 L-6 4 Z" fill="${c}" stroke="#0c1218" stroke-width="1.5"/></svg>`,
        missile: `<svg width="${30 * hs}" height="${12 * hs}" viewBox="-15 -6 30 12" style="display:block;transform:translate(-50%,-50%);overflow:visible"><path d="M14 0 L8 -3 L-12 -3 L-15 -6 L-15 6 L-12 3 L8 3 Z" fill="#f3eee2" stroke="${c}" stroke-width="2"/><circle cx="-16" cy="0" r="4" fill="#ffb347"/></svg>`,
      }[o.head] || `<div style="width:${44 * hs}px;height:${44 * hs}px;transform:translate(-50%,-50%)">${ICON[o.head](o.headColor || c).replace("<svg ", `<svg width="${44 * hs}" height="${44 * hs}" style="display:block;overflow:visible" `)}</div>`;
      head.innerHTML = `<div class="rot">${H}</div>`;
      gsap.set(head, { autoAlpha: 0 });
      tl.to(head, { autoAlpha: 1, duration: 0.2 }, t);
      if (o.headUntil != null) tl.to(head, { autoAlpha: 0, duration: 0.3 }, o.headUntil);
    }
    const pr = { p: 0 }, rot = head && head.querySelector(".rot");
    const upd = () => { mp.setAttribute("stroke-dashoffset", (1 - pr.p).toFixed(4)); if (head) { const q = at(Math.max(0.001, pr.p)); head.style.transform = `translate(${q[0]}px,${q[1]}px)`; rot.style.transform = `rotate(${o.head === "ship" || o.head === "jet" || o.head === "missile" ? q[2] : 0}deg)`; } };
    upd();
    tl.to(pr, { p: 1, duration: dur, ease: o.ease || "power1.inOut", onUpdate: upd, immediateRender: false }, t);
    if (o.until != null) tl.to(g, { autoAlpha: 0, duration: 0.4 }, o.until);
    return { g, at, head, end: pts[pts.length - 1] };
  };
  // curved arc A -> B (bulge = fraction of the length, + = to the left of travel)
  S.arcPts = (A, Bp, bulge = 0.2, k = 24) => { const dx = Bp[0] - A[0], dy = Bp[1] - A[1], L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L;
    const C = [(A[0] + Bp[0]) / 2 + nx * L * bulge, (A[1] + Bp[1]) / 2 + ny * L * bulge], out = [];
    for (let i = 0; i <= k; i++) { const u = i / k; out.push([(1 - u) * (1 - u) * A[0] + 2 * u * (1 - u) * C[0] + u * u * Bp[0], (1 - u) * (1 - u) * A[1] + 2 * u * (1 - u) * C[1] + u * u * Bp[1]]); } return out; };
  // polygon from [lon,lat] rings (geo.json), outlined + filled; returns the <g>
  S.poly = (rings, o = {}) => {
    const t = o.t || 0, s = S.scaleAt(t), c = o.color || S.GOLD;
    const d = rings.map((r) => "M" + r.map((q) => S.G(q[1], q[0]).map((v) => v.toFixed(1)).join(",")).join("L") + "Z").join("");
    const g = document.createElementNS(NS, "g");
    g.innerHTML = `<path d="${d}" fill="${c}" fill-opacity="${o.fill != null ? o.fill : 0.28}" stroke="${c}" stroke-width="${(o.width || 3.5) / s}" stroke-linejoin="round" style="filter:drop-shadow(0 0 ${6 / s}px ${c})"/>`;
    svg.appendChild(g);
    tl.fromTo(g, { autoAlpha: 0 }, { autoAlpha: 1, duration: o.dur || 0.5, ease: "power2.out", immediateRender: true }, t);
    if (o.dimAt != null) tl.to(g, { autoAlpha: o.dimTo != null ? o.dimTo : 0.18, duration: 0.5 }, o.dimAt);
    if (o.until != null) tl.to(g, { autoAlpha: 0, duration: 0.4 }, o.until);
    return g;
  };
  S.flashAt = (pt, t, o = {}) => {  // burst (flak / hit), screen size
    const s = S.scaleAt(t), r = (o.r || 26) / s;
    const el = document.createElement("div");
    el.style.cssText = `position:absolute;left:${pt[0] - r}px;top:${pt[1] - r}px;width:${2 * r}px;height:${2 * r}px;border-radius:50%;background:radial-gradient(circle, #fffbe6 0%, #ffd34d 30%, rgba(255,120,20,.75) 55%, rgba(255,80,0,0) 72%)`;
    document.getElementById("pins").appendChild(el); gsap.set(el, { autoAlpha: 0 });
    tl.fromTo(el, { autoAlpha: 0, scale: 0.3 }, { autoAlpha: 1, scale: 1.1, duration: 0.12, ease: "power2.out", immediateRender: false }, t);
    tl.to(el, { autoAlpha: o.keep ? 0.55 : 0, scale: o.keep ? 0.8 : 1.5, duration: 0.45, ease: "power1.in" }, t + 0.12);
    if (window.SFX && o.sfx !== false) SFX(o.sfx || "impact", t);
    return el;
  };
  // small icons in world space at a point (screen size px): fish, tag, hurricane, star
  const ICON = {
    fish: (c) => `<svg viewBox="-22 -12 44 24"><path d="M-14 0 C-6 -10 8 -10 14 0 C8 10 -6 10 -14 0 Z M-14 0 L-21 -7 L-21 7 Z" fill="${c}" stroke="#0c1218" stroke-width="1.5"/><circle cx="8" cy="-2" r="1.8" fill="#0c1218"/></svg>`,
    tag: (c) => `<svg viewBox="-16 -16 32 32"><path d="M-12 -6 L2 -6 L12 0 L2 6 L-12 6 Z" fill="${c}" stroke="#0c1218" stroke-width="1.5"/><circle cx="-7" cy="0" r="2.2" fill="#0c1218"/></svg>`,
    hurricane: (c) => `<svg viewBox="-34 -34 68 68"><g fill="${c}" stroke="#0c1218" stroke-width="1.5"><path d="M-2 -11 C 6 -24 20 -30 32 -28 C 22 -24 14 -16 11 -4 Z"/><path d="M2 11 C -6 24 -20 30 -32 28 C -22 24 -14 16 -11 4 Z"/><circle r="12"/></g><circle r="5.5" fill="#0c1218"/></svg>`,
    q: (c) => `<svg viewBox="-20 -24 40 48"><text x="0" y="16" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="44" fill="${c}" stroke="#0c1218" stroke-width="1.5">?</text></svg>`,
  };
  S.icon = (kind, pt, o = {}) => {
    const t = o.t || 0, s = S.scaleAt(t), w = (o.size || 44) / s;
    const el = document.createElement("div");
    el.style.cssText = `position:absolute;left:${pt[0] - w / 2}px;top:${pt[1] - w / 2}px;width:${w}px;height:${w}px;filter:drop-shadow(0 0 ${5 / s}px rgba(0,0,0,.8))`;
    el.innerHTML = ICON[kind](o.color || S.GOLD).replace("<svg ", `<svg width="${w}" height="${w}" style="display:block;overflow:visible" `);
    document.getElementById("pins").appendChild(el);
    tl.fromTo(el, { autoAlpha: 0, scale: 0.3 }, { autoAlpha: 1, scale: 1, duration: 0.4, ease: "back.out(2)", immediateRender: true }, t);
    if (o.spin) tl.fromTo(el.firstChild, { rotation: 0 }, { rotation: -o.spin, duration: END - t + 0.5, ease: "none", transformOrigin: "50% 50%", immediateRender: true }, t);
    if (o.bob) tl.fromTo(el, { y: 0 }, { y: -o.bob / s, duration: 0.9, yoyo: true, repeat: Math.ceil((END - t) / 0.9), ease: "sine.inOut", immediateRender: false }, t + 0.4);
    if (o.until != null) tl.to(el, { autoAlpha: 0, duration: 0.3 }, o.until);
    return el;
  };
  // hurricane glyph that travels along a track (returns the route)
  S.hurricane = (pts, o = {}) => {
    const r = S.route(pts, { color: o.color || "#f0f0f0", width: 5, dash: [10, 10], t: o.t, dur: o.dur, ease: "none" });
    const s = S.scaleAt(o.t || 0), w = (o.size || 74) / s;
    const el = document.createElement("div"); el.style.cssText = "position:absolute;left:0;top:0;";
    el.innerHTML = `<div class="spin" style="width:${w}px;height:${w}px;transform:translate(-50%,-50%);filter:drop-shadow(0 0 ${8 / s}px rgba(0,0,0,.9))">${ICON.hurricane(o.color || "#f3eee2").replace("<svg ", `<svg width="${w}" height="${w}" style="display:block;overflow:visible" `)}</div>`;
    document.getElementById("pins").appendChild(el);
    const pr = { p: 0 }; const upd = () => { const q = r.at(pr.p); el.style.transform = `translate(${q[0]}px,${q[1]}px)`; }; upd();
    gsap.set(el, { autoAlpha: 0 }); tl.to(el, { autoAlpha: 1, duration: 0.3 }, o.t || 0);
    tl.to(pr, { p: 1, duration: o.dur || 3, ease: "none", onUpdate: upd, immediateRender: false }, o.t || 0);
    tl.fromTo(el.querySelector("svg"), { rotation: 0 }, { rotation: -720, duration: END + 1, ease: "none", transformOrigin: "50% 50%", immediateRender: true }, 0);
    return { route: r, el, at: r.at };
  };
  // storm swirl (big soft cloud spiral) moving across the screen-world from A to B
  S.storm = (A, Bp, o = {}) => {
    const t = o.t || 0, s = S.scaleAt(t), w = (o.size || 620) / s;
    const el = document.createElement("div"); el.style.cssText = `position:absolute;left:${A[0] - w / 2}px;top:${A[1] - w / 2}px;width:${w}px;height:${w}px;pointer-events:none`;
    const arms = [0, 120, 240].map((a) => `<path transform="rotate(${a})" d="M0 0 C 40 -10 90 -60 70 -150 C 120 -80 110 0 40 30 Z" fill="rgba(235,240,245,.55)"/>`).join("");
    el.innerHTML = `<svg viewBox="-200 -200 400 400" width="${w}" height="${w}" style="display:block;overflow:visible;filter:blur(${6}px)"><circle r="190" fill="url(#skst)"/><defs><radialGradient id="skst"><stop offset="0" stop-color="rgba(230,236,242,.6)"/><stop offset=".55" stop-color="rgba(200,210,220,.25)"/><stop offset="1" stop-color="rgba(200,210,220,0)"/></radialGradient></defs><g class="arms">${arms}</g><circle r="16" fill="rgba(20,30,40,.8)"/></svg>`;
    document.getElementById("pins").appendChild(el);
    tl.fromTo(el, { autoAlpha: 0, x: 0, y: 0 }, { autoAlpha: 0.95, duration: 0.6, immediateRender: true }, t);
    tl.to(el, { x: Bp[0] - A[0], y: Bp[1] - A[1], duration: o.dur || 2.5, ease: "none" }, t);
    tl.fromTo(el.querySelector(".arms"), { rotation: 0 }, { rotation: -300, duration: (o.dur || 2.5) + 0.5, ease: "none", svgOrigin: "0 0", immediateRender: true }, t);
    if (o.until != null) tl.to(el, { autoAlpha: 0, duration: 0.5 }, o.until);
    return el;
  };
  S.clouds = (n = 5, op = 0.14) => LivingK(B).clouds({ n, opacity: op });
  S.finish = () => {   // the one tween that drives camera + screen followers
    { const d = document.getElementById("date"); if (d) d.style.display = "none"; }
    place(0);
    const pr = { t: 0 };
    tl.to(pr, { t: END, duration: END, ease: "none", onUpdate: function () { place(this.time()); }, immediateRender: false }, 0);
    window.__timelines = window.__timelines || {};
  };
  return S;
};
