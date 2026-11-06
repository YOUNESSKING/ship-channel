# Critique 1: Oriskany thumbnails, judged for click-through

Critic: independent CTR review, 2026-11-06. I looked at all three 1280×720 files, all three 168×94 sidebar files,
`feed_strip.png`, and the full source frames NARA 6698617–6698628. I read `TITLES_THUMBS.md`, `make_thumbs.py` and
FORGOTTEN_FLEET_STUDY §3b, §6 row 11 and the final DO/DON'T lists. **Revised after the coordinator added
`competitor_compare.jpg` + `COMPETITORS.md`** (the top Oriskany videos on YouTube). The competitor section below changes
the ranking.

## Verdict in one paragraph

These three are honest, clean and competent, but too safe. They share one font, one cream colour, one blue-grey sea
and one dark gradient, so in the feed they look like one thumbnail shown three times (see `feed_strip.png`). That
means Test & Compare would mostly test the crops. None has a colour accent, so none jumps out of a dark-mode feed.
Each one also has a fixable focus problem: in A the text covers the hull, in B the ship is too small, and in C the
foam pulls the eye away from the ship. The photos are the real asset, since nobody else in the niche has *real* frames
of a carrier standing on end. Right now the crops hide that asset.

## Competitor context (changes the ranking)

From `competitor_compare.jpg` and `COMPETITORS.md`:
- **B is the image people have already seen.** The 4.1M-view War History Online clip uses an aerial from the same
  2006 scuttling series (charges firing, smoke puffs, a blue sea) with no text. The USA Military Channel one (0.92M) uses
  a tilted, sinking hull, which is close to C. So B, and to a lesser degree C, look like "the clip I already watched"
  next to those results in Search and Suggested for this topic. Familiarity can help recognition, but for a new
  channel's CTR, novelty wins. **B drops from my top pick to third.**
- **A is the only image no competitor uses.** The carrier standing on end is our one visual nobody else has. **A moves
  to first**, provided it gets the recrop below. Without the foam it reads as a rusty wall and wastes that advantage.
- **Brightness:** every competitor tile is bright, saturated blue water and/or sky, and ours are the three darkest tiles
  on the grid. That weighs against my earlier "go darker/deeper blacks" advice for B. **Revised grade for all three:**
  lift the sea's exposure (+0.3–0.5 EV in the midtones) and push its blue/teal saturation moderately. Keep the dark
  gradient only in the text zone, so the text keeps its contrast. This is a global grade on a real photo, so it's
  allowed. Stop short of the competitors' cyan-poster look, because over-saturated rust turns orange and starts to read
  as fire, which is a misleading "added flames" effect by grade.
- **No competitor is a long-form "why" story with a text promise.** The top results are a clip, a 2006 TV documentary
  and a vlog. Our text is a real differentiator in this specific search result, so keep words on the thumbnails.
  Don't copy the 4.1M clip's no-text style.
- Dark Seas uses a **red circle** as its accent. A red word on ours would echo that convention without copying a
  layout, which is fine. Don't add a red circle as well.

## Scores

| Thumb | Score /10 | One-line reason |
|---|---|---|
| A, ON PURPOSE (NARA 6698624) | **7** (6.5 before the competitor grid) | The only image no Oriskany competitor uses, and the strangest real frame of the three, but the crop cuts off the white water, so at sidebar size it reads as "rusty brown slab", not "carrier going under". "PURPOSE" sits on top of the hull. |
| B, NAVY DID THIS (NARA 6698618) | **5** (5.5 before) | It shares a photo family with the 4.1M-view competitor thumbnail, so it reads as "seen it". The smoke is dramatic, but the ship fills only ~15 % of the frame and is grey on grey. At sidebar size it's a sliver. "DID THIS" covers the bow. The gold rule is invisible small. |
| C, WHY SINK HER? (NARA 6698625) | **6** (6.5 before) | Close to the 0.92M competitor's tilted-hull frame. The most readable text at sidebar size (one big line, top band, dark sea behind it). But the brightest thing in the frame is the foam, not the ship. The bottom-left is muddy brown dust. The text repeats title A almost word for word. |

### Fit with each title (curiosity gap, with no repetition), /10

