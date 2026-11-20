# Critique of the hook, v1 (0:00-0:53) - Samuel B. Roberts

Method: 54 frames (1 per second, 0-53 s) in one sheet, plus a read of `NARRATION_v1.txt`, `chapter/c01.json`,
`build/beats.py` B["c01"], `build/words.json` (word times), CLAUDE.md, STYLE_LOCK section 3, `footage/FOOTAGE_LIST.md`,
the 480i film contact sheets (nara_77765, nara_76144). No repo file was edited except this report.

## 1. Verdict in plain English

The owner is right. The hook is a slideshow of mostly calm, grey, static ships and an abyss, and the real battle only shows up in
the back half. The 53 s do not feel like "a small ship charged battleships"; they feel like a documentary about mud.

What is weak, shot by shot (times from the render):

1. **0:00-3:77, the opening map.** The strongest slot in the video is a slow push on a wide, dark, calm Pacific map. Frames at 0, 1
   and 2 s are almost identical. Nothing moves except the camera, nothing is at stake, and the only hard element (a red label
   "NEARLY 23,000 FT DOWN") is text on a still. It satisfies "first frame is a map" and nothing else.
2. **3.8-8.7 s, the "small American warship ... charged a fleet of battleships" lines (the promise, spoken by 6-8 s).**
   - `cm_NH_90603` is a calm 1920 px profile of the Roberts off Boston, June 1944: grey, still, harbour-calm, low-res. "Charged"
     is shown by a ship standing still.
   - `cm_80_G_46989` ("the Japanese fleet") is, in frames 6-8 s, **an empty horizon**: cloud, sea, a few specks. This breaks the
     owner rule "no shot on an empty horizon" and proves nothing. This is the worst shot in the hook: it carries the title promise
     and shows nothing.
3. **8.7-22.2 s, 13.5 s of sea floor.** Three NOAA clips and two cards, all the same olive/brown nodule field. The gauge bars
   (11.4 s) are fine as a graphic but sit on the same dim murky film. The Kilimanjaro card (17.5-22.2 s, 4.7 s) is white text on a
   **dark brown, dim, near-static** background (against the "cards must read bright" rule, and over the 4 s change rule: one
   frame for 4.7 s with only the text arriving). It is 42 percent of the hook, it has no ship, no battle, no people, no stakes.
   The viewer has not seen a single shot of the battle in 22 s.
4. **22.2-35.3 s, the photo run.** Five stills, 2.8-3.5 s each, with slow flat pushes ("push": null, no depth parallax, no subject
   aim). The labels are honest but the viewer reads the sheet as "random grey ships":
   Heermann smoke (a different ship), Butler sister ship (twice in a row: 382868 then L45 Dennis), then sailors, then splashes.
   Only the sailors (270514) and the splashes (288886) are real battle images; 288886 arrives at 31.9 s, which is when the words
   say "sent straight at the biggest guns", the first time the picture pays the promise. That is half-way through the hook.
5. **39.4 s, "Her crew called her the Sammy B"** is on `cm_L45_74_08_01`, USS Dennis. It is a different ship under the nickname of this one.
6. **44.0 s, "her captain told them not to expect to survive"** finally gets the strongest picture in the hook, the St. Lo
   explosion (270516). It appears at 0:44, after the viewer has probably clicked away. The two best assets (explosion, shell
   splashes) are in the last third; the weakest (abyss, empty horizon, harbour profile) are at the front.
7. **Motion.** Count the moving things in the sheet: the map, the NOAA film (slow crawl), a bar chart. Every photo is a flat
   Ken Burns. No parallax, no particle, no camera shake, no impact, no 'something new every 1.5-4 s' beyond cut rhythm. SFX is
   off in the whole hook (`sfx: false` on 15 of 16 shots in c01.json; beats.py wants IMP/EXPL on splashes and the explosion but they
   are not active in the segment list).
8. **The structure** is "depth facts first, the battle later". The narration is written that way and cannot change, so the picture
   must carry the second story (the battle) under the depth words. Right now it does not.

Rules actually broken (CLAUDE.md / STYLE_LOCK 3): no shot on an empty horizon (s03); every shot proves the spoken words (s03, s02,
Dennis for "Sammy B"); no dark text cards (s07 card on dim brown); a wow early then every 30 s (first real wow: 0:44); photos aim at
the subject (all pushes are `null`).

