# USS Nevada (BB-36): footage scout

Scouted 2026-11-17. Nothing has been downloaded into the repo. Every NARA item below was opened through the catalog
JSON (`https://catalog.archives.gov/proxy/records/search?naId=<NAID>`, header `Content-Type: application/json`, no key
needed). I quoted its `useRestriction` field and read its shot list. Resolution and duration come from `ffprobe` over HTTP
on the real file. Time codes come from contact sheets I pulled from the files (frame grabs at fixed steps), so they
are accurate to about ±5 s. Check each one in the editor.

**Rights basis.**
- RG 428 (Navy), RG 80 (Navy stills), RG 374 (DTRA atomic-test stills), RG 434 (DOE) and RG 330 (DoD) items are
  US federal works, so they are public domain.
- NARA lists most RG 428 reels as `"Undetermined"`, its default for reels nobody has reviewed. Some RG 428 colour reels
  and some 111-ADC/342-USAF reels carry `"Restricted - Possibly"` with NARA's standard note:
  "Some or all of this material may be restricted by copyright or other intellectual property right restrictions".
  These are still Navy/Signal Corps/USAF camera-unit film. They are marked **VERIFY** below. Prefer the
  "Undetermined" raw reels when there is a choice.
- archive.org items are used only when they are federal films (credits or end-card numbers checked). Excluded:
  PeriscopeFilm (CC BY-NC-ND or none), "de-oldify" colourised uploads (NC-ND), TV documentaries and YouTube mirrors.

**Downloads.** NARA films and stills download directly from the `catalog.archives.gov/medialz/...` URLs. From this
machine they answer with HTTP 200 or 206, and range requests work. archive.org download URLs also work. Wikimedia and
NHHC (history.navy.mil) do not answer from this machine: NHHC returns 503 or times out, and Wikimedia blocks
downloads. Items marked **OWNER DOWNLOAD** must be fetched by hand.

**Honesty rule.** The "does NOT show" notes are binding.

---

## TOP 15 HOOK CANDIDATES (ranked)

