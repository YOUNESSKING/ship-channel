# Pronunciation dictionary (shared by every video)

Owner rule (2026-10-26, after the Morgan comments about "Nathanael Greene"): **check every name before voicing.**

## Check before every narration
1. List every person, place and unit name in `script.md`.
2. Phonemize each one (no listening needed), from `/home/user/battle-maps/tts`:
   ```
   python3 -c "from kokoro_onnx import Kokoro; k=Kokoro('kokoro-v1.0.onnx','voices-v1.0.bin'); [print(w,'->',k.tokenizer.phonemize(w,'en-us')) for w in ['Nathanael Greene','Tarleton']]"
   ```
3. **Check the STRESS mark (ˈ), not only the sounds**: the primary stress must sit on the right syllable (Cornwallis was respelled to the right vowel but kept the stress on CORN). Anything wrong or unsure: find a respelling that phonemizes right, add it to the table below AND to the `SAY` dict in the video's `tools/narrate.py` (the script text stays correct; only the spoken text changes).
4. Voice a **20-second names clip** (each name said once, in a short sentence) and send it to the owner. Record the full narration only after the owner approves it.

## Dictionary
| Written | Say (SAY respelling) | Kokoro before → after | Video |
|---|---|---|---|
| Nathanael (Greene) | Nathaniel | `nˈæθɐnˌeɪl` ("NATH-an-ail", wrong) → `nɐθˈænjəl` | Morgan (fixed after viewer comments) |
| Tarleton | Tarlton | `tˈɑːɹɹəltən` → `tˈɑːɹltən` | Morgan |
| Banastre | Bannister | `bˈænæstɚ` → `bˈænɪstɚ` | Morgan |
| Bemis (Heights) | Beemis | → "BEE-mis" | Morgan |
| Burgoyne | (as written) | `bˈɜːɡɔɪn`, fine | Morgan |
| **Cornwallis** | no respelling works: every spelling keeps the stress on CORN. Use exact phonemes `kɔːɹnwˈɑːlɪs` (possessive `kɔːɹnwˈɑːlɪsᵻz`) via `k.create(..., is_phonemes=True)`; tool: `greene2/tools/revoice_name.py` | `kˈɔːɹnwɔliz` (CORN-wallis, wrong) → `kɔːɹnwˈɑːlɪs` (korn-WAH-lis) | Greene remake (owner caught it, 2026-10-27) |
| Cowpens, Saratoga | (as written) | `kˈaʊpənz`, `sˌæɹɐtˈoʊɡə`, fine | Morgan |

