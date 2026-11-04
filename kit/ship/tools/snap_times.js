// Seek a GSAP / HyperFrames page (window.__timelines.main) to given times and screenshot each one (fast previews, no full render).
// NODE_PATH=$(npm root -g) node kit/ship/tools/snap_times.js PAGE.html[?query] OUT_PREFIX t1,t2,... [width=1920 height=1080]
// Writes OUT_PREFIX_<t>.jpg and prints window.__sink (facts, landT ...) if the page has it. CDN gsap is served from map-kit/vendor.
const { chromium } = require("playwright"), fs = require("fs"), path = require("path");
(async () => {
  const [pg, pre, times, w = "1920", h = "1080"] = process.argv.slice(2);
  const [file, query] = pg.split("?");
  const exe = ["/usr/bin/google-chrome", "/usr/bin/chromium"].find((p) => fs.existsSync(p));
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const p = await b.newPage({ viewport: { width: +w, height: +h } });
  const gsapLocal = path.resolve(__dirname, "../../../map-kit/vendor/gsap.min.js");
  await p.route(/cdn\.jsdelivr\.net\/npm\/gsap/, (r) => r.fulfill({ path: gsapLocal, contentType: "application/javascript" }));
  await p.goto("file://" + path.resolve(file) + (query ? "?" + query : ""), { waitUntil: "load" });
  await p.waitForFunction(() => !!(window.__timelines && window.__timelines.main));
  await p.evaluate(async () => { await document.fonts.ready; });
  const info = await p.evaluate(() => ({ dur: window.__timelines.main.duration(), sink: window.__sink || null }));
  for (const t of times.split(",").map(Number)) {
    await p.evaluate(async (tt) => {
      window.__timelines.main.seek(tt, false);
      document.querySelectorAll("video").forEach((v) => { const a = +(v.dataset.start || 0), ms = +(v.dataset.mediaStart || 0); try { v.currentTime = Math.max(0, tt - a + ms); } catch (e) {} });
      await new Promise((r) => setTimeout(r, 120));
    }, t);
    // HyperFrames shows a .clip only inside [data-start, data-start + data-duration]
    await p.evaluate((tt) => { document.querySelectorAll(".clip").forEach((e) => { const a = +e.dataset.start, d = +e.dataset.duration; if (!isNaN(a) && !isNaN(d)) e.style.visibility = tt >= a && tt < a + d ? "visible" : "hidden"; }); }, t);
    await p.screenshot({ path: `${pre}_${t.toFixed(2)}.jpg`, type: "jpeg", quality: 88 });
  }
  console.log(JSON.stringify({ duration: info.dur, sink: info.sink && { landT: info.sink.landT, tUnder: info.sink.tUnder, facts: info.sink.facts } }));
  await b.close();
})();
