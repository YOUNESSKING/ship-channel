#!/usr/bin/env python3
"""Channel version of generate_thumbnail.py: Nano Banana Pro through fal (key in ~/.fal_key), no headshot needed.
Usage: generate_fal.py --prompt "..." --output a.png [--aspect-ratio 16:9] [--resolution 2K] [--reference art.jpg ...]
--reference = edit mode (fal-ai/nano-banana-pro/edit), the images are sent inline as data URIs.
Appends ../brand-style.md to the prompt unless --no-style. Prints the cost-bearing call once; never prints the key."""
import argparse, base64, json, mimetypes, os, subprocess, sys, tempfile
from pathlib import Path
ap = argparse.ArgumentParser()
ap.add_argument('--prompt', required=True); ap.add_argument('--output', required=True)
ap.add_argument('--aspect-ratio', default='16:9', choices=['16:9', '9:16']); ap.add_argument('--resolution', default='2K', choices=['1K', '2K', '4K'])
ap.add_argument('--no-style', action='store_true'); ap.add_argument('--reference', nargs='*', default=[]); a = ap.parse_args()
prompt = a.prompt
style = Path(__file__).resolve().parent.parent / 'brand-style.md'
if not a.no_style and style.exists(): prompt += '\n\nBRAND STYLE GUIDE (follow these rules):\n' + style.read_text().strip()
key = open(os.path.expanduser('~/.fal_key')).read().strip()
req = {'prompt': prompt, 'num_images': 1, 'aspect_ratio': a.aspect_ratio, 'resolution': a.resolution, 'output_format': 'png'}
if a.reference: req['image_urls'] = ['data:%s;base64,%s' % (mimetypes.guess_type(f)[0] or 'image/jpeg', base64.b64encode(open(f, 'rb').read()).decode()) for f in a.reference]
with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as tf: json.dump(req, tf)
ep = 'https://fal.run/fal-ai/nano-banana-pro' + ('/edit' if a.reference else '')
r = subprocess.run(['curl', '-s', '-m', '300', ep, '-H', 'Authorization: Key ' + key, '-H', 'Content-Type: application/json', '-d', '@' + tf.name], capture_output=True, text=True)
os.unlink(tf.name)
try: url = json.loads(r.stdout)['images'][0]['url']
except Exception: print('Error: no image returned:', r.stdout[:300], file=sys.stderr); sys.exit(1)
Path(a.output).parent.mkdir(parents=True, exist_ok=True)
subprocess.run(['curl', '-s', '-m', '120', '-o', a.output, url], check=True); print('saved', a.output)
