# Credits: Oriskany test v2

## Photos (public domain, U.S. Government works; National Archives Catalog, U.S. Navy 2006 series)
| Shot | NARA ID | What it shows (NARA title, shortened) |
|---|---|---|
| p01_afloat | 6698606 | Decommissioned USS Oriskany (CV 34) before the sinking, May 2006 |
| p03_eod | 6698615 | USN Explosive Ordnance Disposal sailors on a patrol boat before the sinking, 17 May 2006 |
| p04_blast | 6698617 | Port side view of Oriskany as the explosive charges designed to sink her explode |
| p05_smoke / p05b_smoke2 | 6698618 / 6698619 | Oriskany after the charges, smoke rising |
| p06_list | 6698621 | Oriskany listing as she settles |
| p07_stern | 6698623 | One end of the carrier lifting as she goes down |
| p08_gone | 6698626 | The water where she went under |
| p12_slam | 6698624 | Oriskany going under (dimmed, behind "ON PURPOSE.") |
| p10_bw | 7578422 | "CVA 34 Oriskany" (1950s Navy photo) |
| p11_tow | 6698598 | Aerial view of Oriskany preparing to get underway after final preparations, Pensacola |
| p13_cut | 6698569 | Resolve Marine Group employee cutting holes in the flight deck during preparation |
| p14_sparks | 6698580 | Resolve Marine Group employee cutting away the anchor chain |
| p15_aerial | 6698599 | Aerial view of Oriskany under tow, May 2006 |
| p16_crowd | 6698586 | Media along the sea wall documenting the last voyage |
| p18_porthole | 6698555 | View inside Oriskany at NAS Pensacola during final preparations |
Source: https://catalog.archives.gov/id/<NARA ID>. Photos downloaded by the footage agent (videos/oriskany/footage/src/photos).

## Music
"Stories About the World That Once Was" by Chris Zabriskie, from the album Music from Neptune Flux.
Licensed under Creative Commons Attribution 4.0 (creativecommons.org/licenses/by/4.0/). chriszabriskie.com
(file: assets/music/candidates/zabriskie/neptuneflux-01.m4a; swappable via MUSIC=... in build/mix.py)

## Sound effects
All SFX are synthesized in-house for this channel (kit/ship/sfx, make_sfx.py). No credit needed. No battle-maps or
prehistory sound files are used.

## Narration
Kokoro TTS v1.0, voice am_michael (Apache 2.0 model). AI voice: tick YouTube's altered/synthetic content box.
Word timing: faster-whisper base.en alignment (MIT).

## Maps and graphics
Terrain & bathymetry: Mapzen / AWS Terrain Tiles (open data), baked with mk/tools/bake_sea.py.
Ship drawings: kit/ship (original line art). Map engine: map-kit (HyperFrames + GSAP). Cards/options/X-ray: templates/.
3D photo moves: Depth Anything V2 Small (Apache 2.0).
