// Typography / safe-area check for a built chapter (or any GSAP page with window.__timelines.main).
// NODE_PATH=$(npm root -g) node templates/check_safe_text.js work/c01/index.html [step=0.5] [--font Oswald]
// Seeks every `step` seconds and lists every VISIBLE text element (effective opacity > 0.1) that breaks a rule:
//   size  : rendered cap-height box < 3.5 % of frame height (font-size < 38 px at 1080p)
//   bottom: any part in the bottom 10 % of the frame (YouTube player bar / mobile scrubber)
//   corner: inside the top-right corner (right 20 %, top 12 %: YouTube card / info overlays)
//   font  : family is not the channel font (default Oswald)
// Exit code 1 when anything fails. Also prints window.__safeLog (what templates/lib/safe_area.js moved or enlarged).
const { chromium } = require("playwright"), fs = require("fs"), path = require("path");
(async () => {
  const args = process.argv.slice(2); const page = args[0]; const step = +(args.find((a, i) => i > 0 && /^[\d.]+$/.test(a)) || 0.5);
  const fi = args.indexOf("--font"), font = fi > 0 ? args[fi + 1] : "Oswald";
  const exe = ["/usr/bin/google-chrome", "/usr/bin/chromium"].find((p) => fs.existsSync(p));
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const gsapLocal = path.resolve(__dirname, "../map-kit/vendor/gsap.min.js");
  await p.route(/cdn\.jsdelivr\.net\/npm\/gsap/, (r) => r.fulfill({ path: gsapLocal, contentType: "application/javascript" }));
  await p.goto("file://" + path.resolve(page), { waitUntil: "load" });
  await p.waitForFunction(() => !!(window.__timelines && window.__timelines.main));
  await p.evaluate(async () => { await document.fonts.ready; await new Promise((r) => setTimeout(r, 300)); });
  const dur = await p.evaluate(() => window.__timelines.main.duration());
  const bad = new Map();
  for (let t = 0; t <= dur + 1e-6; t += step) {
    const res = await p.evaluate(({ t, font }) => {
      window.__timelines.main.seek(t, false);
      const root = document.getElementById("root") || document.body, rr = root.getBoundingClientRect(), H = rr.height, W = rr.width;
      const out = [];
      document.querySelectorAll(".clip").forEach((e) => { const a = +e.dataset.start, d = +e.dataset.duration; if (!isNaN(a) && !isNaN(d)) e.style.visibility = t >= a && t < a + d ? "visible" : "hidden"; });
      const els = Array.from(root.querySelectorAll("*")).filter((e) => !["SCRIPT", "STYLE"].includes(e.tagName) && Array.from(e.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim()));
      for (const e of els) {
        let op = 1, x = e, hidden = false;
        while (x && x !== document) { const cs = getComputedStyle(x); op *= +cs.opacity; if (cs.visibility === "hidden" || cs.display === "none") hidden = true; x = x.parentElement; }
        if (hidden || op < 0.1) continue;
        const box = e.getBoundingClientRect(); if (!box.width || !box.height) continue;
        const rg = document.createRange(); rg.selectNodeContents(e); const rt = rg.getBoundingClientRect();   // the TEXT's own box, not a wide container
        const r = rt.width && rt.height ? rt : box;
        const cs = getComputedStyle(e), fsz = parseFloat(cs.fontSize);
        // rendered size: font-size times the accumulated scale (box height / layout height)
        const scale = e.offsetHeight ? box.height / e.offsetHeight : (e.getBBox ? box.height / Math.max(1, e.getBBox().height) : 1);
        const px = fsz * scale * (1080 / H), txt = e.textContent.trim().replace(/\s+/g, " ").slice(0, 40);
        const top = (r.top - rr.top) / H, bot = (r.bottom - rr.top) / H, right = (r.right - rr.left) / W, left = (r.left - rr.left) / W;
        if (bot <= 0 || top >= 1 || right <= 0 || left >= 1) continue;
        const why = [];
        if (px < 37.5) why.push(`size ${px.toFixed(0)}px`);
        if (bot > 0.9) why.push(`bottom ${(bot * 100).toFixed(0)}%`);
        if (right > 0.8 && top < 0.12) why.push("top-right corner");
        if (font && !cs.fontFamily.includes(font)) why.push(`font ${cs.fontFamily.split(",")[0]}`);
        if (why.length) out.push(`${why.join(", ")} | "${txt}"`);
      }
      return out;
    }, { t, font });
    for (const r of res) { if (!bad.has(r)) bad.set(r, []); bad.get(r).push(t.toFixed(1)); }
  }
  const log = await p.evaluate(() => window.__safeLog || []);
  if (log.length) console.log("safe_area.js adjusted:\n  " + log.join("\n  "));
  if (!bad.size) console.log(`PASS: no text breaks the size / safe-area / font rules (${dur.toFixed(1)} s checked every ${step} s)`);
  else { console.log(`FAIL: ${bad.size} text problems`); for (const [k, ts] of bad) console.log(`  ${k}  @ ${ts.slice(0, 6).join(",")}${ts.length > 6 ? " ..." : ""}`); }
  await b.close(); process.exit(bad.size ? 1 : 0);
})();
