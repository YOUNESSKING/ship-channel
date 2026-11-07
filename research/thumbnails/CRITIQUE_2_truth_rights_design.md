# Critique 2: truth, rights and design of the Oriskany thumbnail concepts

Reviewer: independent critic, 2026-11-07. Scope: the 3 concepts in `THUMBNAIL_STUDY.md` §10 (`concepts_mockup.jpg`)
and the 3 current drafts `videos/oriskany/thumbnails/v2_T1/T2/T3*.jpg` (`make_thumbs_v2.py`).
Launch title: "Nobody Wanted This Aircraft Carrier, So They Sank It".

Checked: FACT_SHEET + FACTCHECK_A/B/C, NARRATION_v3, `full/build/make_shotlists.py` (on-screen cards), FOOTAGE_LIST,
CREDITS, MANIFEST, the source photos at full size, the 1969 reel (`footage/src/film/nara_87411.mp4`), and the live NARA
catalog records (`catalog.archives.gov/proxy/records/search?naId=…`, fetched today) for 87411, 6698620, 6698621,
6698623 and 6450776. I made throwaway test renders in the scratchpad. None of them is a deliverable. Paths are at the end.

## Verdict table

| Candidate | Truth | Rights | Craft /10 | One line |
|---|---|---|---|---|
| Concept 1: "37 MINUTES" on 6698623 | **PASS** | **PASS** | **6** | True and spoken twice. But at 168×94 it is an orange plank in foam, the same failure that sank T1. The island is under water in this frame. |
| Concept 2: "700 LB INSIDE" on 6698621 | **FAIL as worded** (PASS with fix) | **PASS** (not yet in CREDITS) | **6** (8 with fixes) | Best carrier silhouette of the shoot. The bare "700 LB INSIDE" reads as explosives. The crop clips the island. |
| Concept 3: split "1969 \| 2006" (as specified) | **PASS** | **PASS** (low residual risk, see §2) | **4.5** | The specified crop cuts ~45 % of the 1969 ship. The right half duplicates Concept 1. |
| Concept 3 rebuilt: stacked, 1969 over 2006 (6698621) | **PASS** | **PASS** | **8** (tested) | The best thumbnail on the table: the same ship from the same side, blue then, rust now. |
| v2 T1 "NAVY DID THIS" (6698624) | PASS | PASS | 4.5 | Rust slab. Drop it. |
| v2 T2 "37 MINUTES" (6698619) | PASS | PASS | 6.5 | Reads as a carrier. The sea is graded violet (measured hue 274°), not blue. |
| v2 T3 "WHAT'S LEFT INSIDE?" (6698625) | PASS | PASS | 5 | A thin wedge in a foam disc. |

---

## 1. Truth

### Concept 1: "37 MINUTES": PASS
- Fact: FACT_SHEET G5, HIGH. FACTCHECK_C confirms 10:25 → 11:02 a.m. CT (NAVREL, MARAD07, AP06, GWR). BBC's "30 minutes"
  is the outlier.
- The video says it at **~0:12** (NARRATION_v3 l.5: "Thirty-seven minutes later, she was gone.") and again at **~8:10**
  (l.79, "She took thirty-seven minutes."). Chapter c05 is titled "Thirty-Seven Minutes", and the shot list shows a
  counting "37 minutes" card (`make_shotlists.py` l.225). The promise is paid off within 15 s.
- The words add to the launch title: they say how fast. ✔
- Picture note: the study says 6698623 has "two small boats for scale". At full size (`z623.png`), the right-hand object
  in the foam is **not a boat**. It is the top of Oriskany's **island** (stack cap and platforms) going under. Only the
  left object is a boat. This is not a truth problem for the thumbnail, because nothing is captioned. But it explains the
  craft problem: the one feature that says "aircraft carrier" is already under water in this frame.

### Concept 2: "700 LB INSIDE": FAIL as worded
- Fact: E7, HIGH. FACTCHECK_B B18 confirms "an estimated 700 lb" of solid PCBs (EPA release, NAVSEA fact sheet). The video
  says "An estimated seven hundred pounds stayed aboard" (l.87, ~8:40) and shows a "PCBs LEFT ABOARD ≈700 lb" card
  with the kicker "Still inside her" (`make_shotlists.py` l.238–239). So the number is delivered.
