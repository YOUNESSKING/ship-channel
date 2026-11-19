#!/usr/bin/env python3
"""build_list.py - writes FOOTAGE_LIST.md from footage.json (run tools/build_catalog.py first)."""
import json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d = json.load(open('footage.json')); P = d['photos']; F = d['films']; G = d['groups']
esc = lambda s: (s or '').replace('|', '/').replace('\n', ' ')
mm = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'
o = []
o.append('''# USS Ranger (CV-61) - footage list

Built 2026-11-19 for the Ranger video ("The Top Gun Carrier Sold for One Cent"). Files sit in `src/` (git-ignored by `videos/**/src/`): `src/photos/` (stills, longest side capped at 3840 px, JPEG q90; NARA = the catalog's largest scan, DVIDS = the CDN copy, 2000 px max, see below) and `src/film/` (NARA reels as downloaded, 720x480; DVIDS mp4 at the best public size up to 1080p; archive.org MPEG-2 originals). Contact sheets (one frame every 2 s, timestamp burned in, 36 per sheet) are in `sheets/<stem>_NN.jpg`. Machine-readable copy: `footage.json` (`photos`, `films`, `groups`). Helper scripts in `tools/` (NARA proxy search/download, DVIDS fetch, sheets, catalogue builders). **Nothing here is committed.**

**Rights basis.** Every NARA item's `useRestriction` was read through the catalog proxy API (`catalog.archives.gov/proxy/records/search?naId=`) and is quoted verbatim. Stills are all `{"status": "Unrestricted"}`: DVIC/DoD stills (RG 330-CFD), Navy ship-photo file stills (RG 19-N), RG 428 stills (428-GX, 428-KN). The NARA films are RG 428 Naval Photographic Center reels marked `"Undetermined"` (NARA's default for unreviewed reels): Navy camera-unit film, so federal works (same basis as the Nevada list). Each DVIDS page shows the licence line "PUBLIC DOMAIN" (quoted with its copyright line). The three archive.org DoD films carry licenseurl CC0 1.0 with creator "Department of Defense". Nothing is NC/ND. **Not used:** PeriscopeFilm uploads (licence "CC BY-NC-ND" or none), CriticalPast and AWM (licensed stock/clips), Top Gun / Star Trek IV material, news-station video, anything from Wikimedia (blocked, see OWNER_DOWNLOADS.md).

**Honesty rule.** The "does NOT show" column is binding. Ranger is named almost everywhere only by a NARA/DVIC/DVIDS caption: legible hull "61" / "USS RANGER" is stated in the "shows" text only where I saw it in the picture (island of the 8 Jun 1991 homecoming, the 1965 shipyard record prints, the 1967-68 A-7A deck slates). Group H/I/K items are other ships and must be captioned ILLUSTRATIVE.

**Resolution reality.** There is no 1080p+ film of Ranger in service in any public-domain source I could reach. Ranger film = NARA 480i Betacam copies of 1966-1970 reels. The only HD (1080p) material is the 2015 DVIDS tow video of the ex-Ranger and the 2021-22 DVIDS Kitty Hawk tow videos. DVIC stills are 2000-3000 px (not 4K); the only 3840 px still is the VA-145 A-6A slide (505634720). DVIDS original files (up to 6622x4419) need a DVIDS login: see OWNER_DOWNLOADS.md.

**Dates: correct the brief.** DVIDS shows ex-Ranger towed out of Bremerton on **5 Mar 2015** (not 2017-18); Independence left on 11 Mar 2017 and Kitty Hawk on 15 Jan 2022. The ex-Ranger reached Brownsville in 2015 (NavSource arrival 12 Jul 2015; scrapping finished 2017 per Wikipedia): both only from search snippets, verify before scripting.

**Windows** are good to about +/-2-3 s (read from 10 s overviews plus 2 s sheets). Films marked "NOT reviewed" have sheets only: check them in the editor before use.
''')
o.append('## Best items for the hook and key beats\n')
o.append('''| beat | item | why / caution |
|---|---|---|
| Hook: the carrier alive (needs the sharpest) | `nara_6444103`, `nara_6444104`, `nara_6444099` (Dec 1988 bow/starboard-bow aerials, 3000x2000, deck full of jets); `nara_6464138`, `nara_6369415` (3000x2400 port-bow aerials) | The cleanest colour stills of Ranger at sea; slow push on the island/deck, not the centre |
| Hook: Tomcat launch | `nara_6486624`, `nara_6486625`, `nara_6486628`, `nara_6486622`, `nara_6486623` (1 Feb 1993, VF-1 / VF-2 F-14As on Ranger's catapults, 3000 px) | Real Navy stills, the only Ranger-captioned F-14 launches. No F-14 FILM of Ranger exists in the PD sources (gap) |
| Hook / reveal: glory vs end | `dvids_vid_393470` (1080p, 60 s, ex-Ranger under tow, 5 Mar 2015) + `dvids_ima_1799520`/`1799515` (rust, tugs) | The sharpest material on the list. Ship is bare, no aircraft: pair with 1988-93 stills for the contrast |
| Colour film of the ship at its peak | `nara_85335` (1966, 4:28 colour aerials, fireboats, Golden Gate) | Title is cut off at "USS RANGER (CVA-6": verify ship before captioning. SD 480i |
| Colour flight-deck film, verifiably Ranger | `nara_86068` (hand slate "USS RANGER A-7A OPS" ~3:40), `nara_86191` (slate "USS Ranger A7A Corsair" ~2:50), `nara_86067` | A-7A Corsair II ops, tail code NE (1967-68, Vietnam). Not F-14s. SD |
| 1956 launch / 1957 commissioning | `nara_79987` (B&W christening film, 8:22); `nara_7578666` (dressed ship), `nara_7578664` (bronze plaque "1777 U.S.S. RANGER 1957"), `nara_7578669` (platform ceremony) | Film is the bow in the dock with bunting and crowd: the float-out itself was not seen in the reviewed part |
| Vietnam era | `nara_280957271` (VA-165 ordnance, Jan 1968), `nara_505634720` (VA-145 last bombing run, 3840 px, colour), the A-7A reels above | NARA 84175/84181 are Hancock / Coral Sea: do not caption as Ranger |
| Desert Storm / Somalia | `nara_6477881`/`6468800` (Battle Force Zulu aerials, Mar 1991), `nara_6478199` (A-6E with camel mission markings), `nara_6508124` (crew spells RESTORE-HOPE on deck, only 1461 px) | No Desert Storm film of Ranger found. Stills only |
| Last WestPac 1992, last cruise, homecoming | `nara_6486921`, `6486926`, `6486930`, `6486932`, `6484036` (Yokosuka 18 Aug 1992, tugs and rails), `nara_6477567`/`6466181` (island with "61 USS RANGER", 8 Jun 1991), `nara_6655015`/`6655019`/`6655021` (1993 aerials, sailors on the rails) | Caption "her last/final" appears only in some DVIC captions: read before quoting |
| Tow-out / end | `dvids_vid_393470`, `dvids_ima_17993xx` series (6 views, long lens), `dvids_ima_1799515/1799520` | 2000 px CDN copies; originals 4928x3280 / 6622x4419 behind a DVIDS login |
| Other carriers' tows (label ILLUSTRATIVE) | `dvids_vid_828554` (Kitty Hawk 1080p fog tow, 3:23), `dvids_vid_830091`, `dvids_ima_7012822/45/46`, `dvids_ima_3227810..30` (Independence, Foss tugs, 11 Mar 2017), `dvids_ima_8834182` (JFK 2025) | Not Ranger |
| Generic F-14 deck b-roll | `dvids_vid_9295` (TR, Dec 2005, F-14D "101" sunset deck, 480p), stills `dvids_ima_9209877`, `9213038`, `9214015`, `9214816`, `1259569` | Other ships and later years: ILLUSTRATIVE |
''')
o.append('''## Gaps (no public-domain source found)
- **F-14 Tomcat FILM aboard Ranger (1980s-93):** none. Only DVIC stills. Real Navy F-14 deck film is 2005 (480p DVIDS 9295) from another carrier.
- **Desert Storm 1991 and Somalia 1992-93 film of Ranger:** none (AWM holds a 56 min 1991 video shot aboard Ranger: copyright not confirmed PD, not downloaded).
- **1993 decommissioning ceremony:** no film or stills found (the 1993 stills are the homecoming and the Yokosuka visit).
- **Ranger in reserve at Bremerton before 2015, and the voyage / arrival at Brownsville, the Brownsville yard, scrapping with torches:** nothing. Brownsville and torch b-roll is not available from DVIDS/NARA.
- **Ranger commissioning film (Aug 1957) and 1960s Vietnam deck film with her name on screen:** commissioning not found; the A-7A reels are the Vietnam material.
- **Tugs towing a carrier:** only the 2015 Ranger tow, Kitty Hawk 2022 and Independence 2017 (stills).
- **Constellation and Forrestal tow footage:** DVIDS 320929 (20 s, 720x406) only; Saratoga 2014 only as text/photos on a DVIDS news page (not downloaded).
''')
o.append('''## Rights doubts
- NARA RG 428 films say "Undetermined" (default for unreviewed reels). Nevada used the same basis. NARA 148015282 ("F-14 Tomcat the Total Fighter", a commercial Grumman production) is `"Restricted - Possibly"` copyright and was NOT downloaded.
- DVIDS items: page licence "PUBLIC DOMAIN" with the standard line that the work "must comply with the restrictions shown on dvidshub.net/about/copyright" (credit "U.S. Navy photo by ...", no endorsement use).
- DVIDS 828554 date is inconsistent (caption Jan 2022, metadata 2021).
- Several 330-CFD stills depict identifiable crew: fine for editorial use, do not name them.
''')
o.append('## Photos\n')
for g in sorted(G):
    items = [p for p in P if p['group'] == g]
    if not items: continue
    o.append(f'### {g}. {G[g]} ({len(items)})\n')
    o.append('| stem | date | px | shows | does NOT show | record | rights |\n|---|---|---|---|---|---|---|')
    for p in items:
        o.append(f"| `{p['stem']}` | {esc(p['date'])} | {p['w']}x{p['h']} | {esc(p['shows'])} | {esc(p['not_shows'])} | {p['url']} | {esc(p['rights'])} |")
    o.append('')
