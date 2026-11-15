# Critique 2: truth, rights, design. Mallows Bay thumbnails v2

Drafts: `V1_ghost_fleet.jpg`, `V2_1936_today.jpg`, `V3_3200_a_ship.jpg`, `sidebar_strip_v2.png` (builder `make_thumbs_v2.py`).
Checked against: THUMBNAIL_STUDY s10, research/thumbnails/CRITIQUE_2, CLAUDE.md, FACT_SHEET, FACTCHECK_A/C, FOOTAGE_LIST,
HQ_FOOTAGE, full/CREDITS.md, NARRATION_v2.txt, the source frames, and the NOAA wk309 page (fetched 2026-11-15).
Test renders (not in the repo): `/tmp/claude-0/-home-user-ship-channel/80a206ad-823b-5d4d-a2c7-aa717ce129a3/scratchpad/critic2/`
(`V1_test.jpg`, `V2_test.jpg`, `strip_test3x.png`, `test.py`).

## Verdict

| Draft | Truth | Rights | Design /10 | One line |
|---|---|---|---|---|
| V1 "GHOST FLEET" | PASS (fix the narration) | PASS | 6 | True name, clean PD frame, but the hero is a dark brown tangle and the words add nothing to the title |
| V2 "1936 \| TODAY" | **FAIL** as written ("TODAY" is ~6-year-old footage; the 1936 half proves no place) | PASS | 4 | Best idea, weakest build: the 1936 half looks like an ink drawing or an AI pattern |
| V3 "$3,200 A SHIP" | PASS | PASS | 6.5 | Best picture (colour, kayaker for scale) and a true number; red sits on orange trees; upscale halos |

Ranking after the fixes below: V3 > V2 (fixed) > V1. Test V3 against the fixed V2 in Test & Compare. Keep V1 as the reserve.

## 1. Truth

**Not the Accomac. HQ_FOOTAGE needs a correction.** HQ_FOOTAGE (wk309 row, and pick 3) calls the big foreground wreck at 0.5–3.5 s
"the burned-out rusty hull (Accomac)". It is not the Accomac. The Accomac (`noaa_accomac_sassorossi.jpg`,
`noaa_osprey_nest_ship_mcintosh.jpg`) is an intact steel hull that rides high: continuous plating, peeling white paint and a
flat deck edge. The wk309 wreck sits at the waterline. It is a broken-open hull with charred timber and rows of rusted iron
drift bolts standing up. That is a burned wooden hull, the same kind as the fleet. The kayaker photo (V3, bottom right) seems
to show the same hull, with its nest. So no draft shows the Accomac. That is good for truth. Which ship this is remains
unknown (Mallows Bay also has barges and schooners), so never caption the foreground hull as a named WWI steamer. Owner:
please confirm with one look, then fix the label in HQ_FOOTAGE.md (the label only; this critic did not edit it).

**V1 "GHOST FLEET": PASS.** It is the site's common name (NOAA, MD DNR, Shomette's title "The Ghost Fleet of Mallows Bay"). The
rows behind the wreck are the WWI hulls. Problem: `NARRATION_v2.txt` never says "ghost fleet" (grep: 0 hits), so the
thumbnail promises a phrase the video never pays off. Fix: add one line near the reveal, e.g. "Locals call it the Ghost
Fleet." The words also repeat the obvious and add no new information to the title (study s7: words should add to the title).

**V2 "1936 | TODAY": FAIL as written.**
- *1936 is true, and so is the place.* `aerial_1936_fleet.jpg` is a crop of `aerial_mallows_1936_b.jpg` = NARA 18-AA-70-44,
  whose file card reads "Mallows Bay, Md. - on Potomac River below Quantico and between Sandy Point and Liverpool Point". It
  is not the Little Falls frame (that one is `aerial_mallows_1936_a`, E1). Detail the docs miss: the card's "4/8/36" is the
  date the print was *received* from Bolling Field. The film-edge code "...BFX 3-6-36..." gives the flight date as
  **6 March 1936**. The year is right either way. Fix the date in FOOTAGE_LIST A14 and CREDITS.md (date column empty; title still
  "Little Falls"; use the card caption).
