# Gold standard: what the 66-second test does, and how Video 01 breaks it

Gold standard = `videos/test2/final/test2_v9.mp4` (66.4 s). The owner called it "perfect".
Bad preview = `v01_preview_720p_standins.mp4` (17:01). The owner hates it.
Rule of thumb: **every shot proves the exact words, and something new happens at least every 1.5 s.**

---

## A. The gold standard, shot by shot

Cuts sit on the first spoken word of the line (`timing.py`). Text and icons appear on the exact word they show (`Wd(i)` in `anim.js`).
Clip = AI video clip. Stick = animated stick-figure gag.

| # | Time (s) | Dur | Words | On screen | Category | How it moves | Sound | Why it fits |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.0-2.7 | 2.7 | "Say you fall off a boat in the North Atlantic." | Man in orange jacket at a trawler rail, stormy sea | Clip | Slow push 1.00 to 1.07 | Wind, strings start | Shows the sentence literally. |
| 2 | 2.7-7.2 | 4.5 | "Not a shark. Not a whale. Just you... in the water." | Wide grey sea, one tiny red-jacket person | Clip | Slow zoom 1.00 to 1.16 onto the person | Wind, drum enters at 7.19 | "Just you" = one tiny person, alone. |
| 3 | 7.2-11.1 | 3.9 | "fifteen, thirty minutes before you pass out." | Dark clip of a head at the waterline, letterbox bars, huge "15-30 *minutes*", small "UNTIL YOU PASS OUT" | Text over clip (number) | Number fades in on the word "fifteen"; subline on "pass out"; clip pushes 1.0 to 1.1, jumps to 1.2 on "pass out" | Thud on the number | A number needs a big number on a clip of the danger. |
| 4 | 11.1-13.0 | 1.9 | "And that's with a coast guard." | Rescue helicopter with winch; lower third "coast guard *(45 minutes away)*" | Clip + lower third (joke) | Text on the word; clip jumps to 1.14 | Helicopter, a dry wood-block "tok" on the joke | The joke is a number: 45 minutes away. |
| 5 | 13.0-19.0 | 6.0 | "But what about the Ice Age? When sea level was four hundred feet lower, and ice covered the whole north?" | Map: today's coast, then "THE ICE AGE", gauge counts 0 to -120 m (-400 ft), coastline moves out, **ice grows over land**, ice-sheet names, caption "ICE COVERED THE WHOLE NORTH" | Map animation (one continuous shot) | Gauge runs 1.7 s from the words "four hundred"; ice grows per pixel | Swoosh, slide, ice crunch on "ice covered" | A place + a change = a map that shows the change. |
| 6 | 19.0-21.4 | 2.4 | "Would you be better off in a kelp forest?" | Kelp forest underwater | Clip | Push 1.0 to 1.09 | Bubbles bed | Literal. |
| 7 | 21.4-24.1 | 2.7 | "What about a frozen bay full of seals?" | Seals on ice, orca fin slides in | Clip | Push 1.0 to 1.07 | Wind | Literal, plus a hint of danger. |
| 8 | 24.1-26.8 | 2.8 | "Is there any Ice Age ocean where you'd last?" | Empty dark sea, icebergs on horizon | Clip | Slow push-in | Click | The question: an empty ocean. |
| 9 | 26.8-28.2 | 1.4 | "Just you yourself." | Stick figure treading water, "you" + arrow | Stick | Arms flap, bob | Splash | Label names the subject. |
| 10 | 28.2-30.1 | 1.8 | "No boat, no wetsuit," | Boat icon "NO BOAT" and jacket icon "NO WETSUIT", each crossed out | Stick | Icon pops on its word, X lands 0.3 s later | Click per X | Each noun gets its icon, then is struck out. |
| 11 | 30.1-32.1 | 2.0 | "a hundred yards from shore." | Figure, dotted arrow "100 yards", island with palm | Stick | Arrow fades in on "hundred yards" | none | Distance shown as a measured arrow. |
| 12 | 32.1-33.2 | 1.0 | "Let's find out." | Orca breach at dusk | Hero clip | Push | Hard drop | Biggest wow image on the promise. |
| 13 | 33.2-33.6 | 0.5 | (pause) | Black | Black | - | **Total silence** | The drop. |
| 14 | 33.6-38.3 | 4.7 | "the first ocean is the North Atlantic, twenty thousand years ago." | Map, **ice already on land**, ring pin, "NORTH ATLANTIC", "THE FIRST OCEAN" then "LAST GLACIAL MAXIMUM - SEA LEVEL -120 M" | Map | Slow zoom out, ring pulses | Title thud, lo-fi beat starts | Place + date = pin + ice-age map. |
| 15 | 38.3-41.0 | 2.7 | "Near the ice, the water's about zero degrees," | Pack-ice edge, kicker "NEAR THE ICE", "0 C" | Text over clip | "0 C" on the word "zero" | Click | Number on a clip of that exact place. |
| 16 | 41.0-45.2 | 4.2 | "salt water doesn't freeze until, uh, minus one point eight." | Dark frazil-ice clip. "THE WATER 0 C" then "SALT WATER FREEZES AT 0 C", 0 is **struck out**, "-1.8 C" appears, "salt lowers the freezing point" | Text over clip (number gag) | 4 text beats in 4.2 s, strike-through on the word | Scratch + ding | The idea (0 is wrong, -1.8 is right) is acted out. |
| 17 | 45.2-47.3 | 2.0 | "So it's basically slush." | Pancake ice, italic "slush" | Text over clip (one word) | Slow fade | Ice crunch | Word on the matching image. |
| 18 | 47.3-50.2 | 2.9 | "First minute, you can't control your breathing." | Stick figure gasping, "gasp" twice, "COLD SHOCK / 1 *minute* / can't control your breathing", **timer bar** START to 1 MIN | Stick (info) | Marker slides, figure flails | Gasp x2 | Body reaction = stick figure + timer. |
| 19 | 50.2-52.8 | 2.6 | "After ten, your hands stop closing." | Stick figure, **zoom circle on a hand** whose fingers try to close and fail, "DEXTERITY / 10 *minutes*", timer to 10 MIN | Stick (info) | Fingers curl, fail, shake | Click | The hand icon proves the sentence. |
| 20 | 52.8-56.2 | 3.5 | "even if someone threw you a rope... you couldn't hold it." | Thrower in a boat, rope arcs over, label "rope", rope **slips away**, arm drops, "can't hold it" | Stick (story) | Rope draws on the word "rope", falls on "hold it" | Swoosh, slide-whistle | A tiny story with a start and an end. |
| 21 | 56.2-58.5 | 2.3 | "Good news, no Megalodon." | Megalodon underwater, gold plate "EXTINCT / 3.6 million years ago" | Clip + plate | Plate fades in on the word | Thud + click | Name + fact on the creature. |
| 22 | 58.5-61.2 | 2.7 | "Bad news, the cold's already got you." | Figure sinks, X eyes, bubbles, screen dims to black, "LIGHTS OUT / 30 *minutes* / unconscious", timer to 30 MIN | Stick (info) | Sinks 200 px in 1.9 s, dim to 72% | Downsweep + ding | Timeline completes: 1, 10, 30 minutes. |
| 23 | 61.2-66.4 | 5.2 | "I'd say... Minutes. Yeah. Minutes." | Tier board, cursor drags the tile and drops it in "Minutes" on the word | Tier board | Tile drag with ring click | Click, then thud on the drop | The verdict is physical. |

