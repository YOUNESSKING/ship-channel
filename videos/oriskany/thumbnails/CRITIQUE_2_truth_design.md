# Critique 2: truth and design of the Oriskany thumbnails

Reviewer: independent critic (2026-11-06). Inputs: the three 1280×720 JPGs, the 168×94 sidebars, `feed_strip.png`,
`make_thumbs.py`, the three NARA sources, TITLES_THUMBS.md, FACT_SHEET.md, and FOOTAGE_LIST b8 rows 5, 14 and 15.
The launch title is C: "Nobody Wanted This Aircraft Carrier, So They Sank It".

## Summary

| Rank | Thumb | Truth | Craft | One-line verdict |
|---|---|---|---|---|
| 1 | **B: NAVY DID THIS** | PASS | **6/10** | It reads best as an aircraft carrier at feed size, and it is the only text that *adds* to the launch title (who did it). But the text covers about 28 % of the hull and the gold rule touches line 2. |
| 2 | C: WHY SINK HER? | PASS | 5.5/10 | It is honest and clean, and the bottom-right corner is safe. But the ship is small, a stray white boat sits beside the "W", and the words repeat the title. |
| 3 | A: ON PURPOSE | PASS | 5/10 | It is the most dramatic frame, but at 168×94 it reads as "a rusty box in the sea". "PURPOSE" covers the right edge of the silhouette, the crop cuts off the foam ring and the boat that show scale, and the words repeat the title. |

All three pass on truth, and none is clickbait the video fails to pay off. The two biggest craft problems: text sits on
top of the ship in A and B, and A/C say what title C already says.

---

## 1. Truth (all three)

**Pictures.** All three are NARA series 330-CFD-DN-SD-07-08xxx, taken by PH2 Jeffrey P. Kraus, USN, on 17 May 2006,
and their catalogue titles name ex-Oriskany. I checked each thumbnail against its source frame. The crops are
straight crops with no flip, no added smoke or fire, no AI repaint and no fake hull number. The grade is only
Contrast 1.15 and Color 1.05.
- A = 6698624 "bow vertical". She went down stern first, with the bow standing up out of the foam. That is the
  moment shown. ✔
- B = 6698618 "as the charges explode". The white smoke comes from the 22 EOD charges (FACT_SHEET G2). It is not a
  fire or an attack. ✔
- C = 6698625 "final moment", the deck slipping under. ✔

**Words.**
- "ON PURPOSE": true (G1/G2, NAVREL). It is the hook's own line ("The United States Navy did. On purpose.",
  NARRATION_v3 line 3). It is paid off at 0:10.
- "NAVY DID THIS": true. Navy EOD set and fired the charges (G2, NAVREL), and the Navy owned the hull until she
  touched bottom (G12). Two small risks:
  1. "THIS" over white smoke could be read as "the Navy attacked or bombed its own carrier" (a SINKEX). The video
     answers that inside 10 s ("No enemy sank her… On purpose"), so it is paid off quickly. Acceptable.
  2. The faint accusatory tone ("look what they did") is also paid off later by the PCB reversal. Fine.
  Grammar without "THE" is normal thumbnail shorthand.
- "WHY SINK HER?": fair. It is a question and claims nothing, and the video answers it (failed museum and scrap
  sales, reef programme, cost). ✔

**Clickbait check.** Nothing promises an accident, a disaster, a secret or a toxic angle. TITLES_THUMBS banned
"TOXIC" and "LARGEST REEF", and they are not used. ✔

**Rights.** All three are NARA `useRestriction: "Unrestricted"` and the work of a US Navy photographer, so they are
public domain under 17 USC 105. That is fine for a thumbnail. ✔
Housekeeping: `full/CREDITS.md` already logs the three items. Add one line saying they are also used as the
thumbnail, with the NARA IDs.

**Packaging honesty note (not a fail).** With launch title C ("…So They Sank It"), A's "ON PURPOSE" and C's "WHY
SINK HER?" mostly repeat the title. Only B adds new information ("the Navy"). For the Test & Compare run with titles
A or D, A's and C's words carry more weight.

