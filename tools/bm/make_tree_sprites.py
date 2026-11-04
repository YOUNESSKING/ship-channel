"""TREE REDESIGN TEST (owner 2026-10-31, research/TREE_REDESIGN_BRIEF.md): build libraries of REAL aerial tree crowns
from public-domain USGS orthoimagery (The National Map, NAIP Plus / HRO; see assets/src/trees/SOURCES.md).
usage (from cleburne/): python3 tools/make_tree_sprites.py [A|C|all]
  A : isolated trees cut out of an open golf-course landscape (East Potomac Park, DC): full natural outlines.
      tree = darker-than-grass & green (G>B); the source's own cast shadow (blue-dark, B>G) is dropped; clumps are split
      with a distance-transform watershed.
  C : texture synthesis: generated irregular crown outlines filled with windows of a real CLOSED forest canopy photo
      (Rock Creek Park, DC) at native scale, centred on sunlit crown tops -> real leaf detail at 1:1, controlled shapes.
Every sprite is rotated 180 deg (source sun from the S/SE -> our map light from the NW), stored as RGBA (straight alpha),
in source colours; regrading to the map palette happens in ref_look_v10*.py.  Output: assets/src/trees/sprites_{A,C}.npz"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from skimage.morphology import convex_hull_image

SRC = "assets/src/trees"
G = ndimage.gaussian_filter


def cut(img, lab, ids, min_a, max_a, pad=5, min_solid=0.72, ok=None):
    out = []
    objs = ndimage.find_objects(lab)
    for i in ids:
        sl = objs[i - 1]
        if sl is None: continue
        m = lab[sl] == i
        a = m.sum()
        if a < min_a or a > max_a: continue
        if sl[0].start == 0 or sl[1].start == 0 or sl[0].stop == lab.shape[0] or sl[1].stop == lab.shape[1]: continue   # cut by the tile edge
        if a / convex_hull_image(m).sum() < min_solid: continue          # compact crowns only (no merged clumps)
        hh_, ww_ = m.shape
        if max(hh_, ww_) / max(min(hh_, ww_), 1) > 1.45: continue        # no elongated hedges
        edge = max(m[:3].mean(1).max(), m[-3:].mean(1).max(), m[:, :3].mean(0).max(), m[:, -3:].mean(0).max())
        if edge > 0.6: continue                                          # a straight cut side (mosaic seam / clump split)
        y0, y1 = max(sl[0].start - pad, 0), min(sl[0].stop + pad, lab.shape[0])
        x0, x1 = max(sl[1].start - pad, 0), min(sl[1].stop + pad, lab.shape[1])
        mm = (lab[y0:y1, x0:x1] == i)
        mm = ndimage.binary_fill_holes(ndimage.binary_opening(mm, iterations=1))
        mm = G(mm.astype(np.float32), 2.6) > 0.5                          # round off pixel-jagged watershed cuts
        al = np.clip(G(mm.astype(np.float32), 0.8) * 1.6 - 0.3, 0, 1)       # soft, slightly ragged leaf edge
        rgb = img[y0:y1, x0:x1].astype(np.float32)
        if ok is not None and not ok(rgb[mm]): continue
        spr = np.dstack([rgb, al * 255])[::-1, ::-1]                       # 180 deg: light now from the NW
        out.append(spr.astype(np.uint8))
    return out


def build_A():
    sprs = []
    for k in range(10):
        im = Image.open(f"{SRC}/hro_dc_epp_{k}.png").convert("RGB")
        im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)      # 0.24 m/px ~ native HRO
        a = np.array(im).astype(np.float32)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        L = G(a.mean(-1), 0.8)
        tex = np.sqrt(np.clip(G(a.mean(-1) ** 2, 2.0) - G(a.mean(-1), 2.0) ** 2, 0, None))   # leaf texture vs smooth grass
        tree = (L < 92) & (G(g - b, 1.0) > 2) & (G(g - r, 1.0) > -4) & (G(tex, 1.5) > 5.0)
        tree = ndimage.binary_closing(ndimage.binary_opening(tree, iterations=1), iterations=2)
        tree = ndimage.binary_fill_holes(tree)
        dist = ndimage.distance_transform_edt(tree)
        pk = peak_local_max(G(dist, 1.5), min_distance=16, threshold_abs=8, labels=ndimage.label(tree)[0])
        mk = np.zeros(tree.shape, np.int32); mk[tuple(pk.T)] = np.arange(1, len(pk) + 1)
        lab = watershed(-G(dist, 1.5), mk, mask=tree)
        def okA(p):                                                         # dark, textured, green: a crown, not grass
            Lp = p.mean(1)
            return Lp.mean() < 82 and Lp.std() > 9 and (p[:, 1] > p[:, 2]).mean() > 0.9 and (p[:, 2] > p[:, 1] + 3).mean() < 0.03
        sprs += cut(a, lab, range(1, lab.max() + 1), 600, 5000, min_solid=0.82, ok=okA)
    return sprs


def build_C(n=160, seed=5):
    """Angle C: texture synthesis. Each crown OUTLINE is generated (one irregular, noise-warped leafy outline, not
    spheres); its FILL is a window of a real closed forest canopy photo at native scale (0.3 m/px ~ 1:1 on the map),
    centred on a sunlit crown top, so every tree shows real leaf clusters."""
    rng = np.random.default_rng(seed)
    im = Image.open(f"{SRC}/hro_dc_rockcreek.png").convert("RGB")
    a = np.array(im).astype(np.float32)[:1250, :1250]                       # drop the houses/road in the SE corner
    Ls = G(a.mean(-1), 2.2)
    pk = peak_local_max(Ls, min_distance=9, threshold_abs=np.percentile(Ls, 55), exclude_border=30)
    fol = (a[..., 1] >= a[..., 0]) & (a[..., 1] >= a[..., 2] - 2) & (a.max(-1) < 175)
    out = []
    for _ in range(n * 4):
        if len(out) >= n: break
        cy, cx = pk[rng.integers(len(pk))]
        R = rng.uniform(14, 19); s = int(R * 1.35) + 3
        win = a[cy - s:cy + s + 1, cx - s:cx + s + 1]
        if win.shape[:2] != (2 * s + 1, 2 * s + 1) or fol[cy - s:cy + s + 1, cx - s:cx + s + 1].mean() < 0.95: continue
        yy, xx = np.mgrid[-s:s + 1, -s:s + 1].astype(np.float32)
        th = np.arctan2(yy, xx); rr = np.hypot(xx, yy)
        rad = R * (1 + rng.uniform(-0.10, 0.10) * np.cos(2 * th + rng.uniform(0, 6.3)))   # slightly oval
        for k, amp in ((3, 0.07), (5, 0.06), (8, 0.05), (13, 0.04), (21, 0.03)):      # irregular lobed outline (one shape)
            rad = rad * (1 + amp * rng.uniform(0.4, 1.0) * np.cos(k * th + rng.uniform(0, 6.3)))
        al = np.clip((rad - rr) / 1.6 + 0.5, 0, 1)
        out.append(np.dstack([win, al * 255])[::-1, ::-1].astype(np.uint8))
    return out


def build_C2(n=260, seed=11):
    """v11 (judge fixes): like C, but from THREE forest canopy photos (each normalised to the same exposure, so no
    crown-to-crown tone swings), with more varied outlines (oval, lobed, slightly lopsided) and sizes."""
    rng = np.random.default_rng(seed)
    srcs = [("hro_dc_rockcreek.png", (0, 1250, 0, 1250)), ("hro_dc_glover.png", (0, 1200, 0, 880)),
            ("hro_dc_rockcreek2.png", (380, 1200, 0, 1200))]
    ref = None; pools = []
    for fn, (y0, y1, x0, x1) in srcs:
        a = np.array(Image.open(f"{SRC}/{fn}").convert("RGB")).astype(np.float32)[y0:y1, x0:x1]
        fol = (a[..., 1] >= a[..., 0]) & (a[..., 1] >= a[..., 2] - 2) & (a.max(-1) < 175)
        mu, sd = a[fol].mean(0), a[fol].std(0)
        if ref is None: ref = (mu, sd)
        a = (a - mu) / sd * ref[1] + ref[0]                                  # same exposure for every source
        Ls = G(a.mean(-1), 2.2)
        pk = peak_local_max(Ls, min_distance=9, threshold_abs=np.percentile(Ls, 55), exclude_border=30)
        pools.append((a, fol, pk))
    out = []
    for _ in range(n * 6):
        if len(out) >= n: break
        a, fol, pk = pools[rng.integers(len(pools))]
        cy, cx = pk[rng.integers(len(pk))]
        R = rng.uniform(13, 21); s = int(R * 1.45) + 3
        win = a[cy - s:cy + s + 1, cx - s:cx + s + 1]
        if win.shape[:2] != (2 * s + 1, 2 * s + 1) or fol[cy - s:cy + s + 1, cx - s:cx + s + 1].mean() < 0.95: continue
        yy, xx = np.mgrid[-s:s + 1, -s:s + 1].astype(np.float32)
        th = np.arctan2(yy, xx); rr = np.hypot(xx, yy)
        rad = R * (1 + rng.uniform(-0.18, 0.18) * np.cos(2 * th + rng.uniform(0, 6.3)))   # oval
        rad = rad * (1 + rng.uniform(0, 0.12) * np.cos(th + rng.uniform(0, 6.3)))          # lopsided
        for k, amp in ((3, 0.10), (4, 0.07), (6, 0.06), (9, 0.05), (14, 0.04), (22, 0.03)):
            rad = rad * (1 + amp * rng.uniform(0.2, 1.0) * np.cos(k * th + rng.uniform(0, 6.3)))
        al = np.clip((rad - rr) / 1.6 + 0.5, 0, 1)
        out.append(np.dstack([np.clip(win, 0, 255), al * 255])[::-1, ::-1].astype(np.uint8))
    return out


def save(name, sprs):
    np.savez_compressed(f"{SRC}/sprites_{name}.npz", **{f"s{i:04d}": s for i, s in enumerate(sprs)})
    # contact sheet for eyeballing
    n = min(len(sprs), 120); cs = 96; cols = 12
    sheet = Image.new("RGB", (cols * cs, ((n + cols - 1) // cols) * cs), (190, 178, 134))
    for i, s in enumerate(sprs[:n]):
        im = Image.fromarray(s, "RGBA"); im.thumbnail((cs - 4, cs - 4))
        sheet.paste(im, ((i % cols) * cs + 2, (i // cols) * cs + 2), im)
    sheet.save(f"{SRC}/sprites_{name}_sheet.jpg", quality=90)
    print(name, len(sprs), "sprites")


if __name__ == "__main__":
    w = sys.argv[1] if len(sys.argv) > 1 else "all"
    if w in ("A", "all"): save("A", build_A())
    if w in ("C", "all"): save("C", build_C())
    if w in ("C2", "all"): save("C2", build_C2())