**Share of time:** clip with no text 24%, text over clip 26%, stick 25%, map 16%, tier 8%.
**Pace:** 23 visuals in 66.4 s = **2.9 s average** (hook 2.2 s). Range 1.0 to 6.0 s. Longest body shot is 5.2 s and it is the board drag, which moves all the time. No clip sits still longer than 4.5 s without a zoom or a text change.
**Stick gags:** 7 shots, 17 s. Every one carries information: a timer bar, a number, an icon, a distance, a label on the word. None is decoration.

---

## B. The rules

### Which tool for which line
1. **A place, a date, or "land/coast changes" = MAP animation. Never a landscape clip.** The map must show it happening: coastline sliding out, land joining, a strait closing, ice growing (see rule 18).
2. **A number or a temperature = big number over a clip of that exact danger** (cold head in water, ice crystals, pack ice). The number lands on the spoken word. If the number changes (0 to -1.8, 0 to -120 m), animate the change (strike-through, counter).
3. **A body reaction or a time-to-die beat (gasp, hands stop, pass out) = stick gag with a timer bar** and the matching number. Use the same bar style in every chapter, so the viewer learns it.
4. **A joke = a stick gag or a one-word text on a matching clip, with a small sound** (e.g. "coast guard (45 minutes away)" + "tok"). Not a boxed card.
5. **A creature, a habitat, a mood image the line names = real AI clip**, full screen, clean, with a slow push. The clip must show the named thing (kelp forest, seals, megalodon). No "something vaguely related".
6. **A danger entering = clip + one fact plate** (EXTINCT plate with date), not a full-screen card.
7. **A verdict = tier board only at the end of a chapter**, tile dragged and dropped on the verdict word. Never an empty board mid-video.
8. **If a line has no picture that proves it, rewrite the line or add a stick gag with a label. Do not add a pretty clip.**

