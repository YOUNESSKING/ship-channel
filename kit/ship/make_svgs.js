// Writes every ship as a standalone SVG (map paint in blue + realistic livery, side + top) into kit/ship/svg/.
// node kit/ship/make_svgs.js
const fs = require("fs"), path = require("path");
const K = require("./ships.js");
const out = path.join(__dirname, "svg"); fs.mkdirSync(out, { recursive: true });
for (const kind of K.list) for (const view of ["side", "top"]) {
  const w = 1200;
  fs.writeFileSync(path.join(out, `${kind}_${view}.svg`), K.svg(kind, view, { w, paint: "livery", glow: false, id: `${kind}${view}L` }) + "\n");
  fs.writeFileSync(path.join(out, `${kind}_${view}_blue.svg`), K.svg(kind, view, { w, col: "blue", glow: false, keyline: 2.4, id: `${kind}${view}B` }) + "\n");
}
console.log("wrote", fs.readdirSync(out).length, "SVGs to", out);
