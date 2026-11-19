#!/usr/bin/env python3
"""build_catalog.py - writes footage.json (and FOOTAGE_LIST.md tables) from the download metadata + the hand-read notes below.
Run from anywhere: python3 tools/build_catalog.py   (inputs: nara_photos_meta.jsonl, nara_films_meta.jsonl, dvids_meta.jsonl, ia_meta.json)"""
import json, os, re, subprocess
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); os.chdir(ROOT)
J = lambda f: [json.loads(l) for l in open(f)]
NARA_RIGHTS = 'NARA useRestriction: {"status": "Unrestricted"}'
NARA_FILM_RIGHTS = ('NARA useRestriction: {"status": "Undetermined"} (NARA default for unreviewed RG 428 reels). Basis: US Navy camera-unit film '
                    '(Record Group 428, Naval Photographic Center slate "428.NPC.<n>"), so a US federal work in the public domain.')
def dvids_rights(m): return f'DVIDS page licence line: "PUBLIC DOMAIN". Copyright line: "{m["copyright_line"][:160]}"'

# ---------------------------------------------------------------- photos
RANGER = r'USS RANGER \(CV[ -]61\)|USS Ranger \(CV 61\)|Aircraft Carrier USS RANGER \(CV 61\)'
def group_for(t, local):
    T = t.upper()
    if local and local.startswith('19-NN'): return 'E'
    if 'RESTORE HOPE' in T or 'BATTLE FORCE ZULU' in T or 'DESERT' in T: return 'F'
    if re.search(r'F-14|TOMCAT', T): return 'B'
    if re.search(r'HANGAR|PLANE CAPTAIN|ORDNANCE|MAINTENANCE|HANDLER|CRASH AND RESCUE|PHOTOGRAPHER|MISSION MARKINGS|TECHNICIANS|FLIGHT DECK CREW|AIRCRAFT TECHNICIANS|FORKLIFT', T): return 'C'
    if re.search(r'VIETNAM|NORTH VIETNAM|A-6', T) and 'RANGER' in T and re.search(r'\b19(6|7)\d', ''): return 'J'
    if re.search(r'TUG|PIER|MOORED|MOORING|ENTERS PORT|ARRIVES|YOKOSUKA|OAKLAND|PEARL HARBOR|MAN THE RAIL|MANNING THE RAIL|MAN THE RAILS|HOME', T): return 'D'
    if re.search(r'MIDWAY|KITTY HAWK|CONSTELLATION|INDEPENDENCE|THREE CARRIERS|AIRCRAFT CARRIERS USS', T): return 'K'
    return 'A'
GROUPS = {'A': 'Ranger underway / aerial / hull views (1981-1993)', 'B': 'F-14 Tomcat ops aboard Ranger (1987-1993)',
          'C': 'Ranger crew, hangar, deck work (1989-1991)', 'D': 'Ranger in port / tugs / arrivals / manning the rails',
          'E': 'Ranger 1957 christening-commissioning and 1965 shipyard record photos (NARA 19-N)', 'F': 'Desert Storm, Battle Force Zulu, Somalia',
          'G': 'Ex-Ranger at Bremerton and towed out, 2015 (DVIDS)', 'H': 'OTHER ex-carriers towed / dismantled (ILLUSTRATIVE, not Ranger)',
          'I': 'F-14 Tomcat carrier ops on OTHER ships (ILLUSTRATIVE, not Ranger)', 'J': 'Vietnam-era Ranger stills (1968-1975)',
          'K': 'Sister / neighbouring carriers (context)', 'L': 'VIP visits and press (1980-83), low priority'}
