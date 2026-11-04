"""'Frontlines' restoration pass for archival film clips (test for the owner, 2026-10).

usage: python3 tools/restore_film.py IN.mp4 OUT.mp4 [--tint]
- fills 16:9 (crops the black bars the clips were padded with, then crops 4:3 film top/bottom)
- vidstab stabilisation (2 passes), deflicker, temporal + spatial denoise (no motion interpolation: it smeared fast shots in the test),
  gentle sharpening, a contrast curve with lifted blacks (clean "restored" look, not crushed)
- --tint: a restrained period colour grade (warm highlights, olive-teal shadows). NOT colourisation: the AI colourisers
  tested (DDColor) gave false colours (red helmets, blue tanks), so real colours are not attempted.
"""
import os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from archive_shots import film_crop  # noqa: E402


def restore(src, out, tint=False, W=1920, H=1080):
    c = film_crop(src)
    fill = ([f"crop={c}"] if c else []) + [f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={W}:{H}"]
    trf = tempfile.mktemp(suffix=".trf")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", ",".join(fill + [f"vidstabdetect=shakiness=6:accuracy=12:result={trf}"]),
                    "-f", "null", "-"], check=True)
    vf = fill + [f"vidstabtransform=input={trf}:smoothing=18:zoom=3:optzoom=0", "deflicker=size=7:mode=pm",
                 "hqdn3d=3:2:7:6",
                 "unsharp=5:5:0.7:5:5:0.0", "curves=all='0/0.05 0.25/0.22 0.5/0.52 0.75/0.8 1/0.97'"]
    if tint:
        vf += ["format=rgb24", "colorbalance=rs=-0.05:gs=0.02:bs=-0.03:rm=0.04:gm=0.01:bm=-0.04:rh=0.08:gh=0.04:bh=-0.06",
               "eq=saturation=1.0:gamma=1.0"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", ",".join(vf), "-r", "30", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "18", "-pix_fmt", "yuv420p", "-an", out], check=True)
    os.remove(trf)


if __name__ == "__main__":
    restore(sys.argv[1], sys.argv[2], tint="--tint" in sys.argv)
