# Fleet's End vector logo: independent critique (2026-11-10)

Reviewed: `icon_A/B.svg|png`, `icon_*_176/98/48/24.png`, `lockup_*.png`, `banner_*.png`, `make_vector_logo.py`,
the rejected `../logo_avatar_800.png`, the v3 thumbnails, `research/FORGOTTEN_FLEET_STUDY.md` and
`research/thumbnails/THUMBNAIL_STUDY.md`. I measured the banner with numpy and rendered test mock-ups of the fixes. The mock-ups are in
the scratchpad only and not in the repo.

## Scores

| Concept | Score | One-line verdict |
|---|---|---|
| A "Last light" (carrier stern-first in front of the sun) | **5.5 / 10** | It reads as a carrier at 98 px and up. It does not read as *sinking*: the ship looks like a ramp or a launch. The sun is generic and brings back the yellow we said we would avoid. |
| B "Last stand" (bow vertical against the sun) | **3 / 10** | It fails the core test. At every size it reads as a **sailboat** (a black sail, with the gold deck-edge stroke as the luff) or a **shark fin**. The white foam ellipse reads as a surfboard or a UFO. Drop it. |

## What works (keep)
- The palette idea: navy sky, steel-blue sea, red waterline and white Anton type. It matches the v3 thumbnails.
- Text outlined to paths: no font dependency. A clean, reproducible builder.
- The wordmark: Anton, "FLEET'S" in white and "END" in red. This is the strongest asset in the set. Red on "END" also separates us from
  *Forgotten Fleet* (both names start with "F…Fleet", so the stress must fall on **END**, and it does).
- The circle split by a horizon is a good structure for a "what happened to it" channel: above the line is the ship, below it is the answer.

## Problems found

### 1. Readability at YouTube sizes
- **A at 24 px:** a gold blob with a dark diagonal smear. The ring (8 units → 0.375 px), the red waterline (5 units → 0.23 px) and the
  reflections (7 units → 0.33 px) all vanish or turn to mud. The brand signature (the red waterline) is **invisible** at 24 and 48 px.
