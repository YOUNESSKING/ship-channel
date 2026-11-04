# Template list (made by make_docs.py - do not edit by hand)

Time values ("at" fields): see README.md, section "Time values".


## black

Black hold (the silent drop, rule 30). Total silence: no sound events.

Variants: `hold`


## number_clip

Big number over a clip: kicker + number + hairline + italic subline (rule 15a). Number can count or be struck out and replaced.

Variants: `right`, `center_bars`, `left_stack`, `strike_swap`


| parameter | what it does |
|---|---|
| `kicker` | small caps line above the number, e.g. "Near the ice" |
| `number` | the big number text, e.g. "0°C" or "15-30" (use ° for degrees) |
| `unit` | italic word after the number, e.g. "minutes" |
| `subline` | small line under the number |
| `number_at` | when the number appears (time spec; default 0.6 s after shot start) |
| `subline_at` | when the subline appears |
| `size` | number size in px |
| `side` | variant right: "right" (default) or "left" |
| `count` | {"from":0,"to":-1.8,"decimals":1,"dur":1.2,"suffix":"°C"} - animate the number instead of showing it fixed |
| `jump_at` | time of an instant zoom step on the clip |
| `jump_scale` | zoom after the step (default 1.2) |
| `dim` | variant center_bars/strike_swap: dark shade strength "dk" (default) or "lt" |
| `lead1` | strike_swap: first small line ("The water") |
| `lead2` | strike_swap: second small line ("Salt water freezes at") |
| `old` | strike_swap: the number that gets struck out ("0°C") |
| `new` | strike_swap: the true number ("-1.8°C") |
| `show_at` | strike_swap: when lead1 + old number appear |
| `swap_at` | strike_swap: when lead1 changes to lead2 |
| `strike_at` | strike_swap: when the line strikes out the old number |
| `new_count` | strike_swap: true = new number counts from 0 to its value |

## lower_third

One-word / short italic lower third on a clip (rule 15b). For jokes and one-word labels.

Variants: `italic_word`, `two_part`, `kicker_line`


| parameter | what it does |
|---|---|
| `text` | main text |
| `at` | when it appears (time spec; default 0.3 s) |
| `size` | text size px (default 46, two_part 40) |
| `aside` | two_part: the italic aside, e.g. "(45 minutes away)" |
| `aside_at` | two_part: when the aside appears |
| `kicker` | kicker_line: small caps line |
| `jump_at` | instant zoom step on the clip |
| `jump_scale` | zoom after the step (default 1.14) |
| `joke_sound` | two_part: dry "tok" on the aside (default true) |
| `plain` | true (or "card": true in the shot, with no clip) = a text card on a dark picture, text in the middle, bigger |

## extinct_plate

Gold-framed plate on a clip: EXTINCT + date (rule 15c, rule 6). Also works for other one-fact plates (e.g. "UNKNOWN").

Variants: `right`, `center`, `left`


| parameter | what it does |
|---|---|
| `word` | big word, default "EXTINCT" |
| `date` | italic line, e.g. "3.6 million years ago" |
| `at` | when the plate fades in (time spec; default 0.4 s) |
| `sound` | false = no stamp sound |

## title_card

Chapter title card: kicker + name + hairline + date, over a dimmed clip, with whoosh + thud (rule 52).

Variants: `center_bars`, `left_plate`, `minimal`


| parameter | what it does |
|---|---|
| `kicker` | small caps line, e.g. "Chapter one" |
| `title` | chapter name |
| `date` | italic line, e.g. "20,000 years ago" |
| `date_at` | when the date appears (time spec; default 0.9 s) |
| `size` | title size px (auto-fit by default) |

## stick_gag

Generic stick gag that carries information: stick figure + big number + icon (+ optional timer bar). Use when none of the special gags fits (rule 9).

Variants: `text_right`, `icon_pair`


| parameter | what it does |
|---|---|
| `pose` | "tread" (default), "gasp", "float" or "sink" |
| `kicker` | small caps line |
| `number` | big number |
| `unit` | italic unit |
| `line` | italic line under the number |
| `number_at` | when the number shows (time spec) |
| `line_at` | when the line shows |
| `icon` | icon name (boat, wetsuit, lifering, bottle, flame, phone, fish, snowflake, thermometer, clock, hand, rope, shore, shark, penguin, person, orca, salt, mussel, dice, hut, bowl, river, tree, croc) or raw svg |
| `icon_label` | caps label under the icon |
| `icon_at` | when the icon pops |
| `cross` | draw a gold X over the icon 0.3 s later |
| `timer` | {"from":0,"to":1,"labels":[...]} - show the timer bar and move the marker |

