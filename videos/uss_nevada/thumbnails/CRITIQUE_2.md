# Critique 2: USS Nevada thumbnails v2 (two rounds: CTR, then truth / rights / design)

Drafts: N1-N11 (builder `make_thumbs_v2.py`), v1 V1-V3 as baseline, AI1/AI2 (vidIQ generated). Title tested against:
**"Two Atomic Bombs Couldn't Sink Her. Then What Did?"** Checked against: CLAUDE.md, STYLE_LOCK s3-s6, THUMBNAIL_STUDY
(s7-s10), Mallows CRITIQUE_1_ctr / CRITIQUE_2, v1 CRITIQUE_1, FACTCHECK_B, FOOTAGE_LIST, CREDITS.md.
Tests: vidIQ `score_thumbnail` on every draft; pixel metrics (mean luma, blue-hue share, bottom-right luma); 168x94 strip in
colour + greyscale (`sidebar_strip_v2*.png`); text-box coordinates against the timestamp and hover zones.

## Round 1: click-through (study rubric + vidIQ)

| Criterion (study s9) | N10 2 A-BOMBS (lagoon) | N6 2 A-BOMBS (ring) | N11 SURVIVED (lagoon) | N9 TARGET (ring) | N3 big 2 |
|---|---|---|---|---|---|
| 1. Blue/teal dominant | **1** (57 % blue-hue) | 0.5 (36 %) | **1** (58 %) | 0.5 (40 %) | 0.5 (21 %, sky) |
| 2. Not dark overall | 1 (L 0.50) | 1 (0.49) | 1 (0.50) | 1 (0.48) | 1 (0.60) |
| 3. Colour, not B&W | 1 | 1 | 1 | 1 | 1 |
| 4. Destruction moment shown | 1 (Able) | 1 (Able) | 1 | 1 | 0 (ship only) |
| 5. Ship reads at 168x94 | 1 (tower + turrets) | 1 | 1 | 1 | 1 |
| 6. True number | 1 | 1 | 0 | 0 | 1 |
| 7. No arrow/face/giant-name | 1 | 1 | 1 | 1 | 1 |
| 8. Distinct from FF AI-yellow | 1 | 1 | 1 | 1 | 1 |
| 9. Bottom-right clear | 1 | 1 | 1 | 1 | 1 |
| **Total /9** | **9** | **8.5** | **8** | **7.5** | **7.5** |
| Split (study: best median, weak n) | yes | yes | yes | yes | no |
| Red word survives greyscale | yes (box) | yes | yes | yes | yes |
| Words vs title | repeats ("two atomic bombs") | repeats | repeats ("couldn't sink") | **adds** | repeats |
| vidIQ | **91** | **90** | **91** | 87 | 86 |

Findings and fixes applied:
1. **The first split (N1, 60/40, two text blocks) scored 81: "comparison not immediately clear", "cluttered".** Fix: equal
   50/50 halves, one white divider, one word block at the bottom centre (N6: 90, N10: 91). Kept.
2. **N7 (giant 2 + A-BOMBS + SURVIVED over the close shot) hid the tower.** Rejected and deleted: the ship is the subject.
3. **N4 first build put SHE / SURVIVED over the lagoon mushroom.** Moved the words to the bottom-left over open water.
4. **v1 V1 (72) lost points for "too busy" (sea texture, grain) and negative space.** The 7-9 frame median stack removed grain
   and dust (N8 rebuilt from the same shot: 81); the close shot of the tower + a plain second half did the rest.
5. **Mushroom size at sidebar.** A tighter lagoon crop (x1.25 upscale) was tried and dropped before scoring: visibly soft.
   The red-ring frame (N6) is the boldest blast at 168x94, the lagoon frame (N10) the bluest: test them against each other.
6. **Words repeat the main title** in the three top drafts. The study finds repeat/add inconsistent (10/20 vs 14/20), so the
   image carries the click; the pairing in TITLES_THUMBS uses the alternate titles where the word adds. N9 TARGET is the
   only word that adds to the main title: reserve, and first swap-in if the main pick under-performs.
7. **vidIQ is a floor, not a forecast** (FF study: 89 flopped, 77 hit). All three picks clear 90.

Ranking: **N10 > N6 > N11** (N9, N3 reserve). Test & Compare: A = N10, B = N6 (tests the blast image), C = N11 (tests the word).

## Round 2: truth, rights, design

