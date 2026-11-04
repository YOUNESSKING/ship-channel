# Forgotten Fleet (@forgottenfleet1): teardown study

Date: 2026-11-04. Author: research agent. Scope: every one of the 88 uploads, plus a deep look at 4 videos (Arizona, Pearl Harbor 8, Flier, PT-305).

**Sources and tags used in this file**
- **[VQ-ids]**: vidIQ `get_videos_by_ids` pulled 2026-11-04. Exact views, likes, comments, publish time, length and description for all 88 videos.
- **[VQ-ch]**: vidIQ `channel_stats`, daily counts from 2026-03-01.
- **[VQ-vs]**: vidIQ `video_stats`, daily views for the first 8 days of 10 videos.
- **[VQ-kw]**: vidIQ `keyword_research`.
- **[VQ-watch]**: vidIQ `video_watch` (an AI that watches the video; it can be wrong, see section 4).
- **[TR]**: vidIQ transcripts of 4 videos.
- **[CM]**: vidIQ comments. 100 top threads each for Arizona, Pearl Harbor 8 and PT-109; all threads for Flier; the 100 newest comments channel-wide.
- **[VQ-score]**: vidIQ title and thumbnail scores.
- **[YT]**: yt-dlp (video list, auto-chapters, tabs).
- **[WEB]**: web search, used for fact-checks.
- **EST**: an estimate or inference, not a measured number.

Raw data is in the scratchpad and was not committed: `videos.json` (88 rows) and `table.md`.

---

## 0. Verified channel facts (the "known so far" brief, checked)

| Claim in brief | Verified value | Source |
|---|---|---|
| Created 2026-03-01, GB | Channel created 2026-03-01 22:33 UTC; country GB. First upload 2026-03-03. | [VQ-ch] |
| ~15.1K subs, 7.17M views, 88 videos | 15,100 subs, 7,182,131 views, 88 videos (2026-11-04) | [VQ-ch] |
| ~3 uploads/week | 2.5 a week over the channel's life. 4.2 a week in June. 2.8 a week from Aug to Oct. | [VQ-ids] |
| 14–24 min, early ~8 min | Mar–Jun: 8–14 min (mean 9.9). From 2026-07-05: 14–24 min (mean 17.2). | [VQ-ids] |
| Median ~13.5K, mean ~91K | **Median 12,364, mean 81,716** (sum 7.19M) | [VQ-ids] |
| Hits/flops as listed | Confirmed: Arizona 1,159,072; PH-8 769,236; PT-109 549,846; Petticoat 422,162; Iowa 241,065; Kidd 1,998 (only 2 days old, so not yet a flop); PT-305 1,202; Flier 2,631 | [VQ-ids] |
| AI British TTS voice | **Not settled.** [VQ-watch] heard a "human, RP accent" voice on both videos it watched. Viewers flag mispronunciations ("Mocha-pu" for Mokapu). No top comment calls it AI. Owner should listen to 60 s and decide. | [VQ-watch], [CM] |
| ~90% archival, ~10% 2D graphics | **Wrong for the videos themselves.** Arizona: ~35% archival photos, ~20% archival film/newsreel, ~25% modern drone/stock/tourist video, ~15% NPS underwater/ROV video, ~5% graphics, 0% AI. Flier: ~60% archival (25% of the ship itself), ~12% maps, ~15% graphics. **Thumbnails are 100% AI images**, and one still shows the Gemini sparkle watermark (Shinano). | [VQ-watch], thumbnails |
| No host | Confirmed: faceless | [VQ-watch] |
| Shorts / community / playlists | **0 Shorts** (no Shorts tab). **1 playlist** ("Warships"). No community posts found. | [YT], [VQ] |

---
## 1. Best vs Worst (top 5 against bottom 5)

"Worst" means the bottom 5 **long-form videos (14 min and up, i.e. from 2026-07 on) that are at least 21 days old**. These are compared like for like, in the same era and format, as the top 5. All 5 top hits are also in this era.
- Kidd (2 days old) is excluded because it is too new.
- The all-time bottom 5 are all short 8–10 min videos from Mar–Jun: U-Boat 583, Bikini radioactive 661, John Burke 824, Yorktown car 1,085, Thresher 1,204. They follow the same pattern; see section 2.

| | **Arizona** "Why The Uss Arizona Can Never Be Raised" | **PH-8** "Where Are All 8 Pearl Harbor Battleships Now" | **PT-109** "Where Is the Real PT-109 Now" | **Petticoat** "Where Is the REAL Pink Submarine From Operation Petticoat Now" | **Iowa** "Where Are All 4 Iowa-Class Battleships Now" | **PT-305** "Where Is the Real PT-305 Now" | **Missouri** "How the USS Missouri Made Japan Surrender" | **PH wrecks** "Where Are Pearl Harbor's Shipwrecks Now" | **Flier** "Where Is the USS Flier Now" | **Wisconsin** "Where Is USS Wisconsin Battleship Now" |
|---|---|---|---|---|---|---|---|---|---|---|
| Views [VQ-ids] | **1,159,072** | **769,236** | **549,846** | **422,162** | **241,065** | 1,202 | 1,732 | 1,931 | 2,631 | 2,947 |
| Views at ~day 1 / day 7 [VQ-vs] | 2.1K / 23K, then took off from day 7 (448K by day 13) | 91K / 371K | 116K / 474K | 167K / 371K | 14K / 175K | 264 / 1,047 | 627 / 1,437 | 1,294 / 1,594 | 609 / 2,457 | 1,773 / 2,678 |
| Topic fame: monthly YouTube searches [VQ-kw] | "uss arizona" 48,321 (+78%) | "pearl harbor battleships" 4,353 | "pt 109" 5,203 | "operation petticoat" <750 | "iowa class battleship" 3,959 | "pt 305" <750 | "uss missouri" 9,585 | "pearl harbor shipwrecks" <750 | "uss flier" <750 | "uss wisconsin" 6,308 |
| Fame hook (EST) | Most famous wreck in the US | Pearl Harbor, 8 ships | JFK | Cary Grant film | Biggest battleships | none | famous, but the answer is known | 3rd PH video in 3 months | none | museum ship, answer is obvious |
| Title template | Why X Can Never Be Raised | Where Are All N X Now | Where Is the Real X Now | Where Is the REAL X From [Film] Now | Where Are All N X Now | Where Is the Real X Now | How X Did Y | Where Are X Now | Where Is X Now | Where Is X Now |
| Title length (chars) | 39 | 44 | 28 | 61 | 42 | 28 | 41 | 39 | 26 | 37 |
| vidIQ title score [VQ-score] | 89 | – | – | – | – | 80 | – | – | 87 | – |
| Thumbnail text | WHY NOT RAISE IT? | 85 YEARS LATER | WHERE IS IT NOW? | WHERE IS IT NOW? | 80 YEARS LATER | WHERE IS IT NOW? | IT ENDED. | 85 YEARS LATER | 65 YEARS MISSING | 83 YEARS LATER |
| Thumbnail subject | AI aerial of memorial over wreck | AI line of BBs + one green wreck | AI PT-109 at speed | AI pink sub on a tropical beach | AI 4 Iowas in formation | AI PT-305 at speed (**same layout as PT-109**) | AI Missouri beside the Arizona memorial | AI rusty wrecks in a lagoon | AI sub at speed | AI Wisconsin at a pier |
| vidIQ thumbnail score [VQ-score] | **77** | – | – | – | – | 83 | – | – | **89** | – |
| Length | 21:48 | 16:28 | 17:40 | 15:44 | 15:36 | 18:37 | 17:35 | 17:16 | 18:39 | 15:46 |
| Published (UTC) | Tue 21:00 | Tue 21:00 | Mon 19:00 | Thu 16:00 | Mon 22:00 | Tue 17:00 | **Wed** 22:00 | **Wed** 19:00 | Mon 21:00 | **Wed** 20:00 |
| Days since previous upload | 2.0 | 2.1 | 2.9 | 1.9 | 5.0 | 2.0 | 2.0 (right after the Iowa hit) | 1.9 | 2.1 | **1.0** |
| Like rate | 0.36% | 1.44% | 0.75% | 0.99% | 1.21% | 0.92% | 3.12% | 1.19% | 0.68% | 2.31% |
| Comment rate | 0.08% | 0.13% | 0.08% | 0.09% | 0.11% | 0.17% | 0.17% | 0.05% | 0.08% | 0.27% |
| Comment content [CM] | Family-grave stories (top 208–447 likes); "war grave, leave it"; fuel-amount corrections | Family members who served; "Utah is NOT next to Arizona" (x5) | JFK memories; "PT boats weren't plywood" (76 likes); wrong engine footage | Film nostalgia, many languages; "wrong actor photo" | (not pulled) | (2 comments) | – | – | 2 comments, both off-topic | – |
| Hook, first 30 s [TR] | Present-tense mystery: "there is a battleship... Something stops them every time." **The answer is held back for 20 min.** | "8 battleships... one survived two atomic bombs, another vanished." 4 teasers, then **5 reveals, one by one** | (not pulled) | (not pulled) | (not pulled) | **Gives the answer by 1:20** ("return to New Orleans, be rebuilt"). Then a 1943 résumé. | – | – | **Gives the answer at 0:30** ("divers found something 330 ft beneath"). Then a résumé ("Gato-class... Electric Boat"). | – |

**What separates them (numbers, not vibes)**
- **Fame decides almost everything. Packaging scores do not.**
  - Flier scored *higher* than Arizona on both title (87 against 89, about equal) and thumbnail (**89 against 77**), yet got 440x fewer views.
  - The thumbnail template is identical across hits and flops: yellow 2–4 word caps, AI aerial, teal sea.
- **The outcome is binary and visible within 24 h.** Hits had 14K–167K views by day 1. Flops had 264–1,773 and were flat by day 3–4 (Flier went from 2,457 on day 7 to 2,631 lifetime). [VQ-vs]
  - YouTube's day-1 test decides it.
  - Arizona is the one exception: slow on day 1, then it caught Browse on day 6–7 and kept running.
