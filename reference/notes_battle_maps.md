# battle-maps repo: what to reuse for the naval channel ("what happened to this ship")
Source repo: /home/user/younessking/battle-maps (channel "Generals on the Map", 17 videos, Oct-Nov 2026). Read: CLAUDE.md, HANDOVER.md, STYLE_LOCK.md, README, channel/CHANNEL.md, setup.sh, map-kit/, tts/, templates/, library/, research/ (DATA_RULES, CHANNEL_LOG, PACKAGING_GUIDE, LESSONS_PUBLISHING_AND_THUMBNAILS, GEMINI_BRIEF_v3, CONSIDERING, OWNER_DIALOGUE_*), plus the Patton #15 folder (WWII, US Army film) and the Arnold #17 folder (newest; it has a naval battle at Valcour Island).
**Path gotcha:** the scripts hard-code `/home/user/battle-maps` (CLAUDE.md: "The repo must live at /home/user/battle-maps"). This copy is at `/home/user/younessking/battle-maps`. Symlink it or sed the paths before running anything.

---

## 1. Pipeline end to end (order, tools, time)
The canonical order is the no-skip checklist in HANDOVER 0b step 7. Each video lives in its own folder, copied from the skeleton (newest skeleton: `arnold/` or `grant/`; the official reference skeleton is `rokossovsky/`).