- **Why it still fails:** on a photo of a carrier being scuttled, "700 LB INSIDE" will be read as *explosives*. The
  video itself primes that reading. The hook says "twenty-two charges inside" (l.5). l.77 says "more than five hundred
  pounds of explosives". FACTCHECK_C notes MARAD's "approximately 750 pounds of explosives". The fire chapter shows a
  "≈700 FLARES IN THE LOCKER" card (l.154). A viewer who clicks for "700 lb of something dangerous left inside" meets
  three other ~700/~500 figures before the PCB payoff. Paired with title D ("What the Navy Left Inside…"), it suggests
  the Navy left 700 lb of explosives aboard, which is false. That is the kind of contradiction behind the two "text
  contradicts title" flops in the study (§7).
- It also doesn't pair with the launch title. Test & Compare tests thumbnails under **one** title, and under "Nobody
  Wanted This Aircraft Carrier…" the words "700 LB INSIDE" are a non sequitur. Keep this concept for a title-D test only.
- **Fix:** "**700 LB OF PCBs**" (3 words plus a number, Anton 130 px ≈ 760 px wide) or "**PCBs LEFT INSIDE**". Either is
  then a PASS. Do not use "≈": Anton has no ≈ glyph (it renders as a .notdef box). "~700" renders but reads as noise
  at 168 px. A bare "700" is acceptable rounding, because the source figure is itself "an estimated 700". Never "TOXIC"
  or "POISON" (TITLES_THUMBS rule).

### Concept 3: "1969 | 2006": PASS (both frames are Oriskany in those years)
- **1969 frame:** NARA 87411. Catalog title "AERIALS OF USS ORISKANY (CVA-34)", productionDate **1969-09-10**, RG 428
  (General Records of the Department of the Navy), series "Moving Images Relating to Military Activities". The ship in
  the frame matches Oriskany's post-1959 SCB-125A fit: angled deck, enclosed hurricane bow, single island with a tall
  lattice mast. The hull number is **not legible** (SD film), so identity rests on the NARA title. MANIFEST already rates
  it HIGH and uses this reel 4 times in the cut, so the thumbnail is consistent with the video. Small gap: the production
  date has not been cross-checked against her 1969 WestPac cruise dates. Add one line to the fact sheet (DANFS) before
  publish. A wrong year here would be a visible error. A wrong ship is very unlikely.
- **2006 frame:** 6698623. Catalog: "Aerial starboard side stern view … USS ORISKANY (CV 34) sinking", 17 May 2006. ✔
- The years are the frames' own dates, so they claim nothing beyond what the frames show. ✔

### v2 drafts
- T1 "NAVY DID THIS": PASS (G2, Navy EOD set the charges; paid off at 0:05). T2 "37 MINUTES": PASS. 6698619 is the
  moment the charges fire, which is when the 37-minute clock starts, so the words and the picture agree. T3 "WHAT'S LEFT
  INSIDE?": PASS. It is a question, answered at ~8:40.

### Does anything promise what the video doesn't deliver?
Only Concept 2 as worded (the explosives reading). Nothing else over-promises. None of the concepts says "toxic",
"secret", "disaster" or "largest".

---

## 2. Rights

| Source | NARA useRestriction (live, today) | Creator | Verdict | In CREDITS.md? |
|---|---|---|---|---|
| 6698620 (starboard bow, sinking) | Unrestricted | PH2 Jeffrey P. Kraus, USN | PASS: PD, 17 USC 105 | yes (l.101) |
| 6698621 (starboard bow, deck awash) | Unrestricted | PH2 Kraus, USN | PASS | **no: add it** |
| 6698623 (starboard stern, last of the deck) | Unrestricted | PH2 Kraus, USN | PASS | yes |
| 6698619 / 6698624 / 6698625 (v2 drafts) | Unrestricted | PH2 Kraus, USN | PASS | yes |
| 6450776 (Bremerton, 1990) | Unrestricted | LT Fallon, USN | PASS | yes |
| 87411 (1969 aerials, film) | **Undetermined** (accessRestriction: Unrestricted) | none listed; RG 428, 428-NPC (Naval Photographic Center) | **PASS, low residual risk** | yes (l.37–38) |

**87411 decision: usable.** NARA's "Undetermined" is its default for reels nobody has reviewed. It is not a finding of
a restriction. The reel is a 428-NPC item, "Aerials of USS Oriskany", raw Navy aerial footage of a Navy ship in a Navy
record group. That is a work of federal employees on duty, so it is public domain under 17 USC 105. FOOTAGE_LIST (rights
basis, l.5) and CREDITS already reached that conclusion, and the film is in the cut 4 times (f_c02_s01, f_c03_s40/41,
f_c07_s43/48). If the reel were not PD, the video would already carry the risk, so the thumbnail adds none. The residual
risk is that RG 428 holds a few donated or contractor reels. Nothing in this record suggests that (no creator, no
copyright note, no newsreel title).

