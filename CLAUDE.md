# Ship Channel: instructions for agents

Read `PLAN.md` first. Detailed reuse notes: `reference/notes_battle_maps.md`, `reference/notes_prehistory.md`.
The original rulebooks are kept unchanged in `reference/battle-maps/` (HANDOVER, STYLE_LOCK) and
`reference/prehistory/` (GOLD_STANDARD, HOUSE_STYLE, animation_kit). When a rule here and a rule there
disagree, this file wins.

## Channel
- Name: **Fleet's End** (@FleetsEnd). Logo (owner pick 2026-11-10): concept D "Last light", a black Essex-class carrier going down against a red-orange sun (#D9572B), white waterline and ring. Final files: `assets/brand/final/` (builder `assets/brand/make_vector_logo.py`). Wordmark: Anton, FLEET’S white + END red, tagline steel-blue. No gold/yellow.
- Niche: ship history, "what happened to it" stories, mostly US Navy (public-domain imagery).
- Format: 14–24 min long-form, 2–3 uploads a week max, never daily (inauthentic-content policy).
- Faceless, AI narration. Tick YouTube's "altered or synthetic content" box: Yes.
- Voice (owner pick 2026-11-10): designed voice 3 "Archive" = Kokoro style blend bm_fable 0.40 + am_michael 0.40 + bm_lewis 0.20, speed 0.92 (`tts/design_voice.py`, style file `videos/oriskany/voice_sample/designed/3_archive_style.npy`; copy it to `tts/voices/archive_style.npy`). Run the pronunciation gate (`tts/PRONUNCIATION.md`) with this voice.
- Avoid topics the clone channels already did (list in `research/TOPICS.md`).

## Path fix
Copied tools still hard-code `/home/user/battle-maps` or `/home/user/prehistory-channel`. Before running one,
patch it to use paths relative to this repo. Never delete or edit the source repos.

## Rules (carried over)
- Fact sheet first: Gemini dossier, then 3 independent fact-checkers on official sources. Gemini invents claims.
- Hook approved by the owner before the full script. Shot-list gate before any render. Ask before any spend.
- Line 1 = the stakes. Title promise spoken by 10–15 s. First frame is a map. No ship résumé in the first 2 min.
- Every shot proves the spoken words. Something new on screen every 1.5–4 s, hard cap 6 s per shot.
- A place or date = a map. A number lands on its spoken word. A clip is reused at most twice, 3+ min apart.
- No plain black/dark text cards (owner, 2026-11-05): every text or number card sits on a dimmed moving background
  (matching film, tagged generic b-roll, or a moving map/photo) to keep viewers engaged.
- A wow early, then every 30 s for the first 3 min; a mid-video reversal; a closing question; ending ≤ 45 s.
- Rights: PD / CC0 / CC BY / CC BY-SA only, never NC/ND. Read each item's rights field. Log every file in
  the video's `CREDITS.md`, and every film clip in `MANIFEST.md` with what it does NOT show.
- Archive film: no "Deep Time" grade (`GRADE=none`); pillarbox or upscale old 4:3 film; trim leaders.
- Loudness: -14 LUFS with a measured trim (STYLE_LOCK 2c-9). Renders run detached and resumable.
- Packaging: 3 titles scored ≥ 85 in vidIQ + 2–3 thumbnails in Test & Compare; 1–3 true words on the
  thumbnail; check it at sidebar size.
- Commit after every step. Never commit keys; keys live in `~/.el_key*`, `~/.fal_key` etc. (`tools/setup_keys.sh`).

## Still to build
Sea-floor map look (re-grade `bake.py`), modern carrier silhouette, sinking animation, ship `brand-style.md` for
thumbnails. Ship SFX now = real Epidemic recordings (`assets/sfx/EPIDEMIC_SFX.md`, files git-ignored) through the v2
chain in `tools/sound/` (reference build: `videos/oriskany/test_v3/build/mix_v2.py`, `SOUND_REPORT_v2.md`). Owner
listened to Oriskany test v4 and approved the sound (2026-11-04), with one change: horn 4 dB quieter (-10 → -14 dB).
Owner change 2026-11-05: horn at most 2 s, at most 2 per video, never under speech; no effect rings >1.5 s past its event. Owner 2026-11-08: SFX -3 dB, ends with its shot. Event roles: explosion/charges -7, impact -10, hit/stamp -11, boom -14, jet -17 (plus -6 dB at 2.5 kHz), whoosh -15, ship (groan/flood/bubbles) -16, riser -20, horn -23, pop -23, tick -23 dB; beds 2 dB down: projector -29, drone/waves/underwater -32 dB. Every effect is silent by the next picture cut after its event (0.25 s fade ending on the cut; a whoosh on the cut itself may run ≤ 0.4 s into the next shot); beds start and stop with their shots (0.25 s fades). Voice and music unchanged. Owner 2026-11-08: quieter SFX (critic v5): per-cue trims may only cut (gain ≤ 0, lowpass, longer fade); one-off exception: the 2nd hook blast (17.65) may run ≤ 0.25 s past its cut into the voice gap, faded, ending before the next word; LRA floor for full-length masters 1.7 LU (was 2); big beats ≥ +1 LU over speech (was +3). Those roles and levels are now locked (`tools/sound/check_sound_lock.py`); the approved look/sound reference is `videos/oriskany/test_v4/` with the 2026-11-08 levels.

## Competitor lessons (Forgotten Fleet)
Full study with the final, critic-checked DO / DON'T lists: `research/FORGOTTEN_FLEET_STUDY.md`
(last section). Key gates for every topic:
- The ship is famous, nobody has covered it yet, and the answer surprises. Never a "it's in a museum" answer.
- Hold the answer until the last act; no ship résumé up front.
- Never repeat the same harbour/cluster within ~3 months; vary title and thumbnail templates.
- Judge a video on day 7–14 Studio data, not day 1.