| | A: ON PURPOSE | B: NAVY DID THIS | C: WHY SINK HER? |
|---|---|---|---|
| **"Nobody Wanted This Aircraft Carrier, So They Sank It"** (launch, vidIQ 92) | 4: "so they sank it" already says on purpose | **7**: the title says *they*, the thumb names who and shows the violent act the title doesn't mention | 4: the title already answers "why" (nobody wanted it) |
| **"Why the Navy Sank Its Own Aircraft Carrier"** (88) | 5: "its own" already implies on purpose, so the words only reinforce | 4: "Navy" is repeated, so no gap | **2**: the same question twice |
| **"What the Navy Left Inside the Carrier It Sank"** (88) | **7**: deliberate act + a hidden cargo is a two-part mystery | 5: "Navy" is repeated; the smoke hints at the contents, which is good, but the words add nothing | **7**: two different open questions (why + what) |

## Best pairings

If Test & Compare runs title–thumbnail pairs, pick each pairing on its own merit and don't pair them by letter:

Revised after the competitor grid:

1. **"Nobody Wanted This Aircraft Carrier, So They Sank It" + A's image, recut, with B's words "NAVY DID THIS".**
   This puts our one unique image with the only words that open a gap under the launch title: the title says *they*,
   and the thumbnail names who. "ON PURPOSE" would repeat "so they sank it". The words are true (FC-C A2/A3).
2. **"What the Navy Left Inside the Carrier It Sank" + A, recut, with "ON PURPOSE".** "Deliberately sunk" + "something
   left inside" is the strongest two-part gap. It reads as a cover-up story without saying "toxic". (In a
   thumbnail-only test under one title, use only one of these two A variants.)
3. **"Why the Navy Sank Its Own Aircraft Carrier" + B on 6698619 or C with *new words*** (see C fix 1). Treat this
   as the "familiar image" control against A. Never run title A with "WHY SINK HER?".

If Test & Compare runs only thumbnails under the launch title (C), the order is now **A-recut ("NAVY DID THIS") >
B-recut > C**: A wins on novelty, and C's question is already answered by that title.

## Ranked changes

### A: ON PURPOSE (NARA 6698624)
1. **Recrop lower and wider, so the sinking shows.** The current crop (`cy=0.33`, full width) cuts off the foam ring
   and the small boat beside the hull. That boat is the only scale cue in the frame: next to it, the slab becomes a
   ship. Centre at about `cy=0.45` so the frame runs from the top of the deck to the turquoise swirl. The portrait
   source only allows a 1993-px-wide 16:9 crop, so moving the crop changes what's in it vertically, not how wide
   it is. Resolution is fine, because 1993 → 1280 is a downscale.
2. **Get the text off the hull.** Put the slab in the left 45 % (`cx≈0.55` in the source) and the words in clear sea on
   the right. Nothing should touch the rust. Right now the P-U-R of "PURPOSE" sits on the deck, which flattens both.
3. **One accent colour.** Make "PURPOSE" red (≈ #E0352B) or pure white with a red underline block. Cream on grey-blue
   loses in a dark feed, and the study's own spec (§6 row 11) says white + one red word. This also separates us from
   FF's yellow.
4. **Grade:** lift the sea's exposure and blue saturation (it's the darkest tile on the competitor grid), add
   +10–15 % local contrast/clarity on the slab only (it's hazy), and keep the turquoise of the foam. That
   teal against the rust is the complementary pop this image has and the others don't. Lift the foam whites a little
   and don't clip them.
5. **Text size:** keep it about the same (190 px). Two lines is right. Keep it out of the bottom-right 200×80 (the
   timestamp).
6. Optional alternative frame: **NARA 6698623** (landscape, the flight deck tilting into the white water, two small
   boats for scale, a support ship on the horizon). At sidebar size it's the most obviously an *aircraft carrier
   sinking* of all 15 frames. It's a better base than 6698624 if A's slab still reads as "wall" after the recrop.

### B: NAVY DID THIS (NARA 6698618)
1. **Swap to NARA 6698619**, the same moment shot closer from the same angle. The ship is about 2× larger, the island
   and the deck markings read clearly, the smoke fills the upper left, and the right third is empty dark sea for text.
   That's the biggest *fix* for B. It is still from the same scuttling series as the 4.1M competitor thumbnail, though,
   so B stays the "familiar image" variant. Run it as the control against A, not as the lead.
2. **Text in the empty top-right sea** of 6698619, not over the deck. Currently "DID THIS" covers the bow and the
   island. Stack it as NAVY / DID THIS, right-aligned, at about the same size.
3. **Drop the thin gold underline.** At 168 px it's a 1-px line that does nothing, and at full size it reads like a
   divider. If you want an accent, set "NAVY" in the red from A-3. Use the same red across the set so the channel
   gets a look.
4. **Grade:** the photo is flat and grey. Brighten and add blue to the sea (see the competitor section), not darken
   it: the competitor tiles are all bright. Add local contrast between the white smoke and the rust deck. Use the
   dark gradient only behind the text. Don't push saturation into a fake "fire" orange (no added flames, and no
   colouring smoke to look like fire).
