#!/usr/bin/env python3
"""Tile thumbnails for the tier boards (gap T11): one still per chapter, c01.jpg ... c10.jpg (c01 = the v9 North Atlantic tile image).
   python3 make_thumbs.py CLIPS_DIR OUT_DIR       (CLIPS_DIR holds the Video 01 clips named like C02-12.mp4)
The frames are the ones suggested in plan/needs.md (T11). Change FRAMES to pick another still. The jpgs are media: do not commit them."""
import os, sys, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = {'c02': ('C02-12.mp4', 2.0), 'c03': ('vidiq_C03-17.mp4', 2.0), 'c04': ('vidiq_H17.mp4', 2.0), 'c05': ('C05-05.mp4', 2.0), 'c06': ('C06-11.mp4', 2.0),
          'c07': ('C07-08.mp4', 2.0), 'c08': ('vidiq_C08-13.mp4', 2.0), 'c09': ('C09-04.mp4', 2.0), 'c10': ('C10-10.mp4', 2.0)}
clips, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
shutil.copy2(os.path.join(HERE, 'lib', 'icy_sea.jpg'), os.path.join(out, 'c01.jpg'))
for k, (f, t) in FRAMES.items():
    src = os.path.join(clips, f)
    if not os.path.exists(src): print('missing', src); continue
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', src, '-frames:v', '1', '-vf', 'scale=480:270:force_original_aspect_ratio=increase,crop=480:270', '-q:v', '3', os.path.join(out, k + '.jpg')], check=True)
print('thumbs ->', out)
