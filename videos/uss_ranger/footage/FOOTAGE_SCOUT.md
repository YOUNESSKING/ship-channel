# USS Ranger (CV-61): footage scout

Scouted and downloaded 2026-11-19 (unlike Nevada the scout and the download were one pass).

**How items were found.**
- NARA: `tools/nara_search.py` / `nara_collect.py` call `https://catalog.archives.gov/proxy/records/search?q=...&page=N&typesOfMaterials=...` (header `Content-Type: application/json`, no key; do NOT add a `limit` parameter, it breaks the proxy and returns the HTML page). Hits were filtered to titles/notes naming Ranger with CV-61 / CVA-61 (336 still candidates), 93 + 14 stills downloaded with `tools/nara_download.py`. Record fields (useRestriction, local identifier, caption, scan URL) come from the same API by `naId`.
- DVIDS: item pages work with curl; discovery only through web search (the search/tag pages are challenged). `tools/dvids_fetch.py` reads the page (licence line, date, resolution) and downloads the CDN file (images `.../2000w_q95.jpg`, videos the best mp4 up to 1920x1080 named in the page's m3u8 ladder).
- archive.org: advanced-search JSON; the three DoD (DIMOC) films in `usgovfilms` carry CC0 marks and the original MPEG-2 files were fetched.
- Queries that returned nothing usable: DVIDS "Ranger" 1980s-90s; DVIDS Constellation tow; NARA 1957 Ranger commissioning film; Desert Storm Ranger film; any Brownsville shipbreaking film; archive.org "scrapping" Navy films.

**Findings that change the script.**
1. Tow date is 5 Mar 2015 (DVIDS), not 2017-18.
2. NARA 84175 and 84181 look like Ranger in the title search but are USS Hancock (CVA-19, slates and "19" on the deck) and Coral Sea (CVA-43): do not use as Ranger.
3. NARA 85335's record title is cut off at "USS RANGER (CVA-6".
4. NARA 428-NPC-998 (Ranger launched at Newport News, 1929) and the CV-4 reels (1920s-43) are the FIRST Ranger (CV-4), not CV-61: excluded.
5. The 19-N "CVA 61 Ranger" file includes undated 1957 ceremony/ship interior prints and Oct 1965 Hunters Point antenna-arrangement prints.

**Sizes.** 136 stills, 30 films/videos, about 6 GB in `src/`. 
