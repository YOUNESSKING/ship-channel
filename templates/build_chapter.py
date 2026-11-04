#!/usr/bin/env python3
"""Shot list -> HyperFrames chapter project.

  python3 build_chapter.py chapter.json [--out DIR] [--no-media] [--list]

Reads a chapter JSON (see README.md), writes <out>/index.html (the composition), <out>/sfx_events.json, the conformed
clips and fonts. Then render with render_chapters.sh. Times inside a chapter are chapter-local seconds.
"""
import json, os, re, sys, shutil, subprocess, hashlib, argparse, html as _html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from blocks import REGISTRY
from blocks.common import esc

class BuildError(Exception): pass
import colorsys as _cs
_HEX = re.compile(r'#([0-9a-fA-F]{6})\b'); _RGB = re.compile(r'rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)')
def retint(text, th):
    """Animation colour theme per video (owner, 30 Oct 2026: the green ink was chosen for V03's jungle; each video picks its own).
    Every green/teal colour (hue 80-200 deg) of an animation block is moved to th['hue'] (deg), saturation x th['sat'], lightness kept."""
    h0, sf = float(th.get('hue', 36)) / 360, float(th.get('sat', .8))
    def conv(r, g, b):
        h, l, sa = _cs.rgb_to_hls(r / 255, g / 255, b / 255)
        if not (80 / 360 <= h <= 200 / 360) or sa < .06: return None
        r2, g2, b2 = _cs.hls_to_rgb(h0, l, min(1, sa * sf)); return round(r2 * 255), round(g2 * 255), round(b2 * 255)
    def fh(m):
        x = m.group(1); c = conv(int(x[:2], 16), int(x[2:4], 16), int(x[4:], 16))
        return m.group(0) if c is None else '#%02x%02x%02x' % c
    def fr(m):
        c = conv(*(int(m.group(i)) for i in (1, 2, 3)))
        return m.group(0) if c is None else m.group(0).split('(')[0] + '(%d,%d,%d' % c
    return _RGB.sub(fr, _HEX.sub(fh, text))
def norm(w): return re.sub(r'[^a-z0-9]', '', str(w).lower())

class Words:
    """Narration word list of a chapter. Optional spliced inserts (extra recorded lines):
         "inserts": [{"id":"kelp","audio":"../voice/insert_kelp.mp3","words":"../voice/insert_kelp_words.json","after_word":986}]
       The insert is cut in after word `after_word` (in the middle of the gap to the next word, or at "cut": narration seconds).
       Every later word moves later by the insert length. Original word numbers stay the same ("w987"); the insert's own words are
       "kelp.3" (start of its word 3), "kelp.3e" (end), "kelp.end" (end of the insert)."""
    def __init__(self, path, offset=0.0, inserts=(), base=None):
        self.w = json.load(open(path)); self.off = offset
        self.n = [norm(x['w']) for x in self.w]; self.ins = []
        for k in inserts:
            def rp(q): return q if os.path.isabs(q) else os.path.normpath(os.path.join(base or '.', q))
            iw = json.load(open(rp(k['words']))); a = int(k['after_word'])
            L = float(k.get('dur') or self._probe(rp(k['audio'])) or (iw[-1]['end'] + .05))
            cut = float(k['cut']) if 'cut' in k else (self.w[a]['end'] + self.w[a + 1]['start']) / 2
            self.ins.append(dict(id=k['id'], after=a, cut=cut, L=L, words=iw, audio=rp(k['audio'])))
        self.ins.sort(key=lambda x: x['after'])
        self.flat = []
        for i in range(len(self.w)): self.flat.append((self.n[i], self.start(i), self.end(i)))
        for x in self.ins:
            x['t0'] = self.ins_start(x)
            for q in x['words']: self.flat.append((norm(q['w']), x['t0'] + q['start'], x['t0'] + q['end']))
        self.flat.sort(key=lambda r: r[1])
    @staticmethod
    def _probe(f):
        try: return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).decode().strip())
        except Exception: return None
    def shift(self, i): return sum(x['L'] for x in self.ins if i > x['after'])
    def ins_start(self, x): return x['cut'] - self.off + sum(y['L'] for y in self.ins if y['after'] < x['after'])
    def insert_total(self): return sum(x['L'] for x in self.ins)
    def start(self, i): return self.w[i]['start'] - self.off + self.shift(i)
    def end(self, i): return self.w[i]['end'] - self.off + self.shift(i)
    def ins_time(self, iid, what):
        for x in self.ins:
            if x['id'] == iid:
                if what == 'end': return x['t0'] + x['L']
                k = int(what.rstrip('e')); q = x['words'][k]; return x['t0'] + (q['end'] if what.endswith('e') else q['start'])
        raise BuildError(f'no insert "{iid}" in this chapter')
    def find(self, text, after, nth=1):
        toks = [norm(x) for x in text.split() if norm(x)]
        hits = []
        for i in range(len(self.flat) - len(toks) + 1):
            if [r[0] for r in self.flat[i:i + len(toks)]] == toks and self.flat[i][1] >= after - 0.3: hits.append(i)
        if len(hits) < nth:
            near = ' '.join(r[0] for r in self.flat if abs(r[1] - after) < 4)
            raise BuildError(f'word "{text}" (#{nth}) not found after {after:.2f}s. Words near there: {near}')
        return self.flat[hits[nth - 1]][1]

