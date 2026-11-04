# V02 sound pass (GOLD rules 65, 70, 99, 100)

Owner's note: V02 is "not engaging at all". The Depth Theory hit (research/depththeory-spermwhale-study.md section 4) has about 16 SFX/min in bursts, a signature sound and a bed that never goes silent. Before this pass V02 had about 21 graphic transients/min, all synth clicks and ticks. It had no environment, no real animal or nature sounds and no signature, and the music sat 20 dB under the voice. For the first 35 s after the drop (the rules section) there was no music at all.

## What changed
- `templates/mix_audio.py` mixes four stems, all levelled against the voice. The levels are fixed and no longer recomputed per chapter, so the bed that runs on across chapters never jumps at a join.
  1. **Environment**, cue `env:<name>`: a library bed looped seamlessly (2 s equal-power crossfades, random start). It ducks under the voice through the speech gate (sidechain) and rises in voice pauses. Defaults are `--amb-db -22` under speech and `--amb-gap-db -14` in pauses, which keeps it about 8 dB under the music bed. Leave `dur` out and the bed runs to the end of the chapter. Several env events crossfade over 1.5 s (0.3 s at chapter edges). During a verdict sting duck the bed dips by about 6 dB but never goes silent.
  2. **Things**, cue `el:<name>`: one ElevenLabs recording, peak-normalised and multiplied by `gain`. `dur` trims it, with a 0.8 s fade-out. It plays 3 dB lower under speech. Default level is `--things-db +2`. The files come from `--el-dir` (default `videos/video02/sfx_el`), falling back to `templates/tests_anim/sfx_el`.
  3. **Mood**: the music bed, `heart` (one beat, or with `dur` a heartbeat that speeds up from 72 to 112 bpm), `hit` (deep hit), `boom`, `el:deep_boom`, `el:heartbeat`, the stings `duck`/`riser`/`vhit` (unchanged; still 4 full stings) and the signature.
  4. **Graphics**, synth only: `tick tok ticks(dur) ticks_up(dur) beep(dur) thud thud_soft click scratch marker swoosh shimmer title stamp snap ding*`. A gain-1 cue peaks at `--sfx-db +6` re the voice RMS, which is close to what the old per-chapter normalisation gave (+9 to +15). `tick` is now the bright count-up tick from tests_anim (`V.tick2`).
- Identical events (same cue within 15 ms, e.g. two swooshes stacked on one build) are merged.
- `--stems` writes `audio/stem_voice.wav`, `audio/stem_sd.wav` and `stem_gate.npy` for level checks. The temporary music and voice wavs are deleted after use.
- `templates/sfx_voices.py` gains (additions only) `tick2 ticks beep shimmer marker heart heart_run hit`, ported from tests_anim `make_tests.py` (CUE) and `make_test4.py` (heart).
- `mix_all.sh`: the music never stops. The hook score plays until the drop, then 0.6 s of silence and black (rule 30), then the lo-fi bed fades in during the rules section and continues as one slice through the end screen. The lo-fi bed is now at `-14/-6` (was `-20/-12`). Folders are configurable (`WORK REND OUTD OUT`). `build_final.sh` calls it for its mix section, so drafts and the final use the same chain.
- Loudness is still set by `templates/mux.sh` (loudnorm two-pass to -14 LUFS, ebur128 trim, alimiter at -1.5 dBFS sample peak). That file is unchanged.

## Sound library (`videos/video02/sfx_el/`, ElevenLabs sound-generation v2, key ~/.el_key2)
Cost measured at about **10 credits per generated second** (22 s bed = 220 credits). This pass spent **4,505 credits** (character_count 4,570 → 9,075; 25,727 left for V03).
- **Beds** (25 s, generated with `loop: true`, then highpass 35 Hz, dynaudnorm, gentle compression and limiting so no call pokes out):
  - `env_mangrove` (hook/rules, modern croc river)
  - `env_coal` (ch01: drips and big insect wings; no birds, no frogs)
  - `env_floodplain` (ch02: wind and a wide river)
  - `env_hellcreek` (ch03 and the outro: dusk river, frogs, birds)
  - `env_monsoon` (ch04)
  - `env_billabong` (ch05)
  - `env_lakeshore` (ch06)
  - `env_temperate` (ch07, warm Thames)
  - `env_thames_cold` (ch07 winter, the ch03 14 °C gauge, S19)
  - `env_cerrejon` (ch08)
  - `env_coast` (ch09: surf, no gulls)
  - `env_sahara_river` (ch10)
  - `env_amazon` (ch11)
  - `env_kemkem` (ch12)
- **Things**: `splash_small splash_big croc_lunge jaws_snap reeds_rustle mud_squelch bones_crack insect_wings thunder rain_burst steps_mud steps_giant roar_theropod croc_bellow croc_hiss croc_headslap croc_headslap_b snake_slide hippo_grunt lion_roar_far sink_bubbles death_roll fire_crackle ice_crack fish_splash lizard_hiss`. The tests_anim files are still available as fallbacks: `footsteps_wet leaves_rustle birds_flap branch_creak torch_click sub_boom jungle_bed`.
- **Mood**: `heartbeat` (slow, recorded), `deep_boom`.
- **Signature**: `sig_frost` (plant and returns), `sig_frost_b` (softer return), `sig_frost_big` (payoff). These are compressed so the sparse crackle reads.

