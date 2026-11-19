# USS Ranger: items the owner must download by hand

Build machine limits seen on 2026-11-19: Wikimedia (Commons API and upload.wikimedia.org) answers HTTP 429 "too many requests" from this cloud IP (no download possible); history.navy.mil (NHHC) fails TLS/proxy; navy.mil returns 403; loc.gov search returns 403; navsource.org is unreachable; DVIDS search pages sit behind a JavaScript challenge (item pages and CDN files work) and the "Download" buttons need a DVIDS login. So:

## 1. DVIDS originals (log in at dvidshub.net, free) - the sharp Ranger tow stills
The files in `src/photos/dvids_ima_*` are the public CDN copy (2000 px wide). The page lists the originals:

| DVIDS id | page | original | wanted stem |
|---|---|---|---|
| 1799520 | https://www.dvidshub.net/image/1799520 (towed away from Bremerton, 5 Mar 2015, MC Seaman Frost) | 6622x4419 | `dvids_ima_1799520` (replace) |
| 1799515 | https://www.dvidshub.net/image/1799515 | 2100x1400 (CDN copy is already full) | - |
| 1799342, 1799349, 1799353, 1799356, 1799358 | https://www.dvidshub.net/image/<id> ("USS Ranger departs Bremerton", PO2 Seth Coulter) | 4928x3280 each | same stems |
| 1799348 | same series | 4928x2768 | same stem |
| 6967137 | ex-Kitty Hawk, bollards foreground | 5057x3371 | `dvids_ima_6967137` |
| 8834182 | ex-JFK (2025) | 6048x4024 | `dvids_ima_8834182` |
Save as JPEG, longest side <= 3840 px.

## 2. Wikimedia Commons (US Navy / DoD photos with PD-USGov) - not fetched
Search Commons by hand for: "USS Ranger (CV-61)" category (decommissioning 10 Jul 1993 at Bremerton, Ranger at Bremerton inactive ships, 1957 commissioning at Norfolk, Vietnam-era Ranger photos, VF-1 / VF-2 F-14s on Ranger, 1992 Doolittle B-25 re-enactment launch from Ranger, Ranger and Forrestal-class carriers at Brownsville / International Shipbreaking). Accept only files whose page shows "PD-USGov-Military-Navy" (or DoD) AND a source (NHHC / NARA / DVIDS). Note rights and source for CREDITS.md.

## 3. NHHC (history.navy.mil) - photo pages not reachable
`https://www.history.navy.mil/our-collections/photography/us-navy-ships/aircraft-carriers/ranger-cv-61.html` (Ranger CV-61 photo set: look for 1957 commissioning, 1960s Vietnam, 1993 decommissioning). Save large scans as `src/photos/nhhc_<number>.jpg`.

## 4. Candidates found but NOT downloaded (rights unclear)
- Australian War Memorial F04634 "USS Ranger, Gulf War 1991" (56 min video shot aboard Ranger by an RAAF reservist). Not US-government: Australian copyright, treat as NOT usable unless AWM licence is confirmed (https://www.awm.gov.au/collection/F04634).
- archive.org PeriscopeFilm "1959 Marine Corps recruiting film USS RANGER CV-61 & recon scouts" (24994ThreeGuysCalledMac), "RA-5C Vigilante aboard USS Ranger" (80354: CC BY-NC-ND: NOT allowed), "Ballad of John Greene" (A-7 era, no licence given). Look for the original USMC / Navy reels in the NARA catalog (RG 127 / RG 428) before using.
- NARA 148015282 "F-14 Tomcat the Total Fighter": commercial production, "Restricted - Possibly": skip.
- 330-DIMOC-3139 "FLIR Camera Desert Storm" (NARA, "Restricted - Possibly"): carrier air wing 8, not Ranger.
- CriticalPast clips of Ranger F-14 deck ops (VF-1, 1980): licensed stock, not PD.