- **Search volume does not decide it.** Petticoat had <750 searches a month and got 422K. Wisconsin had 6,308 a month and got 2.9K. Missouri had 9,585 a month and got 1.7K. The hits are Browse/Suggested wins on an emotional pop-culture or grave angle.
- **The "answer" must be unknown AND interesting.**
  - Flops answer "Where is it now?" with "in a museum" (Wisconsin, PT-305, Kidd, Laffey 6.2K) or "on the bottom, as you'd expect" (Flier).
  - Hits answer with a twist: guns in the desert, one ship survived two atomic bombs, a pink sub, JFK's boat lost. Arizona answers "why not raise it" with war-grave law, the oil, and men choosing to be interred.
- **Self-cannibalisation.** By its date "Pearl Harbor's Shipwrecks Now" (1.9K) was at least the channel's 10th Pearl Harbor/Arizona video. "Pearl Harbor's Surviving Ships Now" (10K) came 3 weeks after PH-8.
- **Wednesday:** 3 of the bottom 5 went out on a Wednesday. Across all 13 Wednesday uploads the median is 3,019 and there are 0 hits over 100K. Mon/Thu/Fri medians are 12K–40K. This is weak evidence (n=13); treat it as a hint, not a rule.
- **Engagement is inverse.** Flops have the *higher* like rates (2.3% median under 5K views against 1.2% for hits). Flops only reach existing subscribers. Hits reach cold, older Browse viewers who rarely like (Arizona 0.36%).