### Stick gags
9. Each gag must contain at least one of: a timer bar with a marker, a number, a labelled icon, a measured distance, a zoom-circle. Check: remove the narration, can you still tell the point? If not, it is filler.
10. Labels and icons arrive on their word (+/- 0.15 s). X marks land 0.3 s after the icon.
11. White line art on near-black, gold hairline accents, the same figure, the same wave line every time. Water line at about y 430-490.
12. No empty boxes or unlabelled rectangles. A box must say what it is ("ICE 2 km").
13. Length 1.4-3.5 s, one idea. A 4-5 s gag needs 2 beats (like the rope gag: throw, then slip).
14. The cold chain (1 min, 10 min, 30 min with the same bar) repeats in every chapter where cold is the danger, and in other chapters its equivalent (heat, thirst, salt).

### Text overlays
15. Three allowed shapes: (a) kicker (Jost caps, tracked) + big number (Cormorant) + gold hairline + italic subline; (b) one italic word/phrase lower third; (c) gold plate for EXTINCT. Fade in 0.5-1.1 s, no bounce.
16. Never repeat the same boxed card. Max 2 identical templates in one chapter. "DRINKABLE? NO" in a dark box 9 times is the failure case. Say drinkable-or-not with a gag or a clip with one italic word.
17. Text sits on a clip fresh for that line, dimmed (dark shade), never blurred. Letterbox bars only on big title moments. No baked-in text from the clip, no logos, no watermark.

### Maps
18. Every map in a chapter shows the ice-age state: **ice sheets visible on land from the first frame or growing**, ocean darker, no ice drawn on water. If the place is far from the ice (Red Sea, Sunda, Carpentaria, Mexico), zoom out so the nearest ice sheet is in frame, or add a small world inset with the ice sheets and a pin. A map with no ice is a wrong map.
19. Show the change: today's coast to -120 m coast, with the **sea-level gauge** counting 0 to -120 m in sync with the words. Show joined land (Britain-France, Siberia-Alaska, New Guinea-Australia), a strait closing (Bosphorus, Bab-el-Mandeb) as an animated event, not a still.
20. Pin ring + place name + date line on the word that says the place. Credits line small. No label collisions.
21. Map length 4.5-6 s. One idea per map.

### Pacing
22. Average shot 2.5-3 s in the body, 2 s in the hook. Max 4.5 s for a clip, 5.5 s for anything that keeps moving. Hard cap: no shot over 6 s.
23. Something new every 1.5 s: a cut, a text beat, a counter step, a gag beat or a zoom jump. A slow push alone does not count after 3 s.
24. Cut on the first word of the line. First change in a new shot within 0.2 s.

### Clip content
25. Right era, right animal: every animal must belong to the time and place the line is about, OR be named in the line (like the megalodon with the EXTINCT stamp in v9). Dinosaurs are welcome when the script talks about them (or in a dinosaur video); they are wrong only when they appear by accident in an Ice Age scene (check silhouettes behind text cards too). No accidental modern objects (boats, cars, lifebuoys, oil rigs, lab gloves, tweezers, modern clothes), no baked-in text or logos or watermarks, no captions in other languages.
26. Animals never pose or face the camera. Side profile, moving, doing something.
27. A clip is accepted only if one look at a frame says "that is the line". Review every clip at 3 frames (start, mid, end) before the build.
28. Each clip is used once per video. Do not stretch a short clip with a frozen last frame.
29. No film look: no grain, vignette, tint or blur.

### Hook
30. Hook (about 33 s): person in danger (0-7 s), a stakes number with a joke (7-13 s), the Ice Age pivot with a map (13-19 s), three promise clips (19-27 s), a stick recap of the rules (27-32 s), hero clip on "Let's find out", **0.5 s black and silence**, then the chapter map. The first number lands at 7 s.

