# Oriskany full video: build report v8, the Archive voice (2026-11-10/11)

**Output:** `videos/oriskany/full/oriskany_full_v8.mp4` (git-ignored, 1.08 GB). H.264 1920x1080, 30 fps, **25,507 frames, 850.23 s
(14:10.2)**, AAC stereo 48 kHz 192k, audio = video length. Narration 832.23 s + the 18 s end screen (v7: 847.6 + 18 = 865.6 s).

v8 = the whole video re-voiced in the owner's designed voice "Archive" (CLAUDE.md "Voice", owner 2026-11-10), every shot, card,
label, map, animation and sound cue re-timed to the new words, all seven chapters re-rendered, and a fresh mix through the locked
v2 chain with the 2026-11-08 SFX levels. Same text (`script/NARRATION_v3.txt`, ending cut option A), same pictures, same music.

## 1. Voice (`build/voice.py`, `build/PRONUNCIATION_GATE_v8.md`)
- Kokoro style blend bm_fable 0.40 + am_michael 0.40 + bm_lewis 0.20 (`tts/voices/archive_style.npy`, `voice=np.load(...)`),
  speed **0.92**; questions **0.852** (= 0.92 x 0.88 / 0.95, the am_michael take's relative slowdown). 225 chunks, same pauses
  (0.3 / 0.6 / 0.9 s), the hook keeps its approved phrase splits and pauses. Out: `audio/voice_archive.wav`.
- Pronunciation: the old fixes (Oriskany, Okaloosa, porgies, MiG) plus three new ones from the gate (Essex class, "Her keel",
  "but her sinking") and one borderline ("towed", 7:18). Names clip: `videos/oriskany/voice_sample/names_archive.mp3` (22 s).
- The raw Archive chunks peak up to +2.3 dBFS and had clipped in the 16-bit chunk cache (36 samples). Chunks are now cached as
  float and the whole take is scaled by 0.5 (-6 dB; the mix normalises the voice to its locked -29 LUFS, so the level does not change).
  The 8 clipped chunks were re-voiced: identical lengths, so no word moved.
- Word timings: faster-whisper **small.en** (base.en put words up to ~0.5 s off around spoken numbers), aligned to the script words
  (sequence match; a number heard as digits is spread over its digit tokens), then snapped to pauses inside sentences (whisper
  stretched "charges | inside" over the pause). The v7 timings are kept in `build/words_v7.json`.
- faster-whisper failed on files with `open() got an unexpected keyword argument 'metadata_errors'` (PyAV 19 dropped it):
  fixed with `pip install av==15.1.0` (faster-whisper 1.2.1 is the latest and still passes it).

## 2. Re-time and rebuild
- `build/warp_v8.py`: a monotonic v7 -> v8 time map on every word start/end (the two word lists are identical). Used only where
  earlier builds wrote absolute seconds: the v2-v7 cue rules in `sfx_full.py` (whoosh/riser keeps, moved horns, S5 drops, V6/v7
  per-cue trims), `music_bed.py` (loop point, the "Then she was gone" dip, outro entry), `snr_words.py` regions, the reuse report.
  Everything else is word-anchored and was simply regenerated: `make_shotlists.py` (222 shots c02-c07), `make_anims.py` (34 hero
  scenes), `mk/tools/render_maps.sh` (46 maps; the two plan-only scenes c07_storm/c07_reefpin are not on screen and fail on the new
  words, as expected), `make_segments.py` (107 film/photo + 15 still segments), `render_all.sh` c01-c07.
- **Hook** (`build/hook_v8.py`): the approved test-v4 hook, shot for shot and look for look, re-timed: each cut keeps its lead on
  the word it lands on; each test-v4 clip is re-timed to its new shot length (linear per shot, plus a knot on the baked event:
  dive "Gulf", hull touchdown "floor?", end-map "thirteen"); clip speeds 0.84-1.35x (only s07, the 22-charges photo push, is
  above 1.1x). Clips in `segments_hook/`. Cuts sit half a frame after the frame time, as test v4's did: on the exact frame the
  render lost the first white frame of the 2nd blast flash (fixed, checked frame by frame). The hook now ends at 48.98 s (v7 48.63).
  c01 is rendered by `render_all.sh` like the other chapters (`mix_full.py` now joins `render_c01.mp4`; `HOOK_SRC=test_v4`
  gives the old picture).
- Sound: 108 cues (as v7), 70 bed segments, sync max 1.2 frames. Changes beyond the re-time, all cuts or moves only:
  - hull thump (impact, hook): it landed on "floor?" (28.77 s) where the softer Archive "floor?" ducks the punch bus, and the lock
    measured the beat +0.4 LU over speech (+0.3 on the stern-touch frame). Moved to **29.133 s**, the frame the re-timed hull
    settles flat on the seabed, just after "floor?" in the voice gap: **+2.2 LU**. Level and lowpass unchanged.
  - groan @26.1: -6 dB (was -3), jets @233.5 and @320.6: -6 dB (were -3), for the Archive words "to", "for", "the" (see 4).
  - lock (`tools/sound/check_sound_lock.py`): the one-off hook-blast gap-carry exception now also names the same cue at its v8
    time, 17.167 s (it still ends before the next word, "Thirty"). CLAUDE.md still says 17.65 (v7 time); not edited.
- Music: unchanged tracks, levels and crossfades; switch points moved with their words (loop 353.7 s, tension at the c06 start,
  outro 791.8 s, -12 dB dip 528.2-530.3 s under "Then she was gone").
- MANIFEST.md / CREDITS.md regenerated (`build/paperwork.py`; narration credit now names the Archive blend). Note: the hook rows
  of MANIFEST still give test-v4 reel times (the clips are the same, only re-timed).

## 3. Checks (all pass)
| check | result |
|---|---|
| `templates/check_safe_text.js` (every chapter, 0.5 s) | **PASS** c01-c07 (`chapter/safe_c0*.txt`) |
| `check_sound_lock.py` static + render | **SOUND LOCK OK**: -14.0 LUFS, TP -1.7 dBTP, LRA 1.9 LU (floor 1.7), linear loudnorm, music under speech -24.1 dB, 10 big beats >= +1 LU (min +2.0), 108 cues within 3 frames, every cue silent by its shot end, 70 beds on cuts |
| loudness, ebur128 on the mp4 (`build/ebur128_v8.txt`) | **-14.0 LUFS integrated, true peak -1.7 dBFS (<= -1.5), LRA 1.9 LU** |
| `tools/film/check_clips.py --no-cuts` (`build/check_clips_v8.txt`) | 99 BLOB + 10 FLASH: the same pattern as v4-v7 (drawn dark boards / card shades; flashes = the two hook blasts 3.93 + 17.20, the c05 "they fired" flash 516.2, and the bright/dark cuts at 92.5, 96.0, 211.4, 236.7, 312.4, 349.6, 773.9) |
| blackdetect 0.25 s / 0.06 | none (`build/blackdetect_v8.txt`) |
| shots over 6 s (`build/check_numbers.py`) | **0** (longest 5.8 s); 2 short shots < 1.2 s as before (Panther 1.04 s, "they fired" flash 1.02 s) |
| numbers land on their words (`build/check_numbers_v8.json`) | **48 numbers**, each resolved on its spoken word by the chapter builder's own resolver, all inside their shots (the 37 count lands on "seven" +0.15 s as approved) |
| clip / photo reuse | clean (`build/shotlist_report.md`) |
| `FINAL_SHEET_v8.jpg` (one frame every 10 s) | looked at: every frame is the intended shot, no black, no stray text, the end screen holds the map |

Big beats over speech (LU): 3.93 +3.6 · 10.10 +4.0 · 17.18 +2.6 · 19.48 +3.1 · 29.13 +2.2 · 516.21 +2.9 · 533.48 +2.0 · 791.00 +3.9.

## 4. Speech-band SNR (1-4 kHz, voice bus over the effects buses; `build/snr_words.py` -> `build/snr_v8.json`)
| place (v7 name) | v7 min word | **v8** words |
|---|---|---|
| hook "she was gone." (splash) | was +2.4 | she +14.2, **was +4.5**, gone +16.1 |
| groan "millions to put" | millions +5.8 | millions +7.1, **to +3.1** |
| thump "sea floor?" | floor +7.0 | **floor? +3.3** (the thump now follows the word; the residue is the waves/underwater bed) |
| whoosh "About thirteen" | | min +15.0 |
| jet 1 (12,000 sorties) | more +8.1 | flew +3.0, more +9.5 |
| jet 2 ("record for one carrier") | one +3.4 | **for +1.0**, one +12.9 |
| jet 3 ("of the pilots") | the -2.8 | **the +1.6** |
| flood "Then she was gone." | was +6.9 | was +10.5 |
Still under +3: "for" (+1.0) and "the" (+1.6): both 0.1 s function words; the critic's target was +6 (not a lock rule). The next
step, if wanted, would be removing those two jet cues.

## 5. Description and upload kit
Chapter times regenerated from `chapters.json` (`build/desc_times.py oriskany_full_v8.mp4`) in `YOUTUBE_DESCRIPTION_DRAFT.md`,
`upload_kit/upload_kit.html` and its PDF: 0:00 Hook · 0:48 Nobody Wanted Her · **2:55** The Mighty O · **5:53** The Bargain ·
**7:55** Thirty-Seven Minutes · **9:15** The Fish Test · **11:13** The Real Reason. Length 14:10. The kit's "Publish by 9 November"
line is unchanged (owner decision pending; see 6).

## 6. Re-voice the SS United States lines (after 12 November)
Lines that will change: `NARRATION_v3.txt` line 9 from "On November twelfth, the ocean liner SS United States is scheduled to follow
her down. About thirteen nautical miles away." and lines 123 ("... Okaloosa County plans to sink the SS United States. She will lie
about thirteen nautical miles from the Oriskany.") and 125 ("And here is the twist. ... Now it is about to take her title.").
Narration spans now: 40.13-48.53 s (hook) and 800.50-821.70 s (c07).

**Fast path (the new sentences fit their old slots, nothing else moves):**
```
cd videos/oriskany/full
# edit script/NARRATION_v3.txt (keep paragraphs; keep "The answer is buried ... And it matters right now." in line 9)
python3 build/revoice_lines.py            # dry run: each changed run vs its slot (up to 6 % time-compression allowed)
python3 build/revoice_lines.py --write    # writes audio/voice_archive.wav, build/words.json, build/chunks.json
python3 build/voice_gate.py small.en      # pronunciation gate on the new take
python3 build/make_shotlists.py && python3 build/hook_v8.py
(cd mk && RERENDER=1 bash tools/render_maps.sh c07_okaloosa c07_endmap c07_title)   # maps timed to these words
ARCHIVE_GRADE=ship python3 build/make_segments.py f_c07_s37.mp4 f_c07_s40.mp4 p_c07_s41.mp4
nohup bash build/render_all.sh c01 c07 > build/render_ssus.log 2>&1 &
MIX_WORK=/dev/shm/oriskany_mix JOIN_PATH=/dev/shm/joined_silent.mp4 nohup python3 build/mix_full.py > build/mix_ssus.log 2>&1 &
python3 build/check_numbers.py && python3 build/desc_times.py oriskany_full_v8.mp4
```
(A dry run with "...followed her down." / "...Okaloosa County sank the SS United States." fits: 4.93 s in a 5.85 s slot, 6.95 s in 7.65 s.)
If a new paragraph is longer than its slot, `revoice_lines.py` stops: then run `python3 build/voice.py` (re-voices only the changed
chunks from its cache, every later word moves) and the whole of section 2 again (shot lists, hook, maps, heroes, segments, all
renders, mix), about 3 hours.

**Shots that depend on these words** (change the text on them if the facts change):
- hook: c01 s18 `gulfpin.mp4` (Pensacola pin, 38.2-40.1), s19 `f19_stacks.mp4` (liner film, 40.1-42.1), s20 `f20_bow.mp4` lower third
  "1968 FILM / SS UNITED STATES" on "United", s20c `f20b_profile.mp4`, s21 `endmap.mp4` (46.1-49.0; **baked labels "SS UNITED
  STATES · NOV 12" and "13 NAUTICAL MILES"** from test v4: a new date or distance needs that map re-made in `test_v4/mk`).
- c07: s37 number card **"NOV 12" / "10 A.M. · WEATHER PERMITTING"** on "November" (`f_c07_s37.mp4`, 800.4-804.4), s38 map
  `m_c07_okaloosa` (804.4-808.3), s39 map `m_c07_endmap` (808.3-812.4, the SS United States pin + "13 NAUTICAL MILES"), s40 film
  (812.4-814.2), s41 number card "$50,000 / OKALOOSA COUNTY'S SHARE" on "fifty" (814.2-819.4), s42 map `m_c07_title`
  ("PLANNED · LARGEST ARTIFICIAL REEF", 819.4-822.2) and the end screen map `m_c07_endscreen` (SS United States pin).
  Card texts live in `build/make_shotlists.py` (c07 beats); map texts in `mk/scenes-src/c07_*.js`.
- sound: the liner horn at 799.8 s (in the voice gap before "On November twelfth", `sfx_full.py` v4 rule) and the "the answer" boom
  at 791.0 s; both re-place themselves from the new words.
- description: the first paragraph and the kit's "Publish by" line mention the sinking date.

## 7. Disk
Deleted (all rebuildable): old chapter renders, `chapter/work`, `chapter/media_cache`, the HyperFrames extract cache and
`/root/.cache/hyperframes/history` (renderer file-history snapshots), `/root/.cache/pip`, the v7 sfx/punch/beds/music stems,
`audio/voice_v1.wav`, `voice_v2.wav`, the v7 voice and its chunk cache. `audio/music_bed_v1.wav` keeps the approved hook music
samples (52 s) that `music_bed.py` needs. During the mix the stems and the join were kept in `/dev/shm`. Free now ~1.5 GB with
`oriskany_full_v7.mp4` still present: **its deletion was refused by this session's permission check**, so v7 (1.09 GB) is still on
disk; delete it by hand once v8 is accepted.

## 8. Open items
- "towed" at 7:18 ("she was towed back to Texas"): whisper small.en writes "told"; base.en heard "towed". Owner ear-check.
- True-peak margin: the AAC 192k encode of the Archive voice overshoots its master by up to ~3 dB at random frames; the mix needed
  the lowest MASTER_LIMITS step (0.70) to pass (TP -1.7). A future re-mix may need one more step.
- "for" (+1.0 dB) and "the" (+1.6 dB) speech-band SNR under the jets (section 4).
- CLAUDE.md still gives the hook-blast exception as "17.65"; in v8 the same cue is at 17.167 s (lock updated, CLAUDE.md not).
