META = dict(name='black', about='Black hold (the silent drop, rule 30). Total silence: no sound events.', variants=['hold'], params={})
def build(ctx):
    return dict(html=f'<div id="{ctx.id}" class="clip shot" data-start="{ctx.a:.3f}" data-duration="{ctx.dur:.3f}" data-track-index="1" style="background:#000"></div>')
