# Critique 1: Mallows Bay thumbnails, click-through and fit with the study data

Critic: independent CTR pass, 2026-11-15. Drafts judged: `V1_ghost_fleet.jpg`, `V2_1936_today.jpg`, `V3_3200_a_ship.jpg`
(builder `make_thumbs_v2.py`), with `T1–T3` as the older baseline. Title tested against: **"100+ Ships Are Rotting 30 Miles
From the White House"**. Read first: `research/thumbnails/THUMBNAIL_STUDY.md` §6–10, `CRITIQUE_1_method_ctr.md`,
`FORGOTTEN_FLEET_STUDY.md` (final DO/DON'T), `PACKAGING_GUIDE.md` §3, `LESSONS_PUBLISHING_AND_THUMBNAILS.md` part 2.

Tests (scratchpad only, nothing in the repo was edited except this file):
1. Pixel metrics on every draft (mean luminance, saturation, blue-hue share, luminance of the red words against what is behind them).
2. 168×94 renders, plus a greyscale + 1 px blur "squint" version of each.
3. A **feed test**: our 168×94 tiles pasted between real sheet A winners (FF Arizona, Sunken Inside, FF "85 YEARS LATER",
   Deep Sea Relics Yamato, Historsea "SECRET WARSHIP GRAVEYARD", Drowned Iron Akagi) and sheet C losers.
4. Mock-ups of the fixes below, built with the builder's own functions (`cover`, `sea_grade`, `word_shade`, `words`).

## Verdict

| Criterion (study §9, adapted to a fleet of wrecks) | V1 GHOST FLEET | V2 1936 \| TODAY | V3 $3,200 A SHIP |
|---|---|---|---|
| 1. Blue/teal sea dominant | 0.5: blue-hue share 36 %, but the bottom half is rust | 0.5: only the right half (24 %) | **1**: 44 %, the bluest of all six drafts |
| 2. Not dark overall | 1 (mean L 0.43) | 1 (0.56) | 1 (0.38, sunlit) |
| 3. Colour, not B&W | 1 | 0.5: half is B&W | 1 |
| 4. Wreck as the subject | 1 | 1 | 1 |
| 5. Reads as **ships/wrecks** at 168×94 | 0.5: a rusty pier or burnt jetty; no hull shape | 0.5: left half is a leaf/fish-scale texture; right half = V1's debris | 0.5: the hulls read as sandbars; the **kayak** is the clearest object |
| 6. True number in the words | 0 | 0.5: a year, and "1936" alone means nothing to a stranger | **1**: $750,000 ÷ 233 = $3,219 (FACTCHECK_A D5), spoken in NARRATION_v2 l. 77 |
| 7. Avoids arrow/circle, face, giant-name templates | 0.5: the place's nickname as giant text is the NAME_TEXT pattern (0.84×) | 1 | 1 |
| 8. Distinct from the FF/clone AI-yellow look | 1 | 1 | 1 |
| 9. Nothing in the bottom-right 300×160 | 1 | 1 | 1 |
| **Total /9** | **6.5** | **7.0** | **8.5** |
| Clear at sidebar size? | Text yes; picture no | Text yes; picture half | Text yes; picture half |
| Obvious focal point? | No: the words, then a mass of rust | Yes: the split itself | Wrong one: the cyan kayak |
| Red word survives greyscale? | **No** | **No** | **No** |
| Stands out in the feed test? | No: brown-blue mush next to single-ship heroes | **Yes**: the white half is unique in a blue feed | Partly: bright, but reads as a kayak-tour vlog |
| Pairs with the title (one promise, completes) | **Repeats** ("fleet" = "100+ ships", "ghost" = "rotting") | Weak: "TODAY" repeats "Are Rotting" | **Completes**: why is a fleet worth $3,200 a ship? |
| **Rank** | **3** | **2** | **1** |

All three beat the old T1–T3 (T1 B&W, T2 dark L 0.31 and no wreck visible, T3 sepia with no ship). The v2 brief from the
study was followed: blue, bright, colour, real PD images, nothing bottom-right. **But the fixes went to the colour, which
the critique of the study already called the weakest signal, and not to the one thing every sheet A winner has: one
large, unmistakable ship shape.** In the feed test, every winner's tile shows a hull outline you can name at a glance.
None of ours do. That is the main problem, and it can be partly fixed with crops.

## Problems that hit all three

1. **No ship shape.** Mallows Bay's wooden steamers burned to the waterline in 1925; from a low drone angle they are lines
   of stakes. At 168×94 that reads as jetties, oyster beds or a flooded pier. The only images in our PD pool where the
   hulls clearly look like *boats* are the **1936 aerial** (pointed hull outlines from above) and the **bow of the
   hulk** in the NOAA drone clip at 1.0–1.5 s (V1 uses 1.6 s, when the bow has slid out of frame).
2. **The red word disappears.** Red #E0352B has a luma of 103. The sea behind the red words, even after `word_shade`, is
   73–93 (measured). In the greyscale squint test "FLEET", "TODAY" and "$3,200" vanish and only the black stroke is left.
   Red on blue only works on hue, and hue is the first thing lost on a small, dim phone screen or for colour-blind viewers
   (red/blue are fine for them, but the luma match still kills it in peripheral vision). The **payload word** is the red one
   in V2 and V3, so the most important word is the weakest one. Fix: white word on a solid red box (the Forgotten
   Naval History "one white word in a red box" look, 3 of the top 11 in sheet A). In the mock it survives greyscale.
3. **Word position is fine**: all top-left, cap height ~150 px (≈ 21 % of the height, ≈ 20 px at 168×94), right edge ≤ x 930,
   clear of the top-right hover icons and the bottom-right timestamp. Keep that. Do not move words to the top-right.

## Per draft

### V1 GHOST FLEET: rank 3, 6.5/9. Rework or drop.
- **The words add nothing.** "Ghost fleet" is the site's common name, so it is also the title of most existing Mallows Bay
  videos and articles. In Search it blends in; in Browse it repeats the title ("100+ ships rotting" = a ghost fleet). The
  study's NAME_TEXT template (the name as giant text) is one of the two weak ones (0.84×, 1/9 hits).
- **The picture is a rust heap.** The foreground hulk fills 55 % of the frame, but its bow (the only ship cue, the pale
  planking curve bottom-left) is cut at the frame edge. The hull rows behind read as jetties.
- **Fix (if kept for testing):** frame at **t = 1.2 s** instead of 1.6 s; `cover(d, cx=0.0, cy=0.75)`; same grade. That
  brings the whole bow curve in, so the hulk reads as a ship's bow. Change the words to **"TOO LATE"** ("TOO" white, "LATE" white
  on a red box), Anton 170, top-left at x 44, y 18. It completes the title ("why are they rotting? they came too late") and
  is a mystery the video answers in act 1–2. **Owner check:** FACT_SHEET C19 (HIGH) / FACTCHECK_A (MED): "none reached a
  European port during hostilities"; a thumbnail can't hedge, so the owner must OK it. Fallback: **"BURNED"** (1925 burn,
  Quantico photos). Do not use "NEVER SAILED" (C19 forbids it).

