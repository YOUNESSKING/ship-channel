// GLOBE OPENING ("Frontlines" style, owner test 2026-10-05): dark NASA Blue Marble Earth in space with clouds + atmosphere glow,
// the camera swings to Europe, a series title, a glowing place marker, then dives straight down through the clouds.
// Globe(B, GG, { tex, clouds, keys: [[t, lat, lon, dist]], target: [lat, lon, "LABEL", tLabel], title: [kicker, name, sub, t0, t1], diveT, cloudT })
window.Globe = function (B, GG, o) {
document.getElementById("world").style.visibility = "hidden";
document.getElementById("date").style.display = "none";
document.getElementById("credit").textContent = "Earth: NASA Earth Observatory (Blue Marble, public domain)";
const scene = document.getElementById("scene");
const cv = document.createElement("canvas"); cv.width = 1920; cv.height = 1080; cv.style.cssText = "position:absolute;inset:0;";
scene.insertBefore(cv, document.getElementById("fx"));
const R = new THREE.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(1920, 1080, false); R.setClearColor(0x020306);
const S3 = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(36, 1920 / 1080, 0.05, 5000);
const xyz = (lat, lon, r) => { const ph = (lon + 180) / 180 * Math.PI, th = (90 - lat) / 180 * Math.PI;
  return new THREE.Vector3(-r * Math.cos(ph) * Math.sin(th), r * Math.cos(th), r * Math.sin(ph) * Math.sin(th)); };
// stars (seeded, so every render frame is identical)
let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const sg = new THREE.BufferGeometry(), sp = [];
for (let i = 0; i < 2500; i++) { const v = new THREE.Vector3(rnd() - 0.5, rnd() - 0.5, rnd() - 0.5).normalize().multiplyScalar(2500); sp.push(v.x, v.y, v.z); }
sg.setAttribute("position", new THREE.Float32BufferAttribute(sp, 3));
S3.add(new THREE.Points(sg, new THREE.PointsMaterial({ color: 0xbfc8d8, size: 2.2, sizeAttenuation: false, transparent: true, opacity: 0.7 })));
const TL = new THREE.TextureLoader();
const earth = new THREE.Mesh(new THREE.SphereGeometry(100, 160, 120), new THREE.MeshPhongMaterial({ map: TL.load(o.tex), shininess: 10, specular: 0x1a222e }));
S3.add(earth);
const cloudMat = new THREE.MeshLambertMaterial({ map: TL.load(o.clouds), transparent: true, opacity: 0.55, depthWrite: false });
const clouds = new THREE.Mesh(new THREE.SphereGeometry(100.9, 160, 120), cloudMat); S3.add(clouds);
const atm = new THREE.Mesh(new THREE.SphereGeometry(104, 96, 72), new THREE.ShaderMaterial({ side: THREE.BackSide, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false,
  vertexShader: "varying vec3 vN; void main(){ vN = normalize(normalMatrix * normal); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
  fragmentShader: "varying vec3 vN; void main(){ float i = pow(0.72 - dot(vN, vec3(0.0,0.0,1.0)), 3.0); gl_FragColor = vec4(0.35,0.55,1.0,1.0) * i; }" }));
S3.add(atm);
S3.add(new THREE.AmbientLight(0x8090a8, 0.42));
const sun = new THREE.DirectionalLight(0xfff1dc, 1.05); sun.position.copy(xyz(38, -35, 1000)); S3.add(sun);
// glowing target marker (HTML, projected)
const css = document.createElement("style");
css.textContent = `.gl-lbl{position:absolute;left:0;top:0;transform:translate(-50%,-100%);white-space:nowrap;font-family:Oswald;font-weight:500;letter-spacing:.3em;color:#f4efe2;font-size:26px;text-shadow:0 0 12px rgba(255,214,140,.6),0 2px 4px #000}
.gl-lbl:after{content:"";display:block;margin:8px auto 0;width:12px;height:12px;border-radius:50%;background:#ffd58a;box-shadow:0 0 16px 6px rgba(255,190,90,.8)}
.gl-title{position:absolute;left:0;right:0;text-align:center;font-family:Oswald;color:#f4efe2;text-shadow:0 3px 22px rgba(0,0,0,.95)}
.gl-cloud{position:absolute;left:50%;top:50%;width:1400px;height:800px;margin:-400px 0 0 -700px;opacity:0}
#gl-white{position:absolute;inset:0;background:radial-gradient(ellipse at center,#eef0f3 0%,#d9dde3 60%,#b9bfc8 100%);opacity:0}`;
document.head.appendChild(css);
const [tLat, tLon, tName, tLab] = o.target;
const lbl = document.createElement("div"); lbl.className = "gl-lbl"; lbl.textContent = tName; scene.insertBefore(lbl, document.getElementById("credit"));
const tP = xyz(tLat, tLon, 101.2);
// camera keyframes [t, lat, lon, dist]; smooth (cosine) interpolation between keys
const K = o.keys, st = { t: 0, lab: 0 };
const camAt = (t) => { let i = 0; while (i < K.length - 2 && t > K[i + 1][0]) i++;
  const a = K[i], b = K[i + 1], u = Math.min(1, Math.max(0, (t - a[0]) / (b[0] - a[0]))), e = (1 - Math.cos(Math.PI * u)) / 2;
  return [a[1] + (b[1] - a[1]) * e, a[2] + (b[2] - a[2]) * e, a[3] + (b[3] - a[3]) * Math.pow(e, b[4] || 1)]; };
const render = () => {
  const [la, lo, d] = camAt(st.t); cam.position.copy(xyz(la, lo, d)); cam.lookAt(0, 0, 0);
  clouds.rotation.y = st.t * 0.004;
  cloudMat.opacity = 0.55 + 0.35 * Math.max(0, Math.min(1, (st.t - o.diveT) / (o.cloudT - o.diveT)));
  R.render(S3, cam);
  const v = tP.clone().project(cam); const facing = tP.clone().normalize().dot(cam.position.clone().normalize()) > 0.2;
  lbl.style.left = ((v.x + 1) / 2 * 1920) + "px"; lbl.style.top = ((1 - v.y) / 2 * 1080) + "px"; lbl.style.opacity = facing ? st.lab : 0;
};
B.tl.to(st, { t: B.T.duration, duration: B.T.duration, ease: "none", onUpdate: render }, 0);
B.tl.fromTo(st, { lab: 0 }, { lab: 1, duration: 1.0, onUpdate: render, immediateRender: false }, tLab);
B.tl.to(st, { lab: 0, duration: 0.6, onUpdate: render }, o.diveT + 0.6);
B.tl.eventCallback("onUpdate", render);
render();
// series title: thin kicker, big name, sub line
const [k1, k2, k3, t0, t1] = o.title;
const ti = document.createElement("div"); ti.className = "gl-title"; ti.style.top = "390px";
ti.innerHTML = `<div style="font-size:30px;letter-spacing:.7em;color:#d9c9a3">${k1}</div><div style="font-size:124px;font-weight:700;letter-spacing:.06em;line-height:1.12">${k2}</div><div style="font-size:30px;letter-spacing:.45em;color:#d9c9a3">${k3}</div>`;
scene.insertBefore(ti, document.getElementById("credit")); GG.hide(ti);
B.tl.fromTo(ti, { autoAlpha: 0, letterSpacing: "0.25em", scale: 1.04 }, { autoAlpha: 1, letterSpacing: "0em", scale: 1, duration: 1.6, ease: "power2.out" }, t0);
B.tl.to(ti, { autoAlpha: 0, duration: 1.0 }, t1);
// flying through the clouds: soft puffs rush past, then white-out (the next scene starts in the same white and clears)
const wh = document.createElement("div"); wh.id = "gl-white"; scene.insertBefore(wh, document.getElementById("credit"));
[0, 1, 2, 3, 1, 2].forEach((n, i) => {
  const c = document.createElement("img"); c.className = "gl-cloud"; c.src = `assets/media/cloud_puff${n}.png`; scene.insertBefore(c, wh);
  const t = o.cloudT - 1.1 + i * 0.22, dx = [-420, 380, -200, 300, 120, -330][i], dy = [-180, 160, 220, -140, -40, 60][i];
  B.tl.fromTo(c, { opacity: 0, scale: 0.5, x: dx * 0.3, y: dy * 0.3 }, { opacity: 0.95, scale: 1.6, x: dx, y: dy, duration: 0.7, ease: "power1.in", immediateRender: false }, t);
  B.tl.to(c, { scale: 3.4, x: dx * 2.4, y: dy * 2.4, opacity: 0, duration: 0.7, ease: "power1.in" }, t + 0.7);
});
B.tl.fromTo(wh, { opacity: 0 }, { opacity: 1, duration: 0.9, ease: "power2.in", immediateRender: false }, o.cloudT - 0.6);
};
