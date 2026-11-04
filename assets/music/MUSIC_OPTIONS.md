# Music options: Ship Channel (own sound, not the battle-maps bed)

Checked 2026-11-04. The owner rejected the test video's music because "Long Note One" (Kevin MacLeod) is the battle-maps
channel's bed. The aim here is a separate musical identity: dark, cinematic, oceanic, tension plus melancholy, with no
vocals and no busy lead melody, so it sits under narration.

**Preview reel:** `assets/music/MUSIC_PREVIEW.mp3` (3:01, 128 kbps, 2.9 MB). It has 25 s of each candidate below, with a 1 s gap
between them. Each excerpt is levelled to -16 LUFS so they can be compared fairly. The excerpts are taken from the body of
each track, not the intro.
Reel order and start times: #1 0:00 · #2 0:26 · #3 0:52 · #4 1:18 · #5 1:44 · #6 2:10 · #7 2:36.

The full tracks are in `assets/music/candidates/`, which is local only. That folder is excluded through
`.git/info/exclude` and is never committed.

## Excluded because the other channels already use them

These tracks appear in battle-maps CREDITS.md, make_music_bed.py, check_sound_lock.py or the Epidemic CATALOG, or in
prehistory-channel. They must not repeat here:

- **Kevin MacLeod:** Long Note One, Long Note Two, Wounded, Anguish, Crusade, Killing Time, The Pyre, Clash Defiant,
  Fife and Drum, Heavy Heart, Ready Aim Fire, Undaunted, Darkest Child, Five Armies, Heroic Age, Dark Walk.
- **Epidemic Sound:** The Great War (Jon Björk), Five Minutes Out (John Utah).
- **prehistory-channel:** all of its music is synthesised. There is no third-party music to avoid.

## Candidates

| # | Title | Artist | License (quoted from source page) | Source URL | Mood | Where it fits | Content ID risk | Downloaded? |
|---|---|---|---|---|---|---|---|---|
| 1 | Stories About the World That Once Was (6:55), from *Music from Neptune Flux* (2016) | Chris Zabriskie | "All of my music is free to use in creative projects under the Creative Commons Attribution 4.0 license. Credit is required for free use." / "Can I use your songs in a video I make money from? Yes." | https://chriszabriskie.com/neptuneflux/ (license: https://chriszabriskie.com/use/) | Slow, low synth swells, dark and elegiac. Very few onsets (about 11/min), steady level. | **Main theme / hook bed**, and under long narrative stretches. It is long enough not to need looping. | **Low.** The artist says: "If you receive a copyright claim on my music, it did not come from me." He is published through ASCAP, which collects performance royalties and is not a Content ID registration. | Yes |
| 2 | That Hopeful Future Is All I've Ever Known (3:39), *Neptune Flux* | Chris Zabriskie | same as #1 | https://chriszabriskie.com/neptuneflux/ | Low sustained pads, almost no attack (about 5 onsets/min). Bittersweet. | **Reveal**: the answer to "what happened to it", and calm-after-the-sinking beats | Low (same as #1) | Yes |
| 3 | Your Mother's Daughter (3:34), *Neptune Flux* | Chris Zabriskie | same as #1 | https://chriszabriskie.com/neptuneflux/ | Steady low pulse (about 177 onsets/min) at an even level. Ticking-clock tension, low in the spectrum, so it stays out of the voice band. | **Tension**: the attack, the fire, damage control | Low (same as #1) | Yes |
| 4 | To Hide Their Secrets (3:14), *Neptune Flux* | Chris Zabriskie | same as #1 | https://chriszabriskie.com/neptuneflux/ | Starts quiet and rhythmic, then builds roughly 10 dB to a loud final minute. | **Mid-video reversal / build** into a big moment. Use the last minute only under a short narration gap. | Low (same as #1) | Yes |
| 5 | Abyss (2:14), from *Library Music Vol 1* | Rafael Archangel | "Abyss by Rafael Archangel is licensed under a CC0 1.0 Universal License" | https://freemusicarchive.org/music/Rafael_Archangel/Library_Music_Vol1/Rafael_Archangel_-_Library_Music_Vol1_-_05_Abyss/ | Dark rhythmic pulse at a flat level. Short and loopable. | **Tension**: alternate or second tension cue | Low. It is CC0, and no Content ID statement was found on the artist page. | Yes (FMA stream copy. FMA "download" needs a login, so the owner should re-download the full-quality file while logged in) |
| 6 | Living Shipwreck (3:38), from *Underwater Wonders* | John Bartmann | "Living Shipwreck by John Bartmann is licensed under a CC0 1.0 Universal License" | https://freemusicarchive.org/music/John_Bartmann/underwater-wonders/living-shipwreck/ | Underwater-documentary bed, low and calm (about 13 onsets/min), mildly mysterious. | **Wreck-today / dive footage**, sea-floor map scenes | Low. It is CC0, and no Content ID statement was found. Keep the FMA page URL as proof. | Yes (FMA stream copy, same note as #5) |
| 7 | I Should Have Been More Human (3:44), *Neptune Flux* | Chris Zabriskie | same as #1 | https://chriszabriskie.com/neptuneflux/ | Sparse, melancholy, slowly resolving | **Outro / closing question** (the ≤ 45 s ending) | Low (same as #1) | Yes |
| 8 | Hidden Abyss (8:50), from *Mnemonic Crystal* | Robert Coulombe | "Hidden Abyss by Robert Coulombe is licensed under a Attribution 4.0 International License" | https://freemusicarchive.org/music/robert-coulombe/mnemonic-crystal/hidden-abyss/ | Long dark ambient piece, but noticeably brighter than the others (median spectral centroid about 1.5 kHz) | Spare long bed only. It may compete with the voice. | Low. No statement found. | Yes, but **not in the reel**: the reel had to stay under 3 MB, and this was the weakest fit |

