# Critique A: picture and truth (`oriskany_full_v1.mp4`, 14:45)

Critic: independent pass, 2026-11-05. **Method:** I extracted 1,770 frames (one every 0.5 s, 480p) and a 2 s contact grid with
the spoken words from `build/words.json` under each frame. I took full-resolution frames at every suspect moment and ran
ffmpeg scene detection (189 hard cuts). I read every caption against `NARRATION_v2.txt`, `FACT_SHEET.md`, the three
`FACTCHECK_*` files and `MANIFEST.md`. Shot times come from `chapter/c0*.json` (absolute = chapter offset + shot start).
Nothing was re-rendered and no other file was edited. The scratch frames were deleted afterwards.

Severity: **MUST FIX** = false, misleading or visibly broken. **SHOULD FIX** = breaks a channel rule or weakens the proof.
**NICE** = polish. Items in chapter 1 (0:00–0:48.6) are marked *approved hook: owner decision*.

---

## MUST FIX

### M1. Leftover demo text "salt lowers the freezing point" on two cards
- **3:43.0–3:43.8 (c03 s14)**: under the big "4", over the Oriskany aerial. Spoken: *"…the Navy cited him for downing four."*
- **6:27.5–6:29.4 (c04 s07)**: under "2 MORE YEARS". Spoken: *"It would take two more years."*
- **Evidence:** in both frames, gold text reads **"salt lowers the freezing point"**. It is the default `subline` in
  `templates/blocks/number_clip.py:86` (`ctx.p('subline', 'salt lowers the freezing point')`), left over from the
  prehistory demo (`templates/demo/natlantic.json`). The swap variant (`old`/`new`) has no `subline`, so the default shows.
- **Fix:** change the default in `number_clip.py` to `''`, or pass `"subline": ""` on c03 s14 and c04 s07. Then grep all
  templates for other demo defaults. Re-render c03 and c04.

### M2. Text runs off the frame (clipped words)
| time | shot | what shows | spoken |
|---|---|---|---|
| 3:53–3:55 | c03 s18 | "12,000 sortie" (the **s** is cut off at the right edge) | "…more than twelve thousand combat sorties." |
| 6:55–6:57 | c04 s15 | "**C**ONTAMINATED MATERIAL COMES OU**T**" (cut on both sides) | "…material that contaminated had to come out" |
| 7:41–7:44 | c04 s27 | "NAVY SPENDING, SPRING 200" (the 6 is cut off) | "…twelve point seven million dollars" |
| 9:15–9:19 | c05 s22 | "LARGEST ARTIFICIAL REEF IN THE WOR" (cut off) | "…the largest artificial reef in the world." |
- **Fix:** add auto-fit (shrink to 90 % of the frame width) to `text_card`, `number_clip` and the `anim_gauge` label, or
  break the line in two: "LARGEST ARTIFICIAL REEF / IN THE WORLD", "CONTAMINATED MATERIAL / COMES OUT". Move "12,000 sorties"
  left so it ends ≥ 96 px from the edge. These near-misses are the same bug, so check them too: "26 OCT 1966 → 26 OCT 1967
  ONE YEAR TO THE DAY" (5:24, ends about 20 px from the edge) and "THE WARNING CLEAN TO THE NEW STANDARD" (13:17, ends about
  20 px from the edge).

### M3. A half-frame shading box with hard edges on every lower third and text card over film or photos
- **Evidence (full-res frames):**
  - 1:34.5 (c02 s13, "A WARSHIP AS A THEME PARK"): the dark shade stops in a straight line about 14 % below the top and
    about 72 % across. The top band and the bottom-right block stay lighter, so a visible rectangle sits on the photo.
  - The same box appears at:
    - 1:44 (c02 s16) and 2:04 (c02 s23); 2:22 (c02 s27);
    - 3:26 (c03 s09) and 4:06 (c03 s22); 5:08–5:10 (c03 s41) and 5:26–5:28 (c03 s46); 5:42–5:46 (c03 s50);
    - 9:06–9:08 (c05 s20); 9:56–9:58 (c06 s09);
    - 10:44 (c06 s21) and 11:10 (c06 s29); 13:12–13:14 (c07 s30).
