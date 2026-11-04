# Channel colour grade (owner choice, 27 Oct 2026): B "Deep Time"
Teal shadows, warm golden highlights, a bit more contrast, slightly richer colour. Makes Wan / Kling / vidIQ / stock clips look like one series and matches the gold-on-dark graphics. Subtle: no grain, blur or vignette (house rule: no film look).
- `deep_time.vf` is the ffmpeg filter. `build_chapter.py` applies it to every CLIP when it conforms media (maps, text, stick figures and stills are not graded; `map_clip` shots, including baked maps and crops, are skipped automatically).
- Turn off for a run: `GRADE=none`; per clip: `"clip": {"file": ..., "grade": false}`.
- Test sheet: before/after on 6 clips from 4 sources was approved by the owner (A Glacier / B Deep Time / C Field Journal; B chosen).
- Video 01 was re-rendered with the grade on 27 Oct 2026 (chapters via the builder; the v9 opening graded on its AI clip shots only, with ffmpeg `enable='between'` filters). In `render_chapters.py` a 1080p chapter with many clips (ch03, 32 clips) needs more RAM than `cpu3c` 8 vCPU: ffmpeg frame extraction was OOM-killed (exit 137); use `--flavor cpu3g`.
