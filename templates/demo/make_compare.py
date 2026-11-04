#!/usr/bin/env python3
"""Side-by-side stills: v9 (left) vs the template build (right).
   python3 make_compare.py WORK_DIR V9_VIDEO OFFSET OUT_DIR  name:v9_time:label ...
   Template frames come from `hyperframes snapshot`, or from a rendered draft if DEMO_VIDEO is set (demo time = v9 time - OFFSET)."""
import sys, os, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont
work, v9, off, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
items = [a.split(':', 2) for a in sys.argv[5:]]
os.makedirs(out, exist_ok=True); tmp = os.path.join(out, '_tmp'); os.makedirs(tmp, exist_ok=True)
times = ','.join(f'{float(t) - off:.3f}' for _, t, _ in items)
RENDER = os.environ.get('DEMO_VIDEO')      # a rendered draft of the template build: frames are cut from it (the real thing)
if not RENDER: subprocess.run(['npx', '-y', 'hyperframes@0.8.188', 'snapshot', work, '--at', times, '--no-end', '--keep', '-o', tmp], check=True, capture_output=True)
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
except Exception: font = ImageFont.load_default()
for name, t, label in items:
    t = float(t); a = os.path.join(tmp, f'v9_{t}.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{t}', '-i', v9, '-frames:v', '1', a], check=True)
    d = t - off; fn = ('%g' % round(d, 3)).rstrip('0') if False else ('%g' % round(d, 3))
    b = os.path.join(tmp, f'at-{fn}s.png')
    if RENDER: subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{d:.3f}', '-i', RENDER, '-frames:v', '1', b], check=True)
    A = Image.open(a).convert('RGB').resize((960, 540)); B = Image.open(b).convert('RGB').resize((960, 540))
    im = Image.new('RGB', (1920, 600), (12, 12, 12)); im.paste(A, (0, 60)); im.paste(B, (960, 60))
    dr = ImageDraw.Draw(im)
    dr.text((14, 16), f'v9 approved   t={t:.1f}s   {label}', fill=(233, 220, 192), font=font)
    dr.text((974, 16), f'template build   t={d:.1f}s', fill=(201, 164, 92), font=font)
    im.save(os.path.join(out, f'compare_{name}.jpg'), quality=88)
    print('saved', f'compare_{name}.jpg')
shutil.rmtree(tmp)
