# USS Nevada (BB-36) - footage list

Built 2026-11-17 for video 3 (USS Nevada). Files sit in `src/` (git-ignored): `src/photos/` (stills, longest side capped at 3840 px, JPEG q90; NARA items from the catalog's full scans, LoC items from the master TIFFs; a card/book-page scan also has a `_c.jpg` crop of the picture), `src/film/` (NARA reels as downloaded, 480p-1080p H.264; the Crossroads colour windows are cut from the 1080p ProRes master). Contact sheets (one frame every 2 s, timestamp burned in, 36 frames per sheet) are in `sheets/<stem>_NN.jpg`. Machine-readable copy: `footage.json`. **Nothing here is committed.**

**Rights basis.** Every NARA item's `useRestriction` field was read through the catalog proxy API (`catalog.archives.gov/proxy/records/search?naId=`) and is quoted verbatim in each row. Every LoC item's `rights_advisory`/`rights_information` was read from `loc.gov/item/<id>/?fo=json` and is quoted. US federal works only: RG 80 / 19-N (Navy), RG 428 (Navy film), RG 374 and RG 434 (atomic-test and DOE photos), RG 330 (DoD), RG 111 (Army Signal Corps), LoC FSA/OWI (Office of War Information). **NARA marks most RG 428 reels `"Undetermined"`** (its default for unreviewed reels): they are Navy camera-unit film, so federal works. Four films carry NARA's `"Restricted - Possibly"` copyright note and are marked VERIFY (the Pearl Harbor DoD film, the spring-1942 colour reel, the kamikaze colour reel and 111-ADC-9878). The Crossroads colour film comes from an archive.org upload with no licence field; the basis is the Navy end card (see the film entries). Nothing is NC/ND. No newsreel, TV documentary, or finished John Ford "December 7th" frame was used.

**Honesty rule.** The "does NOT show" column is binding: never caption a shot with a place, date, ship or person it does not verifiably show. Nevada is told by tripod masts, 14-in triple and twin turrets, and (in colour film) the orange-red paint; where that is not visible the entry says "not identifiable". Windows were read from 2-6 s contact sheets plus scene-cut detection, so in/out times are good to about +/-1-3 s: check them in the editor.

**Corrections to the scout.** (1) `nevada_evacuation` (428-NPC-18466) and `nevada_damage_bikini` (428-NPC-18494) are COLOUR and show the orange-red Nevada deck, turrets, crates and the damage: the scout listed them as B&W. (2) `111-ADC-9878` "USS Nevada is hit" is a US Navy Bureau of Aeronautics film (the last 3:40 are the USS Randolph, not Nevada). (3) The colour slides 80-GK-13512/13513, titled "USS Arizona exploding" by NARA, are widely identified as the USS Shaw magazine explosion: caption generically. (4) `nevada_scenes_colour` (428-NPC-8390) cannot be placed at Iwo Jima from the picture alone.

Counts: 126 stills (122 photos, 4 map/document pages), 38 film files (289 min of film, of which 6 are cut windows of the Crossroads colour master).


## Best items for the hook and the key beats (start here)

- **Hook (orange Nevada, colour, HD):** `crossroads_mn6517_w01` 0.0-34.1 s (Nevada wide at anchor 0-4.3, hull and crew 4.3-14.6, deck under the 14-in guns 14.6-28.7, tower 28.7-34.1); `nevada_evacuation` (colour, 480p) 21-120 s (orange deck, turret from above, wake), 130-164 s (crates), 321-365 s (turret roofs); `nevada_damage_bikini` (colour, 480p) 15-285 s (the damage after Able).
- **Able, colour HD:** `crossroads_mn6517_w03` 4.1-37.8 s (flash at ~6 s then the mushroom, one 25 s aerial shot), 53-60 s (red-rimmed mushroom); file is 69 s only.
- **Baker, colour HD:** `crossroads_mn6517_w05` 0-49 s (one continuous shot of the water column and base surge from a ship/shore); file is 69 s only; B&W HD from the island: `baker_enyu_hd` 20-105 s; stills `cx_baker_wilson_cloud`, `cx_baker_d10s_saratoga`.
- **Target ships:** `crossroads_mn6517_w07` 29-67 s (Nagato), stills `cx_saratoga_going_down_627506`, `cx_nagato_steams_to_bikini`.
- **Nevada after Able (B&W):** `nevada_after_able` 10-52 s and 192-230 s.
- **Pearl Harbor:** stills `ph_nevada_after_attack_32583`, `ph_nevada_waipio_33020_c`, `ph_loc_nevada_beached_hospital_point`, Arizona/Battleship Row stills; the DoD colour film `pearl_harbor_attack_dod` (VERIFY).
- **Normandy:** `d_nevada_utah_salvo_truman` (the best single picture), `d_cherbourg_nevada_231637_c`.
- **The sinking:** `sinking_1948_r1` 55-98 s, 432-488 s; `sinking_1948_r2` 56-95 s (the broadside at ~1:22). No still photo of the 1948 sinking and no film of the capsizing were found.


## A. Operation Crossroads, Bikini 1946 (the orange Nevada, Able, Baker, the target fleet, decontamination, animals, Bikinians)

| # | title | type | record URL | rights (verbatim) | what it shows | what it does NOT show / caveats | local file |
|---|---|---|---|---|---|---|---|
| A1 | 374-ANT-18-35326: Project 18 - Operation Crossroads (Bikini) Detonation (1946-07-25) | photo 3840x3089 | https://catalog.archives.gov/id/146763012 | NARA useRestriction: {"status": "Unrestricted"} | Baker (25 Jul 1946), ground view from an island: the column and wide condensation (Wilson) cloud, ship silhouettes at its base, palms and a hut in the foreground. The iconic Baker still | Ships at the base are specks: none can be named, Nevada is not identifiable. Frame is on a white print border (crop the edge) | `src/photos/cx_baker_wilson_cloud.jpg` (crop: `src/photos/cx_baker_wilson_cloud_c.jpg`) |
| A2 | 374-ANT-18-22: Project 18 - Operation Crossroads (Bikini) Detonation (1946-07-25) | photo 3840x3024 | https://catalog.archives.gov/id/146763002 | NARA useRestriction: {"status": "Unrestricted"} | Baker from Enyu Island 10 s after the burst: hollow white water column, dark hull silhouettes at its foot. Printed caption: "view from Enyu 10 seconds after explosion showing stern of Saratoga rising 43 feet on first wave crest" | Not Nevada. NARA lists it only as "Baker Cloud, Ground View (Eneu Island) D+10 Seconds". Report-page scan with caption text and punch holes: use the crop | `src/photos/cx_baker_d10s_saratoga.jpg` (crop: `src/photos/cx_baker_d10s_saratoga_c.jpg`) |
| A3 | 374-ANT-18-CR-1130-19: Project 18 - Operation Crossroads (Bikini) Detonation (1946-07-25) | photo 3840x2968 | https://catalog.archives.gov/id/146763014 | NARA useRestriction: {"status": "Unrestricted"} | Baker, first moments, from an island: a small dome at the horizon beyond a dark treeline (printed "Figure 41 - Film M1428A - Frame 30") | Tiny subject, report-figure label at the bottom (crop it). No ship readable | `src/photos/cx_baker_island_palms_a.jpg` (crop: `src/photos/cx_baker_island_palms_a_c.jpg`) |
| A4 | 374-ANT-18-CR-1131-07: Project 18 - Operation Crossroads (Bikini) Detonation (1946-07-25) | photo 3840x3024 | https://catalog.archives.gov/id/146763016 | NARA useRestriction: {"status": "Unrestricted"} | Baker, a few frames later, from the same island: the dome and spray ring at the horizon, palm trunks at left and right ("Figure 49 - Film M1428A - Frame 120") | Tiny subject, report-figure label (crop it). Ships not readable | `src/photos/cx_baker_island_palms_b.jpg` (crop: `src/photos/cx_baker_island_palms_b_c.jpg`) |
| A5 | 374-ANT-18-DBCR-PBM-178-403: Project 18 - Operation Crossroads (Bikini) Detonation (1946-07-25) | photo 3062x3840 | https://catalog.archives.gov/id/146763018 | NARA useRestriction: {"status": "Unrestricted"} | Baker from the air: white hollow dome of spray and the Wilson cloud with the circular shock ring on the water, scattered cumulus around | Print on a mount with stamp text at the top (crop). Individual ships not visible | `src/photos/cx_baker_aerial_wilson.jpg` (crop: `src/photos/cx_baker_aerial_wilson_c.jpg`) |
| A6 | 374-ANT-18-LML-643: Project 18 - Operation Crossroads (Bikini) Detonation (1946-07-01) | photo 3840x3224 | https://catalog.archives.gov/id/146763020 | NARA useRestriction: {"status": "Unrestricted"} | Able from the air in COLOUR: small mushroom over the lagoon, atoll rim and cumulus below. The print has faded to deep red/brown | Strong colour cast (grade it, say so in VO). Ships not visible | `src/photos/cx_able_aerial_colour.jpg` |
| A7 | 374-ANT-18-154626AC: Project 18 - Operation Crossroads (Bikini) Detonation (1946-07-01) | photo 3648x2980 | https://catalog.archives.gov/id/146763006 | NARA useRestriction: {"status": "Unrestricted"} | Able cloud, ground view: tall white mushroom with a dark stem over the horizon, white cumulus, palms, a hut and a figure on the beach in the foreground | Ships not visible | `src/photos/cx_able_ground_palms.jpg` (crop: `src/photos/cx_able_ground_palms_c.jpg`) |
| A8 | 374-ANT-18-18-2: Project 18 - Operation Crossroads (Bikini) Detonation (1946-07-01) | photo 3809x3044 | https://catalog.archives.gov/id/146763008 | NARA useRestriction: {"status": "Unrestricted"} | Aerial of a billowing dark-edged cloud column rising through broken cumulus (series "Detonation", no caption; the build and the sky fit Able) | NARA gives no caption: do not caption as Able or Baker without checking the film. No ships | `src/photos/cx_able_cloud_18_2.jpg` (crop: `src/photos/cx_able_cloud_18_2_c.jpg`) |
| A9 | 374-ANT-18-30: Project 18 - Operation Crossroads (Bikini) Detonation (1946-07-25) | photo 3705x3004 | https://catalog.archives.gov/id/146763004 | NARA useRestriction: {"status": "Unrestricted"} | Sailors sitting and standing at a ship's rail watching a distant Baker cloud at the horizon; print label "Personnel observing Test Baker" | Which ship is not stated; not shown to be Nevada | `src/photos/cx_baker_observers_deck.jpg` (crop: `src/photos/cx_baker_observers_deck_c.jpg`) |
| A10 | 374-ANT-18-CR-553-14: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-06) | photo 3840x3022 | https://catalog.archives.gov/id/146763102 | NARA useRestriction: {"status": "Unrestricted"} | AERIAL of the target array in Bikini Lagoon: dozens of anchored ships on a flat sea to the horizon (NARA: "Able Target Array in Bikini Lagoon") | Individual ships cannot be named; Nevada cannot be picked out | `src/photos/cx_able_target_array.jpg` (crop: `src/photos/cx_able_target_array_c.jpg`) |
| A11 | 374-ANT-18-CR-655-2: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-07) | photo 3044x3653 | https://catalog.archives.gov/id/146763104 | NARA useRestriction: {"status": "Unrestricted"} | Wrecked Army trucks and vehicles piled on a deck; behind them the base of a tower and a gun turret. NARA title: "Inspection of Army Vehicle on Deck of USS Nevada, Post Able" | The ship is Nevada only by the NARA caption; the tower/turret behind are consistent with the film nevada_after_able | `src/photos/cx_nevada_truck_post_able.jpg` (crop: `src/photos/cx_nevada_truck_post_able_c.jpg`) |
| A12 | 374-ANT-18-3: Project 18 - Operation Crossroads (Bikini) Test Activities (1946) | photo 3840x3082 | https://catalog.archives.gov/id/146763026 | NARA useRestriction: {"status": "Unrestricted"} | Two goats tethered in wooden frames on a ship's deck with feed buckets and straw (NARA: "Tethered Goats") | Which target ship is not stated: do not say Nevada. Good for the "goats, pigs and rats" line | `src/photos/cx_goats_tethered.jpg` (crop: `src/photos/cx_goats_tethered_c.jpg`) |
| A13 | 374-ANT-18-4: Project 18 - Operation Crossroads (Bikini) Test Activities (1946) | photo 3504x2819 | https://catalog.archives.gov/id/146763028 | NARA useRestriction: {"status": "Unrestricted"} | A B-29 on the ramp in front of a hangar, a tail letter visible, crew standing at the nose (NARA: "B-29 Bomb Drop Aircraft") | NARA does not name the aircraft: it is NOT confirmed as "Dave's Dream". Do not caption it with that name | `src/photos/cx_b29_bomb_drop_aircraft.jpg` (crop: `src/photos/cx_b29_bomb_drop_aircraft_c.jpg`) |
| A14 | 374-ANT-18-5: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-07) | photo 3045x3840 | https://catalog.archives.gov/id/146763030 | NARA useRestriction: {"status": "Unrestricted"} | Officers and VIPs standing on a battleship deck under a turret and director tower (NARA: "VIPs & Officers on USS New York, Post-Able") | USS New York, not Nevada | `src/photos/cx_vips_new_york_post_able.jpg` (crop: `src/photos/cx_vips_new_york_post_able_c.jpg`) |
| A15 | 374-ANT-18-62-DBCR-52: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-07-25) | photo 3030x3840 | https://catalog.archives.gov/id/146763032 | NARA useRestriction: {"status": "Unrestricted"} | Aerial over the lagoon: Saratoga low in the water among small craft, wing tip at left (NARA: "USS Saratoga Sinking") | Ship is small in the frame; grainy | `src/photos/cx_saratoga_sinking_aerial.jpg` (crop: `src/photos/cx_saratoga_sinking_aerial_c.jpg`) |
| A16 | 80-G-627506: Photograph of the USS Saratoga (CV-3) going down at 1540 Baker Day in Bikini Lagoon during Operation Crossroads (1946-07-25) | photo 3000x2283 | https://catalog.archives.gov/id/520999 | NARA useRestriction: {"status": "Unrestricted"} | Flat sea with two ship silhouettes on the horizon; NARA caption: Saratoga "going down at 1540 Baker Day in Bikini Lagoon" | Saratoga is a distant low silhouette: weak as a picture, useful as a record. Printed number on the left edge | `src/photos/cx_saratoga_going_down_627506.jpg` (crop: `src/photos/cx_saratoga_going_down_627506_c.jpg`) |
| A17 | 374-ANT-18-1: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-08) | photo 3840x3062 | https://catalog.archives.gov/id/146763022 | NARA useRestriction: {"status": "Unrestricted"} | A tug alongside a battleship, hosing it with water jets (NARA: "Tug Spraying Off Ship") | Which target ship is not stated | `src/photos/cx_decon_tug_spraying.jpg` (crop: `src/photos/cx_decon_tug_spraying_c.jpg`) |
| A18 | 374-ANT-18-ABCR-191-2846: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-07) | photo 3697x2842 | https://catalog.archives.gov/id/146763038 | NARA useRestriction: {"status": "Unrestricted"} | Target ships in the lagoon, one covered in decontamination spray; the print caption reads "U.S.S. Hughes covered with decontamination spray" | Hughes, not Nevada | `src/photos/cx_decon_hughes_spray.jpg` (crop: `src/photos/cx_decon_hughes_spray_c.jpg`) |
| A19 | 374-ANT-18-CR-2416-8: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-08-06) | photo 3774x3114 | https://catalog.archives.gov/id/146763084 | NARA useRestriction: {"status": "Unrestricted"} | Four sailors scrubbing the wet deck of the submarine Sea Raven with brooms and buckets, the fleet on the horizon (6 Aug 1946) | Submarine Sea Raven, not Nevada | `src/photos/cx_decon_scrub_sea_raven.jpg` (crop: `src/photos/cx_decon_scrub_sea_raven_c.jpg`) |
| A20 | 374-ANT-18-CR-2416-1: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-08-06) | photo 3059x3840 | https://catalog.archives.gov/id/146763082 | NARA useRestriction: {"status": "Unrestricted"} | Sailors with a hose and a deck gun on the USS Salt Lake City (6 Aug 1946), spraying her down | Salt Lake City, not Nevada | `src/photos/cx_decon_salt_lake_city_hose.jpg` (crop: `src/photos/cx_decon_salt_lake_city_hose_c.jpg`) |
| A21 | 374-ANT-18-CR-2416-10: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-07) | photo 3840x2938 | https://catalog.archives.gov/id/146763086 | NARA useRestriction: {"status": "Unrestricted"} | A tug (Achomawi) alongside the battleship New York, spraying salt water on her hull and tower; a fine mist rises (post Baker) | USS New York, not Nevada | `src/photos/cx_decon_new_york_saltwater.jpg` (crop: `src/photos/cx_decon_new_york_saltwater_c.jpg`) |
| A22 | 374-ANT-NA-80-G-627514: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-07) | photo 3827x3061 | https://catalog.archives.gov/id/146763120 | NARA useRestriction: {"status": "Unrestricted"} | Sailors with long-handled brooms and hoses washing down a wet ship deck (NARA: "Sailors Washing Down Ship Deck") | Which ship is not stated | `src/photos/cx_decon_washdown_deck.jpg` (crop: `src/photos/cx_decon_washdown_deck_c.jpg`) |
| A23 | 374-ANT-18-2: Project 18 - Operation Crossroads (Bikini) Test Activities (1946) | photo 3136x3840 | https://catalog.archives.gov/id/146763024 | NARA useRestriction: {"status": "Unrestricted"} | Two men in white caps on a deck with a hand-held radiation monitoring instrument (NARA: "Two Men on Board Ship with Monitoring Device") | Ship not named | `src/photos/cx_monitor_men_deck.jpg` (crop: `src/photos/cx_monitor_men_deck_c.jpg`) |
| A24 | 374-ANT-18-ABCR-654-2597: Project 18 - Operation Crossroads (Bikini) Test Activities (1946) | photo 3707x2992 | https://catalog.archives.gov/id/146763062 | NARA useRestriction: {"status": "Unrestricted"} | Men on the Hughes's deck while she is towed, one with a monitoring instrument; caption on the print: "Checking Radioactivity aboard Hughes during towing" | Hughes, not Nevada | `src/photos/cx_monitor_hughes_towing.jpg` (crop: `src/photos/cx_monitor_hughes_towing_c.jpg`) |
| A25 | 374-ANT-18-CR-1133-11: Project 18 - Operation Crossroads (Bikini) Test Activities (1948-04-09) | photo 3774x3114 | https://catalog.archives.gov/id/146763078 | NARA useRestriction: {"status": "Unrestricted"} | Twisted, scorched interior of the Hughes at Puget Sound, 9 Apr 1948 (inspection of bomb damage) | Hughes, not Nevada; the print is a report page with caption text | `src/photos/cx_hughes_interior_1948.jpg` (crop: `src/photos/cx_hughes_interior_1948_c.jpg`) |
| A26 | 374-ANT-NA-80-G-627515: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-07) | photo 3840x3042 | https://catalog.archives.gov/id/146763122 | NARA useRestriction: {"status": "Unrestricted"} | Sailors and visitors on a damaged deck beside a hatch and a sign "ATTENTION VISITORS NO SMOKING NO SOUVENIRS" (NARA: "Damage to USS Pensacola") | Pensacola, not Nevada. Good for "inspectors boarded the target ships" | `src/photos/cx_pensacola_damage.jpg` (crop: `src/photos/cx_pensacola_damage_c.jpg`) |
| A27 | 374-ANT-NA-80-G-627500: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-07) | photo 3075x3840 | https://catalog.archives.gov/id/146763118 | NARA useRestriction: {"status": "Unrestricted"} | Crushed superstructure and a bent mast on the submarine Skate with a "Keep clear - danger" sign (NARA: "Damage to USS Skate Post Able") | Submarine Skate, not Nevada | `src/photos/cx_skate_damage.jpg` (crop: `src/photos/cx_skate_damage_c.jpg`) |
| A28 | 374-ANT-18-ABCR-227-243-58: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-08-02) | photo 3827x3148 | https://catalog.archives.gov/id/146763042 | NARA useRestriction: {"status": "Unrestricted"} | The German cruiser Prinz Eugen at anchor, broadside, tall tower foremast (printed "Prinz Eugen Aug 2, 1946") | A target ship, not Nevada | `src/photos/cx_prinz_eugen_a.jpg` (crop: `src/photos/cx_prinz_eugen_a_c.jpg`) |
| A29 | 374-ANT-18-ABCR-227-243-61: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-08-02) | photo 3840x3131 | https://catalog.archives.gov/id/146763048 | NARA useRestriction: {"status": "Unrestricted"} | The Prinz Eugen at anchor on a flat sea, three-quarter bow view (printed "Prinz Eugen Aug 2, 1946") | A target ship, not Nevada | `src/photos/cx_prinz_eugen_b.jpg` (crop: `src/photos/cx_prinz_eugen_b_c.jpg`) |
| A30 | 374-ANT-18-BBCR-227-501-67: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-07) | photo 3840x3086 | https://catalog.archives.gov/id/146763070 | NARA useRestriction: {"status": "Unrestricted"} | The attack transport USS Catron (APA-71) at anchor, broadside, two masts and kingposts (print: "USS Catron, Pre-Baker") | Catron was a Crossroads test vessel. Do NOT say it is the transport from which Nevada's crew watched Able: that is not established | `src/photos/cx_catron_pre_baker.jpg` (crop: `src/photos/cx_catron_pre_baker_c.jpg`) |
| A31 | 374-ANT-18-CR-104: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-03) | photo 3840x3045 | https://catalog.archives.gov/id/146763072 | NARA useRestriction: {"status": "Unrestricted"} | Bikini islanders wading and boarding an LCM at the beach beneath palms (March 1946) | Wide beach; people are small in the frame | `src/photos/cx_bikinians_lcm.jpg` |
| A32 | 374-ANT-18-CR-109: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-03) | photo 3840x3088 | https://catalog.archives.gov/id/146763074 | NARA useRestriction: {"status": "Unrestricted"} | Bikini women and a man weaving thatch inside a hut (NARA: "Native Women Weaving Thatch on Bikini Island") | Portrait-quality interior | `src/photos/cx_bikinians_weaving.jpg` (crop: `src/photos/cx_bikinians_weaving_c.jpg`) |
| A33 | 374-ANT-18-CR-146: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-03) | photo 3840x3055 | https://catalog.archives.gov/id/146763080 | NARA useRestriction: {"status": "Unrestricted"} | Bikinians loading belongings, including bundles of pandanus thatch, onto LST-1108 on the beach (hull number 1108 readable) | Evacuation of the islanders before the tests, not the tests | `src/photos/cx_bikinians_loading_lst.jpg` (crop: `src/photos/cx_bikinians_loading_lst_c.jpg`) |
| A34 | 374-ANT-18-CR-422-1: Project 18 - Operation Crossroads (Bikini) Test Activities (1946) | photo 3030x3840 | https://catalog.archives.gov/id/146763096 | NARA useRestriction: {"status": "Unrestricted"} | A steel camera tower being erected among the palms on Bikini, a man high on the frame beside a crane (NARA: "Photo Towers Erected on Bikini") | Construction, not an instrument in use | `src/photos/cx_photo_towers.jpg` (crop: `src/photos/cx_photo_towers_c.jpg`) |
| A35 | 374-ANT-18-CR-511-3: Project 18 - Operation Crossroads (Bikini) Test Activities (1946-06) | photo 3840x2980 | https://catalog.archives.gov/id/146763100 | NARA useRestriction: {"status": "Unrestricted"} | Flight deck of the carrier Saratoga with the island and Army vehicles and equipment arranged on deck as test objects | Saratoga, not Nevada | `src/photos/cx_saratoga_deck_army_equipment.jpg` (crop: `src/photos/cx_saratoga_deck_army_equipment_c.jpg`) |
| A36 | 80-G-396226: Atomic cloud during "Able Day" blast at Bikini. First picture of atomic shock wave (1946-07-01) | photo 3000x1559 | https://catalog.archives.gov/id/520713 | NARA useRestriction: {"status": "Unrestricted"} | Able: a pale mushroom column over the horizon above a palm-lined shore; NARA: "first picture of atomic shock wave" | Ships not visible | `src/photos/cx_able_80g_396226.jpg` (crop: `src/photos/cx_able_80g_396226_c.jpg`) |
| A37 | 80-G-396229: Atomic cloud during Baker Day blast at Bikini (1946-07-25) | photo 3000x2462 | https://catalog.archives.gov/id/520714 | NARA useRestriction: {"status": "Unrestricted"} | Baker: the huge white cloud and column rising at the horizon above the lagoon, white condensation ring around the base | Ships at the base are specks | `src/photos/cx_baker_80g_396229.jpg` |
| A38 | 80-G-396231: Atomic cloud during Baker Day blast at Bikini. Atomic cloud shrouds target fleet. Sweeping out in all directions, this haze of water, steam and spray and radiocative substances obscured all but outer fringes of the Cross Roads target fleet a few minutes after the blast (1946-07-25) | photo 3000x2482 | https://catalog.archives.gov/id/520715 | NARA useRestriction: {"status": "Unrestricted"} | Baker: the haze of spray and radioactive mist spreading over the target fleet; palms in the foreground | Ships indistinct in the mist | `src/photos/cx_baker_80g_396231.jpg` (crop: `src/photos/cx_baker_80g_396231_c.jpg`) |
| A39 | 111-SC-421091: Japanese Battleship "Nagato" (1946) | photo 1968x1567 | https://catalog.archives.gov/id/175739069 | NARA useRestriction: {"status": "Unrestricted"} | Aerial of the Japanese battleship Nagato under way toward Bikini, pagoda-type foremast, hull streaked with rust. Signal Corps caption: "steams towards Bikini atoll ... will be used as a target for the atomic bomb test" | Nagato, not Nevada. Army Signal Corps print WPA-46-65008 | `src/photos/cx_nagato_steams_to_bikini.jpg` |
| A40 | 434-LB-5-XBD201208-00468: Progress of the shock wave from the Test Able explosion at Bikini Atoll, Operation Crossroads.  Photograph of image taken October 3, 1950 (1946-07-01) | photo 2000x2750 | https://catalog.archives.gov/id/22118342 | NARA useRestriction: {"status": "Unrestricted"} | Able: the fireball and the circular shock wave on the lagoon, taken from the air (book-page scan with caption: "Progress of the shock wave") | Page scan from a 1950 book; ships not visible. Crop to the photograph | `src/photos/cx_able_shockwave_book.jpg` (crop: `src/photos/cx_able_shockwave_book_c.jpg`) |
| A41 | 434-LB-5-XBD201208-00473: Atomic bomb cauliflower after-cloud at Bikini Atoll. Photograph of image taken October 3, 1950 (1946-07-25) | photo 2000x2750 | https://catalog.archives.gov/id/22118352 | NARA useRestriction: {"status": "Unrestricted"} | Baker cauliflower cloud with the base surge, ships beneath it; the page caption says Nagato (left) and Nevada (right) are at the foot of the cloud | Page scan of a 1950 book. The ships at the foot are specks: you may use the CAPTION as the source for "Nevada is under this", not the pixels. Crop to the photograph | `src/photos/cx_baker_nagato_nevada_book.jpg` (crop: `src/photos/cx_baker_nagato_nevada_book_c.jpg`) |
| A42 | 80-G-373119: Northside of Bikini Atoll in the Marshall Islands (1944-02-28) | photo 3840x2675 | https://catalog.archives.gov/id/404794508 | NARA useRestriction: {"status": "Unrestricted"} | Oblique aerial of the north side of Bikini Atoll: palms on a sand spit, a lagoon edge (taken Feb 1944 from USS Manila Bay) | Taken in 1944, 2 years before the tests; no ships | `src/photos/cx_bikini_1944_north.jpg` (crop: `src/photos/cx_bikini_1944_north_c.jpg`) |
| A43 | 80-G-373118: Northwest Tip of Bikini Atoll in the Marshall Islands (1944-02-28) | photo 3840x2659 | https://catalog.archives.gov/id/404794506 | NARA useRestriction: {"status": "Unrestricted"} | Oblique aerial of the north-west tip of Bikini Atoll, a low wooded islet in a wide reef (Feb 1944) | Taken in 1944; no ships | `src/photos/cx_bikini_1944_northwest.jpg` (crop: `src/photos/cx_bikini_1944_northwest_c.jpg`) |
| A44 | 80-G-373120: Southeast Island of Bikini Atoll in the Marshall Islands (1944-02-28) | photo 3840x2675 | https://catalog.archives.gov/id/404794510 | NARA useRestriction: {"status": "Unrestricted"} | Oblique aerial of the south-east island of Bikini Atoll: a thin island line and open lagoon (Feb 1944) | Taken in 1944; no ships | `src/photos/cx_bikini_1944_southeast.jpg` (crop: `src/photos/cx_bikini_1944_southeast_c.jpg`) |
| A45 | 80-G-400949: Aerial of Kwajalein after the Marine invasion. The fleet in the harbor brought in supplies to set up what became one of our advanced Pacific bases. (1944-03) | photo 2170x3000 | https://catalog.archives.gov/id/520716 | NARA useRestriction: {"status": "Unrestricted"} | Aerial of Kwajalein after the Marine invasion: Navy camp and runway on a sand island, many ships anchored in the harbour beyond | Not 1946. Kwajalein is where the Able bomber took off (the script), but this picture is from 1944 | `src/photos/cx_kwajalein_1944.jpg` (crop: `src/photos/cx_kwajalein_1944_c.jpg`) |
| A46 | [Mushroom cloud with ships below during Operation Crossroads nuclear weapons test on Bikini Atoll] (1946-07) | photo 2836x3840 | https://www.loc.gov/pictures/item/2012648160/ | No known restrictions on publication. | Crossroads, bright white dome with a dark rim just after the burst, ships tiny below and a beach at the bottom. LoC title: "Mushroom cloud with ships below during Operation Crossroads" [1946 July]. Looks like an early Able/Baker dome | LoC does not say Able or Baker. Ships tiny. From an album in the Ira Eaker papers (official photos compiled by the USAAF general); LoC: "No known restrictions on publication" | `src/photos/cx_loc_able_flash.jpg` |
| A47 | [Mushroom cloud with ships below during Operation Crossroads nuclear weapons test on Bikini Atoll] (1946-07) | photo 2818x3840 | https://www.loc.gov/pictures/item/2012648161/ | No known restrictions on publication. | Crossroads, a small round cloud head above scattered cumulus, ships below (portrait format print) | Unspecified test. From an album in the Ira Eaker papers (official photos compiled by the USAAF general); LoC: "No known restrictions on publication" | `src/photos/cx_loc_able_small_dome.jpg` |
| A48 | [Mushroom cloud with ships below during Operation Crossroads nuclear weapons test on Bikini Atoll] (1946-07) | photo 2873x3840 | https://www.loc.gov/pictures/item/2012648162/ | No known restrictions on publication. | A cloud column and mushroom head rising over cumulus above a coast (portrait format, same album) | Unspecified test (looks like Able). From an album in the Ira Eaker papers (official photos compiled by the USAAF general); LoC: "No known restrictions on publication" | `src/photos/cx_loc_crossroads_column.jpg` |
| A49 | [Mushroom cloud with ships below during Operation Crossroads nuclear weapons test on Bikini Atoll] (1946-07) | photo 2851x3840 | https://www.loc.gov/pictures/item/2012648164/ | No known restrictions on publication. | A tall narrow column with a flat cloud head rising above the horizon, sea haze (portrait format) | Unspecified test (looks like Able). From an album in the Ira Eaker papers (official photos compiled by the USAAF general); LoC: "No known restrictions on publication" | `src/photos/cx_loc_able_column.jpg` |
| A50 | [Mushroom cloud with ships below during Operation Crossroads nuclear weapons test on Bikini Atoll] (1946-07) | photo 2852x3840 | https://www.loc.gov/pictures/item/2012648166/ | No known restrictions on publication. | Aerial of a wide dome-shaped surge cloud with a bright rim over the lagoon, cumulus all around (portrait format) | Unspecified test (the dome form fits Baker). From an album in the Ira Eaker papers (official photos compiled by the USAAF general); LoC: "No known restrictions on publication" | `src/photos/cx_loc_baker_dome.jpg` |
| A51 | [Mushroom cloud with ships below during Operation Crossroads nuclear weapons test on Bikini Atoll] (1946-07) | photo 2836x3840 | https://www.loc.gov/pictures/item/2012648170/ | No known restrictions on publication. | Aerial of the spreading base surge ring and collapsing column over cumulus, ships tiny below | Unspecified test (the form fits Baker). From an album in the Ira Eaker papers (official photos compiled by the USAAF general); LoC: "No known restrictions on publication" | `src/photos/cx_loc_baker_base_surge.jpg` |