# hand-read overrides after viewing the picture: stem -> (shows addition, not_shows)
OV = {
 '6477567': ('Island close-up: "61" and "USS RANGER" legible on the island, crew manning the rails and bunting', 'Not at sea; homecoming of 8 Jun 1991 (caption). Faces too small to name'),
 '6466181': ('Island with "61" and "USS RANGER" legible, crew on rails', 'Homecoming day, not combat'),
 '6466179': ('Hull side with "USS RANGER" lettering legible, crew on the pier side', 'Black-and-white print'),
 '6433592': ('Island silhouette against San Diego city lights with a lit "61"', 'Dark frame; not a flight-ops image'),
 '6486623': ('F-14A "200" of a VF squadron on the deck with island behind', 'Squadron not read from the picture (caption says VF-2)'),
 '6486622': ('Catapult steam, F-14A at launch', 'Ship name not visible: caption only'),
 '6508124': ('Aerial of the flight deck with the crew spelling "RESTORE-HOPE" on the deck', 'Low-resolution scan (1461 px). Date in the NARA record is 2000-01-01 (a placeholder): the event is Dec 1992 off Somalia per the caption'),
 '6444103': ('Bow-on aerial at sea, deck full of aircraft, wake', 'No hull number legible'),
 '6444104': ('Starboard bow aerial at sea, deck full of aircraft', 'No hull number legible'),
 '6444099': ('Starboard bow aerial at sea', 'No hull number legible'),
 '6444102': ('Ship silhouetted against a red sunset on the horizon', 'A shape only: no markings legible'),
 '6464137': ('Bow aerial, aircraft ranged on deck', 'No hull number legible'),
 '6452117': ('Two F-14As pass over the carrier (vertical frame)', 'Carrier is a speck: caption only'),
 '6452123': ('View from an F-14A cockpit: pilot helmet in the foreground, carrier deck full of aircraft', 'Not a launch'),
 '6469206': ('F-14A tail/canopy and a plane captain in red polishing the canopy', 'Ship not visible'),
 '6469211': ('Flight-deck crew group portrait, goggles and helmets, thumbs up', 'People unnamed'),
 '6478199': ('Weapons crewman beside an A-6E with camel mission markings (Desert Storm tally)', 'Person unnamed; mission markings are camel silhouettes, not bomb counts'),
 '6483832': ('Overhead: carrier with the oiler and escort on a replenishment run', 'Which ship is which is from the caption'),
 '280957271': ('B&W: crewmen load ordnance onto an A-6 Intruder on deck (VA-165), Gulf of Tonkin, Jan 1968', 'Print has a white border; ship not visible in the frame, name from the caption'),
 '505634720': ('Colour: three VA-145 A-6A Intruders over cloud, bombs falling (the last bombing run, Vietnam)', 'Taken from another aircraft; ship not visible. 4:3-ish transparency scan'),
 '7578664': ('B&W record print of the bronze plaque "1777 U.S.S. RANGER 1957 / the eighth ship of the fleet to bear the name", with the list of earlier ships and honours', 'Plaque only, not the ship. Print border visible'),
 '7578666': ('B&W: carrier dressed overall with flags and bunting at its pier, aerial (1957 ceremony set)', 'No hull number legible; print border'),
 '7578669': ('B&W: officers and civilians on the platform of a ceremony in front of the hull, speakers at microphones', 'Nobody named; the set is the 1957 launch/commissioning file (inferred from the plaque and bunting)'),
 '7578692': ('B&W record print: island antenna arrangement with a numbered key; label reads "USS RANGER (CVA61) ... 22 OCTOBER 1965", San Francisco Bay Naval Shipyard (Hunters Point)', 'Technical documentation print with key text over the picture'),
 '7578695': ('B&W record print: island starboard side looking forward, antenna key; label "USS RANGER (CVA61) ... 22 OCTOBER 1965"', 'Technical print with key text'),
 '7578698': ('B&W record print of the mast and island (antenna arrangement), label dated Oct 1965', 'Technical print with key text'),
 '7578700': ('B&W record print of the island (antenna arrangement), label dated Oct 1965', 'Technical print with key text'),
 '7578703': ('B&W record print: flight deck looking aft with antenna key; label dated Oct 1965', 'Technical print with key text'),
}
NOTSHOW_DEFAULT = {
 'A': 'Date and place come from the NARA/DVIC caption; no event beyond the caption. Hull number not legible unless the shows column says so',
 'B': 'Ship identification by caption (and the tall island); squadron markings not read from the picture unless stated. Not footage',
 'C': 'Ship not identifiable from the picture itself (close crop): identification is the DVIC caption only. People unnamed',
 'D': 'Caption-only identification unless "61/USS RANGER" is stated in the shows column. Not at sea; not combat',
 'E': 'Undated print in the NARA file "CVA 61 Ranger" (a 19-N ship-photo file); date and place not stated on the print unless the shows column says so. Interior views show the ship only through the file title',
 'F': 'Caption-only identification. Does not show combat (Ranger flew from the Gulf of Oman/Persian Gulf area; the images are rear-area, transit and homecoming)',
 'J': 'Captions name Ranger; the ship may not be in frame',
 'L': 'Ceremony/press scene: ship identified by caption only; not hook material',
 'K': 'Ranger is only one of the ships in frame / named by caption; small at this scale',
}
def date_of(m):
    d = m.get('date')
    return (d[0] if isinstance(d, list) and d else d) or ''
