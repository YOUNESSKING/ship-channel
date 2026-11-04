# House style (approved on Test 2 v9, Oct 2026)

These are the decisions made while building Test 2. Follow them on every video unless the owner changes them.

## Format
- Fossil-like premise: "How long would YOU last in every ___?" or "Could X beat every Y?"
- Hook (about 30 s): cinematic, 2 s cuts, music builds, then a **hard drop to black and silence on "Let's find out."**
- Body: a relaxed lo-fi beat. The narration is a friend thinking out loud: deadpan, dry jokes, written-in "uh"s and restarts.
- Each chapter: the good news, then a catch at the end of the line, then a verdict.
- The **tier list appears only at the end of a chapter**, when the tile drops into place. **Never show an empty tier list mid-video.**
- Research guides: `research/fossil-style-bible.md` and `research/fossil-deep-study.md` (the "feeling engine").

## Voice
- ElevenLabs **v4, voice "Will"**, with acting tags such as `[deadpan]`, `[sighs]`, `[pause]`, `[thinking]`, `[flat]`.
- Write disfluencies and pauses into the script text itself.
- Commercial use needs a paid ElevenLabs plan.

## Visuals
- **Every shot proves the words being said**, so no generic mood clips.
- **Clip sources, in order** (owner's decision, 24 Oct 2026; tests in `research/free-model-test/`):
  0. **Always vidIQ Seedance 2 Fast** for the **hook** (the first ~30 s, every clip) and for **hero shots** (the 1-3 key wow moments per chapter, plus the thumbnail moment). These need the best quality, so they skip the cheaper models.
  1. **Main for everything else: Wan 2.2 Lightning**, self-hosted on RunPod with `tools/runpod-wan22/`. About $0.10 per clip, about 4 min. Batch all of a video's shots in one GPU session.
  2. **If Wan fails** (most likely on fast or dramatic action): try **Seedance 1.5 Pro** and **Kling 2.5 Turbo** on fal.ai with `tools/fal_dramatic_test.py`, and keep the better one. They cost about $0.13-0.25 and $0.35; use only Kling's best 2-3 s.
  - **Learned on Video 01:** animals in motion and people go to **Kling 2.5 Turbo Pro first** (it fixed all 5 shots Wan failed, first try). **One species per shot:** never ask for two different animals in one clip; split it into two quick cuts.
  - **Species drift:** video models (Wan, Kling, even Veo 3.1) turn a specific species into a generic one after 1-3 s (leopard seal -> ordinary seal). For species-critical shots: use only the first 1-2 s before the drift, or the correct start image as a still with a slow camera move. Don't pay for premium video models to fix it (Veo 3.1 about $1.20 per 6 s clip: too expensive, and it drifted too).
  3. **If those fail too:** use **vidIQ Seedance 2 Fast** (140 credits). It was the clear winner on the orca breach.
  - Realistic documentary look. Animals never pose or face the camera.
- **Channel colour grade: B "Deep Time"** (owner choice, 27 Oct 2026): teal shadows, warm golden highlights, a little more contrast. Applied automatically to every clip by `templates/build_chapter.py` (`templates/grade/`); maps, text, stick figures are not graded. Starts with Video 02.
- **No film look.** No grain, blur, tint or vignette; clips are shown full and clean.
- **No clip appears twice in a video**, and that includes two crops of the same clip.
- **Text overlays get their own fresh clip** that relates to the line, shown dimmed rather than blurred.
- **Check `library/` before generating.** Save every new clip there with its prompt, and update `used_in`.
- Stick-figure gags stay, as simple white line art.
- **Quality check in batches of 50:** every clip and start image is checked one by one before the edit (KEEP / TRIM to the usable part / REDO). See GOLD_STANDARD.md rule 34. **Check while the batch is still generating** and send REDOs straight back to the running machines. The checker is a separate Sonnet (minimum) helper, never the one that made the clips, looking at 8-10 frames per clip minimum. Quality over everything. **Then the owner double-checks every kept clip** in labelled review videos before anything goes into the edit.
- **Tease every 60-90 s** with a deadpan joke or a striking era animal (cave lion, sabre-tooth, short-faced bear, Megalania...); out-of-era animals like dinosaurs only as a named joke with the EXTINCT plate. See rule 35.

## Start images (owner's decision, 26 Oct 2026)
- **Z-Image Turbo** (Tongyi-MAI, Apache 2.0) on a rented GPU replaces Seedream: about 7 s and $0.002 per image (about $0.60 per video). Tools: `tools/runpod-zimage/` (setup.sh installs it; worker uses 9 steps, guidance 0, 1664x928).
- Because it is so cheap, **check every image before it becomes a clip and retry any weak one** (new seed or a fixed prompt), as many times as needed. Seedream ($0.04) stays as the fallback for an image Z-Image can't get right.
- **Tricky animal anatomy** (hyenas, unusual Ice Age animals): make the start image with **Seedream 4.5** on fal (about $0.04); it beat Z-Image on the cave hyena.
- Tested and rejected: Qwen-Image, HiDream-I1, FLUX.1 Krea/dev. Z-Image Base works too ($4.80 per video, 88 s per image).
- Setup gotcha: uninstall the base image's torchaudio before installing new torch/diffusers, or diffusers fails to import.

## Spending money or credits (owner rule, 27 Oct 2026)
- **Ask the owner FIRST before ANY spend that wasn't already agreed for that exact task** (fal, RunPod, vidIQ, ElevenLabs, any paid API). Say the service, what it's for, and the exact amount. Never give a helper a budget for a paid service the owner hasn't approved for that task.
- Agreed spends must stay inside the agreed amount; if more is needed, stop and ask.
- Report the balance after each paid job.

## Renting machines (owner rules, 26 Oct 2026)
- **Price cap:** never rent above **$0.89/h** per machine for this work. If cheap ones are sold out, use fewer machines and wait.
- **Keep scouting:** while a batch still has more than about 45 min of work left, check for newly available cheap machines every 5 min and add them (a new machine needs about 20 min of setup, so near the end it is not worth it).
- **Reuse machines between tasks:** if the next task on the same type of machine starts within about 20-30 min, keep the machine, clean it (delete old outputs/models it doesn't need) and start the next task on it, instead of deleting it and renting a new one (saves the 10-20 min setup and its cost). Delete it when there is no next task soon.
- **Only touch your own machines:** a launcher or driver must only delete machines it launched (by id or name), never "all pods on the account".

## Pipeline: never wait for a whole step (owner rules, 26 Oct 2026)
Each piece moves on the moment it passes its check; nothing skips a check.
1. **Image -> clip right away:** each start image goes to the Wan machines as soon as it passes its image check (bad images are retried first). The L40S machines make the images too, so no separate image machine is needed.
2. **Check while generating** (rule 34): REDOs go straight back to the running machines.
3. **Build a chapter as soon as all its clips pass** (KEEP or TRIM). A chapter with a REDO waits for that clip; the others keep going.
4. **Render a chapter as soon as it is built** and its still-frame check looks right, on a rented render machine.
5. **Rent GPUs about 20 min before they are needed** (e.g. while the shot plan is finishing), so setup is done when the work starts.
6. **Write the publish pack** (title, description, chapters, thumbnail) while the final 1080p renders.
Later: a ready-made machine image with all software pre-installed (cuts 5-8 min per machine); start the next video's research and script while the current one renders and gets reviewed.

## Text: style C, "nature-doc cinematic"
- Cormorant Garamond 600 in warm white (#F6EFE0) for titles and numbers, italic for words like *minutes*.
- Jost caps with wide tracking for small kickers.
- Gold #C9A45C hairline rules. Asides are gold italic subtitle lines.
- Letterbox bars only on big title moments. Slow fades, no bouncing.
- No red, no heavy outlines, no meme fonts.
- The EXTINCT stamp is a gold-framed plate.
- Sources: `videos/test2/build/` (style C), with fonts in `textstyles/fonts/`.

## Maps
- Made with the battle-maps map-kit (copy in `maps/`), but with **style C typography**: no Oswald, no parchment date scroll, no boxed captions, no date banner.
- Ice grows **gradually over the land** (per-pixel, relief visible). **No ice on the water**: the ocean darkens instead.
- The sea-level change gets the **gauge animation**, counting 0 down to −120 m in sync with the coastline change.
- No label collisions. Credits read "Terrain: Mapzen / AWS Terrain Tiles · Ice extent approximate".
- Tools: `bake.py`/`bake_hd.py` with `SEA_LEVEL`, `make_ice_progress.py`. See `maps/README.md`.

## Sound
- Self-made score (royalty-free, owner's choice, confirmed 26 Oct 2026): hook strings and drums with a drop to silence, body lo-fi (templates/make_lofi_bed.py). No library music needed.
- SFX on cuts, stamps and tier drops. Loudness about −14 LUFS.

## Packaging promise (owner rule, 27 Oct 2026)
- Title + thumbnail + video are ONE promise. Every thing the thumbnail shows or says (the creature, the threat, the number) must be in the video, and the main promise must be paid in the first 30-60 s; otherwise viewers click away. Before upload, write down the timecode where each thumbnail element appears (in the publishing PDF).

## Delivery
- Final renders at 1080p (tests were 720p).
- Tick YouTube's "altered or synthetic content" box when realistic AI scenes are used.

## Style review additions (29 Oct 2026)
- Verdict: big tier word (Cormorant, warm white, gold underline, ~12% of frame height) on the verdict word, then the board (GOLD rules 64-65).
- Gold #C9A45C is the only pointing colour in-video: hand-drawn circle, measuring bracket, highlights. Red stays in the thumbnail and the "Wiped out" tier colour.
- Size charts reveal in order: known first, giant second, bracket, number last (rule 67).
- Ending: on the finished board, no separate end card (rule 80).
- Thumbnails: our warm red/black/orange look, Anton text in post (white + one red word), no googly eyes, no engraving style.

## Production checklist (30 Oct 2026)
Follow GOLD_STANDARD rules 82-94 on every video: one fact sheet; count "okay" before recording; thumbnail planned with the script; real footage first, one stock list and one download; one test per tricky species; state every cost first; the shot-list gate (era, repeats, 1080p, no placeholders) before any render; hook approved first; short review reels; renders on rented machines; commit after every step.

## Animation and sound design (LOCKED 30 Oct 2026, GOLD rules 95-101)
- Animation = third picture source for what cameras can't film; gold line-art on a dark ink background in the colour of the video's world (V03 jungle = green-ink, V02 rivers = warm river-mud umber; chapter key `anim_theme`), layered greens for nature, hero animal in true colours; never deep blue, never a flat-vector Depth Theory / BTB copy.
- "You" = our simple stick figure; supporting cast = stick figure + one prop; modes: backlit, gold X-ray, tiny crowds.
- Motion: snap in 0.3-0.5 s, slow drift, constant small motion, count-ups land with flash + gold ring + deep hit, mini scenes for joke lines, lists with gold box and strike-through.
- Sound: four layers (environment, things, mood, graphics), ~16 SFX/min in bursts, one signature sound, voice ~11-12 dB over the bed, ElevenLabs sounds for nature/animals, synth for graphics.
- Reference tests and code: templates/tests_anim/ (make_tests.py, make_test4-7.py, out/ALL_TESTS.mp4, out/test6_cast.mp4, out/test7_voice_sound.mp4).
