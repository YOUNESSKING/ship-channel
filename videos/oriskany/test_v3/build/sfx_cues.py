"""v3 sound cues, generated from the word timings (build/words.json) and the shot timeline (chapter/c01.json):
every cue sits on the frame where its visual event happens. Roles/levels come from tools/sound/sfx_mix_lib.py
(battle-maps locked levels). Writes build/sfx_cues.json and audio/sfx.wav, prints the cue table."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
sys.path.insert(0, os.path.join(ROOT, "tools/sound"))
import sfx_mix_lib as L
W = json.load(open(os.path.join(HERE, "words.json"))); W = W["words"] if isinstance(W, dict) else W
CH = json.load(open(os.path.join(HERE, "../chapter/c01.json")))
w = lambda i: W[i]["start"]
def word(txt, after=0.0):   # first word at/after `after` whose text starts with txt
    return next(x["start"] for x in W if x["start"] >= after - 1e-6 and x["w"].lower().strip(",.?").startswith(txt))
def shot(sid):
    s = next(s for s in CH["shots"] if s["id"] == sid)["start"]
    return float(s) if isinstance(s, (int, float)) else (float(s[1:]) if s[0] == "t" else w(int(s[1:])))
HERO_LAND = 17.50 + 1.76   # kit ShipSink touchdown (landAt = (T_FEET - 0.05) / DUR) -> narration 19.26
CUES = [  # [t, role, what is on screen]
 [w(0),                "hit",       "MAY 17, 2006 card lands (number_at w0)"],
 [shot("a02"),         "whoosh",    "map dive from the Gulf to the reef (biggest move #1)"],
 [shot("a04"),         "explosion", "photo of the charges going off: flash + shake frame"],
 [shot("a06") + 1.15,  "hit",       "37 MINUTES count lands"],
 [shot("a07"),         "impact",    "bow-high photo: hull going under"],
 [shot("a08"),         "ship",      "flood rush as she slips under", "flood_rush_1.wav"],
 [word("nine", 15.0),  "hit",       "ABOUT 900 FT card lands"],
 [shot("a09") + 0.15,  "ship",      "hero: hull groan as the drawn carrier goes down", "hull_groan_1.wav"],
 [HERO_LAND,           "impact",    "hero: hull touches the seabed (silt + shake)"],
 [word("feet", 19.0),  "hit",       "depth gauge lands on 212 FT"],
 [shot("v12") + 0.45,  "jet",       "A-4 catapult launch passes the camera"],
 [word("purpose", 24),  "slam",      "ON PURPOSE. slam (flash cut)"],
 [word("three", 26),   "hit",       "3 YEARS card lands"],
 [word("twenty", 27),  "hit",       "$20 MILLION card lands"],
 [40.15,               "tick",      "KEEP HER struck through", "strike_scrape_1.wav"],
 [40.40,               "tick",      "SCRAP HER struck through", "strike_scrape_2.wav"],
 [40.65,               "hit",       "gold box lands on SINK HER"],
 [word("hidden", 42),  "tick",      "x-ray: ??? glows inside the hull", "sonar_ping_1.wav"],
 [shot("v23a") + 0.5,  "ship",      "SS United States on screen: liner horn (funnels smoking)", "horn_distant_1.wav", 3.5],
 [shot("a20"),         "whoosh",    "end map pull-back (biggest move #2)"],
 [word("reason", 51),  "hit",       "THE SAME REASON stamp lands"],
]
total = float(CH["duration"])
placed = L.render(CUES, total, os.path.join(HERE, "../audio/sfx.wav"))
json.dump(CUES, open(os.path.join(HERE, "sfx_cues.json"), "w"), indent=1)
json.dump(placed, open(os.path.join(HERE, "sfx_placed.json"), "w"), indent=1)
for p in placed: print(f"{p[0]:7.2f}  {p[1]:9s} {p[3]:6.1f} dB  {p[2]:24s} {p[4]}")
print(len(placed), "cues,", round(len(placed) / total * 60, 1), "per minute")
