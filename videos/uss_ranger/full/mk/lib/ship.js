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
  const S = { B, tl, END, GOLD: "#D9572B", ORG: "#D9572B", TEAL: "#8fb0cc", STEEL: "#8fb0cc", BLUE: "#4f8df0", RED: "#e0403a", INK: "#f3eee2", BOX: "rgba(10,24,38,.9)" };
  const css = document.createElement("style");
  css.textContent = `
    .sk-f { position:absolute; left:0; top:0; will-change: transform; }
    .sk-lbl { position:absolute; white-space:nowrap; font-family:Oswald; font-weight:700; letter-spacing:.08em; color:#f7f3ea;
              text-shadow:0 2px 6px rgba(0,0,0,.95), 0 0 3px #000; }
    .sk-box { padding:2px 14px; background:rgba(10,24,38,.9); border:2px solid #f3eee2; border-radius:3px; text-shadow:none; }
    .sk-date { position:absolute; left:90px; top:78px; font-family:Oswald; font-weight:700; font-size:46px; letter-spacing:.16em;
               color:#f7f3ea; text-shadow:0 2px 8px rgba(0,0,0,.9); white-space:nowrap; }
    .sk-date .rule { height:3px; background:#D9572B; margin-top:6px; transform-origin:0 50%; box-shadow:0 1px 4px rgba(0,0,0,.7); }
    .sk-card { position:absolute; font-family:Oswald; font-weight:700; color:#f4f1ea; background:rgba(12,18,26,.9);
               border-top:6px solid #D9572B; padding:26px 48px 30px; box-shadow:0 20px 40px rgba(0,0,0,.5); text-align:center; }
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
    BNY: [40.7003, -73.9729], HANOI: [21.03, 105.85], TRUCBACH: [21.047, 105.838], YANKEE: [17.5, 108.5],
    // Mallows Bay (FACTCHECK_C: GNIS bay point; White House; FACTCHECK_B: Sandy Point just north of the bay, Widewater opposite)
    WH: [38.8977, -77.0365], MALLOWS: [38.4726, -77.2686], QUANTICO: [38.5221, -77.2930], WIDEWATER: [38.445, -77.318],
    ALEX: [38.8048, -77.0469], SANDY: [38.487, -77.262], BASIN: [38.466, -77.262], NANJ: [38.455, -77.215],
    NORTHBEND: [43.4065, -124.2243], ABERDEEN: [46.9754, -123.8157], JAMES: [37.13, -76.65], BERLIN: [52.52, 13.40],
    FRANCE: [47.5, -2.5], BRITAIN: [51.5, -1.5], NYC: [40.70, -74.00], ARMEUR: [49.0, 2.3] };
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
    const d = rings.map((r) => "M" + r.map((q) => (o.px ? q : S.G(q[1], q[0])).map((v) => v.toFixed(1)).join(",")).join("L") + "Z").join("");
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
  // Mallows Bay helpers: S.wt = spoken-word time with a fallback (never throws); S.hulls = rows of small hull ovals (world space)
  S.wt = (word, fb = 0.2, k = 0, off = 0) => { try { return S.w(word, k, off); } catch (e) { return fb; } };
  S.hulls = (C, o = {}) => {
    const t = o.t || 0, s = S.scaleAt(t), rows = o.rows || 6, cols = o.cols || 10, L = (o.len || 34) / s, W = L * 0.24, gx = W * 2.1, gy = L * 1.25;
    const ang = o.rot || -60, c = o.color || "rgba(243,238,226,.82)";
    const g = document.createElementNS(NS, "g"); let k = 0;
    for (let r = 0; r < rows; r++) for (let q = 0; q < cols; q++) {
      if (o.ragged && ((r * 7 + q * 3) % 5 === 0)) continue;
      const x = (q - cols / 2) * gx + (r % 2) * gx * 0.5, y = (r - rows / 2) * gy;
      const e = document.createElementNS(NS, "ellipse");
      e.setAttribute("cx", (C[0] + x).toFixed(1)); e.setAttribute("cy", (C[1] + y).toFixed(1)); e.setAttribute("rx", (W / 2).toFixed(2)); e.setAttribute("ry", (L / 2).toFixed(2));
      e.setAttribute("fill", "rgba(40,30,22,.55)"); e.setAttribute("stroke", c); e.setAttribute("stroke-width", (1.6 / s).toFixed(2));
      g.appendChild(e); k++;
      tl.fromTo(e, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.25, immediateRender: true }, t + (o.stagger || 0.012) * k);
    }
    g.setAttribute("transform", `rotate(${ang} ${C[0]} ${C[1]})`);
    svg.appendChild(g); return g;
  };

  // ================= USS Nevada additions =================
  const mpp = M.meters_per_px;
  S.mpx = (m) => m / mpp;                                              // metres -> map px (at the basemap centre latitude)
  S.off = (pt, eastM, northM) => [pt[0] + eastM / mpp, pt[1] - northM / mpp];
  S.yd = (y) => y * 0.9144;

  // ---- USS Nevada places (lat, lon) ----
  Object.assign(S.PL, {
    PEARL: [21.345, -157.975], ENTR: [21.318, -157.968], FORD: [21.3644, -157.9600], HOSP: [21.3410, -157.9645], WAIPIO: [21.3432, -157.9720],
    BIKINI: [11.6, 165.45], KWAJ: [8.72, 167.73], ATTU: [52.9, 173.1], PUGET: [47.56, -122.63], UTAH: [49.42, -1.18], CHERB: [49.64, -1.62],
    TOULON: [43.12, 5.93], IWO: [24.78, 141.32], OKI: [26.3, 127.8], WRECK: [20.9, -158.95], OAHU: [21.45, -157.95], NORFOLK: [36.95, -76.3],
    BANGOR: [54.66, -5.67], AIM: [11.583, 165.507], BURSTA: [11.583, 165.50197], BURSTB: [11.585, 165.505],
    // Battleship Row, 7 Dec 1941 (berth centres, from the OSM shore of Ford Island; row runs NE -> SW along the island's east shore)
    NV: [21.36438, -157.95117], AZ: [21.36296, -157.95303], AZ_O: [21.36234, -157.95236], TN: [21.36142, -157.95465], WV: [21.36081, -157.95398],
    MD: [21.35989, -157.95628], OK: [21.35928, -157.9556], CA: [21.35819, -157.95771] });
  // Nevada's 08:40 run: out from F-8, down the row, then the channel to the entrance (lat, lon)
  S.RUN = [[21.36438, -157.95117], [21.36247, -157.94909], [21.35964, -157.95186], [21.3568, -157.95486], [21.35555, -157.95715], [21.35462, -157.95816],
    [21.35222, -157.96417], [21.34862, -157.96889], [21.34183, -157.97121], [21.33383, -157.97258], [21.32744, -157.97173], [21.32104, -157.96889], [21.31544, -157.96761], [21.30745, -157.96846]];
  S.ang = (a, b) => Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI;
  S.sl = (m, t = 0, k = 1.35) => m / mpp * S.scaleAt(t) * k;     // ship length in SCREEN px for a real length in metres (k = exaggeration)
  // top-down ship silhouettes, drawn pointing right (+x) in a 100 x 24 box
  const SHIP = {
    bb: '<path d="M-49 -5.5 L28 -8 L40 -5 L50 0 L40 5 L28 8 L-49 5.5 Z"/><g class="d"><circle cx="-30" cy="0" r="4.2"/><circle cx="-18" cy="0" r="4.2"/><circle cx="26" cy="0" r="4.2"/><rect x="-4" y="-4" width="14" height="8" rx="2"/></g>',
    cru: '<path d="M-49 -4.2 L26 -5.8 L38 -3.5 L50 0 L38 3.5 L26 5.8 L-49 4.2 Z"/><g class="d"><circle cx="-34" cy="0" r="3"/><circle cx="30" cy="0" r="3"/><rect x="-10" y="-3" width="14" height="6" rx="2"/></g>',
    dd: '<path d="M-49 -3 L28 -4 L50 0 L28 4 L-49 3 Z"/><g class="d"><rect x="-6" y="-2.2" width="10" height="4.4" rx="1.5"/></g>',
    tr: '<path d="M-49 -6 L36 -6.5 L50 0 L36 6.5 L-49 6 Z"/><g class="d"><rect x="-30" y="-4" width="12" height="8"/><rect x="2" y="-4" width="12" height="8"/></g>',
    lsm: '<path d="M-49 -6 L38 -6 L50 -3 L50 3 L38 6 L-49 6 Z"/><g class="d"><rect x="-44" y="-4" width="12" height="8"/></g>',
    tug: '<path d="M-26 -8 L18 -9 L28 0 L18 9 L-26 8 Z"/><g class="d"><rect x="-16" y="-5" width="16" height="10" rx="2"/></g>',
    b29: '<path d="M50 0 L14 -3 L8 -22 L-1 -22 L-2 -3 L-34 -2 L-40 -9 L-47 -9 L-45 0 L-47 9 L-40 9 L-34 2 L-2 3 L-1 22 L8 22 L14 3 Z"/>',
  };
  const SHIP_H = { bb: 24, cru: 20, dd: 14, tr: 20, lsm: 20, tug: 28, b29: 48 };
  S.ship = (kind, pt, o = {}) => {
    const t = o.t || 0, s = S.scaleAt(t), w = (o.len || 90) / s, fill = o.fill || "#f3eee2", stroke = o.stroke || "#D9572B";
    const h = w * (SHIP_H[kind] || 24) / 100 * (o.fat || 2.1);
    const wrap = document.createElement("div"); wrap.style.cssText = `position:absolute;left:${pt[0]}px;top:${pt[1]}px;width:0;height:0;will-change:transform`;
    const inner = document.createElement("div"); inner.style.cssText = `position:absolute;left:0;top:0;width:${w}px;height:${h}px;filter:drop-shadow(0 0 ${6 / s}px rgba(0,0,0,.9))`;
    inner.innerHTML = `<svg width="${w}" height="${h}" viewBox="-50 ${-(SHIP_H[kind] || 24) / 2} 100 ${SHIP_H[kind] || 24}" preserveAspectRatio="none" style="display:block;overflow:visible"><g fill="${fill}" stroke="${stroke}" stroke-width="${o.sw || 2.6}" stroke-linejoin="round">${SHIP[kind]}</g></svg>`;
    inner.querySelectorAll(".d").forEach((g) => { g.setAttribute("fill", o.deck || "rgba(20,28,38,.55)"); g.setAttribute("stroke", "none"); });
    wrap.appendChild(inner); document.getElementById("pins").appendChild(wrap);
    gsap.set(inner, { xPercent: -50, yPercent: -50, rotation: o.rot || 0, transformOrigin: "50% 50%" });
    gsap.set(wrap, { autoAlpha: 0 });
    tl.to(wrap, { autoAlpha: 1, duration: o.dur || 0.45, ease: "power2.out" }, t);
    if (o.until != null) tl.to(wrap, { autoAlpha: 0, duration: 0.35 }, o.until);
    return { wrap, inner, p0: pt, s };
  };
  // path sample (smooth through pts) for movers
  const sampleHidden = (pts) => { const g = document.createElementNS(NS, "path"); g.setAttribute("d", smooth(pts)); g.setAttribute("fill", "none"); g.setAttribute("stroke", "none"); svg.appendChild(g);
    const L = g.getTotalLength(), N = 200, a = []; for (let i = 0; i <= N; i++) { const q = g.getPointAtLength(L * i / N); a.push([q.x, q.y]); }
    return (p) => { const f = Math.min(N, Math.max(0, p * N)), i = Math.min(N - 1, Math.floor(f)), u = f - i; const A = a[i], Bq = a[i + 1], P = a[Math.min(N, i + 4)], Q = a[Math.max(0, i - 3)];
      return [A[0] + (Bq[0] - A[0]) * u, A[1] + (Bq[1] - A[1]) * u, Math.atan2(P[1] - Q[1], P[0] - Q[0]) * 180 / Math.PI]; }; };
  // move a ship along pts (world px): o.t, o.dur, o.ease, o.rotAdd (deg added to the travel heading: 180 = stern first), o.keepRot
  S.sail = (sh, pts, o = {}) => {
    const at = sampleHidden(pts), pr = { p: 0 }, p0 = sh.p0, add = o.rotAdd || 0;
    const upd = () => { const q = at(pr.p); gsap.set(sh.wrap, { x: q[0] - p0[0], y: q[1] - p0[1] }); if (!o.keepRot) gsap.set(sh.inner, { rotation: q[2] + add }); };
    tl.to(pr, { p: 1, duration: o.dur || 2, ease: o.ease || "power1.inOut", onUpdate: upd, immediateRender: false }, o.t || 0);
    return at;
  };
  S.turn = (sh, from, to, t, dur = 0.8) => tl.fromTo(sh.inner, { rotation: from }, { rotation: to, duration: dur, ease: "sine.inOut", immediateRender: false }, t);
  // static circle (radius in metres, or screen px with o.px) drawn in the world; pops in
  S.circ = (pt, rM, o = {}) => {
    const t = o.t || 0, s = S.scaleAt(t), r = o.px ? o.px / s : rM / mpp, c = o.color || "#f3eee2";
    const g = document.createElementNS(NS, "circle"); g.setAttribute("cx", pt[0]); g.setAttribute("cy", pt[1]); g.setAttribute("r", r);
    g.setAttribute("fill", o.fill || "none"); g.setAttribute("stroke", c); g.setAttribute("stroke-width", (o.width || 3.5) / s);
    if (o.dash) g.setAttribute("stroke-dasharray", `${o.dash[0] / s} ${o.dash[1] / s}`);
    g.style.filter = `drop-shadow(0 0 ${4 / s}px ${c})`; svg.appendChild(g);
    tl.fromTo(g, { autoAlpha: 0, scale: 0.25, svgOrigin: `${pt[0]} ${pt[1]}` }, { autoAlpha: 1, scale: 1, svgOrigin: `${pt[0]} ${pt[1]}`, duration: o.dur || 0.6, ease: "power2.out", immediateRender: true }, t);
    if (o.until != null) tl.to(g, { autoAlpha: 0, duration: 0.35 }, o.until);
    return g;
  };
  S.cross = (pt, o = {}) => {  // crosshair, screen-size radius
    const t = o.t || 0, s = S.scaleAt(t), r = (o.r || 34) / s, c = o.color || "#f3eee2", w = 3 / s;
    const g = document.createElementNS(NS, "g");
    g.innerHTML = `<circle cx="${pt[0]}" cy="${pt[1]}" r="${r}" fill="none" stroke="${c}" stroke-width="${w}"/><path d="M${pt[0] - r * 1.5},${pt[1]} H${pt[0] - r * 0.45} M${pt[0] + r * 0.45},${pt[1]} H${pt[0] + r * 1.5} M${pt[0]},${pt[1] - r * 1.5} V${pt[1] - r * 0.45} M${pt[0]},${pt[1] + r * 0.45} V${pt[1] + r * 1.5}" stroke="${c}" stroke-width="${w}" fill="none"/>`;
    g.style.filter = `drop-shadow(0 0 ${4 / s}px rgba(0,0,0,.9))`; svg.appendChild(g);
    tl.fromTo(g, { autoAlpha: 0, scale: 1.8, svgOrigin: `${pt[0]} ${pt[1]}` }, { autoAlpha: 1, scale: 1, svgOrigin: `${pt[0]} ${pt[1]}`, duration: 0.5, ease: "power2.out", immediateRender: true }, t);
    if (o.until != null) tl.to(g, { autoAlpha: 0, duration: 0.3 }, o.until);
    return g;
  };
  S.burst = (pt, t, o = {}) => {   // blast star (screen size), pops and stays
    const s = S.scaleAt(t), r = (o.r || 40) / s, c = o.color || "#D9572B";
    let d = ""; for (let i = 0; i < 16; i++) { const a = i * Math.PI / 8, rr = i % 2 ? r * 0.45 : r; d += (i ? "L" : "M") + (pt[0] + Math.cos(a) * rr).toFixed(1) + "," + (pt[1] + Math.sin(a) * rr).toFixed(1); }
    const g = document.createElementNS(NS, "g");
    g.innerHTML = `<path d="${d}Z" fill="#fff4dc" stroke="${c}" stroke-width="${5 / s}" stroke-linejoin="round" style="filter:drop-shadow(0 0 ${12 / s}px ${c})"/><circle cx="${pt[0]}" cy="${pt[1]}" r="${r * 0.22}" fill="${c}"/>`;
    svg.appendChild(g); gsap.set(g, { autoAlpha: 0 });
    tl.fromTo(g, { autoAlpha: 0, scale: 0.2, svgOrigin: `${pt[0]} ${pt[1]}` }, { autoAlpha: 1, scale: 1, svgOrigin: `${pt[0]} ${pt[1]}`, duration: 0.3, ease: "back.out(2.4)", immediateRender: false }, t);
    if (o.until != null) tl.to(g, { autoAlpha: 0, duration: 0.4 }, o.until);
    return g;
  };
  S.xmark = (pt, t, o = {}) => {
    const s = S.scaleAt(t), r = (o.r || 24) / s, c = o.color || "#e0403a";
    const g = document.createElementNS(NS, "g");
    g.innerHTML = `<path d="M${pt[0] - r},${pt[1] - r} L${pt[0] + r},${pt[1] + r} M${pt[0] + r},${pt[1] - r} L${pt[0] - r},${pt[1] + r}" stroke="#0c1218" stroke-width="${12 / s}" stroke-linecap="round"/><path d="M${pt[0] - r},${pt[1] - r} L${pt[0] + r},${pt[1] + r} M${pt[0] + r},${pt[1] - r} L${pt[0] - r},${pt[1] + r}" stroke="${c}" stroke-width="${7 / s}" stroke-linecap="round"/>`;
    svg.appendChild(g); gsap.set(g, { autoAlpha: 0 });
    tl.fromTo(g, { autoAlpha: 0, scale: 2, svgOrigin: `${pt[0]} ${pt[1]}` }, { autoAlpha: 1, scale: 1, svgOrigin: `${pt[0]} ${pt[1]}`, duration: 0.25, ease: "power3.out", immediateRender: false }, t);
    return g;
  };

  // ---- shared pieces ----
  // Battleship Row companions (everything except Nevada): static grey-blue icons. o: t, len (screen px), rot (deg), until, only
  S.rowShips = (o = {}) => {
    const L = o.len || 34, out = {}, rot = o.rot != null ? o.rot : 135;
    const list = [["AZ", "bb"], ["AZ_O", "tr"], ["TN", "bb"], ["WV", "bb"], ["MD", "bb"], ["OK", "bb"], ["CA", "bb"]];
    for (const [k, kind] of list) { if (o.only && !o.only.includes(k)) continue;
      out[k] = S.ship(kind, S.P(k), { t: o.t || 0, len: kind === "tr" ? L * 0.8 : L, rot, fill: o.fill || "#b3cadf", stroke: o.stroke || "#0c1218", sw: 2.2, until: o.until, dur: o.dur }); }
    return out;
  };
  // deterministic scatter of target-ship dots around a point (metres radius), skipping a hole around `hole`
  S.scatter = (c, n, rM, seed = 7, hole = null, holeM = 500) => {
    let a = seed; const rnd = () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
    const out = []; let g = 0;
    while (out.length < n && g++ < 2000) { const ang = rnd() * 6.283, r = Math.sqrt(rnd()) * rM, p = S.off(c, Math.cos(ang) * r * 1.25, Math.sin(ang) * r * 0.8);
      if (hole && Math.hypot(p[0] - hole[0], p[1] - hole[1]) < holeM / mpp) continue;
      if (out.some((q) => Math.hypot(q[0] - p[0], q[1] - p[1]) < 150 / mpp)) continue; out.push(p); }
    return out;
  };
  S.fade = (el, t, dur = 0.5, to = 0) => tl.to(el, { autoAlpha: to, duration: dur }, t);   // fade a returned element (ship.wrap / dot / etc.)
  // ================= USS Ranger additions =================
  Object.assign(S.PL, {
    BREMERTON: [47.557, -122.632], SEATTLE: [47.606, -122.335], SANDIEGO: [32.70, -117.20], NORTHISLAND: [32.705, -117.19], CORONADO: [32.686, -117.183],
    NEWPORTNEWS: [36.98, -76.43], CAPEHORN: [-55.98, -67.27], PANAMA: [9.08, -79.68], BROWNSVILLE: [25.95, -97.40], BRAZOS: [26.07, -97.15],
    SOUTHPADRE: [26.10, -97.165], LEXMUS: [27.815, -97.389], FAIRVIEW: [45.546, -122.43], PORTLAND: [45.52, -122.68], COLMOUTH: [46.25, -124.05],
    MOGADISHU: [2.04, 45.34], ARABIAN: [16, 62], HORMUZ: [26.5, 56.3], TONKIN: [20.0, 107.6], IRAN: [32.0, 54.0], PERSGULF: [27.4, 51.6] });
  // ship icon of the Ranger: top-down carrier pointing right (flat deck, angled deck to port, island on the starboard side)
  SHIP.cv = '<path d="M-49 6 L-49 -6 L-42 -11.5 L-12 -9 L30 -6 L44 -4 L50 0 L44 4 L30 6 Z"/><g class="d"><rect x="4" y="2" width="11" height="3.6" rx="1"/></g>';
  SHIP_H.cv = 24;
  S.cv = (pt, o = {}) => S.ship("cv", pt, { len: 110, fat: 1.7, fill: "#D9572B", stroke: "#f7f3ea", sw: 2.4, ...o });
  // tow route 2015: Bremerton -> Juan de Fuca -> Pacific coast (offshore) -> round the southern tip -> up the Atlantic -> Gulf of Mexico -> Brazos Santiago.
  // Offshore illustrative polyline (exact route unverified); TOW_PAC ends at the southern tip, TOW_ATL continues from it.
  S.TOW_PAC = [[47.557, -122.632], [47.9, -122.62], [48.15, -123.1], [48.45, -124.9], [46.5, -125.6], [42, -126.2], [37, -124.3], [33, -120.3], [28.3, -117.2], [23.2, -112.2],
    [17.5, -106.5], [14, -98.5], [10, -91], [5, -85.5], [-1, -82.8], [-8, -82.3], [-16, -77.3], [-26, -73.3], [-36, -75.3], [-46, -77.6], [-53, -77.4], [-56.0, -74.0], [-57.3, -69.5]];
  S.TOW_ATL = [[-57.3, -69.5], [-57.2, -65.5], [-55.6, -61.5], [-50, -61.5], [-42, -57], [-35, -52], [-28, -46], [-22, -39.5], [-13, -35.5], [-6, -32.5], [1, -39], [6.5, -48], [11, -56],
    [15.2, -62.2], [15.8, -70], [17.5, -78], [20.2, -84.2], [21.7, -85.8], [24, -88], [25.3, -92], [25.7, -96.2], [26.07, -97.12]];
  S.TOW = S.TOW_PAC.concat(S.TOW_ATL.slice(1));
  // 1958 ghost line (Atlantic -> Cape Horn -> Pacific), schematic
  S.GHOST58 = [[-49, -56.2], [-52.5, -59], [-55, -63.5], [-56.15, -67.27], [-56.1, -70.5], [-54.3, -74.5], [-52.2, -77.3]];
  // Brownsville ship channel (schematic centre line, from the Brazos Santiago pass to the port)
  S.CHAN = [[26.07, -97.15], [26.06, -97.19], [26.035, -97.235], [26.0, -97.29], [25.97, -97.355], [25.952, -97.395]];
  // normal offset of a px path (right-hand normal in screen coords), d map px
  S.offsetPath = (pts, d) => pts.map((p, i) => { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
    return [p[0] - dy / L * d, p[1] + dx / L * d]; });
  S.COL = [[46.25, -124.05], [46.2, -123.85], [46.17, -123.5], [46.14, -123.1], [46.06, -122.9], [45.88, -122.8], [45.7, -122.77], [45.64, -122.62], [45.6, -122.45]];
  return S;
};
