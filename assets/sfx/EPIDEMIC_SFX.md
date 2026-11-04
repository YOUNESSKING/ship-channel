# Epidemic Sound SFX catalog (ship channel)

The audio files live in `assets/sfx/epidemic/` and are **git-ignored**: they are licensed to the owner's Epidemic
Sound subscription and must never be committed. This catalog lets you download them again.

**Re-download.** Use the Epidemic Sound MCP tool `DownloadSoundEffect(id, {fileType: "WAV"})`. It returns a
signed URL. Fetch it with `curl`, then convert the file:
`ffmpeg -i in.wav -ar 48000 -c:a pcm_s24le assets/sfx/epidemic/<file>`.

**File names.** Each file is named `<role>_<a|b|c>__<first 8 hex of the Epidemic ID>.wav`.

**md5 lock.** `tools/sound/epidemic_md5.json` holds the md5 of every file. `check_sound_lock.py` stops the build
if a file is missing, replaced, or not in this catalog. The md5 values are for the 48 kHz / 24-bit conversion
made with this repo's ffmpeg.

**Levels.** The role level is the dB value the renderer applies (`tools/sound/sfx_mix_lib.py`), after each segment
is normalised:
- one-shots are peak-normalised to -3 dBFS, the same as every battle-maps kit file;
- beds (loops) are RMS-normalised to -20 dBFS.

Where the levels come from:
- explosion, impact, hit, jet, whoosh and tick come from STYLE_LOCK section 3;
- pop, boom, riser, projector and drone come from the STYLE_LOCK section 2a sound-design table;
- **ship** and **horn** are new ship-channel roles. They need the owner's sign-off.

**Sync type** says which point of the sound is placed on the visual event frame:
- **peak** = its loudest 50 ms;
- **onset** = its first frame within 20 dB of its loudest.

"Chosen" = used in `videos/oriskany/test_v3` (the new-sound remix) or set as the role's default file.

