# Critique 1: thumbnail study method + CTR judgement of the concepts

Critic: independent, skeptical pass, 2026-11-07. I recomputed every headline count from `data.csv` (240 coded) and
`all_videos.csv` (878) with my own script, viewed sheets A/B/C, `concepts_mockup.jpg`, the v2 drafts and their feed
strip, `competitor_compare.jpg`, and the 17 May 2006 frames 6698606–6698628. I also built quick mock-ups of my own
picks (scratchpad only, not committed). No vidIQ credits spent.

## Verdict in five lines

1. **The arithmetic is right; the labels are looser than the prose.** Every count in the TL;DR reproduces, but "blue sea"
   and "grey" overlap (22 thumbnails are coded as both), and the "then/now split 2.19×" is mostly *not* then/now.
2. **One finding is solid-ish:** saturated colour beats desaturated *within* channels (sign test 12 channels vs 1).
   Everything else (number, dark, wreck, template ranking) is noise-level at this n.
3. **The study is unblinded:** the coder looked at sheets with views and outlier printed on every tile, then coded
   subjective fields (palette, "dark"). That alone can produce a 47-vs-34 gap. Treat all colour findings as hints.
4. **Of the three concepts, Concept 2's photo is good but its words are risky, Concept 1's photo fails at sidebar size,
   and Concept 3 should be dropped.** The best single frame in the archive was not considered: **NARA 6698612** (bow
   high, island going under).
5. **Final Test & Compare set** (launch title "Nobody Wanted This Aircraft Carrier, So They Sank It"):
   **A = 6698612 + "37 MINUTES"**, **B = 6698621 + "$20 MILLION"**, **C = 6698624 recut + "NAVY DID THIS"**. Specs in §4.

## 1. Recomputed counts

Pool: 240 rows = 20 channels × 12 (top 4 / middle 4 / bottom 4 by outlier). A = 20, C = 20. My top-4/bottom-4 split
is re-derived per channel from `outlier`.

| Finding (study) | Study says | I get | Fisher p (2-sided) | Per-channel sign test (top-4 minus bottom-4) | Rating |
|---|---|---|---|---|---|
| Blue/teal/turquoise dominant | 12/20 vs 8/20; 47/80 vs 34/80 | **Same** (rule = palette contains blue/teal/turq) | A/C 0.34; 80/80 **0.057** | **12 channels +, 1 −, 7 tie; p = 0.003** | Real direction, overstated label (see 1a) |
| … same, but excluding "grey-blue/grey-teal" | — | 10/20 vs 7/20; **35/80 vs 28/80** | 0.33 | 8 +, 2 −; p = 0.11 | Effect halves when grey-blues are excluded |
| Grey/B&W/sepia palette | 2/20 vs 10/20; 32/80 vs 39/80 | **Same** (rule = palette starts with grey/sepia) | A/C **0.014**; 80/80 0.34 | (palette contains grey/sepia) 2 +, 11 −; p = 0.02 | A/C gap is cross-channel; mirror image of the blue finding |
| Archive B&W/sepia photo | 2/20 vs 8/20; 19/80 vs 28/80 | Not reproducible from `medium`: I get **1/20 vs 5/20; 15/80 vs 20/80** | — | 1 +, 5 −; p = 0.22 | Weak |
| Dark overall | 4/20 vs 1/20; 7/80 vs 15/80 | Same | 80/80 0.11 | 3 +, 7 −; p = 0.34 | Weak (3 of the 8-gap is Deep Sea Relics alone) |
| Number in text | 6/20 vs 3/20; 17/80 vs 12/80 | Same | 0.45 / 0.41 | 8 +, 5 −; p = 0.58 | **Noise** |
| 1–3 words or none | 9/20 vs 9/20; 46/80 vs 46/80 | Same | 1.0 | — | Correct "no effect" |
| AI image | 14/20 vs 11/20; 38/80 vs 37/80 | Same | — | — | Correct "no effect" |
| Same template for top-4 and bottom-4 | 14/20 channels | **14/20** | — | — | Correct |
| Split median 2.19× (n=6) | 2.19× | Same arithmetic | — | — | **Wrong label** (see 1b) |
| A and C same median age | 140 / 142 d | 140.5 / 142 | — | — | Correct, but see 1c |

Template medians (WRECK_UW 1.09, AI_NOTEXT 1.06, PHOTO_HOOK 1.06 … NAME_TEXT 0.84, HOST_FACE 0.25) all reproduce,
including geo-means and hit/flop counts.

### 1a. "Blue sea" is really "colour vs no colour"
- 22 thumbnails (grey-blue, grey/blue, grey-teal, grey-teal storm, grey + blue text) are counted as **both** blue and grey.
  "Blue-grey" counts only as blue, "grey-blue" counts as both. Two codes for nearly the same picture land on different
  sides of the headline finding.
