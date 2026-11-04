# Lessons for the publishing-guide PDF and the thumbnail PDF
Written 2026-10-26 from the battle-maps channel (12 videos; Tactical Genius-style "Top 3 Legendary Tactical Moves"). Sources:
HANDOVER.md (§1b thumbnail formula, §6 lessons, §10 first live numbers), research/PACKAGING_GUIDE.md, STYLE_LOCK.md and the
Meade #12 session. Each rule says WHY, so another channel can judge its own edge cases.

---

## Part 1. The publishing-guide PDF ("everything the owner needs to upload")

### 1.1 What the PDF must contain (in this order)
1. **Cover:** channel series name + the main thumbnail, big, with one line on how it was made.
2. **The finished video:** file name, resolution, fps, codecs, size, length, download link, voice used, music + licence,
   sound-effect licences, any locked choices (e.g. which flags). *Why: the owner uploads from this page without opening anything else.*
3. **Chapters table:** start times + titles, computed from the final timing file (never by ear).
4. **Key frames:** a strip of frames from the first minute. *Why: the owner checks the hook at a glance before uploading.*
5. **Title:** the locked title + its score, plus 3 scored alternatives.
6. **Thumbnails:** main + A/B alternative, with a short "why this text" (which winning type it is) and a "checked" note
   (what was verified in the AI image).
7. **Description, ready to paste:** first line = the title; everything after it = the description.
8. **Upload settings:** tags, category, audience, captions (list the hard names to check in auto-captions), synthetic-content
   answer, pinned comment, schedule.
9. **Upload checklist** (play the master once, upload, paste, thumbnail, fill the email, disclosure, end screen, schedule,
   check CTR/retention at 24-48 h).
10. **"Facts to double-check before publishing" box:** every figure that is approximate, single-source or second-hand.
    *Why: the script was fact-checked, but some numbers rest on one source; the owner must see them before going public.*

