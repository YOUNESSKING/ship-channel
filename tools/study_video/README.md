# study_video: study a competitor video (transcript, frames, sound design)

Study only: downloaded media is git-ignored and never used in our videos (owner rule, 30 Oct 2026).

## A. From any session, including the cloud (no download): `gemini_watch.py`
Google Gemini watches and listens to the public YouTube video itself.
Needs a free key from https://aistudio.google.com/apikey saved as the environment variable `GEMINI_API_KEY`
(cloud: environment settings, then a new session; never paste it in chat or commit it).
```
python3 tools/study_video/gemini_watch.py URL --ask sound  --start 0 --end 180   # sound design map
python3 tools/study_video/gemini_watch.py URL --ask design --start 0 --end 180   # shots, graphics, editing
python3 tools/study_video/gemini_watch.py URL --ask hook                          # first 60 s
python3 tools/study_video/gemini_watch.py URL --ask full                          # structure, every animal and place
```
Output: `research/video_study/<id>/gemini_*.md`. Free tier is rate-limited; one call at a time.

## B. On the owner's own computer (YouTube blocks yt-dlp on cloud machines): `study_video.py`
Install once: `pip install -U yt-dlp faster-whisper numpy matplotlib` and ffmpeg (optional: `pip install demucs` for `--stems`).
```
python3 tools/study_video/study_video.py URL [URL ...] --minutes 3 [--stems]
```
Output in `research/video_study/<id>/`: transcript (captions, else local Whisper, free), 1 fps frames + contact sheets,
scene cuts, `sound/loudness.csv`, `sound/events.csv` (deep hits, silences/drops, risers), `sound/sound_map.png`
(loudness with cuts, hits, silences, risers and the spoken words on one timeline), `REPORT.md` (cuts/min, hits/min, LUFS).
Hit detection only counts bass-heavy booms (tested: a voice-only track gives ~5 false hits/min; check by ear).
Then commit and push the folder (media files stay out via .gitignore) so the cloud session can read the results.
