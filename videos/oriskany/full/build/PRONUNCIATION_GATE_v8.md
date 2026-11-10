# Oriskany v8, Archive voice: pronunciation gate (2026-11-10)

Voice: Kokoro style blend bm_fable 0.40 + am_michael 0.40 + bm_lewis 0.20 (`tts/voices/archive_style.npy`), speed 0.92,
questions 0.852 (= 0.92 x 0.88 / 0.95, the am_michael take's relative slowdown). Text: `script/NARRATION_v3.txt`.
Built by `build/voice.py` (225 chunks, 832.23 s of narration; v7 was 847.6 s).

## Method
1. `build/voice.py` transcribes every chunk with faster-whisper small.en (the word timings come from the same pass).
2. `build/voice_gate.py` spells out the digits whisper prints and diffs the transcript against the script, word by word
   (`build/voice_gate_diff_timing.json`, log `build/voice_gate_final.log`). base.en was also run on the first take.
3. Every hard name: `phonemize` checked for stress, then said once in `videos/oriskany/voice_sample/names_archive.mp3`
   (22 s, `build/names_clip.py`): Oriskany, Okaloosa, MiG-fifteens, porgies, Bremerton, Escambia, Pensacola, Corpus Christi,
   Beaumont, Mare Island, Tonkin, Hanoi, Stockdale, McCain, Essex-class, "Her keel", Gustav, Skyhawk, vermilion, PCBs.
   small.en reads the clip back correctly (Mare Island as "Mer Island": the right "mair" vowel).

## Fixes
| word | problem with the Archive voice | fix | after |
|---|---|---|---|
| Oriskany | Kokoro stresses OR-iskany | phonemes `ɔːɹˈɪskəni` (kept from v1-v7) | heard "Oriskany" |
| Okaloosa | OH-kaloosa | phonemes `ˌoʊkɐlˈuːsə` (kept) | heard "Okaloosa" |
| porgies | "porjeez" | phonemes `pˈɔːɹɡiz` (kept) | heard "porgies" |
| MiG, MiG-fifteens | read "my-gee" | respelled "Mig" (kept) | heard "MiG-15s" |
| Essex-class | `ˈɛsɪksklˈæs` runs together: heard "Essex **glass**" by base.en and small.en | respelled "Essex class" (`build/text_fix_v8.json`) | heard "Essex class" |
| Her keel (sentence start) | unstressed, r-less `hɜː`: heard "**Hakeel** was laid" | phonemes `hˈɜːɹ kˈiːl` (`build/phon_fix_v8.json`) | heard "Her keel was laid" |
| but her sinking | r-less `hɜː`: heard "but **our** sinking" | phonemes `bˌʌt hɜːɹ sˈɪŋkɪŋ` | heard "but her sinking" |
| towed (back to Texas) | heard "told" by small.en (base.en: "towed") | phonemes `tʰˈoʊd`: in a solo take small.en hears "towed", in the full take it still writes "told" | **borderline, open**: listen at 7:18 |

## Left as is (transcript spelling, not speech)
Numbers and dollar amounts (whisper prints digits), "1990s", ordinals ("26th"), grey/gray, centrepiece/centerpiece,
"Vermillion", "Gustave" (base.en only), "The storms saw to that" heard "soar" (saw/soar merge of the British-blend vowel;
the sense is clear in context).