| # | Step | Tool / command (run from the video folder) | Time |
|---|---|---|---|
| 0 | Setup | `setup.sh`: ffmpeg, `npm i -g hyperframes`, `hyperframes browser ensure`, pip numpy pillow kokoro-onnx soundfile rembg[cpu] reportlab fonttools pypdfium2, Kokoro model files into `tts/`, hyperframes + remotion skills. Done marker `/tmp/battle-maps-setup.done`. **Not in setup.sh:** `/opt/models/depth_anything_v2_small.onnx` (huggingface onnx-community/depth-anything-v2-small, `onnx/model.onnx`) + `pip install onnxruntime opencv-python-headless` (needed for 3D-depth photos; assembly fails without it); `pip install affine pysheds` (needed for rivers from the DEM). | ~5-10 min |
| 1 | Research | The owner pastes `research/GEMINI_BRIEF_v3.md` into Gemini Deep Research and attaches the result. Then 3 Sonnet fact-check agents check it against primary/official texts (archive.org OCR of the official histories) → `<v>/research/FACTCHECK_A/B/C_*.md` + `FACT_NOTES.md` | Gemini: owner's time; fact-checks ~30-60 min in parallel |
| 2 | Script | `<v>/script.md`: `## SECTION` headers; every paragraph starts with `[MAP: scene-para-id \| visual notes]` or `[ARCHIVE: notes]`; 2,400-2,700 words for 16-19 min (2,089 words came out at 13:29). `tools/count_words.py` | — |
| 3 | Names check | `tts/PRONUNCIATION.md`: phonemize every name (`k.tokenizer.phonemize(w,'en-us')`), **check the stress mark**, add respellings to `SAY` / exact phonemes to `tools/tts_names.py` PHON, then a 20 s names clip (`tools/names_clip.py`) for the owner's approval | ~15 min |
| 4 | Voice | `tools/narrate.py am_michael` → `audio/voice.wav` + `audio/timing.json` (per-paragraph AND per-sentence timing; `B.at(para, phrase)` lands on the word). Partial edits: `tools/narrate_changed.py` (re-voices only the changed paragraphs) | ~15 min for 18 min of speech |
| 5 | Music bed | `python3 tools/make_music_bed.py` (4 Kevin MacLeod tracks fitted to the chapters, 5 s crossfades) | ~1 min |
| 6 | Basemaps | `tools/bake.py NAME LAT LON ZOOM EXAG` → `LIFT=1 tools/bake_hd.py NAME` → (from #16 on) `NO_TREES=1 FULL=1 python3 tools/ref_look_v11.py NAME 2880 1620 assets/NAME_hd_lift.jpg` + `make_detail_layers.py` (rivers/water) + `make_land.py` (land mask). Bake one map at a time (OOM risk, ~6 GB RAM) | ~3 min per map for v11 + tile download |
| 7 | Images/film | Image agent (Sonnet) runs BEFORE the map agents: commander photos → `<name>_head.png` (rembg isnet-general-use cut-out) + `_head_flat.png`; flags; archive stills; film clips via `assets/film/cut_clips.sh` + `MANIFEST.md`; every file logged in `assets/media/CREDITS.md` | 30-90 min |
| 8 | Map scenes | Opus agents (max 3 at once), one per move, with a shared `research/AGENT_COMMON.md` + `SCENES.md`. Write `scenes-src/SCENE.js` → `tools/build_scene.py SCENE BASEMAP FIRST_TAG LAST_TAG` → `hyperframes lint .` → `hyperframes snapshot . --at ...` → ONE contact sheet (`tools/make_sheet.py`, `quick_sheet.py`), max 3 rounds. A scene = one unbroken run of `[MAP]` paragraphs | 15-25 min per sheet; a 1-2 min scene ~30-60 min to write |
| 9 | Owner approval | One labelled sheet per move. "Never render without the owner's OK" | — |
| 10 | Render | `bash tools/render_all.sh --assemble "SCENE BASEMAP FIRST LAST" ...` (detached, sequential, resumable, writes `logs/render_all.done`), or `tools/render_direct.sh` when agents wrote inline scene builders (Patton/Arnold: render_all would overwrite them) | **The slowest step:** 9-13x real time. 2.5 h for 16 min (Grant), ~4 h 15 min for 19 scenes (Patton) |
| 11 | Assemble | `tools/assemble_full.py` (edit SCENES/CHAPTERS at the top): cuts the renders by paragraph offsets, builds archive shots (`archive_shots.py`, `archive.json` keyed by PARAGRAPH INDEX, `archive_inserts.json` keyed by tag + spoken from/to words), collects SFX cues (`sfx_cues.py`) → `sfx_mix.py`, mixes voice + ducked music + ducked SFX, two-pass loudnorm to -14 LUFS. `VOICE=audio/voice.wav` for plain Kokoro. Sound-only change: `--audio-only` (~5 min) | ~20 min |
| 12 | Loudness fix | It always misses. Grant's recipe (STYLE_LOCK 2c-9): `volume=1.45dB,alimiter=limit=0.82:level=disabled` on the master audio, then remux with `build/video_only_1080p.mp4` → -14.3 LUFS, TP -1.0. Measure with ebur128 every time. Check with ffprobe that the master is 1920x1080 | ~5 min |
| 13 | Checks | `tools/check_sound_lock.py` must say OK; a style-audit agent (`arnold/build/AUDIT_STYLE.md`: one frame every 2 s against every STYLE_LOCK rule, findings ranked worst first); check one bomb/impact frame against its sound | 30-60 min |
| 14 | Packaging | `research/PACKAGING_GUIDE.md` (0b wins): 3 titles scored with vidIQ (>= 85), 2-3 thumbnails, description, chapters from timing.json, tags → `<v>/youtube/` + `tools/make_publish_guide.py` → publishing PDF | ~1 h |
| 15 | Delivery | Gofile: `curl -F "file=@X.mp4" https://upload.gofile.io/uploadfile`, check the md5. Needs the owner's explicit OK. The owner uploads to YouTube himself ("Never upload or edit anything on YouTube ourselves") | — |
| 16 | Analytics | DATA_RULES standard Studio prompt for days 1-3 → `research/CHANNEL_LOG.md` | — |

Estimated real work is ~1.5-2 h per video plus render time (HANDOVER §8). Use one fresh session per video (5-10x cheaper); a full video is ~25-45M tokens.

---

## 2. Reusable as-is (exact paths)
- **Map engine, portable kit:** `map-kit/` with `MAP_MAKING_GUIDE.md`. It was written "for another channel"; it covers any topic and is marked war-neutral. It contains lib/ (battle.js, fx.js, gg.js, living.js, battle.css), vendor/gsap.min.js, tools (bake.py, bake_hd.py, make_land.py, fetch_osm.py, make_geo_layer.py, make_rivers_dem.py, make_control.py, make_front_lines.py, build_scene.py, render_all.sh, scene_template.html, make_sheet.py, phrase_t.py, narrate.py, archive_shots.py), fonts (Oswald 500/700, Special Elite), grain.png, a sample basemap, a tested `scenes-src/example_route.js` (a self-drawing route, which is exactly a ship track) and `examples/advanced_kursk_scene.js`. Quick test command at the bottom of the guide. The **newer** versions of the tools are in `arnold/tools/` (assemble_full.py, sfx_cues.py, sfx_mix(_lib).py, check_sound_lock.py, restore_film.py, make_publish_guide.py, finalize.sh, render_direct.sh, render_queue.sh, quick_sheet.py, rebuild_all.sh, narrate_changed.py, tts_names.py, names_clip.py, make_heads.py, cutout_heads.py, make_period_flags.py, make_headline_arnold.py). For the Oriskany you would copy `arnold/` (or `patton/`, which is WWII with film) as the skeleton, not `map-kit/` alone.
- **Ship art already built:**
  - `map-kit/lib/gg.js` `G.ship` (side silhouette).
  - `arnold/tools/va_kit.js`: top-down boat counters at a constant on-screen size (gondola, galley, schooner, ship-of-the-line with gun ports, radeau, gunboat, bateau), boats moving along a path with the heading following the path, gunfire from a moving boat. Used in `arnold/scenes-src/m2a-m2d.js` (Valcour Island naval battle).
  - `arnold/tools/vk_kit.js` (from Grant): top-down ironclad gunboats and paddle-steamer transports.
  - Ocean-scale map example: `goosegreen/scenes-src/hook-atlantic.js` (task force across the Atlantic).
  - Ship guns: STYLE_LOCK 3a "Ships' guns firing → same K.gun → arc → K.impact from the ship's bow". Aircraft: `K.aircraft` (jet / turboprop / heli, shadows, shoot-downs, `down: t`), `K.bombRun` with shake. This covers carrier jets and Vietnam strikes.
- **Effects:** `K.badge` (round photo badge + name), `K.casualties` card, `GG.stamp`, `GG.card`, method card, `B.date` scroll, `B.stat`, `B.caption`, `K.target` rings, `K.smoke` (burning ship), `GG.night`, living map (`L.clouds`, `L.shimmer`, `L.scaleBar`, `L.north`).
- **TTS:** Kokoro-82M ONNX (`kokoro-onnx`, model files from github.com/thewh1teagle/kokoro-onnx releases), voice **`am_michael`, speed 0.95-1.0**. Free, runs locally on CPU, Apache-2.0 weights. This is the default from #16 on (STYLE_LOCK 2c-3: "keep this one"). Optional voice A = Chatterbox VC (MIT) conversion to an owner reference voice: `tts/setup_clone.sh` + `tts/convert_voice.py IN REF OUT` (~15-20 min, or ~2 h if it shares the CPU with renders; resumable chunks in `OUT.parts/`). Pronunciation workflow + dictionary: `tts/PRONUNCIATION.md`. Disclosure: YouTube "Altered or synthetic content = Yes"; the description says "Narration voice: AI-generated".
- **SFX kit (locked):** `goosegreen/assets/media/sfx/` + levels in `tools/sfx_mix_lib.py` KINDS. The base files are original numpy/scipy synthesis (`SFX_CREDITS.md`, no licence risk). The locked impacts are real recordings from freesound in `candidates/cand1-4_hit.wav` (credit line in the Arnold description: "artillery distance" by 2887679652 CC BY 4.0, Aegersum CC BY 3.0, juskiddink CC BY 4.0, Kostrava CC0). zoom_whoosh and prop_flyby are Mixkit (free licence). `*.wav` is git-ignored: copy them with `cp -rn goosegreen/assets/media/sfx/. <v>/assets/media/sfx/` and then run `check_sound_lock.py`. Table of levels: STYLE_LOCK §3.
- **Epidemic Sound:** an active owner subscription. Catalogue in `library/epidemic/CATALOG.md` (cannons, mortars, explosions, **"Naval Battle, Medium Bombardment" ambience**, 2 orchestral tracks), test tool `library/epidemic/tools/sfx_music_test.py`. The files are NOT in git ("the repo is public"). Safe only while the subscription is active and the channel is connected in Epidemic. The Epidemic Sound MCP is available in this environment.
- **Music:** Kevin MacLeod CC BY 4.0, "Long Note One" → "Wounded" → "Long Note Two" → "Anguish" (`goosegreen/assets/media/music_src_*.mp3`, `make_music_bed.py`), plus "Five Armies" approved. Mix: MUSIC_VOL 0.08, sidechain duck (thr 0.03, ratio 6, 20/400 ms), SFX ducked lightly, -14 LUFS, TP -1.5, AAC 192k (STYLE_LOCK §5).
- **Archive film recipe (directly transferable to Navy film):** `patton/assets/film/cut_clips.sh` (curl archive.org NARA items by identifier → ffmpeg scale + crop to fill 16:9, 30 fps, crf 20, no audio, 6-7 s clips) + `MANIFEST.md` table (clip, archive.org id, NARA title/id, in/out, what it shows, what it suits, **honesty notes** on what the footage does NOT show). `tools/restore_film.py` (vidstab, deflicker, denoise, contrast, `--tint` period grade; AI colourisation was rejected for false colours). `archive_shots.py` handles the "Netflix look": projector frame (`"frame": true`), 3D-depth photos (`"depth": true`), headline card, date cards, labels "PLACE · DATE". Credit line: "US Army Signal Corps / US National Archives". For Navy use "US Navy / US National Archives" or NHHC.
- **Credits process:** `<v>/assets/media/CREDITS.md`, one line per file: file | what | author | date | source page | licence | credit line. Good examples in `patton/assets/media/CREDITS.md` (LoC, Commons PD-USGov-Military; IWM rejected as non-commercial). Allowed: PD, CC0, CC BY, CC BY-SA. Never NC/ND, never untagged uploads, never a fake likeness.
- **Fact-check agent briefs:** `patton/research/FACTCHECK_B_bulge_move2.md` is the model: "Sources actually read" list (full-text archive.org OCR), then a table: # | dossier claim | CONFIRMED/CORRECTED/UNVERIFIED | correct fact / safe hedged wording | source + snippet. `FACT_NOTES.md` = corrections (biggest first), facts used per section, open items ("do not voice until checked"), a **"Packaging TEST claims"** table (every title/thumbnail word: verdict + source). Gemini brief sourcing rules: `research/GEMINI_BRIEF_v3.md` "Sourcing rules" 1-10 (citation per bullet; VERIFIED / SINGLE SOURCE / TRADITION / DISPUTED labels; ranges with who says what; quotes with recipient; superlatives need an exact source; only Commons files actually opened; end with a fact-check list).
- **Map/scene agent briefs:** `patton/research/AGENT_COMMON.md` / `arnold/research/AGENT_COMMON.md` (parallel-agent rules: only touch your files, no commits, no renders, one contact sheet, max 3 rounds, check flags/colours on every frame, grep every `B.at` phrase) + `templates/MAP_AGENT_BRIEF.md` (the older Morgan-era brief; its "detailed map style" tilt/satIntro part is obsolete).
- **Judge / critique loops:** (a) 3 independent judges with a shared brief, no reading of each other's files, verdict files (`research/REF_LOOK_JUDGE_BRIEF.md`, `MAP_COLOUR_*`, `STYLE_CRITIQUE.md`/`STYLE_IDEAS_REVIEW.md`, `ORANGE_EFFECT_*`: ideas → critique → review); (b) the post-render style audit (`arnold/build/AUDIT_STYLE.md`); (c) the topic study pipeline researcher → picker → YouTube-manager critic → meta-critic (`research/NEXT_COMMANDER_BRIEF.md`, `research/study/1-4_*.md`).
- **Competitor tooling:** `research/tools/yt_channel_scan.py @Handle [max]` (yt-dlp metadata + thumbnails → `research/competitors/<handle>.md/.json`, works without vidIQ), `topic_saturation.py`, `retention_from_frames.py` (reads retention from Studio screen recordings, within ~2 points). **Run it on @forgottenfleet1 first.**
- **Packaging templates:** `research/PACKAGING_GUIDE.md` + `research/LESSONS_PUBLISHING_AND_THUMBNAILS.md` (the PDF contents list, title/description/chapter/tag rules). Examples: `arnold/youtube/youtube_title_and_description.txt`, `chapters.txt`, `tags.txt`, `thumbs_feed_strip.jpg`, `sidebar_test_sheet_2x.jpg`; publishing PDF builder `arnold/tools/make_publish_guide.py`; thumbnail compositors `rokossovsky/tools/make_thumb.py`, `sherman/tools/make_thumb_interim.py`, `make_thumb_labels.py`.
- **Engagement code:** `lib/engage.js` (`E.subscribe`, `E.decide`, `E.final`) + `reference/engagement-examples/*.js`.
- **Clean-screen snippet:** `templates/clean_screen_v11.js` (labels leave after 3.5 s, colour dissolves).

---

## 3. Needs adapting (land → sea)
- **Terrain → bathymetry:** `bake.py` already reads AWS Terrarium tiles, which include ocean depth (sea colour ramps by `-elev/2500`: SEA (168,186,184) → SEA_DEEP (132,156,160)). For ocean shots, invert the emphasis: hillshade the sea floor (shelf, trench, reef site) and flatten the land. The Oriskany reef site (~24 mi off Pensacola, ~212 ft) needs zoom ~12-14 coastal detail. Terrarium bathymetry is coarse near shore; NOAA/GEBCO grids are a better source (public domain / free). The `SEA_BELOW` trick exists for polders. The `v11` look (sand ground, river belts) is land-specific; for a naval channel lock a new "sea-first" grade with one test sheet.
- **Unit counters/fronts → ship tracks:** use `B.arrow` / `B.line` (dashed) as self-drawing voyage tracks with a ship counter riding the path (`va_kit.js` path-follow pattern). Replace `K.front` and territory with a few things: ports, sea lanes, operating areas (Yankee Station), ranges (`K.target` rings, the range-ring helpers from morgan). Territory overlays (`make_control.py`) can still show who held which coast or sea zone.
- **Ship icons:** the existing art is sailing/ironclad era plus one modern side silhouette. A modern top-down carrier silhouette (Essex/27C angled deck), destroyers, a tug tow and a sinking animation (list, settle, bubbles, a wake fading) must be drawn as SVG in the va_kit style, constant on-screen size.
- **Flags:** period US ensign (48-star until 1959, 50-star after; the Oriskany was commissioned in 1950, so the 48-star applies until 1959). `make_period_flags.py` draws flags.
- **Commander badges → ship/crew badges:** a badge for the ship (official USN photo) plus captains/admirals; initials when there is no PD photo.
- **"Top 3 tactical moves" formula → ship-life arc:** build, career highlights, disaster (1966 fire), decline, fate. The method card and "What would you do?" card fit a decision (scrap vs reef, the 2006 sinking plan). The family-story final line fits naval veterans very well ("if someone in your family served aboard...").
- **SFX:** jets (`jet_flyby`), helicopters, gunfire, explosions are in the kit. Missing: ship horn, sea/wave ambience, steam catapult launch, arresting-gear trap, underwater rumble, the scuttling charges, hull groans. Get them from Epidemic (licensed) or freesound CC0/CC BY. Don't synthesize "ref" sounds (the owner rejected invented sounds, STYLE_LOCK 2c-5).
- **Archive:** WWII-era Navy film is on archive.org (NARA RG 428 Navy, RG 80; "111-adc" is the Army series). DVIDS (US government, PD; check individual items for third-party content), NHHC (mostly PD; some items are courtesy/copyrighted, check each one), Navy Visual News, NOAA (reef). Post-1970 colour footage makes the "projector frame + tint" look optional: test it first.
- **Gemini brief:** rewrite GEMINI_BRIEF_v3 sections for a ship: hull/class specs, commissioning/decommissioning dates, deployments with lat/lon, incidents with casualty ranges, the final disposition, and visual sources (NHHC NH-numbers, NARA IDs, DVIDS IDs with licence lines). Keep sourcing rules 1-10 unchanged.
- **Titles:** the "<Name>'s Top 3 Legendary Tactical Moves | The Man Who…" pattern was copied from the competitor Tactical Genius. For the new channel, copy forgottenfleet1's own winning pattern the same way (HANDOVER §10: "copy the winning competitor's pattern exactly").

---

## 4. Hard-won rules, owner decisions, style (quoted)
**Process**
- "Test before applying: show any new look/sound as snapshots or a 1-minute clip first; apply only after the owner approves." "Tests are small" ("All this for a test?").
- "Never render or upload without the owner's explicit OK in plain words" (sheets need no approval since 2026-10-29). Gofile needs an explicit OK. Some auto modes block Gofile uploads.
- "Everything lands on main". Commit and push at every milestone. The disk is ~1.5 GB free: never `git merge` all of main (2 GB). Use a worktree with `--no-checkout`.
- The cloud machine reboots every ~30-60 min and whenever the session is idle ~20 min. Start renders detached (setsid nohup), stay in the turn with <10-min waits, make every job resumable. Wait on a PID or done-file, never on a `pgrep -f` pattern. **Never `pkill -f` a pattern that matches your own command** (it killed the shell 3+ times). `setsid nohup … &` reports "Done" at once: check with pgrep.
- Usage limits stop agents mid-task: resume them with SendMessage (they keep context). Max 3 agents. Sonnet for search/download/sound/simple maps, Opus for main maps. Image agent before map agents. ONE contact sheet per round (opening single snapshots was "the biggest usage cost").
- Delete `scenes/*/snapshots` and `/root/.cache/hyperframes/history` (it grew to 9 GB). Rename old test scenes `test-*` (sfx_cues collects cues from every built scene).
- Renderer lessons: no CDN loads during render (all assets local, @font-face inline); register `window.__timelines["main"]`; no DOM measurement in timeline callbacks; camera clamped inside 2880x1620; never CSS attribute selectors on `style` (~10x slower renders); GSAP writes inline opacity, so fade layers with `filter: opacity()`.
- Network: Overpass fails through the proxy; Nominatim and Natural Earth work. Wikimedia blocks the IP after a while: send a UA, pause 2-3 s, use standard thumb widths (960/1280/1920), fall back to `images.weserv.nl/?url=upload.wikimedia.org/...` or the LoC API. vidIQ can only fetch YouTube/vidIQ-hosted image URLs.
- Script-format bugs (2c-7): "no `]` inside a `[MAP: ...]` tag … every spoken paragraph starts with its own tag (an untagged paragraph is skipped)". After any text change, grep every `B.at(...)` phrase (a missing phrase silently gives a bare map). `archive.json` is keyed by paragraph index: remap it after inserting paragraphs. After any timing change, run `assemble_full.py --audio-only` (sfx sync drifted 7 s once).
- Research quality: Gemini invented quotes, numbers and page numbers in every dossier (Patton ~12 corrections, Arnold ~15, Grant ~25). "Gemini's page numbers are not trustworthy." Three Sonnet fact-checkers against official histories are mandatory. Quote marks only on verbatim quotes. Superlatives need a source. Footage honesty: never label a clip as a place/person it doesn't verifiably show.

**Style (locked)**
- Open on an animated map, "never a photo". A clean first frame (units moving, nothing else). "Nothing appears on screen before the narrator says it." "One big card at a time" (legend/badges step out). "The date scroll NEVER disappears." Labels/captions leave after ~3.5 s (`LBL_LIFE = 3.5`). "Something new every 2-4 s, never more than 4 s without a change." Flat 2D map, no globe, no 3D tilt.
- Colours: hero blue `#1f4fc4` / enemy red `#c4121f`, front lines `#2c57b7`/`#bc2528`, night `#4a6a9a`/`#a8503c`, neutral `#77746c`, gold `#c9b48a`, text `#f7f3ea`. Font Oswald (labels/cards), Special Elite (date scroll). Vignette + grain, 1920x1080, 30 fps. Black outline on white card text.
- Sound: "the boom is always on the impact" (launches quiet). Every bombing run and shell hit shakes the screen. Aircraft sound only when an aircraft is on screen. The zoom whoosh only on the 2-3 biggest camera moves. "Artillery shots only where you can see them." No synthesized `ref:*` sounds.
- Archive: never a slideshow. The picture changes every 2.5-3 s; every photo moves (push-in/pan ~15-20 %); film fills 16:9 (crop, no bars); short "PLACE · DATE" labels. The amount is "moderate and quick": a background block after the hook plus ≤ 3 blocks of ~8-10 s, ~30 s total. "Long archive stretches lose viewers."
- Every move ends on a casualty card (real numbers only) or a RESULT card, then the method card. "Never invent figures."
- Rejected list: STYLE_LOCK §7 (globe openings, 3D tilt, flat icons, synthetic booms, NC/ND licences, Seed-VC, Chatterbox TTS cloning, music at 0.35, trees, country names under flags…).

---

## 5. Script / narration / title / thumbnail rules
- **Hook (STYLE_LOCK 1a):**
  - Line 1 = the STAKES of THIS story in 1-2 fresh sentences (~8 s), ending on the place name. "Never reuse another video's stakes sentence with the names swapped." Never date + place first, never a belief or background first.
  - Then the hard number + disaster.
  - "The title's promise is spoken as a result within the first 10-15 s"; visual payoff by ~0:25-0:30.
  - Camera dive by ~6 s, ONE continuous zoom (no cut/white flash) onto the place.
  - Twist shown as action; name slam + 3 snap cuts; hook ~60-65 s.
- **Opening rule (owner 2026-10-31):** "stay in ONE crisis story until the general enters as its turn (~0:45-1:00, one line, one human detail); never a CV, birth/schooling, achievement list … in the first two minutes; background <= ~20 s right before move 1." Proof: the flops (Gavin, Collins) switched to a CV at ~0:25 and lost 2/3 of viewers by 0:42. For a ship this means no "laid down in 1944 at Brooklyn Navy Yard…" résumé up front; open on the sinking/fire story.
- **Script must read cold** (1c-5): no dangling references, no repeated statistic, flashbacks say how far back. Spoken words only on cards.
- **Engagement (1b), exactly three beats:**
  - The woven subscribe line after part 1 in the "D2" pattern: close the section → the hard question part 2 answers → "That's the kind of question we answer here, and subscribing is how you catch the next one." → "Here's how…". "Never an order", written fresh each time.
  - One "What would you do?" card, before the reveal.
  - The final 1-2-3 question + family-story line ("We read every one").
  - Ending ≤ 45 s after the last result; the last ~20 s stay clean for the end screen. "NO spoken next-video pitch."
- **Pacing:** am_michael speed 0.95; 0.45 s between paragraphs, 1.0 s between sections. Write 2,400-2,700 words for 16-19 min (so ~2,100-3,300 for 14-24 min). Numbers-dense narration.
- **Titles:**
  - "Copy the winning competitor's pattern exactly." Thomas: only the title changed, CTR 0.9 % → 3.84 %, impressions 750 → 612k ("the title rule is our biggest lever").
  - vidIQ score ≥ 85, but "the pattern beats the score". ≤ 100 characters.
  - No negation hooks, no "forgotten / underrated / fired / almost" angles or nicknames. "Clear and true." Every title claim sourced in FACT_NOTES' Packaging TEST claims.
  - Launch with 3 titles (A locked format, B curiosity/famous-event, C hybrid) in Test & Compare; the owner picks the main one.
  - Note: "Why the Navy Sank Its Own Aircraft Carrier" is a curiosity title (type B): check it against FACT_NOTES ("sank" = scuttled as an artificial reef, 17 May 2006).
- **Thumbnails:**
  - 1-3 words, ALL CAPS, understandable with zero context, tension. Winning types: the hero's defiance, the enemy's verbatim words, ominous stakes. 4+ words and nicknames lose. Quote marks only on verbatim words.
  - Same promise as the title and the first 30 s.
  - Face pop (the subject, here the ship) + ONE recognisable context image + a torn red brush banner. Dark desaturated background, subject in colour. Check spelling, labels and stray insignia/symbols.
  - Show all variants on one sheet with a 168x94 feed strip. Compare with the sidebar: search the topic and beat the big videos' thumbnails. The Arnold lesson: the big videos write the NAME in big text on bright warm images, and ours (dark, small text, no name) lost at 2.85 % CTR.
  - vidIQ `generate_thumbnail` in two steps (dark scene, then the same image + subject + banner), 22 credits each. Credits ran out (0 until 22 Nov). OpenArt free plan watermarks outputs: don't use it.
- **Description:**
  - Line 1-2 = the script's hook. "NO links at all" (spam flags on new channels); name licences in words.
  - Chapters from timing.json: 0:00 first, each ≥ 10 s, no duplicate times.
  - Exactly 3 hashtags, 12-18 tags ≤ 500 characters, category Education, not made for kids, synthetic content = Yes. Business email as a placeholder for the owner to fill.

---

## 6. Known problems / open issues / what didn't work
- Loudness never lands at -14 on the first pass: -15 with peaky Kokoro, -12.7 with voice A. Always measure and trim.
- Renders are slow (9-13x real time) and die on reboots. `render_all.sh` vs inline builders conflict (use `render_direct.sh`). 4 parallel renders were no faster and crashed; render one at a time.
- `owner_ref.wav` is missing (voice A used `test_A_chatterbox.mp3` as reference). The depth model is not in setup.sh. `restore_film.py` must be copied into the skeleton or assemble fails.
- Wikimedia IP blocks left initials badges. Overpass is dead. The NHD service times out and is US-only (outside the US use WorldCover / DEM; check water by eye). Terrarium tiles stop at z15. The proxy drops tile connections (bake.py retries now).
- Map agents drift from the locked style: they thinned fronts to 8-10, used wrong-date overlays, dropped flags on frames, put flags over water or under the legend. The Arnold audit found 21 issues after render (hook too slow, cards before their words, end-screen space).
- An AI image showed forbidden symbols (Confederate flags) despite "no flags": inpaint them. AI faces don't match real people: never claim a likeness.
- The owner pasted the wrong research file twice: check the topic first.
- Open, not in the rules (`research/CONSIDERING.md`): the orange capture effect, using territory colours less, the 40-second formula, softening the last subscribe line.
- `templates/MAP_AGENT_BRIEF.md` has an obsolete "detailed map style" section (tilt, satIntro, thomas demo3). Ignore it.

---

## 7. Channel performance data / learnings
| Video | Impressions | Views | CTR | Notes |
|---|---|---|---|---|
| Thomas | 703k | 123k | 3.85 % | 0.9 % until retitled to the competitor pattern |
| Morgan | 240k | 45k | 4.06 % | AVD 6:17-6:22 |
| 2 Para | 180k | 39k | 4.55 % | broke out via Suggested on day 2 |
| Greene, Smith, Gavin, Collins | 2.4k-18k | — | 3.8-4.7 % | |
| Patton | — | 135 (early) | — | 48.2 % at 0:40 |
| Arnold | — | — | 2.38 % all sources, Browse 2.85 % | the click failed |

- 81-95 % of views come from Home/Browse. End screens are negligible (0.6 % CTR). Views are 96-99 % non-subscribers.
- **DATA_RULES (locked 2026-11-02):** YouTube judges a new video in two stages: (1) a day-1/2 test batch sized by channel momentum, then (2) expansion if watch time per impression (CTR × AVD) is ~18 s+ and Suggested CTR is ~3.5 %+. Results: Morgan 18.0 s and 2 Para 17.9 s expanded, Patton 15.2 s slow, Greene 12.7 s flat, Gavin 7.8 s and Arnold 8.2 s cut.
- Rules from that:
  - Publish the strongest videos back to back, 2-4 days apart; never follow a flop.
  - Write for minutes watched (AVD), not just 0:30. Each part opens on its own crisis and ends on a result + a question.
  - Win the Suggested sidebar.
  - Measure days 1-3 per traffic source with the standard Studio prompt (text in DATA_RULES.md). If Suggested CTR < ~2.5 % or watch time per impression < ~15 s, Test & Compare a new thumbnail first. "An untested video is not dead": re-test it when the channel is hot.
- Retention: ≥ ~64 % at 0:30 was necessary but not sufficient. The body is flat after 1:00 for every video, so each point held at 0:40 carries through. A 2:00-6:30 plateau at 38-39 % shows the maps hold viewers.
- Era signal: Civil War and Revolution won; WWII went 0/3 (crowded sidebar). A crowded topic is fine only if the thumbnail wins the sidebar (2 Para yes, Patton no). Prefer high-stakes stories that few big channels cover well.
- Studio AI is useful for single-number questions only; check its claims (it suggested false titles).
