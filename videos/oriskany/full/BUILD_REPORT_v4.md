# Oriskany full video: build report v4, picture (2026-11-05)

**Output:** `videos/oriskany/full/oriskany_full_v4.mp4` (git-ignored, 1.09 GB). H.264 1920x1080, 30 fps, **25,968 frames, 865.6 s
(14:25.6)**, AAC stereo 48 kHz, audio = video length. Same timing as v3: no word, shot start or chapter start moved, so the
description timestamps are unchanged. v3 was deleted after v4 passed the picture checks (v2 deleted before the renders, for disk).

v4 = v3 + the picture fixes below + the sound agent's v4 sound (`build/SFX_FIX_v4.md`, not touched here). The hook (0-48.6 s) is
unchanged: it is still the approved test v4 picture, frame for frame.

## Numbers

| measure | v3 | **v4** | target |
|---|---|---|---|
| integrated (ebur128 on the mp4, `build/ebur128_v4.txt`) | -14.0 LUFS | **-14.0 LUFS** | -14 ± 0.5 |
| true peak | -1.7 dBTP | **-1.5 dBTP** | ≤ -1.5 → PASS |
| LRA | 2.1 LU | **1.9 LU** | 2-8 → FAIL by 0.1 (sound side, see below) |
| SFX cues | 150 | **148 (10.3/min)**, sync max 1.1 frames, 0 over 3 | ≤ 3 frames |
| `check_safe_text.js` | PASS | **PASS c02-c07** (`chapter/safe_c0*.txt`); c01 unchanged (PASS in v3) | |
| `check_clips.py --no-cuts` (`build/check_clips_v4.txt`) | 95 BLOB + 10 FLASH | **99 BLOB + 10 FLASH**: the same 10 flashes as v2/v3 (hook blasts, the c05 "they fired" flash, bright/dark cuts); the BLOB regions are the v3 ones, a few now split in two because the card shots are no longer flat dark | |
| blackdetect (0.25 s, pix 0.06) | none | **none** (`build/blackdetect_v4.txt` empty) | |

`check_sound_lock.py --render` stops the mix script on two items, both on the sound side and both already reported by the sound agent
(`build/SFX_FIX_v4.md`): **LRA 1.9 < 2** (the owner's quieter horn) and the **approved hook thump at 28.70 s, +2.8 LU** (owner: hook left
as is). The mp4 itself was written before the check. The picture changes moved no cue: they only changed which shots get a bed (projector
under the two new NARA-film card backgrounds, c03 s03 and s45; the generic bed under c07 s17; none under c04 s24, now a map).

`FINAL_SHEET_v4.jpg` (one frame every 10 s) looked at. Every changed shot was also checked frame by frame at 480p (below).

## Owner priority: no plain dark text cards

Rule (CLAUDE.md, owner 2026-11-05): every text or number card sits on a dimmed moving background. All **31** text cards in c02-c07 now
have one. Check: a script over `chapter/c02-c07.json` finds **0** `text_card`, `number_clip` or `lower_third` shots without a clip
(the hook c01 is excluded, approved). Each card was checked at 480p at 35 % and 85 % of the shot: text readable, no clash.

How (`build/make_shotlists.py` `cbg=`, `build/make_segments.py`, `templates`):
- **G** = generic US Government film (keeps its ILLUSTRATIVE tag, drawn on top); **F** = NARA Oriskany film of the matching era (with a
  date tag where it is not the moment named); **P** = 2006 NARA photo with the 2.5D push; **MS** = a slowly pushed still of one of the
  video's own map / document frames, blurred and darkened slightly so its labels never compete with the card text.
- Word / pair / line cards keep their centred card layout over the clip (`"card_bg": true`, `templates/build_chapter.py`) with a soft
  full-frame shade (`.cardDim` in `templates/lib/blocks.css`); number cards use the existing number layout with its full-frame shade.
- Reuse: clip and photo reuse report clean (no clip or photo over 2 uses or under 3 min apart; `build/shotlist_report.md`). New
  sources: NARA 39085 69-72 s (the building ways right after the launch), NARA 86313 (A-4E with bombs, 1968), NOAA "red snapper
  offload" (G18), NARA photos 6698558 / 6698561 / 6698570 / 6698601 / 6698607 / 6698623 (all "Unrestricted", in FOOTAGE_LIST and
  CREDITS_DRAFT).

