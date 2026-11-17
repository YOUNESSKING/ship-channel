# USS Nevada thumbnails v1 (Test & Compare)

Builder: `make_thumbs.py` (helpers copied from Mallows `make_thumbs_v2.py`; run from anywhere, paths relative to the repo).
All 1280x720 JPG + `_sidebar.png` (168x94). `sidebar_strip.png` = the three at sidebar size, colour row on top, greyscale row below.
Rules kept: real archive frames only, no repaint/AI, sea-only grade (+25 % sat, 45 % toward 195 deg, +0.35 EV mids), white Anton words with stroke 9 + shadow,
one red box (white word on #E0352B), sharpen 1.1 max after resize, bottom-right 300x160 and top-right hover zone clear, nothing written about colour.
Film frames are the active 4:3 picture of the 1080p file (pillarbox removed, leader not used).

| File | Shows | Words | Source and rights |
|---|---|---|---|
| `V1_survived_2_a_bombs.jpg` | Nevada at anchor in the Bikini lagoon, wide, colour film, blue-graded sea | SURVIVED / [2 A-BOMBS] (red box) | Navy film MN 6517 "Operation Crossroads: Able and Baker Day Tests" (NARA/archive.org IA000015), window `crossroads_mn6517_w01g.mp4` at 0.5 s. US Navy production = federal work, PD |
| `V2_bulls_eye.jpg` | Split: Able column over the lagoon (B&W still) / Nevada's tripod mast and 14-in turrets (colour film) | [BULL'S-EYE] (red box) | Left NARA 80-G-396226, Able 1 Jul 1946, `Unrestricted`. Right same film, `w01g` at 32 s |
| `V3_they_missed.jpg` | Nevada's mast, bridge and forward turrets against a stormy sky, colour film | THEY / [MISSED] (red box) | `w01g` at 32 s, full 16:9 crop. Same film/rights as V1 |

Truth lines: SURVIVED 2 A-BOMBS = FACTCHECK_B (true; never "only"). BULL'S-EYE = the Navy's target ship for Able (narration line "The Navy chose her as the bull's-eye"; FACTCHECK C1/F3).
THEY MISSED = Able missed her by about a third of a mile (narration, hook; FACTCHECK says say "about", not yards). It is about the first bomb only. The colour is the film's own faded colour with a mild balance; no text says "restored" or "orange".

## Ranking (see CRITIQUE_1.md)
1. **V1 SURVIVED / 2 A-BOMBS**: only draft with a whole ship in a blue sea and the title's promise as a number. Pair with a title that does not repeat the words (title 4 or 3 in TITLES_THUMBS.md).
2. **V3 THEY MISSED**: strongest curiosity gap ("who missed what?"), tall readable silhouette, warm and bright. Truth limited to Able, so owner check.
3. **V2 BULL'S-EYE**: the split is rare in the niche, but half is B&W and the words add little without the title.

Test & Compare order: V1 vs V3 vs V2. Judge on day 7-14 Studio data.

## Weak points to know
- The Nevada film is soft 16 mm scanned to 1080p, with dust and a vertical scratch; at feed size it reads, up close it is grainy.
- No frame of the 1948 sinking was used: all are dark B&W (rule: dark and grey lose; study s3).
- Rights residual: film windows are Navy productions hosted at archive.org; NARA's own record for the colour reel says "Undetermined" for some Navy colour film (see FOOTAGE_LIST). Treat as federal work; confirm once at the NARA catalog if the owner wants certainty.
