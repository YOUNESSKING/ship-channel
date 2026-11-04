"""Measure a finished mix (mix_clip.py v2 output) -> WORK/measure.json, used by check_sound_lock.py --render and
the SOUND_REPORT. Everything is measured, nothing assumed:
  * integrated / TP / LRA of the encoded master (ffmpeg ebur128);
  * BS.1770 K-weighted momentary loudness (400 ms, 50 ms hop) of the master and of every stem at master scale;
  * speech reference = median master momentary over windows inside words that touch no SFX cue;
  * big beats (explosion / impact / boom cues) = master momentary max in [event - 0.1, event + 0.6] minus that reference;
  * music under voice = median music-stem M minus median voice-stem M, both inside words (exact, from the stems);
    music in gaps = median music-stem M >= 0.25 s from any word, re the voice-in-speech median;
  * battle-maps comparison: the same blind estimator on the master and on the reference mixes (50 ms RMS, 30th
    percentile of the gap frames re the speech median; words from faster-whisper, cached), since the reference has
    no stems;
  * spectral balance of the master (< 120 Hz, 120-300, 300-3000, 3-8k, > 8k re total) and the bus limiter load.
usage: measure_mix.py --out OUT.mp4 --work WORK --words words.json --cues placed.json [--ref DIR]"""
import argparse, glob, json, os, re, subprocess, sys
import numpy as np, soundfile as sf
from scipy.signal import lfilter

SR = 48000
HOP, WIN = 0.05, 0.4
# BS.1770-4 K-weighting at 48 kHz
KB1, KA1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
KB2, KA2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]


