# Oriskany test v2 (1-minute hook)

Owner feedback on v1: own music, engineered SFX, the repo animation engines instead of PIL drawings, wow shots first.

## Build order
1. `python3 build/voice.py` - Kokoro per phrase + faster-whisper word timings -> audio/voice.wav, build/words.json
2. Maps (map-kit, HyperFrames): `cd mk && python3 tools/bake_sea.py gulf_pan 29.95 -86.75 9 && SS=1 python3 tools/bake_sea.py pan_close 30.22 -86.85 11`,
   then `python3 tools/build_scene.py dive gulf_pan dive dive` / `endmap pan_close endmap endmap`, render each scene.
3. Hero (kit ShipSink + ruler): `cd hero && hyperframes render . -o renders/hero.mp4`
4. Photo shots (archive_shots.py, 3D depth moves): `python3 build/shots.py`
5. Copy dive/endmap/hero mp4 to segments/, then the chapter (template engine):
   `cd ../../../templates && python3 build_chapter.py ../videos/oriskany/test_v2/chapter/c01.json` and render chapter/work/c01.
6. Sound: `python3 build/mix.py` (MUSIC=path to swap the theme) -> audio/mix.wav (-14 LUFS, <= -1 dBTP)
7. Mux: `ffmpeg -i render_c01.mp4 -i audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest oriskany_test_v2.mp4`
