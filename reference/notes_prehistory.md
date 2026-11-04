# Prehistory channel ("Strata") repo: what a naval-history channel can reuse

Repo: `/home/user/prehistory-channel` (branch `main`, last commit 2 Nov 2026). Owner: GitHub YOUNESSKING. Two finished videos: V01 "How Long You'd Last in Every Ice Age Ocean?" (15:31-15:36, 1080p, graded) and V02 "Would Crocodiles Dominate Every Prehistoric River?" (16:06, -14.3 LUFS). V03 (tiger) is approved but not built. Every path below is relative to the repo root.

---

## 1. The pipeline, end to end

The model to copy is V02 (`videos/video02/plan/`). The order comes from VIDEO03_START.md and GOLD rules 82-94.

| # | Step | Tools / scripts | Notes |
|---|---|---|---|
| 0 | Keys | `bash tools/setup_keys.sh` | Writes git-ignored `~/.rp_key`, `~/.fal_key`, `~/.el_key{,2,3}`, `~/.pixabay_key`. Never print a key. NOT SET can mean a proxy-injected secret, so test with one free call. |
| 1 | Research + fact sheet | Parallel search / WebFetch (the Firecrawl key was invalid) | One fact sheet per video, so every number comes from one source (rule 82). Example: `research/video01-ice-age-oceans/FACTCHECK.md`. |
| 2 | Script | `research/<video>/SCRIPT_v1.md` (`## SECTION` headers) | Before recording, count "okay" (max 2) and check for repeated openers (rule 83). Plan the thumbnail together with the script (rule 84). |
| 3 | Voice + word timings | `videos/video02/voice/record.py` | ElevenLabs `/v1/text-to-speech/{voice}/with-timestamps`, model `eleven_v4`, voice "Will" `bIHbv24MWmeRgasZH58o`. Records one segment per section with `previous_text`/`next_text`, falls back to a second key when credits run out, and writes `words.json` (`[{w,start,end,seg}]`), `segments.json` and `narration_full.mp3`. The single-file version is `videos/test2/tts_will.py`. |
| 4 | Shot list | `research/video02-crocodile-rivers/make_shotlist.py` -> `shotlist.json` | Opus plans the shots, Sonnet builds and judges, Haiku does mechanical work (QUEUE). |
| 5 | Stock list | One PDF list of clip IDs; the owner downloads once | Licences go in `videos/<v>/media/real/LICENCES.csv` (columns: file, species, shows, source_page_url, author, licence_as_stated, attribution_line, resolution, duration_s, caveats). |
| 6 | AI media | `tools/runpod-zimage/` (Z-Image Turbo stills, about $0.002 each); `tools/runpod-wan22/` (Wan 2.2 Lightning, about $0.10/clip); `tools/fal_dramatic_test.py` (Kling 2.5 / Seedance 1.5); vidIQ Seedance 2 hero clips (about 140 credits each) | QC with a separate Sonnet checker at 8-10 frames per clip, verdict KEEP/TRIM/REDO in `qc.csv` (rule 34). Then the owner checks labelled review reels. |
| 7 | Maps | `maps/` kit (see section 2) + `tools/runpod-cpu/maps_job.py` | Clean bakes go into `map_clip`. |
| 8 | Plan -> chapter JSONs | `videos/video02/plan/make_plan.py` (SPEC/REBAL/HOOK/HOOK_FX/CUT/POST dicts) + `prep_media.py`, `media_index.py` | One JSON per chapter. Shots start on word indexes (`"w812"`, `"@phrase"`). |
| 9 | Build + render | `templates/build_chapter.py ch.json [--res 1080] [--no-media]` -> HyperFrames project; `npx hyperframes@0.8.188 snapshot ... --at t1,t2`; `templates/render_chapters.sh` (hash-skips unchanged chapters); `build_all.sh` | Gate before rendering: line-and-era contact sheet, repeat check, every source 1080p+, no placeholders (rule 89). |
| 10 | Mix | `templates/mix_audio.py` (4 layers), `videos/video02/plan/mix_all.sh`, `templates/mux.sh` (two-pass loudnorm to -14 LUFS + limiter at -1.5 dBFS) | `handover/animation_kit/docs/sfx_density.py` counts SFX per minute. |
| 11 | Final | `videos/video02/plan/build_final.sh` (`BUILD_KEYS="ch11 ch12"` rebuilds only those chapters) | Renders on rented CPU pods: `tools/runpod-cpu/render_chapters.py --pods 4`. |
| 12 | Publish pack | `tools/build_publish_guide.py` (PDF), `videos/0X/publish/{description.txt,chapters.txt,tags.txt,pinned_comment.txt}`, thumbnails | Delivered by Gofile link. The publishing-guide spec is `research/publishing/LESSONS_FROM_BATTLE_MAPS_CHANNEL.pdf`. |