Fallback if the owner wants zero "Undetermined" items: a 1959 post-conversion broadside, **NARA 7578428–7578434**
(19-NN-CVA 34, "after SCB-125A conversion", 27 Apr 1959, **Unrestricted**, 3150 px). Label it "1959". It has the same
angled-deck silhouette as 2006, so the then/now match still holds. It is **B&W**, though, which loses the blue
advantage that is the whole reason for this concept. 6450776 (1990) is colour but grey and moored, and "1990 | 2006"
says "laid up, then sunk", which is a weaker contrast. The study's fallback, 6450776, is legal but a design downgrade.

**Housekeeping (CLAUDE.md "log every file"):** add 6698621 to `full/CREDITS.md`, and add a "Thumbnail" note on every
row whose item appears in the chosen thumbnails (87411, 6698620/21/23).

---

## 3. Design craft

### Measured sea colour (mean RGB of open-sea patches)
| Frame | Hue | Saturation (HLS) | Lightness | Note |
|---|---|---|---|---|
| 1969 film (87411) | 220° | **0.57** | 0.40 | real saturated blue |
| 6698623, upper sea | 224° | 0.20 | 0.76 | the bluest 2006 frame |
| 6698623, lower right | n/a | 0.01 | 0.37 | neutral grey |
| 6698621, mid sea | n/a | 0.01 | 0.58 | neutral grey |
| 6698620 | n/a | 0.01 | 0.28 | grey-green |
| v2 T2 output sea | **274°** | 0.06 | 0.31 | **violet**: the v2 grade pushed a slightly magenta source toward purple |

### Can an honest grade make the 2006 sea blue?
**Steel-blue, yes. Turquoise, no.** And the study's grade recipe will not get there:
- It masks by hue 160–270°. At saturation 0.01 the hue is noise, so the mask comes out patchy and blotchy, and "+40 %
  saturation" of 0.01 is 0.014, which is invisible. The recipe only works on the top band of 6698623.
- What works (tested, `g_both.jpg`): a **Lab b\* shift of −12 to −14 and a\* of −2 to −3, on the sea only**, plus an
  L lift of +8–15 % on the sea, feathered 5–8 px, with σ≈0.6 noise added in Lab. That is a white-balance correction of
  hazy grey water. It is defensible, and it reads as steel-blue at feed size.
- **Two honesty traps I hit in testing:**
  1. On 6698621 the grey hull has the same saturation as the sea, so a colour-based mask **turned the hull blue**
     (`g_both.jpg` bottom). Use a **hand-drawn ship polygon** (island, deck, hull, anchor chains) as an exclusion.
     Never use a colour key.
  2. A mask with the wrong horizon tinted a **blue wedge into the grey sky** (`c1b_view.jpg`). Stop the mask exactly
     at the horizon line and leave the sky untouched.
- The ceiling: sea saturation no higher than **0.25** (HLS), hue 205–220°. Anything beyond that, or any cyan/green push,
  is repainting. If you want real blue, it has to come from the 1969 film. That is the strongest argument for the
  split concept.
- Fix T2's violet: neutralise the sea first (a\* −3 to bring hue 274° back to neutral), then b\* −12. Remove the
  `[-6, +4, +18]` RGB push in `grade()`, which is what creates the purple.

### Reads as an aircraft carrier at 168×94? (I rendered each crop at true sidebar size)
| Frame | Island visible | Verdict at 168×94 |
|---|---|---|
| 6698621 (Concept 2) | yes, plus the full deck and the bow overhang | **clearly a carrier** (best) |
| 6698620 | yes, plus the deck markings, ship awash | **clearly a carrier, clearly sinking** |
| 87411, 1969 (stacked strip) | yes, plus the wake | **clearly a carrier** |
| 6698619 (T2) | yes, plus smoke | carrier |
| 6698623 (Concept 1) | **no, it is under water** | "orange plank in foam". The same failure mode both earlier critics flagged in T1 |
| 6698624 / 6698625 (T1/T3) | no | slab / wedge |

