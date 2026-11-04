#!/usr/bin/env python3
"""Oriskany full video, step 2B: every kit / hero ANIMATION scene (33 hero segments + 3 Wikimedia-photo fallbacks).

  python3 build/make_anims.py cfg              -> hero/scenes_cfg.js (scene list, durations, scene-relative word times)
  python3 build/make_anims.py render [names]   -> segments/h_*.mp4 (resumable: skips a scene whose mp4 is newer than the
                                                  scene sources; FORCE=1 re-renders), writes build/anim_beats.json
  python3 build/make_anims.py snaps NAME t,t   -> hero/snaps/NAME_t.jpg quick stills
  python3 build/make_anims.py sheet            -> hero/ANIMS_SHEET.jpg (one frame per scene at its main beat)
  python3 build/make_anims.py all              -> cfg + render + beats + sheet (run detached: nohup ... &)

Scenes are drawn by hero/scenes.js (families: board/ledger/tally/rounds/pcb chart/snapper/deck cutaway/apart/ShipSink/
reef cross-section) in the approved test v4 look (kit ShipSink + CarrierHero, Oswald, cream + gold, labels >= 38 px,
nothing in the bottom 10 % or the top-right corner). Every beat (hit / landing / impact) is exported by the page and
written to build/anim_beats.json with its frame, chapter-local and absolute time, so sound cues can be re-timed.
Charts use only FACTCHECK_B numbers (screening values 50 / 20 ppb, ~2.9 and ~3.5-3.9 years; snapper ~7x attributed).
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.dirname(HERE)
HERO = os.path.join(FULL, 'hero')
SEG = os.path.join(FULL, 'segments')
FPS = 30
PAD = 0.4            # rendered past the shot end (the chapter conform trims; never freeze the last frame)

# scene -> (family, stage).  Fallbacks: rendered as h_*.mp4 only; the step-3 builder swaps them in for the p_ file if the
# owner's Wikimedia download is missing (see anim_beats.json "replaces").
FAMILY = {
    'c02_sisters': ('sisters', None), 'c02_ledger_a': ('ledger', 'a'), 'c02_ledger_b': ('ledger', 'b'),
    'c02_tally': ('tally', 'c02'), 'c07_tally': ('tally', 'c07'),
    'c04_deck_a': ('deck', 'a'), 'c04_deck_a2': ('deck', 'a2'), 'c04_deck_b': ('deck', 'b'), 'c04_deck_c': ('deck', 'c'),
    'c05_hero_a': ('sink', 'a'), 'c05_hero_b': ('sink', 'b'),
    'c06_rounds_a': ('rounds', 'a'), 'c06_rounds_b': ('rounds', 'b'),
    'c06_snapper_a': ('snapper', 'a'), 'c06_snapper_b': ('snapper', 'b'),
    'c07_apart': ('apart', None),
}
for st in ('lines_a', 'lines_b', 'lines_c', 'lines_d', 'lines_e', 'species_a', 'species_b', 'down_a', 'down_b', 'down_c', 'down_d'):
    FAMILY['c06_' + st] = ('pcb', st)
for st in ('settle', 'funnel', 'depths_a', 'depths_b', 'depths_d', 'today', 'depths_c', 'divers', 'wreck2008'):
    FAMILY['c07_' + st] = ('reef', st)

# fallbacks for the three owner-download Wikimedia photos in c07 (RENDER_PLAN "Owner downloads")
FALLBACKS = [
    dict(scene='c07_wreck2008', file='h_c07_wreck2008.mp4', replaces='p_c07_s02.mp4', shot='s02', chapter='c07',
         shows='Fallback for the Wikimedia wreck photo: kit hulk on the seabed, marine growth spreads 2006 -> JULY 2008, fish gather, light shafts'),
    dict(scene='c07_depths_c', file='h_c07_depths_c.mp4', replaces='p_c07_s09.mp4', shot='s09', chapter='c07',
         shows="Fallback for Greg Grimes' island photo: cross-section close on the island, label 'ISLAND TOP 84 FT' lands on 'eighty'"),
    dict(scene='c07_divers', file='h_c07_divers.mp4', replaces='p_c07_s12.mp4', shot='s12', chapter='c07',
         shows='Fallback for the Wikimedia divers photo: diver icons descend to the island top, bubbles rise'),
]


def load(p): return json.load(open(os.path.join(FULL, p)))


def scenes():
    words = load('build/words.json')
    segs = load('build/segments.json')
    chap = {c['key']: c for c in (load(f'chapter/c0{i}.json') for i in range(1, 8))}
    out = []
    for s in segs:
        if s['kind'] != 'hero': continue
        out.append(dict(scene=s['scene'], file=s['file'], chapter=s['chapter'], shot=s['shot'], dur=s['dur'],
                        t0_abs=s['t0_abs'], narration=s['narration'], shows=s['shows'], replaces=None))
    for fb in FALLBACKS:
        c = chap[fb['chapter']]
        sh = next(x for x in c['shots'] if x['id'] == fb['shot'])
        i = c['shots'].index(sh)
        a = float(sh['start'][1:]); b = float(c['shots'][i + 1]['start'][1:])
        t0 = c['audio_offset'] + a
        nar = ' '.join(w['w'] for w in words if t0 - 0.05 <= w['start'] < t0 + (b - a))
        out.append(dict(scene=fb['scene'], file=fb['file'], chapter=fb['chapter'], shot=fb['shot'], dur=round(b - a, 3),
                        t0_abs=round(t0, 3), narration=nar, shows=fb['shows'], replaces=fb['replaces']))
    for s in out:
        s['family'], s['stage'] = FAMILY[s['scene']]
        s['render_dur'] = round(s['dur'] + PAD, 3)
        s['chapter_t0'] = round(s['t0_abs'] - chap[s['chapter']]['audio_offset'], 3)
        s['words'] = [dict(w=w['w'], t=round(w['start'] - s['t0_abs'], 3), e=round(w['end'] - s['t0_abs'], 3))
                      for w in words if s['t0_abs'] - 0.3 <= w['start'] < s['t0_abs'] + s['render_dur'] + 0.3]
    return out


def write_cfg():
    sc = scenes()
    cfg = {s['scene']: dict(dur=s['render_dur'], shot_dur=s['dur'], family=s['family'], stage=s['stage'], words=s['words'])
           for s in sc}
    with open(os.path.join(HERO, 'scenes_cfg.js'), 'w') as f:
        f.write('// generated by build/make_anims.py cfg: scene -> render duration, family, stage, scene-relative word times\n')
        f.write('window.SCENES = ' + json.dumps(cfg, indent=0) + ';\n')
    print(f'wrote hero/scenes_cfg.js ({len(cfg)} scenes)')
    return sc


SRC = ['scenes.js', 'scenes.html', 'scenes_cfg.js', 'sinking.js', 'carrier_hero.js', 'ships.js']


def stale(path):
    if os.environ.get('FORCE') == '1' or not os.path.exists(path): return True
    m = os.path.getmtime(path)
    return any(os.path.getmtime(os.path.join(HERO, f)) > m for f in SRC)


def node(args):
    env = dict(os.environ, NODE_PATH=subprocess.check_output(['npm', 'root', '-g']).decode().strip())
    return subprocess.run(['node'] + args, env=env, check=True, capture_output=True, text=True).stdout


def render(names=None):
    sc = write_cfg()
    os.makedirs(SEG, exist_ok=True)
    bdir = os.path.join(HERO, 'beats'); os.makedirs(bdir, exist_ok=True)
    for s in sc:
        if names and s['scene'] not in names: continue
        out = os.path.join(SEG, s['file']); bj = os.path.join(bdir, s['scene'] + '.json')
        if not stale(out) and os.path.exists(bj):
            print('skip (up to date)', s['file']); continue
        t = time.time()
        tmp = out[:-4] + '.part.mp4'
        node([os.path.join(HERO, 'render_anim.js'), os.path.join(HERO, 'scenes.html') + '?scene=' + s['scene'], tmp, bj])
        os.replace(tmp, out)
        print(f'rendered {s["file"]} ({s["render_dur"]:.2f} s) in {time.time() - t:.0f} s', flush=True)
    beats(sc)


def beats(sc=None):
    sc = sc or scenes()
    res = {'_about': 'Animation beat frames for sound re-timing. t = seconds into the clip (= into the shot, the clip starts at the shot '
                     'start, no trim); frame = round(t*30); chapter_t = shot start + t (chapter-local, as sfx_cNN.json "at" in shot '
                     'seconds = t); abs_t = narration time. "main" = the beat the sfx list calls "its main graphic beat".',
           'fps': FPS, 'scenes': {}}
    for s in sc:
        bj = os.path.join(HERO, 'beats', s['scene'] + '.json')
        if not os.path.exists(bj): continue
        b = json.load(open(bj))
        bl = []
        for x in b.get('beats', []):
            bl.append(dict(t=x['t'], frame=round(x['t'] * FPS), chapter_t=round(s['chapter_t0'] + x['t'], 3),
                           abs_t=round(s['t0_abs'] + x['t'], 3), kind=x['kind'], note=x['note'], main=bool(x.get('main'))))
        res['scenes'][s['scene']] = dict(file=s['file'], chapter=s['chapter'], shot=s['shot'], shot_dur=s['dur'],
                                         clip_dur=s['render_dur'], chapter_t0=s['chapter_t0'], abs_t0=s['t0_abs'],
                                         replaces=s['replaces'], narration=s['narration'], beats=bl,
                                         missing_words=b.get('missing', []), sound_hint=b.get('cues', []))
    try: res['templates'] = template_beats()
    except Exception as e: res['templates'] = {'_error': repr(e)}
    with open(os.path.join(HERE, 'anim_beats.json'), 'w') as f: json.dump(res, f, indent=1)
    print('wrote build/anim_beats.json', len(res['scenes']), 'scenes')


def template_beats():
    """Beats of the template animation blocks (anim_gauge / anim_options / anim_xray / number_clip counts), resolved with the
    chapter builder's own time specs (templates/build_chapter.py Ctx.t), chapter-local seconds. Rendered inside the chapter."""
    sys.path.insert(0, os.path.join(FULL, '..', '..', '..', 'templates'))
    import build_chapter as bc
    out = {}
    for i in range(1, 8):
        cp = os.path.join(FULL, 'chapter', f'c0{i}.json'); B = bc.Builder(cp, media=False); ch = B.chapter; shots = ch['shots']
        starts = []
        for k, s in enumerate(shots):
            st = s.get('start', 0.0)
            starts.append(float(st) if isinstance(st, (int, float)) else bc.Ctx(B, s, starts[-1] if starts else 0.0, 0.0).t(st))
        ends = starts[1:] + [float(ch['duration'])]
        rows = []
        for s, a, b in zip(shots, starts, ends):
            tp, v, p = s['template'], s.get('variant'), s.get('params', {})
            C = bc.Ctx(B, s, a, b); T = lambda spec, rel=None: round(C.t(spec, rel), 3)
            ev = []
            try:
                if tp == 'anim_gauge':
                    if v == 'meter': ev.append(('land', T(p.get('count_at'), 1.6) + float(p.get('dur', 1.4)), f"meter lands {p.get('value')} {p.get('unit', '')}"))
                    else:
                        its = p.get('items', []); h = next((k for k, it in enumerate(its) if it.get('hero')), len(its) - 1)
                        for k, it in enumerate(its):
                            at = C.t(it.get('at'), .7 + k * 1.6)
                            cat = C.t(it.get('count_at'), (at - a) + (.9 if k == h else .6)); d = float(it.get('dur', 1.4 if k == h else .7))
                            ev.append(('land' if k == h else 'pop', round(cat + d, 3), f"bar {it.get('label')} = {it.get('value')}" + (' (hero)' if k == h else '')))
                elif tp == 'anim_options':
                    for it in p.get('items', []):
                        if it.get('at') is not None: ev.append(('pop', T(it['at']), f"option {it['text']}"))
                        if it.get('strike_at') is not None: ev.append(('scrape', T(it['strike_at']), f"strike {it['text']}"))
                        if it.get('chosen'): ev.append(('land', T(it['at']), f"chosen {it['text']} (gold box after the last strike)"))
                elif tp == 'anim_xray':
                    if p.get('organ_at') is not None: ev.append(('pop', T(p['organ_at']), f"organ glows {p.get('organ_label', '')}"))
                    for r in p.get('readouts', []): ev.append(('pop', T(r.get('at')), f"readout {r.get('text')}"))
                elif tp == 'number_clip':
                    c = p.get('count')
                    if c and c.get('land_at') is not None: ev.append(('land', T(c['land_at']), f"count lands {p.get('number')}"))
                    elif v == 'strike_swap': ev.append(('scrape', T(p.get('strike_at'), 2.2), f"strike {p.get('old')} -> {p.get('new')}"))
                    elif p.get('number_at') is not None: ev.append(('land', T(p['number_at']), f"number {p.get('number')}"))
                else: continue
            except Exception as e: ev.append(('error', a, repr(e)))
            if ev: rows.append(dict(shot=s['id'], template=tp, variant=v, start=round(a, 3),
                                    beats=[dict(kind=k, chapter_t=round(t, 3), t=round(t - a, 3), frame=round((t - a) * FPS), note=n) for k, t, n in ev]))
        out[f'c0{i}'] = rows
    return out


