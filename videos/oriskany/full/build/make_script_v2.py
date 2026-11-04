"""SCRIPT_v2 / NARRATION_v2 = v1 with chapter-2 cuts only (no new facts), to pull the mid-video reversal earlier
(script agent's own flag: v1 reversal at ~67 %). Each cut is (exact v1 text in SCRIPT, exact v1 text in NARRATION, new text)."""
import os, re
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../script")
sc = open(os.path.join(S, "SCRIPT_v1.md")).read(); na = open(os.path.join(S, "NARRATION_v1.txt")).read()
CUTS = [
 # 1. the 1953 deck-bomb paragraph (+ its visual note) -- whole paragraph
 ("Not every danger came from the enemy. On the sixth of March, nineteen fifty-three, a bomb hung up on a landing Corsair. [FC-A B5] It broke loose and exploded on her deck. [FC-A B5] It killed two sailors and wounded more than a dozen. [FC-A B5; safe 14]\n\n> [CARD: date line 6 MAR 1953 on \"sixth of March\"] → [FILM: 428-NPC-9584 F4U Corsair lands, FOOT b2 #2] → [FILM: 428-NPC-9584 a bomb shakes loose from a landing F4U and explodes, FOOT b2 #3 (NARA undated: caption \"ORISKANY, EARLY 1950s\", never \"6 March 1953\"; trim the over-exposed head; no casualties shown)] → [CARD: \"2 KILLED\" on \"two sailors\"].\n\n",
  "Not every danger came from the enemy. On the sixth of March, nineteen fifty-three, a bomb hung up on a landing Corsair. It broke loose and exploded on her deck. It killed two sailors and wounded more than a dozen.\n\n", ""),
 # 2. MiG fight: drop the "officially two shot down" sentence; "credited with one" -> "one MiG" (same fact)
 (" Officially, two MiGs were shot down and two damaged. [FC-A B2]", " Officially, two MiGs were shot down and two damaged.", ""),
 ("was credited with one at the time.", "was credited with one at the time.", "was credited with one MiG at the time."),
 # 3. Vietnam: drop the tonnage sentence
 (" She dropped nearly ten thousand tons of ordnance. [FC-A C2]", " She dropped nearly ten thousand tons of ordnance.", ""),
 (" → [FILM: A-4E bombs on the wing, FOOT b3 #9] → [CARD: \"10,000 TONS\" on \"ten thousand\"]", None, " → [FILM: A-4E bombs on the wing, FOOT b3 #9]"),
 # 4. Stockdale: drop the Medal of Honor sentence
 (" In nineteen seventy-six, he received the Medal of Honor. [FC-A C1c, safe 7]", " In nineteen seventy-six, he received the Medal of Honor.", ""),
 # 5. 1967: drop the Forrestal sentence (and its map beat)
 (" That July, the carrier Forrestal caught fire nearby, and the Oriskany sent help. [FC-A C14]", " That July, the carrier Forrestal caught fire nearby, and the Oriskany sent help.", ""),
 (" → [MAP: Forrestal pin on \"Forrestal\", date line 29 JUL 1967 (no Forrestal footage in our list)]", None, ""),
 # 6. McCain: drop the 23rd-mission sentence
 (" It was his twenty-third mission, and his first over Hanoi. [FC-A C12c]", " It was his twenty-third mission, and his first over Hanoi.", ""),
 # 7. air-wing losses paragraph (+ visual note)
 ("On that tour, her air wing lost about half its planes. [FC-A C15] Twenty pilots were killed, and nine were captured. [FC-A C15]\n\n> [ANIM: grid of aircraft icons, half fade on \"half\"; CARD \"20 KILLED · 9 CAPTURED\" on the words] over [FILM: crowded deck, FOOT b3 #10, dimmed].\n\n",
  "On that tour, her air wing lost about half its planes. Twenty pilots were killed, and nine were captured.\n\n", ""),
 # 8. homecoming: drop the March 1976 sentence
 ("She came home from her last deployment in March nineteen seventy-six. [FC-A D0] ", "She came home from her last deployment in March nineteen seventy-six. ", ""),
]
for a, b, new in CUTS:
    assert sc.count(a) == 1, ("script", a[:60]); sc = sc.replace(a, new)
    if b is not None:
        if new and b == a: pass
        nb = new if not new.startswith(" →") else ""
        if a.startswith("was credited"): nb = new
        assert na.count(b) == 1, ("narr", b[:60]); na = na.replace(b, nb)
sc = sc.replace("# SCRIPT v1:", "# SCRIPT v2:", 1)
sc = sc.replace("## How to read this file", "## v2 changes (2026-11-04)\nChapter-2 cuts only, no new facts, to pull the reversal earlier: the 1953 deck-bomb paragraph, the \"officially two\nMiGs\" sentence, the ordnance tonnage, Stockdale's Medal of Honor line, the Forrestal sentence, McCain's 23rd mission,\nthe 1967 air-wing losses, and the March 1976 homecoming line. Chapter times below are v1 estimates; the real times\nare in `../full/chapters.json` (from the voice take).\n\n## How to read this file", 1)
open(os.path.join(S, "SCRIPT_v2.md"), "w").write(sc); open(os.path.join(S, "NARRATION_v2.txt"), "w").write(na)
paras = [p for p in na.split("\n\n") if p.strip()]
tot = sum(len(p.split()) for p in paras); c = 0
for p in paras:
    if p.startswith("It looked like the perfect ending") or p.startswith("Not all of the PCBs"): print(p[:40], c, round(c / tot * 100, 1))
    c += len(p.split())
print("words", tot)
