# Oriskany full video: build report v3 (2026-11-05)

**Output:** `videos/oriskany/full/oriskany_full_v3.mp4` (git-ignored). H.264 1920x1080, 30 fps, **25,968 frames, 865.6 s (14:25.6)**,
AAC stereo 48 kHz, audio = video length. v2 (884.8 s) is kept on disk; v1 was deleted after v3 passed its checks.

v3 = v2 (see `BUILD_REPORT_v2.md`) + two owner decisions of 2026-11-05:

## 1. Ending: option A (owner decision)

Cut from the narration (no re-voicing, `build/voice_cut_v3.py`, map in `build/cuts_v3.json`):

| cut | text | v2 span | removed |
|---|---|---|---|
| 1 | "Nobody would take her whole. Nobody could make a scrap deal stick. And the PCBs were in her wiring, where only taking her apart could reach them." | 805.434-815.067 | 9.633 s |
| 2 | "By the Navy's own sums, it was also the cheapest." | 818.098-821.751 | 3.653 s |
| 3 | "She is nine hundred and ninety feet long. No explosives this time. They will flood her." | 836.922-842.852 | 5.930 s |
| | | **total** | **19.216 s** |

- Cuts sit at chunk boundaries (sentence starts), in silence, with 10 ms crossfades placed entirely inside the pauses. The pause that
  remains at each join is the longer of the two original pauses (so the paragraph break before "She is still the only…" stays 0.6 s).
- **Answer section: 801.93 s ("So that is why…") → 846.60 s (last word) = 44.7 s** (was 64 s). Voice end 846.6 s; end screen 19 s.
- Everything after each cut moved with it: words.json, chunks.json, chapters.json (c07 now 161.05 s), shots (five c07 beats removed:
  the "How it ends" options + wiring x-ray of the recap, the "Navy's own sums" bars, the 990 FT photo and the NO EXPLOSIVES card),
  segments (5 renamed to their new shot ids, 1 rebuilt for its new length, 1 removed), SFX cues (the critic-B rules now run in v2 time
  through the cut map), beats.
- Shot rules after the cut: no shot over 6 s or under 1.2 s outside the hook (`build/shotlist_report.md`: no pacing flags); "The bottom of
  the Gulf" options now 3.3 s, the Okaloosa map unchanged (4.2 s); numbers still on their words (NOV 12 on "November", $50,000 on
  "fifty"); clip reuse report clean (no clip or photo over 2 uses or under 3 min apart; the cut removed one photo use, LoC HAER 582545).
- Music: not cut. The outro ("I Should Have Been More Human") still enters at 806.3 s, on the same words as in v2, and plays on to the end;
  the end-screen lift (+8 dB) follows the new voice end.
- Only c07 was re-rendered. Text: `script/NARRATION_v3.txt`, `script/SCRIPT_v3.md` (v2 files kept); the description timestamps are unchanged
  (all chapter starts are before the cut); MANIFEST.md and CREDITS.md (99 items) regenerated.
- Small layout fix found by the v3 check: on "NOV 12" the block's drop-in and the number's pop-in overlap, so the number dipped into the
  bottom 10 % for a few frames. `templates/lib/safe_area.js` now fits/wraps text before it lifts blocks, and lifts with a 24 px entry margin.

## 2. LRA rule (owner decision 2026-11-05)

`tools/sound/check_sound_lock.py`: a master longer than 5 min must have **2 ≤ LRA ≤ 8 LU** (the battle-maps reference band); short tests
keep **LRA ≥ 5 LU**. The decision and date are in a comment at the check and in the module docstring.

## Numbers (v3)

| measure | v2 | **v3** | target |
|---|---|---|---|
| integrated (ebur128 on the mp4) | -14.0 LUFS | **-14.0 LUFS** | -14 ± 0.5 |
| true peak | -1.5 dBTP | **-1.7 dBTP** | ≤ -1.5 |
| LRA | 2.1 LU | **2.1 LU** | 2-8 (new rule) → **PASS** |
| music under voice, whole video | -24.1 dB | **-24.1 dB** | not louder than v1 (-24.1) |
| music under voice, c06-c07 30 s windows | -24.5 … -27.9 | **-24.5 … -27.9**; the new ending window (806-836 s) -30.3 | -24..-28 |
| end screen (master M median) | -27.3 LUFS | **-25.2 LUFS** | ~-25 |
| SFX cues | 157 | **150 (10.4/min)**, sync max 1.1 frames, 0 over 3 | ≤ 3 frames |
| big beats ≥ +3 LU over speech | 9/10 | **9/10**: only the hook thump at 28.70 s, +2.9 LU (approved hook, left as is per the owner) | |
| `hit` cues | 1 (stamp) | 1 (stamp, +6.1 LU) | |

## Checks

- `check_safe_text.js`: **PASS c01-c07** (c07 also checked every 0.1 s across the whole chapter: PASS).
- `check_sound_lock.py`: static lock OK; render check: **only failure = hook beat at 28.70 s +2.9 LU vs +3.0** (owner: approved hook, report only).
  LRA passes under the new rule.
- ebur128: -14.0 LUFS, TP -1.7 dBTP.
- `check_clips.py --no-cuts`: 95 BLOB + 10 FLASH (`build/check_clips_v3.txt`), the same intentional flags as v2; none in the new ending.
- `FINAL_SHEET_v3.jpg` (every 10 s) looked at, and **`ENDING_SHEET_v3.jpg`: every second from 795 s to the end (71 frames)** looked at:
  MARAD card → SAVINGS COULD BE WIPED OUT → "So that is why" over the sinking photo → "The bottom of the Gulf" options over reef fish (tag on) →
  THE ONLY CARRIER EVER REEFED → SS United States film → NOV 12 → Okaloosa map → 13 NAUTICAL MILES end map → $50,000 → PLANNED · LARGEST
  ARTIFICIAL REEF → 1969 aerial → sinking photo → end screen card. No black frames, no empty cards, no stray labels from the cut lines.

## Left for the owner

- Hook thump 28.70 s at +2.9 LU (approved hook).
- Same open NICE items as v2 (e.g. the SS United States film at 812-815 s still shows a carrier in the background, critic A N6; pronunciation check by ear, critic B N5).
- vidIQ titles / Test & Compare thumbnails (spend gate). Publish before 11 Nov.
