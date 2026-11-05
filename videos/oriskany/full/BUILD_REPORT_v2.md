# Oriskany full video: build report v2 (2026-11-05)

**Output:** `videos/oriskany/full/oriskany_full_v2.mp4` (git-ignored, 1.06 GB). H.264 1920x1080, 30 fps, **26,544 frames, 884.8 s**
(same length and same chapter starts as v1, so the description timestamps are unchanged). AAC stereo 48 kHz. Audio = video length.
v1 (`oriskany_full_v1.mp4`) is still on disk; delete it once the owner has watched v2.

## Numbers

| measure | v1 | **v2** | target |
|---|---|---|---|
| integrated (ebur128 on the mp4) | -14.0 LUFS | **-14.0 LUFS** | -14 ± 0.5 |
| true peak | -1.6 dBTP | **-1.5 dBTP** | ≤ -1.5 |
| LRA | 2.4 LU | **2.1 LU** | lock rule ≥ 5: **fails, owner decision (rule not changed)** |
| music under voice, whole video (measure_mix) | -24.1 dB | **-24.1 dB** | owner: not louder than v1 → **held** |
| music under voice c06-c07, 30 s windows | -26 to -31 dB | **-24.5 to -27.9 dB** | -24..-28 (critic B S1) |
| music under voice 370-410 s (v1 hole) | -28 / -31 / **-40** / -27 | **-21.8 / -23.8 / -23.8 / -26.0** | no hole (S2) |
| music during "Then she was gone" (538.5-540.5) | full bed | **-12 dB dip** | S3 |
| end screen (868-881 s, master M median) | -33.2 LUFS | **-27.3 LUFS** | ~-25 (N1, +8 dB on the bed) |
| hook 0-48.6 s (mp4) | -13.2 LUFS | **-13.1 LUFS** (+0.14 dB master gain; cues, beds, music samples identical) | unchanged |
| SFX cues | 197 (13.4/min) | **157 (10.6/min)**; sync max 1.1 frames, 0 over 3 | ≤ 3 frames |
| loudest beat after the hook (measure_mix) | 781 s bar-chart hit -7.2 LUFS | **815 s answer boom -8.0; 526 s charges -9.2 (+4.9 LU, was +3.2)** | no hit louder than the sinking |
| `hit` role over voice (local) | up to +8.5 LU, 11 cues | **1 cue: the 145.3 s DEFAULTED stamp, +6.1 LU** | stamp only |

Checks run on the final files:
- `check_safe_text.js`: **PASS on all 7 chapters** (`chapter/safe_c0*.txt`; c01 is the approved test v4 picture, unchanged).
- `check_sound_lock.py`: static lock **OK**. Render check **fails on two items**:
  1. **LRA 2.1 LU < 5** (rule unchanged as instructed; v1 was 2.4, the battle-maps references 2.2-2.5).
  2. **Hook beat at 28.70 s ("floor" thump) +2.9 LU over the whole-video speech median** (v1 +3.0). Nothing in the hook changed: the
     whole-video speech median rose 0.2 LU (fewer loud cues → 0.1-0.2 dB more master gain). Fixing it means touching the approved hook
     or the locked levels → owner decision. All other 9 big beats pass (526 s charges now +4.9 LU, was +3.2).
- ebur128 on the master: -14.0 LUFS, TP -1.5 dBTP.
- `tools/film/check_clips.py --no-cuts`: exit 1 with **97 BLOB + 10 FLASH** flags (`build/check_clips_v2.txt`). Looked at by eye: BLOBs are the drawn
  dark graphics (as v1); FLASHes are the two hook blasts, the c05 "they fired" flash, and hard cuts between bright film/photo and dark
  cards/maps (92.4, 96.0, 213.1, 238.9, 317.3, 355.9, 788.1 s). No burns, no leaders, no black frames.
- `FINAL_SHEET_v2.jpg`: one frame every 10 s (89 frames), looked at. Plus targeted frame grabs at every critique item (below).

## Pass / fail: every MUST item of both critiques, checked on v2 frames / audio

