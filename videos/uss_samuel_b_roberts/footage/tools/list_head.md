# USS Samuel B. Roberts (DE-413) - footage list

Built 2026-11-19/20 for the Samuel B. Roberts video. Files sit in `src/` (git-ignored): `src/photos/` (stills, longest side capped at 3840 px, JPEG q90) and `src/film/` (NARA reels as downloaded 720x480; NOAA mp4 up to 1080p). Contact sheets (one frame every 2 s, timestamp burned in, 36 per sheet) are in `sheets/<stem>_NN.jpg`. Machine-readable copy: `footage.json` (`photos`, `films`, `groups`, `film_groups`). Tools in `tools/` (NARA proxy search/download/scan, Commons HTML scraper + thumbnail fetch, NOAA REST fetch, sheets, `build_catalog.py`). **Nothing here is committed.**

**Rights basis.** NARA: every record's `useRestriction` was read through the catalog proxy and is quoted (stills/documents "Unrestricted"; RG 428 Navy reels "Undetermined" = NARA's default, Navy camera-unit film, federal work; `428-NPC-1690` "Unrestricted"). Items marked "Restricted - Possibly" were NOT used (428-NPC-6063 CVE burning, 428-NPC-11054 Iwo Jima CVE, 80-MN-5802 "The Fleet That Came To Stay", all 111-ADC Army reels). Wikimedia Commons stills: each file page was read; only files whose page carries PD-USGov-Navy / PD US Navy / CC-PD-Mark / PD-Japan-oldphoto+PD-1996 style markers were kept (listed in the rights column with the page URL); no NC/ND. NOAA: media-kit "Usage and Credit" (video portal "in the public domain", credit NOAA Ocean Exploration; items whose caption says "copyright" need permission: none used). **Not used:** the 2022 Caladan Oceanic / Vescovo / EYOS dive imagery of the wreck (copyrighted per the brief; five Commons uploads dated 22 Jun 2022 carry a CC BY-SA-4.0 label but their provenance is unverified, so they were not downloaded: `Aft Gun Mount - GM3 Paul H. Carr's Position...`, `Pilot House and 40mm gun mount...`, `The bow of the USS Samuel B. Roberts...`, `Broken Stern Section...`, `Hull number 413...`, `Torpedo tubes of the wrecked...`; the Johnston wreck photos likewise), PeriscopeFilm, CriticalPast, news footage, Challenger Deep / Vescovo Commons photos.

**Honesty rule.** The "does NOT show" column is binding. Nothing in the public-domain sources shows Samuel B. Roberts in the battle: there is NO photograph or film of her on 25 Oct 1944 (she is the ship in no picture). Pictures of the battle show her sisters/neighbours or the carriers. Everything marked ILLUSTRATIVE (groups E, G, J, film groups B, D, E, F, G) must be captioned as such. The Taffy 3 film that exists on NARA is the single 198 s reel `nara_77765` (title "Kalinin Bay burning": the burning is only smoke).

**Corrections to the brief.** (1) "The Fleet That Came to Stay" (80-MN-5802) is about Okinawa 1945, not Leyte, and NARA marks it "Restricted - Possibly": not used. (2) NARA 428-NPC-4470 titled "Japanese attack on Gambier Bay" is June 1944 Marianas flight ops, with no attack visible and a land airstrip at the end. (3) The 80-G Samar photos in the NARA catalog (80-G-270516, 270517, 287497, 48888, 288133 ...) have catalog descriptions but NO digitised scans there; scans came from Wikimedia Commons file pages (NARA / NHHC sources). NARA's description of 80-G-270516 says "Oct. 24, 1944": the explosion on St. Lo was 25 Oct. (4) The NARA record date of 428-NPC-5984 (Sangamon) says 13 Oct but shows a burning escort carrier (25 Oct kamikaze on Sangamon, Taffy 1).

**Resolution reality.** No 1080p film of the battle exists. NARA Navy reels are 720x480 (silent, grainy, slates). The sharp material is the 3840 px (original up to 6200 px) 1944 scans: see "Best items". Deep-ocean b-roll from NOAA is 1080p.

**Windows** are good to about +/-2-3 s (read from 10 s overviews plus 2 s sheets). Films marked "title-level only" have sheets only: check them in the editor before use.

## Best items for the hook and key beats

