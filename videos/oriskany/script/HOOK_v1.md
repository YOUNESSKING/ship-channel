# HOOK v1: "Why the Navy Sank Its Own Aircraft Carrier" (0:00–~0:46), for owner approval

Rebuilt from test v3's critiques (`test_v3/FIX_LIST.md` items 6–8, 9–11, 14, 16; `CRITIQUE_VISUAL.md` top 5).
Every fact is tagged to the three fact-checks in `research/`:
FC-A = `FACTCHECK_A_service.md` (row IDs as printed: A7, C7, D5 ...),
FC-B = `FACTCHECK_B_reef_pcb.md` (B1–B44 as printed),
FC-C = `FACTCHECK_C_sinking_today.md`. FC-C has no row IDs, so rows are counted in table order:
section A (sinking day) A1 date · A2 charges · A3 who · A4 weight · A5 10:25 · A6 37 min · A7 predicted 5 h ·
A8 stern first · A9 212 ft · A10 upright/bow south · A11 22.5 nmi · A12 24 mi · A13 26 mi · A14 coords · A15 Florida
ownership · A16 largest reef ship; section B (today) B1 deck 145–150 · B2 island 84 · B3 bridge · B4 settled 10 ft ·
B5 storms/Gustav · B6 list · B7 funnel casing · B8 don't enter · B9 technical dive · B10 4,200 trips · B11 $3.6M ·
B12 Guinness; section C (SS United States) C1 990 ft · C2 12 Nov 10 a.m. · C3 ceremony · C4 tow · C5 site · C6 depth ·
C7 no explosives · C8 lawsuit · C9 $1M · C10 budget · C11 13 nmi · C12 no news change; E1–E5 = the five narration
sentences in section E; D1 = Titanic.
FOOT = `footage/FOOTAGE_LIST.md` (beat # / row #). Tags are stripped for TTS.

**Say it right (Kokoro check before voicing, `tts/PRONUNCIATION.md`):** Oriskany = or-ISS-kuh-nee (Kokoro
tends to say or-iss-KAY-nee; add exact phonemes if the respelling fails).

**Publish deadline:** by 11 Nov 2026. The SS United States line is in the future tense and dated "November twelfth"
(no "this month" / "next week"), so it stays true whichever day before the 12th we publish (FC-C C2, C12).

## Narration (≈108 words, ≈44–46 s at Kokoro ≈150–155 wpm with the two pauses)

1. Right now, two hundred and twelve feet under the Gulf of Mexico, lies an aircraft carrier. [FC-C A9]
2. No enemy sank her. The United States Navy did. On purpose. [FC-C A3, A16]
3. Navy demolition divers set off twenty-two charges inside the USS Oriskany. [FC-C A2, A3, E1] *(0.5 s pause for the boom)*
4. Thirty-seven minutes later, she was gone. [FC-C A6, E2]
5. Getting her ready to sink took over three years and about twenty million dollars. [FC-C E4; FC-B B15]
6. So why pay millions to put a carrier on the sea floor? [FC-B B15]
7. Why not keep her? Why not scrap her? *(speed 0.88, short gaps)*
8. The answer is buried in her past. And in what was still inside her when she sank. [FC-B B18]
9. And it matters right now. [FC-C C2]
10. On November twelfth, the ocean liner SS United States is scheduled to follow her down. [FC-C C2]
11. About thirteen nautical miles away. [FC-C C11]

Checks: line 1 = the stakes in present tense; first wow (the blast) on screen at ~3 s; the title promise ("the
United States Navy did. On purpose.") is spoken by ~10–11 s; the SS United States is named (FIX 7); no "for the very
same reason" (FIX 8); no ship résumé, no 1960s film except the one earned "No enemy sank her" cut; the answer (PCBs
+ reef economics) is not given; longest sentence 16 words; numbers spelled as spoken; no parentheses.

## Shot plan (times are estimates; re-time on `words.json` after the voice take)

Rules applied: frame 0 is a map (clean, nothing else on it); nothing on screen before its word; one big card at a
time; a change every 1.5–4 s, no shot over 6 s; labels ≥ 3.5 % frame height on a scrim, above the bottom 10 %;
one grade (2006 photos neutral, no sepia; film `GRADE=none`); real recorded SFX only (FIX 4).

| t (s) | words | picture | card / sound | source |
|---|---|---|---|---|
| 0.0–2.9 | "Right now, two hundred and twelve feet under the Gulf of Mexico," | [MAP] continuous dive: Gulf of Mexico → Pensacola → the wreck pin (FWC coords 30°02.555′N 87°00.397′W), camera drops below the surface, a depth line falls | "212 FT" slams on "feet" (~1.9 s), soft hit; underwater bed starts | FC-C A9, A14; existing `dive.mp4` |
| 2.9–5.6 | "lies an aircraft carrier." | **WOW 1:** [PHOTO: NARA 6698618, aerial port bow as the charges explode] hard cut, slow push-in, held 2.7 s | real explosion recording, peak on the cut (≤ 2 frames after onset) | FOOT b8 #5 |
| 5.6–6.4 | (breath) | [PHOTO: NARA 6698619, smoke drifting aft] | — | FOOT b8 #6 |
| 6.4–8.0 | "No enemy sank her." | [FILM: 428-NPC-37479 A-4 "314" on the catapult, Oct 1966] (only 1960s shot in the hook) | real catapult recording, cut to 1.25 s so it ends on the cut | FOOT b3 #1 |
| 8.0–10.0 | "The United States Navy did." | [FILM: 428-NPC-37453 island "34"] (trim head +0.15 s so the S-2 "13" never shows) | — | FOOT b3 #6 |
| 10.0–11.3 | "On purpose." | [PHOTO: NARA 6698627, the boil of foam] | "ON PURPOSE." snaps in on "purpose" (0.1 s scale 1.15→1.0), slam | FOOT b8 #17 |
| 11.3–13.0 | "Navy demolition divers set off" | [PHOTO: NARA 6698576, EOD sailor spools det cord, 13 May 2006] | small tag "NAVY EOD · MAY 2006" after "divers" | FOOT b6 #17 |
| 13.0–14.6 | "twenty-two charges" | [PHOTO: NARA 6698573, EOD sailors inside the hull] | "22 CHARGES" lands on "twenty-two" | FOOT b6 #16; FC-C A2 |
| 14.6–16.2 | "inside the USS Oriskany." | [PHOTO: NARA 6698609, SH-3 circling the stripped hulk, 17 May 2006] | name plate "USS ORISKANY" on "Oriskany"; date "17 MAY 2006" in the plate's subline (the date sits on the blast-day image, FIX 6) | FOOT b8 #1 |
| 16.2–16.7 | (0.5 s pause) | [PHOTO: NARA 6698617, port side as the charges explode] | second real blast, in the clear | FOOT b8 #4 |
| 16.7–19.5 | "Thirty-seven minutes later," | one camera series, ~0.8 s each: [PHOTO: 6698610 stern going under] → [6698611 bow rising] → [6698612 steep angle] | "37 MINUTES" lands on "minutes" (no counter roll) | FOOT b8 #9–11; FC-C A6 |
| 19.5–21.0 | "she was gone." | [PHOTO: 6698624 bow vertical] → [6698626 only foam left] | low hull groan + water close | FOOT b8 #14, #16 |
| 21.0–23.6 | "Getting her ready to sink took over three years" | [PHOTO: NARA 6698569, worker cuts holes in the flight deck, 20 Apr 2006] (2006, never 1952 film: FIX 9) | "3+ YEARS" on "three" | FOOT b6 #14 |
| 23.6–25.8 | "and about twenty million dollars." | [PHOTO: NARA 6698553, Navy diver welds aboard, 18 Apr 2006], right third darkened behind the number | "≈ $20 MILLION" on "twenty" (no unspoken subline) | FOOT b6 #10 |
| 25.8–29.0 | "So why pay millions to put a carrier on the sea floor?" | [ANIM: sinking cross-section to scale: keel 212 ft, flight deck ~145–150 ft, island top 84 ft; gauge labelled "KEEL", starts at 0] | hull touchdown on "floor": silt puff, one impact | FC-C A9, B1, B2 (FIX 10) |
| 29.0–32.4 | "Why not keep her? Why not scrap her?" | [ANIM: options: "KEEP HER?" appears on "keep", "SCRAP HER?" on "scrap", over the dimmed cross-section; no box, no strike yet (the answer waits)] | two soft ticks | — |
| 32.4–34.6 | "The answer is buried in her past." | [FILM: 428-NPC-16662 Oriskany at anchor, 1952] (shows "her past"; no date label) | — | FOOT b2 #6 |
| 34.6–38.0 | "And in what was still inside her when she sank." | [ANIM: xray: real Essex-class profile drawn to Oriskany's lines, a scan beam sweeps, compartments glow one by one, one "?" tag; first frame complete, teal/gold map palette] | sonar ping at -12 dB, in a voice gap | FIX 12 |
| 38.0–39.6 | "And it matters right now." | [MAP: Gulf, the Oriskany wreck pin glowing] | — | FC-C A14 |
| 39.6–41.4 | "On November twelfth, the ocean liner" | [FILM: 428-NPC-39181 SS United States funnels, 1968] | real liner horn in the gap before "On" (signature sound, FIX A4) | FOOT b10 #2 |
| 41.4–43.8 | "SS United States is scheduled to follow her down." | [FILM: 428-NPC-39181 bow with "UNITED STATES" lettering] | name plate "SS UNITED STATES" (5 % height) on "United States"; "NOV 12" in its subline | FOOT b10 #3 |
| 43.8–46.0 | "About thirteen nautical miles away." | [MAP: zoom out from the Oriskany pin to the SS United States site (30°07.148′N 86°46.755′W), dashed line] | "13 NAUTICAL MILES" on "thirteen"; Pensacola inside frame from the start | FC-C C5, C11 |

Clip-reuse plan: the 1966 catapult and island films come back once in the Vietnam chapter (≥ 4 min later); the
sinking stills come back once in the sinking chapter (≥ 8 min later); nothing else from the hook is reused.

## For the test v4 build
- Use the shot table above as the cue list; time each card with `B.at` on the spoken word.
- "On purpose." keeps its slam card; the blast stills hold long enough to read (2.7 s for the first).
- MANIFEST.md rows needed for the films used here: 428-NPC-37479, 428-NPC-37453, 428-NPC-16662, 428-NPC-39181
  (with what each does NOT show, per FOOTAGE_LIST).
