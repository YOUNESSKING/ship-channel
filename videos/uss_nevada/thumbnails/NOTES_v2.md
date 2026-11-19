# USS Nevada thumbnails v2 (Test & Compare)

Builder: `make_thumbs_v2.py` (run from anywhere; paths relative to the repo; frame cache in `/dev/shm/nevada_thumbs_v2`).
All 1280x720 JPG + `_sidebar.png` (168x94). Strips: `sidebar_strip_v2.png` (colour row, greyscale row; real-photo set, ranked),
`sidebar_strip_v2_grey.png` (all grey), `sidebar_strip_v2_with_ai.png` (ranked set + the two AI options at the end).
v1 files (V1-V3, `make_thumbs.py`, `NOTES.md`, `CRITIQUE_1.md`) are kept unchanged. Critiques of this round: `CRITIQUE_2.md`.

## How the stills were made (real frames only)
- Each film still is the **median of 7-9 consecutive frames** of one shot, aligned by phase correlation: removes grain and
  dust, adds nothing. Then vertical film scratches are refilled from the clean columns either side (restoration only).
- Active 4:3 picture only (pillarbox removed, no leader). Splits are two real 1946 frames side by side with a **white 10 px
  divider**; the ship is never pasted into an explosion.
- Grade: sea/sky-only (blue-cyan hue mask, +35 % sat, hue toward 200 deg) + mild midtone lift + contrast 1.08 (tonal).
  No colour push on the ship (removed after critique 2). White Anton, stroke 9 + shadow, one red #E0352B box, sharpen 1.1.
- Zones: bottom-right 300x160 holds only sea/sky in every pick (word boxes end at x <= 940); top-right hover corner clear.

## vidIQ scores
`vidiq_score_thumbnail`, all against the main title **"Two Atomic Bombs Couldn't Sink Her. Then What Did?"**. The tool
needs a videoId; none exists yet, so every call used the same stand-in (`j3--VLSgWmA`, a Pearl Harbor battleship video in
the niche) so the scores are comparable with each other. Upload route (the tool refuses local files and most hosts): images
packed into a short lossless-quality MP4 -> `vidiq_video_upload` -> `vidiq_edit_media extract_thumbnail` (1 credit) -> the
returned image URL scored. vidIQ's self-score for its own AI images equals `score_thumbnail` (checked on AI2: 94 = 94).

