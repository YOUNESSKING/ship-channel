#!/usr/bin/env python3
"""words_to_timing.py WORDS.json OUT.json  (NEW, not in the original kit)
Builds audio/timing.json in the kit's format from a word-level file ([{w,start,end},...], [bracket] tags skipped) for
human voice-over. Every WORD becomes a `sents` entry [charStart,t0,t1], so B.at(para, phrase) lands on the exact word.
Edit PARAS: (id, first word index, last word index, start override or None)."""
import json, sys, re
words = [x for x in json.load(open(sys.argv[1])) if not re.match(r"^\[.*\]$", x["w"])]
def find(t, nth=0):   # index of the word that starts at ~t
    return min(range(len(words)), key=lambda i: abs(words[i]["start"] - t))
PARAS = [  # (id, tag note, first word start time, last word start time, scene start override)
    ("iceage-1", "present coast -> -120 m coast, ice sheets grow", 13.008, 18.08, 13.0),
    ("iceage-2", "(next narration - only marks the end of the scene)", 19.04, 22.96, 19.0),
    ("natlantic-1", "push in to the North Atlantic, 20,000 years ago", 33.627, 37.52, 33.6),
    ("natlantic-2", "(next narration - only marks the end of the scene)", 38.32, 39.08, 38.3),
]
paras = []
for pid, note, a, b, t0 in PARAS:
    i, j = find(a), find(b)
    ws = words[i:j + 1]
    text, sents, c = "", [], 0
    for w in ws:
        sents.append([len(text), w["start"], w["end"]]); text += w["w"] + " "
    paras.append({"section": "ICE AGE", "tag": f"MAP: {pid} | {note}", "start": t0, "end": ws[-1]["end"], "text": text.strip(), "sents": sents})
json.dump({"voice": "human", "speed": 1.0, "duration": words[-1]["end"] + 1, "paragraphs": paras}, open(sys.argv[2], "w"), indent=1)
for p in paras: print(p["tag"][:20], p["start"], round(p["end"], 2), p["text"])