o.append('## Films and video\n')
for g in sorted(set(f['group'] for f in F)):
    o.append(f'### Group {g}: ' + {'A': 'Ranger film (1966-1970)', 'E': 'Ranger 1956 christening', 'G': 'Ex-Ranger tow 2015', 'H': 'Other ex-carriers (ILLUSTRATIVE)', 'I': 'Generic Navy / F-14 (ILLUSTRATIVE)', 'K': 'Sister carriers and context (NOT Ranger)'}[g] + '\n')
    for f in [x for x in F if x['group'] == g]:
        o.append(f"#### `{f['stem']}`: {esc(f['title'])}")
        o.append(f"- file `{f['file']}`, {f['res'] if 'res' in f else ''}, {mm(f['duration'])} ({f['duration']} s), date {esc(f['date'])}; record {f['url']}")
        o.append(f"- rights: {esc(f['rights'])}")
        o.append(f"- shows: {esc(f['shows'])}")
        o.append(f"- does NOT show: {esc(f['not_shows'])}")
        o.append(f"- avoid: {esc(f['avoid'])}; status: {f['status']}; sheets: {len(f['sheets'])} (`sheets/{f['stem']}_NN.jpg`)")
        if f['windows']:
            o.append('- windows (seconds from file start):')
            for w in f['windows']:
                o.append(f"  - {mm(w['in'])}-{mm(w['out'])} ({w['in']}-{w['out']} s): {esc(w['shows'])}" + (f" / not: {esc(w['not_shows'])}" if w['not_shows'] else ''))
        o.append('')
open('FOOTAGE_LIST.md', 'w').write('\n'.join(o))
print(len('\n'.join(o)))