### Cost and time per video
- **Cash:** about $16-19 for a new video, made up of Z-Image $0.60, Wan clips $10-11, fal retries $3-4 and CPU renders $2-3 (QUEUE). V01 estimate: about $17-19 plus ElevenLabs (`COST_TIME.md`). V03 estimate: $15-20, plus vidIQ 1,600-2,400 credits.
- **Subscriptions:** ElevenLabs Creator $22/mo (about 100k characters, about 6 videos). A 17-minute script is about 2,643 words, about 15-17k characters. Vecteezy Pro is the owner's own subscription.
- **Other unit costs:**
  - ElevenLabs sound effects: about 10 credits per generated second. The V02 library cost 4,505 credits.
  - Thumbnails: fal Nano Banana Pro about $0.15 per image. One V01 round was 12 images, about $1.80.
  - CPU pod (`cpu3c`, 16 vCPU): about $0.48/h. Four pods for an hour is about $2.
  - GPU price cap: $0.89/h.
- **Time:** V01 was estimated at 2-3 days elapsed and 15-20 h of machine time, with about 1-2 h of owner review. The V03 honest estimate is about 5.5-6 days (2 for the base, 2-2.5 for the one-off animation kit, about 2 for 40 scenes), or about 4 days at 15 % animation. Owner time is about 3-4 h across 4 checks: script, voice, hook, final.
- **Render speed:** HyperFrames 1080p takes about 5 min per minute of video (16 min is about 75-90 min). A map scene takes 30-60 min to write and 10-20 min to render.
- **Script length:** about 165-180 wpm, so 14-24 min is roughly 2,300-4,300 words.

---

## 2. Reusable as-is for ship videos

- **Template engine** (`templates/`): shot-list JSON -> HTML/GSAP -> MP4.
  - Timing is driven by words: `w123`, `w123e`, `@phrase#2`, `end-0.5`. Spliced narration inserts are supported.
  - The builder warns on gaps, shots over 6 s, too-short clips and unknown parameters.
  - Blocks that carry over directly:
    - `number_clip` (count-up and `strike_swap`): tonnage, 911 ft, 212 ft depth, $ cost
    - `lower_third`: names, ranks, dates
    - `title_card`: chapter, kicker, date
    - `text_card`
    - `problem_counter`: "problem one: PCBs"
    - `scale_ruler` with your own `svg` silhouette: carrier vs a known object
    - `map_clip`: pin, name, date, `measure` bar, `track`
    - `clip_plain`, `black`
    - `extinct_plate` with `word`: "SUNK" / "STRUCK" / "SCUTTLED" + date
    - `outro` / `end_screen`
  - Parameters: `templates/TEMPLATES.md`. Galleries: `templates/demo/gallery_*.jpg`.
- **Animation kit:** `templates/blocks/anim_gauge.py`, `anim_lockon.py`, `anim_options.py`, `anim_xray.py` + `anim_common.py`. Worked custom scenes: `v02_anim_a/b/c.py`. Demo: `templates/demo_anim/`. Style tests: `templates/tests_anim/make_test*.py`, `out/ALL_TESTS.mp4`, `test6_cast.mp4`, `test7_voice_sound.mp4`.
  - Naval uses: depth gauge (sinking to 212 ft), options list ("scrap / museum / reef", struck through), X-ray hull cutaway (PCB and fuel removal, compartments), lock-on (kamikaze/aircraft target).
  - Retint per video with the chapter key `"anim_theme": {"hue":..,"sat":..}`.
  - Docs: `handover/animation_kit/HANDOVER.md` (setup, 5-step scene method, starter prompt), `docs/scene_plan_example.json`, `example_anim_*.json`, `example_sound_ch07.json`.
