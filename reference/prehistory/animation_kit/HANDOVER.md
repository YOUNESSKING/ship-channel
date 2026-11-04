# Animation kit: handover

This is the kit behind the 19 animations in our Video 02 ("Would Crocodiles Dominate Every Prehistoric River?").
Give the whole folder to the other channel. Their Claude Code session can read this file and start making scenes.

## 1. What's in the folder

| Folder / file | What it is |
|---|---|
| `examples/v02_19_scenes_with_sound.mp4` | **Watch this first.** All 19 scenes with the final sound (2.5 min). |
| `examples/demo_generic_blocks.mp4` | The 4 ready-made scene types (gauge, lock-on, options list, X-ray) in their variants. |
| `examples/test6_people_and_xray.mp4` | The stick-figure "you", the role props (scientist, hunter…) and the gold X-ray mode. |
| `templates/` | The engine: shot-list JSON → HTML animation → MP4 (HyperFrames), plus the sound mixer. |
| `templates/blocks/anim_*.py` | **Ready-made scenes**, driven by JSON parameters: `anim_gauge`, `anim_lockon`, `anim_options`, `anim_xray`. Shared parts are in `anim_common.py`. |
| `templates/blocks/v02_anim_a/b/c.py` | Our 19 custom scenes, as **worked examples** for writing new ones. |
| `templates/tests_anim/make_test*.py` | The style tests the look was locked from. |
| `docs/RULES_95-101_animation_and_sound.md` | **The style rules: read before making anything.** |
| `docs/SOUND_DESIGN_V02.md` | How the sound works: 4 layers, levels, signature sound, density. |
| `docs/scene_plan_example.json`, `docs/example_anim_*.json`, `docs/example_sound_ch07.json` | How each scene was planned against the script, and how sounds are placed on words. |
| `docs/mix_all.sh`, `docs/sfx_density.py` | Our full-video sound chain, and the sound-effects-per-minute check. |
| `docs/sfx_library_names.txt` | The names of the 45 recorded sounds we used. **The audio files are not included** (see section 5). |

## 2. Setup (one time)
- Linux or Mac, with Python 3 + numpy, ffmpeg, and Node 18+ (HyperFrames runs through `npx`, with headless Chrome).
- Test it:
  ```
  cd templates
  python3 build_chapter.py --list
  python3 build_chapter.py demo_anim/demo_anim.json
  npx -y hyperframes@0.8.188 snapshot demo_anim/work/demo_anim --at 2,6
  ```
- Read `templates/README.md` (4-step build) and `templates/TEMPLATES.md` (every block and its parameters).

## 3. How one scene is made
1. **Pick the line.** Every animation explains ONE thing the narrator says (rule 95). Good cases are what no camera can film:
   - "you" in the scene
   - inside the body (X-ray)
   - a size or number comparison (gauge)
   - a choice ("what would you do?" list)
   - a predator spotting you (lock-on)
   - a joke as a 3–6 s mini scene
2. **Time it to the voice.** Shots start on word indexes (`"start": "w812"`) from a `words.json` of word timings (any forced aligner, or ElevenLabs timestamps). Never use guessed seconds.
3. **Use a ready block first.** If one fits, it's only JSON, for example:
   ```json
   {"id": "C11-16", "template": "anim_gauge", "variant": "bars", "start": "w2091", "params": {...}}
   ```
   For a new idea, copy the closest scene from `v02_anim_*.py` and change it. Add the new block name to `OPTIONAL` in `templates/blocks/__init__.py`.
4. **Look before rendering.** Run `npx hyperframes snapshot ... --at t1,t2,t3`, then check the stills: line and picture match, nothing empty, text big enough on a phone.
5. **Render.** Use `render_chapters.sh`, which skips chapters that haven't changed. 1080p takes about 5 minutes of machine time per minute of video, so rent a machine if it's slow.

## 4. The look (locked, rules 96–98)
- Gold line-art (#C9A45C, the only pointing colour) and warm-white type (Cormorant Garamond + Jost) on a **dark ink background tinted to the video's world**:
  - set the chapter key `"anim_theme": {"hue": 34, "sat": 0.75}` (we used river-mud brown for crocs, green for a jungle)
  - every green in the blocks is retinted to that hue automatically
- The hero animal is a **true-colour silhouette**, not line art. We use free PhyloPic CC0 shapes; see `templates/lib/anim_assets/LICENCE.txt`.
- **Motion:**
  - elements snap in within 0.3–0.5 s, then the camera drifts slowly
  - something new every 1–3 s, and nothing fully still
  - count-ups land with a flash, a gold ring and a deep hit
- **People:** "you" is always the simple stick figure. Other people are the same figure plus ONE prop that shows the role.
- **Never:** deep blue, cartoon eyes, or a flat-vector copy of another channel's style.

## 5. Sound (rules 99–100): this is what makes the scenes feel alive
- **Four layers:**
  1. an **environment** bed per place that never stops (`env:name`)
  2. **things**: real recorded sounds (`el:name`)
  3. **mood**: a music bed that never stops, heartbeats, booms on reveals
  4. **graphics**: synth tick, beep, thud, click, scratch and whoosh on every on-screen event; built into the blocks
- **One signature sound per video:** plant it in the hook, bring it back, then pay it off out loud.
- **Density and levels:**
  - about 16 sound effects per minute, in bursts; check with `sfx_density.py`
  - voice about 11–12 dB over the sound design
  - final loudness −14 LUFS
- **Mixer settings we ended on** (after our owner's feedback):

  | Setting | Value |
  |---|---|
  | Music under the voice | `--music-db -20` |
  | Music in pauses | `--music-gap-db -12` |
  | Environment under the voice | `--amb-db -30` |
  | Environment in pauses | `--amb-gap-db -23` |
  | Graphic sounds | `--sfx-db 10` |
  | Recorded sounds | `--things-db 6` |

  `mux.sh` sets −14 LUFS with one gain plus a fast limiter, so the hits keep their punch. Don't use dynamic loudnorm: it flattens them.
- **The recorded sounds are not included.** They were made with our ElevenLabs subscription. The other channel should generate their own, using the names in `docs/sfx_library_names.txt` as the list, with their own ElevenLabs paid plan (sound generation, about 10 credits per second). Point the mixer at their folder with `--el-dir`.

## 6. Paths to change
- `mix_audio.py`'s default `--el-dir` points to `videos/video02/sfx_el`; pass your own folder.
- `docs/mix_all.sh` is our V02 script, with paths to our voice and music files. Use it as a model and don't run it as is.

## 7. Starter message for their Claude Code session
> Read `HANDOVER.md`, then `docs/RULES_95-101_animation_and_sound.md`, `docs/SOUND_DESIGN_V02.md` and `templates/README.md`. Watch the frames of `examples/v02_19_scenes_with_sound.mp4`. Set up and render the demo (`templates/demo_anim`) to prove the kit works. Then, for my script and `words.json`, propose a list of animation scenes: the line, the block (ready or new), the duration and the sounds. Show it to me before building. Build each scene, check it with snapshots, render, mix with the four sound layers, and send me a short reel of only the new scenes with sound.