## Signature: frost crackle (the cold is the real enemy)
- **Planted** under H13, "And the one river where nothing even has to fight it?", as something "you" hear with no picture change. The old synth `icecrunch` at H13 stays under it.
- **Back** at:
  - ch03 S06 "Below that", over a light cold-wind bed
  - ch03 C03-19 "Remember that number"
  - ch07 C07-13 "Fourteen degrees"
  - ch07 S11 "gets cold"
  - ch07 C07-21 "Florida cold snap"
  - ch07 S12 "In winter"
  - final "Because of the winter"
- **Paid off** in S19, "It was the cold.": the big crackle starts 0.4 s before "cold" while a winter-wind bed rises.
- Fact-check of the crocodile-call alternative, which I dropped:
  - The low-frequency bellow and its infrasound "water dance" (subaudible vibration, SAV) are well documented in American alligators. SAV is also documented in the American crocodile (Herpetological Bulletin 170, 2024; Garrick & Lang 1977).
  - For *Crocodylus porosus*, the field recordings describe headslaps, growls, hisses, roars, narial geysering and bubble-blowing (UniSC / Australia Zoo project, 2024). Sub-audible vibrations are still on that project's wish list, not recorded.
  - The headslap is ancestral to crocodylids (Senter 2008).
  - So a true sound for our saltwater croc would be the headslap plus growl, not an infrasound bellow. The script has no line that pays a croc call off out loud, while the frost crackle is paid off by "It was the cold." The headslap stays in the library as a "things" sound (`croc_headslap`, used on "strongest bite" and on rivals).

## Events (`fixpass/sound_<chapter>.json`, merged by make_plan.py as `extra_events`)
- One environment bed per river runs over the whole chapter. ch00 has two beds around the silent drop, ch07 crossfades from the warm river into cold wind before "Hippos are fine", and the outro goes from the dusk river to winter wind under S19 and back for the end screen.
- Things land on the line or shot that shows or says them (word specs `wNNN`): bites → `jaws_snap`, fires → `fire_crackle`, Allosaurus and T. rex → `steps_giant` + `roar_theropod`, Megalania → `lizard_hiss`, Titanoboa → `snake_slide`, hippos, lions, and so on.
- Heartbeats sit on tense beats: the Allosaurus bank, "who's already here", the hippo's own heat, winter coming, Titanoboa's wrap, "eight times heavier", "our croc is food here", the S17 lock-on and "another predator".
- `el:deep_boom` plays only on the 4 big reveals (Deinosuchus, SuperCroc, Purussaurus, "this guy" = Spinosaurus), plus one soft one on "it probably ate them" (S10, as planned). The stings are untouched.
- The scenes in plan.json emit their own graphic sounds through the blocks (ticks, hits, shimmer, beep, click, scratch, marker, swoosh). The sound files add only environment, things, mood and the signature around them; plan.json's per-scene things/mood items are covered here.

## Measurements (scratch build, `--no-media`, voice = narration_full.mp3, the real mux.sh chain on dummy video)
Sound design (SD) = music + ambience + things + graphics. LUFS was measured with ffmpeg ebur128 on the stems, "under speech" = speech gate > 0.5.

| chapter | voice over SD, under speech | voice over SD, whole chapter | SD in pauses vs under speech | final integrated | true peak | clipped samples |
|---|---|---|---|---|---|---|
| ch00 (hook score + bed) | 13.7 LU | 11.6 LU | +3.8 LU | -14.2 LUFS | -0.7 dBFS | 0 |
| ch01 | 12.2 LU | 9.4 LU | +4.9 LU | -14.2 LUFS | -0.7 dBFS | 0 |
| ch07 | 12.1 LU | 9.8 LU | +4.0 LU | -14.2 LUFS | -0.8 dBFS | 0 |

Before this pass (old levels, ch01): 18.4 LU under speech and 15.6 LU whole, so the voice was nearly dry.

## Checked by looking at waveforms and levels (no listening possible)
- Per-file analysis of the library:
  - Durations match the request.
  - No bed has persistent tonal peaks (a music check). The exception is a whistling-wind band of 2-6 kHz in `env_thames_cold`, which is expected.
  - Loop seams are handled by the crossfade looper. A 70 s loop of the spikiest bed has no gaps.
  - The heartbeat shows lub-dub pairs every 1.5 s.
  - The headslap shows a hard transient followed by a growl.
- ch00: the sound design is exactly silent in the 0.6 s drop and back after it. Its lowest level elsewhere is -42 dBFS, so the bed never goes silent.
- ch01 and ch07: the per-second SD level never drops below -38 dBFS, including during the sting ducks (-34 and -26 dBFS).
- No clipped samples after mux.sh. Integrated loudness is within 0.3 LU of -14.
- Every cue in all 14 built chapters resolves to a synth voice or a library file.
- `fixpass/sfx_density.py` counts the density (see below).

## Density (`python3 fixpass/sfx_density.py [WORK] --extra-anim 6.5`)
- Raw events: 29.8/min.
- Perceived sounds (a same-cue run under 0.2 s apart counts as one): 27.0/min.
- Of that, this pass adds about 8.6/min (things + mood + signature). The rest is the existing block graphics (~19 perceived/min, mostly label clicks, board ticks and swooshes).
- With the ~19 animation scenes it comes to about 31 perceived/min. Some of their graphics replace the clicks of the 56 cut shots.
- The minutes run 20-35, so there are no truly calm minutes yet. To reach rule 100's average of ~16 with calm minutes near 4, the block graphics have to thin out (one click per label group, no swoosh + click on every map label), not the real sounds.
