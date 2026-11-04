from .common import *
from . import lower_third as _lt, number_clip as _nc
META = dict(name='text_card', about='A text card with no clip: dark textured picture and text in the middle. For a one-word beat ("okay.", "just rivers"), a two-part joke, or a number on its own. Use it to split a long line into two cuts (text templates over clips are limited to 2 per chapter, rule 16; cards count on their own).',
  variants=['word', 'pair', 'line', 'number', 'number_left'],
  params={'text': 'word / pair / line: the main text', 'at': 'when the text appears (time spec; default 0.3 s)', 'size': 'text size px',
          'aside': 'pair: the italic aside (shown after the text)', 'aside_at': 'pair: when the aside appears', 'joke_sound': 'pair: dry "tok" on the aside (default true)', 'kicker': 'small caps line above (line, number, number_left)',
          'number': 'number / number_left: the big number', 'unit': 'number: italic unit after the number', 'subline': 'number: small line under the number', 'number_at': 'number: when the number appears',
          'subline_at': 'number: when the subline appears', 'count': 'number: {"from":0,"to":-1.8,"decimals":1,"dur":1.2,"suffix":"°C"} counting number', 'dim': 'number: dark shade "dk" (default) or "lt"'})
def build(ctx):
    ctx.shot['card'] = True
    v = ctx.variant
    if v in ('word', 'pair', 'line'):
        ctx.variant = {'word': 'italic_word', 'pair': 'two_part', 'line': 'kicker_line'}[v]; return _lt.build(ctx)
    ctx.variant = 'center_bars' if v == 'number' else 'left_stack'; return _nc.build(ctx)
