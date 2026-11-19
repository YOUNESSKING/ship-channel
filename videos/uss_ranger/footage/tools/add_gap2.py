#!/usr/bin/env python3
"""add_gap2.py - gap agent #2 (2026-11-19): merge the new NARA/DVIDS stills and films into footage.json and append new group sections to
FOOTAGE_LIST.md. Inputs are the download metadata written by nara_download.py / dvids_fetch.py (paths below). Idempotent: skips stems already present."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); os.chdir(ROOT)
T = "/tmp/g2/"
NARA_RIGHTS = 'NARA useRestriction: {"status": "Unrestricted"}'
FILM_RIGHTS = ('NARA useRestriction: {"status": "Undetermined"} (NARA default for unreviewed RG 428 reels). Basis: US Navy camera-unit film '
               '(Record Group 428, Naval Photographic Center slate "428.NPC.<n>"), so a US federal work in the public domain.')
def dv_rights(m): return f'DVIDS page licence line: "PUBLIC DOMAIN". Copyright line: "{m["copyright_line"][:160]}"'
NAD = "NARA/DVIC caption only; date and place as captioned, nothing beyond the caption. Hull number not legible unless the shows column says so. NOT Ranger"
VIS = {  # visual notes read on contact sheets
 "6410079": "F-14A with swept wings on a catapult, deck crew in the foreground, heavy sea behind", "6410076": "Same catapult scene, F-14A seen from the wing, deck crew walking",
 "6446094": "F-14A lifting off a runway (NAS Oceana, grass and trees behind)", "6446096": "F-14A just airborne, gear down, from the front quarter", "6446095": "F-14A rotating on the runway",
 "6479663": "F-14 nose emerging from a cloud of catapult steam", "6486045": "Close portrait of a catapult crewman in goggles and green helmet, sea behind", "6384548": "Deck handler leaning into a line, steam rolling along the deck, jets behind",
 "6456128": "S-3A Viking half hidden in catapult steam, crewman crouched at the track", "6409599": "A-6E head-on on the catapult, plane director signalling, sea horizon", "6409600": "A-6E on the cat, directors and crew, steam at right",
 "6409586": "A-6E just launched, rear view, crew at the cat track", "6409587": "A-6E rotating off the bow cat in smoke", "6410025": "A-6E on a catapult in front of the island, deck crew and parked jets",
 "6405125": "A-6E silhouetted on the catapult at dusk", "6640167": "A-6E about to touch down, sun glitter on the sea, seen from the stern", "6640166": "Overhead of a woodland-camouflage A-6E being prepared, red-shirt ordnancemen",
 "6485144": "A-6E in the groove close to the deck, parked A-6s and island behind", "6423938": "A-6E on touchdown, hook down, smoke at the wheels, F-14 parked behind", "6416209": "A-6E (tail code AA) rolling out on the deck",
 "6416306": "F-14 on approach in landing configuration against a pale sky", "6427745": "Underside of an aircraft with its wheels, orange sunset behind",
 "6372099": "Port beam of Enterprise on a dark blue sea, deck full of aircraft", "6640676": "Bow-on, Enterprise ploughing a big white bow wave (1998 photo)", "6405185": "Aerial three-quarter bow, deck crowded with aircraft",
 "6405186": "Aerial bow with white wake, aircraft on the angled deck", "6394957": "Black and white: Enterprise inside what looks like the Golden Gate headlands", "6484934": "Black and white port beam on a grey sea, deck full",
 "6450776": "Port bow close, grey hull with moored ships beyond", "6450774": "Starboard bow close, chain-link fence in front", "6450779": "Starboard bow close, with a second hull at right", "6450778": "Cutter foreground, a carrier in layup behind", "6450777": "Cutter, cruiser and a carrier island at a pier",
 "6457066": "Carrier museum at pier with aircraft on deck and a grey submarine moored in front", "6457067": "Portrait crop of the same scene", "6457068": "Wide view of the museum carrier and the submarine",
 "6440366": "High aerial over a shipyard waterfront with dry docks and cranes", "6378788": "Aerial of two big hulls side by side in a basin, cranes", "6418365": "Low aerial over the yard, big gantry crane left", "6418364": "Same yard, gantry crane labelled NEWPORT NEWS", "6418175": "Looking straight down into a hull in the shipway with cranes", "6417297": "Aerial of the yard and the York/James waterfront with a gantry crane",
 "6468685": "Overhead on a carrier under way with a white wake", "6468804": "Cruiser under way on a calm sea (not a carrier)", "6467556": "Laser-guided bombs on trolleys across the flight deck, A-6Es and the island behind", "6467895": "A-6E with a load of Mark 82 bombs under the wing, deck crew",
 "6485550": "Marines beside an LCAC landing craft on white sand, blue sky", "6485551": "Portrait crop of the same LCAC scene", "6483298": "Crane unloading sacks and boxes on a quay beside a boat", "6486213": "Somali children looking at the camera on a grass bank",
 "6419144": "High aerial on a carrier ahead, small in a blue sea", "6368080": "Aerial starboard quarter on a hazy grey sea, deck crowded", "6368081": "Aerial beam on a hazy grey sea", "6697751": "Two firefighters in hoods and red helmets, hangar bay behind, sparks", "6383910": "Aerial of a carrier in dry dock in a busy shipyard, hull number 66 visible at the bow end",
 "6410079x": ""}
def nara_ph(m, grp, extra_not=""):
    vis = VIS.get(str(m["naId"]), ""); ttl = (m["title"] or "").strip()
    d = (m.get("date") or [None]); d = d[0] if isinstance(d, list) else d
    return dict(stem=m["stem"], group=grp, file=m["file"], title=f'{m["local"]}: {ttl}', url=f'https://catalog.archives.gov/id/{m["naId"]}',
                rights="NARA useRestriction: " + json.dumps(m["use"]) if m.get("use") else NARA_RIGHTS, date=(d or "")[:10],
                shows=(vis + " / " if vis else "") + "NARA caption: " + ttl, not_shows=(extra_not + ". " if extra_not else "") + NAD,
                w=m["w"], h=m["h"], source="NARA")
def dv_ph(m, grp, vis, extra_not):
    return dict(stem=f'dvids_ima_{m["id"]}', group=grp, file=m["file"], title=f'DVIDS {m["id"]}: {m["title"]}', url=m["url"], rights=dv_rights(m), date=m["date"],
                shows=(vis + " / " if vis else "") + "DVIDS caption: " + m["desc"][:260].replace("\n", " "), not_shows=extra_not, w=m["resolution_page"] and None, h=None, source="DVIDS",
                original_res_on_page=m["resolution_page"], virin=m["virin"])
def load(f): return [json.loads(l) for l in open(T + f)] if os.path.exists(T + f) else []
nara = {str(m["naId"]): m for m in load("nara_ph_meta.jsonl")}
dv = {m["id"]: m for m in load("dvids_new.jsonl") if m["type"] == "image"}
GROUPS = {
 "M": "Ex-carrier tows and departures for scrapping (Forrestal 2010, JFK 2025): ILLUSTRATIVE, not Ranger",
 "N": "Bremerton / Puget Sound inactive-ship layup (1990 NARA) and a carrier's last voyage (ILLUSTRATIVE, not Ranger)",
 "O": "Desert Storm / Gulf 1991: carrier deck, bombs, Battle Force Zulu (NOT Ranger)",
 "P": "Operation Restore Hope, Somalia 1992-93 (ground and landing craft, NOT Ranger)",
 "Q": "Flight-deck b-roll: A-6E Intruder, F-14 Tomcat, catapult steam (other carriers, ILLUSTRATIVE)",
 "R": "USS Enterprise (CVN-65) and other carriers at sea 1978-1998 (labelled by ship, NOT Ranger)",
 "S": "Museum carriers: Intrepid (1989), Midway (2014), Lexington (2025)",
 "T": "Shipyard construction / dry dock aerials: Newport News 1980-87, Norfolk 1982 (ILLUSTRATIVE)",
 "U": "Shipboard firefighting (ILLUSTRATIVE, 2002)"}
PH = []  # (id kind, key, group, extra_not)
spec = {
 "M": [("d","290724","Ex-Forrestal under tow past the Naval War College and the Newport Bridge, tug alongside","NOT Ranger. 2010 move Newport to Philadelphia, not the Brownsville voyage. Original on page 2100x1500"),
       ("d","290725","Ex-Forrestal leaving Newport, wide panorama","NOT Ranger. 2010 Newport to Philadelphia, not Brownsville"),
       ("d","290733","Ex-Forrestal leaving Newport, smaller crop","NOT Ranger. 2010 Newport to Philadelphia, not Brownsville"),
       ("d","8834178","Ex-JFK at Pier 4, Philadelphia, at sunrise before leaving for Brownsville","NOT Ranger. No tow shown yet; ship stationary. Page original 6048x4024 (login-only), file is the 2000 px CDN copy"),
       ("d","8834179","Ex-JFK at sunrise, Philadelphia Navy Yard Annex pier","NOT Ranger. Ship stationary at pier. Page original 6048x4024"),
       ("d","8834181","Ex-JFK moored in Philadelphia","NOT Ranger. Ship stationary at pier. Page original 6048x4024"),
       ("d","8834183","Ex-JFK with tugboats alongside, Delaware River, portrait frame","NOT Ranger. Departure 16 Jan 2025 from Philadelphia, not Brownsville arrival. Page original 4284x5712")],
 "N": [("n","6450776","","Date from the NARA record (25 Jan 1990 at Puget Sound Naval Shipyard, Naval Inactive Ship Maintenance Facility). Oriskany (CV 34), NOT Ranger, which was not yet inactive. Hull number not legible"),
       ("n","6450774","","Hornet (CVS 12), NOT Ranger. Layup 1990, Bremerton"),
       ("n","6450779","","Bennington (CVS 20), NOT Ranger. Layup 1990, Bremerton"),
       ("n","6450778","","Bon Homme Richard (CVA 31) and gunboat Canon (PG 90), NOT Ranger. Layup 1990, Bremerton"),
       ("n","6450777","","Oriskany with cutter Glacier and cruiser Oklahoma City, NOT Ranger. Layup 1990, Bremerton"),
       ("d","112224","Kitty Hawk leaving San Diego with sailors manning the rails, 2008","NOT Ranger. Kitty Hawk 2008 final voyage to Bremerton, not Ranger's 1993 departure. Page original 3008x2000")],
 "O": [("n","6467556","","Aboard Kennedy (CV-67), NOT Ranger. Date per record 23 Jan 1991. A-6E deck, bombs: no mission, no night, no explosion"),
       ("n","6467895","","VA-75 A-6E (Kennedy), NOT Ranger. 1 Feb 1991. Armed on deck only: no launch or strike"),
       ("n","6468685","","America (CV-66) in Battle Force Zulu, 2 Mar 1991, NOT Ranger"),
       ("n","6468804","","Cruiser USS Normandy (CG-60) in Battle Force Zulu, 3 Mar 1991: NO carrier, NOT Ranger"),
       ("n","6640166","","Carrier unnamed in the caption (A-6E in woodland camouflage, Feb 1990), NOT Ranger and not Desert Storm (1990-02 record date)"),
       ("n","6640167","","Carrier unnamed in the caption (Feb 1990 record date), NOT Ranger. Country unknown in the finding aid"),
       ("d","2357954","USAF-credited photo: F-14A Tomcats in formation, one refuelling from a KC-10A, Feb 1991","Tomcats' carrier/squadrons not named in the shown caption; NOT a deck picture, NOT Ranger. Page original 2810x1830")],
 "P": [("n","6485550","","Marines landing from an LCAC (15 Dec 1992). No Mogadishu name in the caption beyond Operation Restore Hope; NOT Ranger. No firing, no crowd"),
       ("n","6485551","","Portrait crop, LCAC-22, 15 Dec 1992. NOT Ranger"),
       ("n","6483298","","Port crane unloading relief supplies, Jan 1993. Town not named in the caption. NOT Ranger"),
       ("n","6486213","","Somali children at a food distribution site (Dec 1992). Humanitarian context only; NOT Ranger, no Navy ship"),
       ("d","812366","President Bush walking through a crowd of troops, Mogadishu airport","31 Dec 1992 visit, ground only: NO Navy ship, NO landing. Page original 2880x1924"),
       ("d","812362","President Bush surrounded by service members, Mogadishu, 1 Jan 1993","Ground only: NO Navy ship. Page original 1518x1008")],
 "Q": [("n",s,"","Other carrier or airfield: see caption. NOT Ranger. Captioned date may be the roll date") for s in
       ["6410079","6410076","6479663","6486045","6384548","6456128","6409599","6409600","6409586","6409587","6410025","6405125","6485144","6423938","6416209","6416306","6427745","6446094","6446096","6446095"]] +
      [("d","9213429","F-14 in a cloud of catapult steam, Truman 2005","Truman (CVN 75), NOT Ranger. Page original 2100x1500"),
       ("d","9209292","Catapult crewman's thumbs-up, F-14 behind, Roosevelt 1999","Theodore Roosevelt, NOT Ranger. Original 1777x1372"),
       ("d","9209004","F-14 launching from the waist cat as four F/A-18s wait on the bow cats, Enterprise 1999","Enterprise, NOT Ranger. Original 2100x1500"),
       ("d","9208189","Officer watching an F-14 hurtle down the cat, Nimitz 1998 (portrait)","Nimitz, NOT Ranger. Original 1289x1923"),
       ("d","3413","F-14B (VF-32) launching off a waist catapult, Truman, 26 Dec 2004","Truman, NOT Ranger. Original 2520x1800"),
       ("d","9213572","F-14D being towed across the Roosevelt's deck, 2005","Roosevelt, NOT Ranger. Original 1840x1224"),
       ("d","9215596","F-14D near-supersonic flyby, Roosevelt, final Tomcat launch, 2006","Roosevelt, NOT Ranger. Original 1330x904")],
 "R": [("n","6372099","","Enterprise CVN-65 only (label it Enterprise). 1982 caption date"), ("n","6640676","","Enterprise, 1998 caption date (record date 1998-01-01), NOT the 1980s"),
       ("n","6405185","","Enterprise, Feb 1986"), ("n","6405186","","Enterprise, Feb 1986"), ("n","6394957","","Enterprise, black and white, Sept 1982"), ("n","6484934","","Enterprise, black and white, Fleet Exercise 89 (14 Oct 1989)"),
       ("n","6368080","","Forrestal (CV-59) 1982, NOT Ranger. Flight deck crowded, no event"), ("n","6368081","","Forrestal (CV-59) 1982, NOT Ranger"), ("n","6419144","","Kitty Hawk (CV-63), 30 Jan 1983 en route San Diego after Puget Sound overhaul, NOT Ranger")],
 "S": [("n","6457066","","Intrepid Sea-Air-Space Museum, May 1989 (Fleet Week), with ex-USS Growler (SSG 577). Carrier-as-museum precedent; no interior"),
       ("n","6457067","","Portrait crop of the same Intrepid / Growler scene"), ("n","6457068","","Wide view of Intrepid / Growler"),
       ("d","1239637","Mannequin posed as a launch crewman on the Midway flight deck, 6 Apr 2014","USS Midway Museum, San Diego. Page original 3552x2368"),
       ("d","1250770","Midway museum in San Diego, 6 Apr 2014 (caption: museum seen in San Diego)","Visitor-flight-deck scene; not at sea. Page original 3552x2368"),
       ("d","9228754","Marines presenting colours on the Lexington flight deck, 30 Jul 2025","USS Lexington (CV 16) Museum on the Bay, Corpus Christi. Page original 8256x5504. Not a tour or aircraft view")],
 "T": [("n","6440366","","Newport News Shipbuilding graving dock, Abraham Lincoln (CVN-72) under construction, caption date 1987. 1980s, NOT the 1950s Forrestal-class era"),
       ("n","6378788","","Newport News, Carl Vinson (CVN-70) under construction, ~1980 aerial. NOT the 1950s"),
       ("n","6418365","","Newport News Shipbuilding, Theodore Roosevelt (CVN-71) under construction, Sept 1984. NOT the 1950s"),
       ("n","6418364","","Same, port bow. Sept 1984. NOT the 1950s"), ("n","6418175","","Abraham Lincoln in the shipway, May 1987. NOT the 1950s"),
       ("n","6417297","","Abraham Lincoln in Shipway 12, 26 Oct 1985. NOT the 1950s"),
       ("n","6383910","","Carrier America (CV 66) in dry dock at Norfolk Naval Shipyard, June 1982. NOT Ranger")],
 "U": [("n","6697751","","Hangar bay fire drill, Kitty Hawk, 25 Jan 2002: faces of identifiable crew (do not name). ILLUSTRATIVE. Not a fire at Ranger, no flames")]}
def build_photos():
    out = []
    for g, items in spec.items():
        for k, key, vis, nt in items:
            if k == "n" or (k == "d" and False):
                m = nara.get(key)
                if not m: continue
                e = nara_ph(m, g, nt)
                if vis: e["shows"] = vis + " / " + e["shows"]
            else:
                m = dv.get(key)
                if not m: continue
                e = dv_ph(m, g, vis, nt)
                im = __import__("PIL.Image", fromlist=["x"]).open(m["file"]); e["w"], e["h"] = im.size
            out.append(e)
    return out
FILMS = [
 dict(id="75365", g="V", date="1956-05-20", shows="Black-and-white aerial of a big hull in the building ways under construction, cranes and trucks all around, one finished flight deck at 0:35 beside the ways, camera moving fast and tilting. Silent.",
      ns="Only the NARA title (CONSTRUCTION OF USS INDEPENDENCE (CVA-62)) names the ship; yard not named on any frame; no welding or torch close-ups; not Ranger (Independence was a Forrestal-class sister)",
      avoid="0:00-0:08 NARA logo card; 0:05 white frame; 2:13-2:32 grey and black tail", win=[(10,50,"Low aerial passes over the hull framing in the shipway","Ship not named on screen"),(50,95,"Hull sections, cranes and a floating crane in the harbour (0:45-0:55)",""),(95,132,"Pan across the yard and a deep excavated dock, motion blur 1:35-1:50","")]),
 dict(id="87003", g="V", date="1969-01-31", shows="Colour aerials over a big shipyard with red gantry cranes, steam and smoke, dry docks, a floating crane on a barge with a steam plume (2:30), a red-and-white merchant hull in the ways with masts (2:40-3:10).",
      ns="Nimitz is NOT identifiable on any frame (a red cargo hull is in the ways); no cutting or dismantling; no people close up. The Newport News location is from the record title",
      avoid="0:00-0:08 slate '428.NPC.41766'; ends in a green blur ~4:28", win=[(10,60,"Smoking yard, gantry cranes, dry docks seen from the air",""),(60,130,"Crane booms and dry dock floor, hazy",""),(145,185,"Floating crane on a barge with steam plume, then the hull in the ways",""),(185,265,"Merchant hull in the ways, shipway no. 11 sign (3:50), crane and shed roofs","")]),
 dict(id="87453", g="V", date="1969-10-07", shows="Colour close work in a shipyard: steel framework and cranes against sky (0:25-0:55), dark cavities with welding glow (1:00-2:50, underexposed), welders in hard hats with flying sparks and a grinder (3:00-4:45), an orange torch flare.",
      ns="Cutting torches here are BUILDING (welding) a hull: not scrapping and not a carrier being dismantled. Hull not named; Nimitz only by the record title; much of 1:00-2:50 is very dark",
      avoid="0:00-0:08 slate '428.NPC.43373'; 0:10-0:25 paper tags close-up; white flash ~4:50-4:55; green leader ~5:00", win=[(25,55,"Hull steelwork and crane jibs against the sky",""),(175,225,"Welders and sparks (colour, dark but sparks bright)",""),(225,285,"Grinder sparks, worker in hard hat, orange flare","Torch and sparks are shipbuilding")]),
 dict(id="86427", g="V", date="1968-06-22", shows="Colour keel-laying ceremony for Nimitz at the yard, officials on a flag-draped stand and crowd (0:20-4:50), then a crane lifting a prefabricated unit over the dock (5:00-5:30) and dock-floor aerials (5:30-5:50). Later ~6:00-8:50 more ceremony and crowd.",
      ns="Ceremony of identifiable officials and civilians (do not name); no ship afloat; ship not seen. Clapper reads NIMITZ with a 1968 date",
      avoid="0:00-0:08 slate '428.NPC.40168'; 0:10-0:20 clapperboard", win=[(300,350,"Crane lifts a section over the dock, aerial of keel blocks and shipway","")]),
 dict(id="87638", g="W", date="1970-01-21", shows="Colour: title card 'USS MIDWAY CVA-41 MODERNIZATION / San Francisco Bay Naval Shipyard's greatest challenge / scheduled completion June 1970' (0:15-0:25), shipyard piers with Midway's island, big gantry crane and lifting arm (0:30-2:30), then a long recommissioning ceremony on a flag-draped stage (2:40 to the end, dark).",
      ns="No Ranger. Ceremony is a stage with unnamed officers; ship at sea not shown. The 1970 record date is the recommissioning (Jan 1970). The card text is the only on-screen identification",
      avoid="0:00-0:08 slate '428.NPC.43976'; 0:10-0:15 hand-held slate; ceremony (2:40-12:00) is a static dark stage", win=[(20,30,"On-screen title card (text on a photo) about Midway's modernization",""),(30,150,"Shipyard: Midway at the pier, cranes, steel lifting arm, shipyard gantries","")]),
 dict(id="78768", g="X", date="", shows="Black-and-white firefighting training at a land site: burning fuel pools with thick black smoke, hose teams advancing in gear (0:10-2:00), dark smoke-filled segments (2:15-3:30), more fires at 4:00-5:55. Ends further on (6:00-11:00 not reviewed).",
      ns="A training ground (Naval Damage Control Training Center, Philadelphia per title), NOT a ship and NOT a carrier. Faces of trainees, do not name. ILLUSTRATIVE only",
      avoid="0:00-0:08 slate 'NAMC Photo Service Dept 428.NPC.9524'; 2:15-3:30 mostly black; ~3:50 second slate", win=[(10,130,"Fuel fire with hose teams advancing through black smoke",""),(240,355,"Second burn: flames and hose crews","")]),
 dict(id="87602", g="Y", date="1969-12-17", shows="Colour (grainy, washed out) flight-deck film on Constellation: rear and side views of jets on a wet deck, tail code NK on F-4 Phantom IIs and A-7 Corsair IIs, deck crew in rain gear (0:10-5:50), launches and arrested landings 6:00-10:40.",
      ns="Constellation (CVA-64), NOT Ranger. No F-14s (1969). Faces of crew (do not name). Some frames overexposed and soft",
      avoid="0:00-0:08 slate '428.NPC.43838'; white frame ~2:40; 'End of Recording' card at ~10:40", win=[(10,120,"Aircraft tails and wet deck, crew in oilskins",""),(180,350,"F-4 and A-7 nose and wing views, launch smoke",""),(360,640,"Catapult launches and recoveries, spray on deck","")]),
 dict(id="88003", g="Y", date="1971-01-01", shows="Colour flight-deck stock footage on Kitty Hawk (hand slate and wing lettering 'USS KITTY HAWK'): pilot in cockpit, A-7 Corsair II 'VA-192' close-ups (0:25-1:50), crew handling bombs and arresting-wire work (2:00-3:50), F-4 launches (4:00-5:50), ordnancemen loading bombs (6:00-7:00), A-7 'Cutie Dragon' markings (7:10), catapult crew and A-6 recoveries (10:00-11:55). 13:37 total.",
      ns="Kitty Hawk (CVA-63) only, NOT Ranger; Vietnam era, no F-14. Identifiable faces (do not name). 11:55-13:37 not reviewed",
      avoid="0:00-0:08 slate '428.NPC.45808'; hand-held slates at 0:10-0:20, 3:40, 6:10, 9:40", win=[(25,110,"Close-ups: A-7 nose, pilot, bomb under wing",""),(120,230,"Deck crew, arresting wire, wheel chocking",""),(240,350,"F-4 launches on the cat, steam and sea",""),(360,420,"Ordnancemen carrying and fusing bombs",""),(600,715,"Catapult crew, A-6 and A-7 launches and recoveries","")]),
 dict(id="85734", g="Y", date="1967-05-29", shows="Colour deck film on Intrepid (title): VIP and crew groups (0:10-0:55), a helicopter marked 'SARATOGA' and officers (1:00-1:50), a lot of A-4 Skyhawk deck work: taxi, catapult, launch and recovery with arresting-gear spray (2:00-9:20).",
      ns="Intrepid (CVS-11), NOT Ranger; one helicopter in the frame carries SARATOGA lettering (visiting aircraft). A-4 era, no F-14. Faces of crew (do not name)",
      avoid="0:00-0:08 slate '428.NPC.38371'; olive-green ends at ~9:30", win=[(65,110,"Helicopter landing on the deck",""),(120,340,"A-4 taxi, launch, crew signals, hot exhaust haze",""),(360,550,"A-4 launches and landings, flight deck crew","")]),
 dict(id="85930", g="Z", date="1941-01-01", shows="Black-and-white navy yard film: sailors and cars on a pier (0:10-1:50), ship bows alongside, small craft (2:00-2:50), a crane lifting a large bow/superstructure section onto the ways (3:05-4:50), framework of a ship in the ways (5:00-5:45), then a title card 'U.S.S. SHUBRICK March 12 1940' (5:50).",
      ns="No carrier; no scrapping. Record date is 1941 (title), the Shubrick card says 1940. Yard named only by the title (Norfolk). Not Ranger",
      avoid="0:00-0:08 slate '428.NPC.38989'; 5:50 title card", win=[(40,150,"Pier, ship hulls and yard cranes",""),(185,300,"Crane lifts a ship section over the ways and sets it down","")]),
 dict(id="83543", g="Z", date="1952-04-09", shows="Black-and-white: a blimp over yard cranes (0:10-1:50), then long aerial runs over the yard with docks, piers and moored ships (2:00-5:20).",
      ns="No carrier named or identifiable; yard by the record title only (Norfolk Naval Shipyard, Portsmouth VA). Not Ranger",
      avoid="0:00-0:08 slate '428.NPC.31700'; white-out ~3:40; end 5:30+", win=[(10,110,"Blimp passing yard cranes",""),(120,215,"Aerial runs over docks and piers",""),(230,320,"Aerial over the yard with ships alongside","")]),
 dict(id="881042", g="AA", date="04.25.2023", shows="1080p: aerials of the museum carrier at the San Diego pier and its flight deck (0:05-0:30), an interview with a labelled volunteer (0:30-1:05), archive stills/clips including carrier operations (1:05-1:50), the ship at the pier, interior, 'USS Midway Museum' signs (1:55-2:20).",
      ns="Not Ranger. Archival insert clips (1:05-1:50) have an unverified origin: do not use them. The interviewee's lower-third names him (a private citizen: do not use). Title/credit: DVIDS Fleet Public Affairs Center San Diego",
      avoid="0:00-0:03 sign card; interview 0:30-1:05", win=[(5,30,"Aerial of the pier and Midway's flight deck, hull number and aircraft",""),(115,140,"Pier, signage and interior","")]),
 dict(id="943718", g="AA", date="10.30.2024", shows="1080p grey wet-weather b-roll of Nimitz (CVN-68) leaving Puget Sound Naval Shipyard Bremerton, 30 Oct 2024: F/A-18 and crew on a wet deck (0:05-0:55), hull number 68 and armed sailors at the rail (0:55-2:00), distant shore and aircraft (2:00-2:50).",
      ns="Nimitz, NOT Ranger; no pier or mothball view, no exterior of the ship; crew faces (do not name); Japanese JS NAVY patches on some sailors",
      avoid="0:00-0:04 black text slate", win=[(5,30,"Wet flight deck, F/A-18 and crew",""),(55,100,"Hull number 68, crew at the rail","")]),
 dict(id="746282", g="AA", date="04.06.2020", shows="1080p: Carl Vinson (CVN-70) leaving dry dock at Puget Sound Naval Shipyard, 6 Apr 2020: hull and workers at the dry-dock caisson (0:05-1:10), crane and docks wide shots (1:15-1:30), tug boats and floating pier (1:30-2:00), the carrier at the pier under a blue sky (2:15-2:40).",
      ns="Carl Vinson, NOT Ranger; no mothballed ships; crew faces (do not name)",
      avoid="0:00-0:04 black text slate", win=[(5,70,"Dry-dock hull, workers and mooring work",""),(75,95,"PSNS cranes and piers wide",""),(135,160,"Carrier at the pier in sun","")]),
]
FGROUPS = {"V": "Shipbuilding / construction film: Forrestal-class era and Nimitz (NARA, NOT Ranger)", "W": "Midway modernization 1970 (NARA, shipyard)", "X": "Shipboard-type firefighting training (ILLUSTRATIVE)",
 "Y": "Carrier flight-deck film 1967-71, other ships: Constellation, Kitty Hawk, Intrepid (NOT Ranger)", "Z": "Norfolk Naval Shipyard 1940s-50s (yard b-roll, ILLUSTRATIVE)", "AA": "DVIDS HD: Midway museum, Puget Sound carriers (NOT Ranger)"}
def build_films():
    nm = {str(m["naId"]): m for m in load("nara_film_meta.jsonl")}; dm = {m["id"]: m for m in load("dvids_vid.jsonl")}
    import subprocess
    out = []
    for f in FILMS:
        i = f["id"]
        if i in nm:
            m = nm[i]; stem = f"nara_{i}"; url = f"https://catalog.archives.gov/id/{i}"
            use = (m.get("use") or {}).get("status", ""); rights = FILM_RIGHTS if use == "Undetermined" else "NARA useRestriction: " + json.dumps(m["use"])
            res = "720x480 H.264 59.94i-as-60p, NARA mp4 as downloaded (Digital Betacam copy, SD)"; title = m["title"][:160]; date = f["date"] or ((m.get("date") or [""])[0] or "")[:10]; src = "NARA"; w, h = 720, 480
        elif i in dm:
            m = dm[i]; stem = f"dvids_vid_{i}"; url = m["url"]; rights = dv_rights(m); title = f'DVIDS {i}: {m["title"]}'; date = m["date"]; src = "DVIDS"; w, h = m["w"], m["h"]; res = f"{w}x{h} H.264 (DVIDS mp4)"
        else: continue
        fp = f"src/film/{stem}.mp4"
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", fp]).decode().strip())
        sheets = sorted(s for s in os.listdir("sheets") if s.startswith(stem + "_"))
        wins = [dict(**{"in": a, "out": b}, shows=s, not_shows=n) for a, b, s, n in f["win"]]
        out.append(dict(stem=stem, group=f["g"], file=fp, title=title, url=url, rights=rights, date=date, shows=f["shows"], not_shows=f["ns"], w=w, h=h, res=res, duration=round(dur, 2),
                        windows=wins, avoid=f["avoid"], status="reviewed on overview sheets (5-30 s step), NOT frame-checked: confirm in/out in the editor", sheets=sheets, source=src))
    return out
def fmt(s): return f"{int(s)//60}:{int(s)%60:02d}"
def md(photos, films, gnames_p, gnames_f):
    L = ["", "## Additions 2026-11-19 (footage gap agent #2): recycling, Bremerton, Gulf, museum carriers, generic deck b-roll", "",
         "Added by the second gap pass. Same rights basis and binding \"does NOT show\" column as above. Stills: NARA = the catalog's largest scan capped at 3840 px; DVIDS = the 2000 px CDN copy (the page lists the larger original; the Download button needs a DVIDS login, tried again 2026-11-19 and refused: 403 \"You must be logged in\"). "
         "NOTE: no Ranger-named stills or film were found in this pass: everything below is ILLUSTRATIVE (other ships, other years) and must be captioned by its own ship name. Windows are read from 5-30 s overview sheets (+/-5-10 s), confirm in the editor.", "",
         "### Gaps still open after this pass", "- Ship recycling at Brownsville (torches, cranes cutting sections, ESCO / All Star / International Shipbreaking yards): no public-domain photo or film found. MARAD publishes press text, not images; DVIDS has tows and departures only (nothing at the Brownsville yard). The only cutting/welding shots are NARA shipbuilding (nara_87453, Nimitz 1969: welders and sparks, labelled as building).",
         "- Ranger at her Bremerton pier 1994-2014: none (only the 2015 tow and the 1990 layup views of OTHER carriers, group N). Wikimedia Commons holds 'Aerial Bremerton Shipyard' (CC BY-SA 3.0) and the Ranger tow at 6622x4419 but the Commons upload server answered HTTP 429 for the whole session (see `tools/commons_fetch.py`, ready to run later).",
         "- Desert Storm / Somalia FILM of a carrier: none in NARA (Restore Hope reels are \"Restricted - Possibly\") or DVIDS. Stills only.", "- Columbia River / USACE Portland and 1957 Ranger commissioning: nothing found.", ""]
    for g in gnames_p:
        its = [p for p in photos if p["group"] == g]
        if not its: continue
        L += [f"### {g}. {GROUPS[g]} ({len(its)})", "", "| stem | date | px | shows | does NOT show | record | rights |", "|---|---|---|---|---|---|---|"]
        for p in its: L.append(f'| `{p["stem"]}` | {p["date"]} | {p["w"]}x{p["h"]} | {p["shows"].replace("|","/")} | {p["not_shows"].replace("|","/")} | {p["url"]} | {p["rights"].replace("|","/")} |')
        L.append("")
    L += ["### Films and video added", ""]
    for g in gnames_f:
        its = [f for f in films if f["group"] == g]
        if not its: continue
        L += [f"#### Group {g}: {FGROUPS[g]}", ""]
        for f in its:
            L += [f'##### `{f["stem"]}`: {f["title"]}', f'- file `{f["file"]}`, {f["res"]}, {fmt(f["duration"])} ({f["duration"]} s), date {f["date"]}; record {f["url"]}', f'- rights: {f["rights"]}',
                  f'- shows: {f["shows"]}', f'- does NOT show: {f["not_shows"]}', f'- avoid: {f["avoid"]}; status: {f["status"]}; sheets: {len(f["sheets"])} (`sheets/{f["stem"]}_NN.jpg`)', "- windows (seconds from file start):"]
            for w in f["windows"]: L.append(f'  - {fmt(w["in"])}-{fmt(w["out"])} ({w["in"]}-{w["out"]} s): {w["shows"]}' + (f' / not: {w["not_shows"]}' if w["not_shows"] else ""))
            L.append("")
    return "\n".join(L) + "\n"
if __name__ == "__main__":
    d = json.load(open("footage.json")); have = {x["stem"] for x in d["photos"] + d["films"]}
    ph = [p for p in build_photos() if p["stem"] not in have]; fl = [f for f in build_films() if f["stem"] not in have]
    taken = set(d["groups"])
    for k in list(GROUPS) + list(FGROUPS):
        if k in taken: sys.exit(f"group letter {k} already used in footage.json: rename in add_gap2.py")
    d["photos"] += ph; d["films"] += fl; d["groups"].update(GROUPS); d["groups"].update(FGROUPS)
    json.dump(d, open("footage.json", "w"), indent=1, ensure_ascii=False)
    open("FOOTAGE_LIST.md", "a").write(md(ph, fl, list(GROUPS), list(FGROUPS)))
    print("added photos", len(ph), "films", len(fl))
