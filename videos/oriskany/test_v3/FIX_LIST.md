# Oriskany: merged fix list from two independent critics (test v3)

Sources: CRITIQUE_VISUAL.md (story/visuals, overall 6/10) and CRITIQUE_SOUND_ACCURACY.md (sound/accuracy/rights).
Apply to v4 and the full video.

## A. Sound (biggest problem: the mix is flattened)
1. Master stage: the loudness pass silently switched to dynamic mode (+9.2 dB needed), so voice got ~8 dB of
   limiting and big beats are no louder than speech (LRA 2.0). Fix: compress/limit the voice stem before the mix
   (2.5:1 at -24 dB, limiter ~-9 dBFS), final -14 LUFS with the 2c-9 linear gain + alimiter 0.84; FAIL the build
   if loudnorm is not linear. Stereo master, pad audio to video length, 0.6 s fade-out.
2. Music is inaudible (27.5 dB under voice). Re-check the 0.08 level against the new voice level, so it sits
   where battle-maps' did.
3. Sync: explosion +73 frames late, flood rush +71 (masks "feet"), catapult +58 (no aircraft on screen).
   Trim to 0.9 / 1.2 / 1.25 s, 0.5 s voice pause after "charges", remove the 19.31 hit; "37" counter must land
   on the word (start 11.52, 0.7 s count).
4. SFX are all synthesized: battle-maps rules (STYLE_LOCK §7, 2c-5) forbid that. Use real recordings for
   charges, hull, catapult, horn (owner decision: Epidemic Sound or freesound CC0/CC BY). Horn, sonar, scrapes
   are inaudible (10-23 dB under voice).
5. Sound design vanishes 30-40 s; low end < 120 Hz as loud as the voice band: high-pass beds, fill the gap.

## B. Hook and story
6. Rebuild 0-8 s: frame 0 = map dive; stakes line first ("Right now, 212 feet under the Gulf of Mexico..."),
   blast by ~3 s held 2+ s, date moves onto the blast card, title promise paid before ~8 s.
7. Say "SS United States" in the narration.
8. Fix "for the very same reason" right after "hidden inside her" (sounds like PCBs; the shared reason is reefing).

## C. Picture
9. Wrong-era shots: no 1960s service film in the first 20 s; "3 years" goes over the 2006 prep stills
   (6698569, 6698555), not 1952 film; "1968" launch label → "1967-68" or no year; "DECOMMISSIONED 1976" not over
   1966 film.
10. Sinking animation 25 ft too shallow (flight deck ~145-150 ft, island top ~84 ft); gauge must read the
    seabed/hull correctly, not "32 FT" while floating.
11. Options board: highlight lands on "Sink her" and holds; no box on Keep/Scrap; spoken or remove
    "WHAT DO YOU DO WITH a carrier?"; drop or speak "budgeted at under $3 million" (say $2.8M if used).
12. Clean-up: compositing seam 10.0-10.3 s, f06 ghosting cut, blob over catapult clip ~21.3 s, film-burn glitch
    40.3 s, stray underline, empty black opening of the X-ray, "1 minutes" counter frame.
13. Labels ≥ 3.5% frame height and above YouTube's player bar; one colour grade for photos/film/maps.

## D. Voice
14. Kokoro: split the 13-word sentence, slow the question block (speed 0.88), remove two mid-sentence pauses,
    5-10 ms fades at chunk edges; test "Oriskany" and "Pensacola" pronunciation.

## E. Rights and paperwork
15. Write MANIFEST.md for every film clip (with what it does NOT show); add licence/author columns for film in
    CREDITS.md; remove unused items and the stale v2 note; credits without links (STYLE_LOCK 6).
16. Timing: "this month" only works if published by Nov 11, 2026; otherwise re-voice after Nov 12.

## Keep
- "No enemy sank her. The United States Navy did. On purpose." over the war film, then the slam card.
- The SS United States ending map (both reefs, 13 nmi apart).
- Numbers landing on their words; the to-scale cross-section idea.
- Loudness target met (-14.3 LUFS, -1.2 dBTP), no clipping, public-domain sourcing clean.
