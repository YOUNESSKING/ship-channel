# Ship Channel: instructions for agents

Read `PLAN.md` first. Detailed reuse notes: `reference/notes_battle_maps.md`, `reference/notes_prehistory.md`.
The original rulebooks are kept unchanged in `reference/battle-maps/` (HANDOVER, STYLE_LOCK) and
`reference/prehistory/` (GOLD_STANDARD, HOUSE_STYLE, animation_kit). When a rule here and a rule there
disagree, this file wins.

## Channel
- Niche: ship history, "what happened to it" stories, mostly US Navy (public-domain imagery).
- Format: 14–24 min long-form, 2–3 uploads a week max, never daily (inauthentic-content policy).
- Faceless, AI narration. Tick YouTube's "altered or synthetic content" box: Yes.
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
chain in `tools/sound/` (reference build: `videos/oriskany/test_v3/build/mix_v2.py`, `SOUND_REPORT_v2.md`); the owner
still has to listen and sign off the new roles before they are locked.

## Competitor lessons (Forgotten Fleet)
Full study with the final, critic-checked DO / DON'T lists: `research/FORGOTTEN_FLEET_STUDY.md`
(last section). Key gates for every topic:
- The ship is famous, nobody has covered it yet, and the answer surprises. Never a "it's in a museum" answer.
- Hold the answer until the last act; no ship résumé up front.
- Never repeat the same harbour/cluster within ~3 months; vary title and thumbnail templates.
- Judge a video on day 7–14 Studio data, not day 1.