### 1.2 Title rules (from the first live numbers: a hook-first title got 0.9 % CTR)
- **Copy the winning competitor's pattern exactly:** `<Name>'s Top 3 Legendary Tactical Moves | The Man Who <huge result>`.
  Famous name first, series name, short subtitle. Best subtitle = "The Man Who <beat/broke/saved/stopped> <something famous>".
- **Score every option** (vidIQ `score_title`, type long) and lock one that scores **>= 85**; but the pattern beats the score,
  never trade it for a few points.
- **Avoid** "forgotten / underrated / fired / almost / nearly" angles and nicknames (the competitor's "The General Truman Fired"
  flopped; our Thomas title with "almost fired" got 0.9 % CTR).
- **No negation** as the hook ("He wasn't a genius..."): the brain reads the strong word, the promise flips.
- **Clear and true:** every claim self-explanatory and accurate ("Britain's best what?" confused the owner).
- **The title in the PDF and metadata file must be the scored, locked one**, never an unscored alternative.
- **The promise must be paid in the first 30 s of the video** (Thomas paid his title promise at 7:37 and viewers left).

### 1.3 Description rules
- **Line 1-2 = the script's own hook** in plain words (only these lines show before "more"). Never "In this video...".
- Then one paragraph naming the 3 moves, then the one-line method/payoff, then the engagement question.
- **NO links anywhere** (new channels get flagged as spam). Name licences in words: "Licensed under Creative Commons:
  By Attribution 4.0". Keep every CC BY credit line (music, sound effects, images, map data).
- **Only names and numbers that are actually said in the recorded voice.** A helper once listed researchers never mentioned.
- **Exactly 3 hashtags.** Business email = a placeholder the owner fills in.
- Write the description only after the final voice is locked (facts change during fact-checking).

### 1.4 Chapters
- From the final `timing.json` (paragraph start times), anchored to paragraph ids, never hard-coded seconds.
- First chapter **0:00**; every chapter **>= 10 s**; **no two chapters with the same time** (YouTube rejects duplicates;
  Meade had a "What would you do?" chapter on the same second as Move 3: dropped it).
- ~10-16 chapters for 16-19 min; titles are mini-hooks ("The Gap in Jackson's Line", "Sickles Moves Forward").
- Keep one chapter file as the single source: if the build writes a shorter chapters file (5 music sections), overwrite it
  from the description before building the PDF (Meade's first PDF showed the 5 music chapters instead of the 16).

### 1.5 Tags and settings
- 12-18 English tags, <= 500 characters, order: broad (military history, the war) -> topic (battles, concepts) -> names said
  in the video -> long-tail phrases. No tag for anything not in the video.
- Category **Education**; audience **not made for kids**.
- **Altered or synthetic content:** the question is about realistic content that could fool viewers (a real person saying
  something they didn't, fake footage of real events). Animated maps, real archive photos and designed cards are NOT AI video.
  The only AI part is the narration voice. Both answers are defensible; we tick **Yes** (no reach penalty, removes any risk for a
  new channel). Whatever you choose, answer the same way on every video of the series.
- Pinned comment = the final engagement question ("Which was his greatest move: 1, 2 or 3? Which commander next?").

### 1.6 The master file and delivery (checked before the PDF is built)
- **ffprobe: 1920x1080** (an old audio-only remix once silently turned the master into 720p).
- **Loudness: measure with ebur128, target -14 LUFS.** The cloned voice comes out ~1.2-1.3 dB too loud after the standard
  finalize (-12.7 LUFS on Meade and Peng): lower the final mix by the difference and remux. Always measure; never assume.
- **Sound sync:** check one impact frame against its sound (the boom must land on the fireball, within 2-3 frames).
- Download link: the cloud machine is temporary, so the master must be uploaded (Gofile) and the link put in the PDF.
  Some session permission modes block uploads to public file hosts even after the owner says yes: switch to a mode that asks,
  or add a permission rule, then upload. Rebuild the PDF with the link afterwards.
- For a chat preview (30 MB limit): two 540p halves.

### 1.7 After publishing
- Read CTR and 30-s retention at 3, 7 and 28 days; save each read in the video folder.
- If CTR < 2 % after ~1,000 impressions: change the title to the pattern first, then switch to the alternative thumbnail.

---

## Part 2. The thumbnail PDF ("how every thumbnail is made and checked")

### 2.1 The picture formula (identical on all 13 studied Tactical Genius thumbnails)
- **Left 2/3:** dark, desaturated, moody, realistic **aerial battlefield**: red/blue unit blocks, big curved white arrows,
  fire and black smoke, small place labels and commander name tags.
- **Right 1/3:** the commander's **REAL photo**, cut out (background removed), grey/contrast boosted, looking toward the map,
  with a dark gradient behind so it separates from the battlefield.
- **Bottom-left: red brush-stroke banner** with big white text.
- 1280x720, readable at phone size (168x94): check it small before uploading.

### 2.2 How it is made (our tool chain)
1. vidIQ `generate_thumbnail` with **2-3 of the competitor's top thumbnails as `referenceImages`** and a prompt that names the
   real battle, period uniforms, terrain, "keep the picture on the LEFT two-thirds, leave the RIGHT third dark and empty",
   **"no text, no letters, no flags, no modern objects, no aircraft, no tanks"** (adapt to the era).
2. A small compositor script (`tools/make_thumb.py`): place our own labels, cut out the real photo with rembg, add the gradient,
   draw the banner, export A and B.
3. Never a fake likeness of a real person: real public-domain photo, or a generic soldier of the right era if none exists.

### 2.3 Checks on the AI image (every time; these went wrong before)
- **Labels and geography:** the AI writes wrong or misspelled labels; ask for no text and add our own small tags in the right
  places (e.g. SEMINARY RIDGE, CEMETERY RIDGE, PICKETT, MEADE). Make sure no tag hides behind the banner (move it if it does).
- **Equipment and era:** no tanks, planes or modern vehicles where there were none.
- **Sides and colours:** the hero's blocks in the hero colour, the enemy's in the other; match the video's convention.
- **Forbidden symbols:** zoom in on every unit. The AI drew small **red flags (Confederate battle flags)** in the ranks even when told
  "no flags". Paint them out (inpainting) before compositing; check again after. Same rule for any symbol the channel bans.
- **Inpaint smudges** are fine if invisible at thumbnail size; never paint over a unit block.

### 2.4 The text (what decides the click)
- **1-3 words, ALL CAPS, understandable with zero context, creates tension.** Three winning types:
  1. **The hero's decision/defiance in plain words:** "LET THEM COME" (1.0M views), Meade: **STAY AND FIGHT**.
  2. **The enemy's own words (verbatim, in quote marks):** "AMATEURS" (773k), Meade: **"MY FAULT"** (Lee, as recorded).
  3. **Ominous stakes:** "AT THE GATES" (585k), Jackson: 3 ARMIES BEATEN.
- **Losers:** nicknames or insults that need background ("DUGOUT DOUG" 29k), 4+ word lines (1.7x), negations.
- **Quote marks only on verbatim quotes.**
- **Same promise as the title** (one promise across title, thumbnail and the first 30 s). Never contradict the title
  (a sister channel's CTR fell to 1.7 % from exactly that). The thumbnail completes the title, it doesn't repeat it.

### 2.5 Delivering the thumbnails
- Always **2 variants of different text types** (main + alternative) for YouTube's **Test & compare**.
- In the PDF, for each: the image, the text type, why it was chosen, and a "checked" line (labels added, flags removed,
  no anachronisms, real photo + its licence).

---

## Part 3. General lessons that keep the whole pipeline safe
- **Never render or upload without the owner's explicit OK in plain words**; show snapshot sheets per part first.
- **Commit and push after every milestone**: machines reboot and usage limits stop agents (resume them, don't restart them).
- **Fact-check every number and quote**; log corrections; quote marks only on verbatim words, with the recorder named for
  recollections; superlatives ("the only", "the largest") need a source that says exactly that.
- **Licences:** public domain, CC0, CC BY, CC BY-SA only; no NonCommercial, no NoDerivatives; credit every CC BY item.
- **Review the helpers' work against the locked style before showing the owner** (Meade: thinned front lines, a wrong-date map,
  a missing flag and an initials badge where a real photo existed were all caught and fixed before the owner saw them).
