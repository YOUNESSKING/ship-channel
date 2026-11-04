# Title, Thumbnail, Description, Chapters & Tags Guide (battle-maps channel)

How to write the YouTube packaging for every video. Adapted from the owner's packaging guide for the sister channel
(Psycho Décodé, videos 1–4) to this English military-history channel. Each rule says **why**, so edge cases can be
judged instead of followed blindly. Worked example: `morgan/youtube/youtube_metadata.md` (+ the PDF next to it).

---

## 0b. PACKAGING RULES (LOCKED, owner 2026-11-01, from the Patton #15 packaging test; they ADD to the rest of this guide and, where they differ, THEY WIN)
Worked example: `patton/research/PACKAGING_TEST_PATTON.md`, `patton/youtube/test/`, `patton/research/FACT_NOTES.md` ("Packaging TEST claims").
1. **Three titles and two or three thumbnails for YouTube Test & Compare, at launch.**
   - Title A = the locked format `<Name>'s Top 3 Legendary Tactical Moves | The Man Who <true, concrete result>`.
   - Title B = a curiosity title that leads with the famous battle or stakes casual WWII/history fans already know (Patton: "Battle of the Bulge: How Patton Turned His Army North and Reached Bastogne in a Week").
   - Title C = a hybrid: the name + the stakes or the three places.
   - The OWNER picks the main title (Patton: B) and the main thumbnail (Patton: BROKE THE SIEGE); the others go into Test & Compare. A title that leaves the locked format is allowed when the owner picks it, and the PDF says so.
   - Score every title with vidIQ (`vidiq_score_title`, >= 85) and show the owner all of them with score and sources.
2. **Every claim in a title, banner or thumbnail label is literally true and sourced** in `<name>/research/FACT_NOTES.md` (add a "Packaging TEST claims" table: claim, verdict, source). No invented time limits ("in 48 hours"), no "saved the war", no "forgotten", no exact figures that are only on one source, no code words or quotes that the check found unsourced. Concrete + time-bound + famous works ONLY when literally true (Patton: "in a Week" = Verdun 19 Dec to link-up 26 Dec).
3. **Every thumbnail = the commander's face (face pop, STYLE_LOCK 6) + ONE instantly recognisable context image + 1-3 words in high contrast that match a title's promise:**
   - context images: snow + tanks + the town's road sign; a clear map of the key move (an arrow that visibly turns or breaks through); a battle-shape map of the breakout. Colour portrait only; the context stays dark and desaturated (HANDOVER 1b).
   - made by vidIQ in one go (battlefield first, then the same image + portrait + torn red banner; variant text by editing the finished image).
   - **check before showing:** banner spelling; every map label spelled and placed right (a label hidden by the portrait or on the wrong side is fixed); no stray rank insignia (three stars on the helmet only, no single collar star); the whole face inside the frame; the picture matches the video (no fake battle details). Show all variants on ONE sheet WITH a 168x94 feed-size strip.
   - match each thumbnail to the title it can sit with; if one fits only one title, say so (Test & Compare mixes them).
4. **Description, chapters and tags as usual, no links.** The publishing PDF lists the test titles and thumbnails, says which are main/optional, and carries the Test & Compare note.
5. **End screen:** from the channel's busiest video (currently Morgan) to the new video, plus subscribe, over the last ~20 s. Free; expect little (channel end-screen CTR 0.6%).
6. **After the upload, log in `research/CHANNEL_LOG.md`:** which title and thumbnail won, CTR, and impressions on days 1-3, kept SEPARATE from retention at 0:30 and 1:00. Packaging never fixes retention: the opening rule (STYLE_LOCK 1a, 1c) decides 0:30.

---

## 0. Order of work

1. **Validate the topic** before writing anything (§1).
2. **Title**: write options, score them, lock one (§2).
3. **Thumbnail**: must make the *same promise* as the title (§3).
4. **Description**: only after the final audio is locked (§4).
5. **Chapters**: computed from the final timeline, never guessed (§5).
6. **Tags + category** (§6).
7. Save everything in `<name>/youtube/youtube_metadata.md`, build the upload PDF (`<name>/youtube/<Name>-YouTube-upload.pdf`: thumbnail, title, alternatives, settings, description, tags) and give the owner the exact text to paste.
   **Never upload or edit anything on YouTube ourselves.**