- *But the draft's crop proves no place.* `old.crop((560,230,1180,816))` keeps only hull outlines: no shore, no water edge.
  `**1.9` gamma then turns them into a black-on-white leaf pattern. To a viewer it reads as a drawing or texture, not as an
  aerial photo of the same bay. That is the kind of "fake-looking" image the brand rule (real photos only) is meant to prevent.
- *"TODAY" is not literally true.* wk309 "Birds of Mallows Bay" was published **November 2020** (NOAA page). The drone shot
  is from autumn 2020 or earlier, about 6 years old at upload. The bay looks much the same, but the hulls keep eroding and
  the study's own precedent is that "both dates are the frames' own dates" (s10 concept 3). "NOW" has the same problem.
- **Fix:** "**1936 | 2020**" (both are the frames' own dates). If the owner wants the present tense, use current footage: no
  PD frame newer than 2022 is in `src/`. The Sassorossi Accomac photo (2022) is the wrong subject.

**V3 "$3,200 A SHIP": PASS.** FACTCHECK_A D5 corrected the price to $750,000 for 233 ships, 12 Sept 1922 (USSB 1923, Oregonian
1922). $750,000 / 233 = $3,219, so "$3,200" is an honest round-down, and narration line 77 says "about three thousand
two hundred dollars a ship". Three loose ends:
1. Narration **line 7 (hook)** says "for about three thousand dollars each". Change it to "about thirty-two hundred dollars
   each" so the number on the thumbnail is spoken in the first minute, not at line 77.
2. FACT_SHEET D5 still shows the $750k/$862k conflict and NRHP's "$3,300". Update it to the FACTCHECK_A result ($750,000,
   HIGH; $3,200 each), or the next checker will flag the thumbnail.
3. Without a verb, "$3,200 A SHIP" could be read as the *building* cost. The video answers it at once (they cost
   ~$750k to build), which makes it a fair curiosity gap, not a lie. If the owner wants it airtight: "**SOLD: $3,200**"
   (2 tokens) or "**$3,200 EACH**".

## 2. Rights: all PASS

| Source | Used in | Basis | Check |
|---|---|---|---|
| `hq_noaa_wk309_birds.mp4` @1.6 s, 2.2 s | V1, V2 right | NOAA Earth Is Blue wk309. Page credits: "Footage: Paul Chetirkin/NOAA, Matt McIntosh/NOAA, Shannon Shikles/NOAA, Nick Zachar/NOAA". **No Duke or partner credit** (the Duke credit is only on wk240). US Gov work = PD | Frames clean: no caption box, no "earth is blue" bug (enters ~3 s, bottom-right of the frame; also outside both crops: V1 keeps source x 48–1136, V2 keeps x 258–802). Letterbox removed correctly (crop 1280x612+0+32). Music is irrelevant to a still. In CREDITS.md line 92 |
| `aerial_1936_fleet.jpg` (= `aerial_mallows_1936_b`) | V2 left | NARA 18-AA-70-44, `useRestriction: Unrestricted`, Army Air Corps = federal | It is Mallows Bay (card caption). Not the Little Falls frame `_a`. In CREDITS.md line 80 (fix the date and title as above) |
| `noaa_kayaker_wrecks_mcintosh.jpg` | V3 | NOAA ONMS web image 20211025, "Photo: Matt McIntosh/NOAA" | In CREDITS.md line 7. No watermark. The kayaker is not identifiable from above (no face), so model-release risk is low |

Residual risk (same as the earlier critique): "/NOAA" in a credit is taken to mean federal staff. McIntosh appears as NOAA
staff on every ONMS page, so the risk is acceptable. If the owner wants certainty, one email to ONMS settles it for every
McIntosh source.

## 3. Design

Common to all three:
- **Stroke too thin.** 4 px on 170 px Anton is ~0.5 px at 168x94, so the outline vanishes in the sidebar and the white words
  merge into bright water/sky (see V2 "1936" in the strip). Fix: `stroke_width=9`, plus a soft drop shadow (offset +6,+8,
  black alpha 170, GaussianBlur 6) under the stroke. Tested: `strip_test3x.png` reads clearly better.
- **Oversharpening of upscaled sources.** Drone frames are 1280x612 upscaled x1.18; the kayaker photo is 1000x563 upscaled
  x1.28. `Sharpness 1.3/1.4` puts visible halos on the stakes and the kayak edge (at 2x zoom: ringing and JPEG blocks).
  Use `enhance(1.1)` at most, applied *after* the resize, not before.