| # | item | v2 check (frame or measurement) | result |
|---|---|---|---|
| A-M1 | "salt lowers the freezing point" subline | `number_clip.py` has no default subline any more (empty = no element). 222.98 s (4 / NAVY CITATION) and 388.5 s (2 MORE YEARS): no subline | **PASS** |
| A-M2 | text clipped at the frame edge | new shrink-to-fit pass in `templates/lib/safe_area.js` (64 px stage = 96 px margin at 1080p; wraps when shrinking would go under the 38 px minimum). 232 s "12,000 sorties" (x0.78), 416.5 s CONTAMINATED MATERIAL COMES OUT, 461 s "NAVY SPENDING, SPRING / 2006" (wrapped), 555 s LARGEST ARTIFICIAL REEF IN THE WORLD (x0.64), 323.9 s ONE YEAR TO THE DAY, 796 s CLEAN TO THE NEW STANDARD: all inside the frame | **PASS** |
| A-M3 | half-frame shading box | `.scrimLB` and `.scrimR` are now full-frame (1280x720 stage) soft radial gradients that reach 0 inside the frame. 94.8 s (theme park), 327.5 s (McCain), 590 s (EPA), 761.5 s: no edge | **PASS** |
| A-M4 | ILLUSTRATIVE tag missing / dimmed | tags are no longer burned into the clips; `build_chapter.py` draws them as a top layer (z 50) on every shot with generic film, below the letterbox bar when there is one. 615 s (254 fish), 731.5 s (4,200 dive trips), 736.5 s ($3.6 million), 72.5 s, 784 s, 792 s: tag full opacity | **PASS** |
| A-M5 | Panther / Corsair swapped | in-points forced from the reel frames (reel 78776: F9F "111" 12-15.9 s, F4U 16-24 s). 206.5 s "Mighty O" = Corsair; 212.8 s "Panther jets" = Panther. MANIFEST rows match | **PASS** |
| A-M6 | "WORLD'S LARGEST REEF" | map `c07_title` re-rendered: **"PLANNED · LARGEST ARTIFICIAL REEF"** (855.6 s) | **PASS** |
| A-M7 | invented $24M "new standard" bar | gauge removed; card **"MARAD · JAN 2008 / SAVINGS COULD BE WIPED OUT"** (799 s) | **PASS** |
| A-M8 | press ≈$20M shown as the Navy's sums | 780-788 s bars now read **"REEF · PRESS EST. 2006"** and **"SCRAP · USNI 2006 EST."**; 818-822 s "By the Navy's own sums" now shows the Navy's own ratio (scrap + recycle 4 : reef + cleanup 1, the USNI06 "about a quarter" claim), no dollar figure | **PASS** |
| B-M1 | whoosh on every map move | 35 body whooshes dropped; kept 153.66, 484.78, 686.84 + the hook pair; the end-screen whoosh moved to 865.9 (after "comments.") | **PASS** |
| B-M2 | jets over the 1945 launch film | 172.91 / 181.41 / 188.17 dropped. 325.94 kept: the A-4's nose is in frame from the cut and it launches at ~327.8 (checked on frames) | **PASS** |
| B-M3 | bar-chart booms louder than the sinking | 9 gauge/stamp hits re-roled to `pop` (-20); only the 145.3 stamp stays `hit` (+6.1 LU). 526.27 charges now +4.9 LU (boom layer added, S3). The 815 s answer boom (-8.0 LUFS) stays the loudest beat after the hook, 1.2 dB over the charges (locked role levels; changing that is an owner call) | **PASS** (note) |
| B-M4 | publish before 12 Nov | v2 is ready 5 Nov; description draft says publish before 11 Nov | **PASS** (owner to publish) |

SHOULD / NICE items done (picture, critic A): S1 clip reuse (Kitty Hawk reel 2 uses: 58 s + 784 s; Fort McHenry reel 2 uses: 71 s + 791 s; no clip or photo
over 2 uses or under 3 min apart, `build/shotlist_report.md`); S2 (61 s now the real 1990 Bremerton row photo with a 0→13 YEARS count; 365 s reef fish;
758 s 1990 Bremerton photo "1976-2006 / NEVER TAKEN APART"); S3 (date tags "FILM: ORISKANY A-4s, 1968 (NOT HIS AIRCRAFT)" / "FILM: ORISKANY, 1968
(NOT HIS LAUNCH)", kickers "HER AIR WING COMMANDER" / "VA-163 · SHOT DOWN 26 OCT 1967"); S4 (swap on "four"); S5 (PROTEST → two-part card on
"protested"/"December"; EPA ruling over a 2006 photo with the kicker first; RELEASED over the 28 Jan 1973 task-group photo; press ≈$20M over the media
on the seawall; Florida Senate ≈$21M over the Pensacola aerial; MARAD source on screen 790.6-795.8 s, then again 797-801 s); S6 (167 s now the 1990
Bremerton mothball photo); S7 (= M4); S8 (see "narration change"); S9 (13 YEARS count at 61-62 s); S11 (first silhouette in at the cut).
Sound (critic B): S1, S2, S3 (groan 1 at 532.80 running through the stern-first shot, groan 2 dropped, -12 dB music dip 538.46-540.6, boom layer on
the charges), S4, S5 (risers only at 266, 517, 566, 810), N1, N3 (bubbles dropped), N4 (horn at 827.55), N7 (212 FT lands on the touchdown frame,
544.27; picture fix in `hero/sinking.js`). Locked roles/levels unchanged (horn -14, MUSIC_VOL 0.08, TRIM -6).

## Narration change (S8) — exactly one sentence