- It looks like a broken grade or a compositing error, and it repeats roughly 15 times.
- **Fix:** the shade or vignette layer in `lower_third` / `text_card` (`dim` over a clip) is sized or positioned in a
  smaller box than 1920×1080. It may be a 0.72-width layer anchored at the top-left, or an un-scaled 1440 layer. Make it full
  frame (`inset:0`), re-render c02, c03, c05, c06 and c07, and check one frame per lower third.

### M4. Generic footage with NO "ILLUSTRATIVE" tag (the letterboxed number cards hide it)
| time | shot | footage (MANIFEST) | what's on screen | spoken |
|---|---|---|---|---|
| 10:13.6–10:16.0 | c06 s13 | NOAA Deepwater Horizon lab, 2010 (`g_lab_a`) | "254 fish" over gloved hands filleting a red snapper, **no tag** | "Two hundred and fifty-four fish from the wreck." |
| 12:08.8–12:13.8 | c07 s13 | NOAA, Florida Keys diver over elkhorn coral (`g_keys_diver`) | "FIRST YEAR 4,200 dive trips", **no tag** | "…four thousand two hundred charter dive trips." |
| 12:13.8–12:18.0 | c07 s14 | NOAA angler, Gulf (`g_recfish_b`) | "ECONOMIC IMPACT $3.6 million", **no tag** | "…three point six million dollars of economic impact" |
- **Why it's wrong:** with "254 fish from the wreck" over a snapper being cut up, the viewer reads it as the Oriskany sample.
  It is a 2010 oil-spill lab. "4,200 dive trips" over a coral-reef diver reads as the Oriskany. The build report (leftover
  #3) calls the first case "hard to read". In fact the tag is **absent**, because the card's letterbox bars cover the top 8 %
  where the tag sits.
- **Fix:** draw the tag above the letterbox and the dim layer, inside the picture area (y ≥ letterbox + 16 px). Alternatively,
  use the un-letterboxed `text_card` style for these three. Check every `b_` shot once more after the re-render.

### M5. Panther / Corsair swapped against the words
- **3:31.5–3:33.2 (c03 s11)**: spoken *"four of her Panther jets"*. The frames at 211.5 s and 212.0 s show a **propeller F4U
  Corsair** landing. No Panther is visible in this shot.
- **3:25.7–3:28.2 (c03 s09)**: spoken *"Her crews called her the Mighty O"*. This shot shows the **F9F Panther jet** ("111").
- MANIFEST lists the opposite (s09 = Corsair, s11 = Panther then Corsair). The in-points or files are swapped.
- **Fix:** swap the two in-points so the Panther sits under "Panther jets". Alternatively, trim s11 to the Panther portion
  only (reel 78776 at about 15.2 s), and fix the MANIFEST rows to match.

### M6. "WORLD'S LARGEST REEF" label is false
- **14:13.9–14:16.7 (c07 s47)**: a gold tag on the SS United States pin reads **"WORLD'S LARGEST REEF"**. Spoken: *"Now it is
  about to take her title."*
- **Evidence:** the title is "largest **artificial** reef" (Guinness record 84541, FACTCHECK_C). The world's largest reef is
  the Great Barrier Reef. The tag also states as present fact something that is still planned (12 Nov, weather permitting).
  TITLES_THUMBS.md already bans "LARGEST REEF" wording.
- **Fix:** "LARGEST ARTIFICIAL REEF → NEXT?" or "TITLE PASSES NOV 12 (PLANNED)".

### M7. Invented dollar figure: "REEF, NEW STANDARD 24 $M"
- **13:17.3–13:21.8 (c07 s32)**: a bar chart shows SCRAP 24 $M against **REEF, NEW STANDARD 24 $M**. Spoken: *"…could wipe out
  the savings of reefing compared to scrapping."*
- **Evidence:** the MARAD Jan 2008 report (FACTCHECK_B B27) says cleaning to the BMP "could negate potential cost advantages".
  It is a general warning with no figure, and it is not about the Oriskany. No source gives a $24 M reef cost. The "$M" scale
  makes a made-up number look like a finding.
- **Fix:** drop the units and the number. Show two equal-length unlabelled bars marked "SCRAP" / "REEF TO NEW STANDARD" with
  "≈ SAME?", or just a text card: "SAVINGS COULD BE WIPED OUT · MARAD, 2008".

### M8. "By the Navy's own sums, it was also the cheapest" uses a press figure as the Navy's
- **13:00–13:08 (c07 s27–s28) and 13:38–13:42 (c07 s37)**: the bars show "REEF (FINAL) 20 $M" against "SCRAP (USNI 2006 EST.)
  24 $M", under the kicker "The cheapest, *by its own sums*".
- **Evidence:** the $20 M is the **press** sinking-day total (F4, AP/BBC). The Navy's own figure when it called her a bargain
  was $12.7 M and rising (F1, USNI06). The EPA line items add to $23.6 M (F3), which nearly equals the $24 M scrap estimate.
  So "cheapest by its own sums" is shakier than the chart suggests.
- **Fix:** label the reef bar "REEF (PRESS EST., 2006) ≈ 20". Or use the Navy's "$12.7 M AND RISING" for the "bargain" beat,
  and soften the kicker to "Cheaper, *on paper*". (If the script line changes, that is the owner's call. The picture must not
  add precision the words don't have.)

---

## SHOULD FIX

### S1. Same generic clips used far beyond "at most twice, 3+ min apart"
- **Ex-Kitty Hawk reel (DVIDS 828554):** 9 uses, at 0:58, 1:01, 1:11, 2:03, 2:21, 6:05, 12:38, 13:04, 13:26.
  - `g_kh_c` (tug ahead of the hulk) is used at 1:11, 2:03 and 12:38. The first two are **52 s apart**.
- **Fort McHenry `g_fm_tow`:** used at 1:36, 1:42, 2:23 and 12:55. The hull "43 FORT McHENRY" is readable each time; the first
  two are **6 s apart**.
- Viewers will notice the same hull number four times.
- **Fix:** keep at most 2 uses per clip, 3+ min apart. Replace 1:42 (c02 s16), 2:23 (c02 s28), 2:03 (c02 s23) and
  12:38 (c07 s21) with:
  - text cards over the real NARA photos already in the build (the 1990 Bremerton row photo used at 5:50, the 1990s hulk
    stills);
  - or a ledger/stamp animation.

### S2. Generic footage that contradicts the words, even with its tag
- **6:04.9–6:07.7 (c04 s02)**: *"…old warships to states **as reefs**"* over ex-Kitty Hawk under tow **to a scrapyard**. Use
  the hook's reef/foam shot or a map of Gulf reef sites.
- **12:38.4–12:42.8 (c07 s21)**: *"taking her apart is exactly what **nobody had managed** to do"* over a carrier visibly on
  its way to the breakers ("…TOWED TO A SCRAPYARD"). It argues against the line. Use the Mare Island map or the
  "ALMOST NOTHING CUT" ledger instead.
- **1:01.0–1:03.3 (c02 s05)**: *"For thirteen years, she just waited"* over a tug moving in fog. Nothing waits. Use the
  real 1990 Bremerton row photo (`p_c03_s52`, shown at 5:50). That was the script's original plan (SCRIPT_v2, line 95).

### S3. Labels that tie later film to named men
- **4:05.4–4:07.4 (c03 s22)**: "CDR JAMES STOCKDALE" over A-4Es in flight from a **1968** reel (NARA 86638). Stockdale was
  shot down in 1965. This reads as his aircraft.
- **5:25.7–5:29.7 (c03 s46)**: "VA-163 LCDR JOHN McCAIN" over a catapult launch from the **1968** reel (86313). McCain was a
  POW from Oct 1967. This reads as McCain launching.
- **Fix:** add a small date tag ("ORISKANY A-4s · 1968 FILM"), or put the name over a PD portrait. NHHC has official
  portraits of both men; check the rights field.

### S4. "NAVY CITATION, 2023" shown next to "1" for about 1.5 s
- **3:41.0–3:42.9 (c03 s14)**: the kicker changes to "NAVY CITATION, 2023" at *"cited"*, while the number still reads **1**.
  It reads as "2023 citation: 1". The 4 only lands at 3:43.4.
- **Fix:** switch the kicker on "four", at the same moment as the number.

### S5. Near-empty dark frames for 3.4–4.5 s while the words run on
In each of these cards only a small kicker is on screen until the main text lands. That breaks "something new every
1.5–4 s".
| shot | time | lead before the main text |
|---|---|---|
| c02 s24 "A PROTEST" | 2:06.2 | 3.9 s |
| c06 s07 "EPA RULING" | 9:46.6 | 3.6 s |
| c03 s49 "RELEASED · MARCH 1973" | 5:36.6 | 3.4 s |
| c04 s28 "PRESS, SINKING DAY" | 7:44.1 | 3.4 s |
| c04 s29 "FLORIDA SENATE" | 7:48.7 | 3.4 s |
| c07 s30 "MARAD … JAN 2008" | 13:10.5 | **4.5 s** |

- In c07 s30, the source line "MARAD · REPORT TO CONGRESS · JAN 2008" + "A WARNING" is visible for only about **0.7 s**
  (13:15.0–13:15.7) before the cut. The source attribution is unreadable.
- **Fix:**
  - Put a picture under the long-lead cards: the GAO/scrap ledger for "A PROTEST"; the EPA map for "EPA RULING";
    a McCain 1973 release photo (NHHC) for c03 s49.
  - Or show the main text one word earlier.
  - For MARAD, show the kicker from the shot start and hold the card ≥ 2 s after "warning".

### S6. Off-era photo at 2:47 spoils the sinking day
- **2:47.4–2:49.9 (c02 s33)**: *"So what kind of ship ends up like this?"* over the **2006** photo of a veteran saluting from
  the seawall. The narrative is in 1999 here. The same photo is used correctly at 8:27 (c05 s07, *"One of them stood on
  the seawall and saluted"*), so this use also blunts that later beat.
- **Fix:** use the 1990s hulk photo or the Beaumont reserve-fleet still.

### S7. ILLUSTRATIVE tags dimmed to near-illegible by the animation overlays
- 1:11–1:16 (c02 s08), 12:55–12:58 (c07 s26), 13:04–13:06 (c07 s28), 13:26–13:29 (c07 s34) and 13:35–13:38 (c07 s36): the tag
  is grey on grey under the "How it ends" / gauge shade.
- **Fix:** composite the tag after the dim layer at full opacity. The same render-order change fixes M4.

### S8. "Four of her sisters were already museums" (1:16–1:19, c02 s09): the timeline is wrong for the picture
- The shot sits at 1989 / early 1990s in the story. At that time only Yorktown (1975) and Intrepid (1982) were museums;
  Lexington opened in 1992 and Hornet in 1998.
- The graphic shows 4 "MUSEUM" tags at once. FACTCHECK_A D4b confirmed the sentence from the GSEC Navy text, but not its date.
- **Fix:** add years under the tags (1975 / 1982 / 1992 / 1998). If the owner agrees, change the narration to "Within a few
  years, four of her sisters were museums."

### S9. Pacing: no wow between 0:48 and 1:28 (40 s)
- First-3-minute beats:
  - 0:10 "On purpose"; 0:19 "37 minutes"; 0:25 "$20 million"; 0:40 SS United States;
  - then nothing until 1:28 "City of America" theme park;
  - then 1:56 "over $1 million" against the $600,000 appraisal; 2:22 "almost nothing cut"; 2:40 "around a continent".
- Decommissioned, Bremerton, "waited", "struck" (0:48–1:19) is a 40-s flat stretch against the "every 30 s" rule.
- **Fix (picture side):** open c02 with the real 1990 photo of three carriers rusting in a row, with "13 YEARS" counting up
  on "thirteen". Or pull the "City of America" tease forward. Whether to change the script is the owner's call.

### S10. Ending length
- The answer starts at 13:21.8 (*"So that is why the Navy sank its own aircraft carrier"*). The voice ends at 14:25.8, which
  is **64 s**, plus an 18 s end-screen hold.
- If "ending" means the SS United States coda plus the question (13:41.9 → 14:25.8), it is 44 s and passes.
- Read strictly from the reveal, it fails the ≤ 45 s rule.
- **Fix:** trim the c07 s33–s37 recap (13:21–13:42 restates the four reasons already given). For example, cut s34 + s37 and
  the "cheapest" gauge, which is also M8.

### S11. 1:16.0–1:16.6 (c02 s08 → s09): an empty dark frame
The frame is blank between "How it ends" and the sisters graphic, on *"Four of her sisters"*. Start the first silhouette at
the cut.

---

## NICE

- **N1. 9:04.3–9:05.0 (c05 s19):** "ON THE SEABED 212 FT" is printed while the drawn hull is still tilted in mid-water. It
  only settles at about 9:05.5. Hold the label until touchdown, or start the settle earlier.
- **N2. Film-gate edges on the 1969 aerials:** 0:50 (c02 s01), 5:06 (c03 s40) and 14:17–14:21 (c07 s48) show dark gate slivers
  at the left and right edges, plus a dust blob (14:17). Crop 1–2 % more, or pillarbox cleanly (CLAUDE.md archive-film rule).
- **N3. 7:31–7:34 (c04 s24):** "$800,000 ONE MORE TOW" (the June 2005 tow) plays over the NASA Rita loop (Sept 2005), before
  Rita is named. It is tagged, but out of order. Use the June 2005 tow map instead and keep Rita for c04 s25.
- **N4. 10:41–10:43 (c06 s20):** the "VERMILION SNAPPER" and "SCAMP" chips overlap each other and the "NEVER CROSSED EITHER
  LINE" label. Space them out.
- **N5. 10:10 (c06 s11):** the counter passes through "1 ROUNDS". Use singular/plural or start at 8.
- **N6. 13:46–13:48 (c07 s39):** the SS United States film has an unidentified aircraft carrier in the background, on
  *"She will not be the biggest for long."* Some viewers will read it as the Oriskany. Use the profile window (`b10_ssus_profile`)
  without the carrier.
- **N7. 10:55–10:57 (c06 s24):** the rubble reef sits 8 mi NW of the pin. The direction is illustrative (CREDITS note), but
  nothing on screen says so. Add "(position approx.)".
- **N8. Hook** *(approved hook: owner decision)*: shots of 0.33 s (0:17.7, c01 s09) and 0.7 s (0:19.9 and 0:20.6) are under
  the 1.5 s floor. 0:16.0–0:16.7 shows the helicopter photo before its "17 MAY 2006 · USS ORISKANY" lower third lands. No
  truth problems found in the hook. Every caption (212 ft, 22 charges, 37 minutes, 3+ years, ≈$20 M, 13 nautical miles,
  SS United States NE of the Oriskany, 1968 FILM) matches the fact sheet and lands on its word.

---

## Checked and OK
- **Structure:**
  - First frame: a map (Gulf bathymetry, 0:00).
  - Title promise (title A "Why the Navy Sank Its Own Aircraft Carrier"): spoken 0:06.4–0:11.5 ("No enemy sank her. The
    United States Navy did. On purpose."). Passes.
  - No ship résumé before 2:56 (the war years start at c03, 2:56). Passes.
  - Reversal: 7:58 ("not the only place the PCBs were hiding") into the fish test at 10:16 ("not what anyone wanted").
    Passes.
  - Closing question: 14:16–14:25. Passes.
- **Shot length:** longest 5.93 s (c03 s52); nothing over 6 s apart from the 20 s end screen.
- **Numbers that land on their word** (checked frame by frame): 212 ft; 22; 37 (both); $20 M; $600,000; 3 bids; 6 weeks;
  1 MiG; 12,000; 7½; ≈700 flares; 5,400 °F; 7 h; 44; 5½; $2.8 M / $2.1 M / $7.6 M; ½+; $3.7 M; $800,000; 12.7; ≈$20 M;
  ≈$21 M; 500+ lb; 10:25 a.m.; ≈5 h; ≈700 lb; 254; 8 rounds; 4,200; $3.6 M; 67; 97 %; 990 ft; NOV 12; 13 nmi; $50,000.
- **Dates and names that match the fact sheet:**
  - SEPT 1976; JULY 1989; SEPTEMBER 1995; 1996; 1997; 1999; MAY 1944; 13 OCTOBER 1945; AUGUST 1947; JUNE 1950;
    18 NOV 1952; MAY–DEC 1965; 9 SEPT 1965; 26 OCT 1966; 26 OCT 1967.
  - NOV 2003; APRIL 2004; JUNE 2005; RITA 2005; 22 MAR 2006; 15 FEB 2006 (EPA Region 4); 17 MAY 2006; GUSTAV 2008;
    LATE 2009.
  - VA-163 (not VA-46); Truc Bach Lake; Mare Island, Vallejo; Escambia FL + Baldwin AL; Okaloosa County.
  - The bill of sale says "OVER $1 MILLION" (true per GAO95).
- **ILLUSTRATIVE tags** are present and readable on all other generic shots (Kitty Hawk, Fort McHenry, NOAA snapper,
  anglers, Navy divers in Colombia, NASA Rita and Gustav).
- **No true black frames, no leaders and no stretched 4:3.** The hard cuts flagged by `check_clips` are all intentional.