---

## 2. Thumbnail A: ON PURPOSE (NARA 6698624)

**Truth: PASS. Craft: 5/10.**

Problems:
1. **Text covers the subject.** "PURPOSE" (bbox x 602–1220, y 399–565) lies over the right 284 px of the ship
   (ship x ≈ 376–886). It cuts off the right edge of the silhouette, which is the shape that says "a ship standing
   on end".
2. **The ship is not recognisable at feed size.** In the sidebar it is a brown rectangle. The cues that would say
   "huge ship going down" are the foam ring and the small support boat (scale). The crop (`cy=0.33`) cuts both off
   at the bottom edge: the boat is sliced at y≈690–720 and is now just clutter.
3. **`cx=0.42` does nothing.** With `frac_w=1.0` the crop is already the full source width, so you cannot move the
   ship sideways. That is why the text has nowhere clean to go.
4. **Size hierarchy.** "ON" and "PURPOSE" are both 190 px, so a 187 px wide "ON" hangs over a large empty patch of
   water. The function word is as loud as the payload word.
5. **Softness.** The source is hazy. Downscaling 1993→1280 with Lanczos and no sharpening leaves it mushy next to B.

Fixes (in `make_thumbs.py`):
- Crop: `crop(a, 0.42, 0.33, 1.0)` → `crop(a, 0.5, 0.40, 1.0)`. The crop now spans source y ≈ 640–1761, so the ship
  top keeps a ~20 px margin and the foam ring and boat come into frame.
- Text: size 190 → **140**, right edge x 1220 → **1255**, y 150 → **110**, `gap=1.0` → **0.95**. "PURPOSE" is then
  ~455 px wide, starting at x≈800, and overlaps only the outer ~85 px of the deck edge instead of 284 px.
- Optional hierarchy: "ON" at 110 and "PURPOSE" at 140, both right-aligned.
- Shade: start the right gradient later and make it stronger: `(t-0.35)/0.65` → `(t-0.50)/0.50`, and peak alpha
  200 → 220. The text column stays dark and the ship stays ungraded.
- Sharpen after `crop`: `img.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=3))`.
- Check again at 168×94. If it still reads as a "box", A is the thumbnail to drop from the Test & Compare set.

---

## 3. Thumbnail B: NAVY DID THIS (NARA 6698618)

**Truth: PASS. Craft: 6/10.**

Problems:
1. **The gold underline collides with line 2.** Measured: "NAVY" glyph bottom y=265, rule y=277–285, "DID THIS"
   glyph top y=287. That leaves a **2 px** gap, so the rule looks glued to "DID THIS" (see zoom) and reads as a
   strike-through or box line. The line pitch (165) is only 23 px larger than the glyph height (142), and the rule
   fills almost all of that space.
2. **Text covers the ship.** The hull and deck run from x≈136 to x≈989, y≈301–557. "DID THIS" (x 730–1230,
   y 287–431) covers the island's aft edge and the whole forward ~240 px of the flight deck, which is about 28 % of the
   hull. The deck tip pokes out between "DID" and "THIS" as an odd sliver.
3. **The crop wastes the top.** `cy=0.42` puts ~300 px of plain water above the ship and pushes the ship up into
   the text band.
4. **Code smell.** `text()` has an `underline_first` option, but B ignores it and redraws the rule by hand with
   duplicated numbers. That is how the collision got past review.

Fixes:
- Crop: `crop(b, 0.48, 0.42, 0.85)` → `crop(b, 0.48, 0.30, 0.85)`. It clamps to y0=0, so the ship drops to
  y≈361–618 and the horizon line of spectator boats sits under the text, which is a nice "public event" cue.
- Text: size 165 → **140**, anchor top y 70 → **15** (Anton has ~55 px internal top space at 140), `gap=1.0` →
  **1.12**. Glyphs then sit at about y 70–191 and 227–348, which is clear of the island top at y≈361.
- Underline: use `text(..., underline_first=True)` and set the rule at `bb[3]+12 … bb[3]+19` (7 px). At gap 1.12
  that leaves about 17 px between the rule and "DID THIS". Or drop the rule completely: the words already work.