| # | Item | ID / source | Format | Colour | Best moments | Shows | Does NOT show | Rights (quoted) |
|---|---|---|---|---|---|---|---|---|
| 1 | **"Operation Crossroads: Able and Baker Day Tests", Commander Joint Task Force One (Navy film MN-6517, NPC 1949), 2K-scan ProRes** | archive.org `OperationCrossroads` (file `IA000015_OperationCrossroads.mov`, 32.8 GB; proxy `IA000015_OperationCrossroads.mp4` 640x360) https://archive.org/details/OperationCrossroads | 1920x1080 ProRes 24 fps, 24:31 | **COLOUR** (faded: cyan/magenta cast, needs a grade) | **0:44-1:05 Nevada in her orange-red paint at Bikini, anchored, crew climbing the ladder, 14-in turrets with white-painted tops (the only colour close-up of the orange paint I found).** Able: 8:10 aerial burst over the atoll, 8:30-8:50 fireball/mushroom from the air, 10:00 mushroom over the horizon. Baker: 18:30-19:20 column from shore (palm trees in front), 19:50-20:50 aerial column and base surge. 12:40-14:15 wrecked target ships after Able. 23:10-24:00 a target vessel capsizing. End card "MN 6517 NPC 1949" at 24:30 | the only sharp colour film of Nevada's target paint, plus colour Able/Baker | Nevada is identifiable only at 0:44-1:05 (tower foremast, 14-in guns, orange hull). The red-tinted wreck at 14:00-14:15 is NOT identified (probably Sakawa). Ships in the blast shots are too small to name | archive.org: no licence field. Uploader `associate-yvonne-wang@archive.org`, collection "ephemera". The film is a US Navy production (Commander JTF-1, Naval Photographic Center; end card "MN 6517 NPC 1949"), so it is a PD federal work. Has Navy narration (also PD). Mute it and use your own VO |
| 2 | **SINKING THE USS NEVADA (reel 1 of 2)** | NARA 428-NPC-3646, NAID **76879**, https://catalog.archives.gov/id/76879, file https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-3646.mp4 | **1920x1080** h264 24 fps, 8:45 | B&W | 1:55 (114 s) close aerial of Nevada burning; 4:38 (278 s) Nevada low and burning, big smoke; 6:50 (409 s) close aerial broadside, smoke pouring; 3:00-3:30 bomb/torpedo hits (shot list: "TBF drops torpedo; torpedo wake followed by explosions"); 7:30-8:30 bombs exploding beside her | 31 Jul 1948, the last day: gunfire, bombs and an aerial torpedo | NARA marks some shots "very jumpy; NG". The final plunge is NOT confirmed in the shot list | useRestriction: "Undetermined" (RG 428 Navy film, PD) |
| 3 | **SINKING THE USS NEVADA (reel 2 of 2)** | NARA 428-NPC-3647, NAID **76880**, https://catalog.archives.gov/id/76880, file https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-3647.mp4 | **1920x1080**, 8:48 | B&W | 0:16-0:50 "Sea-going tug towing BB at sea"; **1:22 (82 s) close aerial broadside of the scarred hulk (the best full shot of the ship in 1948)**; 1:55 hulk with tug; 5:46 (346 s) broadside; 6:50-8:00 near misses and explosions; 8:31 BB smoking | the tow-out and the target attacks of 31 Jul 1948 | the ship is not named on screen. That it is Nevada comes from NARA's title. Make sure each shot you use is the BB, not the tug | "Undetermined" |
| 4 | **Baker Day blast, aerial, HD** | NARA 428-NPC-18813, NAID **81230**, https://catalog.archives.gov/id/81230, file https://catalog.archives.gov/medialz/mopix/428/NPC/428-npc-18813.mp4 | **1920x1080**, 11:05 | B&W | 0:20 slate "BAKER DAY 25 July 46"; 1:45-5:10 column and cloud rising through the cumulus; 5:50-10:40 cloud spreading over the lagoon (target ships visible as specks in the darker frames) | the whole Baker cloud, filmed from the air | individual ships cannot be identified, so Nevada is not identifiable | "Undetermined" |
| 5 | **Baker blast from Enyu Island camera tower, HD** | NARA 428-NPC-18554, NAID **81102**, https://catalog.archives.gov/id/81102, file .../428-npc-18554.mp4 | **1920x1080**, 10:48 | B&W | 0:55-1:45 water column and base surge with the target line on the horizon; 3:00-5:00 surge rolls across the fleet; 7:45 wave breaks on the beach | the classic ground-level Baker, with ships on the horizon (NARA: "Target fleet, showing 'B' bomb explosion. VG") | ships are silhouettes; Nevada cannot be named | "Undetermined" |
| 6 | **Baker "Wilson cloud" still photo (the iconic image)** | NARA 374-ANT-18-35326, NAID **146763012**, https://catalog.archives.gov/id/146763012, file https://catalog.archives.gov/medialz/stillpix/374-ant/102707987/374-ANT-18-35326-AC.jpg | 4001x3218 JPEG | B&W | n/a | Baker column and condensation cloud, ships silhouetted, palm trees and a hut in the foreground | ships cannot be named | useRestriction: "Unrestricted" |
| 7 | **Nevada after Able: damage film** | NARA 428-NPC-18363, NAID **81020**, file .../428-npc-18363.mp4 | 720x480, 4:47 | B&W | **0:26 and 1:02 Nevada broadside at Bikini after Able (tower mast, scorched)**; 0:44 shattered bridge works; 1:56 crushed truck on deck; 3:25 bow view down the 14-in guns; 3:43 Army half-track | Nevada's survival after Able (slate: "NEVADA ... 5 JULY 46") | B&W, so the orange paint cannot be seen | "Undetermined" |
| 8 | **Nevada & Nagato, aerial, COLOUR, post-Baker** | NARA 428-NPC-18798, NAID **81227**, file .../428-npc-18798.mp4 | 720x480, 6:51 | **COLOUR** (16 mm, faded) | 3:20 handwritten slate ("29 July 1946 ..."); **3:30-4:05 two battleships from the air: Nevada (left) and Nagato (right, pagoda mast)**; 0:20-1:10 fireboat spraying a ship; 4:10-5:00 Nagato close (NOT Nevada) | shot list: "USS Nevada, BB-36 and the Nagato"; "Nevada and Nagato alongside a small floating dry dock" | soft and faded. Which ship is which needs a frame check: Nevada is the one with the tripod/tower mast and no pagoda | "Undetermined" |
| 9 | **Nevada beached and burning at Hospital Point, 7 Dec 1941, 09:25** | 80-G-19940. NARA NAID **221948868** (record only, NO digital object). Hi-res copy on Wikimedia: `File:USS Nevada temporarily beached on hospital point 925AM NARA-80-G-19940.jpg` (5735x4529) | 5735x4529 JPEG | B&W | n/a | NARA caption: "Pearl Harbor, T.H. taken by surprise ... USS NEVADA (BB-36) burning." | | NARA "Unrestricted". Wikimedia "Public domain". **OWNER DOWNLOAD** (Wikimedia is blocked here) |
| 10 | **Nevada moving away from the burning ships, 7 Dec 1941** | NARA 80-G-32583, NAID **12009029**, file https://catalog.archives.gov/medialz/stillpix/080-g/80-G-32583.jpg | 3944x3184 JPEG | B&W | n/a | caption: "The USS Nevada (BB36) after the Japanese attack ... Moving to position away from enflamed ships. Foreground salvage and rescue tugs gun crews in action." Huge smoke pall, tug in front | the ship is small in the frame | "Unrestricted" |
| 11 | **Nevada aground at Waipio Point, tug alongside, smoke** | NARA 80-G-33020, NAID **404794279**, file https://catalog.archives.gov/medialz/stillpix/080-g/Batch0010/80-G-0033020_001.jpg | 8050x5352 (print scan, crop the margin card) | B&W | n/a | caption: "after the Japanese attack on Pearl Harbor, Dec. 7, 1941. Aground." Close, dramatic, with tug YT alongside | second grounding (Waipio Point), not Hospital Point | "Unrestricted" |
| 12 | **Pearl Harbor Attack Film (DoD)**: Nevada under way during the attack | NARA 330-DIMOC-DNDEE161692, NAID **147970730**, file https://catalog.archives.gov/medialz/mopix/330/DIMOC/330-dimoc-dndee161692.mp4 | 720x480, 5:36 | colour (heavily faded, bluish) | agency index: **"0:54-1:21: USS Nevada underway and past the 1010 dock trying to reach open sea, being attacked with her guns firing back, she turns left and runs aground at Hospital Point. In the foreground, Oglala rolls over and sinks."** Also 2:17-2:27 USS Shaw magazine explosion | the only motion film of the sortie | low resolution; Nevada is small behind Oglala (my grabs at 0:50-1:25 are soft) | "Restricted - Possibly", specific "Copyright". **VERIFY** before use (origin of the camera film not stated) |
| 13 | **Able shock wave from the air (photo)** | NARA 434-LB-5-XBD201208-00468, NAID **22118342**, file https://catalog.archives.gov/medialz/stillpix/434-lb/Installment_5/434-LB-5-XBD201208-00468.jpg | 2000x2750 (book-page scan with caption text, crop it) | B&W | n/a | Able fireball with the shock-wave ring on the lagoon and the atoll chain | ships not visible | "Unrestricted" |
| 14 | **Baker from Enyu, Saratoga's stern lifted on the wave crest (photo)** | NARA 374-ANT-18-22, NAID **146763002**, file https://catalog.archives.gov/medialz/stillpix/374-ant/102707987/374-ANT-18-022.jpg | 3931x3096 | B&W | n/a | "Baker Cloud, Ground View (Eneu Island) D+10 Seconds." The print caption reads "Figure 22 - view from Enyu 10 seconds after explosion showing stern of Saratoga rising 43 feet on first wave crest". Ships visible in front of the column | not Nevada (ships named only as Saratoga) | "Unrestricted" |
| 15 | **Nevada's 14-in guns fire at Cherbourg, June 1944 (photo)** | NARA 80-G-231636, NAID **219775743**, file https://catalog.archives.gov/medialz/stillpix/080-g/Batch0009/80-G-231636_001.jpg (and 80-G-231637, NAID **219775742**, `.../80-G-231637_001.jpg`, closer, the ship firing a broadside with flags) | 7748x5360 (crop the caption card) | B&W | n/a | caption: "14" guns of the USS NEVADA (BB36) shells Nazi shore batteries at Cherbourg, France", taken from USS Ancon | 231636: the ship is small. 231637: a stanchion crosses the frame | "Unrestricted" |

