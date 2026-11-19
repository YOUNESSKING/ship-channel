# Pronunciation gate: USS Samuel B. Roberts (Archive voice, 2026-11-20)

faster-whisper small.en on every chunk vs the script (`build/voice_gate.py`): first pass 41/243 chunks differed.
Fixes (`text_fix.json`, `phon_fix.json`, Kokoro phonemes checked to hit every occurrence):
| word | Kokoro before | fix | heard after |
|---|---|---|---|
| Samar (x6) | sˈæmɚ (SAM-er) | sˈɑːmɑːɹ (SAH-mar) | Samar |
| Leyte (x3) | lˈeɪt ("late") | text "Laytee" | LAY-tee ("lady"/"laity", flapped t) |
| coxswain | kˈɑːkssweɪn | text "coxun" (COX-un) | ok |
| Checotah | tʃˈɛkɑːɾə | tʃəkˈoʊɾə (chuh-KOH-tuh) | ok ("Chicoda") |
| Morizet | mˈɔːɹɪzɪt | mˌɔːɹɪzˈeɪ (mor-ih-ZAY) | ok |
| Kurita (x2) | kjʊɹɹˈiːɾə (kyoo-) | kʊɹˈiːɾə (koo-REE-tuh) | ok |
| Chokai (x3) | tʃˈɑːkaɪ | tʃˈoʊkaɪ (CHOH-kai) | ok |
| Takeo | tˈeɪkɪˌoʊ | tɑːkˈeɪoʊ (tah-KAY-oh) | ok |
| Gambier (Bay) | ɡˈæmbiɚ | text "Gambeer" | ok |
| Guadalcanal | ɡwɑːdˈælkənəl | text "Gwadal-canal" (gwah-dul-kuh-NAL) | ok |
Second pass: 36/243 differ, all homophones / number formats / whisper spellings (Hoel = "hole" is right; Kongo = "Congo"; crewed/crude;
wrecks/rex; metres/meters; Saint Lo/St. Lo). EYOS read "EYE-ohs" (company's own pronunciation not found: owner ear-check).
Names clip for the owner: `voice_sample/names_sbr.mp3` (36 names, 65.5 s).