---

## 1. Validate the topic first

- Topic + packaging drive views; a strong intro is only table stakes.
  *Why (sister channel):* competitor flops had intros as strong as their hits (40 transcripts studied).
- Proof of demand = the same topic doing well on **several channels**. Use `vidiq_outliers` / search.
  Here: `research/VIDEO_IDEAS_v2.md` already lists the outliers per idea (e.g. Daniel Morgan: a 123x outlier on a
  tiny channel, no bigger channel covering him in the general format — that gap is the opportunity).
- Record the competitor video IDs, titles, views and thumbnail notes in `<name>/youtube/competitors.md`
  and save their thumbnails in `<name>/youtube/competitor_refs/`.

---

## 2. Title

### Rules
| Rule | Why |
|---|---|
| **Score every option with `vidiq_score_title`** (type `long`, 5 credits each). Target **≥ 85**. | Don't lock an unscored title. Morgan: 93 / 95 / 93 / 96. |
| **Use the Tactical Genius pattern: `<Name>'s Top 3 Legendary Tactical Moves \| <3-6 word subtitle>`**, name first; best subtitle = "The Man Who <huge, well-known result>". Avoid "fired / almost" angles and nicknames. | Thomas (2026-10-05): a hook-first title got CTR 0.9 %. TG's "The Man Who…" titles reach 238k-1.1M views; their "The General Truman Fired" got 30k. See HANDOVER §10. (Replaces the old Morgan rule "hook first, series name after".) |
| **No negation as the hook** ("He wasn't a genius…"). | Sister channel video 2: the brain reads the strong word before the negation; the promise flips. |
| Be **clear and accurate**: every claim must be true and self-explanatory. | Morgan v1 "Destroyed Britain's Best" confused the owner ("Britain's best what?") and overstated it; "Britain's Elite" is clear and true. |
| Match the **emotional register** of the competitor hits (underdog, "the general who never lost", enemy's arrogance). | See `research/NICHE_ANALYSIS.md`. |
| The title in `youtube_metadata.md` must be the **scored, locked** one. | Sister channel V4: a helper agent wrote an unscored title into the metadata file. |
| ≤ 100 characters (YouTube limit). | |

### Pattern that worked
**Current (2026-10-05):** `George Thomas's Top 3 Legendary Tactical Moves | The Man Who Saved the Union Army` (vidIQ 86), modelled on TG's Ridgway 1.11M / Zhukov 629k / Manstein 238k.

Older (Morgan, before the Thomas CTR data, no longer the model):
`[Hook: the most shocking true fact]: [General]'s Top 3 Tactical Moves`
- Morgan (95, locked): *He Destroyed Britain's Elite in 1 Hour: Daniel Morgan's Top 3 Tactical Moves*
- Morgan A/B alternative (96): *How a Crippled Wagon Driver Wiped Out Britain's Elite in Under an Hour*

---

## 3. Title ↔ thumbnail: one promise

- Thumbnail = 2–5 words, ALL CAPS, **one red element** (the emotional payload), no negation,
  tested at 168×94 px (phone size). The general's portrait on one side, the key map moment behind.
- **The thumbnail must never contradict the title.**
  *Why (sister channel):* video 2 had CTR 1.7 % while its live thumbnail said the opposite of its title.
- The thumbnail completes the title, it doesn't repeat it word for word when possible.
- Make 2–3 options and use Studio → **Test & compare**.
- **Face pop (Thomas, 2026-10-26):** boost contrast + saturation on the general's face (light rim against the map) so the expression reads at phone size.
- **End screen:** every video's last ~20 s carries YouTube's end screen pointing to ONE named video + subscribe (no spoken pitch unless the owner asks, 2026-10-29); 12.7 % of Thomas's traffic came from Up Next.
- **Proof the title matters most:** Thomas with only the title changed to the TG pattern: CTR 0.9 % → 3.84 %, impressions 750 → 612K.

---

## 4. Description

Write it **after the voice is final** (facts can change during fact-checking and re-voicing).

### Template (paste-ready shape)
```
[LINE 1–2 — THE HOOK: the script's own opening, in plain words. These are the only lines shown before
 "more", so they must make someone want to watch.]

In this video we break down [General]'s three greatest tactical moves: [3 moves, each naming the REAL
 battle / people actually said in the recorded voice].

[ONE payoff line — the video's closing idea.]

CHAPTERS
0:00 …

SOURCES
- …

CREDITS (images, terrain, music — required by the CC BY licences)
…

Narration voice: AI-generated (Kokoro TTS). Maps: original animations.
📩 Business enquiries: [email to fill in]

#[General] #[Battle] #[War]
```

### Rules
| Rule | Why |
|---|---|
| Name **only battles, people and numbers that are in the recorded script**. | Sister channel V4 cited researchers who were never in the voice. |
| **Fact-check every name and number** before it goes in (and before voicing). Use the Gemini v3 fact-check list. | Morgan research had 5 errors (see HANDOVER §8.12). |
| First line = the script's hook, not "In this video…". | The first ~2 lines are all most viewers see. |
| Keep every CC BY / CC BY-SA credit line, but **write NO links (no URLs) anywhere in the description**: name the licence instead ("licensed under Creative Commons Attribution 4.0"). | Owner: YouTube treats links on new channels as possible spam. Naming the licence still satisfies the attribution. |
| Exactly **3 hashtags**. | More than 3 looks spammy. |
| Business email: `[email to fill in]` — **the owner must fill it in.** | |

---

## 5. Chapters

- Compute them from the **final** timeline, never by ear: the paragraph start times in `<name>/audio/timing.json`
  (our assembly keeps the voice timeline unchanged, so these are the final times). Re-run whenever the audio changes.
- Anchor chapters to **paragraph ids** (e.g. `cow-13`), never to a hard-coded second.
- First chapter = `0:00`; every chapter ≥ 10 s (YouTube minimum); ~10–12 chapters for 16–19 min
  (hook, each move's setup / key moment / result, ending).
- Chapter titles: short, the section's idea — they double as mini-hooks ("The Shot That Killed Fraser").

---

## 6. Tags & category

- 12–18 English tags, **≤ 500 characters total**, comma-separated, in this order:
  1. broad: `military history`, `history documentary`, the war (`American Revolution`)
  2. topic: the battles and concepts (`Battle of Cowpens`, `double envelopment`)
  3. names said in the video (`Banastre Tarleton`, `Nathanael Greene`)
  4. long-tail phrases people search (`greatest military tactics`, `animated battle map`)
- Same fact rule: no tag for a person or battle that isn't in the video.
- Category: **Education**, always.
- Mark **Altered or synthetic content = Yes** (AI narration voice).

---

## 7. Final checklist (tick before handing to the owner)

- [ ] Topic validated by ≥ 2 competitor outliers; refs saved in `youtube/competitor_refs/`
- [ ] Title scored ≥ 85 with vidIQ; hook inside ~60 chars; ≤ 100 chars; clear and true
- [ ] No negation as the hook (title and thumbnail)
- [ ] Thumbnail makes the same promise as the title; 2–3 options for Test & compare
- [ ] Description line 1 = script hook; every name/number fact-checked and actually in the voice
- [ ] Chapters from `timing.json` on the FINAL audio; start at 0:00; each ≥ 10 s
- [ ] Credits + email placeholder + 3 hashtags
- [ ] 12–18 tags, ≤ 500 chars; category Education; synthetic content = Yes
- [ ] `youtube_metadata.md` and the PDF hold the locked title (not an alternative)

---

## 8. How sure are we?

- **Measured (sister channel):** the video 2 CTR/thumbnail mismatch, the chapter-timing errors, the fact errors,
  the vidIQ title scores.
- **Good practice, not yet proven on this channel:** hashtag count, tag order, chapter count, the hook-first title.
  Revisit after each video's Studio numbers (CTR, first-30-s retention) come in — ask the owner for
  screenshots; vidIQ has no impressions/CTR.