photos = []
for m in J('nara_photos_meta.jsonl'):
    nid = str(m['naId']); t = (m['title'] or '').replace('\n', ' ')
    g = group_for(t, m['local'])
    if re.search(r'Vice President|Vice Premier|Geng|press corps|aerial demonstration', t): g = 'L'
    if nid in ('280957271', '505634720'): g = 'J'
    if nid in ('6451640', '6483817', '6483819', '6483820', '6483821', '6483822', '6483823', '6469205', '6469208', '6469216', '6469212', '6469215', '6469218', '6469219', '6469214'): g = 'F'
    if nid in ('6353481', '6353504', '6351406', '6419762', '6450094', '6408697', '6408693', '6408684', '6382074'): g = 'K' if nid in ('6353481', '6353504', '6351406', '6408697', '6408693') else 'D' if nid in ('6419762', '6450094', '6408684', '6382074') else 'K'
    sh, ns = OV.get(nid, (None, None))
    shows = (sh + ' | NARA caption: ' if sh else 'NARA caption: ') + t
    if m.get('note'):
        note = re.sub(r'\s+', ' ', m['note'].replace('The original finding aid described this photograph as:', '')).strip()
        if note and g != 'E': shows += ' [finding aid: ' + note[:160] + ']'
    if g == 'E' and not sh:
        shows = 'B&W record print from the NARA file "CVA 61 Ranger" (19-N series): ' + {
            '7578665': 'ship interior/space', }.get(nid, 'see picture: ceremony or interior/exterior record photo of the new carrier')
    photos.append(dict(stem=m['stem'], group=g, file=m['file'].replace('src/', 'src/'), title=f"{m['local'] or nid}: {t[:110]}", url=f"https://catalog.archives.gov/id/{nid}",
                       rights=NARA_RIGHTS, date=date_of(m), shows=shows, not_shows=ns or NOTSHOW_DEFAULT.get(g, NOTSHOW_DEFAULT['A']), w=m['w'], h=m['h'], source='NARA'))
DV_G = {'1799342': 'G', '1799348': 'G', '1799349': 'G', '1799353': 'G', '1799356': 'G', '1799358': 'G', '1799515': 'G', '1799520': 'G',
        '7012822': 'H', '7012845': 'H', '7012846': 'H', '6967137': 'H', '3227810': 'H', '3227818': 'H', '3227826': 'H', '3227830': 'H', '8834182': 'H',
        '9210458': 'H', '9209601': 'K', '9207837': 'K'}
DV_SHOWS = {
 '1799342': 'Distant long-lens: ex-Ranger under tow, Port Orchard Bay, mountains behind, tug alongside', '1799348': 'Distant long-lens: ex-Ranger under tow, Olympic range behind',
 '1799349': 'Bow-quarter close view of the grey hull with a tug and a harbour boat in front, evergreen shore', '1799353': 'Close view of the hull with a tug, trees behind',
 '1799356': 'Long-lens: the whole carrier on the water with a tug in the foreground, snow-capped Olympics behind', '1799358': 'Close: tug in front, hull and island, snow mountains',
 '1799515': 'Starboard bow/side: weathered hull, rust streaks, two tugs at the bow, island with masts', '1799520': 'Side view of the whole carrier: rust, faded paint, tugs, calm water',
 '7012822': 'Ex-Kitty Hawk as a grey shape through fog between trees, tug beside it (2022 tow)', '7012845': 'Ex-Kitty Hawk in fog behind a Washington State ferry',
 '7012846': 'Ex-Kitty Hawk in dense fog with two tugs', '6967137': 'Rusty mooring bollards in the foreground, ex-Kitty Hawk behind (Mar 2021, Bremerton)',
 '3227810': 'Foss tug passing the ex-Independence, a shore building and cranes (Mar 2017)', '3227818': 'Foss tug "Henry Foss"-type tug in front of the ex-Independence hull and island',
 '3227826': 'Ex-Independence under tow on the water with a tug (wide)', '3227830': 'Panorama: ex-Independence with a tug on each side, flat light',
 '8834182': 'Ex-USS John F. Kennedy at the pier, rust, tugs (Jan 2025, from Newport)', '9210458': 'Tugs pushing Kitty Hawk at Changi (2001), crowd on deck',
 '9209601': 'Constellation and Kitty Hawk steaming together (1999)', '9207837': 'Constellation silhouetted at sunset (1997)',
 '1259569': 'F-14 Tomcat on the catapult, catapult crewman crouching (USS George Washington, 2002)', '1259599': 'F-14 landing/ taxi on USS George Washington, island with "73" (2002)',
 '9208863': 'Ordnancemen load an AIM-9 on an F-14 (USS Enterprise, 1998)', '9209877': 'F-14A at night, red deck lights, afterburner (USS Enterprise, 2000)',
 '9210504': 'Steam from a previous catapult launch, an F-14 being taken into position (USS Constellation, 2001)', '9212415': 'Carrier from above with an F-14B launching (USS George Washington, 2004)',
 '9213038': 'F-14B catapulted, afterburner, seen from astern (USS Harry S. Truman, 2004)', '9214015': 'F-14D from behind on the catapult, steam, deck crew (2005)',
 '9214816': 'F-14D nose-on with catapult steam, yellow-shirts (USS Theodore Roosevelt, 2006)'}