### V2 1936 | TODAY: rank 2, 7.0/9 as built; ~8/9 with the fixes. Test & Compare slot B.
- **Right idea, wrong crop.** The 1936 aerial is the single best "100+ ships" proof we own: rows of ship-shaped hulls from
  above, a NARA PD photo (useRestriction Unrestricted). The builder's crop `(560, 230, 1180, 816)` shows ~50 hulls, each
  ≈ 3 px wide at 168×94, so it turns into a texture (leaves, scales). Also gamma 1.9 + contrast 1.25 blows the hull
  interiors out into blotches.
- **The words are the weak half.** "1936" carries no meaning for a stranger (critique 1: years only work when the ship is
  famous), and "TODAY" restates the title's present tense. The split earns its place as **a picture** (dozens of
  boats → rotting stakes), not through the words. Then/now evidence in the study is n = 2, so this is the test slot,
  not the lead.
- **B&W half:** the study counts B&W as a minus, but critique 1 showed that is a cross-channel effect. In our feed test
  the white half is the most distinct tile on the page, because every competitor is blue. Keep it.
- **Fixes (exact):**
  - Left crop: `old.crop((980, 0, 1300, 360))` (the darkest, largest hulls next to the shore; 8:9, ≈ 12 hulls, each ≈ 10 px
    wide at sidebar size). Gamma **1.6** (was 1.9); keep the cool tint and contrast 1.25.
  - Right half: frame **t = 1.2 s** (was 2.2), `cover(rows, 640, 720, cx=0.0, cy=0.5)`. The hulk's bow then fills the lower
    half of the right side: a ship shape on both sides of the divider.
  - "TODAY": white Anton 140 on a solid red #E0352B box (padding 14 px, stroke 3 px), text origin x 690, y 28. "1936" unchanged
    (white, 150, x 36, y 14).
  - Mock: `/tmp/claude-0/-home-user-ship-channel/80a206ad-823b-5d4d-a2c7-aa717ce129a3/scratchpad/critic1/mock/v2_fixA.jpg`.
    At 168×94 the 1936 hulls read as boats, the red box survives greyscale.

### V3 $3,200 A SHIP: rank 1, 8.5/9. Main upload, after fixes.
- **Best words of the three.** It is the only draft whose text **completes** the title instead of repeating it: the title
  says *where* and *how many*, the thumbnail adds a paradox (*a fleet sold for $3,200 a ship?*). True and spoken (narration
  line 77 of 183, ~40 % in, so the promise is paid mid-video, not at the end). A viewer may read it as "you can buy one
  today"; that is curiosity, not a contradiction, since the video states it is the 1922 price.
- **Wrong focal point.** The most saturated, most compact object is the cyan kayak. At sidebar size the thumbnail reads as a
  paddling-trip vlog, and the hulls read as sandbars. The wrecks have to dominate, with the kayak kept small as the scale cue.
