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
| `shore_label` | text on the pale shore (default "ICE") |
| `shore` | "palm" (sea default: warm island) or "ice" (pale cold shore with shore_label; ice default). Use "ice" for any cold or inland scene: no palm trees in the Ice Age |

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
| `glow` | roadmap: {"name":"Southern Ocean","at":T} - that tile gets a gold ring and lifts on its word (join.md: the next ocean glows on "south") |
| `stagger` | roadmap: seconds between tiles (default 0.18), or give "reveal_times": [specs] |
| `reveal_times` | roadmap: one time spec per tile |
| `tile` | drop: {"name":"North Atlantic","image":"thumb.jpg"} |
| `tier` | drop: tier the tile lands in (e.g. "Minutes") |
| `drop_at` | drop: time spec of the verdict word (the thud) |
| `note` | drop: small italic line next to the landed tile, e.g. "*in the water" |
| `note_at` | drop: when the note shows (default 0.5 s after the drop) |
| `slot_x` | drop: x of the landing spot (default: next free place in the row) |
| `cursor` | drop: show the cursor (default true) |
| `n_total` | drop: total chapters, picks the compact board when more than 6 (default 5) |
| `add_tier_at` | drop: time spec. A new tier row (the FIRST entry of "tiers", or "new_tier") slides in on top of the board at this moment, then the tile drops into it (gap T2: the "Days" row at chapter 9). Pass "tiers" with the new tier first. |
| `new_tier` | drop: name of the tier that slides in (default: first of "tiers") |
| `verdict` | drop: big verdict word shown on the drop (about 12 % of frame height, Cormorant, warm white, gold underline; style review 04/07) |
| `sting` | drop: "full" = music dips out 0.8 s before the word, riser, deep hit on the word (4 key verdicts only); "thud" = deep hit only (default when verdict is set) |
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
| `pin` | {"x":640,"y":330,"track":[[t,x,y],...]}  pin position in the 1280x720 picture (labeled variant); track = positions over the clip seconds when the bake moves (Video 02 map jsons) |
| `name` | place name, e.g. "North Atlantic" |
| `name_at` | when the pin + name appear (time spec) |
| `date` | bottom line, e.g. "LAST GLACIAL MAXIMUM · SEA LEVEL -120 M" (every variant) |
| `date_at` | when the bottom line shows |
| `gauge` | {"from":0,"to":-120,"at":"@four","dur":1.7,"x":930,"y":120,"label_ft":"(-400 ft)"}  sea-level gauge (gauge variant) |
| `credits` | small credits line bottom right (default none; maps baked by the map-kit already have it) |
| `pins` | [{"x":246,"y":240,"x0":251,"y0":245,"label":"","at":T}] many small gold pins that drift with the bake (pins_dur = bake seconds) |
| `pins_dur` | seconds the pins take to drift from x0,y0 to x,y (default: the shot) |
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
| `slots` | end_screen: false = no video slots, only the thanks line and the subscribe circle in the middle (default true) |
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

## anim_gauge

Count-up gauge on green ink. "bars" = 2-4 horizontal bars (e.g. you vs the animal), each with an icon / line-art / image and a label; the hero bar (last, or "hero":true) counts ~1.4 s and lands with flash + gold ring + deep hit. "meter" = one tall meter with reference marks (e.g. conversation / jet engine) that fills to the value and lands the same way.

Variants: `bars`, `meter`


| parameter | what it does |
|---|---|
| `kicker` | small caps title top left, *word* = gold italic (e.g. "Bite force") |
| `kicker_at` | when the kicker shows (default 0.2) |
| `unit` | italic unit after every number (e.g. "psi") |
| `decimals` | decimals of the numbers (default 0) |
| `max` | value at the full bar / meter top (default: largest value) |
| `items` | bars: [{"label":"YOU","value":160,"glyph":{"person":"you"} / {"shape":"croc"} / {"icon":"hand"} / {"image":"path.png"},"at":T,"count_at":T,"dur":1.4,"hero":true}] |
| `value` | meter: the value counted to |
| `label` | meter: caps label under the big number |
| `glyph` | meter: optional glyph next to the big number (as items) |
| `count_at` | meter: when the count starts (default 1.6) |
| `dur` | meter: count length (default 1.4) |
| `marks` | meter: reference marks [{"value":60,"label":"CONVERSATION","at":T}] |
| `note` | italic comparison line at the bottom (e.g. "more than six times yours") |
| `note_at` | when the note shows (default land + 1.3) |
| `circle` | true = a gold marker circle is drawn round the hero number after the land |
| `circle_at` | when the circle draws (default land + 0.8) |