for m in J('dvids_meta.jsonl'):
    if m['type'] != 'image': continue
    i = m['id']; g = DV_G.get(i, 'I')
    ns = {'G': 'Ranger is identified by the DVIDS caption; no hull number legible at this scale. Taken at the 2015 tow (not at the inactive-ships berth). The CDN copy is 2000 px; the page lists the original at ' + m['resolution_page'],
          'H': 'NOT Ranger: illustrative of the same tow/dismantling story. The DVIDS caption labels this ship by its own name' + ('; note DVIDS calls Independence "CVN-62" in captions, she was conventionally powered CV-62' if 'Independence' in m['title'] else ''),
          'I': 'NOT Ranger and not a Ranger-era F-14 (late 1990s-2006, other carriers). Generic b-roll only; label ILLUSTRATIVE',
          'K': 'Not Ranger'}[g]
    try: w, h = Image.open(m['file']).size
    except Exception: w = h = 0
    photos.append(dict(stem=os.path.basename(m['file'])[:-4], group=g, file=m['file'], title=f"DVIDS {i}: {m['title'][:100]}", url=m['url'], rights=dvids_rights(m), date=m['date'],
                       shows=DV_SHOWS.get(i, '') + f' | DVIDS caption: {m["desc"][:260]}', not_shows=ns, w=w, h=h, source='DVIDS', original_res_on_page=m['resolution_page'], virin=m['virin']))

# ---------------------------------------------------------------- films
def nara_film(stem, naid, group, title, date, dur, shows, not_shows, windows, avoid, review='reviewed on 2 s sheets + 10 s overview'):
    return dict(stem=stem, group=group, file=f'src/film/{stem}.mp4', title=title, url=f'https://catalog.archives.gov/id/{naid}', rights=NARA_FILM_RIGHTS, date=date,
                shows=shows, not_shows=not_shows, w=720, h=480, res='720x480 H.264 59.94i-as-60p, NARA mp4 as downloaded (Digital Betacam copy, SD)', duration=dur, windows=windows,
                avoid=avoid, status=review, sheets=[f for f in sorted(os.listdir('sheets')) if f.startswith(stem + '_')])
