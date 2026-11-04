META = dict(name='clip_plain', about='Plain full-bleed clip with trim (in) and slow push. No text.',
  variants=['push', 'pull', 'jump'],
  params={'dim': '0-1, optional dark shade over the clip (default 0 = none)',
          'jump_at': 'variant jump: time of the zoom step (default: half of the shot)', 'jump_scale': 'variant jump: zoom after the step (default 1.14)'})
def build(ctx):
    v = ctx.variant
    push = {'push': (1.0, 1.07, '50% 55%'), 'pull': (1.15, 1.0, '50% 50%'), 'jump': (1.0, 1.06, '50% 40%')}[v]
    h = ctx.video(push)
    if v == 'jump':
        ctx.js.append(f"jump('#{ctx.id}_v',{ctx.t(ctx.p('jump_at'), ctx.dur/2):.3f},{ctx.p('jump_scale', 1.14)},'{push[2]}');")
    dim = ctx.p('dim', 0)
    if dim: h += ctx.overlay(f'<div style="position:absolute;inset:0;background:rgba(0,0,0,{dim})"></div>')
    return dict(html=h)