- Keep the right edge at x=1230–1240. The bottom-right corner is open water, so the timestamp is safe.

---

## 4. Thumbnail C: WHY SINK HER? (NARA 6698625)

**Truth: PASS. Craft: 5.5/10.**

Problems:
1. **Stray object.** The white support ship (source x≈548–818, y≈450–563) lands at output x≈37–181, y≈100–158,
   directly behind and to the left of the "W". At sidebar size it is a white dash in front of "WHY" (see feed strip).
2. **The ship is too small.** It is about 480 px wide (37 % of the frame), and the foam disc takes more room than the
   ship. At 168×94 the text dominates and the ship is a thin wedge.
3. **The top shade crushes the sea** to near-black under the text. That is fine for legibility, but together with
   the brown dust plume (lower-left) the frame looks muddy, not "blue Gulf".
4. **The build differs from the brief.** TITLES_THUMBS concept 3 was a then/now split (1969 colour aerial plus the
   2006 sinking) with the text at the bottom. The built version is single-frame with the text at the top. Text at
   the top is the *right* call, because the bottom-right is the timestamp zone. Dropping the 1969 half, though,
   makes A and C the same idea (bow up in foam), which wastes a Test & Compare slot.

Fixes:
- Crop: `crop(c, 0.56, 0.47, 0.80)` → `crop(c, 0.64, 0.45, 0.70)`. The source window becomes x≈860–2960,
  y≈307–1488. The support ship drops out of frame, the hull grows to ~550 px, and the ship top lands at y≈270, 44 px
  below the text glyphs (y 82–226).
- Text: keep 165 and x=60. Optionally set y 30 → **10** for a bit more air above the ship.
- Shade: peak 190 → **160**, so the water keeps some blue.
- Better: build the then/now split as briefed (left: 428-NPC-43159 1969 colour still, right: this frame), so C tests
  a really different promise from A.
- Bottom-right: the foam sits under the timestamp. Nothing important is lost. OK.

---

## 5. Cross-cutting craft notes

- **Font and colour.** Anton warm white (246,241,230) works well on dark sea and is clearly not the Forgotten Fleet
  yellow look. Kerning is Anton's default and fine at these sizes. Line breaks are fine ("ON / PURPOSE",
  "NAVY / DID THIS", single-line question).
- **Shadow.** The shadow layer is pasted with its own blurred alpha used as the mask, so it is attenuated twice and
  almost invisible. That is OK on dark water, but it gives no help where B's text meets smoke. Use the blurred alpha
  only once: `sh_b = sh.filter(GaussianBlur(6)); img.paste(sh_b, (0,0), sh_b.split()[3])`, and raise the offset to
  (5,6).
- **Gradient banding.** The 8-bit "L" mask ramps over about 800 px into near-black. Banding is faint but can show
  after YouTube re-encodes. Add ±2 noise to the mask, or save the final JPEG at `quality=95, subsampling=0` (files
  stay under 400 KB).
- **Timestamp safe zone** (about x 1150–1270, y 670–712): clear on all three. ✔
- **Brand consistency.** Same font, colour, shade style and source shoot, so the three feel like one channel. ✔ But
  A and C are nearly the same image idea. To vary templates (FF study DO 10), make one of them the then/now split or
  the 1969 colour aerial.
- **Compression.** JPEG q92, 157–254 KB. No visible blocking at 100 %. Grain in A comes from the source.

## 6. Ranking and recommended Test & Compare set

1. **B**, after the fixes (crop cy 0.30, text 140/gap 1.12, rule moved). Best carrier read, and its words add to the
   title.
2. **C**, recropped (0.64/0.45/0.70), or better the then/now split.
3. **A**, recropped (cy 0.40) with text 140 at x=1255. Keep it only if the sidebar now reads as a ship. Otherwise
   swap it for the 1969 colour aerial plus "ON PURPOSE".

After the fixes, re-run `make_thumbs.py`, regenerate the sidebars and the feed strip, and view them next to two or
three top Essex-class or carrier videos before uploading.
