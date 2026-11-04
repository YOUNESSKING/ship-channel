"""Final mix + master + mux v2 (battle-maps STYLE_LOCK sections 5 + 2c-9, with the critic fixes of
videos/oriskany/test_v3/CRITIQUE_SOUND_ACCURACY.md). Every video uses this.

1. VOICE STEM before the mix: 5 ms fade-in / 10 ms fade-out on every TTS chunk edge (chunks.json), high-pass 80 Hz,
   -2 dB at 160 Hz (Kokoro is chesty), gentle de-ess, gain to VOICE_LUFS, compressor 2.5:1 at -24 dB (5 / 80 ms),
   limiter at -9 dBFS (VOICE_CEIL), padded to the video length, centred in stereo.
2. MIX (locked section 5): music at MUSIC_VOL 0.08 (2 s in / 3 s out) ducked under the voice (sidechain 0.03 / 6 /
   20 / 400); SFX at FULL level ducked lightly (0.03 / 3 / 10 / 300); beds (projector, drone, waves, underwater)
   ducked like the SFX. Music and beds high-passed at BED_HPF Hz, SFX at 35 Hz. amix (stereo), bus limiter 0.5,
   0.6 s fade-out on the last 0.6 s (the video's fade).
3. MASTER (2c-9): measure I, ONE linear gain + alimiter (MASTER_LIMIT, 0.84 first) to -14 LUFS, then the two-pass
   loudnorm I=-14 / TP=-1.5 / LRA=11 linear=true with the measured_* values. The build FAILS if loudnorm reports
   normalization_type != linear, if the predicted TP (input_tp + offset) is above -1.5, or if the encoded AAC 192k
   master is outside -14 +/- 0.5 LUFS or above -1.5 dBTP. The limiter is lowered in steps (0.84 -> 0.76) until the
   encoded master meets TP <= -1.5.
Writes OUT.mp4 (video stream copied, stereo AAC 192k, audio = video length) and WORK/{mix,voice_bus,music_bus,
sfx_bus,beds_bus}.wav + WORK/master.json (every number, for measure_mix.py / check_sound_lock.py).

usage: python3 mix_clip.py --video V.mp4 --voice voice.wav --chunks chunks.json --sfx sfx.wav --music bed.wav
                           [--beds beds.wav] --out OUT.mp4 --work DIR
"""
import argparse, json, os, re, subprocess, sys
import numpy as np, soundfile as sf

MUSIC_VOL = 0.08
MUSIC_TRIM_DB = 0.0    # calibrated against the battle-maps reference (see measure_mix.py / SOUND_REPORT_v2.md)
VOICE_LUFS = -23.0
VOICE_CEIL = "-9dB"
BED_HPF = 70
MASTER_LIMITS = (0.84, 0.82, 0.80, 0.78, 0.76)
TARGET_I, TARGET_TP = -14.0, -1.5
LN = "loudnorm=I=-14:TP=-1.5:LRA=11"
SR = 48000


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg failed: {' '.join(cmd)[:300]}\n{r.stderr[-2000:]}")
    return r.stderr


def ebur(p):
    s = run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"])
    s = s[s.rindex("Summary:"):]
    g = lambda k: float(re.search(k + r":\s+(-?[\d.]+|-inf)", s).group(1).replace("-inf", "-99"))
    return {"I": g("I"), "LRA": g("LRA"), "TP": g("Peak")}


def loudnorm_json(p, af):
    s = run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", af, "-f", "null", "-"])
    return json.loads(s[s.rindex("{"): s.rindex("}") + 1])


def prep_voice(voice, chunks, out):
    a, sr = sf.read(voice, dtype="float32")
    if a.ndim > 1: a = a.mean(axis=1)
    fi, fo = int(0.005 * sr), int(0.010 * sr)
    for c in json.load(open(chunks))["chunks"]:
        i0, i1 = int(round(c["start"] * sr)), int(round(c["end"] * sr))
        a[i0:i0 + fi] *= np.linspace(0, 1, fi); a[max(i0, i1 - fo):i1] *= np.linspace(1, 0, i1 - max(i0, i1 - fo))
    tmp = out + ".24k.wav"; sf.write(tmp, a, sr, subtype="FLOAT")
    run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "aresample=48000:resampler=soxr", "-c:a", "pcm_f32le", out])
    os.remove(tmp)