Add new rows for every video. Names from earlier videos with known fixes: see each video's `tools/narrate.py` `SAY` dict (e.g. Goose Green: Piaggi, Estévez).
| Tecumseh | exact phonemes `təkˈʌmsə` (sherman/tools/tts_names.py PHON) | `tˈɛkəmsˌeɪ` (TEK-um-say) → `təkˈʌmsə` (tuh-KUM-suh) | Sherman |
| Appomattox | exact phonemes `ˌæpəmˈæɾəks` | `ɐpˈɑːmɐtˌɑːks` (a-POM-a-tox) → `ˌæpəmˈæɾəks` (ap-uh-MAT-ux) | Sherman |
| Oostanaula | exact phonemes `ˌuːstənˈɑːlə` | `ˈuːstɐnˌɔːlə` (OO-stan-awla) → `ˌuːstənˈɑːlə` (oo-stuh-NAH-luh; Wikipedia "oo-stuh-NA-luh") | Sherman |
| Chattahoochee | exact phonemes `tʃˌæɾəhˈuːtʃiː` | `tʃˈæɾɐhˌuːtʃiː` (CHAT-a-hoochee) → `tʃˌæɾəhˈuːtʃiː` (chat-uh-HOO-chee) | Sherman |
| Salkehatchie | exact phonemes `sˌɔːlkɪhˈætʃi` | `sˈælkɪhˌætʃi` (SAL-ki-hatchie) → `sˌɔːlkɪhˈætʃi` (sawl-kee-HATCH-ee) | Sherman |
| Macon (Georgia) | Maykon | `mˈækən` (MACK-en) → `mˈeɪkən` (MAY-kun) | Sherman |
| Kennesaw, Resaca, Allatoona, Milledgeville, Griswoldville, Hardee, Schofield, Slocum, Jonesboro, Durham | (as written) | `kˈɛnɪsˌɔː`, `ɹᵻsˈɑːkə`, `ˌælɐtˈuːnə`, `mˈɪlɪdʒvˌɪl`, ... fine | Sherman |
| Patton | exact phonemes `pˈætən` | `pˈæʔn` (glottal stop) → `pˈætən` | Patton |
| Bastogne | `bæstˈoʊn` (ba-STONE, Merriam-Webster; Americans since 1944) | `bˈæstɑːɡni` → `bæstˈoʊn` | Patton |
| McAuliffe | `mɪkˈɔːlɪf` (mik-AW-lif) | `mək ˈɔːlɪf` (split) → one word | Patton |
| Avranches / Pontaubault / Sélune / Le Mans / Mortain / Alençon / Argentan / Mantes / Chaumont / Assenois | Americanised French: `ɑːvɹˈɑːnʃ`, `pˌɑːntoʊbˈoʊ`, `seɪlˈuːn`, `lə mˈɑːn`, `mɔːɹtˈæn`, `ɑːlɑːnsˈoʊn`, `ɑːɹʒɑːntˈɑːn`, `mˈɑːnt`, `ʃoʊmˈoʊn`, `ɑːsənwˈɑː` | Kokoro read them as English spellings (AV-rantchiz, Le MANZ, AR-jenten, ...) | Patton |
| Kluge / Hausser / Nierstein / Grossgerau / Remagen / Schnee Eifel | German: `klˈuːɡə`, `hˈaʊsɚ`, `nˈɪɹʃtaɪn`, `ɡɹˈoʊsɡɛɹˌaʊ`, `ɹɪmˈɑːɡən`, `ʃnˈeɪ ˈaɪfəl` | Kloodj, HAW-ser, Re-MAY-jen, SHNEE... → fixed | Patton |
| Meuse / Moselle / Verdun | `mjˈuːz`, `moʊzˈɛl`, `vɚdˈʌn` (ver-DUN) | stress/voicing fixed | Patton |
| Jaques | NOT verified (Jakes vs Jacks): name removed from the script | | Patton |
Web check 2026-10-31 confirmed only Bastogne (Merriam-Webster ba-STONE); the rest follow standard English/WWII-documentary usage and Gemini's guide (Avranches ah-VRAHNSH, Sélune say-LOON, Mortain mor-TAN, Argentan ar-zhahn-TAHN, Assenois ah-sen-WAH, Chaumont shoh-MOHN, Nierstein NEER-shtine, Oppenheim OP-en-hime).
| Donelson / Tilghman / Grierson / Beauregard / Weyanoke / Trevilian / Gouverneur (Warren) | exact phonemes `dˈɑːnəlsən` (DON-ul-sun), `tˈɪlmən` (TIL-mun, silent g), `ɡɹˈɪɹsən` (GREER-sun), `bˈoʊɹəɡˌɑːɹd` (BOH-ruh-gard), `wˈaɪɐnˌoʊk` (WYE-uh-noke), `tɹəvˈɪljən` (truh-VIL-yun), `ɡˈʌvɚnɪɹ` (GUV-er-neer) | Kokoro said DOHN-elson, TIL-g-man, GRY-er-son | Grant (Weyanoke: Virginia DOE WYE-uh-nok; Tilghman/Trevilian/Grierson/Beauregard: standard usage, unverified, owner ear-check) |
| Vicksburg, Yazoo, Chickahominy, Bruinsburg, Hinks, Dimmock, Drewry, Hovey, Forrest, Halleck, Foote, Buckner, Pemberton, Hankinson | (as written) | fine in Kokoro | Grant |