All Zabriskie audio was downloaded from the artist's own player files at
`https://audio.chriszabriskie.com/neptuneflux/neptuneflux-NN.m4a`, where NN is the track number on the album.
The full album is on Bandcamp at https://chriszabriskie.bandcamp.com/album/music-from-neptune-flux, as pay-what-you-want,
for the original files.

### Considered and rejected

- **Scott Buckley (CC BY 4.0).** His library is now in a "Smart Content ID" system: "This system scans the description of videos
  using my music looking for a credit. If no credit is found, the system places a copyright claim on the video" (claims
  come from "We Are Era Music BV"). It is registered with Content ID, so it fails the brief.
- **Kevin MacLeod, unused tracks** such as Shadowlands 1 - Horizon, Drums of the Deep and Stay the Course. They were downloaded
  locally to `candidates/macleod/` but are not recommended. incompetech now says the music is "pre-registered" in YouTube
  Content ID, and that claims follow when the credit is missing. That fails the "never registered with Content ID" rule.
  MacLeod is also the battle-maps sound, which works against a separate identity.
- **FMA tracks found but licensed NC, ND or NC-SA**, so they are not allowed: Scanglobe *Submarine* album (CC BY-NC-SA),
  Crowander "Underwater" (BY-NC), Filmy Ghost "Shipwreck on Klein Curacao" (BY-NC-ND), Marc Burt "Deep Sea" (BY-NC),
  the silence industry (BY-NC-SA), Blue Dot Sessions (NC).

## Recommendation

Using one album for most cues gives the channel a single recognisable sound. *Music from Neptune Flux* is a score about
drowned, lost worlds, which suits the theme.

- **Main theme:** #1 "Stories About the World That Once Was" by Chris Zabriskie (hook and main narrative bed).
- **Tension:** #3 "Your Mother's Daughter" by Chris Zabriskie. #4 "To Hide Their Secrets" is the build into the reversal, and
  #5 "Abyss" (CC0) is a second tension cue.
- **Outro:** #7 "I Should Have Been More Human" by Chris Zabriskie (closing question and end screen). #2 is for the reveal.

These picks are based on objective analysis of the audio: loudness profile, onset density and spectral balance. The owner
should confirm them by ear with the preview reel before `make_music_bed.py` is pointed at the new tracks.

**Description credit**, one line per track used:

```
"Stories About the World That Once Was" by Chris Zabriskie, from the album Music from Neptune Flux.
Licensed under Creative Commons Attribution 4.0 (creativecommons.org/licenses/by/4.0/). chriszabriskie.com
```

CC0 tracks need no credit, but list them anyway in `CREDITS.md` with the FMA URL as proof of license.

## If the Epidemic Sound subscription is active

These are suggestions from the Epidemic catalog. None of them overlap with the two battle-maps tracks in
`battle-maps/library/epidemic/CATALOG.md`. The owner downloads them in Epidemic with the channel connected, then adds them to
the catalog. Never commit them, because the repo is public. They are safe only while the subscription is active.

| Title | Artist | Epidemic id | Length | Tags | Use |
|---|---|---|---|---|---|
| Exit Fade | DEX 1200 | 6b945918-3ef0-4793-88bb-f0a670a24b72 | 4:09 | ambient, cinematic, dark, mysterious, no vocals | main bed |
| Signs | Lennon Hutton | e67ca2b6-04bf-46f6-9a43-8d3b9e323406 | 3:42 | dark ambient, cinematic, pulses, suspense, no vocals | tension |
| Shadows Unseen | DEX 1200 | 05eb720b-c5de-4a7f-b56b-42db86d273ce | 4:28 | ambient, cinematic, dark, mysterious, no vocals | reveal / outro |