def snaps(name, times):
    write_cfg()
    d = os.path.join(HERO, 'snaps'); os.makedirs(d, exist_ok=True)
    print(node([os.path.join(HERO, 'render_anim.js'), os.path.join(HERO, 'scenes.html') + '?scene=' + name,
                os.path.join(d, name), '-', times]))


def sheet():
    from PIL import Image, ImageDraw, ImageFont
    sc = scenes(); ab = json.load(open(os.path.join(HERE, 'anim_beats.json')))['scenes']
    tw, th, cols = 480, 270, 6
    items = [s for s in sc if s['scene'] in ab and os.path.exists(os.path.join(SEG, s['file']))]
    rows = (len(items) + cols - 1) // cols
    img = Image.new('RGB', (cols * tw, rows * (th + 34)), (10, 12, 14))
    fp = os.path.join(HERO, 'fonts', 'oswald.ttf')
    try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    except Exception: font = ImageFont.load_default()
    tmpd = os.path.join(HERO, 'snaps'); os.makedirs(tmpd, exist_ok=True)
    for i, s in enumerate(items):
        b = ab[s['scene']]['beats']; m = next((x for x in b if x['main']), b[-1] if b else None)
        t = min(s['dur'] - 0.1, (m['t'] + 0.35) if m else s['dur'] * 0.6)
        jp = os.path.join(tmpd, f'sheet_{s["scene"]}.jpg')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{t:.3f}', '-i', os.path.join(SEG, s['file']), '-frames:v', '1',
                        '-vf', f'scale={tw}:{th}', jp], check=True)
        x, y = (i % cols) * tw, (i // cols) * (th + 34)
        img.paste(Image.open(jp), (x, y + 34))
        ImageDraw.Draw(img).text((x + 6, y + 7), f'{s["file"][:-4]}  @{t:.2f}s' + ('  (fallback)' if s['replaces'] else ''), fill=(232, 214, 160), font=font)
    img.save(os.path.join(HERO, 'ANIMS_SHEET.jpg'), quality=86)
    print('wrote hero/ANIMS_SHEET.jpg', len(items), 'scenes')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if cmd == 'cfg': write_cfg()
    elif cmd == 'render': render(sys.argv[2:] or None)
    elif cmd == 'beats': beats()
    elif cmd == 'snaps': snaps(sys.argv[2], sys.argv[3])
    elif cmd == 'sheet': sheet()
    elif cmd == 'all': render(); sheet()
    else: sys.exit(__doc__)
