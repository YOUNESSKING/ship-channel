#!/usr/bin/env python3
"""SFX density of V02 (GOLD rule 100: ~16/min on average, in bursts; busy minutes 25-30, calm ~4).
Reads the built <work>/<chapter>/sfx_events.json files and prints SFX per minute of the whole video, by layer.
  python3 fixpass/sfx_density.py [WORK_DIR (default ../work)] [--extra-anim N]   (N = graphic sounds per animation scene not built yet)
Counted: every event except 'duck' (a music dip, not a sound) and 'env:*' beds (layer 1, always on). A 'ticks'/'ticks_up' train counts 1
per started 0.25 s (it is a burst of transients). Second table: PERCEIVED sounds - a run of the same cue less than 0.2 s apart
(a counter's tick train, two swooshes on one build) is one sound, a ticks train is one sound. Layers: things = el:* real recordings, mood = heart/boom/hit/vhit/riser/sig, graphics = the rest."""
import sys, os, json, math, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = 'ch00 ch01 ch02 ch03 ch04 ch05 ch06 ch07 ch08 ch09 ch10 ch11 ch12 final'.split()
MOOD = {'heart', 'heartbeat', 'boom', 'hit', 'vhit', 'riser', 'sig', 'deep_boom'}
def layer(c):
    if c.startswith('el:'):
        n = c[3:]
        if n.startswith('sig_'): return 'mood'
        if n in ('heartbeat', 'deep_boom', 'sub_boom'): return 'mood'
        return 'things'
    return 'mood' if c in MOOD else 'graphics'
def weight(e):
    if e['cue'] in ('ticks', 'ticks_up'): return max(1, math.ceil(float(e.get('dur') or 1) / .25))
    return 1
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('work', nargs='?', default=os.path.join(HERE, '..', 'work'))
    ap.add_argument('--extra-anim', type=float, default=0, help='spread N extra graphic sounds per minute evenly (animation scenes not built yet)')
    a = ap.parse_args(); t0 = 0.0; rows = []; envs = []
    for k in KEYS:
        p = os.path.join(a.work, k, 'sfx_events.json')
        if not os.path.exists(p): print('missing', p); continue
        ev = json.load(open(p))
        sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..', 'templates')); import mix_audio as MA
        for e in MA.thin(MA.dedupe(ev['events'])):
            if e['cue'] == 'duck': continue
            if e['cue'].startswith('env:'): envs.append((k, e['cue'], round(t0 + e['t'], 1), e.get('dur'))); continue
            rows.append((t0 + e['t'], layer(e['cue']), weight(e), e['cue']))
        t0 += ev['duration']
    nm = int(math.ceil(t0 / 60)); per = [{'things': 0, 'mood': 0, 'graphics': 0} for _ in range(nm)]
    for t, l, w, c in rows: per[min(nm - 1, int(t // 60))][l] += w
    rows.sort(key=lambda r: (r[3], r[0])); pc = [0] * nm; last = {}
    for t, l, w, c in rows:
        if c in last and t - last[c] < .2: last[c] = t; continue
        last[c] = t; pc[min(nm - 1, int(t // 60))] += 1
    print(f'video {t0/60:.2f} min, {len(envs)} environment beds')
    print('min  things mood graphics  total perceived' + ('  +anim' if a.extra_anim else ''))
    tot = 0
    for i, p in enumerate(per):
        s = sum(p.values()); tot += s
        bar = '#' * int(s + a.extra_anim)
        print(f'{i:>3}  {p["things"]:>6} {p["mood"]:>4} {p["graphics"]:>8}  {s:>5} {pc[i]:>9}' + (f'  {s + a.extra_anim:>5.0f}' if a.extra_anim else '') + f'  {bar}')
    print(f'perceived average {sum(pc) / (t0 / 60):.1f} sounds/min' + (f' (+anim {sum(pc) / (t0 / 60) + a.extra_anim * .6:.1f}, assuming 60 % of the anim sounds are separate)' if a.extra_anim else ''))
    print(f'average {tot / (t0 / 60):.1f} SFX/min' + (f' (+anim {tot / (t0 / 60) + a.extra_anim:.1f})' if a.extra_anim else ''))
    gaps = [k for k in KEYS if not any(x[0] == k for x in envs)]
    if gaps: print('chapters without an environment bed:', ' '.join(gaps))
if __name__ == '__main__': main()
