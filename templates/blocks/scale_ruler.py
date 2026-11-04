from .common import *
META = dict(name='scale_ruler', about='Constant ruler (rule 54): stick figure next to the animal (silhouette or on a clip) with a measure label. Scale is true: the animal is drawn as long, relative to a 1.75 m figure, as its real length.',
  variants=['silhouette', 'water', 'clip'],
  params={'animal': 'silhouette name: shark, orca, bear, mammoth, leopard_seal, crocodile (or give "svg")', 'svg': 'your own silhouette: svg inner markup drawn in a 1000-unit-wide box, feet/belly line at y=0, facing right',
          'length_m': 'animal length in metres (e.g. 6)', 'label': 'measure label text, e.g. "6 m (20 ft)"; default made from length_m',
          'name': 'caps name under the animal, e.g. "GREAT WHITE SHARK"', 'human_m': 'figure height in metres (default 1.75)', 'human_label': 'tiny label next to the figure (default "you")',
          'animal_at': 'when the animal shows (default 0.25 s)', 'ruler_at': 'when the ruler line draws (default 1.0 s)',
          'figure': 'clip variant: {"x":150,"feet_y":620,"scale":1.0} where the figure stands', 'span': 'clip variant: {"x0":420,"x1":1100,"y":230} where the animal is in the picture (px)'})
_FILL = 'fill="#1a2429" stroke="#e9dcc0" stroke-opacity=".55" stroke-width="3" stroke-linejoin="round"'
SIL = {
 'shark': f'<path {_FILL} d="M1000,-120 C940,-170 800,-205 640,-208 L560,-212 L500,-335 L470,-212 C340,-200 200,-170 110,-130 L30,-250 L55,-120 L10,-20 L120,-90 C260,-70 420,-70 520,-75 L570,-10 L640,-80 C760,-72 900,-85 1000,-120 Z"/>',
 'orca': f'<path {_FILL} d="M1000,-110 C980,-170 900,-200 780,-205 L660,-208 L610,-440 L560,-208 C420,-200 260,-170 130,-130 L20,-250 L50,-120 L10,-20 L140,-80 C300,-55 480,-45 640,-55 L720,10 L760,-60 C870,-55 960,-70 1000,-110 Z"/><path d="M880,-125 q50,-25 90,-20" fill="none" stroke="#f6efe0" stroke-opacity=".5" stroke-width="10" stroke-linecap="round"/>',
 'bear': f'<g {_FILL}><ellipse cx="470" cy="-330" rx="340" ry="190"/><path d="M200,-470 C300,-560 420,-520 460,-470 Z"/><ellipse cx="840" cy="-350" rx="120" ry="95"/><path d="M900,-400 L1000,-340 L1000,-300 L900,-290 Z"/><circle cx="800" cy="-440" r="28"/>'
         '<rect x="190" y="-230" width="100" height="230" rx="30"/><rect x="330" y="-230" width="100" height="230" rx="30"/><rect x="560" y="-230" width="100" height="230" rx="30"/><rect x="700" y="-250" width="100" height="250" rx="30"/></g>',
 'mammoth': f'<g {_FILL}><ellipse cx="470" cy="-340" rx="340" ry="200"/><ellipse cx="720" cy="-420" rx="200" ry="230"/><rect x="190" y="-230" width="100" height="230" rx="30"/><rect x="350" y="-230" width="100" height="230" rx="30"/><rect x="570" y="-230" width="100" height="230" rx="30"/><rect x="720" y="-230" width="100" height="230" rx="30"/>'
           '<path d="M880,-330 C960,-300 990,-200 940,-90" fill="none" stroke-width="64" stroke-linecap="round" stroke="#e9dcc0" stroke-opacity=".55"/><path d="M880,-330 C960,-300 990,-200 940,-90" fill="none" stroke-width="58" stroke-linecap="round" stroke="#1a2429"/>'
           '<path d="M840,-300 C900,-250 880,-160 830,-130" fill="none" stroke="#f6efe0" stroke-width="12" stroke-linecap="round"/></g>',
 'leopard_seal': f'<g {_FILL}><path d="M52,-58 C110,-86 190,-118 280,-152 C390,-186 520,-202 636,-198 C716,-194 764,-180 810,-176 C870,-176 940,-172 985,-150 C1002,-140 1004,-118 992,-104 C974,-90 930,-86 880,-80 C820,-72 760,-36 690,-14 C620,4 520,-4 420,-14 C300,-24 200,-10 118,-16 C84,-18 62,-30 52,-58 Z"/>'
         '<path d="M52,-58 C34,-74 12,-84 0,-98 C14,-70 22,-52 34,-40 C18,-30 6,-18 0,-4 C26,-14 48,-26 62,-34 Z"/><path d="M606,-62 C586,-30 566,4 520,12 C556,-8 576,-40 586,-74 Z"/><path d="M300,-30 C288,-4 268,12 232,18 C260,-2 276,-18 284,-38 Z"/>'
         '<path d="M992,-114 C940,-104 892,-104 846,-116" fill="none" stroke="#f6efe0" stroke-opacity=".55" stroke-width="5" stroke-linecap="round"/><circle cx="900" cy="-146" r="8" fill="#f6efe0" stroke="none" fill-opacity=".8"/>'
         '<g fill="#f6efe0" fill-opacity=".28" stroke="none"><circle cx="360" cy="-110" r="9"/><circle cx="470" cy="-140" r="8"/><circle cx="560" cy="-90" r="9"/><circle cx="650" cy="-150" r="7"/><circle cx="260" cy="-84" r="7"/></g></g>',
 'crocodile': f'<g {_FILL}><path d="M0,-34 C90,-40 190,-78 300,-100 C420,-124 540,-124 640,-120 C720,-118 790,-114 842,-118 L954,-120 C984,-118 1000,-106 1000,-92 L990,-78 C968,-70 930,-68 892,-70 C836,-68 786,-58 710,-50 L700,-14 L690,0 L610,0 L606,-30 C520,-26 440,-26 360,-30 L350,0 L270,0 L262,-34 C170,-28 80,-24 0,-34 Z"/>'
         '<path d="M0,-34 C-10,-46 -10,-46 0,-34 Z"/><g fill="none" stroke="#e9dcc0" stroke-opacity=".7" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"><path d="M200,-90 l16,-26 l16,24 M290,-112 l16,-28 l16,26 M380,-124 l16,-28 l16,26 M470,-128 l16,-28 l16,26 M560,-128 l16,-28 l16,26 M650,-124 l16,-26 l16,24"/>'
         '<path d="M860,-76 l14,18 l14,-18 l14,18 l14,-18 l14,18 l14,-18" stroke-width="5"/></g>'
         '<ellipse cx="846" cy="-132" rx="26" ry="18" fill="#1a2429" stroke="#e9dcc0" stroke-opacity=".55" stroke-width="3"/><circle cx="850" cy="-134" r="7" fill="#f6efe0" stroke="none" fill-opacity=".9"/></g>',
}
def _ruler(p, x0, x1, y, label, at):
    return (f'<g id="{p}-ruler"><path id="{p}-rl" d="M{x0:.0f},{y} H{x1:.0f}" fill="none" stroke="{GOLD}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
            f'<line x1="{x0:.0f}" y1="{y-14}" x2="{x0:.0f}" y2="{y+14}" stroke="{GOLD}" stroke-width="3"/><line x1="{x1:.0f}" y1="{y-14}" x2="{x1:.0f}" y2="{y+14}" stroke="{GOLD}" stroke-width="3"/>'
            f'<text id="{p}-rt" x="{(x0+x1)/2:.0f}" y="{y-24}" text-anchor="middle" class="itsv" style="font-size:54px" opacity="0">{rich_svg(label)}</text></g>')
