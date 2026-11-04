// LIVING MAP (map-detail test, owner 2026-10-06): small always-on motion and map furniture.
// const L = LivingK(B, { mpp }) ; L.clouds({ t0, t1, n, opacity }) ; L.shimmer(paths, { t0, t1 }) ; L.scaleBar(mpp) ; L.north()
window.LivingK = function (B, opt = {}) {
  const tl = B.tl, world = document.getElementById("world"), scene = document.getElementById("scene");
  const L = {};
  // slow cloud shadows drifting across the land (soft dark blobs in world space, under labels and units)
  L.clouds = (o = {}) => {
    const n = o.n || 6, t0 = o.t0 || 0, t1 = o.t1 != null ? o.t1 : B.T.duration, op = o.opacity != null ? o.opacity : 0.22;
    const layer = document.createElement("div"); layer.style.cssText = "position:absolute;left:0;top:0;width:2880px;height:1620px;pointer-events:none;overflow:hidden";
    world.insertBefore(layer, document.getElementById("overlay"));
    let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < n; i++) {
      const w = 500 + rnd() * 600, h = w * (0.45 + rnd() * 0.3), x = rnd() * 3200 - 400, y = rnd() * 1500 - 100;
      const c = document.createElement("div");
      c.style.cssText = `position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:50%;background:radial-gradient(ellipse at center, rgba(0,0,0,${op}) 0%, rgba(0,0,0,${op * 0.55}) 45%, rgba(0,0,0,0) 72%);filter:blur(18px)`;
      layer.appendChild(c);
      tl.fromTo(c, { x: 0, y: 0 }, { x: 260 + rnd() * 160, y: -60 - rnd() * 60, duration: Math.max(1, t1 - t0), ease: "none" }, t0);
    }
    return layer;
  };
  // shimmer travelling along rivers: paths = [[[x,y],...], ...] in map px
  L.shimmer = (paths, o = {}) => {
    const svg = document.getElementById("overlay"), t0 = o.t0 || 0, t1 = o.t1 != null ? o.t1 : B.T.duration;
    paths.forEach((pts, i) => {
      const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
      p.setAttribute("d", "M" + pts.map((q) => q[0].toFixed(1) + " " + q[1].toFixed(1)).join(" L"));
      p.setAttribute("fill", "none"); p.setAttribute("stroke", o.color || "rgba(220,238,255,0.55)"); p.setAttribute("stroke-width", o.width || 1.6);
      p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-dasharray", "10 46");
      svg.insertBefore(p, svg.firstChild);
      tl.fromTo(p, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -56 * (t1 - t0) * 0.6 }, duration: Math.max(1, t1 - t0), ease: "none" }, t0);
    });
  };
  // scale bar (bottom-left) that follows the camera zoom, and a north arrow
  L.scaleBar = (mpp, o = {}) => {
    const el = document.createElement("div"); el.style.cssText = "position:absolute;left:70px;bottom:52px;font-family:Oswald;color:#f4f1ea;font-size:18px;letter-spacing:.12em;text-shadow:0 1px 3px #000;z-index:20";
    el.innerHTML = `<div class="bar" style="height:8px;border:2px solid #f4f1ea;border-top:none;box-shadow:0 1px 3px rgba(0,0,0,.6)"></div><div class="lab" style="margin-top:4px"></div>`;
    scene.insertBefore(el, document.getElementById("credit"));
    const bar = el.querySelector(".bar"), lab = el.querySelector(".lab"), NICE = [0.5, 1, 2, 5, 10, 20, 25, 50, 100, 200];
    const upd = () => { const s = gsap.getProperty(world, "scale") || 1, mPerScreenPx = mpp / s;
      const km = NICE.find((k) => (k * 1000) / mPerScreenPx >= 110) || 200; bar.style.width = ((km * 1000) / mPerScreenPx).toFixed(0) + "px"; lab.textContent = km + (km < 1 ? "" : "") + " KM"; };
    tl.eventCallback("onUpdate", ((prev) => function () { if (prev) prev.apply(this, arguments); upd(); })(tl.eventCallback("onUpdate")));
    upd(); return el;
  };
  L.north = () => {
    const el = document.createElement("div"); el.style.cssText = "position:absolute;right:70px;top:150px;width:44px;text-align:center;font-family:Oswald;color:#f4f1ea;font-size:18px;text-shadow:0 1px 3px #000;z-index:20";
    el.innerHTML = `<svg width="30" height="44" viewBox="0 0 30 44" style="display:block;margin:0 auto;filter:drop-shadow(0 1px 2px rgba(0,0,0,.7))"><path d="M15 2 L27 40 L15 32 L3 40 Z" fill="#f4f1ea"/><path d="M15 2 L15 32 L3 40 Z" fill="#9a9384"/></svg>N`;
    scene.insertBefore(el, document.getElementById("credit")); return el;
  };
  return L;
};