_OFF = re.compile(r'([+-]\d+(?:\.\d+)?)$')
class Ctx:
    """What a block sees: its shot, its times, helpers for the clip, sfx and params."""
    def __init__(self, B, shot, a, b):
        self.B = B; self.shot = shot; self.a = a; self.b = b; self.dur = b - a
        self.id = re.sub(r'[^A-Za-z0-9_]', '_', str(shot['id']))
        if not self.id[0].isalpha(): self.id = 's' + self.id
        self.variant = shot.get('variant'); self.params = shot.get('params', {}); self._used = set()
        self.chapter = B.chapter; self.events = []; self.js = []; self.warnings = []
    # ---- params
    def p(self, name, default=None):
        self._used.add(name); return self.params.get(name, default)
    def unused_params(self): return [k for k in self.params if k not in self._used]
    # ---- time: number = seconds after the shot start; "w12" word start; "w12e" word end; "@zero" first spoken "zero"; "t38.3" chapter time; "end"; add +/-seconds
    def t(self, spec, rel=None):
        if spec is None:
            if rel is None: raise BuildError(f'shot {self.id}: a time is missing')
            return self.a + rel
        if isinstance(spec, (int, float)): return self.a + float(spec)
        s = str(spec).strip(); off = 0.0
        m = _OFF.search(s)
        if m and len(s) > len(m.group(1)) and not re.fullmatch(r'[+-]?\d+(\.\d+)?', s):
            off = float(m.group(1)); s = s[:m.start()].strip()
        W = self.B.words
        if re.fullmatch(r'[+-]?\d+(\.\d+)?', s): return self.a + float(s)
        if s == 'start': return self.a + off
        if s == 'end': return self.b + off
        if s.startswith('t') and re.fullmatch(r't\d+(\.\d+)?', s): return float(s[1:]) + off
        mi = re.fullmatch(r'([A-Za-z_]\w*)\.(end|\d+e?)', s)
        if mi: return W.ins_time(mi.group(1), mi.group(2)) + off
        mm = re.fullmatch(r'w(\d+)(e?)', s)
        if mm:
            i = int(mm.group(1))
            if i >= len(W.w): raise BuildError(f'shot {self.id}: word index {i} does not exist')
            return (W.end(i) if mm.group(2) else W.start(i)) + off
        if s.startswith('@'):
            txt = s[1:]; nth = 1
            mn = re.search(r'#(\d+)$', txt)
            if mn: nth = int(mn.group(1)); txt = txt[:mn.start()]
            return W.find(txt, self.a, nth) + off
        raise BuildError(f'shot {self.id}: cannot read time "{spec}"')
    # ---- sound
    def sfx(self, cue, t, gain=1.0): self.events.append({'t': round(t, 3), 'cue': cue, 'gain': gain})
    # ---- clip
    @property
    def clip(self): return self.shot.get('clip') or {}
    @property
    def plain(self): return bool(self.shot.get('card') or self.params.get('plain')) and not self.clip.get('file')
    def video(self, push=(1.0, 1.06, '50% 50%'), track=1, dim=None):
        """The shot's video element (conformed, trimmed) + its slow push + optional jumps. Returns html ('' if the shot has no clip)."""
        c = self.clip
        if not c.get('file'):
            if self.shot.get('card') or self.params.get('plain'):      # a text card: dark textured picture instead of a clip (no clip needed)
                self._used.add('plain'); vid = f'{self.id}_v'; pu = c.get('push', [1.0, 1.04, '50% 50%'])
                if pu: self.js.append(f"kb('#{vid}',{self.a:.3f},{self.b:.3f},{pu[0]},{pu[1]},'{pu[2] if len(pu) > 2 else '50% 50%'}');")
                return f'<div id="{vid}" class="clip card" data-start="{self.a:.3f}" data-duration="{self.dur:.3f}" data-track-index="{track}"></div>'
            return ''
        vid = f'{self.id}_v'
        src = self.B.conform(self, c)
        if src: h = (f'<video id="{vid}" class="clip aivid" data-start="{self.a:.3f}" data-duration="{self.dur:.3f}" data-media-start="0" '
                     f'src="{src}" muted playsinline data-track-index="{track}"></video>')
        else: h = (f'<div id="{vid}" class="clip ph" data-start="{self.a:.3f}" data-duration="{self.dur:.3f}" data-track-index="{track}">'
                   f'<div class="phlabel">CLIP MISSING: {esc(c["file"])}</div></div>')
        pu = c.get('push', list(push) if push else None)
        if pu:
            self.js.append(f"kb('#{vid}',{self.a:.3f},{self.b:.3f},{pu[0]},{pu[1]},'{pu[2] if len(pu) > 2 else '50% 50%'}');")
        for j in c.get('jumps', []):
            self.js.append(f"jump('#{vid}',{self.t(j['at']):.3f},{j['scale']},'{j.get('origin', pu[2] if pu and len(pu) > 2 else '50% 50%')}');")
        return h
    def overlay(self, inner, z=10, track=2, cls='ov', style=''):
        return (f'<div id="ov-{self.id}" class="clip {cls}" data-start="{self.a:.3f}" data-duration="{self.dur:.3f}" '
                f'data-track-index="{track}" style="z-index:{z};{style}">{inner}</div>')
    def shot_div(self, inner, cls='', track=1):
        return (f'<div id="{self.id}" class="clip shot {cls}" data-start="{self.a:.3f}" data-duration="{self.dur:.3f}" '
                f'data-track-index="{track}">{inner}</div>')
    def asset(self, path):
        """Copy a file (relative to the chapter json, or absolute) into the project assets and return its relative src."""
        return self.B.add_asset(path)

