"""Shared drawing helpers (copied from the approved v9 build, style C)."""
import html as _html
GOLD = '#c9a45c'; WARM = '#f6efe0'; SOFT = '#e9dcc0'; ITAL = '#d9bd7e'
DEG = '<span class="deg">&deg;</span>'
X0 = [140, 447, 753, 1060]          # timer bar stop positions (START, 1, 10, 30)
DEFAULT_LABELS = ['START', '1 MIN', '10 MIN', '30 MIN']

def esc(s): return _html.escape(str(s), quote=False)
def rich(s):
    """Text -> html. '°' becomes the small style-C degree sign, '-' before a digit becomes a minus, *word* becomes italic."""
    import re
    s = esc(s).replace("'", '\u2019')
    s = re.sub(r'(^|[\s(])-(?=\d)', lambda m: m.group(1) + '&minus;', s)
    s = s.replace('−', '&minus;').replace('–', '&ndash;').replace('°', DEG)
    s = re.sub(r'(?<=\d)-(?=\d)', '&ndash;', s)
    s = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', s)
    return s
def rich_svg(s):
    """Like rich() but italic runs become <tspan> (for use inside svg <text>)."""
    return rich(s).replace('<i>', '<tspan font-style="italic">').replace('</i>', '</tspan>')

def fig(p, hx, hy, s, sw=6.5):
    sy = hy - 78 * s
    return f'''<g id="{p}-fig" fill="none" stroke="#fff" stroke-width="{sw*s:.2f}" stroke-linecap="round" stroke-linejoin="round">
  <g id="{p}-head"><circle cx="{hx}" cy="{hy-112*s:.1f}" r="{24*s:.1f}" fill="#050505"/>
   <g id="{p}-eyes"><circle cx="{hx-8*s:.1f}" cy="{hy-117*s:.1f}" r="{3*s:.1f}" fill="#fff" stroke="none"/><circle cx="{hx+8*s:.1f}" cy="{hy-117*s:.1f}" r="{3*s:.1f}" fill="#fff" stroke="none"/></g>
   <g id="{p}-eyesX" opacity="0" stroke-width="{2.6*s:.2f}"><path d="M{hx-12*s:.1f},{hy-121*s:.1f} l{8*s:.1f},{8*s:.1f} m{-8*s:.1f},0 l{8*s:.1f},{-8*s:.1f}"/><path d="M{hx+4*s:.1f},{hy-121*s:.1f} l{8*s:.1f},{8*s:.1f} m{-8*s:.1f},0 l{8*s:.1f},{-8*s:.1f}"/></g>
   <path id="{p}-mouth" d="M{hx-8*s:.1f},{hy-104*s:.1f} Q{hx},{hy-99*s:.1f} {hx+8*s:.1f},{hy-104*s:.1f}" stroke-width="{3*s:.2f}"/>
   <ellipse id="{p}-mouthO" cx="{hx}" cy="{hy-102*s:.1f}" rx="{8*s:.1f}" ry="{11*s:.1f}" fill="#000" stroke-width="{3*s:.2f}" opacity="0"/></g>
  <line x1="{hx}" y1="{hy-88*s:.1f}" x2="{hx}" y2="{hy}"/>
  <g id="{p}-armL"><line x1="{hx}" y1="{sy:.1f}" x2="{hx}" y2="{sy+56*s:.1f}"/></g>
  <g id="{p}-armR"><line x1="{hx}" y1="{sy:.1f}" x2="{hx}" y2="{sy+56*s:.1f}"/></g>
  <g id="{p}-legL"><line x1="{hx}" y1="{hy}" x2="{hx}" y2="{hy+84*s:.1f}"/></g>
  <g id="{p}-legR"><line x1="{hx}" y1="{hy}" x2="{hx}" y2="{hy+84*s:.1f}"/></g>
</g>'''

def waterline(y, w=1700, amp=12, period=110):
    d = f'M-200,{y} '; x = -200
    while x < w:
        d += f'q {period/4},{-amp} {period/2},0 t {period/2},0 '; x += period
    return d
def water(p, y, op=.7):
    return (f'<g id="{p}-water"><path d="{waterline(y)} V800 H-200 Z" fill="#101a1f" fill-opacity="{op}"/>'
            f'<path d="{waterline(y)}" fill="none" stroke="#e9dcc0" stroke-width="3" stroke-linecap="round" stroke-opacity=".85"/></g>')