## stick_land

Story gag: the figure falls from the top of the picture (as if dropped offshore) and lands on dry ground instead of water: soft thud, dust puff, a label on its word. Same figure and line style as stick_water (gap T4).

Variants: `grass`, `snow`


| parameter | what it does |
|---|---|
| `label` | word that appears after the landing (default "grass" / "snow") |
| `label_at` | when the label shows (time spec) |
| `land_at` | when the feet touch the ground (time spec; default 1.1 s) |
| `result` | optional italic line under the figure (e.g. "dry") |
| `result_at` | when the result line shows |
| `water_hint` | true = a faint dashed wave where the water should have been, which vanishes on landing (default true) |

## stick_rope

Story gag: a thrower in a boat throws a rope, it arcs over, then slips away. Two beats (rule 13).

Variants: `rope_slip`


| parameter | what it does |
|---|---|
| `label` | word on the rope ("rope") |
| `result` | final line ("can't hold it") |
| `throw_at` | when the arm throws and the rope draws (time spec) |
| `label_at` | when the label shows |
| `slip_at` | when the rope slips away and the arm drops |
| `result_at` | when the final line shows |

## stick_timer

Stick-figure body gag with the timer bar (rule 3, 9, 14): gasp (1 min), hand (10 min), lights_out (30 min). Same bar in every chapter.

Variants: `gasp`, `hand`, `lights_out`


| parameter | what it does |
|---|---|
| `kicker` | small caps line ("Cold shock") |
| `number` | big number ("1") |
| `unit` | italic unit ("minute") |
| `line` | italic line ("can't control your breathing") |
| `line_at` | when the italic line appears (time spec) |
| `from_stop` | timer start stop 0-3 (default per variant: gasp 0, hand 1, lights_out 2) |
| `to_stop` | timer end stop 0-3 |
| `labels` | four labels for the bar, default ["START","1 MIN","10 MIN","30 MIN"]; change them for heat/thirst/salt chains |
| `gasp_words` | gasp: the two shout words (default ["gasp","gasp"]) |
| `gasp_at` | gasp: list of 2 time specs |
| `sink_at` | lights_out: when the figure starts to sink |
| `dim_at` | lights_out: when the screen dims |
| `dim_to` | lights_out: final darkness 0-1 (default .72) |

## stick_walk

Story gag: the figure walks across a dry crossing between two places (two caps labels, a dashed path, a label on its word, then an italic result word). "channel" = a dry valley between two cliffs (England-France), "bridge" = a flat land bridge (gap T5).

Variants: `channel`, `bridge`


| parameter | what it does |
|---|---|
| `from_label` | caps label on the left land (default "ENGLAND") |
| `to_label` | caps label on the right land (default "FRANCE") |
| `label` | italic label over the crossing (e.g. "Channel Tunnel") |
| `label_at` | when the label shows (time spec) |
| `result` | big italic result word at the end (e.g. "walking") |
| `result_at` | when the result lands |
| `walk_at` | when the figure starts walking (default 0.3 s) |
| `walk_end` | when the figure arrives (default: 0.4 s before the end of the shot) |

## stick_water

Stick figure treading water, then a chain of beats in one shot: "you" label, crossed-out items (NO BOAT), measured distance to shore (rule 9, 10).

Variants: `sea`, `ice`


| parameter | what it does |
|---|---|
| `beats` | list of beats: {"kind":"you","label":"you","label_at":T} / {"kind":"items","at":T,"items":[{"icon":"boat","label":"NO BOAT","at":T}]} / {"kind":"distance","at":T,"label":"100 yards","label_at":T}. "at" = when the beat (a cut + zoom) starts. Icons: boat, wetsuit, lifering, bottle, flame, phone, fish, rope, hand ... |
| `cross` | items: draw a gold X on each item 0.3 s later (default true) |
| `shore_label` | ice variant: text on the ice edge (default "ICE") |

## scale_ruler

Constant ruler (rule 54): stick figure next to the animal (silhouette or on a clip) with a measure label. Scale is true: the animal is drawn as long, relative to a 1.75 m figure, as its real length.

Variants: `silhouette`, `water`, `clip`