## anim_lockon

Lock-on hook scene: "jungle" = night jungle (parallax trees, vines, fronds, light rays, mist, fireflies); "river" = night river bank (far tree line, reeds, water with glints, eyes on the water surface); "eyes_room" = dark room that fills with blinking eyes. The figure walks in, eyes appear, gold brackets lock on with a held beep, kicker line, heartbeat rings, optional animal slides in.

Variants: `jungle`, `river`, `eyes_room`


| parameter | what it does |
|---|---|
| `who` | the target: you / explorer (head torch beam) / scientist / hunter / honey / worker / child (default you) |
| `target_x` | where the figure stops (x px, default 400 / 330) |
| `walk_dur` | walk-in seconds (default up to the lock; 0 = already standing) |
| `eyes_at` | when the eyes open (default 1.8) |
| `eyes` | [x,y] of the eyes (default by variant) |
| `lock_at` | when the brackets snap (default 3.2) |
| `beep` | held beep length in s (default 1.0) |
| `kicker` | caps line, *word* = gold italic (default "IT ALREADY *sees* YOU"; "" = none) |
| `kicker_at` | default lock + 0.45 |
| `animal` | optional {"image":"path.png"} / {"shape":"croc"} (+ "w": width px, "y": ground y) sliding in from the right |
| `animal_at` | default lock + 1.8 |
| `heart` | true = heartbeat rings speeding up after the lock (heart sound), or a list of times |
| `hud` | small place/time caption top left (e.g. "SUNDARBANS · 02:14 AM") |
| `distance` | optional readout {"from":38,"to":12,"unit":"m","label":"DISTANCE","at":T,"dur":1.9} |
| `rain` | true = light rain (jungle) |

## anim_options

"What would you do?" spine: title + rows that click in, gold box on the current row, gold strike-through on finished rows, verdict line. "list" = centred list; a row's mini scene replaces the list for its time, then the list comes back. "side" = list on the left, mini scenes play in a gold-framed panel on the right.

Variants: `list`, `side`


| parameter | what it does |
|---|---|
| `title` | caps title, *word* = gold italic (default "What would you do?") |
| `title_at` | default 0.25 |
| `items` | [{"text":"Run","at":T,"box_at":T,"strike_at":T,"scene":{"type":"run/climb/hide/swim/stand","at":T,"dur":3,"label":"TIGERS RUN 60 KM/H","animal":{"image":"tiger.png"} / {"shape":"croc"}}}] |
| `numbered` | true = "1. Run" (default true) |
| `chosen` | item field: true = the final answer; ONLY this row gets the gold box (after the last strike, held to the shot end, >= 1.5 s). Struck rows never get a box. |
| `hair` | true = gold hairline under the title (default false: it read as a stray underline) |
| `scrim` | dark ellipse behind the list for a moving bg_clip (default: on when the shot has bg_clip) |
| `verdict` | italic line at the end (e.g. "Bad plan.") |
| `verdict_at` | when the verdict shows |

## anim_xray

Gold X-ray mode: "human" = the stick figure "you" switches to a gold X-ray body; "animal" = a line-art animal (croc_gfx shapes: croc, monitor, theropod, fish ...) or a tinted image as a gold X-ray. One organ glows and pulses (heart beats with the heart sound, lungs breathe), a scan line sweeps, readouts pop in with leader lines.

Variants: `human`, `animal`


| parameter | what it does |
|---|---|
| `organ` | heart / lungs / brain / gut / gland / dot (default heart) |
| `organ_pos` | animal: [fx, fy] = share of the length from the tail end, share of the height above the belly |
| `organ_size` | organ radius px (default by variant) |
| `organ_label` | caps label next to the organ (e.g. "SALT GLANDS") |
| `organ_at` | when the organ lights up (default xray_at + 0.5) |
| `xray_at` | human: when the normal figure turns into the X-ray (default 0.6; 0 = X-ray from the start) |
| `who` | human: the role before the switch (you / scientist / ...) |
| `shape` | animal: croc_gfx shape (default croc) |
| `image` | animal: optional image path drawn gold-tinted instead of the shape |
| `animal_w` | animal: length px (default 980) |
| `bpm` | heart beat rate (default 70; beats get the heart sound) |
| `heart_sound` | false = no heart sound |
| `scan` | false = no scan line |
| `readouts` | [{"text":"HEART RATE *40 bpm*","at":T}] labels with leader lines |
| `kicker` | caps title top left, *word* = italic |
| `kicker_at` | default 0.2 |
| `line` | italic line at the bottom |
| `line_at` | when the line shows |

