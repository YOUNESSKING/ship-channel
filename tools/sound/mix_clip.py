"""Final mix + mux, the battle-maps locked chain (STYLE_LOCK section 5, assemble_full.py / make_clip.py):
voice + music at MUSIC_VOL 0.08 (2 s fade-in, 3 s fade-out) ducked under the voice (sidechain 0.03 / ratio 6 / 20 ms / 400 ms)
+ SFX at FULL level ducked lightly (0.03 / ratio 3 / 10 ms / 300 ms), amix, limiter 0.5, two-pass loudnorm -14 LUFS,
TP -1.5, LRA 11 (linear), AAC 192k.
usage: python3 mix_clip.py VIDEO.mp4 VOICE.wav SFX.wav MUSIC_BED.wav OUT.mp4 [MIX.wav]"""
import json, subprocess, sys
MUSIC_VOL = 0.08
video, voice, sfx, music, out = sys.argv[1:6]; mixwav = sys.argv[6] if len(sys.argv) > 6 else out[:-4] + "_mix.wav"
total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], capture_output=True, text=True).stdout)
f = ["[0:a]aresample=48000,asplit=3[vo][key][key2]",
     "[1:a]aresample=48000[sfxin]",
     "[sfxin][key2]sidechaincompress=threshold=0.03:ratio=3:attack=10:release=300[sfx]",
     f"[2:a]aresample=48000,atrim=0:{total},volume=0.08,afade=t=in:d=2,afade=t=out:st={total - 3}:d=3[mus]",
     "[mus][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[musd]",
     "[vo][musd][sfx]amix=inputs=3:normalize=0,alimiter=limit=0.5:level=false[aout]"]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", sfx, "-i", music, "-filter_complex", ";".join(f), "-map", "[aout]",
                "-t", f"{total:.2f}", "-c:a", "pcm_s16le", mixwav], check=True)
LN = "loudnorm=I=-14:TP=-1.5:LRA=11"
r = subprocess.run(["ffmpeg", "-nostats", "-i", mixwav, "-af", LN + ":print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
af = (f"{LN}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", mixwav, "-af", af, "-map", "0:v", "-map", "1:a",
                "-t", f"{total:.2f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
# STYLE_LOCK 2c-9 loudness recipe: the linear loudnorm can land under -14 (true-peak bound); measure, then ONE gain trim + limiter
def meas(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    s = r[r.rindex("Summary:"):]; I = float(s.split("I:")[1].split()[0]); tp = float(s.split("Peak:")[1].split()[0]); return I, tp
I, tp = meas(out)
if I < -14.4:
    tmp = out[:-4] + "_trim.mp4"
    g = -14.2 - I
    for k in range(4):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", f"volume={g:.2f}dB,alimiter=limit=0.82:level=disabled,aresample=48000", "-map", "0:v", "-map", "0:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp], check=True)
        I2, tp2 = meas(tmp)
        if I2 >= -14.4 or k == 2: break
        g += (-14.2 - I2)
    import os; os.replace(tmp, out); I, tp = I2, tp2
print("wrote", out, round(total, 2), "s", f"| {I:.1f} LUFS, TP {tp:.1f} dBTP")