### Text legibility
Anton at 130–150 px gives 17–20 px cap height at 168×94: legible. The white plus red #E0352B with a 4 px stroke is fine.
The problems are placement, not type:
- Concept 2's mock-up puts the words on a darkened band of pale haze. It looks muddy, and it is the only dark zone in a
  bright frame (the study's own "dark overall" minus).
- Concept 3's "1969" sits on a soft SD sky. It is fine at feed size.

### Banding and compression
- The top-left 620×330 gradient in Concept 1 ramps from light sea to dark over a short distance. Keep `shade()`'s
  σ=3 noise on the mask and a blur of ≥60 px, and export q95 with 4:4:4 (as `save()` does).
- The 1969 frame is **720×480 SD** (SAR 10:11; the 1080p clip is a pillarboxed upscale with a dark gate bar at
  x≈1650–1690). A smooth SD sky upscaled 2.5–3× shows blocky bands. Crop most of the sky out of the 1969 strip and add
  1–1.5 % monochrome grain. Use a **non-generative** upscale only (Lanczos plus a light unsharp). No AI upscaler: it
  would invent hull detail on an identity shot.
- At real feed size (desktop home ≈ 360×202, so each stacked strip is ~360×101), the SD source is at or above native
  resolution, so the softness only shows on TV-size tiles. Acceptable.

### Safe zones (1280×720)
- Bottom-right timestamp: x 1100–1280, y 640–720. Hover icons (Watch later / Add to queue): x 1150–1280, y 0–130. Keep
  both clear of words and of key ship detail.
- In Concept 2 the bow forefoot and the anchor chain fall under the timestamp (minor). Every other candidate has open
  sea there.

---

## 4. Per-candidate fixes (exact numbers)

### Concept 1, "37 MINUTES" on 6698623: Truth PASS · Rights PASS · Craft 6/10
1. Crop `(0, 140, 3000, 1828)`, not the study's top edge y≈93. At y 93 a sliver of the far patrol boat (source y ≈
   83–105) stays on the top edge.
2. Grade: the Lab sea-only grade above (b\* −14, a\* −3, L +8 %). This frame takes it best (`g623_sb.png` reads blue).
3. Words: keep "37" red + "MINUTES" white, 150 px, top-left x 40, y 20. With this crop the deck corner lands at about
   (736, 142), so the text stays off the ship.
4. **The real fix is the photo.** If the slab still fails a 5-second "what is this?" test with someone who hasn't seen
   the project, move "37 MINUTES" to **6698620**. It has the island, the deck markings and the whole ship awash, and it
   is the **exact frame on screen when the narrator says "She took thirty-seven minutes"** (shot list l.225). Crop
   `(375, 100, 2935, 1540)`, which keeps the helicopter fuselage at bottom-left out. Words 130 px (not 150) at x 40,
   y 560, over dark sea; at 150 px "MINUTES" touches the hull at x ≈ 560–700. Grade the sea only, below the horizon at
   output y ≈ 285 (left) / 245 (right). Projected craft: 7.5/10.

### Concept 2, "700 LB INSIDE" on 6698621: Truth FAIL as worded · Rights PASS (log it) · Craft 6 → 8
1. Words: "**700 LB OF PCBs**" (or "PCBs LEFT INSIDE"). Pair it **only** with title D, not in the launch Test & Compare.
2. Crop: the study's 86 % crop centred at x 56 % starts at x≈390, exactly where the island's aft edge is, so the island
   gets clipped. Use `(120, 100, 2940, 1686)` (2820×1586). It keeps the whole island, loses ~45 px of the flight-deck tip,
   and stays above the helicopter skid (source y ≥ 1695 at x < 375).
3. Words placement: not on the sky band. Right-align at x 1240, cap top at y ≈ 175, 120–130 px, over the open sea
   between the horizon and the bow deck. In this crop that is clean sea from y ≈ 118–170 to ≈ 370 across the right
   half. The left end must clear the horizon (≈ y 170 at x 480). That keeps the hover-icon zone (y < 130) clear and needs
   only a light gradient (alpha ≤ 110), because the sea is mid-grey.
4. Grade: sea only (b\* −14, a\* −3, L +15 %) with a **hand ship mask**. Lift the hull shadow side +0.4 EV inside the
   ship mask with a luminance curve, no colour shift.