- **A, ship contrast:** the black ship (#06101A) only shows where it crosses the sun. The forward ~30 % of the hull and the bow overhang
  sit on the navy sky (#0A1622), at a contrast of about 1.05 : 1. At 48 px the carrier shrinks to a short wedge on a disc, which can read as a
  submarine (the narrow, tall island reads as a sub's sail).
- **A, a cross on a sinking ship:** the mast plus its yard (`M134.5,6…` and `M129,-2 L142,-2…`) render as a "+" above a sinking hull. At 98 px and up
  it reads as a grave cross or a memorial. Drop the yard.
- **B:** a sailboat at every size. A bow on end has no carrier cues: no island, no flight-deck overhang, no hull flare.

### 2. Concept strength
- **A is not sinking.** I measured it: only the stern keel corner is under water (keel at y 316 against horizon 307, a 9 px wedge). The stern
  end of the flight deck is **25 px above** the waterline (x 64, y 283). A ship tilted 17° and almost fully above water reads as
  "taking off", "launching" or "riding a wave". The idea needs at least a third of the hull under the line.
- **The sunset is a cliché.** It is the stock "silhouette + setting sun + reflections" of travel, cruise and tropical logos. It says "nostalgia
  and sailing into the sunset", not "what happened to it". It also makes the avatar mostly **gold/yellow**, the colour that
  FORGOTTEN_FLEET_STUDY row 11 tells us to avoid ("one distinct accent colour (not yellow)"). Add the gold ring and the gold tagline, and
  the yellow family takes over the brand.
- The strongest, truest image for this channel is the **waterline itself**: the ship above, its fate below. The Oriskany really went down
  stern-first. That image is already in the thumbnails (the "37 MINUTES" bow-up shot), so the logo can echo it without a sun.

### 3. Craft
- **Carrier proportions (A), compared with an Essex / SCB-27C (Oriskany) profile:**
  - Island position: 124–146 on a 222 deck = 56–66 % from the stern. That is acceptable (the Essex island sits just forward of midships). Keep it about 52–68 %.
  - Island shape: it is 22 units long and 42 tall (with the mast), a tall narrow tower. The real island is **long and low**, about 1/7 of the deck length, with one
    big stack with a raked cap. As drawn it reads Nimitz or submarine. Make it 34–38 long and 20 high for the base, with the bridge and stack on top (spec below).
  - Flight deck slab: 5 units thick (2.3 % of length). It disappears below 98 px. Use 9 units (about 3.7 %): the overhanging deck is *the*
    carrier cue.
  - Hull: a flat keel with symmetric 10/18 rakes reads as a barge. Give it a raked, flared bow (stem from deck x 236 down to keel x 224) and
    a stern cut-up (keel ends at x 36, knuckle at 22,24). The bow overhang should be clearly longer than the stern overhang.
- **Balance and crop:** the content is clipped at r = 256 but the ring sits at r = 246 (stroke 242–250). A 6–14 px band of navy, sea and red
  line shows **outside** the ring. In the lockup this is plainly visible as a blue crescent under the ring and the red line poking out on both
  sides (lockup x ≈ 28 and 452). It looks unfinished.
- **Gradients:** the radial sun gradient (#F4C76A → #E8A33A) cannot be seen below 176 px. It is harmless, but it is dead weight. The sea gradient is fine.
- **SVG hygiene:** the sea rect and all four reflection bars are drawn **twice** (once in `sun_and_sea`, once as `cover` + `refl`).
  There are two `<defs>` blocks, and a dead first `text_path` call in `lockup()` (line 145). This is not visible, but fix it before this becomes the master.
- **Lockup typography:**
  - The apostrophe is a correct curly ’. The T–’ gap (about 20 px) is wider than ’–S (about 15 px): kern T’ by −20 font units.
  - The word gap of 46 px is fine.
  - The tagline "WHAT HAPPENED TO THE SHIPS" is ~880 px wide against a ~980 px wordmark: neither justified nor clearly shorter. It is set
    in gold (yellow again). The wording is clumsy: plural "ships" and no verb energy.
  - The lockup canvas has about 296 px of dead space on the right (content ends at x 1504 of 1800).
  - The icon's centre (y 240) sits 16 px above the centre of the text block (about 256).

### 4. Distinctiveness
- Forgotten Fleet: AI photoreal, yellow caps, turquoise sea. A gold-sun avatar plus a gold tagline drifts toward them in the sidebar.
- Naval-history channels generally use crests, anchors or photoreal ships. A flat white carrier cut by a red waterline in a red ring is
  unclaimed territory and matches our white/red thumbnails.
- Name confusion (Fleet's End / Forgotten Fleet): never use an "F" monogram or an anchor. Both push us into the generic pile. Keep "END" red
  and big.

### 5. Technical
- **Ring inside the crop:** yes (the outer stroke edge is at 250 < 256). The problem is the art *outside* the ring (see Craft).
- **Banner safe area:** I measured the content bbox at x 534–1943, y 522–881. That is **inside** the safe area 1546 × 423 (x 507–2053, y 508–931), but:
  - It is off-centre: 27 px left margin against 110 px right. Shift it +41 px.
  - The top margin is only 14 px.
  - The banner horizon is at y 950 (H × 0.66), **below** the safe strip. On desktop (which shows the centred 2560 × 423 strip) and on mobile, the sea and the red line
    never appear, so the banner is just navy with a lockup. Only TV shows the sea.
  - The avatar sits right next to the banner on desktop, so repeating the icon in the banner wastes space.

## MUST FIX (whichever direction)
1. **Drop concept B.**
2. **Clip the art inside the ring:** `<clipPath><circle r="241"/>` (not 256). Ring: `r="247" stroke-width="12"` (stroke 241–253, inside 256).
3. **Thicken everything that has to survive 24 px** (units in the 512 box):
   - ring 8 → 12;
   - red waterline 5 → 12 (`y = hz − 6`);
   - flight-deck slab 5 → 9;
   - delete the reflection bars (or keep at most 2 bars at 14 units high, ≥ 0.6 opacity, and accept that they vanish at 48 px).
4. **Sink the ship:** at least 35 % of the hull length under the waterline. Stern-first, with the deck crossing the horizon at about 35 % of its length from the stern. Rotation −17° → **−20°**.
5. **Remove the mast yard** (no "+" over a sinking ship). Keep a plain pole mast.
6. **Remove gold as a brand colour:** no gold ring and no gold tagline. Ring: red #D9372B (or white #F4F1EA). Tagline: white at 75 % or steel
   #8FB3D3.
7. **Banner:**
   - put the horizon/red line at y ≈ 860–880 (inside the 508–931 strip);
   - centre the content (shift +41 px);
   - keep ≥ 40 px clear inside the safe area on all sides;
   - replace the icon with the series promise, e.g. "EVERY SHIP HAS AN ENDING · NEW STORY EVERY WEEK" (Oswald 700, 54 px, white 80 %).
8. Remove the duplicate sea rect, the duplicate reflections, the second `<defs>` and the dead `text_path` call in `make_vector_logo.py`.

## SHOULD FIX
- Redraw the carrier as an Essex SCB-27C profile: a long, low island with a stack (path below).
- Lockup:
  - kern T’ −20 units;
  - set the tagline to the wordmark width exactly (tracking about 0.11 at 62 px, or 66 px with tracking 0.08);
  - crop the canvas to the content + 40 px;
  - align the icon centre to the text-block centre.
- Tagline wording: "WHAT HAPPENED TO THE SHIP" (singular, as in the channel description) or "EVERY SHIP HAS AN ENDING".
- Drop the radial sun gradient (if the sun is kept, use one flat colour).
- Export one 800 × 800 PNG for upload. YouTube downsizes it itself, so check the 24/48 renders but do not design a separate small variant unless the
  24 px test fails.

## Recommended final direction: "Waterline" (concept C)

The white carrier going down stern-first, sliced by the red waterline. The submerged part shows as a faint ghost under the
surface. That ghost *is* the channel promise: what happened below the line. No sun. Colours are only navy, steel-blue, white and red, so it matches
the thumbnails and the wordmark exactly and stays clear of the yellow look. I rendered it at 176/98/48/24 px. It is the only version in which the
carrier and the red line both still read at 24 px (a white wedge on navy over a red bar).

Note: this is closer to the rejected raster (white ship, red line) in palette than A is. The differences are what make it a logo rather than a
clip-art drawing: a true Essex profile, a real sink angle with a third of the hull under water, the ghost hull, the art clipped inside the ring, a red ring
instead of gold, and no cross-mast. Show the owner C next to a fixed A ("A-fix" below) so he can choose with the problems spelled out.

### C, exact SVG spec (512 × 512)
```
clipPath "disc": circle cx=256 cy=256 r=241        (all art inside this)
clipPath "above": rect x=0 y=0 w=512 h=296
clipPath "below": rect x=0 y=296 w=512 h=216
sky:   rect 512×512 fill #0A1622
sea:   rect y=296 h=216, linear gradient top→bottom #1C4A72 → #0F2C47
SHIP (bow to the right, deck top at y=0, keel at y=38; units before transform):
  M0,0 L246,0 L246,9 L0,9 Z                                   flight deck (overhangs both ends)
  M10,9 L236,9 L224,38 L36,38 L22,24 L10,24 Z                 hull: raked bow, stern cut-up
  M128,0 L128,-20 L166,-20 L166,0 Z                           island base (52–67 % from stern)
  M134,-20 L134,-31 L160,-31 L160,-20 Z                       bridge
  M138,-31 L136,-42 L152,-42 L154,-31 Z                       stack, slightly raked
  M157,-31 L157,-56 L160,-56 L160,-31 Z                       pole mast (NO yard)
ship transform: translate(40,404) rotate(-20) scale(1.80) translate(0,-38)
  -> stern ~38 % under the line, bow tip ≈ (448,205), inside r=241
draw 1: SHIP clipped to "below", fill #6E9AC0, opacity 0.40      (ghost hull under water)
draw 2: SHIP clipped to "above", fill #F4F1EA                    (ship above water)
waterline: rect x=0 y=290 w=512 h=12 fill #D9372B                (drawn last, inside disc clip)
ring: circle cx=256 cy=256 r=247 fill=none stroke #D9372B stroke-width 12   (outside the clip)
```
Optional, for 176 px and up only: 3 tiny bubbles (circles r = 4, 3 and 2 at (96,330), (110,352) and (88,372), #F4F1EA at 0.5 opacity) rising from the stern.
Don't add more than that.

### Fallback "A-fix" (if the owner wants to keep the sun)
- Use the same ship path and transform as C, filled #06101A.
- Sun: one flat colour, **red-orange #D9572B** (not gold). Centre (276,300), r = 150, clipped above the horizon. Move the sun so the whole hull above
  water sits *on* the disc: no part of the black ship on the navy sky.
- Waterline: white #F4F1EA, 10 units (the red is now in the sun).
- Ring: white, 12 units.
- No reflections, no gradient.
- I would still rank it below C: at 24 px it becomes an orange dot, and the
  sunset reading remains.