def read48(p, tmpdir):
    if p.endswith(".wav"):
        a, sr = sf.read(p, dtype="float64", always_2d=True)
        if sr == SR: return a
    t = os.path.join(tmpdir, "_dec_" + os.path.basename(p) + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-vn", "-ac", "2", "-ar", str(SR), "-c:a", "pcm_f32le", t], check=True)
    a, _ = sf.read(t, dtype="float64", always_2d=True); os.remove(t); return a


def momentary(a):
    k = lfilter(KB2, KA2, lfilter(KB1, KA1, a, axis=0), axis=0)
    p = (k ** 2).sum(axis=1)
    c = np.concatenate([[0.0], np.cumsum(p)]); w, h = int(WIN * SR), int(HOP * SR)
    n = max(0, (len(p) - w) // h + 1); i = np.arange(n) * h
    return -0.691 + 10 * np.log10((c[i + w] - c[i]) / w + 1e-12)        # window i = [i*HOP, i*HOP + 0.4]


def ebur(p):
    s = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    s = s[s.rindex("Summary:"):]
    g = lambda k: float(re.search(k + r":\s+(-?[\d.]+)", s).group(1))
    return {"I": g("I"), "LRA": g("LRA"), "TP": g("Peak")}


def masks(words, n, cues=()):
    centre = np.arange(n) * HOP + WIN / 2
    inword = np.zeros(n, bool); near = np.zeros(n, bool); clean = np.ones(n, bool)
    for w in words:
        inword |= (centre >= w["start"]) & (centre <= w["end"])
        near |= (centre >= w["start"] - 0.25) & (centre <= w["end"] + 0.25)
    lo, hi = np.arange(n) * HOP, np.arange(n) * HOP + WIN
    for c in cues:
        clean &= ~((lo < c["end"]) & (hi > c["start"]))
    span = (centre > words[0]["start"]) & (centre < words[-1]["end"])
    return inword, ~near & span, clean


def blind_gap_estimate(a, words):
    m = a.mean(axis=1); h = int(HOP * SR); n = len(m) // h
    r = 10 * np.log10((m[: n * h].reshape(n, h) ** 2).mean(1) + 1e-12)
    t = np.arange(n) * HOP + HOP / 2
    sp = np.zeros(n, bool); near = np.zeros(n, bool)
    for w in words:
        sp |= (t >= w["start"]) & (t <= w["end"]); near |= (t >= w["start"] - 0.25) & (t <= w["end"] + 0.25)
    gap = ~near & (t > words[0]["start"]) & (t < words[-1]["end"])
    return float(np.percentile(r[gap], 30) - np.median(r[sp]))


def whisper_words(wav, cache):
    if os.path.exists(cache): return json.load(open(cache))
    from faster_whisper import WhisperModel
    a, _ = sf.read(wav, dtype="float32", always_2d=True); a = a.mean(1)[::3].copy()   # 48k -> 16k
    m = WhisperModel("base.en", device="cpu", compute_type="int8")
    W = [{"w": w.word, "start": w.start, "end": w.end} for s in m.transcribe(a, language="en", word_timestamps=True,
                                                                              beam_size=5)[0] for w in s.words]
    json.dump(W, open(cache, "w")); return W


def bands(a):
    m = a.mean(axis=1); F = np.abs(np.fft.rfft(m)) ** 2; f = np.fft.rfftfreq(len(m), 1 / SR); T = F.sum()
    db = lambda lo, hi: round(10 * np.log10(F[(f >= lo) & (f < hi)].sum() / T), 1)
    return {"<120": db(0, 120), "120-300": db(120, 300), "300-3k": db(300, 3000), "3-8k": db(3000, 8000), ">8k": db(8000, 24000)}


def main():
    ap = argparse.ArgumentParser()
    for k in ("out", "work", "words", "cues"): ap.add_argument("--" + k, required=True)
    ap.add_argument("--ref")
    A = ap.parse_args(); W = A.work
    words = json.load(open(A.words)); words = words["words"] if isinstance(words, dict) else words
    placed = json.load(open(A.cues))["cues"]; master = json.load(open(os.path.join(W, "master.json")))
    g = 10 ** (master["master_gain_db"] / 20)
    mst = read48(A.out, W); M = momentary(mst)
    inword, gap, clean = masks(words, len(M), placed)
    speech_ref = float(np.median(M[inword & clean]))
    beats = []
    for c in placed:
        if c["role"] in ("explosion", "impact", "boom"):
            i0, i1 = int(max(0, c["event"] - 0.1) / HOP), int((c["event"] + 0.6) / HOP)
            mm = float(M[i0:i1].max())
            beats.append({"t": c["event"], "role": c["role"], "what": c["note"], "momentary_max": round(mm, 1),
                          "above_speech_lu": round(mm - speech_ref, 1)})
    st = {k: momentary(read48(os.path.join(W, k + ".wav"), W) * g) for k in ("voice_bus", "music_bus", "sfx_bus", "beds_bus", "punch_bus")}
    n = min(len(M), *(len(v) for v in st.values())); vo, mu = st["voice_bus"][:n], st["music_bus"][:n]
    iw, gp = inword[:n], gap[:n]
    voice_sp = float(np.median(vo[iw])); mus_sp = float(np.median(mu[iw])); mus_gap = float(np.median(mu[gp]))
    sd = 10 * np.log10(10 ** (st["sfx_bus"][:n] / 10) + 10 ** (st["beds_bus"][:n] / 10) + 10 ** (st["punch_bus"][:n] / 10) + 10 ** (mu / 10))
    stem_sum = sum(read48(os.path.join(W, k + ".wav"), W) for k in ("voice_bus", "music_bus", "sfx_bus", "beds_bus", "punch_bus"))
    bus_pk = float(np.abs(stem_sum).max())
    fin = ebur(A.out)
    res = {"integrated": fin["I"], "true_peak": fin["TP"], "lra": fin["LRA"],
           "speech_momentary_median": round(speech_ref, 1),
           "speech_momentary_p95": round(float(np.percentile(M[inword & clean], 95)), 1),
           "beats": beats,
           "voice_in_speech_M": round(voice_sp, 1), "music_in_speech_M": round(mus_sp, 1),
           "music_under_voice_db": round(mus_sp - voice_sp, 1), "music_in_gaps_db": round(mus_gap - voice_sp, 1),
           "music_duck_db": round(mus_gap - mus_sp, 1),
           "sound_design_under_voice_db": round(float(np.median(sd[iw])) - voice_sp, 1),
           "sound_design_floor_gaps_M": round(float(np.percentile(sd[gp], 10)), 1),
           "bus_peak_before_limiter_dbfs": round(20 * np.log10(bus_pk), 1), "bands_re_total_db": bands(mst),
           "blind_gap_re_speech_db": round(blind_gap_estimate(mst, words), 1),
           "cues": [{k: c[k] for k in ("event", "role", "file", "start", "end", "measured", "offset_frames", "note")} for c in placed]}
    if A.ref and os.path.isdir(A.ref):
        refs = {}
        cache = os.path.join(W, "ref"); os.makedirs(cache, exist_ok=True)
        for f in ("style-reference-rokossovsky-v8.mp4", "hook-reference-rokossovsky-v2.mp4", "hook-reference-meade-v3.mp4"):
            p = os.path.join(A.ref, f)
            if not os.path.exists(p): continue
            wav = os.path.join(cache, f[:-4] + ".wav")
            if not os.path.exists(wav):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-vn", "-ac", "2", "-ar", str(SR), wav], check=True)
            a = read48(wav, cache); rw = whisper_words(wav, wav[:-4] + ".words.json")
            e = ebur(wav)
            refs[f] = {"blind_gap_re_speech_db": round(blind_gap_estimate(a, rw), 1), "I": e["I"], "LRA": e["LRA"], "TP": e["TP"]}
        if refs:
            mean = float(np.mean([v["blind_gap_re_speech_db"] for v in refs.values()]))
            res.update({"reference": refs, "ref_gap_mean_db": round(mean, 1),
                        "ref_gap_delta_db": round(res["blind_gap_re_speech_db"] - mean, 1)})
    json.dump(res, open(os.path.join(W, "measure.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k not in ("cues",)}, indent=1))


if __name__ == "__main__":
    main()