| card | at (s) | text | background | tag / label |
|---|---|---|---|---|
| c02 s12 | 90.4 | THE PLAN / "CITY OF AMERICA" | pushed still: Tokyo Bay map, PLANNED ATTRACTION (`m_c02_pacific_b` end) | |
| c02 s16 | 102.1 | EARLY 1990s / SOLD FOR SCRAP | pushed still: Bremerton map, FOR SCRAP (`m_c02_scrap_a` end) | |
| c02 s17 | 105.7 | DEFAULTED. | same map, pulling out | |
| c02 s21 | 117.7 | NAVY APPRAISAL / $600,000 | pushed still: the bill of sale (`h_c02_ledger_a` end) | |
| c02 s22 | 120.9 | 3 bids | pushed still: the bill of sale with its price (`h_c02_ledger_b` end), panning | |
| c02 s23 | 122.8 | THE CONDITION / SCRAP HER IN THE U.S. | pushed still: Bremerton map, STILL NAVY PROPERTY (`m_c02_scrap_b` end) | |
| c02 s24 | 126.2 | A PROTEST. / Work held up until December. | pushed still: the bill of sale, panning | |
| c02 s27 | 140.7 | 1997 / ALMOST NOTHING CUT | pushed still: Mare Island scrap-yard map (`m_c02_mare` end) | |
| c02 s28 | 143.4 | DEFAULTED. | same map, pulling out | |
| c03 s03 | 185.6 | 6 weeks / AFTER JAPAN SURRENDERED | NARA film 39085: the empty building ways after the launch, Oct 1945 | |
| c03 s05 | 192.5 | AUGUST 1947 / WORK STOPPED | pushed still: New York Navy Yard map (frame before its MAY 1944 date) | |
| c03 s15 | 223.8 | ROYCE WILLIAMS · 2023 / NAVY CROSS | pushed still: the 4 vs 7 MiG map | |
| c03 s24 | 251.7 | PRISONER OF WAR / 7½ years | pushed still: Stockdale shoot-down map, North Vietnam | |
| c03 s45 | 323.2 | 26 OCT 1966 → 26 OCT 1967 / ONE YEAR TO THE DAY | NARA film 86313: A-4E with bombs on Oriskany's deck | FILM: ORISKANY, 1968 |
| c04 s15 | 413.2 | THE CLEANUP RULE / CONTAMINATED MATERIAL COMES OUT | pushed still: Corpus Christi map, 11 MONTHS | |
| c04 s16 | 417.4 | UNLESS THE EPA AGREES | same map, pulling out | |
| c04 s19 | 429.1 | SPENT ON THE DECK / ½+ | photo 6698570: the bare steel flight deck, 2006 | BARE FLIGHT DECK · PENSACOLA, 2006 |
| c04 s20 | 431.3 | A COMPUTER MODEL / $3.7 million | photo 6698561: inside the stripped hull, 2006 | INSIDE THE HULL · PENSACOLA, 2006 |
| c05 s12 | 524.7 | 17 MAY 2006 / 10:25 a.m. | photo 6698607: support ship with media on scene, 17 May 2006 | |
| c05 s22 | 553.4 | GUINNESS WORLD RECORDS / LARGEST ARTIFICIAL REEF IN THE WORLD | photo 6698623: the last of the deck in a ring of foam, 17 May 2006 | |
| c06 s13 | 613.6 | 254 fish | (v3) NOAA lab film | ILLUSTRATIVE · NOAA · FISH SAMPLES FOR TESTING, 2010 |
| c06 s21 | 642.8 | 2012 PETITION / ENVIRONMENTAL GROUPS | (v3) NOAA snapper film | ILLUSTRATIVE · NOAA · RED SNAPPER, GULF OF MEXICO |
| c06 s29 | 669.2 | FLORIDA / NO ADVISORY ISSUED | (v3) NOAA anglers | ILLUSTRATIVE · NOAA · RED SNAPPER FISHING, GULF OF MEXICO |
| c07 s11 | 723.3 | FLORIDA FWC / NEVER GO INSIDE | (v3) Navy divers on a wreck | ILLUSTRATIVE · U.S. NAVY DIVERS ON A WRECK, COLOMBIA, 2014 |
| c07 s13 | 728.8 | FIRST YEAR / 4,200 dive trips | (v3) NOAA diver, Florida Keys | ILLUSTRATIVE · NOAA · DIVER ON A REEF, FLORIDA KEYS |
| c07 s14 | 733.8 | ECONOMIC IMPACT / $3.6 million | (v3) NOAA angler | ILLUSTRATIVE · NOAA · FISHING, GULF OF MEXICO |
| c07 s17 | 743.3 | 67 jobs | NOAA film: red snapper landed at a Gulf dock | ILLUSTRATIVE · NOAA · RED SNAPPER LANDED, GULF OF MEXICO |
| c07 s25 | 773.4 | THE NAVY'S SUMS / REEF vs. SCRAP | photo 6698601: aerial, the hulk under tow to the reef site, 15 May 2006 | |
| c07 s30 | 790.5 | MARAD · JAN 2008 / A WARNING | (v3) retired ship towed out, Mayport | ILLUSTRATIVE · U.S. NAVY · RETIRED SHIP TOWED OUT, MAYPORT, 2021 |
| c07 s31 | 795.7 | THE WARNING / CLEAN TO THE NEW STANDARD | photo 6698558: technicians on the stripped deck, 2006 | |
| c07 s32 | 797.3 | MARAD · JAN 2008 / SAVINGS COULD BE WIPED OUT | photo 6698597: aerial, the hulk at the Pensacola pier | |