Runners-up for the hook: 374-ANT-18-CR-1131-07 (Baker from the island, ships on the horizon, NAID 146763016),
374-ANT-18-DBCR-PBM-178-403 (Baker from the air, 12,000 ft, NAID 146763018), and 374-ANT-18-LML-643 (Able from the air,
colour but badly faded, NAID 146763020).

---

## 1. Operation Crossroads (Bikini, 1946)

### Film: Nevada named in the NARA shot list (all RG 428, `"Undetermined"`, 720x480 unless noted)

| NAID | ID | Title | Dur | Best moments / shot list (quoted) | Does NOT show |
|---|---|---|---|---|---|
| 81039 | 428-NPC-18466 | OP. CROSSROADS NEVADA EVACUATION FOR "A" DROP | 9:25 | "Equipment on deck of USS NEVADA (BB-36) ... Men setting animal crates on deck of NEVADA ... Men evacuating NEVADA and getting into LCM alongside ... Man checking list of names". "OVERALL QUALITY: EXCELLENT" | B&W, so no orange |
| 81046 | 428-NPC-18476 | OP. CROSSROADS | 12:10 | shots 6-9: "Equipment aboard USS NEVADA ... Sailors securing hatch aboard NEVADA ... Muster and crew leaving NEVADA"; 10-11: target array pan | first half is USS New York |
| 81020 | 428-NPC-18363 | INSPECTING DAMAGE AFTER "A" DAY | 4:47 | see hook #7 | |
| 81062 | 428-NPC-18494 | Navada [sic] Damage & Bikini Recreation | 12:13 | "PAN, Turrets and aft, showing damaged planes, etc., aboard USS NEVADA (BB-36)". "EXCELLENT" | the rest is a beach recreation area |
| 81227 | 428-NPC-18798 | OPERATION CROSSROADS | 6:51 | **colour**, see hook #8 | |
| 81170 | 428-NPC-18653 | OPERATION, "CROSSROADS" | 11:26 | "Target array ... Nagato and Prinz Eugen are afloat; the Nevada is listing" | my grabs show mostly cloud-covered aerials; Nevada is hard to find |
| 81137 | 428-NPC-18602 | TARGET SHIPS - BIKINI (15 Jul 46) | 11:53 | "9) MS USS NEVADA (SV)" among New York, Arkansas, Nagato, Salt Lake City | |
| 81141 | 428-NPC-18606 | TARGET SHIPS - BIKINI (16 Jul 46) | 11:38 | "damage shots on ... USS NEW YORK, USS FALLON, USS NEVADA" | |
| 81109 / 81110 | 428-NPC-18565 / 18566 | target ships / activities on Bikini | 9:29 / 11:39 | "HA MS USS NEVADA, with other target ships in BG" | |
| 80896 | 428-NPC-18138 | TARGET SHIPS IN BIKINI LAGOON | 11:26 | "LS Japanese BB NAGATO & USS NEVADA (BB-36)" | |
| 80890 | 428-NPC-18132 | target ship arriving / camera towers | 9:06 | "LS Japanese BB Nagato, USS NEVADA & IN BG USS SARATOGA" | |
| 80916 | 428-NPC-18171 | AERIA[L] target fleet (14 Jun 46) | 9:50 | "MS AV USS NEVADA ... MS Pan USS NEVADA ... LS USS NEVADA and USS INDEPENDENCE" | B&W |
| 81123 | 428-NPC-18586 | RADIOLOGICAL CHECK / TARGET FLEET DAMAGE | 6:23 | ends "LS MS USS NEVADA SV" | |
| 81029 | 428-NPC-18405 | OP. CROSSROADS (29 Jun 46) | n/a | observers "escorted by CAPT G.C. ADELL, CO of USS NEVADA" | Nevada not shown |
| 80854 | 428-NPC-18082 | Arrival of Target Ships at Pearl Harbor (8 May 46) | 7:50 | "From small boat: USS NAVADA (BB-36) entering Pearl Harbor (SV, some with filters...)". FINE GRAIN MASTER. My grabs at 1:13-3:10 show the battleship close and head-on | **still grey, before the orange paint** (painted at Bikini, cf. 428-NPC-18202 "PAINTING USS NEVADA", not digitised) |