- Under the study's own rule, **our T2's slate sea would probably be coded "grey-blue", i.e. "blue"**. So the line "their
  sea is charcoal-grey, which is the main thing the data penalises" over-reads the evidence.
- What survives: within a channel, the more saturated, colourful frames tend to be the hits. This could be a topic effect
  (wreck aerials and "found" stories are both the hit topics *and* the blue pictures), not a thumbnail effect.
- Counter-examples on the sheets: FF's three flops are all turquoise/bright blue (PT-305, Thresher, Bikini), and so are
  Hidden History's and Sunken Inside's worst. Valor Vault's best (Yorktown, 49×) is a grey-green sonar image.
  **Blue is not protective; a famous, uncovered topic is.**

### 1b. The "then/now split" is mostly not then/now
The 6 SPLIT-tagged thumbnails:

| Outlier | Channel | Words | Then/now? |
|---|---|---|---|
| 62.21 | Iron & Sea | MORE SHIPS IN A MONTH / THAN THE U.S. IN A YEAR | No: China vs US |
| 5.32 | Sunken Inside | 1912 / 2026 | **Yes**, but the channel median is 569 views on 14.4K subs (inflated) |
| 3.32 | Oceanliner Designs | (none) | No: Titanic vs Icon of the Seas |
| 1.06 | Sea Power Reports | NZ's 40-YEAR CHOICE / VS | No: Mogami vs Type 31 |
| 1.05 | Deep Sea Relics | MIDWAY GRAVEYARD: KAGA FOUND | Yes (archive / wreck) |
| 0.15 | Deep Sea Relics | ONLY ONE? | No: Arizona vs Hood |

True then/now **n = 2 (5.32×, 1.05×)**. The 2.19× median is pulled up by a 62× "vs" comparison. DO #6 ("test one then/now
split") has no support in this data. The 1912/2026 hit also works because "Titanic" needs no label; "1969 | 2006" on a
ship most Browse viewers can't name says nothing on its own.

### 1c. Other confounds the study under-weights
- **Unblinded single coder.** The 12 coding sheets carried views and outlier on each tile. Palette and brightness are
  judgement calls, and the coder knew the outcome. That is the biggest threat to findings 2 and 3. Fix: re-code the
  palette from pixels (mean saturation, hue share of the lower half) or have a second coder work from unlabelled sheets.
- **Stratified pool → medians near 1.0 by construction.** The study says so, but then ranks templates by those medians.
  The 0.94–1.09 spread is an artefact, not "templates don't matter". Single-channel templates (FACE_DIAGRAM, PHOTO_ARROW,
  AI_PAINT_LABEL) come out at exactly 1.00 because 4 + 4 + 4 of one channel always do.
- **Topic, not thumbnail.** Sheet A is Arizona, Yamato, Pearl Harbor, PT-109, Bismarck, the biggest ship ever, Niagara
  Falls. Sheet C is Egyptian barges, NATO, a Coast Guard cutter, instructional films. A/C is mostly a topic comparison.
- **Age within channel.** A/C median age matches, but inside some channels age drives outlier: Spearman ρ(age, outlier)
  = +0.65 for Deep Sea Relics, +0.48 for Valor Vault, +0.31 for Historsea. Deep Sea Relics supplies 3 of the A-set numbers,
  3 of the "wreck" winners and 3 of the "dark" differences. One channel's old videos carry several "findings".
- **Channel size / format mix.** Lost Vessel (sleep videos), Armoured Archivist (full public-domain films) and
  Historsea (host vlogs, NATO) aren't the same product as ours. Their template contrasts tell us little about a
  14–24 min "what happened to it" story.
- **Outcome = views, not CTR.** Views also come from impressions, which depend on topic demand and channel authority.
  A brand-new channel gets few Browse impressions, so for us the thumbnail's first job is **instant legibility next to
  the video it sits beside in Suggested**, not mimicking colour statistics.
- **The "number" finding is mostly years.** Of the 17 top-4 numbers, 7 are "N YEARS LATER / FOUND AFTER N YEARS" (4 from
  Deep Sea Relics) and 2 are film years "(1943)/(1944)". Durations like "37 MINUTES" have no direct evidence either way.
  Money appears twice in top-4s ($23B, $800M) and never in bottom-4s: n = 2, a curiosity, not evidence.

### 1d. Scorecard
- **Solid:** within one channel, the template rarely decides hit or flop (14/20); word count and AI-vs-real show no
  effect; host-face is weak (4/6 flops, though n=6 and two channels); contradicting text = flop (n=2, but our truth rule
  already covers it).
