# Critique 2 (CTR): USS Ranger thumbnails v2a (first build)
Builder `make_thumbs_v2.py`. Looked at: `round1_sidebar_v2a.png` (168x94, colour + grey) and the 246x138 montage, plus 640x360 previews.
Pixel check (mean luminance / blue share / size): T1 0.46 / 64 % / 383 KB; T2 0.49 / 48 % / 254 KB; T3 0.62 / 42 % / 258 KB; T4 0.58 / 39 % / 250 KB. All bright enough, all blue-led, all < 2 MB.
Words and boxes keep clear of the bottom-right 300x160 and the top-right hover zone in all four. Title context: a "one cent" promise ("what happened to her").

| Draft | Words | Ship readable at 168x94 | Grey test | Rank | Verdict |
|---|---|---|---|---|---|
| T1 aerial 1988 | WORTH 1¢? | Yes: whole flight deck, jets, wake, on a bright blue sea. Slightly small, "1¢?" box covers the wake | Box goes mid-grey, white word still reads | 1 | Best sea and clearest "carrier". Question mark = curiosity gap |
| T2 bow-on 1993 | ONE CENT | Yes: tall bow, island, crowded deck, the most "this is a carrier" silhouette | Reads | 2 | Best picture, words too small ("CENT" is a 125 px label), box nearly touches bottom edge |
| T3 the tow 2015 | FOR 1¢ | Yes: huge hull, tug | Reads | 3 | Whole rusting hull is the payoff image; sky is near white, water over-cyan, left part of the hull cut |
| T4 split | 1¢ | Left half yes, right half hull small | "1¢" strong | 4 | Diagonal seam is neat, but two small ships; box is the loudest thing and blocks the sky between them; blue band under the tow hull = grade bleeding onto the hull |

Fixes for build 2:
1. T1: crop tighter so the carrier is 20 % bigger; keep words top-left.
2. T2: enlarge ONE / CENT (CENT to ~170 px), keep the whole box inside the frame with margin; soften the dark halo by the bow (lower the sea lift).
3. T3: water less cyan, keep a hint of sky colour (sea-only grade, sky untouched), include the full bow at left, raise the sea-mask line so the hull is not touched.
4. T4: smaller box, move the waterline mask so no blue band on the hull.
5. Bright areas: T3 sky is the only near-white zone, acceptable (not a video shot).
