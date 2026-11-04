// map agent va: probe a built scene frame by frame for flag placement problems (headless chrome).
//   node tools/va_probe.js SCENE [STEP=0.25]  -> JSON lines {t, flags:[{k,x,y,r,op}], hud:[{n,r}], pins:[{n,r}]}
// k = us|gb, (x, y) = world px of the pin, r = screen rect [x0,y0,x1,y1]; checked by tools/va_flagcheck.py
const path = require("path"), pp = require("/opt/node22/lib/node_modules/hyperframes/node_modules/puppeteer-core");
(async () => {
  const b = await pp.launch({ executablePath: "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell", args: ["--no-sandbox", "--allow-file-access-from-files"] });
  const p = await b.newPage(); await p.setViewport({ width: 1920, height: 1080 });
  await p.evaluateOnNewDocument(() => { window.__timelines = {}; });
  p.on("pageerror", (e) => console.error("ERR", e.message));
  await p.goto("file://" + path.resolve("scenes/" + process.argv[2] + "/index.html")); await new Promise((r) => setTimeout(r, 1500));
  const step = +(process.argv[3] || 0.25);
  const out = await p.evaluate((step) => {
    const tl = window.__timelines.main, END = tl.duration(), res = [];
    const eop = (el) => { let o = 1; for (let e = el; e && e !== document.body; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === "none" || cs.visibility === "hidden") return 0; o *= +cs.opacity;
      const m = /opacity\(([\d.]+)\)/.exec(cs.filter || ""); if (m) o *= +m[1]; } return o; };
    const R = (el) => { const r = el.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom].map((v) => Math.round(v)); };
    const scene = document.getElementById("scene"), world = document.getElementById("world");
    for (let t = 0; t <= END - 0.05; t += step) {
      tl.seek(t, false);
      const flags = [], hud = [], pins = [];
      world.querySelectorAll("img").forEach((im) => { const s = im.getAttribute("src") || ""; const k = /continental|us_flag/.test(s) ? "us" : /gb_flag/.test(s) ? "gb" : null; if (!k) return;
        const pin = im.closest(".gg-pin"); if (!pin || im.offsetWidth < 40) return; const op = eop(im); if (op < 0.05) return;
        flags.push({ k, x: Math.round(parseFloat(pin.style.left)), y: Math.round(parseFloat(pin.style.top)), r: R(im), op: +op.toFixed(2) }); });
      const inner = (el) => { let c = el; for (let i = 0; i < 4 && c; i++) { const r = R(c); if (r[2] - r[0] < 1880 && r[3] - r[1] < 1000) return c; c = c.firstElementChild; } return null; };
      [...scene.children].forEach((el) => { if (el === world || el.id === "credit") return; const c = inner(el); if (!c) return; const r = R(c); if (r[2] - r[0] < 2) return;
        const op = eop(c); if (op < 0.3) return; hud.push({ n: (el.id || el.className || "").toString().slice(0, 20) + ":" + (c.textContent || "").trim().slice(0, 24), r }); });
      world.querySelectorAll(".gg-pin").forEach((pin) => { if (pin.querySelector("img[src*=flag], img[src*=colours]")) return; const op = eop(pin); if (op < 0.3) return; const c = pin.firstElementChild; if (!c) return;
        const r = R(c.firstElementChild || c); if (r[2] - r[0] < 3 || r[2] < 0 || r[0] > 1920 || r[3] < 0 || r[1] > 1080) return; pins.push({ n: (pin.textContent || "").trim().slice(0, 22) || (pin.querySelector("svg") ? "svg" : "?"), r }); });
      const m = new DOMMatrix(getComputedStyle(world).transform); const wr = world.getBoundingClientRect();
      res.push({ t: +t.toFixed(2), flags, hud, pins, cam: [m.a, m.e, m.f, wr.left, wr.top] });
    }
    return res;
  }, step);
  require("fs").writeFileSync(`/tmp/claude-0/-home-user-battle-maps/ea403ef6-3b59-5ee8-9889-dab5cb0fb2ba/scratchpad/probe_${process.argv[2]}.json`, JSON.stringify(out));
  await b.close();
})();