| parameter | what it does |
|---|---|
| `animal` | silhouette name: shark, orca, bear, mammoth, leopard_seal, crocodile (or give "svg") |
| `svg` | your own silhouette: svg inner markup drawn in a 1000-unit-wide box, feet/belly line at y=0, facing right |
| `length_m` | animal length in metres (e.g. 6) |
| `label` | measure label text, e.g. "6 m (20 ft)"; default made from length_m |
| `name` | caps name under the animal, e.g. "GREAT WHITE SHARK" |
| `human_m` | figure height in metres (default 1.75) |
| `human_label` | tiny label next to the figure (default "you") |
| `animal_at` | when the animal shows (default 0.25 s) |
| `ruler_at` | when the ruler line draws (default 1.0 s) |
| `figure` | clip variant: {"x":150,"feet_y":620,"scale":1.0} where the figure stands |
| `span` | clip variant: {"x0":420,"x1":1100,"y":230} where the animal is in the picture (px) |

## problem_counter

"Problem one / problem two" counter overlay on a clip or plain dark (rule 55). The deciding problem can be marked gold.

Variants: `corner_badge`, `center_line`, `pips`


| parameter | what it does |
|---|---|
| `n` | which problem: 1, 2 or 3 |
| `total` | how many problems this chapter (default 2) |
| `title` | short italic name, e.g. "the cold" |
| `at` | when it appears (time spec; default 0.3 s) |
| `decider` | true = this is the problem that decides: gold ring + "THE DECIDING PROBLEM" |
| `word` | override the caps word (default "PROBLEM ONE" / "PROBLEM TWO") |
| `plain` | true = no clip, dark background |

## tier_board

Tier board (rules 7, 43, 58). "roadmap" = the empty board with ALL chapter tiles listed by name; "drop" = the tile is dragged and dropped on the verdict word (optionally a new tier row slides in first); "final" = the finished board with a slow camera move and glowing rows / lifted tiles; "final_wide" = the finished board, whole, fixed camera.

Variants: `roadmap`, `drop`, `final`, `final_wide`


| parameter | what it does |
|---|---|
| `title` | board title (default "How long would you last in each Ice Age ocean?") |
| `tiers` | list of [name, colour]; default Overnight/Hours/An hour/Minutes/Seconds |
| `tiles` | roadmap: list of {"name":"North Atlantic","image":"thumb.jpg"} - every chapter, in order (image optional) |
| `placed` | tiles already on the board: list of {"name","image","tier"} |
| `reveal_at` | roadmap: time spec of the first tile (default 0.5 s) |
| `stagger` | roadmap: seconds between tiles (default 0.18), or give "reveal_times": [specs] |
| `reveal_times` | roadmap: one time spec per tile |
| `tile` | drop: {"name":"North Atlantic","image":"thumb.jpg"} |
| `tier` | drop: tier the tile lands in (e.g. "Minutes") |
| `drop_at` | drop: time spec of the verdict word (the thud) |
| `slot_x` | drop: x of the landing spot (default: next free place in the row) |
| `cursor` | drop: show the cursor (default true) |
| `n_total` | drop: total chapters, picks the compact board when more than 6 (default 5) |
| `add_tier_at` | drop: time spec. A new tier row (the FIRST entry of "tiers", or "new_tier") slides in on top of the board at this moment, then the tile drops into it (gap T2: the "Days" row at chapter 9). Pass "tiers" with the new tier first. |
| `new_tier` | drop: name of the tier that slides in (default: first of "tiers") |
| `highlight_row` | final: tier name whose row glows gold (default none) |
| `highlight_at` | final: when the row glows (default 0.4 s) |
| `highlight_tiles` | final: list of {"name":"Bering Sea","at":T} - the tile lifts and gets a gold ring on its word, soft click; stays lifted |
| `pan` | final: camera move "bottom_to_top", "top_to_bottom", "focus" (stay on the highlighted row) or "none" (default: focus when a row is highlighted, else bottom_to_top) |
| `zoom` | final: camera zoom (default 1.45) |
| `focus_row` | final: tier name to centre on when pan is "focus" (default: highlight_row) |

## map_clip

Plays a pre-baked map video (any mp4) and, if you want, adds the style C overlays: pin ring + place name, date line, sea-level gauge (rules 1, 18-21).

Variants: `baked`, `labeled`, `gauge`