def timer_bar(p, labels=None):
    lab = labels or DEFAULT_LABELS
    s = f'<g id="{p}-bar"><line x1="140" y1="655" x2="1060" y2="655" stroke="{WARM}" stroke-opacity=".28" stroke-width="2"/>'
    s += f'<line id="{p}-prog" x1="140" y1="655" x2="1060" y2="655" stroke="{GOLD}" stroke-width="3"/>'
    for x, l in zip(X0, lab):
        s += f'<line x1="{x}" y1="646" x2="{x}" y2="664" stroke="{WARM}" stroke-width="1.5"/><text class="tbl" x="{x}" y="696" text-anchor="middle">{esc(l)}</text>'
    s += f'<g id="{p}-mk"><circle cx="0" cy="655" r="9" fill="{GOLD}" stroke="#000" stroke-width="2"/></g></g>'
    return s
def block(i, x, y, w, inner, align='center', z=''):
    return f'<div id="{i}" class="blk op0" style="left:{x}px;top:{y}px;width:{w}px;text-align:{align};{z}">{inner}</div>'
def num(i, big, unit, bsize, usize, extra=''):
    u = f'<i style="font-size:{usize}px"> {rich(unit)}</i>' if unit else ''
    return f'<div id="{i}" class="cg" style="{extra}"><span style="font-size:{bsize}px">{rich(big)}</span>{u}</div>'
def bars(): return '<div class="bar" style="top:0"></div><div class="bar" style="bottom:0"></div>'
def xmark(i, x, y, r=100): return f'<path id="{i}" d="M{x-r},{y-r} L{x+r},{y+r} M{x+r},{y-r} L{x-r},{y+r}" stroke="{GOLD}" stroke-width="10" stroke-linecap="round" fill="none"/>'

