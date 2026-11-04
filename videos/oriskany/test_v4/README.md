# Oriskany test v4 (HOOK_v1, 50.2 s)

Build order (all paths relative to this folder):
1. `python3 build/voice.py` (Kokoro am_michael 0.95, question block 0.88, Oriskany phoneme fix) -> audio/voice.wav, build/words.json, build/chunks.json
2. `ARCHIVE_GRADE=ship python3 build/films.py && ARCHIVE_GRADE=ship python3 build/shots.py` -> segments/ (graded film + photo shots)
3. maps: `cd mk && python3 tools/build_scene.py dive gulf_pan dive dive` (and gulfpin, endmap pan_close), render each scene with `npx hyperframes render`, copy to segments/
4. hero: `cd hero && npx hyperframes render . -o renders/hero.mp4`, split at 3.6 s into segments/hero_a.mp4 + hero_b.mp4
5. `cd ../../../templates && GRADE=none python3 build_chapter.py ../videos/oriskany/test_v4/chapter/c01.json`, `node templates/check_safe_text.js` (must PASS), render chapter/work/c01 -> chapter/render_c01.mp4
6. `python3 build/mix.py` -> oriskany_test_v4.mp4 (fails if the sound lock breaks)
7. `python3 ../../../tools/film/make_paperwork.py .` -> MANIFEST.md, CREDITS.md
Reports: SOUND_REPORT.md, CHANGES.md, contact_sheet.jpg.
