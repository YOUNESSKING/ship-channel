# tools/grade: one colour grade for ship videos

`ship_grade.py` = per-source normalisation (cast removed, matched black / white points, saturation pulled to one target, B&W and
sepia sources made neutral grey) + one fixed LOOK (light teal shadows, warm-cream highlights, +5 % contrast) that sits with the map-kit
palette. Maps are the reference and are not graded.

- Archive shots: `tools/maps/archive_shots.py` shot key `"grade": "ship"` or env `ARCHIVE_GRADE=ship` (photos and film). With the grade
  on, the photo vignette drops from 0.32 to a light 0.14.
- Chapter clips that were not built through archive_shots: `GRADE=ship_archive` (templates/grade/ship_archive.vf = LOOK only).
  Do not stack it on segments already graded with `"grade": "ship"`.
- Check: `python3 tools/grade/ship_grade.py --sheet OUT.jpg --map MAP.mp4 photo.jpg clip.mp4@1.0 ...` -> before / after sheet.
  Preview: `preview/grade_sheet.jpg` (2006 photos, 1952 B&W film, 1966 / 1968 Kodachrome film, the dive map).
