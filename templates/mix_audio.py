#!/usr/bin/env python3
"""Sound for one chapter: sfx_events.json (+ the narration slice and an optional music file) -> audio/mix_raw.wav.

  python3 mix_audio.py WORK_DIR [--voice narration.mp3 --offset 33.6] [--music bed.wav --music-db -19 --music-gap-db -12]
                                [--el-dir DIR] [--amb-db -27 --amb-gap-db -21] [--stems]

Four layers (GOLD rules 99-100):
  1 environment  "env:<name>"  a recording from the sound library looped seamlessly (crossfaded) for "dur" seconds. It goes to the
                               ambience stem, which ducks under the voice (sidechain) and rises a little in voice pauses. Several env
                               events crossfade (1.5 s fades; 0.3 s at the chapter edges). Never leave a chapter without one.
                               Old ambience cues wind/ocean/bubbles/heli (synth) still work as before.
  2 things       "el:<name>"   one recording from the library (videos/video02/sfx_el/<name>.mp3, else templates/tests_anim/sfx_el/),
                               peak-normalised x gain; "dur" trims it with fades. Ducks 3 dB under the voice.
  3 mood         music bed (--music), heart / heart (dur = speeding heartbeat) / hit / boom / el:deep_boom / el:heartbeat,
                               verdict stings duck + riser + vhit (max 4 full stings, rule 65), the signature el:sig_headslap.
  4 graphics     synth: tick, ticks (dur), ticks_up (dur), tok, beep (dur, held 1.2 kHz lock-on), thud, thud_soft, click,
                               scratch, marker, swoosh, shimmer, title, stamp, ...  (see CUES)
Levels are fixed against the voice (so the music bed, which runs on across chapters, never jumps at a chapter join).
Identical events (same cue within 15 ms) are merged. --stems also writes audio/stem_voice.wav + stem_sd.wav (sound design)
for level checks (fixpass/SOUND.md). Final loudness (-14 LUFS) is set by mux.sh."""
import sys, os, json, argparse, subprocess, wave, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sfx_voices as V
SR = V.SR
EL_DIR = os.path.normpath(os.path.join(HERE, '..', 'videos', 'video02', 'sfx_el'))
EL_FALLBACK = [os.path.join(HERE, 'tests_anim', 'sfx_el')]
CUES = {
 'thud': lambda d: V.thud(1.2), 'thud_soft': lambda d: V.thud(.8, 46, 80), 'title': lambda d: _sum(V.thud(1.6, 34, 110), V.swoosh(.35) * .25),
 'stamp': lambda d: _sum(V.thud(.8, 45, 120), V.click() * .55), 'click': lambda d: V.click(), 'tick': lambda d: V.tick2(), 'tok': lambda d: V.tok(),
 'swoosh': lambda d: V.swoosh(.4), 'swoosh_rope': lambda d: V.swoosh(.45, 400, 2500), 'scratch': lambda d: V.scratch(), 'ding': lambda d: V.ding(1320),
 'ding_hi': lambda d: V.ding(1568), 'ding_low': lambda d: V.ding(440), 'gasp': lambda d: V.gasp(), 'splash': lambda d: V.splash(), 'downsweep': lambda d: V.downsweep(1.5, 300),
 'slide_down': lambda d: V.slide_down(.8, 1300, 180), 'icecrunch': lambda d: V.icecrunch(d or 1.8), 'heli': lambda d: V.heli(d or 2.0), 'wind': lambda d: V.wind(d or 3.0),
 'ocean': lambda d: V.ocean(d or 3.0), 'bubbles': lambda d: V.bubbles(d or 3.0),
 'snap': lambda d: _sum(V.click() * .9, V.thud(.5, 60, 160) * .8), 'boom': lambda d: _sum(V.thud(1.8, 32, 100), V.taiko(1.4) * .6),
 'riser': lambda d: V.downsweep(.75, 300)[::-1] * .8, 'vhit': lambda d: _sum(V.thud(1.6, 38, 90), V.click() * .35), 'duck': lambda d: np.zeros(1),   # verdict sting (style review 07 #1): duck = music dips out for dur s   # snap = jaw shut, boom = trailer hit
 # graphics for the animation blocks (rule 99 layer 4; tests_anim make_tests.py CUE / make_test4.py heart)
 'ticks': lambda d: V.ticks(d or 1.0), 'ticks_up': lambda d: V.ticks(d or 1.5, True), 'beep': lambda d: V.beep(d or 1.2),
 'shimmer': lambda d: V.shimmer(), 'marker': lambda d: V.marker(), 'hit': lambda d: V.hit(), 'heart': lambda d: V.heart_run(d) if d else V.heart()}
