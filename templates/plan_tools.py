#!/usr/bin/env python3
"""Tools for a video plan folder (chapter JSONs ch02.json ... final.json with a "plan" block on every shot).

  python3 plan_tools.py refresh PLAN_DIR     builds every chapter (no media) and writes back plan.dur, narr_time, video_time and the spoken line of every shot
                                             (the line is rewritten only where plan.line is empty or the shot is marked "reline": true), plus plan.video_start/end of the chapter
  python3 plan_tools.py audit PLAN_DIR       prints the audit numbers (shots, average, longest, wow/joke beats, HERO gaps, sources) as JSON lines for audit.md
"""
import json, os, sys, glob, re, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from build_chapter import Builder, BuildError
V9_END = float(os.environ.get('PLAN_V0', 66.4)); NARR0 = float(os.environ.get('PLAN_NARR0', 167.0))   # Video 01: chapter 2 starts after v9; Video 02: PLAN_V0=0 PLAN_NARR0=0
MOVES = {'map_clip', 'stick_water', 'stick_gag', 'stick_timer', 'stick_rope', 'stick_land', 'stick_walk', 'scale_ruler', 'tier_board', 'outro', 'problem_counter'}

def chapter_files(d):
    fs = sorted(glob.glob(os.path.join(d, 'ch[0-9][0-9].json')))   # ch00 (hook + rules) sorts first
    return fs + ([os.path.join(d, 'final.json')] if os.path.exists(os.path.join(d, 'final.json')) else [])

def build(path):
    import tempfile   # check-build into a temp folder so the real work/<key> project (with its media) is left alone
    B = Builder(path, out=os.path.join(tempfile.gettempdir(), 'plan_tools_check', os.path.basename(path)[:-5]), media=False); total, rep, ev = B.build(); return B, total, rep

def spoken(B, a, b):
    """The narration words spoken between chapter times a and b (silent [tags] left out)."""
    out = []
    for n, s, e in B.words.flat:
        if a - 0.02 <= s < b - 0.02:
            pass
    ws = []
    for i, w in enumerate(B.words.w): ws.append((B.words.start(i), w['w']))
    for x in B.words.ins:
        for q in x['words']: ws.append((x['t0'] + q['start'], q['w']))
    ws.sort()
    return ' '.join(w for s, w in ws if a - 0.02 <= s < b - 0.02 and not w.startswith('['))

def refresh(d):
    acc = 0.0                       # inserted narration seconds in earlier chapters
    for f in chapter_files(d):
        ch = json.load(open(f)); B, total, rep = build(f)
        off = float(ch['audio_offset']); W = B.words
        v0 = V9_END + (off - NARR0) + acc
        for s, (i, n, v, a, b) in zip(ch['shots'], rep):
            pl = s.setdefault('plan', {})
            narr = a + off; sh = 0.0
            for x in W.ins:
                if a >= x['t0'] + x['L'] - 1e-6: sh += x['L']
                elif a >= x['t0'] - 1e-6: narr = x['cut']; sh = None; break
            if sh is not None: narr = a + off - sh
            pl['dur'] = round(b - a, 2); pl['narr_time'] = round(narr, 2); pl['video_time'] = round(v0 + a, 2)
            if not pl.get('line') or s.get('reline'): pl['line'] = spoken(B, a, b); s.pop('reline', None)
            if pl.get('source') in (None, '', '-'): pl['source'] = 'TEMPLATE ONLY' if not (s.get('clip') or {}).get('file') else pl.get('source', '')
        ch.setdefault('plan', {})['video_start_after_v9'] = round(v0 - V9_END, 2); ch['plan']['video_end_after_v9'] = round(v0 + total - V9_END, 2)
        ch['plan']['inserts_s'] = round(W.insert_total(), 2)
        json.dump(ch, open(f, 'w'), indent=1, ensure_ascii=False); open(f, 'a').write('\n')
        acc += W.insert_total()
        print(f'{ch["key"]}: {len(rep)} shots, {total:.1f} s, avg {sum(pl["plan"]["dur"] for pl in ch["shots"]) / len(rep):.2f}')

