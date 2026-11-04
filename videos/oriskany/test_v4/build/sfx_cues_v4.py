"""v4 sound cues: every cue sits on the frame of its visual event (shot start + offset from chapter/c01.json), real Epidemic
recordings only (tools/sound/sfx_mix_lib.py v2, STYLE_LOCK role levels). No sound without its picture: the A-4 stays on the
catapult in f03, so no jet; the horn plays on the SS United States cut. Writes audio/sfx.wav, audio/punch.wav, audio/beds.wav,
build/sfx_placed.json."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
sys.path.insert(0, os.path.join(ROOT, "tools/sound"))
import sfx_mix_lib as L
W = json.load(open(os.path.join(HERE, "words.json")))
CH = json.load(open(os.path.join(HERE, "../chapter/c01.json")))
SHOTS = L.shot_table(CH, W)
TOTAL = float(CH["duration"])
word = lambda txt, after=0.0: next(x["start"] for x in W if x["start"] >= after - 1e-6 and x["w"].lower().strip(",.?").startswith(txt))
st = {s[0]: s[1] for s in SHOTS}
off = lambda shot, t: round(t - st[shot], 3)   # absolute narration time -> offset in the shot
C = lambda shot, at, role, note, **k: dict(shot=shot, at=at, role=role, note=note, **k)
CUES = [
 C("s01", 0.35, "whoosh", "map dive starts moving (biggest move #1)", file="whoosh_a__689b1489.wav"),
 C("s01", off("s01", word("feet", 2.0)), "hit", "212 FT card lands on 'feet'", len=1.2),
 C("s02", 0.00, "explosion", "WOW 1: blast photo cut + white flash + shake", file="charges_c__f6f10ea4.wav", src=1.76, len=1.2, tail=0.3),
 C("s05", off("s05", word("purpose", 10.0)), "boom", "ON PURPOSE. lands on 'purpose'", len=1.3),
 C("s09", 0.00, "explosion", "second blast photo + flash (smoke, in the voice gap)", file="charges_a__955e7371.wav", src=17.24, len=0.33, tail=0.25),
 C("s10", off("s10", word("seven", 18.0) + 0.15), "pop", "37 lands (count ends on 'thirty-seven')"),
 C("s11", 0.00, "impact", "bow standing vertical: water closing over the hull", file="splash_a__1d6949d6.wav", tail=0.15),
 C("s11", 0.05, "ship", "flood rush as the bow slips under (to the foam cut)", file="flood_a__db95b348.wav", tail=0.1),
 C("s11b", 0.00, "ship", "only foam left: air bursting out", file="bubbles_a__e58b390c.wav", tail=0.15),
 C("s12", off("s12", word("three", 22.0)), "pop", "3+ YEARS lands on 'three'"),
 C("s14", 0.25, "ship", "drawn carrier going down: hull groan (until touchdown)", file="groan_a__7c63fd7c.wav", len=2.4, tail=0.0),
 C("s14", 2.70, "impact", "hull touches the seabed on 'floor' (underwater thump)", file="charges_b__0ecb5c38.wav", len=1.0),
 C("s17", 0.00, "riser", "reverse riser INTO the x-ray reveal (peaks on the cut)", lead=True),
 C("s19", 0.00, "horn", "SS United States on screen: liner horn (signature sound)", end_shot="s20", tail=0.0),
 C("s21", 0.00, "whoosh", "end map pull-back (biggest move #2)", file="whoosh_b__8d9712d2.wav"),
]
# density (SOUND_DESIGN_V02 ~16/min): small pops on 22 / $20 / 13 / ? and the two option ticks are left out on purpose
FILM = ["s03", "s04", "s16", "s19", "s20", "s20b"]
B = lambda role, shot, note, **k: dict(role=role, shot=shot, note=note, **k)
BEDS = [B("waves", "s01", "Gulf of Mexico: sea under the map dive", end_shot="s01", fade=0.6),
        B("waves", "s05", "foam / sea photos of the sinking day", end_shot="s11b", fade=0.5, src=12.0),
        B("underwater", "s14", "drawn sinking: underwater ambience", end_shot="s15", fade=0.5, src=2.0),
        B("drone", "s15", "the question block: low tension drone", end_shot="s18", fade=1.0, src=6.0),
        B("waves", "s21", "end map: sea", fade=0.8, src=30.0)]
_m = []
order = [s[0] for s in SHOTS]
for s in FILM:   # projector loop under archive film; consecutive film shots share one loop
    if _m and order.index(_m[-1]["end_shot"]) == order.index(s) - 1: _m[-1]["end_shot"] = s
    else: _m.append(B("projector", s, "projector loop under archive film", end_shot=s, fade=0.15))
BEDS += _m
if __name__ == "__main__":
    A = os.path.join(HERE, "../audio"); os.makedirs(A, exist_ok=True)
    placed, pb = L.render(CUES, SHOTS, TOTAL, os.path.join(A, "sfx.wav"), BEDS, os.path.join(A, "beds.wav"), punch_out=os.path.join(A, "punch.wav"))
    json.dump({"cues": placed, "beds": pb, "shots": SHOTS}, open(os.path.join(HERE, "sfx_placed.json"), "w"), indent=1)
    for p in placed:
        print(f"{p['event']:6.2f} {p['role']:9s} {p['level_db']:6.1f} dB {p['file']:26s} {p['start']:6.2f}-{p['end']:6.2f} sync({p['sync']}) {p['offset_frames']:+5.1f} f  {p['note']}")
    for b in pb: print(f"  bed {b['role']:10s} {b['start']:6.2f}-{b['end']:6.2f} {b['level_db']} dB {b['file']}")
    print(len(placed), "cues,", round(len(placed) / TOTAL * 60, 1), "per minute")
