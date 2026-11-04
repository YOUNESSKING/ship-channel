from .common import *
META = dict(name='title_card', about='Chapter title card: kicker + name + hairline + date, over a dimmed clip, with whoosh + thud (rule 52).',
  variants=['center_bars', 'left_plate', 'minimal'],
  params={'kicker': 'small caps line, e.g. "Chapter one"', 'title': 'chapter name', 'date': 'italic line, e.g. "20,000 years ago"',
          'date_at': 'when the date appears (time spec; default 0.9 s)', 'size': 'title size px (auto-fit by default)'})
def build(ctx):
    v = ctx.variant; p = ctx.id
    k = ctx.p('kicker', ''); title = ctx.p('title', ''); date = ctx.p('date', ''); dat = ctx.t(ctx.p('date_at'), .9)
    n = max(1, len(title))
    if v == 'center_bars':
        size = ctx.p('size', int(min(118, 1100 / (n * .62))))
        inner = '<div class="shade"></div>' + bars() + block(f'{p}-blk', 0, 230, 1280,
            f'<div class="jo gold">{rich(k)}</div><div class="cg" style="font-size:{size}px;letter-spacing:.05em;margin-top:18px;text-transform:uppercase">{rich(title)}</div><div class="gr"></div>'
            f'<div id="{p}-d" class="cg" style="font-size:42px"><i>{rich(date)}</i></div>')
        push = (1.18, 1.0, '50% 50%')
    elif v == 'left_plate':
        size = ctx.p('size', int(min(104, 640 / (n * .62))))
        inner = '<div class="scrimL"></div>' + bars() + block(f'{p}-blk', 80, 250, 760,
            f'<div class="jo gold">{rich(k)}</div><div class="cg" style="font-size:{size}px;letter-spacing:.05em;margin-top:18px;text-transform:uppercase">{rich(title)}</div><div class="gr l"></div>'
            f'<div id="{p}-d" class="cg" style="font-size:40px"><i>{rich(date)}</i></div>', 'left')
        push = (1.0, 1.1, '30% 50%')
    else:
        size = ctx.p('size', int(min(84, 1000 / (n * .62))))
        inner = '<div class="shade dk"></div>' + block(f'{p}-blk', 0, 270, 1280,
            f'<div class="jo gold">{rich(k)}</div><div class="cg" style="font-size:{size}px;letter-spacing:.06em;margin-top:16px;text-transform:uppercase">{rich(title)}</div><div class="gr"></div>'
            f'<div id="{p}-d" class="cg" style="font-size:36px"><i>{rich(date)}</i></div>')
        push = (1.12, 1.0, '50% 50%')
    ctx.js.append(f"drop('#{p}-blk',{ctx.a:.3f});pop('#{p}-d',{dat - .05:.3f},.4);")
    ctx.sfx('title', ctx.a + .05, 1.0)
    return dict(html=ctx.video(push) + ctx.overlay(inner))
