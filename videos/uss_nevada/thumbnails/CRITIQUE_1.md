# Critique 1: truth, rights, design. USS Nevada thumbnails v1

Checked against: CLAUDE.md, STYLE_LOCK s6, THUMBNAIL_STUDY (TL;DR, s10), Mallows CRITIQUE_1/2, NARRATION_v1.txt, FACTCHECK_B, FOOTAGE_LIST,
the source frames, `sidebar_strip.png` (colour + greyscale). Pixel metrics: V1 mean luma 0.53, blue-hue share 29 %; V2 0.55, 1 %; V3 0.65, 2 %. Bottom-right 300x160 clear in all three.

## Verdict (after the fixes below were applied to the builder)

| Draft | Truth | Rights | Design /10 | One line |
|---|---|---|---|---|
| V1 SURVIVED / 2 A-BOMBS | PASS | PASS (residual note) | 7.5 | Whole ship, blue sea, true number; soft film |
| V2 BULL'S-EYE | PASS (Able only) | PASS | 6 | Rare split; B&W half; words add little |
| V3 THEY MISSED | PASS with owner check | PASS | 7 | Best gap; ship is a tower, not a whole ship |

Ranking: V1 > V3 > V2.

## 1. Truth
- **V1 PASS.** "Survived 2 A-bombs" is FACTCHECK_B title claim, true. No "only", no "unscathed". The hook line 1-3 says it in the first 10 s.
- **V2 PASS, one trap fixed.** First build used a Baker photo next to BULL'S-EYE, which would imply the second bomb was aimed at her. Swapped to NARA 80-G-396226, whose title says "Able Day" (FOOTAGE_LIST A36). Bull's-eye is a Navy term spoken at hook line 11. Still: the picture shows a bomb and the ship together, with no word that the bomb missed; the title or description must carry "survived".
- **V3 PASS with owner check.** "They missed" is true for Able only (about a third of a mile, FACTCHECK C1: never state yards as flat fact; none on the image). Viewer may read it as "both bombs missed"; Baker was never aimed at her. The hook corrects this within seconds (second bomb "went off under the water"). Owner: accept, or use V1 only.
- **Colour.** Nothing on any image says "orange", "restored" or "colourised". The film is faded; the builder applies a mild saturation lift and the sea-only blue. The ship reads salmon-red, which is the film, not a repaint. Do not describe it as "international orange" in the upload text next to the thumbnail.
- No named ship other than Nevada is implied. The Able still shows no ships (FOOTAGE_LIST says "ships not visible"), so nothing is falsely placed at Bikini.

## 2. Rights: all PASS
| Source | Used in | Basis |
|---|---|---|
| Navy film MN 6517 window `crossroads_mn6517_w01g` (0.5 s, 32 s) | V1, V2, V3 | US Navy production (COMJTF-1 film, end card "MN 6517 NPC 1949") = federal work. Hosted as archive.org IA000015; the video itself already uses it (MANIFEST) |
| NARA 80-G-396226 | V2 | NARA `useRestriction: Unrestricted`; Navy photograph |
Residual: some NARA Navy colour film carries "Undetermined"; treated as federal work. No Ocean Infinity/SEARCH wreck image is used (copyrighted).
Add the three rows to `full/CREDITS.md` (still frames of already-credited film; the Able photo is already row A36).

## 3. Design
Fixes applied during the build (v0 -> v1): 
1. V2 first used the colour Able film frames (washed, the cloud read as a face/hole). Swapped to the B&W NARA still, a clear column.
2. V2 halves swapped (blast left, ship right) so the red box sits over the bomb half and no longer covers the mast tip.
3. V3 words moved to a stacked left column so the mast and yardarm are not hidden.
4. V1 red box moved up 25 px off the bottom edge; shade widened.
5. Tower frame is the 32 s one (the 30 s frame is a close-up of a turret roof and reads as a white blob).
Kept from Mallows: stroke 9 + shadow, white word in a red box (survives greyscale: confirmed in the greyscale row), sharpen 1.1, sea-only grade.

- **V1 (7.5).** Bright, blue sea, long hull, 2 lines of big text. Problems: ship only ~1/3 of the frame height and soft/posterised from the 16 mm source; the box "2 A-BOMBS" is wide but fine at 168x94. Greyscale: both lines readable.
- **V2 (6).** Split gives a clear then/target idea and reads at 168x94, but the blast half is grey, so the thumbnail is half B&W (study: grey loses). BULL'S-EYE spans both halves and fully covers the top of the blast; OK.
- **V3 (7).** Tall silhouette, mast and turrets read at sidebar size; warm, bright. Salmon cast could look dull next to blue feeds. Stormy sky is grey (kept; sky is not in the sea mask).
- Zones: text ends x <= 850 (V1 700, V2 665, V3 ~430), nothing in top-right 120 px or bottom-right 300x160.

## 4. Not done / open
- No sinking-film frame (dark B&W). A bright "2 A-BOMBS" over the Able colour dome could be tried if V1 loses.
- Owner: V3 words (see truth).