Not digitised (order from NARA if wanted): 428-NPC-18202 "PAINTING USS NEVADA AND VARIOUS OTHER SHOTS OF TARGET SHIPS
BIKINI" (NAID 80933). **This is the reel most likely to show the orange paint being applied.** Also 428-NPC-18255
"USS NEVADA AND OTHER TARGET SHIPS BIKINI" (NAID 80962) and 428-NPC-1045 "SINKING OF THE USS NEVADA (BB-36)" (NAID
75806, Aug 1948).

### Film: Able and Baker blasts (raw reels, `"Undetermined"`)

| NAID | ID | Res | What (shot list) |
|---|---|---|---|
| 81230 | 428-NPC-18813 | **1080p** | Baker aerial, see hook #4 |
| 81102 | 428-NPC-18554 | **1080p** | Baker from Enyu, see hook #5 |
| 81184 | 428-NPC-18681 | 480p, 7:18 | "ENTIRE REEL MADE UP OF THREE CAMERA TOWER SHOTS ... BAKER TEST EXPLOSION. THEY ARE ALL EXCELLENT. CAMERAS WERE ON TOWERS 3A (ENYU ISLAND), AND TOWERS 1 and 2 ON BIKINI." |
| 80965 | 428-NPC-18260 | 4:42 | "Atom bomb explodes; column of water shoots skyward; base surge spreads, enveloping target ships" |
| 81079 | 428-NPC-18524 | 11:52 | Baker from the air: "pressure waves. VG ... waves ... breaking on the shoreline" |
| 81099 | 428-NPC-18549 | 14:13 | Baker from USS Mt. McKinley, target ships and cloud development, "VG" |
| 81240-81242 | 428-NPC-18856/18857/18858 | 5:09 / 9:45 / 2:28 | Baker from USS Kenneth Whiting, "camera holds through all phases", "QUALITY GOOD" |
| 81250 | 428-NPC-18876 | 11:25 | "From the beach ... into target group as A-bomb explodes ... waves ... breaking on beach" |
| 81232 | 428-NPC-18821 | 11:51 | Able, "vertical shot" of the target layout as the bomb explodes, "GOOD" |
| 81031 | 428-NPC-18415 | 10:20 | Able drop from the air, "Column of smoke showing the white hot heat inside (very good shot)" |
| 81041 | 428-NPC-18469 | 10:14 | Able mushroom from PGM-23, "halo effect ... VG" |
| 81053 / 81061 / 80999 / 81000 / 81043 | 428-NPC-18484 / 18493 / 18316 / 18317 / 18471 | 8-12 min | Able from the camera towers over the target array |
| 80987 / 80980 | 428-NPC-18297 / 18289 | n/a | Able seen by goggled observers on Panamint and Fall River (good people-reaction shots) |
| 81076 | 428-NPC-18514 | 10:44 | **colour**, test animals (goats, rats) after Able; LST-661 smoking. Not Nevada. Grim: optional |

