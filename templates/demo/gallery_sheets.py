#!/usr/bin/env python3
"""Snapshots one still per shot of demo/work/gallery and writes contact sheets gallery_1.jpg ... (6 stills each).
   python3 gallery_sheets.py"""
import json, os, subprocess, shutil, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); work = os.path.join(HERE, 'work', 'gallery'); tmp = os.path.join(HERE, 'work', '_snap')
ch = json.load(open(os.path.join(HERE, 'gallery.json')))
OFF = {'tier_board_drop': 3.15, 'map_clip_labeled': 1.0, 'map_clip_gauge': 1.6, 'stick_water_sea': 3.35,   # by template_variant, or by shot id (wins)
       'g32_tier_board_drop_newtier': 3.3, 'g33_outro_question': 2.2, 'g34_outro_card': 2.2, 'g35_outro_end_screen': 3.0, 'g36_stick_land_grass': 2.4, 'g37_stick_land_snow': 2.9,
       'g38_stick_walk_channel': 3.1, 'g39_stick_walk_bridge': 3.1, 'g44_map_measure_inset': 2.3, 'g45_map_polar': 2.6, 'g30_tier_board_final': 2.5, 'g31_tier_board_final_wide': 2.2,
       'g40_stick_gag_penguin': 2.2, 'g41_stick_gag_croc': 2.2}
shots = ch['shots']; times = []
for s in shots:
    key = f"{s['template']}_{s['variant']}"
    times.append(s['start'] + OFF.get(s['id'], OFF.get(key, 2.6)))
os.makedirs(tmp, exist_ok=True)
subprocess.run(['npx', '-y', 'hyperframes@0.8.188', 'snapshot', work, '--at', ','.join(f'{t:.2f}' for t in times), '--no-end', '--keep', '-o', tmp], check=True, capture_output=True)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
ims = []
for s, t in zip(shots, times):
    f = os.path.join(tmp, 'at-%gs.png' % round(t, 2))
    pic = Image.open(f).convert('RGB').resize((640, 360)); im = Image.new('RGB', (640, 388), (0, 0, 0)); im.paste(pic, (0, 28)); d = ImageDraw.Draw(im)
    d.text((8, 3), f"{s['template']} / {s['variant']}", fill=(201, 164, 92), font=font); ims.append(im)
per = 6
for k in range(0, len(ims), per):
    sheet = Image.new('RGB', (1280 + 6, 3 * 388 + 12), (20, 20, 20))
    for j, im in enumerate(ims[k:k + per]): sheet.paste(im, ((j % 2) * 646, (j // 2) * 394))
    sheet.save(os.path.join(HERE, f'gallery_{k // per + 1}.jpg'), quality=85)
shutil.rmtree(tmp); print('sheets:', (len(ims) + per - 1) // per)

# ---- icon + silhouette sheet (every stick-gag icon and every scale_ruler silhouette), drawn straight from the blocks
sys.path.insert(0, os.path.join(HERE, '..'))
from blocks.common import ICONS
from blocks.scale_ruler import SIL
h = '<html><body style="margin:0;background:#050505"><svg width="1280" height="1120" viewBox="0 0 1280 1120" font-family="Jost,sans-serif">'
for i, n in enumerate(ICONS):
    x = 110 + (i % 7) * 175; y = 90 + (i // 7) * 150
    h += f'<g transform="translate({x},{y}) scale(.62)">{ICONS[n]}</g><text x="{x}" y="{y+78}" fill="#c9a45c" font-size="14" text-anchor="middle" letter-spacing="2">{n.upper()}</text>'
ORDER = ['mammoth', 'bear', 'orca', 'shark', 'leopard_seal', 'crocodile'] + [k for k in SIL if k not in ('mammoth', 'bear', 'orca', 'shark', 'leopard_seal', 'crocodile')]
for i, n in enumerate(ORDER):
    x = 40 + (i % 3) * 420; y = 880 + (i // 3) * 170
    h += f'<g transform="translate({x},{y}) scale(.38)">{SIL[n]}</g><text x="{x+190}" y="{y+26}" fill="#c9a45c" font-size="13" text-anchor="middle" letter-spacing="2">{n.upper()}</text>'
h += '</svg></body></html>'
open(os.path.join(HERE, 'work', 'icons.html'), 'w').write(h)
chrome = [os.path.join(r, f) for r, _, fs in os.walk(os.path.expanduser('~/.cache/hyperframes/chrome')) for f in fs if f == 'chrome-headless-shell']
if chrome:
    subprocess.run([chrome[0], '--no-sandbox', '--screenshot=' + os.path.join(HERE, 'work', 'icons.png'), '--window-size=1280,1120', 'file://' + os.path.join(HERE, 'work', 'icons.html')], check=True, capture_output=True)
    Image.open(os.path.join(HERE, 'work', 'icons.png')).convert('RGB').save(os.path.join(HERE, 'gallery_icons.jpg'), quality=88); print('gallery_icons.jpg')