def build(ctx):
    v = ctx.variant; p = ctx.id; T = ctx.a
    L = float(ctx.p('length_m', 5)); H = float(ctx.p('human_m', 1.75)); name = ctx.p('name', ''); hl = ctx.p('human_label', 'you')
    label = ctx.p('label') or (f'{L:g} m  *({L*3.28:.0f} ft)*')
    aat = ctx.t(ctx.p('animal_at'), .25); rat = ctx.t(ctx.p('ruler_at'), 1.0)
    js = []; h = ''
    if v == 'clip':
        fg = ctx.p('figure', {'x': 150, 'feet_y': 640, 'scale': 1.0}); sp = ctx.p('span', {'x0': 420, 'x1': 1100, 'y': 200})
        s = fg.get('scale', 1.0); hx = fg['x']; hy = fg['feet_y'] - 84 * s
        svg = (f'<g id="{p}-figw">{fig(p, hx, hy, s)}</g><text x="{hx}" y="{fg["feet_y"]+34}" text-anchor="middle" class="lblm" style="font-size:16px">{esc(hl)} &middot; {H:g} m</text>'
               + _ruler(p, sp['x0'], sp['x1'], sp['y'], label, rat))
        h = ctx.video((1.0, 1.05, '50% 50%')) + ctx.overlay('<div class="shade"></div><div class="scrimL" style="width:500px;opacity:.7"></div>' + f'<svg width="1280" height="720" viewBox="0 0 1280 720" style="position:absolute;left:0;top:0">{svg}</svg>'
               + (f'<div id="{p}-nm" class="jo gold op0" style="position:absolute;left:{(sp["x0"]+sp["x1"])/2-300:.0f}px;width:600px;text-align:center;top:{sp["y"]+34}px;font-size:16px">{esc(name)}</div>' if name else ''))
        js.append(f"pose('{p}',{hx},{hy},{s},{{aL:15,aR:-15,lL:4,lR:-4}});bob('#{p}-figw',{T:.3f},{ctx.dur:.3f},4,.8);")
        if name: js.append(f"pop('#{p}-nm',{rat + .5:.3f},.4);")
    else:
        animal_px = min(760, 1.5 * 220 * L / H); ppm = animal_px / L; s = ppm * H / 220
        sil = ctx.p('svg') or SIL[ctx.p('animal', 'shark')]
        ax0 = 1220 - animal_px - 20 if animal_px > 500 else 1220 - animal_px - 60; ax0 = max(ax0, 330); ax1 = ax0 + animal_px
        if v == 'silhouette':
            base = 560; hx = 190; hy = base - 84 * s; sc = animal_px / 1000
            svg = (f'<line x1="60" y1="{base}" x2="1220" y2="{base}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="2"/>'
                   f'<g id="{p}-figw">{fig(p, hx, hy, s)}</g><text x="{hx}" y="{base+36}" text-anchor="middle" class="lblm" style="font-size:16px">{esc(hl)} &middot; {H:g} m</text>'
                   f'<g transform="translate({ax0:.0f},{base}) scale({sc:.4f})"><g id="{p}-an" opacity="0">{sil}</g></g>')
            top = base - 600 * sc if ctx.p('animal', 'shark') in ('bear', 'mammoth') else base - 380 * sc
            ry = max(130, top - 70)
            if name: svg += f'<text id="{p}-nm" x="{(ax0+ax1)/2:.0f}" y="{base+36}" text-anchor="middle" class="tbl" style="font-size:18px" opacity="0">{esc(name.upper())}</text>'
            svg += _ruler(p, ax0, ax1, ry, label, rat)
        else:  # water
            wy = 330; hx = 190; hy = wy + 60 - 0 ; sc = animal_px / 1000; s = min(s, 1.4)
            hy = wy + 70
            svg = (f'<g id="{p}-figw">{fig(p, hx, hy, s)}</g>'
                   f'<path d="{waterline(wy)} V800 H-200 Z" fill="#101a1f" fill-opacity=".55"/><path d="{waterline(wy)}" fill="none" stroke="#e9dcc0" stroke-width="3" stroke-linecap="round" stroke-opacity=".85"/>'
                   f'<g transform="translate({ax0:.0f},{wy+250}) scale({sc:.4f})"><g id="{p}-an" opacity="0">{sil}</g></g>'
                   f'<text x="{hx}" y="{wy-130*s-10:.0f}" text-anchor="middle" class="lblm" style="font-size:16px">{esc(hl)} &middot; {H:g} m</text>')
            if name: svg += f'<text id="{p}-nm" x="{(ax0+ax1)/2:.0f}" y="{wy+250+30}" text-anchor="middle" class="tbl" style="font-size:18px" opacity="0">{esc(name.upper())}</text>'
            svg += _ruler(p, ax0, ax1, 690, label, rat)
        h = ctx.shot_div(f'<div id="{p}-kb" class="kb"><svg width="1280" height="720" viewBox="0 0 1280 720">{svg}</svg></div>', 'stick')
        js.append(f"pose('{p}',{hx},{hy},{s},{{aL:20,aR:-20,lL:5,lR:-5}});bob('#{p}-figw',{T:.3f},{ctx.dur:.3f},{6 if v=='water' else 3},.7);kb('#{p}-kb',{T:.3f},{ctx.b:.3f},1.0,1.04,'40% 50%');")
        js.append(f"tl.fromTo('#{p}-an',{{opacity:0,x:40}},{{opacity:1,x:0,duration:.7,ease:'power2.out'}},{aat:.3f});" + (f"pop('#{p}-nm',{rat + .5:.3f},.4);" if name else ''))
    js.append(f"tl.fromTo('#{p}-rl',{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.7,ease:'power1.out'}},{rat:.3f});fadeIn('#{p}-rt',{rat + .45:.3f},.5);")
    ctx.js.append('\n'.join(js)); ctx.sfx('swoosh', aat, .25); ctx.sfx('click', rat + .5, .5)
    return dict(html=h)