W = lambda a, b, s, n='': dict({'in': a, 'out': b, 'shows': s}, not_shows=n)
films = [
 nara_film('nara_85335', 85335, 'A', 'USS RANGER (CVA-6[title truncated in NARA]) - aerial colour, San Francisco Bay, fireboats (428-NPC-37142)', '1966-08-25', 267.97,
  'Colour aerial sequence of a large carrier with fireboat sprays and small craft in San Francisco Bay: Golden Gate Bridge at ~0:20, city skyline 3:20-4:10, low aerial passes along the flight deck (jets lined up) ~0:50-1:00. Opens with a helicopter in warm light at 0:10',
  'The NARA title is cut off at "USS RANGER (CVA-6": hull number/name not legible on any sheet frame, so the ship is Ranger only by the record title (verify against the full title/other reels before captioning). No sound check done',
  [W(10, 20, 'Helicopter landing in warm backlight (leader-like, orange wash)', 'Not the ship'), W(20, 60, 'Carrier at the Golden Gate then with fireboats; deck aircraft close at 0:50', 'Ship not named on screen'),
   W(60, 130, 'Carrier with fireboat plumes, small boats; city behind', ''), W(130, 250, 'Long aerial run along the city front; SF skyline 3:20-4:10', '')],
  'Slate 0:00-0:08 ("428.NPC.37142 / Source: Digital Betacam"); "End of Recording" card from ~4:15. Strong, saturated colour: a hook candidate for the Ranger-arrives-home beat'),
 nara_film('nara_86067', 86067, 'A', 'A-7A CORSAIR 2 OPERATIONS ABOARD USS RANGER (428-NPC-39271)', '1967-12', 580.71,
  'Colour: pilots briefed in a ready room (0:10-2:50, map boards), deck prep with A-7A Corsair II tail code "NE", air-to-air flight of A-7As over cloud 4:20-6:50, catapult/arrest scenes with A-4s "NE" 7:00-9:20',
  'Ship name only in the NARA title (no hull number or "Ranger" legible on the sheets reviewed); tail code NE matches CVW-2 as a cross-check, not proof. Not Desert Storm era, no F-14s',
  [W(10, 170, 'Pilots and officers in the ready room, map, briefing', 'No names'), W(180, 260, 'Flight-deck crew and cockpit close-ups (A-7A)', ''), W(260, 410, 'A-7As flying over cloud (air-to-air, wingmen), best colour', 'Not carrier-based shots'),
   W(420, 560, 'Catapult launch crew, arrester-wire landings, A-4 "NE"', '')], 'Slate 0:00-0:06; hand-held card at ~9:20-9:30; frame jitter in the tower shots'),
 nara_film('nara_86068', 86068, 'A', 'A-7A CORSAIR 2 OPERATIONS ABOARD USS RANGER (428-NPC-39272)', '1967-12', 560.06,
  'Colour: A-7A "315 NE" on deck with yellow-shirt director (0:10-0:35), pilots and ordnance crew in red/green jerseys (0:40-3:30); a hand-held slate at ~3:40 reads "USS RANGER ... A-7A OPS" (the one on-screen identification in this reel); map room and ready room 3:50-6:20; bomb/rocket loading 6:30-7:30; A-7A launch from the catapult and a landing 8:00-9:10',
  'Tail code NE and the slate only; the film is not dated on screen (title says Dec 1967). No exterior ship view in the sheets reviewed',
  [W(10, 55, 'A-7A "315" on the deck, director signals, pilot climbs in', ''), W(60, 220, 'Close work on aircraft, pilots strapping in, ordnance', ''), W(270, 330, 'Armourers and fuzing close-ups', ''), W(450, 560, 'Launch from the catapult and landing, A-7A tail "NE"', '')],
  'Slate 0:00-0:07; hand slate ~3:38-3:44 (use as proof, not as picture); dark ready-room frames'),
 nara_film('nara_86191', 86191, 'A', 'A-7A CORSAIR 2 OPERATIONS ABOARD USS RANGER (CVA-61) (428-NPC-39600)', '1968-01', 513.58,
  'Colour: A-7A "321"/"NE" in wide deck shots with red-shirt crew (0:10-1:40); a helicopter on deck and A-4s (1:40-1:55); flight-deck control tower interior (Air Boss, 2:00-2:45); camera slate at ~2:50 reading "...A7A Corsair USS Ranger"; A-7 takeoff 3:00-3:25; bomb stacks and fuzing 3:30-5:50; tower launches 6:00-8:20',
  'Hull number never legible; "USS Ranger" appears only on the slate and in the title. A-7A (not F-14); in-theatre date inferred from the title',
  [W(10, 100, 'A-7A "321" on deck, wide with armourers, steady shots', ''), W(105, 170, 'Crowded deck with helicopter, A-4 and A-7 parked', ''), W(180, 285, 'Air Boss tower interior with yellow "AIR OFFICER" jerseys', ''),
   W(300, 330, 'A-7A launches and passes', ''), W(330, 520, 'Bomb stacks, red-shirt ordnance handling, closeups', 'Ordnance is stored/handled only'),],
  'Slate 0:00-0:06; camera slate 2:48-2:58; flare/blown highlights at 1:30 and ~3:20'),
 nara_film('nara_87809', 87809, 'A', 'A-B [sic] ACCIDENT ON BOARD USS RANGER (CVA-61) (428-NPC-44782)', '1970-05', 221.78,
  'Colour (faded): flight deck during launches/recoveries, F-4 Phantoms, A-6 Intruders, A-7s, an SH-3 helicopter; bursts of steam/spray and smoke at 2:00-2:30',
  'The reviewed 10 s frames do not clearly show what the "accident" was; no ship name/number on screen. Do not caption anything as a crash without checking the 2 s sheets. Faded colour, soft',
  [W(10, 60, 'Helicopter, F-4, A-6 on deck', ''), W(60, 130, 'Deck handling, A-7/F-4/A-6 on catapults', ''), W(165, 200, 'SH-3 helicopter landing, crew on deck', '')],
  'Slate 0:00-0:08; green leader at ~3:28-3:40'),
 nara_film('nara_79987', 79987, 'E', 'CHRISTENING OF USS RANGER CVA 61 (428-NPC-15341)', '1956-09-01', 502.43,
  'B&W: bow of a carrier in the building dock/ways seen from beside, bunting, a dignitaries platform with a microphone, large crowd of sailors and families; officers with a woman holding flowers (the sponsor presumably), later the bow from the front with red-white-blue bunting and cranes',
  'The reel is identified by the NARA title only; the sheets do not show "Ranger" lettering. The actual slide-down or float-out is not seen in the part reviewed (reviewed to 5:50; sheets 06-07 cover the end). SD B&W',
  [W(8, 60, 'Locked-off view of the bow with the sponsor platform and crowd below', ''), W(68, 90, 'Platform with microphones and bunting, ceremony', 'Nobody named'), W(135, 175, 'Crowd close-ups of sailors and families', ''),
   W(175, 200, 'Bow from below with bunting', ''), W(215, 260, 'Officers and sponsor with bouquet, close', ''), W(320, 350, 'Bow front view from ground level, bunting, cranes', '')],
  'Slate 0:00-0:08 (NARA eagle logo, then "428.NPC.15341 Source: Digital Betacam"; flash/white frame at ~0:06). Not reviewed after 5:50'),
 # ----- context films
 nara_film('nara_86297', 86297, 'K', 'DEPARTURE OF THE USS FORRESTAL (CVA-59) (428-NPC-39840)', '1968-04-08', 165.7,
  'Colour aerial of the lead ship of the class steaming away on a calm sea, "59" painted on the hull side at 0:05-0:12, deck striping and island clearly visible; low sun glint 1:25-1:45',
  'Forrestal (CVA-59), the class leader: ILLUSTRATIVE for "Forrestal-class" only, not Ranger. Slates at the end',
  [W(5, 12, 'Hull number 59 close', ''), W(15, 130, 'Carrier steaming away, aerial, steady, long clean take', '')], 'NARA eagle slate 0:00-0:04; clapper slates 2:13-2:40 and a black frame; avoid after 2:10'),
 nara_film('nara_85665', 85665, 'K', 'A-6A IN FLIGHT AND LAUNCH FROM USS FORRESTAL (CVA-59) (428-NPC-38209)', '1967-04', 765.6,
  'Colour: A-6A Intruder deck handling and catapult launches off a Forrestal-class deck (0:10-4:30); then long cockpit/air-to-air refuelling sequences (4:30-12:30)',
  'Forrestal, not Ranger. Illustrative of A-6A ops on a sister carrier', [W(10, 120, 'A-6A on the catapult, yellow-shirt signal, launch, steam', ''), W(130, 260, 'Takeoff from the bow and cockpit views', '')], 'Clapper slate 0:00-0:08; black frames in the cockpit run'),
 nara_film('nara_86312', 86312, 'K', 'UNDERWAY REPLENISHMENT AT SEA, ON YANKEE STATION (428-NPC-39915)', '1968-07-11', 671.73,
  'Colour: replenishment at sea off Vietnam: oilers/stores ship alongside, cargo nets, forklift on the hangar-bay edge, band on the flight deck, aircraft with "USS CONSTELLATION VAH-8" lettering',
  'USS Constellation (CVA-64) per aircraft markings and the slate "UNREP CVA64"; not Ranger. ILLUSTRATIVE of carrier life', [W(20, 300, 'UNREP lines, cargo, crews in life vests', ''), W(300, 520, 'Flight deck band, ships alongside', '')], 'Slate 0:00; "End of Recording" at ~10:50'),
 nara_film('nara_84175', 84175, 'K', 'VIETNAM CARRIER AIR STRIKES South China Sea (428-NPC-34706)', '1965-02-11', 661.63,
  'B&W: carrier underway aerials (2:30-4:10; "19" on the bow deck at ~3:15 = USS Hancock CVA-19), flight-deck action: F-8 Crusaders, A-1 Skyraiders, launches, ordnance',
  'USS HANCOCK (CVA-19) per slates and the deck number: NOT Ranger. Illustrative Vietnam-era carrier ops only', [W(150, 255, 'Hancock aerial underway, B&W', ''), W(290, 560, 'Flight-deck action, launches and traps', '')], 'Slates at 0:00, ~4:10 (Hancock slate) and end white frame'),
 nara_film('nara_84181', 84181, 'K', 'VIET NAM CARRIER AIR STRIKES (428-NPC-34724)', '1965-02-10', 662.1,
  'B&W: continuous launch/recovery cycles: A-4 Skyhawks (VA-155 "NL"), F-4, F-8, arrester landings, catapult launches with steam, "USS CORAL SEA" on an F-4 at 0:20',
  'USS CORAL SEA (CVA-43) air wing: NOT Ranger. ILLUSTRATIVE', [W(0, 600, 'Launches/traps, 3-4 s shots, many clean ones', '')], 'No slate at start; frame grain; end blank grey'),
 nara_film('nara_83299', 83299, 'K', 'COMMISSIONING USS KITTY HAWK (CVA-63) (428-NPC-30453)', '1961-05', 354.0,
  'Colour: dark hangar-deck ceremony, ranks of sailors, bandsmen, ship banner "USS KITTY HAWK CVA-63"', 'Kitty Hawk, not Ranger; very dark, little use', [W(5, 40, 'Banner and hangar crowd', '')], 'Very dark; slate 0:00-0:05'),
 nara_film('nara_84173', 84173, 'K', 'VIETNAM CARRIER AIR STRIKE (428-NPC-34704)', '1965-02-01', 534.5, 'Not reviewed in detail: B&W Feb 1965 carrier strike coverage, same series as 84175/84181', 'Ship not identified; NOT reviewed beyond the sheets', [], '', 'NOT reviewed: sheets only'),
 nara_film('nara_84189', 84189, 'K', 'VIET NAM CARRIER AIR STRIKES (428-NPC-34744)', '1965-02-11', 608.16, 'Not reviewed in detail: B&W carrier strike coverage', 'Ship not identified; NOT reviewed beyond the sheets', [], '', 'NOT reviewed: sheets only'),
 nara_film('nara_85907', 85907, 'K', 'USS CONSTELLATION (CVA-64) OPS (428-NPC-38910)', '1967-08', 645.65, 'Not reviewed in detail: Constellation operations (sister Vietnam-era carrier)', 'Constellation, NOT Ranger', [], '', 'NOT reviewed: sheets only'),
 nara_film('nara_86016', 86016, 'K', 'OPERATIONS ABOARD USS CONSTELLATION (CVA-64) (428-NPC-39124)', '1967-11', 350.98, 'Not reviewed in detail', 'Constellation, NOT Ranger', [], '', 'NOT reviewed: sheets only'),
 nara_film('nara_75529', 75529, 'K', 'CONSTRUCTION OF USS FORRESTAL (CVA-59) (428-NPC-457)', '1954-08-10', 203.4, 'Not reviewed in detail: Newport News construction of the class leader (1954)', 'Forrestal, NOT Ranger (but same yard and class)', [], '', 'NOT reviewed: sheets only'),
 nara_film('nara_87552', 87552, 'K', 'SECNAV VISITS THE USS SARATOGA (CVA-60) (428-NPC-43668)', '1969-11-05', 269.8, 'Not reviewed in detail', 'Saratoga, NOT Ranger', [], '', 'NOT reviewed: sheets only'),
 nara_film('nara_85922', 85922, 'K', 'USS FORRESTAL FIRE (428-NPC-38981)', '1967-07', 236.7, 'Not reviewed in detail: aftermath of the Forrestal fire (graphic subject: check before use)', 'Forrestal, NOT Ranger', [], '', 'NOT reviewed: sheets only'),
 nara_film('nara_85924', 85924, 'K', 'USS FORRESTAL FIRE (428-NPC-38983)', '1967-10-18', 66.0, 'Not reviewed in detail: Forrestal fire, short reel', 'Forrestal, NOT Ranger', [], '', 'NOT reviewed: sheets only'),
 nara_film('nara_76799', 76799, 'K', 'AIRCRAFT CARRIER OPERATIONS (428-NPC-3354)', '', 670.2, 'Not reviewed in detail: undated carrier operations reel (likely 1950s-60s)', 'Ship and date unknown', [], '', 'NOT reviewed: sheets only'),
]
# DVIDS videos
dm = {m['id']: m for m in J('dvids_meta.jsonl') if m['type'] == 'video'}
def dv(i, group, shows, not_shows, windows, avoid, review='reviewed on 2 s sheet'):
    m = dm[i]; f = f'src/film/dvids_vid_{i}.mp4'
    pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate:format=duration', '-of', 'json', f], capture_output=True, text=True)
    d = json.loads(pr.stdout); s = d['streams'][0]
    return dict(stem=f'dvids_vid_{i}', group=group, file=f, title=f"DVIDS {i}: {m['title']}", url=m['url'], rights=dvids_rights(m), date=m['date'], shows=shows + f' | DVIDS caption: {m["desc"][:240]}',
                not_shows=not_shows, w=s['width'], h=s['height'], res=f"{s['width']}x{s['height']} {s['r_frame_rate']} fps H.264 (DVIDS mp4)", duration=round(float(d['format']['duration']), 1), windows=windows, avoid=avoid, status=review,
                sheets=[x for x in sorted(os.listdir('sheets')) if x.startswith(f'dvids_vid_{i}_')])