- **Map kit** (`maps/`, battle-maps engine): the strongest fit for naval topics.
  - Terrain bake: `tools/bake.py NAME LAT LON ZOOM [EXAG]` + `bake_hd.py` (dark "documentary" grade `_hd_ref.jpg`). Data from Mapzen/AWS Terrain Tiles, open, no key.
  - Scenes: `scenes-src/*.js` -> `tools/build_scene.py` -> `npx hyperframes lint/snapshot/render`, or `tools/render_all.sh`.
  - Engine helpers that suit naval scenes:
    - `GG.ship` (ship silhouettes), `GG.arc` (ballistic arcs), `B.arrow` (self-drawing routes)
    - `K.aircraft` (top-down planes flying a path), `K.impact` (explosion + shake), `K.target`
    - `B.camera` (wide -> close -> wide)
    - `L.clouds`, `scaleBar`, `north`
  - Full method: `maps/GUIDE_COPY.md`. Clean no-text bakes for `map_clip`: `tools/bake_clean.py`.
  - Credit line: "Terrain: Mapzen / AWS Terrain Tiles". Natural Earth is public domain. OSM is ODbL with on-screen credit.
- **Archival photo/film shots:** `maps/tools/archive_shots.py` (written for battle-maps WWII videos). It turns a JSON list of `{"film":..., "ss":..., "label":...}` or `{"photo":..., "move":"in|out|left|right", "focus":[x,y]}` into sub-pixel smooth push/pan shots (about 18 % push, 12 % pan). It also does `"parallax": true` (rembg cut-out 2.5D), lower-third labels and a "Frontlines"-style big-year headline card. Aim for 3-5 s per shot. The owner's note on an earlier video: "photos held too long, never moving; use film".
- **Sound design:**
  - Mixer: `templates/mix_audio.py`, four stems with a sidechain duck. Final settings: `--music-db -20 --music-gap-db -12 --amb-db -30 --amb-gap-db -23 --sfx-db 10 --things-db 6 --el-dir <your folder>`.
  - Synth graphic sounds: `templates/sfx_voices.py` (tick, tok, thud, click, scratch, marker, swoosh, beep, heart, hit, stamp, ding...).
  - Recorded library: `videos/video02/sfx_el/` (45 ElevenLabs files, made on the owner's paid plan, so the same owner can reuse them).
    - Ship-usable files: `deep_boom`, `heartbeat`, `splash_big`, `splash_small`, `sink_bubbles`, `thunder`, `rain_burst`, `fire_crackle`, `ice_crack`, `env_coast`.
    - New sounds to generate: hull groan, horn, sonar ping, jet launch, deck wind, the scuttling charges.
  - The map engine has its own `explosion` and `impact` SFX cues.
  - Rules: `handover/animation_kit/docs/SOUND_DESIGN_V02.md`, `RULES_95-101`.
- **TTS:**
  - ElevenLabs. Voice tests are in `voice/`: "Will", "Roger", "Chris" and 3 designed voices (`designed_voice1-3_opening.mp3`), with the script in `voice/script_v4.txt`. Acting tags `[deadpan] [pause] [sighs]` work. **Commercial use needs a paid ElevenLabs plan.**
  - Free fallback: Kokoro ONNX (`maps/tools/narrate.py am_michael`), which voices one clip per sentence, giving exact `timing.json`.
- **Loudness/mux:** `templates/mux.sh`. Use one gain plus a fast limiter, not dynamic loudnorm (that flattens hits). Measure the result. The battle-maps cloned voice came out 1.2-1.3 dB hot.
- **Rented machines:**
  - `tools/runpod-cpu/` (`launch.py prices|up|status|down`, `render_chapters.py`, `maps_job.py`). Pods self-terminate, and the tools only kill pods that carry their own name.
  - `tools/runpod-multi/launch_one.py` is now name-filtered.
- **Thumbnails:**
  - Skill: `.claude/skills/video-thumbnail/` (`scripts/generate_fal.py --prompt --output --aspect-ratio 16:9 --resolution 2K [--reference img]`; with `--reference` it uses edit mode `fal-ai/nano-banana-pro/edit`). It appends `brand-style.md`, which must be rewritten for ships. There is no headshot step.
  - Text goes on in post with `tools/make_thumb.py pic.png out.jpg "15|red+Minutes|white" --cap 120 --grit 1`. Font: Anton (`tools/fonts/Anton-Regular.ttf`, OFL). It writes a `_168.png` phone preview.
- **Competitor study:**
  - `.claude/skills/watch/` (bradautomates/claude-video, MIT). With `GEMINI_API_KEY` Gemini watches the YouTube URL itself. Otherwise it uses yt-dlp + ffmpeg frames + captions or Whisper. `--start/--end`, `--question`.
  - `tools/study_video/gemini_watch.py URL --ask hook|design|sound|full`. Free key; output in `research/video_study/<id>/`.
  - `tools/study_video/study_video.py` must run on the owner's own PC, because YouTube blocks yt-dlp on cloud machines. It reports cuts/min, deep hits, silences, LUFS and Demucs stems.
  - vidIQ: `video_watch` 25 credits, `video_transcript` 5, `channel_stats` + `channel_videos` about 10.
  - Owner rule: study only, never reuse the downloaded media.
- **Publish pack:** `tools/build_publish_guide.py` (paths hard-coded to V01 and an old scratchpad, so edit before use). Description and pinned-comment models: `videos/video02/publish/`.
- **Library practice:** `library/catalog.csv` + README rules (check before you generate, one use per video, log the prompt and `used_in`). Copy the idea for an archival-asset catalogue.

---

## 3. Needs adapting for archival naval footage

1. **Grade:** `templates/grade/deep_time.vf` (teal shadows, gold highlights) is applied automatically to every clip in `build_chapter.py`. Archival B&W and faded Kodachrome need `GRADE=none` or a new `.vf` (for example a neutral contrast/denoise filter). The "no film look" rule (no grain, vignette or tint) also conflicts with the archival aesthetic. That is a decision for the new channel; the battle-maps kit uses vignette + grain.
2. **Resolution rule:** "real footage 1080p or better" (rules 61, 86, 89c) is impossible for NARA 16 mm and 1950s-60s film (often 480p or 4:3). It needs a new rule: allow SD archival, upscale it, then either pillarbox on a blurred or dark fill or use a 4:3 frame. The builder conforms to 16:9 at 1280x720/1920x1080, so add a pillarbox option. Burned-in leader, countdown and title cards must be trimmed (LICENCES.csv caveats already flag them).
3. **Typography and colour:** style C (Cormorant Garamond 600 #F6EFE0, Jost caps, gold #C9A45C hairlines) is a "nature-doc" look. A naval channel can keep it, or switch to the battle-maps look: Oswald labels, Special Elite typewriter dates, the "Frontlines" year card in `archive_shots.py`, dark relief grade. Pick ONE palette per channel (GUIDE_COPY).
4. **"You" stick figure and tier board:** these belong to the survival game format. A "what happened to this ship" video is a chronological story. Keep the stick cast + one prop (sailor cap, officer, diver) for animations. Drop `tier_board`, or reuse it as a timeline/roadmap.
5. **Music:** the self-made beds (`templates/make_lofi_bed.py`, V02 `make_hook_music.py`, V01 `build/gen_audio.py`) are lo-fi/taiko. Naval documentary needs a dark cinematic bed. Use Epidemic/ElevenLabs Music only if licensed.
6. **Silhouettes:** the built-in `scale_ruler` animals (shark, orca...) need ship SVGs: Essex-class carrier side view, aircraft. Hand-drawn or PD sources (PhyloPic-style CC0 is for animals only).
7. **Footage sourcing:** the rules say "Vecteezy Pro first" for nature. For ships, use public domain first: NARA (catalog.archives.gov), NHHC, DVIDS, Navy.mil, and archive.org mirrors of NARA films. V02 already pulled from archive.org with licence metadata.
   - **Always read each item's rights field.** FOOTAGE_FREE.md found agency pages that carry copyrighted contributor content: "fws.gov pages can carry non-PD contributor content". NHHC "courtesy" collections and DVIDS work by contractors or foreign photographers are not automatically PD.
   - Never NC/ND licences. Credit every CC BY item.
   - Wikimedia Commons blocked automated downloads from the cloud machine (24 Oct). Freesound and Pixabay return 403 to scripts. Plan for owner-side downloads.
8. **AI picture rules:** the source order (Wan/Kling/vidIQ) is for prehistoric scenes. For real ships, AI video risks wrong hull numbers and anachronisms, so treat it as a last resort. Use real photos with motion plus animation for what cameras missed (sinking under water, the 2006 explosive scuttling, reef growth). Apply rule 73 (line-and-era gate) and rule 62 (line = picture) strictly: right ship class, right era aircraft, hull number 34.
9. **Thumbnails:** brand-style.md says "one huge creature, white-dot eyes, warm red/black/orange, never deep blue". This must be rewritten. The battle-maps formula fits better: dark moody AI scene on the left 2/3, a **real PD photo cut out (rembg)**, a banner, 1-3 caps words (decision, quote, stakes). Never fake a real person's likeness. Inpaint out wrong flags and symbols.
10. **The synthetic-content box:** battle-maps reasoning was that archive photos, maps and cards are not AI video and only the voice is AI. They ticked Yes for safety. Answer the same way on every video.

---

## 4. Hard-won rules, mistakes, owner decisions, style

**Rules worth carrying over (GOLD_STANDARD.md):**
- **Rule 1:** "A place, a date, or 'land/coast changes' = MAP animation. Never a landscape clip."
- **Rule 2:** "A number ... = big number over a clip of that exact danger ... The number lands on the spoken word."
- **Rule 8:** "If a line has no picture that proves it, rewrite the line or add a [graphic] with a label. Do not add a pretty clip."
- **Rules 22-24, pacing:**
  - Body average 2.5-3 s, hook 2 s. Clip max 4.5 s, moving thing max 5.5 s, hard cap 6 s.
  - "Something new every 1.5 s."
  - Cut on the first word of the line.
- **Rule 28:** each clip used once, and never stretch a clip with a frozen last frame.
- **Rule 61:** the same clip or shoot at most 2 uses per video, never back to back, at least 3 min apart. Clips from the same shoot count as one.
- **Rule 62:** "Line and picture must match ... never a stand-in."
- **Rule 72:** no empty frames, at most 2 text cards in a row. Labels at least 3.5 % of frame height, names at least 5 %. Static map at most 4.5 s.
- **Rule 74:** evidence cards only from CC0 / CC BY / CC BY-SA, never NC. Credit bottom-left and in the description.
- **Rules 82-94:**
  - one fact sheet (V02 hook said 16,000 N while the chapter said 16,414 N)
  - thumbnail planned with the script (V01 had a shark thumbnail for a video whose first line is "Not a shark")
  - one test per tricky subject before the batch
  - spend gate
  - shot-list gate before any render
  - hook built and approved first
  - short review reels, aiming for one review round
  - renders on rented machines, clean disk, commit after every step
- **Rules 95-101 (locked):**
  - Animation is a third picture source for what no camera filmed, one idea per scene.
  - Elements snap in within 0.3-0.5 s, then the camera drifts. Something new every 1-3 s, the picture moving in 80 % or more of seconds.
  - Count-ups land with a flash + a gold ring + a deep hit.
  - Sound in four layers. About 16 SFX/min in bursts. One signature sound planted in the hook, brought back, paid off out loud. Voice 11-12 dB over the bed. -14 LUFS.
  - Picture mix: at most about 20 s of one source in a row.

**Production mistakes (QUEUE "Video 02 lessons"):**
- Use only proven GPU types. Two A40 pods were OOM-killed and sat idle for about 1 h.
- Check the price before keeping a pod: $1.09/h pods were launched against a $0.89/h cap.
- Check pods 10 min after launch.
- QC starts with the first clip.
- No test calls to paid APIs without the owner's OK (a Kling job was sent by mistake).
- One vidIQ job at a time; two agents running at once burned extra credits.
- Keep at least 100 vidIQ credits.
- Another session's launcher killed our CPU pods. Kill only pods carrying your own name.
- A 1080p chapter with 32 clips was OOM-killed on an 8-vCPU `cpu3c` pod; use `--flavor cpu3g`.
- Container restarts kill background jobs: use `setsid nohup`, cache per chapter, and check every downloaded mp4 with ffprobe (a pod that dies mid-download leaves a truncated file).
- The V02 final died once on a full disk.
- Video models drift. A specific species turned generic after 1-3 s, and Veo did not fix it. Use stills with motion instead of paying for redos. The ship equivalent is a specific ship.
- Map labels: Overpass is blocked from the cloud, so use Natural Earth or hand-placed labels. Keep the camera inside the 2880x1620 map at every key. All assets local (no CDN).

**Owner rules:**
- Ask before ANY spend not already agreed, and state the service, purpose and amount. Report the balance after each paid job.
- Deleting files and uploading to public hosts need an OK.
- Plain short English, summary first. The owner likes PDFs for lists.
- Same-channel topic spacing of 6 weeks or more.
- Never download from YouTube for reuse.
- Tick the synthetic-content box.
- No silence after board drops.
- End on the content, not an end card; the board holds 10 s for end-screen elements.
- "Title + thumbnail + video are ONE promise ... paid in the first 30-60 s"; write down the timecode of each thumbnail element in the publish PDF.

**Style specifics:**
- Fonts: Cormorant Garamond 600 + Jost, plus Anton for thumbnails only.
- Colours: warm white #F6EFE0, gold #C9A45C as the only in-video pointing colour; red only in thumbnails.
- Text fades over 0.5-1.1 s with no bounce. Letterbox bars only on big title moments.
- Hook: about 2 s cuts. Body: about 3 s average.
- No on-screen captions or subtitles beyond these text shapes. BTB-style kinetic two-tone captions were rejected; one italic "echo word" per chapter is allowed.

---

## 5. Hook, retention, script, title and thumbnail rules that transfer

**Hook:**
- 28-35 s, 70-90 words, about 14-18 shots (rule 36).
- Wow image at second 1-2 and then at least every 4 s (rule 37).
- Exactly one number, by second 12 (rule 40).
- Promise line on the biggest image, then a tonal drop (rules 38, 42).
- Plant-and-pay: every hook image comes back named later (rule 44).
- Claim-hook variant (rule 59): claim + 3 proofs (0-13 s), one question by 21 s, roadmap by about 45 s.
- DT lesson: put danger in the first 15 s. Their hit had about 16 SFX/min against the flop's 6, and the picture moved 83 % of the time (`research/depththeory-squid-vs-whale.md`).
- Battle-maps: a hook-first title got 0.9 % CTR, and a title promise paid at 7:37 lost viewers. Pay the promise in 30 s.

**Retention:**
- An open loop or tease about every 60-90 s, and a wow beat every 30 s in the first 3 min (rules 35, 45).
- Name the problems out loud ("one problem... a second problem"). The deciding reason is stated 15-35 s before the payoff (rules 49, 55).
- Mid-video reversal at 55-65 % of the runtime (rule 56).
- One flagged controversial take plus a closing question (rule 57).
- An honest hedge once per chapter, followed by a committed verdict (rule 51).
- Vary chapter lengths (40/65/90 s; verdict 16).
- Pattern break every 45-60 s.
- Two music states only: main and "reflective" (rule 78).

**Script engine (BTB study, strongest lesson):**
- Their hit and their essay version had the same facts and differed 17x in views. The difference: a WHY question stated by 0:32-1:08, answered by a chain of reasons; each chapter's "plan" fails and causes the next.
- Causal bridges, not name-only openers.
- One everyday-object comparison per subject, drawn on screen ("as long as 3 football fields").
- Ending = perspective flip + three-line callback + sign-off.
- Fact-check famous numbers, because sizes start comment wars ("older estimates said X").
- The ship equivalent: "Why the Navy sank its own carrier": scrap was too toxic or costly → museum failed → reef plan → PCB fight → explosive scuttling → today.

**Titles:**
- Fossil hits are one plain question of 44-50 characters, with no pipe, emoji or hype.
- Copy the winning competitor's pattern exactly (battle-maps).
- Avoid "forgotten / underrated / almost / nearly" and nicknames. No negation as the hook.
- Score titles with vidIQ `score_title` at 85 or more, but the pattern beats the score.

**Thumbnails:**
- Thumbnail → title → thumbnail: the text complements the title and never repeats it.
- 1-3 words, at most about 10 characters per line, one red word; Anton cap 110-140 px on 1280x720 with a thin outline + soft glow.
- One focal subject on the left 55-65 %, the dark right side for text. Nothing in the bottom-right (the timestamp sits there).
- Check at 168x94.
- A scale figure must be at least 6 % of frame height. "One idea" check.
- Never-use list of other channels' signatures.
- 4 concepts per round, 2 for Test & Compare. Test & Compare decides on watch-time share and is inconclusive at low impressions.
- Battle-maps winning text types: the hero's decision ("LET THEM COME", 1.0M), the enemy's verbatim quote ("AMATEURS", 773k), ominous stakes ("AT THE GATES", 585k).
- After publishing: read CTR and 30-s retention at 3, 7 and 28 days. If CTR is under 2 % after about 1,000 impressions, change the title to the pattern first, then the thumbnail.

**Description:**
- Lines 1-2 = the hook in plain words, never "In this video...".
- No links (new channels get flagged). Name licences in words.
- Exactly 3 hashtags.
- 12-18 tags, 500 characters or fewer.
- Chapters from the final timing file, each 10 s or longer, no duplicate times.
- Write the description only after the voice is locked.

---

## 6. Known problems and open issues

- `handover/animation_kit/` contains only `HANDOVER.md` + `docs/`. Its `examples/` and `templates/` folders do not exist; the code lives at `templates/` (repo root) and the videos in `templates/tests_anim/out/` and `templates/demo_anim/`.
- `templates/TEMPLATES.md` does not document the `anim_*` blocks; read the code or the `example_anim_*.json` files.
- V02 sound density came out about 27-31 perceived SFX/min against the 16 target. The block graphics (label clicks, swooshes) need thinning; there are no calm minutes yet.
- Templates use a 1280x720 design space only (1080 is a scaled stage). Size charts are true to scale, so a tall subject makes the human tiny.
- V02 needed many placeholders and REDOs: 50 placeholders at draft. Real footage had no match for specific behaviours. Expect "NO MATCH" gaps with archival footage too, so plan animation fallbacks.
- vidIQ credits are scarce: about 5 left before the Nov 22 renewal, the connector was down on 30 Oct, and a new account was connected.
- The RunPod balance was low ($2.89); every top-up needs approval.
- Old scripts hard-code dead scratchpad paths (`tools/build_publish_guide.py` `S=...`; `docs/mix_all.sh` uses V02 paths). `mix_audio.py`'s default `--el-dir` is V02.
- The owner still has to rotate the API keys shared in chat.
- Firecrawl key invalid.
- Media is git-ignored (finals, work dirs, `videos/video01/media/`). A fresh clone has no rendered videos, only code, JSON, the SFX library, the clip library (90 MB) and thumbnails.
- The engraving thumbnail exception (rule 81) is still the owner's open decision.

---

## 7. Real channel performance data

- **None for this channel's own videos.** V01 and V02 were delivered to the owner (Gofile) with A/B thumbnails ready. The repo holds no CTR, views or retention reads, only a plan to read them at 3, 7 and 28 days.
- **Battle-maps sister channel** (same owner, 12 videos, `LESSONS_FROM_BATTLE_MAPS_CHANNEL.pdf`):
  - A hook-first title got **0.9 % CTR**; the "almost fired" title flopped.
  - A sister channel's CTR fell to **1.7 %** when the thumbnail contradicted the title.
  - Competitor (Tactical Genius) thumbnail-text views: 1.0M / 773k / 585k winners vs 29k for a nickname.
- **Competitors (studied):**
  - **Fossil:** 12M, 3.6M, 1.7M (in 7 days) and 1.5M on its top 4 = 94 % of about 20M channel views. Formula-repeat "9 Minutes" got 405k. The "I Simulated..." videos got 9-176k.
  - **Beyond The Blue:** "How Long You'd Last in Every Prehistoric Ocean" 3.26M. The essay version of the same facts got about 192K. The same 11 stops repeated 14 days later got 51K.
  - **Depth Theory:** sperm whale about 400K in 3 days (1,682 words, 168 wpm, -15.1 LUFS, 16 SFX/min) vs colossal squid about 35K.