### Sound
31. Hook = strings + taiko + riser, hard stop on the drop. Body = one lo-fi beat that starts on the chapter title thud.
32. SFX on every picture event: number thud, X click, strike scratch + ding, gasp, rope swoosh, stamp thud, tile click and drop thud. Roughly one SFX per 3 s.
33. Ambience under each clip's world (wind, ocean, bubbles, ice). Music ducked about 17-20 dB under voice. About -14 LUFS.

---

### Quality check (owner's rule, 24 Oct 2026)
34. **Check every clip one by one in batches of 50** (and at the end of every batch, even if smaller). Nothing goes into the edit without passing.
    - For each clip, look at frames from the start, middle and end, plus one per second.
    - Compare it with its line in the shot list: does it visibly show what is said? Right era and right animal? No accidental text, logos, modern objects or wrong creatures? Animals moving naturally, not posing? No melting faces, extra limbs or broken water? Correct anatomy close-up (mouths, tongues, teeth, eyes)? Believable scale (animal size vs people, prey, landscape)? Natural motion (no stiff standing, jerky or 'raw' movement; animals that should move actually walk/trot/swim)? Calm, sensible camera move? Weather consistent (snow, rain, wind and waves all moving the same believable direction)? No unrequested animal entering the frame?
    - Give one verdict per clip and write it to `qc.csv` (shot id, verdict, in/out seconds, reason):
      - **KEEP**: the whole clip is good.
      - **TRIM**: only part is good, so note the usable in/out seconds and use only that part (it must still fill the shot; if it is too short, the shot gets a different visual instead).
      - **REDO**: it fails, so write the reason and a fixed prompt, then send it to the retry queue (Wan again, then fal, then vidIQ, per the source order).
    - **Check the start images the same way before they become clips.** A bad image is much cheaper to fix (Z-Image Turbo: about $0.002, so retry freely with a new seed or a fixed prompt) than a bad clip.
    - Report each batch to the owner in one short line: kept / trimmed / redo counts.
    - **Who checks (owner rule, 26 Oct 2026):** a SEPARATE checker, never the helper that made the clips. **Sonnet is the minimum** (Haiku is too weak for motion and anatomy). Quality comes before speed and cost.
    - **Look at 8-10 frames per clip minimum** (not 4), evenly spread, so motion problems show (stiff animals, jerks, odd camera moves, weather direction). For hero shots or unsure cases, look at more.
    - **Owner's final check (owner rule, 26 Oct 2026):** after the helper's check, the helper does all its work first (KEEP, TRIM the bad part off, REDO and remake), then every clip it KEEPs or TRIMs goes to the owner in a labelled review video (number + shot name + KEEP/TRIM; each TRIM is shown in full first, then the part that will be used, so the owner can judge the cut). Nothing goes into the edit until the owner has approved it. Send review videos in batches as clips pass (don't wait for the whole batch). The owner's rejections go straight back into the retry queue with the owner's reason.
    - **Check while generating, not after (owner rule, 26 Oct 2026):** start checking clips and images as soon as the first ones arrive, keep checking the rest as they land, and put every REDO straight back into the job queue so the machines that are already running remake it (no new setup, no idle time). Don't wait for the whole batch to finish.

### Keep the viewer hooked (owner's rule, 24 Oct 2026)
35. **Tease with jokes and striking visuals that fit the era, about every 60-90 s.**
    - **Wow animals of the era**, used as hero shots (vidIQ quality), each tied to a line that names them. Ice Age examples: woolly rhino, cave lion, short-faced bear, sabre-tooth cat (Smilodon), giant ground sloth, glyptodont, giant beaver, dire wolf, Irish elk, Diprotodon, the giant monitor lizard Megalania, Thylacoleo (the "marsupial lion"), walrus and seal colonies, orca pods.
    - **Open loops:** tease something coming up ("and that's not even the scariest thing in this water... we'll get there"), then pay it off with the hero shot.
    - **Out-of-era animals only as a deliberate joke the script names**, for example a megalodon or a dinosaur with the gold EXTINCT plate and a deadpan line ("Good news: not this guy."). Never by accident.
    - **Jokes:** at least one deadpan joke beat per chapter, shown with a stick gag that carries information or a quick visual punchline. Never a filler gag.

### Hooks and retention (from Fossil's top video, owner approved 24 Oct 2026; source: research/fossil-hook-study.md)
Owner's note: Video 01 keeps the approved v9 opening as it is for now. These rules apply to new hooks and to every chapter.
36. **Hook length: 28-35 s, 70-90 words, 14-18 shots.** At least 7 of the hook's sentences end with a question mark; none after the promise line.
37. **Wow density in the hook: a named wow animal (or striking place) on screen at least every 4 s**, i.e. at least 7 wow shots in the first 30 s. First wow at second 1-2 (not after the first spoken sentence).
38. **Hook order is fixed:** you-are-the-person (0-3 s), one central question (by 8 s), 3-4 preview questions each with its own creature or place (8-21 s), the rule line "no X, no Y" (21-27 s), "Let's find out." on the biggest image (27-31 s), then 0.5-2 s of silence.
39. **Each preview question names a different flavour of danger** (cold, predator, salt, ice, thirst). No two preview questions about the same threat.
40. **The hook has exactly one number, and it lands by second 12.** More numbers wait for the body.
41. **No joke inside the hook. First joke 8-15 s after "Let's find out."** (Fossil: 12 s.) Check the joke is deadpan: understatement, no "so... small win".
42. **Tonal drop:** hook music is cinematic (riser from 0:23, hit on the promise). It cuts to near-silence for 0.5-2 s and the lo-fi beat starts on the chapter title. The voice becomes relaxed on the first line ("Okay, so the first ocean is ...").
43. **The empty tier board shows for 4-8 s within 15 s of the drop.** It is the main open loop; the verdict vocabulary (Minutes, Hours...) is said out loud once.
44. **Plant-and-pay:** every hook wow animal that is not a joke must come back later in a chapter, named, within the video. List them in the shot list (Planted at X, paid at Y). Check: no hook creature is orphaned.
45. **Wow cadence after the hook: one wow shot (hero creature, huge place, or surprising picture) at least every 30 s in the first 3 minutes.** Longest gap 40 s. Rule 35 (60-90 s hero shots) stays for the whole video.
46. **Joke cadence: at least 5 jokes (verbal or visual) in minutes 0-3, none closer than 12 s apart.** Mix at least 3 types: deadpan line, stick gag, one-word asterisk/lower third, verdict-click.
47. **Relief then catch:** in each chapter, 2-3 pieces of good news in a row, then the catch in the last clause, voice slows on it. First chapter must have one by 1:30. Check: the last 7 words of the turn carry the bad news.
48. **Body translation: every key number gets one sentence about your body or the animal's** (e.g. oxygen = top of Everest; here: cold = "you can't hold a rope"). One per chapter, never a paragraph of scenery.
49. **Callback killer:** the thing that kills you in a chapter should be a number said earlier in that same chapter (Fossil: oxygen at 1:17, kills you at 2:24). Check: in each chapter the verdict reason was stated at least 20 s before.
50. **Chapter 1 pace: first chapter must be 60-90 s and end on the tier drop by 2:30.** A 20-30 s throwaway joke chapter is allowed only as chapter 1 (Fossil: Precambrian, 30 s). Name-only chapter openers ("The Southern Ocean.") with no bridge sentence.
51. **Honest hedge once per chapter** ("probably", "I don't even know", "scientists argue") followed by a committed verdict. Never a hedge as the last word.
52. **Title cards: name + date + whoosh. Maps: place and date. Every map has the ice (rule 18).** Check that the first map is on screen by 0:40 after the drop, not later.

### More retention rules (from Fossil's orcas video, owner approved 25 Oct 2026; source: research/fossil-hook-study-2.md)
53. **Two worlds, one hero.** Tag every shot HERO (the person or animal being tested, for us the swimmer) or WORLD (place, threat, number). A HERO shot must come back **at least every 30 s** in the body (Fossil 2: 1:19, 1:37, 2:25, 2:51). Check: list the HERO shot times for each chapter; no gap over 30 s.
54. **Constant ruler.** Every chapter's main threat gets **exactly one comparison sentence** to the hero (size, weight, speed or bite, e.g. "a third of the size of..." / "as long as a car") in the same line that names it, **plus one scale picture** (stick figure beside the animal, with metres or feet on it). Check: one sentence and one scale picture per chapter.
55. **Count the problems out loud.** In each chapter the voice says "one problem... a second problem" (his gap: 33 s) and later says which one decides ("the food problem alone finishes the round", 1:44). The deciding reason is stated 15-35 s before the verdict. This sharpens rule 49. Check: both phrases exist in the script, and the second problem comes within 35 s of the first.
56. **Mid-video reversal.** Put one chapter at **55-65% of the video** where the hero really can lose and the verdict is worse than the viewer expected. Say it once ("the first place where something here can actually kill you"). Check the timestamp and the line.
57. **One flagged unpopular verdict per video.** Say "I'm going to get comments for this" or similar 8-15 s before the tile drops; give the reason; then drop the tile and click. End with "Do you agree? Tell me where you would put it" in the last 15 s. Check: exactly one flagged verdict, and a closing question.
58. **Roadmap board.** When the empty board appears (rule 43), **all chapter tiles must be visible on it with names** (his: 11 tiles for 11 stops). Check: tile count equals chapter count.
59. **Claim-hook (type B), for animal videos only.** Allowed shape if a future video is about an animal rather than "you": claim + 3 proofs with real or clean footage (0-13 s) -> one question (by 21 s) -> group size and rules with ONE number (by 40 s) -> board with all tiles (by 45 s) -> 1-2 s black -> chapter 1 (by 55 s). Keep rule 36-43 (type A) for "you" videos. Video 01 stays type A.
60. **Planned stills (owner approved 27 Oct 2026, after the Video 02 draft).** Plan **15-20% of the creature/scene shots as still images with motion** from the start, not only as a fallback. Every still moves: a slow push or pull, a pan across the frame, or a light effect (drifting haze, water shimmer, a light sweep). Use them for: (a) wide establishing scenes (a lake, a valley, a herd far away), (b) shots the video model gets wrong (walking, limbs, many animals, fights), (c) a calm beat between fast cuts. Each still holds 2.5-4 s, never more than 2 stills in a row, and each image still goes through the image QC (rule 34). Check: count the stills in the shot list (15-20% of creature/scene shots), and confirm none is static.
61. **No visible repeats (owner, 28 Oct 2026).** Clips from the same shoot (same creator, same place, e.g. Pixabay 173059/173061, 83831/83832, 13022/13024) count as ONE clip. One clip or shoot appears at most twice in a video, never in two shots in a row, and its two uses are at least 3 minutes apart. Real footage must be 1080p or better. Check: a script lists every source with its timestamps and flags any shoot used 3+ times or twice within 3 minutes.
62. **Line and picture must match (owner, 28 Oct 2026).** If the voice names an animal ("giant fish"), the picture shows that animal, or a size chart of it; never a stand-in animal (a turtle for "giant fish").
63. **"Okay" at most twice per script (owner, 28 Oct 2026).** Vary the chapter openers ("Next stop:", "Now,", a straight date and place) instead of starting every river with "Okay,". Check: count "okay" in the script before recording.

### Style review rules (owner approved 29 Oct 2026; sources: research/style_review/04_final_verdict.md, 07_btb_adopt_verdict.md, research/beyondtheblue-deep-study.md)
64. **Big verdict word.** On the verdict word the tier word is the biggest text on screen (about 12-13% of frame height), Cormorant, warm white with a gold underline, over a dark vignette, for 1.5-2 s; then the board. Fast entrance is allowed here only (exception to rule 15). Template: `tier_board` drop, `verdict` param.
65. **Verdict sting.** Full sting (music dips out 0.8 s before the word, reversed-sweep riser, deep hit on the word, music back after) on at most 4 verdicts per video: the first river, the reversal (rule 56), the biggest-threat chapter and the last one. Every other verdict gets the deep hit only, so it never becomes a formula. Template: `sting: "full" | "thud"`; mix cues `duck`, `riser`, `vhit`.
66. **Gold hand-drawn circle** (#C9A45C, draws in 0.4 s, marker sound) to point at the one detail the line names (nostrils, a tooth, our croc in a crowd). Max 1 per chapter. Never red in-video: red stays in the thumbnail and the "Wiped out" tier colour only.
67. **Reveal-order size comparisons.** Known thing first (our croc or the human), then the giant slides in on its name, then the gold measuring bracket, then the number last. No chart shows everything at once.
68. **"Plan fails" beat in each chapter.** 2-3 beats: the hero tries its special move (salt glands, death roll, ambush), it doesn't work here, then why. Written into the script, never added afterwards. Chapters link by cause ("and that is exactly what kills it in the next river").
69. **The hero acts.** The line-art croc / stick kit acts out the plan in graphics (max 2 gags per chapter, never the same rig twice in a row). The caption is our italic lower third, not speech bubbles. Real clips keep the real species.
70. **Fixed sound per graphic event.** Bracket = tape tick, circle = marker, tile drop = click + deep hit, title = whoosh + thud, counter = tok. Same event, same sound, across the whole video.
71. **Structure caps.** Rules section 20 s or less, over the roadmap board; first river by about 0:40; first verdict by 1:45; a type-B modern-footage opener at most about 8 s and only the sharpest 1080p clips; no dark card in the hook except one deliberate punch card.
72. **No empty frames, no dark-card runs.** A card shows its text from its first frame. At most 2 text cards in a row; put numbers over a clip that matches the line when one exists. Labels at least 3.5% of frame height, creature names at least 5%. Static map holds 4.5 s or less. Check: 640x360 contact sheet before render.
73. **Line-and-era gate for ALL footage** (AI, stock, stills): no grass, birds, flowers, fences, farms, boats or modern people before their time; the named species only. One contact sheet per chapter, checked before render.
74. **Evidence cards.** One or two real fossil or trace photos per video in a thin framed card (Wikimedia CC0 / CC BY / CC BY-SA only, never NC), credit bottom-left and in the description.
75. **VS card** for a head-to-head: 3 words a side in Jost, gold "vs", no bell or record scratch. Can replace a size chart.
76. **Drawn mechanisms.** When the line explains something invisible (can't digest, low oxygen, heat stroke), draw it moving in line-art (slowing heartbeat, bubbles stopping) instead of a static number card.
77. **One echo word per chapter.** The chapter's key word comes back as our italic lower third (rule-15 fade), max once per chapter, never on a number shot.
78. **Two music states.** The main bed, and a "reflective" pad state for the reversal chapter and the outro. Nothing more.
79. **Shadow-pass bridges** (max 3 per video): a dark silhouette of the next creature passes over the end of one chapter to start the next, only where the chapters link by cause.
80. **Ending.** The outro recaps the deciding reason in one continuous shot, then ends on the finished board (no separate end card); the board holds 10 s for the YouTube end-screen elements.
81. **Not copied from Beyond The Blue:** their engraving thumbnails, flat-vector world, red accents, fake human host, two-tone kinetic captions, freeze-frame slams, false-relief hook jokes, gore, or reusing a whole set within 6 weeks.

### Production checklist: no repeat of Video 01/02 errors (owner approved 30 Oct 2026)
**Before the script is locked**
82. **One fact sheet.** Every number said or shown comes from one fact sheet per video (source + value). Graphics read their numbers from it; the hook and the chapters can never disagree (V02: 16,000 vs 16,414 N).
83. **Count before recording.** "Okay" max 2 (rule 63), no repeated chapter openers. Checked by script before the voice is made.
84. **Thumbnail planned with the script.** The thumbnail's picture and text are chosen while writing, and each promise is in the video, ideally in the first 30 s (V01: a shark thumbnail for a video that says "Not a shark"). One 3-agent round (ideas, critique, verdict), locked style (HOUSE_STYLE), phone-size check, then the owner picks.

**Before any media is made or bought**
85. **Real footage first.** For every shot of a living animal or place, the stock list (Vecteezy Pro, Pixabay) is made first. AI only for prehistoric animals and places, or what stock really can't show. Never pay for an AI clip that stock could replace.
86. **One stock list, one download.** All stock picks for the whole video go to the owner in one list (one PDF), downloaded once, licences logged once. No later swap rounds. Real footage must be genuine (not AI-made stock), 1080p or better, wild (no zoo fences, walls, keepers, farm pens).
87. **One test per tricky species.** When an animal must be a specific species (leopard seal, phytosaur nostrils), make ONE test image or clip and get the owner's OK before the batch. If the video model drifts, use a still with motion instead of paying for redos.
88. **Spend gate.** State the cost before every paid job. Only one vidIQ job at a time (two agents at once burned extra credits). Keep at least 100 vidIQ credits. Rented pods self-terminate; check none are left running after each job.

**Before the first render**
89. **Shot-list gate (all four must pass):** (a) line-and-era contact sheet, every shot against its line (rules 62, 73); (b) repeat check script, same clip or shoot max 2 uses, never back to back, 3 min apart (rule 61); (c) every source 1080p+; (d) no placeholders left. No render until all pass.
90. **Hook first.** Build the hook (sharpest clips, its music, its sound hits) before the chapters, and get the owner's one approval on it. The chapters are built after.
91. **Cards and pauses.** No empty frames, max 2 text cards in a row (rule 72), no silence after board drops.

**Reviews and renders**
92. **Short review reels.** The owner reviews short reels of the new or changed moments (like the V02 95 s fix reel), plus ONE full draft at the end. Target: one review round.
93. **Renders on rented machines** for the full draft and the 1080p final (chapters cached; a restart loses only one chapter). Keep the session disk clean as you go: delete stale caches, old reels and extracted zips after each step, so a render never dies on a full disk.
94. **Commit after every step** so a container restart loses nothing.

### Animation and sound design (owner approved and LOCKED 30 Oct 2026; sources: research/depththeory-spermwhale-study.md s.4-6, research/depththeory-squid-vs-whale.md, templates/tests_anim/ tests 1-7, research/style_review/14-16)
95. **Animation is a third picture source**, for what no camera can film: "you" in the scene, the hero's plan failing, inside the body (heat, heart, lungs), how a hunt works, "what would you do?" choices, size and number comparisons, history, jokes. Every animation explains ONE thing that the line says; no decoration.
96. **Our look (locked):** gold line-art and warm-white type (Cormorant + Jost) on a **dark ink background whose colour matches the video's world** (owner, 30 Oct 2026: V03 tiger/jungle = deep green-ink #173126 -> #040806 radial; V02 crocodile rivers = warm river-mud umber, set per video with the chapter key `anim_theme` {hue, sat}, which retints every green of the animation blocks) with a vignette; nature scenes are layered greens (far = lighter and hazier, near = darker); the hero animal in its true colours (tiger: amber body, dark stripes, thin warm rim; `templates/tests_anim/tiger_fill.png`, PhyloPic CC0); gold #C9A45C is the only pointing colour; red only in the thumbnail and the "Wiped out" tier; never deep blue; never a flat-vector copy of Depth Theory / Beyond The Blue.
97. **People (locked):** "you" is always our **simple stick figure** (blocks/common.py `fig`). Supporting characters = the same figure + **ONE prop** that says the role (scientist: lab coat + glasses + clipboard; hunter: pith helmet + rifle; local worker: one costume item; child: smaller figure). **Modes** for ideas: backlit silhouette in a warm light disc; **gold X-ray** cutaway (organ glows, scan line); crowds as tiny repeated figures. Reference: `templates/tests_anim/out/test6_cast.mp4`.
98. **Motion grammar (locked):** elements **snap in in 0.3-0.5 s** (strong ease-out), then the scene **drifts slowly** (push/pan) while small things keep changing; something new every 1-3 s; the picture moves in at least 80 % of seconds; nothing fully still (sway, particles, pulses, blinks). Count-ups: anticipation, then ~1.3-1.5 s count, **land with a short flash + an expanding gold ring + a deep hit**. Joke or metaphor lines become a 3-6 s **mini scene**. Lists ("what would you do?") are a spine: current row gets a gold box, finished rows a gold strike-through. Rich scenes use 4-6 parallax layers, light rays, mist, particles, a light source (torch/sun).
99. **Sound design in four layers (locked):** (1) **environment** bed that never stops and changes per place (rain, insects, wind, water; ElevenLabs sound effects); (2) **things** (footsteps, rustles, the animal's real sounds, branches, birds); (3) **mood** (our own low music bed that never stops, heartbeat, deep boom on reveals; max 4 full stings per rule 65); (4) **graphics** (tick = counter, held beep = lock-on, thud = stamp/land, click = list item, scratch = strike-through, marker = circle, soft whoosh = scene build). Real recordings (ElevenLabs) for animals and nature; synthesised sounds only for graphics.
100. **Sound density and mix (locked):** about **16 sound effects per minute on average, in bursts** on the key lines, calmer minutes between; **one signature sound** per video planted in the hook as something "you" feel or hear, back at every related beat, paid off out loud once; voice about **11-12 dB above** the sound design (sidechain duck), the bed rises a little in voice pauses, no silence after board drops; final -14 LUFS.
101. **Picture-source mix for a new video (owner approved for V03, 30 Oct 2026):** animation ~25 %, real ~20 %, other AI ~20 %, vidIQ hero ~12 %, board and cards ~15 %, maps ~5 %, evidence cards ~3 % (research/style_review/16_v03_retention_verdict.md). Hard checks: max ~20 s of one source in a row, the hero animal in at most 40 % of shots, max 2 text cards in a row, the hero back at least every 30 s.
