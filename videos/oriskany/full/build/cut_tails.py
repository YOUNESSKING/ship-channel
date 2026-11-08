"""SFX_FIX_v5 spot-check: what sounds in the 0.5 s after a picture cut (owner 2026-11-08: "they stay after the scene is over").

For each cut it reports
  carry      = the cues whose event lies in an EARLIER shot and whose audible tail (> -50 dBFS, measured on the levelled,
               faded segment by sfx_mix_lib.render -> "audible_end") passes the cut, with how far (s);
  stem_db    = RMS / peak dBFS of the effect stems (sfx + punch + beds, before the mix) in [cut, cut + 0.5];
  bus_db     = the same on the mix buses (sfx_bus + punch_bus + beds_bus: ducked + filtered, before mastering);
  new        = the cues that START inside the window (the new shot's own sounds: they are allowed).
usage: python3 build/cut_tails.py PLACED.json STEMS_DIR MIX_DIR OUT.json [cut ...]   (no cuts = every cut)"""
import bisect, json, os, sys
import numpy as np, soundfile as sf

SR, WIN = 48000, 0.5


def window(paths, t0, t1):
    acc = None
    for p in paths:
        if not os.path.exists(p): continue
        with sf.SoundFile(p) as f:
            f.seek(int(t0 * f.samplerate)); a = f.read(int((t1 - t0) * f.samplerate), dtype="float64", always_2d=True)
        acc = a if acc is None else acc[: len(a)] + a[: len(acc)]
    if acc is None or not len(acc): return None, None
    m = acc.mean(axis=1)
    rms = float(np.sqrt((m ** 2).mean())); pk = float(np.abs(acc).max())
    return round(20 * np.log10(rms + 1e-12), 1), round(20 * np.log10(pk + 1e-12), 1)


def main():
    placed_p, stems, mix, out = sys.argv[1:5]
    P = json.load(open(placed_p)); shots = P["shots"]; starts = [s[1] for s in shots]
    cuts = [float(x) for x in sys.argv[5:]] or [s[1] for s in shots[1:]]
    shot_of = lambda t: shots[bisect.bisect_right(starts, t + 1e-6) - 1]
    rows = []
    for c in cuts:
        carry = []
        for p in P["cues"]:
            sh = shot_of(p["event"])
            if sh[2] <= c + 1e-3 and p.get("audible_end", p["end"]) > c + 1e-3:
                carry.append(dict(role=p["role"], event=p["event"], shot=sh[0], past_cut=round(p.get("audible_end", p["end"]) - c, 3), note=p["note"][:60]))
        new = [f"{p['role']}@{p['event']:.2f}" for p in P["cues"] if c - 1e-3 <= p["start"] < c + WIN]
        beds = [f"{b['role']} {b['start']:.2f}-{b['end']:.2f}" for b in P.get("beds", []) if b["start"] < c + WIN and b["end"] > c - 1e-3]
        s_rms, s_pk = window([os.path.join(stems, f) for f in ("sfx.wav", "punch.wav", "beds.wav")], c, c + WIN)
        b_rms, b_pk = window([os.path.join(mix, f) for f in ("sfx_bus.wav", "punch_bus.wav", "beds_bus.wav")], c, c + WIN)
        p_rms, _ = window([os.path.join(stems, f) for f in ("sfx.wav", "punch.wav", "beds.wav")], c - WIN, c)
        rows.append(dict(cut=round(c, 3), carry=carry, new=new, beds=beds, stem_rms=s_rms, stem_peak=s_pk, bus_rms=b_rms, bus_peak=b_pk,
                         stem_rms_before=p_rms))
    json.dump(rows, open(out, "w"), indent=1)
    for r in rows:
        print(f"{r['cut']:8.3f} carry {len(r['carry'])} max {max([x['past_cut'] for x in r['carry']] or [0]):.2f} s | stem rms {r['stem_rms']} pk {r['stem_peak']} "
              f"| bus rms {r['bus_rms']} | before {r['stem_rms_before']} | new {r['new']}")


if __name__ == "__main__":
    main()