## 2. What to build instead (same narration, same timings)

Core idea: **two layers, one story.** The words about depth get a single vertical "descent" graphic whose top is the real 25 Oct
1944 battle (surface) and whose bottom is the 1080p NOAA sea floor. The words about the ship and the fight get the 3840 px
battle photos in depth-parallax, sharpest first. Every shot starts on a subject, the explosion/splashes are pulled forward to
where the words allow, and the two best assets are used twice in the hook range (once early flash, once on their words) only if the
3-minute rule allows (it does not, so each is used once; see reuse notes).

### Opening and the "first frame is a map" rule
- **Recommended: keep the map, change what it does.** The rule (CLAUDE.md "first frame is a map", battle-maps 1a: "map with
  units ALREADY MOVING") is met by frame 0 being a map. It does not say the map must be slow. Make frame 0 a *violent* map:
  already mid-zoom, hard push (whoosh), a depth ticker counting 0 -> 22,600 FT that **lands on the word "feet" (1.9 s)** with a
  hit, red-orange ring pulsing on the Samar spot, then at 2.4 s the map **punches through the surface** (zoom-whoosh) and the
  water-column graphic starts at 3.77 s. That is three beats in 3.77 s instead of one, it proves the spoken words (feet under
  the Philippine Sea), and the number lands on its spoken word.
- **Hybrid to offer the owner (needs his OK, a small exception):** the voice starts at 0.35 s. Put a 0.3-0.5 s cold frame
  before it: map with the St. Lo explosion (`cm_80_G_270516`) as a hot, glowing flash inside the Samar spot, then the map
  zoom. It breaks "frame 0 is only a map" slightly and does not prove the words, so I would **not** do it; the plain map +
  ticker is the compliant opening, and it is engaging if it moves fast.
- **Argument if the owner insists on opening on a photo:** the rule exists because battle-map channels get their identity from the
  map; this channel's identity is archive photos plus maps. Defensible, but the first 3 s are about depth ("23,000 feet under
  the sea"), and no battle photo proves that. The best honest "engaging" version is a **photo that becomes the map**: a 4 K splash
  photo (288886, dimmed) as the sea surface, the camera pushing down through its water line into the dark map/water column. That
  is the same as the recommended opening with the surface photo visible for 0.4 s at frame 0 behind the map tint. I would try
  this as a test frame; if it reads as a map first, it is compliant.

### Shot-by-shot plan
Word times from `words.json`. Hard cap 6 s per shot; target 2-3 s. "Parallax" = 2.5D depth move (`focus.py` subject point + manual
fix, crosshair sheet check, never centre). Photo stems from `footage/src/photos`. ILLUSTRATIVE tags stay.

| # | time | narration | show | why | motion |
|---|---|---|---|---|---|
| 1 | 0.00-1.9 | "Almost twenty-three thousand feet" | Philippine Sea map (`m_c01_open`, re-cut) | place + number | frame 0 already mid-push, hard zoom toward Samar; ticker 0 -> 22,600 FT lands on "feet" (1.9) with hit; whoosh |
| 2 | 1.9-3.77 | "under the Philippine Sea," | same map, label "PHILIPPINE SEA" + red ring "WRECK SITE · APPROX." | place on its word | continued dive, then punch through the surface (whoosh, cut at 3.77) |
| 3 | 3.77-5.8 | "there is a small American warship" | `cm_80_G_382868` John C. Butler (5346 px, sharp, camouflaged, bow wave) tagged ILLUSTRATIVE | sharpest "small warship" picture, a real DE at speed; no 480p | parallax push toward the bow and 5-inch gun, slight handheld drift |
| 4 | 5.8-7.3 | "that once charged a fleet" | `cm_80_G_378525` Yamato + heavy cruiser, Samar | the enemy, in the promise sentence (replaces the empty-horizon 46989; this Yamato photo is unused elsewhere before c05) | parallax push to the Yamato bow/smoke, red ring on Yamato; whoosh |
| 5 | 7.3-8.8 | "of battleships." | `cm_80_G_46989` **tight crop on the line of ships** (focus crosshair on the ship cluster, no cloud band at frame top) or, if the crop is still sparse, `cm_80_G_270511` burning carrier | must show the fleet, not sky | fast push to the subject; if used, 4 red hull markers pop on the horizon ships on "battle-" |
| 6 | 8.8-11.5 | "She is the deepest shipwreck ever found." | **Descent graphic:** top = 288886 shell splashes (dim, the surface of the battle), camera drops through the water column to the NOAA 1080p floor (`noaa_29866` or `noaa_31374`, brighter clip) | links the battle to the depth; proves "deepest" | vertical dive, ticker; stamp "DEEPEST SHIPWRECK EVER FOUND" slams on "deepest" (hit) |
| 7 | 11.5-14.3 | "Nearly twice as deep as the Titanic." | same column: Titanic marker at 12,500 ft passes at "Titanic" (13.5), Roberts marker at 22,600 on "twice" | number on its word | existing `anim_gauge` data, rebuilt vertical over the moving NOAA bg (bright) |
| 8 | 14.4-17.6 | "Stand Mount Kilimanjaro on the sea floor beside her" | mountain silhouette (Kilimanjaro 19,341 ft) rises from the floor into the column | proves the picture of the sentence | rise animation on "Stand" (14.5); NOAA floor film behind, brightened |
| 9 | 17.6-22.2 | "and its summit would still be about three thousand feet under the waves." | summit flag, line from summit to the surface counts 3,000 FT on "three thousand" (19.5-20.5), the splash photo at the top shakes on "waves" (21.2) | replaces the dark Kilimanjaro text card | no plain text card; background is the moving column + brighter NOAA |
| 10 | 22.4-25.0 | "She was one of the smallest warships in the battle." | `cm_80_G_288885` Heermann + a Butler-class DE laying smoke (5580 px) | a real small escort in the battle (ILLUSTRATIVE for Roberts) | parallax push to the DE at the right, not the centre; smoke drift |
| 11 | 25.2-26.8 | "A destroyer escort," | `cm_L45_74_08_01` USS Dennis, sister DE (5299 px) | shows what a DE is | push to bridge/guns |
| 12 | 26.8-28.6 | "built for chasing submarines." | `cm_80_G_295001` USS Raymond (DE-341) refuelling, or `cm_80_G_264041` | a DE at work | slow parallax; whoosh on cut |
| 13 | 28.7-30.3 | "And on one October morning in nineteen forty-four," | `cm_80_G_270514` sailors on the flight deck watch the smoke and splashes, 25 Oct 1944 | a real 25 Oct 1944 picture, first human beat | parallax toward the smoke on the right |
| 14 | 30.3-31.8 | (same sentence, "nineteen forty-four") | date stamp "25 OCT 1944" slams on a dimmed `cm_80_G_270511` burning escort carrier | a date on a moving, bright background (no black card) | push into the smoke column |
| 15 | 31.9-33.6 | "she was sent straight at the biggest guns" | `cm_80_G_288886` three shell splashes, 5568 px | the biggest wow so far, on its words | parallax push to the splash columns; IMP sfx on "biggest" (33.4) |
| 16 | 33.6-35.3 | "in the world." | the Yamato 18-inch guns: `cm_Kongo_on_sea_trials_1936` or a tight Yamato crop (`cm_80_G_48888` is used in c02: avoid) | the biggest guns | slow reveal on the barrels |
| 17 | 35.4-38.4 | "This is the USS Samuel B. Roberts." | `cm_NH_96011` (3840 px, Oct 1944, the only sharp Roberts photo) + lower third on "Samuel" | first time the viewer sees the hero, sharp and at speed | parallax push toward the bridge, bow wave; hit on "Roberts" (38.0) |
| 18 | 39.4-41.3 | "Her crew called her the Sammy B." | `cm_NH_90603` Roberts (1920 px, her again, not Dennis) or `cm_Launch...` (3840 px) | the right ship under the nickname | stamp "SAMMY B." slams on "Sammy" (40.5) |
| 19 | 41.6-43.8 | "And that morning, her captain told them" | `cm_80_G_270511` burning escort carrier is used up at #14: use `cm_80_G_288881` kamikaze on White Plains instead | the morning's danger, no repeat | dive-bomb parallax, slow push |
| 20 | 43.8-45.8 | "not to expect to survive." | `cm_80_G_270516` St. Lo explosion (5600 px) | the strongest picture in the hook, on the stakes word | parallax into the fireball, impact + shake on "expect" (44.0) |
| 21 | 45.9-47.6 | "So how did a ship this small" | `cm_80_G_288885` or the Butler plan crop: small ship against a scale | "small" | quick push, then the 306-ft marker beside the 22,600-ft marker |
| 22 | 47.6-49.0 | "end up this deep?" | `noaa_29866` 1080p floor, bright, with a depth ticker counting 0 -> 22,600 FT | reversal visual | fast descent; hit on "deep" (48.3) |
| 23 | 49.1-51.2 | "And what did the cameras find," | trench map, dark sea east of Samar, sonar rings expand from the "?" | the question; cameras | rings pulse 2 per second, slow descent |
| 24 | 51.2-53.3 | "when someone finally reached her?" | NOAA ROV light cone on the floor (1080p) with a "2022" stamp or the map "?" pulsing; end hard on "?" | closing question hand-off to "Start with the place" | light sweeps, "?" pulses; cut to c02 map |

Count: 24 shots in 53 s = a new image every 2.2 s average, none over 3.2 s; first real battle image at 7 s (4, 5), the shell
splashes at 31.9 s on their words, the explosion at 44 s on "survive". A wow at about 5.8, 8.8 (dive), 14.5 (mountain rising),
28.7, 33.4, 44.0: roughly every 8-15 s instead of one at 44 s. Some photos could still be swapped for variety; the crosshair sheet
decides.

### Reuse and rights checks before building
- Reuse (max 2, 3+ min apart): 270516 is in c05, 288886 in c04, 288881 in c04, 288885 in c01 and elsewhere, 378525 in c05,
  48888 in c02 (about 1:50, too close to 0:06, so I kept it out of the hook), L42_09_06_03 already has two uses. Confirm with `build/shotlist_report.md` after the
  re-plan; 288881 and 270511 each end up on their second use only if they appear again.
- `cm_NH_96011` appears at #17 and later in the video: fine (>3 min apart if the later use is). Do not also use it at 3.77 s.
- The 2022 wreck footage stays out. The last shot uses NOAA's own 1080p public-domain ROV footage, tagged ILLUSTRATIVE.
- SFX roles stay as locked (impact -10 on splashes, explosion -7 on St. Lo, whoosh -15 on camera moves only; no hull groan).

### Which 480i film is worth using despite "sharpest only"
**None in the hook.** I checked `nara_77765` (the only real Taffy 3 reel): 1:44-1:50 shows white splash columns around a distant
carrier, but the ship is a few pixels high, grey on grey, and the sheet shows a flat horizon in most of it. It is worse than the
5568 px still `cm_80_G_288886`, and it also breaks the "never 480p in the hook" rule. `nara_77732` (Sangamon, AA fire and planes) is
480i grey and a different task unit. If the owner wants film motion in the battle beat anyway, the one candidate is
**`nara_77765` 1:44.5-1:46.0, 1.5 s only, cropped tight on the splash columns, as shot 15b between 288886 and the Yamato guns,
with an on-screen "NARA film, 480i" tag**, but my recommendation is no: parallax + impact SFX on the 4K stills gives more
energy. The sharp motion that does exist (`nara_76144`, 35 mm Kitkun Bay deck, May 1944) does not prove any hook words; keep it
for c02.

### Production notes
- New template needed: vertical descent graphic (surface photo -> water column -> NOAA floor, markers for Titanic and the Roberts,
  a mountain that rises). Fallback with existing parts: `anim_gauge` bars over bright NOAA film plus a photo-to-sea-floor crossfade
  push (clip `deep_field` brightened); do not fall back to a text card.
- Parallax: run `focus.py` on the 10 hook photos, add the manual fix file, and check a crosshair sheet before segments.
- Re-time against `words.json`; use anchor phrases above. After the rebuild, make a 1-fps sheet for 0-53 s and check:
  no frame on empty horizon, no dark card, subject in frame at the first frame of each shot.