| Rank | File | Shows | Words | vidIQ | Notes |
|---|---|---|---|---|---|
| **1 (main)** | `N10_split_lagoon_2.jpg` | Nevada at Bikini, tower + 14-in turrets (left) \| Able mushroom over the lagoon and reef from the air (right) | [2 A-BOMBS] | **91** | Bluest pick (57 % blue-hue pixels, study's strongest signal); split reads at 168x94 |
| **2 (T&C B)** | `N6_half_split_box_only.jpg` | Same left \| Able mushroom with its red-rimmed condensation ring, from the air | [2 A-BOMBS] | **90** | Boldest blast at sidebar size; tests the bomb image vs N10 |
| **3 (T&C C)** | `N11_split_lagoon_survived.jpg` | As N10 | [SURVIVED] | **91** | Tests the word vs N10 |
| 4 (reserve) | `N9_split_target.jpg` | As N6 | [TARGET] (on the ship half) | 87 | Only word that ADDS to the main title |
| 5 (reserve) | `N3_big_2.jpg` | Nevada's tower and turrets full frame | giant [2] + A-BOMBS | 86 (89 with an earlier +12 % colour push, removed) | Single image, no split |
| - | `N5_half_split.jpg` | As N6 | SURVIVED (top) + [2 A-BOMBS] | 88* | Two text blocks; N6 cleaner |
| - | `N4_lagoon_she_survived.jpg` | Lagoon mushroom (left 560) \| Nevada | SHE / [SURVIVED] | 87* | Words too small at sidebar |
| - | `N2_she_survived.jpg` | Whole ship, full frame (barge in front) | SHE [SURVIVED] | 84* | Soft wide shot |
| - | `N1_split_2_a_bombs.jpg` | 60/40 split, whole ship \| ring | SURVIVED / [2 A-BOMBS] | 81* | vidIQ: "comparison not clear" -> led to the 50/50 splits |
| - | `N8_wide_survived_2.jpg` | v1 V1 rebuilt from the denoised still | SURVIVED / [2 A-BOMBS] | 81* | "Too busy" (sea texture) |
| v1 | `V3_they_missed.jpg` / `V2_bulls_eye.jpg` / `V1_survived_2_a_bombs.jpg` | (v1) | | 87 / 87 / 72 | Baseline |
| AI | `AI2_split_survived.jpg` | **AI image** (vidIQ generate): orange battleship \| atoll mushroom | [SURVIVED] | 94 | AI, see below. Never the main pick |
| AI | `AI1_orange_nevada_2_a_bombs.jpg` | **AI image**: orange battleship, mushroom behind | [2 A-BOMBS] | 100 (self) | AI, wrong ship shape; not recommended |

\* scored on the first build, which had a +12 % global colour push; the files in the folder are the rebuilt versions
without it (the only scored-then-changed files; N6 re-scored after the change: 90 -> 90).

## Sources and rights
| Piece | Source | Rights |
|---|---|---|
| Nevada close (all splits, N3) | Navy film MN 6517 "Operation Crossroads: Able and Baker Day Tests" (COMJTF-1, NPC 1949), window `crossroads_mn6517_w01g.mp4` 5.5 s (median of 7 frames). before Able (topmasts still standing; BS-A1: both came down in Able), exact date not recorded | US Navy production = federal work, PD. Hosted at archive.org `OperationCrossroads` (no licence field). Residual: NARA lists some Navy colour reels "Undetermined"; treated as federal work (as in v1, MANIFEST) |
| Nevada wide (N1, N2, N8) | same film, `w01g` 3.4 s (median of 7) | same |
| Able, lagoon aerial (N4, N10, N11) | same film, window `crossroads_mn6517_w03.mp4` 29.5 s (median of 7). FOOTAGE_LIST: w03 4.1-37.8 s = Able, one aerial shot | same |
| Able, red-rimmed mushroom (N1, N5, N6, N9) | same film, `w03` 54 s (median of 9). FOOTAGE_LIST: w03 53-60 s = Able red-rimmed mushroom | same |
| AI1, AI2 | `vidiq_generate_thumbnail`, 2026-11-19 (vidIQ account output) | AI-generated; no archive content. No watermark or logo seen at 100 %. Label as AI |

Colour note: `w01g` is the video's own colour-corrected window ("restored toward the documented international orange",
CREDITS.md / FACTCHECK_B C2). The thumbnail adds no colour to the ship. No image says "orange", "colour" or "restored".
CREDITS.md: these are stills of already-credited windows (w01g, w03); add one line "thumbnail stills: w01g 3.4/5.5 s,
w03 29.5/54 s" when the upload kit is built.

## Truth lines
- **2 A-BOMBS** / **SURVIVED**: FACTCHECK_B F1 (afloat after Able 1 Jul and Baker 25 Jul 1946). Never "only" (F2). The split
  shows one bomb (Able); the number is about her, not the picture.
- **TARGET**: C1 (aiming point / "bull's-eye" of Able) and F1 (in the Baker target array). True for both tests.
- The Nevada frame predates Able (topmasts standing); the split does not claim it was taken after a blast.
- Able mushrooms are real Able frames from the same Navy film; neither shows Nevada (FOOTAGE_LIST: ships not identifiable).

## AI options (labelled, never the main pick)
- **AI2 `AI2_split_survived.jpg` (94).** Plausible WWII battleship with two tripod masts, one funnel and twin forward turrets;
  not Nevada's exact 1946 outline (her forward turrets are a triple below a twin, and her mainmast was cut down in the 1942 rebuild). Right half is
  a generic atoll mushroom (Able-like). Too-saturated orange and turquoise. Usable as a Test & Compare extra only if the owner
  accepts AI in packaging (STYLE_LOCK s6 says real archive photos only, so default = do not use).
- **AI1 `AI1_orange_nevada_2_a_bombs.jpg` (100).** Ship is wrong (pre-dreadnought-like casemate guns, a gun cluster that no US
  battleship had), and the mushroom sits right behind her, which would have engulfed the ship: dramatised. Do not use.

## Weak points
- Source is soft 16 mm; the median stack cleans grain but cannot add detail. At feed size the ship reads; on a TV it is soft.
- "2 A-BOMBS" and "SURVIVED" restate the main title; the picture carries the proof. See pairing in `script/TITLES_THUMBS.md`.
- vidIQ score is a floor, not a prediction (THUMBNAIL_STUDY DON'T 6). Judge on day 7-14 Studio data.