- **Weak but directional:** colourful/saturated beats grey/desaturated within channels (unblinded, overlapping codes).
- **Noise:** number in text, dark overall, wreck as subject, arrows, question, text position.
- **Wrong:** "then/now split = best cross-cutting feature"; "the charcoal sea is the main thing the data penalises"
  (our sea would be coded "grey-blue" = blue by the study's own rule); the §9 rubric giving equal points to "number" and
  "blue" (one is noise, the other is the only directional signal) and none to "readable as a sinking carrier at 168×94",
  which is the criterion that matters most for a new channel.

## 2. The three concepts and the v2 drafts, for CTR in Browse/Suggested

Context: we'll sit next to Dark Seas, FF, Deep Sea Relics and the 4.1M War History Online clip. All of them are bright,
saturated, and show one instantly readable ship. Ours must read as **"an aircraft carrier going under, for real"** at
168×94. Being the only *real* photo of a *real* carrier sinking is our edge; a cyan AI-style grade would throw it away.

| | Photo | Reads as a sinking carrier at 168×94? | Words | Verdict |
|---|---|---|---|---|
| Concept 1 "37 MINUTES" | 6698623 (last of the deck) | **No.** In the mock-up's sidebar tile it's a tan plank in white foam: no island, no bow shape. The brightest thing is the foam. | Good, true (G5, confirmed in FACTCHECK_C) | Right words, wrong photo. Same flaw the critics found in T1/T3. |
| Concept 2 "700 LB INSIDE" | 6698621 (whole carrier, deck nearly awash) | **Yes, as a carrier**; less obviously sinking (could be a hulk at sea) | **Risky.** On a warship "700 LB" reads as a bomb or ordnance. The 700 lb is the PCB chemical itself, spread through cable, gaskets and paint (FACTCHECK_B B18). The implied meaning is false even though the number is true. It also doesn't link to the launch title. | Keep the photo, change the words. |
| Concept 3 "1969 \| 2006" | film frame from 87411 + 6698623 | Left half: a blurry upscaled video frame. Right half: the same plank as Concept 1. | Two dates with no meaning to someone who doesn't know the ship | **Drop.** Rights "Undetermined" too; then/now evidence is n=2. |
| v2 T1 "NAVY DID THIS" | 6698624 (bow vertical) | Only if recropped to include the foam and the boat (the current crop is a rust wall) | Adds "who" to the launch title | Keep as the novelty slot, recut |
| v2 T2 "37 MINUTES" | 6698619 (charges firing) | Carrier yes; small and grey-on-grey; same photo family as the 4.1M clip ("seen it") | Good | Words survive, photo replaced |
| v2 T3 "WHAT'S LEFT INSIDE?" | 6698625 | Weak: plank + foam | Fine with title D only | Drop for the launch test |

**The missing frame: NARA 6698612** ("Starboard bow: steep angle, 17 May 2006", JO1 Jackey Bratt, USN, Unrestricted;
FOOTAGE_LIST b8 #11). The bow points at the sky, the island is going under in smoke, and the flight-deck overhang
makes the outline unmistakably a carrier. In my mock it was the only tile that still read as "carrier sinking" at
168×94. It's the universal "ship going down" shape, and it's true. Caveat: the 0.92M USA Military Channel thumbnail is
a similar tilted-hull angle, so in *Search* for "Oriskany" it may look familiar. Our traffic is Browse/Suggested, where
legibility beats novelty.

## 3. Final set for Test & Compare

**Launch title: "Nobody Wanted This Aircraft Carrier, So They Sank It"** (vidIQ 92). Run a thumbnail-only test under it.
Three different photos, three different promises: speed, cost, agency. Judge on day 7–14 watch-time share, not day 1.

| Slot | Photo | Words | What the words add to the title | True because |
|---|---|---|---|---|
| **A (lead)** | 6698612 | **37 MINUTES** | How fast (spectacle) | G5 HIGH; FACTCHECK_C confirmed (10:25 → 11:02 CT) |
| **B** | 6698621 | **$20 MILLION** | A paradox: they spent $20M on a ship nobody wanted | FACT_SHEET script line HIGH "finished at about $20 million" (USNI06 + AP06 + FLSEN); AP and Florida Legislature figures. **Owner check:** EPA's own total is $15.63M and its line items add to $23.6M. Either keep "$20 MILLION" and say "about $20 million" in the narration, or use the fallback in §4 B |
| **C** | 6698624 recut | **NAVY DID THIS** | Who "they" are | G2 HIGH (Navy EOD set the 22 charges) |

Not in the set: "700 LB INSIDE" (bomb misread). Keep the 6698621 + mystery idea for title D only, worded **"LEFT INSIDE"**
(2 words, no number). "ON PURPOSE" repeats "so they sank it". "1969 | 2006" is dropped.

## 4. Exact specs (output 1280×720, Anton-Regular from `tools/fonts/`, as in `make_thumbs_v2.py`)

Shared rules: real NARA photo only, no repaint, no added smoke/fire, no fake hull number. White = #FFFFFF, red =
#E0352B, black stroke 5 px #0A0E16 at 1280 px, soft drop shadow (offset 5/7, 40 % black). **Nothing in the bottom-right
300×160 px** (sea only). Export JPEG q 95, subsampling 0. Check each at 168×94 next to sheet A before uploading.

**Sea-only grade (all three).** Mask: below the horizon line only, pixels with B ≥ R and saturation < 35 % and luminance
< 80 % (this excludes rust, foam and hull highlights). On the mask, blend 45 % toward a steel-blue tint (R × 0.80,
G × 0.98, B × 1.18), i.e. a hue around 205–210°. **Not cyan/teal 195°**: a cyan sea under a rust hull reads as AI. Then a
whole-frame midtone lift (gamma 0.88 ≈ +0.3 EV), except slot C (see below). Don't touch the sky, the hull or the foam.

### A: "37 MINUTES" on NARA 6698612 (lead)
- **File:** `videos/oriskany/footage/src/photos/nara_6698612.jpg` (3000×1382).
- **Crop:** x 500–2633, y 60–1260 (2133×1200, 16:9) → 1280×720. The island sits at the left edge, the bow tip just
  inside the right edge, horizon at y ≈ 470/720. Sea fills the lower third.
- **Words:** one line, bottom-left over the dark sea: "**37**" red + "**MINUTES**" white. Cap height ≈ 125 px (Anton
  170 pt), baseline y = 680, left x = 40. It ends at about x 600, well clear of the bottom-right box. No gradient is
  needed; the sea is dark enough. Add a 20 % black gradient under the text only if the grade lifts the sea too much.
- **Grade:** sea mask as above (horizon at source y ≈ 770). Raise local contrast +10 % on the hull so the black
  silhouette keeps its edge details. Leave the grey sky as it is: the dark bow against it is the contrast.

### B: "$20 MILLION" on NARA 6698621
- **File:** `nara_6698621.jpg` (3000×1993).
- **Crop:** 2580×1451, centre at x 56 % / y 52 % (x 390–2970, y 311–1762) → 1280×720. This drops the helicopter skid at
  bottom-left. The ship spans the frame, island left, bow right.
- **Words:** one line in the top band over sea/sky: "**$20**" red + "**MILLION**" white, cap height ≈ 120 px (Anton 165 pt),
  baseline y = 175, left x = 40. 25 % black gradient from the top edge down to y 220, left 60 % only.
- **Grade:** sea mask (horizon ≈ y 170 in output); lift the shadow side of the hull +0.4 EV (as the study says) so the
  bottom third isn't a black band; the bottom-right is sea and the bow chain only.
- **Fallback words if the owner rejects the figure:** "**$ MILLIONS**" ("$" red, "MILLIONS" white), same size and
  position. Don't use "NOBODY WANTED": it repeats the title.

### C: "NAVY DID THIS" on NARA 6698624 (novelty slot)
- **File:** `nara_6698624.jpg` (1993×3000, portrait).
- **Crop:** full width 1993×1121, vertical centre at 47 % (y 849–1970) → 1280×720. The slab fills the left-centre, the foam
  ring and the small boat are in frame (the boat is the only scale cue). The bow tip can touch the top edge.
- **Words:** two lines, right-aligned at x = 1240, in the clear sea right of the slab: "**NAVY**" red (baseline y 250),
  "**DID THIS**" white (baseline y 430), cap height ≈ 125 px. Both lines must stay off the rust; the bottom-right
  300×160 stays foam/sea only.
- **Grade:** sea mask only, **no** global midtone lift (the foam clips already; in my mock it blew out). Pull the foam
  highlights −0.2 EV so the turquoise inside the foam shows; that is real colour in this frame.

## 5. Process notes for the next pass
- Before the thumbnail goes up, render the three as a 168×94 strip pasted into sheet A, and ask one person who hasn't
  seen the video "what is this a picture of?". If the answer for any tile isn't "a carrier sinking", swap it.
- If Test & Compare picks A, keep 6698612 out of the video's first 2 minutes. It belongs to the ending; the hook rule
  forbids the answer up front, and using it twice spends the image.
- Fix the study (owner's call, I did not edit it): relabel "split" as "split/comparison" and drop DO #6; mark the blue
  finding "unblinded, overlaps grey"; delete the §9 rubric's equal weights; add 6698612 to §10.
