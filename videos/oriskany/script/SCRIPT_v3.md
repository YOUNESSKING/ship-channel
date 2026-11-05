<!-- v3 (owner decision 2026-11-05, ending option A): three passages cut from the ending, see full/build/cuts_v3.json. Text otherwise = SCRIPT_v2. -->
# SCRIPT v2: "Why the Navy Sank Its Own Aircraft Carrier" (USS Oriskany)

Target ~16 min. Publish by **11 Nov 2026** (SS United States sinking is set for 12 Nov, 10 a.m., weather permitting).
Hook approved separately: `HOOK_v1.md` (owner gate). Shot-list gate before any render. Plain narration for Kokoro:
`NARRATION_v1.txt`.

## v2 changes (2026-11-04)
Chapter-2 cuts only, no new facts, to pull the reversal earlier: the 1953 deck-bomb paragraph, the "officially two
MiGs" sentence, the ordnance tonnage, Stockdale's Medal of Honor line, the Forrestal sentence, McCain's 23rd mission,
the 1967 air-wing losses, and the March 1976 homecoming line. Chapter times below are v1 estimates; the real times
are in `../full/chapters.json` (from the voice take).

## How to read this file
- Narration paragraphs are plain text. Every factual sentence ends with a source tag in brackets. Tags are stripped
 for TTS.
- `>` lines are the visual note for the paragraph above: [FILM: ...], [PHOTO: ...], [MAP], [ANIM: ...], [CARD: ...].
 FOOT bN #M = `footage/FOOTAGE_LIST.md` beat N, row M. Owner-download items are marked OWNER DL.
- Tag keys: **FC-A** = `research/FACTCHECK_A_service.md` (row IDs as printed: A3, C7, D6a ...). **FC-B** =
 `research/FACTCHECK_B_reef_pcb.md` (B1–B44). **FC-C** = `research/FACTCHECK_C_sinking_today.md`, rows counted in
 table order (no IDs printed there): A1 date, A2 22 charges, A3 Navy EOD, A4 >500 lb, A5 10:25, A6 37 min, A7 ~5 h
 predicted, A8 stern first, A9 212 ft, A10 upright bow south, A11 22.5 nmi, A12 24 mi, A13 26 mi, A14 coords, A15
 Florida ownership, A16 largest reef ship; B1 deck 145–150 ft, B2 island 84 ft, B3 bridge, B4 settled ~10 ft, B5
 storms/Gustav, B6 list, B7 funnel casing, B8 don't go inside, B9 technical dive, B10 4,200 trips, B11 $2.2M/$3.6M/67
 jobs, B12 Guinness; C1 990 ft, C2 12 Nov 10 a.m., C3 ceremony, C4 tow, C5 site, C6 180 ft, C7 no explosives, C8
 lawsuit, C9 $1M, C10 budget, C11 ~13 nmi, C12 no change; E1–E5 the narration sentences; D1 Titanic.
- Nothing marked WRONG or UNVERIFIED in the fact-checks is used. Left out on purpose: Vietnam battle-star count,
 fire injury number, "Soviet" MiG pilots, the 5° list, the "$92 million a year" claim, "only ship ever" (we say
 "first"), "fish are safe now", "Florida banned sinkings", "911 ft", Nimitz, Holden, mileage of the 1999 tow.

## Say it right (gate every name before voicing; add to `tts/PRONUNCIATION.md` and the video's `SAY` dict)
| Written | Say | Note |
|---|---|---|
| Oriskany | or-ISS-kuh-nee | Kokoro tends to say or-iss-KAY-nee; use exact phonemes if no respelling works |
| Pensacola | pen-suh-KOH-luh | |
| Stockdale | STOCK-dayl | |
| Okaloosa | oh-kuh-LOO-suh | |
| Bremerton | BREM-er-tun | check |
| Beaumont | BOH-mont | check |
| Corpus Christi | KOR-pus KRIS-tee | check |
| Escambia | es-KAM-bee-uh | check |
| Hanoi | ha-NOY | check |
| MiG | MIG (one word, not M-I-G) | |
| A-four | "A-four" (written so in NARRATION) | |

## Structure at a glance (twist / reveal every ~90 s)

| # | Chapter | Est. time | Twist / reveal that opens or closes it |
|---|---|---|---|
| 0 | Hook | 0:00–0:47 | Blast; "No enemy sank her..."; $20M just to get her ready; SS United States open loop |
| 1 | Nobody Wanted Her | 0:47–3:00 | Theme park in Tokyo Bay (1:27) · scrap buyer defaulted (1:44) · Pegasus paid double the appraisal and still failed (1:51–2:20) · dragged round South America (2:40) |
| 2 | The Mighty O | 3:00–6:52 | A WWII carrier that missed WWII (3:08) · MiG fight, Navy Cross 70 years later (3:36) · 1953 deck bomb (3:59) · Stockdale (4:30) · the fire (4:48) · family prompt at the first emotional peak (5:28) · McCain, one year to the day (6:02) |
| 3 | The Bargain | 6:52–9:00 | First warship offered (7:02) · PCBs in the wooden flight deck (7:43) · about 7x the money first committed (8:51) |
| 4 | Thirty-Seven Minutes | 9:00–10:27 | Five hours predicted, 37 minutes taken (9:50) · Guinness record (10:14) |
| 5 | The Fish Test (mid-video reversal) | 10:27–12:27 | 700 lb of PCBs left aboard (10:27) · EPA's first approval of its kind (10:52) · fish above screening values (11:25) · numbers fall, no advisory (12:00) |
| 6 | The Real Reason (final act: the answer) | 12:27–14:50 | Storms pushed her 10 ft into the seabed (12:43) · 97 % in the wiring = taking her apart (13:34) · MARAD warning (14:14) · **the answer (14:27)** |
| 7 | Ending | 14:50–15:38 | Only carrier ever reefed · SS United States, Nov 12, 10 a.m., 990 ft, no explosives, 13 nmi · Okaloosa paid toward the Oriskany and now takes her title · closing question |