## croc_gfx

Video 02 graphics: "size_chart" = rivals and our 5 m croc in lanes at true scale next to a 1.8 m human, metre grid, ruler + label per animal (rule 54); "lineup" = rival silhouettes in a row that fade out one by one; "footprints" = three-toed prints walk along a river bank; "heads" = phytosaur vs crocodile head profiles (nostril circles or a "not related" sign); "count" = N different crocodilian silhouettes pop in with a big number; "tooth_banana" = a Deinosuchus tooth next to a banana on a cm ruler; "teeth" = a blade-like serrated tooth next to a cone tooth; "debate" = two Spinosaurus silhouettes, wading vs swimming, with a big "?".

Variants: `size_chart`, `lineup`, `footprints`, `heads`, `count`, `tooth_banana`, `teeth`, `debate`


| parameter | what it does |
|---|---|
| `items` | size_chart: list of {"shape":"croc/theropod/spino/snake/sawfish/fish/monitor/amphibian/slim/skull/bus/car","lane":"bank" (same lane = same ground line),"length_m":7,"min_m":4.5 (optional range),"name":"SMILOSUCHUS","label":"7 m","at":T,"ours":true (warm white = our croc)} drawn top to bottom; lineup: list of {"shape","name","fade_at":T} |
| `human_m` | size_chart: human height (default 1.8) |
| `human_label` | size_chart: label under the human (default "human") |
| `kicker` | small caps line top left |
| `note` | big italic gold line top right (e.g. "8x heavier") |
| `note_at` | when the note shows |
| `line` | italic line at the bottom (lineup / footprints / heads / count) |
| `line_at` | when the line shows |
| `prints_at` | footprints: time of the first print (prints follow every 0.35 s) |
| `label` | footprints / count: caps label |
| `mode` | heads: "nostrils" (circles land on nostril_at / tip_at) or "unrelated" (a not-equal sign lands on line_at) |
| `nostril_at` | heads: when the circle on the phytosaur nostrils lands |
| `tip_at` | heads: when the circle on the croc snout tip lands |
| `n` | count: how many silhouettes (default 7) |
| `number_at` | count: when the big number lands |
| `stagger` | count / lineup: seconds between silhouettes |
| `a_at` | tooth_banana / teeth / debate: when the first object shows |
| `b_at` | tooth_banana / teeth / debate: when the second object (or the "?") shows |
| `a_label` | teeth / debate: label of the left object |
| `b_label` | teeth / debate: label of the right object |

## croc_stick

Video 02 stick gags with the line-art croc: checklist (icons on their words), run_away (person runs from a labelled millipede), bite_car (car lands on the tooth row + number), mud_timer (croc in a mud pool + the timer bar), tally (two counters), lizard_car (lizard grows to car length), swim_route (dotted sea route between two river mouths + distance), temp_bar (body temperature falls in steps, labels on words), days_bar (the timer bar for a cold snap; can run off the edge), wrap (snake loops round the croc, two lengths), thermo (thermometer rises into the danger zone + number), eight (eight small crocs = one giant), roll (croc tries to roll, "?"), bite_bars (bar chart of two bite forces), eyes (only the eyes above water while a giant walks past on the bank), buffet (a giant croc with a fork, a small croc served on a plate).

Variants: `checklist`, `run_away`, `bite_car`, `mud_timer`, `tally`, `lizard_car`, `swim_route`, `temp_bar`, `days_bar`, `wrap`, `thermo`, `eight`, `roll`, `bite_bars`, `eyes`, `buffet`