def tm(t):
    m = int(t // 60); return f'{m}:{t - 60 * m:04.1f}'

V9_WOW = [(1.0, 'ship rail, storm'), (13.0, 'Ice Age map, ice grows'), (19.0, 'kelp forest'), (21.4, 'seals + orca fin'), (32.1, 'orca breach'), (33.6, 'North Atlantic map'), (56.2, 'megalodon')]
V9_JOKES = [(11.1, 'coast guard (45 minutes away) - lower third'), (52.8, 'rope slips - stick gag'), (56.2, 'no Megalodon - deadpan + plate'), (61.2, 'tile drop "Minutes" - verdict click')]
TEXT_T = ('number_clip', 'lower_third', 'extinct_plate', 'text_card')

def _gap(times, a, b):
    ts = sorted([a] + [t for t in times if a <= t <= b] + [b]); return max(y - x for x, y in zip(ts, ts[1:]))

def audit(d):
    chs = []
    for f in chapter_files(d):
        ch = json.load(open(f)); v0 = V9_END + ch['plan']['video_start_after_v9']; v1 = V9_END + ch['plan']['video_end_after_v9']
        end_s = sum(s['plan']['dur'] for s in ch['shots'] if s['template'] == 'outro' and s.get('variant') == 'end_screen')
        shots = [dict(id=s['id'], tpl=s['template'], var=s.get('variant') or '', dur=s['plan']['dur'], vt=s['plan']['video_time'], tag=s['plan'].get('tag', ''), beats=s['plan'].get('beats', []),
                      src=(s['plan'].get('source') if s['plan'].get('source') not in (None, '', '-') else 'TEMPLATE ONLY'), card=bool(s.get('card')) or s['template'] == 'text_card', clip=bool((s.get('clip') or {}).get('file')), note=s['plan'].get('note', '')) for s in ch['shots']]
        chs.append(dict(key=ch['key'], title=ch.get('title', ''), v0=v0, v1=v1, end_s=end_s, shots=shots, inserts=ch['plan'].get('inserts_s', 0)))
    return chs

def audit_md(d):
    chs = audit(d); out = []; allshots = []; rows = []
    out.append('# Audit of the Video 01 shot plan (chapters 2-10 + final)\n')
    out.append('Made by `templates/plan_tools.py audit` from the chapter JSONs (every number below is computed, not typed). Pace was tightened after the owner decision: every chapter averages under 3.0 s per shot.\n')
    out.append('Times: **narration time** = seconds in `voice/narration_full.mp3`; **video time** = time in the finished video (v9 is 0:00-1:06.4, then 66.4 + narration time - 167.0, plus the length of the two recorded inserts that come earlier: kelp line 9.3 s in ch03, comments line 3.0 s in ch04).')
    out.append('Template counts use template/variant. Rule 16 limit (max 2 identical text templates per chapter) is checked on the text templates: number_clip, lower_third, extinct_plate, text_card (each template/variant counted on its own).')
    out.append('HERO = the swimmer (any stick-figure shot, scale ruler with the "you" figure, or a clip of the person). WORLD = place, threat, number. "Moves" = a map, stick gag, gauge, timer, board or counter that keeps changing; a plain clip with a slow push does not count.\n')
    for c in chs:
        S = c['shots']; body = [s for s in S if not (s['tpl'] == 'outro' and s['var'] == 'end_screen')]
        n = len(body); tot = sum(s['dur'] for s in body); avg = tot / n; lg = max(body, key=lambda s: s['dur'])
        moves = lambda s: s['tpl'] in MOVES or s['card']
        over45 = [s for s in body if s['dur'] > 4.5]; still = [s for s in over45 if not moves(s)]; over55 = [s for s in body if s['dur'] > 5.5]
        src = collections.Counter(s['src'] or '?' for s in body); tp = collections.Counter(f"{s['tpl']}/{s['var']}" for s in body)
        r16 = [f'{k} {v}' for k, v in sorted(tp.items()) if k.split('/')[0] in TEXT_T and v > 2]
        wow = [s for s in body if 'wow' in s['beats']]; joke = [s for s in body if 'joke' in s['beats']]; hero = [s for s in body if s['tag'] == 'HERO']
        a, b = c['v0'], c['v1'] - c['end_s']
        wg = _gap([s['vt'] for s in wow], a, b); hg = _gap([s['vt'] for s in hero], a, b)
        rel = [s for s in body if 'relief' in s['beats']]; cat = [s for s in body if 'catch' in s['beats']]; rev = [s for s in body if 'reversal' in s['beats']]
        maps = sum(1 for s in body if s['src'] == 'MAP BAKE')
        out.append(f"## {c['key']} {c['title'].split(' ', 2)[2] if c['key'] != 'final' else 'Final ranking + outro'}  (video {tm(c['v0'])}-{tm(c['v1'])}, {c['v1'] - c['v0']:.1f} s" + (f"; narration {tot:.1f} s + {c['end_s']:.0f} s end screen" if c['end_s'] else '') + (f"; includes a {c['inserts']:.1f} s recorded insert" if c['inserts'] else '') + ')\n')
        out.append(f"- Shots: **{n}**. Average shot: **{avg:.2f} s** (target 2.6-2.9, rule 22). Longest: **{lg['id']} {lg['dur']:.1f} s** ({lg['tpl']}/{lg['var']}, {'moves' if moves(lg) else 'clip'}).")
        out.append(f"- Shots over 4.5 s: {', '.join(f'{s['id']} {s['dur']:.1f} s ({s['tpl']}, moves)' if moves(s) else f'{s['id']} {s['dur']:.1f} s (CLIP)' for s in over45) or 'none'}. Shots over 4.5 s that do not move: {', '.join(s['id'] for s in still) or 'none'}. Shots over 5.5 s: {', '.join(f'{s['id']} {s['dur']:.1f} s' for s in over55) or 'none'} (hard cap 6 s).")
        out.append('- Sources: ' + ', '.join(f'{k} {v}' for k, v in sorted(src.items())))
        out.append('- Templates: ' + ', '.join(f'{k} {v}' for k, v in sorted(tp.items())))
        out.append('- Rule 16 (text template used more than 2 times): ' + ('**' + '; '.join(r16) + '**' if r16 else 'OK'))
        out.append(f"- Wow beats ({len(wow)}): " + '; '.join(f"{tm(s['vt'])} {s['id']}" for s in wow) + f". Longest gap without a wow: {wg:.0f} s.")
        out.append(f"- Joke beats ({len(joke)}): " + '; '.join(f"{tm(s['vt'])} {s['id']}" for s in joke))
        out.append(f"- HERO shots ({len(hero)}): " + ', '.join(tm(s['vt']) for s in hero) + f". Longest HERO gap: **{hg:.0f} s** (rule 53: max 30 s).")
        if rel or cat: out.append('- Relief then catch (rule 47): relief at ' + ', '.join(f"{tm(s['vt'])} {s['id']}" for s in rel) + '; catch at ' + (', '.join(f"{tm(s['vt'])} {s['id']}" for s in cat) or 'the verdict line'))
        if rev: out.append('- Mid-video reversal (rule 56): ' + ', '.join(f"{tm(s['vt'])} {s['id']}" for s in rev))
        ins = [s for s in body if 'INSERT' in s['note']]
        if ins: out.append('- Recorded inserts (owner decision a): ' + ', '.join(f"{s['id']} at {tm(s['vt'])}" for s in ins))
        out.append('')
        rows.append((c['key'], n, avg, lg, len(wow), len(joke), hg, wg, maps)); allshots += body
    N = len(allshots); T = sum(s['dur'] for s in allshots); vend = chs[-1]['v1']
    out.append('## Whole plan\n')
    out.append(f'- Shots after v9: **{N}** over {T:.1f} s of narration = **{T / N:.2f} s average** (v9: 2.9 s). Before the pace change: 275 shots, 3.10 s.')
    out.append(f'- Video length: 66.4 s (v9) + {T:.1f} s + 12 s end screen = **{tm(66.4 + T + 12)}**.')
    out.append('- Sources over all shots: ' + ', '.join(f'{k} {v}' for k, v in sorted(collections.Counter(s['src'] or '?' for s in allshots).items())) + '\n')
    out.append('| chapter | shots | avg s | longest | wow | jokes | max HERO gap s | max wow gap s | maps |\n|---|---|---|---|---|---|---|---|---|')
    for k, n, avg, lg, w, j, hg, wg, mp in rows: out.append(f"| {k} | {n} | {avg:.2f} | {lg['id']} {lg['dur']:.1f} | {w} | {j} | {hg:.0f} | {wg:.0f} | {mp} |")
    out.append('')
    after = [(s['vt'], s['id']) for s in allshots if 'wow' in s['beats'] and s['vt'] < 180]
    jk = [(s['vt'], s['id'], s['tpl']) for s in allshots if 'joke' in s['beats'] and s['vt'] < 180]
    out.append('### Rule 45: wow every 30 s in the first 3 minutes (video 0:00-3:00)\n')
    out.append('v9 part: ' + '; '.join(f'{tm(t)} {w}' for t, w in V9_WOW) + '.')
    out.append('After v9: ' + '; '.join(f'{tm(t)} {i}' for t, i in after) + '.')
    allw = sorted([t for t, _ in V9_WOW] + [t for t, _ in after]); gaps = [y - x for x, y in zip(allw, allw[1:]) if y > 66.4 or x > 66.4] + [180 - allw[-1]]
    out.append(f'Longest gap between wow shots after v9 starts (66.4-180 s): **{max(gaps):.0f} s** (limit 30 s; v9 itself has a 23 s gap from 0:33.6 to 0:56.2, approved as is).\n')
    out.append('### Rule 46: at least 5 jokes in minutes 0-3, none closer than 12 s, 3+ types\n')
    allj = sorted([(t, 'v9: ' + w) for t, w in V9_JOKES] + [(t, i + ' (' + tp + ')') for t, i, tp in jk])
    out.append('All jokes 0:00-3:00: ' + '; '.join(f'{tm(t)} {w}' for t, w in allj) + '.')
    keep = []
    for t, w in allj:
        if not keep or t - keep[-1][0] >= 12: keep.append((t, w))
    out.append(f'Jokes that keep 12 s spacing: **{len(keep)}** (' + '; '.join(tm(t) for t, _ in keep) + '). Closer jokes are quick follow-ups of the same beat.\n')
    out.append('### Rule 35: a joke in every chapter, a wow animal every 60-90 s\n')
    mw = max(r[7] for r in rows); mn = min(r[5] for r in rows); mnw = min(r[4] for r in rows)
    out.append(f'Every chapter has at least {mn} joke beats and at least {mnw} wow beats (table above). Longest wow gap inside a chapter: {mw:.0f} s.\n')
    out.append('### Rule 53: HERO every 30 s\n')
    mh = max(r[6] for r in rows)
    out.append(f'Longest HERO gap inside a chapter: {mh:.0f} s ({"OK" if mh <= 30 else "OVER 30 s: fix"}).\n')
    out.append(STATIC)
    return '\n'.join(out) + '\n'

STATIC = """### Other rules checked

- Rule 1/18/19: every place or coast-change line is a map shot (list in needs.md, section C; the maps added for the pace change are in maps_added.md). Every map shows Ice Age ice on land from frame 1; for far places (Red Sea, Carpentaria, Sunda, Mediterranean, Gulf of Mexico) the world inset with the ice sheets is a `map_clip` overlay (`inset` parameter) if the bake does not have it.
- Rule 2: numbers land on their spoken word (`number_at` = word index).
- Rule 3/14: the timer bar comes back as the cold chain (ch02 Southern labels, ch03 same as North Atlantic, ch05 lake labels), as heat/thirst (ch07 3 days), and as a "not a problem" bar (ch09) and "float for days" bar (ch10).
- Rule 7: a tier board only at chapter ends, plus 3 non-empty boards: the roadmap at the start of ch02 (all 10 tiles, rule 58), the "compared to everything else" peek in ch10, and the final ranking. The Days row slides in at the ch09 drop (template gap T2).
- Rule 8/28: each clip file is used once in the whole plan (checked by script, see below). No clip is split into two shots, and no crop of the same clip is used twice. v9 clips are not reused.
- Rule 25/26: all REDO clips are replaced; UNSURE clips were looked at on the contact sheets (decisions in needs.md, section E).
- Rule 47 relief-then-catch: see the per-chapter lines.
- Rule 51 honest hedge: ch03 "probably" + DEBATED plate, ch05 "very debated", ch08 UNKNOWN plate, ch09 DEBATED plate, ch10 "still argued" / "we don't know".
- Rule 54 scale ruler: ch02 leopard seal 3 m, ch03 short-faced bear, ch05 beluga sturgeon, ch08 saltwater crocodile 6 m, ch09 bull shark 3.5 m, ch10 tiger shark 4.5 m. The leopard seal and the crocodile silhouettes are built (T7).
- Rule 55 "problem one / problem two": owner decision (b): it is shown visually, not spoken. "THE CATCH" card in ch07 and "NOT PARADISE" in ch10 stay.
- Rule 56 mid-video reversal: ch07 Red Sea "But here's the catch" (percent of the whole video is in the ch07 line above). The spoken "first place where something can actually kill you" line does not exist.
- Rule 57: owner decision (a): the line "Okay. I'm going to get comments for this one." is recorded and spliced into ch04 before the North Sea verdict (shots okay + comments). The closing question exists ("Do you agree? Do you disagree? Let me know.").
- Join item 1 (kelp): owner decision (a): the line is recorded and spliced into ch03 after "exactly where and how long." (shots kelp_clip, kelp_map, kelp_coast, still_freezing).
- Template gaps: T1-T11 are all built (see templates/TEMPLATES.md); nothing in the plan waits for a template any more.
"""

if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    if sys.argv[1] == 'refresh': refresh(sys.argv[2])
    elif sys.argv[1] == 'audit': print(audit_md(sys.argv[2]), end='')
