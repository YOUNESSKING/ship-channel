#!/bin/bash
# dl_broll.sh - download the GENERIC US Government b-roll (public domain) used as honest, labelled illustration in the full
# Oriskany video (FOOTAGE_LIST.md, section "Generic US Government b-roll"). None of it shows the Oriskany.
# Files land in src/film/<stem>.mp4 (git-ignored). Resumable.
set -e
cd "$(dirname "$0")"; mkdir -p src/film
dl() { stem="$1"; url="$2"; [ -s "src/film/$stem.mp4" ] && [ -e "src/film/$stem.mp4.ok" ] && return
  for i in 1 2 3; do curl -sS -L -C - -o "src/film/$stem.mp4" "$url" && [ -s "src/film/$stem.mp4" ] && touch "src/film/$stem.mp4.ok" && echo "$stem ok" && break; sleep 5; done; }
NF=https://download.gallery.brightcove.com/api/gallery/account/659677166001/site/site-600408/video
# NOAA Fisheries b-roll packages (PD, credit "NOAA Fisheries"; slate lists any third-party clips: checked by eye)
dl noaa_snapper_school   $NF/5305427942001/download   # Red Snapper, Schooling (Gulf of Mexico)
dl noaa_snapper_recfish  $NF/5306967905001/download   # Red Snapper, Recreational Fishing (Gulf)
dl noaa_snapper_offload  $NF/5305793758001/download   # Red Snapper, Commercial Offload (Destin, FL)
dl noaa_barotrauma       $NF/5345612626001/download   # Snapper/Grouper with Barotrauma, Fish Descenders, Rec Fishing
dl noaa_corals_gulf      $NF/5231418011001/download   # Corals of the Atlantic, Gulf, Keys and Caribbean
dl noaa_coral_fgb        $NF/1553921798001/download   # Coral Reefs, Coral Spawning, and Fish (Flower Gardens NMS, Florida Keys NMS, NWHI)
dl noaa_dwh_sampleprep   $NF/906139606001/download    # Deepwater Horizon Seafood Sample Prep (Pascagoula lab, 6 May 2010)
dl noaa_dwh_fishsampling $NF/886018561001/download    # Deepwater Horizon Fish Sampling in the Gulf (6 May 2010)
# DVIDS (U.S. Navy, PUBLIC DOMAIN per each page)
dl dvids_828554 https://d34w7g4gy10iej.cloudfront.net/video/2201/DOD_108768698/DOD_108768698.mp4   # ex-Kitty Hawk towed from Bremerton, 15 Jan 2022
# NASA Goddard SVS (NASA media: not copyrighted; credit NASA/GSFC SVS)
dl nasa_gustav_3545 https://svs.gsfc.nasa.gov/vis/a000000/a003500/a003545/gustav831cloudHeightsparta1280x720_30.mp4   # Hurricane Gustav, 31 Aug 2008 (TRMM/GOES)
dl nasa_rita_3438   https://svs.gsfc.nasa.gov/vis/a000000/a003400/a003438/rita_1280x720.mp4                          # Hurricane Rita push-in, GOES IR, 18-25 Sep 2005
dl dvids_358436 https://d34w7g4gy10iej.cloudfront.net/video/1409/DOD_101923424/DOD_101923424-1024x576-1769k.mp4   # U.S. Navy MDSU-2 divers on a wreck, Cartagena, Colombia, 1 Sep 2014
dl dvids_791060 https://d34w7g4gy10iej.cloudfront.net/video/2104/DOD_108287411/DOD_108287411-1024x576-1769k.mp4   # decommissioned USS Fort McHenry departs Mayport under tow, 16 Apr 2021