| parameter | what it does |
|---|---|
| `kicker` | small caps line (top) |
| `number` | big number |
| `unit` | italic unit after the number |
| `number_at` | when the number lands |
| `line` | italic line |
| `line_at` | when the italic line shows |
| `label` | caps / italic label of the main object |
| `label_at` | when the label shows |
| `items` | checklist: [{"icon":"thermometer","label":"TEMPERATURE","at":T}]; temp_bar: [{"label":"can't warm up","at":T}]; bite_bars: [{"label":"OUR CROC","value":16000,"max":null,"text":"16,000 N","at":T}] |
| `labels` | mud_timer / days_bar: the four timer-bar labels |
| `from_stop` | timer start stop 0-3 |
| `to_stop` | timer end stop 0-3, or 4 = run off the right edge |
| `move_at` | when the marker / croc / snake / lizard starts moving |
| `move_dur` | how long the move takes |
| `a` | tally: {"label":"AMERICAN CROCODILES","from":0,"to":151,"at":T} |
| `b` | tally: {"label":"ALLIGATORS","value":0} |
| `at2` | second beat (run_away: "(probably)"; roll: "?") |

## v02_anim_a

V02 fix-pass scenes, batch A: "s01_checks" = the four checks as a list spine with icons + gold box (R05); "s02_ladder" = the tier ladder: our croc steps down Dominate > Establish > Survive (R09); "s03_bite" = bite-force bars, amphibians stop short, our croc counts to 16,414 N (C01-17); "s04_fire" = coal-swamp fires, the croc slides into the water (C01-21); "s05_mud" = croc waits in the mud, HOBBIES card, then WATER | BANK split (C02-21); "s06_temp" = thermometer counts to 14 C, frost below the line, empty riverbank (C03-14).

Variants: `s01_checks`, `s02_ladder`, `s03_bite`, `s04_fire`, `s05_mud`, `s06_temp`


| parameter | what it does |
|---|---|
| `at` | dict of beat name -> time spec (override the default beats of the variant; see BEATS in the module) |
| `value` | s03_bite: our bite value (default 16414) |
| `unit` | s03_bite: unit (default N) |

## v02_anim_b

Video 02 fix pass, batch B custom scenes (PLAN.md S07-S13): "xray_palate" = croc head X-ray, bony roof + throat flap, holds prey underwater and breathes (S07); "xray_salt" = drying creek, backlit giants, our croc leaves along a gold path, X-ray salt glands (S08); "lake_lock" = Turkana lakeshore, gold ticks over the herds, camera to the water, lock-on brackets find the giant (S09); "scientist" = scientist + clipboard, ? card, shrug, quote types in, pan to the early humans (S10); "xray_hippo" = cold Thames, hippo vs croc in gold X-ray, heat / no heat, three gold X (S11); "sea_options" = way-out list, escape by sea, North Sea in winter mini scene, strike (S12); "body_temp" = basking croc, body-temperature gauge lands 32-33 C, dive + energy bars drain, croc hides in the shade (S13).

Variants: `xray_palate`, `xray_salt`, `lake_lock`, `scientist`, `xray_hippo`, `sea_options`, `body_temp`


| parameter | what it does |
|---|---|
| `at` | optional dict of beat times {"name": time spec} overriding the word-based defaults of the variant (see the BEATS table in the code) |
| `kicker` | optional caps kicker override (*word* = gold italic) |

## v02_anim_c

Video 02 fix-pass scenes, batch C (S14-S19 + Kem Kem quote). Beats are fixed to the V02 narration words. hides_eats passes its params to anim_options/list.

Variants: `special_move`, `death_roll`, `bite_gauge`, `not_noticed`, `hides_eats`, `cold_enemy`, `kemkem_quote`


| parameter | what it does |
|---|---|
| `ours` | bite_gauge: our bite (default 16414) |
| `value` | bite_gauge: Purussaurus bite (default 50000, shown with "+") |
| `unit` | bite_gauge: default N |
| `max` | bite_gauge: value at the full bar (default 52000) |
| `row_at` | bite_gauge: Purussaurus row |
| `count_at` | bite_gauge: count start |
| `land_at` | bite_gauge: land |
| `items` | hides_eats: as anim_options |
| `title` | hides_eats: as anim_options |
| `title_at` | hides_eats: as anim_options |
| `numbered` | hides_eats: as anim_options |
| `subline` | hides_eats: italic line at the bottom ("in a river full of *fish*") |
| `subline_at` | hides_eats: when it shows |
| `thicken_at` | hides_eats: when the fish shoal thickens |
| `glow_at` | hides_eats: when all rows glow |
| `copies_at` | bite_gauge: times of the three copies of our bar |
