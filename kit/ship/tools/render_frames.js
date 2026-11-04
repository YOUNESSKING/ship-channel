// Render a GSAP / HyperFrames-style page frame by frame (seek -> screenshot) into an MP4 with ffmpeg (no audio).
// NODE_PATH=$(npm root -g) node kit/ship/tools/render_frames.js PAGE.html[?query] OUT.mp4 [fps=30]
// Writes OUT.cues.json (window.__sink.cues if the page has them) next to the video. Frames are piped, nothing big on disk.
const { chromium } = require("playwright"), { spawn } = require("child_process"), fs = require("fs"), path = require("path");
(async () => {
  const [pg, out, fpsA] = process.argv.slice(2); const fps = +(fpsA || 30);
  const [file, query] = pg.split("?");
  const exe = ["/usr/bin/google-chrome", "/usr/bin/chromium"].find((p) => fs.existsSync(p));
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto("file://" + path.resolve(file) + (query ? "?" + query : ""), { waitUntil: "commit" });
  await p.waitForFunction(() => !!(window.__timelines && window.__timelines.main));
  await p.evaluate(async () => { await document.fonts.ready; });
  const info = await p.evaluate(() => ({ dur: window.__timelines.main.duration(), sink: window.__sink || null }));
  const n = Math.round(info.dur * fps);
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", out], { stdio: ["pipe", "inherit", "inherit"] });
  for (let i = 0; i < n; i++) {
    await p.evaluate((t) => { window.__timelines.main.seek(t, false); }, i / fps);   // braces: never return the timeline (playwright would try to serialise it and hang)
    const buf = await p.screenshot({ type: "jpeg", quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    if (i % 30 === 0) process.stdout.write(`frame ${i}/${n}\r`);
  }
  ff.stdin.end(); await new Promise((r) => ff.on("close", r));
  if (info.sink) fs.writeFileSync(out.replace(/\.mp4$/, ".cues.json"), JSON.stringify(info.sink, null, 1));
  await b.close(); console.log(`\nwrote ${out} (${n} frames, ${info.dur.toFixed(2)} s)`);
})();