| parameter | what it does |
|---|---|
| `pin` | {"x":640,"y":330}  pin position in the 1280x720 picture (labeled variant) |
| `name` | place name, e.g. "North Atlantic" |
| `name_at` | when the pin + name appear (time spec) |
| `date` | bottom line, e.g. "LAST GLACIAL MAXIMUM · SEA LEVEL -120 M" (every variant) |
| `date_at` | when the bottom line shows |
| `gauge` | {"from":0,"to":-120,"at":"@four","dur":1.7,"x":930,"y":120,"label_ft":"(-400 ft)"}  sea-level gauge (gauge variant) |
| `credits` | small credits line bottom right (default none; maps baked by the map-kit already have it) |
| `zoom` | [from,to] slow zoom, default [1.0,1.0] (the baked map already moves) |
| `measure` | {"from":{"x":640,"y":210},"to":{"x":640,"y":520},"label":"1,000 km","at":"@thousand","dur":0.9,"label_side":"right"}  gold measure bar that draws between two points on a word (gap T8) |
| `inset` | {"pin":{"lat":20,"lon":38.5},"corner":"tl"/"tr"/"bl"/"br","w":300,"at":0.3,"label":"ICE AGE ICE SHEETS"}  small world map with the Ice Age ice sheets and a gold pin on the place (rule 18, gap T10); for places far from the ice |
| `polar` | {"center":[640,360],"two_r":1011,"pin":{"lat":-62,"lon":-40},"pin_name":"","rings":[{"lat":-60,"label":"TODAY'S WINTER EDGE","at":T,"label_lon":90},{"lat":-50,"label":"ICE AGE EDGE","at":T,"grow_from":-60,"dur":1.6}]}  overlays for the south-polar stereographic bake (gap T9): rings drawn by latitude (dashed gold), pin by lat/lon. two_r = 2*R in frame pixels (kit: 2170.5 at 2880 px wide, so about 1011 at zoom 1.05 in a 1280 frame) |

## clip_plain

Plain full-bleed clip with trim (in) and slow push. No text.

Variants: `push`, `pull`, `jump`


| parameter | what it does |
|---|---|
| `dim` | 0-1, optional dark shade over the clip (default 0 = none) |
| `jump_at` | variant jump: time of the zoom step (default: half of the shot) |
| `jump_scale` | variant jump: zoom after the step (default 1.14) |

## outro

Outro (gap T3). "question" = "Do you agree?" over the finished board (dimmed) with a gold italic line; "card" = the same on a dark picture without the board; "end_screen" = the 12 s end-screen layout (2 video slots + subscribe circle, music only, fades to black).

Variants: `question`, `card`, `end_screen`


| parameter | what it does |
|---|---|
| `question` | big line (default "Do you agree?") |
| `line` | gold italic line (default "Tell me where you would put it") |
| `line_at` | when the italic line shows (time spec; default 1.2 s) |
| `board` | question: true = show the finished board dimmed behind the text (default true; needs "placed") |
| `placed` | tiles on the board: list of {"name","image","tier"} |
| `tiers` | list of [name, colour] (default: the 6 final tiers, Days first) |
| `title` | board title (default "How long would you last in each Ice Age ocean?") |
| `bg` | end_screen: "board" (dimmed finished board, default) or "dark" |
| `slot_a` | end_screen: caps label under the left video slot (default "WATCH NEXT") |
| `slot_b` | end_screen: caps label under the right video slot (default "MORE ICE AGE") |
| `thanks` | end_screen: italic line on top (default "Thanks for watching") |
| `subscribe` | end_screen: caps label under the subscribe circle (default "SUBSCRIBE") |
| `fade_s` | end_screen: fade to black at the end, seconds (default 1.2) |
| `end_screen_s` | ignored (kept for old plans): use a separate end_screen shot |

## text_card

A text card with no clip: dark textured picture and text in the middle. For a one-word beat ("okay.", "just rivers"), a two-part joke, or a number on its own. Use it to split a long line into two cuts (text templates over clips are limited to 2 per chapter, rule 16; cards count on their own).

Variants: `word`, `pair`, `line`, `number`, `number_left`


| parameter | what it does |
|---|---|
| `text` | word / pair / line: the main text |
| `at` | when the text appears (time spec; default 0.3 s) |
| `size` | text size px |
| `aside` | pair: the italic aside (shown after the text) |
| `aside_at` | pair: when the aside appears |
| `joke_sound` | pair: dry "tok" on the aside (default true) |
| `kicker` | small caps line above (line, number, number_left) |
| `number` | number / number_left: the big number |
| `unit` | number: italic unit after the number |
| `subline` | number: small line under the number |
| `number_at` | number: when the number appears |
| `subline_at` | number: when the subline appears |
| `count` | number: {"from":0,"to":-1.8,"decimals":1,"dur":1.2,"suffix":"°C"} counting number |
| `dim` | number: dark shade "dk" (default) or "lt" |
