"""Shot table for the 48 clean Video 01 map bakes (read by bake_run.py). Timing (length, gauge time) comes from v01_map_plan.json.
VIEWS: basemap canvas (2880x1620 at tile zoom z, Web-Mercator; or south-polar stereographic). The planner's "zoom" numbers in needs.json are tile zooms for a
2880-px canvas, which is far too wide at z3-z4, so z is re-chosen here per place (see maps/README.md).
SHOT keys: view; s=(s0,s1) camera scale (1.0 = canvas pixels 1:1; 0.667 = whole canvas); pin=(lat,lon) anchors the camera so the pin stays at its planned screen
position (zoom is about the pin) ; center=[(lat,lon),(lat,lon)] camera path when there is no pin; pan=(t0,t1);
sl=(from,to) sea level, timed by the template gauge (plan) or sl_t=(t0,dur); p=(p0,p1) ice progress; extras; inset=True adds the world inset with ice sheets."""
VIEWS = {
 "polar_s":   dict(proj="polar", lat=-90, lon=0, mpp=6626, rot0=0, zt=5, exag=1.0),
 "weddell":   dict(proj="polar", lat=-72, lon=-50, mpp=2600, rot0=130, zt=6, shelf_edge=-600, exag=1.0),
 "bering":    dict(proj="merc", lat=63.5, lon=-168, z=5.3),
 "bering_w":  dict(proj="merc", lat=63, lon=-165, z=4.8),
 "bering_s":  dict(proj="merc", lat=58.5, lon=-172, z=5.7),
 "npacific":  dict(proj="merc", lat=58, lon=-150, z=4.7),
 "northsea":  dict(proj="merc", lat=56, lon=5, z=5.5),
 "dogger":    dict(proj="merc", lat=53.5, lon=2.5, z=6.0),
 "baltic":    dict(proj="merc", lat=60, lon=16, z=5.6),
 "britain":   dict(proj="merc", lat=54.5, lon=-3, z=6.0),
 "channel":   dict(proj="merc", lat=51, lon=-1.5, z=6.6),
 "channel2":  dict(proj="merc", lat=50, lon=-2, z=7.0),
 "blacksea":  dict(proj="merc", lat=46, lon=33, z=5.6),
 "bosporus":  dict(proj="merc", lat=41.5, lon=29.5, z=7.2),
 "caucasus":  dict(proj="merc", lat=42.3, lon=43, z=7.0),
 "wmed":      dict(proj="merc", lat=40, lon=3, z=5.9),
 "gibraltar": dict(proj="merc", lat=36, lon=-5.5, z=7.4),
 "cmed":      dict(proj="merc", lat=42, lon=12, z=6.5),
 "iberia":    dict(proj="merc", lat=40, lon=-4, z=6.4),
 "lion":      dict(proj="merc", lat=43, lon=4, z=7.2),
 "redsea":    dict(proj="merc", lat=20, lon=39, z=6.3),
 "babel":     dict(proj="merc", lat=13, lon=43, z=7.4),
 "sahul":     dict(proj="merc", lat=-11, lon=138, z=5.7),
 "carp":      dict(proj="merc", lat=-13, lon=139, z=6.7, lake=dict(seed=(-14, 139.2), level=-30, box=(-17.8, -10.8, 135.5, 141.2))),
 "gulfmex":   dict(proj="merc", lat=28, lon=-90, z=5.6),
 "florida":   dict(proj="merc", lat=27, lon=-83, z=6.6),
 "newmexico": dict(proj="merc", lat=33, lon=-106, z=6.5),
 "sunda":     dict(proj="merc", lat=2, lon=108, z=6.2),
 "seasia":    dict(proj="merc", lat=5, lon=115, z=5.6),
 "bering_km": dict(proj="merc", lat=63.5, lon=-168, z=4.6),
 "pacific":   dict(proj="merc", lat=52, lon=-130, z=6.0),
 "namerica":  dict(proj="merc", lat=40, lon=-100, z=4.9),
 "world":     dict(proj="merc", lat=20, lon=10, z=3.4),
}
PLAN_PIN = "plan"     # use the pin screen position planned in the chapter JSON
A = lambda **k: k
GOLD_ = (201, 164, 92); KELPG = (120, 190, 110)
KELP = [(66, -169), (62, -168), (58, -158), (56, -146), (54, -136), (50, -129), (46, -125), (41, -124.5), (36.5, -122.3)]
SHOTS = {
 "MAP_02a": A(view="polar_s", s=(0.86, 0.94), sl=(-120, -120), p=(0.85, 1.0), pin=(-62, -40), free_pin=True),
 "MAP_02b": A(view="polar_s", s=(0.72, 0.76), sl=(-120, -120), p=(1.0, 1.0), extras=[
     dict(k="icering", lat0=-60, lat1=-50, t0=0.6, t1=4.6)]),
 "MAP_02c": A(view="weddell", s=(0.80, 0.86), sl=(0, -120), p=(0.3, 1.0), p_t=(0.4, 4.4), extras=[dict(k="zoneline", t0=2.9)]),
 "MAP_03a": A(view="bering", s=(0.74, 0.86), sl=(0, 0), p=(1.0, 1.0), pin=(66, -169)),
 "MAP_03b": A(view="bering", s=(0.78, 0.82), sl=(0, -120), p=(0.45, 1.0), center=[(64.5, -168), (64.5, -168)]),
 "MAP_03c": A(view="bering_w", s=(0.80, 0.86), sl=(-120, -120), p=(0.9, 1.0), pin=(65, -168), extras=[
     dict(k="glow", boxes=[(52, 72, -180, -150), (52, 72, 160, 180)], t0=0.3, t1=1.4)]),
 "MAP_03d": A(view="bering_s", s=(0.86, 0.9), sl=(-120, -120), p=(0.9, 1.0), pin=(57.5, -172), pan=((61, -172), 0.0, 2.6), extras=[
     dict(k="line", pts=[(53, -153), (52.5, -160), (53.5, -167), (55.5, -174), (58, -179)], t0=0.6, t1=2.4, dash=(26, 18), color=(236, 224, 196), w=3)]),
 "MAP_03e": A(view="bering_w", s=(0.95, 0.70), sl=(-120, -120), p=(1.0, 1.0), center=[(63, -166), (62, -165)]),
 "MAP_03f": A(view="npacific", s=(0.74, 0.82), sl=(-120, -120), p=(0.95, 1.0), pin=(64, -165), extras=[
     dict(k="glow", boxes=[(52, 72, -180, -150), (52, 72, 160, 180)], t0=0.0, t1=1.0, alpha=0.25)]),
 "MAP_04a": A(view="northsea", s=(0.72, 0.82), sl=(0, 0), p=(0.95, 1.0), pin=(56, 3)),
 "MAP_04b": A(view="northsea", s=(0.76, 0.82), sl=(0, -120), p=(0.45, 1.0), center=[(55, 2), (55, 2)]),
 "MAP_04c": A(view="dogger", s=(0.84, 0.92), sl=(-120, -120), p=(0.95, 1.0), pin=(54.5, 2), extras=[
     dict(k="walk", pts=[(51.5, -0.1), (51.8, 1.5), (52.1, 3.2), (52.4, 4.9)], t0=1.2, t1=3.8)]),
 "MAP_04d": A(view="baltic", s=(0.80, 0.90), sl=(-120, -120), p=(0.9, 1.0), pin=(58, 19)),
 "MAP_04e": A(view="britain", s=(0.80, 0.88), sl=(-120, -120), p=(0.9, 1.0), pin=(53, -1.5), extras=[
     dict(k="dots", pts=[(51.3, -1.8), (51.9, 0.2), (52.4, -1.2), (51.2, 1.2), (52.9, 0.6)], t_in=0.2, t_out=2.4, r=7)]),
 "MAP_04f": A(view="channel", s=(0.80, 0.86), sl=(0, -120), p=(0.5, 1.0), pin=(50.3, -1)),
 "MAP_04g": A(view="channel2", s=(0.82, 0.88), sl=(-120, -120), p=(1.0, 1.0), center=[(50.3, -1.5), (50.3, -1.5)], extras=[
     dict(k="line", pts=[(51.8, -1.6), (51.5, 0.2), (51.6, 1.0), (51.9, 1.7)], t0=0.2, t1=1.4, color=(150, 205, 235), w=4),
     dict(k="line", pts=[(51.9, 6.2), (52.0, 4.5), (52.2, 3.0), (51.9, 1.7)], t0=0.2, t1=1.4, color=(150, 205, 235), w=4),
     dict(k="line", pts=[(49.4, 0.5), (49.6, -0.8), (49.8, -2.2), (49.9, -3.2)], t0=0.6, t1=1.8, color=(150, 205, 235), w=4),
     dict(k="line", pts=[(51.9, 1.7), (51.0, 1.4), (50.5, 0.0), (50.1, -2.0), (49.9, -3.2), (49.6, -5.2), (49.2, -7.5), (48.8, -9.5)], t0=1.5, t1=4.2, color=(190, 230, 250), w=6)]),
 "MAP_05a": A(view="blacksea", s=(0.74, 0.84), sl=(0, 0), p=(0.95, 1.0), pin=(43, 34)),
 "MAP_05b": A(view="bosporus", s=(0.80, 0.86), sl=(0, -120), p=(0.45, 1.0), pin=(41.1, 29.05), inset=True),
 "MAP_05c": A(view="blacksea", s=(0.80, 0.86), sl=(-120, -120), p=(1.0, 1.0), center=[(46, 33), (46, 33)], extras=[
     dict(k="line", pts=[(48.5, 12), (47.5, 18), (45, 22), (44.3, 26.5), (45.2, 29.4)], t0=0.6, t1=2.2, color=(150, 205, 235), w=5),
     dict(k="line", pts=[(53.5, 31), (51, 31.2), (49, 33.5), (47.5, 33), (46.3, 32)], t0=1.6, t1=3.2, color=(150, 205, 235), w=5),
     dict(k="lake", seed=(43.5, 34), t0=0.4, t1=3.4, color=(96, 150, 180), alpha=0.5)]),
 "MAP_05d": A(view="blacksea", s=(0.80, 0.86), sl=(-120, -120), p=(1.0, 1.0), center=[(45, 36), (45, 37.5)]),
 "MAP_05e": A(view="caucasus", s=(0.80, 0.88), sl=(-120, -120), p=(1.0, 1.0), pin=(42.3, 43.1)),
 "MAP_05f": A(view="bosporus", s=(0.80, 0.84), sl=(-120, 0), sl_t=(0.7, 2.2), p=(0.55, 0.2), center=[(41.5, 29.5), (41.5, 29.5)], inset=True, extras=[
     dict(k="arrow", pts=[(40.6, 27.2), (40.9, 28.6), (41.4, 29.5), (42.0, 30.5)], t0=1.3, t1=3.0, color=(150, 205, 235), w=8)]),
 "MAP_06a": A(view="wmed", s=(0.76, 0.86), sl=(0, 0), p=(0.95, 1.0), pin=(36, -5.5), inset=True),
 "MAP_06b": A(view="gibraltar", s=(0.80, 0.86), sl=(0, -120), p=(0.5, 1.0), center=[(36, -5.5), (36, -5.5)], inset=True),
 "MAP_06c": A(view="cmed", s=(0.76, 0.84), sl=(-120, -120), p=(1.0, 1.0), center=[(41.5, 11.5), (41.5, 11.5)], inset=True),
 "MAP_06d": A(view="iberia", s=(0.78, 0.86), sl=(-120, -120), p=(1.0, 1.0), pin=(39, -4), inset=True, extras=[
     dict(k="glow", boxes=[(36, 43.6, -9.5, 3.5)], t0=0.2, t1=1.4, alpha=0.22)]),
 "MAP_06e": A(view="lion", s=(0.80, 0.86), sl=(-120, 0), p=(1.0, 0.7), center=[(42.8, 4), (42.8, 4)], inset=True, extras=[
     dict(k="dots", pts=[(42.5, 4.2), (42.2, 4.8), (42.8, 3.7), (42.0, 4.1)], t_in=0.2, t_out=5.5, r=8, sink=True)]),
 "MAP_07a": A(view="redsea", s=(0.76, 0.86), sl=(0, 0), p=(1.0, 1.0), pin=(20, 38.5), inset=True),
 "MAP_07b": A(view="babel", s=(0.82, 0.90), sl=(0, 0), p=(1.0, 1.0), pin=(12.6, 43.3), inset=True, extras=[
     dict(k="ring", pt=(12.6, 43.3), r=90, t0=1.5)]),
 "MAP_07c": A(view="babel", s=(0.82, 0.86), sl=(0, -120), p=(0.5, 1.0), center=[(13, 43), (13, 43)], inset=True),
 "MAP_08a": A(view="sahul", s=(0.76, 0.86), sl=(0, 0), p=(1.0, 1.0), pin=(-14, 139), inset=True),
 "MAP_08b": A(view="sahul", s=(0.78, 0.84), sl=(0, -120), p=(0.5, 1.0), center=[(-10, 138), (-10, 138)], inset=True),
 "MAP_08c": A(view="carp", s=(0.80, 0.88), sl=(-120, -120), p=(1.0, 1.0), center=[(-13, 139), (-13, 139)], inset=True, extras=[
     dict(k="lake", t0=0.4, t1=2.4, color=(110, 175, 205), alpha=0.55, use_view_lake=True)]),
 "MAP_08d": A(view="carp", s=(0.80, 0.84), sl=(-120, -60), p=(1.0, 0.45), center=[(-13, 139), (-13, 139)], inset=True, extras=[
     dict(k="lake", t0=0.0, t1=0.1, color=(110, 175, 205), alpha=0.55, use_view_lake=True, t_out=(2.4, 2.9))]),
 "MAP_09a": A(view="gulfmex", s=(0.74, 0.84), sl=(0, 0), p=(1.0, 1.0), pin=(25, -90)),
 "MAP_09b": A(view="gulfmex", s=(0.78, 0.84), sl=(0, -120), p=(0.5, 1.0), center=[(27, -88), (27, -88)]),
 "MAP_09c": A(view="florida", s=(0.82, 0.90), sl=(-120, -120), p=(1.0, 1.0), pin=(27, -82), inset=True, extras=[
     dict(k="coast"), dict(k="glow", boxes=[(24, 31, -87.5, -82.5)], t0=0.2, t1=1.3, alpha=0.3)]),
 "MAP_09d": A(view="gulfmex", s=(0.90, 0.98), sl=(-120, -120), p=(1.0, 1.0), pin=(28.5, -89.5), extras=[
     dict(k="line", pts=[(37, -89.5), (34.5, -90.8), (32, -91.2), (30.4, -91.3), (29.6, -90.4), (28.6, -89.6)], t0=0.2, t1=2.4, color=(150, 205, 235), w=5)]),
 "MAP_09e": A(view="newmexico", s=(0.80, 0.90), sl=(-120, -120), p=(1.0, 1.0), pin=(32.8, -106.3), inset=True),
 "MAP_10a": A(view="sunda", s=(0.74, 0.84), sl=(0, 0), p=(1.0, 1.0), pin=(2, 108), inset=True),
 "MAP_10a2": A(view="sunda", s=(0.80, 0.86), sl=(0, 0), p=(1.0, 1.0), center=[(0, 108), (0, 108)], inset=True),
 "MAP_10b": A(view="sunda", s=(0.78, 0.84), sl=(0, -120), p=(0.5, 1.0), center=[(2, 108), (2, 108)], inset=True),
 "MAP_10c": A(view="sunda", s=(0.78, 0.82), sl=(-120, -120), p=(1.0, 1.0), center=[(2, 108), (2, 108)], inset=True, extras=[dict(k="alaska", t0=0.2, t1=1.5)]),
 "MAP_10d": A(view="sunda", s=(0.78, 0.86), sl=(-120, -120), p=(1.0, 1.0), pin=(3, 107), inset=True, extras=[dict(k="coast")]),
 "MAP_10e": A(view="sunda", s=(0.80, 0.86), sl=(-120, -120), p=(1.0, 1.0), center=[(2, 108), (2, 108)], inset=True, extras=[
     dict(k="line", pts=[(1.5, 103), (2.4, 105), (3.6, 106.6), (5, 108), (6.6, 109.6), (8, 110.6)], t0=0.3, t1=2.2, color=(150, 205, 235), w=5),
     dict(k="line", pts=[(-3, 108), (-4.2, 110), (-4.9, 113), (-4.5, 115.5), (-4.0, 117.5)], t0=1.2, t1=3.0, color=(150, 205, 235), w=5)]),
 "MAP_10f": A(view="sunda", s=(0.80, 0.84), sl=(-120, 0), p=(1.0, 0.3), center=[(2, 108), (2, 108)], inset=True),
 "MAP_10g": A(view="seasia", s=(0.80, 0.86), sl=(0, 0), p=(1.0, 1.0), center=[(5, 113), (5, 113)], inset=True, extras=[
     dict(k="arrow", pts=[(1, 108), (6, 106), (12, 102), (14.5, 101.5)], t0=0.5, t1=2.2, color=(236, 224, 196), w=6),
     dict(k="arrow", pts=[(1, 109), (5, 112), (10, 115), (14, 109)], t0=0.9, t1=2.6, color=(236, 224, 196), w=6),
     dict(k="arrow", pts=[(0, 110), (-2, 116), (-4, 122), (-3, 126)], t0=1.3, t1=3.0, color=(236, 224, 196), w=6),
     dict(k="arrow", pts=[(2, 109), (4, 116), (8, 120), (11, 122)], t0=1.7, t1=3.4, color=(236, 224, 196), w=6)]),
 "MAP_F":   A(view="world", s=(0.70, 0.76), sl=(0, -120), p=(0.5, 1.0), center=[(18, 10), (18, 10)], extras=[
     dict(k="glow", boxes=[(52, 72, -180, -150), (52, 72, 160, 180)], t0=0.4, t1=1.0, alpha=0.4),
     dict(k="glow", boxes=[(48, 58, -3, 9)], t0=0.8, t1=1.4, alpha=0.4),
     dict(k="glow", boxes=[(-9, 9, 95, 119)], t0=1.2, t1=1.8, alpha=0.4),
     dict(k="glow", boxes=[(-25, -4, 127, 150)], t0=1.6, t1=2.2, alpha=0.4)]),
 # ---- 17 shots added for the pace change (plan/maps_added.md); lengths come from the chapter JSONs
 "MAP_02c2": A(view="weddell", s=(1.0, 1.12), sl=(-120, -120), p=(1.0, 1.0), center=[(-72, -50), (-71, -52)], extras=[dict(k="zoneline", t0=0.0)]),
 "MAP_03d2": A(view="bering_s", s=(0.92, 1.0), sl=(-120, -120), p=(1.0, 1.0), pin=(57.5, -172), pin_screen=(640, 420), extras=[
     dict(k="coastline", level=-120, box=(52, 61, -180, -163), t0=0.5, t1=2.0, color=GOLD_, w=4)]),
 "MAP_03e2": A(view="bering_km", s=(0.8534, 0.8534), sl=(-120, -120), p=(1.0, 1.0), anchor_at=((68, -168), (640, 260))),
 "MAP_03f2": A(view="npacific", s=(0.74, 0.80), sl=(-120, -120), p=(0.9, 1.0), pin=(64, -165)),
 "MAP_03g":  A(view="npacific", s=(0.80, 0.86), sl=(-120, -120), p=(1.0, 1.0), center=[(52, -138), (52, -138)], extras=[dict(k="walk", pts=KELP, t0=0.4, t1=3.0, color=KELPG, w=4, alpha=0.95)]),
 "MAP_03g2": A(view="pacific", s=(0.80, 0.90), sl=(-120, -120), p=(1.0, 1.0), center=[(57, -138), (54, -133)], extras=[dict(k="walk", pts=KELP, t0=0.0, t1=1.8, color=KELPG, w=4, alpha=0.95)]),
 "MAP_04d2": A(view="baltic", s=(0.92, 0.96), sl=(-120, -120), p=(0.85, 1.0), center=[(58.5, 18), (58.5, 18)]),
 "MAP_05d2": A(view="blacksea", s=(1.0, 1.1), sl=(-120, -120), p=(1.0, 1.0), center=[(43.5, 39), (43.5, 41)]),
 "MAP_06c2": A(view="cmed", s=(0.95, 1.0), sl=(-120, -120), p=(1.0, 1.0), center=[(41, 9), (41, 9)]),
 "MAP_06e2": A(view="lion", s=(0.84, 0.86), sl=(-120, 0), p=(1.0, 0.8), center=[(42.8, 4), (42.8, 4)], inset=True, extras=[
     dict(k="dots", pts=[(42.5, 4.2), (42.2, 4.8), (42.8, 3.7), (42.0, 4.1)], t_in=0.0, t_out=9, r=8, sink=True)]),
 "MAP_07b2": A(view="redsea", s=(0.67, 0.74), sl=(0, 0), p=(1.0, 1.0), center=[(17, 41), (17, 41)], inset=True, extras=[dict(k="ring", pt=(12.6, 43.3), r=70, t0=0.6)]),
 "MAP_07c2": A(view="babel", s=(0.95, 1.05), sl=(-120, -120), p=(1.0, 1.0), center=[(13, 43), (13, 43)], inset=True),
 "MAP_08b2": A(view="sahul", s=(0.70, 0.74), sl=(-120, -120), p=(1.0, 1.0), center=[(-12, 134), (-12, 134)], inset=True, extras=[
     dict(k="glow", boxes=[(-45, 2, 112, 155)], t0=0.1, t1=0.8, alpha=0.2, land=True)]),
 "MAP_08c2": A(view="carp", s=(0.90, 0.96), sl=(-120, -120), p=(1.0, 1.0), center=[(-13, 139), (-13, 139)], inset=True, extras=[
     dict(k="lake", t0=0.2, t1=1.4, color=(110, 175, 205), alpha=0.55)]),
 "MAP_09e2": A(view="namerica", s=(1.0, 0.70), sl=(-120, -120), p=(1.0, 1.0), pin=(32.8, -106.3), inset=True),
 "MAP_10d2": A(view="sunda", s=(0.70, 0.74), sl=(-120, -120), p=(1.0, 1.0), pin=(3, 107), inset=True, extras=[dict(k="coast", draw=(0.2, 1.2), color=GOLD_)]),
 "MAP_10g2": A(view="seasia", s=(0.74, 0.80), sl=(0, 0), p=(1.0, 1.0), center=[(5, 113), (5, 113)], inset=True, extras=[
     dict(k="arrow", pts=[(1, 108), (6, 106), (12, 102), (14.5, 101.5)], t0=0.4, t1=2.0, color=(236, 224, 196), w=6),
     dict(k="arrow", pts=[(1, 109), (5, 112), (10, 115), (14, 109)], t0=0.8, t1=2.4, color=(236, 224, 196), w=6),
     dict(k="arrow", pts=[(0, 110), (-2, 116), (-4, 122), (-3, 126)], t0=1.2, t1=2.8, color=(236, 224, 196), w=6),
     dict(k="arrow", pts=[(2, 109), (4, 116), (8, 120), (11, 122)], t0=1.6, t1=3.2, color=(236, 224, 196), w=6)]),
}