### Other Crossroads films (federal, archive.org)

| Identifier | Title | Res / dur | Colour | Rights (quoted) | Notes |
|---|---|---|---|---|---|
| `rpoperationcrossroads001` | Operation Crossroads (Navy, Office of Information, 1949) | 640x480, 24:56 (965 MB) | colour | no licence field. Creator "U S Navy Dept; Office Of Information" (Prelinger), PD federal | same film as hook #1 at lower resolution. Use hook #1 |
| `UWMCEMC122005OperationCrossroads` | Operation Crossroads (Dept of the Navy, 1949) | 641x486, 26:49 | n/a | "publicdomain/mark/1.0" | another print of the same film |
| `gov.ntis.ava13712vnb1` | Operations Crossroads (Dept of the Navy, 1949, NTIS) | 640x480 MPEG2, 27:02 | colour | "licenses/publicdomain" | another print of the same film |
| `MISC1323OperationCrossroads1948` | Operation Crossroads (Army MISC-1323 / Navy MN 5345, NARA 88210) | 1280x720 .mov, 26:45 | colour | "publicdomain/mark/1.0" | uploader: "source file isn't in the greatest shape" |
| `gov.doe.0800002` | Nuclear Test Film - Project Crossroads (JTF-1 report, Navy Photographic Science Lab, DOE release) | 640x480, 42:32 | **B&W** (metadata wrongly says colour) | "publicdomain/zero/1.0" (CC0) | 2:40 animated target-array map with **NEVADA at the centre**; 1:40 battleship at anchor; 21:20-27:00 damage close-ups. Narrated |
| `explosion-atomic-weapon-test-operation-crossroads-bikini-atoll` | Baker explosion, "Recorded by the U.S. Navy" | **1920x1080** HEVC 25 fps, 2:12 | B&W | "publicdomain/mark/1.0" | an unattributed HD upload; the source is not given. Prefer NARA 18813/18554 |
| `Operatio1946`, `Operatio1946_2` | Operation Crossroads Parts I/II (Handy Org. for Cmdr JTF-1) | 640x480, 12:06 / 14:30 | B&W | "licenses/publicdomain" | Prelinger, sponsor US Navy CJTF-1 |
| `342-usaf-34282a` = NARA 342-USAF-34282A (NAID 68771) | Project Crossroads (USAF, 12.6 h of raw film) | 655x480, 12:39:32 | B&W | NARA "Restricted - Possibly", "Copyright", **VERIFY** | reel 3: "Vice Admiral W.H.P. Blandy inspecting the battleship USS Nevada". Reels 4 and 7: Able and Baker from several cameras |

Excluded: PeriscopeFilm items (`83144-operation-crossroads-vwr` etc.: none or "by-nc-nd/4.0"),
`de-oldify-atomic-test-bikini-*` ("by-nc-nd/4.0"), `80524-the-air-force-and-the-atomic-bomb-vwr` ("by-nc-nd/4.0"),
`428-NPC-20012` (Paramount News: commercial newsreel), and the "Trinity & Beyond" frame on Wikimedia (a commercial documentary).