### Film: Operation Crossroads (MN-6517), window 01: Nevada in her orange paint at Bikini

- record: https://archive.org/details/OperationCrossroads  
- rights (verbatim): archive.org item "OperationCrossroads": NO licenseurl in the item metadata (collection "ephemera", uploader associate-yvonne-wang@archive.org, subject "Ephemeral Film", description "Commander joint task"). Basis: the film is a US Navy production (Commander Joint Task Force One; end card "MN 6517 NPC 1949", Naval Photographic Center), so a US federal work in the public domain. Other archive.org copies of the same film carry licenses: gov.ntis.ava13712vnb1 "licenses/publicdomain", UWMCEMC122005OperationCrossroads "publicdomain/mark/1.0", MISC1323OperationCrossroads1948 "publicdomain/mark/1.0".  
- file: `src/film/crossroads_mn6517_w01.mp4` (34.1 s, 1920x1080 h264 24/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/crossroads_mn6517_w01_01..01.jpg`  
- note: Cut from archive.org OperationCrossroads (IA000015_OperationCrossroads.mov, 1920x1080 ProRes 24 fps, 24:31, colour, faded to a cyan/magenta cast: needs a grade). Navy film "Operation Crossroads: Able and Baker Day Tests", Commander Joint Task Force One, end card "MN 6517 NPC 1949" = US Navy production (federal work). Window is H.264 CRF 18 with the original audio (Navy narration) as AAC: mute it. The film is 4:3 inside a 16:9 raster (black pillars). Source window 0:43.2-1:17.3.  
- how it was checked: viewed on a 640x360 proxy at 2 s steps and cut by scene detection; the window itself is the cut HD file  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-4.3 | NEVADA at anchor, wide: the whole ship in orange-red paint with white-topped turrets, tripod foremast, calm lagoon, a boat alongside. THE hook colour shot | Colour has faded to pink/red; grade toward #D9572B and say that the colour was restored. Name comes from the Navy/NARA record of this sequence and the 14-in turrets + tripod mast; no ship name is shown on screen |
| 4.3-6.8 | Same ship, closer: orange hull and superstructure, crew along the rail | Same caveat |
| 6.8-10.6 | Hull side and rail close: sailors lined at the rail on the orange hull, a ladder | Same caveat |
| 10.6-14.6 | A launch alongside and men going up/down the side ladder; orange hull | Same caveat |
| 14.6-22.8 | Officers and civilians walking along the deck under the long 14-in barrels (white tips) | People are not identified |
| 22.8-24.8 | A jeep-type vehicle parked on the orange deck (test vehicles) | Vehicle type only |
| 24.8-26.7 | Another vehicle (half-track / armoured car) on the deck | Vehicle type only |
| 26.7-28.7 | A tank on deck, white top | Vehicle type only |
| 28.7-34.1 | Nevada's tripod tower/bridge from the deck, orange-red, white-topped turret in front, sky behind | No hull number visible |


### Film: Operation Crossroads (MN-6517), window 02: goats and test animals being handled

- record: https://archive.org/details/OperationCrossroads  
- rights (verbatim): archive.org item "OperationCrossroads": NO licenseurl in the item metadata (collection "ephemera", uploader associate-yvonne-wang@archive.org, subject "Ephemeral Film", description "Commander joint task"). Basis: the film is a US Navy production (Commander Joint Task Force One; end card "MN 6517 NPC 1949", Naval Photographic Center), so a US federal work in the public domain. Other archive.org copies of the same film carry licenses: gov.ntis.ava13712vnb1 "licenses/publicdomain", UWMCEMC122005OperationCrossroads "publicdomain/mark/1.0", MISC1323OperationCrossroads1948 "publicdomain/mark/1.0".  
- file: `src/film/crossroads_mn6517_w02.mp4` (14.7 s, 1920x1080 h264 24/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/crossroads_mn6517_w02_01..01.jpg`  
- note: Cut from archive.org OperationCrossroads (IA000015_OperationCrossroads.mov, 1920x1080 ProRes 24 fps, 24:31, colour, faded to a cyan/magenta cast: needs a grade). Navy film "Operation Crossroads: Able and Baker Day Tests", Commander Joint Task Force One, end card "MN 6517 NPC 1949" = US Navy production (federal work). Window is H.264 CRF 18 with the original audio (Navy narration) as AAC: mute it. The film is 4:3 inside a 16:9 raster (black pillars). Source window 1:17.5-1:32.2.  
- how it was checked: viewed on the proxy; cut lists approximate (+/-1 s)  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-3.7 | Sailors/officers handling a spotted animal (goat or pig) at the rail | Which ship is not stated on screen; the preceding shots are Nevada but this is NOT shown to be on Nevada |
| 3.7-6 | Close-up of a curly-haired goat's head | Same |
| 6-8.9 | Goat close-up, horns, ears tagged/marked | Same |
| 8.9-12.3 | A spotted animal held down and examined | Same |
| 12.3-14.7 | Animal held down by hand on a table or deck | Same |


### Film: Operation Crossroads (MN-6517), window 03: Able, 1 July 1946, in colour

- record: https://archive.org/details/OperationCrossroads  
- rights (verbatim): archive.org item "OperationCrossroads": NO licenseurl in the item metadata (collection "ephemera", uploader associate-yvonne-wang@archive.org, subject "Ephemeral Film", description "Commander joint task"). Basis: the film is a US Navy production (Commander Joint Task Force One; end card "MN 6517 NPC 1949", Naval Photographic Center), so a US federal work in the public domain. Other archive.org copies of the same film carry licenses: gov.ntis.ava13712vnb1 "licenses/publicdomain", UWMCEMC122005OperationCrossroads "publicdomain/mark/1.0", MISC1323OperationCrossroads1948 "publicdomain/mark/1.0".  
- file: `src/film/crossroads_mn6517_w03.mp4` (69.2 s, 1920x1080 h264 24/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/crossroads_mn6517_w03_01..01.jpg`  
- note: Cut from archive.org OperationCrossroads (IA000015_OperationCrossroads.mov, 1920x1080 ProRes 24 fps, 24:31, colour, faded to a cyan/magenta cast: needs a grade). Navy film "Operation Crossroads: Able and Baker Day Tests", Commander Joint Task Force One, end card "MN 6517 NPC 1949" = US Navy production (federal work). Window is H.264 CRF 18 with the original audio (Navy narration) as AAC: mute it. The film is 4:3 inside a 16:9 raster (black pillars). Source window 7:56.7-9:06.0 (the cut was stopped early: the download was too slow; the rest of the Able sequence up to 10:07 is NOT in this file).  
- how it was checked: viewed on the proxy at 2 s steps; cut times from scene detection (0.15)  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-4.1 | A B-29 above a sea of cumulus (the bomber) | Not shown to be Dave's Dream; no name legible |
| 4.1-6.3 | Aerial of the atoll rim and lagoon from far away, the screen whitening | Before the flash |
| 6.3-31.3 | THE FLASH: white-out for ~3 s, then the Able fireball and mushroom rising over the atoll, seen from the air in one 25 s shot | Ships are specks, no Nevada |
| 31.3-37.8 | Fireball close, red-orange/white | Ships not visible |
| 37.8-39.5 | Observer in a cockpit | People not identified |
| 39.5-51.1 | Red-rimmed fireball, filling the frame | Ships not visible |
| 51.1-53.1 | Cockpit / observer | People not identified |
| 53.1-60.1 | The mushroom with its red glow rim, seen from the air | Ships not visible |
| 60.1-62.5 | Sailors on a ship's deck with binoculars watching the burst | Ship not named |
| 62.5-66.9 | Horizon from a ship, the glow at the horizon whitening | Distance shot |
| 66.9-69.2 | Observers at the rail, a bright haze at the horizon | Ship not named |


### Film: Operation Crossroads (MN-6517), window 05: Baker, 25 July 1946, in colour

- record: https://archive.org/details/OperationCrossroads  
- rights (verbatim): archive.org item "OperationCrossroads": NO licenseurl in the item metadata (collection "ephemera", uploader associate-yvonne-wang@archive.org, subject "Ephemeral Film", description "Commander joint task"). Basis: the film is a US Navy production (Commander Joint Task Force One; end card "MN 6517 NPC 1949", Naval Photographic Center), so a US federal work in the public domain. Other archive.org copies of the same film carry licenses: gov.ntis.ava13712vnb1 "licenses/publicdomain", UWMCEMC122005OperationCrossroads "publicdomain/mark/1.0", MISC1323OperationCrossroads1948 "publicdomain/mark/1.0".  
- file: `src/film/crossroads_mn6517_w05.mp4` (69.0 s, 1920x1080 h264 24/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/crossroads_mn6517_w05_01..01.jpg`  
- note: Cut from archive.org OperationCrossroads (IA000015_OperationCrossroads.mov, 1920x1080 ProRes 24 fps, 24:31, colour, faded to a cyan/magenta cast: needs a grade). Navy film "Operation Crossroads: Able and Baker Day Tests", Commander Joint Task Force One, end card "MN 6517 NPC 1949" = US Navy production (federal work). Window is H.264 CRF 18 with the original audio (Navy narration) as AAC: mute it. The film is 4:3 inside a 16:9 raster (black pillars). Source window 18:09.5-19:18.5 (stopped early: the download was too slow; the aerial part 19:23-21:01 is NOT in this file).  
- how it was checked: viewed on the proxy at 6 s steps; cut times from scene detection  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-49.3 | ONE LONG SHOT of Baker from a ship/shore at the horizon: the water column and base surge climb out of the lagoon, white spray collapsing outward, palm tops at the bottom edge | Ships are black specks and cannot be named. The first ~12 s are the still horizon before the burst |
| 49.3-55.5 | Ships on the horizon under the spreading column, a low shore line | Ships specks |
| 55.5-69 | A palm tree at the left, ships on the horizon, the cloud wall growing behind | Ships specks |


### Film: Operation Crossroads (MN-6517), window 06: decontamination begins, USS New York

- record: https://archive.org/details/OperationCrossroads  
- rights (verbatim): archive.org item "OperationCrossroads": NO licenseurl in the item metadata (collection "ephemera", uploader associate-yvonne-wang@archive.org, subject "Ephemeral Film", description "Commander joint task"). Basis: the film is a US Navy production (Commander Joint Task Force One; end card "MN 6517 NPC 1949", Naval Photographic Center), so a US federal work in the public domain. Other archive.org copies of the same film carry licenses: gov.ntis.ava13712vnb1 "licenses/publicdomain", UWMCEMC122005OperationCrossroads "publicdomain/mark/1.0", MISC1323OperationCrossroads1948 "publicdomain/mark/1.0".  
- file: `src/film/crossroads_mn6517_w06.mp4` (41.5 s, 1920x1080 h264 24/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/crossroads_mn6517_w06_01..01.jpg`  
- note: Cut from archive.org OperationCrossroads (IA000015_OperationCrossroads.mov, 1920x1080 ProRes 24 fps, 24:31, colour, faded to a cyan/magenta cast: needs a grade). Navy film "Operation Crossroads: Able and Baker Day Tests", Commander Joint Task Force One, end card "MN 6517 NPC 1949" = US Navy production (federal work). Window is H.264 CRF 18 with the original audio (Navy narration) as AAC: mute it. The film is 4:3 inside a 16:9 raster (black pillars). Source window 21:28.9-22:10.4.  
- how it was checked: viewed on the proxy at 6 s steps; approximate  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-12 | Carrier-deck and gun activity after the tests: sailors with planes, a man at a prop, then men lifting a hatch cover | Ship not named |
| 12-17.6 | Hull of the battleship NEW YORK with the name "NEW YORK" painted on her, white spray along her side | New York, not Nevada |
| 17.6-41.5 | A tug or fire boat jetting water onto a battleship; mist drifting; wash-down | Ship identity only from the "NEW YORK" shot just before |


### Film: Operation Crossroads (MN-6517), window 07: wash-down, officers on the target fleet, the Nagato

- record: https://archive.org/details/OperationCrossroads  
- rights (verbatim): archive.org item "OperationCrossroads": NO licenseurl in the item metadata (collection "ephemera", uploader associate-yvonne-wang@archive.org, subject "Ephemeral Film", description "Commander joint task"). Basis: the film is a US Navy production (Commander Joint Task Force One; end card "MN 6517 NPC 1949", Naval Photographic Center), so a US federal work in the public domain. Other archive.org copies of the same film carry licenses: gov.ntis.ava13712vnb1 "licenses/publicdomain", UWMCEMC122005OperationCrossroads "publicdomain/mark/1.0", MISC1323OperationCrossroads1948 "publicdomain/mark/1.0".  
- file: `src/film/crossroads_mn6517_w07.mp4` (37.1 s, 1920x1080 h264 24/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/crossroads_mn6517_w07_01..01.jpg`  
- note: Cut from archive.org OperationCrossroads (IA000015_OperationCrossroads.mov, 1920x1080 ProRes 24 fps, 24:31, colour, faded to a cyan/magenta cast: needs a grade). Navy film "Operation Crossroads: Able and Baker Day Tests", Commander Joint Task Force One, end card "MN 6517 NPC 1949" = US Navy production (federal work). Window is H.264 CRF 18 with the original audio (Navy narration) as AAC: mute it. The film is 4:3 inside a 16:9 raster (black pillars). Source window 22:10.6-22:47.7 (stopped early: the download was too slow; the later Nagato shots to 23:17 are NOT in this file).  
- how it was checked: viewed on the proxy at 6 s steps; approximate  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-29.6 | Fire boats and tugs spraying down damaged ships; a ship with scaffolding; then a group of officers/observers in sun helmets looking at the fleet | People not identified |
| 29.6-36.6 | The Japanese battleship NAGATO afloat and damaged, pagoda mast, low in the water | Nagato (pagoda foremast), not Nevada |


### Film: 428-NPC-18466: OP. CROSSROADS NEVADA EVACUATION FOR "A" DROP - BIKINI (21 Jun 1946)

- record: https://catalog.archives.gov/id/81039  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/nevada_evacuation.mp4` (565.2 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/nevada_evacuation_01..08.jpg`  
- note: RG 428. THE SCOUT SAID B&W: IT IS COLOUR (orange-red Nevada, white turret tops). 720x480 transfer, 4:3.  
- how it was checked: viewed on 6 s sheets and cut by scene detection 0.12; shot descriptions are at 6 s resolution (+/-3 s)  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 12-21.4 | Slate card "CROSSROADS ... Date: ... June 46" held to camera | Slate only; text not readable on the sheet |
| 21.4-30.1 | Orange-red deck and boxes close, a sailor at work | Colour faded; no name visible |
| 30.1-38.2 | Deck gear and a hatch from above | - |
| 38.2-64.2 | Distant ship on the horizon, sea in front | Which ship: not identified |
| 64.2-118.1 | Forecastle seen from above: a twin 14-in turret with white-tipped barrels, orange deck, wake streaming past (the ship under way) | Nevada by the title and the turret; no hull number visible |
| 118.1-130.4 | A lifeboat/whaleboat in its cradle, orange deck | - |
| 130.4-163.7 | Sailors loading wooden crates (animal crates) and boxes on deck | Crates are not shown to hold animals |
| 163.7-183 | Twin-barrel turret and a floatplane wing with a white star on the deck | - |
| 183-214 | Sailors on a ladder and a crowd in an LCM alongside (the crew leaving) | No faces identified |
| 214-240.8 | Officers checking a list and shaking hands on deck | People not identified |
| 281.9-294 | A cardboard box addressed to "CAPT ... U.S.S. NEVADA" (the label is partly legible) | Label only |
| 305.9-321 | Floatplane on a catapult and gun tubs, other ships behind | - |
| 321-365.1 | Orange turret roofs with large white painted markings, men working on them | - |
| 365.1-474.7 | Crew carrying sacks and bedrolls down the ladders, sorting gear | Crew leaving Nevada; matches the script line about leaving the ship |
| 474.7-541.1 | A crowd of sailors packed on the deck and in an LCM pulling away | - |


### Film: 428-NPC-18494: OP. CROSSROADS Navada Damage & Bikini Recreation - Bikini (5 Jul 1946)

- record: https://catalog.archives.gov/id/81062  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/nevada_damage_bikini.mp4` (733.3 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/nevada_damage_bikini_01..11.jpg`  
- note: RG 428. COLOUR (orange-red paint). Nevada part is 0:12-4:45; the rest (to 12:13) is a beach recreation area, not Nevada. 720x480, 4:3.  
- how it was checked: viewed on 6 s sheets and cut by scene detection 0.12  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-13.2 | Leader and slate "PLACE: BIKINI ... DATE: 5 JULY 46" | Slate only |
| 15.7-49.5 | Orange deck wreckage: a crane lifting a smashed aircraft, a turret roof, the barrels of a 14-in gun | Ship named by NARA title only |
| 49.5-92.2 | A white half-track and tank on the deck, then wreckage heaps from the bow side | - |
| 92.2-153.7 | Heaped debris, crushed vehicles, torn plates, a gun barrel above truck tyres | - |
| 153.7-182.8 | Burnt, twisted superstructure interior | - |
| 182.8-222 | Slate (second), then the forecastle: turret roof with white markings and the bow | - |
| 222-256.9 | Searchlight platform and a bent mast, a wrecked radar rack, gun barrel | - |
| 256.9-284.2 | The shattered tripod mast and bridge top, torn deck | - |


### Film: 428-NPC-18363: OP. CROSSROADS INSPECTING DAMAGE AFTER "A" DAY - BIKINI (6 Jul 1946)

- record: https://catalog.archives.gov/id/81020  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/nevada_after_able.mp4` (286.7 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/nevada_after_able_01..04.jpg`  
- note: RG 428. B&W, round-corner mask. Slate "NEVADA ... 5 JULY 46". 720x480.  
- how it was checked: viewed on a 6 s sheet; windows approximate (+/-3 s)  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 10-30 | NEVADA broadside at Bikini after Able: the tripod foremast and the 14-in turrets, forward superstructure scorched | Name from the slate/NARA title; tower matches Nevada |
| 30-52 | Shattered upper bridge works and mast top close, hull "130" painted at one point | Not a hull number of Nevada: it is a marking on the wreckage |
| 52-75 | Nevada again at distance from a boat, hull and tower | - |
| 76-82 | Slate card held by a sailor ("NEVADA ... 5 JULY 46") | Text partly legible |
| 82-148.4 | Deck wreckage: crushed truck (1:54-2:06), torn deck plates, a man in a doorway | B&W so no orange |
| 192-230 | Bow view: the twin 14-in guns, an Army half-track on the forecastle | - |
| 230-286.7 | Funnel base and wrecked gun tubs, wreckage at the stern end | - |


### Film: 428-NPC-18798: OPERATION CROSSROADS (colour, 1946)

- record: https://catalog.archives.gov/id/81227  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/nevada_nagato_colour.mp4` (411.0 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/nevada_nagato_colour_01..06.jpg`  
- note: RG 428. COLOUR 16 mm, soft and faded; 720x480, 6:51. Dated by the slate "29 July 1946 Bomb ... Target Array Bikini" (NARA date field says 1954).  
- how it was checked: viewed on a 6 s sheet; early part is dark and not understood  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 18-75.2 | Fire boat spraying a ship at night? (dark, glare of floodlights, deck equipment lit) | Ship not identified |
| 78-160 | Night flares/lights over the target fleet, a white glow on the water | No ship readable |
| 194-230 | Slate "L. BROCK ... 29 July ... Target Array Bikini", then colour aerial: two battleships at anchor in the lagoon, one (left) with a tripod mast and no pagoda | Which ship is Nevada needs a frame check: scout reads the left one as Nevada |
| 230-246 | Closer aerial: the same two battleships, a small floating dock | - |
| 246-300 | The Japanese Nagato (pagoda foremast) at anchor close from the air | Nagato, not Nevada |


### Film: 428-NPC-18082: OPERATION CROSSROADS: Arrival of Target Ships at Pearl Harbor (8 May 1946)

- record: https://catalog.archives.gov/id/80854  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/target_ships_arrive_pearl.mp4` (470.4 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/target_ships_arrive_pearl_01..07.jpg`  
- note: RG 428, fine-grain master. 720x480, 7:50.  
- how it was checked: scout list only for the shot; the film was NOT viewed frame by frame by me  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 61.3-127.1 | From a small boat: a battleship entering Pearl Harbor head-on, still in grey paint (NARA: "USS NAVADA [sic] (BB-36) entering Pearl Harbor") | Grey, before the orange paint; the scout confirmed on its grabs |


### Film: 428-NPC-18554: OP. CROSSROADS "B" BOMB EXPLOSION - ENYU ISLAND (25 Jul 1946)

- record: https://catalog.archives.gov/id/81102  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/baker_enyu_hd.mp4` (647.9 s, 1920x1080 h264 24/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/baker_enyu_hd_01..09.jpg`  
- note: RG 428. 1920x1080 B&W (4:3 pillarboxed), 10:48.  
- how it was checked: viewed on a 6 s sheet (first 4:48 only)  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-12 | Leader, slate "CROSSROADS station/camera...", then a still seascape with a small plant at the horizon | - |
| 20-26 | The burst starts: spray at the horizon, the cloud wall appears | Burst is at about 0:24-0:30 |
| 26-105 | Water column and base surge advancing along the horizon, a bush in the foreground; the target line is on the horizon | Ships are silhouettes; Nevada cannot be named |
| 180-300 | The surge rolling across the fleet line as a long white wall | - |


### Film: 428-NPC-18813: OPERATION "CROSSROADS" Bomb Blast ("Baker") Bikini (25 Jul 1946)

- record: https://catalog.archives.gov/id/81230  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/baker_aerial_hd.mp4` (665.0 s, 1920x1080 h264 24/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/baker_aerial_hd_01..10.jpg`  
- note: RG 428. 1920x1080 B&W (4:3 pillarboxed), 11:05.  
- how it was checked: viewed on two 6 s sheets (to 9:30)  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 6-22 | Slate "BAKER DAY 25 July 46 Mission 46 Sortie I" | Slate only |
| 70-120 | Aerial: the Wilson cloud and base surge dome seen over cumulus | Ships not visible |
| 120-320 | Aerial: the cloud column slowly drifting, grey | Flat, low contrast |
| 324-570 | Aerial: the spread cloud over the lagoon | Ships as specks in darker frames only |


### Film: 428-NPC-18514: "A" DAY AND "ATI" DAY - BIKINI ATOLL OP. CROSSROADS (colour)

- record: https://catalog.archives.gov/id/81076  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/able_animals_colour.mp4` (644.2 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/able_animals_colour_01..09.jpg`  
- note: RG 428. COLOUR, dark Kodachrome. 720x480, 10:44. Contains animal handling: not graphic in the part viewed.  
- how it was checked: viewed on 6 s sheets (to 9:30); later part not viewed  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 12-20 | A sheep or goat lying in a crate, dark | Dim |
| 24-42 | A chart/ board of squares (animal positions) shown to camera | - |
| 84-102 | Goat close-ups, white goat with horns | Ship not named |
| 72-80 | White rats in a straw-filled box | - |
| 162-200 | Sailors with a goat in a pen (the goat standing in straw) | - |
| 330-430 | Sailors loading cases and boxes on the deck of a small boat | - |
| 528-560 | Slate "CROSSROADS AACR 102 ... 1 JULY 1946 ... KODA-DAY" | Slate only |
| 546-584 | Ships of the target fleet at anchor in grey light, colour | - |


### Film: 428-NPC-18415: A-DAY BOMB DROP Bikini (1 Jul 1946)

- record: https://catalog.archives.gov/id/81031  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/able_drop_air.mp4` (620.1 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/able_drop_air_01..09.jpg`  
- note: RG 428. COLOUR 720x480, 10:20. Only viewed as a 20 s-step overview montage: windows are coarse (+/-10 s); no ship is named by me.  
- how it was checked: overview montage only  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-40 | Aerial colour: the Able cloud rising beside a flat blue lagoon and reef, cumulus around | Ships not visible |
| 40-300 | Aerial colour passes over the atoll rim, reef and the drifting Able cloud | Ships not visible |
| 300-560 | More aerial atoll and cloud views, one dark gap near 8:00 | No ship named |


### Film: 428-NPC-18821: TARGET FLEET ARRAY AT TIME OF BLAST (Able)

- record: https://catalog.archives.gov/id/81232  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/able_target_array.mp4` (710.8 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/able_target_array_01..10.jpg`  
- note: RG 428. B&W 720x480, 11:51. Only viewed as a 20 s-step overview montage: windows are coarse (+/-10 s); no ship is named by me.  
- how it was checked: overview montage only  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 20-50 | Vertical aerial: the target ships as dots on the lagoon | Ships not nameable |
| 150-300 | Vertical shot: the Able cloud blooming over the array (ring and dome) | No ship nameable |
| 300-700 | Long vertical view of billowing cloud tops | Little ship content |


### Film: 428-NPC-18171: AERIAL view of the target fleet (14 Jun 1946)

- record: https://catalog.archives.gov/id/80916  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/aerial_target_fleet.mp4` (589.9 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/aerial_target_fleet_01..09.jpg`  
- note: RG 428. B&W 720x480, 9:50, round-corner mask. NARA list: "MS AV USS NEVADA ... MS Pan USS NEVADA ... LS USS NEVADA and USS INDEPENDENCE". Only viewed as a 20 s-step overview montage: windows are coarse (+/-10 s); no ship is named by me.  
- how it was checked: overview montage plus NARA list  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 20-140 | Low aerial over the anchored target fleet, battleships among the ships | Nevada not picked out by me; the NARA list names her |
| 220-300 | Close views of battleships at anchor | Not identified by me |
| 320-450 | Officers on deck in conference | People not identified |


### Film: 428-NPC-18681: OP. CROSSROADS (Baker from three camera towers, 25 Jul 1946)

- record: https://catalog.archives.gov/id/81184  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/baker_towers.mp4` (437.6 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/baker_towers_01..07.jpg`  
- note: RG 428. COLOUR (green-cast) 720x480, 7:18. Only viewed as a 20 s-step overview montage: windows are coarse (+/-10 s); no ship is named by me.  
- how it was checked: overview montage only  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 20-100 | Quiet horizon, then the burst | Ships specks |
| 100-420 | The dark cloud wall and spray collapsing at the horizon | Ships specks |


### Film: 428-NPC-18476: OP. CROSSROADS (22 Jun 1946)

- record: https://catalog.archives.gov/id/81046  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/crossroads_18476.mp4` (730.1 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/crossroads_18476_01..11.jpg`  
- note: RG 428. COLOUR 720x480, 12:10. NARA: first half is USS New York; shots 6-9 aboard Nevada. Only viewed as a 20 s-step overview montage: windows are coarse (+/-10 s); no ship is named by me.  
- how it was checked: overview montage plus NARA list  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 20-160 | Crew with gear and sacks on a deck (colour) | Which ship: not named |
| 160-330 | Officers, a slate, battleship tower and turrets with orange-red paint, hatches secured | Nevada per NARA list for later shots, not confirmed by me |
| 330-600 | Sailors in boats and ladders, other ships at anchor | Not identified |


### Film: 428-NPC-18138: TARGET SHIPS IN BIKINI LAGOON, PGM 29

- record: https://catalog.archives.gov/id/80896  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/target_ships_lagoon.mp4` (685.6 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/target_ships_lagoon_01..10.jpg`  
- note: RG 428. B&W 720x480, 11:26. NARA list: "LS Japanese BB NAGATO & USS NEVADA (BB-36)". Only viewed as a 20 s-step overview montage: windows are coarse (+/-10 s); no ship is named by me.  
- how it was checked: overview montage plus NARA list  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 15-120 | Carriers and cruisers anchored in the lagoon, close boat views | Not named by me |
| 200-330 | Battleships and the slate "CROSSROADS target ships ... 31 May 46" | Nevada not picked out by me |
| 330-685.6 | Parade of target ships: transports, subs, a hospital-type ship, cruisers | - |


### Film: 428-NPC-18586: RADIOLOGICAL CHECK ON PG-29 & TARGET FLEET DAMAGE BIKINI

- record: https://catalog.archives.gov/id/81123  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/radiological_check.mp4` (383.2 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/radiological_check_01..06.jpg`  
- note: RG 428. 720x480, 6:23. NARA: ends "LS MS USS NEVADA SV". Decontamination/monitoring candidate. Not viewed by me.  
- how it was checked: NARA list only  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-383 | Radiation monitoring and damage to the target fleet; Nevada at the end per NARA | Not viewed by me |


### Film: 428-NPC-18602: TARGET SHIPS - BIKINI (15 Jul 1946)

- record: https://catalog.archives.gov/id/81137  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/target_ships_15jul.mp4` (713.1 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/target_ships_15jul_01..10.jpg`  
- note: RG 428. 720x480, 11:53. NARA: "9) MS USS NEVADA (SV)" among New York, Arkansas, Nagato, Salt Lake City. Not viewed by me.  
- how it was checked: NARA list only  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-713 | Target ships at Bikini after Able; shot 9 is Nevada per NARA | Not viewed by me |


## B. Pearl Harbor, 7 December 1941

| # | title | type | record URL | rights (verbatim) | what it shows | what it does NOT show / caveats | local file |
|---|---|---|---|---|---|---|---|
| B1 | 80-G-32583: Photograph of the USS Nevada after the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12009029 | NARA useRestriction: {"status": "Unrestricted"} | Nevada under way/heading out of the burning line: dark smoke wall over the harbour behind, a tug in the foreground, her tower mast above the smoke. NARA/Navy caption: "moving to position away from enflamed ships" | The ship is small in the frame. Foreground tug stands between camera and ship | `src/photos/ph_nevada_after_attack_32583.jpg` |
| B2 | 80-G-33020: The USS Nevada (BB36) After the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x2553 | https://catalog.archives.gov/id/404794279 | NARA useRestriction: {"status": "Unrestricted"} | Nevada aground (Waipio Point), tug alongside at right, smoke hazing the tower and the 14-in turret. Print caption: "after the Japanese attack ... Aground" | Second grounding (Waipio Point), NOT Hospital Point. Mounted on a NARA caption card: use the crop | `src/photos/ph_nevada_waipio_33020.jpg` (crop: `src/photos/ph_nevada_waipio_33020_c.jpg`) |
| B3 | 80-G-19942: Photograph of USS Arizona on Fire after Attack on Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12008980 | NARA useRestriction: {"status": "Unrestricted"} | The Arizona on fire: black smoke column, the burning tower structure and a mast above the water line | Title from NARA. Shot at water level, no other ship readable | `src/photos/ph_arizona_burning_19942.jpg` |
| B4 | 80-G-19951: Photograph of Burning Oil from Shattered Fuel Tanks during Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12008981 | NARA useRestriction: {"status": "Unrestricted"} | Burning oil and black smoke over the harbour with a small boat at the right (NARA: "Burning Oil from Shattered Fuel Tanks") | Dark, graphic; no named ship | `src/photos/ph_burning_oil_19951.jpg` |
| B5 | 80-G-32414: Photograph of the USS West Virginia and the USS Tennessee after the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12008986 | NARA useRestriction: {"status": "Unrestricted"} | Battleship Row from across the water: the West Virginia and Tennessee with their cage/tripod masts above a wall of oil fire and smoke | NARA title names West Virginia and Tennessee; Nevada is not in this frame | `src/photos/ph_wv_tennessee_32414.jpg` |
| B6 | 80-G-32421: Photograph of the USS Arizona, the USS Tennessee, and the USS West Virginia after the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12008989 | NARA useRestriction: {"status": "Unrestricted"} | Smoke pall over Battleship Row, masts of the ships beneath it, a long low dock in the foreground | NARA names Arizona, Tennessee, West Virginia; individual ships hard to tell apart | `src/photos/ph_arizona_tn_wv_32421.jpg` |
| B7 | 80-G-32419: Photograph of Burning and Damaged Ships at Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12008988 | NARA useRestriction: {"status": "Unrestricted"} | Heavy smoke and a collapsing superstructure with a mast at the right edge; one foreground tower (NARA: "Burning and Damaged Ships") | Ship not named by NARA | `src/photos/ph_burning_ships_32419.jpg` |
| B8 | 80-G-32424: Photograph of Burning and Damaged Ships at Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12008991 | NARA useRestriction: {"status": "Unrestricted"} | Battleships with tripod masts engulfed in black smoke at the waterline, a second battleship at right | Not named by NARA | `src/photos/ph_burning_ships_32424.jpg` |
| B9 | 80-G-32427: Photograph of Burning and Damaged Ships at Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12008992 | NARA useRestriction: {"status": "Unrestricted"} | Wreckage of a battleship: a leaning, burning mast and twisted crane, a tower and crane boom at the right; thick smoke | Not named by NARA | `src/photos/ph_burning_ships_32427.jpg` |
| B10 | 80-G-32432: Photograph of Burning and Damaged Ships at Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12008995 | NARA useRestriction: {"status": "Unrestricted"} | Smoke column over the harbour, a battleship at the shore beyond a road, a number "69" on the lower left | Not named by NARA | `src/photos/ph_ships_smoke_32432.jpg` |
| B11 | 80-G-32537: Photograph of the USS Oglala Capsized and Sinking after the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3100x3840 | https://catalog.archives.gov/id/12009013 | NARA useRestriction: {"status": "Unrestricted"} | The minelayer Oglala capsizing: a huge hull plated wall with black smoke at the right (the scan is rotated 90 degrees; this file is rotated upright) | Oglala, not Nevada; script mentions her rolling over in the DoD film | `src/photos/ph_oglala_32537.jpg` |
| B12 | 80-G-32545: Photograph of the USS Arizona Burning after the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12009017 | NARA useRestriction: {"status": "Unrestricted"} | Arizona burning seen through a palm frond, a wooden pier in the foreground; smoke and a tower on the horizon | NARA caption: Arizona burning | `src/photos/ph_arizona_burning_32545.jpg` |
| B13 | 80-G-32608: Photograph of the USS Arizona Burning after the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x3004 | https://catalog.archives.gov/id/12009044 | NARA useRestriction: {"status": "Unrestricted"} | Arizona: the foremast and bridge structure collapsing forward, cranes and rigging at the left | NARA caption: Arizona burning | `src/photos/ph_arizona_burning_32608.jpg` |
| B14 | 80-G-32609: Photograph of the USS Arizona after the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12009046 | NARA useRestriction: {"status": "Unrestricted"} | Arizona's tripod tower and wrecked superstructure standing out of the water with small boats alongside | NARA caption: Arizona | `src/photos/ph_arizona_32609.jpg` |
| B15 | 80-G-32916: Photograph of the USS Arizona Burning after the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12009082 | NARA useRestriction: {"status": "Unrestricted"} | Arizona burning: big black smoke plume and the burning tower, a wreck in the foreground | NARA caption: Arizona burning | `src/photos/ph_arizona_burning_32916.jpg` |
| B16 | 80-GK-13512: Photograph of USS Arizona Exploding Fiercely at Pearl Harbor after Japanese Attack (1941-12-07) | photo 3840x3084 | https://catalog.archives.gov/id/12009094 | NARA useRestriction: {"status": "Unrestricted"} | COLOUR: an orange fireball and black smoke from an exploding ship against a blue sky | NARA title says "USS Arizona exploding" but this colour slide (80-GK-13512/13513) is widely identified as the magazine explosion of the destroyer USS SHAW in the floating drydock: caption it only as "a ship exploding at Pearl Harbor" until checked against NHHC | `src/photos/ph_ship_explosion_gk13512_COLOUR.jpg` |
| B17 | 80-GK-13513: Photograph of USS Arizona Burns at Pearl Harbor after Japanese Attack (1941-12-07) | photo 3840x3084 | https://catalog.archives.gov/id/12009095 | NARA useRestriction: {"status": "Unrestricted"} | COLOUR: a close, larger orange-yellow fireball over the harbour, blue sky above | Same caveat: NARA title says Arizona, likely the USS Shaw explosion. Caption generically | `src/photos/ph_ship_explosion_gk13513_COLOUR.jpg` |
| B18 | 80-G-33058: Photograph of Burning and Damaged Ships at Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12009087 | NARA useRestriction: {"status": "Unrestricted"} | Wide view: battleship masts on the right, a long oil fire at their feet, two ships at left, a rail across the foreground | Not named by NARA | `src/photos/ph_burning_ships_33058.jpg` |
| B19 | 80-G-32691: Photograph of Burning and Damaged Ships at Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12009053 | NARA useRestriction: {"status": "Unrestricted"} | Smoke over the line of ships from the deck of a ship in the foreground, a motor boat crossing the harbour | Not named by NARA | `src/photos/ph_burning_ships_32691.jpg` |
| B20 | 80-G-32476: Photograph of Gun Crews during the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12009005 | NARA useRestriction: {"status": "Unrestricted"} | A gun crew behind sandbags firing during the attack, smoke over the harbour far behind | Location not stated beyond Pearl Harbor | `src/photos/ph_gun_crew_32476.jpg` |
| B21 | 80-G-32543: Photograph of Gun Crews during the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12009016 | NARA useRestriction: {"status": "Unrestricted"} | Machine gunners behind a sandbag parapet with hills and the field behind, during the attack | Location not stated beyond Pearl Harbor | `src/photos/ph_aa_gun_crew_32543.jpg` |
| B22 | 80-G-33053: Photograph of Japanese Planes in Action Over Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12009086 | NARA useRestriction: {"status": "Unrestricted"} | A Japanese plane (small dark speck near the top) over the burning harbour; a crane and cars at the left, smoke columns | Plane is tiny | `src/photos/ph_jap_planes_33053.jpg` |
| B23 | 80-G-32486: Photograph of the Capsized USS Oklahoma and the USS Maryland after the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12009007 | NARA useRestriction: {"status": "Unrestricted"} | The capsized Oklahoma bottom up with the tower of the Maryland rising beyond | NARA: capsized Oklahoma and Maryland | `src/photos/ph_oklahoma_maryland_32486.jpg` |
| B24 | 80-G-182873: Photograph of Pearl Harbor (1941-10-30) | photo 3840x3100 | https://catalog.archives.gov/id/12008978 | NARA useRestriction: {"status": "Unrestricted"} | Aerial over Pearl Harbor lochs and Ford Island seen under a wing, mountains behind (30 Oct 1941, before the attack) | Before the attack; ships are not distinguishable | `src/photos/ph_aerial_oct_1941_182873.jpg` |
| B25 | 80-G-276509: Photograph of Pearl Harbor (1942-05-21) | photo 3840x3100 | https://catalog.archives.gov/id/12009110 | NARA useRestriction: {"status": "Unrestricted"} | Vertical-oblique aerial of Ford Island and the harbour, with the Navy Yard at the bottom (21 May 1942, after the attack) | Not 7 Dec 1941 | `src/photos/ph_aerial_may_1942_276509.jpg` |
| B26 | 80-G-32792: Panorama of the Japanese Attack on Pearl Harbor (1941-12-07) | photo 3840x2419 | https://catalog.archives.gov/id/12009061 | NARA useRestriction: {"status": "Unrestricted"} | Hazy panorama of the harbour with smoke clouds on the horizon (NARA: "Panorama of the Japanese attack on Pearl Harbor") | Faint; mounted on a caption card (use the crop) | `src/photos/ph_panorama_32792.jpg` (crop: `src/photos/ph_panorama_32792_c.jpg`) |
| B27 | 80-G-32776: Photograph of Burning and Damaged Ships at Pearl Harbor (1941-12-07) | photo 3840x3100 | https://catalog.archives.gov/id/12009060 | NARA useRestriction: {"status": "Unrestricted"} | A Marine/sailor sentry with a rifle on a road beside a white building, a vast black smoke cloud over the harbour | No ships | `src/photos/ph_sentry_smoke_32776.jpg` |
| B28 | Pearl Harbor bombing. USS Nevada. Beached at Hospital Point (1941-12-07 (photo date per caption; the OWI/LoC print is dated "1942 Dec.")) | photo 3840x3080 | https://www.loc.gov/pictures/item/2017694985/ | The contents of the Library of Congress Farm Security Administration/Office of War Information Black-and-White Negatives are in the public domain and are free to use and reuse. Credit Line: Library of Congress, Prints & Photographs Division, Farm Security Administration/Office of War Information Black-and-White Negatives. For information about reproducing, publishing, and citing material from this collection, as well | Nevada beached at Hospital Point: tower masts and forward superstructure above the water line, smoke hanging at her bow (OWI print, issued Dec 1942) | LoC caption says "Beached at Hospital Point" | `src/photos/ph_loc_nevada_beached_hospital_point.jpg` |
| B29 | Pearl Harbor bombing. USS West Virginia a flame. Disregarding the dangerous possibilities of explosions, U.S. sailors man their boats at the side of the burning battleship, USS West Virginia, to better fight the flames started by Japanese torpedoes and bombs. Note the national colors flying against the smoke-blackend sky (1941-12-07 (photo date per caption; the OWI/LoC print is dated "1942 Dec.")) | photo 3840x3076 | https://www.loc.gov/pictures/item/2017694988/ | The contents of the Library of Congress Farm Security Administration/Office of War Information Black-and-White Negatives are in the public domain and are free to use and reuse. Credit Line: Library of Congress, Prints & Photographs Division, Farm Security Administration/Office of War Information Black-and-White Negatives. For information about reproducing, publishing, and citing material from this collection, as well | The West Virginia ablaze with fire boats spraying her; tripod masts and white water jets | West Virginia, not Nevada | `src/photos/ph_loc_west_virginia_afire.jpg` |
| B30 | Pearl Harbor bombing. Burning oil. Streaming from the shattered fuel tanks, oil turned parts of Pearl Harbor into a sea of flames, following the Japanese attacks. This picture was taken from near the naval air station boat landing. Barely visible through the smoke area are a damaged U.S. battleship and the capsized USS Oklahoma (1941-12-07 (photo date per caption; the OWI/LoC print is dated "1942 Dec.")) | photo 3840x3094 | https://www.loc.gov/pictures/item/2017695000/ | The contents of the Library of Congress Farm Security Administration/Office of War Information Black-and-White Negatives are in the public domain and are free to use and reuse. Credit Line: Library of Congress, Prints & Photographs Division, Farm Security Administration/Office of War Information Black-and-White Negatives. For information about reproducing, publishing, and citing material from this collection, as well | A wall of black smoke and fire from burning oil, a floating hull at lower right (LoC title: "Burning oil. Streaming from the shattered fuel tanks") | Not named | `src/photos/ph_loc_burning_oil.jpg` |
| B31 | Pearl Harbor bombing. USS Shaw. Hit by three bombs which exploded her forward magazine, the 1,500 ton destroyer Shaw lies a twisted mass of wreckage in the heavily-bombed floating drydock YFD-2. Note the bow of the Shaw lying on its side in the foreground. Part of the drydock, at right, is under water while the other side is listing heavily. Both the Shaw and the drydock are now back in use (1941-12-07 (photo date per caption; the OWI/LoC print is dated "1942 Dec.")) | photo 3840x3076 | https://www.loc.gov/pictures/item/2017694984/ | The contents of the Library of Congress Farm Security Administration/Office of War Information Black-and-White Negatives are in the public domain and are free to use and reuse. Credit Line: Library of Congress, Prints & Photographs Division, Farm Security Administration/Office of War Information Black-and-White Negatives. For information about reproducing, publishing, and citing material from this collection, as well | The destroyer Shaw burning in the floating drydock after her forward magazine exploded | Caption names the Shaw | `src/photos/ph_loc_shaw.jpg` |
| B32 | Pearl Harbor bombing. USS Oklahoma. Rescue crews are shown here working on the upturned hull of the 29,000 ton battleship USS Oklahoma, which capsized in Pearl Harbor after being blasted by Japanese warplanes. Holes were burned through the hull to permit the rescue of some of the men trapped below. Note one of the Oklahoma's launches in the foreground. The battleship, USS Maryland is in the background (1941-12-07 (photo date per caption; the OWI/LoC print is dated "1942 Dec.")) | photo 3840x3099 | https://www.loc.gov/pictures/item/2017694991/ | The contents of the Library of Congress Farm Security Administration/Office of War Information Black-and-White Negatives are in the public domain and are free to use and reuse. Credit Line: Library of Congress, Prints & Photographs Division, Farm Security Administration/Office of War Information Black-and-White Negatives. For information about reproducing, publishing, and citing material from this collection, as well | Oklahoma's upturned hull with rescue crews and a small boat alongside, tower of another battleship behind | LoC caption: USS Oklahoma rescue | `src/photos/ph_loc_oklahoma_rescue.jpg` |
| B33 | USS Arizona, at height of fire, following Japanese aerial attack on Pearl Harbor, Hawaii (1941-12-07) | photo 3840x3063 | https://www.loc.gov/pictures/item/92500933/ | No known restrictions on publication. | Arizona at the height of the fire: dense black smoke and her tower, a launch in the foreground. Official U.S. Navy photograph | LoC title: USS Arizona, at height of fire | `src/photos/ph_loc_arizona_height_of_fire.jpg` |
| B34 | Wreckage of USS Arizona, Pearl Harbor, Hawaii, December 7, 1941 (1941-12-07) | photo 3049x3840 | https://www.loc.gov/pictures/item/2002719512/ | No known restrictions on publication. | The Arizona's wreck from the water: crane boom bent over, bridge collapsed, tripod tower standing | LoC title: Wreckage of USS Arizona | `src/photos/ph_loc_arizona_wreck.jpg` |
| B35 | [Pearl Harbor naval base and U.S.S. Shaw ablaze after the Japanese attack] (1941-12-07) | photo 3840x3361 | https://www.loc.gov/pictures/item/98506923/ | No known restrictions on publication. | Palm fronds at the left, a huge orange-white explosion and black smoke over a pier; the Shaw's magazine blowing up | LoC title: "Pearl Harbor naval base and U.S.S. Shaw ablaze" | `src/photos/ph_loc_shaw_ablaze.jpg` |


### Film: 330-DIMOC-DNDEE161692: Pearl Harbor Attack Film (DoD)

- record: https://catalog.archives.gov/id/147970730  
- rights (verbatim): NARA useRestriction: {"note": "Some or all of this material may be restricted by copyright or other intellectual property rights restrictions.", "specificUseRestrictions": ["Copyright"], "status": "Restricted - Possibly"} - VERIFY: US government camera film (Navy/Army Signal Corps/DoD), so a federal work, but NARA flags possible copyright; confirm with NARA before use  
- file: `src/film/pearl_harbor_attack_dod.mp4` (336.3 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/pearl_harbor_attack_dod_01..05.jpg`  
- note: DoD compilation of real colour film from 7 Dec 1941. Heavily faded to blue; 720x480, 5:36. The NARA record says the film origin is not stated: the tape may be a compilation. Mark the clip as "film shot at Pearl Harbor on 7 Dec 1941" and not as the finished Ford movie.  
- how it was checked: viewed on 6 s sheets; Nevada shots NOT confirmed by eye  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 10-16.5 | NARA leader card then a dark frame | Leader |
| 30-48 | A ship's mast and rigging at the pier, then a long view of burning ships under a black smoke wall | Ship names not on screen |
| 54-63 | Smoke over the harbour from a quay | - |
| 72-95 | Capsized/listing hull at the pier, smashed gear (the Oglala rolling over per the DoD index) | Per index, not read off the picture |
| 96-160 | Harbor with columns of black smoke and a distant ship; the DoD index puts "USS Nevada underway ... running aground at Hospital Point" at 0:54-1:21 but she is a tiny, soft speck | Nevada not identifiable in my viewing: soft and faded; verify against the DoD index before use |
| 140-164 | Gun and a quay with smoke behind (1:42) | - |


### Film: 428-NPC-13585: DECEMBER 7th (MN-2868/MN-2862), raw outtakes

- record: https://catalog.archives.gov/id/79638  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/dec7_outtakes_13585.mp4` (727.2 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/dec7_outtakes_13585_01..11.jpg`  
- note: RG 428 raw/outtake film from the Navy-made "December 7th" (Ford/Toland). B&W, 720x480, 12:07. NOT THE ATTACK: this is the 1942 salvage period, and some shots are STAGED (actors on a bridge). Use only as "after the attack"; never for 7 Dec.  
- how it was checked: viewed on one 6 s sheet (first 4:48): the NARA shot list the scout quotes ("Colors flying from stern of USS NEVADA") is not located by me  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 6-42 | Officers on a bridge wing with binoculars: STAGED scene for the Ford film | DO NOT USE as real: re-creation material |
| 48-72 | A ship's bow with men dropping cables over the side | Unclear |
| 84-125 | Large ships (a tug and a battleship hull) in the harbour with crowds on deck, then water pouring out of hull openings as the ship is pumped out | Salvage, 1942; ship names are not on screen in what I viewed |
| 125-165 | A battleship hull at a pontoon with water jets, tug alongside | Which battleship: not named |
| 165-215 | Tug alongside a battleship with the tripod mast, crowds on the barge deck | Not named |
| 215-290 | Men at a drydock gate and pumps; ship's hull emptied | - |


### Film: 428-NPC-13590: DECEMBER 7th (MN-2862 & MN-2868), raw outtakes

- record: https://catalog.archives.gov/id/79640  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/dec7_outtakes_13590.mp4` (668.0 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/dec7_outtakes_13590_01..10.jpg`  
- note: RG 428 raw outtakes. B&W, 720x480, 11:08. NOT THE ATTACK; some of it is staged. Scout: shots 19-21 are Nevada leaving Pearl in new war paint (not located by me).  
- how it was checked: viewed on two 6 s sheets (to 9:36): ships are not identified by me  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 12-50 | Distant ship on the horizon with smoke puffs in the sky | Staged/or exercise: not the attack |
| 54-100 | A twin gun mount and wave spray on a ship under way, crew at the rail | Which ship: not stated |
| 102-126 | Landing boats at a Honolulu quay with Diamond Head behind | - |
| 166-200 | A crane and gantry over a repair basin, a flag | - |
| 200-230 | A big hull in drydock, bow view | - |
| 245-285 | Battleship broadside at distance: a tripod tower behind a crane (about 4:06-4:36) and a long twin-gun turret line | Identity not stated |
| 330-360 | The Bay Bridge (San Francisco) at dusk and a city skyline | Place only |
| 370-395 | A battleship sailing under/near the Bay Bridge with the skyline behind | Not identified as Nevada |
| 420-452 | Battleship beam view, sailors on the rail, a gun turret and the bridge (about 7:00-7:12) | - |
| 450-510 | Army trucks full of cheering soldiers in Honolulu streets | - |
| 540-570 | A battleship at distance with a small boat below, then a close bow/side view (8:42-9:30) | - |


### Film: 428-NPC-34385: "DECEMBER SEVENTH" MN-2868 (1942 outtakes)

- record: https://catalog.archives.gov/id/84082  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/dec7_outtakes_34385.mp4` (480.8 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/dec7_outtakes_34385_01..07.jpg`  
- note: RG 428. 720x480, 8:01. NOT THE ATTACK. Only skimmed.  
- how it was checked: only the NARA title checked; not used by me  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-480.8 | Raw outtake reel (1942): not catalogued by me | Skimmed, not described: treat as unchecked |


### Film: 428-NPC-16439: RESULTS OF PEARL HARBOR RAID

- record: https://catalog.archives.gov/id/80388  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/results_pearl_raid.mp4` (372.6 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/results_pearl_raid_01..06.jpg`  
- note: RG 428. 720x480, 6:13. Post-attack aftermath. Scout list: "CU Sign on turret of the USS NEVADA, from CincPac to Pacific Fleet ... Marine guards on the USS NEVADA". Not viewed by me.  
- how it was checked: scout list only  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-372.6 | Aftermath of the raid; the scout lists a turret sign and Marine guards on Nevada | Not viewed by me; times unknown |


### Film: 428-NPC-47635: Pearl Harbor (1942, colour)

- record: https://catalog.archives.gov/id/2663400  
- rights (verbatim): NARA useRestriction: {"note": "Some or all of this material may be restricted by copyright or other intellectual property rights restrictions.", "status": "Restricted - Possibly"} - VERIFY: US government camera film (Navy/Army Signal Corps/DoD), so a federal work, but NARA flags possible copyright; confirm with NARA before use  
- file: `src/film/pearl_1942_colour_47635.mp4` (587.9 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/pearl_1942_colour_47635_01..09.jpg`  
- note: RG 428. COLOUR 720x480, 9:48. Spring 1942. Scout: "USS Nevada (BB-36) as it moved towards drydock, a tugboat ... towed the USS Nevada out of drydock". Not viewed by me.  
- how it was checked: scout list only  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-587.9 | Salvage-period colour (spring 1942): Nevada and tug per the scout | Not viewed by me; times unknown. Not 7 Dec |


## C. Salvage, rebuild, and the ship before the war (1915-1943)

| # | title | type | record URL | rights (verbatim) | what it shows | what it does NOT show / caveats | local file |
|---|---|---|---|---|---|---|---|
| C1 | Pearl Harbor bombing. Nevada underway. Severely damaged and beached during the Japanese attack on Pearl Harbor, the USS Nevada gets ready to leave her Hawaiian anchorage for permanent repairs at a U.S. port. Temporary repairs made at Pearl Harbor enabled the battleship to make the voyage under her own power (1942-04 (photo; the OWI print is dated "1942 Dec."; the Nevada left Pearl Harbor in April 1942)) | photo 3840x3056 | https://www.loc.gov/pictures/item/2017694997/ | The contents of the Library of Congress Farm Security Administration/Office of War Information Black-and-White Negatives are in the public domain and are free to use and reuse. Credit Line: Library of Congress, Prints & Photographs Division, Farm Security Administration/Office of War Information Black-and-White Negatives. For information about reproducing, publishing, and citing material from this collection, as well | Nevada seen across calm water with three men wading in the foreground: the repaired battleship getting ready to leave Pearl Harbor for permanent repairs (OWI caption) | LoC caption: "gets ready to leave her Hawaiian anchorage for permanent repairs". 1942, not 7 Dec 1941 | `src/photos/c_loc_nevada_underway_1942.jpg` |
| C2 | USS Nevada (BB-36) (1943) | photo 3840x3126 | https://catalog.archives.gov/id/38329769 | NARA useRestriction: {"status": "Unrestricted"} | Nevada in her rebuilt WWII form seen from the starboard bow, tripod masts, turrets and a bright sea (NARA record: Boston Navy Yard / convoy duty period) | Small print; NARA gives only "1943" | `src/photos/c_nevada_1943_boston.jpg` |
| C3 | 19-N-5-25-7: Photograph of USS Nevada (BB-36) (1915-10-03) | photo 3840x2945 | https://catalog.archives.gov/id/496080801 | NARA useRestriction: {"status": "Unrestricted"} | The new Nevada on trials, broadside, two cage masts and a thick smoke plume (3 Oct 1915) | Early form: cage masts, not the later tripods. Mounted on a BuShips card with a colour bar (use the crop) | `src/photos/c_nevada_1915_trial_a.jpg` (crop: `src/photos/c_nevada_1915_trial_a_c.jpg`) |
| C4 | 19-N-5-25-14: Photograph of USS Nevada (BB-36) (1915-11-15) | photo 3840x2951 | https://catalog.archives.gov/id/496080813 | NARA useRestriction: {"status": "Unrestricted"} | Nevada on trials, bow-on three-quarter at speed, heavy black smoke and a big bow wave (15 Nov 1915) | Cage masts. Card with colour bar (crop) | `src/photos/c_nevada_1915_trial_b.jpg` (crop: `src/photos/c_nevada_1915_trial_b_c.jpg`) |
| C5 | 19-N-5-25-10: Photograph of USS Nevada (BB-36) (1916-11-03) | photo 3840x2994 | https://catalog.archives.gov/id/496080807 | NARA useRestriction: {"status": "Unrestricted"} | Nevada on trials, broadside to the right, smoke streaming back from the funnel (3 Nov 1916) | Cage masts. Card with colour bar (crop) | `src/photos/c_nevada_1916_trial.jpg` (crop: `src/photos/c_nevada_1916_trial_c.jpg`) |
| C6 | 19-N-1996: Photograph of USS Nevada (BB-36) (1918-05-11) | photo 3840x2908 | https://catalog.archives.gov/id/496080830 | NARA useRestriction: {"status": "Unrestricted"} | Nevada at anchor in 1918, bow three-quarter, flags and cage masts, dark grey paint (11 May 1918) | Cage masts. Card with colour bar (crop) | `src/photos/c_nevada_1918.jpg` (crop: `src/photos/c_nevada_1918_c.jpg`) |
| C7 | 19-N-11014: Photograph of USS Nevada (BB-36) (1927-06-04) | photo 3840x2991 | https://catalog.archives.gov/id/496080868 | NARA useRestriction: {"status": "Unrestricted"} | Nevada under way in 1927, flat sea, the cage masts still in place | Before the 1927-30 rebuild. Card (crop) | `src/photos/c_nevada_1927.jpg` (crop: `src/photos/c_nevada_1927_c.jpg`) |
| C8 | 19-N-13713: Photograph of USS Nevada (BB-36) (1929-09-18) | photo 3840x2909 | https://catalog.archives.gov/id/496080872 | NARA useRestriction: {"status": "Unrestricted"} | Nevada at the Norfolk Navy Yard, 18 Sep 1929, the masts being rebuilt as tripods and a crane at the stern | Printed note: "Norfolk Navy Yard Portsmouth Va, Sept 18 1929". Card (crop) | `src/photos/c_nevada_1929_norfolk.jpg` (crop: `src/photos/c_nevada_1929_norfolk_c.jpg`) |
| C9 | 19-N-15041: Photograph of USS Nevada (BB-36) (1935) | photo 3840x2909 | https://catalog.archives.gov/id/496080874 | NARA useRestriction: {"status": "Unrestricted"} | Nevada in 1935, bow-on three-quarter, the tripod masts and 14-in turrets of the form she kept to Pearl Harbor | Card (crop) | `src/photos/c_nevada_1935.jpg` (crop: `src/photos/c_nevada_1935_c.jpg`) |
| C10 | 19-N-2844: Photograph of USS Nevada (BB-36) (1920-01) | photo 3840x2896 | https://catalog.archives.gov/id/496080862 | NARA useRestriction: {"status": "Unrestricted"} | Crew standing at attention on a bare wooden deck, Captain McDougall and officers at the far end (Guantanamo Bay, Jan 1920) | Pre-war people shot; not Pearl Harbor. Card (crop) | `src/photos/c_nevada_1920_guantanamo.jpg` (crop: `src/photos/c_nevada_1920_guantanamo_c.jpg`) |
| C11 | NEVADA on trial run (22 1/2 knots) (1915) | photo 3840x2798 | https://www.loc.gov/pictures/item/2014700981/ | No known restrictions on publication. For more information, see George Grantham Bain Collection - Rights and Restrictions Information https://www.loc.gov/rr/print/res/274_bain.html | NEVADA on trial run at 22.5 knots, a big dark smoke plume, cage masts (Bain News Service) | Bain print, 1915-16; cage masts, not the WWII look | `src/photos/c_loc_nevada_trial_bain.jpg` |


## D. Atlantic war 1943-44 (Attu, Normandy, Utah Beach, Cherbourg)

| # | title | type | record URL | rights (verbatim) | what it shows | what it does NOT show / caveats | local file |
|---|---|---|---|---|---|---|---|
| D1 | 2015-15: USS Nevada (BB-36) (1944-06-06) | photo 800x642 | https://catalog.archives.gov/id/350894712 | NARA useRestriction: {"status": "Unrestricted"} | Nevada firing a salvo on D-Day: a huge black powder cloud at her muzzles and the long grey hull under way. Caption: "firing a salvo at enemy shore batteries north of Utah Beach ... picture taken from the USS Quincy. Credit: U.S. Navy" | From the Truman Library photo collection (NARA item 2015-15, credit U.S. Navy). Utah Beach sector; not Cherbourg | `src/photos/d_nevada_utah_salvo_truman.jpg` |
| D2 | 80-G-231636: 14" Guns of the USS Nevada Shells Nazi Shore Batteries at Cherbourg, France (1944-06-25) | photo 3840x2656 | https://catalog.archives.gov/id/219775743 | NARA useRestriction: {"status": "Unrestricted"} | Nevada firing at Cherbourg from the USS Ancon: the 14-in guns flash and a pall of smoke hangs over the sea; the ship is a small grey shape | NARA date field says 1 Jun 1944, the text says Cherbourg (25 Jun). Ship is small. Mounted on a caption card (crop) | `src/photos/d_cherbourg_nevada_231636.jpg` (crop: `src/photos/d_cherbourg_nevada_231636_c.jpg`) |
| D3 | 80-G-231637: 14" Guns of the USS Nevada Shells Nazi Shore Batteries at Cherbourg, France (1944-06-25) | photo 3840x2656 | https://catalog.archives.gov/id/219775742 | NARA useRestriction: {"status": "Unrestricted"} | Closer: Nevada firing a broadside past a ship's stanchion, battle flags flying, smoke hanging at the bow (taken from the Ancon) | A pole crosses the frame (the stanchion). Caption card (crop) | `src/photos/d_cherbourg_nevada_231637.jpg` (crop: `src/photos/d_cherbourg_nevada_231637_c.jpg`) |
| D4 | 80-G-252294: Sailors Attending Catholic Mass Aboard the USS Nevada Waiting for D-Day (1944-06-02) | photo 3840x2676 | https://catalog.archives.gov/id/404794396 | NARA useRestriction: {"status": "Unrestricted"} | Two prints of sailors packed on Nevada's deck at Catholic Mass beneath the 14-in turret, 2 Jun 1944 at an English port waiting for D-Day | Mounted card with two prints (crop) | `src/photos/d_mass_aboard_nevada_252294.jpg` (crop: `src/photos/d_mass_aboard_nevada_252294_c.jpg`) |
| D5 | 80-G-231976: Enemy Shore Batteries at Cherbourg, France, Return Fire of Allied Naval Forces, as Seen From the USS Quincy (1944-06-25) | photo 3840x2628 | https://catalog.archives.gov/id/219775737 | NARA useRestriction: {"status": "Unrestricted"} | Water columns and smoke rising as German shore batteries at Cherbourg return fire on the Allied ships (25 Jun 1944, from USS Quincy) | Small print on a large card (crop); no ship readable | `src/photos/d_cherbourg_return_fire_231976.jpg` (crop: `src/photos/d_cherbourg_return_fire_231976_c.jpg`) |
| D6 | 80-G-231643: German Shell Fire on Iles Saint Marcouf, Morning of "D" Day (1944-06-06) | photo 3840x2655 | https://catalog.archives.gov/id/219775761 | NARA useRestriction: {"status": "Unrestricted"} | German shell bursting by Iles Saint-Marcouf off Utah Beach on the morning of D-Day, seen from USS Quincy | Flat grey sea; subject small. Caption card (crop) | `src/photos/d_st_marcouf_shellfire_231643.jpg` (crop: `src/photos/d_st_marcouf_shellfire_231643_c.jpg`) |
| D7 | 80-G-231649: Minesweepers Exploding Mines in Boat Channel Across Cardonnet Bank off "Utah" Beach, Cherbourg Peninsula, "D" Day as Seen From USS Quincy (1944-06-06) | photo 3840x2647 | https://catalog.archives.gov/id/219775755 | NARA useRestriction: {"status": "Unrestricted"} | Minesweepers exploding mines in the boat channel off Utah Beach: a white burst on a grey sea, ships on the horizon | Caption card (crop) | `src/photos/d_minesweepers_utah_231649.jpg` (crop: `src/photos/d_minesweepers_utah_231649_c.jpg`) |
| D8 | 80-G-231247: Part of Task Force, View of Landing Craft With French Coast in Background as Seen From USS Ancon (1944-06-06) | photo 3840x2636 | https://catalog.archives.gov/id/219775754 | NARA useRestriction: {"status": "Unrestricted"} | Landing craft and ships spread over the water with the French coast beyond, barrage balloons above, rigging and gun mounts of the USS Ancon in the foreground | Caption card (crop) | `src/photos/d_task_force_utah_231247.jpg` (crop: `src/photos/d_task_force_utah_231247_c.jpg`) |
| D9 | 80-G-244213: Soldiers in a "Duck" Headed for the Beach Head Are Viewed From the Bridge of the Battleship Arkansas (1944-06-06) | photo 3840x2634 | https://catalog.archives.gov/id/219775705 | NARA useRestriction: {"status": "Unrestricted"} | A DUKW heading for the beach, seen from the bridge of the battleship Arkansas over the twin 12-in guns of a forward turret | Arkansas, not Nevada (but the same job). Caption card (crop) | `src/photos/d_view_from_arkansas_244213.jpg` (crop: `src/photos/d_view_from_arkansas_244213_c.jpg`) |
| D10 | 80-G-257293: Close-Up of a German Heavy Coastal Battery Draped in Netting (1944-09-22) | photo 3840x2614 | https://catalog.archives.gov/id/219775707 | NARA useRestriction: {"status": "Unrestricted"} | A heavily camouflaged German gun position on the quay at Le Havre: a concrete casemate under netting with a gun barrel | Le Havre, Sept 1944, not Cherbourg; generic coastal-gun image. Caption card (crop) | `src/photos/d_german_battery_257293.jpg` (crop: `src/photos/d_german_battery_257293_c.jpg`) |
| D11 | 80-G-285135: View of the Pontoon Causeway at "Utah" Beach (1944-11-07) | photo 3840x2677 | https://catalog.archives.gov/id/219775709 | NARA useRestriction: {"status": "Unrestricted"} | The pontoon causeway at Utah Beach with landing craft and a ship alongside, a flat sea behind | Nov 1944 (months after D-Day). Caption card (crop) | `src/photos/d_pontoon_causeway_utah.jpg` (crop: `src/photos/d_pontoon_causeway_utah_c.jpg`) |
| D12 | 80-G-252597: Landing Craft Protected By Destroyers Going in to Beach on Coast of France on D-Day (1944-06-06) | photo 2714x2120 | https://catalog.archives.gov/id/219775774 | NARA useRestriction: {"status": "Unrestricted"} | Landing craft going in to the French coast on D-Day, a gunner's director in the foreground, destroyers around | Normandy, sector not stated | `src/photos/d_landing_craft_destroyers_252597.jpg` |
| D13 | Attu, Aleutian Islands. Landing boats pouring soldiers and their equipment onto the beach at Massacre Bay. This is the Southern landing force (1943-05) | photo 3840x3133 | https://www.loc.gov/pictures/item/2017872356/ | No known restrictions on images made by the U.S. government; images copied from other sources may be restricted. For information, see U.S. Farm Security Administration/Office of War Information Black & White Photographs https://www.loc.gov/rr/print/res/071_fsab.html | Landing boats at Massacre Bay on Attu putting soldiers and equipment ashore on a grey beach | Army landing on Attu in May 1943, no Nevada. OWI print | `src/photos/d_attu_landing_loc.jpg` |
| D14 | [Americans setting up tents on the beach after amphibious landings; Holts Bay, Attu, Aleutian Islands] (1943-05) | photo 1536x1247 | https://www.loc.gov/pictures/item/2017656317/ | No known restrictions on publication. | Tents going up on a bleak beach at Holts Bay, Attu, with mist-covered hills behind (photo by U.S. Navy) | No ship; small scan (1536 px) | `src/photos/d_attu_camp_loc.jpg` |


### Film: 428-NPC-4312: USS NEVADA BOMBARDS FRENCH COAST PRIOR TO INVASION LSTs AND (5 Jun 1944)

- record: https://catalog.archives.gov/id/77052  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/nevada_bombards_france.mp4` (282.4 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/nevada_bombards_france_01..04.jpg`  
- note: RG 428. B&W 720x480, 4:42. NARA title says Nevada bombards the French coast; the picture does not show a 14-in salvo. Scout: shot 1 "MS USS NEVADA bombarding French coast". On my 6 s sheet the content is not what the title promises.  
- how it was checked: viewed on one 6 s sheet  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 6-20 | Rows of rocket-launcher/gun tubes at a ship's rail, a blast of smoke at 0:18 | Not Nevada's 14-in guns, not identified |
| 20-52.6 | Sailors handling large brass shell cases in a magazine/ready room, close-ups | 5-in ammunition per the title; ship not stated |
| 62.4-72.8 | A canvas bag stencilled "COMBAT PHOTO UNIT 8 U.S. NAVY" | Props/identification of the camera unit |
| 72.8-280 | A convoy of ships and landing craft on a grey sea under a heavy sky, from a ship's wake | No Nevada firing in what I viewed; a transport at 3:00 is not named |


### Film: 428-NPC-4313: INVASION OF FRANCE, ACTIVITY OFF COAST ON "D" DAY (6 Jun 1944)

- record: https://catalog.archives.gov/id/77053  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/dday_offshore.mp4` (556.0 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/dday_offshore_01..08.jpg`  
- note: RG 428. B&W 720x480, 9:16. Scout: "LCVPs heading for beach, USS NEVADA fires BG ... LCVP sinking".  
- how it was checked: viewed on one 6 s sheet (first 4:48)  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 6-70 | A sailor reading a message slip/dispatch, close-ups of the card | Which ship is not named |
| 70-100 | A convoy of ships and fast boats in a grey dawn | Which ships: not identified |
| 220-276 | Landing craft launching from a ship and men in a sinking boat | Not identified as Nevada |


### Film: 428-NPC-4308: ACTIVITY IN SEINE BAY NEAR ST. MARCOUX; LANDING CRAFT MOVE... (7 Jun 1944)

- record: https://catalog.archives.gov/id/77048  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/seine_bay_nevada.mp4` (272.3 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/seine_bay_nevada_01..04.jpg`  
- note: RG 428. B&W, 720x480, 4:32. Scout: "MS USS NEVADA fires, LCI fires FG". Not viewed by me.  
- how it was checked: scout list only  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-272 | Seine Bay off Normandy 7 Jun 1944; Nevada firing per the scout | Not viewed |


## E. Pacific 1945 (Iwo Jima, Okinawa, the kamikaze)

| # | title | type | record URL | rights (verbatim) | what it shows | what it does NOT show / caveats | local file |
|---|---|---|---|---|---|---|---|
| E1 | 80-G-307090: Photograph of LCI-52 Tied to the USS Nevada (BB-36) off Iwo Jima (1945-02-22) | photo 1929x1278 | https://catalog.archives.gov/id/148728558 | NARA useRestriction: {"status": "Unrestricted"} | Crowded decks as the landing craft LCI-52 lies alongside the Nevada off Iwo Jima (22 Feb 1945) | Mooring/transfer scene, not gunfire. NARA scan is small (896 KB) | `src/photos/e_lci52_alongside_nevada_307090.jpg` |
| E2 | 80-G-307089: Photograph of LCI-52 Tied to the USS Nevada (BB-36) off Iwo Jima (1945-02-22) | photo 1326x1942 | https://catalog.archives.gov/id/148728556 | NARA useRestriction: {"status": "Unrestricted"} | Aerial/high view of the LCI-52 bows tied to a larger ship with crane and gun tubs, off Iwo Jima | Small scan; second view of the same transfer | `src/photos/e_lci52_alongside_nevada_307089.jpg` |


### Film: 428-NPC-7512: AERIAL AND NAVAL BOMBARDMENT OF OKINAWA (Apr 1945)

- record: https://catalog.archives.gov/id/78111  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/okinawa_bombardment_hd.mp4` (421.1 s, 1920x1080 h264 24/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/okinawa_bombardment_hd_01..06.jpg`  
- note: RG 428. 1920x1080 B&W (4:3 pillarboxed), 7:01. The same film is on archive.org as NPC-7512 ("USS Nevada (BB-36)", licenseurl publicdomain/mark/1.0).  
- how it was checked: viewed on two 6 s sheets (to 4:48); the 14-in "DA" shots in the NARA list are not located by me  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 6-14.2 | A grinning sailor holds the slate card to camera | Slate only |
| 14.2-29.6 | Two cameramen (one with a movie camera) shooting from a gun tub | People not identified |
| 29.6-87.9 | Okinawa shore at a distance: spots of gunfire and smoke on the low hills | Not yet Nevada guns |
| 87.9-135.3 | A crowd of gun crew around a director/rangefinder; the shore with shell bursts | Ship named by NARA title |
| 135.3-188.8 | Planes over the coast, shore smoke, gun crew in a mount | - |
| 214-252 | A gun mount firing at the beach; a cruiser broadside at distance | - |
| 254-300 | Gun-director men and shell bursts on the shore | - |


### Film: 428-NPC-8390: USS NEVADA; SCENES ABOARD (colour)

- record: https://catalog.archives.gov/id/78476  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/nevada_scenes_colour.mp4` (332.4 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/nevada_scenes_colour_01..05.jpg`  
- note: RG 428. COLOUR 720x480, 5:32, undated. Scout: Iwo Jima, Feb 1945 ("Muzzles of main battery rifles as they fire ... smoke rings"). The anchorage with many landing craft and a low flat coast may equally be Normandy: do NOT caption the place until checked.  
- how it was checked: viewed on two 6 s sheets (first 4:48)  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 7-24 | Smoke and gunfire on a low coast from a ship | Place unconfirmed |
| 24-35.6 | A battleship (grey, tripod-type mast) sitting in an anchorage, bow-on | Ship not identified; not stated to be Nevada |
| 35.6-64.5 | Sailors in helmets at the rail with binoculars; a man writing on a pad | - |
| 64.5-70.3 | Twin gun barrels and the sea at night-blue | - |
| 70.3-104.5 | A big ship firing with white smoke, other ships beyond; shore bursts | - |
| 104.5-124.9 | Rows of brass shell cases in a magazine and a gun muzzle at the edge | Ordnance close-up |
| 124.9-185 | Sailors in white hats and steel helmets at their stations, handling gear and rations | - |
| 185-332.4 | A crowded anchorage with landing craft, a low coast, helmeted gun crews | - |


### Film: 428-NPC-8391: USS NEVADA; IWO JIMA (colour)

- record: https://catalog.archives.gov/id/78477  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/nevada_iwo_jima.mp4` (659.2 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/nevada_iwo_jima_01..10.jpg`  
- note: RG 428. COLOUR 720x480, 10:59. WARNING: the first 2:45 show wounded and bodies being handled on a ship's deck.  
- how it was checked: viewed on one 6 s sheet (first 4:48)  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 14.7-165 | Treatment of wounded men on a ship's deck and carrying stretchers with bodies | Sensitive. Not stated to be Nevada's own |
| 168-288 | Mount Suribachi and the Iwo Jima coast under shell bursts, in colour | Place by the title; Suribachi visible |
| 288-310 | Smoke from a ship firing and splashes, small craft near | - |


### Film: 111-ADC-9878: USS NEVADA IS HIT (27 Mar 1945)

- record: https://catalog.archives.gov/id/23643  
- rights (verbatim): NARA useRestriction: {"specificUseRestrictions": ["Copyright"], "status": "Restricted - Possibly"} - VERIFY: US government camera film (Navy/Army Signal Corps/DoD), so a federal work, but NARA flags possible copyright; confirm with NARA before use  
- file: `src/film/nevada_is_hit.mp4` (450.9 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/nevada_is_hit_01..07.jpg`  
- note: Filed in NARA's Army Signal Corps series (111-ADC) but the film itself is a US NAVY Bureau of Aeronautics production (opening card "JBA ON U.S.S. NEVADA 27 MARCH 1945", end card "THE END Bureau of Aeronautics 1945"): federal work. B&W 720x480, 7:31. WARNING: shows dead and wounded. After 3:48 the reel continues with a different ship (USS RANDOLPH, 11 March 1945): NOT Nevada.  
- how it was checked: viewed on two 6 s sheets; windows approximate (+/-3 s)  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 6-14.4 | Title card "JBA ON U.S.S. NEVADA 27 MARCH 1945" | Title only |
| 14.4-28.8 | Sea and sky with distant ships; small dark shapes in the sky (the attacking planes) | Planes tiny |
| 28.8-52.3 | Fire and flash inside a hangar-like space and smoke on deck right after the hit | Interior view, ship by the title |
| 52.3-119.8 | Aftermath on deck: a stretcher bearer, a debris-strewn deck, men with hoses, a fire main | Contains bodies at about 1:24 |
| 119.8-177.6 | Wrecked aircraft with the US star and number "10" lying on the deck, crew dragging fittings, a doctor treating a man | Bodies and casualties on deck |
| 177.6-198 | A turret top and gun house with a shell hole and gouges, crew gathering | - |
| 198-228 | Crew sitting in a group, battleship superstructure with a crowd, the end card at 3:48 | The Nevada part ends at 3:48; the rest (Randolph, fire at night) is another ship |


### Film: 428-NPC-11162: Activity Aboard the USS Nevada (kamikaze, March 1945, colour)

- record: https://catalog.archives.gov/id/2485240  
- rights (verbatim): NARA useRestriction: {"note": "Some or all of this material may be restricted by copyright or other intellectual property right restrictions.", "status": "Restricted - Possibly"} - VERIFY: US government camera film (Navy/Army Signal Corps/DoD), so a federal work, but NARA flags possible copyright; confirm with NARA before use  
- file: `src/film/nevada_kamikaze_colour_a.mp4` (581.8 s, 720x480 h264 60/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/nevada_kamikaze_colour_a_01..09.jpg`  
- note: RG 428. COLOUR 720x480, 9:42. Shows the damage and casualties of the 27 Mar 1945 kamikaze hit: use with care. archive.org copy NPC-11162 is tagged publicdomain/mark/1.0. Not viewed by me.  
- how it was checked: scout list only  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 0-581.8 | Damage and casualties from the kamikaze hit (scout) | Not viewed by me |


## F. The 1948 sinking

_No stills in this group._


### Film: 428-NPC-3646: SINKING THE USS NEVADA (reel 1 of 2), 31 Jul 1948

- record: https://catalog.archives.gov/id/76879  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/sinking_1948_r1.mp4` (524.6 s, 1920x1080 h264 24/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/sinking_1948_r1_01..08.jpg`  
- note: RG 428. 1920x1080 B&W (4:3 pillarboxed), 8:45. The ship is not named on screen: "Nevada" comes from NARA's title.  
- how it was checked: viewed on two 6 s sheets; cut list by scene detection (0.22)  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 55.4-69 | Close low aerial of the burning battleship: superstructure and foremast, smoke bursting at the bow, then a white-out flash | Ship by title only |
| 69-98.2 | Aerial broadside passes: the ship, scarred and scorched, rolls through frame and out | - |
| 98.2-142.3 | Aerial: the ship under a long smoke plume streaming from the stern, small boat at upper right | - |
| 142.3-164 | Distant ship, white splashes near her | - |
| 167.6-185.4 | Distant burning ship with explosions beside her | - |
| 185.4-230 | Burning ship, bursts beside the hull; the plume | - |
| 257.5-300 | Distant ship, shell splashes | - |
| 360-432.9 | The burning hulk from a high angle, a bomb splash and smoke | - |
| 366-399.8 | Aerial: the ship with its stern burning | - |
| 399.8-432.9 | Aerial: the hulk smoking, close | - |
| 432.9-461.7 | Aerial close: the ship down by the stern, white spray from near-misses | - |
| 461.7-487.8 | Close aerial of the burning battleship, rolling toward the camera | - |
| 487.8-524.6 | Distant ship, many white splashes from rows of bombs; then a long line of splashes | - |


### Film: 428-NPC-3647: SINKING THE USS NEVADA (reel 2 of 2), 31 Jul 1948

- record: https://catalog.archives.gov/id/76880  
- rights (verbatim): NARA useRestriction: {"status": "Undetermined"} - US federal film (Navy/Signal Corps), public domain; "Undetermined" is NARA's default for unreviewed reels  
- file: `src/film/sinking_1948_r2.mp4` (528.4 s, 1920x1080 h264 24/1 fps (NARA mp4 as downloaded, not re-encoded)); sheets: `sheets/sinking_1948_r2_01..08.jpg`  
- note: RG 428. 1920x1080 B&W (4:3 pillarboxed), 8:48. The ship is not named on screen. NARA's shot list also has the tug (title: "Sea-going tug towing BB at sea"): make sure each shot you use is the battleship.  
- how it was checked: viewed on two 6 s sheets  

| window (s) | shows | does NOT show / caveats |
|---|---|---|
| 6-56 | A big ship and a small tug in the open sea from a plane (the tow-out) | The tug and the BB are both small |
| 56-95 | Close aerial of the scarred battleship: superstructure scorched, tripod tower, side cut open (1:22 is the best full broadside) | Ship by title only |
| 95-115 | The ship's deck seen from almost straight above: a mass of damaged gear and the wake | - |
| 110-125 | A tug with its wake alongside the hulk | The tug is the main subject |
| 125-330 | Distant ship on a flat sea; shell splashes and smoke around her; the hulk being shelled | Ship small |
| 330-360 | The battleship from above, three-quarter, with white bursts beside her; then from the side | - |
| 360-480 | Distant, hazy: the hulk smoking, planes passing, bombs bursting | Very small subject |
| 498-528 | The burning battleship close, smoke pouring from the superstructure, then from above, flames near the stern | The last frames: she is still afloat; the capsizing is NOT in this film (not located) |


## G. People (Hill, Ross, Thomas, admirals)

_No stills in this group._


## H. Generic / illustrative b-roll (USS Iowa firing, submarine USS Nevada SSBN-733)

| # | title | type | record URL | rights (verbatim) | what it shows | what it does NOT show / caveats | local file |
|---|---|---|---|---|---|---|---|
| H1 | 330-CFD-DN-SC-86-04795.jpeg: An overhead view of the battleship USS IOWA (BB-61) firing a 15-gun broadside to starboard (1984-07) | photo 3000x2004 | https://catalog.archives.gov/id/6404906 | NARA useRestriction: {"status": "Unrestricted"} | Overhead view of the battleship USS Iowa (BB-61) firing a 15-gun broadside to starboard: flame and smoke from nine 16-in and six 5-in guns, night/dusk light | The 1980s recommissioned Iowa (DoD, 1984), NOT the 1948 firing at Nevada. Use as "an Iowa broadside"; say so | `src/photos/h_iowa_broadside_1984.jpg` |
| H2 | 330-CFD-DN-SN-87-04598.jpeg: An aerial bow view of the battleship USS IOWA (BB-61) firing a broadside to starboard from the ship's Mark 7, 16-inch, 50 caliber guns during its shakedown cruise (1984-08-24) | photo 2856x1920 | https://catalog.archives.gov/id/6419831 | NARA useRestriction: {"status": "Unrestricted"} | Aerial bow view of Iowa firing a broadside to starboard: a giant spreading smoke cloud on a flat sea | Iowa in 1984, not 1948 | `src/photos/h_iowa_aerial_bow_1984.jpg` |
| H3 | 330-CFD-DN-ST-86-02456.jpeg: An aerial port view of the battleship USS IOWA (BB 61) firing to starboard from its No. 1 Mk 7 16-inch gun turret (1984-08) | photo 2741x1851 | https://catalog.archives.gov/id/6409036 | NARA useRestriction: {"status": "Unrestricted"} | Aerial port view of Iowa firing from her No. 1 Mark 7 16-in gun, a fireball and sun glitter on the sea, a second ship in the distance | Iowa in 1984, not 1948 | `src/photos/h_iowa_aerial_port_1984.jpg` |
| H4 | 330-CFD-DN-SN-87-00411.jpeg: A starboard bow view of the nuclear-powered strategic missile submarine USS NEVADA (SSBN 733) underway (1986-10-23) | photo 3000x2250 | https://catalog.archives.gov/id/6419504 | NARA useRestriction: {"status": "Unrestricted"} | The submarine USS Nevada (SSBN-733) under way, bow-on starboard view, sail and bow wave, B&W | The modern submarine, not the battleship. DoD photo | `src/photos/h_ssbn733_underway_1986.jpg` |
| H5 | 330-CFD-DN-ST-87-00388.jpeg: A starboard bow view of the nuclear-powered strategic missile submarine USS NEVADA (SSBN-733) underway (1986-08-16) | photo 2830x1850 | https://catalog.archives.gov/id/6420912 | NARA useRestriction: {"status": "Unrestricted"} | The nuclear submarine USS Nevada (SSBN-733) running on the surface, black hull and sail in colour | The modern submarine | `src/photos/h_ssbn733_underway_colour.jpg` |
| H6 | 330-CFD-DF-SC-87-12797.jpeg: A UGM-96A Trident T submarine-launched ballistic missile is launched from the nuclear-powered strategic missile submarine USS Nevada (SSBN-733). This is the 52nd Trident launch and the 27th demonstration and shakedown launch from the Nevada (1986-09-30) | photo 2359x2975 | https://catalog.archives.gov/id/6412750 | NARA useRestriction: {"status": "Unrestricted"} | A Trident missile launched from the submarine USS Nevada (SSBN-733): the missile rising from a burst of white water | Test launch, 1986 | `src/photos/h_ssbn733_trident_launch.jpg` |
| H7 | 330-CFD-DN-ST-91-00355.jpeg: A bow view of the nuclear-powered strategic missile submarine USS NEVADA (SSBN 733) moored at a pier at Long Beach Naval Shipyard (1990-08-06) | photo 1900x2790 | https://catalog.archives.gov/id/6466373 | NARA useRestriction: {"status": "Unrestricted"} | Bow view of USS Nevada (SSBN-733) moored at a pier with a crane and fenders beside her | 1990 photo | `src/photos/h_ssbn733_pier_1990.jpg` |
| H8 | 330-CFD-DN-ST-87-00372.jpeg: Former crew members of the World War II battleship NEVADA (BB 36) attend the commissioning of the nuclear-powered strategic missile submarine USS NEVADA (SSBN 733) (1986-08-16) | photo 3000x1974 | https://catalog.archives.gov/id/6420896 | NARA useRestriction: {"status": "Unrestricted"} | Former crew members of the battleship Nevada among the crowd at the submarine's commissioning, 16 Aug 1986 | People in a crowd; no names given. Good link to "carried there by a submarine named Nevada" | `src/photos/h_ssbn733_former_crew.jpg` |
| H9 | 330-CFD-DN-ST-87-00382.jpeg: A former crew member of the World War II battleship NEVADA (BB 36), right, and a crew member of the nuclear-powered strategic missile submarine USS NEVADA (SSBN 733), salute after raising the ship's commissioning pennant (1986-08-16) | photo 1974x3000 | https://catalog.archives.gov/id/6420906 | NARA useRestriction: {"status": "Unrestricted"} | A sailor in dress whites saluting on the submarine's deck while an elderly former Nevada crewman stands beside him | Caption: a former battleship crew member and a crew member of the submarine | `src/photos/h_ssbn733_commissioning_salute.jpg` |


## I. Maps and documents

| # | title | type | record URL | rights (verbatim) | what it shows | what it does NOT show / caveats | local file |
|---|---|---|---|---|---|---|---|
| I1 | 80-G-47105: Photograph of Map of Pearl Harbor (1941-12-07) | document 3100x3840 | https://catalog.archives.gov/id/12009088 | NARA useRestriction: {"status": "Unrestricted"} | Navy line map "Pearl Harbor - Dec. 7, 1941": Ford Island, Battleship Row and the lochs with labelled berths and attack notes | Black and white line map; text is small | `src/photos/i_pearl_harbor_map_47105.jpg` |
| I2 | BUSHIPS - USS NEVADA - Torpedo & Bomb Damage, 12/7/41, Pearl Harbor (1941-12-07) | document 2496x3840 | https://catalog.archives.gov/id/134079043 | NARA useRestriction: {"status": "Unrestricted"} | Cover page of the Bureau of Ships War Damage Report No. 17, "U.S.S. NEVADA: Torpedo and Bomb Damage, December 7, 1941, Pearl Harbor" (14 Sep 1942) | First page only; NARA holds the full report (more image pages on the record). Originally CONFIDENTIAL, now unrestricted | `src/photos/i_bushps_nevada_damage_cover.jpg` |
| I3 | USS NEVADA - Rep Of participation in Bombardment & Occup Of ATTU (1943-05-29) | document 3191x3840 | https://catalog.archives.gov/id/135947405 | NARA useRestriction: {"status": "Unrestricted"} | First page of the USS NEVADA report on participation in the bombardment and occupation of Attu (29 May 1943) | First page only; typed text, readable at full size | `src/photos/i_nevada_attu_report.jpg` |
| I4 | USS NEVADA - Press Release on War Operations (1945) | document 2712x3840 | https://catalog.archives.gov/id/77539240 | NARA useRestriction: {"status": "Unrestricted"} | Typed Navy press release on USS Nevada's war operations, summarising Pearl Harbor, salvage and the later campaigns | First page only (Micro Serial 147051) | `src/photos/i_nevada_press_release.jpg` |


## Gaps and owner actions (honest list)

1. **The 1948 sinking itself.** `sinking_1948_r1/r2` (HD) show the burning, scarred hulk, the tow, the shelling and the bombing, but I did NOT find the capsizing or the final plunge in either reel, and the ship is never named on screen. NARA 428-NPC-1045 "SINKING OF THE USS NEVADA (BB-36)" (NAID 75806, Aug 1948) is not digitised: order it. No 1948 still photo exists in the NARA online catalog or LoC; try NHHC (unreachable from here, see OWNER_DOWNLOADS.md). No footage of the Iowa, Astoria or Pasadena firing was found: `h_iowa_*` are 1984 DoD photos of the recommissioned Iowa and must be labelled as such.
2. **Pearl Harbor, Nevada under way / beached, as motion.** The only motion film is the DoD colour reel `pearl_harbor_attack_dod`: soft, blue-faded, and I could not pick Nevada out by eye (the agency index says 0:54-1:21). NARA marks it VERIFY. Stills cover the beaching: `ph_loc_nevada_beached_hospital_point` (LoC/OWI), `ph_nevada_after_attack_32583`, `ph_nevada_waipio_33020_c`. The sharpest print (NARA 80-G-19940, NAID 221948868, 5735x4529) has no scan on NARA: Wikimedia only (OWNER_DOWNLOADS).
3. **Salvage 1942, Puget Sound 1942-43, Attu, Toulon.** No stills of Nevada being refloated, in the Puget Sound yard, off Attu or at Toulon were found on NARA/LoC. `dec7_outtakes_*` (raw 1942 salvage film) show battleships being pumped out and docked but I could not tie a shot to Nevada by eye (and 13585 contains STAGED shots of actors). The NARA colour reel `pearl_1942_colour_47635` (NARA: "Nevada ... towed out of drydock", VERIFY) was not viewed by me. Documents stand in for Attu (`i_nevada_attu_report`).
4. **Okinawa kamikaze, 27 Mar 1945.** Only film (`nevada_is_hit`, `nevada_kamikaze_colour_a`), no stills found. Both show casualties.
5. **People.** No portrait of Edwin J. Hill, Donald K. Ross or Francis J. Thomas was found on NARA or LoC. Search NHHC and Wikimedia (OWNER_DOWNLOADS.md). `h_ssbn733_former_crew` is the only "Nevada veterans" image.
6. **Dave's Dream.** No picture is labelled with that name. `cx_b29_bomb_drop_aircraft` (NARA 374-ANT-18-4) is an unnamed Crossroads B-29: do not caption it "Dave's Dream". The B-29 in `crossroads_mn6517_w03` (0-4 s) is also unnamed.
7. **Orange paint being applied.** NARA 428-NPC-18202 "PAINTING USS NEVADA AND VARIOUS OTHER SHOTS OF TARGET SHIPS BIKINI" (NAID 80933) and 428-NPC-18255 "USS NEVADA AND OTHER TARGET SHIPS BIKINI" (NAID 80962) are not digitised: order them. The orange is already well covered in `crossroads_mn6517_w01`, `nevada_evacuation`, `nevada_damage_bikini` (all colour).
8. **Colour restoration.** The Crossroads colour film and the NARA colour reels have faded to cyan/magenta/red. If graded back toward #D9572B, say on screen or in the voice-over that colour was restored.
9. **The wreck, 2020.** Ocean Infinity / SEARCH imagery has no free licence: describe it with a map or depth graphic, or get written permission. Nothing of it is in this library.
10. **Crossroads animals.** `cx_goats_tethered` and `able_animals_colour`, `crossroads_mn6517_w02` show goats and rats, but none is tied to Nevada's pilot house on screen. Do not caption them as Nevada's animals.
11. **Not downloaded (candidates for later).** 428-NPC-18171 (aerial target fleet, "MS AV USS NEVADA ... LS USS NEVADA and USS INDEPENDENCE", NAID 80916), 428-NPC-18138 (NAID 80896, "LS Japanese BB NAGATO & USS NEVADA"), 428-NPC-18132 (NAID 80890), 428-NPC-18602/18606/18565/18566 (target ships, "MS USS NEVADA"), 428-NPC-18586 (radiological check, NAID 81123), 428-NPC-4313/4308 (D-Day), 428-NPC-7511 and 428-NPC-8389 (Okinawa/Iwo, 14-in muzzles), 428-NPC-11163 (NAID 2485242, colour, damage and burial at sea), 428-NPC-11161 (colour, battleships under way), 342-USAF-34282A (12.6 h of USAF Crossroads film, 11 GB, "Blandy inspecting the battleship USS Nevada" on reel 3, VERIFY). archive.org copies with a PD mark: NPC-7512, NPC-7511, NPC-8519 (Iwo Jima: Solace, Nevada, rockets), NPC-11162, NPC-11163. Also on archive.org: "USA - BB-36 USS Nevada Booklet of General Plans (1946)" (bb36bogp1946; licence not checked) for ship drawings.
12. **Rights items to confirm before upload.** (a) The four NARA "Restricted - Possibly" reels (federal film, NARA's standing copyright note). (b) The archive.org Crossroads master has no licence field: rely on the Navy end card; the same film is PD-marked on other archive.org items (listed in the film entries). (c) `cx_loc_*` are from an album in the Ira Eaker papers: LoC says "No known restrictions on publication" but the photographers are not named. (d) The FSA/OWI items are US government (Office of War Information) prints.
13. **Crossroads colour windows NOT cut (download too slow).** Two windows of the ProRes master (archive.org `IA000015_OperationCrossroads.mov`) were seen on the 640x360 proxy but not cut: **12:35.5-14:22.5** (burning ship, then the light carrier INDEPENDENCE with hull number 22 and her torn flight deck, wrecked superstructures; scene cuts at 12:47.8, 12:51.3, 13:10.8, 13:14, 13:36.9, 13:52.4, 13:56.6, 14:00.6, 14:04.2, 14:17.9) and **22:47.7-24:09.4** (more Nagato, then a flat-decked target vessel rolling over with oil streaming, not identified; cuts at 23:22.6, 23:37.8, 23:55.1, 24:08.1). Cut with `ffmpeg -ss <in> -i <mov URL> -t <len> -c:v libx264 -crf 18`; each needs about 2-3 GB of download.
14. **Truncated Crossroads windows.** `crossroads_mn6517_w03` (Able) stops at source 9:06 and `crossroads_mn6517_w05` (Baker) at 19:18: the rest of each sequence (Able 9:06-10:08 column/mushroom; Baker 19:23-21:01 aerial dome and surge) was not downloaded. Re-cut from the .mov if wanted.