- **The number is the invisible word** (red on blue, luma 103 against 73). The number is the payload, so it must be the most
  legible thing in the frame.
- **Source resolution:** the NOAA file is 1000×563 (`...-kayaker-1000.jpg`), upscaled 1.28× already. Fine at feed size,
  soft on TV. Look for a larger master on the NOAA page (same image without the `-1000` suffix) before the final export.
- **Fixes (exact):**
  - Crop: `cover(k, cx=0.62, cy=0.80, zoom=1.15)` (was 0.5 / 0.6 / 1.0). The long pointed hull in the middle becomes the
    biggest shape (≈ 60 % of the width); the kayak drops to the lower-left third and stays in as scale; the tree line shrinks.
    Do not go past zoom 1.15 on the 1000 px source.
  - Words: **"$3,200"** white Anton 165 on a red box (pad 14, stroke 3), origin x 50, y 22; **"A SHIP"** white Anton 165,
    22 px after the box. One line, ends ≈ x 840. `word_shade` stays (0.55, box 10, 10, 980, 210).
  - Grade: unchanged (sea-only, hue toward 195°, lift 0.3 EV). Do **not** desaturate the kayak (no local repaint rule);
    the crop does the work.
  - Mock: `/tmp/claude-0/-home-user-ship-channel/80a206ad-823b-5d4d-a2c7-aa717ce129a3/scratchpad/critic1/mock/v3_fixD.jpg`.
- Expected score after fixes: 9/9 on the rubric, with "reads as wrecks" still the soft spot (it is 0.5 → ~0.75; no PD frame of
  this site will ever read like an intact battleship).

## Main upload and Test & Compare

| Slot | Draft | Words | What it adds to the title |
|---|---|---|---|
| **Main (A)** | V3 fixed | **$3,200** (red box) A SHIP | A paradox: price |
| **B** | V2 fixed | 1936 \| **TODAY** (red box) | Proof of scale over time (the picture, not the words) |
| **C** (optional) | V1 reworked | TOO **LATE** (red box) | A mystery: why they were wasted. Only with owner OK on C19; otherwise run A against B only |

V1 as it stands ("GHOST FLEET") should not go into the test: it repeats the title and is the default name every competitor
already uses. Judge on day 7–14 data (watch-time share), not day 1.

## Checklist for the builder (`make_thumbs_v2.py`)
1. Add a `boxword()` helper: red #E0352B rectangle with 14 px padding behind a white Anton word with a 3 px #080A0E stroke.
   Use it for the one red element in each thumbnail; never draw red text straight on the sea.
2. V1: frame t 1.6 → 1.2, `cx 0.25 → 0.0`, `cy 0.6 → 0.75`; words → "TOO LATE" (owner check) or drop V1.
3. V2: left crop → `(980, 0, 1300, 360)`, gamma 1.9 → 1.6; right frame t 2.2 → 1.2, `cx 0.35 → 0.0`; "TODAY" → white on red box, 140 px, at (690, 28).
4. V3: `cover(k, cx=0.62, cy=0.80, zoom=1.15)`; "$3,200" → white on red box, 165 px, at (50, 22); "A SHIP" white 165 after it.
5. Re-export the 168×94 strip **and a greyscale copy of it**; every word must still be readable in the grey copy.
6. Paste the strip into sheet A (as in the feed test) and ask someone who hasn't seen the video "what is this a picture of?".
   If the answer isn't "old shipwrecks / a ship graveyard", recrop.

## Rights notes found on the way
- Do **not** use the striking top-down "hull mosaic" or the tree-topped-hull drone shots in `hq_noaa_wk240_sanctuary.mp4`
  (0:15–0:28). MANIFEST flags them as likely Duke University footage (not PD), and they have burned-in text.
- All three V drafts use cleared material: NOAA staff drone clip `hq_noaa_wk309_birds` (frames before the 3 s "earth is blue"
  overlay), NARA 18-AA-70-44 (Unrestricted), NOAA photo by Matt McIntosh (US Gov work). The NOAA *Accomac* photos (Sassorossi,
  McIntosh) are the only images where a whole ship reads instantly, but *Accomac* is a 1928 ferry, not one of the WWI
  fleet; keep it for the video, not the thumbnail promise of "100+ ships".

## Owner decision 2026-11-15
Owner rejected V1-V3 ("none of these are good") and asked for vidIQ thumbnails. Two made with `vidiq_generate_thumbnail`
(44 credits, references: FF "Why The USS Arizona Can Never Be Raised" and Historsea "Philadelphia's Forgotten Warship Fleet"):
`AI1_ghost_fleet.jpg` (vidIQ self-score 86) and `AI2_30_miles_from_dc.jpg` (86). Both are AI images, not real photos.
Truth notes: AI2 shows the Capitol dome on the horizon, which cannot be seen from Mallows Bay (32 mi away): dramatised.
Both water colours are bluer and clearer than the real Potomac.