Times are at 150 wpm with no pauses (2,344 words = 15:38). With the hook pauses and slower question blocks
(speed 0.88) the voice take should land at about 16:00–16:30. Re-time every chapter from `words.json`.

Wow every ~30 s in the first 3 min: blast 0:03 · sinking 0:17 · $20M 0:23 · SS United States 0:41 · mothball row at
Bremerton 0:55 · struck from the list 1:05 · Tokyo Bay theme park 1:27 · default 1:44 · Pegasus 1:51 · stalled at
Mare Island 2:15 · round South America 2:40 · launched after the surrender 3:08.

---

## 0. HOOK (0:00–0:47)

Right now, two hundred and twelve feet under the Gulf of Mexico, lies an aircraft carrier. [FC-C A9]

> [MAP] frame 0 = clean map dive, Gulf → Pensacola → wreck pin; "212 FT" on "feet". On "lies an aircraft carrier" hard cut to **WOW 1** [PHOTO: NARA 6698618 aerial, charges exploding] held 2.7 s, then [PHOTO: 6698619]. Full shot plan in `HOOK_v1.md`.

No enemy sank her. The United States Navy did. On purpose. [FC-C A3, A16]

> [FILM: 428-NPC-37479 A-4 "314" catapult, Oct 1966, FOOT b3 #1] → [FILM: island "34", FOOT b3 #6] → [CARD: "ON PURPOSE." slam over PHOTO 6698627 boil].

Navy demolition divers set off twenty-two charges inside the USS Oriskany. [FC-C A2, A3, E1] Thirty-seven minutes later, she was gone. [FC-C A6, E2]

> [PHOTO: 6698576 det cord, FOOT b6 #17] → [PHOTO: 6698573 EOD inside hull; CARD: 22 CHARGES] → [PHOTO: 6698609 SH-3 over hulk; name plate USS ORISKANY · 17 MAY 2006] → 0.5 s pause, [PHOTO: 6698617 blast] → [PHOTO: 6698610 → 6698611 → 6698612 → 6698624 → 6698626; CARD: 37 MINUTES on "minutes"].

Getting her ready to sink took over three years and about twenty million dollars. [FC-C E4; FC-B B15] So why pay millions to put a carrier on the sea floor? [FC-B B15] Why not keep her? Why not scrap her?

> [PHOTO: 6698569 deck cutting, 2006; CARD: 3+ YEARS] → [PHOTO: 6698553 welder; CARD: ≈ $20 MILLION] → [ANIM: sinking cross-section to scale] → [ANIM: options "KEEP HER?" / "SCRAP HER?", no box yet].

The answer is buried in her past. And in what was still inside her when she sank. [FC-B B18] And it matters right now. [FC-C C2] On November twelfth, the ocean liner SS United States is scheduled to follow her down. [FC-C C2] About thirteen nautical miles away. [FC-C C11]

> [FILM: 1952 at anchor, FOOT b2 #6] → [ANIM: xray profile, scan beam, one "?"] → [MAP: wreck pin] → [FILM: SS United States funnels, FOOT b10 #2; horn] → [FILM: bow lettering, FOOT b10 #3; name plate SS UNITED STATES · NOV 12] → [MAP: zoom out, both pins, CARD: 13 NAUTICAL MILES].

---

## 1. NOBODY WANTED HER (0:47–3:00)

Start with the day her service ended. In September nineteen seventy-six, the Navy decommissioned her. [FC-A D1] She was laid up at Bremerton, Washington, in a row of silent grey ships. [FC-A D1; FOOT b5 #2]

> [MAP: Bremerton, Puget Sound pin; date line SEPT 1976 on "September"] → [PHOTO: NARA 6450776 laid up at Bremerton, FOOT b5 #1 (not decommissioning day)] → [PHOTO: NARA 6450773 Hornet, Oriskany, Bennington in a row, 1990, FOOT b5 #2; arrow on the middle hull].

For thirteen years, she just waited. In July nineteen eighty-nine, she was struck from the Navy list. [FC-A D3] On paper, she was no longer a warship. [FC-A D3]

> [PHOTO: NARA 6450777 mothball row, 1990, FOOT b5 #3, slow push] → [CARD: STRUCK · JULY 1989 on "struck"].

A ship like that usually ends one of two ways. A museum, or a scrapyard. Four of her sisters would become museums. [FC-A D4b]

> [ANIM: options board returns from the hook: "MUSEUM?" on "museum", "SCRAPYARD?" on "scrapyard"; four small Essex-class silhouettes with "MUSEUM" tags on "four of her sisters"].

Then, in the early nineteen nineties, an offer came from across the Pacific. [FC-A D4] Japanese investors wanted her as the centrepiece of an attraction in Tokyo Bay. [FC-A D4] They called it City of America. [FC-A D4] An American warship, as a theme park in Japan. [FC-A D4] The money never came. [FC-A D4] And nobody else asked for her. [FC-A D4b]

> [MAP: Pacific, arc from Bremerton to Tokyo Bay; pin on "Tokyo Bay"] → [CARD: "CITY OF AMERICA" on its words, over the map] → [ANIM: "MUSEUM?" struck through on "never came"]. No photo exists of the plan: map only.

So the Navy tried the scrapyard. In the early nineteen nineties, she was sold for scrap. [FC-A D5] The buyer defaulted. [FC-A D5] She never even left Navy custody. [FC-A D5]

> [PHOTO: NARA 6450776 Bremerton, different crop] → [CARD: SOLD FOR SCRAP on "scrap"] → [CARD: DEFAULTED stamp on "defaulted"]. No date on screen (disputed 1993/1994).

In September nineteen ninety-five, a start-up scrap firm called Pegasus bought her for just over a million dollars. [FC-A D6a, D6b; safe 11] The Navy had appraised her at six hundred thousand. [FC-A D6a] Three companies had bid. [FC-A D6a] The deal said she had to be cut up in the United States. [FC-A D6a] A losing bidder protested, and the work was held up until that December. [FC-A D6a]

> [CARD: "$1.2 MILLION" lands on "million", then "APPRAISED $600,000" on "six hundred thousand" (a gold bracket between them)] → [MAP: Bremerton → San Francisco Bay tow line].

In nineteen ninety-six, she was towed down from Bremerton to San Francisco Bay. [FC-A D6c] Pegasus planned to break her up at the old Mare Island yard. [FC-A D6b] A year later, almost nothing had been cut. [FC-A D6c] The Navy ended the contract for default and took her back. [FC-A D6c]

> [MAP: tow line animates along the coast, pin "MARE ISLAND, VALLEJO" on "Mare Island"] → [CARD: DEFAULTED, second stamp, same style] → [ANIM: "SCRAPYARD?" gets a second strike]. No footage of the Mare Island period found: map + cards only.

Two scrap deals had collapsed. [FC-A D7] Two more attempts to sell her found no taker at all. [FC-A D7]

> [ANIM: tally board, four ticks, one per word group: 2 COLLAPSED · 2 NO TAKER].

So in nineteen ninety-nine, she was towed out of California. [FC-A D8] All the way around South America. [FC-A D8] To a reserve fleet at Beaumont, Texas. [FC-A D8] A ship nobody would take, dragged around a continent, to wait some more.

> [MAP: long tow line San Francisco → round Cape Horn → Beaumont, Texas, date line 1999; the camera follows the line, Beaumont pin on "Beaumont"]. No mileage on screen (unverified).

So what kind of ship ends up like this? To understand what was being thrown away, go back to the war she was built for. The one she missed.

> [PHOTO: NARA 6698587 veteran saluting the departing carrier, 15 May 2006, FOOT b7 #8 (CIV photographer: check rights before use; fallback PHOTO 6698588 crowd on the shore path)] → [FILM: 1945 launch newsreel, FOOT b1 #1] on "the war she was built for".

---

## 2. THE MIGHTY O (3:00–6:52)

Her keel was laid in Brooklyn in May nineteen forty-four. [FC-A A3] She was launched on the thirteenth of October, nineteen forty-five. [FC-A A4] Six weeks after Japan surrendered. [FC-A A4] A Second World War carrier that never fought in the Second World War. [FC-A A4]

> [MAP: New York Navy Yard, Brooklyn pin; date line MAY 1944] → [FILM: 208-UN-177 hull on the ways + crowd, FOOT b1 #1, #3 (not the 1950 commissioning)] → [CARD: "SIX WEEKS" on "six weeks", small subline "after Japan surrendered" only as spoken].

In August nineteen forty-seven, the work stopped. [FC-A A5] Then, in June nineteen fifty, war broke out in Korea, and the Navy rushed her to completion. [FC-A A6] She was the last Essex-class carrier ever finished. [FC-A A9] Her crews called her the Mighty O. [FC-A C17]

> [CARD: WORK STOPPED · AUG 1947] → [MAP: Korean peninsula, date line JUNE 1950] → [PHOTO: NH 97408 off New York, 6 Dec 1950, FOOT b1 #4, OWNER DL; fallback PHOTO NARA 7578420 aerial, FOOT b2 #20] → [CARD: "THE MIGHTY O" lower third on "Mighty O"].

On the eighteenth of November, nineteen fifty-two, four of her Panther jets met seven MiG-fifteens. [FC-A B2] One pilot, Royce Williams, was credited with one MiG at the time. [FC-A B3, safe 13] In twenty twenty-three, the Navy cited him for downing four. [FC-A B3] It upgraded his Silver Star to the Navy Cross. [FC-A B4]

> [MAP: off northeast Korea, date line 18 NOV 1952; four blue jet tracks vs seven red tracks, two red tracks end on "shot down"] → [FILM: F9F Panther on deck, FOOT b2 #1 ("early 1950s": no date label, no combat shown)] → [CARD: 1 → 4 on "one" and "four"] → [CARD: NAVY CROSS · 2023]. No dogfight footage exists: map animation only.

Then came Vietnam. Between May and December nineteen sixty-five, she flew more than twelve thousand combat sorties. [FC-A C2] A record for one carrier deployment at the time. [FC-A C2]

> [MAP: Gulf of Tonkin, Yankee Station, date line 1965] → [FILM: A-4 "314" catapult, FOOT b3 #1 (2nd and last use, >4 min after the hook); 1966 film, so no 1965 label] → [CARD: "12,000 SORTIES" on "twelve thousand"] → [FILM: A-4E bombs on the wing, FOOT b3 #9].

On the ninth of September, nineteen sixty-five, the man who led her air wing was shot down. [FC-A C1a] Commander James Stockdale's Skyhawk was hit by anti-aircraft fire over North Vietnam. [FC-A C1a] He was held prisoner for seven and a half years. [FC-A C1b]

> [MAP: North Vietnam, date line 9 SEPT 1965, a single track ends in a flash] → [FILM: A-4Es in flight, FOOT b3 #12 (not Stockdale's aircraft; no caption naming him)] → [CARD: name plate "CDR JAMES STOCKDALE" on "Stockdale" (no portrait in our PD list; add NHHC photo only if PD is confirmed)] → [CARD: "7½ YEARS" on "seven and a half"]. 

A year later, the danger came from inside the ship. [FC-A C3] On the morning of the twenty-sixth of October, nineteen sixty-six, she was on Yankee Station in the Gulf of Tonkin. [FC-A C3] Two sailors were stowing magnesium parachute flares. [FC-A C4] One went off by accident. [FC-A C4]

> [MAP: Yankee Station pin, date line 26 OCT 1966] → [ANIM: xray of the ship, forward hangar bay one glows; a small flare locker icon] → [FILM: crew pull hose lines, 26 Oct 1966, FOOT b4 #1]. The fire's origin is not on film: animation only, no reconstruction of people.

In a panic, a sailor threw the burning flare into a locker packed with about seven hundred more. [FC-A C4, C5; safe 3] They burn at about five thousand four hundred degrees Fahrenheit. [FC-A C6] The fire burned for about seven hours. [FC-A C9; safe 4]

> [ANIM: locker icon, "700" on "seven hundred", heat glow] → [CARD: "5,400°F" on "five thousand four hundred"] → [FILM: smoke pouring past the island, FOOT b4 #4] → [FILM: firefighters in the hangar, FOOT b4 #8] → [FILM: OBA team at a hatch, FOOT b4 #10]. The sailor is not named or shown.

Most of the dead were officers, many of them pilots, trapped in their staterooms by the smoke. [FC-A C10] The fire killed forty-four men. [FC-A C7; safe 1] Dozens more were hurt. [FC-A safe 2]

> [FILM: heavy smoke over the island, FOOT b4 #5] → [FILM: burned A-4E in the smoke, FOOT b4 #2] → [CARD: "44" on "forty-four", plain, no hit sound; music to the reflective pad]. No injury number on screen.

Eleven days later, her crew stood in formation for a burial at sea. [FOOT b4 #11–13 (NARA 428-NPC-37596, 6 Nov 1966)]

> [FILM: crew in whites, Marine colour guard, FOOT b4 #11 (SENSITIVE: memorial; no music hit, voice slow, hold ≤ 4 s)] → [FILM: crew in formation, destroyer escorts abeam, FOOT b4 #12]. Do NOT use the flag-draped remains photo (b4 #14).

Did you, or someone in your family, serve aboard the Oriskany? In that fire, or in any other year? Tell us their story in the comments. We read every one.

> [FILM: destroyer escorts in the sun glare, FOOT b4 #13, slow] with a small lower third "TELL US THEIR STORY" on "tell us their story". First emotional peak (~5:28): the single family/veteran prompt (study A12).

She was repaired in San Francisco and was back off Vietnam the next summer. [FC-A C11] On the twenty-sixth of October, nineteen sixty-seven, she launched a strike on Hanoi. [FC-A C12a] One year to the day after the fire. [FC-A C12a]

> [MAP: San Francisco → Gulf of Tonkin, date line 1967] → [FILM: island with A-4Es parked, FOOT b3 #8 (label "1967–68" or no year)] → [CARD: "ONE YEAR TO THE DAY" on its words, over the date line 26 OCT 1966 → 26 OCT 1967].

One of the pilots was Lieutenant Commander John McCain. [FC-A C12a] A surface-to-air missile tore the wing off his A-four Skyhawk. [FC-A C12a] He came down in a lake in the middle of the city. [FC-A C12b; safe 5] He was released in March nineteen seventy-three, after five and a half years. [FC-A C13; safe 6]

> [FILM: catapult launch, FOOT b3 #11 (aircraft type hard to read: no "McCain's jet" caption)] → [CARD: name plate "LCDR JOHN McCAIN · VA-163" on "McCain" (never VA-46)] → [MAP: Hanoi, the thermal power plant target, a missile track meets the jet track; zoom to Truc Bach Lake on "a lake in the middle of the city"] → [CARD: "5½ YEARS" on "five and a half"].

Two of America's best-known prisoners of war had flown from her deck. [FC-A C1a, C12a] Forty-four of her men had died in a single morning. [FC-A C7] And by the late nineteen nineties, nobody would pay to keep her, or even to cut her up. [FC-A D4, D7] Then, in two thousand three, Congress changed the rules. [FC-B B1]

> [FILM: 1969 aerial at speed, FOOT b3 #17, slow push] → [CARD: two name plates side by side, STOCKDALE · McCAIN, on "prisoners of war"] → [PHOTO: Bremerton mothball row, FOOT b5 #2, second use, >5 min after first] → [MAP: Washington, D.C. pin, date line NOV 2003 on "two thousand three"].

---

## 3. THE BARGAIN (6:52–9:00)

In November two thousand three, Congress gave the Navy the power to donate old warships to states as reefs. [FC-B B1] The Oriskany was the first warship the Navy offered. [FC-B B2]

> [MAP: D.C. → Gulf coast; the Oriskany icon moves from Beaumont to the Gulf] → [CARD: "FIRST" on "first"] over [PHOTO: NARA 6695641 rusting hull under tow at Pensacola, FOOT b6 #1].

Four bids came in, from five states. [FC-B B5] Florida, Mississippi, Texas, and Georgia with South Carolina. [FC-B B5] In April two thousand four, the Navy picked Florida as the best value. [FC-B B5] The plan was to sink her before the end of that summer. [FC-B B6] It would take two more years.

> [MAP: Gulf coast, the five states light up one by one on their names; Florida stays lit, date line APRIL 2004] → [CARD: "SUMMER 2004" on "summer", then struck on "two more years"].

First, she had to be cleaned. The work was done in Corpus Christi, Texas, and took eleven months. [FC-B B7] Congress had committed two point eight million dollars to the project. [FC-B B8] Two point one million of it was for removing contaminants. [FC-B B8]

> [MAP: Corpus Christi pin] → [ANIM: cost gauge (a column on the hull), "$2.8M" lands on "two point eight", "$2.1M CLEANUP" slice on "two point one"]. No 2004 cleanup footage in our PD list: map + gauge only (the 2006 Pensacola stills are final prep, not this work).

Then workers stripped the asphalt off her flight deck. [FC-B B9] The wood underneath was full of PCBs. [FC-B B9] The Navy blamed fluid from her catapults. [FC-B B9] Under the cleanup rules, material that contaminated had to come out, unless the EPA agreed otherwise. [FC-B B20] So the whole wooden deck came out. [FC-B B9]

> [ANIM: xray profile, flight deck layer peels: asphalt → wood glows amber on "PCBs"; catapult tracks highlighted on "catapults"] → [CARD: "PCBs" lower third, one italic word] → [PHOTO: NARA 6698558 technicians on the stripped deck, 2006, FOOT b6 #12 (2006 Pensacola, not the 2004 deck removal: no date caption that says otherwise)].

The cost of removing contaminants grew to more than seven point six million dollars. [FC-B B9] At least half of it went on that deck. [FC-B B9] On top of that, the Navy spent three point seven million on a computer model. [FC-B B14] Its job was to prove the PCBs left aboard were safe. [FC-B B14]

> [ANIM: cost gauge rises, "$7.6M" on "seven point six", half the column turns amber on "half"] → [ANIM: gauge adds "$3.7M MODEL" on "three point seven"].

From Texas, she was towed to Pensacola. [FC-B B10; FOOT b6 #1] Then came hurricane season. [FC-B B10] In June two thousand five, she was towed back to Texas to hide from it. [FC-B B10] That tow cost another eight hundred thousand dollars. [FC-B B10] She rode out Hurricane Rita at Beaumont. [FC-B B10]

> [PHOTO: NARA 6695642 kids on the pier watching her arrive, FOOT b6 #2] → [MAP: Pensacola → Beaumont tow line; hurricane symbol crosses the Gulf on "Rita"] → [ANIM: gauge "+$800,000"]. No year spoken for the first Pensacola arrival (NARA catalog date only).

By the spring of two thousand six, the Navy's bill was twelve point seven million dollars, and rising. [FC-B B11] Press reports on sinking day put the total at about twenty million. [FC-B B15] Florida's own legislature later put it at about twenty-one million, almost all of it Navy money. [FC-B B16]

> [ANIM: gauge "$12.7M" on "twelve point seven" → "≈ $20M" on "twenty million"] → [CARD: "FLORIDA SENATE: ≈ $21M" on "twenty-one"].

That is about seven times what Congress first committed. [FC-B B8, B15, B17] And the flight deck was not the only place the PCBs were hiding.

> [CARD: "$2.8M → ≈ $20M" side by side, gold bracket "≈ 7×" on "seven times"] → [ANIM: xray, a faint amber web through the hull (no label yet), one "?" on "hiding"].

---

## 4. THIRTY-SEVEN MINUTES (9:00–10:27)

On the twenty-second of March, two thousand six, she came back to Pensacola for the last time. [FC-B B26] She was the test case for new national cleanup rules for ships sunk as reefs. [FC-B B25]

> [MAP: Beaumont → Pensacola, date line 22 MAR 2006] → [PHOTO: NARA 6695614 tugs turn her at NAS Pensacola, FOOT b6 #4 (photographer CIV: check rights; fallback 6695615 likewise CIV, else 6696606 press-conference photo b6 #5)].

In May, a Navy bomb-disposal team went deep inside her hull. [FC-C A3; FOOT b6 #16–18] On the fifteenth, tugs pulled her away from the pier. [FOOT b7 #2] Former sailors lined the shore to watch her go. [FOOT b7 #10] One of them stood on the seawall and saluted. [FOOT b7 #8]

> [PHOTO: NARA 6698577 EOD sailor deep in a hatch, FOOT b6 #18] → [PHOTO: 6698593 tug against the hull, FOOT b7 #2] → [PHOTO: 6698599 aerial with base and shoreline, FOOT b7 #4 (map hand-off)] → [PHOTO: 6698588 crowd on the shore path, FOOT b7 #10] → [PHOTO: 6698587 veteran saluting, FOOT b7 #8 (second use, >6 min after ch. 1; CIV photographer, rights check)].

On the morning of the seventeenth of May, she sat at anchor more than twenty miles out in the Gulf. [FC-C A1, A11; FOOT b7 #11] The team had placed twenty-two charges on pipes and valves deep in her hull. [FC-C A2] More than five hundred pounds of explosives. [FC-C A4]

> [MAP: Pensacola → reef site, pin, date line 17 MAY 2006, "22 NM" scale bar] → [PHOTO: 6698606 hulk at anchor, open sea, FOOT b7 #11] → [ANIM: xray, 22 small charge points light up along the hull bottom on "twenty-two"] → [CARD: "500+ LB" on "five hundred"].

At ten twenty-five in the morning, they fired. [FC-C A5] The Navy expected her to take about five hours to sink. [FC-C A7] She took thirty-seven minutes. [FC-C A6]

> [CARD: clock 10:25 on "ten twenty-five"] → [PHOTO: 6698616 smoke plume, FOOT b8 #3 (sinking set, second use, >8 min after hook)] → [CARD: "≈ 5 HOURS" on "five hours", then struck; "37 MIN" lands on "thirty-seven"] → [PHOTO: 6698620 hull settling, FOOT b8 #7] → [PHOTO: 6698621 deck nearly awash, FOOT b8 #8].

She went down stern first, her bow rising into the air. [FC-C A8] Then she was gone. She settled upright on the bottom, her bow pointing due south. [FC-C A10] Two hundred and twelve feet down. [FC-C A9]

> [PHOTO: 6698622 deck tilted, FOOT b8 #12] → [PHOTO: 6698623 last of the deck, FOOT b8 #13] → [PHOTO: 6698625 bow slipping under, FOOT b8 #15] → [ANIM: hero sinking to scale, gauge labelled KEEL from 0 to 212 FT on "two hundred and twelve"; silt puff on touchdown; bow points to a "S" compass mark].

The moment she touched bottom, she belonged to Florida. [FC-C A15] She was the largest ship ever deliberately sunk as a reef. [FC-C A16] Guinness World Records lists her as the largest artificial reef in the world. [FC-C B12]

> [PHOTO: 6698613 onlooker on MV Powhatan phones, empty sea, FOOT b8 #19] → [CARD: "FLORIDA" on "Florida"] → [CARD: "LARGEST ARTIFICIAL REEF IN THE WORLD · GUINNESS WORLD RECORDS" on "largest"] (no Guinness logo).

It looked like the perfect ending. But her sinking came with a condition. And Florida had to keep checking it. [FC-B B24]

> [PHOTO: 6698628 monitoring vessel on the slick, FOOT b8 #18] → [ANIM: one fish icon on the wreck pin, a "?" on "checking"].

---

## 5. THE FISH TEST (10:27–12:27) — mid-video reversal

Not all of the PCBs came out. An estimated seven hundred pounds stayed aboard. [FC-B B18] They were locked in electrical cable, gaskets, insulation and paint. [FC-B B18] All the liquid PCBs had been removed. [FC-B B18]

> [ANIM: xray returns, the amber web from ch. 3 now lit and labelled on each spoken word: CABLE · GASKETS · INSULATION · PAINT] → [CARD: "≈ 700 LB" on "seven hundred"] (music: reflective pad state).

The EPA reviewed the Navy's studies. [FC-B B22] On the fifteenth of February, two thousand six, it ruled. [FC-B B22] Sinking her with the PCBs aboard would not pose an unreasonable risk. [FC-B B22; safe 1] It was the first approval of its kind ever given to a ship. [FC-B B23; safe 2] And the EPA said it applied to her alone. [FC-B B23]

> [MAP: Atlanta (EPA Region 4) pin, date line 15 FEB 2006] → [CARD: quote card "NOT AN UNREASONABLE RISK" on "unreasonable risk", credit "EPA, 15 Feb 2006"] → [CARD: "FIRST" on "first"].

There was a condition. Florida had to keep catching fish on the wreck and testing them. [FC-B B24; safe 3] From December two thousand six to November two thousand ten, the state and Escambia County sampled eight rounds of fish. [FC-B B32] Two hundred and fifty-four fish from the wreck. [FC-B B32]

> [MAP: wreck pin and a control reef pin near Pensacola Bay] → [ANIM: fish icons drop into a sample tray on the wreck pin, round counter 1 → 8; "254" on "two hundred and fifty-four"]. No fish footage in our PD list: animation; if NOAA PD reef-fish footage is found, it may replace (must show red snapper).

The first results were not what anyone wanted. [FC-B B29] For the first two years, the average PCB level in those fish was above two lines. [FC-B B29] Florida's screening value. And the EPA's. [FC-B B29]

> [ANIM: gauge, two horizontal lines labelled "FLORIDA" and "EPA" on their words; the average bar rises above both on "above two lines"; rounds 1–4 marked "YEARS 1–2"] (verdict sting: music dips out 0.8 s before "above").

Screening values are not poison limits. They are the levels at which health officials take a closer look. [FC-B B29; safe 4] The highest readings were in red snapper and porgies. [FC-B B31] Vermilion snapper and scamp never crossed either line. [FC-B B31]

> [ANIM: lines relabel "SCREENING VALUE" on "screening values"; magnifier icon on "closer look"] → [ANIM: species bars: RED SNAPPER, PORGIES above; VERMILION SNAPPER, SCAMP below, on their names].

Environmental groups, using the state's own data, went further. [FC-B B38; safe 8] They said snapper on the carrier carried about seven times more PCBs than snapper on a rubble reef. [FC-B B38] That reef was eight miles away. [FC-B B38] And tagging suggested the snapper tend to stay on the wreck. [FC-B B42]

> [CARD: attribution plate "ENVIRONMENTAL GROUPS (2012 PETITION), FROM FWC DATA" on "environmental groups"] → [ANIM: two snapper icons, carrier vs rubble reef, bracket "≈ 7×" on "seven times"; MAP inset "8 MI"] → [ANIM: a tag icon circles the wreck on "stay"]. The 54 ppb and "+1,446 %" figures are not used.

Then the numbers came down. [FC-B B30; safe 6] By about three years, the average was below Florida's line. [FC-B B30] By about four years, it was below both. [FC-B B30] No fish-eating advisory was ever issued for the wreck. [FC-B B41; safe 7]

> [ANIM: the average bar falls under "FLORIDA" on "below Florida's line", under "EPA" on "below both"] → [CARD: "NO ADVISORY ISSUED" on "no fish-eating advisory"].

The last published results stop there, about four years after the sinking. [FC-B B43] So here is the question the fish leave behind. If the Navy knew the PCBs were there, why not just take them out?

> [ANIM: gauge timeline ends in a dashed line after year 4 on "stop there"] → [ANIM: xray amber web pulses, one "?" on "take them out"].

---

## 6. THE REAL REASON (12:27–14:50) — final act, the answer

To answer that, go back down to the wreck. She does not sit the way she did on the day she sank. [FC-C B4] The storms saw to that. [FC-C B4, B5]

> [MAP: dive from the surface to the wreck] → [PHOTO: Wikimedia "Oriskany July 2008" divers on the island, Gareth Richards, CC BY-SA 3.0, OWNER DL, FOOT b9 #1 (July 2008, not "today"; credit in video and CREDITS.md)].

Within about two and a half years, storms had pushed her roughly ten feet down into the seabed. [FC-C B4] Among them was Hurricane Gustav, in two thousand eight. [FC-C B5] In late two thousand nine, a storm tore away the casing around her funnel. [FC-C B7]

> [ANIM: cross-section, hull sinks 10 ft into the sediment on "ten feet", gauge "~10 FT"] → [MAP: hurricane track over the wreck pin, date line 2008] → [ANIM: funnel casing peels away, date line LATE 2009]. Side-scan sonar image as reference only (FOOT b9 #4, low-res).

Today her flight deck lies about one hundred and forty-five to one hundred and fifty feet down. [FC-C B1] The top of her island is eighty-four feet down. [FC-C B2] The deck is beyond normal sport-diving limits. [FC-C B9] Florida warns divers never to go inside. [FC-C B8]

> [ANIM: cross-section labels "FLIGHT DECK ~145–150 FT" and "ISLAND TOP 84 FT" on their numbers; a dashed "SPORT LIMIT" line above the deck] → [PHOTO: Wikimedia Greg Grimes island top ~80 ft, CC BY-SA 2.0, OWNER DL, FOOT b9 #3] → [CARD: "DO NOT ENTER" on "never to go inside"].

The divers came anyway. In her first year, there were about four thousand two hundred charter dive trips. [FC-C B10] They brought about three point six million dollars of economic impact to two counties. [FC-C B11] Escambia, in Florida, and Baldwin, in Alabama. [FC-C B11] And sixty-seven jobs. [FC-C B11]

> [PHOTO: Wikimedia "Oriskany July 2008" series, another frame (catwalks, fish), FOOT b9 #2] → [CARD: "4,200 DIVE TRIPS" on "four thousand two hundred"] → [MAP: Escambia and Baldwin counties light up on their names; CARD "$3.6M" on "three point six"].

Now back to the question. Why leave the PCBs in? [FC-B B18] Almost all of what was left, ninety-seven percent, was in her wiring. [FC-B B19] The Navy said ripping it all out would mean taking the ship apart. [FC-B B19]

> [ANIM: xray, the amber web resolves into cable runs through every deck on "wiring"; "97 %" lands on "ninety-seven"] → [ANIM: the profile breaks into sections on "taking the ship apart"].

And taking her apart is exactly what nobody had managed to do. [FC-A D7] Two scrap deals had collapsed. [FC-A D7] Two more had found no taker. [FC-A D7] Getting the wiring out meant doing the very job that had already failed. [FC-B B19; FC-A D7]

> [ANIM: the tally board from ch. 1 returns: 2 COLLAPSED · 2 NO TAKER (callback)] → [PHOTO: NARA 6698554 rusted, gutted interior, 18 Apr 2006, FOOT b6 #7].

A reef was different. The Navy said reefing and cleanup cost about a quarter of taking a ship apart and recycling it. [FC-B B3] Even as the bill climbed, the Navy still called her a bargain. [FC-B B3, B11] Next to an estimated twenty-four million dollars to scrap her. [FC-B B3]

> [ANIM: two columns, "REEF" and "SCRAP", on their words; the reef column at "≈ 1/4" on "a quarter"] → [ANIM: reef column grows to "≈ $20M", scrap column "≈ $24M (USNI, 2006)" on "twenty-four"; gold bracket between them].

But that bargain would not hold for long. Within two years, the government's own ship-disposal agency gave a warning. [FC-B B27] Cleaning ships to the new standard could wipe out the savings of reefing compared to scrapping. [FC-B B27]

> [CARD: "MARAD, REPORT TO CONGRESS, JAN 2008" plate on "ship-disposal agency"] → [ANIM: the two columns, reef column rises to meet the scrap column on "wipe out the savings"; then both fade to the options board].

So that is why the Navy sank its own aircraft carrier. The bottom of the Gulf was the one door left. [FC-B B3]

> [ANIM: options board, final state: "MUSEUM?" struck on "whole", "SCRAPYARD?" struck on "stick", then "THE BOTTOM OF THE GULF" appears on its words, boxed and held 1.5 s] → [PHOTO: 6698624 bow vertical, FOOT b8 #14 (second use)]. Note: "the cheapest" is the Navy's own cost claim (FC-B B3), said as such.

---

## 7. ENDING (14:50–15:38) — ≈ 45 s after the answer

She is still the only aircraft carrier ever sunk as a reef. [FC-B B28] She will not be the biggest for long. [FC-C A16, C1]

> [ANIM: hero cross-section on the sea floor, light shafts, fish icons] → [FILM: SS United States full profile, 1968, FOOT b10 #7].

On November twelfth, at ten in the morning, weather permitting, Okaloosa County plans to sink the SS United States. [FC-C C2] She will lie about thirteen nautical miles from the Oriskany. [FC-C C11]

> [CARD: "NOV 12 · 10 A.M." on "November twelfth"] → [MAP: Okaloosa County, Destin pin on "Okaloosa"] → [MAP: end map, both wreck pins, dashed "13 NAUTICAL MILES" on "thirteen"; labels ≥ 3.5 %].

And here is the twist. Okaloosa County put fifty thousand dollars toward sinking the Oriskany. [FC-B B16] Now it is about to take her title. [FC-C A16]

> [CARD: "$50,000" on "fifty thousand", over the Oriskany pin] → [MAP: the "LARGEST" tag slides from the Oriskany pin to the SS United States pin on "take her title"].

So, was the bottom of the Gulf the best way to remember the Mighty O? Or just the cheapest way to let her go? Tell us in the comments.

> [MAP holds on both pins (end-screen space, last ~20 s with the music bed); CARD: "BEST WAY? OR CHEAPEST?" on its words]. No spoken next-video pitch.

---

## Gate checklist (for the reviewer)
- Hook: stakes line first, present tense; wow by ~3 s; promise spoken by ~10–11 s; SS United States named; no résumé.
- No ship résumé in the first 2 min: build/launch first appears at ~3:00, as a flashback answering "what was being thrown away".
- Answer held: the full "why" (wiring = dismantling; reef ≈ ¼ cost; nobody would take her) is spoken only at ~13:34–14:50.
 PCBs appear first at ~7:43 as a cost driver and at ~10:27 as the reversal, never as the answer.
- Mid-video reversal at ~10:27–12:27 (starts at ≈ 67 %; the fish turn at ~11:25. If the owner wants it nearer 60 %, cut the 1953 deck-bomb paragraph and trim ch. 2), fair wording: "screening values", attributed snapper figure, vermilion/scamp, "no advisory was ever issued", "last published results stop there".
- One family/veteran prompt at the first emotional peak (~5:28, after the fire), none at 0:30.
- Ending ≈ 45 s after the answer (14:50 → 15:38; 117 words, 45 s at Kokoro 155 wpm), closing question, no next-video pitch.
- Every place or date has a [MAP] or a date line; every number lands on its spoken word.
- Clip reuse: catapult film (hook, ch. 2), island film (hook only), sinking stills (hook, ch. 4/6, different frames except 6698624 used twice >13 min apart), veteran salute (ch. 1, ch. 4, >6 min apart), Bremerton row (ch. 1, ch. 2, >4 min apart).
- Rights to check before render: CIV-photographer NARA stills (6698587, 6695614, 6695615), Wikimedia CC BY-SA items (credit in video), no NC/ND.
