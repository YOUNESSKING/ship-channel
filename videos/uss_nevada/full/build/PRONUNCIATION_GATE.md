# Pronunciation gate (USS Nevada, Archive voice)

faster-whisper **small.en** on every chunk of `audio/voice_archive.wav`, diffed against `script/NARRATION_v1.txt`
(`build/voice_gate.py small.en`; report `build/voice_gate_report.txt`): 29 of 226 chunks differ, all spelling or number
format (centre/center, harbour/harbor, "1,500", "28th") or the intended pronunciations below. No real misreadings.

Phoneme fixes (`build/phon_fix.json`, applied in `build/voice.py`):

| word | Kokoro default | fixed to | whisper heard |
|---|---|---|---|
| boatswain | BOAT-swain | BOH-sun | "boson" / "boesen" |
| forecastle | FORE-castle | FOHK-sul | "folksill" |
| Kwajalein | kwa-JA-leen | KWAH-juh-lin | Kwajalein |
| Waipio | WAY-pee-oh | wy-PEE-oh | Waipio |
| Cherbourg | CHUR-burg | SHAIR-boorg | Cherbourg |
| Toulon | TOO-lahn | too-LOHN | Toulon |
| Sakawa / Nagato | sa-KA-wa / na-GA-to (US vowels) | sah-KAH-wah / nah-GAH-toh | Sakawa / Nagato |
| Attu | uh-TOO | AT-too | Attu |
| Carlisle | CAR-lie-ul | car-LYLE | "car Lyle" |

Owner ear-check: `voice_sample/names_nevada.mp3` (50 s, 29 names). Borderline: "Fires broke out on her decks" (whisper:
"on a dex"), "Sedberry" (whisper: "said Berry", which is the intended SED-berry).
