// Render one scene of scenes.html frame by frame (seek -> screenshot -> ffmpeg), like kit/ship/tools/render_frames.js.
//   NODE_PATH=$(npm root -g) node render_anim.js "scenes.html?scene=NAME" OUT.mp4 BEATS.json
//   NODE_PATH=$(npm root -g) node render_anim.js "scenes.html?scene=NAME" OUT_PREFIX - 0.5,1.2,3   (stills only)
// BEATS.json = window.__anim ({beats, cues, missing, duration}) exported by the page.
const { chromium } = require("playwright"), { spawn } = require("child_process"), fs = require("fs"), path = require("path");
(async () => {
  const [pg, out, beatsOut, times] = process.argv.slice(2); const fps = 30;
  const [file, query] = pg.split("?");
  const exe = ["/usr/bin/google-chrome", "/usr/bin/chromium"].find((p) => fs.existsSync(p));
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on("pageerror", (e) => errs.push(String(e))); p.on("console", (m) => { if (m.type() === "error") errs.push(m.text()); });
  await p.goto("file://" + path.resolve(file) + (query ? "?" + query : ""), { waitUntil: "load" });
  await p.waitForFunction(() => !!(window.__timelines && window.__timelines.main) || !!window.__animError, null, { timeout: 30000 });
  const fail = await p.evaluate(() => window.__animError || null);
  if (fail) { console.error("scene error:", fail, errs.join("\n")); process.exit(2); }
  await p.evaluate(async () => { await document.fonts.ready; });
  const info = await p.evaluate(() => ({ dur: window.__timelines.main.duration(), anim: window.__anim || null }));
  if (errs.length) console.error("page errors:\n" + errs.join("\n"));
  if (beatsOut === "-") {
    for (const t of times.split(",").map(Number)) {
      await p.evaluate((tt) => { window.__timelines.main.seek(tt, false); }, t);
      await p.screenshot({ path: `${out}_${t.toFixed(2)}.jpg`, type: "jpeg", quality: 88 });
    }
    console.log(JSON.stringify(info.anim && { beats: info.anim.beats, missing: info.anim.missing }));
    await b.close(); return;
  }
  const n = Math.round(info.dur * fps);
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-crf", "16", "-preset", "medium", "-r", String(fps), out], { stdio: ["pipe", "inherit", "inherit"] });
  for (let i = 0; i < n; i++) {
    await p.evaluate((t) => { window.__timelines.main.seek(t, false); }, i / fps);
    const buf = await p.screenshot({ type: "jpeg", quality: 93 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
  }
  ff.stdin.end(); const code = await new Promise((r) => ff.on("close", r));
  if (code !== 0) { console.error("ffmpeg failed"); process.exit(3); }
  fs.writeFileSync(beatsOut, JSON.stringify(Object.assign({ duration: info.dur }, info.anim || {}), null, 1));
  await b.close(); console.log(`wrote ${out} (${n} frames)`);
})().catch((e) => { console.error(e); process.exit(1); });
