// 3D TACTICAL BOARD ("Frontlines" style test): the dark map texture on a flat plane seen by a moving perspective camera;
// everything on it (units, boats, fire, arrows) is drawn in one SVG layer, projected from map px every frame.
// Board(B, { tex, keys: [[t, camX, camY(height), camZ, lookX, lookZ]] (map px; Y = height) }) -> { svg, P(x, y) -> [sx, sy], hooks, render }
window.Board = function (B, o) {
document.getElementById("world").style.visibility = "hidden";
document.getElementById("date").style.display = "none";
const scene = document.getElementById("scene");
const cv = document.createElement("canvas"); cv.width = 1920; cv.height = 1080; cv.style.cssText = "position:absolute;inset:0;";
scene.insertBefore(cv, document.getElementById("fx"));
const R = new THREE.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(1920, 1080, false); R.setClearColor(0x07090d);
const S3 = new THREE.Scene(); S3.fog = new THREE.Fog(0x07090d, 900, 2600);
const cam = new THREE.PerspectiveCamera(40, 1920 / 1080, 1, 8000);
const geo = new THREE.PlaneGeometry(2880, 1620); geo.rotateX(-Math.PI / 2);
const tex = new THREE.TextureLoader().load(o.tex); tex.anisotropy = 8;
S3.add(new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tex })));
const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
svg.setAttribute("width", 1920); svg.setAttribute("height", 1080); svg.style.cssText = "position:absolute;inset:0;overflow:visible";
svg.innerHTML = `<defs><filter id="bglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>`;
scene.insertBefore(svg, document.getElementById("credit"));
const K = o.keys, st = { t: 0 }, hooks = [];
const at = (t) => { let i = 0; while (i < K.length - 2 && t > K[i + 1][0]) i++;
  const a = K[i], b = K[i + 1], u = Math.min(1, Math.max(0, (t - a[0]) / (b[0] - a[0]))), e = (1 - Math.cos(Math.PI * u)) / 2;
  return a.map((v, j) => v + (b[j] - v) * e); };
const P = (x, y, h = 0) => { const v = new THREE.Vector3(x - 1440, h, y - 810).project(cam); return [(v.x + 1) / 2 * 1920, (1 - v.y) / 2 * 1080]; };
const render = () => {
  const k = at(st.t); cam.position.set(k[1] - 1440, k[2], k[3] - 810); cam.lookAt(k[4] - 1440, 0, k[5] - 810);
  R.render(S3, cam); hooks.forEach((f) => f(P));
};
B.tl.to(st, { t: B.T.duration, duration: B.T.duration, ease: "none", onUpdate: render }, 0);
B.tl.eventCallback("onUpdate", render); tex.onUpdate = render; render();
return { svg, P, hooks, render };
};