AMB_LEGACY = ('wind', 'ocean', 'bubbles', 'heli')
def _sum(a, b):
    n = max(len(a), len(b)); o = np.zeros(n); o[:len(a)] += a; o[:len(b)] += b; return o
def write(path, x):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
def decode(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(float) / 32768
_EL = {}
def el_file(name, el_dir):
    for d in [el_dir] + EL_FALLBACK:
        for ext in ('.mp3', '.wav'):
            p = os.path.join(d, name + ext)
            if os.path.exists(p): return p
    return None
def el_load(name, el_dir):
    if name not in _EL:
        p = el_file(name, el_dir); _EL[name] = decode(p) if p else None
    return _EL[name]
def el_thing(x, d):
    """a recording, peak 1; dur trims it (0.8 s fade-out, short fade-in) like tests_anim make_test7."""
    x = x / (np.max(np.abs(x)) + 1e-9)
    if d and d * SR < len(x):
        x = x[:int(d * SR)].copy(); f = min(len(x) // 3, int(.8 * SR)); x[-f:] *= np.linspace(1, 0, f)
        fi = min(len(x) // 4, int(.03 * SR)); x[:fi] *= np.linspace(0, 1, fi)
    return x
def el_loop(x, d, seed=0, xf=2.0):
    """a bed looped seamlessly to d seconds: rms 1, equal-power crossfades of xf s at every seam, random start inside the file."""
    x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9); n = int(d * SR); L = len(x); F = int(min(xf * SR, L / 4))
    fin = np.sin(np.linspace(0, np.pi / 2, F)); fout = np.cos(np.linspace(0, np.pi / 2, F))
    pos = int(np.random.default_rng(seed).uniform(0, L - 2 * F)); piece = x[pos:]; out = np.zeros(n + L); o = 0; first = True
    while o < n:
        p = piece.copy()
        if not first: p[:F] *= fin
        if o + len(p) < n: p[-F:] *= fout
        out[o:o + len(p)] += p; o += len(p) - F; piece = x; first = False
    return out[:n]
def env_curve(n, i0, L, fi, fo):
    e = np.zeros(n); j = min(n, i0 + L)
    if j <= i0: return e
    e[i0:j] = 1; fi = min(fi, (j - i0) // 2); fo = min(fo, (j - i0) // 2)
    if fi: e[i0:i0 + fi] = np.sin(np.linspace(0, np.pi / 2, fi))
    if fo: e[j - fo:j] *= np.cos(np.linspace(0, np.pi / 2, fo))
    return e
def speech_gate(nar, N):
    """0..1: 1 while the voice speaks (smoothed, ~0.4 s release) - the sidechain for music, ambience and things."""
    fr = 441; nf = N // fr; vr_ = np.sqrt((nar[:nf * fr].reshape(nf, fr) ** 2).mean(1)); act = (vr_ > .02).astype(float)
    gate = np.clip(np.convolve(act, np.ones(25) / 25, 'same') * 3, 0, 1); gate = np.convolve(gate, np.ones(15) / 15, 'same')
    return np.interp(np.arange(N) / SR, (np.arange(nf) + .5) * fr / SR, gate)
def dedupe(events):
    out = []
    for e in sorted(events, key=lambda q: (q['cue'], q['t'])):
        if out and out[-1]['cue'] == e['cue'] and abs(out[-1]['t'] - e['t']) < .015 and e['cue'] != 'duck':
            out[-1]['gain'] = max(out[-1].get('gain', 1.0), e.get('gain', 1.0)); continue
        out.append(dict(e))
    return sorted(out, key=lambda q: q['t'])
LOW = {'click', 'tick', 'tok', 'swoosh', 'swoosh_rope', 'ding', 'ding_hi', 'ding_low', 'shimmer', 'thud_soft'}
def thin(events, gap=1.0, win=6.0, max_low=1):
    """Density limiter (GOLD rule 100: ~16 SFX/min in bursts). Small graphic cues (LOW) are dropped when another sound already
    plays within `gap` s before them, or when `max_low` small cues were kept in the last `win` s. Real recordings, mood, beds,
    count-up trains and stings are never dropped."""
    out = []; kept = []; low = []
    for e in sorted(events, key=lambda q: q['t']):
        c = e['cue']
        if c == 'duck' or c.startswith('env:') or c not in LOW:
            out.append(e)
            if c != 'duck' and not c.startswith('env:'): kept.append(e['t'])
            continue
        t = e['t']
        if any(0 <= t - k < gap for k in kept[-6:]) or sum(1 for k in low if t - k < win) >= max_low: continue
        out.append(e); kept.append(t); low.append(t)
    return out
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('work'); ap.add_argument('--voice'); ap.add_argument('--offset', type=float)
    ap.add_argument('--music', help='ONE music file (wav/mp3). Swap it to change the music; nothing else needs to change')
    ap.add_argument('--music-db', type=float, default=-19.0, help='music level under speech, dB below the voice rms (default -19)')
    ap.add_argument('--music-gap-db', type=float, default=-12.0, help='music level between sentences (default -12)')
    ap.add_argument('--music-start', type=float, default=0.0, help='chapter second where the music file starts (default 0)')
    ap.add_argument('--music-offset', type=float, default=0.0, help='seconds INTO the music file where this chapter begins (one long continuous bed is sliced per chapter, so chapters join with no seam)')
    ap.add_argument('--music-lift', help='"T,DB": from chapter second T the music is lifted by DB (1 s ramp), e.g. the music-only end screen')
    ap.add_argument('--music-fade-in', type=float, default=0.7); ap.add_argument('--music-fade-out', type=float, default=0.0)
    ap.add_argument('--el-dir', default=EL_DIR, help='sound library for el:/env: cues (default videos/video02/sfx_el; templates/tests_anim/sfx_el is the fallback)')
    ap.add_argument('--amb-db', type=float, default=-22.0, help='environment bed under speech, dB re the voice rms (default -22: 8 dB under the music bed)')
    ap.add_argument('--amb-gap-db', type=float, default=-14.0, help='environment bed in voice pauses (default -14)')
    ap.add_argument('--sfx-db', type=float, default=6.0, help='graphic/mood synth cues: a gain-1 cue peaks this many dB re the voice rms (default +6, close to the old per-chapter scaling)')
    ap.add_argument('--things-db', type=float, default=2.0, help='el: recordings: a gain-1 sound peaks this many dB re the voice rms (default +2), 3 dB less under speech')
    ap.add_argument('--no-thin', action='store_true', help='keep every small graphic cue (default: thin() limits the density)')
    ap.add_argument('--stems', action='store_true', help='also write audio/stem_voice.wav and audio/stem_sd.wav (level checks)')
    a = ap.parse_args()
    ev = json.load(open(os.path.join(a.work, 'sfx_events.json'))); dur = ev['duration']; N = int(SR * (dur + .5))
    off = a.offset if a.offset is not None else ev.get('audio_offset', 0.0)
    out = os.path.join(a.work, 'audio'); os.makedirs(out, exist_ok=True)
    sfx = np.zeros(N); amb = np.zeros(N); thg = np.zeros(N); envb = np.zeros(N)
    events = dedupe(ev['events'])
    if not a.no_thin: events = thin(events)
    ducks = [(e['t'], e.get('dur', 1.0)) for e in events if e['cue'] == 'duck']
    for e in events:
        cue = e['cue']; g = e.get('gain', 1.0); d = e.get('dur'); i = int(e['t'] * SR)
        if not 0 <= i < N: continue
        if cue.startswith('env:'):
            x = el_load(cue[4:], a.el_dir)
            if x is None: print('unknown sound', cue); continue
            L = int((d or (dur - e['t'])) * SR); edge = lambda at: int((.3 if at else 1.5) * SR)
            y = el_loop(x, L / SR, seed=zlib.crc32(f"{cue}{e['t']}".encode()))
            envb += np.pad(y, (i, max(0, N - i - len(y))))[:N] * env_curve(N, i, len(y), edge(e['t'] < .05), edge(e['t'] + L / SR > dur - .05)) * g
            continue
        if cue.startswith('el:'):
            x = el_load(cue[3:], a.el_dir)
            if x is None: print('unknown sound', cue); continue
            V.put(thg, el_thing(x, d), e['t'], g); continue
        if cue not in CUES: print('unknown cue', cue); continue
        sig = CUES[cue](d); tgt = amb if cue in AMB_LEGACY else sfx
        j = min(N, i + len(sig)); tgt[i:j] += sig[:j - i] * g * (1.0 if tgt is sfx else .4)
    if not a.voice:
        b = sfx + amb + thg + envb * .2; write(os.path.join(out, 'sfx_bed.wav'), b / (np.max(np.abs(b)) + 1e-9) * .8); print('sfx_bed.wav written (no voice given)'); return
    tmp = os.path.join(out, 'voice.wav'); inserts = ev.get('inserts', []); LI = sum(x['dur'] for x in inserts)
    AF = 'highpass=f=70,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=3,equalizer=f=3500:t=q:w=1:g=1.5'
    def load(src, ss=None, t=None):
        cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + (['-ss', f'{ss:.3f}'] if ss is not None else []) + (['-t', f'{t:.3f}'] if t else []) + ['-i', src, '-ac', '1', '-ar', str(SR), '-af', AF, tmp]
        subprocess.run(cmd, check=True)
        with wave.open(tmp) as w: return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    v = load(a.voice, off, dur - LI)
    if inserts:   # splice the extra recorded lines into the narration slice (cut points are narration seconds), short fades, level matched to the voice before the cut
        fd = int(.012 * SR); pieces = []; pos = 0
        for x in sorted(inserts, key=lambda q: q['cut']):
            c = int((x['cut'] - off) * SR); ins = load(x['audio']); seg = v[pos:c].copy()
            ref = v[max(0, c - 5 * SR):c]; rr = np.sqrt(np.mean(ref[np.abs(ref) > .02] ** 2)) if np.any(np.abs(ref) > .02) else 0; ri = np.sqrt(np.mean(ins[np.abs(ins) > .02] ** 2)) if np.any(np.abs(ins) > .02) else 0
            if rr and ri: ins = ins * float(np.clip(rr / ri, .6, 1.6))
            if len(seg) > fd: seg[-fd:] *= np.linspace(1, 0, fd)
            if len(ins) > 2 * fd: ins[:fd] *= np.linspace(0, 1, fd); ins[-fd:] *= np.linspace(1, 0, fd)
            pieces += [seg, ins]; pos = c
            tail = v[c:c + fd]; tail *= np.linspace(0, 1, len(tail)) if len(tail) else 1
        v = np.concatenate(pieces + [v[pos:]])
    nar = np.zeros(N); nar[:min(N, len(v))] = v[:N]
    vr = np.sqrt(np.mean(nar[np.abs(nar) > .02] ** 2)) if np.any(np.abs(nar) > .02) else .1
    rms = lambda x: np.sqrt(np.mean(x[x != 0] ** 2)) + 1e-9
    db = lambda x: 10 ** (x / 20)
    gate = speech_gate(nar, N); tt_ = np.arange(N) / SR
    dip = np.ones(N)   # verdict sting: music out over 0.15 s, back in over 0.6 s after dd seconds
    for (dt, dd) in ducks: dip *= 1 - np.clip(np.minimum((tt_ - dt) / .15, (dt + dd + .6 - tt_) / .6), 0, 1) * .97
    # graphics + mood synth: fixed level re the voice (gain-1 cue peaks a.sfx_db re voice rms); legacy synth ambience as before
    sd = sfx * vr * db(a.sfx_db) + (amb / rms(amb) * vr * db(-24) if amb.any() else 0)
    # things: recordings, 3 dB lower while the voice speaks
    sd = sd + thg * vr * db(a.things_db) * (1 - gate * (1 - db(-3)))
    # environment: under the music, ducked by the voice (sidechain), a little up in pauses; dips 6 dB under a verdict sting
    if envb.any():
        envg = db(a.amb_db) * gate + db(a.amb_gap_db) * (1 - gate)
        sd = sd + envb * vr * envg * (1 - (1 - dip) * .5)
    mus = np.zeros(N)
    if a.music:
        # ONE music file = the whole music input (swap the file, re-run this script, nothing else changes).
        # It is levelled against the voice (a.music_db under the voice rms), ducked on speech (a.music_gap_db between sentences),
        # faded in over a.music_fade_in and out over a.music_fade_out.
        m = os.path.join(out, 'music.wav'); subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{a.music_offset:.3f}', '-i', a.music, '-ac', '1', '-ar', str(SR), '-t', f'{dur + .5 - a.music_start:.3f}', m], check=True)
        with wave.open(m) as w: mu = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        os.remove(m)
        mm = np.zeros(N); i0 = int(a.music_start * SR); k = min(N - i0, len(mu)); mm[i0:i0 + k] = mu[:k]
        env = db(a.music_gap_db) * (1 - gate) + db(a.music_db) * gate
        if a.music_lift:
            lt, ldb = [float(q) for q in a.music_lift.split(',')]; env *= 10 ** (ldb / 20 * np.clip(tt_ - lt, 0, 1))
        env *= dip
        fi = int(a.music_fade_in * SR); fo = int(a.music_fade_out * SR); end_i = int(dur * SR)
        if fi: env[i0:i0 + fi] *= np.linspace(0, 1, fi)
        if fo: env[end_i - fo:end_i] *= np.linspace(1, 0, fo)
        mus = mm / rms(mm[mm != 0] if np.any(mm) else mm) * vr * env
    sd = sd + mus
    end = int(dur * SR); mix = nar[:end] + sd[:end]; pk = np.max(np.abs(mix)) + 1e-9
    if os.path.exists(tmp): os.remove(tmp)
    if a.stems:
        write(os.path.join(out, 'stem_voice.wav'), nar[:end] / pk * .8); write(os.path.join(out, 'stem_sd.wav'), sd[:end] / pk * .8)
        np.save(os.path.join(out, 'stem_gate.npy'), gate[:end:441].astype(np.float32))
    write(os.path.join(out, 'mix_raw.wav'), mix / pk * .8); print('mix_raw.wav written', round(dur, 1), 's')
if __name__ == '__main__': main()