| role | Epidemic ID | title | duration | chosen? | level role (STYLE_LOCK) | file / region used |
|---|---|---|---|---|---|---|
| demolition / underwater charges (sequence) | f6f10ea4-5ac6-422d-9e03-e5b4067f0ede | Explosions, Real, Multiple Explosions, Distant | 8.08 s | **yes** (both charges) | explosion -4 (sec. 3) | `charges_c__f6f10ea4.wav`: crack 0.17 s (1st charge) and 1.80 s (main blast) |
| underwater charges | 955e7371-94ff-4eff-912e-fe7a43ca9f9d | Explosions, Real Underwater ThunderFlash, Thump, DR05 | 37.61 s | candidate | explosion -4 | `charges_a__955e7371.wav`: thumps at 8.2 / 17.3 / 31.0 s, 93 % < 120 Hz |
| underwater charges / seabed thump | 0ecb5c38-256a-4acc-b02f-20376555aea0 | Explosions, Real Underwater ThunderFlash, Thump, D100 | 34.55 s | **yes** (seabed impact) | impact -7 | `charges_b__0ecb5c38.wav`: thump at 17.62 s |
| big water impact / splash | 1d6949d6-3190-4556-8fb3-7c6ff2f39e2b | Water, Impact, Shot, Fast, Short, Splash 01 | 9.31 s | **yes** | impact -7 (sec. 3) | `splash_a__1d6949d6.wav`: 0-1.2 s |
| big water impact / splash | 3ba7bd2a-989e-4f1e-ab84-a3f797ed1582 | Water, Impact, Shot, Fast, Short, Splash 02 | 11.41 s | candidate | impact -7 | `splash_b__3ba7bd2a.wav` |
| big water impact / splash | abc500c8-1c74-4575-9f48-e26767355c84 | Water, Splash, Big, Dive | 29.20 s | candidate | impact -7 | `splash_c__abc500c8.wav` |
| ship hull metal groan / stress | 7c63fd7c-450a-4b97-beb3-154ff7d02ff9 | Metal, Friction, Sheet Metal, Rubber Mallet, Creaks and Croaks, Deep, Groans 01, Schoeps (MS) | 17.19 s | **yes** | ship -13 (new) | `groan_a__7c63fd7c.wav`: groans 7.55-10.5 s |
| ship hull metal groan / stress | 2bc7c5e1-70de-4a4c-9d47-55807e0d3231 | Metal, Friction, Resonating Heater, Stress, Rumble 01 | 15.75 s | candidate | ship -13 | `groan_b__2bc7c5e1.wav` |
| hull scrape (underwater) | 87dfc4bf-1ef0-48f7-9e46-3dce396d3314 | Boats, Underwater, Ship, Large, Scrape, Rock Grounded, Underwater Perspective | 24.00 s | candidate | ship -13 | `groan_c__87dfc4bf.wav` |
| water rush / flooding | db95b348-3614-4374-bc94-e6a8068e7784 | Water, Turbulent, Dam, Huge, Water Splash, Beating Over Dam 02 | 120.00 s | **yes** | ship -13 | `flood_a__db95b348.wav`: from 0.70 s |
| water rush / flooding (underwater) | 3e14e767-3a83-4ea5-bc58-9809cf9cd90a | Water, Underwater, Movement, Underwater Texture, Submarine, Ship, Underwater Earthquake, Heavy Deep Bubbles, Rumble | 18.35 s | candidate | ship -13 | `flood_b__3e14e767.wav` |
| bubbles / air release | e58b390c-c846-4a03-81fd-5fb737e5e14d | Water, Underwater, Bubbles, Submerge, Gurgle | 11.86 s | **yes** | ship -13 | `bubbles_a__e58b390c.wav`: burst 2.95-4.5 s |
| bubbles / air release | 18fdc570-27b3-454c-a479-5b0e77e6e86d | Water, Movement, Submerge, Bucket, Air Pockets Release, Splash, Hydrophone, Ultrasonic 07 | 13.15 s | candidate | ship -13 | `bubbles_b__18fdc570.wav` |
| distant ship horn | 463af07a-e0b5-41be-9019-008d70e379e2 | Boats, Horn, Distant, Big Transatlantic Ship | 34.69 s | **yes** (signature) | horn -10 (new) | `horn_a__463af07a.wav`: 1st blast 0.2-7.8 s |
| distant ship horn | 54cd7292-c39f-4675-adcc-5f47ef5ed251 | Boats, Horn, Large Passenger Ship, Distant Blasts Reverberating Across Sea, Seagulls Reacting, Hurtigruten | 21.33 s | not downloaded yet | horn -10 | |
| distant ship horn | 67be070b-563c-4380-95be-55a0302300c0 | Boats, Horn, Ship, Ferry, Medium Close | 13.38 s | not downloaded yet | horn -10 | |
| jet catapult launch (carrier deck) | 9fc48bf0-bb23-42cb-9f9e-82b9f0b3c542 | Aircraft, Military, Jet, Pass, External 01 | 13.89 s | **yes** | jet -11 (sec. 3) | `jet_a__9fc48bf0.wav`: from 3.55 s, loudest ~4.4 s |
| jet catapult launch | d47bee57-0d37-426d-aaaa-25651ea4fc3d | Aircraft, Jet, Exterior, Passby, Takes Off At Runway, Close | 32.02 s | candidate | jet -11 | `jet_c__d47bee57.wav` |
| jet catapult launch | 7a5b5e5c-b24f-4b84-9bea-95205923ef67 | Aircraft, Military, Aircraft, Combat Jet, FA18 Hornet, Takeoff | 71.00 s | not downloaded yet | jet -11 | (Epidemic has no real steam-catapult recording; "catapult" search = siege engines) |
| jet flyby | da6a1527-fa97-469b-a1d8-cf04446bc29f | Aircraft, Military, Jet, Pass, External 04 | 10.08 s | candidate | jet -11 | `jet_b__da6a1527.wav` |
| jet flyby | 01f6e64f-09f5-4d22-b7bb-210eb00c194d | Aircraft, Jet, Small Jet Turbine Plane, Fly By 06, Runway Position 2, CM4 | 40.02 s | not downloaded yet | jet -11 | |
| ocean waves bed | 3d49f79f-73c8-4e2a-b59a-cfef1429d686 | Water, Wave, Ocean, Medium Waves, Wind | 129.54 s | **yes** | bed -30 (sec. 2a drone-bed level) | `waves_a__3d49f79f.wav` |
| ocean waves bed | 50834cc7-afbe-4d43-afc8-2d92df548aa4 | Water, Surf, Ocean, Constant Roaring Waves | 141.66 s | not downloaded yet | bed -30 | |
| underwater ambience bed | 127d88ce-948f-47cb-877f-98e9e25ca787 | Ambience, Underwater, Deep 01 | 180.00 s | **yes** | bed -30 | `underwater_a__127d88ce.wav` |
| underwater ambience bed | 58a16de1-4407-4dc5-aad2-b7a2126a2194 | Ambience, Underwater, Distant, Low Rumble 02 | 99.03 s | not downloaded yet | bed -30 | |
| film projector loop (archive film) | 5648e70b-bdf2-4398-b0b4-100db78c5df9 | Communications, Audio Visual, 8mm Projector | 20.00 s | **yes** | projector -27 (sec. 2a) | `projector_b__5648e70b.wav` |
| film projector loop | 6f4d59cf-da38-4457-a743-daa61310bf31 | Communications, Audio Visual, Analog Film, Movie Projector, Loop | 7.00 s | candidate | projector -27 | `projector_a__6f4d59cf.wav` |
| film projector loop | 0b041df3-b57d-4ec6-a047-359c44e38e71 | Communications, Audio Visual, 35mm Projector, Kinoton FP30 E, Close To Shutter 01 | 131.22 s | not downloaded yet | projector -27 | |
| cinematic whoosh (camera moves) | 689b1489-8811-4963-a9af-28187d5c7486 | Swooshes, Whoosh, Deep, Low, Cinematic | 2.44 s | **yes** (both big moves) | whoosh -12 (sec. 3 zoom) | `whoosh_a__689b1489.wav`: from 0.15 s |
| cinematic whoosh | 8d9712d2-0cbf-44bb-a3fb-0abfcd15bf9f | Swooshes, Whoosh, Big, Cinematic | 3.50 s | candidate | whoosh -12 | `whoosh_b__8d9712d2.wav` |
| cinematic whoosh | 553c6ec9-a5dd-41a6-a575-fd3cb8d3bcd3 | Swooshes, Whoosh, Deep, Crisp, Cinematic 01 | 4.44 s | not downloaded yet | whoosh -12 | |
| dry pop (labels) | 844f57e0-db47-4ea9-b712-8757b37ef151 | User Interface, Click, Button, Short, Soft, Click, Mid, Dry, Woody | 2.72 s | **yes** | pop -20 (sec. 2a) | `pop_b__844f57e0.wav`: 0-0.25 s |
| dry pop (labels) | 9da883ac-6b03-4df0-b8e6-cd85c7c926a5 | User Interface, Click, Pops, Glass, UI, Pops | 0.66 s | candidate | pop / tick -20 | `pop_a__9da883ac.wav` |
| cinematic boom (key beats) | 2f0a40ab-f23a-4927-a911-1d70459d52e7 | Designed, Boom, Cinematic, Deep, Boom, Impact | 2.80 s | **yes** | boom -11 (sec. 2a) | `boom_a__2f0a40ab.wav`: hit 0.11 s |
| cinematic boom | 240e5b47-f13f-49e8-a66a-75720e0a2428 | Designed, Boom, Cinematic Hit, Low Boom | 3.50 s | candidate (rejected for sync: 4 sub pulses, loudest is the 2nd at 0.49 s) | boom -11 | `boom_b__240e5b47.wav` |
| reverse riser (into reveals) | fd98cb0b-3c2f-47e9-a88a-052bed1de9a9 | Designed, Riser, Transition, Reverse, Eerie, Fast, Short | 2.88 s | **yes** | riser -17 (sec. 2a) | `riser_a__fd98cb0b.wav`: peak 2.21 s on the reveal |
| reverse riser | dbd5c65b-6273-498f-891d-f89bb2bea94c | Designed, Riser, Transition, Traditional, Reverse, Cymbal, Fast | 5.56 s | candidate | riser -17 | `riser_b__dbd5c65b.wav` |
| low tension drone bed | 244a55e9-ac7a-40dd-98d1-22e104fe7155 | Designed, Drone, Tension, Low | 55.92 s | **yes** | drone -30 (sec. 2a) | `drone_a__244a55e9.wav`: from 6 s |
| low tension drone bed | 54e34fc2-46d0-46f2-a873-42cdccfd9d53 | Designed, Drone, Bassy Tension | 29.99 s | not downloaded yet | drone -30 | |
| metal creak | c464d466-0179-4ffb-8ec6-0ed0890f6c90 | Metal, Movement, Rattle, Shipping Container, Drag, Creak, Squeak, Heavy, Deep, Big Reverb | 9.97 s | not downloaded yet (not in the test) | ship -13 | |
| metal creak | a01ebcd2-9068-441a-9c03-e16f23425aa3 | Doors, Creak, Metal, Slow, Long, Heavy 01 | 9.24 s | not downloaded yet | ship -13 | |
| metal creak | fa68242a-061f-45cc-badc-97a4ec5ffc05 | Metal, Movement, Shipping Container, Drag, Creak, Squeak, Heavy, Deep, Big Reverb 04 | 4.52 s | not downloaded yet | ship -13 | |

## Notes

**Real or designed.** "Designed" in an Epidemic title means sound-designed from recorded material. Epidemic does
not mean it as synthesis in our sense.
- The **story sounds** use the "Real" field recordings wherever Epidemic has one: charges, underwater thumps,
  splash, flood, bubbles, horn, jets, waves, underwater ambience and projector.
- The **cinematic layer** (boom, riser, drone, whoosh) is Epidemic "Designed" material. STYLE_LOCK 2c-5
  (owner 2026-11-03) banned the *synthesized* versions of these sounds (`ref_sounds.py`). The owner now asks
  for real library recordings in these roles, but they still need the owner's ear before they are locked.

**Not downloaded yet.** Candidates marked "not downloaded yet" are roles the 1-minute test does not use, or
reserves. The owner asked for the test first; download them when the full video needs them.

**Rights.** Epidemic Sound subscription licence (owner's account). Content ID: Epidemic recordings are cleared
for the subscribed channel. Keep the channel connected to the Epidemic account before upload.