Not covered by the card rule (they are animations, not text cards, so left as they are; owner call): the x-ray, gauge and options
blocks (e.g. 390, 396-404, 420-428, 460-479, 566-578, 678-686, 746-756, 776-783 s) still draw on the dark animation board. Two of
them already have film under them (c02 s08, c07 s28).

## Critic A NICE items + the fresh look: fixed / not fixed

| # | item | v4 | check |
|---|---|---|---|
| N1 | "ON THE SEABED 212 FT" printed while the hull is still tilted (9:04) | **fixed**: `hero/sinking.js` `levelEarly` levels the hull by depth before it reaches the bottom; it touches flat on "twelve" (beat 544.27 s, unchanged within 4 ms) | frames 544.0-544.9 s: hull level when 212 FT prints |
| N2 | film-gate slivers + dust on the 1969 aerials (0:50, 5:06, 14:17) | **fixed**: reel 87411 cropped to its clean area (`make_segments.py`, 684x456+16+12) | 50.5, 306, 838-840 s: clean edges, no blob seen |
| N3 | $800,000 tow over the Rita loop | **fixed**: the number now sits on the June 2005 tow map (Pensacola → Texas, JUNE 2005, gently pushed), on the left so it clears the HURRICANE SEASON label; Rita stays for the next shot (map) | 451.8, 453.5 s |
| N4 | overlapping VERMILION SNAPPER / SCAMP chips (10:41) | **fixed**: SCAMP moved right, NEVER CROSSED EITHER LINE lifted off the line | 641-643 s |
| N5 | "1 ROUNDS" | **fixed**: ROUND / ROUNDS follows the number | snaps at 0.1-0.4 s of the scene |
| N6 | SS United States film with a carrier behind (13:3x) | **fixed**: the automatic window started on the river shot; profile window now 144.1-161.8 s, this use 155.0 s (the hook uses 150.5-152.7) | 812-814 s: the liner alone |
| N7 | rubble reef direction not marked as approximate | **fixed**: label "RUBBLE REEF (POSITION APPROX.)" | 654-656 s |
| N8 | hook shots under 1.5 s, helicopter photo before its label | **not fixed**: approved hook (owner decision); no true defect found | |
| A-S* | v2/v3 open SHOULD items | none left on the picture side (v2 report: all done) | |
| fresh | 1990s-2000s card stretch was ~25 % flat dark screen (c02 22 %, c04 12 %) | **fixed** by the card backgrounds above | |
| fresh | text over busy map/document backgrounds | **fixed** while building: card backgrounds made from the video's own maps/documents are blurred + darkened (first render showed CITY OF AMERICA over TOKYO BAY, 3 bids over the bill of sale) | c02 sheet re-checked |
| fresh | hero-scene kickers sit ~80 px from the top edge (e.g. HER ESSEX-CLASS SISTERS) | not changed: inside the project's safe-area rule (bottom 10 % + top-right corner); would need all 31 hero renders | |
| fresh | stills dead for > 3 s | none found: every photo has its 2.5D move; the 18 s end screen holds the map by design | |
| fresh | the order "UPRIGHT ON THE SEABED" (top view, 9:00) before the side view still descending (9:03) | not changed (same as v3, approved order of the sinking shots) | |
| fresh | labels before their event, black frames, jumps at cuts, text clipped, contradictions with the words | none found on the 2 s frame pass (433 frames, 480p) or the targeted frames | |

## Renders

c02-c07 re-rendered (render_all.sh, detached, resumable, one at a time); c02-c04 a second time after the card shade was lightened and
the $800,000 moved. Hero scenes re-rendered: `c05_hero_b`, `c06_rounds_b`, `c06_species_b`; map: `c06_rubble`. New segments: 24 card
backgrounds (`b_*`), `s_c04_s24`, the four 1969 aerials, the SS United States profile. Disk: v2, v3, `chapter/joined_silent.mp4` (rebuilt
by the mix) and `mk/scenes/` (map build folders, rebuilt on demand) deleted; `chapter/joined_silent.mp4` of v4 is kept for sound re-mixes.

## Paperwork

MANIFEST.md (60 film rows) and CREDITS.md (107 items) regenerated: adds NARA 39085 (69-72 s), NARA 86313 (A-4E), NOAA offload, six
2006 NARA photos; drops the NASA Rita loop (no longer on screen; Gustav stays). Description timestamps unchanged (header now says v4).
Note: for `b_c03_s45` the film engine skipped an internal cut, so the clip on screen starts at reel 204.9 s (MANIFEST says 202.2 s).
