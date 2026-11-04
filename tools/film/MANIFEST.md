# Patton #15 archive film (cut by `cut_clips.sh`; sources downloaded from archive.org item pages, originals are NARA / US Army Signal Corps film)

Licence basis for ALL film below: works of the US federal government (US Army Signal Corps film held by the US National Archives, NARA record group 111), public domain. The archive.org items are the NARA uploads (identifiers `111-adc-*`, `ARC-*`); ADC-1672b carries the Public Domain Mark 1.0 (creativecommons.org/publicdomain/mark/1.0/). ARC-39153 is a United News / OWI newsreel in NARA (PDM 1.0, same item used in collins/). Credit line (no link in the description): "US Army Signal Corps / US National Archives".
Clips are silent, 1920x1080 (sources are 640x360 to 720x480, upscaled and CROPPED to fill 16:9, no black bars), 30 fps, 6-7 s each. `restore_film.py`-style tint/restore + projector frame at build time (`"tint": true, "frame": true`). `src/` is deleted after cutting (about 700 MB); rerun `cut_clips.sh` to regenerate.

| clip | source item (https://archive.org/details/<id>) | NARA title / id | in (s) | out (s) | shows | suits |
|---|---|---|---|---|---|---|
| m1_coutances_halftracks | ADC-1672b (NARA 15479) | 4th Armored Division, Coutances, France, 29 Jul 1944 | 124 | 131 | GIs and a half-track/truck on a Coutances street (slate "COUTANCES 29 JULY") | background block (Normandy, July 1944) and Move 1 end |
| m1_avranches_pows | 111-adc-2041 (NARA 15847) | "4th Armored Division takes Avranches, France", 31 Jul-3 Aug 1944 | 380 | 386 | start: slate "AVRANCHES 31 JULY"; then a column of German prisoners, hands on heads, on a tree-lined road | Move 1 end, background block |
| m1_columns_pow | 111-adc-2041 | same | 332 | 338 | long column of marching men on a hedgerow road (German prisoners) | background block / Move 1 end |
| m1_armored_cars | 111-adc-2041 | same (Mont-Saint-Michel part, 3 Aug 1944) | 750 | 756 | M8 armoured cars and crews on a coast road | Move 1 end (label as Avranches area, August 1944) |
| m2_aircraft_snow | ARC-39153 | December 1944 Newsreel: Battle of the Bulge; Bastogne | 348 | 354 | formation of transport aircraft in the sky, then low over snow | Move 2 end (C-47 supply drop idea; the newsreel does not name the date/place of this shot, keep the label generic) |
| m2_bundles_tank | ARC-39153 | same | 372 | 378 | aircraft in formation seen from a plane, parachute bundles falling in snow country | Move 2 end (air supply, Dec 1944) |
| m2_bastogne_sign | ARC-39153 | same | 462 | 469 | two US officers shake hands at a board with the letters "BA..." (Bastogne), a brigadier general speaks | Move 2 end (Bastogne; the officer is NOT identified, never say McAuliffe) |
| m2_halftracks_snow | 111-adc-3114 (NARA 16917) | "101st Airborne Division, near Bastogne, Belgium ... Third Army enters St. Hubert", 12-13 Jan 1945 | 12 | 18 | crews dig out a snow-covered half-track | Move 2 end (Ardennes, winter 1944-45) |
| m2_column_snow | 111-adc-3114 | same | 190 | 197 | files of troops walking over snow fields | Move 2 end |
| m3_pontoon_ferry | 111-adc-9718 (NARA 23483) | "Third Army crosses the Rhine", 27 Mar 1945 | 70 | 77 | gun and vehicles on a pontoon ferry/bridge; troops watching | Move 3 end |
| m3_columns_pontoon | 111-adc-9718 | same | 192 | 199 | column of prisoners crossing a pontoon bridge | Move 3 end |
| m3_dukw_gun | 111-adc-9718 | same | 396 | 403 | DUKW amphibious truck with a gun leaving the water | Move 3 end |
| m3_dukw_river | 111-adc-9718 | same | 430 | 437 | DUKW with troops crossing the Rhine | Move 3 end |

Honesty notes: (1) 111-adc-9718's NARA title says "Third Army"; the shoulder patches in it look like the 3rd Infantry Division (Seventh Army), so the clips are labelled only "THE RHINE · MARCH 1945", never "Oppenheim" or "5th Infantry Division". There is NO identified footage of the Oppenheim crossing itself. (2) No identified footage of the Bastogne supply drops of 23 Dec 1944 was found (the 111-adc-3376 "Parachute supplies, Bleialf" item is aerial Germany 1945 and was rejected). (3) Nothing in the clips shows the Sicily slapping. (4) Scanned for sources and not used: 111-adc-3586 (4th Armored Div, Daun-Koblenz Mar 1945), 111-adc-3725 (4th Armd road to Worms), ADC-2640b (Patton addresses officers, Nov 1944), 111-adc-3167 (Bastogne back to the Belgians, Jan 1945): all candidates if the owner wants more.

Stills for the background block: see `../media/CREDITS.md`; shot lists: `../../archive.json` (key "4") and `../../archive_move_ends.json`.