### DO (each backed by a data point)
1. **DO pick ships the average 60-year-old American already knows by name**: Arizona, JFK, Cary Grant, Missouri/Iowa. The top 5 = 48% of all channel views. 16 videos ≥100K produce 69% of views (top 10).
2. **DO use a pop-culture or celebrity bridge.** Film/celebrity-linked titles have a median of **168,715** (n=5: PT-109, PT-73, Petticoat, Mister Roberts 23.5K, Run Silent 2K). The channel median is 12.4K.
3. **DO frame the title as an impossibility or obstacle when the ship is famous.** "Can Never Be Raised" titles have a median of 55K and a mean of 318K (n=4: Arizona 1.16M, Utah 99K, Bismarck 11K, Thresher "Can Never Be Recovered" 1.2K). Bismarck and Thresher show that the template alone is not enough.
4. **DO use the "Where Are All N [class] Now" roll-call for famous classes.** That template has a median of 38K and 0 videos under 5K (n=11): Iowa 241K, PH-8 769K, Alaska 67K, North Carolina 56K. It is the channel's safest format.
5. **DO hold the answer back.** Arizona answers the title question at ~19:50 of 21:48. PH-8 reveals one ship at a time across 16 min. Flier (0:30) and PT-305 (1:20) give the answer away in the hook.
6. **DO tease several surprising outcomes in the first 20 s** ("one survived two atomic bombs, another vanished"). PH-8 had 91K views on day 1.
7. **DO ask "where are you watching from / family connection?" early.** It produced the top comments on Arizona (447, 323, 208 likes) and PH-8 (516 likes: "my great uncle was Isaac C. Kidd"). Those are long, emotional comments. Put it at ~0:30–0:45, as they do, or later (see DON'T #9).
8. **DO make the video 15–18 min with a 2–3 day gap.** The 15–18 min bucket has a median of 14.8K and 6 hits (n=21). Videos posted ≥1.5 days after the previous one have a median of ~13K, against 5.7K when the gap was under 1.5 days (n=26).
9. **DO slow down after a flop streak.** After 5 flops in a row (Sep 22–Oct 2), FF paused for 9 days. They came back with "Utah Can NEVER Be Raised" (99K, 4,194 a day), the template of their biggest hit.
10. **DO use real NPS/NOAA underwater footage, drone shots of the actual site, and ROV wreck video.** That is ~40% of Arizona's visuals [VQ-watch], and it reads as "where it is now".
11. **DO keep a source list in the description.** All 88 videos list institutions (NPS, NHHC, NARA). It's cheap credibility, but see DON'T #7.
12. **DO end on an emotional image plus a single next-video pointer.** Arizona ends on the bell and the memorial; PT-305 ends on "the next video is on screen".

### DON'T (each backed by a data point)
1. **DON'T make "Where Is X Now" about an obscure ship.** That template has a median of 8.3K, and 8 of its 18 videos are under 5K. PT-305 1.2K, Flier 2.6K, Most-Feared Sub 3.0K and Laffey 6.2K are all obscure-ship cases.
2. **DON'T pick a ship whose answer is "a museum you can visit".** Wisconsin 2.9K, PT-305 1.2K, Kidd 2.0K. In contrast, Texas, whose answer has drama (sinking at her berth, dry-dock rescue), got 35K.
3. **DON'T reuse a hit's thumbnail layout for a lesser ship.** PT-305 copied PT-109's exact thumbnail (same composition, same text) and got 1,202 against 549,846.
4. **DON'T do a 3rd or 4th video on the same harbour within 3 months.** Pearl Harbor's Shipwrecks 1.9K, Surviving Ships 10K and Oil Leak 13.8K all came after the PH-8 and Arizona hits.
5. **DON'T rely on vidIQ scores to pick winners.** Flier's thumbnail scored 89 and flopped; Arizona's scored 77 and got 1.16M. Use the scores as a floor only.
6. **DON'T upload daily.** June ran at 4.2 a week with a median of 3,347. July dropped to 0.9 a week, switched to the new format, and had a median of 147,557. The sub count also stalled (7.4K to 7.6K across June).
7. **DON'T get facts wrong on a topic veterans' families watch.** The top-liked factual replies are corrections: Utah's location (x5 on PH-8), "PT boats weren't plywood" (76 likes), the 3,000-miles-from-the-sea error on Arizona's Guns, the wrong actor's photo on Petticoat, the wrong Packard engine. See section 4 for the confirmed errors.
8. **DON'T open with a ship résumé.** Flier spends 0:58–5:35 on its class and first patrol; PT-305 spends 2:05–5:50 on specs and torpedoes. Both flopped. Arizona's résumé lasts ~1 min and is turned into story (the band).
9. **DON'T put the comment CTA before the story has started.** FF puts it at 0:33 (Arizona), 0:32 (PH-8), 0:36 (Flier) and 1:36 (PT-305). It interrupts the hook at the riskiest retention point. The comments come anyway; ask at the first emotional peak instead (EST, retention data not available).
10. **DON'T leave third-party credits and watermarks visible.** Flier shows "courtesy of yap films" over documentary footage on 7 shots, and a bamboo-raft clip with an unrelated YouTuber's on-screen credits. One thumbnail still carries the Gemini watermark.
11. **DON'T let AI thumbnails show the wrong ship.** The D-Day thumbnail drew "The thumbnail of Nelson and Rodney was rubbish. B turret superfiring." The PH-8 thumbnail shows Iowa-like modern battleships, not the 1941 ships.
12. **DON'T publish on Wednesday until our own data says otherwise.** FF's 13 Wednesday uploads: median 3,019, 0 hits.
13. **DON'T follow a hit with a "how/why" history explainer.** "How the USS Missouri Made Japan Surrender" came 2 days after the Iowa hit (241K) and got 1,732. The momentum didn't transfer to a different promise.

---
## 2. Full video list analysis

### 2a. Eras: the channel changed format on 2026-07-05

| Era | Dates | n | Mean length | Uploads/week | Median views | Mean | ≥100K | <5K |
|---|---|---|---|---|---|---|---|---|
| A: "Why is X still there?" | Mar 3 – Jun 30 | 46 | 9.9 min | 3.0 (June: 4.2) | 5,367 | 61,235 | 8 | 22 |
| B: "Where is X now?" + roll-calls, longer | Jul 5 – Nov 2 | 42 | 17.2 min | 2.8 | 15,442 | 104,147 | 8 | 11 |
| B, only videos ≥21 days old | | 32 | | | 20,101 | 118,586 | 7 | 8 |

By month [VQ-ids]:

| Month | Uploads | Median | Mean length | ≥100K |
|---|---|---|---|---|
| Mar | 4 | 126,885 | 11.3 | 2 |
| Apr | 11 | 8,400 | 10.2 | 3 |
| May | 13 | 4,762 | 10.3 | 2 |
| Jun | 18 | 3,347 | 9.2 | 1 |
| Jul | 4 | 147,557 | 16.8 | 3 |
| Aug | 13 | 14,828 | 15.9 | 2 |
| Sep | 12 | 20,101 | 19.2 | 2 |
| Oct | 12 | 13,234 | 17.0 | 1 |

**What changed on 2026-07-05**
- Length roughly doubled, from ~9–10 to 16–18 min.
- Titles moved from "Why is X Still There" to "Where Is X Now" and "Where Are All N X Now".
- Uploads dropped from near-daily to ~3 a week.
- Thumbnails kept the same AI-aerial and yellow-text template; early ones also used dark underwater scenes, such as Bismarck "ILLEGAL TO TOUCH" and Shinano "FORBIDDEN TO SEARCH".
- Descriptions, sources and auto-chapters stayed the same.

**Subscriber growth comes in steps tied to hits** [VQ-ch]:
- Apr 16–20: Shinano, +~900.
- May 18–23: Missouri next to Arizona, +~1,000.
- Jul 8–11: PH-8, 7.6K to 9.1K.
- Aug 5–10: Iowa.
- Sep 15–25: Arizona, 13.2K to 14.3K.
- Oct 23–25: Petticoat.
- Between hits subs are flat; Oct 1–20 stayed at 14.4–14.6K.
- Subs per view is 0.21%, which is low (EST: typical documentary channels run 0.5–1%). Hits bring cold viewers who don't subscribe.

### 2b. What predicts a hit (all 88 videos)

| Group | n | Median | Mean | ≥100K | <5K |
|---|---|---|---|---|---|
| **Film / celebrity link** (PT-109, PT-73, Petticoat, Mister Roberts, Run Silent) | 5 | **168,715** | 233,256 | 3 | 1 |
| **Japanese ships** (Nagato, Yamato, Shinano, Musashi, Taiho...) | 6 | **100,538** | 120,098 | 3 | 1 |
| **PT boats** | 4 | 110,875 | 193,199 | 2 | 1 |
| "Can Never Be Raised/Recovered" | 4 | 55,452 | 317,795 | 1 | 1 |
| "Where Are All N [class] Now" | 11 | 38,146 | 118,795 | 2 | **0** |
| Pearl Harbor / Arizona cluster | 13 | 34,276 | 226,267 | 5 | 3 |
| Battleships / classes (any) | 20 | 27,728 | 91,291 | 4 | 3 |
| Listicles ("7 Deepest", "5 Sunken Warships You Can See") | 5 | 53,035 | 54,693 | 1 | 1 |
| "Why is X Still [There/Missing/...]" | 30 | 13,567 | 88,671 | 8 | 11 |
| **"Where Is X Now" (single ship)** | 18 | **8,349** | 76,277 | 3 | 8 |
| German ships | 7 | 11,172 | 89,738 | 1 | 3 |
| **Submarines** | 10 | **3,202** | 53,612 | 1 | 6 |
| "They Located X After N Years — This Is What They Found" | 3 | 4,526 | 15,928 | 0 | 2 |
| Other / one-off templates (U-Boat life, John Burke, WTC ship, Andrea Doria...) | 17 | **3,695** | 15,219 | 1 | 10 |

| Length | n | Median | ≥100K |
|---|---|---|---|
| <10 min | 27 | 6,717 | 5 |
| 10–15 | 27 | 5,979 | 3 |
| **15–18** | 21 | **14,828** | **6** |
| 18–21 | 10 | 14,922 | 1 |
| 21+ | 3 | 92,387 | 1 (Arizona) |

| Gap since previous upload | n | Median |
|---|---|---|
| <1.5 days | 26 | **5,671** |
| 1.5–2.5 days | 31 | 13,033 |
| 2.5–4 days | 18 | 13,794 |
| 4+ days | 12 | 12,280 |

| Title length | n | Median | ≥100K |
|---|---|---|---|
| <40 chars | 31 | 14,144 | 7 |
| 40–49 | 29 | 10,459 | 6 |
| 50–59 | 20 | 11,599 | 2 |
| 60+ | 8 | 8,604 | 1 (Petticoat) |

Momentum: the video after a ≥100K hit had a median of 9,429 (n=16). The video after a <5K flop had a median of 5,675 (n=32). There is a little carry-over, much less than topic choice.

**Conclusion: ship fame plus a twist answer explains most of the variance.** Length helps at 15–18 min. Gaps under 1.5 days hurt. Submarines (except movie subs) and obscure ships fail. Japanese super-ships and Pearl Harbor work. Title and thumbnail scores do not discriminate (see section 3).

### 2c. Every video (chronological) [VQ-ids, 2026-11-04]
Views/day = lifetime views / days since publishing (unfair to old videos, since views die after ~4 days).

| # | Published | Title | Len | Views | Views/day | Likes % | Template |
|---|---|---|---|---|---|---|---|
| 1 | 2026-03-03 Tue | Why Was Prinz Eugen Left to Rot | 13:43 | 14,144 | 57 | 2.7 | Why is X Still ... |
| 2 | 2026-03-04 Wed | Why Is USS Saratoga Still Underwater | 12:36 | 30,368 | 124 | 2.9 | Why is X Still ... |
| 3 | 2026-03-05 Thu | Why is the Nagato Battleship Still There | 9:56 | 223,402 | 917 | 3.3 | Why is X Still ... |
| 4 | 2026-03-29 Sun | Why is USS Arizona Still Leaking Oil | 8:56 | 266,731 | 1,213 | 1.5 | Why is X Still ... |
| 5 | 2026-04-01 Wed | Why Nobody Came When the USS Indianapolis Sank | 13:43 | 3,019 | 14 | 3.4 | Other |
| 6 | 2026-04-03 Fri | Why is the Bismarck Still There | 8:41 | 583,193 | 2,717 | 1.2 | Why is X Still ... |
| 7 | 2026-04-05 Sun | Why is the USS Cyclops Still Missing After 100 Years | 10:22 | 13,033 | 61 | 2.5 | Why is X Still ... |
| 8 | 2026-04-07 Tue | Why is USS Arkansas Battleship Still There | 9:22 | 54,025 | 256 | 2.0 | Why is X Still ... |
| 9 | 2026-04-10 Fri | Why is the Yamato Battleship Still There | 11:08 | 192,676 | 927 | 2.0 | Why is X Still ... |
| 10 | 2026-04-14 Tue | Why the Musashi Battleship Was So Hard to Sink | 9:19 | 8,400 | 41 | 3.1 | Other |
| 11 | 2026-04-17 Fri | Why is the Shinano Still Missing | 10:19 | 289,011 | 1,441 | 2.0 | Why is X Still ... |
| 12 | 2026-04-20 Mon | Tirpitz: The Most Hunted Battleship of World War II | 10:26 | 2,146 | 11 | 3.4 | Other |
| 13 | 2026-04-23 Thu | Why is the USS Scorpion Still Classified | 9:30 | 6,717 | 35 | 2.8 | Why is X Still ... |
| 14 | 2026-04-27 Mon | What They Still Won’t Tell You About the USS Thresher | 11:12 | 3,424 | 18 | 3.2 | Other |
| 15 | 2026-04-30 Thu | Why is the SS Richard Montgomery Still Full of Bombs | 8:01 | 1,999 | 11 | 1.9 | Why is X Still ... |
| 16 | 2026-05-05 Tue | Why is HMS Hood Still Unsalvaged | 8:40 | 4,179 | 23 | 3.0 | Why is X Still ... |
| 17 | 2026-05-12 Tue | Life on a U-Boat was Horrifying | 10:54 | 583 | 3 | 4.6 | Other |
| 18 | 2026-05-17 Sun | Why is the USS Johnston Still There | 11:31 | 1,816 | 11 | 3.2 | Why is X Still ... |
| 19 | 2026-05-18 Mon | Why Is the USS Missouri Still Next to the USS Arizona | 8:13 | 405,268 | 2,387 | 2.4 | Why is X Still ... |
| 20 | 2026-05-20 Wed | Why is the USS Utah Still Leaking Oil | 9:28 | 4,762 | 28 | 3.1 | Why is X Still ... |
| 21 | 2026-05-21 Thu | Why Are 2 WWII Submarines Still Sitting on a Scottish Beach | 9:57 | 53,783 | 323 | 1.6 | Why is X Still ... |
| 22 | 2026-05-22 Fri | Why Is the USS Nevada Still Forgotten | 11:33 | 4,505 | 27 | 2.9 | Why is X Still ... |
| 23 | 2026-05-23 Sat | Why Is There a Car Still Inside the USS Yorktown | 12:24 | 1,085 | 7 | 3.5 | Why is X Still ... |
| 24 | 2026-05-26 Tue | Why Is The IJN Taiho Still Missing | 12:10 | 5,371 | 33 | 1.8 | Why is X Still ... |
| 25 | 2026-05-27 Wed | Why Is The USS Wasp Still At The Bottom Of The Ocean | 9:41 | 10,165 | 63 | 1.3 | Why is X Still ... |
| 26 | 2026-05-28 Thu | They Located USS Harder After 80 Years — This Is What They Found | 8:29 | 40,597 | 254 | 1.4 | They Located X ... This Is What They Found |
| 27 | 2026-05-29 Fri | They Located USS Lexington After 76 Years — This Is What They Found | 9:43 | 4,526 | 29 | 2.0 | They Located X ... This Is What They Found |
| 28 | 2026-05-30 Sat | 5 Sunken Warships You Can See Without Going Underwater | 10:41 | 116,276 | 738 | 1.1 | Listicle (N ships) |
| 29 | 2026-06-04 Thu | Why is the USS Constitution Still in Service | 8:12 | 2,831 | 19 | 1.8 | Why is X Still ... |
| 30 | 2026-06-05 Fri | The 7 Deepest Warship Wrecks Ever Found | 12:19 | 93,562 | 617 | 1.5 | Listicle (N ships) |
| 31 | 2026-06-06 Sat | SS John Burke: The Liberty Ship That Vanished in 3 Seconds | 10:32 | 824 | 5 | 3.4 | Other |
| 32 | 2026-06-07 Sun | 5 Sunken WWII Ships That Could Still Explode Today | 10:58 | 5,979 | 40 | 1.3 | Listicle (N ships) |
| 33 | 2026-06-08 Mon | Why No One Is Allowed Near the Deadliest Shipwreck in History | 8:14 | 16,449 | 111 | 2.7 | Other |
| 34 | 2026-06-09 Tue | Why This WW2 Shipwreck Is Worth Trillions | 9:04 | 3,000 | 20 | 2.5 | Other |
| 35 | 2026-06-10 Wed | Why Is the Scharnhorst Illegal to Salvage | 10:00 | 2,831 | 19 | 2.4 | Why is X Still ... |
| 36 | 2026-06-11 Thu | Why Divers Keep Dying Inside the Andrea Doria | 10:02 | 5,364 | 37 | 1.5 | Other |
| 37 | 2026-06-12 Fri | Why Are the Bikini Atoll Shipwrecks Still There | 8:06 | 291,175 | 2,013 | 1.3 | Why is X Still ... |
| 38 | 2026-06-13 Sat | Nobody Expected to Find a Ship Beneath the World Trade Center | 8:06 | 1,381 | 10 | 3.8 | Other |
| 39 | 2026-06-15 Mon | Why Nobody Will Ever Raise the Edmund Fitzgerald | 8:18 | 3,695 | 26 | 2.1 | Other |
| 40 | 2026-06-16 Tue | Why Are the Truk Lagoon Shipwrecks Still There | 8:08 | 2,999 | 21 | 1.8 | Why is X Still ... |
| 41 | 2026-06-17 Wed | Why Are the Bikini Atoll Shipwrecks Still Radioactive | 8:28 | 661 | 5 | 4.4 | Why is X Still ... |
| 42 | 2026-06-19 Fri | Why the USS Thresher Can Never Be Recovered | 8:32 | 1,204 | 9 | 4.2 | Why X Can Never Be Raised |
| 43 | 2026-06-20 Sat | Why America Can't Get Its Own Warship Back From North Korea | 8:38 | 4,647 | 34 | 1.1 | Other |
| 44 | 2026-06-22 Mon | Why Is USS Oklahoma Still So Hard to Find | 8:23 | 18,263 | 136 | 1.7 | Why is X Still ... |
| 45 | 2026-06-28 Sun | Why Is the Graf Spee Still in a South American River | 9:26 | 14,102 | 110 | 2.1 | Why is X Still ... |
| 46 | 2026-06-30 Tue | Divers Went Inside the SS Thistlegorm After 85 Years — This Is What They Found | 9:57 | 2,661 | 21 | 1.6 | They Located X ... This Is What They Found |
| 47 | 2026-07-05 Sun | Why are the Midway Shipwrecks Still There | 18:08 | 141,658 | 1,164 | 1.0 | Why is X Still ... |
| 48 | 2026-07-07 Tue | Where Are All 8 Pearl Harbor Battleships Now | 16:28 | 769,236 | 6,431 | 1.4 | Where Are All N / class Now |
| 49 | 2026-07-10 Fri | Why Can't You Visit the USS Utah | 15:44 | 153,457 | 1,317 | 1.3 | Other |
| 50 | 2026-07-29 Wed | Where Are Pearl Harbor's Surviving Ships Now | 16:40 | 10,459 | 107 | 2.1 | Where Is X Now |
| 51 | 2026-08-03 Mon | Where Are All 4 Iowa-Class Battleships Now | 15:36 | 241,065 | 2,605 | 1.2 | Where Are All N / class Now |
| 52 | 2026-08-05 Wed | How the USS Missouri Made Japan Surrender | 17:35 | 1,732 | 19 | 3.1 | Other |
| 53 | 2026-08-08 Sat | Where Are All 4 South Dakota-Class Battleships Now | 14:47 | 38,146 | 436 | 2.0 | Where Are All N / class Now |
| 54 | 2026-08-11 Tue | Where Are the North Carolina-Class Battleships Now | 17:49 | 55,702 | 652 | 1.5 | Where Are All N / class Now |
| 55 | 2026-08-14 Fri | Where Are All 4 Colorado Class Battleships Now | 14:53 | 12,047 | 148 | 2.1 | Where Are All N / class Now |
| 56 | 2026-08-16 Sun | Where Is USS Texas Now | 13:34 | 35,364 | 443 | 1.3 | Where Is X Now |
| 57 | 2026-08-18 Tue | The 7 Most Powerful American Battleships | 17:50 | 4,614 | 59 | 2.0 | Listicle (N ships) |
| 58 | 2026-08-19 Wed | Where Is USS Wisconsin Battleship Now | 15:46 | 2,947 | 38 | 2.3 | Where Is X Now |
| 59 | 2026-08-22 Sat | Why Are the Savo Island Shipwrecks Still There | 15:42 | 14,828 | 201 | 0.8 | Why is X Still ... |
| 60 | 2026-08-24 Mon | Where Are All 5 Queen Elizabeth-Class Battleships Now | 14:09 | 31,311 | 438 | 0.8 | Where Are All N / class Now |
| 61 | 2026-08-26 Wed | Where Are All The Yorktown-Class Carriers Now | 16:38 | 13,168 | 189 | 1.0 | Where Are All N / class Now |
| 62 | 2026-08-28 Fri | Where Are All The Fletcher-Class Destroyers Now | 14:49 | 7,136 | 106 | 0.9 | Where Are All N / class Now |
| 63 | 2026-08-31 Mon | Where Is the Real PT-109 Now | 17:40 | 549,846 | 8,501 | 0.7 | Where Is X Now |
| 64 | 2026-09-02 Wed | Why Can't We Just Reactivate the Iowa-Class Battleships | 18:50 | 24,145 | 385 | 0.6 | Other |
| 65 | 2026-09-04 Fri | Where Is The Real USS Laffey Now | 16:36 | 6,240 | 103 | 0.6 | Where Is X Now |
| 66 | 2026-09-06 Sun | PT Boats You Can Still See Today | 19:56 | 53,035 | 906 | 1.0 | Listicle (N ships) |
| 67 | 2026-09-08 Tue | Why The Uss Arizona Can Never Be Raised | 21:48 | 1,159,072 | 20,475 | 0.4 | Why X Can Never Be Raised |
| 68 | 2026-09-10 Thu | Where Is the USS Essex Now | 24:27 | 92,387 | 1,692 | 0.8 | Where Is X Now |
| 69 | 2026-09-15 Tue | Where Is the Real PT-73 Now | 17:56 | 168,715 | 3,394 | 0.8 | Where Is X Now |
| 70 | 2026-09-18 Fri | Where Are All 50 Casablanca-Class Carriers Now | 20:37 | 16,057 | 344 | 0.6 | Where Are All N / class Now |
| 71 | 2026-09-21 Mon | Where Are the Alaska-Class Battlecruisers Now | 18:19 | 66,624 | 1,526 | 0.7 | Where Are All N / class Now |
| 72 | 2026-09-22 Tue | Why Is USS Indianapolis Still There | 16:24 | 4,551 | 107 | 1.2 | Why is X Still ... |
| 73 | 2026-09-26 Sat | Where Is USS Franklin Now | 19:04 | 12,761 | 329 | 0.6 | Where Is X Now |
| 74 | 2026-09-28 Mon | Where Is the USS Flier Now | 18:39 | 2,631 | 72 | 0.7 | Where Is X Now |
| 75 | 2026-09-30 Wed | Where Are Pearl Harbor's Shipwrecks Now | 17:16 | 1,931 | 56 | 1.2 | Where Is X Now |
| 76 | 2026-10-02 Fri | Where Is America’s Most Feared Submarine of WW2 Now | 21:34 | 2,981 | 91 | 0.7 | Where Is X Now |
| 77 | 2026-10-11 Sun | Why The USS Utah Can NEVER Be Raised | 16:44 | 99,732 | 4,194 | 0.4 | Why X Can Never Be Raised |
| 78 | 2026-10-13 Tue | Where Is the Real PT-305 Now | 18:37 | 1,202 | 55 | 0.9 | Where Is X Now |
| 79 | 2026-10-16 Fri | Why The Bismarck Can Never Be Raised | 18:37 | 11,172 | 592 | 0.2 | Why X Can Never Be Raised |
| 80 | 2026-10-18 Sun | Why They Refuse to Stop the Pearl Harbor Oil Leak | 18:04 | 13,787 | 822 | 0.3 | Other |
| 81 | 2026-10-20 Tue | Where Are All 7 D-Day Battleships Now | 17:35 | 56,256 | 3,825 | 0.3 | Where Are All N / class Now |
| 82 | 2026-10-22 Thu | Where Is the REAL Pink Submarine From Operation Petticoat Now | 15:44 | 422,162 | 32,932 | 1.0 | Where Is X Now |
| 83 | 2026-10-24 Sat | Where Is the Ship That Almost Killed President Roosevelt Now | 15:05 | 1,541 | 142 | 0.6 | Where Is X Now |
| 84 | 2026-10-25 Sun | Where Is Henry Fonda’s REAL Ship From Mister Roberts Now | 14:02 | 23,519 | 2,420 | 0.7 | Where Is X Now |
| 85 | 2026-10-26 Mon | Truman Used This Yacht as a Floating White House. So What Happened to It? | 17:13 | 12,682 | 1,465 | 0.7 | Other |
| 86 | 2026-10-28 Wed | Where Is the REAL Submarine From Run Silent, Run Deep Now | 14:26 | 2,039 | 305 | 1.1 | Where Is X Now |
| 87 | 2026-10-31 Sat | Where Are the USS Arizona’s Guns Now | 16:10 | 34,276 | 8,845 | 0.6 | Where Is X Now |
| 88 | 2026-11-02 Mon | Where Is the USS Kidd Now | 14:47 | 1,998 | 1,272 | 1.7 | Where Is X Now |

---

## 3. Packaging

### 3a. Title formulas (all 88)

| Formula | Example (views) | Notes |
|---|---|---|
| Why is [ship] Still There / Still Missing / Still Underwater | Bismarck 583K, Nagato 223K, Yamato 193K | Era A staple, 30 uses, median 13.6K |
| Why [ship] Can NEVER Be Raised | Arizona 1.16M, Utah 99K | Caps "NEVER" on Utah. Bismarck re-use got 11K. |
| Where Is the (REAL) [ship] Now | PT-109 550K, PT-73 169K, Petticoat 422K | "REAL" only works with a film/celebrity link. Without one: PT-305 1.2K. |
| Where Are All N [class] Now | PH-8 769K, Iowa 241K | Safest: no video under 5K |
| N [superlative] Warships... (listicle) | 5 You Can See Without Going Underwater 116K, 7 Deepest 94K | |
| They Located X After N Years — This Is What They Found | Harder 41K, Lexington 4.5K | Abandoned after 3 uses |
| Explainers ("How X Did Y", "Life on a U-Boat was Horrifying") | 583–1,732 | Every one flopped |

Style: title case is inconsistent ("Uss" in their top video). No years, no numbers except class counts, no brackets, no emojis. 68% of titles are under 50 characters.

### 3b. Thumbnails (20 viewed) [vidIQ get_images]
- **Every thumbnail is an AI-generated photoreal image.**
  - Mostly a drone aerial over turquoise water, or a ship at speed in heavy spray. Early videos also used dark underwater scenes with a sub's searchlight.
  - The ships are approximations: Iowa-style hulls used for the 1941 Pearl Harbor ships, a fake "SS-31" hull number on the pink sub, a wrong turret layout on Nelson/Rodney (viewer complaint).
  - The Shinano thumbnail still carries the **Gemini sparkle watermark** (bottom right).
- **Text**: one style throughout. Heavy condensed sans in **yellow with a black outline**, 2–4 words, upper left or top band.
  - The formulas are "N YEARS LATER", "WHERE IS IT NOW?", "WHY NOT RAISE IT?", "STILL RADIOACTIVE", "ILLEGAL TO TOUCH", "FORBIDDEN TO SEARCH", "STUCK SINCE 2024", "IT ENDED.", "WHY IN THE DESERT?".
  - Occasionally they add an inset photo (Arizona's Guns) or a red label box (John Burke "HIT BY KAMIKAZE", with an AI pilot face).
- **Palette**: teal/blue sea, yellow text, grey ship. No faces, maps, arrows or circles. No real photos, apart from one inset.
- **Accuracy issues**:
  - "83 YEARS LATER" on Wisconsin (commissioned 1944, so 82). EST
  - The Truman yacht thumbnail shows "U.S.S. WILLIAMSBURG" docked in front of the Capitol. In reality she was a wreck in Italy, and a commenter says "SHE'S BEEN SCRAPPED".
- The hits and the flops use **the same template**. Thumbnails are not what separates them.

### 3c. Scores [VQ-score]

| Video | Title score | Thumbnail score | Views |
|---|---|---|---|
| Why The Uss Arizona Can Never Be Raised | 89 | 77 ("too safe/generic", "busy") | 1,159,072 |
| Where Is the USS Flier Now | 87 | 89 ("follows high-performing patterns") | 2,631 |
| Where Is the Real PT-305 Now | 80 | 83 | 1,202 |

**Lesson for our PLAN:** our rule "3 titles ≥85 in vidIQ" is a floor, not a predictor. The topic gate (fame + twist) must come first.

---

## 4. The videos themselves

### 4a. Hooks (quoted from [TR])
- **Arizona (1.16M)**, 0:00–0:33: "Right now, at the bottom of Pearl Harbor, there is a battleship. It's been there since December 7th, 1941. It will still be there long after everyone watching this is gone. And the strangest thing about that is not why it sank. It's what happens every single time anyone seriously looks at the question of what it would take to raise it. Something stops them every time. The Arizona is not a mystery... It is something stranger than that. And the closer you look at it, the stranger it gets."
  - Then the CTA at 0:33: "drop a comment below and let us know where in the world you're watching from... if you or your family have any connection to the Arizona..."
- **PH-8 (769K)**, 0:00–0:32: "On the morning of December 7th, 1941, eight American battleships are sitting quietly in Pearl Harbor. Within 2 hours, every one of their stories will change forever. Most people know how the attack ended. Almost nobody knows what happened next. Some of these ships never left Pearl Harbor. Others came back from the bottom of the harbor to fight again. One survived two atomic bombs. Another vanished into the Pacific forever. By the end of this video, you will know what really happened to every battleship at Pearl Harbor."
  - Then a milestone thank-you and the CTA.
- **Flier (2.6K)**, 0:00–0:36: "USS Flier disappeared in less than 30 seconds... Of the 86 men aboard, only eight would eventually survive... For the next 65 years, nobody knew exactly where USS Flier was. One of her survivors spent decades trying to find her. He died before anyone could. Then, just 1 year later, divers found something sitting 330 ft beneath the sea."
  - This is a decent hook, but it **gives the answer away** and the ship is unknown.
  - At 0:58 it moves to "Gato-class... Electric Boat... launched July 1943".
- **PT-305 (1.2K)**, 0:00–1:34: a full biography summary that **reveals the ending at ~1:10** ("return to New Orleans, be rebuilt almost from the keel up"). The CTA comes at 1:36, then specs (78 ft, three Packards, 40 knots).

**Pattern:** hits use present tense, a big unanswered question and a list of teased twists. Flops tell the story in order and give the answer away.

### 4b. Structure, pacing, ending
- **Arizona structure** [VQ-watch]:
  - hook (0:52)
  - "Quiet Years" résumé (1 min)
  - Dec 7 (3 min)
  - aftermath, trapped men
  - salvage and memorial
  - wreck condition and oil
  - human remains and the law
  - comparison with Oklahoma
  - NPS "let nature take it"
  - answer and emotional close (bell)
  - end-screen pointer
  - Eight chapter cards (serif type on a dark band). The answer is spoken at ~19:50.
- **PH-8 structure**: a reveal ladder.
  - Arizona, then Utah, then Oklahoma ("here's the twist"), then WV/California/Tennessee/Maryland, then Surigao Strait (the payoff: "the ships Japan sank came back to win the last battleship duel"), then Nevada ("refused to die twice"), then Pennsylvania (nuked), then Missouri watching over Arizona.
  - A "here's the twist" or "that's where it gets strange" beat comes every ~1.5–2 min.
- **Flier**: in chronological order. It drags in the survival trek (8:00–11:30: generic island photos, static markers [VQ-watch]). The 3–4 photos of Flier repeat 10+ times.
- **PT-305**: the last ~4 min repeat the same points ("She survived... She survived... She survived"). It is padding.
- **Pacing**: average shot length ~3.2–4.5 s. Ken Burns moves on stills. Longest holds 5–7 s [VQ-watch].
- **Narration**: ~130 wpm. The script style uses lots of short declarative sentence fragments ("Still there. Still liquid."), a pattern typical of LLM-written scripts (EST).
- **Endings**: a one-sentence summary, then "If you want more stories... the next video is already on screen / that one is right here". No subscribe pitch in the body except the opening comment prompt and a "Like/Subscribe/Bell" animation (Arizona 0:33).

### 4c. Visual style, maps, sound, voice [VQ-watch]
- **Visual mix (Arizona)**:
  - archival photos ~35%, archival film/newsreel ~20%
  - modern drone/stock/tourist video ~25%
  - NPS/NOAA underwater and ROV ~15%
  - 2D graphics ~5% (animated counters such as "1,177 Men Died", lower-third pills, chapter cards)
  - **0% AI** inside the video.
- **Maps**: Arizona has 3 basic maps (an archival Pacific map, a satellite view of the harbour with fuel icons, a pin on Hawaii). There is **no Battleship Row mooring map**, even though the story turns on "moored behind Vestal". Flier uses more maps (Navy track charts, vector island hops), but they are static markers.
- **Sound**: a continuous ambient orchestral/synth bed, ducked. Sparse SFX (underwater bubbles, a low boom, a bell). One viewer asked: "Tell us why you felt this video required 'music'."
- **Voice**: British RP male, measured.
  - [VQ-watch] calls it human. The brief assumed ElevenLabs. Unresolved.
  - Pronunciation errors flagged by viewers: "Mokapu" said as "Mocha-pu".
  - The transcript renders the architect as "Priest" (Preis), likely a TTS or ASR issue.

### 4d. Fact-check: confirmed errors [TR] against [WEB]

| # | Video | Claim in video | Reality | Source |
|---|---|---|---|---|
| 1 | Arizona | The band played the Battle of Music Dec 6 and "came second"; next morning "most of them were dead" | The Arizona band **did not play on Dec 6** (they had already qualified and attended as spectators). **All 21** died. | ussarizona.org "Where they really were"; cpf.navy.mil band history |
| 2 | Arizona | "Close to a million gallons" of fuel aboard | **1.1–1.5 million gallons** (NPS archive: 1.4M; USNI: 4,630 tons, about 1.1M) | NPS (archived), USNI *Naval History* 2004 |
| 3 | Arizona | "A quart of oil seeps out every single day" | NPS/USGS figures: **2–9 quarts a day** (rising from ~1 qt in 1998 to ~9.5 qt in 2006) | NPS-linked studies via [WEB] |
| 4 | Arizona | Turret 3/4 guns "mounted in shore batteries... defending the island for the rest of the war" | **Battery Arizona was never completed or fired.** Battery Pennsylvania test-fired once, in Aug 1945, after the fighting had ended. | fortwiki Battery Arizona; ww2db |
| 5 | Arizona | "More than 30 men" interred in the wreck | **44** survivors interred (the last was Lauren Bruner, 2019). Technically "more than 30", but it undersells. | NPS USS Arizona Interments; wearethemighty |
| 6 | PH-8 | "Right next to the Arizona sits... the USS Utah... a few hundred yards from the memorial" | Utah lies on the **far (NW) side of Ford Island**. Vestal was next to Arizona. Five separate viewer corrections. | [CM]; NPS |
| 7 | PH-8 | "More Pearl Harbor battleships were killed by American nuclear tests than were sunk outright by the Japanese" | 2 (Nevada, Pennsylvania) against 2 permanently lost to the attack (Arizona, Oklahoma), or 3 if Utah counts. **False as stated.** | arithmetic from the video's own content |
| 8 | PH-8 | Lists Utah as one of the "8 battleships" | Utah was a demilitarised target ship (AG-16). The usual 8 are Arizona, California, Maryland, Nevada, Oklahoma, Pennsylvania, Tennessee, West Virginia (viewer comment). | [CM] |
| 9 | PT-109 | PT boats called "plywood" | Hulls were double-diagonal mahogany planking; only decks and superstructure were plywood (76-like correction). Footage at 14:49 shows a Liberty L-12, not the Packard 4M-2500. McMahon is called a radio operator; he was a motor machinist's mate. | [CM] (not independently verified, EST) |
| 10 | Arizona's Guns | The desert barrel is "3,000 miles from the sea" | Phoenix is ~350 miles from the Pacific (several corrections) | [CM] |
| 11 | Petticoat | A photo labelled as Tony Curtis | It is Richard Gilliland (who played the role in the TV series) | [CM] |

Checked and correct: 1,177 dead; 1,760-lb bomb at ~8:06; Isaac Kidd's ring fused to the bulkhead; Stratton (died 2020 aged 97); memorial dedicated 30 May 1962, 184 ft, architect Preis was interned; Lou Conter died April 2024 aged 102; Oklahoma sank under tow in May 1947; Nevada found in 2020 at >15,000 ft; Pennsylvania scuttled at Kwajalein in Feb 1948; Flier found in 2009 by YAP Films at ~330 ft.

Doubtful but not verified: Arizona "sank in 8 minutes 30 seconds"; the explosion "registered on seismographs"; "tapping sounds for 2 days" from Arizona (tapping is well documented for West Virginia and Oklahoma). **Error rate: roughly 1 material error per 4–5 minutes in the Arizona script. Viewers notice, but the errors don't hurt views.**

---

## 5. Audience [CM]

**Who they are (EST from comments):** older Americans and veterans; children and grandchildren of WWII sailors; Navy retirees who were stationed at Pearl Harbor; strong UK, Australian, German and Italian film-nostalgia viewers on Petticoat. Many date stamps ("I visited in 1976"; "I was 9 when PT-109 was in theaters").

**What they praise:** "well told story", "superb work", "I never knew this". Above all they post family stories, which are most of the top comments:
- Arizona: "My Grandfather is entombed in the USS Arizona" (208), "My namesake is entombed..." (323)
- PH-8: "My great uncle was Isaac C. Kidd" (516); a footlocker returned after California was raised (294)

**What they complain about**
1. **Factual errors and loose wording.** This is the main complaint: Utah location, plywood, 3,000 miles, wrong photos, wrong engine, "front to back? You mean bow to stern?", "the war was not 'just beginning' in 1941", "Some of the videos are incorrect and inaccurate".
2. Pronunciation of Hawaiian place names.
3. Music under narration (1 comment).
4. Wrong ship details in AI thumbnails (Nelson/Rodney).
5. **AI voice: no complaints found** among the ~400 threads read. The audience doesn't care, or can't tell.

**Owner engagement:** **0 owner replies, 0 pinned comments by the owner** in the ~400 threads read. Hundreds of veterans' family stories are left unanswered.

**Suspicious comments:** a competitor account, **@RevivetheFleetExplained**, and **@hloaha** post AI-written discussion-bait questions on FF's newest videos. They have tell-tale "?\" artifacts, for example "Was destroying a proven wartime submarine a practical military decision—or a…". Other clone channels are farming FF's comment sections.

**Free topic ideas from viewer requests and comments** (check against `research/TOPICS.md`; ★ = not yet done by FF and not in our avoid list):
- ★ **USS Nevada "should have been a museum ship"** (747 likes, the top PH-8 comment). FF only did "Why Is the USS Nevada Still Forgotten" (Era A, 4.5K). An angle like "The Navy Nuked Its Toughest Battleship, Then Torpedoed It" is strong.
- ★ **USCGC Taney**, the last ship still afloat from the Pearl Harbor attack (Baltimore museum).
- ★ **USS West Virginia**: "should have been saved"; Doris Miller; the men tapping inside until Dec 23.
- ★ **USS Vestal**, the repair ship beside Arizona.
- ★ **USS Ward**, which fired the first American shot (the midget sub found in 2002).
- ★ **PT-59**, Kennedy's second boat (Battleship Cove, Fall River).
- ★ The **pink-sub-in-Long-Beach story** ("a big part of the pink submarine story is missing").
- ★ **USS Houston / HMAS Perth**: a commenter's father survived Perth. This overlaps our TOPICS #17 (looted wrecks).
- ★ **USS Enterprise CV-6**: "20 battle stars, sold for scrap". FF did not cover this; our avoid list has "Enterprise", so check which Enterprise.
- ★ **USS Samuel B. Roberts**, the deepest wreck (Taffy 3, a sister story to our #9 Johnston).
- ★ **USS Balao's conning tower** in the Navy Museum; **Down Periscope** (our TOPICS #5 Pampanito, now confirmed by a commenter); **"The Wackiest Ship in the Army"** and **"Father Goose"** as more film-ship angles.
- ★ **Battery Pennsylvania / Battery Arizona**: a commenter works on the site. Good B-roll for an Arizona-adjacent video (but that would be a 10th Pearl Harbor video for FF).

---

## 6. Weaknesses and openings: what we can do better

| # | FF weakness (evidence) | Our move | Our tool |
|---|---|---|---|
| 1 | **Accuracy**: ~5 material errors in the Arizona script, 3 in PH-8; viewers correct them in the top comments (section 4d) | A fact sheet before the script: 3 independent checkers on official texts, a "Packaging TEST claims" table, and a pinned "Corrections & sources" comment | Fact-check loop (`reference/notes_battle_maps.md` §2, FACTCHECK_A/B/C format; CLAUDE.md "Fact sheet first") |
| 2 | **No real maps**: Arizona has no Battleship Row mooring map, although the story turns on "moored behind Vestal"; Flier's trek uses static pins | Every place or date gets a map: animated mooring diagrams, ship tracks, survivor routes, sea-floor depth | `map-kit/` + `scenes-src/example_route.js` (a self-drawing route = ship track), `G.ship`; re-grade `bake.py` for the sea floor |
| 3 | **Static, repeated stills**: Flier reuses 3–4 photos 10+ times; 5–7 s static holds | Hard cap of 6 s, film over photos, parallax on stills, a clip reused at most twice and 3+ min apart | `archive_shots.py` (push/pan, `parallax`, `frame`, date cards), `cut_clips.sh` NARA film, `restore_film.py` |
| 4 | **No explainer animation**: no bomb path into the magazine, no hull cutaway, no depth sense ("330 ft") | Show the mechanism: a depth gauge on each wreck, a cutaway of the flooding, an "options struck out" sequence for "why not raise it" (scrap / museum / reef / raise) | `anim_gauge` (depth), `anim_xray` (hull cutaway), `anim_options` (struck-out options) |
| 5 | **Answer given away / résumé openings** on flops | Line 1 = the stakes; the title promise spoken by 10–15 s, but the *full* answer held for the final act; no résumé in the first 2 min; a twist every ~90 s like PH-8 | CLAUDE.md hook rules; `research/PACKAGING_GUIDE.md` |
| 6 | **Comment CTA at 0:33 interrupts the hook** | Ask at the first emotional peak (~3–5 min), e.g. "If someone in your family served on her, tell us their name" | script template |
| 7 | **0 owner replies, 0 pins**, on an audience posting family stories | Reply to the top 20 family comments in the first 48 h; pin a sources/corrections comment; a "Your Family's Ship" community post asking for requests | engagement routine; vidIQ `generate_comment_replies` (draft only, human approves) |
| 8 | **0 Shorts** | Cut 2–3 Shorts per video (the twist moment: "one survived two atomic bombs") pointing to the long video | `captions-and-clipping` / `youtube-shorts` skills |
| 9 | **Weak playlists** (1 playlist) | Series playlists: "Pearl Harbor Ships", "Movie Ships", "Ships Sunk on Purpose", "Ghost Fleets", for session time | YouTube Studio (manual) |
| 10 | **Descriptions**: the source list names institutions but links nothing; chapters are auto-generated; no hashtags | Linked sources (NHHC/NARA item IDs), written chapters, 3 hashtags, an AI-voice disclosure line | `tools/build_publish_guide.py` |
| 11 | **AI thumbnails with the wrong ship** and one with a Gemini watermark; identical template for every video | A real archival photo cut out on a dark scene, 1–3 true words; one distinct accent colour (not yellow, so we stand apart in the sidebar); check at sidebar size | `video-thumbnail` skill + `tools/make_thumb.py` (Anton, white + one red word); PLAN "Thumbnail" rules |
| 12 | **Third-party footage with visible watermarks/credits** (YAP Films, a YouTuber's raft clip, AP newsreel) | PD/CC only, with every file logged; no TV-documentary footage | `CREDITS.md`, `MANIFEST.md` rules (CLAUDE.md "Rights") |
| 13 | **Sound**: one continuous ambient bed, few SFX | Layered sound design: hull groan, swell, explosions on cue, silence beats at the emotional peaks | `templates/mix_audio.py` (4 layers + ducking), `sfx_cues.py`, ElevenLabs SFX set |
| 14 | **Pronunciation** (Mokapu, Preis) | A pronunciation gate for every proper noun before the voice render | `tts/PRONUNCIATION.md`, `tools/tts_names.py` |
| 15 | **Topic over-mining**: 13 Pearl Harbor videos, falling returns (Shipwrecks 1.9K) | Own new clusters FF hasn't touched: sunk-on-purpose (Oriskany, SS United States), ghost fleets (Mallows Bay, Suisun), movie ships (Pampanito, Ranger, Bounty) | `research/TOPICS.md` |
| 16 | **Cadence swings** (4.2 a week in June gave a 3.3K median) | Steady 2–3 a week, never under 1.5 days apart; strongest videos back to back; never follow a flop with a key video | `research/DATA_RULES.md` rule 1 |
| 17 | **Few viewers subscribe** (0.21% subs/view) | A reason to subscribe: a recurring series promise ("every ship the Navy sank on purpose"), an end-screen series playlist | channel branding |

---

## 7. Risks seen

- **Copyright exposure (FF's, and a warning for us).**
  - Visible "courtesy of yap films" watermark on 7 Flier shots: commercial documentary footage.
  - An unrelated YouTuber's raft clip with on-screen credits.
  - AP/Movietone newsreel of the Oklahoma salvage.
  - NPS videos (public domain, fine).
  - No claims are visible from outside, but Content ID matches would show as lost revenue, not as public signals (EST).
  - **Our rule (PD/CC only, logged) avoids all of this.**
- **Demonetisation / inauthentic-content signals.**
  - Near-daily uploads in June (18 videos).
  - Template titles.
  - AI thumbnails with a leftover Gemini watermark.
  - LLM-style scripts.
  - The channel is still growing, so no visible penalty yet (EST). The June slump (median 3.3K) came while they ran the daily schedule.
- **Engagement anomaly.** Like rates fell from ~2.2% (Era A median) to ~0.8% (Era B). Arizona is at 0.36%. This matches broad Browse reach to older viewers (EST), not fake views: the day-by-day curves look organic and comments are long and personal.
  - vidIQ's daily channel series has one glitch: +537K views on 2026-09-09, when the per-video stats show Arizona at ~2K that day. Treat that point as a data artefact.
- **Comment hijacking.** Competitor clone channels post AI-written questions under FF's videos (@RevivetheFleetExplained). Expect the same under ours; don't do it ourselves.
- **Factual-error risk.** On war-grave topics, errors draw veterans' families' corrections. FF hasn't been hurt yet, but a big error on a grave story is a reputational risk.
- **Topic collision.** FF is fast and mines its own hits (Utah, Bismarck "Never Be Raised" follow-ups within ~5 weeks). Any movie-ship or Pearl Harbor idea we have is at risk of being taken. Ship first-to-market topics fast (TOPICS lesson 1).

---

## Critic review and final DO / DON'T

Reviewer: skeptical-strategist pass, 2026-11-04. Every number below was recomputed from `videos.json` (88 rows) with a fresh script. No new vidIQ credits were spent. Web checks: cpf.navy.mil band history, history.com, NPS 2004 administrative history, NPS 1996 Resources Management Plan, National WWII Museum, USNI *Naval History* Feb 2004, YouTube monetization-policy help page and YPP FAQ (July 2025).

**What holds up:** median 12,364; mean 81,716; top 5 = 48.4% of views; top 10 = 69.2%; 16 videos ≥100K. Film/celebrity n=5 median 168,715; "Where Is X Now" n=18 median 8,350; submarines n=10 median 3,202; Wednesday n=13 median 3,019 with 0 hits; Era A median 5,368 vs Era B 15,442 (≥21 days old: 20,101). The arithmetic is right. Several of the conclusions drawn from it are not.

### A. Disagreements (claim → evidence → correction)

| # | Claim in the report | What the raw data / sources show | Correction |
|---|---|---|---|
| 1 | "16 videos ≥100K produce 69% of views (top 10)" (DO #1) | Two numbers mixed up. Top 10 = 69.2%. The 16 videos ≥100K = **83.1%**. | The skew is even stronger than stated: 18% of uploads make 83% of views. The channel is a hit lottery. Plan for the median video (≈12K), not the mean. |
| 2 | **Gaps under 1.5 days hurt** (median 5.7K against 13K; DO #8, DON'T #6) | Confounded with the era. 22 of the 26 short-gap uploads are Era A. **Inside Era A: gap <1.5 d median 5,672, gap ≥1.5 d median 4,762.** No effect, the reverse if anything. Inside Era B only 4 videos had a short gap (median 8.6K). That is too few to test. | No measurable gap effect. Keep "never daily, 2–3 a week" because of the **inauthentic-content policy** and our production capacity, not because of FF's data. Confidence that gap affects views: low. |
| 3 | **15–18 min is the sweet spot** (DO #8) | Also an era artefact. Every 15–18 min video is Era B. Inside Era B: 15–18 min median 14,828 (n=21), 18–21 min 14,922 (n=10), 10–15 min 17,783 (n=8). That is flat. Meanwhile 5 of FF's 16 hits ran **under 10 min** (Bismarck 583K at 8:41, Missouri/Arizona 405K at 8:13, Bikini 291K at 8:06). | Length doesn't predict views in this data. Our 14–24 min choice is about RPM and watch time, which we can't measure from outside. State it as a business choice, not a finding. |
| 4 | **Format change on 2026-07-05 caused the improvement** (Era A 5.4K → Era B 20K) | At least 4 things changed at once: format/length, upload rate (June 4.2/wk → July 0.9/wk), **topic mix** (Pearl Harbor and famous US battleships: the PH cluster median was 18K in Era A and 67K in Era B), and channel size (7.6K → 15K subs). March, the first month, at 8–14 min, had a median of 126,885 (n=4). | We can't attribute the jump to format. The safest reading is that topic choice moved, and the Era B template happened to be applied to famous US ships. |
| 5 | **Film/celebrity link median 168,715** (DO #2) | n=5, and 2 of the 5 are PT boats (PT-109 = JFK, PT-73 = McHale's Navy TV). **Pure film ships (Petticoat, Mister Roberts, Run Silent) n=3: median 23,519**, 1 hit, 1 flop (2,039). Mister Roberts and Run Silent were 7–10 days old. Petticoat and Run Silent were both submarines from 1958–59 films, 6 days apart. | A movie link is a real but **noisy** lever: 1 in 3 for pure film ships. The median depends on whichever video lands 3rd. Confidence: low-medium. Use it only when the film is a household name AND the "where now" answer has a twist. |
| 6 | **"Where Is X Now" median 8.3K** (DON'T #1) | Weaker than it looks. Remove the film/PT titles and the remaining 13 have a **median of 2,981, 0 hits, 7 under 5K** (best: Essex 92K, Texas 35K, Arizona's Guns 34K). | Strengthen DON'T #1. Without a famous name or film link this template is a flop by default. Confidence: medium-high (n=13). |
| 7 | **Wednesday is bad** (DON'T #12) | The gap holds inside both eras: A Wed 3,890 vs 5,675 (n=6); B Wed 2,947 vs 31,311 (n=7). But **8 of the 13 Wednesday uploads are follow-ups to a recent hit or cluster**: Bikini Radioactive 5 days after Bikini, Missouri Surrender 2 days after Iowa, Wisconsin 16 days after Iowa, Iowa Reactivate, PH Surviving Ships, PH Shipwrecks, Utah Oil (2 days after Missouri/Arizona), Run Silent (6 days after Petticoat). The day is confounded with cannibalisation and with FF's habit of putting the weaker filler mid-week. YouTube has no weekday penalty mechanism, and we would launch with ~0 subscribers. | Treat it as a filler and cannibalisation effect, not a weekday effect. Don't make a weekday rule. Test our own schedule after 20 uploads. Confidence it's the day itself: low. |
| 8 | **"Packaging scores don't predict"** (DON'T #5) | 3 data points, all scored 77–89: a restricted range, and topic fame wasn't held constant. This shows that a high score doesn't rescue an obscure topic. It does not show that scores don't predict. FF used one thumbnail template for everything, so packaging hardly varied and its effect can't be measured from this channel at all. | "Scores are not sufficient" (fair). "Scores don't predict" (overreach). Keep our ≥85 floor and Test & Compare. Thumbnail quality is untestable from FF because FF never varied it. |
| 9 | **"Search volume does not decide it"** | 10 hand-picked extreme cases. Keyword choice was inconsistent ("uss arizona" against "pearl harbor shipwrecks"), and volumes were measured in Nov 2026, possibly inflated by FF's own hits (Arizona +78%). **Spearman rank correlation between search volume and views across those 10 = +0.41** (positive, n.s.). Missouri and Wisconsin flopped as cluster follow-ups. | Search volume isn't sufficient, and the hits are Browse/Suggested-driven, but the data lean positive. Don't drop keyword checks; use them as a tiebreaker. Confidence either way: low. |
| 10 | **"The outcome is binary and visible within 24 h"** | Their own #1 video contradicts this: Arizona had **2.1K on day 1**, the same as the flops (Wisconsin 1,773, Flier 609), then 23K on day 7 and 448K by day 13. | Don't kill or rework a video on day-1 numbers. Judge on day 7–14 (impressions, CTR and retention, which only *our* Studio will show). |
| 11 | **Hold the answer back / no résumé opening** (DO #5, DON'T #8) | n=4 transcripts (2 hits, 2 flops), fully confounded with fame (the flops were obscure ships). Arizona held its answer but was *slow* on day 1. We have no retention curves. | It's a reasonable craft rule and matches our CLAUDE.md hook rules, but FF's data doesn't prove it. Confidence: low (craft prior, not evidence). |
| 12 | **DO #7 "ask the comment CTA at 0:30–0:45" vs DON'T #9 "don't put the CTA before the story"** | The two items contradict each other. | Single rule: family-connection prompt at the first emotional peak (~3–5 min) plus a pinned comment. EST, no retention data. |
| 13 | **DON'T #3: reusing a hit's thumbnail layout caused the PT-305 flop** | n=1. The report itself says all hits and flops share one template. PT-305 flopped because it was obscure and a museum answer. | Drop it as a causal claim. (Still don't clone layouts, for the inauthentic-content reason in B5.) |
| 14 | **DO #9: pause after a flop streak** | n=1 anecdote. Utah's 99K came 1 month after Arizona's 1.16M, which still fed Suggested traffic, and Utah reused the Arizona template. | Low confidence. Not a rule. |
| 15 | **DO #1: pick ships a 60-year-old American knows** | Fame alone fails: Missouri (household name) got 1.7K, Wisconsin 2.9K, Indianapolis 3.0K and 4.6K. Non-US ships worked: Japanese ships n=6, median 100K; Bismarck 583K. And almost every proven name (Arizona, PT-109, Iowa, Missouri, Petticoat, Bismarck, Yamato...) is on **our avoid list** in TOPICS.md. | Redefine it as "famous **and** not yet covered, **and** the answer is surprising". For us the usable form is: the most famous still-untaken ships (TOPICS #1–#11), and be first. |
| 16 | **DO #10: "drone shots of the actual site"** | FF's ~25% modern drone/stock/tourist video is almost certainly not PD/CC; we can't fly drones; our rules allow PD/CC only. | Change to: DVIDS / NHHC / NOAA / NPS (federal = usually PD; check each item, since some NPS media is contractor-copyrighted), Wikimedia CC BY/BY-SA drone footage, and our own map/3D animation for "where it is now". |

**Fact-check spot-check (section 4d, Arizona video)**
- **#1 Band (real error, slightly misframed).** CPF Band history: Arizona's band placed **second on 22 Nov** in the semifinal; on 6 Dec several members only *attended*; **the entire band (21) was killed**. History.com: "Contrary to some reports, NBU 22 did not perform." So the "came second" detail is true but has the wrong date, and "most of them were dead" is wrong (all of them died). It's a common myth, which makes it an easy hit for commenters.
- **#4 Guns "defending the island for the rest of the war" (real error).** NPS 1996 plan: "Battery Arizona was never finished." NPS 2004 admin history and the National WWII Museum: Battery Pennsylvania was completed in Aug 1945 and test-fired once around VJ Day. Confirmed material error.
- **#2 "Close to a million gallons" and #3 "a quart a day" (downgrade both: imprecise, not material errors).** USNI 2004 gives 1.1M gallons and "about two quarts a day"; NPS measured ~1 qt/day in 1998 rising to ~9 qt in 2006; NPS/press now say "2–9 quarts". FF is at the low edge with outdated figures, but these are not falsehoods. The report's claim of "1 material error per 4–5 min" is therefore **overstated**. Two confirmed material errors in 21:48 (band, guns), plus the PH-8 errors (Utah location, "more killed by nukes"), is closer to the truth.

**Voice: ElevenLabs/TTS vs human RP. Evidence:**
- For a **human**: one AI watcher (vidIQ `video_watch`) said "human"; no viewer complaints about an AI voice; there's a milestone thank-you in PH-8 (but that's scripted, so weak). vidIQ's watcher is not a validated AI-voice detector, so this evidence is weak.
- For **TTS** (stronger):
  - (a) **The Era A descriptions are the narration script with numbers spelled out for a TTS engine**: "nineteen forty one" (Bismarck, Missouri, Utah), "twenty twenty-five" (Truk), "thousand and fifty five men" (Yamato), "seventy six years" (Lexington). That's ~30 of the 46 Era A descriptions, a classic TTS-normalisation artefact. A human narrator reads "1941" fine.
  - (b) Hawaiian place-name errors ("Mocha-pu") that a paid VO artist would usually check.
  - (c) The rest of the pipeline is visibly AI (Gemini-watermarked thumbnails, LLM-style script), at 2.5–4 long videos a week.
  - "Priest" for Preis is an ASR transcript error and proves nothing either way.
- **Verdict:** probably TTS (medium confidence).
- **What the user should do:**
  1. Download a 30–60 s clip and run it through ElevenLabs' AI Speech Classifier (free; it flags ElevenLabs-made audio).
  2. Listen for identical breath and prosody patterns repeated across videos.
  3. Whatever the result, the decision doesn't change: the audience showed **0 voice complaints in ~400 threads**, so a good British TTS voice plus a pronunciation gate is enough. Keep ticking "altered or synthetic: Yes" as CLAUDE.md says.

**Missing from the report**
- **(B1) YPP "inauthentic content" (renamed 15 Jul 2025).** Examples include "narrated stories with only superficial differences". Reviewers look at titles, thumbnails, descriptions, the most-viewed videos and the newest videos. FF's 18× "Where Is X Now" + 11× "Where Are All N X Now" + one thumbnail template + reused description formula is exactly the pattern reviewers sample, so copying FF's "safest" template wholesale is a monetisation risk for a new channel applying to YPP.
- **(B2) AI disclosure and thumbnails.** The disclosure label is for realistic synthetic *video* content. Thumbnails fall under the misleading-thumbnail / metadata rules instead. A photoreal AI ship that is the wrong ship (Nelson/Rodney, Iowa hulls for 1941) or in a false state (Williamsburg "docked at the Capitol") is a misleading-metadata risk as well as an accuracy one. Third-party sources say AI thumbnails need no disclosure; low confidence, so check YouTube's help page before launch.
- **(B3) Comment-farming clones** (@RevivetheFleetExplained) will target us too. Turn on held-for-review for links, reply to family stories, and never run the tactic ourselves.
- **(B4) Being first.** TOPICS.md lesson 1: clones of FF hits got 578 against 769K and 179 against 550K. That's the strongest topic signal we have, and the report's DO list leaves it out. FF publishes ~3 a week and mines its own hits within 5 weeks, so time-sensitive topics (SS United States sinking, Nov 12 2026) must ship before FF.
- **(B5) No CTR, impressions, retention or traffic-source data.** Every claim about hooks, CTAs, Browse vs Search and thumbnails is inference from views, likes and comments on one channel. Expect to overturn half of this with our own Studio data after ~20 uploads.
- **(B6) Survivorship and age bias.** 10 Era B videos are under 21 days old, and Kidd (2 days) and Run Silent (7 days) are in the medians. Views/day penalises old videos. All patterns are from n=88 on a single 8-month-old channel.

### B. Final DO list (≤12)

| # | DO | Data point | Confidence |
|---|---|---|---|
| 1 | **Choose topics on fame AND novelty AND a surprising answer.** Run the topic gate before any packaging work. | 16 of 88 videos = 83% of views. Famous-but-answer-known flops: Missouri Surrender 1.7K, Wisconsin 2.9K. | High (direction), medium (exact gate) |
| 2 | **Be first on a topic, and ship time-sensitive ones fast** (SS United States sinking 12 Nov 2026; Oriskany). | Clones of FF hits got 578 vs 769K and 179 vs 550K (TOPICS.md). FF re-mines its own hits within ~5 weeks. | High |
| 3 | **Use a roll-call or multi-outcome structure for famous groups** ("what happened to all N"), varied in wording and visuals each time. | "Where Are All N" n=11: median 38K, 0 under 5K; PH-8 769K. | Medium (n=11, all Era B, US battleships) |
| 4 | **Use a "why it can't be done" / impossibility angle on famous wrecks**, backed by the real legal or physical obstacle. | Arizona 1.16M, Utah 99K; but Bismarck re-use 11K, Thresher 1.2K (n=4). | Low-medium |
| 5 | **Use a film or celebrity bridge only when the film or person is a household name** and the "where now" answer has a twist. | Pure film ships n=3: Petticoat 422K, Mister Roberts 24K, Run Silent 2K. JFK's PT-109 550K. | Low-medium |
| 6 | **Go beyond US ships when the ship is legendary** (Japanese/German icons not yet taken). | Japanese ships n=6, median 100K; Bismarck 583K. | Medium |
| 7 | **Run a fact sheet with 3 checkers on official sources, and pin a sources/corrections comment.** | Confirmed errors (band, Battery Arizona, Utah location) are the top-liked factual replies; the Utah correction appeared ×5. | High (reputation); low (effect on views) |
| 8 | **Reply to family/veteran comments in the first 48 h.** | Top comments are family stories (516, 447, 323 likes); FF has 0 owner replies in ~400 threads. | Medium (cheap, positive; views effect unmeasured) |
| 9 | **Use PD federal media (NHHC, NARA, DVIDS, NOAA, NPS after checking each item's rights), CC BY drone footage, and our own maps/animations for "where it is now".** | FF shows YAP Films watermarks on 7 shots, plus a YouTuber's clip; our rights rule is PD/CC only. | High |
| 10 | **Vary the packaging and the script structure across videos.** Keep a style, but don't use one template for everything. | YPP inauthentic-content policy (Jul 2025) names "superficial differences"; reviewers sample titles, thumbnails, descriptions. | High (policy) |
| 11 | **Judge a video on day 7–14 with Studio CTR/retention, not on day 1.** | Arizona: 2.1K on day 1 (flop-level), 448K by day 13. | Medium |
| 12 | **Verify the thumbnail ship is the right ship, period and state.** Use an archival cut-out where possible, and check at sidebar size. | Nelson/Rodney turret complaint; Iowa hulls on 1941 ships; Williamsburg shown "at the Capitol"; Gemini watermark left on Shinano. | High (accuracy/policy) |

### C. Final DON'T list (≤12)

| # | DON'T | Data point | Confidence |
|---|---|---|---|
| 1 | **Don't use "Where Is X Now" for a ship without a famous name or film link.** | Without film/PT titles: n=13, median 2,981, 0 hits, 7 under 5K. | Medium-high |
| 2 | **Don't pick a ship whose answer is "a museum you can visit"** unless something dramatic happened there. | Wisconsin 2.9K, PT-305 1.2K, Kidd 2.0K; Texas (sank at berth, dry-dock rescue) 35K. | Medium |
| 3 | **Don't make a 2nd–4th video on the same harbour or cluster within ~3 months, or a mid-week filler follow-up to a hit.** | PH Shipwrecks 1.9K, PH Surviving Ships 10K; 8 of 13 Wednesday uploads were cluster follow-ups (median 3.0K). | Medium |
| 4 | **Don't copy FF's single title + thumbnail + description template at volume.** | 29 videos on two title templates and 1 thumbnail style; inauthentic-content review samples exactly this metadata. | High (policy risk) |
| 5 | **Don't upload daily or near-daily.** | Policy, plus capacity for the fact-check gate. FF's own data shows no clean gap effect (Era A: <1.5 d 5.7K vs ≥1.5 d 4.8K), so this is a policy rule, not a views rule. | High (policy), low (views) |
| 6 | **Don't ship a script with an unverified "famous fact".** Myths spread on war-grave topics. | Arizona band "played Dec 6" myth (History.com calls it out); "guns defended the island" (Battery Arizona never completed). | High |
| 7 | **Don't use photoreal AI ships that misrepresent the real ship, or leave tool watermarks.** | Viewer complaints on D-Day/Nelson; Gemini sparkle on the Shinano thumbnail. | High |
| 8 | **Don't use TV-documentary or other YouTubers' footage, even briefly.** | YAP Films credit visible on 7 Flier shots; third-party raft clip. | High |
| 9 | **Don't trust vidIQ title/thumbnail scores to rescue a weak topic.** | Flier thumbnail scored 89 and got 2.6K; Arizona scored 77 and got 1.16M (n=3). | Medium (as "not sufficient") |
| 10 | **Don't make weekday, length or gap rules from FF's data.** | Wednesday, 15–18 min and gap effects all vanish or are confounded once you split by era or by follow-up status (A2, A3, A7). | Medium |
| 11 | **Don't follow a hit with a "how/why" explainer of a different promise** — or any explainer title. | Missouri Surrender 1.7K (2 days after Iowa 241K); Era A "Other" explainers median 3.2K (n=12). | Medium |
| 12 | **Don't mispronounce names.** Gate every proper noun before the voice render, and don't publish a TTS voice without a listen-through. | "Mocha-pu" and other Hawaiian place names are the 2nd-most-common complaint. | Medium |
