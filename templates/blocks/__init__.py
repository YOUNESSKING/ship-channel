import importlib
NAMES = ['clip_plain', 'number_clip', 'lower_third', 'extinct_plate', 'title_card', 'stick_timer', 'stick_rope', 'stick_water', 'stick_gag',
         'scale_ruler', 'problem_counter', 'tier_board', 'map_clip', 'black', 'stick_land', 'stick_walk', 'outro', 'text_card', 'croc_gfx', 'croc_stick']
# Animation blocks (GOLD rules 95-98): generic ones for every video + per-video scene modules. Optional: a missing module is skipped.
OPTIONAL = ['anim_gauge', 'anim_lockon', 'anim_options', 'anim_xray', 'v02_anim_a', 'v02_anim_b', 'v02_anim_c']
REGISTRY = {}
for n in NAMES + OPTIONAL:
    try: m = importlib.import_module('.' + n, __name__)
    except ModuleNotFoundError as e:
        if n in OPTIONAL and e.name and e.name.endswith(n): continue
        raise
    REGISTRY[m.META['name']] = m