| Draft | Truth | Rights | Design /10 | One line |
|---|---|---|---|---|
| N10 2 A-BOMBS (lagoon) | PASS | PASS (residual note) | 8.5 | Blue, clean split, true number; lagoon blast is small but readable |
| N6 2 A-BOMBS (ring) | PASS | PASS | 8.5 | Boldest blast; less blue |
| N11 SURVIVED | PASS | PASS | 8 | Same as N10, verb instead of number |
| N9 TARGET | PASS | PASS | 7.5 | Adds to the title; word sits on the ship's hull |
| AI2 SURVIVED (AI) | PASS as a dramatisation only | vidIQ output | 7 | Not Nevada's exact outline; STYLE_LOCK s6 wants real photos |
| AI1 2 A-BOMBS (AI) | **FAIL** (wrong ship; blast placed where it would engulf her) | vidIQ output | 6 | Do not use |

### Truth
- **"2 A-BOMBS" / "SURVIVED": PASS.** FACTCHECK_B F1: present and afloat after Able (1 Jul) and Baker (25 Jul 1946). No "only",
  no "unscathed". The split shows one bomb (Able); "2" is about her, and the hook says the second bomb within seconds.
- **"TARGET": PASS.** C1 (Zeropoint / bull's-eye ship for Able) and she was in the Baker target array (BUAER table, 1,060 yd).
- **Picture order.** The Nevada frame shows her topmasts and yardarm standing, so it predates Able (BS-A1: both topmasts came down in Able); exact date not recorded. A split does not
  claim "after"; no word says "after" or "then/now". Fine.
- **Which bomb.** Both mushroom frames are Able (FOOTAGE_LIST w03 4.1-37.8 s and 53-60 s). No Baker image is used beside a
  word that implies she was aimed at in Baker. Neither frame shows Nevada; none is captioned as showing her.
- **Colour.** The ship's colour comes from the video's `w01g` window (colour-corrected toward the documented international
  orange, BS-A1); FACTCHECK_B C2 forbids "red". First build added a +12 % global colour push: **removed** (fix 1 below), so
  the thumbnail adds no colour to the ship; the sea/sky-only grade stays (STYLE_LOCK s6). Nothing written about colour.
- **Restoration.** Median stack + scratch fill remove film defects only (no inpainted objects, no AI upscaling). Disclosed in NOTES_v2.

### Rights: all real-photo drafts PASS
| Source | Used in | Basis |
|---|---|---|
| MN 6517 `w01g` 3.4 s, 5.5 s | all splits, N2, N3, N8 | US Navy production (COMJTF-1, "MN 6517 NPC 1949") = federal work; archive.org `OperationCrossroads`; already in MANIFEST/CREDITS |
| MN 6517 `w03` 29.5 s, 54 s | N1, N4-N6, N9-N11 | same film, already credited (CREDITS row `crossroads_mn6517_w03`) |
| vidIQ generated images | AI1, AI2 | AI output, no archive input; label "AI" if ever used; tick YouTube's synthetic box already applies |
Residual (as v1): NARA lists some Navy colour reels "Undetermined"; treated as federal work. No NC/ND material, no wreck
imagery (Ocean Infinity/SEARCH) used.

### Design
- **Zones.** Word boxes: 2 A-BOMBS x 340-940, SURVIVED x 387-892, TARGET x 54-445, all y >= 540; bottom-right 300x160 holds sea /
  dark lagoon only (luma 0.20-0.29). **N5's top word ran to x 1176, into the hover-icon corner: fixed** (128 px at x 668,
  ends ~1120). Top-right is sky/cloud in all picks.
- **Sidebar.** At 168x94 the tower + turrets read as a battleship, the mushroom reads at once, the red box survives greyscale
  (`sidebar_strip_v2_grey.png`).
- **Divider** 10 px white: survives the downscale as a 1 px line (keeps the "two photos" reading honest).
- **Softness.** 16 mm source; sharpen 1.1 after resize only. N10's lagoon blast is native resolution (no upscale).
- **AI1/AI2.** No watermark, logo or garbled text at 100 %. AI2's sea/orange are hyper-saturated next to our real frames; it
  would look like a different channel's template (FF AI look, study DON'T 5).

### Fixes applied in this round
1. Removed the +12 % colour push on the Nevada pieces (tonal contrast 1.08 only). N6 re-scored 90 -> 90; N3 89 -> 86 (kept honest).
2. N5 top word moved out of the hover corner.
3. Rebuilt everything; strips regenerated.

## Not done / open
- Owner: accept "2 A-BOMBS" restating the main title (data neutral), or lead with N9 TARGET.
- Owner: AI2 is offered only because the brief allowed 1-2 AI extras; the locked rule (STYLE_LOCK s6) is real photos only.
- A 4K/2K re-scan of the MN 6517 reel (`IA000015_OperationCrossroads.mov`, 1920x1080 ProRes) would not add detail beyond the
  current frames; the softness is in the 16 mm original.
