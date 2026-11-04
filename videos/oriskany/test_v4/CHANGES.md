# Test v4: FIX_LIST status (test_v3/FIX_LIST.md)

| # | Item | Status | How |
|---|---|---|---|
| 1 | Master stage (voice comp/limit, linear-only loudnorm, stereo, pad, fade) | DONE | tools/sound/mix_clip.py v2 via build/mix.py: -13.9 LUFS, -1.5 dBTP, LRA 5.8, loudnorm linear, stereo, audio = video length, 0.6 s fade |
| 2 | Music audible at the battle-maps level | DONE | music -22.0 dB under voice, -19.7 dB in gaps (battle-maps refs -17.3; delta -0.8 dB) |
| 3 | Sync (explosion / flood / catapult late; 37 on its word) | DONE | every cue on its event frame, 16/16 within 3 frames; the A-4 does not launch in f03, so no jet sound; 37 count ends on "thirty-seven" (land_at), the montage starts before the word |
| 4 | Real recordings, no synthesized SFX | DONE | Epidemic only (md5-checked by check_sound_lock); horn / ship roles still need the owner's ear |
| 5 | Dead 30-40 s, low end | DONE | drone bed 29.6-39.6, underwater bed under the sinking; HPF on beds/music, shelf on SFX |
| 6 | Hook rebuilt: map frame 0, stakes line, blast by ~3 s held 2+ s, title promise by ~10 s | MOSTLY | frame 0 = clean map; "Right now, two hundred and twelve feet under the Gulf of Mexico"; blast photo at 4.30 (held 2.1 s, explosion +4.6 LU); "The United States Navy did. On purpose." at 8.0-10.4. The blast lands at 4.3 s, not ~3 s: the stakes line takes 4.1 s to say |
| 7 | Say "SS United States" | DONE | spoken at 42.1 s, name plate on the word |
| 8 | No "for the very same reason" | DONE | HOOK_v1 wording |
| 9 | Wrong-era shots | DONE | the only 1960s film in the hook is under "No enemy sank her" / "The United States Navy did" (the ship herself, OFF VIETNAM 1966 label); "3+ years" over the 2006 flight-deck cutting photo; 1952 film only under "buried in her past", no date label; no DECOMMISSIONED card |
| 10 | Sinking animation depths / gauge | DONE | kit sinking v2 (deck ~147 ft, island 84 ft, seabed 212 ft); gauge AT THE SURFACE 0 FT -> FLIGHT DECK DEPTH -> ON THE SEABED 212 FT; touchdown on "floor" (28.70) |
| 11 | Options board / unspoken lines | DONE | HOOK_v1 holds the answer: "Why not?" + "Keep her?" / "Scrap her?" on their words, no box, no strike; no "$3 million" subline; no unspoken title |
| 12 | Clean-up (seam, ghosting cut, blob, burn glitch, X-ray empty frame, "1 minutes") | DONE | films fill the frame (no blurred-bg seam); check_clips on every segment: no internal cuts (the "13" plane is cut out of the island clip); BLOB flags are the subject (liner hull, dark interior, sea), FLASH flags are the designed blast flashes; X-ray starts with the ship (first_frame full); counter unit hidden until >= 2 |
| 13 | Labels >= 3.5 %, above the player bar; one grade | DONE | check_safe_text.js PASS (50.2 s every 0.5 s); ARCHIVE_GRADE=ship on every photo and film |
| 14 | Voice: question block slower, no rushed long lines, pauses, pronunciation | DONE | question block at speed 0.88; Oriskany voiced with exact phonemes ɔːɹˈɪskəni (Kokoro default was OR-iss-kuh-nee); 0.55 s pause after "Oriskany." for the second blast. Longest sentence is 15 words ("On November twelfth...") at ~150 wpm |
| 15 | MANIFEST + CREDITS (used items only, no URLs) | DONE | tools/film/make_paperwork.py -> MANIFEST.md (6 film clips), CREDITS.md |
| 16 | "This month" timing | DONE | HOOK_v1 says "On November twelfth": true for any publish date up to Nov 11 |

Not met: moving film is 24 % of screen time (stills 36 %, maps/animation 40 %). Every 2006 event (charges, sinking, prep, tow) exists only as Navy stills; more film would mean 1960s footage under 2006 narration (FIX 9 forbids it).