def main():
    ap = argparse.ArgumentParser()
    for k in ("video", "voice", "chunks", "sfx", "music", "out", "work"): ap.add_argument("--" + k, required=True)
    ap.add_argument("--beds")
    A = ap.parse_args(); W = A.work; os.makedirs(W, exist_ok=True)
    total = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration",
                                  "-of", "csv=p=0", A.video], capture_output=True, text=True).stdout)   # audio = video length
    vp = os.path.join(W, "voice_prep.wav"); prep_voice(A.voice, A.chunks, vp)
    vg = VOICE_LUFS - ebur(vp)["I"]
    voice_chain = (f"highpass=f=80,equalizer=f=160:t=q:w=1:g=-2,deesser=i=0.25:m=0.5:f=0.5:s=o,volume={vg:.2f}dB,"
                   f"acompressor=threshold=-24dB:ratio=2.5:attack=5:release=80:makeup=1,"
                   f"alimiter=limit={VOICE_CEIL}:attack=2:release=40:level=disabled,apad=whole_dur={total:.3f},"
                   f"atrim=0:{total:.3f},pan=stereo|c0=c0|c1=c0")
    beds = A.beds or os.path.join(W, "_silence.wav")
    if not A.beds: sf.write(beds, np.zeros((int(total * SR), 2), "float32"), SR, subtype="FLOAT")
    mus_gain = MUSIC_VOL * 10 ** (MUSIC_TRIM_DB / 20)
    f = [f"[0:a]{voice_chain},asplit=5[vo][k1][k2][k3][vs]",
         f"[1:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=35,apad=whole_dur={total:.3f},atrim=0:{total:.3f}[sfxin]",
         "[sfxin][k1]sidechaincompress=threshold=0.03:ratio=3:attack=10:release=300,asplit=2[sfx][ss]",
         f"[2:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f={BED_HPF},apad=whole_dur={total:.3f},atrim=0:{total:.3f},"
         f"volume={mus_gain:.4f},afade=t=in:d=2,afade=t=out:st={total - 3:.3f}:d=3[mus]",
         "[mus][k2]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400,asplit=2[musd][ms]",
         f"[3:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f={BED_HPF},apad=whole_dur={total:.3f},atrim=0:{total:.3f}[bd]",
         "[bd][k3]sidechaincompress=threshold=0.03:ratio=3:attack=10:release=300,asplit=2[bedd][bs]",
         f"[vo][musd][sfx][bedd]amix=inputs=4:normalize=0,alimiter=limit=0.5:level=false,afade=t=out:st={total - 0.6:.3f}:d=0.6,"
         "aformat=channel_layouts=stereo[aout]"]
    stems = {k: os.path.join(W, k + ".wav") for k in ("mix", "voice_bus", "music_bus", "sfx_bus", "beds_bus")}
    run(["ffmpeg", "-v", "error", "-y", "-i", vp, "-i", A.sfx, "-i", A.music, "-i", beds, "-filter_complex", ";".join(f),
         "-map", "[aout]", "-c:a", "pcm_f32le", stems["mix"], "-map", "[vs]", "-c:a", "pcm_f32le", stems["voice_bus"],
         "-map", "[ms]", "-c:a", "pcm_f32le", stems["music_bus"], "-map", "[ss]", "-c:a", "pcm_f32le", stems["sfx_bus"],
         "-map", "[bs]", "-c:a", "pcm_f32le", stems["beds_bus"]])
    I0 = ebur(stems["mix"])
    master = os.path.join(W, "master.wav"); rep = {"total": total, "voice_gain_db": round(vg, 2), "mix": I0, "tries": []}
    gain = TARGET_I - I0["I"]
    for lim in MASTER_LIMITS:
        for _ in range(3):   # gain + limiter -> measure -> one correction (the limiter takes a little loudness)
            run(["ffmpeg", "-v", "error", "-y", "-i", stems["mix"], "-af",
                 f"volume={gain:.2f}dB,alimiter=limit={lim}:level=disabled,aresample=48000", "-c:a", "pcm_f32le", master])
            m1 = loudnorm_json(master, LN + ":print_format=json")
            if abs(float(m1["input_i"]) - TARGET_I) <= 0.2: break
            gain += TARGET_I - float(m1["input_i"])
        offset = TARGET_I - float(m1["input_i"]); pred_tp = float(m1["input_tp"]) + offset
        af = (f"{LN}:measured_I={m1['input_i']}:measured_TP={m1['input_tp']}:measured_LRA={m1['input_lra']}"
              f":measured_thresh={m1['input_thresh']}:offset={m1['target_offset']}:linear=true:print_format=json")
        m2 = loudnorm_json(master, af)
        run(["ffmpeg", "-v", "error", "-y", "-i", A.video, "-i", master, "-af", af.replace(":print_format=json", "") + ",aresample=48000",
             "-map", "0:v:0", "-map", "1:a:0", "-t", f"{total:.3f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
             "-movflags", "+faststart", A.out])
        fin = ebur(A.out)
        rep["tries"].append({"limit": lim, "gain_db": round(gain, 2), "loudnorm_pass1": m1, "loudnorm_pass2": m2,
                             "predicted_tp": round(pred_tp, 2), "final": fin})
        if m2.get("normalization_type") != "linear":
            json.dump(rep, open(os.path.join(W, "master.json"), "w"), indent=1)
            sys.exit(f"LOUDNESS FAIL: loudnorm went {m2.get('normalization_type')} (pred TP {pred_tp:.2f}); build stopped")
        if fin["TP"] <= TARGET_TP and abs(fin["I"] - TARGET_I) <= 0.5:
            break
    else:
        json.dump(rep, open(os.path.join(W, "master.json"), "w"), indent=1)
        sys.exit(f"LOUDNESS FAIL: no limiter setting met -14 LUFS / TP <= -1.5 (last {fin})")
    p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,channels,duration",
                                   "-of", "json", A.out], capture_output=True, text=True).stdout)["streams"]
    rep.update({"master_gain_db": round(gain, 2), "master_limit": lim, "normalization_type": m2["normalization_type"],
                "final": fin, "streams": p, "chain": {"voice": voice_chain, "graph": f}})
    json.dump(rep, open(os.path.join(W, "master.json"), "w"), indent=1)
    print(f"wrote {A.out} {total:.2f} s | {fin['I']:.1f} LUFS, TP {fin['TP']:.1f} dBTP, LRA {fin['LRA']:.1f} LU | "
          f"gain {gain:+.2f} dB, alimiter {lim}, loudnorm {m2['normalization_type']}")


if __name__ == "__main__":
    main()