### Photos: Crossroads (all NARA `"Unrestricted"`)

| NAID | ID | Size | Shows |
|---|---|---|---|
| 146763012 | 374-ANT-18-35326 | 4001x3218 | iconic Baker column and Wilson cloud (hook #6) |
| 146763002 | 374-ANT-18-22 | 3931x3096 | Baker D+10 s, Saratoga's stern on the wave (hook #14) |
| 146763016 / 146763014 | 374-ANT-18-CR-1131-07 / CR-1130-19 | ~3950x3090 | Baker from the island, ships on the horizon (report-figure labels at the bottom; crop) |
| 146763018 | 374-ANT-18-DBCR-PBM-178-403 | 3218x4036 | Baker from 12,000 ft, dome and shock ring |
| 146763020 | 374-ANT-18-LML-643 | 4227x3549 | Able from the air, colour, faded red |
| 146763006 | 374-ANT-18-154626AC | 3648x2980 | Able cloud from the ground with palms and a hut |
| 146763102 | 374-ANT-18-CR-553-14 | 4244x3340 | **Able target array in Bikini Lagoon from the air (ships visible)** |
| 146763104 | 374-ANT-18-CR-655-2 | 3044x3653 | "Inspection of Army Vehicle on Deck of USS Nevada, Post Able": crushed truck, Nevada's turret and tower behind |
| 22118342 | 434-LB-5-XBD201208-00468 | 2000x2750 | Able shock wave (hook #13) |
| 6217459 / 6234450 / 6234438 | (NARA Boston gallery) | ~700-900 KB | Able mushroom over the lagoon; Baker fall-back "shower down on the Crossroads target fleet" |

Wikimedia (Commons file pages read via a fetch service; **OWNER DOWNLOAD**):
- `File:USS Nevada (BB-36) Operation Crossroads Target Ship.jpg`, 1139x674.
  - Licence: "Public domain".
  - Credit: "USNavy Photo via https://www.navsource.net/archives/01/36g.htm".
  - Description: "painted in orange as target ship for the Operation Crossroads Able". B&W, small.
- **Avoid** `File:Nevada during Operation Crossroads 1946.jpg` and `File:USS Nevada during Operation Crossroads 1946.jpg`.
  They are tagged "CC BY-SA 4.0 / Own work / Jdogmad, 2021", which is not plausible for a 1946 photo; this looks like
  colourised or laundered material.
- **Avoid** `File:USS Nevada (BB-36) after ABLE.jpg`, an Arthur Beaumont painting, 500x428. Beaumont's copyright
  status is unclear.

---

## 2. Pearl Harbor, 7 Dec 1941

| Item | ID / URL | Format | Rights (quoted) | Shows | Does NOT show |
|---|---|---|---|---|---|
| Pearl Harbor Attack Film | NAID 147970730 (330-DIMOC-DNDEE161692) | 720x480 colour (faded), 5:36 | "Restricted - Possibly" / "Copyright". **VERIFY** | 0:54-1:21 Nevada's sortie and grounding (agency index) | low resolution |
| 80-G-19940 beached at Hospital Point 09:25 | NARA NAID 221948868 (no scan); Wikimedia 5735x4529 | photo | "Unrestricted" / "Public domain". OWNER DOWNLOAD | hook #9 | |
| 80-G-32583 moving away from the burning ships | NAID 12009029, `.../080-g/80-G-32583.jpg` | 3944x3184 | "Unrestricted" | hook #10 | |
| 80-G-33020 aground, Waipio Point | NAID 404794279, `.../Batch0010/80-G-0033020_001.jpg` | 8050x5352 | "Unrestricted" | hook #11 | not Hospital Point |
| 80-G-32505 aerial of the 2nd grounding | Wikimedia `File:USS Nevada aerial view 2nd grounding off Waipio Point Nara 80-G-32505.jpg` | 5713x4538 | "Public domain"; credit "Official U.S. Navy photo 80-G-32505 from the U.S. Navy Naval History and Heritage Command" | Ford Island seaplane base after the attack, Nevada aground in the distance | OWNER DOWNLOAD |
| 80-G-32560 sortie begins | Wikimedia `File:USS Nevada begins her escape attempt from Pearl 80G32560.jpg` | 2929x2365 | "Public domain" | "stern and rear mast of USS Nevada (BB-36) visible at left from behind dense smoke of the burning oil from the USS Arizona" | Nevada only partly visible |
| USS Nevada afire off Ford Island | Wikimedia `File:USS Nevada (BB-36) afire off Ford Island 1941.jpg` | 2913x2319 | "Public domain" (no source number given; look up the 80-G number before use) | Nevada burning off the seaplane base | |
| 80-G-32558 / 32562 / 32556 / 32894, NH 97397 | Wikimedia (same names) | ~600-730 px only | "Public domain" | the sortie down the channel | low resolution; NHHC has bigger scans (site unreachable from here) |
| 306548 beached at Hospital Point | NARA NAID 306548 (RG 128) | small GIF (83 KB) | "Unrestricted" | | too small; use 80-G-19940 |
| Salvage photo "USS Nevada, port side; 2/19/42" (Pearl Harbor Naval Shipyard, RG 181) | NAID 296953 | small GIF | "Unrestricted" | refloated hull | too small |
| DECEMBER 7th (MN-2868/MN-2862) outtakes | NARA 428-NPC-13585 (NAID 79638, 12:07), 428-NPC-13590 (NAID 79640, 11:08), 428-NPC-34385 (NAID 84082, 8:01) | 720x480 B&W | "Undetermined" | raw 1942 salvage footage: "ECU Letters: 'Nevada' on side of BB"; "Colors flying from stern of USS NEVADA ... PAN to battle eroded side from being sunk"; Nevada moved into drydock by tugs; 13590 #19-21 Nevada leaving Pearl in new war paint, hull name "painted over, but legible" | **NOT the attack.** The released John Ford/Toland film "December 7th" mixes in studio re-creations: do not use the finished film for attack shots; use only these raw outtakes and say "after the attack" |
| RESULTS OF PEARL HARBOR RAID | 428-NPC-16439, NAID 80388, 6:13 | 720x480 | "Undetermined" | "CU Sign on turret of the USS NEVADA, from CincPac to Pacific Fleet ... Marine guards on the USS NEVADA" | aftermath, not the attack |
| Pearl Harbor (spring 1942) colour | 428-NPC-47635 (NAID 2663400, 9:48) and 428-NPC-47626 (NAID 2663240, 11:19) | 720x480 **colour** | "Restricted - Possibly", **VERIFY** | "USS Nevada (BB-36) as it moved towards drydock, a tugboat ... towed the USS Nevada out of drydock". 47626: damaged California, Pennsylvania, Nevada | spring 1942, not 7 Dec |

---

## 3. Normandy, June 1944 (Utah Beach, Cherbourg)

| Item | ID | Format | Rights | Shows / best | Does NOT show |
|---|---|---|---|---|---|
| USS NEVADA BOMBARDS FRENCH COAST PRIOR TO INVASION | 428-NPC-4312, NAID 77052, `.../428-npc-4312.mp4` | 720x480, 4:42 | "Undetermined" | shot 1 "MS USS NEVADA bombarding French coast"; then 5-in cases, convoy, LSTs with barrage balloons | the rest is convoy, not Nevada |
| INVASION OF FRANCE, ACTIVITY OFF COAST ON "D" DAY | 428-NPC-4313, NAID 77053, 9:16 | 720x480 | "Undetermined" | "LCVPs heading for beach, USS NEVADA fires BG ... LCVP sinking" | |
| ACTIVITY IN SEINE BAY ... WHILE USS NEVADA BOMBARDS (7 Jun 44) | 428-NPC-4308, NAID 77048, 4:32 | 720x480 | "Undetermined" | "MS USS NEVADA fires, LCI fires FG" | |
| 80-G-231636 / 231637 Cherbourg | NAIDs 219775743 / 219775742 | 7748x5360 | "Unrestricted" | hook #15 | |
| 80-G-252294 Mass aboard Nevada before D-Day | NAID 404794396, `.../Batch0010/80-G-0252294_001.jpg` | 5279x3679 | "Unrestricted" | sailors at Mass "at an English port waiting for D-Day" | |
| 80-G-231957 warships bombard Utah Beach | Wikimedia `File:Warships bombard targets ashore in support of the D-Day landings on Utah Beach, 6 June 1944.jpg` | 5471x4088 | "Public domain"; credit "Official U.S. Navy photo 80-G-231957 from the ... NHHC" | from USS Quincy; "the ship in the left center distance **appears to be** USS Nevada" | not confirmed as Nevada. OWNER DOWNLOAD |
| Nevada fires at Utah Beach (forward 14-in) | Wikimedia `File:USS Nevada (BB-36) fires in support of Normandy.jpg` | 200x157 only | "Public domain" (NHHC) | | too small; find the NHHC original |

---

## 4. Iwo Jima / Okinawa 1945 (RG 428 unless noted)

- **428-NPC-7512** (NAID 78111), **1920x1080**, 7:01, "Undetermined".
  - Shot list: "DA 14" guns of USS NEVADA bombarding Okinawa ... 40mm guns on USS NEVADA strafe beach ... Bombs falling and exploding on Okinawa (good)".
  - The best HD combat clip.
- **428-NPC-8390** (NAID 78476), **colour**, 5:32, "Undetermined": "USS NEVADA; SCENES ABOARD".
  - Shot list: "Muzzles of main battery rifles as they fire ... smoke rings".
  - Iwo Jima, Feb 1945.
- **428-NPC-8389** (NAID 78475) and **428-NPC-8391** (NAID 78477), "Undetermined": Iwo Jima from Nevada, 14-in muzzles firing.
- **428-NPC-7308** (NAID 78017): "14" gun flash from USS NEVADA FG".
- **428-NPC-7511** (NAID 78110), 9:13: "Main battery of USS NEVADA firing".
- **428-NPC-11162** (NAID 2485240) and **428-NPC-11163** (NAID 2485242): **colour**, the kamikaze hit of 27 Mar 1945, damage and casualties, burial at sea.
  - NARA: "Restricted - Possibly", **VERIFY**.
  - The archive.org copy (`NPC-11162`) is tagged "publicdomain/mark/1.0", "United States Naval Photographic Center film #11162".
  - It shows the dead: use with care.
- **111-ADC-9878** (NAID 23643), "USS NEVADA IS HIT", 7:31, Army Signal Corps.
  - Shot list: "Japanese plane crashes into USS Nevada. Excellent MSs, explosion on deck".
  - "Restricted - Possibly / Copyright", **VERIFY**.
- **428-NPC-11161** (NAID 2485234): colour, Nevada, West Virginia, Colorado, Texas and Arkansas under way. **VERIFY**.

---

## 5. Sinking, 31 July 1948

- **428-NPC-3646 and 428-NPC-3647**: HD, see hooks #2 and #3. These are the best and only digitised film of the sinking.
- **428-NPC-1045**, "SINKING OF THE USS NEVADA (BB-36)" (NAID 75806, Aug 1948): not digitised. Order it if more is needed.
- Photos: no 1948 sinking photo was found in the NARA online catalog. Commons lists none. NHHC was unreachable from this
  machine. The owner should search NHHC for "Nevada 1948" (an NH-series print may exist). Until then, use frame grabs
  from 3646/3647.

---

## 6. Wreck, 2020 (~15,400 ft, ~65 nm SW of Pearl Harbor)

- The imagery is by **Ocean Infinity / SEARCH, Inc.**, credited as "Ocean Infinity & SEARCH, Inc." or "Courtesy of Ocean
  Infinity" in the press.
- Their 11 May 2020 press release offered a press-kit download with a "caption and credit sheet". **No free licence was
  found.**
- No NOAA or Navy federal copy was found. NHHC only linked to the press kit.
- **Status: DESCRIBE ONLY.** Show it with a map, a depth graphic or an animation. Get written permission from SEARCH
  Inc. / Ocean Infinity before using any frame.
- Sources:
  [Defense Daily press release](https://www.defensedaily.com/press-releases/uss-nevada-located-by-search-and-ocean-infinity/),
  [Military Times](https://www.militarytimes.com/off-duty/military-culture/2020/05/12/iconic-wwii-battleship-discovered-nearly-3-miles-beneath-the-surface/),
  [Task & Purpose video](https://taskandpurpose.com/news/uss-nevada-wreckage-video/),
  [Maritime Executive](https://maritime-executive.com/article/ocean-infinity-finds-famed-battleship-uss-nevada).

---

## Notes for the edit
- **Orange paint.** Only hook #1 (0:44-1:05) shows it clearly. The film has faded to pink/magenta, so grade it back toward
  orange (#D9572B-ish) **and say on screen or in VO that colour was restored**. Hook #8 is a weaker, softer second source.
  For more, order 428-NPC-18202 ("PAINTING USS NEVADA").
- Old 4:3 film: pillarbox it or upscale it, with no "Deep Time" grade (`GRADE=none`). The NARA 1080p files (3646, 3647,
  18813, 18554, 7512) are already HD transfers of 4:3 frames inside a 16:9 raster.
- The hook map rule: Bikini Atoll first frame. The DOE film (`gov.doe.0800002`, about 2:40) has an animated target-array
  chart with NEVADA at the bullseye, useful as reference for our own map.
- Contact sheets used for this scout are in the session scratchpad (not the repo).