| beat | item | why / caution |
|---|---|---|
| Hook (sharpest, battle day) | `cm_80_G_270514` (sailors silhouetted watching smoke and splashes, flight deck), `cm_80_G_270516` (St. Lo explosion, 5600 px), `cm_80_G_288886` (three shell splashes at a carrier's side, 5568 px), `cm_80_G_288885` (Heermann + a Butler-class DE laying smoke, 5580 px), `cm_80_G_270511` (burning escort carrier, 5600 px) | Real 25 Oct 1944 pictures; scale to 3840 px; push into the subject not the centre |
| Hook: the enemy | `cm_80_G_48888` (Yamato bow-on, 5593 px), `cm_80_G_378525` (Yamato and a cruiser), `cm_L42_09_06_03` (Yamato at Samar), `cm_80_G_46989` (fleet on the horizon, 5664x2826) | Identification by caption |
| Hook: kamikaze | `cm_80_G_288881`, `cm_80_G_288882` (kamikaze diving on White Plains, 5600 px), `cm_NH_71524`/`cm_NH_71528` (Suwannee hit, 5400 px) | Suwannee is Taffy 1 (other task unit), White Plains is Taffy 3 |
| Samuel B. Roberts herself | `cm_NH_96011` (Oct 1944, 5658 px), `cm_NH_90603` (June 1944, 2562 px), `cm_Launch_of_U_S_Navy_destroyer_escort_USS_Samuel_B` (launch, 6000 px) | Only three public-domain photos of her; none from the battle |
| The real words | `nara_78682556_p01` ... `p23` (the 20 Nov 1944 action report: "Combined Action Report, Surface Engagement off Samar ... and Report of Loss of U.S.S. SAMUEL B. ROBERTS", SECRET stamp, 23 pages) | Page 2 holds "launched a torpedo attack from a range of 4,000 yards" and the 608 rounds of 5-inch; read pages before quoting |
| People | `cm_Robert_W_Copeland` (500 px only), `cm_NH_92320` (Evans), `cm_80_G_371327` (Sprague) | Copeland copy is low-res: owner hand download, see OWNER_DOWNLOADS.md. No portrait of coxswain Samuel B. Roberts or of Paul H. Carr found |
| Sister DEs and Butler class | `cm_80_G_382868` (John C. Butler, 5346 px), `cm_L45_74_08_01` (Dennis, 5299 px), `cm_80_G_264041`, `cm_80_G_295001` (Raymond), plans `cm_John_C_Butler_class_destroyer_escort_inboard_pro` | ILLUSTRATIVE for Roberts |
| Battle film | `nara_77765` (Taffy-style: shell splashes around a distant carrier 1:15-1:45), `nara_77732` (burning escort carrier 3:00-4:30, Sangamon) | SD, silent, haze |
| Destroyer b-roll | `nara_77716` (sharp destroyer alongside 1:40-3:55), `nara_77710`/`nara_77677` (smoke screens), `nara_77862` (abandon ship, swimmers) | All ILLUSTRATIVE, other ships and dates |
| Carrier flight ops | `nara_76144` (Kitkun Bay May 1944, sharp 35mm), `nara_77138` (Gambier Bay Jun 1944) | Taffy 3 carriers before the battle |
| Survivors / namesake ships | `nara_6410132`, `nara_6408184`, `nara_6406875` (1985-86 survivors at FFG-58 commissioning) , `nara_6409895`, `nara_6439683` (FFG-58), `cm_Ffg58minedamage` (1988 mine damage) | Post-war |
| The deep | `noaa_31374`, `noaa_31426`, `noaa_31371`, `noaa_29866` (abyssal 1080p), `noaa_4660` (marine snow), `noaa_29719` (halosaur at 5,510 m), `cm_NH_96797` + `cm_USN_710619` (Trieste with USS Lewis DE-535 over the Marianas Trench, 23 Jan 1960, 5600 px) | Trieste photos show the destroyer escort USS Lewis (DE-535) escorting the dive (a Butler-class sister per Wikipedia: verify before saying "sister"); do not imply the Roberts wreck |

## Gaps (no public-domain source found)
- **Any photo or film of Samuel B. Roberts in action or sinking;** any photo of her crew, of coxswain Samuel B. Roberts, or Paul H. Carr; Copeland is only 500 px.
- **Gambier Bay straddled / sinking** (`LeyteGambierBayStraddle` is only 640 px and could not be fetched at full size here); Gambier Bay sinking, Johnston sinking and Hoel hits: only small Commons scans.
- **Survivors in the water / rafts at Samar** (rescue 26-28 Oct): only a tiny Commons print (not downloaded) and the generic `nara_77862`.
- **Film of 5-inch guns firing from a DE, depth charges from a DE, torpedo launch:** none found (NARA reel titles do not match; `nara_77716` shows a destroyer, not firing).
- **Sea-floor map / wreck imagery:** all copyrighted (2022 dives): use maps and NOAA illustrative b-roll.
- **Library of Congress, NHHC, NavSource:** unreachable from this server (loc.gov 429/403, history.navy.mil and navsource.org no connection).

## Rights doubts
- NARA RG 428 reels say "Undetermined" (default for unreviewed reels), same basis as earlier videos.
- Commons "PD-Japan-oldphoto / PD-1996" Japanese ship photos: public domain in Japan before 1956 and restored-PD in the US; the owner accepted this basis in the brief.
- Commons-sourced 80-G files: the PD claim rests on the Commons page (US Navy work); the NARA catalog records of the 80-G items were checked where listed ("Unrestricted").
- Four Commons files are `PD-Australia` (AWM-sourced) or tiny: dropped.
- Several 1985-86 DVIC stills show identifiable survivors and guests: editorial use, do not name them.

## Photos

