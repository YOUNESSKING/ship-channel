"""v3 NEW SOUND: cues from the visual event frames (shot start + offset, chapter/c01.json), real Epidemic recordings
(tools/sound/sfx_mix_lib.py v2). Event offsets are the frames the critic measured (CRITIQUE_SOUND_ACCURACY section 2).
Critic sync fixes applied: explosion peak on the blast cut and trimmed to 0.9 s, flood rush ends at the a08b cut
(bubbles take over on the boil), catapult jet peaks while the A-4 passes and ends at the v12 cut, the redundant 19.31 hit
is gone, the slam moves to the ON PURPOSE flash cut, the horn is audible on the SS United States cut, the dead 30-40 s
stretch gets the drone bed. (The "37" counter landing late is a picture fix: the pop sits on the frame where 37 lands.)
Writes audio/sfx_v2.wav, audio/punch_v2.wav (unducked big beats), audio/beds_v2.wav, build/sfx_placed_v2.json."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
sys.path.insert(0, os.path.join(ROOT, "tools/sound"))
import sfx_mix_lib as L
W = json.load(open(os.path.join(HERE, "words.json")))
CH = json.load(open(os.path.join(HERE, "../chapter/c01.json")))
SHOTS = L.shot_table(CH, W)
TOTAL = float(CH["duration"])
C = lambda shot, at, role, note, **k: dict(shot=shot, at=at, role=role, note=note, **k)
CUES = [
 C("a01", 0.40, "boom", "MAY 17, 2006 card first visible (hook stamp)", len=1.2),
 C("a02", 0.00, "whoosh", "map dive cut (biggest move #1)"),
 C("a03b", 0.00, "explosion", "first charge: water plume photo cut (sequence 1/2)", file="charges_c__f6f10ea4.wav", src=0.07, len=0.6),
 C("a04", 0.00, "explosion", "main blast photo + white flash (sequence 2/2), trimmed 0.9 s", file="charges_c__f6f10ea4.wav", len=0.9, tail=0.25),
 C("a06", 0.99, "pop", "37 reached on screen (13.20)"),
 C("a07", 0.00, "impact", "bow-high photo: hull going under (water impact)", file="splash_a__1d6949d6.wav", tail=0.3, end_shot="a07"),
 C("a08", 0.00, "ship", "flood rush as she slips under (ends at the a08b cut)", file="flood_a__db95b348.wav", tail=0.15),
 C("a08b", 0.00, "ship", "boil photo: air bursting out (bubbles)", file="bubbles_a__e58b390c.wav"),
 C("v10", 0.40, "pop", "ABOUT 900 FT first visible (15.70)"),
 C("a09", 0.15, "ship", "hero: hull groan as the drawn carrier goes down (until touchdown)", file="groan_a__7c63fd7c.wav", len=1.75, tail=0.0),
 C("a09", 1.77, "impact", "hero: hull touches the seabed 19.27 (underwater thump)", file="charges_b__0ecb5c38.wav", len=1.2),
 C("a09", 1.77, "boom", "seabed touchdown: cinematic boom layer under the thump (key beat)", len=1.2),
 C("v12", 0.65, "jet", "A-4 shoots past the camera 21.00-21.40, ends at the v12 cut", file="jet_a__9fc48bf0.wav", src=3.55, tail=0.1),
 C("a12", 0.00, "boom", "ON PURPOSE. flash cut 24.33", len=1.4),
 C("a13", 0.29, "pop", "3 YEARS first visible (26.30)"),
 C("a14", 0.20, "pop", "$20 MILLION first visible (27.75)"),
 C("a17", 4.49, "pop", "KEEP HER struck through (40.37)"),
 C("a17", 4.95, "boom", "gold box lands on SINK HER (40.83)", len=1.0, tail=0.12),
 C("a19", 0.00, "riser", "reverse riser INTO the x-ray reveal (peaks on the a19 cut)", lead=True),
 C("v23a", 0.00, "horn", "SS United States on screen: liner horn (signature), over the SS United States shots",
   end_shot="v23b", tail=0.0),
 C("a20", 0.00, "whoosh", "end map pull-back (biggest move #2)", file="whoosh_a__689b1489.wav"),
 C("a20", 2.10, "boom", "THE SAME REASON stamp visible (51.40)", len=1.4),
]
FILM = ["v06", "v07", "v10", "v12", "v13", "a13", "v18", "v19", "v21", "v23a", "v23b", "v23c"]
B = lambda role, shot, note, **k: dict(role=role, shot=shot, note=note, **k)
BEDS = [B("waves", "a01", "Gulf of Mexico: sea bed under the opening photo + map dive", end_shot="a02", fade=0.8),
        B("underwater", "a09", "hero sinking: underwater ambience", fade=0.5, src=2.0),
        B("drone", "a15", "the question block (was dead air 30-40 s): low tension drone", end_shot="a17", fade=1.0, src=6.0),
        B("waves", "a20", "end map: sea bed", fade=0.8, src=30.0)]
_merged = []
for s in FILM:   # projector loop under every archive-film shot; consecutive film shots share one loop
    if _merged and _merged[-1]["end_shot"] == SHOTS[[x[0] for x in SHOTS].index(s) - 1][0]:
        _merged[-1]["end_shot"] = s
    else:
        _merged.append(B("projector", s, "projector loop under archive film", end_shot=s, fade=0.15))
BEDS += _merged

if __name__ == "__main__":
    A = os.path.join(HERE, "../audio")
    placed, pb = L.render(CUES, SHOTS, TOTAL, os.path.join(A, "sfx_v2.wav"), BEDS, os.path.join(A, "beds_v2.wav"),
                          punch_out=os.path.join(A, "punch_v2.wav"))
    json.dump({"cues": placed, "beds": pb, "shots": SHOTS}, open(os.path.join(HERE, "sfx_placed_v2.json"), "w"), indent=1)
    for p in placed:
        print(f"{p['event']:6.2f} {p['role']:9s} {p['level_db']:6.1f} dB {p['file']:26s} {p['start']:6.2f}-{p['end']:6.2f}"
              f" sync({p['sync']}) {p['offset_frames']:+5.1f} f  {p['note']}")
    for b in pb: print(f"  bed {b['role']:10s} {b['start']:6.2f}-{b['end']:6.2f} {b['level_db']} dB {b['file']}")
    print(len(placed), "cues,", round(len(placed) / TOTAL * 60, 1), "per minute")
