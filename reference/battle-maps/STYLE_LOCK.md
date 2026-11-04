# STYLE LOCK: the channel's fixed look, sound and music (owner-approved on Goose Green, 2026-09-29)

**Owner: "I love this video. Lock it in. Don't reinvent the wheel every time."**
Every new video uses EXACTLY what is below. Don't search for new music or sounds, don't restyle, and don't re-test
anything on this page. Only NEW ideas go through "test before applying" (snapshots / 1-min clip, then owner approval).
Everything here is already the default in `goosegreen/` (copy it; see HANDOVER 0b step 1), so doing nothing = locked style.

## 0. The reference clip (hear and see it before any new video)
`reference/style-reference-30s.mp4` (owner-approved 2026-09-30): Goose Green move 3, mixed with the locked sounds and levels:
artillery impacts, an Argentine jet + turboprop shot down by AA, helicopters, then the **Harrier bombing run with the camera
shake**. Every new video must sound and look like this. Before the final assemble, build a test clip of the new video's
busiest 30 s (`make_clip.py SCENE --from P --to P`) and compare it with this reference: same boom-on-impact, same aircraft
sounds, same shake (music is now quieter: 0.08, section 5). If it differs, fix the new video, never the reference.
Rebuild recipe: `python3 tools/make_clip.py move3 --from move3-1 --to move3-5`, then cut 8.5-29.5 s + 87.5-96.5 s.

## 0b. THE COMPLETE REFERENCE VIDEO (LOCKED, owner 2026-10-10: "perfect, make sure this style is locked"): Rokossovsky #8
The finished Rokossovsky video is the channel's locked look + sound, end to end. Every new video copies it.
- **Watch first:** `reference/style-reference-rokossovsky-v8.mp4` (~1:37: wide option-1 overview with the invasion arrows and a bomb run,
  a tank ambush close-up, the night counter-barrage at Kursk, the bombing of the Bobruisk pocket, projector-frame archive film) and
  `reference/hook-reference-rokossovsky-v2.mp4` (the locked hook, section 1a). Final master: https://gofile.io/d/nWvp2ksX (15:29).
- **Skeleton to copy for every new video: `rokossovsky/`** (lib/, tools/, vendor/, assets/fonts, assets/grain.png, assets/media/sfx/,
  music, flags, emblem). It has every fix: hook lock, sound sync (`sfx_cues.py` reads the current timing), voice-A mix
  (`voice_owner.wav`), `make_clip.py` with voice A, archive builder, thumbnail compositor, publishing guide.