films += [
 dv('393470', 'G', '1080p: ex-Ranger under tow in Port Orchard Bay, long-lens: tug at the bow, whole ship on the water, close on the island with the Olympics behind. ~13 steady takes of 3-8 s',
    'Ranger named by the DVIDS caption only: no hull number or name legible. Hull is stripped/grey, no aircraft; flight deck bare. Date taken 5 Mar 2015 (page). No audio checked',
    [W(0, 5, 'Bow-on three-quarter: tug under the flare, shore plants in the foreground', ''), W(6, 17, 'Whole ship passing left, tug at the bow', ''), W(18, 29, 'Bow quarter with tug', ''),
     W(30, 42, 'Long shot across water with Olympic peaks, tugs and a boat', ''), W(36, 42, 'Close on island and flight deck with snow mountains behind', ''), W(42, 52, 'Stern-quarter pass', '')], 'None: no slate, begins on picture. Handheld/long-lens shake slight'),
 dv('828554', 'H', '1080p: ex-Kitty Hawk towed in fog from Bremerton (the same Navy tow chain as Ranger): hull side, tugs, rust-brown flight deck edge; ~3:23', 'Kitty Hawk, NOT Ranger. Caption date is 15 Jan 2022 while the metadata says 2021: do not date it',
    [W(0, 70, 'Carrier in fog, tugs coming into frame, steady lateral pass', 'Sheets 02-03 (70-203 s) not reviewed in detail')], 'None', 'sheet 01 reviewed; 02-03 not'),
 dv('830091', 'H', '1080p: "Ghost Ship - Kitty Hawk" (Jan 2022), 2:40', 'Kitty Hawk, NOT Ranger. NOT reviewed in detail', [], 'Unknown', 'NOT reviewed: sheets only'),
 dv('320929', 'H', '720x406, 20 s: first super-carrier headed for scrap (ex-Forrestal leaving Philadelphia, 2014 per the DVIDS description)', 'Low resolution (720x406). Forrestal, NOT Ranger', [], 'Unknown', 'NOT reviewed: sheet only'),
 dv('150095', 'K', '720x406, 2:03: "Remembering Forrestal" (2012)', 'Low resolution; Forrestal, NOT Ranger; subject is the 1967 fire/memorial: check before use', [], 'Unknown', 'NOT reviewed: sheets only'),
 dv('9295', 'I', '480p: flight-deck operations on USS Theodore Roosevelt at sunset (22 Dec 2005): F-14D "101" (CO\'s aircraft, VF-31) with director signalling, plane captains, catapult crew, steam in sun glow. Tail with "Felix" in a Santa hat',
    'NOT Ranger and not the 1980s-90s. 720x480. ILLUSTRATIVE F-14 deck b-roll (the only HD-ish F-14 deck footage found; it is SD)', [W(4, 62, 'F-14D "101" on deck, hand signals, nosewheel, sun low, many clean 3-5 s shots', ''), W(62, 100, 'Catapult crew silhouettes in steam, sunset', '')],
    'DVIDS slate text 0:00-0:03 (black); the clip ends on a long silhouette shot'),
]
# archive.org DIMOC films
ia_rights = 'archive.org item metadata licenseurl "http://creativecommons.org/publicdomain/zero/1.0/" (CC0 mark); creator "Department of Defense" (DIMOC = DoD Defense Imagery film, a US federal work)'
films += [
 dict(stem='ia_dimoc_804615', group='I', file='src/film/ia_dimoc_804615.mpeg', title='U.S. NAVY: AROUND THE CLOCK AND ACROSS THE GLOBE (DoD PIN 804615, 1988)', url='https://archive.org/details/gov.dod.dimoc.804615',
      rights=ia_rights, date='1988', shows='SD Navy promotional film (13:48): opens with an F-14 on a carrier deck cross-faded with a submarine (0:00-0:08), then fleet scenes, missile launches, a homecoming kiss on a carrier pier (1:50-2:20), SEAL boats, Alvin',
      not_shows='Not Ranger; the F-14 image carries other ship text. Low-quality 1980s video (480i MPEG-2 640x480, soft). Reviewed only the first 6 minutes', w=640, h=480, res='640x480 MPEG-2 29.97i as archive.org original', duration=827.9,
      windows=[W(0, 8, 'F-14 on deck, overlay dissolve with sub', 'Dissolve, not a clean shot'), W(105, 140, 'Homecoming on a carrier flight deck/pier, family hugging sailors', 'Ship not named')], avoid='Graphics/captions inside the picture; CBS-style lower thirds ("CAPT Gary Wheatley")',
      status='first 6 min reviewed (10 s overview); rest not', sheets=[f for f in sorted(os.listdir('sheets')) if f.startswith('ia_dimoc_804615_')]),
 dict(stem='ia_dimoc_25127', group='K', file='src/film/ia_dimoc_25127.mpeg', title='FACE OF A NATION (DoD PIN 25127, 1967)', url='https://archive.org/details/gov.dod.dimoc.25127',
      rights=ia_rights, date='1967', shows='"The story of the attack aircraft carrier and the men who man and maintain the aircraft" (28:14 SD)', not_shows='NOT reviewed (overview sheet only); ship not identified', w=640, h=480, res='640x480 MPEG-2 as archive.org original', duration=1694.2,
      windows=[], avoid='unknown', status='NOT reviewed: sheets only', sheets=[f for f in sorted(os.listdir('sheets')) if f.startswith('ia_dimoc_25127_')]),
 dict(stem='ia_dimoc_25684', group='K', file='src/film/ia_dimoc_25684.mpeg', title='CNO SITREP 30/EDITION 10 (DoD PIN 25684, 1974)', url='https://archive.org/details/gov.dod.dimoc.25684',
      rights=ia_rights, date='1974', shows='Navy newsreel (29:26 SD): new classes of ships and aircraft incl. the F-14 (description)', not_shows='NOT reviewed; F-14 segment location unknown. Pre-Ranger-F-14 (Ranger got Tomcats in 1980s)', w=640, h=480, res='640x480 MPEG-2', duration=1766.3,
      windows=[], avoid='unknown', status='NOT reviewed: sheets only', sheets=[f for f in sorted(os.listdir('sheets')) if f.startswith('ia_dimoc_25684_')]),
]
films.sort(key=lambda f: (f['group'], f['stem']))
photos.sort(key=lambda p: (p['group'], p['date'], p['stem']))
json.dump(dict(photos=photos, films=films, groups=GROUPS), open('footage.json', 'w'), indent=1)
print(len(photos), 'photos', len(films), 'films')
import collections
print(collections.Counter(p['group'] for p in photos))
