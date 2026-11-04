#!/usr/bin/env python3
"""Writes TEMPLATES.md from the META of every block, so the list of templates and parameters never goes out of date."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blocks import REGISTRY
LETTER = {'number_clip': 'a', 'lower_third': 'b', 'extinct_plate': 'c', 'title_card': 'd', 'stick_timer': 'e', 'stick_rope': 'e', 'stick_water': 'e', 'stick_gag': 'e',
          'scale_ruler': 'f', 'problem_counter': 'g', 'tier_board': 'h', 'map_clip': 'i', 'clip_plain': 'j', 'black': '-', 'stick_land': 'e', 'stick_walk': 'e', 'outro': 'k', 'text_card': 'l'}
out = ['# Template list (made by make_docs.py - do not edit by hand)\n', 'Time values ("at" fields): see README.md, section "Time values".\n']
for n, m in sorted(REGISTRY.items(), key=lambda kv: (LETTER.get(kv[0], 'z'), kv[0])):
    M = m.META
    out.append(f'\n## {n}\n\n{M["about"]}\n\nVariants: ' + ', '.join(f'`{v}`' for v in M['variants']) + '\n')
    if M['params']:
        out.append('\n| parameter | what it does |\n|---|---|')
        for k, v in M['params'].items(): out.append(f'| `{k}` | {v.replace("|", "/")} |')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TEMPLATES.md'), 'w').write('\n'.join(out) + '\n')
print('TEMPLATES.md written')