# ---- icons for stick gags: drawn around (0,0), about 180 px wide, white line art on a dark fill (same look as v9) ----
_G = 'fill="none" stroke="#fff" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"'
ICONS = {
 'boat': f'<g {_G}><path d="M-90,10 L90,10 L60,60 L-60,60 Z" fill="#26262c"/><line x1="0" y1="10" x2="0" y2="-90"/><path d="M6,-85 L70,-10 L6,-10 Z" fill="#26262c"/></g>',
 'wetsuit': '<g fill="#26262c" stroke="#fff" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"><path d="M-30,-70 L-10,-82 Q0,-70 10,-82 L30,-70 L78,-40 L62,-4 L40,-20 L40,48 L-40,48 L-40,-20 L-62,-4 L-78,-40 Z"/><line x1="0" y1="-72" x2="0" y2="40"/></g>',
 'lifering': f'<g {_G}><circle r="62" fill="#26262c"/><circle r="26" fill="#050505"/><path d="M-44,-44 L-18,-18 M44,-44 L18,-18 M-44,44 L-18,18 M44,44 L18,18"/></g>',
 'bottle': f'<g {_G}><path d="M-18,-80 h36 v22 q30,14 30,50 v84 q0,12 -12,12 h-72 q-12,0 -12,-12 v-84 q0,-36 30,-50 z" fill="#26262c"/><path d="M-30,-8 h60" /></g>',
 'flame': f'<g {_G}><path d="M0,-84 C10,-50 52,-34 48,16 C44,56 14,70 0,70 C-16,70 -48,56 -48,16 C-48,-12 -26,-24 -16,-56 C-8,-40 -2,-60 0,-84 Z" fill="#26262c"/><path d="M0,70 C-18,60 -22,34 -4,14 C0,30 22,34 14,58 C10,66 6,68 0,70 Z"/></g>',
 'phone': f'<g {_G}><rect x="-38" y="-78" width="76" height="150" rx="14" fill="#26262c"/><line x1="-14" y1="-62" x2="14" y2="-62"/><circle cx="0" cy="54" r="6"/></g>',
 'fish': f'<g {_G}><path d="M-80,0 C-40,-52 30,-52 60,0 C30,52 -40,52 -80,0 Z" fill="#26262c"/><path d="M60,0 L98,-34 L98,34 Z" fill="#26262c"/><circle cx="-44" cy="-8" r="5" fill="#fff"/></g>',
 'snowflake': f'<g {_G}><path d="M0,-80 V80 M-69,-40 L69,40 M-69,40 L69,-40"/><path d="M-14,-66 L0,-52 L14,-66 M-14,66 L0,52 L14,66"/></g>',
 'thermometer': f'<g {_G}><rect x="-16" y="-84" width="32" height="118" rx="16" fill="#26262c"/><circle cx="0" cy="56" r="28" fill="#26262c"/><line x1="0" y1="-52" x2="0" y2="52" stroke="{GOLD}"/></g>',
 'clock': f'<g {_G}><circle r="66" fill="#26262c"/><path d="M0,-40 V0 L28,18"/></g>',
 'hand': f'<g {_G}><path d="M-34,70 V0 q0,-10 12,-10 h4 V-62 q0,-12 12,-12 t12,12 V-14 V-72 q0,-12 12,-12 t12,12 V-14 V-62 q0,-12 12,-12 t12,12 V30 q0,40 -34,40 z" fill="#26262c"/></g>',
 'rope': f'<g fill="none" stroke="#d9b278" stroke-width="9" stroke-linecap="round"><path d="M-70,30 C-70,-50 70,-50 70,30 C70,70 -40,70 -40,10 C-40,-20 40,-20 40,10"/></g>',
 'shore': '<g fill="#2a2d30" stroke="#e9dcc0" stroke-width="3"><path d="M-90,50 C-40,20 40,16 90,34 L90,70 L-90,70 Z"/></g><g stroke="#e9dcc0" stroke-width="5" stroke-linecap="round" fill="none"><path d="M30,26 C36,-20 28,-50 20,-70"/><path d="M20,-70 q-40,-8 -62,22 M20,-70 q-10,-44 -52,-46 M20,-70 q30,-36 66,-26 M20,-70 q44,0 60,36"/></g>',
 'shark': f'<g {_G}><path d="M-90,30 C-50,-10 10,-30 40,-70 C46,-30 70,-6 96,24 C60,20 30,36 0,40 C-30,44 -60,40 -90,30 Z" fill="#26262c"/></g>',
 # ---- added for Video 01 (gap T6) ----
 'penguin': f'<g {_G}><path d="M0,-84 C-36,-84 -52,-52 -52,-8 C-52,38 -40,78 0,78 C40,78 52,38 52,-8 C52,-52 36,-84 0,-84 Z" fill="#26262c"/><path d="M0,-46 C-26,-36 -30,4 -26,36 C-22,64 22,64 26,36 C30,4 26,-36 0,-46 Z" fill="#050505" stroke-width="5"/><path d="M-52,-14 C-80,8 -84,34 -66,52 M52,-14 C80,8 84,34 66,52"/><path d="M-9,-60 L9,-60 L0,-44 Z" fill="{GOLD}" stroke="{GOLD}" stroke-width="3"/><circle cx="-16" cy="-68" r="4.5" fill="#fff" stroke="none"/><circle cx="16" cy="-68" r="4.5" fill="#fff" stroke="none"/><path d="M-22,78 h-18 M22,78 h18"/></g>',
 'person': f'<g {_G}><circle cy="-60" r="24" fill="#26262c"/><path d="M-40,76 V-6 Q-40,-28 -18,-28 H18 Q40,-28 40,-6 V76" fill="#26262c"/><path d="M0,-28 V76" stroke-width="5"/></g>',
 'orca': f'<g {_G}><path d="M-92,-4 C-60,-34 -20,-44 20,-44 L40,-96 L52,-42 C70,-38 86,-24 96,-4 C80,18 40,34 -10,34 C-40,34 -70,24 -92,-4 Z" fill="#26262c"/><path d="M-92,-4 L-116,-34 L-104,-4 L-116,26 Z" fill="#26262c"/><path d="M30,10 C54,12 72,4 84,-8 C74,-2 52,0 30,-2 Z" fill="#f6efe0" stroke="none"/><path d="M52,-24 q16,-6 26,2" fill="#f6efe0" stroke="none" stroke-width="0"/><ellipse cx="58" cy="-18" rx="13" ry="6" fill="#f6efe0" stroke="none" transform="rotate(-18 58 -18)"/><path d="M-6,22 L-24,56" /></g>',
 'salt': f'<g {_G}><path d="M-52,-18 L0,-46 L52,-18 L52,34 L0,62 L-52,34 Z" fill="#26262c"/><path d="M-52,-18 L0,10 L52,-18 M0,10 V62" stroke-width="5"/><path d="M-84,70 h0.1 M-70,56 h0.1 M-92,52 h0.1 M72,66 h0.1 M88,52 h0.1 M60,-62 h0.1 M-62,-56 h0.1 M-44,-84 h0.1" stroke-width="10"/></g>',
 'mussel': f'<g {_G}><path d="M-70,50 C-92,-10 -50,-70 10,-72 C54,-72 82,-30 80,6 C78,34 40,56 -10,56 C-36,56 -56,54 -70,50 Z" fill="#26262c"/><path d="M-62,40 C-30,10 14,-20 66,-52 M-52,50 C-18,28 30,0 76,-22 M-60,18 C-34,-4 -2,-32 30,-62" stroke-width="4.5"/></g>',
 'dice': f'<g {_G}><g transform="rotate(-12)"><rect x="-62" y="-62" width="124" height="124" rx="22" fill="#26262c"/></g><g fill="#fff" stroke="none" transform="rotate(-12)"><circle cx="-30" cy="-30" r="9"/><circle cx="30" cy="-30" r="9"/><circle cx="0" cy="0" r="9"/><circle cx="-30" cy="30" r="9"/><circle cx="30" cy="30" r="9"/></g></g>',
 'hut': f'<g {_G}><path d="M-88,10 L0,-76 L88,10 Z" fill="#26262c"/><path d="M-64,10 V70 H64 V10" fill="#26262c"/><path d="M-20,70 V32 Q0,16 20,32 V70" fill="#050505"/><path d="M-88,10 L-100,24 M88,10 L100,24"/></g>',
 'bowl': f'<g {_G}><path d="M-82,0 H82 C82,50 44,76 0,76 C-44,76 -82,50 -82,0 Z" fill="#26262c"/><path d="M-30,76 V90 H30 V76"/><path d="M-40,-18 C-56,-36 -24,-48 -40,-70 M0,-18 C-16,-36 16,-48 0,-70 M40,-18 C24,-36 56,-48 40,-70" stroke-width="5.5"/></g>',
 'river': f'<g {_G}><path d="M-90,-40 C-60,-64 -30,-16 0,-40 C30,-64 60,-16 90,-40"/><path d="M-90,0 C-60,-24 -30,24 0,0 C30,-24 60,24 90,0"/><path d="M-90,40 C-60,16 -30,64 0,40 C30,16 60,64 90,40"/></g>',
 'tree': f'<g {_G}><path d="M0,80 V10" stroke-width="12"/><path d="M0,40 L-26,14 M0,28 L24,4" stroke-width="7"/><path d="M-64,16 C-92,-8 -74,-50 -42,-48 C-40,-82 8,-92 30,-66 C62,-72 84,-34 62,-8 C74,14 46,28 20,18 C0,26 -34,28 -64,16 Z" fill="#26262c"/></g>',
 'croc': f'<g {_G}><path d="M-98,6 C-70,-14 -40,-30 0,-34 C40,-38 62,-40 96,-26 L100,-12 L50,-4 L96,6 L96,18 C60,14 30,24 0,30 C-30,34 -70,30 -98,6 Z" fill="#26262c"/><path d="M-60,-22 l8,-10 l8,10 M-30,-30 l8,-10 l8,10 M0,-34 l8,-10 l8,10" stroke-width="5"/><path d="M52,-4 l6,8 l6,-8 l6,8 l6,-8 l6,8 l6,-8" stroke-width="3.5"/><circle cx="60" cy="-30" r="5" fill="#fff" stroke="none"/><path d="M-20,28 l-10,26 h22 M34,22 l8,28 h-20" stroke-width="6"/></g>',
}
def icon(name):
    if name in ICONS: return ICONS[name]
    if name.lstrip().startswith('<'): return name       # raw svg allowed
    raise KeyError(f'unknown icon "{name}". Known icons: {", ".join(sorted(ICONS))}')