- **Grade: natural, not fake.** Measured on the sea: V1 S 29–31 % → 36–39 %, hue shifted ≤ 3°; V3 S 33 → 40 %. Brown-green
  shallows (hue 103–131) are correctly left out of the mask. Keep it.
- **Zones are fine.** Bottom-right 300x160 holds only texture (no words, no key subject) in all three. The top-right hover
  zone (right ~120 px of the top 110 px) is clear: text ends at x ≈ 820 (V1), 1015 (V2), 930 (V3).
- Cap height 146 px at size 170 (Anton "H" bbox), in line with the study's ~150 px.

**V1 (6/10).** The bottom 45 % is a dark brown-black tangle of charred timber. It is the brightest-contrast subject, so the eye
lands on it first, yet it reads as "junk" at sidebar size. The hull rows (the actual story) are a thin band. There is
also a white block at bottom-left (x 0–110, y 600–720), a bright distraction near the progress-bar corner. Fixes: `cover(drone,
cx=0.25, cy=0.6, zoom=1.12)` with `cx=0.35` pushes the block out of frame (or patch it darker: multiply that box by 0.6 with a
40 px feather). Keep `word_shade` at 0.55. Better words (if the narration line is added): "**GHOST FLEET**" stays. A
stronger alternative that adds to the title: "**100+ SHIPS**" (FACTCHECK_C: 100+ is the title claim, already checked).

**V2 (4/10 now; ~7/10 after the fixes).**
- Left half: use the full scan `aerial_mallows_1936_b.jpg`, `crop((1560, 640, 2840, 2080))` (1280x1440 = 8:9), which keeps
  the hull raft *and* the curved Maryland shore. Gamma `**1.35` (not 1.9), tint ×(0.95, 0.98, 1.03), Contrast 1.15. Tested in
  `V2_test.jpg`: it now reads as an aerial photo of a bay full of ships, and the shore curve answers the drone's treeline.
- Words: "**1936**" white / "**2020**" red, size 150, stroke 9, `word_shade` 0.5 boxes (0,0,470,190) and (640,0,1080,190).
- Right half: unchanged crop (`cx=0.35`, t=2.2 s); sharpen 1.1.
- Divider: the 8 px white bar at x 636–643 is good.

**V3 (6.5/10).** Best frame of the set: blue water, a bright blue kayak as a human scale cue, hull lines leading the eye.
Problems: (a) the red "$3,200" sits over the orange-brown autumn tree line (y 0–110), red on rust with poor hue contrast,
and only the 0.55 shade saves it; (b) the kayaker sits at x 320–570, y 560–650, low and small (≈ 250 px wide = 33 px at
sidebar), so it is the best detail but barely survives; (c) halos (see above). Fixes: raise `word_shade` strength to 0.7
over (10, 10, 980, 240); move the words down to y = 40 so most of the cap height sits on blue water; `cover(k, cx=0.45,
cy=0.75, zoom=1.12)` brings the kayak up and larger (≈ 280 px), still leaving the bottom-right 300x160 to wreck texture.
Sharpness ≤ 1.1.

## 4. Summary of builder changes (`make_thumbs_v2.py`)

1. `words()`: `stroke_width=9` + drop shadow (offset 6/8, alpha 170, blur 6). All drafts.
2. Sharpness 1.3/1.4 → 1.1, after resizing. All drafts.
3. V1: `cover(..., cx=0.35, cy=0.6, zoom=1.12)` or darken the white block at (0–110, 600–720).
4. V2: left from `aerial_mallows_1936_b.jpg` crop (1560,640,2840,2080), gamma 1.35, contrast 1.15; text "1936" | "2020".
5. V3: `word_shade` 0.7, words at y 40, `cover(k, cx=0.45, cy=0.75, zoom=1.12)`.
6. Docs (owner or the builder, not this critic): HQ_FOOTAGE wk309 "Accomac" label → "burned wooden hull (not the Accomac)";
   FOOTAGE_LIST A14 / CREDITS line 80: flown 6 Mar 1936, received 8 Apr 1936, card title "Mallows Bay, Md."; FACT_SHEET D5 →
   $750,000 / $3,200 each; narration line 7 → "about thirty-two hundred dollars"; add "Locals call it the Ghost Fleet."