### Concept 3, "1969 | 2006" as specified: Truth PASS · Rights PASS · Craft 4.5/10
- The specified 1969 crop (centre x 69 %, 520×585 of the 1080 clip at 0:02) spans x 1065–1585. In that frame the ship
  runs from x 740 to x 1470, so the crop **cuts the stern half** (visible in the mock-up). The halves are 84 px wide at
  168×94, so each ship is ≤ 70 px. The right half is the same 6698623 slab as Concept 1, so Concept 1 and Concept 3 in one
  Test & Compare would partly test the same image.

### Concept 3 rebuilt: **stacked**, 1969 above / 2006 below: Truth PASS · Rights PASS · Craft 8/10 (tested: `c3_stack_view.jpg`)
Both ships are long and horizontal, so a top/bottom split (two 1280×360 strips) roughly doubles the ship size at sidebar
scale (~137 px wide instead of ~70). Both frames show the **starboard side, bow to the right, island visible**, so it
reads as the same ship at once. That match is true: both frames are catalogued starboard views.
1. Top strip: grab from the **reel**, not the 1080 clip. `nara_87411.mp4` at t≈62 s (progressive, 720×480). Resize to
   655×480 to correct the 10:11 SAR, crop `(109, 208, 591, 344)`, Lanczos to 1280×360, then UnsharpMask(2, 50, 2) and
   1–1.5 % grain. Better still, set the crop top to ~225 so less SD sky shows (banding). Stay inside the clean area
   (`make_segments.py` 684×456+16+12).
2. Bottom strip: **6698621** crop `(0, 740, 3000, 1584)` to 1280×360. Sea-only Lab grade with a hand ship mask.
3. Divider: white bar, 8 px (y 356–364).
4. Words: "**1969**" white, 130 px, x 30, y ≈ 190 (over the wake, left of the stern, which lands at x ≈ 314).
   "**2006**" red #E0352B, 130 px, x 30, y ≈ 560 (over the foreground sea, below the island). The bottom-right and
   top-right are clear.
5. Optional third word: none. The dates are the hook, and the title says the rest.

### v2 T2 "37 MINUTES" (6698619): Truth PASS · Rights PASS · Craft 6.5/10
- Fix the violet sea (see §3). Text bottom glyph edge ≈ y 698 is 22 px from the frame edge, and the watched-progress
  bar covers the bottom ~4–6 px, so move the baseline up 20 px. Superseded by Concept 1 / 6698620 if those are built.

### v2 T1 (4.5/10) and T3 (5/10)
- Retire both. The slab and the wedge fail the 168×94 test, and both promises are carried better elsewhere.

---

## 5. Final recommended 3 for Test & Compare (launch title: "Nobody Wanted This Aircraft Carrier, So They Sank It")

| Slot | Thumbnail | Promise | Why |
|---|---|---|---|
| **A** | **"37 MINUTES" on NARA 6698620** (crop and grade §4, Concept 1 item 4) | speed | The study's best word signal (a true number) on the frame that reads most clearly as a sinking carrier. It is literally the frame on screen when "thirty-seven minutes" is spoken. |
| **B** | **Stacked "1969 / 2006": NARA 87411 over NARA 6698621** | then/now | The only honest route to a really blue thumbnail, the best-scoring cross-cutting feature (split), two true numbers, and the clearest "same ship" read at sidebar size. |
| **C** | **"WHAT'S LEFT INSIDE?" on NARA 6698623** (Concept 1's crop and grade; words 130 px at x 40, y 20, ≈ 990 px wide) | mystery | The brightest, bluest 2006 frame. A question cannot mislead, and the hook pays it off ("what was still inside her", 0:20). The slab read is the weak point; slots A and B carry the carrier read. |

Each slot uses a different image and a different promise, so the test measures something. Keep Concept 2 ("700 LB OF
PCBs" on 6698621) for a later title-D test. Before upload: log 6698621 and the thumbnail uses in CREDITS.md, add the
1969 cruise-date check to the fact sheet, and review all three at 168×94 and on a feed strip next to 2–3 real carrier
videos. Judge on day 7–14.

---

Scratch test renders (not deliverables), in `/tmp/claude-0/-home-user/e065d3fa-b63b-536b-bb86-8680d09491b8/scratchpad/`:
`z623.png` (island top in the foam), `g_both.jpg` / `g_sb.png` (Lab grade; the blue-hull trap on 6698621),
`c3_stack_view.jpg` (stacked split at full, 4× sidebar and 1× sidebar), `c1b_view.jpg` (6698620 "37 MINUTES"; the sky
wedge is a mask error, shown as a warning), `reel62.png` (the 1969 reel frame).