class Builder:
    def __init__(self, chapter_path, out=None, media=True, res=None):
        self.cp = os.path.abspath(chapter_path); self.dir = os.path.dirname(self.cp)
        self.chapter = json.load(open(self.cp)); self.media = media
        self.res = int(res or self.chapter.get('res', 720))
        if self.res not in (720, 1080): raise BuildError('res must be 720 or 1080')
        self.key = self.chapter.get('key', os.path.splitext(os.path.basename(self.cp))[0])
        self.W = int(self.chapter.get('width', 1280)); self.H = int(self.chapter.get('height', 720))
        if (self.W, self.H) != (1280, 720): raise BuildError('Only 1280x720 is supported (render at 1080p later with the render script).')
        self.out = os.path.abspath(out or os.path.join(self.dir, 'work', self.key))
        self.cache = os.path.join(self.dir, 'media_cache'); self.assets = {}; self.warn = []
        wp = self.chapter['words']; wp = wp if os.path.isabs(wp) else os.path.join(self.dir, wp)
        self.words = Words(wp, float(self.chapter.get('audio_offset', 0.0)), self.chapter.get('inserts', []), self.dir)
        self.clips_dir = self.chapter.get('clips_dir', 'clips')
        if not os.path.isabs(self.clips_dir): self.clips_dir = os.path.join(self.dir, self.clips_dir)
    def resolve(self, p, base=None):
        if os.path.isabs(p): return p
        for b in ([base] if base else []) + [self.dir]:
            if os.path.exists(os.path.join(b, p)): return os.path.join(b, p)
        return os.path.join(base or self.dir, p)
    # ---- media
    def probe(self, f):
        try: return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).decode().strip())
        except Exception: return None
    def conform(self, ctx, c):
        src = self.resolve(c['file'], self.clips_dir)
        if not os.path.exists(src): self.warn.append(f'{ctx.id}: clip file not found: {src}'); return None
        if not self.media: return 'assets/clips/' + ctx.id + '.mp4'
        off = float(c.get('in', 0.0)); need = ctx.dur
        d = self.probe(src)
        if d is not None and d - off < need - 0.05:
            self.warn.append(f'{ctx.id}: clip has only {d-off:.2f}s after "in" but the shot needs {need:.2f}s (last frame will freeze; rule 28). Use a longer clip or earlier "in".')
        os.makedirs(self.cache, exist_ok=True)
        gname = os.environ.get('GRADE', 'deep_time'); gfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'grade', gname + '.vf')
        grade = open(gfile).read().strip() if (c.get('grade', ctx.shot.get('template') != 'map_clip') and gname != 'none' and os.path.exists(gfile)) else ''
        key = hashlib.md5(f'{src}|{os.path.getmtime(src):.0f}|{off}|{need:.3f}|{self.res}|{grade}'.encode()).hexdigest()[:12]
        dst = os.path.join(self.cache, f'{ctx.id}_{key}.mp4')
        if not os.path.exists(dst):
            mw, mh = (1920, 1080) if self.res == 1080 else (1280, 720)
            vf = f'scale={mw}:{mh}:force_original_aspect_ratio=increase,crop={mw}:{mh},fps=30,tpad=stop_mode=clone:stop_duration=4,setsar=1'
            if grade: vf += ',' + grade
            tmp = dst + '.tmp.mp4'
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{off:.3f}', '-i', src, '-an', '-t', f'{need + 0.2:.3f}', '-vf', vf,
                            '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-g', '15', '-pix_fmt', 'yuv420p', tmp], check=True)
            os.replace(tmp, dst)
        rel = f'assets/clips/{ctx.id}.mp4'; self.assets[rel] = dst
        return rel
    def add_asset(self, path):
        src = self.resolve(path)
        if not os.path.exists(src): self.warn.append(f'asset not found: {src}'); return ''
        rel = 'assets/img/' + os.path.basename(src); self.assets[rel] = src; return rel

    def build(self):
        ch = self.chapter; shots = ch['shots']; W = self.words
        # resolve start times (chapter seconds)
        starts = []
        for i, s in enumerate(shots):
            st = s.get('start', 0.0 if i == 0 else None)
            if st is None: raise BuildError(f'shot {s.get("id")}: "start" is missing')
            if isinstance(st, (int, float)): starts.append(float(st))           # a number = chapter seconds
            else: starts.append(Ctx(self, s, starts[-1] if starts else 0.0, 0.0).t(st))   # "w117" / "@zero" / "t38.3"
        total = float(ch['duration']) + W.insert_total() if 'duration' in ch else None    # "duration" = narration length WITHOUT inserts
        ends = []
        for i, s in enumerate(shots):
            if 'end' in s: e = Ctx(self, s, starts[i], starts[i]).t(s['end'])
            elif 'dur' in s: e = starts[i] + float(s['dur'])
            elif i + 1 < len(shots): e = starts[i + 1]
            elif total: e = total
            else: raise BuildError(f'last shot {s.get("id")} needs "end" or "dur" (or set chapter "duration")')
            ends.append(e)
        total = total or max(ends)
        for i in range(len(shots) - 1):
            if ends[i] < starts[i + 1] - 0.02: self.warn.append(f'gap of {starts[i+1]-ends[i]:.2f}s after shot {shots[i]["id"]} (black)')
            if ends[i] > starts[i + 1] + 0.02: self.warn.append(f'shot {shots[i]["id"]} overlaps the next shot by {ends[i]-starts[i+1]:.2f}s')
        body = []; js = []; css_extra = {}; events = []; report = []; defs_extra = {}
        for s, a, b in zip(shots, starts, ends):
            name = s['template']
            if name not in REGISTRY: raise BuildError(f'shot {s.get("id")}: unknown template "{name}". Known: {", ".join(sorted(REGISTRY))}')
            mod = REGISTRY[name]
            if 'variant' not in s: s['variant'] = mod.META['variants'][0]
            if s['variant'] not in mod.META['variants']:
                raise BuildError(f'shot {s["id"]}: template {name} has no variant "{s["variant"]}". Variants: {", ".join(mod.META["variants"])}')
            ctx = Ctx(self, s, a, b)
            if b - a > 6.0 and s['variant'] not in getattr(mod, 'LONG_OK', ()): self.warn.append(f'shot {ctx.id} is {b-a:.1f}s long (rule 22: hard cap 6 s)')
            try: r = mod.build(ctx)
            except KeyError as e: raise BuildError(f'shot {ctx.id} ({name}): missing or bad value {e}')
            th = ch.get('anim_theme')
            if th and (name.startswith('anim_') or name.startswith('v02_anim')):
                r = {k: (retint(v, th) if isinstance(v, str) else v) for k, v in r.items()}; ctx.js = [retint(x, th) for x in ctx.js]
            if s.get('bg_clip'):   # (ship channel v3) an animation shot over a darkened MOVING clip: the clip plays underneath, the block's ink background turns translucent
                _bc = s['bg_clip']; _keep = s.get('clip'); s['clip'] = {'file': _bc['file'], 'push': _bc.get('push', [1.0, 1.06, '50% 50%'])}
                _bg = ctx.video(track=0); s['clip'] = _keep; css_extra['bgclip_' + ctx.id] = f'#{ctx.id}{{background:transparent !important}}'
                r['html'] = _bg + r['html'].replace('class="an-bg" style="background:', f'class="an-bg" style="opacity:{1 - float(_bc.get("show", 0.45)):.2f};background:', 1)
            body.append(r['html']); js.append(f'// ---- {ctx.id}: {name}/{s["variant"]}\n' + '\n'.join(ctx.js) + '\n' + r.get('js', ''))
            if r.get('css'): css_extra[name] = r['css']
            defs_extra.update(r.get('defs') or {})
            for u in ctx.unused_params(): self.warn.append(f'shot {ctx.id}: parameter "{u}" is not used by {name}/{s["variant"]} (typo?)')
            if s.get('flash'):   # 2-frame white flash on the cut (trailer hit); "dip" = a soft dark dip instead (cinematic)
                col, o0, fd = ('#000', .75, .45) if s['flash'] == 'dip' else ('#fff', .85, .22)
                body.append(f'<div id="{ctx.id}-fl" class="clip" data-start="{a:.3f}" data-duration="0.25" data-track-index="8" style="position:absolute;left:0;top:0;width:1280px;height:720px;background:{col};z-index:55;opacity:0"></div>')
                js.append(f"tl.fromTo('#{ctx.id}-fl',{{opacity:{o0}}},{{opacity:0,duration:{fd},ease:'power2.out',immediateRender:false}},{a:.3f});")
            if s.get('frost'):   # frost creeps in from the edges over the shot
                body.append(f'<div id="{ctx.id}-fr" class="clip" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="8" style="position:absolute;left:0;top:0;width:1280px;height:720px;z-index:54;opacity:0;pointer-events:none;'
                            f'background:radial-gradient(ellipse at center,rgba(220,235,245,0) 45%,rgba(220,235,245,.35) 70%,rgba(240,248,255,.92) 100%);box-shadow:inset 0 0 140px 30px rgba(235,245,255,.75)"></div>')
                js.append(f"tl.fromTo('#{ctx.id}-fr',{{opacity:0}},{{opacity:1,duration:{max(.5, b - a - .2):.2f},ease:'power1.in',immediateRender:false}},{a:.3f});")
            ev = ctx.events
            if s.get('sfx') is False: ev = []
            elif isinstance(s.get('sfx'), list):
                for x in s['sfx']: ev.append({'t': round(ctx.t(x.get('at')), 3), 'cue': x['cue'], 'gain': x.get('gain', 1.0)})
            if s.get('ambience'):
                am = s['ambience']; ev.append({'t': round(a, 3), 'cue': am['cue'], 'gain': am.get('gain', 0.3), 'dur': round(b - a, 3)})
            events += ev; report.append((ctx.id, name, s['variant'], a, b))
        for x in ch.get('extra_events', []):   # chapter-level sound design (environment / things / mood layers); "t" = chapter seconds or a time spec ("w812", "@word")
            t0 = x['t'] if isinstance(x['t'], (int, float)) else Ctx(self, {'id': 'snd'}, 0.0, total).t(x['t'])
            e = {'t': round(float(t0), 3), 'cue': x['cue'], 'gain': x.get('gain', 1.0)}
            if x.get('dur'): e['dur'] = x['dur']
            events.append(e)
        fo = float(ch.get('fade_out', 0)); fi = float(ch.get('fade_in', 0))
        if fo: body.append(f'<div id="fade" class="clip" data-start="{total-fo:.3f}" data-duration="{fo:.3f}" data-track-index="9"></div>'); js.append(f"gsap.set('#fade',{{opacity:0}});tl.to('#fade',{{opacity:1,duration:{fo},ease:'none'}},{total-fo:.3f});")
        if fi: body.append(f'<div id="fadein" class="clip" data-start="0" data-duration="{fi:.3f}" data-track-index="9" style="position:absolute;left:0;top:0;width:1280px;height:720px;background:#000;z-index:60"></div>'); js.append(f"tl.fromTo('#fadein',{{opacity:1}},{{opacity:0,duration:{fi},ease:'none'}},0);")
        css = open(os.path.join(HERE, 'lib', 'fonts_face.css')).read() + open(os.path.join(HERE, 'lib', 'style.css')).read() + open(os.path.join(HERE, 'lib', 'blocks.css')).read() + ''.join(css_extra.values())
        if ch.get('font') == 'oswald':   # (ship channel v3) one font family for the whole chapter: Oswald (map/label font), gold stays the accent colour
            css += ("@font-face{font-family:'Oswald';font-weight:500;src:url('assets/fonts/oswald-latin-500-normal.woff2') format('woff2')}"
                    "@font-face{font-family:'Oswald';font-weight:700;src:url('assets/fonts/oswald-latin-700-normal.woff2') format('woff2')}"
                    "#root *{font-family:'Oswald',sans-serif !important;font-style:normal !important}"
                    "#root svg text,#root svg tspan{font-family:'Oswald',sans-serif !important;font-style:normal !important}")
        rt = open(os.path.join(HERE, 'lib', 'runtime.js')).read()
        title = _html.escape(ch.get('title', self.key))
        RW, RH = (1920, 1080) if self.res == 1080 else (1280, 720)
        STAGE0 = STAGE1 = ''
        if self.res == 1080:
            css += 'html,body,#root{width:1920px;height:1080px}#stage{position:absolute;left:0;top:0;width:1280px;height:720px;transform:scale(1.5);transform-origin:0 0;overflow:hidden}'
            STAGE0 = '<div id="stage">'; STAGE1 = '</div>'
        page = f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width={RW}, height={RH}"/>
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{css}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{RW}" data-height="{RH}">
{STAGE0}{('<svg width="0" height="0" style="position:absolute"><defs>' + ''.join(defs_extra.values()) + '</defs></svg>') if defs_extra else ''}{chr(10).join(body)}{STAGE1}
</div>
<script>{rt}
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines['main'] = tl;
</script>
</body></html>'''
        os.makedirs(os.path.join(self.out, 'assets', 'fonts'), exist_ok=True)
        old = os.path.join(self.out, 'assets', 'clips')
        if os.path.isdir(old): shutil.rmtree(old)
        open(os.path.join(self.out, 'index.html'), 'w').write(page)
        for f in os.listdir(os.path.join(HERE, 'lib', 'fonts')): shutil.copy2(os.path.join(HERE, 'lib', 'fonts', f), os.path.join(self.out, 'assets', 'fonts', f))
        if ch.get('font') == 'oswald':
            for f in ('oswald-latin-500-normal.woff2', 'oswald-latin-700-normal.woff2'): shutil.copy2(os.path.join(HERE, '..', 'map-kit', 'assets', 'fonts', f), os.path.join(self.out, 'assets', 'fonts', f))
        for f in ('hyperframes.json', 'package.json', 'meta.json'): shutil.copy2(os.path.join(HERE, 'lib', 'hf_template', f), os.path.join(self.out, f))
        shutil.copy2(os.path.join(HERE, 'lib', 'icy_sea.jpg'), os.path.join(self.out, 'assets', 'icy_sea.jpg'))
        for rel, src in self.assets.items():
            dst = os.path.join(self.out, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst): os.remove(dst)
            try: os.link(src, dst)
            except OSError: shutil.copy2(src, dst)
        events.sort(key=lambda e: e['t'])
        json.dump({'chapter': self.key, 'duration': round(total, 3), 'audio_offset': self.words.off, 'events': events,
                   'inserts': [{'id': x['id'], 'audio': x['audio'], 'cut': round(x['cut'], 3), 'at': round(x['t0'], 3), 'dur': round(x['L'], 3)} for x in self.words.ins]}, open(os.path.join(self.out, 'sfx_events.json'), 'w'), indent=1)
        return total, report, events

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('chapter', nargs='?'); ap.add_argument('--out'); ap.add_argument('--no-media', action='store_true'); ap.add_argument('--res', type=int, choices=[720, 1080], help='720 (default, drafts) or 1080 (delivery)')
    ap.add_argument('--list', action='store_true', help='list templates, variants and parameters')
    a = ap.parse_args()
    if a.list or not a.chapter:
        for n, m in sorted(REGISTRY.items()):
            print(f'{n}  -  {m.META["about"]}\n   variants: {", ".join(m.META["variants"])}')
            for k, v in m.META['params'].items(): print(f'     {k}: {v}')
        return
    try:
        B = Builder(a.chapter, a.out, media=not a.no_media, res=a.res); total, rep, ev = B.build()
    except BuildError as e:
        sys.exit(f'ERROR: {e}')
    for (i, n, v, s, e) in rep: print(f'  {s:7.2f} - {e:7.2f}  {e-s:4.1f}s  {i:12s} {n}/{v}')
    print(f'built {B.out}/index.html  ({total:.1f}s, {len(rep)} shots, {len(ev)} sfx events)')
    for w in B.warn: print('WARNING:', w)
if __name__ == '__main__': main()