- **What is locked in it (all from sections 1a-5; do exactly this):**
  - Maps: HD dark relief (`bake.py` then `bake_hd.py` -> use `<map>_hd_ref`), 1941-44 names, big towns only, living map, both period
    flags on every map shot, emblem only on German land and never fading, legend top-centre.
  - Option 1 territory (multiply `_mx` control overlays, one per date, 1 s cross-fade) on wide shots; option 2 glowing two-colour fronts
    (`K.front`, **width 15, glow 0.47**, never thinner) on close-up battles; one wide shot -> push-in -> close-up -> zoom-out per move.
  - Units: silhouette counters with flag chips + size marks; commander badges with the REAL licensed photo (initials only if none);
    Stalin-type figures as text cards, never a likeness.
  - Action: `K.gun` -> arc -> `K.impact` (boom on impact, default shake); `K.bombRun` with glowing `c47g` planes (few, spaced, they
    leave); night beats with `K.night`; stamps (hit + shake), counters (ticks), fire sacks, rings.
  - Every move ends: casualty card (the OLD clean `K.casualties` card from `lib/fx.js`, real numbers only; owner 2026-10-29: NOT the Meade/Sherman-style ranges card) or a RESULT card when no reliable figure exists, then the
    method card that adds one line per move.
  - Archive: Netflix look (headline card, 3D-depth photos, projector-frame film, headline date cards), licensed only: US government film
    (Signal Corps, Capra "Why We Fight"), NARA CC0, Commons CC BY / CC BY-SA / PD stills with credits. Never untagged uploads.
    **ARCHIVE LENGTH (owner 2026-10-29, Sherman #13 review): moderate and quick.** The archive LOOK is untouchable (never restyle it);
    only the amount is set: the background block after the hook as now, plus at most 3 short blocks of ~10 s (one where each move
    ends), cuts every 2.5-3 s, about 30 s of archive in total besides the background block. Long archive stretches lose viewers.
    **GROUND ABOUT TO BE LOST (owner 2026-10-29, test E2 approved):** before a front moves, the ground that will change hands first
    turns PALER (its territory layer fades to 40 % over ~1.3 s on the narration cue), then cross-fades to the winner's colour over ~1 s
    as the front moves. Never stronger/more saturated colour to show a loss. Layers: `sherman/tools/make_loss_layers.py`; scene
    pattern: `sherman/scenes-src/test-E2-lose.js` (`lay` / `loss` helpers).
    **TERRITORY TONED DOWN (owner 2026-10-29, test E1 approved):** with the lifted maps, every multiply territory layer gets
    `filter: saturate(0.8)` (in `sherman/lib/battle.css`; copy it into new skeletons) so red and blue look as strong as before, not
    stronger. Never raise territory saturation.
    **OWNER-APPROVED AFTER THE VIDEO TEST (2026-10-29, Sherman #13; reference scenes in `sherman/scenes-src/test-*.js`, images `sherman/build/approve/`):**
    - A1 bigger units: counters ~54 px and names ~19 px on screen (constant at any camera scale), corps counters on close-ups; the OLD
      counter look (no keyline, no dark layer). `test-A1-units.js`.
    - A2 bigger labels: town labels ~36 px, story-place labels ~32 px, constant on screen; BUT a town label must never hide troops or the fight:
      when units are near a town (or fighting starts there), shrink that label to the old small size or fade it. `test-A2-labels.js`.
    - A4 lighter Confederate red: territory multiply colour (232,52,52) -> (240,105,95) (with E1's saturate 0.8). `test-A4-red.js`.
    - B1 march maps: during a march/raid deep in enemy land, no enemy fill: own ground + the army's band coloured, a faint enemy glow
      only where the sides touch, enemy ground named by labels. `test-B1-march.js`.
    - B2 overview framing: pull the overview out until both sides' ground is clearly visible (not 85 % one colour). `test-B2-frame.js`.
    - B3 decision card keeps moving: lighter dim, slow camera push, arrows keep drawing, options pulse on their words (a beat every
      <= 2.5 s), and a BLACK OUTLINE on the white card text (2 px stroke + soft shadow). `test-B3-decide.js`.
    - C1 the first-second stamp states the STAKES (not a date). `test-C1-stamp.js`. **SUPERSEDED by section 1c (2026-11-01): clean first frame, every card on its spoken word.**
    - C2 hook: one big text block on screen at a time (each new card replaces the last; map labels and the date stay; the legend and corner badges step out while a card is up, section 1c). `test-C2-onetext.js`.
    - C3 last 20 s: the final-question card shrinks to the top band so YouTube end-screen elements fit; the map stays alive under
      it. `test-C3-endscreen.js`.
    - REJECTED (never apply): A3 legend chips in the on-map colours (too strong), A5 dark edge on the red front band, E3 colour that
      fades away from the front, cream keylines on counters, the navy/blue day grade.
  - Sound: the locked kit (section 3/3a), music 0.08 (section 4-5), -14 LUFS; **after ANY timing change, `assemble_full.py --audio-only`
    and check one bomb run frame vs sound** (the Rokossovsky remix fixed a 7 s drift).
  - Voice A (section 6). Thumbnail: vidIQ battlefield (left 2/3, labels checked/redone) + the commander's REAL photo cut out on the
    right third + red brush banner, 1-3 words (`rokossovsky/tools/make_thumb.py`). Title: vidIQ >= 85, TG pattern.
- **NEW IN THIS VIDEO, EACH ONE LOCKED (owner 2026-10-10: "I do like it... the things that we changed"):**
  1. **The hook v2** (section 1a): hard number + disaster as line 1, a big number card slamming in during the first second, a camera
     dive into the battlefield by ~6 s, a beat every 2-4 s, white-flash cut to the payoff by ~0:22, the commander's name held back
     (mystery "?" badge) until the twist, the prison-bars sequence with one stamp per detail, name slam + 3 snap cuts + title card.
  2. **Dark HD maps everywhere** (`<map>_hd_ref`: the dark "Frontlines" grade of the HD relief) for overview AND battle maps.
     **UPDATED 2026-10-29 (owner approved the C1 test, Sherman #13): bake every map with `LIFT=1 python3 tools/bake_hd.py <map>` and use
     `<map>_hd_lift`**: the SAME grey-green hue, land ramp (24,31,31)->(190,202,184), every map normalised to land median 0.70 (ridge maps
     no longer come out dark), sea (18,33,44), softer fine texture on close-ups (zoom >= 11: smoothing 1.6, fine 0.04). Day close-ups land at
     luma ~110-118 like the reference's day close-ups. **Never navy/blue on day shots: blue-muted = night** (owner 2026-10-29). Night (`K.night` /
     `GG.night`) unchanged. **Unit counters keep the old look** (no cream keyline: owner 2026-10-29). Test: `sherman/build/test-c1-compare.mp4`,
     study: `research/MAP_COLOUR_REVIEW.md`. `bake_hd.py` with LIFT=1 is in `sherman/tools/` (copy it into new skeletons).
  3. **Wide -> close -> wide per move:** option-1 territory on the wide shot, push-in to option-2 glowing fronts for the fight,
     zoom back out to option 1 for the result; the control overlay changes with every date the narration says.
  4. **Real licensed photos in every commander badge** (Soviet PD-Russia, Bundesarchiv CC BY-SA with credit), never initials when a
     licensed photo exists; overlays on the badge for story beats (prison bars, greyed + DISMISSED / SACKED stamps).
  5. **Text-only "duel" cards for a dictator or a figure with no licensed likeness** (ONE BLOW vs TWO BLOWS, "go and think it over" x2).
  6. **Night barrage beat** (`K.night` + rows of `K.gun` -> arc -> `K.impact`, shake on every impact), **tank-ambush beat** (tanks out
     of the woods, fire from the flank, pull back), **fire-sack beat** (isolated heavy tanks under guns on both flanks).
  7. **Casualty card when real numbers exist, otherwise a RESULT card** (never invent figures); **method card that lights one line per
     move** (`GG.METHOD` + `GG.METHOD_TITLE = "<NAME>'S METHOD"`).
  8. **Archive from US government film** (Capra's "The Battle of Russia", Army-Navy Screen Magazine / Signal Corps) + CC BY 4.0
     stills, in the projector frame with headline date cards; a designed headline card (no real masthead) for events with no film.
  9. **Thumbnail = vidIQ battlefield + the commander's REAL photo cut out + red banner** (`rokossovsky/tools/make_thumb.py`; check the
     AI image's labels and redo wrong ones).
  10. **Partial re-voice without re-recording everything:** `narrate_changed.py`, convert only the changed head with voice A and splice
     it onto the old voice-A take; then `--audio-only` remix (sound sync is automatic now, `sfx_cues.py`).
  11. **Engine (in `rokossovsky/lib`):** USSR + Reich flag keys (`flag: "ussr"` / `"reich"`, or any png path), method-card title.
- **Per-move snapshot sheets before any render; the owner approves; never render without the OK** (HANDOVER 0b step 7).

## 1. Where it lives (copy from goosegreen/ into every new video)
| What | File |
|---|---|
| All visual effects + defaults | `lib/fx.js` (`const K = FXK(B)`) + `lib/battle.js` |
| Sound levels per effect | `tools/sfx_mix_lib.py` (KINDS) |
| Sound files | `assets/media/sfx/` (incl. `candidates/cand1-4_hit.wav`) + `SFX_CREDITS.md` |
| Music | `assets/media/music_src_*.mp3` -> `python3 tools/make_music_bed.py` |
| Final mix (levels, ducking, loudness) | `tools/assemble_full.py` (full video), `tools/make_clip.py` (tests) |
| Reference scenes to copy from | `goosegreen/scenes-src/move3.js` (Harrier bombing run, helicopters, AA, casualty card), `test-terr-f.js` (fronts + territory, final look), `move1.js` (night attack) |

## 1a. THE HOOK (LOCKED, owner 2026-10-09, Rokossovsky hook v2: "I do like it... I want all videos to have strong hooks like this")
**UPDATED 2026-10-31 (owner, Cleburne v3): STAY IN THE STORY, NO CV IN THE FIRST TWO MINUTES.** Data: research/CHANNEL_LOG.md
("why views stalled"). Hits (Thomas 123k, Morgan 45k, 2 Para 39k) told ONE continuous crisis story for 45-100 s and brought the general
in as its turn (Thomas named at 0:47 "But one general does not leave the field", Morgan 1:20, move 1 at 2:20); the flops (Gavin, Collins)
left the story at ~0:25 for a CV ("He was an orphan...", nickname + list of achievements, birth/West Point) and lost two thirds of viewers by 0:42.
- 0:00-~0:45: one continuous story told as action on the map: stakes -> the place -> the number/disaster -> the title's promise as a result
  by 10-15 s (unchanged) -> then BACK INTO the danger (e.g. "But at dawn, it looked hopeless...") until the general enters.
- The general enters as the TURN of that story at ~0:45-1:00, in one line with at most ONE human detail ("His name was Patrick Cleburne,
  and he was born in Ireland"), then name slam + 3 snap cuts (unchanged).
- NEVER in the first two minutes: birth, schooling, career list, nickname + list of achievements, politics/controversy detours. Background
  max ~20 s, only the context needed for move 1, placed right before it. Move 1 starts by ~1:30-2:00.
- Do NOT follow "intro 20-25 s, name + move 1 by 0:25" (Studio AI advice): our hits did the opposite.
- Reference: Cleburne v3 opening `cleburne/scenes-src/hook-a.js` hook-3 (rewind to dawn, guns stuck, 3 TO 1, "the general in the gap",
  the order), master `cleburne/build/cleburne-v3.mp4` (not in git).
**UPDATED 2026-10-28 (owner, Meade #12), REVISED same day: THE OPENING = THE STAKES OF THIS STORY -> CONTINUOUS ZOOM -> NUMBER.**
Reference for the opening: `reference/hook-reference-meade-v3.mp4` (0:00-1:03) + `reference/hook-reference-meade-v3-sheet.jpg`
(scene source `meade/scenes-src/hook-a.js`). Why: "Fifty-one thousand men..." as line 1 jumped in with no context; the old Greene opening
("the American Revolution was dying in the South") set the stakes first. The rest of the hook below is unchanged.
- **Script, before the number (~6-10 s, 1-2 short sentences): the STAKES of this particular story, written fresh every time.**
  Ask: *what was about to be lost or won if this commander failed?* The war, the capital, the revolution, the whole army, the South,
  the empire... Say THAT in plain, dramatic words, then bring the viewer to the place where it was decided, ending on the place name so the
  number lands there. Examples (each a different stake, each worded differently; NOT templates):
  - Meade: "Robert E. Lee had beaten the Union army again and again. And now he marches into Pennsylvania, to a small town called
    Gettysburg." (stake: an unbeaten enemy on Northern soil)
  - Greene: "In the summer of seventeen eighty, the American Revolution was dying in the South." (stake: the cause itself)
  - Possible others: "If Moscow fell, the Soviet Union fell with it." / "One more defeat, and there would be no army left to lose." /
    "The war was supposed to be over by Christmas. Then..."
- **NEVER reuse another video's stakes sentence with the names swapped** (owner 2026-10-28: a session copied "had beaten ... again and again.
  And now he marches into..." onto another general). Check before voicing: *"Could this line open a different video if I swapped the names?
  If yes, rewrite it from this video's research."* The stakes come from the Gemini brief's "stakes" section and FACT_NOTES.
- **The stakes must be true and sourced** (log in FACT_NOTES): no "the war was about to be lost" unless sources say so; concrete stakes
  (a capital, an army, a deadline, a cause) beat vague ones.
- **Visual = the stakes shown as action, chosen to fit the line:** frame 0 = a wide map with units already moving, both flags, territory,
  the key commander's real-photo badge; **a stamp within the first second**; then whatever shows THIS stake: past defeats as one stamp each
  (Meade), a capital ring pulsing under arrows (a capital about to fall), territory shrinking date by date (a cause dying), a countdown...
  Then **ONE continuous geographic zoom** (zoom whoosh) from the overview straight down onto the place, arriving on the spoken place name:
  both maps driven by the same camera at true position and scale, the overview cross-faded out between ~6x and ~14x with feathered edges,
  **never a cut or a white flash** (owner: the cut "is not seamless").
- **The big number card slams on its own words**, then ticks; the other cards on their words as before.
- **Timing (owner 2026-10-28): keep the stakes frame SHORT (1-2 sentences, ~8 s) and SPEAK THE TITLE'S PROMISE AS A RESULT BY 10-15 s**, right after it
  (e.g. the number sentence itself says the result: "...in three days, and Lee lost."). The stakes frame is the ONLY thing allowed before the
  promise; it is not "background". The visual payoff on the map (the battle won) can land by ~0:25-0:30; dive by ~6-8 s; a beat every 2-4 s.
  (Meade v3 speaks the result only at ~0:32: new videos must say it by 10-15 s.)
- **Rule of the hook below (line 1 = number) now applies to the sentence AFTER the stakes frame.**
Reference: `reference/hook-reference-rokossovsky-v2.mp4` (0:00-1:04, voice + music + SFX) and its beat sheet
`reference/hook-reference-rokossovsky-v2-sheet.jpg`. Every video's first minute must match it. v1 of that hook was REJECTED as
"boring, not visual": a belief as line 1, no card, 7-10 s with nothing new, an 18 s static badge. Never ship a hook like that again.
**Script (first ~60 s, 4 paragraphs):**
1. **After the stakes frame (see UPDATED above): a hard number + the disaster/stakes in 3 short sentences** ("Four hundred thousand German soldiers. Lost in a single summer.
   And it all began in a swamp the Germans were sure no army could cross."). Never a date + place, never a belief or background first.
2. **The promise SPOKEN by 10-15 s; the visual flash-forward / payoff by ~0:25-0:30** (the title + thumbnail promise paid: "Three days later, a whole German army was trapped...").
3. **The human twist as ACTION, not a portrait** (prison, wound, disgrace, odds against the man), every detail its own beat.
4. **Name reveal + the three moves as quick cuts**, then "These are <Name>'s three greatest tactical moves." Hook total ~60-65 s.
**Visuals + sound (check each on the snapshot sheet before rendering):**
- Frame 0: map with units ALREADY MOVING (guns firing, counters advancing), flags + territory on screen.
- **A stamp slams in within the first second** (stakes frame), and **the big number card slams in on the number's words** (hit + shake) and ticks up (ticks); a stamp on the punchline (hit + shake).
- **A hard zoom-whoosh camera DIVE within the first ~6 s** onto the place of the story.
- **Something new every 2-4 s, never more than 4 s without a change** (camera move, stamp, counter, units moving, impacts, cut).
  Make the snapshot sheet every ~2.5 s for the first 30 s to prove it.
- **White-flash cut into the flash-forward**; the trap/victory slams shut with boom + shake; zoom-out whoosh to the big picture.
- **Twist sequence:** hard cut to dark, the year rolls back with ticks, an overlay that SLAMS (e.g. prison bars) over the real photo badge,
  one stamp per spoken detail (hit + small shake + red pulse), caveats as a small caption ("by his family's account").
- **Name slams in** (hit + shake), then 3 snap cuts (~3 s each, whoosh + hit) of the three battles, then the title card (riser + boom).
- SFX on every beat; the zoom whoosh only on the 2-3 biggest camera moves (dive, flash-forward, zoom-out).
**Proved by data (Morgan analytics 2026-10-25, owner-approved 2026-10-26; `morgan/youtube/analytics_2026-10-25.md`):** Morgan opened on
a date + background and named the promise only at 0:35: 44 % of viewers were gone by 0:42. So, on top of the rules above:
- **The title's promise is spoken as a result within the first 10-15 s** (owner 2026-10-28: only the short stakes frame may come before it) (e.g. "In under an hour, one crippled wagon driver wiped out
  Britain's most feared legion."). Holding back the hero's NAME for the slam is fine; holding back the PROMISE is not.
- **Background (dates, earlier defeats, the war so far) gets at most 15-20 s, and only after the promise** (the 1-2 sentence stakes frame at the very start is not background).
- **The three moves are previewed by 0:45** (name slam + 3 snap cuts finished by then): tighten the twist rather than drop beats.
- Targets: **≥ 65 % retention at 0:30 and ≥ 55 % at 1:00** (HANDOVER §10). Check the script against them before voicing.
**Confirmed again (George Thomas 2nd read 2026-10-26):** 94.4 % → 51.2 % by 0:45; the old Thomas hook (date + place first) shows the curve bottoming just before the hero appears (0:47). No new rule: the hook above already fixes this.
**Source to copy:** `rokossovsky/scenes-src/hook-a.js` + `hook-b.js` on branch `claude/rokossovsky-video-8` (script: `rokossovsky/script.md` HOOK).

## 1b. ENGAGEMENT BEATS (LOCKED, owner 2026-10-14: "I do like them... make it official")
Reference: `reference/engagement-test-peng.mp4` (1:04, Peng #10 test). Code: `lib/engage.js` (`const E = EngageK(B)`, loaded by
`tools/scene_template.html`; in `rokossovsky/` and `peng/`). Worked examples: `reference/engagement-examples/` (subscribe-move1c.js,
decide-move3c.js, final-ending-b.js). Studied from Tactical Genius (Ridgway transcript + top comments) and YouTube's spam / fake-engagement
policy (asking to like, comment or subscribe is allowed; never rewards, coercion or repeated comments). Every video has exactly these three:
1. **Woven subscribe line after move 1 = the "D2" pattern (owner 2026-10-29; replaces the older "...exactly what subscribing keeps
   bringing you" wording, which sounded like an order).** Never an order ("Subscribe!", "hit subscribe"); the ask is stated as what
   subscribing does, inside a bridge that keeps the story moving. Write it FRESH for each video, fitted to its topic (never copy the
   example word for word), in 4 beats with no pause:
   (1) close move 1 ("<move 1 place> was only the beginning."); (2) the hard QUESTION that move 2 answers, in the story's own terms;
   (3) one short clause saying this channel answers questions like that and that subscribing is how you catch the next one;
   (4) straight back into the story ("Here's how <Name> did it.").
   Example (Sherman #13): "Atlanta was only the beginning. So how do you march an army across a whole state with no supply line?
   That's the kind of question we answer here, and subscribing is how you catch the next one. Here's how Sherman did it."
   Visual: `E.subscribe(t, until)` = small SUBSCRIBE button bottom-right, a cursor clicks it (SUBSCRIBED, bell rings), slides
   out, timed on the subscribing clause; then the NEXT: <move 2> label. Never a full-screen subscribe card.
2. **One "What would you do?" card per video**, at the move's biggest decision, BEFORE the narration reveals the real choice:
   "Now stop for a moment, and put yourself in <Name>'s place. <situation in 2 short sentences>. Do you <A>, or do you <B>? Tell us in the
   comments what you would have done. And then..." Visual: `E.decide({ sub, a, b, real, t, tCount, tReveal, until })` = dimmed map,
   WHAT WOULD YOU DO? + two option boxes (A / B) + TELL US IN THE COMMENTS with 3 ticks; on the reveal the real choice lights blue and
   the other greys (hit). Only once per video (more gets repetitive).
3. **The final question (last paragraph, replaces "Which commander should we cover next?")**: "So which was <Name>'s greatest move?
   One, <move 1>. Two, <move 2>. Or three, <move 3>? Tell us in the comments. And if someone in your family served in <war/place>, on
   either side, tell us their story. We read every one. Subscribe, so you don't miss the next commander." Visual:
   `E.final({ moves: [[NAME, DATE] x3], tShow, tNums, tAsk, tFamily, tSub, until })` = three numbered cards popping in as each move is
   named, 1, 2 OR 3? (gold), the family-story line, and the corner subscribe button. For wars with no living families (ancient,
   18th-19th century) replace the family line with "and tell us which commander we should cover next".
Owner kept BOTH spoken subscribe asks (after move 1 and at the very end), as in the reference.
**Ending rules (Thomas 2nd read 2026-10-26: the 81 s ending lost 6.4 points with no next video offered; the 7:25 subscribe dip used the old wording, made before this section, so beat 1 stays as it is):**
- **The ending is ≤ 45 s after the final battle result**: method recap + callback in one short paragraph, legacy kept to 1-2 sentences, then the final question (beat 3).
- **NO spoken next-video pitch by default (owner 2026-10-29, overrides the Thomas rule):** the narrator never tells the viewer "next, watch X" unless the owner asks for it in that video. The end screen (set in Studio) can still show a video.
- The last ~20 s leave room for **YouTube's end screen** (map stays on screen; set that same video + subscribe in Studio). Target: ≤ 3 points lost in the ending. Time each beat with `B.at` on the spoken words.

## 1c. ON-SCREEN TEXT AND CLUTTER (LOCKED, owner 2026-11-01, from the Patton #15 review; applies to the WHOLE video, every scene, from the next video on)
Owner: "the things we applied to the video, not the packaging, should be rules and apply through the whole video." (Patton #15 itself keeps what it has.)
These rules REPLACE C1 ("stamp in the first second") and the "legend and date stay" part of C2 in section 0b, and add to 1a. Reference: Patton #15 `patton/tools/pc_body_hook-a.js` (declutter block) and `pc_body_hook-b.js`.
1. **Nothing appears on screen before the narrator says it.** Every card, stamp, banner, tag, number, name plate and badge lands ON or AFTER its own spoken word (use `B.at(para, "word")`).
   The big text of a stamp is a word the narrator says ("TRAPPED" on "trapped", never "CUT OFF" if "cut off" is never spoken). Sub-lines under a card may use only spoken words.
   A person's badge/photo/name appears only after the narrator has said that name (no McAuliffe badge before his name is spoken; mystery "?" badge until the name slam). Audit every stamp/card/badge text against the paragraph text before voicing.
2. **A clean first frame.** Frame 0 = the map and the units already moving, nothing else: no half-faded legend, no stamp, no badge. The date scroll comes in on the spoken date word.
   The first card lands on the first words that call for it (not at 0.1 s). (This replaces the C1 first-second stamp.)
3. **One big card at a time, and the screen is clear around it.** While any big card (title card, stamp, number card, decision card, result card) is on screen, the clutter steps out: the colour legend (red/blue/who is who), corner commander badges and similar HUD fade out (use `filter: opacity()`, never a second autoAlpha tween on the same element) about 0.15 s before the card, and come back about 0.3 s after it leaves. Big cards stay ~2-3 s, not longer.
   **The date scroll NEVER disappears** (owner 2026-11-01); cards sit below it and never overlap it. The legend is first shown after the opening cards (when the camera has arrived), not at 0.8 s.
4. **Artillery shots only where you can see them.** Gun flashes, arcs, impacts and their booms (and the screen shake that goes with each impact) are kept for artillery that is clearly visible and large enough to read at that camera scale; no continuous barrage of tiny unseen shells (Patton #15 had ~25 shells in the first 25 s: the sound ran on after the artillery was off screen). A hook has at most ~1 shot per 2 s and only on a visible beat; when the camera leaves the guns or the shells land off screen, the cues stop. Check the cue list (`build/sfx_cues.json`) in the first 60 s against the frames.
5. **The script must make sense when read cold.** Before voicing, read the whole spoken text as a viewer would: every transition has something it points back to ("The room where..." with no room before it is a bug), no sentence names the hero before the name slam (say "the general"), no repeated statistic, no "But ... But" stacks, a flashback says how far back ("Three days earlier"). After ANY text change, grep every `B.at(...)` phrase of every scene against the new text (a missing phrase silently breaks the scene).
6. **The name slam by ~1:00 and move 1 by ~2:00** (1a). Keep each narrated line in the hook short enough for that.
Packaging experiments (Test & Compare titles/thumbnails, `research/CONSIDERING.md` and `research/PACKAGING_TEST_PATTON.md`) are NOT part of these rules yet.

## 2. Visuals (locked)
- **Opening:** every video opens on an animated MAP with units on screen in the first second. Never a photo. Photos only after the hook. The whole first minute follows the LOCKED HOOK (section 1a).
- **Map:** parchment shaded relief (`bake.py`), faint dashed grid (`K.grid`), vignette + grain, date top-left. Flat, no 3D tilt.
- **Colours:** counters/aircraft/arrows blue `#1f4fc4` (hero) / red `#c4121f` (enemy). Day front lines `#2c57b7` / `#bc2528` (30% muted from the counters). Night lines + territory tint `#4a6a9a` / `#a8503c`. Neutral grey `#77746c`, gold `#c9b48a`, text `#f7f3ea`, font Oswald.
- **Front lines (`K.front`):** glowing band, width 15, glow 0.47, drawn on, gentle pulse.
  - Only the REAL front (where the sides touch) is two-coloured. Lines behind it are one colour.
  - **Wide campaign maps** (a whole country or theatre: Korea, Sicily, Normandy, Holland): every front line between the two sides is **two-coloured, blue on our side and red on theirs, never one colour** (owner 2026-10-04). One-colour lines are only for reserve/depth lines on close-up battle maps.
  - When a front collapses, the two-colour band MOVES to the next line (`to` + `moveT`, moveDur 3.0).
- **Territory ("E" look, `K.frontTint`):** alpha 0.34, depth 170 px behind the front (95 px for a forward zone that will be lost), soft 24, clipped to land with a land mask (`elev > 0.5`). Lost ground flickers then fades (`K.lose`). End every scene with `K.raiseTerritory()`.
- **WHO CONTROLS THE GROUND + NATION FLAGS, ON EVERY MAP (owner 2026-10-05, Gavin):** every map scene, the overview maps AND
  every battle map, shows which side holds which ground and whose flag it is:
  - **Territory colours (strong, not faded):** Allies/hero `#2e5cb2`, Axis/enemy `#be3a2a`, neutral `#807c72`; alpha 0.46 inside,
    up to 0.66 right at the border, clipped to land; a two-colour front band where the sides meet; thin country borders.
    Generator: `gavin/tools/make_europe_control.py` (historical borders `world_1938.geojson` + front polylines per date ->
    `assets/media/<map>_ctl_<date>.png`, placed with `B.image(...)` and cross-faded when the date changes).
  - **The map changes with time:** one overlay per date the narration reaches (e.g. Jul 43 / Sep 43 / Jun 44 / Sep 44), cross-fade 1 s.
  - **Nation flags on the map** (flag ~115 px on screen; since 2026-10-31 NO name under them, section 2b), one per power on screen;
    "NEUTRAL" labels on neutral countries; legend card ALLIES / AXIS / NEUTRAL top-centre. Use the PERIOD national flags:
    Germany 1933-45 = the red flag with the white disc and swastika (`ger_reich_flag.png`, owner's choice), Kingdom of Italy
    with the Savoy shield (`italy_flag.png`), USSR 1936-55 (`ussr_flag.png`), UK, US 48-star. Unit counters keep their small flag chips.
  - Battle maps: the same colours fill each side's ground behind its front (on top of the `K.front` lines), with the flags of
    the nations fighting placed on their ground. Reference: `gavin/scenes-src/intro.js` (hook-3) and `ending.js`.
  - Fact-check every front line per date and log it in FACT_NOTES ("control map").
- **Night (`K.night`):** fully muted palette + brightness boost on lines and territory; normal at dawn.
- **Unit symbols (`K.counter`):** infantry X · artillery = howitzer silhouette · tank/armour = tank silhouette · mech = X + track · AA = twin barrels · HQ = flag. Flag badge + size mark (••• platoon, I company, II battalion, III regiment).
- **Artillery:** the gun fires (`K.gun`: flash, smoke, recoil), shell arc, **impact** (`K.impact`: fireball, shock ring, smoke, small shake).
- **Aircraft (`K.aircraft`):** detailed top-down jets / turboprops / helicopters with ground shadow, spinning props/rotors, dotted flight path; shoot-downs smoke, spiral and crash; helicopters' shadows close in when they land.
- **WW2 transport / plane symbol (locked, owner 2026-10-06): the glowing C-47, `K.aircraft({ kind: "c47g", side })`.** White body with a soft glow; the **outline and glow take the side colour: blue = Allies (`side: "carth"`), red = Germans/enemy (`side: "rome"`)**. Size ~30 on wide maps. Planes **fly in spaced out (few, not swarms), do their job (drop / bomb) and fly off the map**; never stop or fade in mid-air. Preview: `frontlines-1m/build/plane-glow-sides.png`; used in the 1-min D-Day test (`frontlines-1m/scenes-src/europe_hd.js`). The old twin-boom `cargo` and the striped `c47` icons were rejected (looked like drones / didn't convince).
- **Bombing run (owner's favourite, copy exactly):** jet flies the run (size 84, alt 30, dur 3.2); each bomb is `K.impact(x, y, t0 + 1.55 + k * 0.25, { r: 20, shake: first ? 5 : false })`, i.e. just after the jet passes, sticks 0.25 s apart. Code: `goosegreen/scenes-src/move3.js` ("the Harrier strike").
- **Also:** ship silhouettes with muzzle flashes, burning places with smoke columns (`K.smoke`), pulsing target rings on objectives (`K.target`), commander badge (`K.badge`, initials on dark tint if no legal photo), casualty card after every move with losses (`K.casualties`), captions bottom-centre.

## 2a. MERGED "FRONTLINES" LOOK (owner-approved 2026-10-06, the 1-min D-Day test; lessons from Netflix "WWII: From the Frontlines")
Our locked style (sections 2-5) stays the base; these are ADDED on top. Reference build: `frontlines-1m/` (scenes `europe_hd`, `normandy_hd`, archive `a-1`/`a-2`; `ONEMIN=1 python3 tools/assemble_dday.py`); final test video https://gofile.io/d/YX3zQBqK.
- **Open on a 2D map, no globe.** The owner dropped the globe/cloud dive: start straight on the dark 2D map with units moving in the first second (the 3D tilt is out too: maps stay flat).
- **Detailed maps (HD relief):** `tools/bake_hd.py` = zoom+1 terrain tiles, 5760x3240 shown at 2880x1620, 4-direction hillshade + slope + ambient occlusion + fine texture (since 2026-10-29: `LIFT=1` -> `<map>_hd_lift`, the default basemap, see 0b item 2). Rivers traced from the elevation data (`make_rivers_dem.py`), places from OSM (`fetch_osm.py`).
- **Geography layer (`make_geo_layer.py BASE STYLE SKIP MAXV MINPOP`):** only BIG towns (population >= MINPOP, e.g. 8000; no villages, no suburbs), small labels, period names (1944 names, HIST dict), labels never collide. Put it ABOVE the territory layer (else it turns pink). Story places (e.g. Sainte-Mère-Église, Utah Beach) as small white-box labels; keep them small.
- **Territory:** strong colours drawn with `mixBlendMode = "multiply"` (`_mx` overlays: axis (232,52,52) / allied (110,160,255)) so the relief shows through the colour.
- **Living map (`lib/living.js`, `LivingK`):** drifting cloud shadows, shimmer on rivers, scale bar, north arrow. Always on.
- **Flags + emblem:** the period national emblem sits ON its country's land (e.g. the Nazi emblem centred on Germany): never over the sea, over labels, or cut by the frame edge; it STAYS for the whole map (never fades). No country-name label next to it (the flag says it). Every power in the story has its flag visible (UK, USA, USSR...); widen the camera if one is off-screen.
- **BOTH OPTIONS ARE LOCKED AND KEPT (owner 2026-10-06): never delete either one.** Choose per shot:
  - **Option 1 = territory colours** (each side's ground filled with strong colour + flags) -> **overhead / wide shots** (a continent, a country, a campaign overview).
  - **Option 2 = two glowing front lines only** (no fill) -> **close-up battle maps** (a town, a river crossing, a beachhead), where the fill would hide the terrain, roads and units.
  - Use your eye: if a close-up reads better with fill (or a wide shot with lines), pick that; a video can use both (wide shots option 1, then option 2 when the camera goes in close). If the owner names one ("use option 1/2"), use it everywhere they say.
- **OPTION 2 details: "front lines only".** Drop the territory fill entirely (no `_mx` / control overlay) and show who holds what ONLY with the **two-colour glowing front lines** (`K.front`, width 15, glow 0.47: blue band on the Allied side, red band on the Axis side) wherever the sides touch; the legend shows two short glowing lines instead of squares. Flags, emblem, labels, planes and everything else stay the same. Lines come from the same control map: `python3 frontlines-1m/tools/make_front_lines.py OVERLAY.png OUT.json [MINLEN]` (traces the axis/allied border, drops coast rims, orients blue to the Allied side). Example: `frontlines-1m/scenes-src/test-opt2.js`; comparison sheet `frontlines-1m/build/territory-options.jpg`.
- **Planes:** the glowing C-47 (`c47g`, section 2), few and spaced out; they drop/bomb and then fly off the map.
- **Archive sections (Netflix look, `tools/build_film_dday.py` + `archive_shots.py`):** (1) a **newspaper headline card** (`make_headline_dday.py`) with a paper-page sound; (2) **photos with 3D depth** (parallax, `"depth": True`) with a small caption (unit · place · date); (3) restored, tinted **film inside a projector frame** (`"frame": True`) with a quiet projector loop; (4) **date cards in headline style** ("6 JUNE 1944 / NORMANDY, FRANCE"). Never a slideshow.
- **Sound design (Frontlines-style, mixed separately from the locked SFX, `assemble_dday.py`):** cinematic whoosh on camera moves (-14 dB), dry pop on labels (-20), big cinematic boom on key beats (-11), reverse riser into reveals (-17), newspaper page (-12), projector loop under film (-27), low tactical/tension drone bed (-30). The locked battle sounds (section 3a), plane sound B, music 0.08 + the locked mix chain are unchanged.
- **Voice:** voice A (section 6); option 2 = plain am_michael. **Music:** the channel bed; Kevin MacLeod "Five Armies" (CC BY 4.0, from 1:00) matched to the bed loudness is approved for this look.

## 2b. MAP LOOK v11 + CLEAN SCREEN (LOCKED, owner 2026-10-31: "Yes, do like this look. Let's lock it down.")
Applies to every NEW video from #16 on (owner 2026-10-31: Patton #15 stays on the old look). It REPLACES the basemap look (look E / plain `_hd_lift`) and is ADDED on top of
sections 2 and 2a (counters, front lines, territory options 1/2, flags, planes, sounds all stay). Reference reel (old on top,
new below): `reference/style-reference-maplook-v11.mp4`; trees close-up vs the owner's reference film:
`reference/style-reference-maplook-v11-trees.jpg`; seamless colour fade: `reference/style-reference-maplook-v11-fade.jpg`.
Code snippets for the scenes: `templates/clean_screen_v11.js`. How it was found (judges, checker, versions v3-v11):
`research/TREE_REDESIGN_BRIEF.md`, `cleburne/build/judge-trees-v10.md`, `cleburne/build/check-trees-v10.md`.
- **Basemap = `cleburne/tools/ref_look_v11.py`, full bake:** from the video folder,
  `FULL=1 python3 tools/ref_look_v11.py <map> 2880 1620 assets/<map>_hd_lift.jpg` (about 3 min for 5760x3240; ~6 GB RAM;
  without `FULL=1` it renders a 1920x1080 preview crop around CX,CY with a vignette). Copy into the new video's `tools/`:
  `ref_look_v11.py`, `make_detail_layers.py`, `make_tree_sprites.py`, and `assets/src/trees/` (the sprite library
  `sprites_C2.npz` + public-domain USGS sources, SOURCES.md). Inputs: `assets/src/<map>_hd_elev.npy` (`bake_hd.py`) and
  `assets/media/<map>_det_riv.png`, `_det_rivS.png`, `_det_swamp.png` (`make_detail_layers.py`; NHD/NLCD are US-only, outside
  the US the script's WIDE mode uses DEM rivers + ESA WorldCover water: check the rivers by eye).
  - **Ground:** pale muted sand (no orange), relief about half as strong as before, fine paper grain, soft wide hills.
  - **Rivers (copied from the owner's reference film):** speckled stony grey water, thin dark rim, narrow brown dirt bank, pale
    green grass strip, then the trees. **Creeks:** thin dark wiggly hairlines (no straight trenches, no ghost lines).
  - **Trees:** ONLY as belts along the rivers, near-continuous, placement free (not data-accurate, owner: "the trees should be
    just around the river"); every tree a separate crown made from REAL public-domain aerial canopy photos, with its own light
    (top-left lit), soft edge (no outline), its own soft shadow; olive ~RGB 74,82,52. Never sphere/dot/cartoon trees, never
    scattered groves on the hills, never trees along tiny creeks.
- **Clean screen (`templates/clean_screen_v11.js`):**
  - **Nation flags show NO country name under them** (no "UNITED STATES" / "CONFEDERATE STATES"); the flags themselves stay
    on every map (section 2 rule unchanged).
  - **Words on screen leave after ~3.5 s (`LBL_LIFE = 3.5`):** the captions of what the narrator says, place-name boxes, town
    names, map stamps (WRONG HILL, REPULSED...) and belief cards. Unit names under the counters stay with their counters.
- **Option 1 -> option 2 is SEAMLESS:** when the camera dives from a wide territory-colour shot into a close-up with front
  lines only, the colours dissolve over ~2.8 s during the dive (`sine.inOut`), never switched off in one frame; when the
  colours come back they fade in over ~2.2 s.
- Known open point (owner not asked yet): the territory colours were tuned for the old green-grey map and look strong orange /
  blue-grey on the pale sand in wide shots; retune only if the owner asks.

## 2c. GRANT #16 LOCKS (owner 2026-11-02, from the Grant review; applies from the next video on; reference build `grant/`, master https://gofile.io/d/bZlvwa4F `Grant-Top3-1080p-v2.mp4`)
Owner: "put the things we used for this video as rules." The thumbnail method used here (vidIQ in one go, three variants) is NOT part of these rules: packaging stays an experiment (section 1c last line, PACKAGING_GUIDE 0b).
1. **Maps: NO TREES, NO MODERN RESERVOIRS.** Bake with `NO_TREES=1 FULL=1 python3 tools/ref_look_v11.py ...` (`MAIN_ONLY=1` exists if trees ever return: belts only on the main river, never on side bays/oxbows). `NO_RESERVOIR=1` (and `NO_AREAS=1` where the NHD river polygons ARE a reservoir, e.g. Cumberland/Tennessee) in `tools/make_detail_layers.py`, which now normalises the USGS NHD field names (the service returns UPPER/lower case). Rebake script: `grant/tools/rebake_v2.sh`; bake ONE map at a time (an out-of-memory kill leaves the old look).
2. **Territory colours WHEN THEY HELP THE VIEWER (owner 2026-11-03, Arnold #17; REPLACES the 2026-11-02 "territory colours minimised / half strength" rule):** show who controls the ground and what has been captured whenever it helps the viewer follow the story: on wide/overview shots (who holds which region, by date) AND on close-ups when ground changes hands (a captured city, fort, redoubt, island, river line; ground lost or won as the front moves). Use the locked full-strength territory colours of section 2 (blue/red, the old `saturate(0.8)` tone is fine), clearly readable at a glance; half-strength fills that nobody notices are NOT allowed any more. Leave the colours out only where they add nothing (a pure manoeuvre close-up where the two glowing front lines already say who is where, a night action, a naval fight on open water). Switching between a coloured shot and a fronts-only shot still dissolves smoothly (~2.8 s). Judge each shot by eye: "does the colour tell the viewer something?"
3. **Voice: the plain Kokoro `am_michael` narration is the default from #16 (owner: "keep this one")**; voice A (Chatterbox conversion) is optional only if the owner asks. Assemble with `VOICE=audio/voice.wav python3 tools/assemble_full.py`. Audio-only swap needs no re-render.
4. **Archive style is mandatory and complete** (never drop it again; check it on the sheet before the render): every archive photo with 3D depth (`"depth": true`) INSIDE the projector frame (`"frame": true`, now also for photos: `archive_shots.projector_frame`), designed newspaper headline card (no real masthead, `grant/assets/media/headline_donelson.jpg` pattern) + headline-style date cards, background block ~20-28 s, the bridge/second block, AND one short ~8 s block where each move ends, spliced into a map paragraph with `archive_inserts.json` (`{"<para tag>": {"from": "<spoken start words>", "to": "<spoken end words>", "shots": [...]}}`; `assemble_full.py` cuts the map video and keeps the voice running; pick a stretch with no essential card). Civil War = photos + engravings, no film.
5. **NO synthesized "reference" sounds (owner 2026-11-03, Arnold #17; REPLACES the Grant #16 rule "reference sound design is part of the build"):** the owner: "look at the previous videos, you didn't use these sounds, you just invented them". `tools/ref_sounds.py` (label pop, extra whoosh, cinematic boom, reverse riser, newspaper page, projector loop) is NOT used: every `ref:*` cue stays silent, exactly as in the locked reference video (Rokossovsky #8) and all videos before Grant. Only the locked kit of section 3/3a plays (hit, tick, whoosh = `zoom_whoosh` on the 2-3 biggest moves, fire, impact, mg, explosion, aircraft...). `assemble_full.py` places ref sounds only with `REF_SOUNDS=1` (never set it).
6. **Every move ends on a card:** `K.casualties` when the narrator says real numbers (both sides only if both are spoken), else a RESULT card; then the method card. Numbers only from FACT_NOTES.
7. **Script-format bugs that wrecked the voice (never again):** no `]` inside a `[MAP: ...]` tag (narrate.py cuts the tag at the first `]` and the TTS reads the rest aloud), every spoken paragraph starts with its own `[MAP: id | ...]` / `[ARCHIVE: ...]` tag (an untagged paragraph is skipped), and cards use only words the narrator says. After any script change run `narrate_changed.py`, check `audio/timing.json` for the tag list and total, then rebuild scenes.
8. **Build hygiene:** `tools/rebuild_all.sh` / `rebuild_final.sh` rebuild every scene against the final maps + timing; `tools/quick_sheet.py SCENE STEP` makes a contact sheet for any scene; LOOK at every sheet before the render (the ending shipped broken once: an undefined unit stopped the whole scene). Delete `scenes/*/snapshots` and the hyperframes history cache (`/root/.cache/hyperframes/history` grows to 9 GB) as you go; run a background loop that deletes it during builds and renders. The machine restarts when the session is idle: stay in the turn (bounded wait loops) while a render runs.
9. **Loudness recipe (worked on Grant):** assemble, then `volume=1.45dB,alimiter=limit=0.82:level=disabled` on the master's audio, remux with `build/video_only_1080p.mp4` = -14.3 LUFS, true peak -1.0.

## 3. Sound effects (locked files and levels)
Rule: every visual beat has a sound, and **the boom is always on the impact** (launches are quiet). **Aircraft sounds only when an aircraft is on screen** (owner 2026-10-06): never a plane/jet/heli sound over parachutes or an empty sky; give `K.aircraft` the sound (its default) or show the planes. Levels are dB in `sfx_mix_lib.py`:

| Kind (`SFX(kind, t)`) | Sound | Level | Min gap |
|---|---|---|---|
| impact (shells, mortars landing) | real distant artillery `cand3_hit`, `cand1_hit` | -7 | 0.25 s |
| explosion (bombs, big blasts, `K.impact` r >= 20) | real distant explosions `cand2_hit`, `cand4_hit` | -4 | 0.20 s |
| fire (gun launch) | `gun_fire` | -24 | 0.35 s |
| mortar (launch) | `mortar_thump` | -24 | 0.30 s |
| jet | `jet_flyby` (roar + Doppler, loudest mid-flight) | -11 | 1.2 s |
| prop (turboprop / transport) | `prop_flyby` = Mixkit "Low airplane flying over" (owner pick "sound B", 2026-10-06; replaced the old prop sound) | -13 | 1.5 s |
| heli | `heli_flyby` (rotor thumps) | -14 | 2.0 s |
| missile | `missile_launch_hit` | -9 | 0.8 s |
| hit | `hit` | -8 | 0.5 s |
| whoosh (zoom) | `zoom_whoosh` (Mixkit "Cinematic tunnel reverb woosh", deep, reverb tail; owner pick 2026-09-30) | -12 | 0.5 s |

**Zoom / transition sound (owner 2026-09-30):** only on the BIGGEST camera moves (the hook dive, the flash-forward cut, the
hook zoom-out). No zoom sound on ordinary camera moves, arrows or commander badges (badges slide in silently). The sound is
`zoom_whoosh.wav` (owner picked it from 3 rounds of tests; Mixkit Sound Effects Free License, no credit needed), checked by the sound lock.
| mg | `mg_burst` | -18 | 1.0 s |
| tick (counters) | `counter_tick` | -20 | 0.12 s |
| static (radio) | `radio_static` | -21 | 3.0 s |

`K.impact`, `K.gun` and `K.aircraft` call `SFX()` automatically, so scenes get the right sound without extra code.

## 3a. THE BATTLE SOUNDS (owner's favourites, locked 2026-09-30; enforced by `tools/check_sound_lock.py`)
Hear them in `reference/style-reference-30s.mp4`. Every session must use exactly these; the build STOPS if they change.
| On screen | Code (does the sound automatically) | What you hear |
|---|---|---|
| Field artillery / mortars firing | `K.gun` (or the scene's `shoot()` helper) | quiet launch thud (-24 dB), never a boom |
| **Artillery shells landing** | `K.impact` r < 20 | **real distant-artillery boom** (cand3 / cand1, -7 dB) + fireball + smoke + small shake |
| **Ships' guns firing** (e.g. HMS Arrow) | same `K.gun` -> arc -> `K.impact` from the ship's bow | quiet launch, **same real artillery boom on impact** |
| **Planes bombing** | **`K.bombRun({ pts, t, bombs: [[x,y], ...] })`** (one line: jet + bombs 0.25 s apart + **SCREEN SHAKE** on the first bomb) | jet roar with Doppler (-11 dB), then **real distant-explosion booms** (cand2 / cand4, -4 dB) + **camera shake** |
| Jets / turboprops / helicopters | `K.aircraft` kind `jet` / `turboprop` / `heli` | engine flyby loudest mid-flight (-11 / -13 / -14 dB) |
| Aircraft shot down | `K.aircraft({ down: t })` | engine sound, then crash fireball |
Rule: **the boom is always on the impact.** **Bombing always SHAKES the screen** (first bomb of every run, strength 5; every big explosion shakes 6, shells 3). Never set `shake: false` on a bombing run, **and never switch the shake off on shell hits or explosions either** (owner 2026-10-03: every shell that lands shakes, also every shell of a volley; the O.P. Smith video lost it in 4 scenes this way). Leave `K.impact` at its default shake. Examples to copy: ship + field-gun barrage `goosegreen/scenes-src/move1.js`
("the barrage"), bombing run `move3.js` ("the Harrier strike").

## 4. Music (locked)
- Kevin MacLeod (incompetech.com, CC BY 4.0), in this order: **"Long Note One"** (hook + move 1) -> **"Wounded"** (move 2) -> **"Long Note Two"** (move 3) -> **"Anguish"** (ending).
- Build: `python3 tools/make_music_bed.py` (fits each track to its chapter, 5 s crossfades, -20 LUFS, 3 s fade-out).

## 5. Mix levels (locked, in assemble_full.py / make_clip.py)
- Music `MUSIC_VOL = 0.08` (owner 2026-09-30 chose option C of a 0.18 / 0.12 / 0.08 test; the reference clip still has the older 0.18 music), 2 s fade-in, 3 s fade-out.
- Music ducked under the voice: sidechain threshold 0.03, ratio 6, attack 20 ms, release 400 ms.
- SFX ducked lightly under the voice: threshold 0.03, ratio 3, attack 10 ms, release 300 ms.
- **Sound effects at FULL level** (no overall SFX volume cut), as in the newest videos (Rokossovsky #8 to Meade #12). Owner 2026-10-26: "use the option the newest session is using". The -4 dB cut (`SFX_VOL = 0.63`, owner 2026-10-14) applies to the **Goose Green remix only** and stays in `goosegreen/tools/` and its sound check; don't copy it into new videos.
- Limiter 0.5, then two-pass loudnorm to **-14 LUFS**, true peak -1.5 dB, LRA 11. Audio AAC 192k.
- Sound-only changes never need a re-render: `python3 tools/assemble_full.py --audio-only`.

## 6. Voice, hook, thumbnail, description
- **Voice (DEFAULT, owner-locked 2026-10-06): voice A** = the Kokoro am_michael narration converted to the owner's reference voice with `tts/convert_voice.py` (ref `tts/voices/owner_ref.wav`, sample `tts/voices/test_A_chatterbox.mp3`; setup `bash tts/setup_clone.sh`). Same pacing and timestamps as the Kokoro take. **Option 2 (fallback only, or when the owner asks):** the plain Kokoro am_michael narration.
  Steps: `tools/narrate.py` (am_michael) → `audio/voice.wav` + `timing.json` → `/home/user/cb-venv/bin/python /home/user/battle-maps/tts/convert_voice.py audio/voice.wav /home/user/battle-maps/tts/voices/owner_ref.wav audio/voice_owner.wav` (~15-20 min per 18 min) → mix `voice_owner.wav`.
- Hook: formula in HANDOVER section 1 (stakes-first line, flash-forward, change every 3-5 s, SFX on every beat).
- Thumbnail: formula in HANDOVER 1b (vidIQ + Tactical Genius references, 1-3 word text, generic officer). **Face pop (Thomas read 2026-10-26):** the portrait's face gets extra contrast + saturation (and a light rim against the map) so the expression reads at 168×94; text stays 1-3 words in high contrast.
- Description: copy the layout of `goosegreen/build/youtube_description.txt` (chapters, sources, map/music/SFX/image credits), but with **NO links at all** (owner rule 2026-10: new channels get flagged as spam; write "licensed under Creative Commons Attribution 4.0" instead of the URL). Full rules: `research/PACKAGING_GUIDE.md`.

## 7. Tried and REJECTED (don't offer these again)
- Voice: Chatterbox text-to-speech cloning (`tts/clone_voice.py`, pacing off); Seed-VC conversion (B: ~4 h per video on CPU, not preferred by ear).
- Opening on a photo.
- Synthesized artillery booms (replaced by real recordings).
- The `sfx/candidates/bombs/` clips (owner disliked them).
- Loud gun-launch sounds / boom at launch instead of impact.
- Bright, fully saturated front lines; tint spilling onto sea or distant land. (Faded territory is also out: since 2026-10-05 territory is strong, see section 2.)
- Two-coloured lines behind the front.
- Globe / cloud-dive openings and 3D tilted maps (owner 2026-10-06: open on the flat 2D map). Village-level labels, big labels, modern merged town names, emblems over the sea or fading away.
- Simple flat aircraft icons, drone-like twin-boom transports, planes that stop in mid-air (exception: the glowing C-47 `c47g` is the approved WW2 plane symbol).
- NATO dot/oval artillery and oval tank symbols (silhouettes chosen).
- Music at 0.35 (too loud).
- Map trees as dots, spheres or one fused clump; trees scattered everywhere / data-accurate forest cover; orange saturated relief ("cartoonic"); country names under flags; captions/labels that stay on screen for 10+ s; territory colours that switch off in one frame (all owner 2026-10-31, see 2b).
- Licences: no NonCommercial / NoDerivatives (no IWM Non-Commercial, no BBC SFX). Never a fake likeness of a real person.
- **NO TREES (owner 2026-11-01, Grant #16 review: trees were distracting, first 'main river only', then 'remove those trees'):** bake with `NO_TREES=1 FULL=1 python3 tools/ref_look_v11.py <map> 2880 1620 assets/<map>_hd_lift.jpg` (grant/tools version; `MAIN_ONLY=1` keeps only the main river's belt if trees ever come back). NO MODERN RESERVOIRS: `NO_RESERVOIR=1` (and `NO_AREAS=1` for the Cumberland/Tennessee, where the NHD river polygons are Lake Barkley / Kentucky Lake) in `grant/tools/make_detail_layers.py`; that script also normalises the USGS NHD field names (the service returns UPPER/lower case now). Rivers, creeks, ground and territory colours as before.
