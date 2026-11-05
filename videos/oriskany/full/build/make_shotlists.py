"""Full Oriskany video: shot lists c01..c07 (templates/build_chapter.py format, as test v4), per-chapter sound cue lists,
segment specs for the render step, and a report (pacing, film %, clip reuse).

Every beat below = (anchor, sources, options). The anchor is the narration phrase the cut lands on (searched after the
previous shot start). A beat longer than ~4.2 s with several sources is split into pieces (one per source, cut on the
word nearest the even split), so the picture changes every 1.5-4 s. Sources:
  F:<clip>.mp4   real NARA film, from build/film_windows.json (same continuous, vetted shot; never across a cut)
  P:<NARA id> or P:<file stem>   archive photo (footage/src/photos), 2.5D move via archive_shots.py
  M:<scene>      map-kit scene (built in step 2; what it shows = "map" option -> RENDER_PLAN.md)
  H:<scene>      kit/ship hero animation (sinking, cross-sections, tally ...; "hero" option)
  CARD           text_card (option "card")
  A:<template>   anim block rendered by the chapter builder (anim_options / anim_xray / anim_gauge)
Options: num (number_clip), swap (number_clip strike_swap), lt (lower_third kicker_line), card, params (anim), map, hero,
label (film/photo baked label), dim, move (photo), sfx [(role, at, note, extra)], fallback (owner-download fallback note).
Out: chapter/cNN.json, build/sfx_cNN.json, build/segments.json, build/shotlist_report.md
"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FULL = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(FULL, "../../.."))
W = json.load(open(os.path.join(HERE, "words.json")))
CH = {c["key"]: c for c in json.load(open(os.path.join(FULL, "chapters.json")))["chapters"]}
FW = json.load(open(os.path.join(HERE, "film_windows.json")))
# Generic US Government b-roll (public domain; footage/FOOTAGE_LIST.md "Generic US Government b-roll"; footage/dl_broll.sh).
# NEVER the Oriskany: every segment gets a burned-in top-left source tag ("ILLUSTRATIVE · ..."). Windows = continuous shots picked
# from footage/sheets/<stem>_0.jpg (source seconds); film_shot still skips any internal cut it finds.
GEN = {
 "kh_a": ("dvids_828554", [[1.0, 31.0]], "ILLUSTRATIVE · U.S. NAVY · EX-KITTY HAWK, BREMERTON, 2022"),
 "kh_b": ("dvids_828554", [[82.0, 100.0]], "ILLUSTRATIVE · U.S. NAVY · EX-KITTY HAWK, BREMERTON, 2022"),
 "kh_c": ("dvids_828554", [[138.0, 186.0]], "ILLUSTRATIVE · U.S. NAVY · EX-KITTY HAWK TOWED TO A SCRAPYARD, 2022"),
 "fm_tow": ("dvids_791060", [[128.0, 205.0]], "ILLUSTRATIVE · U.S. NAVY · RETIRED SHIP UNDER TOW, MAYPORT, 2021"),
 "fm_out": ("dvids_791060", [[226.0, 246.0]], "ILLUSTRATIVE · U.S. NAVY · RETIRED SHIP TOWED OUT, MAYPORT, 2021"),
 "rita": ("nasa_rita_3438", [[0.2, 13.0]], "NASA · HURRICANE RITA, SEPT 2005 (GOES)"),
 "gustav": ("nasa_gustav_3545", [[0.2, 9.0]], "NASA · HURRICANE GUSTAV, AUG 2008"),
 "snap_b": ("noaa_snapper_school", [[39.0, 51.0]], "ILLUSTRATIVE · NOAA · RED SNAPPER, GULF OF MEXICO"),
 "snap_c": ("noaa_snapper_school", [[52.0, 69.5]], "ILLUSTRATIVE · NOAA · RED SNAPPER, GULF OF MEXICO"),
 "recfish_a": ("noaa_snapper_recfish", [[8.5, 30.0]], "ILLUSTRATIVE · NOAA · RED SNAPPER FISHING, GULF OF MEXICO"),
 "recfish_b": ("noaa_snapper_recfish", [[30.0, 41.0]], "ILLUSTRATIVE · NOAA · FISHING, GULF OF MEXICO"),
 "lab_a": ("noaa_dwh_sampleprep", [[19.0, 35.5]], "ILLUSTRATIVE · NOAA · FISH SAMPLES FOR TESTING, 2010"),
 "lab_b": ("noaa_dwh_sampleprep", [[40.0, 64.0]], "ILLUSTRATIVE · NOAA · FISH SAMPLES FOR TESTING, 2010"),
 "lab_c": ("noaa_dwh_sampleprep", [[64.0, 87.0]], "ILLUSTRATIVE · NOAA · FISH SAMPLES FOR TESTING, 2010"),
 "keys_diver": ("noaa_corals_gulf", [[115.18, 120.08]], "ILLUSTRATIVE · NOAA · DIVER ON A REEF, FLORIDA KEYS", 1.15),   # shot is 4.75 s cut-free: played at 0.87x
 "reef_fish": ("noaa_coral_fgb", [[8.0, 70.0]], "ILLUSTRATIVE · NOAA · REEF FISH"),
 "navy_wreck_b": ("dvids_358436", [[64.0, 100.0]], "ILLUSTRATIVE · U.S. NAVY DIVERS ON A WRECK, COLOMBIA, 2014"),
}
for _k, _v in GEN.items():
    _r, _w, _t = _v[:3]
    FW["g_" + _k + ".mp4"] = {"reel": _r, "clip_in": 0.0, "windows": _w, "tag": _t, "slow": _v[3] if len(_v) > 3 else None}
# Switch for the three owner-download Wikimedia photos in c07 (RENDER_PLAN "Owner downloads"). While a photo is missing from
# footage/src/photos/, its shot uses the kit/hero fallback scene (rendered by make_anims.py). Drop the .jpg in and re-run
# make_shotlists.py + make_segments.py (+ the c07 chapter render) to put the real photo back. WIKI_FALLBACK=1 forces the fallbacks,
# WIKI_FALLBACK=0 forces the photos.
PHOTO_DIR = os.path.join(ROOT, "videos/oriskany/footage/src/photos")
WIKI = {"P:wiki_oriskany_2008_a": ("H:c07_wreck2008", "Fallback for the Wikimedia wreck photo: kit hulk on the seabed, marine growth 2006 -> JULY 2008, fish, light shafts"),
        "P:wiki_grimes_island": ("H:c07_depths_c", "Fallback for Greg Grimes' island photo: cross-section close on the island, 'ISLAND TOP 84 FT' on 'eighty'"),
        "P:wiki_oriskany_2008_b": ("H:c07_divers", "Fallback for the Wikimedia divers photo: diver icons descend to the island top, bubbles rise")}
def wiki_src(src):
    if src not in WIKI: return src, None
    have = os.path.exists(os.path.join(PHOTO_DIR, src[2:] + ".jpg"))
    sw = os.environ.get("WIKI_FALLBACK")
    use_fb = (sw == "1") or (sw != "0" and not have)
    return (WIKI[src][0], WIKI[src][1]) if use_fb else (src, None)
END_SCREEN = 18.0          # end-screen hold after the last word (music bed + end map)
SPLIT_AT = 4.2             # beats longer than this get split across their sources
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
NW = [norm(x["w"]) for x in W]


def find(phrase, after):
    toks = [norm(x) for x in phrase.replace("-", " ").split() if norm(x)]
    for i in range(len(W) - len(toks) + 1):
        if W[i]["start"] >= after - 0.05 and NW[i:i + len(toks)] == toks:
            return i
    near = " ".join(x["w"] for x in W if abs(x["start"] - after) < 5)
    raise SystemExit(f'anchor "{phrase}" not found after {after:.2f}: {near}')


def E(anchor, src, **kw):
    return dict(anchor=anchor, src=src if isinstance(src, list) else [src], **kw)


# ------------------------------------------------------------------------------------------------------------------ beats
B = {}
B["c02"] = [
 E("Start with the day", "F:b3_aerial_underway_1969.mp4"),
 E("In September nineteen seventy-six", "M:c02_bremerton", map="Pacific Northwest -> Puget Sound; pin BREMERTON, WASHINGTON; date line SEPT 1976 lands on 'September'; 'DECOMMISSIONED' tag on 'decommissioned'"),
 E("She was laid up", ["P:6450776", "G:kh_a"], label="BREMERTON, WASHINGTON"),
 E("For thirteen years", "P:6450773", num=dict(variant="right", kicker="LAID UP · BREMERTON", number="13", unit="years", number_at="@thirteen", count={"from": 0, "to": 13, "dur": 0.35, "land_at": "@years"})),   # v2: S2/S9 real 1990 row photo + count
 E("In July nineteen eighty-nine", "P:7578429", num=dict(variant="center_bars", number="STRUCK", subline="FROM THE NAVY LIST · JULY 1989", number_at="@struck", dim="dk")),
 E("On paper", "P:7578430", dim=0.35),
 E("A ship like that", "A:anim_options", params=dict(title="How it *ends*", numbered=False, items=[dict(text="A museum?", at="@museum"), dict(text="A scrapyard?", at="@scrapyard")]), bg="G:fm_tow"),   # v2: one Fort McHenry use in c02
 E("Four of her sisters", "H:c02_sisters", hero="Four Essex-class side silhouettes (kit/ship/ships.js carrier, straight-deck variant) slide in one per beat; a gold 'MUSEUM' tag pops on each on 'museums'. No names (sisters not named in narration)."),
 E("Then in the early", "M:c02_pacific_a", map="Wide North Pacific; dashed arc starts at Bremerton and draws west across the ocean; date line EARLY 1990s"),
 E("Japanese investors", "M:c02_pacific_b", map="Arc lands in Tokyo Bay; pin TOKYO BAY on 'Tokyo Bay'; small tag 'PLANNED ATTRACTION' on 'attraction'"),
 E("They called it", "CARD", card=dict(variant="line", text="“CITY OF AMERICA”", kicker="THE PLAN", at="@city")),
 E("An American warship", "P:7578432", lt=dict(kicker="THE PLAN", text="A WARSHIP AS A THEME PARK", at="@theme")),
 E("The money never came", "A:anim_options", params=dict(title="How it *ends*", numbered=False, items=[dict(text="A museum?", at=0.05, strike_at="@never"), dict(text="A scrapyard?", at=0.05)])),
 E("So the Navy tried", "M:c02_scrap_a", map="Back at the Bremerton pin; tag 'FOR SCRAP' on 'scrapyard'"),
 E("In the early nineteen nineties she was sold", "CARD", card=dict(variant="line", text="SOLD FOR SCRAP", kicker="EARLY 1990s", at="@sold")),
 E("The buyer defaulted", "CARD", card=dict(variant="word", text="DEFAULTED.", at="@defaulted")),
 E("She never even left", "M:c02_scrap_b", map="Same Bremerton pin, closer; tag 'STILL NAVY PROPERTY' on 'custody'"),
 E("In September nineteen ninety-five", "H:c02_ledger_a", hero="A bill-of-sale document graphic (Oswald, gold rule): header 'SALE · SEPTEMBER 1995' on 'September', 'BUYER: PEGASUS (START-UP)' typed in on 'Pegasus'"),
 E("for just over a million", "H:c02_ledger_b", hero="Same document: price line '$1.2 MILLION' stamps in on 'million' (pop)"),
 E("The Navy had appraised", "CARD", card=dict(variant="number", kicker="NAVY APPRAISAL", number="$600,000", number_at="@six")),
 E("Three companies had bid", "CARD", card=dict(variant="number", number="3", unit="bids", number_at="@three")),
 E("The deal said", "CARD", card=dict(variant="line", kicker="THE CONDITION", text="SCRAP HER IN THE U.S.", at="@cut")),
 E("A losing bidder", "CARD", card=dict(variant="pair", text="A PROTEST.", at="@protested", aside="Work held up until December.", aside_at="@december", joke_sound=False)),
 E("In nineteen ninety-six", "M:c02_tow_sf", map="Tow line draws Bremerton -> down the Pacific coast -> San Francisco Bay; date line 1996"),
 E("Pegasus planned", "M:c02_mare", map="Zoom into San Francisco Bay; pin 'MARE ISLAND, VALLEJO' on 'Mare Island'"),
 E("A year later", "CARD", card=dict(variant="line", kicker="1997", text="ALMOST NOTHING CUT", at="@almost")),
 E("The Navy ended the contract", "CARD", card=dict(variant="word", text="DEFAULTED.", at="@default")),
 E("Two scrap deals", "H:c02_tally", hero="Tally board (Oswald, gold ticks): '2 SCRAP DEALS · COLLAPSED' ticks on 'collapsed'; '2 MORE · NO TAKER' ticks on 'no taker'. Reused as a callback in c07."),
 E("So in nineteen ninety-nine", "M:c02_horn_a", map="San Francisco Bay; tow line starts south down the coast; date line 1999 on 'nineteen ninety-nine'"),
 E("All the way around", "M:c02_horn_b", map="Camera follows the tow line down South America, round Cape Horn, up the Atlantic, into the Gulf; pin BEAUMONT, TEXAS on 'Beaumont'. No mileage on screen."),
 E("A ship nobody would take", "M:c02_horn_c", map="Pull back to show the whole route (San Francisco -> Cape Horn -> Beaumont) as one line; tag 'RESERVE FLEET · BEAUMONT'"),
 E("So what kind of ship", "P:6450777", label="LAID UP · BREMERTON, 1990"),   # v2 S6: was the 2006 saluting veteran (off-era, spoils c05)
 E("To understand what was", "P:7578428", move="in"),
 E("go back to the war", "F:b1_launch_crowd.mp4"),
]
B["c03"] = [
 E("Her keel was laid", "M:c03_brooklyn", map="New York harbour; pin NEW YORK NAVY YARD, BROOKLYN; date line MAY 1944 on 'May'"),
 E("She was launched", "F:b1_launch_hull.mp4", lt=dict(kicker="13 OCTOBER 1945", text="LAUNCH · NEW YORK NAVY YARD", at="@thirteenth")),
 E("Six weeks after", "CARD", card=dict(variant="number", number="6", unit="weeks", subline="AFTER JAPAN SURRENDERED", number_at="@six")),
 E("A Second World War carrier", "F:b1_launch_bow.mp4"),
 E("In August nineteen forty-seven", "CARD", card=dict(variant="line", kicker="AUGUST 1947", text="WORK STOPPED", at="@stopped")),
 E("Then in June nineteen fifty", "M:c03_korea", map="Korean peninsula + Sea of Japan; date line JUNE 1950 on 'June'; 'KOREA' label on 'Korea'"),
 E("and the Navy rushed", "P:7578420", label="USS ORISKANY · EARLY 1950s"),
 E("She was the last Essex-class", "P:7578422", lt=dict(kicker="USS ORISKANY (CV-34)", text="LAST ESSEX-CLASS CARRIER FINISHED", at="@last")),
 E("Her crews called", "F:b2_f4u_corsair_landing.mp4", reel_in=16.3, lt=dict(kicker="HER NICKNAME", text="THE MIGHTY O", at="@mighty")),
 E("On the eighteenth of November", "M:c03_mig_a", map="Sea of Japan off north-east Korea; date line 18 NOV 1952; four blue jet tracks leave the carrier icon"),
 E("four of her Panther jets", "F:b2_f9f_panther_deck.mp4", reel_in=12.3),   # v2 M5: reel 78776 12-15.9 s = F9F "111"; 16-24 s = F4U
 E("met seven", "M:c03_mig_b", map="Seven red tracks come down from the north and meet the four blue tracks ('4 vs 7' tag on 'seven'). No result shown on the map (narration gives Williams' credit only)."),
 E("credited with one", "P:7578424", num=dict(variant="right", kicker="CREDITED IN 1952", number="1", unit="MiG", number_at="@one mig", dim="dk")),
 E("In twenty twenty-three", "P:7578425", num=dict(variant="strike_swap", lead1="CREDITED IN 1952", old="1", lead2="NAVY CITATION, 2023", new="4", show_at=0.05, swap_at="@four", strike_at="@four", dim="dk")),
 E("It upgraded his Silver Star", "CARD", card=dict(variant="line", kicker="ROYCE WILLIAMS · 2023", text="NAVY CROSS", at="@navy cross")),
 E("Then came Vietnam", "F:b3_unrep_oiler_1966.mp4"),
 E("Between May and December", "M:c03_tonkin", map="Gulf of Tonkin; pin YANKEE STATION; date line 1965 (MAY-DEC) on 'May'"),
 E("she flew more than", "F:b3_a4_catapult_1966.mp4", num=dict(variant="right", number="12,000", unit="sorties", number_at="@twelve", dim="dk")),
 E("A record for one", ["F:b3_f8_launch_1966.mp4", "F:b3_side_launch.mp4"]),
 E("On the ninth of September", "M:c03_stockdale_a", map="North Vietnam; date line 9 SEPT 1965; one blue track leaves the Gulf of Tonkin heading inland"),
 E("the man who led", "F:b3_aerial_launching.mp4"),
 E("Commander James", "F:b3_a4e_formation_1968.mp4", lt=dict(kicker="HER AIR WING COMMANDER", text="CDR JAMES STOCKDALE", at="@james"), tag="FILM: ORISKANY A-4s, 1968 (NOT HIS AIRCRAFT)"),
 E("was hit by anti-aircraft", "M:c03_stockdale_b", map="Same map, closer: flak bursts on 'anti-aircraft'; the blue track ends in a flash over North Vietnam"),
 E("He was held prisoner", "CARD", card=dict(variant="number", kicker="PRISONER OF WAR", number="7½", unit="years", number_at="@seven")),
 E("A year later the danger", "F:b4_fire_island_smoke.mp4"),
 E("On the morning of the twenty-sixth", "M:c03_yankee", map="Gulf of Tonkin; pin YANKEE STATION; date line 26 OCT 1966 on 'twenty-sixth'"),
 E("she was on Yankee", "F:b3_carrier_aerial_1966.mp4", label="USS ORISKANY · GULF OF TONKIN, OCT 1966"),
 E("Two sailors were stowing", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.5, 0.3], organ_label="FLARES", organ_at="@flares", kicker="26 OCT *1966*", kicker_at=0.15, first_frame="full")),
 E("In a panic", "F:b4_fire_hangar_hoses.mp4"),
 E("packed with about", "F:b4_fire_hose_lines.mp4", num=dict(variant="right", kicker="FLARES IN THE LOCKER", number="≈700", number_at="@seven", dim="dk")),
 E("They burn at about", "F:b4_fire_destroyer_alongside.mp4", num=dict(variant="right", number="5,400", unit="°F", number_at="@five", dim="dk")),
 E("The fire burned", "F:b4_fire_sponson_hoses.mp4", num=dict(variant="right", number="7", unit="hours", number_at="@seven", dim="dk")),
 E("Most of the dead", ["F:b4_fire_oba_team.mp4", "F:b4_fire_hangar_sprinkler.mp4"]),
 E("The fire killed", "F:b4_fire_deck_smoke.mp4", num=dict(variant="center_bars", number="44", number_at="@forty", dim="dk"), sfx_none=True),
 E("Dozens more", "F:b4_fire_burned_a4.mp4"),
 E("Eleven days later", ["F:b4_burial_color_guard.mp4", "F:b4_burial_formation.mp4"], sensitive=True),
 E("Did you or someone", "F:b4_burial_escorts.mp4", sensitive=True),
 E("In that fire", "F:b3_aerial_underway_1969.mp4"),
 E("Tell us their story", "F:b3_aerial_underway2_1969.mp4", win=0, lt=dict(kicker="IN THE COMMENTS", text="TELL US THEIR STORY", at="@tell")),
 E("She was repaired", "M:c03_sf_tonkin", map="San Francisco pin ('REPAIRED') -> line across the Pacific to the Gulf of Tonkin; date line 1967"),
 E("On the twenty-sixth of October nineteen sixty-seven", ["F:b3_island_a4e_parked_1968.mp4", "F:b3_deck_parked_1968.mp4"]),
 E("One year to the day", "CARD", card=dict(variant="line", kicker="26 OCT 1966 → 26 OCT 1967", text="ONE YEAR TO THE DAY", at="@one year")),
 E("One of the pilots", "F:b3_a4e_launch_1968.mp4", lt=dict(kicker="VA-163 · SHOT DOWN 26 OCT 1967", text="LCDR JOHN McCAIN", at="@lieutenant"), tag="FILM: ORISKANY, 1968 (NOT HIS LAUNCH)"),
 E("A surface-to-air missile", "M:c03_hanoi_a", map="Hanoi; a red missile track rises and meets the blue jet track on 'missile' (no target named)"),
 E("He came down in a lake", "M:c03_hanoi_b", map="Zoom into central Hanoi; pin TRUC BACH LAKE on 'lake'"),
 E("He was released", "P:148728286", label="ORISKANY WITH ENTERPRISE + RANGER · 28 JAN 1973", num=dict(variant="right", kicker="RELEASED · MARCH 1973", number="5½", unit="years", number_at="@five")),
 E("Two of America's", "F:b3_bow_on_underway_1966.mp4", lt=dict(kicker="POWs WHO FLEW FROM HER DECK", text="STOCKDALE · McCAIN", at="@prisoners")),
 E("Forty-four of her men", "F:b4_fire_damaged_a4_316.mp4"),
 E("And by the late", "P:6450773", move="in"),
 E("Then in two thousand three", "M:c03_dc", map="Washington, D.C. pin; date line 2003; 'CONGRESS' tag on 'Congress'"),
]
B["c04"] = [
 E("In November two thousand three", "M:c04_dc_gulf", map="From the D.C. pin a gold arrow sweeps to the Gulf coast; date line NOV 2003; tag 'WARSHIPS → REEFS' on 'reefs'"),
 E("old warships", "G:reef_fish"),   # v2 S2: was ex-Kitty Hawk towed to a scrapyard
 E("The Oriskany was the first", "P:6695641", num=dict(variant="center_bars", number="FIRST", subline="WARSHIP OFFERED", number_at="@first", dim="dk")),
 E("Four bids came in", "M:c04_states_a", map="Gulf coast states; '4 BIDS · 5 STATES' tag lands on 'five states'"),
 E("Florida Mississippi", "M:c04_states_b", map="Florida, Mississippi, Texas, then Georgia + South Carolina light up, each on its name"),
 E("In April two thousand four", "M:c04_states_c", map="Only Florida stays lit, gold outline; date line APRIL 2004; tag 'BEST VALUE'"),
 E("The plan was to sink", "P:6695642", num=dict(variant="strike_swap", lead1="THE PLAN", old="SUMMER 2004", lead2="IT TOOK", new="2 MORE YEARS", show_at="@summer", swap_at="@two more", strike_at="@two more", dim="dk")),
 E("First she had to be cleaned", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.5, 0.5], organ_label="CLEANUP", organ_at="@cleaned", kicker="BEFORE THE *reef*", kicker_at=0.1, first_frame="full")),
 E("The work was done in Corpus", "M:c04_corpus", map="Texas Gulf coast; pin CORPUS CHRISTI on 'Corpus Christi'; tag '11 MONTHS' on 'eleven months'"),
 E("Congress had committed", "A:anim_gauge", params=dict(variant="meter", kicker="Cost of *cleanup*", value=2.8, label="COMMITTED BY CONGRESS", unit="$ million", decimals=1, max=25, count_at="@two point", dur=1.2)),
 E("Two point one million", "A:anim_gauge", params=dict(variant="bars", kicker="Cost of *cleanup*", unit="$M", decimals=1, max=25, items=[dict(label="COMMITTED", value=2.8, at=0.1, count_at=0.1, dur=0.6), dict(label="FOR CONTAMINANTS", value=2.1, at="@two point one", count_at="@two point one", dur=1.0, hero=True)])),
 E("Then workers stripped", "H:c04_deck_a", hero="Carrier side cutaway (kit carrier_hero): the flight-deck layer lifts; dark asphalt peels back on 'asphalt'"),
 E("The wood underneath", "H:c04_deck_a2", hero="Same cutaway: the exposed wood glows amber on 'PCBs' with a 'PCBs' tag"),
 E("The Navy blamed", "H:c04_deck_b", hero="Same cutaway, closer on the bow: the two catapult tracks light up on 'catapults', amber seeps into the wood"),
 E("Under the cleanup rules", "CARD", card=dict(variant="line", kicker="THE CLEANUP RULE", text="CONTAMINATED MATERIAL COMES OUT", at="@material")),
 E("unless the EPA", "CARD", card=dict(variant="line", text="UNLESS THE EPA AGREES", at="@unless")),
 E("So the whole wooden deck", "H:c04_deck_c", hero="Same cutaway: the whole amber wood layer lifts off the ship and fades (on 'came out')"),
 E("The cost of removing", "A:anim_gauge", params=dict(variant="meter", kicker="Cost of *cleanup*", value=7.6, label="REMOVING CONTAMINANTS", unit="$ million", decimals=1, max=25, count_at="@seven point", dur=1.2, marks=[dict(value=2.1, label="ORIGINAL", at=0.2)])),
 E("At least half", "CARD", card=dict(variant="number", kicker="SPENT ON THE DECK", number="½+", number_at="@half")),
 E("On top of that", "CARD", card=dict(variant="number", kicker="A COMPUTER MODEL", number="$3.7", unit="million", number_at="@three point")),
 E("Its job was to prove", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.45, 0.35], organ_label="SAFE?", organ_at="@safe", kicker="The *model*", kicker_at=0.1, first_frame="full")),
 E("From Texas she was towed", "M:c04_tow_pens", map="Corpus Christi -> Pensacola tow line along the Gulf coast; pin PENSACOLA; 'HURRICANE SEASON' tag on 'hurricane season'"),
 E("In June two thousand five", "M:c04_hurricane", map="Pensacola -> Beaumont tow line (back west); date line JUNE 2005; hurricane symbol in the Gulf"),
 E("That tow cost", "G:rita", num=dict(variant="right", number="$800,000", kicker="ONE MORE TOW", number_at="@eight", dim="dk")),
 E("She rode out Hurricane", "M:c04_rita", map="Hurricane Rita track (Sept 2005) crosses the Gulf to the Texas-Louisiana line; pin BEAUMONT on 'Beaumont'; tag 'RITA · 2005'"),
 E("By the spring of two thousand six", "P:6696606", label="PENSACOLA · 2006"),
 E("the Navy's bill", "A:anim_gauge", params=dict(variant="meter", kicker="The *Navy's* bill", value=12.7, label="NAVY SPENDING, SPRING 2006", unit="$ million", decimals=1, max=25, count_at="@twelve point", dur=1.2)),
 E("Press reports", "P:6698586", num=dict(variant="right", kicker="PRESS, SINKING DAY", number="≈ $20", unit="million", number_at="@twenty")),
 E("Florida's own legislature", "P:6698597", num=dict(variant="right", kicker="FLORIDA SENATE", number="≈ $21", unit="million", number_at="@twenty one")),
 E("almost all of it Navy", "A:anim_gauge", params=dict(variant="bars", kicker="Almost all *Navy money*", unit="", max=21, items=[dict(label="NAVY", value=20, at=0.1, count_at=0.1, dur=0.9, hero=True), dict(label="FLORIDA COUNTIES", value=1, at=0.6, count_at=0.6, dur=0.4)])),
 E("That is about seven times", "A:anim_gauge", params=dict(variant="bars", kicker="About *seven times*", unit="$M", decimals=1, max=21, items=[dict(label="COMMITTED", value=2.8, at=0.1, count_at=0.1, dur=0.5), dict(label="FINAL", value=20, at=0.4, count_at=0.4, dur=1.0, hero=True)])),
 E("And the flight deck was not", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.5, 0.45], organ_label="?", organ_at="@hiding", kicker="Not the *only place*", kicker_at=0.1, first_frame="full")),
]
B["c05"] = [
 E("On the twenty-second of March", "M:c05_pensacola", map="Beaumont -> Pensacola tow line; date line 22 MAR 2006; pin NAS PENSACOLA on 'Pensacola'"),
 E("for the last time", "P:6695614", fallback="CIV photographer (Megan Kohr): if rights not confirmed use P:6696903"),
 E("She was the test case", "P:6696903", lt=dict(kicker="PENSACOLA · 2006", text="THE TEST CASE", at="@test")),
 E("In May a Navy bomb-disposal", "P:6698577", label="NAVY EOD · MAY 2006"),
 E("On the fifteenth tugs", "P:6698593"),
 E("Former sailors lined", ["P:6698599", "P:6698588"]),
 E("One of them stood", "P:6698587", fallback="CIV photographer: if rights not confirmed use P:6698590 (couple on the seawall; caption nobody)"),
 E("On the morning of the seventeenth", "M:c05_reef", map="Pensacola -> reef site (30°02.555'N 87°00.397'W); date line 17 MAY 2006; scale bar '≈ 22 NM' on 'twenty miles'"),
 E("she sat at anchor", "P:6698606"),
 E("The team had placed", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.5, 0.15], organ_label="22 CHARGES", organ_at="@twenty", kicker="Pipes and *valves*", kicker_at=0.1, first_frame="full", readouts=[dict(text="DEEP IN THE HULL", at="@deep")])),
 E("More than five hundred", "P:6698576", num=dict(variant="right", number="500+", unit="lb", subline="OF EXPLOSIVES", number_at="@five", dim="dk")),
 E("At ten twenty-five", "CARD", card=dict(variant="number", kicker="17 MAY 2006", number="10:25", unit="a.m.", number_at="@ten")),
 E("they fired", "P:6698617", flash=True, sfx=[("explosion", 0.0, "charges fire: blast photo + flash (2nd use of the hook blast, 8 min later)", dict(file="charges_c__f6f10ea4.wav", src=1.76, len=1.0, tail=0.3))]),
 E("The Navy expected", "P:6698616", num=dict(variant="right", kicker="THE NAVY EXPECTED", number="≈5", unit="hours", number_at="@five", dim="dk")),
 E("She took thirty-seven", "P:6698620", num=dict(variant="right", number="37", unit="minutes", count=dict(**{"from": 0, "to": 37, "dur": 0.7, "land_at": "@minutes"}), dim="dk")),
 E("She went down stern first", ["P:6698622", "P:6698611"]),
 E("Then she was gone", "P:6698625"),
 E("She settled upright", "H:c05_hero_a", hero="kit/ship/sinking ShipSink, Oriskany hulk, stern-first descent in the water column (wide), compass 'S' mark on 'south'; depth gauge running"),
 E("Two hundred and twelve", "H:c05_hero_b", hero="Same ShipSink, closer: touchdown, silt puff, gauge lands 'ON THE SEABED 212 FT' on 'two hundred and twelve'"),
 E("The moment she touched", "P:6698613", lt=dict(kicker="17 MAY 2006", text="NOW FLORIDA'S REEF", at="@florida")),
 E("She was the largest ship", "P:6698627", num=dict(variant="center_bars", number="LARGEST", subline="SHIP EVER SUNK AS A REEF", number_at="@largest", dim="dk")),
 E("Guinness World Records", "CARD", card=dict(variant="line", kicker="GUINNESS WORLD RECORDS", text="LARGEST ARTIFICIAL REEF IN THE WORLD", at="@largest")),
 E("It looked like", "P:6698626"),
 E("But her sinking came", "P:6698628"),
 E("And Florida had to keep", "M:c05_fishpin", map="Wreck pin off Pensacola; a small fish icon appears on the pin, then a gold '?' on 'checking'"),
]
B["c06"] = [
 E("Not all of the PCBs", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.5, 0.4], organ_label="PCBs", organ_at="@pcbs", kicker="Still *inside her*", kicker_at=0.1, first_frame="full")),
 E("An estimated seven hundred", "P:6698554", num=dict(variant="right", kicker="PCBs LEFT ABOARD", number="≈700", unit="lb", number_at="@seven", dim="dk")),
 E("They were locked in", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.5, 0.4], organ_label="", organ_at=0.1, kicker="Where *they were*", kicker_at=0.1, first_frame="full", readouts=[dict(text="CABLE", at="@electrical"), dict(text="GASKETS", at="@gaskets"), dict(text="INSULATION", at="@insulation"), dict(text="PAINT", at="@paint")])),
 E("All the liquid PCBs", "P:6698555", lt=dict(kicker="REMOVED", text="ALL LIQUID PCBs", at="@liquid")),
 E("The EPA reviewed", "M:c06_epa_a", map="US South-East; pin ATLANTA · EPA REGION 4 on 'EPA'"),
 E("On the fifteenth of February", "M:c06_epa_b", map="Same map; date line 15 FEB 2006 on 'fifteenth'; gold line from Atlanta to the wreck site on 'ruled'"),
 E("Sinking her with the PCBs", "P:6698556", lt=dict(kicker="EPA RULING · 15 FEB 2006", text="“NOT AN UNREASONABLE RISK”", at="@unreasonable", kicker_at=0.15)),
 E("It was the first approval", "P:6698583", num=dict(variant="center_bars", number="FIRST", subline="APPROVAL OF ITS KIND", number_at="@first", dim="dk")),
 E("And the EPA said", "P:6698600", lt=dict(kicker="EPA", text="FOR HER ALONE", at="@alone")),
 E("There was a condition", "M:c06_fishmap", map="Wreck pin + a control reef pin near Pensacola Bay; fish icons on the wreck pin on 'fish'; 'TEST' tag on 'testing'"),
 E("From December two thousand six", "H:c06_rounds_a", hero="Sampling timeline DEC 2006 -> NOV 2010 draws on its dates; fish icons drop into a tray on the wreck pin"),
 E("sampled eight rounds", "H:c06_rounds_b", hero="Round counter 1 -> 8 ticks (lands on 'eight'); 'ESCAMBIA COUNTY + FWC' credit line"),
 E("Two hundred and fifty-four", "CARD", card=dict(variant="number", number="254", unit="fish", subline="FROM THE WRECK", number_at="@two hundred"), bg="G:lab_a"),
 E("The first results", "G:lab_b"),   # was H:c06_lines_a (empty gauge, no information): lines_b now draws the gauge itself
 E("For the first two years", "H:c06_lines_b", hero="Average bar for years 1-2 rises above both lines on 'above two lines' (music dip 0.8 s before)"),
 E("Florida's screening value", "H:c06_lines_c", hero="Lines get labels on their words: 'FLORIDA' (50 ppb) and 'EPA' (20 ppb)"),
 E("Screening values are not", "H:c06_lines_d", hero="Line labels change to 'SCREENING VALUE' on 'screening values'"),
 E("They are the levels", "G:lab_c"),   # was H:c06_lines_e (magnifier icon only)
 E("The highest readings", "H:c06_species_a", hero="Species bars: RED SNAPPER, PORGIES above the lines (on their names)"),
 E("Vermilion snapper and scamp", "H:c06_species_b", hero="VERMILION SNAPPER, SCAMP bars below both lines (on their names)"),
 E("Environmental groups", "CARD", card=dict(variant="line", kicker="2012 PETITION · FROM FWC DATA", text="ENVIRONMENTAL GROUPS", at="@environmental"), bg="G:snap_b"),
 E("They said snapper", "H:c06_snapper_a", hero="Two snapper icons: 'ON THE CARRIER' vs 'ON A RUBBLE REEF'; attribution plate 'ENVIRONMENTAL GROUPS' stays on"),
 E("about seven times more", "H:c06_snapper_b", hero="Gold bracket '≈ 7×' lands on 'seven times' between the two snapper bars"),
 E("That reef was eight", "M:c06_rubble", map="Wreck pin + rubble reef pin; dashed line '8 MI' on 'eight miles'"),
 E("And tagging suggested", "M:c06_tag", map="A tag icon circles the wreck pin on 'stay on the wreck'"),
 E("Then the numbers came down", "H:c06_down_a", hero="Gauge again; the average bar starts to fall (years 3-4 appear)"),
 E("By about three years", "H:c06_down_b", hero="Bar drops under 'FLORIDA' on 'below Florida's line'"),
 E("By about four years", "H:c06_down_c", hero="Bar drops under 'EPA' on 'below both'"),
 E("No fish-eating advisory", "CARD", card=dict(variant="line", kicker="FLORIDA", text="NO ADVISORY ISSUED", at="@no fish"), bg="G:recfish_a"),
 E("The last published", "H:c06_down_d", hero="The timeline ends in a dashed line after year 4 on 'stop there'"),
 E("So here is the question", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.5, 0.4], organ_label="", organ_at=0.1, kicker="The *question*", kicker_at=0.1, first_frame="full")),
 E("If the Navy knew", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.5, 0.4], organ_label="?", organ_at="@take", kicker="Why not *take them out?*", kicker_at="@why", first_frame="full")),
]
B["c07"] = [
 E("To answer that", "M:c07_dive", map="Dive from the sea surface down to the wreck pin off Pensacola (like the hook dive, slower, from the east)"),
 E("She does not sit", "P:wiki_oriskany_2008_a", label="THE WRECK · JULY 2008", fallback="OWNER DOWNLOAD (Wikimedia 'Oriskany July 2008', Gareth Richards, CC BY-SA 3.0); fallback H:c07_today (kit hulk on the seabed, light shafts)"),
 E("The storms saw", "G:gustav"),   # was M:c07_storm (generic swirl, no information); Gustav is named 6 s later
 E("Within about two and a half", "H:c07_settle", hero="Cross-section (kit hulk on seabed): hull sinks ~10 ft into the sediment on 'ten feet'; gauge '≈10 FT'"),
 E("Among them was Hurricane", "M:c07_gustav", map="Hurricane Gustav track (Sept 2008) over the Gulf near the wreck pin; tag 'GUSTAV · 2008'"),
 E("In late two thousand nine", "H:c07_funnel", hero="Cross-section close on the island: the funnel casing peels away on 'tore away'; date 'LATE 2009'"),
 E("Today her flight deck", "H:c07_depths_a", hero="Cross-section: label 'FLIGHT DECK ≈145-150 FT' lands on 'one hundred and forty-five'"),
 E("to one hundred and fifty", "H:c07_depths_b", hero="Same, camera eases to the deck; the range bracket draws"),
 E("The top of her island", "P:wiki_grimes_island", label="ISLAND TOP · 2009", fallback="OWNER DOWNLOAD (Greg Grimes, CC BY-SA 2.0); fallback H:c07_depths_c (label 'ISLAND TOP 84 FT')"),
 E("The deck is beyond", "H:c07_depths_d", hero="Dashed 'SPORT-DIVING LIMIT' line above the deck on 'limits'"),
 E("Florida warns divers", "CARD", card=dict(variant="line", kicker="FLORIDA FWC", text="NEVER GO INSIDE", at="@never"), bg="G:navy_wreck_b"),
 E("The divers came anyway", "P:wiki_oriskany_2008_b", label="DIVERS · JULY 2008", fallback="OWNER DOWNLOAD (Wikimedia 'Oriskany July 2008' #2); fallback H:c07_divers (diver icons descend to the island)"),
 E("In her first year", "CARD", card=dict(variant="number", kicker="FIRST YEAR", number="4,200", unit="dive trips", number_at="@four thousand"), bg="G:keys_diver"),
 E("They brought about", "CARD", card=dict(variant="number", kicker="ECONOMIC IMPACT", number="$3.6", unit="million", number_at="@three point"), bg="G:recfish_b"),
 E("to two counties", "M:c07_counties_a", map="Pensacola area; two county outlines appear on 'two counties'"),
 E("Escambia in Florida", "M:c07_counties_b", map="ESCAMBIA (FL) lights on 'Escambia', BALDWIN (AL) on 'Baldwin'"),
 E("And sixty-seven jobs", "CARD", card=dict(variant="number", number="67", unit="jobs", number_at="@sixty")),
 E("Now back to the question", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.5, 0.4], organ_label="?", organ_at="@pcbs", kicker="Why leave *the PCBs in?*", kicker_at="@why", first_frame="full")),
 E("Almost all of what", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.5, 0.4], organ_label="97 %", organ_at="@ninety", kicker="In her *wiring*", kicker_at="@wiring", first_frame="full")),
 E("The Navy said ripping", "H:c07_apart", hero="Carrier profile breaks into sections on 'taking the ship apart'"),
 E("And taking her apart", "P:6450776", lt=dict(kicker="1976–2006", text="NEVER TAKEN APART", at="@nobody")),   # v2 S2: was ex-Kitty Hawk towed to a scrapyard
 E("Two scrap deals", "H:c07_tally", hero="Callback: the c02 tally board ('2 COLLAPSED · 2 NO TAKER'), same look"),
 E("Getting the wiring out", "P:6698554", move="out"),
 E("A reef was different", "G:snap_c"),   # was M:c07_reefpin (pin glow only)
 E("The Navy said reefing", "CARD", card=dict(variant="line", kicker="THE NAVY'S SUMS", text="REEF vs. SCRAP", at="@reefing")),
 E("cost about a quarter", "A:anim_gauge", params=dict(variant="bars", kicker="About *a quarter*", unit="", max=4, items=[dict(label="SCRAP + RECYCLE", value=4, at=0.1, count_at=0.1, dur=0.5), dict(label="REEF + CLEANUP", value=1, at="@quarter", count_at="@quarter", dur=0.6, hero=True)])),
 E("Even as the bill climbed", "A:anim_gauge", params=dict(variant="bars", kicker="Still a *bargain?*", unit="$M", max=25, items=[dict(label="REEF · PRESS EST. 2006", value=20, at=0.1, count_at="@bill", dur=1.0, hero=True)])),
 E("Next to an estimated", "A:anim_gauge", params=dict(variant="bars", kicker="Still a *bargain?*", unit="$M", max=25, items=[dict(label="REEF · PRESS EST.", value=20, at=0.05, count_at=0.05, dur=0.3), dict(label="SCRAP · USNI 2006 EST.", value=24, at="@twenty four", count_at="@twenty four", dur=1.0, hero=True)]), bg="G:kh_a"),
 E("But that bargain", "P:6695641", move="out"),
 E("Within two years", "CARD", card=dict(variant="line", kicker="MARAD · REPORT TO CONGRESS · JAN 2008", text="A WARNING", at="@warning"), bg="G:fm_out"),
 E("Cleaning ships to the new", "CARD", card=dict(variant="line", kicker="THE WARNING", text="CLEAN TO THE NEW STANDARD", at="@standard")),
 E("could wipe out", "CARD", card=dict(variant="line", kicker="MARAD · JAN 2008", text="SAVINGS COULD BE WIPED OUT", at="@wipe")),   # v2 M7: no invented $ figure
 E("So that is why", "P:6698624", move="in"),
 E("Nobody would take her whole", "A:anim_options", params=dict(title="What do you do with *a carrier?*", numbered=False, items=[dict(text="A museum?", at=0.05, strike_at="@whole"), dict(text="A scrapyard?", at=0.05, strike_at="@stick")])),
 E("And the PCBs were in her wiring", "A:anim_xray", params=dict(image="../../test_v4/assets/carrier_hero_side.png", animal_w=1180, organ="dot", organ_pos=[0.5, 0.4], organ_label="WIRING", organ_at="@wiring", kicker="Only by *taking her apart*", kicker_at="@only", first_frame="full")),
 E("The bottom of the Gulf was", "A:anim_options", params=dict(title="What do you do with *a carrier?*", numbered=False, items=[dict(text="A museum?", at=0.02, strike_at=0.05), dict(text="A scrapyard?", at=0.02, strike_at=0.1), dict(text="The bottom of the Gulf", at="@bottom", chosen=True)]), bg="G:reef_fish"),
 E("By the Navy's own sums", "A:anim_gauge", params=dict(variant="bars", kicker="The Navy's *own sums*", unit="", max=4, items=[dict(label="SCRAP + RECYCLE", value=4, at=0.05, count_at=0.05, dur=0.4), dict(label="REEF + CLEANUP", value=1, at=0.3, count_at=0.3, dur=0.8, hero=True)])),   # v2 M8: the Navy's own ratio (USNI06), not the press $20M
 E("She is still the only", "H:c07_today", hero="Kit hulk upright on the seabed, light shafts, fish icons; tag 'THE ONLY CARRIER EVER REEFED' on 'only'"),
 E("She will not be the biggest", "F:b10_ssus_profile.mp4"),
 E("On November twelfth", "F:b10_ssus_crane_river.mp4", num=dict(variant="right", kicker="10 A.M. · WEATHER PERMITTING", number="NOV 12", number_at="@november", dim="dk")),
 E("Okaloosa County plans", "M:c07_okaloosa", map="Florida panhandle; Okaloosa County outline + DESTIN pin on 'Okaloosa'; liner icon (kit liner_top) appears off Destin on 'SS United States'"),
 E("She is nine hundred and ninety", "P:loc_haer_pa647_582545", num=dict(variant="right", number="990", unit="ft", subline="SS UNITED STATES · 2012 LAYUP", number_at="@nine hundred", dim="dk")),
 E("No explosives this time", "CARD", card=dict(variant="pair", text="NO EXPLOSIVES.", aside="They will flood her.", at="@no explosives", aside_at="@they will", joke_sound=False)),
 E("She will lie about thirteen", "M:c07_endmap", map="test v4 endmap.js re-timed: both pins (USS ORISKANY reef + SS UNITED STATES · NOV 12), dashed '13 NAUTICAL MILES' on 'thirteen'"),
 E("And here is the twist", "F:b10_ssus_stacks.mp4"),
 E("Okaloosa County put", "P:6698606", num=dict(variant="right", kicker="OKALOOSA COUNTY'S SHARE", number="$50,000", number_at="@fifty", subline="TOWARD SINKING THE ORISKANY", dim="dk")),
 E("Now it is about to take", "M:c07_title", map="End map again: a gold 'PLANNED · LARGEST ARTIFICIAL REEF' tag slides from the Oriskany pin to the SS United States pin on 'take her title'"),
 E("So was the bottom", "F:b3_aerial_underway2_1969.mp4"),
 E("Or just the cheapest", "P:6698625", move="out"),
 E("Tell us in the comments", "M:c07_endscreen", map="End map holds both pins (end-screen space right half); card 'BEST WAY? OR CHEAPEST?' on 'tell us'; 18 s hold with the music bed (end screen)", endscreen=True),
]

# ------------------------------------------------------------------------------------------------------------------ build
segments = []; uses = {}; report = []; film_ptr = {}; REEL_USED = {}
MOVES = ["in", "out", "left", "right"]; mv_i = 0


def film_window(clip, dur, used_at, win=None, reel_in=None):
    """next clean sub-window of the vetted continuous shot (advances, so a reuse shows different frames); win = force window index.
    A clip with "slow" plays slowed down: the window only has to hold need / slow source seconds (the segment keeps its length)."""
    w = FW[clip]["windows"]; need = dur + 0.4
    if reel_in is not None:   # v2: a vetted in-point forced from the frames (c03 Panther / Corsair)
        REEL_USED.setdefault(FW[clip]["reel"], []).append((reel_in, reel_in + need)); return round(reel_in, 2), round(need, 2), ""
    if FW[clip].get("slow"):
        a, b = w[0]; return round(a, 2), round(need, 2), ""
    if win is not None:
        a, b = w[win]; start = a + 0.15; REEL_USED.setdefault(FW[clip]["reel"], []).append((start, start + need))
        return round(start, 2), round(min(need, b - a - 0.2), 2), "" if b - a - 0.2 >= need else "SHORT"
    p = film_ptr.get(clip)
    cand = []
    for a, b in w:
        if b - a >= need: cand.append((a, b))
    if not cand:
        a, b = max(w, key=lambda x: x[1] - x[0]); return a + 0.1, min(b - a - 0.2, need), "SHORT"
    if p is None:
        a, b = max(cand, key=lambda x: x[1] - x[0]); start = a + 0.15
    else:
        start = None
        for a, b in cand:
            s = max(a + 0.15, p + 0.1)
            if s + need <= b: start = s; break
        if start is None: a, b = cand[0]; start = a + 0.15
    # never overlap reel seconds already used by ANY clip of the same reel (b1 launch / b2 Panther-Corsair share reel spans)
    reel = FW[clip]["reel"]; used = REEL_USED.setdefault(reel, [])
    tries = 0
    while any(not (start + need <= u0 or start >= u1) for u0, u1 in used) and tries < 400:
        start += 0.25; tries += 1
        a_ok = [w_ for w_ in cand if w_[0] <= start and start + need <= w_[1]]
        if not a_ok:
            nxt = [w_ for w_ in cand if w_[0] > start]
            if not nxt: break
            start = nxt[0][0] + 0.15
    used.append((start, start + need))
    film_ptr[clip] = start + need
    return round(start, 2), round(need, 2), ""


def piece_times(t0, t1, n, after):
    """split [t0,t1] into n pieces cutting at word starts nearest the even split"""
    cuts = [t0]
    for k in range(1, n):
        target = t0 + (t1 - t0) * k / n
        ws = [x["start"] for x in W if cuts[-1] + 1.2 < x["start"] < t1 - 1.2]
        if not ws: break
        cuts.append(min(ws, key=lambda s: abs(s - target)) - 0.08)
    return cuts


def kind(src): return src.split(":")[0] if ":" in src else src


all_chapters = {}
for ck in ["c02", "c03", "c04", "c05", "c06", "c07"]:
    ch = CH[ck]; c0 = ch["start"]; cend = ch["end"] + (END_SCREEN if ck == "c07" else 0.0)
    beats = B[ck]; after = c0
    # resolve beat start times (absolute narration seconds); the first beat starts at the chapter start
    starts = []
    for i, b in enumerate(beats):
        wi = find(b["anchor"], after)
        t = W[wi]["start"] - 0.12
        if i == 0: t = c0
        starts.append(t); after = W[wi]["start"] + 0.05
    shots = []; cues = []; n = 0
    for i, b in enumerate(beats):
        t0 = starts[i]; t1 = starts[i + 1] if i + 1 < len(beats) else cend
        srcs = b["src"]
        npieces = 1
        if (t1 - t0) > SPLIT_AT and len(srcs) > 1: npieces = min(len(srcs), max(2, math.ceil((t1 - t0) / 3.2)))
        pts = piece_times(t0, t1, npieces, after) if npieces > 1 else [t0]
        bounds = pts + [t1]
        for k in range(len(pts)):
            a, z = bounds[k], bounds[k + 1]; src = srcs[k % len(srcs)]; n += 1
            src, fb_shows = wiki_src(src)
            sid = f"s{n:02d}"; kd = kind(src); dur = round(z - a, 3)
            shot = {"id": sid, "start": f"t{a - c0:.2f}", "sfx": False}
            if k == 0 and b.get("tag"): shot["tag"] = b["tag"]          # v2: film date tag (drawn on top by build_chapter)
            clipfile = None
            seg = None
            if kd in ("F", "G"):
                clip = src[2:] if kd == "F" else f"g_{src[2:]}.mp4"; ss, need, flag = film_window(clip, dur, a, b.get("win") if k == 0 else None, b.get("reel_in") if k == 0 else None)
                clipfile = f"f_{ck}_{sid}.mp4"
                seg = dict(file=clipfile, kind="film", clip=clip, reel=FW[clip]["reel"], reel_in=ss, dur=need, label=b.get("label") if k == 0 else None,
                           note=flag)
                if kd == "G": seg.update(generic=True, tag=FW[clip]["tag"]); shot["tag"] = FW[clip]["tag"]   # v2: tag drawn on top, not burned in
                uses.setdefault(clip, []).append(a)
            elif kd == "P":
                pid = src[2:]; move = b.get("move") or MOVES[mv_i % 4]; mv_i += 1
                clipfile = f"p_{ck}_{sid}.mp4"
                seg = dict(file=clipfile, kind="photo", photo=pid, dur=round(dur + 0.35, 2), move=move, depth=True,
                           label=b.get("label") if k == 0 else None, shake=b.get("shake"), fallback=b.get("fallback"))
                uses.setdefault(pid, []).append(a)
            elif kd == "M":
                clipfile = f"m_{src[2:]}.mp4"
                seg = dict(file=clipfile, kind="map", scene=src[2:], dur=round(dur + (0.0 if b.get("endscreen") else 0.35), 2), t0_abs=round(a, 3),
                           narration=" ".join(x["w"] for x in W if a <= x["start"] < z), shows=b.get("map"))
            elif kd == "H":
                clipfile = f"h_{src[2:]}.mp4"
                seg = dict(file=clipfile, kind="hero", scene=src[2:], dur=round(dur + 0.35, 2), t0_abs=round(a, 3),
                           narration=" ".join(x["w"] for x in W if a <= x["start"] < z), shows=fb_shows or b.get("hero"))
                if fb_shows: seg.update(dur=round(dur, 3), replaces=f"p_{ck}_{sid}.mp4")
            if seg: segments.append(dict(chapter=ck, shot=sid, **seg))
            bgfile = None
            if b.get("bg") and k == 0:   # generic US-Gov film UNDER a card (card -> its lower-third / number layout over the film) or an anim (bg_clip)
                bclip = f"g_{b['bg'][2:]}.mp4"; bss, bneed, bflag = film_window(bclip, dur, a)
                bgfile = f"b_{ck}_{sid}.mp4"
                segments.append(dict(chapter=ck, shot=sid, file=bgfile, kind="film", clip=bclip, reel=FW[bclip]["reel"], reel_in=bss, dur=bneed,
                                     label=None, note=bflag, generic=True, tag=FW[bclip]["tag"], under=kd, **({"slow": FW[bclip]["slow"]} if FW[bclip].get("slow") else {})))
                uses.setdefault(bclip, []).append(a); shot["tag"] = FW[bclip]["tag"]
            # template
            if kd == "CARD":
                c = dict(b["card"]); var = c.pop("variant")
                shot.update(template="text_card", variant=var, card=True, params=c)
                if bgfile: shot["clip"] = {"file": bgfile, "push": None}
                if var in ("line", "number") and c.get("kicker") and "kicker_at" not in c:
                    shot["params"]["kicker_at"] = 0.15   # step 3: a card on a dark picture never sits empty until its word (blackdetect found 3.3 s)
            elif kd == "A":
                tpl = src[2:]; p = dict(b["params"]); var = p.pop("variant", None) or {"anim_options": "list", "anim_xray": "animal", "anim_gauge": "bars"}[tpl]
                shot.update(template=tpl, variant=var, params=p)
                if bgfile: shot["bg_clip"] = {"file": bgfile, "show": 0.5}
            elif "num" in b and k == 0:
                p = dict(b["num"]); var = p.pop("variant")
                if var == "right": p.pop("dim", None)
                shot.update(template="number_clip", variant=var, clip={"file": clipfile, "push": None}, params=p)
            elif "swap" in b and k == 0:
                p = dict(b["swap"]); shot.update(template="number_clip", variant="strike_swap", clip={"file": clipfile, "push": None}, params=p)
            elif "lt" in b and k == 0:
                p = dict(b["lt"]); shot.update(template="lower_third", variant="kicker_line", clip={"file": clipfile, "push": None}, params=p)
            elif kd == "M":
                shot.update(template="map_clip", variant="baked", clip={"file": clipfile, "push": None}, params={})
            else:
                pr = {"dim": b["dim"]} if b.get("dim") else {}
                shot.update(template="clip_plain", variant="push", clip={"file": clipfile, "push": None}, params=pr)
            if b.get("flash") and k == 0: shot["flash"] = True
            shots.append(shot)
            # ---- sound cues (test v4 roles; density ~16/min; nothing without its picture)
            if b.get("sensitive") or b.get("sfx_none"): pass
            elif k == 0 and b.get("sfx"):
                for role, at, note, extra in b["sfx"]: cues.append(dict(shot=sid, at=at, role=role, note=note, **extra))
            elif k == 0 and (kd == "M") and (i == 0 or kind(beats[i - 1]["src"][0]) != "M"):
                cues.append(dict(shot=sid, at=0.3, role="whoosh", note=f"map move starts ({src[2:]})"))
            if k == 0 and shot["template"] == "number_clip" and not b.get("sfx_none") and "number_at" in shot["params"]:
                cues.append(dict(shot=sid, at=shot["params"]["number_at"], role="pop", note=f"number lands: {shot['params'].get('number')}"))
            if k == 0 and shot["template"] == "text_card" and shot["variant"] in ("number", "number_left"):
                cues.append(dict(shot=sid, at=shot["params"]["number_at"], role="pop", note=f"card number lands: {shot['params'].get('number')}"))
            if k == 0 and shot["template"] == "text_card" and shot["variant"] == "word":
                cues.append(dict(shot=sid, at=shot["params"]["at"], role="hit", note=f"stamp: {shot['params'].get('text')}"))
            if k == 0 and not (b.get("sensitive") or b.get("sfx_none")):
                pr = shot.get("params", {}); tpl = shot["template"]
                if tpl == "lower_third": cues.append(dict(shot=sid, at=pr.get("at", 0.3), role="tick", note=f"label: {pr.get('text')}"))
                if tpl == "text_card" and shot["variant"] in ("line", "pair"): cues.append(dict(shot=sid, at=pr.get("at", 0.3), role="pop", note=f"card: {pr.get('text')}"))
                if tpl == "anim_options":
                    for it in pr.get("items", []):
                        cues.append(dict(shot=sid, at=it["at"], role="tick", note=f"option appears: {it['text']}"))
                        if "strike_at" in it: cues.append(dict(shot=sid, at=it["strike_at"], role="tick", note=f"option struck: {it['text']}"))
                        if it.get("chosen"): cues.append(dict(shot=sid, at=it["at"], role="boom", note=f"the answer: {it['text']}"))
                if tpl == "anim_xray":
                    prev = shots[-2]["template"] if len(shots) > 1 else ""
                    if prev != "anim_xray": cues.append(dict(shot=sid, at=0.0, role="riser", note="reverse riser INTO the x-ray", lead=True))
                    if isinstance(pr.get("organ_at"), str): cues.append(dict(shot=sid, at=pr["organ_at"], role="tick", note=f"x-ray mark: {pr.get('organ_label')}"))
                    for r_ in pr.get("readouts", []): cues.append(dict(shot=sid, at=r_["at"], role="tick", note=f"readout: {r_['text']}"))
                if tpl == "anim_gauge":
                    if "count_at" in pr: cues.append(dict(shot=sid, at=pr["count_at"], role="pop", note=f"gauge counts: {pr.get('label')}"))
                    for it in pr.get("items", []):
                        if it.get("hero"): cues.append(dict(shot=sid, at=it["count_at"], role="hit", note=f"gauge hero bar lands: {it['label']}", offset_after=it.get("dur", 1.0)))
                if kd == "M" and i > 0 and kind(beats[i - 1]["src"][0]) == "M": cues.append(dict(shot=sid, at=0.1, role="tick", note=f"map beat ({src[2:]})"))
            if kd in ("F", "G") and not b.get("sensitive"):
                cl = src[2:]
                if any(x in cl for x in ("catapult", "_launch", "side_launch", "aerial_launching")): cues.append(dict(shot=sid, at=0.2, role="jet", note=f"aircraft launches on screen ({cl})", end_shot=sid))
            if kd == "P" and src[2:] in ("6698620", "6698622"): cues.append(dict(shot=sid, at=0.0, role="ship", note="hull settling: groan", file="groan_a__7c63fd7c.wav", end_shot=sid))
            if kd == "P" and src[2:] in ("6698611", "6698625"): cues.append(dict(shot=sid, at=0.05, role="ship", note="water closes over the hull: flood", file="flood_a__db95b348.wav", end_shot=sid))
            if kd == "P" and src[2:] == "6698626": cues.append(dict(shot=sid, at=0.0, role="ship", note="foam: air bursting out", file="bubbles_a__e58b390c.wav", end_shot=sid))
            if src == "H:c05_hero_a": cues.append(dict(shot=sid, at=0.2, role="ship", note="drawn carrier going down: hull groan", file="groan_a__7c63fd7c.wav", end_shot=sid))
            if src == "H:c05_hero_b": cues.append(dict(shot=sid, at="@two hundred", role="impact", note="hull touches the seabed (underwater thump)", file="charges_b__0ecb5c38.wav"))
            if src in ("H:c02_ledger_b", "H:c02_tally", "H:c07_tally", "H:c06_snapper_b", "H:c06_lines_b", "H:c06_down_b", "H:c06_down_c", "H:c06_rounds_b", "H:c07_settle", "H:c07_funnel", "H:c07_apart"):
                cues.append(dict(shot=sid, at=0.6, role="pop", note=f"{src[2:]}: its main graphic beat (step 2: retime to the scene's event frame)"))
            if src == "F:b10_ssus_profile.mp4" and ck == "c07": cues.append(dict(shot=sid, at=0.0, role="horn", note="SS United States on screen: liner horn (signature sound, -14)", end_shot=sid))
            report.append((ck, sid, round(a, 2), round(dur, 2), shot["template"], src + (f" + bg {b['bg']}" if bgfile else ""), b["anchor"]))
    # signature beats per chapter (picture-locked)
    beds = []
    film_shots = [g["shot"] for g in segments if g["chapter"] == ck and g["kind"] == "film" and not g.get("generic")]   # NARA archive film only
    generic_shots = [g["shot"] for g in segments if g["chapter"] == ck and g.get("generic")]
    chj = {"key": ck, "title": f"Oriskany full · {ch['title']}", "words": "../build/words.json", "audio_offset": round(c0, 3),
           "clips_dir": "../segments", "duration": round(cend - c0, 3), "fade_out": 0.6 if ck == "c07" else 0.0, "res": 1080,
           "anim_theme": {"hue": 205, "sat": 0.85}, "font": "oswald", "shots": shots}
    json.dump(chj, open(os.path.join(FULL, "chapter", f"{ck}.json"), "w"), indent=1, ensure_ascii=False)
    json.dump({"chapter": ck, "cues": cues, "film_shots": film_shots, "generic_video_shots": generic_shots,
               "beds_hint": "projector loop under consecutive NARA film shots only (-27; never under the modern generic_video_shots, which get the bed of their scene: sea/waves for tows and storms, underwater for reef fish/divers, room tone for the lab); waves under sea photos/maps; underwater under hero sinking/cross-sections; drone under the fish-test gauges and the x-ray question blocks (-30)"},
              open(os.path.join(HERE, f"sfx_{ck}.json"), "w"), indent=1, ensure_ascii=False)
    all_chapters[ck] = (c0, cend, shots, cues)

# c01 = the approved hook: test v4's c01 shots verbatim, clips from test_v4/segments, ends at the chapter break
c1 = json.load(open(os.path.join(ROOT, "videos/oriskany/test_v4/chapter/c01.json")))
c1.update(title="Oriskany full · Hook (= approved test v4)", words="../build/words.json", audio_offset=0.0,
          clips_dir="../../test_v4/segments", duration=round(CH["c02"]["start"], 3), fade_out=0.0)
for s in c1["shots"]:
    if s.get("template") == "anim_xray" and s["params"].get("image", "").startswith("../assets/"):
        s["params"]["image"] = "../../test_v4/assets/" + s["params"]["image"][len("../assets/"):]
json.dump(c1, open(os.path.join(FULL, "chapter", "c01.json"), "w"), indent=1, ensure_ascii=False)
json.dump(segments, open(os.path.join(HERE, "segments.json"), "w"), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------------------------------------------------------ report
L = ["# Shot-list report (generated by build/make_shotlists.py)", ""]
tot = {"film": 0, "photo": 0, "map": 0, "hero": 0, "anim": 0, "card": 0}
FILMTOT = {}
L.append("| chapter | dur s | shots | film % | photo % | map % | hero % | anim % | card % | of which NARA film % | generic US-Gov film % | anim over moving film % | **moving video total %** | longest shot | cues/min |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for ck, (c0, cend, shots, cues) in all_chapters.items():
    d = {k: 0.0 for k in tot}
    ss = [r for r in report if r[0] == ck]
    nara = gen = undr = 0.0
    for _, sid, a, du, tpl, src, anc in ss:
        k = kind(src.split(" + bg ")[0]); bg = " + bg " in src
        key = {"F": "film", "G": "film", "P": "photo", "M": "map", "H": "hero", "A": "anim", "CARD": "card"}[k]
        if key == "card" and bg: key = "film"          # the card's text now sits over moving film (lower-third / number layout)
        if ck == "c07" and src == "M:c07_endscreen": du = max(0.0, du - END_SCREEN)
        d[key] += du
        if k == "F": nara += du
        if k == "G" or (k == "CARD" and bg): gen += du
        if k == "A" and bg: undr += du
    T = sum(d.values()); [tot.__setitem__(k, tot[k] + d[k]) for k in d]
    lg = max(ss, key=lambda r: r[3] if r[5] != "M:c07_endscreen" else 0)
    FILMTOT[ck] = (T, nara, gen, undr)
    L.append(f"| {ck} | {cend - c0:.1f} | {len(ss)} | " + " | ".join(f"{100 * d[k] / T:.0f}" for k in tot)
             + f" | {100 * nara / T:.0f} | {100 * gen / T:.0f} | {100 * undr / T:.0f} | **{100 * (nara + gen + undr) / T:.0f}** | {lg[3]:.1f} s ({lg[1]}) | {len(cues) / ((cend - c0) / 60):.1f} |")
T = sum(tot.values())
_n, _g, _u = (sum(v[i] for v in FILMTOT.values()) for i in (1, 2, 3))
L.append(f"| **c02-c07** | | | " + " | ".join(f"**{100 * tot[k] / T:.0f}**" for k in tot) + f" | **{100 * _n / T:.0f}** | **{100 * _g / T:.0f}** | **{100 * _u / T:.0f}** | **{100 * (_n + _g + _u) / T:.0f}** | | |")
L += ["", "## Pacing flags (shots > 6.0 s or < 1.2 s; end screen excluded)", ""]
for r in report:
    if (r[3] > 6.0 and r[5] != "M:c07_endscreen") or r[3] < 1.2: L.append(f"- {r[0]} {r[1]} {r[3]} s {r[4]} {r[5]} ('{r[6]}')")
L += ["", "## Clip / photo reuse (rule: at most twice, 3+ min apart; hook uses counted from test v4)", ""]
HOOK_USES = {"b3_a4_catapult_1966.mp4": [6.4], "b3_island_34_1966.mp4": [8.0], "b2_oriskany_at_anchor_1952.mp4": [32.7], "b10_ssus_stacks.mp4": [39.6],
             "b10_ssus_underway_side.mp4": [41.6], "b10_ssus_profile.mp4": [43.7], "6698617": [4.3], "6698627": [10.0], "6698576": [11.5],
             "6698573": [13.8], "6698609": [16.0], "6698619": [17.7], "6698610": [18.4], "6698611": [18.4], "6698612": [18.4], "6698624": [19.9],
             "6698626": [20.6], "6698569": [21.3], "6698553": [23.8]}
for k_ in sorted(set(uses) | set(HOOK_USES)):
    allt = sorted(HOOK_USES.get(k_, []) + uses.get(k_, []))
    bad = len(allt) > 2 or any(b - a < 180 for a, b in zip(allt, allt[1:]))
    if bad: L.append(f"- **{k_}** used at {', '.join(f'{t:.0f}s' for t in allt)}")
REELS = {}
for k_, ts in uses.items():
    if k_.startswith("g_") and k_ in FW: REELS.setdefault(FW[k_]["reel"], []).extend((t, k_) for t in ts)
L += ["", "## Generic reels with more than one use (v2 rule for the DVIDS hull reels: at most 2 uses per reel, 3+ min apart)", ""]
for r_, ts in sorted(REELS.items()):
    ts = sorted(ts)
    if len(ts) > 1: L.append(f"- {r_}: " + ", ".join(f"{t:.0f}s {c}" for t, c in ts) + ("  **CHECK**" if r_ in ("dvids_828554", "dvids_791060") and (len(ts) > 2 or any(y[0] - x[0] < 180 for x, y in zip(ts, ts[1:]))) else ""))
L += ["", "## All shots", "", "| ch | shot | start (abs s) | dur | template | source | cut on |", "|---|---|---|---|---|---|---|"]
L += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |" for r in report]
open(os.path.join(HERE, "shotlist_report.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L[:14]))
print(len(report), "shots c02-c07;", len(segments), "segments")
