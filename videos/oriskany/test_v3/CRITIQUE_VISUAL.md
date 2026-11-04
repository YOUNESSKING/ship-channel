# Oriskany test v3: visual and story critique

Scope: storytelling, hook, retention, pacing, picture, editing, typography, and whether each image shows what the narration says. I only mention sound where it breaks a visual moment.
Method: frames every 0.5 s plus full-resolution stills at the key moments (`scratchpad/critic_visual/`), lined up against `build/words.json` and `chapter/c01.json`, with scene-cut detection. Rules checked: CLAUDE.md, STYLE_LOCK 1a/1c/2, GOLD_STANDARD 22/36-45/72, and the Forgotten Fleet study (4a and final DO/DON'T).

## Scores

| | /10 | One line |
|---|---|---|
| Hook | **5.5** | Strong pictures, but line 1 is a date ("May seventeenth, two thousand six"), frame 0 is a photo, and the first wow comes at 7.4 s and is gone 0.7 s later. |
| Story | **7** | Good arc: blast, gone in 37 min, "No enemy sank her. The Navy did. On purpose.", the cost, the 3-option question, the hidden-inside tease, then the SS United States cliffhanger. The best asset (the SS United States) goes unnamed in the narration. |
| Pacing | **7** | No shot runs over 6 s and nothing is dead. The 37-minute montage runs 7 stills in about 3 s (too frantic), while the money shot (the blast) gets 0.7 s. |
| Visuals | **5** | The archive is good, but there are compositing seams, an obstructed frame, a wrong-era shot, a flat clip-art hero animation drawn about 25 ft too shallow, small kickers that can't be read on a phone, and five different colour looks. |
| **Overall** | **6** | The bones of a good hook, roughly 6-8 fixes away from shippable. The fixes are mostly cheap edits, not new builds. |

## Timeline audit (picture vs words)

| time | words | picture | verdict |
|---|---|---|---|
| 0.0-2.9 | "May seventeenth, two thousand six." | 2006 photo: stripped hulk, SH-3 overhead; "MAY 17, 2006" card | Strong image, weak line. Breaks "Line 1 = the stakes", "first frame is a map" and STYLE_LOCK 1a "never a date + place". |
| 2.9-4.6 | "Off the coast of Florida," | Map dive, Gulf → Pensacola → pin | Correct, but it lasts only 1.6 s. |
| 4.6-6.9 | "Navy demolition divers set off" | EOD sailor with a det-cord spool (13 May 2006) | OK |
| 6.9-7.4 | "explosive" | smoke plume photo, 0.5 s | OK, too short |
| 7.4-8.1 | "charges" | **the blast photo, 0.7 s** | Lands on the word, good. The money shot is then thrown away. |
| 8.1-10.6 | "inside a retired American aircraft carrier" | **1966 film, ship in full service, air wing on deck**; lower third "DECOMMISSIONED 1976 / USS Oriskany" | "Retired" is said over a working warship. Leaving the explosion to cut back 40 years kills the momentum. |
| 10.6-12.2 | "...carrier." (then silence) | 1966 bow-on film, destroyer alongside | Résumé footage in the first 15 s |
| 12.2-15.3 | "Thirty seven minutes later, she was gone." | 7 sinking stills in about 3 s with a 0→37 counter | The counter shows "6 minutes" and "14 minutes" over photos that weren't taken at those times. Too frantic. |
| 15.3-17.5 | "About nine hundred feet of warship," | 1969 aerial, "900 ft" | OK |
| 17.5-20.6 | "now sitting two hundred and twelve feet down." | Sinking cross-section with a depth gauge | Best idea in the video. The drawing is generic and the depth is wrong (see the issue table). |
| 20.6-22.2 | "No enemy sank her." | 1968 A-4 catapult launch | Good contrast. There is an obstructed frame at about 21.3. |
| 22.2-24.3 | "The United States Navy did." | "34" on the island, 1966 | Good: the hull number proves which ship it is. |
| 24.3-26.0 | "On purpose." | Slam card over the 2006 boil | Good |
| 26.0-27.6 | "It took three years" | **1952 B&W, at anchor in San Diego**, "PREPARING HER TO SINK · 3 years" | **Wrong era.** It presents a 1952 photo as the 2004-06 preparation. |
| 27.6-29.4 | "and about twenty million dollars" | 2006 welder, blown-out frame; "$20 million"; subline "budgeted at under $3 million" | The subline is never spoken, and the number has low contrast on the flare. |
| 29.4-31.4 | "just to get her ready to sink." | 2006 tow aerial | OK |
| 31.4-33.8 | "So why would the Navy pay millions" | 1966 A-4 "314" on the catapult, "OFF VIETNAM, 1966" | Doesn't show the line (glory footage under a cost question) |
| 33.8-35.9 | "to send one of its own carriers" | c.1967 aerial, soft upscale | Doesn't show the line |
| 35.9-41.2 | "to the bottom of the sea, instead of keeping her, or simply cutting her up for scrap?" | Options board over 1969 film | The highlight box sits on "Keep her" then **"Scrap her"** (two boxes at 39.7). "Sink her" is boxed for only about 0.4 s before the cut. Film-burn glitch at 40.3-40.6. |
| 41.2-42.6 | "The answer starts with what" | 1968 flight deck | Filler |
| 42.6-44.5 | "was hidden inside her." | X-ray: near-black frame, then a flat brown silhouette and "???" | Cheap. "HIDDEN inside" just repeats the words. |
| 44.5-49.3 | "And this month, a second famous American ship is scheduled to go down off the same coast," | SS United States, 1968, 3 shots; tag "SS UNITED STATES · 1968" | Good footage. The **narration never says her name**; only an on-screen tag gives it away. |
| 49.3-53.6 | "for the very same reason." | End map: both wrecks, "13 NAUTICAL MILES APART", "THE SAME REASON" | Good closer. The labels are too small. |

## Issue table

| time | issue | severity | concrete fix |
|---|---|---|---|
| 0.0-2.2 | Line 1 is a date. Frame 0 is a photo, not a map. Nothing is at stake until 7 s (STYLE_LOCK 1a: "never a date + place"; CLAUDE.md: "Line 1 = the stakes", "first frame is a map"). | **high** | Open in the present tense with the stakes, the Arizona pattern: *"Right now, two hundred and twelve feet under the Gulf of Mexico, lies a nine-hundred-foot American aircraft carrier. No enemy put her there."* Frame 0 is the map dive to the wreck pin (the existing `dive.mp4`), with the "212 FT" number slamming on its word. Put the date on the blast card instead. |
| 7.4-8.1 | The blast, the biggest wow in the video, is on screen for 0.7 s, then cuts to 1966 film. | **high** | Hold the blast 2-2.5 s with a push-in, then step through the second and third blast stills (6698618/6698619, aerial port bow). Cut the 1966 service shots (8.1-12.2) out of the hook entirely. |
| 8.1-12.2 | "a retired American aircraft carrier" plays over a 1966 working carrier with a "DECOMMISSIONED 1976" lower third. This is a ship résumé in the first 15 s (breaks "no ship résumé in the first 2 min"). | **high** | Keep the 2006 hulk on screen: the helicopter photo, 6698597 leaving Pensacola, or 6698600 under tow. Put "USS ORISKANY" as a name plate on the hulk. Move the decommission date to the body. |
| 10.0-10.3 | Compositing seam: the sharp inset rectangle shows its edges (a hard line at about y=120 and x≈1710) over a blurred copy, plus an in-clip film cut ghosting inside f06. | **high** | Trim f06 to before its internal film cut (it is about 2.2 s into the segment). Render film full-bleed (crop or upscale) or in a clean pillarbox, never as an inset over a blurred copy of itself. Check `clip_plain`/`lower_third` push scaling. |
| 26.0-27.6 | Wrong era: a 1952 San Diego B&W photo labelled "PREPARING HER TO SINK · 3 years". | **high** | Use 2006 preparation photos already in CREDITS: 6698569 (cutting anchor holes in the flight deck), 6698555 (stripped interior through a hatch). |
| 17.5-20.6 | The hero animation puts the flight deck at about 122 ft and the island top at about 58 ft. The fact sheet (H2/H3, FWC) says the deck is ~145-150 ft and the island top 84 ft. The hull is drawn too tall and sits about 25 ft too shallow. The gauge also reads "32 FT" while the ship is floating (it tracks the keel). The ship is grey clip-art with no detail. | med | Rescale the drawing from the fact sheet (keel 212, deck ~145, island top 84). Let the gauge follow the island top or label it "KEEL", starting from 0. Add hull detail, a darker gradient, light shafts and a silt puff on landing so it doesn't look flat-vector. |
| 12.2-15.3 | 7 stills in about 3 s (0.3-0.6 s each) from mixed angles. It reads as flicker, not a time-lapse. The counter shows "6/14 minutes" over photos not taken at those minutes. | med | Use 4 stills, about 0.8 s each, from one camera position (the Kraus aerial series 6698618→621→624→627) so it reads as one ship going down. Drop the counter roll and slam "37 MINUTES" on "minutes" (12.8). |
| 21.2-21.6 | Obstructed frame: a green/black blob covers the left third of the 1968 catapult film. | med | Trim f12 so it ends before the obstruction, or start v13 0.3 s earlier. |
| 39.5-41.2 | The options board boxes "Keep her", then "Scrap her" (two boxes at 39.7), as if the answer were scrap. "Sink her" gets about 0.4 s of box before the cut. A film-burn and blob transition at 40.3-40.6 looks like a render glitch. The title "WHAT DO YOU DO WITH a carrier?" is never spoken, and a stray underline sits under "YOU DO WITH". | med | Don't box items as they appear. After the "scrap?" line, strike Keep and Scrap, then box and hold "Sink her" for at least 1.2 s (extend into 41.1-42.3, which is filler deck film anyway). Remove the burn transition. Fix the underline offset. Change the title to spoken words ("Keep her? Scrap her?") or drop it. |
| 44.5-49.3 | The narration says "a second famous American ship" while the tag says SS UNITED STATES. The most famous, most searched name in the whole video is never said, and the half-mystery helps no one. | med | Say the name: *"...the SS United States, the fastest ocean liner ever built, is scheduled to go down off the same coast"*. Make it a big name plate (5% of frame height) on the funnel shot, not a corner tag. |
| 27.6 | The "$20 million" number fades in over a blown-out weld flare (low contrast). The subline "budgeted at under $3 million" is never spoken (breaks the STYLE_LOCK rule that every word on screen is spoken). | med | Darken or vignette the right third of p14 behind the number. Either speak the $3 million line (it's a strong wow: "budgeted at under three million") or cut the subline. |
| 31.4-35.9 | "So why would the Navy pay millions to send one of its own carriers to the bottom" plays over glory film (A-4 314, a soft aerial). The picture doesn't show the line. | med | Put "millions" over a cost visual (dollar figures stacking on the hulk), and "to the bottom" over the final-moment still 6698627 "bow disappears", or the map wreck pin. One combat shot is plenty. |
| 42.6-44.5 | The x-ray opens on a near-black frame (a dot and a line). The silhouette is a flat brown blob with an unexplained gold bar across the frame. "???" plus "HIDDEN inside" just repeats the narration. It looks cheap next to everything else. | med | Use a real ship profile (kit/ship line art at Oriskany's proportions) with a scan beam sweeping, and cut-away compartments glowing one by one. Show the first frame complete (GOLD 72: no empty frames). One "?" tag on a compartment, no extra text. |
| 0.5, 9.8, 13.0, 15.3, 26.5, 36+ | Letterspaced kickers ("FINAL CHECK · GULF OF MEXICO", "DECOMMISSIONED 1976", "from the first charge", "USS ORISKANY · 1969 · ABOUT", "PREPARING HER TO SINK", "ABOUT") are about 2% of frame height, and some are grey on grey. They can't be read on a phone. "FINAL CHECK…" runs over the island structure. Kickers ending in "about" look broken. | med | Kickers at least 3.5% of frame height (GOLD 72), with a 60% dark scrim behind them, and placed off busy detail. Drop the "about" kickers (fold the word into the number: "~900 ft"). |
| 50-53.6 | End-map labels ("13 NAUTICAL MILES APART", the ship tags) are about 2% of frame height. The ship icons are tiny. "PENSACOLA" is cut off at the top edge at 49.5-50.0. | med | Labels at least 3.5%. Bigger wreck icons with a glow. Start the zoom-out with Pensacola already inside the frame. |
| 4.6-7.4, 20.6-22, 44.5-49 | Corner tags sit at the very bottom-left (about the bottom 5%). The YouTube player bar and the mobile scrubber cover them. | low | Lift tags above the bottom 10%. |
| whole | Five colour looks: 2006 photos warm/sepia with heavy vignette (frame 0 looks like a 1940s print), 1960s film cool and saturated, 1952 B&W, teal maps, brown-gold x-ray. | low-med | One grade family: 2006 colour photos neutral (no sepia, light vignette), film `GRADE=none` with matched black level, x-ray in the map's teal/gold palette. |
| 33.8-35.9, 8.1-12.2 | Soft upscaled 16 mm (f19, f06, f07) looks mushy at 1080p. | low | Upscale with Real-ESRGAN or similar, or keep these shots small or short. They are at least reasonable B-roll. |
| 44.5 / map | "This month" and "SCHEDULED NOV 12, 2026" date the video. It is stale the day after the sinking. | low | Publish before 12 Nov. Otherwise rewrite to "In November 2026..." and re-voice after the event. |

## Top 5 fixes, ranked by impact

1. **Rebuild seconds 0-8 with the stakes first.** Frame 0 is the map dive to the wreck pin. Line 1 is present tense: *"Right now, 212 feet under the Gulf of Mexico, lies a 900-foot American aircraft carrier. No enemy put her there."* Then the blast as the first wow by about 3 s, held 2+ s. The date goes onto the blast card. This is the Forgotten Fleet Arizona pattern (present tense, location under the sea, an unanswered "why") and STYLE_LOCK 1a. Today a cold viewer gets a date and a still for 3 s.
2. **Take all 1960s service film out of the first 20 s and fix the wrong-era 1952 "3 years" shot.** Keep the hook in 2006 (hulk, blast, sinking), and use 2006 prep photos for "three years / $20 million". The war film belongs at "No enemy sank her" only. That one cut is earned.
3. **Fix the honesty bugs in the animations.** Draw the hero sinking to fact-sheet depths (deck ~145 ft, island top 84 ft, keel 212 ft), with a gauge that starts at 0. On the options board, box "Sink her" only, as the last step, and hold it at least 1.2 s.
4. **Name the SS United States in the narration and give her a proper name plate.** She is the most clickable proper noun in the script and a time-sensitive DO #2 asset. Right now she is "a second famous American ship".
5. **Clean-up pass on compositing and typography.** Fix the inset seam at 10.0-10.3, the obstruction at 21.3, the burn glitch at 40.3, the stray underline, and the empty x-ray first frame. Every kicker and label goes to at least 3.5% height on a scrim and above the bottom 10%. Unify the grade.

## What is genuinely good (keep)

- **"No enemy sank her. The United States Navy did. On purpose."** over war film → the "34" hull number → the slam card. Picture and words lock on every beat. This is the hook's spine.
- **The SS United States cliffhanger and the end map** with both wrecks and the 13 nm line. It's a real, time-sensitive open loop, and the map is the most premium-looking element in the video.
- **Number cards that land on their words** ("MAY 17, 2006" on "May", "900 ft" on "nine", "3 years" on "three", "$20 million" on "twenty", "ON PURPOSE." on "purpose").
- **The sinking cross-section idea** (900 ft of ship in 212 ft of water, drawn to the right length ratio). It's a strong explainer visual once the depths are right and the drawing is upgraded.
- **Real NARA film and 2006 Navy stills throughout.** No AI ships, rights logged per file, and something new on screen every 1.5-3 s with no shot over 6 s.