- **Was:** "Four of her sisters were already museums." (76.281-78.785 s). False at that point in the story (1989): only Yorktown (1975) and
  Intrepid (1982) were museums; Lexington opened in 1992 and Hornet in 1998 (FACTCHECK_A D4b confirmed the sentence but not its date).
- **Now:** "**Four of her sisters would become museums.**" Kokoro am_michael, speed 0.95, en-us, same trim as `build/voice.py`
  (`build/voice_fix_v2.py`). New take 2.545 s vs 2.504 s (+0.041 s), placed at the same start; the rest of the slot to 79.385 s is silence,
  so **no later word moved** (voice.wav is sample-identical outside 76.281-79.385 s; v1 kept as `audio/voice_v1.wav`).
- Picture: the sisters graphic now tags each ship "MUSEUM · 1975 / 1982 / 1992 / 1998". `script/NARRATION_v2.txt` updated.
  Note: re-running `build/voice.py` from scratch would re-place that chunk with its natural length (+0.04 s downstream); use `voice_fix_v2.py` instead.

## Not fixed / left for the owner

1. **LRA 2.1 < 5** and the **hook 28.70 s beat +2.9 LU** (see checks). Both need a lock or hook change.
2. **Ending length 64 s** (13:21.8 → 14:25.8): two options below, not applied.
3. Not asked / not done: critic A NICE N1, N2, N4-N8 (e.g. hull still tilted when "ON THE SEABED" appears, film-gate slivers, SS United States film with a carrier
   in the background), critic B N2, N5 (pronunciation check by ear before upload), N6, N8, S6/S7 script cuts.
4. 6698586 (press on the seawall) is the **tow day, 15 May 2006**; the card's kicker "PRESS, SINKING DAY" describes the ≈$20M figure, not the photo.
5. Plain text cards keep v1's layout: the kicker sits inline before the main line and shows ~1 s before it (e.g. "1997" at 141 s).
6. vidIQ titles and Test & Compare thumbnails: still to do (spend gate).

## Ending: two cut options (owner decision, NOT applied)

The answer starts at 801.8 s ("So that is why the Navy sank its own aircraft carrier"); the voice ends at 865.8 s = **64 s**.

- **Option A: cut the recap (critic A S10) + the liner details → ≈ 44.5 s**
  - cut "Nobody would take her whole. Nobody could make a scrap deal stick. And the PCBs were in her wiring, where only taking her apart could reach
    them." (805.3-815.0 s, 9.7 s; shots c07 s34 options + s35 x-ray);
  - cut "By the Navy's own sums, it was also the cheapest." (818.0-821.9 s, 4.0 s; shot s37);
  - cut "She is nine hundred and ninety feet long. No explosives this time. They will flood her." (836.8-842.7 s, 5.9 s; shots s42-s43).
  - Keeps the answer line, "The bottom of the Gulf was the one door left", the SS United States news, the twist and the question.
- **Option B: keep the recap, cut the coda details → ≈ 43.7 s**
  - cut "By the Navy's own sums, it was also the cheapest." (4.0 s); "Nobody would take her whole." (805.3-807.2 s, 1.9 s);
  - cut ", at ten in the morning," (829.6-831.1 s, 1.5 s);
  - cut "She is nine hundred and ninety feet long. No explosives this time. They will flood her." (5.9 s);
  - cut "And here is the twist. Okaloosa County put fifty thousand dollars toward sinking the Oriskany." (846.9-853.9 s, 7.0 s), so
    "…thirteen nautical miles from the Oriskany. Now it is about to take her title." follows directly.
  - Keeps the full three-reason recap; loses the $50,000 twist.

Either option is a voice edit at sentence gaps (no re-voicing) plus re-timing c07 from the first cut on (`make_shotlists.py` → segments → c07 render → mix).

## Files changed (scripts; media is git-ignored)

`templates/blocks/number_clip.py`, `templates/blocks/lower_third.py` (kicker_at over a clip), `templates/build_chapter.py` (top-layer tags),
`templates/lib/safe_area.js` (shrink-to-fit), `templates/lib/blocks.css` + `style.css` (full-frame scrims); `full/build/make_shotlists.py`
(beats, forced in-points, tags, per-reel reuse report), `make_segments.py` (no burned tags), `sfx_full.py` (critic B cue rules),
`music_bed.py` (per-piece levels, automation, hook samples kept), `voice_fix_v2.py` (new), `mix_full.py` (v2 output), `paperwork.py`;
`full/hero/scenes.js` (sisters), `hero/sinking.js` (212 FT), `mk/scenes-src/c07_title.js`; `footage/FOOTAGE_LIST.md` + `CREDITS_DRAFT.md`
(two new photos, rights read from NARA: Unrestricted). Regenerated: chapter JSONs, segments.json, SFX_RETIME.md, MANIFEST.md (58 film rows),
CREDITS.md (100 items), YOUTUBE_DESCRIPTION_DRAFT.md (timestamps unchanged), FINAL_SHEET_v2.jpg.
