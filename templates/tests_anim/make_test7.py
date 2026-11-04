#!/usr/bin/env python3
"""Test 7: the three scenes (test 4 rich hook, test 2 gauge, test 3 options) with VOICE-OVER (ElevenLabs v4 "Will")
and full SOUND DESIGN in three stems: AMB (environment + mood bed), SFX (things + graphic sounds), VOICE.
AMB ducks under the voice (sidechain), final loudness -14 LUFS.
  python3 make_test7.py   -> out/test7_voice_sound.mp4"""
import os, sys, json, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TPL = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, TPL)
import make_tests as M, make_test4 as T4
import sfx_voices as V
SR = V.SR
SC = [('test4_rich_lockon', 12.0), ('test2_gauge', 9.0), ('test3_options', 10.0)]
OFF = [0.0, 12.0, 21.0]; TOT = 31.0
OUT = os.path.join(HERE, 'out'); TMP = os.path.join(HERE, 'work', 't7'); os.makedirs(TMP, exist_ok=True)

# voice line -> (scene, local time)
VO = [('L1', 0, .15), ('L2', 0, 2.65), ('L3', 0, 5.1), ('L4', 0, 6.6),
      ('L5', 1, .7), ('L7', 1, 5.0),
      ('L8', 2, .25), ('L9', 2, 2.2), ('L10', 2, 4.0), ('L11', 2, 8.6)]
HB = [6.6, 7.5, 8.25, 8.85, 9.35, 9.8, 10.2]
AMB = [  # environment + mood
    ('el:jungle_bed', 0, 0, .9, 12), ('drone', 0, 0, .4, 12),
    ('el:jungle_bed', 1, 0, .25, 9), ('drone', 1, 0, .55, 9),
    ('drone', 2, 0, .5, 10), ('el:jungle_bed', 2, 3.1, .55, 4.6)]
SFX = [  # things + graphic sounds
    ('el:footsteps_wet', 0, .3, .55), ('el:torch_click', 0, .55, .7), ('el:leaves_rustle', 0, 3.0, .8), ('el:tiger_chuff', 0, 3.45, .9),
    ('ticks', 0, 4.2, .25, 1.9), ('beep', 0, 6.1, .35), ('el:tiger_growl', 0, 7.7, 1.0), ('el:sub_boom', 0, 7.85, .9), ('thud', 0, 9.75, .4)]
SFX += [('heart', 0, t, .8) for t in HB]
SFX += [('swoosh', 1, .9, .3), ('ticks', 1, 1.3, .35, .7), ('swoosh', 1, 2.6, .3), ('ticks_up', 1, 3.1, .45, 1.5), ('el:sub_boom', 1, 4.6, .8),
        ('shimmer', 1, 4.6, .3), ('el:tiger_growl', 1, 4.75, .35), ('marker', 1, 5.5, .5)]
SFX += [('click', 2, .9, .5), ('click', 2, 1.28, .5), ('click', 2, 1.66, .5), ('tok', 2, 2.3, .6), ('swoosh', 2, 3.1, .35),
        ('el:footsteps_wet', 2, 3.7, .25), ('el:tiger_growl', 2, 4.3, .45), ('swoosh', 2, 5.55, .5), ('el:birds_flap', 2, 5.75, .7),
        ('el:branch_creak', 2, 5.95, .8), ('thud', 2, 5.98, .45), ('swoosh', 2, 7.7, .3), ('scratch', 2, 8.25, .7), ('tok', 2, 8.65, .5)]

def load(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768

def sig(cue, d):
    if cue.startswith('el:'):
        x = T4.load_el(cue[3:]); x = x / (np.max(np.abs(x)) + 1e-9)
        if d:
            x = x[:int(d * SR)].copy(); f = min(len(x) // 3, int(.8 * SR)); x[-f:] *= np.linspace(1, 0, f); x[:int(.4 * SR)] *= np.linspace(0, 1, int(.4 * SR))
        return x
    if cue == 'heart': return T4.heart()
    return M.CUE[cue](d if d else 9.0)

def stem(events, name):
    buf = np.zeros(int((TOT + 1) * SR))
    for e in events:
        cue, sc, t, g = e[:4]; d = e[4] if len(e) > 4 else None
        V.put(buf, sig(cue, d), OFF[sc] + t, g)
    buf = buf[:int(TOT * SR)]
    p = os.path.join(TMP, name + '.wav')
    with wave.open(p, 'wb') as w:
        b = buf / max(1.0, np.max(np.abs(buf)) / .95)
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((b * 32767).astype('<i2').tobytes())
    return p

def main():
    amb = stem(AMB, 'amb'); sfx = stem(SFX, 'sfx')
    vbuf = np.zeros(int((TOT + 1) * SR))
    for k, sc, t in VO: V.put(vbuf, load(os.path.join(HERE, 'vo', k + '.mp3')), OFF[sc] + t, 1.0)
    vp = os.path.join(TMP, 'voice.wav')
    with wave.open(vp, 'wb') as w:
        b = vbuf[:int(TOT * SR)]; b = b / (np.max(np.abs(b)) + 1e-9) * .95
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((b * 32767).astype('<i2').tobytes())
    # picture: the three rendered scenes, audio dropped
    lst = os.path.join(TMP, 'v.txt'); open(lst, 'w').write(''.join(f"file '{os.path.join(OUT, n)}.mp4'\n" for n, _ in SC))
    vid = os.path.join(TMP, 'video.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-an', '-c:v', 'copy', vid], check=True)
    # mix: voice -16 LUFS; ambience ~-31 LUFS and ducked by the voice; sfx peaks ~-9 dBFS; then -14 LUFS
    fc = ('[0:a]loudnorm=I=-16:TP=-2:LRA=11,asplit=2[v][vk];'
          '[1:a]loudnorm=I=-27:TP=-7:LRA=15[a0];[a0][vk]sidechaincompress=threshold=0.05:ratio=3:attack=20:release=400:makeup=1[a];'
          '[2:a]volume=-4dB[s];[v][a][s]amix=inputs=3:normalize=0,alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=11[m]')
    out = os.path.join(OUT, 'test7_voice_sound.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', vp, '-i', amb, '-i', sfx, '-i', vid, '-filter_complex', fc,
                    '-map', '3:v', '-map', '[m]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', '-shortest', out], check=True)
    print('wrote', out)

if __name__ == '__main__': main()