5. Wording check: "NAVY DID THIS" is true (US Navy scuttling charges, FC-C A2/A3). Keep it. It's the only text in
   the set that creates a *who* gap and not a *why* gap, which is why it pairs best with the launch title.
6. **Don't** switch to NARA 6698617 (the charges firing). It's the closest match to the 4.1M competitor's image, so
   it's the least distinct frame we have.

### C: WHY SINK HER? (NARA 6698625)
1. **Change the words or the pairing.** "WHY SINK HER?" duplicates title A and is answered by title C. True 1–3-word
   options that open a *different* gap:
   - **"ON PURPOSE"** (if A is retired or reworked to the 6698623 frame);
   - **"STILL IN THERE"**, for title D only, and only if the fact sheet confirms material remains aboard (FC-B B18:
     PCBs left in place). Never "TOXIC";
   - **"37 MINUTES"** (the commonly reported time to sink). **Verify against the fact sheet before use.** If it isn't
     in the fact-checks, don't use it.

   If you keep "WHY SINK HER?", run it only with title D.
2. **Recrop tighter on the ship** (`frac_w≈0.62`, centre on the deck edge where it meets the water). The foam disk is
   currently the brightest and largest shape, so the eye lands on white water. Keep about a third of the foam for
   context and cut the rest.
3. **Burn the bottom-left.** The brown dust plume reads as mud at small size. Add a bottom-left vignette (−25 %) and a
   slight desaturation in that corner only. That's a grade, not a repaint.
4. **Accent:** the same red-word rule. For a question, put the red on the last word ("HER?") or on the key new word
   if the words change.
5. **Size/position:** good as is: one line, 165 px, top band, left-aligned. Keep the text clear of the ship's deck
   edge by at least 40 px; right now the "?" nearly touches the open sea, which is fine.
6. Note: the plan (TITLES_THUMBS concept 3) called for a 1969/2006 split frame. What was built is a single frame.
   A then/now split would be the one *structurally different* thumbnail in the set, but at 168 px a split halves the
   ship's size. Test it only as a later fourth variant, not in this first round.

## Set-level changes (apply to all)
0. **Brighten the whole set.** Lift the sea's exposure and blue saturation on all three; ours are the darkest
   tiles on the competitor grid. Keep the dark gradient only behind the text.
1. **Make the three visibly different from each other.** Different text positions are not enough. Use one red-accent
   variant, one with white text only, and one dominated by the teal foam (A). Then Test & Compare learns something.
2. **Pure white (#FFFFFF) over cream for the main words.** Cream reads greyish at sidebar size on blue-grey sea.
3. **Keep the shadow and add a 3–4 px dark stroke** at 1280 px (≈0.5 px at sidebar). This adds crispness, not
   the FF-style thick outline.
4. **Re-check the recuts on `competitor_compare.jpg`**, and add 2–3 FF carrier/Essex thumbnails (yellow text, AI
   art) so we can also see how we sit next to the niche's house style. The competitor grid shows the stopping-power
   problem; `feed_strip.png` alone couldn't.
5. Keep what's right: real NARA photos, no AI, no added flames, no hull number painted in, 2–3 words, condensed heavy
   type, and text away from the timestamp corner. Nothing here breaks the honesty rules. The fixes are about crop,
   colour and which words go with which title.

## Scores after the fixes (estimate)
A-recut, brightened ≈ 8 · B on 6698619 ≈ 6.5 (capped by the familiar image) · C with new words + tighter crop ≈ 6.5. The floor stays: vidIQ scores and these
numbers are not sufficient. Judge on day 7–14 Test & Compare data (study DO 11 / DON'T 9).
